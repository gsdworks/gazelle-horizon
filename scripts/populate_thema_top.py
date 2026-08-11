#!/usr/bin/env python3
"""
populate_thema_top.py
Computes each product's Thema top-level letters (A-Y) from a folder of Shopify
product export CSVs and writes them to custom.thema_top via metafieldsSet.

Usage:
  export SHOPIFY_STORE="gazelle-books-2026.myshopify.com"
  export SHOPIFY_CLIENT_ID="..."
  export SHOPIFY_CLIENT_SECRET="..."
  python3 populate_thema_top.py /path/to/export/csv/folder          # dry-run: first 10 only
  python3 populate_thema_top.py /path/to/export/csv/folder --full   # everything

Safe to re-run: metafieldsSet overwrites in place. Rate-limit aware.
"""
import os, sys, re, json, glob, time
import requests
import pandas as pd

STORE = os.environ.get("SHOPIFY_STORE", "gazelle-books-2026.myshopify.com")
CLIENT_ID = os.environ.get("SHOPIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SHOPIFY_CLIENT_SECRET")
API_VERSION = "2026-07"
URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

if not (CLIENT_ID and CLIENT_SECRET):
    sys.exit("Set SHOPIFY_CLIENT_ID and SHOPIFY_CLIENT_SECRET first.")
if len(sys.argv) < 2:
    sys.exit("Usage: populate_thema_top.py <csv folder> [--full]")

CSV_DIR = sys.argv[1]
FULL = "--full" in sys.argv

def get_token():
    r = requests.post(f"https://{STORE}/admin/oauth/access_token",
                      json={"grant_type": "client_credentials",
                            "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
    if r.status_code != 200:
        sys.exit(f"Token exchange failed ({r.status_code}): {r.text[:300]}")
    return r.json()["access_token"]

TOKEN = get_token()
print("Token acquired OK.")

def gql(query, variables=None, attempt=0):
    r = requests.post(URL, headers={"X-Shopify-Access-Token": TOKEN,
                                    "Content-Type": "application/json"},
                      json={"query": query, "variables": variables or {}})
    if r.status_code == 429 and attempt < 5:
        time.sleep(2 ** attempt)
        return gql(query, variables, attempt + 1)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        # throttled errors come through here on GraphQL too
        if any("THROTTLED" in str(e) for e in data["errors"]) and attempt < 5:
            time.sleep(2 ** attempt)
            return gql(query, variables, attempt + 1)
        sys.exit(f"GraphQL errors: {json.dumps(data['errors'], indent=2)[:500]}")
    return data["data"]

# ---- 1. Compute handle -> top-level letters from the export ----
files = sorted(glob.glob(os.path.join(CSV_DIR, "products_export_*.csv")))
if not files:
    sys.exit(f"No products_export_*.csv files found in {CSV_DIR}")
print(f"Reading {len(files)} export files...")
dfs = [pd.read_csv(f, dtype=str, low_memory=False) for f in files]
df = pd.concat(dfs, ignore_index=True)
prod = df[df["Title"].notna()]
thema_col = [c for c in prod.columns if c.startswith("Thema Subjects")][0]

def top_levels(v):
    if not isinstance(v, str) or not v.strip():
        return []
    parts = [p.strip() for p in re.split(r"[,|]", v) if p.strip()]
    letters = []
    for p in parts:
        if re.fullmatch(r"[A-Z0-9]{1,8}", p) and p[0] in "ABCDFGJKLMNPQRSTUVWXY":
            if p[0] not in letters:
                letters.append(p[0])
    return letters

mapping = {}
for h, v in zip(prod["Handle"], prod[thema_col]):
    tl = top_levels(v)
    if tl:
        mapping[h] = tl
print(f"{len(mapping)} products with at least one top-level subject.")

# ---- 2. Resolve handles -> product GIDs (250 per query page) ----
PRODUCTS_Q = """
query($cursor: String) {
  products(first: 250, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle }
  }
}"""

print("Fetching product IDs...")
gid = {}
cursor = None
while True:
    d = gql(PRODUCTS_Q, {"cursor": cursor})["products"]
    for n in d["nodes"]:
        gid[n["handle"]] = n["id"]
    if not d["pageInfo"]["hasNextPage"]:
        break
    cursor = d["pageInfo"]["endCursor"]
print(f"{len(gid)} products in store.")

# ---- 3. Write metafields in batches of 25 ----
SET_M = """
mutation($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { key }
    userErrors { field message }
  }
}"""

work = [(h, letters) for h, letters in mapping.items() if h in gid]
missing = len(mapping) - len(work)
if missing:
    print(f"NOTE: {missing} export handles not found in store (deleted/changed since export).")

if not FULL:
    work = work[:10]
    print("DRY RUN: writing first 10 products only. Re-run with --full for everything.")

batches = [work[i:i+25] for i in range(0, len(work), 25)]
print(f"{len(work)} products -> {len(batches)} batches of <=25")

ok, err = 0, 0
start = time.time()
for i, batch in enumerate(batches):
    metafields = [{
        "ownerId": gid[h],
        "namespace": "custom",
        "key": "thema_top",
        "type": "list.single_line_text_field",
        "value": json.dumps(letters),
    } for h, letters in batch]
    res = gql(SET_M, {"metafields": metafields})["metafieldsSet"]
    if res["userErrors"]:
        print(f"batch {i}: ERRORS {res['userErrors'][:3]}")
        err += len(res["userErrors"])
    ok += len(batch)
    if i % 40 == 0 and i > 0:
        rate = ok / (time.time() - start)
        eta = (len(work) - ok) / rate / 60
        print(f"  {ok}/{len(work)} written ({rate:.0f}/s, ~{eta:.0f} min left)")
    time.sleep(0.3)  # stay well under throttle

print(f"\nDone: {ok} written, {err} errors, {time.time()-start:.0f}s elapsed.")
if not FULL:
    print("Dry run complete. Check one of the 10 in admin (product page > Metafields),")
    print("confirm thema_top shows letters, then re-run with --full.")
