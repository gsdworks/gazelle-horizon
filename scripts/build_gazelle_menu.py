#!/usr/bin/env python3
"""
build_gazelle_menu.py
Builds the "Main menu (subjects)" navigation menu via the Admin API, from the
20 top-level subject collections, the 124 level-2 sub-collections and the 4
merch collections.

  export SHOPIFY_STORE="gazelle-books-2026.myshopify.com"
  export GAZELLE_CLIENT_ID="..."      # GSD Gazelle Scripts app
  export GAZELLE_CLIENT_SECRET="..."
  python3 scripts/build_gazelle_menu.py --dry-run
  python3 scripts/build_gazelle_menu.py

Shape: 8 level-1 groups, 31 level-2 columns (20 subject + 4 merch + 7 brand
-site links), 126 level-3 links (106 children + one "All <parent>" per
subject column). Horizon renders this as a mega menu: L1 in the header bar,
L2 as column headings, L3 as the links under them.

L1 labels are deliberately SHORT. The first version used descriptive labels
("Science, technology and medicine") and seven of them overflowed Horizon's
header bar into a "More" item. Keep new L1 labels to roughly one or two
words.

⚠️ THREE LEVELS IS THE CEILING. Shopify documents menu nesting as "up to
three levels deep" and this tree already uses all three. A fourth tier is
not a small change - it is not supported by the API at all.

⚠️ RE-RUN BEHAVIOUR: the menu is matched by HANDLE. On a re-run the menu's
own ID is PRESERVED (so the theme setting never has to be re-pointed) but
every menu ITEM is deleted and recreated, because the tree is rebuilt from
scratch with no item IDs. That is not a no-op diff and is not pretended to
be one; item IDs churn, the menu ID does not.

Labels are read from the STORE at run time (not hardcoded) so a re-run after
Billy renames a collection picks up his titles. In --dry-run the committed
titles are shown instead unless credentials happen to be exported, in which
case live titles are read.

Does NOT touch the live main menu, the footer menu, or the theme. Selecting
this menu in Header > menu is a manual step in the theme editor.

Scopes: write_online_store_navigation, read_online_store_navigation,
read_products.
"""
import os, sys, json, importlib.util
import requests

STORE = os.environ.get("SHOPIFY_STORE", "gazelle-books-2026.myshopify.com")
CLIENT_ID = os.environ.get("GAZELLE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GAZELLE_CLIENT_SECRET")
API_VERSION = "2026-07"
URL = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"
HERE = os.path.dirname(os.path.abspath(__file__))

MENU_TITLE = "Main menu (subjects)"
MENU_HANDLE = "gazelle-main-subjects"
BOOKSONIX_CLIENT_ID = "5e994c135911baa59f413b9ac8d79992"

# Constants and helpers come from the collections script rather than being
# duplicated - it is the single source of truth for handles and titles.
_spec = importlib.util.spec_from_file_location(
    "gz_collections", os.path.join(HERE, "create_gazelle_collections.py"))
GZ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(GZ)

# ---------------------------------------------------------------------------
# Structure (authoritative). Child order is the order listed here.
# 18 L2 collections are deliberately NOT in nav - the Fiction long tail
# (FY FX FS FK FU FN FW FT FD), MR, WZ WF WC WK WJ, and TC TN TR. They stay
# live as filter/landing collections. Do not add them here.
# ---------------------------------------------------------------------------
GROUPS = [
    ("Fiction", "F", [
        ("F", "FB FJ FV FH FM FF FL FR"),
        ("D", "DN DC DS DD DB"),
        ("X", "XA XQ"),
    ]),
    ("Children's", "Y", [
        ("Y", "YN YF YB YP YX YD"),
    ]),
    ("Arts & humanities", "A", [
        ("A", "AG AJ AK AT AM AV AF AB"),
        ("N", "NH NK"),
        ("Q", "QR QD"),
        ("C", "CJ CF CB"),
    ]),
    ("Science & medicine", "M", [
        ("P", "PS PH PN PB PD PG"),
        ("T", "TQ TH TG TD TV TB TJ TT"),
        ("M", "MB MJ MK MF MN MQ MX MZ"),
        ("U", "UY UM UN UB UD UR UT UF"),
        ("R", "RN RB RG RP"),
    ]),
    ("Society & business", "J", [
        ("J", "JB JP JN JM JH JW JK"),
        ("K", "KC KJ KN KF"),
        ("L", "LN LA LB"),
        ("G", "GT GB GL GP"),
    ]),
    ("Lifestyle", "W", [
        ("W", "WN WT WD WB WG WM WQ WH"),
        ("V", "VX VF VS"),
        ("S", "SF SC SZ SR SV ST SP"),
    ]),
]

