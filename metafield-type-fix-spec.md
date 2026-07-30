# Spec: Recreate 3 metafield definitions as single_line_text_field

**Store:** gazelle-books-2026.myshopify.com
**App/auth:** BooksoniX Integration app in the **Gazelle Dev org** (grantsd104 account) — NOT the 0-install orphan in the GSD Works Partner org. Same client-credentials flow as `create_gazelle_metafields.py` (env: `GAZELLE_CLIENT_ID`, `GAZELLE_CLIENT_SECRET`, token from `/admin/oauth/access_token`, sent as `X-Shopify-Access-Token`).
**API version:** 2026-07 (same as the create script).

## Why
Dave's BooksoniX push declares every metafield as `single_line_text_field`. Three definitions were created as multi-line on 7 July and are blocking his writes:

| Key | Current type | Values in store |
|---|---|---|
| `custom.prize_achievements` | multi_line_text_field | 7 |
| `custom.reviews` | multi_line_text_field | 104 |
| `custom.author_bio` | multi_line_text_field | 229 |

Shopify cannot change a definition's type in place. Each must be deleted (keeping values) and recreated as `single_line_text_field`. Verified against the live export: no stored value in any of the three contains a newline, so all values validate under the new type. Paragraphs are encoded as HTML (`<p>`/`<br>`), which single-line stores fine.

## THE ONE RULE THAT MATTERS
`metafieldDefinitionDelete` must be called with `deleteAllAssociatedMetafields: false`. If this is ever `true`, the stored values are destroyed with no undo. Hardcode it. Print it in dry-run output. Assert it in code before the mutation fires.

## Execution order (blast-radius ordering)
1. `custom.prize_achievements` (7 values — canary)
2. `custom.reviews` (104)
3. `custom.author_bio` (229)

Stop on any failure or count mismatch. Do not proceed to the next field.

## Step 0 — Backup (before ANY delete)
Write a JSON backup of all values for the three keys to `outputs/metafield_backup_<date>.json`, committed to the repo before step 1 runs. Paginate all products (~1,800; pages of 250):

```graphql
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
```

Store only products where at least one of the three is non-null. Sanity-check the backup counts: expect ~229 / ~104 / ~7 (match against the live definition counts fetched in step 1; the live counts are authoritative). If backup counts don't match live counts, STOP.

## Step 1 — Read existing definition (per field)
```graphql
query GetDef($ns: String!, $key: String!) {
  metafieldDefinitions(first: 1, ownerType: PRODUCT, namespace: $ns, key: $key) {
    nodes {
      id
      name
      namespace
      key
      type { name }
      pinnedPosition
      access { admin storefront }
      metafieldsCount
    }
  }
}
```
Capture: `id` (needed for delete), `name`, `pinnedPosition`, `access`, `metafieldsCount` (baseline for verification).

## Step 2 — Delete (keeping values)
```graphql
mutation DeleteDef($id: ID!) {
  metafieldDefinitionDelete(id: $id, deleteAllAssociatedMetafields: false) {
    deletedDefinitionId
    userErrors { field message }
  }
}
```
Abort the whole run on any userError.

## Step 3 — Recreate as single line
```graphql
mutation CreateDef($def: MetafieldDefinitionInput!) {
  metafieldDefinitionCreate(definition: $def) {
    createdDefinition { id name type { name } metafieldsCount }
    userErrors { field message }
  }
}
```
Input per field (values from step 1):
```json
{
  "name": "<same display name as before>",
  "namespace": "custom",
  "key": "<same key>",
  "ownerType": "PRODUCT",
  "type": "single_line_text_field",
  "pin": <true if pinnedPosition was non-null>,
  "access": { "storefront": "<as captured>", "admin": "<as captured>" }
}
```
If the API rejects the `access.admin` field on create (some versions restrict it), retry with `admin` omitted and log that it fell back to the default. Storefront access MUST be preserved — if storefront read is lost, the theme renders the field blank and it looks like data loss.

## Step 4 — Verify (per field, immediately after recreate)
Re-run the step 1 query. PASS requires all of:
- `type.name == "single_line_text_field"`
- `metafieldsCount` equals the step-1 baseline (7 / 104 / 229)
- `access.storefront` matches what was captured
- key and namespace identical

`metafieldsCount` may lag briefly after recreation; if it reads low, wait 30s and re-query up to 3 times before declaring failure. On persistent mismatch: STOP, report, do not touch the next field.

## Recovery path (only if something goes wrong)
Values can be restored from the step-0 backup via `metafieldsSet` (25 per call, `type: "single_line_text_field"`). Do not build this pre-emptively; it exists as a documented path, not a script.

## Script requirements
- New sibling script `update_gazelle_metafield_types.py` next to `create_gazelle_metafields.py`; reuse its token code.
- `--dry-run` (default ON; require explicit `--execute` to write). Dry run prints: target shop, API version, the three fields with current→new types, and the literal text `deleteAllAssociatedMetafields: false`.
- `--only <key>` flag so the canary can be run alone.
- Every mutation response logged verbatim to `outputs/metafield_type_fix_<date>.log`.
- Nothing else is touched: no other definitions, no metafield values, no products.

## After success
Log to `gazelle-context-working.md` (in-place edits per house rules, update the `Last updated:` line, commit in-session):
- Three definitions recreated as single_line 30 July via script (values preserved: 229/104/7 verified)
- Commitment to Dave: definitions frozen; any future type change is a coordinated migration, agreed in advance
- Confirmed future migration list: `publication_date` (→Date), `author`, `thema_subjects`, `bic_subjects`, `bisac_subjects`, `main_subjects` (→list types). Nothing else moves.
- New Dave bug: `custom.series` is internal tokens (`__line:the_frean_chronicles`) on all 385 products that have one — raised with Dave 30 July
- Trap: pipes occur inside legitimate content (book title "Short | Poto") — future list-splitting must be per-field, never blanket
- Trap: Dave's push declares types per field; he has offered in writing to update his side to match definitions. Single-line alignment chosen for speed, not because of a capability limit.
