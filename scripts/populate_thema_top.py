#!/usr/bin/env python3
"""
populate_thema_top.py
Computes each product's Thema subject codes from a folder of Shopify product
export CSVs and writes TWO metafields via metafieldsSet:

  custom.thema_top  - unique FIRST characters of each valid Thema code   (A-Y)
  custom.thema_l2   - unique FIRST TWO characters of each valid code     (e.g. JB)

Both are list.single_line_text_field and both exist for the same reason:
smart-collection metafield conditions support ONLY "is equal to", so the value
you want to match has to be derived and stored. thema_top drives the 18
top-level subject collections; thema_l2 drives the level-2 sub-collections.

Usage:
  export SHOPIFY_STORE="gazelle-books-2026.myshopify.com"
  export GAZELLE_CLIENT_ID="..."
  export GAZELLE_CLIENT_SECRET="..."
  python3 populate_thema_top.py /path/to/export/csv/folder          # dry-run: first 10 only
  python3 populate_thema_top.py /path/to/export/csv/folder --full   # everything

Safe to re-run: metafieldsSet overwrites in place. Rate-limit aware.

At the end of every run it writes scripts/out/thema_l2_counts.csv (columns
top,l2,products,keep,parent_total at threshold 24, same format as
scripts/thema_l2_counts.py). That is the recurring maintenance check: every
backfill prints the L2 group sizes for free, so a group crossing the threshold
is visible without a separate analysis pass.
"""
import os, sys, re, json, glob, time
import requests
import pandas as pd

STORE = os.environ.get("SHOPIFY_STORE", "gazelle-books-2026.myshopify.com")
CLIENT_ID = os.environ.get("GAZELLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GAZELLE_CLIENT_SECRET")
API_VERSION = "2026-07"
URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"

# Threshold for the keep flag in the counts CSV. Matches scripts/thema_l2_counts.py.
L2_THRESHOLD = 24

# metafieldsSet accepts at most 25 metafields per call. Two metafields per
# product means 12 products per batch (24 entries), NOT the 25 products used
# when only thema_top was written. Raising this silently truncates the write.
PRODUCTS_PER_BATCH = 12

if not (CLIENT_ID and CLIENT_SECRET):
    sys.exit("Set GAZELLE_CLIENT_ID and GAZELLE_CLIENT_SECRET first.")
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

# ---- 1. Compute handle -> (top-level letters, level-2 codes) from the export ----
files = sorted(glob.glob(os.path.join(CSV_DIR, "products_export_*.csv")))
if not files:
    sys.exit(f"No products_export_*.csv files found in {CSV_DIR}")
print(f"Reading {len(files)} export files...")
dfs = [pd.read_csv(f, dtype=str, low_memory=False) for f in files]
df = pd.concat(dfs, ignore_index=True)
prod = df[df["Title"].notna()]
thema_col = [c for c in prod.columns if c.startswith("Thema Subjects")][0]

# EXPORT INTEGRITY: a partial export is the failure this guards against - the
# 18 Aug export held 32,708 of 50,523 products and looked perfectly healthy.
# Unique Handle count must equal the All Books count in admin before the
# export is trusted. Verified equal on the 19 Aug export (50,523 = 50,523).
rows, handles = len(prod), prod["Handle"].nunique()
print(f"INTEGRITY: {rows} rows with a Title, {handles} unique handles.")
if rows != handles:
    print(f"  NOTE: {rows - handles} duplicate handle rows (multi-row products are normal in Shopify exports).")
print("  >>> Confirm the unique-handle count equals All Books in admin before trusting this run. <<<")
if "Status" in prod.columns:
    status = prod["Status"].str.lower().value_counts().to_dict()
    print(f"STATUS SPLIT: {status}")
    # The counts CSV below is ACTIVE-only (it describes what a storefront
    # collection will hold). The metafield write is NOT status-filtered - an
    # archived product keeps a correct thema_l2, it just does not appear in a
    # collection. After the publisher archive sweep these two figures diverge
    # legitimately; that divergence is not a bug.

# A valid Thema code: a letter followed by up to 5 more letters/digits. This
# drops qualifiers (which start with a digit) and the name-format values still
# sitting on the stale cohort. Codes of 1 character contribute to thema_top
# only - there is no level-2 group to put them in.
CODE = re.compile(r"^[A-Z][A-Z0-9]{0,5}$")