# The merch group: level-2 items only, no children.
MERCH_GROUP_LABEL = "Gifts & stationery"
MERCH_ORDER = ["cards-stationery", "posters-wallcharts", "music-audio", "maps"]
MERCH_L1_HANDLE = "cards-stationery"

# Level-1 group of links out to the brand site. type HTTP, not COLLECTION -
# note MenuItemType has NO "URL" value; HTTP is the enum for an external link.
# Edit these here; nothing else needs changing.
EXTERNAL_LINKS_LABEL = "Trade & publishers"
EXTERNAL_LINKS_URL = "https://gazellebookservices.co.uk/"
EXTERNAL_LINKS = [
    ("Publishers",            "https://gazellebookservices.co.uk/publishers"),
    ("Retailers",             "https://gazellebookservices.co.uk/retailers"),
    ("Open a trade account",  "https://gazellebookservices.co.uk/trade-account"),
    ("Catalogues",            "https://gazellebookservices.co.uk/catalogues"),
    ("News",                  "https://gazellebookservices.co.uk/blog"),
    ("About Gazelle",         "https://gazellebookservices.co.uk/about"),
    ("Contact",               "https://gazellebookservices.co.uk/contact"),
]

# Trailing "All ..." item in every subject column.
ALL_LABEL = {
    "F": "All fiction", "D": "All literature", "X": "All graphic novels",
    "Y": "All children's", "A": "All arts", "N": "All history",
    "Q": "All philosophy and religion", "C": "All language",
    "P": "All science", "T": "All technology", "M": "All medicine",
    "U": "All computing", "R": "All earth sciences", "J": "All society",
    "K": "All business", "L": "All law", "G": "All reference",
    "W": "All lifestyle", "V": "All health", "S": "All sport",
}

