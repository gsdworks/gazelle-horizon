# STATUS — Gazelle Books

_The "now" list. Open loops and next actions only. Completed work lives in DONE.md._
_Last updated: 18 August 2026_

## OVERDUE — was committed for Friday 14 August, verify what actually ran
1. **Archive job** — four full publishers (BZ4 Edition Skylight, DB7 Tomas Horych, CU2 Jan Kowalewicz, DD2 U-Line) by pubcode substring in `tags_global` + vendor-name cross-check, plus the Edition Reuss 55 by barcode. Log counts per publisher, report the numbers to Billy. Input is `scripts/EditionReuss.xls`. **Fragile until Dave answers whether his push can un-archive.** UNCONFIRMED whether this ran on 14 Aug — check before re-running.
2. **Discounts follow-up to Billy** — needs Grant's commercial decision (quote separately vs absorb; flagged out-of-SOW in June). Billy expected it by end of that week.
3. **Domain / holding page confirmation to Billy.**

## Blocking go-live
- **DOMAIN — `shop.gazellebookservices.co.uk` serves "This store is unavailable".** Attached to the OLD Gazelle store whose subscription lapsed in July. **DNS CNAME is already correct → do NOT change any DNS record**; the fix is Shopify-side attachment. Order: (a) check the `gazelle-books-2026` plan status FIRST — a dev-plan gate blocks custom domains and makes it a Billy billing conversation; (b) Settings → Domains → Connect existing domain; (c) if "in use by another store", check Grant's password manager for the old store's admin login (Grant built its holding page 1 Apr 2026); (d) else Shopify support release via TXT record — names.co.uk access is held (`marvin@gazellebookservices.co.uk`, credentials in Billy's 3 Feb "Domain" email).
- **DAVE — CRITICAL: can an update push flip an archived product back to active?** If yes, the archive job silently undoes itself and erotic titles reappear on a live store. Unanswered.
- **DAVE — re-push the 1,057-product stale cohort.** One cohort carries every remaining data defect (overlapping: 934 blank Product Type, 548 Thema-as-names, 529 placeholder dimensions, 342 `__line:` series tokens). CSV with per-defect flags emailed 11 Aug. Chase now — no reply.
- **DAVE — duplicate barcodes are integration-created and the hazard is live.** 20 duplicates across 42 products, handle/`-1` pairs; test stock seen landing on the WRONG listing. Asked 11 Aug what causes it. **Fix the cause before deleting anything Shopify-side.** Also gates the EAN-handle rename.

## Open loops — DAVE (send as ONE bundled email)
New asks:
- **Exclude pubcodes BZ4, DB7, CU2, DD2 at source** so the erotic titles cannot return on a re-push.
- **Un-archive question** (see Blocking).
- **Handle generation** — is `handle` create-only or in the update payload? Can he emit EAN handles for new pushes?
- **NEW 18 Aug — three source-data defects:** (1) **Liberty Fund** synopses have en dashes and apostrophes stripped ("17151766", "Gods", "Englands") — per-publisher, other publishers are intact, so not a global encoding fault; (2) **Goose Lane** synopsis has the prize line jammed onto the description with the paragraph break lost ("…Historical WritingWhat happened…"); (3) `main_subjects` value "Mind, body & spirit" comma-splits into three chips — a comma inside a legitimate value is being treated as a delimiter.
Already with him, awaiting response:
- **Duplication cause** — 42 duplicates / 20 barcode groups, sent 11 Aug.
- **Image failure diagnosis** — with him since **9 Jul**, silent since. 4,614 products (9.6%) have no cover; failing at Shopify fetch.
- **Taxable flag** — 312 products, file sent 11 Aug. Books should not be taxable.
- **Internal spreads syncing** — only 64 of ~48k products have 2+ images. His record contradicts itself: "covers only" (Feb) vs "now syncing" (Jul).
- **Archived titles** — approved-only filter + retro-sweep (asked 16 Jul), archive-not-delete (asked 3 Jul).
- **Add `thema_top` to his push** — one line his side; until then every new product misses the subject collections.
- **Escalation lever if silence continues: Paul Theijs.**

Carried, lower priority:
- **Load completion / catalogue count UNCONFIRMED.** API reports 49,363 (later 49,367) vs 48,220 in the same-morning export — ~1,143 gap, cause UNCONFIRMED (export likely ran mid-sync).
- **All products active and published; draft-on-create not operating.** **Verify against the email record before raising** — UNCONFIRMED whether this was ever put to Dave in writing.
- **255 future-dated titles are live.** Same UNCONFIRMED caveat. Billy's answer on desired behaviour still owed.
- **Nova Science publisher name has 3 variants across ~20k products** — fragments the imprint filter. Source normalisation, not urgent.

## Open loops — BILLY
- **Low-stock threshold** — confirm the number (native default 10 is in place) **and** whether to show the exact count ("3 left") or the generic "Low stock" (currently generic). — since 18 Aug
- **Trust strip copy** — returns window + delivery tiers to replace the `Returns [TBC]` placeholder, and confirm "Free UK delivery over £20" (**the announcement bar says £20, the June mockup said £25** — they contradict). — since 18 Aug
- **Author link target** — there is no author collection or facet, so `/search?q=` is the only natively resolvable target. — since 18 Aug
- **Clickable Publisher deferred** — `custom.publisher` has no native link target (no publisher facet, no publisher collection). Imprint is done via `product.vendor` → `/collections/vendors?q=`. Needs a facet or a collection scheme before Publisher can be linked. — since 18 Aug
- **Remaining "Website Points" items** — he said 12 Aug he would come back.
- **Older open decisions:** subject nav labels + main-nav picks; Mixed-media product (126 titles, absent from his 28 May combine list); Trajan Pro licensing; behaviour for future-dated titles; policy-page facts (registered address, company + VAT numbers, returns window, who pays return postage, delivery tiers/rates, despatch cut-off, UK-only vs international); catalogue count nod.
- **Discounts** — expects a follow-up. He believed the 25% RRP automation was live; corrected 12 Aug to agreed-but-not-built, blocked on PUBCODE.
- **Security recommendation** — names.co.uk password was sent plaintext and is weak. Recommend he rotates it and enables 2FA **before go-live**.
- **Product-page preview + go-live framing.** Owed since 20 Jul.
- **Ebook exclusion scope.** He excluded ONIX 14 (Digital, delivered electronically) but not 21 (Electronic book text) or 20 (E-book reader). One-line question: should 21 also be excluded?

## Open loops — FRED
- **Delta (changed-only) stock feed.** Awaiting since ~20 Jul. At ~49.4k products a full nightly snapshot against the ~5k variant-updates/hour ceiling will not fit the 02:00 window. Not a hard go-live blocker (full-file path proven end-to-end), but the maths does not work at this scale.

## Open loops — OURS
- **`gazelle-buy-box-styles` snippet** — `.gz-imprint` uppercase tracked 0.75rem, `.gz-author` slightly muted. The only remaining custom CSS for the buy box; needed because the imprint and author rows had to become custom-liquid blocks (rich-text strips Liquid links), which forfeits their native typography settings. — next session
- **Stock-indicator colour tokens** — `--color-instock` / `--color-lowstock` / `--color-outofstock` are still Horizon defaults (grey dot). Set them to the brand traffic-light colours. — next session
- **Mobile trust strip** — the three inner Groups have "Vertical on mobile" ON, stacking icon above text. Set it OFF on all three. Editor, ~2 min.
- **Synopsis "Read more" clamp** (~10 lines) in the detail-band IIFE. — parked
- **DECISION TO WRITE DOWN: is Claude Code auto mode / agent-executed live pushes acceptable?** Auto mode was accidentally enabled on 18 Aug. Given GSD Gazelle Build is the **published** theme, an agent-executed push is live to anyone with the store password. Switch auto mode off and record the policy.
- **Holding page** — customise `templates/password.liquid`: logo, "New bookshop launching late August" (matches the marketing site), consider email capture. Password stays ON until launch.
- **EAN product URLs** — bulk handle rename pre-launch (`/products/<13-digit EAN>`, mirroring the old site's `/product/<EAN>`). Blocked on duplicate barcodes + Dave's handle answer. **Check first whether Dave's newer pushes already emit EAN handles** — the `inferno-1` / `9781585101139` pairs suggest they might, which would shrink the job to the legacy cohort only. UNCONFIRMED.
- **Exclusion mechanism is now permanent, not a one-off** — Billy sends EAN lists, we archive same day by script. Same route for publishers leaving Gazelle. Automatable by pubcode once PUBCODE is a discrete metafield.
- **Build the subject nav menu.** `write_online_store_navigation` scope held, so scriptable. Gated on Billy's labels. Kills the **"Catagories" typo** in the placeholder menu — that must not ship.
- **Re-run `scripts/populate_thema_top.py`** after Dave's re-push, against a fresh export, to sweep in the stale cohort and the ~1,143 export-gap products.
- **UNCONFIRMED whether these were done in the 11 Aug session** — verify before assuming: Format and Subject filters added in Search & Discovery; the 4 policy pages pasted into admin.
- **Queued front-end work, no dependencies:** New Release ribbon (blocked on `publication_date` type); price display (gated on Billy); Press & Reviews (gated); Subject links (taxonomy); PDF catalogue section (contracted); placeholder content pages; checkout styling; notification email templates.
- **SFTP scheduled pickup in Matrixify.** Wire it and watch it fire once — the only untested part of the pipeline. Not started.
- **Paid Matrixify tier.** Demo won't run production. Blocked on Fred's delta answer.
- **Send-receipt flip.** Billy wants TRUE. Hold FALSE until launch, then verify one-email-per-parcel with notifications on before flipping.
- **Metafield type migration (deferred, not blocking).** Minimal confirmed list: `publication_date` → Date (still 0% ISO — blocks the New-Release rule), plus `author`, `thema_subjects`, `bic_subjects`, `bisac_subjects`, `main_subjects` → list types. Tool built and committed (`update_gazelle_metafield_types.py`, never run). TRAP: pipes occur inside legitimate content — any list-splitting must be per-field, never blanket.
- **Monolith carve into `docs/`.** **Carry into the carve:** the live domain is `shop.gazellebookservices.co.uk` — `gazelle-context-working.md` still says `store.gazellebooks.co.uk` at lines 237, 767, 829, 1092; and the Shopify CLI version is **4.6.0**, not the 3.92.1 recorded at line 759. Also fix the domain in `gazelle-tech-stack.md` (claude.ai side, not this repo).

## Housekeeping
- **⚠️ NEVER use Shopify's platform Custom CSS field** (`config/settings_data.json` → `platform_customizations.custom_css`). It injects an inline `<style>` at the end of `<body>`, invisible in the theme files, and it cost a full session on 18 Aug. **If layout misbehaves inexplicably, check it FIRST.** Clearing it in the editor did not take — push with `shopify theme push --only config/settings_data.json`.
- **GSD Gazelle Build #205873021277 is the ACTIVE/PUBLISHED theme** on the dev store (behind password). Every editor save and every CLI push is live to anyone with the password.
- **`origin` is now SSH** (`git@github.com:gsdworks/gazelle-horizon.git`) — the old "HTTPS push fails, use GitHub Desktop" constraint no longer applies.
- **Live domain is `shop.gazellebookservices.co.uk`** — agreed 3 Feb 2026, reconfirmed by Billy 13 Aug. `store.gazellebooks.co.uk` was never the target; it was a stale string carried for six months.
- **Scripts authenticate via the "GSD Scripts" custom app** (Dev Dashboard + client credentials grant). No static tokens — every run exchanges client id/secret for a short-lived token. Legacy Settings custom apps deprecated 1 Jan 2026.
- **Smart collections on metafields: "is equal to" only.** `list.single_line_text_field` works (equals matches any list entry) and the definition needs the `smartCollectionCondition` capability. Prefix matching is impossible — derive the exact value instead. This is why `thema_top` exists.
- **Run glob scripts against an isolated folder, never Downloads** — 127 accumulated CSVs there, and one stale non-UTF-8 file crashed a run. Current exports live in `~/Downloads/export-11aug`. Mac system Python is 3.9 with old pip (no `--break-system-packages`); consider brew Python.
- **Tick the Tags column in Matrixify export settings** — missing again on 11 Aug, which silently removes any ability to check PUBCODE.
- **Gmail connector is NOT trustworthy for negative results on this project.** A search returning nothing is not evidence of silence — verify with `get_thread` on a known thread before concluding a client hasn't replied.
- **Run a digest after any client exchange that changes state**, not only at session end.
- Store is unbuyable until Fred's stock feed runs — inventory qty=0 store-wide (tracked, policy deny). Known cause, not Dave.
- Native Tags blank — PUBCODE remains buried inside `tags_global`. Homepage curation, discount automation and automated pubcode exclusion ALL block on surfacing it discretely.
- `custom.format` and `custom.genre` — 2 products each, undefined keys not in the 23-field contract. Unexplained. Clean when convenient.
- Handles carrying a `-N` suffix are **not** in themselves a finding — but the handle/`-1` duplicate-barcode pairs ARE. Don't conflate the two.
- BooksoniX Integration app client secret may have been rotated by Dave — UNVERIFIED.
- Shopify CLI now **4.6.0**. If a CLI command behaves oddly for no reason, check the version first.
- Gazelle is a **fork** of `Shopify/horizon` and is the only one there will ever be (one fork per upstream per account). Future GSD projects use a plain repo + mirror-push + `upstream` remote. Do not "harmonise" Gazelle to that shape.
- Context system: drag PROJECT-CONTEXT.md into claude.ai project knowledge after each `/update-context`.
