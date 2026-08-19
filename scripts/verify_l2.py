#!/usr/bin/env python3
"""
verify_l2.py - the five post-run checks for the Thema level-2 sub-collections.

READ ONLY. Makes no writes of any kind.

  export SHOPIFY_STORE="gazelle-books-2026.myshopify.com"
  export GAZELLE_CLIENT_ID="..."      # GSD Gazelle Scripts app
  export GAZELLE_CLIENT_SECRET="..."
  python3 scripts/verify_l2.py ~/Downloads/export-19aug

Argument is the export folder (used to sample products and to cross-check the
stored metafields against the source Thema codes). Optional:
  --counts <path>   counts CSV to compare against (default scripts/out/...)

MUST run under the GSD Gazelle Scripts app. The BooksoniX Integration app is
Dave's and lacks write_publications; our scripts never run under it.
"""
import os, sys, re, csv, json, glob, random
import requests
import pandas as pd

STORE = os.environ.get("SHOPIFY_STORE", "gazelle-books-2026.myshopify.com")
CLIENT_ID = os.environ.get("GAZELLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GAZELLE_CLIENT_SECRET")
API_VERSION = "2026-07"
URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COUNTS = os.path.join(HERE, "out", "thema_l2_counts.csv")
EXPECTED_TOTAL = 150  # 20 top-level + 124 L2 + 4 merch + All Books + Home page

if len(sys.argv) < 2:
    sys.exit("Usage: verify_l2.py <export csv folder> [--counts <path>]")
CSV_DIR = sys.argv[1]
COUNTS = sys.argv[sys.argv.index("--counts") + 1] if "--counts" in sys.argv else DEFAULT_COUNTS

