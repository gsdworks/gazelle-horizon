#!/usr/bin/env python3
"""
create_gazelle_collections.py
Creates the four merchandise smart collections from gazelle-collections-spec.md
via the Shopify Admin GraphQL API, then publishes them to the Online Store channel.

Auth (Dev Dashboard app, post-Jan-2026 flow — client credentials grant):
  export SHOPIFY_STORE="gazelle-books-2026.myshopify.com"
  export SHOPIFY_CLIENT_ID="..."       # from the Dev Dashboard app's credentials
  export SHOPIFY_CLIENT_SECRET="..."   # ditto
App must be installed on the store with write_products + write_publications scopes.

Run:  python3 create_gazelle_collections.py
Idempotent: skips any collection whose handle already exists.
"""
import os, sys, json, requests

STORE = os.environ.get("SHOPIFY_STORE", "gazelle-books-2026.myshopify.com")
CLIENT_ID = os.environ.get("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SHOPIFY_CLIENT_SECRET")
API_VERSION = "2026-07"
URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

if not (CLIENT_ID and CLIENT_SECRET):
    sys.exit("Set SHOPIFY_CLIENT_ID and SHOPIFY_CLIENT_SECRET first (Dev Dashboard app credentials).")

def get_token():
    """Exchange client credentials for a short-lived Admin API access token."""
    r = requests.post(f"https://{STORE}/admin/oauth/access_token",
                      json={"grant_type": "client_credentials",
                            "client_id": CLIENT_ID,
                            "client_secret": CLIENT_SECRET})
    if r.status_code != 200:
        sys.exit(f"Token exchange failed ({r.status_code}): {r.text}\n"
                 "Check the app is installed on the store and credentials are correct.")
    return r.json()["access_token"]

TOKEN = get_token()
print("Token acquired OK.")

def gql(query, variables=None):
    r = requests.post(URL, headers={"X-Shopify-Access-Token": TOKEN,
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

def main():
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
