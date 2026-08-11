#!/usr/bin/env python3
"""
Recreate 3 Gazelle product metafield definitions as single_line_text_field.

Why: Dave's BooksoniX push declares every metafield as single_line_text_field.
Three definitions were created as multi_line_text_field on 7 July 2026 and are
blocking his writes.  Shopify cannot change a definition's type in place, so
each must be DELETED (keeping its values) and RECREATED as single line.

  custom.prize_achievements   multi_line -> single_line   (~7 values)
  custom.reviews              multi_line -> single_line   (~104 values)
  custom.author_bio           multi_line -> single_line   (~229 values)

THE ONE RULE THAT MATTERS
  metafieldDefinitionDelete is ALWAYS called with
  deleteAllAssociatedMetafields: false
  If that is ever true, the stored values are destroyed with no undo.
  It is hardcoded below, printed in dry-run output, and asserted in code
  immediately before the mutation fires.

-------------------------------------------------------------------------------
HOW TO RUN (macOS terminal, from the repo root):

  export GAZELLE_CLIENT_ID='...'
  export GAZELLE_CLIENT_SECRET='...'

  # Step 0 - back up all values for the three keys (READ-ONLY on Shopify;
  #          writes outputs/metafield_backup_<date>.json locally).  Commit it.
  python3 update_gazelle_metafield_types.py --backup

  # Dry run (this is the DEFAULT - no flag needed, and no writes are possible)
  python3 update_gazelle_metafield_types.py
  python3 update_gazelle_metafield_types.py --dry-run

  # Canary only (7 values), still a dry run
  python3 update_gazelle_metafield_types.py --only prize_achievements

  # The real thing - requires the explicit --execute flag AND an existing backup
  python3 update_gazelle_metafield_types.py --execute --only prize_achievements
  python3 update_gazelle_metafield_types.py --execute

(No pip installs needed - uses the Python standard library only.)
-------------------------------------------------------------------------------
"""

import datetime
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

SHOP = os.environ.get("GAZELLE_SHOP", "gazelle-books-2026")
API_VERSION = "2026-07"
CLIENT_ID = os.environ.get("GAZELLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GAZELLE_CLIENT_SECRET")

NAMESPACE = "custom"
OWNER_TYPE = "PRODUCT"
NEW_TYPE = "single_line_text_field"
OLD_TYPE = "multi_line_text_field"

# ---------------------------------------------------------------------------
# NEVER change this.  True destroys every stored value with no undo.
# ---------------------------------------------------------------------------
DELETE_ALL_ASSOCIATED_METAFIELDS = False

# Blast-radius ordering: smallest first, so the canary fails cheap.
# (key, backup alias, expected value count from the live export - a sanity
#  reference only; the live definition count fetched in step 1 is authoritative)
FIELDS = [
    ("prize_achievements", "prz", 7),
    ("reviews",            "rev", 104),
    ("author_bio",         "bio", 229),
]

TODAY = datetime.date.today().isoformat()
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
BACKUP_PATH = os.path.join(OUTPUT_DIR, "metafield_backup_%s.json" % TODAY)
LOG_PATH = os.path.join(OUTPUT_DIR, "metafield_type_fix_%s.log" % TODAY)

# ---------------------------------------------------------------------------
# GraphQL
# ---------------------------------------------------------------------------

BACKUP_QUERY = """
query Backup($cursor: String) {
  products(first: 250, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id
      legacyResourceId
      bio: metafield(namespace: "custom", key: "author_bio") { value }
      rev: metafield(namespace: "custom", key: "reviews") { value }
      prz: metafield(namespace: "custom", key: "prize_achievements") { value }
    }
  }
}
"""

GET_DEF_QUERY = """
query GetDef($ns: String!, $key: String!) {
  metafieldDefinitions(first: 1, ownerType: PRODUCT, namespace: $ns, key: $key) {
    nodes {
      id
      name
      description
      namespace
      key
      type { name }
      pinnedPosition
      access { admin storefront }
      metafieldsCount
    }
  }
}
"""

