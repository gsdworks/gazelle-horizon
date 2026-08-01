# STATUS — Gazelle Books

_The "now" list. Open loops and next actions only. Completed work lives in DONE.md._
_Updated: 2026-08-01_

## Blocking go-live
- **DAVE — full catalogue load.** Store holds ~1,800 of ~54,500 titles (~3%). Event-driven integration only creates a product when a BooksoniX record changes, so the catalogue trickles in ~40–50/day. The full bulk load has never run; the force-update mechanism across the whole catalogue reportedly crashes BooksoniX. **This is the true go-live gate.** Next: once the re-push below is verified, ask Dave (Billy cc) for the plan + timeline on the full load.
- **DAVE — metafield re-push (in flight).** Definitions fixed 30 Jul (3 multi-line definitions were blocking Dave's single-line writes; all 23 now match his payload). **Email sent 30 Jul — awaiting his re-push.** Next: on arrival, pull a fresh export and verify the ~523 has-type/zero-metafield products collapse, and the `%sh_height_mm%` count (895) holds, not climbs.

## Open loops
- **DAVE — series field is junk.** `custom.series` comes through as internal tokens (`__line:the_frean_chronicles`) on all 385 products that have one, not the series name. Raised with Dave 30 Jul in the re-push email. Awaiting fix.
- **DAVE — placeholder tokens.** ~895 products store literal `%sh_height_mm%` as their height from earlier runs. NOT yet raised (unproven whether it's his template or import-side). Check after the re-push: if placeholders clear on their own it was never his; if they persist, raise with evidence.
- **DAVE — other known items** (carried, unverified since last audit): Thema two-format (codes vs decoded names), archive-not-delete, PUBCODE as discrete metafield, approved-only filter. Reconcile against the post-re-push export.
- **BILLY — product-page preview + go-live framing.** Owed since 20 Jul, re-asked 22 Jul. Now have real news: root cause found and fixed, data flowing again, catalogue load is the remaining dependency. Send preview + this update — heads off the third-deferral escalation.
- **FRED — delta (changed-only) stock feed.** Targeted early this week. Explicitly NOT a go-live blocker (full-file path proven end-to-end). Awaiting since ~20 Jul.
- **OURS — SFTP scheduled pickup in Matrixify.** Wire it and watch it fire once — the only untested part of the pipeline. Not started.
- **OURS — paid Matrixify tier.** Demo won't run production. Blocked on Fred's delta answer.
- **OURS — send-receipt flip.** Billy wants send-receipt TRUE. Hold FALSE until launch, then verify one-email-per-parcel with notifications on before flipping. Not started.
- **OURS — barcode-uniqueness store audit** before go-live. Source confirmed single across 54,517 rows (Lee removed fudged `9781909360266`); store-side audit still to run.
- **OURS — metafield type migration (deferred, not blocking now).** Minimal confirmed list: `publication_date` → Date (blocks the New-Release rule), plus `author`, `thema_subjects`, `bic_subjects`, `bisac_subjects`, `main_subjects` → list types (blocks native S&D subject filtering). Nothing else needs to move. Tool is built and committed (`update_gazelle_metafield_types.py`, never run). TRAP: pipes occur inside legitimate content — any list-splitting must be per-field, never blanket.

## Front-end open items (yours alone, cheap — good filler between Dave rounds)
- Nav "Catagories" typo in placeholder menu — must not ship. Admin → Navigation job.
- Featured Collection carousel bleed — RESOLVED 16 Jul (verify still holding).
- Nav taxonomy proposal to Billy — gated on subject-distribution analysis.

## This week (system-critical)
- **OURS — monolith carve into `docs/`.** Carve the detail sections of `gazelle-context-working.md` into `docs/*.md`, then retire it. Quiet-afternoon job. The import chain is now proven (1 Aug), so anything carved into `docs/` will actually load. **Carry into the carve:** correct the stale Shopify CLI version — `gazelle-tech-stack.md` and `gazelle-context-working.md:759` both say **3.92.1**; actual is **4.6.0** (self-upgraded 1 Aug).

## Housekeeping
- `custom.format` and `custom.genre` — 2 products each, undefined keys not in the 23-field contract. Unexplained. Investigate/clean when convenient.
- Next product export MUST include the Tags column (didn't export last time — 0/1,734 rows read as "untagged" when coverage was unreadable).
- BooksoniX Integration app client secret may have been rotated by Dave — UNVERIFIED. The 400 `application_cannot_be_found` came from placeholder creds, not a rotation test. Confirm before the type migration needs API access.
- Shopify CLI now **4.6.0** (self-upgraded from 4.5.2 unprompted mid-`theme pull`, 1 Aug; global npm install so it moved for Gazelle too). If a CLI command behaves oddly for no reason, check the version first.
- Gazelle is a **fork** of `Shopify/horizon` and is the only one there will ever be — GitHub allows one fork per upstream per account. Future GSD projects use a plain repo + mirror-push + `upstream` remote (Eye Books, `gsdworks/eyebooks-horizon`, 1 Aug). Do not "harmonise" Gazelle to that shape; the fork works.
- Context system restructure: STATUS/DONE/digest-protocol now live. Claude.ai side = drag PROJECT-CONTEXT.md after each `/update-context` (GitHub Sync-now connector confirmed unreliable mid-2026 — do not rely on it). Optional later: trial Basic Memory Cloud (~£10/mo, 7-day trial) if the drag keeps getting forgotten.