_TOKEN = None
def token():
    global _TOKEN
    if _TOKEN:
        return _TOKEN
    if not (CLIENT_ID and CLIENT_SECRET):
        sys.exit("Set GAZELLE_CLIENT_ID and GAZELLE_CLIENT_SECRET first.")
    if CLIENT_ID == "5e994c135911baa59f413b9ac8d79992":
        sys.exit("REFUSING TO RUN: that is the BooksoniX Integration app (Dave's). "
                 "Use the GSD Gazelle Scripts credentials.")
    r = requests.post(f"https://{STORE}/admin/oauth/access_token",
                      json={"grant_type": "client_credentials",
                            "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
    if r.status_code != 200:
        sys.exit(f"Token exchange failed ({r.status_code}): {r.text[:300]}")
    _TOKEN = r.json()["access_token"]
    return _TOKEN

def gql(query, variables=None):
    r = requests.post(URL, headers={"X-Shopify-Access-Token": token(),
                                    "Content-Type": "application/json"},
                      json={"query": query, "variables": variables or {}})
    r.raise_for_status()
    d = r.json()
    if "errors" in d:
        sys.exit(f"GraphQL errors: {json.dumps(d['errors'], indent=2)[:600]}")
    return d["data"]

CODE = re.compile(r"^[A-Z][A-Z0-9]{0,5}$")
def derive(v):
    tops, l2s = [], []
    if isinstance(v, str):
        for c in [x.strip() for x in v.split(",") if x.strip()]:
            if not CODE.fullmatch(c):
                continue
            if c[0] not in tops:
                tops.append(c[0])
            if len(c) >= 2 and c[:2] not in l2s:
                l2s.append(c[:2])
    return tops, l2s

PRODUCT_Q = """
query($q: String!) {
  products(first: 1, query: $q) {
    nodes {
      handle title
      subjects: metafield(namespace: "custom", key: "thema_subjects") { value }
      top:      metafield(namespace: "custom", key: "thema_top") { value }
      l2:       metafield(namespace: "custom", key: "thema_l2") { value }
    }
  }
}"""

COLLECTIONS_Q = """
query($cursor: String) {
  collections(first: 100, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      id handle title
      productsCount { count }
      parent: metafield(namespace: "custom", key: "parent_handle") { value }
      ruleSet { rules { column relation condition } }
    }
  }
}"""

def all_collections():
    out, cursor = [], None
    while True:
        d = gql(COLLECTIONS_Q, {"cursor": cursor})["collections"]
        out += d["nodes"]
        if not d["pageInfo"]["hasNextPage"]:
            return out
        cursor = d["pageInfo"]["endCursor"]

def main():
    random.seed(19)  # reproducible sampling
    print(f"store: {STORE}   api: {API_VERSION}")
    print(f"counts CSV: {COUNTS}\n")

    files = sorted(glob.glob(os.path.join(CSV_DIR, "products_export_*.csv")))
    if not files:
        sys.exit(f"No products_export_*.csv in {CSV_DIR}")
    df = pd.concat([pd.read_csv(f, dtype=str, low_memory=False) for f in files],
                   ignore_index=True)
    prod = df[df["Title"].notna()]
    tcol = [c for c in prod.columns if c.startswith("Thema Subjects")][0]

    # ---- CHECK 1: 5 sampled products, stored vs derived-from-source ----
    print("=" * 72)
    print("CHECK 1  five sampled products: thema_top / thema_l2 vs thema_subjects")
    print("=" * 72)
    pool = [(h, v) for h, v in zip(prod["Handle"], prod[tcol].fillna("")) if derive(v)[1]]
    sample = random.sample(pool, 5)
    c1_ok = True
    for h, v in sample:
        want_top, want_l2 = derive(v)
        nodes = gql(PRODUCT_Q, {"q": f"handle:{h}"})["products"]["nodes"]
        if not nodes:
            print(f"  MISSING in store: {h}")
            c1_ok = False
            continue
        n = nodes[0]
        got_top = json.loads(n["top"]["value"]) if n["top"] else []
        got_l2 = json.loads(n["l2"]["value"]) if n["l2"] else []
        ok = sorted(got_top) == sorted(want_top) and sorted(got_l2) == sorted(want_l2)
        c1_ok &= ok
        print(f"  {'PASS' if ok else 'FAIL'}  {h[:40]}")
        print(f"        source   : {(n['subjects']['value'] if n['subjects'] else '')[:60]}")
        print(f"        thema_top: stored {got_top} / expected {want_top}")
        print(f"        thema_l2 : stored {got_l2} / expected {want_l2}")
    print(f"\n  CHECK 1: {'PASS' if c1_ok else 'FAIL'}\n")

    # ---- CHECK 2: exact collection count ----
    cols = all_collections()
    l2s = [c for c in cols if c["parent"]]
    smart = [c for c in cols if c["ruleSet"]]
    print("=" * 72)
    print("CHECK 2  exact collection count")
    print("=" * 72)
    print(f"  total collections in store : {len(cols)}   (expected {EXPECTED_TOTAL})")
    print(f"  with custom.parent_handle  : {len(l2s)}   (expected 124)")
    print(f"  smart (rule-based)         : {len(smart)}")
    print(f"\n  CHECK 2: {'PASS' if len(cols) == EXPECTED_TOTAL and len(l2s) == 124 else 'FAIL'}\n")

    # ---- CHECK 3: 10 sampled L2 collections vs the counts CSV ----
    print("=" * 72)
    print("CHECK 3  ten sampled L2 collections: store count vs counts CSV")
    print("=" * 72)
    csv_counts = {r["l2"]: int(r["products"])
                  for r in csv.DictReader(open(COUNTS, encoding="utf-8-sig"))}
    by_code = {}
    for c in l2s:
        code = next((r["condition"] for r in c["ruleSet"]["rules"]), None) if c["ruleSet"] else None
        if code:
            by_code[code] = c
    c3_ok = True
    for code in random.sample(sorted(by_code), min(10, len(by_code))):
        c = by_code[code]
        store_n, csv_n = c["productsCount"]["count"], csv_counts.get(code, 0)
        gap = abs(store_n - csv_n) / csv_n * 100 if csv_n else 0
        flag = "  <-- GAP > 1%" if gap > 1 else ""
        if gap > 1:
            c3_ok = False
        print(f"  {code:<3} {c['handle']:<38} store {store_n:>5}  csv {csv_n:>5}  "
              f"{gap:5.2f}%{flag}")
    print(f"\n  CHECK 3: {'PASS' if c3_ok else 'REVIEW'}\n")

    # ---- CHECK 4: parent N sanity ----
    print("=" * 72)
    print("CHECK 4  parent N sanity: NH + NK vs the History parent total")
    print("=" * 72)
    # "history-archaeology" is the TOP-LEVEL N collection handle (per
    # SUBJECT_COLLECTIONS) - which is exactly why NK's original child slug
    # collided with it and had to become history-archaeology-studies.
    hist = next((c for c in cols if c["handle"] == "history-archaeology"), None)
    nh = by_code.get("NH"); nk = by_code.get("NK")
    if nh and nk and hist:
        s = nh["productsCount"]["count"] + nk["productsCount"]["count"]
        p = hist["productsCount"]["count"]
        print(f"  NH {nh['productsCount']['count']} + NK {nk['productsCount']['count']} "
              f"= {s}   parent total {p}   ratio {s / p * 100:.1f}%")
        print("  Children may overlap (a product with two codes counts in both), so the")
        print("  sum can exceed the parent slightly. A sum far BELOW the parent means")
        print("  products carry only a 1-character code and have no L2 home.")
        print(f"\n  CHECK 4: {'PASS' if s >= p * 0.9 else 'REVIEW'}\n")
    else:
        print("  Could not resolve NH / NK / History parent - check handles.\n")

    # ---- CHECK 5: parent_handle resolves ----
    print("=" * 72)
    print("CHECK 5  every L2 collection has custom.parent_handle and it resolves")
    print("=" * 72)
    handles = {c["handle"] for c in cols}
    unset = [c["handle"] for c in l2s if not c["parent"]]
    dangling = [(c["handle"], c["parent"]["value"]) for c in l2s
                if c["parent"] and c["parent"]["value"] not in handles]
    print(f"  L2 collections            : {len(l2s)}")
    print(f"  with parent_handle unset  : {len(unset)} {unset[:5]}")
    print(f"  parent_handle not resolving: {len(dangling)} {dangling[:5]}")
    print(f"\n  CHECK 5: {'PASS' if not unset and not dangling else 'FAIL'}\n")

if __name__ == "__main__":
    main()