DELETE_DEF_MUTATION = """
mutation DeleteDef($id: ID!, $deleteAll: Boolean!) {
  metafieldDefinitionDelete(id: $id, deleteAllAssociatedMetafields: $deleteAll) {
    deletedDefinitionId
    userErrors { field message code }
  }
}
"""

CREATE_DEF_MUTATION = """
mutation CreateDef($def: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $def) {
    createdDefinition { id name namespace key type { name } metafieldsCount }
    userErrors { field message code }
  }
}
"""

# ---------------------------------------------------------------------------
# Plumbing
# ---------------------------------------------------------------------------

_log_fh = None


def log(msg, echo=True):
    """Print to stdout and append to the run log."""
    if echo:
        print(msg)
    if _log_fh:
        _log_fh.write("[%s] %s\n" % (datetime.datetime.now().isoformat(timespec="seconds"), msg))
        _log_fh.flush()


def log_verbatim(label, obj):
    """Log a response body verbatim (spec: every mutation response logged verbatim)."""
    body = json.dumps(obj, indent=2, sort_keys=True)
    if _log_fh:
        _log_fh.write("[%s] %s (verbatim):\n%s\n" % (
            datetime.datetime.now().isoformat(timespec="seconds"), label, body))
        _log_fh.flush()
    print("    %s: %s" % (label, json.dumps(obj, sort_keys=True)))


def open_log():
    global _log_fh
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    _log_fh = open(LOG_PATH, "a", encoding="utf-8")
    _log_fh.write("\n%s\n" % ("=" * 78))
    log("run start: argv=%s shop=%s api=%s" % (sys.argv[1:], SHOP, API_VERSION), echo=False)


def die(msg):
    log("ABORT: %s" % msg, echo=False)
    print("\nERROR: %s" % msg, file=sys.stderr)
    sys.exit(1)


def guard_delete_flag():
    """THE ONE RULE. An explicit check, not an assert - `python3 -O` strips
    asserts, and this guard must survive that."""
    if DELETE_ALL_ASSOCIATED_METAFIELDS is not False:
        die("REFUSING TO RUN: deleteAllAssociatedMetafields must be False. "
            "True destroys all stored values with no undo.")


def _token_error(msg, soft):
    """Fail hard normally; in soft mode (dry run) warn and return None."""
    if soft:
        print("\nWARNING: %s" % msg, file=sys.stderr)
        log("token unavailable (soft): %s" % msg, echo=False)
        return None
    die(msg)


def get_token(soft=False):
    """Client-credentials grant - same flow as create_gazelle_metafields.py.

    soft=True is used by the dry run only: a missing/bad credential warns and
    returns None so the offline part of the dry run can still be shown.
    """
    if not CLIENT_ID or not CLIENT_SECRET or CLIENT_ID.strip(". ") == "":
        return _token_error(
            "GAZELLE_CLIENT_ID / GAZELLE_CLIENT_SECRET are not set to real "
            "credentials (see the header of this file). Use the BooksoniX "
            "Integration app in the Gazelle Dev org.", soft)
    url = "https://%s.myshopify.com/admin/oauth/access_token" % SHOP
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        # The oauth endpoint answers with a full HTML error page; pull the gist.
        gist = detail
        marker = "Oauth error"
        if marker in detail:
            start = detail.index(marker)
            gist = detail[start:start + 200].split("<")[0].strip()
        return _token_error("Token request failed (%s): %s" % (e.code, gist[:400]), soft)
    except urllib.error.URLError as e:
        return _token_error("Token request failed (network): %s" % e.reason, soft)
    token = data.get("access_token")
    if not token:
        return _token_error("No access_token in response: %s" % data, soft)
    log("Got token (scopes: %s)" % data.get("scope", "unknown"))
    return token


def graphql(token, query, variables):
    url = "https://%s.myshopify.com/admin/api/%s/graphql.json" % (SHOP, API_VERSION)
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Shopify-Access-Token", token)
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        die("HTTP %s from Admin API: %s" % (e.code, e.read().decode()[:1000]))


