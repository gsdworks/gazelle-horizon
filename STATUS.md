# STATUS — Gazelle Books

_The "now" list. Open loops and next actions only. Completed work lives in DONE.md._
_Last updated: 11 August 2026_

## Blocking go-live
- **DAVE — re-push the 1,057-product stale cohort.** One cohort carries every remaining data defect (overlapping: 934 blank Product Type, 548 Thema-as-names, 529 placeholder dimensions, 342 `__line:` series tokens). Re-push list CSV with per-defect flags emailed 11 Aug. Next: chase if no reply within 48 hours. **Product Type itself is no longer a blocker — it landed at 98.1% coverage, verified against Billy's 28 May combine list.**
- **DAVE — duplicate barcodes are integration-created and the hazard is live.** 20 duplicates across 42 products, handle/`-1` pairs; test stock units seen landing on the WRONG listing of a pair. Asked 11 Aug what causes the duplication. **Fix the cause before deleting anything Shopify-side** — deletion first just lets the integration recreate them.

## Open loops — DAVE
- **Add `thema_top` to his push.** First letters of the Thema codes, one line on his side. Send straight after the Billy call, once the collection structure is approved. Until then every new product arrives without it and misses the subject collections.
- **312 taxable books.** CSV sent 11 Aug. Books should not be taxable.
- **Load completion / catalogue count UNCONFIRMED.** Store reports 49,363 products via API (49,367 later) against 48,220 in the same-morning export — ~1,143 gap, cause UNCONFIRMED (export likely ran mid-sync). Earlier catalogue estimate was ~54,500. Confirm with Dave whether the load has finished before treating any total as final.
- **All products active and published; draft-on-create not operating.** Agreed behaviour was DRAFT on create so Gazelle have oversight. **Verify against the email record before raising** — UNCONFIRMED whether this was ever put to Dave in writing.
- **255 future-dated titles are live.** Agreed rule was that forthcoming titles are not pushed live. Same UNCONFIRMED caveat as above — check the email record first. Billy's answer on desired behaviour is on today's call agenda.
- **Other carried items, unverified:** archive-not-delete, PUBCODE as a discrete metafield, approved-only filter.
- **Nova Science publisher name has 3 variants across ~20k products** — fragments the imprint filter into three entries for one publisher. Source normalisation, not urgent.

## Open loops — BILLY
- **CALL TODAY (11 Aug) — live demo, not a proposal.** Agenda: approve subject collection labels + main-nav picks; Biography as a nav category? (yes means deriving `thema_top2` for second-level codes, since biography is `DN*` under `D` and Thema has no `B` top level); Mixed-media product decision (126 products, absent from his 28 May combine list); Trajan Pro licence; behaviour for the 255 live future-dated titles; policy-page facts (registered address, company + VAT numbers, returns window, who pays return postage, delivery tiers/rates, despatch cut-off, UK-only vs international); catalogue count nod (~49.4k in store).
- **Product-page preview + go-live framing.** Owed since 20 Jul. Now backed by real news: Product Type landed, 24 collections live, catalogue at ~49.4k.
- **Ebook exclusion scope.** He excluded ONIX 14 (Digital, delivered electronically) but not 21 (Electronic book text) or 20 (E-book reader). One-line question: should 21 also be excluded?

## Open loops — FRED
- **Delta (changed-only) stock feed.** Awaiting since ~20 Jul. At ~49.4k products a full nightly snapshot against the ~5k variant-updates/hour ceiling will not fit the 02:00 window. Not a hard go-live blocker (full-file path proven end-to-end), but the maths does not work at this scale.

