# DONE — Gazelle Books

_Append-only permanent log of everything completed and discovered. Newest at the bottom. Never edit existing lines. FULL detail welcome — findings, email facts, decisions, reasoning; this file is the complete record and can grow without limit._
_Full detail for anything here lives in gazelle-context-working.md (the monolith) or git history._

2026-07-07 — 18 metafield definitions bulk-created via Admin API (`create_gazelle_metafields.py`, created=18 failed=0), verified against a live title.
2026-07-08 — Product page built: bottom band (tabs/specs/subjects rail), cover treatment, hero layout.
2026-07-14 — Footer built and styled to mockup (native four-column + utilities bar). Header built native-first (~zero custom CSS). Global page-width fix: `gazelle-layout.liquid` = single source of 1200px width.
2026-07-16 — Featured Collection carousel bleed fixed (contained to 1200px, 6 cards + peek). Full product export audited: force-update had reached only ~3% of catalogue — Dave's fixes correct, propagation was the problem. Fred workstream reconciled: A–N "regression" was a wrong-file artefact; real spec is A–Y and complete.
2026-07-17 — AS400 outbound built and delivered end-to-end via EZ Exporter (25 cols, dual-address proven). Stock import blocked on header row identified and requested. GZ order-ID prefix set.
2026-07-20 — Both import pipelines proven end-to-end in Shopify (stock + tracking), verified against store exports. Split shipment proven. Consolidated email sent to Fred.
2026-07-27 — Fred's four loops closed (header space stripped, duplicate barcode removed at source, order-ref echo confirmed, partial-quantity moot — no backorders). Billy re-engaged, go-live reframed off a date.
2026-07-30 — Diagnosed and fixed the failed force-update root cause: 3 metafield definitions (author_bio, reviews, prize_achievements) were multi-line, blocking Dave's single-line writes. Recreated all three as single line via admin (unstructured-metafields path), values preserved (229/104/7 verified). Confirmed remaining 20 definitions already match Dave's JSON. Emailed Dave to re-push, flagged the series-token bug. Built `update_gazelle_metafield_types.py` (dry-run-safe, backup-first) — committed unused as the tool for the future date/list type migration.
2026-07-30 — Context system restructured: split into CLAUDE.md (procedure) + STATUS.md (now) + DONE.md (log) + build-context.sh, with `/update-context` slash command. Monolith parked as read-only reference pending a later carve into docs/.