def derive(v):
    """Return (top_levels, l2_codes) - both unique, order preserved."""
    if not isinstance(v, str) or not v.strip():
        return [], []
    tops, l2s = [], []
    for c in [x.strip() for x in v.split(",") if x.strip()]:
        if not CODE.fullmatch(c):
            continue
        if c[0] not in tops:
            tops.append(c[0])
        if len(c) >= 2 and c[:2] not in l2s:
            l2s.append(c[:2])
    return tops, l2s

mapping = {}
for h, v in zip(prod["Handle"], prod[thema_col]):
    tops, l2s = derive(v)
    if tops:
        mapping[h] = (tops, l2s)
with_l2 = sum(1 for t, l in mapping.values() if l)
print(f"{len(mapping)} products with at least one top-level subject "
      f"({with_l2} of them with at least one level-2 code).")

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

# ---- 3. Write both metafields, same call per product, batched ----
SET_M = """
mutation($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { key }
    userErrors { field message }
  }
}"""

work = [(h, tl) for h, tl in mapping.items() if h in gid]
missing = len(mapping) - len(work)
if missing:
    print(f"NOTE: {missing} export handles not found in store (deleted/changed since export).")

if not FULL:
    work = work[:10]
    print("DRY RUN: writing first 10 products only. Re-run with --full for everything.")

batches = [work[i:i + PRODUCTS_PER_BATCH] for i in range(0, len(work), PRODUCTS_PER_BATCH)]
print(f"{len(work)} products -> {len(batches)} batches of <={PRODUCTS_PER_BATCH} "
      f"(<={PRODUCTS_PER_BATCH * 2} metafields, under the 25-per-call cap)")

ok, err = 0, 0
start = time.time()
for i, batch in enumerate(batches):
    metafields = []
    for h, (tops, l2s) in batch:
        metafields.append({
            "ownerId": gid[h], "namespace": "custom", "key": "thema_top",
            "type": "list.single_line_text_field", "value": json.dumps(tops),
        })
        # Skip an empty l2 rather than writing an empty list - a 1-character
        # code has no level-2 group and an empty list is not a useful value.
        if l2s:
            metafields.append({
                "ownerId": gid[h], "namespace": "custom", "key": "thema_l2",
                "type": "list.single_line_text_field", "value": json.dumps(l2s),
            })
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

# ---- 4. Recurring check: write the L2 counts CSV ----
# ACTIVE products only - this describes what a storefront collection will hold.
counts_src = prod
if "Status" in prod.columns:
    counts_src = prod[prod["Status"].str.lower() == "active"]

long_rows = []
for h, v in zip(counts_src["Handle"], counts_src[thema_col].fillna("")):
    tops, l2s = derive(v)
    for c in l2s:
        long_rows.append((h, c[0], c))
long = pd.DataFrame(long_rows, columns=["handle", "top", "l2"]).drop_duplicates()
top_counts = long.drop_duplicates(["handle", "top"]).groupby("top").size()
l2_counts = long.groupby(["top", "l2"]).size().rename("products").reset_index()
l2_counts["keep"] = l2_counts["products"] >= L2_THRESHOLD
l2_counts["parent_total"] = l2_counts["top"].map(top_counts)
l2_counts = l2_counts.sort_values(["parent_total", "top", "products"],
                                  ascending=[False, True, False])

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "thema_l2_counts.csv")
l2_counts.to_csv(out_path, index=False)
kept = l2_counts[l2_counts.keep]
print(f"\nL2 groups: {len(l2_counts)}   kept (>= {L2_THRESHOLD}): {len(kept)}   "
      f"dropped: {len(l2_counts) - len(kept)}")
print("kept per parent:", kept.groupby("top").size().to_dict())
print(f"wrote {out_path}")
print("If the kept set differs from the collections that exist, create or drop "
      "the difference by hand - this script does not touch collections.")

if not FULL:
    print("\nDry run complete. Check one of the 10 in admin (product page > Metafields),")
    print("confirm BOTH thema_top and thema_l2 show values, then re-run with --full.")
