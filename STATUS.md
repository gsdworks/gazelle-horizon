# STATUS — Gazelle Books

_The "now" list. Open loops and next actions only. Completed work lives in DONE.md._
_Updated: 2026-07-30_

## Blocking go-live
- **DAVE — full catalogue load.** Store holds ~1,800 of ~54,500 titles (~3%). Event-driven integration only creates a product when a BooksoniX record changes, so the catalogue trickles in ~40–50/day. The full bulk load has never run; the force-update mechanism across the whole catalogue reportedly crashes BooksoniX. **This is the true go-live gate.** Next: once the re-push below is verified, ask Dave (Billy cc) for the plan + timeline on the full load.
- **DAVE — metafield re-push (in flight).** Root cause of the failed force-update found and fixed 30 Jul: 3 definitions were multi-line, blocking Dave's single-line writes. Now aligned. **Emailed Dave to re-run the update push.** Next: on his re-push, pull a fresh export and verify — the ~523 has-type/zero-metafield products should collapse; `%sh_height_mm%` count (895) should hold, not climb.

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

## Front-end open items (yours alone, cheap — good filler between Dave rounds)
- Nav "Catagories" typo in placeholder menu — must not ship. Admin → Navigation job.
- Featured Collection carousel bleed — RESOLVED 16 Jul (verify still holding).
- Nav taxonomy proposal to Billy — gated on subject-distribution analysis.

## This week (system-critical)
- **OURS — fix git push from CLI.** HTTPS push fails (GitHub killed password auth); GitHub Desktop still works. Switch remote to SSH or store a PAT in keychain. The /update-context loop depends on push working. Not started.

## Housekeeping
- `custom.format` and `custom.genre` — 2 products each, undefined keys not in the 23-field contract. Unexplained. Investigate/clean when convenient.
- Next product export MUST include the Tags column (didn't export last time — 0/1,734 rows read as "untagged" when coverage was unreadable).
- Context system restructure: STATUS/DONE/digest-protocol now live. Claude.ai side = drag PROJECT-CONTEXT.md after each /update-context (GitHub Sync-now connector confirmed unreliable mid-2026 — do not rely on it). Optional later: trial Basic Memory Cloud (~£10/mo, 7-day trial) if the drag keeps getting forgotten. Pending: carve monolith into docs/*.md on a quiet afternoon, then retire it.