_TOKEN = None
def get_token():
    global _TOKEN
    if _TOKEN:
        return _TOKEN
    if not (CLIENT_ID and CLIENT_SECRET):
        sys.exit("Set GAZELLE_CLIENT_ID and GAZELLE_CLIENT_SECRET first.")
    if CLIENT_ID == BOOKSONIX_CLIENT_ID:
        sys.exit("REFUSING TO RUN: that is the BooksoniX Integration app (Dave's). "
                 "Use the GSD Gazelle Scripts credentials.")
    r = requests.post(f"https://{STORE}/admin/oauth/access_token",
                      json={"grant_type": "client_credentials",
                            "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
    if r.status_code != 200:
        sys.exit(f"Token exchange failed ({r.status_code}): {r.text[:300]}")
    _TOKEN = r.json()["access_token"]
    return _TOKEN

def have_credentials():
    return bool(CLIENT_ID and CLIENT_SECRET and CLIENT_ID != BOOKSONIX_CLIENT_ID)

def gql(query, variables=None):
    r = requests.post(URL, headers={"X-Shopify-Access-Token": get_token(),
                                    "Content-Type": "application/json"},
                      json={"query": query, "variables": variables or {}})
    r.raise_for_status()
    d = r.json()
    if "errors" in d:
        sys.exit(f"GraphQL errors: {json.dumps(d['errors'], indent=2)[:600]}")
    return d["data"]

COLLECTIONS_Q = """
query AllCollections($cursor: String) {
  collections(first: 100, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes { id handle title }
  }
}"""

MENUS_Q = """
query AllMenus { menus(first: 50) { nodes { id handle title } } }"""

CREATE_M = """
mutation CreateMenu($title: String!, $handle: String!, $items: [MenuItemCreateInput!]!) {
  menuCreate(title: $title, handle: $handle, items: $items) {
    menu { id handle title items { id title items { id title items { id title } } } }
    userErrors { field message code }
  }
}"""

UPDATE_M = """
mutation UpdateMenu($id: ID!, $title: String!, $handle: String!, $items: [MenuItemUpdateInput!]!) {
  menuUpdate(id: $id, title: $title, handle: $handle, items: $items) {
    menu { id handle title }
    userErrors { field message code }
  }
}"""

def store_collections():
    out, cursor = {}, None
    while True:
        d = gql(COLLECTIONS_Q, {"cursor": cursor})["collections"]
        for n in d["nodes"]:
            out[n["handle"]] = n
        if not d["pageInfo"]["hasNextPage"]:
            return out
        cursor = d["pageInfo"]["endCursor"]

def committed_titles(labels):
    """handle -> title from the committed constants, for a token-free dry run."""
    t = {h: title for _l, title, h in GZ.SUBJECT_COLLECTIONS}
    for c in GZ.COLLECTIONS:
        t[c["handle"]] = c["title"]
    for code in GZ.HANDLE_OVERRIDES:
        letter = code[0]
        if letter in GZ.PARENT_SHORT:
            t[GZ.handle_for(code, letter, labels)] = GZ.title_for(code, labels)
    return t

def build_tree(resolve):
    """resolve(handle) -> (gid_or_None, title). Returns (items, counts)."""
    missing, items = [], []
    n1 = n2 = n3 = 0

    def node(handle, title):
        gid, live = resolve(handle)
        if gid is None and live is None:
            missing.append(handle)
        item = {"title": title or live or handle,
                "type": "COLLECTION",
                "url": f"/collections/{handle}"}
        if gid:
            item["resourceId"] = gid
        return item

    labels = GZ.load_labels()
    parent_handle = {l: h for l, _t, h in GZ.SUBJECT_COLLECTIONS}

    for label, l1_letter, columns in GROUPS:
        l1 = node(parent_handle[l1_letter], label)   # L1 label is fixed copy
        l1["items"] = []
        n1 += 1
        for letter, codes in columns:
            ph = parent_handle[letter]
            _gid, live = resolve(ph)
            col = node(ph, live)                      # L2 label = live title
            col["items"] = []
            n2 += 1
            for code in codes.split():
                ch = GZ.handle_for(code, letter, labels)
                _g, clive = resolve(ch)
                col["items"].append(node(ch, clive))  # L3 label = live title
                n3 += 1
            col["items"].append(node(ph, ALL_LABEL[letter]))
            n3 += 1
            l1["items"].append(col)
        items.append(l1)

    merch = node(MERCH_L1_HANDLE, MERCH_GROUP_LABEL)
    merch["items"] = []
    n1 += 1
    for h in MERCH_ORDER:
        _g, live = resolve(h)
        merch["items"].append(node(h, live))
        n2 += 1
    items.append(merch)

    # Level 1: out to the brand site. External links resolve to nothing in the
    # store, so they bypass node() and its missing-handle check entirely.
    ext = {"title": EXTERNAL_LINKS_LABEL, "type": "HTTP",
           "url": EXTERNAL_LINKS_URL, "items": []}
    n1 += 1
    for title, url in EXTERNAL_LINKS:
        ext["items"].append({"title": title, "type": "HTTP", "url": url})
        n2 += 1
    items.append(ext)

    if missing:
        print("\nSTOP: these handles do not exist in the store - a menu with "
              "holes was NOT created:")
        for h in sorted(set(missing)):
            print("  " + h)
        sys.exit(1)
    return items, (n1, n2, n3)

def print_tree(items):
    for a in items:
        print(f"  {a['title']}  ->  {a['url']}")
        for b in a.get("items", []):
            print(f"    {b['title']}  ->  {b['url']}")
            for c in b.get("items", []):
                print(f"      {c['title']}  ->  {c['url']}")

def main():
    dry = "--dry-run" in sys.argv
    live_titles = have_credentials()

    if dry and not live_titles:
        labels = GZ.load_labels()
        titles = committed_titles(labels)
        print("DRY RUN - no credentials exported, so NO API calls are made and")
        print("titles below are the COMMITTED ones. Live titles may differ if")
        print("Billy has renamed anything in admin.\n")
        # Without the store there is nothing to check handles against, so the
        # missing-handle guard cannot fire in this mode. Export credentials
        # for a dry run that actually verifies every handle exists.
        resolve = lambda h: (None, titles.get(h, h))
    else:
        cols = store_collections()
        print(f"read {len(cols)} collections from {STORE}\n")
        resolve = lambda h: ((cols[h]["id"], cols[h]["title"])
                             if h in cols else (None, None))

    items, (n1, n2, n3) = build_tree(resolve)

    if dry:
        print_tree(items)
        print(f"\nL1 {n1}   L2 {n2}   L3 {n3}   (expected 8 / 31 / 126)")
        print("DRY RUN - nothing was written.")
        return

    existing = next((m for m in gql(MENUS_Q)["menus"]["nodes"]
                     if m["handle"] == MENU_HANDLE), None)
    if existing:
        print(f"menu exists ({existing['id']}) - updating in place.")
        print("NOTE: the menu ID is preserved, so the theme setting does not")
        print("need re-pointing, but every menu ITEM is deleted and recreated.")
        res = gql(UPDATE_M, {"id": existing["id"], "title": MENU_TITLE,
                             "handle": MENU_HANDLE, "items": items})["menuUpdate"]
    else:
        print("menu does not exist - creating.")
        res = gql(CREATE_M, {"title": MENU_TITLE, "handle": MENU_HANDLE,
                             "items": items})["menuCreate"]
    if res["userErrors"]:
        sys.exit(f"FAILED: {res['userErrors']}")

    menu = res["menu"]
    print(f"\nOK  {menu['title']}  ({menu['handle']})")
    print(f"    {menu['id']}")
    print(f"    L1 {n1}   L2 {n2}   L3 {n3}")
    print("\nNext, in the THEME EDITOR (this script does not touch the theme):")
    print("  Header > menu block > Menu > select 'Main menu (subjects)'.")
    print("  The live main menu is untouched; switch back at any time.")

if __name__ == "__main__":
    main()
