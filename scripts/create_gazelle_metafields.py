#!/usr/bin/env python3
"""
Create the Gazelle product metafield definitions in Shopify.

What it does:
  1. Exchanges your BooksoniX Integration app's Client ID + Secret for a
     short-lived Admin API token (client-credentials grant).
  2. Creates each product metafield definition below via metafieldDefinitionCreate.
  3. Reports per-field: created / already-exists / error.

It is safe to re-run: definitions that already exist report "already exists"
and are skipped, nothing is overwritten or deleted.

-------------------------------------------------------------------------------
HOW TO RUN (macOS terminal):

  export GAZELLE_CLIENT_ID='<the client id from Dev Dashboard > Settings>'
  export GAZELLE_CLIENT_SECRET='<the secret from Dev Dashboard > Settings>'
  python3 create_gazelle_metafields.py

(No pip installs needed - uses the Python standard library only.)
-------------------------------------------------------------------------------
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

SHOP = os.environ.get("GAZELLE_SHOP", "gazelle-books-2026")
API_VERSION = "2026-07"
CLIENT_ID = os.environ.get("GAZELLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GAZELLE_CLIENT_SECRET")

# ---------------------------------------------------------------------------
# The definitions to create.  (key, type, human-readable name)
# Types are deliberately text now so they ADOPT Dave's current output cleanly.
# The 5 already created manually (publication_date, isbn, author, publisher,
# language) are intentionally NOT listed here.
# Keys listed in SMART_COLLECTION_KEYS additionally get the
# smartCollectionCondition capability (same input shape as custom.thema_top in
# create_gazelle_collections.py) so they can drive smart-collection rules.
# ---------------------------------------------------------------------------
DEFINITIONS = [
    ("subtitle",            "single_line_text_field", "Subtitle"),
    ("series",              "single_line_text_field", "Series"),
    ("series_number",       "single_line_text_field", "Number in Series"),
    ("pages",               "single_line_text_field", "Pages"),
    ("height_mm",           "single_line_text_field", "Height (mm)"),
    ("width_mm",            "single_line_text_field", "Width (mm)"),
    ("depth_mm",            "single_line_text_field", "Depth (mm)"),
    ("illustrations",       "single_line_text_field", "Illustrations"),
    ("author_bio",          "multi_line_text_field",  "Author Biography"),
    ("thema_subjects",      "single_line_text_field", "Thema Subjects"),
    ("bic_subjects",        "single_line_text_field", "BIC Subjects"),
    ("bisac_subjects",      "single_line_text_field", "BISAC Subjects"),
    ("main_subjects",       "single_line_text_field", "Main Subjects"),
    ("keywords",            "single_line_text_field", "Keywords"),
    ("audience",            "single_line_text_field", "Audience"),
    ("prize_achievements",  "multi_line_text_field",  "Prize Achievements"),
    ("tags_global",         "single_line_text_field", "Tags (global)"),
    ("reviews",             "multi_line_text_field",  "Reviews"),
    ("pubcode",             "single_line_text_field", "PUBCODE"),
]

# Definitions that must be usable as a smart-collection condition.
# Smart-collection metafield rules support ONLY "is equal to", and the
# capability cannot be added retrospectively in the admin UI.
SMART_COLLECTION_KEYS = {"pubcode"}

NAMESPACE = "custom"
OWNER_TYPE = "PRODUCT"

MUTATION = """
mutation CreateDef($definition: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition { id namespace key type { name } }
    userErrors { field message code }
  }
}
"""


def die(msg):
    print(f"\nERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def get_token():
    if not CLIENT_ID or not CLIENT_SECRET:
        die("Set GAZELLE_CLIENT_ID and GAZELLE_CLIENT_SECRET env vars first "
            "(see the header of this file).")
    url = f"https://{SHOP}.myshopify.com/admin/oauth/access_token"
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
        die(f"Token request failed ({e.code}): {e.read().decode()}")
    token = data.get("access_token")
    if not token:
        die(f"No access_token in response: {data}")
    print(f"Got token (scopes: {data.get('scope', 'unknown')})\n")
    return token


def graphql(token, query, variables):
    url = f"https://{SHOP}.myshopify.com/admin/api/{API_VERSION}/graphql.json"
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("X-Shopify-Access-Token", token)
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print(f"DRY RUN — no writes will be made.\n")
        print(f"Target shop : https://{SHOP}.myshopify.com")
        print(f"API version : {API_VERSION}")
        print(f"Namespace   : {NAMESPACE}   Owner: {OWNER_TYPE}")
        print(f"\nWould create {len(DEFINITIONS)} definitions:\n")
        for key, mtype, name in DEFINITIONS:
            cap = "  + smartCollectionCondition" if key in SMART_COLLECTION_KEYS else ""
            print(f"  {NAMESPACE}.{key:<20} {mtype:<24} \"{name}\"{cap}")
        print(f"\nRe-run without --dry-run to create these.")
        return

    token = get_token()

    created, skipped, failed = 0, 0, 0
    for key, mtype, name in DEFINITIONS:
        definition = {
            "name": name,
            "namespace": NAMESPACE,
            "key": key,
            "type": mtype,
            "ownerType": OWNER_TYPE,
        }
        if key in SMART_COLLECTION_KEYS:
            definition["capabilities"] = {
                "smartCollectionCondition": {"enabled": True}
            }
        variables = {"definition": definition}
        try:
            resp = graphql(token, MUTATION, variables)
        except urllib.error.HTTPError as e:
            print(f"  x  custom.{key:<20} HTTP {e.code}: {e.read().decode()[:200]}")
            failed += 1
            continue

        if "errors" in resp:
            print(f"  x  custom.{key:<20} GraphQL error: {resp['errors']}")
            failed += 1
            continue

        result = resp["data"]["metafieldDefinitionCreate"]
        errs = result["userErrors"]
        if errs:
            msg = "; ".join(f"{e['message']} ({e.get('code')})" for e in errs)
            if any(e.get("code") == "TAKEN" for e in errs):
                print(f"  =  custom.{key:<20} already exists, skipped")
                skipped += 1
            else:
                print(f"  x  custom.{key:<20} {msg}")
                failed += 1
        else:
            print(f"  +  custom.{key:<20} created ({mtype})")
            created += 1

    print(f"\nDone. created={created}  already-existed={skipped}  failed={failed}")
    if failed:
        print("Any failures above are usually a scope issue (needs write_products) "
              "or a type-string typo. Paste the message to Claude if unsure.")


if __name__ == "__main__":
    main()
