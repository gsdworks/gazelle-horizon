#!/usr/bin/env python3
"""
create_gazelle_collections.py
Creates the four merchandise smart collections from gazelle-collections-spec.md
via the Shopify Admin GraphQL API, then publishes them to the Online Store channel.

Auth (Dev Dashboard app, post-Jan-2026 flow — client credentials grant):
  export SHOPIFY_STORE="gazelle-books-2026.myshopify.com"
  export GAZELLE_CLIENT_ID="..."       # from the Dev Dashboard app's credentials
  export GAZELLE_CLIENT_SECRET="..."   # ditto
App must be installed on the store with write_products + write_publications scopes.

Run:  python3 create_gazelle_collections.py
Idempotent: skips any collection whose handle already exists.
"""
import os, sys, json, requests

STORE = os.environ.get("SHOPIFY_STORE", "gazelle-books-2026.myshopify.com")
CLIENT_ID = os.environ.get("GAZELLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GAZELLE_CLIENT_SECRET")
API_VERSION = "2026-07"
URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

_TOKEN = None

def get_token():
    """Exchange client credentials for a short-lived Admin API access token.

    Acquired LAZILY, on the first API call, so that --dry-run runs offline and
    needs no credentials at all. Nothing below reaches the store until a real
    query is made.
    """
    global _TOKEN
    if _TOKEN:
        return _TOKEN
    if not (CLIENT_ID and CLIENT_SECRET):
        sys.exit("Set GAZELLE_CLIENT_ID and GAZELLE_CLIENT_SECRET first (Dev Dashboard app credentials).")
    r = requests.post(f"https://{STORE}/admin/oauth/access_token",
                      json={"grant_type": "client_credentials",
                            "client_id": CLIENT_ID,
                            "client_secret": CLIENT_SECRET})
    if r.status_code != 200:
        sys.exit(f"Token exchange failed ({r.status_code}): {r.text}\n"
                 "Check the app is installed on the store and credentials are correct.")
    _TOKEN = r.json()["access_token"]
    print("Token acquired OK.")
    return _TOKEN