## Open loops — OURS
- **After the Billy call:** one-liner to Dave adding `thema_top` to his push; then after his re-push, re-run `scripts/populate_thema_top.py` against a fresh export to sweep in the stale cohort and the ~1,143 export-gap products.
- **Build the subject nav menu.** `write_online_store_navigation` scope is held, so this is scriptable rather than a manual admin job. Gated on Billy approving labels today. Kills the **"Catagories" typo** in the placeholder menu at the same time — that must not ship.
- **UNCONFIRMED whether these were done in the 11 Aug session** — verify before assuming: Format and Subject filters added in Search & Discovery; the 4 policy pages pasted into admin.
- **Queued front-end work, no dependencies:** font/serif-role fix (tomorrow, alongside the Trajan answer); PDF catalogue section (contracted); placeholder content pages; checkout styling; notification email templates.
- **SFTP scheduled pickup in Matrixify.** Wire it and watch it fire once — the only untested part of the pipeline. Not started.
- **Paid Matrixify tier.** Demo won't run production. Blocked on Fred's delta answer.
- **Send-receipt flip.** Billy wants TRUE. Hold FALSE until launch, then verify one-email-per-parcel with notifications on before flipping.
- **Metafield type migration (deferred, not blocking).** Minimal confirmed list: `publication_date` → Date (still 0% ISO — blocks the New-Release rule), plus `author`, `thema_subjects`, `bic_subjects`, `bisac_subjects`, `main_subjects` → list types. Tool built and committed (`update_gazelle_metafield_types.py`, never run). TRAP: pipes occur inside legitimate content — any list-splitting must be per-field, never blanket.
- **Monolith carve into `docs/`.** Carve `gazelle-context-working.md` detail into `docs/*.md`, then retire it. **Carry into the carve:** correct the stale Shopify CLI version — `gazelle-tech-stack.md` and `gazelle-context-working.md:759` both say **3.92.1**; actual is **4.6.0**.

## Housekeeping
- **Scripts authenticate via the "GSD Scripts" custom app (Dev Dashboard + client credentials grant).** No static tokens exist — every run exchanges client id/secret for a short-lived token. Legacy Settings custom apps were deprecated 1 Jan 2026.
- **Smart collections on metafields: "is equal to" only.** `list.single_line_text_field` works (equals matches any list entry) and the definition needs the `smartCollectionCondition` capability. Prefix matching is impossible — derive the exact value instead. This is why `thema_top` exists.
- **Run glob scripts against an isolated folder, never Downloads** — 127 accumulated CSVs there, and one stale non-UTF-8 file crashed a run. Current exports live in `~/Downloads/export-11aug`. Mac system Python is 3.9 with old pip (no `--break-system-packages`); consider brew Python.
- **Tick the Tags column in Matrixify export settings** — it was missing from the 11 Aug export again, which silently removes any ability to check PUBCODE.
- **Gmail connector is NOT trustworthy for negative results on this project.** A search returning nothing is not evidence of silence — verify with `get_thread` on a known thread before concluding a client hasn't replied.
- **Run a digest after any client exchange that changes state**, not only at session end.
- Store is unbuyable until Fred's stock feed runs — inventory qty=0 store-wide (tracked, policy deny). Known cause, not Dave.
- 4,614 products (9.6%) have no image.
- Native Tags blank — PUBCODE remains buried inside `tags_global`. Homepage curation stays blocked on Dave surfacing it discretely.
- `custom.format` and `custom.genre` — 2 products each, undefined keys not in the 23-field contract. Unexplained. Clean when convenient.
- Handles carrying a `-N` suffix are **not** in themselves a finding — but the handle/`-1` duplicate-barcode pairs above ARE. Don't conflate the two.
- BooksoniX Integration app client secret may have been rotated by Dave — UNVERIFIED.
- Shopify CLI now **4.6.0**. If a CLI command behaves oddly for no reason, check the version first.
- Gazelle is a **fork** of `Shopify/horizon` and is the only one there will ever be (one fork per upstream per account). Future GSD projects use a plain repo + mirror-push + `upstream` remote. Do not "harmonise" Gazelle to that shape.
- Context system: drag PROJECT-CONTEXT.md into claude.ai project knowledge after each `/update-context`.