# ---------------------------------------------------------------------------
# Step 0 - backup (read-only against Shopify)
# ---------------------------------------------------------------------------

def run_backup(token):
    log("\nStep 0 - BACKUP (read-only; nothing in Shopify is modified)")
    log("  Paginating products, 250 per page...")

    records = []
    counts = {key: 0 for key, _alias, _exp in FIELDS}
    cursor = None
    pages = 0
    scanned = 0

    while True:
        resp = graphql(token, BACKUP_QUERY, {"cursor": cursor})
        if "errors" in resp:
            die("Backup query returned GraphQL errors: %s" % resp["errors"])
        conn = resp["data"]["products"]
        pages += 1
        for node in conn["nodes"]:
            scanned += 1
            entry = {"id": node["id"], "legacyResourceId": node["legacyResourceId"]}
            hit = False
            for key, alias, _exp in FIELDS:
                mf = node.get(alias)
                if mf and mf.get("value") is not None:
                    entry[key] = mf["value"]
                    counts[key] += 1
                    hit = True
            if hit:
                records.append(entry)
        info = conn["pageInfo"]
        log("  page %-3d  products scanned=%-6d  products with data=%d"
            % (pages, scanned, len(records)))
        if not info["hasNextPage"]:
            break
        cursor = info["endCursor"]

    newline_hits = {key: 0 for key, _a, _e in FIELDS}
    for rec in records:
        for key, _alias, _exp in FIELDS:
            val = rec.get(key)
            if val is not None and ("\n" in val or "\r" in val):
                newline_hits[key] += 1

    payload = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "shop": "%s.myshopify.com" % SHOP,
        "api_version": API_VERSION,
        "namespace": NAMESPACE,
        "owner_type": OWNER_TYPE,
        "purpose": ("Pre-change backup of values for the three definitions being "
                    "recreated as %s" % NEW_TYPE),
        "keys": [key for key, _a, _e in FIELDS],
        "products_scanned": scanned,
        "products_with_any_value": len(records),
        "value_counts": counts,
        "values_containing_newline": newline_hits,
        "products": records,
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(BACKUP_PATH, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    log("\n  Backup written: %s" % BACKUP_PATH)
    log("  products scanned            : %d" % scanned)
    log("  products with >=1 of the 3   : %d" % len(records))
    log("\n  Backed-up value counts (expected from the live export in brackets):")
    for key, _alias, expected in FIELDS:
        flag = "OK " if counts[key] == expected else "!! "
        log("    %s%s.%-20s %4d   (expected %d)" % (flag, NAMESPACE, key, counts[key], expected))
    log("\n  Values containing a newline (must be 0 for a clean single-line move):")
    for key, _alias, _exp in FIELDS:
        flag = "OK " if newline_hits[key] == 0 else "!! "
        log("    %s%s.%-20s %4d" % (flag, NAMESPACE, key, newline_hits[key]))

    return counts


def latest_backup_file():
    if not os.path.isdir(OUTPUT_DIR):
        return None
    names = sorted(n for n in os.listdir(OUTPUT_DIR)
                   if n.startswith("metafield_backup_") and n.endswith(".json"))
    return os.path.join(OUTPUT_DIR, names[-1]) if names else None


def backup_counts_from_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data.get("value_counts", {})


# ---------------------------------------------------------------------------
# Step 1 - read the existing definition
# ---------------------------------------------------------------------------

def read_definition(token, key):
    resp = graphql(token, GET_DEF_QUERY, {"ns": NAMESPACE, "key": key})
    if "errors" in resp:
        die("GetDef(%s) returned GraphQL errors: %s" % (key, resp["errors"]))
    nodes = resp["data"]["metafieldDefinitions"]["nodes"]
    return nodes[0] if nodes else None


# ---------------------------------------------------------------------------
# Steps 2-4 - delete, recreate, verify
# ---------------------------------------------------------------------------

def process_field(token, key, expected, backup_counts):
    log("\n" + "-" * 78)
    log("FIELD %s.%s" % (NAMESPACE, key))
    log("-" * 78)

    # --- Step 1 -------------------------------------------------------------
    definition = read_definition(token, key)
    if definition is None:
        die("No definition found for %s.%s - nothing to do, and this is not "
            "the expected state. Stopping." % (NAMESPACE, key))

    log_verbatim("step 1 definition", definition)

    def_id = definition["id"]
    name = definition["name"]
    description = definition.get("description")
    pinned_position = definition.get("pinnedPosition")
    access = definition.get("access") or {}
    storefront_access = access.get("storefront")
    admin_access = access.get("admin")
    baseline_count = definition["metafieldsCount"]
    current_type = definition["type"]["name"]

    log("  id              : %s" % def_id)
    log("  name            : %s" % name)
    log("  current type    : %s" % current_type)
    log("  metafieldsCount : %s   (backup file recorded %s, export expected %s)"
        % (baseline_count, backup_counts.get(key, "n/a"), expected))
    log("  pinnedPosition  : %s  -> pin=%s" % (pinned_position, pinned_position is not None))
    log("  access          : storefront=%s admin=%s" % (storefront_access, admin_access))

    if current_type == NEW_TYPE:
        die("%s.%s is ALREADY %s. Nothing to change - stopping rather than "
            "deleting and recreating a correct definition." % (NAMESPACE, key, NEW_TYPE))
    if current_type != OLD_TYPE:
        die("%s.%s is type '%s', expected '%s'. Stopping - the store does not "
            "match the spec." % (NAMESPACE, key, current_type, OLD_TYPE))

    if backup_counts.get(key) != baseline_count:
        die("Backup/live count mismatch for %s.%s: backup=%s live=%s. "
            "The live count is authoritative and the backup is incomplete. "
            "STOPPING before any delete." % (NAMESPACE, key,
                                             backup_counts.get(key), baseline_count))

    # --- Step 2 -------------------------------------------------------------
    guard_delete_flag()
    log("\n  Step 2 - delete definition with deleteAllAssociatedMetafields: false")
    resp = graphql(token, DELETE_DEF_MUTATION,
                   {"id": def_id, "deleteAll": DELETE_ALL_ASSOCIATED_METAFIELDS})
    log_verbatim("step 2 metafieldDefinitionDelete response", resp)
    if "errors" in resp:
        die("Delete returned GraphQL errors for %s: %s" % (key, resp["errors"]))
    result = resp["data"]["metafieldDefinitionDelete"]
    if result["userErrors"]:
        die("Delete userErrors for %s: %s" % (key, result["userErrors"]))
    log("  deleted: %s" % result["deletedDefinitionId"])

    # --- Step 3 -------------------------------------------------------------
    log("\n  Step 3 - recreate as %s" % NEW_TYPE)
    definition_input = {
        "name": name,
        "namespace": NAMESPACE,
        "key": key,
        "ownerType": OWNER_TYPE,
        "type": NEW_TYPE,
        "pin": pinned_position is not None,
    }
    if description:
        definition_input["description"] = description
    access_input = {}
    if storefront_access:
        access_input["storefront"] = storefront_access
    if admin_access:
        access_input["admin"] = admin_access
    if access_input:
        definition_input["access"] = access_input

    resp = graphql(token, CREATE_DEF_MUTATION, {"def": definition_input})
    log_verbatim("step 3 metafieldDefinitionCreate response", resp)

    def create_failed(r):
        if "errors" in r:
            return True
        res = r["data"]["metafieldDefinitionCreate"]
        return bool(res["userErrors"])

    if create_failed(resp) and "admin" in access_input:
        log("  create rejected; retrying with access.admin OMITTED "
            "(falls back to the API default; storefront access preserved)")
        retry_input = dict(definition_input)
        retry_access = {k: v for k, v in access_input.items() if k != "admin"}
        if retry_access:
            retry_input["access"] = retry_access
        else:
            retry_input.pop("access", None)
        resp = graphql(token, CREATE_DEF_MUTATION, {"def": retry_input})
        log_verbatim("step 3 retry (admin omitted) response", resp)

    if "errors" in resp:
        die("Recreate returned GraphQL errors for %s: %s\n"
            "The definition is DELETED but values are intact (see backup). "
            "Recreate it manually as %s before doing anything else."
            % (key, resp["errors"], NEW_TYPE))
    result = resp["data"]["metafieldDefinitionCreate"]
    if result["userErrors"]:
        die("Recreate userErrors for %s: %s\n"
            "The definition is DELETED but values are intact (see backup). "
            "Recreate it manually as %s before doing anything else."
            % (key, result["userErrors"], NEW_TYPE))
    log("  recreated: %s" % json.dumps(result["createdDefinition"], sort_keys=True))

    # --- Step 4 -------------------------------------------------------------
    log("\n  Step 4 - verify")
    for attempt in range(1, 4):
        check = read_definition(token, key)
        log_verbatim("step 4 verify attempt %d" % attempt, check)
        if check is None:
            die("Verification could not find %s.%s after recreate. STOP." % (NAMESPACE, key))

        checks = {
            "type is %s" % NEW_TYPE: check["type"]["name"] == NEW_TYPE,
            "metafieldsCount == %s" % baseline_count: check["metafieldsCount"] == baseline_count,
            "access.storefront == %s" % storefront_access:
                (check.get("access") or {}).get("storefront") == storefront_access,
            "namespace == %s" % NAMESPACE: check["namespace"] == NAMESPACE,
            "key == %s" % key: check["key"] == key,
        }
        for label, ok in checks.items():
            log("    %s %s" % ("PASS" if ok else "FAIL", label))

        if all(checks.values()):
            log("  VERIFIED %s.%s" % (NAMESPACE, key))
            return

        count_only = (all(v for k, v in checks.items() if not k.startswith("metafieldsCount"))
                      and check["metafieldsCount"] != baseline_count)
        if count_only and attempt < 3:
            log("    metafieldsCount reads %s vs baseline %s - may be lagging. "
                "Waiting 30s and re-querying (attempt %d of 3)."
                % (check["metafieldsCount"], baseline_count, attempt + 1))
            time.sleep(30)
            continue
        die("Verification FAILED for %s.%s after attempt %d. STOP - the next "
            "field will NOT be touched. Values are in the backup."
            % (NAMESPACE, key, attempt))


# ---------------------------------------------------------------------------
# Dry run
# ---------------------------------------------------------------------------

def print_dry_run(fields, token):
    print("\n" + "=" * 78)
    print("DRY RUN - no writes will be made. Re-run with --execute to write.")
    print("=" * 78)
    print("Target shop  : https://%s.myshopify.com" % SHOP)
    print("API version  : %s" % API_VERSION)
    print("Namespace    : %s   Owner: %s" % (NAMESPACE, OWNER_TYPE))
    print("Backup file  : %s" % (latest_backup_file() or "NONE FOUND - run --backup first"))
    print("Log file     : %s" % LOG_PATH)
    print("\nDeletes will be called with:  deleteAllAssociatedMetafields: false")
    print("(hardcoded, asserted in code before the mutation fires - stored values are kept)")

    print("\nFields to recreate, in blast-radius order:\n")
    print("  #  %-28s %-22s -> %-22s %s" % ("field", "current type", "new type", "values"))
    for idx, (key, _alias, expected) in enumerate(fields, 1):
        print("  %d  %-28s %-22s -> %-22s ~%d"
              % (idx, "%s.%s" % (NAMESPACE, key), OLD_TYPE, NEW_TYPE, expected))

    if not token:
        print("\nLive definition state: SKIPPED - no usable API credentials, so the")
        print("current types/counts/access above could not be confirmed against the")
        print("store. The 'values' column is the export figure, not a live read.")
    else:
        print("\nLive definition state (read-only):\n")
        backup_counts = backup_counts_from_file(latest_backup_file()) if latest_backup_file() else {}
        for key, _alias, expected in fields:
            d = read_definition(token, key)
            if d is None:
                print("  %s.%-22s NOT FOUND" % (NAMESPACE, key))
                continue
            acc = d.get("access") or {}
            bk = backup_counts.get(key, "n/a")
            match = "match" if bk == d["metafieldsCount"] else "MISMATCH"
            print("  %s.%-22s type=%-22s count=%-4s  backup=%-4s (%s)"
                  % (NAMESPACE, key, d["type"]["name"], d["metafieldsCount"], bk, match))
            print("      %-24s id=%s" % ('name="%s"' % d["name"], d["id"]))
            print("      pinnedPosition=%-5s -> pin=%-5s  access: storefront=%s admin=%s"
                  % (d.get("pinnedPosition"), d.get("pinnedPosition") is not None,
                     acc.get("storefront"), acc.get("admin")))
            print("      would recreate as: type=%s name=\"%s\" pin=%s "
                  "access.storefront=%s access.admin=%s"
                  % (NEW_TYPE, d["name"], d.get("pinnedPosition") is not None,
                     acc.get("storefront"), acc.get("admin")))

    print("\nPer field the run would: read def -> delete "
          "(deleteAllAssociatedMetafields: false) -> recreate as %s -> verify "
          "(type, count, storefront access, ns/key)." % NEW_TYPE)
    print("Any failure or count mismatch stops the run; later fields are not touched.")
    print("\nNothing else is touched: no other definitions, no metafield values, "
          "no products.\n")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def usage():
    print(__doc__)
    sys.exit(2)


def main():
    argv = sys.argv[1:]
    known = {"--backup", "--dry-run", "--execute", "--only", "-h", "--help"}
    for arg in argv:
        if arg.startswith("-") and arg not in known:
            print("Unknown flag: %s" % arg, file=sys.stderr)
            usage()
    if "-h" in argv or "--help" in argv:
        usage()

    do_backup = "--backup" in argv
    execute = "--execute" in argv

    only = None
    if "--only" in argv:
        i = argv.index("--only")
        if i + 1 >= len(argv):
            die("--only needs a key, e.g. --only prize_achievements")
        only = argv[i + 1]
        valid = [k for k, _a, _e in FIELDS]
        if only not in valid:
            die("--only %s is not one of: %s" % (only, ", ".join(valid)))

    fields = [f for f in FIELDS if only is None or f[0] == only]

    open_log()

    if do_backup:
        token = get_token()
        run_backup(token)
        print("\nBackup complete. Commit %s before running --execute.\n"
              % os.path.relpath(BACKUP_PATH))
        if not execute:
            return
    else:
        token = None

    if not execute:
        # Dry run is the DEFAULT. A live read is used to show real state; it
        # writes nothing. Without usable credentials it still prints the plan.
        if token is None:
            token = get_token(soft=True)
        print_dry_run(fields, token)
        return

    # ---------------- execute path ----------------
    backup_file = latest_backup_file()
    if not backup_file:
        die("No backup found in %s. Run --backup first and commit it; "
            "step 0 is mandatory before any delete." % OUTPUT_DIR)
    backup_counts = backup_counts_from_file(backup_file)

    guard_delete_flag()

    log("\n" + "=" * 78)
    log("EXECUTE - writes WILL be made to %s.myshopify.com" % SHOP)
    log("=" * 78)
    log("Backup in use : %s" % backup_file)
    log("Backup counts : %s" % json.dumps(backup_counts, sort_keys=True))
    log("Delete flag   : deleteAllAssociatedMetafields: false")
    log("Fields        : %s" % ", ".join("%s.%s" % (NAMESPACE, k) for k, _a, _e in fields))
    log("Log file      : %s" % LOG_PATH)

    if token is None:
        token = get_token()

    for key, _alias, expected in fields:
        process_field(token, key, expected, backup_counts)

    log("\n" + "=" * 78)
    log("DONE - %d field(s) recreated as %s and verified."
        % (len(fields), NEW_TYPE))
    log("=" * 78)


if __name__ == "__main__":
    try:
        main()
    finally:
        if _log_fh:
            _log_fh.close()