def gql(query, variables=None):
    r = requests.post(URL, headers={"X-Shopify-Access-Token": get_token(),
                                    "Content-Type": "application/json"},
                      json={"query": query, "variables": variables or {}})
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        sys.exit(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data["data"]

# Stale test collections to remove (verified 11 Aug: compare-at price experiments
# and dead tag-based collections with 0 products). All Books + Home page kept.
DELETE_HANDLES = [
    "business-management",
    "biography-autobiography",
    "bestsellers",
    "cookery",
    "childrens",
    "biography-memoir",
]

# The four collections from the spec. disjunctive=True means OR across rules.
COLLECTIONS = [
    {
        "title": "Posters & Wallcharts",
        "handle": "posters-wallcharts",
        "types": ["Poster", "Wallchart"],
    },
    {
        "title": "Music & Audio",
        "handle": "music-audio",
        "types": ["CD", "Audio", "DVD", "Other audio format"],
    },
    {
        "title": "Cards & Stationery",
        "handle": "cards-stationery",
        "types": ["Cards", "Postcard book or pack", "Diary or journal",
                  "Calendar", "Address book"],
    },
    {
        "title": "Maps",
        "handle": "maps",
        "types": ["Sheet map", "Fold-out book or chart"],
    },
]

EXISTING_Q = """
query($q: String!) {
  collections(first: 1, query: $q) { nodes { id handle } }
}"""

CREATE_M = """
mutation($input: CollectionInput!) {
  collectionCreate(input: $input) {
    collection { id title handle ruleSet { rules { column relation condition } } }
    userErrors { field message }
  }
}"""

PUBLICATIONS_Q = """
query { publications(first: 10) { nodes { id name } } }"""

PUBLISH_M = """
mutation($id: ID!, $input: [PublicationInput!]!) {
  publishablePublish(id: $id, input: $input) {
    userErrors { field message }
  }
}"""

# Subject collections (Thema top-level). Rules bind to the custom.thema_top
# metafield definition, created below with the smart-collection capability.
# Labels are the 11 Aug proposal — retitle after Billy's call if needed.
SUBJECT_COLLECTIONS = [
    ("A", "The Arts", "arts"),
    ("C", "Language & Linguistics", "language-linguistics"),
    ("D", "Literature & Literary Studies", "literature-literary-studies"),
    ("F", "Fiction", "fiction"),
    ("G", "Reference & Interdisciplinary", "reference-interdisciplinary"),
    ("J", "Society & Social Sciences", "society-social-sciences"),
    ("K", "Economics, Finance & Business", "economics-finance-business"),
    ("L", "Law", "law"),
    ("M", "Medicine & Nursing", "medicine-nursing"),
    ("N", "History & Archaeology", "history-archaeology"),
    ("P", "Mathematics & Science", "mathematics-science"),
    ("Q", "Philosophy & Religion", "philosophy-religion"),
    ("R", "Earth Sciences & Environment", "earth-sciences-environment"),
    ("S", "Sport & Leisure", "sport-leisure"),
    ("T", "Technology & Engineering", "technology-engineering"),
    ("U", "Computing & IT", "computing-it"),
    ("V", "Health & Personal Development", "health-personal-development"),
    ("W", "Lifestyle, Hobbies & Leisure", "lifestyle-hobbies-leisure"),
    ("X", "Graphic Novels & Comics", "graphic-novels-comics"),
    ("Y", "Children's & Young Adult", "childrens-young-adult"),
]

DEF_Q = """
query {
  metafieldDefinitions(first: 1, ownerType: PRODUCT,
                       namespace: "custom", key: "thema_top") {
    nodes { id name }
  }
}"""

DEF_CREATE_M = """
mutation($definition: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $definition) {
    createdDefinition { id }
    userErrors { field message }
  }
}"""

def ensure_thema_top_definition():
    nodes = gql(DEF_Q)["metafieldDefinitions"]["nodes"]
    if nodes:
        print(f"DEF   custom.thema_top exists ({nodes[0]['id']})")
        return nodes[0]["id"]
    d = {
        "name": "Thema Top-Level Subjects",
        "namespace": "custom",
        "key": "thema_top",
        "type": "list.single_line_text_field",
        "ownerType": "PRODUCT",
        "capabilities": {"smartCollectionCondition": {"enabled": True}},
    }
    res = gql(DEF_CREATE_M, {"definition": d})["metafieldDefinitionCreate"]
    if res["userErrors"]:
        sys.exit(f"Definition create failed: {res['userErrors']}")
    did = res["createdDefinition"]["id"]
    print(f"DEF   custom.thema_top created ({did})")
    return did

DELETE_M = """
mutation($input: CollectionDeleteInput!) {
  collectionDelete(input: $input) {
    deletedCollectionId
    userErrors { field message }
  }
}"""

def delete_stale():
    deleted, missing = 0, 0
    for h in DELETE_HANDLES:
        nodes = gql(EXISTING_Q, {"q": f"handle:{h}"})["collections"]["nodes"]
        if not nodes:
            print(f"GONE  {h} (not found, nothing to delete)")
            missing += 1
            continue
        res = gql(DELETE_M, {"input": {"id": nodes[0]["id"]}})["collectionDelete"]
        if res["userErrors"]:
            print(f"FAIL  delete {h}: {res['userErrors']}")
        else:
            print(f"DEL   {h}")
            deleted += 1
    print(f"deleted={deleted} already_gone={missing}\n")

# ---------------------------------------------------------------------------
# LEVEL-2 SUB-COLLECTIONS (19 Aug) - run with --l2
#
# 124 second-level subject collections under the existing top-level ones,
# keyed on custom.thema_l2, built with exactly the derive-then-equals pattern
# that built the top level: smart-collection metafield rules support ONLY
# "is equal to", so the matchable value has to be derived and stored first.
#
#   python3 create_gazelle_collections.py --l2 --dry-run
#   python3 create_gazelle_collections.py --l2
#   python3 create_gazelle_collections.py --l2 --counts /path/to/thema_l2_counts.csv
#
# The counts CSV is the SOURCE OF TRUTH for which codes get a collection
# (every row where keep == True). It is not re-derived here. Default is the
# 19 Aug file; populate_thema_top.py writes a fresh one to scripts/out/ on
# every run as the recurring check, but that one does not drive creation
# unless it is passed explicitly.
# ---------------------------------------------------------------------------
import csv, re as _re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COUNTS = os.path.expanduser("~/Downloads/thema_l2_counts.csv")
LABELS_PATH = os.path.join(HERE, "thema_labels_en_v1.6.json")

# --- Handle and title curation ---------------------------------------------
# Handles are PERMANENT URLs, so they are hand-written, not derived from the
# EDItEUR heading (which produces things like
# childrens-young-adult-children-s-picture-books-activity-books-early-learning-concepts).
# Rule: <parent-short>-<child-slug>, under 40 chars, URL-safe, unique.
# validate_handles() enforces all three BEFORE any collection is created.
#
# PARENT_SHORT is a fixed map, deliberately NOT derived from the parent
# collection handle - the parent handle can be renamed without moving every
# child URL.
PARENT_SHORT = {
    "A": "arts",     "C": "language",   "D": "literature", "F": "fiction",
    "G": "reference","J": "society",    "K": "business",   "L": "law",
    "M": "medicine", "N": "history",    "P": "science",    "Q": "philosophy",
    "R": "environment", "S": "sport",   "T": "technology", "U": "computing",
    "V": "health",   "W": "lifestyle",  "X": "comics",     "Y": "childrens",
}

# Child slug per L2 code. Short curated noun phrases, not EDItEUR headings.
# A code missing here falls back to the heading truncated at the first
# comma/colon/slash and slugified - see child_slug().
HANDLE_OVERRIDES = {
    # A - The Arts
    "AG": "fine-decorative-arts", "AJ": "photography", "AK": "design-illustration",
    "AT": "performing-arts", "AM": "architecture", "AV": "music",
    "AF": "art-forms", "AB": "general",
    # C - Language
    "CJ": "teaching-learning", "CF": "linguistics", "CB": "reference",
    # D - Literature
    "DN": "biography", "DC": "poetry", "DS": "history-criticism",
    "DD": "plays-drama", "DB": "classical-texts",
    # F - Fiction
    "FB": "literary", "FJ": "adventure", "FY": "special-features",
    "FV": "historical", "FH": "thriller", "FX": "narrative-themes",
    "FM": "fantasy", "FF": "crime", "FL": "science-fiction", "FR": "romance",
    "FS": "family-life", "FK": "horror", "FU": "humour",
    "FN": "traditional-tales", "FW": "religious", "FT": "family-saga",
    "FD": "speculative",
    # G - Reference
    "GT": "interdisciplinary", "GB": "encyclopaedias", "GL": "library-museum",
    "GP": "research-methods",
    # J - Society
    "JB": "culture", "JP": "politics", "JN": "education", "JM": "psychology",
    "JH": "sociology-anthropology", "JW": "warfare", "JK": "social-welfare",
    # K - Business
    "KC": "economics", "KJ": "management", "KN": "industry",
    "KF": "finance-accounting",
    # L - Law
    "LN": "jurisdictions", "LA": "jurisprudence", "LB": "international",
    # M - Medicine
    "MB": "general", "MJ": "clinical", "MK": "specialties",
    "MF": "basic-sciences", "MN": "surgery", "MQ": "nursing",
    "MX": "complementary", "MR": "study-guides", "MZ": "veterinary",
    # N - History
    "NH": "general", "NK": "archaeology",
    # P - Science
    "PS": "biology", "PH": "physics", "PN": "chemistry", "PB": "mathematics",
    "PD": "general", "PG": "astronomy",
    # Q - Philosophy & Religion
    "QR": "religion", "QD": "general",
    # R - Environment
    "RN": "general", "RB": "earth-sciences", "RG": "geography",
    "RP": "regional-planning",
    # S - Sport
    "SF": "ball-sports", "SC": "general", "SZ": "outdoor-pursuits",
    "SR": "combat-sports", "SV": "field-sports", "ST": "winter-sports",
    "SP": "water-sports",
    # T - Technology
    "TQ": "environmental", "TH": "energy", "TG": "mechanical",
    "TD": "industrial-chemistry", "TV": "agriculture", "TB": "general",
    "TJ": "electronics", "TT": "applied-sciences", "TC": "biochemical",
    "TN": "civil-building", "TR": "transport",
    # U - Computing
    "UY": "computer-science", "UM": "programming", "UN": "databases",
    "UB": "general", "UD": "digital-lifestyle", "UR": "security",
    "UT": "networking", "UF": "business-applications",
    # V - Health
    "VX": "mind-body-spirit", "VF": "family-health", "VS": "self-help",
    # W - Lifestyle
    "WN": "nature", "WT": "travel", "WD": "hobbies-games", "WB": "cookery",
    "WG": "transport", "WM": "gardening", "WQ": "local-family-history",
    "WZ": "stationery-gifts", "WF": "crafts", "WC": "antiques-collectables",
    "WH": "humour", "WK": "home-diy", "WJ": "personal-style",
    # X - Comics
    "XA": "manga-styles", "XQ": "genres",
    # Y - Children's
    "YN": "general-interest", "YF": "fiction", "YB": "picture-books",
    "YP": "educational", "YX": "personal-social", "YD": "poetry",
}

# Starting titles where the EDItEUR heading reads as a codelist entry rather
# than a shop label. Billy renames later; matching is on HANDLE, never title,
# so a retitle in admin does not cause a re-run to create duplicates.
TITLE_OVERRIDES = {
    # Slash-separated or "and"-style headings normalised to the "&" house
    # style used by the rest of this map.
    "DN": "Biography & non-fiction", "DB": "Ancient & classical texts",
    "FH": "Thrillers & suspense", "FW": "Religious & spiritual fiction",
    "GB": "Encyclopaedias & reference", "JP": "Politics & government",
    "JH": "Sociology & anthropology", "MJ": "Clinical & internal medicine",
    "QR": "Religion & beliefs", "SR": "Combat sports & self-defence",
    "TV": "Agriculture & farming", "WC": "Antiques & collectables",
    "AG": "Fine & decorative arts", "AJ": "Photography",
    "AK": "Design & illustration", "AF": "Art forms", "AB": "The arts: general",
    "CB": "Language reference", "CJ": "Language teaching & learning",
    "DC": "Poetry", "DS": "Literary history & criticism", "DD": "Plays & drama",
    "FB": "Literary fiction", "FY": "Fiction: special features",
    "FX": "Fiction: narrative themes", "FF": "Crime & mystery fiction",
    "FJ": "Adventure & action fiction", "FS": "Family life fiction",
    "FK": "Horror & supernatural fiction", "FT": "Family saga fiction",
    "FN": "Traditional tales & retellings",
    "GL": "Library & information sciences", "GP": "Research & information",
    "JB": "Society & culture", "JN": "Education",
    "JK": "Social welfare & criminology",
    "KJ": "Business & management", "KN": "Industry & industrial studies",
    "KF": "Finance & accounting",
    "LN": "Laws by jurisdiction & area", "LA": "Jurisprudence",
    "MB": "Medicine: general", "MK": "Medical specialties",
    "MF": "Pre-clinical medicine", "MQ": "Nursing",
    "MX": "Complementary medicine", "MR": "Medical study guides",
    "PS": "Biology & life sciences", "PD": "Science: general",
    "PG": "Astronomy & space",
    "RP": "Regional & area planning",
    "SF": "Ball sports", "SZ": "Outdoor pursuits", "SV": "Field sports",
    "ST": "Winter sports", "SP": "Water sports",
    "TQ": "Environmental technology", "TH": "Energy technology",
    "TG": "Mechanical engineering",
    "TD": "Industrial chemistry & manufacturing", "TB": "Technology: general",
    "TJ": "Electronics & communications", "TT": "Applied sciences",
    "TN": "Civil engineering & building", "TR": "Transport technology",
    "UM": "Programming & software engineering",
    "UN": "Databases & data management", "UB": "IT: general",
    "UD": "Digital lifestyle guides", "UT": "Networking & communications",
    "VF": "Family & health", "VS": "Self-help & personal development",
    "WN": "Nature & the natural world", "WT": "Travel & holidays",
    "WD": "Hobbies, quizzes & games", "WB": "Cookery, food & drink",
    "WG": "Transport", "WQ": "Local & family history",
    "WZ": "Stationery & gifts", "WF": "Crafts & handicrafts",
    "WK": "Home maintenance & DIY", "WJ": "Personal style guides",
    "XA": "Manga & comic styles", "XQ": "Comics by genre",
    "YN": "Children's: general interest",
    "YB": "Children's: picture & activity books",
    "YF": "Children's & teenage fiction",
    "YX": "Children's: personal & social topics",
    "YD": "Children's poetry & anthologies",
}

MAX_HANDLE_LEN = 40

COLLECTION_Q = """
query($q: String!) {
  collections(first: 1, query: $q) { nodes { id handle title sortOrder } }
}"""

DEF_ANY_Q = """
query($ownerType: MetafieldOwnerType!, $key: String!) {
  metafieldDefinitions(first: 1, ownerType: $ownerType,
                       namespace: "custom", key: $key) {
    nodes { id name }
  }
}"""

def ensure_definition(key, name, mtype, owner_type, smart_collection=False):
    """Create a custom.<key> definition if absent. Returns its id."""
    nodes = gql(DEF_ANY_Q, {"ownerType": owner_type, "key": key})["metafieldDefinitions"]["nodes"]
    if nodes:
        print(f"DEF   custom.{key} exists ({nodes[0]['id']})")
        return nodes[0]["id"]
    d = {"name": name, "namespace": "custom", "key": key,
         "type": mtype, "ownerType": owner_type}
    if smart_collection:
        # Cannot be added retrospectively in the admin UI - it has to be set
        # at create time or the definition is useless for collection rules.
        d["capabilities"] = {"smartCollectionCondition": {"enabled": True}}
    res = gql(DEF_CREATE_M, {"definition": d})["metafieldDefinitionCreate"]
    if res["userErrors"]:
        sys.exit(f"Definition create failed for custom.{key}: {res['userErrors']}")
    did = res["createdDefinition"]["id"]
    print(f"DEF   custom.{key} created ({did})")
    return did

def slugify(s):
    s = s.lower().replace("&", " and ")
    s = _re.sub(r"[^a-z0-9]+", "-", s)
    return _re.sub(r"-+", "-", s).strip("-")

def title_for(code, labels):
    """Starting title: curated override, else the EDItEUR heading, else code."""
    return TITLE_OVERRIDES.get(code) or labels.get(code) or code

def child_slug(code, labels):
    """Curated slug, else the heading truncated at the first , : or / ."""
    if code in HANDLE_OVERRIDES:
        return HANDLE_OVERRIDES[code]
    heading = labels.get(code, code)
    return slugify(_re.split(r"[,:/]", heading)[0])

def handle_for(code, letter, labels):
    return f"{PARENT_SHORT[letter]}-{child_slug(code, labels)}"

def validate_handles(plan):
    """Fail loudly BEFORE any write. plan = [(code, letter, title, handle, n)]."""
    problems = []
    seen = {}
    for code, letter, _title, handle, _n in plan:
        if len(handle) >= MAX_HANDLE_LEN:
            problems.append(f"{code}: handle is {len(handle)} chars (limit {MAX_HANDLE_LEN}): {handle}")
        if not _re.fullmatch(r"[a-z0-9-]+", handle):
            problems.append(f"{code}: handle is not URL-safe: {handle}")
        if handle in seen:
            problems.append(f"{code}: handle collides with {seen[handle]}: {handle}")
        seen[handle] = code
    if problems:
        print("\nHANDLE VALIDATION FAILED - nothing was created:")
        for p in problems:
            print("  " + p)
        sys.exit(1)

def load_labels():
    with open(LABELS_PATH, encoding="utf-8") as f:
        return json.load(f)["labels"]

def load_kept(counts_path):
    with open(counts_path, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    kept = [r for r in rows if str(r.get("keep", "")).strip().lower() == "true"]
    print(f"counts CSV: {counts_path}")
    print(f"  {len(rows)} L2 groups, {len(kept)} kept (keep == True)")
    return kept

def parent_map():
    """letter -> the top-level collection as it exists IN THE STORE.

    Handles come from SUBJECT_COLLECTIONS above; everything else (id, title,
    sortOrder) is read from the store, so a Billy retitle does not break this.
    """
    out = {}
    for letter, _title, handle in SUBJECT_COLLECTIONS:
        nodes = gql(COLLECTION_Q, {"q": f"handle:{handle}"})["collections"]["nodes"]
        if nodes:
            out[letter] = nodes[0]
    return out

def build_l2():
    argv = sys.argv
    dry = "--dry-run" in argv
    counts_path = DEFAULT_COUNTS
    if "--counts" in argv:
        counts_path = argv[argv.index("--counts") + 1]
    if not os.path.exists(counts_path):
        sys.exit(f"Counts CSV not found: {counts_path}")

    labels = load_labels()
    kept = load_kept(counts_path)

    unknown_parents = sorted({r["top"] for r in kept} - set(PARENT_SHORT))
    if unknown_parents:
        sys.exit(f"STOP: kept rows use top-level letters absent from "
                 f"PARENT_SHORT: {unknown_parents}")

    no_curated = [r["l2"] for r in kept if r["l2"] not in HANDLE_OVERRIDES]
    if no_curated:
        print(f"NOTE: {len(no_curated)} codes have no curated slug, falling "
              f"back to the truncated heading: {no_curated}")
    no_label = [r["l2"] for r in kept if r["l2"] not in labels]
    if no_label:
        print(f"NOTE: {len(no_label)} codes have no Thema heading: {no_label}")

    plan = [(r["l2"], r["top"], title_for(r["l2"], labels),
             handle_for(r["l2"], r["top"], labels), int(r["products"]))
            for r in kept]
    validate_handles(plan)
    longest = max(plan, key=lambda x: len(x[3]))
    print(f"handles OK: {len(plan)} unique, all URL-safe, all < {MAX_HANDLE_LEN} "
          f"chars (longest {len(longest[3])}: {longest[3]})")

    if dry:
        # Offline - no token, no API calls.
        print("\nDRY RUN - no writes, no API calls.\n")
        print(f"  {'CODE':<5} {'TITLE':<38} {'HANDLE':<40} {'PRODUCTS':>8}")
        print("  " + "-" * 93)
        for code, letter, title, handle, n in sorted(plan, key=lambda x: (x[1], -x[4])):
            print(f"  {code:<5} {title[:38]:<38} {handle:<40} {n:>8}")
        print(f"\n{len(plan)} collections would be created.")
        print("Re-run without --dry-run to create them.")
        return

    def_id = ensure_definition("thema_l2", "Thema Level-2 Subjects",
                               "list.single_line_text_field", "PRODUCT",
                               smart_collection=True)
    ensure_definition("parent_handle", "Parent Collection Handle",
                      "single_line_text_field", "COLLECTION")

    parents = parent_map()
    print(f"top-level collections found in store: {len(parents)} "
          f"({''.join(sorted(parents))})")
    orphan = sorted({r["top"] for r in kept} - set(parents))
    if orphan:
        sys.exit(f"STOP: kept L2 codes reference top-level letters with no "
                 f"collection in the store: {orphan}. Create those first.")

    pubs = gql(PUBLICATIONS_Q)["publications"]["nodes"]
    online = next((p for p in pubs if p["name"] == "Online Store"), None)
    if not online:
        sys.exit(f"Online Store publication not found. Publications: {[p['name'] for p in pubs]}")

    created, skipped, failed = 0, 0, 0
    for code, letter, title, handle, _n in plan:
        parent = parents[letter]
        existing = gql(EXISTING_Q, {"q": f"handle:{handle}"})["collections"]["nodes"]
        if existing:
            print(f"SKIP  {code:<3} {title[:36]:<38} (handle exists)")
            skipped += 1
            continue

        inp = {
            "title": title,
            "handle": handle,
            "sortOrder": parent["sortOrder"],
            "ruleSet": {"appliedDisjunctively": False, "rules": [{
                "column": "PRODUCT_METAFIELD_DEFINITION",
                "relation": "EQUALS",
                "condition": code,
                "conditionObjectId": def_id,
            }]},
            "metafields": [{
                "namespace": "custom",
                "key": "parent_handle",
                "type": "single_line_text_field",
                "value": parent["handle"],
            }],
        }
        res = gql(CREATE_M, {"input": inp})["collectionCreate"]
        if res["userErrors"]:
            print(f"FAIL  {code:<3} {title[:36]:<38} {res['userErrors']}")
            failed += 1
            continue
        pub = gql(PUBLISH_M, {"id": res["collection"]["id"],
                              "input": [{"publicationId": online["id"]}]})
        errs = pub["publishablePublish"]["userErrors"]
        note = f" (publish errors: {errs})" if errs else ""
        print(f"OK    {code:<3} {title[:36]:<38} -> {handle}{note}")
        created += 1

    print(f"\nL2 done. created={created} skipped={skipped} failed={failed}")
    print("Verify in admin: Products > Collections. Compare a sample of product "
          "counts against the products column in the counts CSV.")

def main():
    if "--l2" in sys.argv:
        build_l2()
        return
    delete_stale()
    def_id = ensure_thema_top_definition()
    # Find the Online Store publication once
    pubs = gql(PUBLICATIONS_Q)["publications"]["nodes"]
    online = next((p for p in pubs if p["name"] == "Online Store"), None)
    if not online:
        sys.exit(f"Online Store publication not found. Publications: {[p['name'] for p in pubs]}")

    created, skipped, failed = 0, 0, 0
    for c in COLLECTIONS:
        existing = gql(EXISTING_Q, {"q": f"handle:{c['handle']}"})["collections"]["nodes"]
        if existing:
            print(f"SKIP  {c['title']} (handle exists: {existing[0]['handle']})")
            skipped += 1
            continue

        rules = [{"column": "TYPE", "relation": "EQUALS", "condition": t}
                 for t in c["types"]]
        inp = {
            "title": c["title"],
            "handle": c["handle"],
            "ruleSet": {"appliedDisjunctively": True, "rules": rules},
        }
        res = gql(CREATE_M, {"input": inp})["collectionCreate"]
        if res["userErrors"]:
            print(f"FAIL  {c['title']}: {res['userErrors']}")
            failed += 1
            continue

        coll_id = res["collection"]["id"]
        pub = gql(PUBLISH_M, {"id": coll_id,
                              "input": [{"publicationId": online["id"]}]})
        errs = pub["publishablePublish"]["userErrors"]
        note = f" (publish errors: {errs})" if errs else ""
        print(f"OK    {c['title']} -> {res['collection']['handle']}{note}")
        created += 1

    # Subject collections against the thema_top definition
    for letter, title, handle in SUBJECT_COLLECTIONS:
        existing = gql(EXISTING_Q, {"q": f"handle:{handle}"})["collections"]["nodes"]
        if existing:
            print(f"SKIP  {title} (handle exists)")
            skipped += 1
            continue
        inp = {
            "title": title,
            "handle": handle,
            "ruleSet": {"appliedDisjunctively": False, "rules": [{
                "column": "PRODUCT_METAFIELD_DEFINITION",
                "relation": "EQUALS",
                "condition": letter,
                "conditionObjectId": def_id,
            }]},
        }
        res = gql(CREATE_M, {"input": inp})["collectionCreate"]
        if res["userErrors"]:
            print(f"FAIL  {title}: {res['userErrors']}")
            failed += 1
            continue
        coll_id = res["collection"]["id"]
        pub = gql(PUBLISH_M, {"id": coll_id,
                              "input": [{"publicationId": online["id"]}]})
        errs = pub["publishablePublish"]["userErrors"]
        note = f" (publish errors: {errs})" if errs else ""
        print(f"OK    {title} -> {handle}{note}")
        created += 1

    print(f"\ncreated={created} skipped={skipped} failed={failed}")
    print("Verify in admin: Products > Collections. Product counts should be roughly:")
    print("  Posters & Wallcharts ~244 | Music & Audio ~210 | Cards & Stationery ~33 | Maps ~26")

if __name__ == "__main__":
    main()
