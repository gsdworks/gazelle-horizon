# STATUS — Gazelle Books

_The "now" list. Open loops and next actions only. Completed work lives in DONE.md._
_Updated: 2026-08-03_

## Blocking go-live
- **DAVE — full catalogue load (RUNNING).** Started overnight Thu 30 Jul, still running. ~35,745 of ~54,500 (~65%) at 3 Aug 10:00. Slow because the Shopify API rate-limits at 2 calls/sec and each record takes several calls; BooksoniX are looking at GraphQL bulk updates as a future improvement. Next: confirm with Dave that it completed, then re-export to take final counts (all current figures are mid-run readings — ratios beat totals).
- **DAVE — Product Type empty on 98.1%** (35,073 of 35,745 blank; the 672 typed are the unchanged pre-June cohort). Cause: Billy's 28 May combine list was never implemented, and the product_type write went out with the 3 June tax-mapping change. **The Format filter is dead across the catalogue.** `gazelle-product-type-mapping.csv` (60 rows) sent to Dave 3 Aug on "Shopify progress", Billy + Paul copied. Next: chase if no reply within 48 hours — escalation includes the ten-week history and keeps Paul on.

## Open loops — DAVE
- **Series field is junk.** All 3,786 products with a series carry `__line:` internal tokens, not the series name (was 385, scaled unchanged). Re-raised 3 Aug with the full count.
- **Thema/BIC as codes — ADVANCING.** 24,456 Thema and 23,223 BIC now code-format (was 6.5% codes on 16 Jul). The 10,713 name-format records are the un-re-pushed tail; completes as the push completes. No action — verify at final export.
- **All products active and published; draft-on-create not operating.** All 35,745 are status=active / Published=true. Agreed behaviour was DRAFT on create so Gazelle have oversight. **Verify against the email record before raising** — UNCONFIRMED whether this was ever put to Dave in writing.
- **216 forthcoming titles are live**, 137 more than 30 days out, furthest 2028-04-28. Agreed rule was that forthcoming titles are not pushed live. **Verify against the email record before raising** (same caveat as above).
- **Other carried items, unverified:** archive-not-delete, PUBCODE as a discrete metafield, approved-only filter. Reconcile against the final post-load export.

## Open loops — BILLY
- **Product-page preview + go-live framing.** Owed since 20 Jul, re-asked 22 Jul. Now have real news: root cause fixed, data flowing, 35k+ titles in and climbing. Send preview + this update — heads off the third-deferral escalation.
- **Ebook exclusion scope.** Billy excluded ONIX 14 (Digital, delivered electronically) but did not mark 21 Electronic book text or 20 E-book reader. One-line question: should 21 also be excluded?
- **Taxonomy / navigation sign-off — UNBLOCKING.** Was blocked on Thema coverage; unblocks when the push completes and Thema is majority codes. Then: subject-distribution analysis → nav proposal.

## Open loops — FRED
- **Delta (changed-only) stock feed.** Awaiting since ~20 Jul. **Now materially more urgent:** at 35,745 products and climbing toward 54,500, a full nightly snapshot against the ~5k variant-updates/hour ceiling will not fit the 02:00 window. Still not a hard go-live blocker (full-file path proven end-to-end), but the maths has changed.

## Open loops — OURS
- **15 duplicate barcodes across 32 products.** Clear in admin before the stock feed runs — a Matrixify hazard, so this is a prerequisite, not housekeeping. Also 3 blank barcodes; all values 13-digit where present.
- **Barcode-uniqueness store audit — DONE at scale** (35,745 products: 15 dupes, 3 blanks, no malformed). Remaining work is the clean-up line above.
- **Launch front-end workstream.** Pages, collections + product assignment, menu hierarchy, remaining visual build. Collections and menu are gated on the push completing and on Product Type landing; **pages and general polish are NOT gated — start there.**
- **SFTP scheduled pickup in Matrixify.** Wire it and watch it fire once — the only untested part of the pipeline. Not started.
- **Paid Matrixify tier.** Demo won't run production. Blocked on Fred's delta answer.
- **Send-receipt flip.** Billy wants TRUE. Hold FALSE until launch, then verify one-email-per-parcel with notifications on before flipping.
- **Metafield type migration (deferred, not blocking now).** Minimal confirmed list: `publication_date` → Date (still 0% ISO at 35,739 free-text values — blocks the New-Release rule), plus `author`, `thema_subjects`, `bic_subjects`, `bisac_subjects`, `main_subjects` → list types (blocks native S&D subject filtering). Tool built and committed (`update_gazelle_metafield_types.py`, never run). TRAP: pipes occur inside legitimate content — any list-splitting must be per-field, never blanket.
- **Nav "Catagories" typo** in the placeholder menu — must not ship. Admin → Navigation job.
- **Monolith carve into `docs/`.** Carve the detail sections of `gazelle-context-working.md` into `docs/*.md`, then retire it. Import chain proven 1 Aug. **Carry into the carve:** correct the stale Shopify CLI version — `gazelle-tech-stack.md` and `gazelle-context-working.md:759` both say **3.92.1**; actual is **4.6.0**.

## Housekeeping
- **Gmail connector is NOT trustworthy for negative results on this project.** A search returning nothing is not evidence of silence — always verify with `get_thread` on a known thread before concluding a client hasn't replied. (Cost us a false "Dave has not replied" on 3 Aug.) Possible contributing factor: a Google Workspace email migration ran 28 Jul (UNCONFIRMED).
- **Run a digest after any client exchange that changes state**, not only at session end. PROJECT-CONTEXT.md sat three days stale because the 31 Jul exchange never got one.
- Store is entirely unbuyable — inventory qty=0 on 35,737 (tracked, policy deny). Known cause: Fred/Matrixify stock feed, not Dave. Resolves when the feed runs.
- 2,063 products have no image; 33,618 exactly one; 64 two or more. Watch as the load completes.
- Native Tags blank on all 35,745 — PUBCODE remains buried inside `tags_global`. Homepage curation stays blocked on Dave surfacing it discretely.
- `custom.format` and `custom.genre` — 2 products each, undefined keys not in the 23-field contract. Unexplained. Clean when convenient.
- 5,393 handles carry a `-N` suffix. **Not a finding** — no identified victim; duplicate titles across publishers are normal in books.
- BooksoniX Integration app client secret may have been rotated by Dave — UNVERIFIED. The 400 `application_cannot_be_found` came from placeholder creds, not a rotation test. Confirm before the type migration needs API access.
- Shopify CLI now **4.6.0** (self-upgraded mid-command 1 Aug, global npm install). If a CLI command behaves oddly for no reason, check the version first.
- Gazelle is a **fork** of `Shopify/horizon` and is the only one there will ever be (one fork per upstream per account). Future GSD projects use a plain repo + mirror-push + `upstream` remote. Do not "harmonise" Gazelle to that shape.
- Context system: drag PROJECT-CONTEXT.md into claude.ai project knowledge after each `/update-context` (GitHub Sync-now connector confirmed unreliable mid-2026).
