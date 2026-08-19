"""
Thema level-2 counts per top-level subject collection.
Usage:  python3 thema_l2_counts.py <folder-with-export-csvs> [threshold]
"""
import sys, glob, os, re, pandas as pd

src = sys.argv[1]
THRESH = int(sys.argv[2]) if len(sys.argv) > 2 else 24
COL = 'Thema Subjects (product.metafields.custom.thema_subjects)'

if src.endswith('.pkl'):
    df = pd.read_pickle(src)
elif src.endswith('.csv'):
    df = pd.read_csv(src, low_memory=False)
else:
    files = sorted(glob.glob(os.path.join(src, 'products_export*.csv')))
    df = pd.concat([pd.read_csv(f, low_memory=False) for f in files], ignore_index=True)

p = df[df['Title'].notna()].copy()
total = len(p)
if 'Status' in p.columns:
    p = p[p['Status'].str.lower() == 'active']
print(f'products: {total}  active: {len(p)}  with thema: {p[COL].notna().sum()}')

CODE = re.compile(r'^[A-Z][A-Z0-9]{0,5}$')
rows = []
for h, val in zip(p['Handle'], p[COL].fillna('')):
    seen = set()
    for c in [x.strip() for x in val.split(',') if x.strip()]:
        if CODE.match(c):
            l2 = c[:2]
            if len(c) >= 2 and l2 not in seen:
                seen.add(l2); rows.append((h, c[0], l2))
long = pd.DataFrame(rows, columns=['handle', 'top', 'l2']).drop_duplicates()
top_counts = long.drop_duplicates(['handle','top']).groupby('top').size()
l2_counts = long.groupby(['top','l2']).size().rename('products').reset_index()
l2_counts['keep'] = l2_counts['products'] >= THRESH
l2_counts['parent_total'] = l2_counts['top'].map(top_counts)
l2_counts = l2_counts.sort_values(['parent_total','top','products'], ascending=[False,True,False])
out = os.path.join(os.path.dirname(src.rstrip('/')) or '.', 'thema_l2_counts.csv')
l2_counts.to_csv(out, index=False)
print(l2_counts.to_string(index=False))
kept = l2_counts[l2_counts.keep]
print(f'\nL2 groups total: {len(l2_counts)}   kept (>= {THRESH}): {len(kept)}   dropped: {len(l2_counts)-len(kept)}')
print('kept per parent:'); print(kept.groupby('top').size().to_string())
print('wrote', out)
