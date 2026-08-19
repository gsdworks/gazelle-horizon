# STATUS — Gazelle Books

_The "now" list. Open loops and next actions only. Completed work lives in DONE.md._
_Last updated: 19 August 2026_

## OVERDUE
1. **Archive job** — four full publishers (BZ4 Edition Skylight, DB7 Tomas Horych, CU2 Jan Kowalewicz, DD2 U-Line) by pubcode substring in `tags_global` + vendor-name cross-check, plus the Edition Reuss 55 by barcode. Log counts per publisher, report the numbers to Billy. Input is `scripts/EditionReuss.xls`. UNCONFIRMED whether this ran on 14 Aug — check before re-running. **Do NOT let any run touch product 9783402135785 (ID 16432574726493) — that is Dave's live archive test.**
2. **Discounts follow-up to Billy** — needs Grant's commercial decision (quote separately vs absorb; flagged out-of-SOW in June). Billy expected it by end of w/c 14 Aug.
3. **Domain / holding page confirmation to Billy.**

## Blocking go-live
- **DOMAIN — `shop.gazellebookservices.co.uk` serves "This store is unavailable".** Attached to the OLD Gazelle store whose subscription lapsed in July. **DNS CNAME is already correct → do NOT change any DNS record**; the fix is Shopify-side attachment. Order: (a) check the `gazelle-books-2026` plan status FIRST — a dev-plan gate blocks custom domains and makes it a Billy billing conversation; (b) Settings → Domains → Connect existing domain; (c) if "in use by another store", check Grant's password manager for the old store's admin login (Grant built its holding page 1 Apr 2026); (d) else Shopify support release via TXT record — names.co.uk access is held (`marvin@gazellebookservices.co.uk`, credentials in Billy's 3 Feb "Domain" email).
- **Two launch-critical items sit with Dave — the archive re-activation test and the duplicates cause.** Detail under Open loops — DAVE.

## Next action — verify the L2 build
- **Run `scripts/verify_l2.py` under the GSD Gazelle Scripts app** — the five post-build checks are written but **NOT YET RUN**, because the only credentials available to the agent were the BooksoniX app's. One command, read-only:
  `python3 scripts/verify_l2.py ~/Downloads/export-19aug`
  Checks: 5 sampled products' metafields vs source codes; exact collection count (expect **150**); 10 sampled L2 counts vs `scripts/out/thema_l2_counts.csv` (>1% gap flagged; store 50,533 vs export 50,523, so small drift is expected); NH + NK vs the History parent; every L2 collection's `parent_handle` resolves.

## Open loops — DAVE
**⚠️ Read the "asks of third parties" principle in `docs/build-manual.md` before adding anything here. Keep asks minimal and non-cumulative.** The Integration Tasks sheet is the single channel; **Dave's outstanding list has been answered in full** and the bundled-email task is closed.

Launch-critical — these two only:
1. **Archive re-activation test.** Product **9783402135785** (Aschendorff Verlag), **ID 16432574726493**, archived manually by Grant. Random pick, not on any exclusion list, 0 stock, no sales. Dave to push an update and report whether the status flips back to active. **Do not touch its status with any script until Dave reports back.** Safe to unarchive afterwards. This is the gate on whether the archive sweep silently undoes itself.
2. **Duplicates cause** — asked 11 Aug, unanswered. 20 duplicates across 42 products, handle/`-1` pairs; test stock seen landing on the WRONG listing. Now known to be a **create collision** (Dave does not set handle; Shopify derives it), so the question is narrowed to why the same title is created twice. **Fix the cause before deleting anything Shopify-side.** Gates the EAN-handle rename.

Queued — put to him only AFTER Billy signs off the subject labels:
- **Push `thema_top` and `thema_l2` natively**, derived the same way (first character / first two characters of each valid Thema code). One change his side retires the backfill entirely. Do not raise it before the labels are settled — it would be a second ask about the same thing.

Slow-burn — in the sheet, do NOT chase separately:
- **Cover image fetch failures.** With him since **9 Jul**, silent since. 4,614 products (9.6%) have no cover; failing at Shopify fetch.
- **Inside spreads.** Only 64 of ~48k products have 2+ images. **~1,600 is the CEILING — that is all BooksoniX holds.** Not a sync bug, a content limit. **Tell Billy** so he isn't expecting catalogue-wide spreads.
- **Re-push the 1,057-product stale cohort** (934 blank Product Type, 548 Thema-as-names, 529 placeholder dimensions, 342 `__line:` series tokens — one overlapping cohort, one re-push clears all four). CSV emailed 11 Aug.
- **Taxable flag** — 312 products, file sent 11 Aug. Books should not be taxable.
- **Three source-data defects (18 Aug):** Liberty Fund synopses stripped of en dashes and apostrophes (per-publisher, not a global encoding fault); Goose Lane prize line jammed onto the description with the paragraph break lost; `main_subjects` "Mind, body & spirit" comma-splitting into three chips.
- **Escalation lever if silence continues: Paul Theijs.**

Parked / Grant-owned — do not re-raise:
- **Pubcode exclusion at source** — Grant's archive sweep covers it.
- **EAN handles** — Dave does not set `handle`, so a bulk rename is safe from clobber. Ours to script.
- **`thema_top` / `thema_l2` backfill** — ours until the native push above lands.

Carried, lower priority:
- **Load completion / catalogue count UNCONFIRMED.** API reported 49,363 (later 49,367) vs 48,220 in an earlier export — cause UNCONFIRMED. The 19 Aug export verified clean at 50,523 = 50,523.
- **All products active and published; draft-on-create not operating.** **Verify against the email record before raising** — UNCONFIRMED whether this was ever put to Dave in writing.
- **255 future-dated titles are live.** Same UNCONFIRMED caveat. Billy's answer on desired behaviour still owed.
- **Nova Science publisher name has 3 variants across ~20k products** — fragments the imprint filter. Source normalisation, not urgent.

## Data pipeline — pubcode
- **`custom.pubcode` definition created 19 Aug by us**, via `scripts/create_gazelle_metafields.py` — single line text, `smartCollectionCondition` enabled, `adminFilterable` on. Not a mystery field, not Dave's. **Empty on every product until his first push maps it.**
- Value spec given to Dave: **bare code only** (`CE1`), lowercase key `custom.pubcode`.
- **When his first push populates it, spot-check the value format BEFORE wiring the discount rule or any exclusion collection to it.** A value arriving in the long `CE1 - LINDEN PUBLISHING INC` form silently breaks an equals-based smart collection.
- **Until then the `tags_global` parse stays the working source** — do not rip it out early.

## Open loops — BILLY
- **Review the 124 L2 sub-collection titles** — starting points from the EDItEUR Thema headings, not final. Matching is on handle, so he can retitle freely in admin without breaking a re-run. — since 19 Aug
- **Decide which children go in the nav vs filter/landing only.** 124 collections do not all belong in a menu. — since 19 Aug
- **`WZ` "Stationery & gifts" overlaps the merch "Cards & Stationery" collection** — two routes to overlapping stock. Needs a call on which wins. — since 19 Aug
- **Inside spreads expectation** — tell him ~1,600 titles is the ceiling, not the catalogue. — since 19 Aug
- **Low-stock threshold** — confirm the number (native default 10 is in place) **and** whether to show the exact count ("3 left") or the generic "Low stock" (currently generic). — since 18 Aug
- **Trust strip copy** — returns window + delivery tiers to replace the `Returns [TBC]` placeholder, and confirm "Free UK delivery over £20" (**the announcement bar says £20, the June mockup said £25** — they contradict). — since 18 Aug
- **Author link target** — there is no author collection or facet, so `/search?q=` is the only natively resolvable target. — since 18 Aug
- **Clickable Publisher deferred** — `custom.publisher` has no native link target. Imprint is done via `product.vendor` → `/collections/vendors?q=`. — since 18 Aug
- **Remaining "Website Points" items** — he said 12 Aug he would come back.
- **Older open decisions:** main-nav picks; Mixed-media product (126 titles, absent from his 28 May combine list); Trajan Pro licensing; behaviour for future-dated titles; policy-page facts (registered address, company + VAT numbers, returns window, who pays return postage, delivery tiers/rates, despatch cut-off, UK-only vs international); catalogue count nod.
- **Discounts** — expects a follow-up. He believed the 25% RRP automation was live; corrected 12 Aug to agreed-but-not-built, blocked on PUBCODE values landing.
- **Security recommendation** — names.co.uk password was sent plaintext and is weak. Recommend he rotates it and enables 2FA **before go-live**.
- **Product-page preview + go-live framing.** Owed since 20 Jul. **The page is now presentable** — send it once the panel/spacing tune under OURS is done.
- **Ebook exclusion scope.** He excluded ONIX 14 (Digital, delivered electronically) but not 21 (Electronic book text) or 20 (E-book reader). One-line question: should 21 also be excluded?

## Open loops — FRED
- **Delta (changed-only) stock feed.** Awaiting since ~20 Jul. At ~50.5k products a full nightly snapshot against the ~5k variant-updates/hour ceiling will not fit the 02:00 window. Not a hard go-live blocker (full-file path proven end-to-end), but the maths does not work at this scale.

## Open loops — OURS
- **Hero/band vertical air** — the hero and the Synopsis tabs read as joined. Band top padding 32 → ~72, or add bottom padding on `product-information`. One number. — next session
- **Cover fill in the panel** — the cover may sit small inside the 460×560 panel. Try image `max-height: 500px`, or a 440×540 panel. **Check on a wide-format art book**, not just a standard trade paperback. — next session
- **Remove the inert `max-width: 720px` on `.gazelle-band__details`** — dead at a 672px column. Next time that file is open.
- **`gazelle-buy-box-styles` snippet** — `.gz-imprint` uppercase tracked 0.75rem, `.gz-author` slightly muted. The only remaining custom CSS for the buy box. — next session
- **Stock-indicator colour tokens** — `--color-instock` / `--color-lowstock` / `--color-outofstock` are still Horizon defaults (grey dot). Set them to the brand traffic-light colours. — next session
- **Mobile trust strip** — the three inner Groups have "Vertical on mobile" ON, stacking icon above text. Set it OFF on all three. Editor, ~2 min.
- **Synopsis "Read more" clamp** (~10 lines) in the detail-band IIFE. — parked
- **DECISION STILL OWED: is Claude Code auto mode / agent-executed live pushes acceptable?** Given GSD Gazelle Build is the **published** theme, an agent-executed push would be live to anyone with the store password. Switch auto mode off and write the policy down.
- **Holding page** — customise `templates/password.liquid`: logo, "New bookshop launching late August", consider email capture. Password stays ON until launch.
- **EAN product URLs** — bulk handle rename pre-launch (`/products/<13-digit EAN>`). Confirmed safe from clobber. Still blocked on the duplicate barcodes. **Check first whether Dave's newer pushes already produce EAN-shaped handles** — UNCONFIRMED.
- **Exclusion mechanism is now permanent, not a one-off** — Billy sends EAN lists, we archive same day by script. Automatable by pubcode once `custom.pubcode` carries values.
- **Build the subject nav menu.** `write_online_store_navigation` scope held, so scriptable. Gated on Billy's labels AND his nav-vs-filter call. Kills the **"Catagories" typo** in the placeholder menu — that must not ship.
- **Maintenance: re-run `scripts/populate_thema_top.py <export> --full` after ANY Dave load.** Neither subject tier is self-maintaining. Read the `scripts/out/thema_l2_counts.csv` it writes; create or drop collections by hand if a group crosses 24. **24 is a create-time rule, not a delete trigger.**
- **UNCONFIRMED whether these were done in the 11 Aug session** — verify before assuming: Format and Subject filters added in Search & Discovery; the 4 policy pages pasted into admin.
- **Queued front-end work, no dependencies:** New Release ribbon (blocked on `publication_date` type); price display (gated on Billy); Press & Reviews (gated); Subject links (now have real targets — 150 collections); PDF catalogue section (contracted); placeholder content pages; checkout styling; notification email templates.
- **SFTP scheduled pickup in Matrixify.** Wire it and watch it fire once — the only untested part of the pipeline. Not started.
- **Paid Matrixify tier.** Demo won't run production. Blocked on Fred's delta answer.
- **Send-receipt flip.** Billy wants TRUE. Hold FALSE until launch, then verify one-email-per-parcel with notifications on before flipping.
- **Metafield type migration (deferred, not blocking).** `publication_date` → Date (still 0% ISO — blocks the New-Release rule), plus `author`, `thema_subjects`, `bic_subjects`, `bisac_subjects`, `main_subjects` → list types. Tool built and committed (`update_gazelle_metafield_types.py`, never run). TRAP: pipes occur inside legitimate content — any list-splitting must be per-field, never blanket. **Note it still uses `GAZELLE_SHOP` (bare name) while every other script now uses `SHOPIFY_STORE` (full domain).**
- **Monolith carve into `docs/`.** **Carry into the carve:** the live domain is `shop.gazellebookservices.co.uk` — `gazelle-context-working.md` still says `store.gazellebooks.co.uk` at lines 237, 767, 829, 1092; and the Shopify CLI version is **4.6.0**, not the 3.92.1 recorded at line 759. Also fix the domain in `gazelle-tech-stack.md` (claude.ai side, not this repo).

## Housekeeping
- **⚠️ CREDENTIALS: all scripts run under the "GSD Gazelle Scripts" app** (client ID `9c1cdb65353e42b36432a5d185e24199`, 26 scopes). **NEVER run our scripts under "BooksoniX Integration"** — that is Dave's and lacks `write_publications`, so it cannot publish a collection. **19 Aug: the BooksoniX client id and secret were found exported in the environment Claude Code inherits** — check what a terminal is carrying before running anything, because the app a script authenticates as is decided by what is exported, not by intent. `verify_l2.py` hard-refuses that client id. Secret-rotation item CLOSED: scripts moved to a separate app, the BooksoniX secret was untouched and has never been committed to git.
- **⚠️ EXPORT INTEGRITY: unique Handle count must equal the All Books count in admin before an export is trusted.** The 18 Aug export held 32,708 of 50,523 and looked healthy; it was discarded.
- **⚠️ NEVER use Shopify's platform Custom CSS field** (`config/settings_data.json` → `platform_customizations.custom_css`). Invisible in the theme files; cost a full session on 18 Aug. **If layout misbehaves inexplicably, check it FIRST.** Clearing it in the editor did not take — push with `shopify theme push --only config/settings_data.json`.
- **GSD Gazelle Build #205873021277 is the ACTIVE/PUBLISHED theme** on the dev store (behind password). Every editor save and every CLI push is live to anyone with the password.
- **`origin` is SSH** (`git@github.com:gsdworks/gazelle-horizon.git`).
- **Live domain is `shop.gazellebookservices.co.uk`** — agreed 3 Feb 2026, reconfirmed by Billy 13 Aug.
- **Smart collections on metafields: "is equal to" only.** Prefix matching is impossible — derive the exact value and store it. This is why `thema_top` and `thema_l2` exist, and why `pubcode`'s value format must be checked before anything is wired to it.
- **`metafieldsSet` caps at 25 metafields per call** — two fields per product means 12 products per batch. Raising it silently truncates.
- **Run glob scripts against an isolated folder, never Downloads.** Current exports live in `~/Downloads/export-19aug`. Mac system Python is 3.9 with old pip; consider brew Python.
- **Tick the Tags column in Matrixify export settings** — missing again on 11 Aug, which silently removes any ability to check PUBCODE.
- **Gmail connector is NOT trustworthy for negative results.** A search returning nothing is not evidence of silence — verify with `get_thread` on a known thread.
- **Run a digest after any client exchange that changes state**, not only at session end.
- Store is unbuyable until Fred's stock feed runs — inventory qty=0 store-wide (tracked, policy deny). Known cause, not Dave.
- `custom.format` and `custom.genre` — 2 products each, undefined keys not in the contract. Unexplained. Clean when convenient.
- Handles carrying a `-N` suffix are **not** in themselves a finding — but the handle/`-1` duplicate-barcode pairs ARE. Don't conflate the two.
- Shopify CLI now **4.6.0**. If a CLI command behaves oddly for no reason, check the version first.
- Gazelle is a **fork** of `Shopify/horizon` and is the only one there will ever be. Future GSD projects use a plain repo + mirror-push + `upstream` remote. Do not "harmonise" Gazelle to that shape.
- Context system: drag PROJECT-CONTEXT.md into claude.ai project knowledge after each `/update-context`.
