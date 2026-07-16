# ⭐ THIS FILE IS THE MASTER SOURCE OF TRUTH — read this first

**Status & purpose.** This document is the canonical operating record for the Gazelle build AND for a new way of working that Bowden Studio intends to standardise across future clients. It is deliberately maintained rigorously and improved on a near-daily basis. It captures two layers: (1) **project/brand state** — Gazelle-specific people, decisions, brand, integration, build progress; and (2) **operational methodology** — how we work: native-first, the Claude Code collaboration loop, git/theme discipline, the reusable process. Layer (2) is the seed of a repeatable Bowden operating model.

**The capture discipline (applies every session).** Treat recording *how to work better* as a first-class task alongside the build itself. Any new working method, tool, technique, decision, or hard-won lesson gets logged here the moment it emerges — do not let learnings evaporate in chat. Edits are surgical (`str_replace`), never overwrite confirmed decisions, always update the timestamp line.

**⚠️ THE LOAD-BEARING DISCIPLINE — re-upload.** This file's own history proves the single biggest risk is the **re-upload lag**: edits get made but not re-uploaded to project knowledge, so a stale copy mounts in the next session and work gets silently re-buried (this caused a real regression). A master-source-of-truth doc that goes stale is worse than none. So: **after every edit, re-upload to project knowledge immediately.** Every session, before editing, verify the timestamp line and line count look current.

**🔮 Forward-looking architectural note (revisit at NEXT-PROJECT kickoff — do NOT act yet).** This single file currently does two jobs: operational methodology (reusable, client-agnostic) and project/brand record (Gazelle-only). While it's one active project that's fine. But when a second client begins, we should **re-evaluate splitting this into two files**: a shared **operational/methodology MD** (the Bowden way of working — becomes the reusable template) and a separate **per-client brand/project MD**. Flagged now so the intent isn't lost; the actual split is a next-project decision, not a now decision.

---

_Last updated: Thursday, 16 July 2026, ~12:00pm BST — **CAROUSEL BLEED FIXED + FRED FILES RECONCILED (see the 16 July note + Session log).** Featured Collection carousel now contained to 1200px (6 cards + peek, was ~8.5 and cut off). **The 14 July diagnosis was WRONG and is corrected below:** it is NOT a `--section-slide-width` calc bug. `snippets/resource-list.liquid` hard-codes the **`force-full-width`** class on the carousel wrapper, and core's `.section > .force-full-width { grid-column: 1 / -1 }` spans all three grid columns — so the track is viewport-width **by native design**, and the calc's `100%` resolving against it is the SYMPTOM not the cause. **Native-first properly exhausted:** `section_width: page-width` is set and it breaks out anyway — `force-full-width` is applied **unconditionally** for `layout_type: carousel`, there is NO native toggle (confirmed in the editor, not inferred from files). Fix added to the EXISTING `gazelle-layout.liquid`: `grid-column: 2` + `--util-page-margin-offset: 0px`, scoped to `.section-resource-list`, specificity 0,3,0 beats core's 0,2,0, no `!important`, peek preserved. **⚠️ THE PROCESS LESSON (the expensive one): Claude Code diagnosed against a STALE local `index.json`** — it read `columns: 4, max_products: 8` while the editor had been 6/12 since 14 July, so every number in its report was built on fiction. Caught by an editor screenshot, not by the file trace. **NEW RULE: pull before any DIAGNOSTIC that reads editor-owned JSON, not just before edits — pull-clobber is a read-accuracy rule as well as a write-safety rule.** **Fred reconciled (was a week stale):** the stock file ARRIVED and is named **`GazelleAvailability_YYYYMMDD.csv`, NOT `GazelleStock`** — confirmed clean, 01:29 daily, import 02:00; tracking file also confirmed clean. **Billy's real homepage artwork is IN** (hero Broadview/Kodama/PMI, focus Debrett's/Marian/Right Book, strip Montagud) — the last big Phase 1 unknown is closed. **RE-UPLOAD TO PROJECT KNOWLEDGE IMMEDIATELY.** — Earlier: 14 July, ~5:00pm: **HEADER BUILT + GLOBAL PAGE-WIDTH FIX (see the 14 July PM note + Session log).** Header done native-first (config + tokens, no custom section, possibly ZERO custom CSS): logo-left, inline nav (Menu row Top), native search/account/basket icons, Scheme 1 Paper, announcement bar live. Deviations flagged for Billy: native icons vs mockup's "Account"/"Basket (0)" text labels; GBP/localization turned OFF (UK-only). Nav still shows OLD placeholder menu incl. "Catagories" typo — do NOT ship; real labels gated on taxonomy. **New `snippets/gazelle-layout.liquid` = THE single global source of page width (1200px)** — overrides `--page-content-width` on `body.page-width-narrow`, Horizon's native calc derives `--page-width` from it; product-page local `--page-width` override removed (commits `f57cc9c` + `eb11f15`). **Platform lessons banked:** `--page-width` lives on `<body>` via `.page-width-*` classes NOT `:root` (so `:root` overrides are INERT — target the body class); override `--page-content-width` not `--page-width` so both agree and carousel/edge components align; narrow preset is really **90rem = 1440px** (not the ~1400 we'd been saying). **Known gaps logged:** `.blog-posts` redeclares width on its own element (stays 1440, core file — fix via scoped section IF blogs kept); `gazelle-focus.liquid` has pre-existing img width/height theme-check errors (pick up in homepage session); **Featured Collection carousel bleeds past 1200 — OPEN, and it's a CONFIRMED requirement not cosmetic** (Billy wants the Waterstones-style 6-then-arrow-6 carousel the mockups copy; diagnosis + fix path in On The Horizon) **[✅ RESOLVED 16 July — and that diagnosis was wrong; see the 16 July note.]**. **Build sequencing decided:** header (placeholders) → subject-distribution analysis → taxonomy proposal to Billy → collections → nested nav lights up the (never-mocked) mega menu. **RE-UPLOAD TO PROJECT KNOWLEDGE IMMEDIATELY.** — Earlier: 14 July, ~3:15pm: **FOOTER BUILT + STYLED TO MOCKUP (see the 14 July note + Session log): native four-column footer + utilities bar, one new style-only section (`gazelle-footer-styles`). Five platform lessons banked: runtime `block.id` ≠ JSON key; `custom-liquid` NOT whitelisted in the footer; pull-clobber extends to Claude's own section files (push-before-pull when local is ahead); rich-text `<br>`/`<p>` storage quirks (`::first-line` workaround, no `::last-line` exists); footer grid caps at 4 top-level blocks.** — Earlier: 8 July, ~5:00pm: **PRODUCT PAGE BUILT (see the 8 July note + Session log): bottom band (tabs/accordion + specs + subjects/classification rail), cover treatment, hero layout. Pull-clobber lessons banked. Dave emailed (dimensions bug + raw classification codes, cc Billy).** — Earlier: 7 July 10pm: collection page + colours + filters done; master-source-of-truth preamble + Claude Code ways-of-working added.** See the two 7-July evening notes below and the Session log for detail. — Earlier: reconciliation pass across all chats since 1 July. **Caught a re-buried regression:** the 2 July project-knowledge copy still showed the outbound order file as A–V ("Bill To requirement now MET"), because the 1 July edit that recorded Fred's A–N reversal was never re-uploaded, and the 2 July Claude Code session edited the older 27-June base. Fixed here: outbound is **A–N (ship-to only), an open regression vs Billy's dual-address requirement**. Also updated this pass: inbound **tracking v3 confirmed** (5 fields, daily 18:00, Matrixify 18:30); **Matrixify plan-tier resolved** (daily batch, no folder-watch tier); new **daily stock file** specced and in flight with Fred; BooksoniX **inside spreads now syncing** and **ISBN-13 confirmed in variant barcode** (both spot-check pending); new **archived-titles-showing-as-Active** issue on Dave. Also added this pass: a standing **NATIVE-FIRST build philosophy** (see section) — max out-of-the-box Horizon, custom only where a confirmed requirement forces it, Claude Code kept tightly scoped; applies at every build stage. **Later same day — field-mapping reconciliation vs the live export:** expanded the Metafields subsection to the full Billy-approved set (from `gazelle-field-mapping-FINAL.xlsx`) with type corrections — Date type for `publication_date`, list types for pipe-delimited `author`/subjects/`author_bio`, discrete `custom.pubcode`, integer/dimension for pages/dims — plus source-data flags (weight junk, empty Gazelle Price) and a flag that Dave's integration still _deletes_ (not archives) on BooksoniX archive. **Brand fonts confirmed via DevTools on the Webflow site (7 July):** headings/buttons = Trajan Pro, body = Switzer (free via Fontshare); build uses Cinzel stand-in for Trajan for now; Fraunces/Figtree dropped; less-all-caps-vs-brand-site conflict flagged for Billy. Merged onto the correct 712-line base (a stale 671-line copy had mounted — see the KNOWN UI BUG note in Document History). **Later still (this session) — Step 1 EXECUTED:** the 18 metafield definitions bulk-created via Admin API (script `create_gazelle_metafields.py`, `created=18 failed=0`) and verified against a live title — caught two Dave bugs (width_mm/height_mm landing as literal `%sh_…%` placeholders; main_subjects `&`/`and` duplication), confirmed PUBCODE lands in tags_global (2nd publisher), and confirmed publication_date was created as text not Date. Step 1 closed; next is smart collections + New-Release rule. **RE-UPLOAD TO PROJECT KNOWLEDGE IMMEDIATELY** — the lag is what caused the re-buried regression. (Prior: 2 July — front-end Liquid build started, product card committed. 1 July — Fred's A–N reversal + tracking v3 [this edit was lost]. 27 June — EZ Exporter/Matrixify findings. 22 June — consolidation.)_

_**7 July (evening) — FONTS DONE + BUILD LOG ADDED + theme consolidated.** Self-hosted both brand fonts live: Switzer (body, woff2) + Cinzel (headings, ttf), via `snippets/gazelle-fonts.liquid` overriding `--font-body--family`/`--font-heading--family`; the `theme.liquid` render hook is a logged core-file exception in CLAUDE.md. Theme housekeeping: consolidated a mess of near-identically-named dev themes onto one clean **"GSD Gazelle Build July 7th"** (published live), deleted the stale ones, kept "Horizon" as base reference — **push target going forward is the GSD theme.** Hard-won git lessons banked (see Build Log): `theme pull` wipes UNCOMMITTED files so commit-before-pull; two same-named themes caused a mis-push (why the rename mattered); `GIT_PAGER=cat` to dodge the pager. **Added a full BUILD LOG & DELIVERY PLAN section** (after the Claude Code build section) — captures Grant's confirmed phase order (VISUAL first → product data → Fred feeds), a page/component tracker, and a complete pre-launch checklist (front-end / back-end-data / feeds / go-live). **Current focus: Phase 1 visual — get product/collection/home/header/footer 80–90% there so Billy can sign off in parallel.** Product page IN PROGRESS now, native-first, building Gazelle-price-only (struck-RRP display still UNANSWERED by Billy — checked inbox 7 July, only the 25% automation thread exists, not the display decision). RE-UPLOAD TO PROJECT KNOWLEDGE._

_**7 July (later evening) — COLLECTION PAGE DONE + COLOURS DONE + FILTERS DONE.** Built both **brand colour schemes** in the theme editor (Scheme 1 Paper site-wide, Scheme 5 Charcoal footer) — lifted every page on-brand at once. **Collection page reached Phase-1 done, native-first with ~zero custom CSS:** card was already wired via `custom-liquid` override; flipped filters to vertical sidebar + pagination to numbered + set grid gaps (all native editor settings); hero uses native title + native per-collection description (dropped the static "Browse by Subject" eyebrow). Configured **Search & Discovery** filters (Format ← product type, Imprint ← vendor, Price kept, Availability removed) — app-side, no pull needed. Two discoveries banked (see Session log): **format-combining can be done natively in S&D grouped-values** (may take that job off Dave), and **demo covers need curating before Billy** (confronting/broken test covers). Pulled editor changes + committed (`d39b900`). Product page is the next and biggest Phase-1 page — left for a fresh session. **⭐ Open TODO: write the detailed CLAUDE.md workflow section (native-first loop, agent leash, git/theme rules, editor-vs-code split, schema-first, and the "draw mockups within Horizon's native capabilities" principle) — intended as the seed for a reusable Bowden template. Full spec in the Session log below.** RE-UPLOAD TO PROJECT KNOWLEDGE._

_**8 July — PRODUCT PAGE BUILT (both bands, one full-day session).** **Bottom band:** `gazelle-book-specs.liquid` specs table (all confirmed metafields wired, `.value` on every one; dimensions deliberately un-guarded so Dave's `%sh_%` bug shows live as evidence) + `sections/gazelle-book-detail-band.liquid` — custom two-column band replacing the earlier native accordion: LEFT = **tabs on desktop / accordion on mobile** (Synopsis, About the Author [auto-hidden when empty], Product Details reusing the specs snippet; **first custom JS in the build** — scoped IIFE, single markup, a11y-correct), RIGHT = extensible rail with **Subjects card** (`main_subjects`, comma-split chips) + **Classification card** (Thema/BIC/BISAC code-groups). **Top band (cover + hero):** `gazelle-cover-styles.liquid` — covers at **fixed 570px height / natural width** (Grant: consistent height, width varies), **left-aligned flush to the Synopsis gutter**, 1px charcoal border + light shadow (spine dropped as gimmicky); hero grid rebalanced to the mockup's **proportional `minmax(300px,1fr) minmax(0,1.15fr)`** pair (killed the dead-middle-gap / buy-box-pinned-right problem) and buy box right edge inset 24px to align with the Subjects card — **all four content edges now key off the same `--gz-gutter` 24px**. **Hard-won learnings (full detail in 8 July Session log):** the ⚠️ **PULL-CLOBBER pattern** (bit us 3× — custom-liquid render blocks in `product.json` get wiped by pulls until committed; new rules below), the **metafield `.value` rule**, the **1400-vs-1200 page-width mismatch** (`page_width: narrow` = 1400; hero constrained to 1200), the **media overflow-clip** (theme clips shadows), the **`media_fit` dead-setting quirk**, and the **diagnostic-first Claude Code method** (read-only diagnose → exact fix; every blind guess swung wrong, every diagnostic landed). **Data findings for Dave (email drafted 8 July, cc Billy):** dimensions `%sh_height_mm%`/`%sh_width_mm%` live on page; Thema/BIC/BISAC contain decoded NAMES not raw codes (Classification card currently duplicates Subjects — needs raw codes for trade buyers). **Product page still to do:** buy-box supporting elements (subtitle, author line, imprint/publisher, trust strip), New Release ribbon (Billy wants it — deferred, don't drop), price display (gated Billy), Press & Reviews + Subject links (gated). **Same-day update (16:49): Billy CONFIRMED raw codes over names AND ruled "we don't need to show BISAC, BIC & THEMA are sufficient" — tiny front-end follow-up: remove the BISAC code-group from the Classification card.** RE-UPLOAD TO PROJECT KNOWLEDGE._

_**14 July — FOOTER BUILT + STYLED TO MOCKUP (one session).** **Built natively in the editor:** four top-level blocks in the `footer` section — Newsletter **group** (Heading "Newsletter" + copy + email-signup nested INSIDE the group, keeping the top level at exactly 4 blocks — the grid caps at 4 and a 5th triggers orphan-row layout), Menu → `Footer Help`, Menu → `Footer Explore`, Text (company info, three paragraphs: name / address+phone+email / registered line). Native `footer-utilities` bar kept as shipped (copyright + policy-list + social-links). Both sections on Scheme 5 Charcoal. Admin side: `footer-help` + `footer-explore` menus created (Help links point at `/` until content pages exist — accepted); all four policy pages created from Shopify templates (wording review with Gazelle later). Email-signup block: corner radius 100→2, integrated button OFF (stacking done in CSS — the toggle alone doesn't stack). **Styled via ONE new file: `sections/gazelle-footer-styles.liquid`** — a style-only section (emits `{% style %}`, renders no markup, `enabled_on: groups: ["footer"]` + a preset so it appears in Add section), added to the footer group in the editor. Route forced by a schema fact: **`custom-liquid` is NOT whitelisted in `sections/footer.liquid`'s block list** (unlike `_product-card`), so the cover-styles render-block pattern doesn't work in the footer. CSS covers: shared heading treatment (menu headings + newsletter heading + company first line — Cinzel 13px/700/.2em/uppercase/`#e8e1d2`), menu links (15.5px `#c4bfb2` → `#fff` hover), company body (15px/1.85), reg line (12.5px `#6e6a60`, own `<p>`), newsletter copy (14.5px `#8a857a`), stacked signup form (column, input full-width, button fit-content), utilities bar (copyright + policy trigger 12.5px muted). **Hard-won lessons (full detail in 14 July Session log + Key Lessons):** (1) **runtime `block.id` ≠ the JSON key** — `.text-block--<id>` selectors NEVER match; target structural preset classes (`.text-block.paragraph` / `.h3` / `.rte:not(.paragraph)`) instead, with the stated assumption of one text block per preset in the footer; (2) **rich-text editor stores Enter inconsistently** — sometimes `<br/><br/>` inside one `<p>`, sometimes a real `</p><p>` split; the company NAME needed `::first-line` (pinned by the explicit break), the REG line needed a genuine paragraph split because **CSS has no `::last-line`**; (3) ⚠️ **PULL-CLOBBER EXTENDS TO CLAUDE'S OWN SECTION FILES** — a pull mid-session reverted the committed selector fix with the stale theme copy (caught before commit, discarded, re-pushed). New rule: **when local is ahead of the theme, PUSH before any pull**; committed work is recoverable via discard, but never commit a pull-diff without reading its direction. **Accepted deviations from mockup:** policy links render as Horizon's native "Terms and Policies" popover trigger (not four inline links — native pattern, kept); Sign up button roundness inherits the global button style (squaring it is a site-wide decision, parked). **Go-live flags:** copyright pulls the store name (currently "Gazelle Dev" — rename at launch); social URLs still placeholder (real FB/X/IG/LinkedIn needed); policy wording review. Footer tracker row → ✅ DONE. RE-UPLOAD TO PROJECT KNOWLEDGE._

_**14 July (PM) — HEADER BUILT + GLOBAL PAGE-WIDTH FIX (one session).** **Header, native-first, zero custom section:** flipped Logo position → Left, Menu Row → Top (inline nav beside the logo, not stacked below), confirmed Scheme 1, announcement bar already live ("Free UK Delivery on website orders over £20"). Turned **GBP currency selector + localization OFF** (not in mockup, Gazelle is UK-only — one toggle to restore). Native search/account/basket render as **icons**, which we KEPT rather than reproducing the mockup's "Account"/"Basket (0)" text labels (native e-comm pattern; text would be pointless custom CSS) — flag to Billy alongside the footer's "Terms and Policies" popover deviation. May end up a genuinely **zero-CSS header**. Nav is STILL the old Main menu (Home / New Books / Bestsellers / **Catagories** [old-site typo, do NOT ship] / Blogs / Contact) — the placeholder taxonomy set was not wired; it's an admin → Navigation job with zero theme work whenever the labels are decided. **Mega menu realisation:** Horizon renders one automatically when a nav item has child links — it is NOT a separate build, just a nested Navigation structure. Never appeared in the June mockups (all flat nav), so its content is an open design question for Billy. **GLOBAL PAGE-WIDTH FIX (the session's real engineering):** the header sat wider than the 1200px hero because Horizon's `page_width: narrow` preset = **1440px** while all mockups + gazelle sections are 1200 — the same mismatch the product-page hero patched locally on 8 July. Claude Code Phase-1 read-only diagnosis found the key fact: **`--page-width` is declared on `<body>` via the `.page-width-narrow` class, NOT on `:root`** — so a `:root` override is inert (element-level decl beats inherited). Fix (commits `f57cc9c` then `eb11f15`): new **`snippets/gazelle-layout.liquid`** (style-only, render-hooked in `theme.liquid` next to `gazelle-fonts`) sets **`--page-content-width: 1200px` on `body.page-width-narrow`** — deliberately overriding CONTENT-width (not page-width) so Horizon's native `calc()` derives `--page-width` from it and both agree; scoped to the narrow class on purpose so the editor Page-width setting stays a live escape hatch. Product-page's local `--page-width` override removed (now redundant), replaced with a pointer comment — **`gazelle-layout` is now THE single source of page width.** Theme-check clean, zero new offences. **Featured Collection carousel STILL bleeds** past 1200 after the fix — diagnosed as the native carousel's `--section-slide-width` calc resolving `100%` against the scroller/viewport not the 1200 content box **[❌ THIS DIAGNOSIS WAS WRONG — corrected 16 July: the cause is the unconditional native `force-full-width` class on the carousel wrapper; the calc was the symptom. RESOLVED 16 July, see that note + the Open Items entry. Left here as the historical record, not as fact.]**; this is Billy's **confirmed Waterstones-style requirement** (6 products, arrow to next 6), so it's an open build item, not cosmetic (see On The Horizon). Do NOT kill the right-side "peek" — that's intended affordance. **Claude Code note:** took "I have now updated my credits" as commit approval — reasonable given the message was mid-approval, outcome correct, but strictly not an approval phrase; leash otherwise held all session. RE-UPLOAD TO PROJECT KNOWLEDGE._

_**16 July (AM) — CAROUSEL BLEED FIXED + FRED FILES RECONCILED + BILLY'S ARTWORK LANDED.** **The carousel (the 14 July open item) is DONE and the 14 July diagnosis was WRONG — corrected in place below.** Root cause is NOT a `--section-slide-width` calc bug: `snippets/resource-list.liquid` (L98–113) hard-codes **`force-full-width`** on the outer `div.resource-list.resource-list__carousel` for the carousel branch, and core `base.css:510` does `.section > .force-full-width { grid-column: 1 / -1 }` — spanning all three grid columns (margin | centre | margin), i.e. the viewport. The slide chain is `width:100%` all the way up, so the calc's `100%` resolves against a viewport-width track. **The calc was the symptom; `force-full-width` is the cause.** **Native-first genuinely exhausted, not assumed:** `section_width` is set to `page-width` and it breaks out ANYWAY — the class is unconditional for `layout_type: carousel`, there is **no native toggle**. That was established **in the theme editor** (Grant screenshotted the panel), not from the file trace — the agent never answered the "under what condition is it applied?" question and jumped straight to CSS. **The fix (committed, pushed, live):** added to the EXISTING `snippets/gazelle-layout.liquid` (NOT a new file — it is already the single global source of width truth and already render-hooked; the agent wanted a new file, overruled): `.section-resource-list > .resource-list__carousel.force-full-width { grid-column: 2; --util-page-margin-offset: 0px; }`. `grid-column: 2` undoes the breakout; zeroing `--util-page-margin-offset` cancels the full-bleed first-slide inset (`--gutter-slide-width`) and arrow padding, both sized for a viewport-width track. Specificity **0,3,0 beats core's 0,2,0** — no `!important`. **Peek preserved** (the 48px `--peek-next-slide-size` reservation lives inside the slide-width calc, independent of container width). **Result: 6 cards + a sliver, was ~8.5 and cut off at the right edge.** Verified by render (the honest bar — DevTools computed-value checks were attempted but ran in iPad emulation at 820px, where a 1200px constraint is moot; the desktop render is the evidence). **⚠️ THE SESSION'S REAL LESSON — the agent diagnosed against a stale `index.json`:** its report confidently stated `columns: 4, max_products: 8` and did arithmetic on it ("1200/4 ≈ 269px per card"), but the editor had been **6 / 12 since 14 July** and the local JSON had never been pulled. Every number was fiction. It was caught by an **editor screenshot**, not by the file trace. **NEW RULE: pull before any DIAGNOSTIC that reads editor-owned JSON, not just before edits.** Pull-clobber has always been framed as a write-safety rule (don't lose work); it is equally a **read-accuracy rule** (don't reason from a stale mirror). **The 14 July pull also surfaced real drift:** Billy's homepage artwork is **IN** — hero slides now BroadviewPress / Kodama / PMI, focus panels Debrett's / Marian Press / Right Book (exactly matching Billy's curation map DA1 / CZ3 / CL8), strip Montagud. All `_-_TEST.png` placeholders gone. **This closes the last big Phase 1 unknown — homepage is essentially there, and the tracker/checklist saying otherwise was stale.** Also in that diff: `gap` 0→20, and the Bestsellers category `emoji` cleared to `""` (Grant's change, kept). **Git note:** `git push` over HTTPS now FAILS ("Password authentication is not supported") — GitHub killed password auth. GitHub Desktop still works (holds the credential). Bank as a to-do: switch the remote to SSH or store a PAT in the keychain, or every CLI push will keep failing. **Minor known consequence of the carousel fix:** core hardcodes the img `sizes` attribute as `16.666...vw` (100/6, **viewport**-relative), so with the track now 1200 inside a 1440 viewport the browser fetches one srcset candidate larger than needed. Core-generated, negligible, not worth chasing. **Fred reconciled — the file was a week stale** (see the AS400 section for the full rewrite): the stock file ARRIVED, it is named **`GazelleAvailability_YYYYMMDD.csv` not `GazelleStock`**, it is confirmed clean against spec, and cadence is **01:29 daily** (import 02:00). Tracking file confirmed clean too. Four questions went to Fred 9 July and the **PO round-trip is the unconfirmed correctness lynchpin**. RE-UPLOAD TO PROJECT KNOWLEDGE._
 
# Gazelle Books – Shopify Build Project Context

## People
- **Grant Davies** (grant@gsdworks.co.uk / grantsd104@gmail.com) – Web developer building the new Shopify retail store, and the **store admin**. Works with George as **Bowden Studio**. Coordinator between the client and technical collaborators.
- **Billy F. K. Howorth** (Billy.Howorth@gazellebookservices.co.uk) – General Manager at Gazelle Book Services. The client and Shopify store owner; primary decision-maker on product/UX.
- **Dave Hyman** (dave.hyman@booksonix.com) – **Owner of BooksoniX**; handles the developer side of the data integration into Shopify. Has admin access to the store (via support@booksonix.com) for the integration. Classic difficult developer; slow to respond.
- **Fred Mitchell** (fred@conciseconsult.com) – IT contractor via **Concise Consulting Ltd** (Park Gate, Brampton Road, Alston, Cumbria, CA9 3AA). Owns the warehouse / order-processing (**AS400**) side and the AS400 order-integration workstream. The existing precedent on his side is the **Debretts** order feed.
- **George** – Grant's business partner; together they are **Bowden Studio**. Built the Webflow brand site (gazellebookservices.co.uk) and holds the proper brand assets (logo SVGs, font licences).

## The Project
Building a brand new Shopify store for Gazelle Book Services: **gazelle-books-2026.myshopify.com** (Horizon theme).
- Clean-slate build, separate from the existing/old store (not a migration).
- Wholesale/B2B and retail are split across two sites:
  - **Webflow brand site** (George, Bowden Studio) at gazellebookservices.co.uk — info site for publishers + wholesalers.
  - **Shopify retail store** (Grant) — consumer e-commerce storefront, to live under **store.gazellebooks.co.uk**.
- Strategy: build back end + front end fully, then swap/point the domain to go live.
- BooksoniX pushes product data into Shopify via an event-driven REST API using ONIX feed data.
- **Scope (SOW, Jan 2026):** custom Horizon theme build, BooksoniX title import, daily stock ingestion, and **order export + order acknowledgement/processing ingestion** (the AS400 workstream is explicitly in scope). £3,000 fee (50% upfront / 50% on delivery). Work outside scope is quoted separately.

## Current Status (June 2026)
- **All three front-end page mockups are complete and unified for Billy's sign-off**: homepage, collection page, product page, all sharing the approved header and the new footer. See "The Three-Page Mockup Set" below.
- A sign-off call with Billy is the immediate next step. The mockups are the artefacts for that call — the goal is to get all three page designs approved in one sitting so the Liquid build can proceed without rework.
- **The build is still gated on data**, not on design. Outstanding blockers: the BooksoniX integration maturing (Dave), the subject taxonomy decision, and the remaining metafields. Grant has said repeatedly that if the data were all in place, the site could go live quickly — the hold-up is the data side.
- **AS400 order integration is the live workstream** (Fred). **Billy rates the Shopify↔AS400 connection his top item; go-live is ~2 weeks out.** State as of 7 July:
  - **Outbound order file: REGRESSED to A–N (ship-to only).** Fred's 30 June revision dropped the Bill To block + Company Name, reverting the A–V spec. **This contradicts Billy's confirmed dual-address requirement and is an OPEN item to resolve with Fred/Billy.** A v2 order file was referenced in Fred's email but never reached the chat — Grant to review it before re-raising bill-to.
  - **Inbound tracking file: CONFIRMED v3.** `GazelleTracking_YYYYMMDD.csv`, 5 fields, daily at 18:00, Matrixify import 18:30. Carrier-URL column is in (no longer an ask).
  - **Matrixify plan-tier: RESOLVED** — daily batch import means folder-watch (Big/Enterprise) tier is not needed.
  - **Daily stock/availability file: ✅ ARRIVED & CONFIRMED CLEAN (9 July).** ⚠️ **Renamed — it is `GazelleAvailability_YYYYMMDD.csv`, NOT `GazelleStock`.** EAN + on-hand qty, full snapshot with explicit `0` rows proven in the data, **01:29 daily**, Matrixify import 02:00. See the AS400 section.
  - **⚠️ PO round-trip: UNCONFIRMED — the correctness lynchpin.** Matrixify joins tracking to order on PO. If the AS400 substitutes its own internal sequence number instead of echoing the PO we send in field A, tracking attaches to nothing. Must be pinned down explicitly with the test order.
  - **ISBN-13 → variant barcode: confirmed landing** (Dave), so the EZ Exporter prerequisite is effectively met; spot-check pending.
  - See "AS400 Order Integration" below.
- **Timeline:** the original end-of-April target slipped long ago. Launch is realistically gated on Dave/BooksoniX. Billy is aware it has slipped and that the delay is on the data/integration side, not on Grant's work. Gazelle are conscious they are "losing money" by not being live.
- **Front-end Liquid build has started (2 July).** Toolchain now set up: **Claude Code** (Opus 4.8) + the **Shopify Dev MCP** (live Liquid/theme-check validation), driving the `gazelle-horizon` repo. First shared component built and committed — the collection **product card** snippet (not yet wired into a template). See "Front-End Liquid Build (Claude Code)" below.

---


---

## Document History (why this consolidation exists)
The project-knowledge copy has repeatedly lagged because updated versions were generated but not re-uploaded. Lineage:
- **24 April** — detailed (~569 lines). Full app/theme operational reference.
- **15 May, 27 May** — generated, never re-uploaded; 27 May not recoverable from chat.
- **9 June** — full rebuild from change summaries (~400 lines, leaner). Current on product/footer/AS400 decisions but **dropped** the Horizon performance guardrails, the detailed theme dev workflow, and the app-CLI gotchas.
- **22 June** — AS400 order-integration update.
- **22 June (this file)** — consolidation: 9 June spine + restored 24 April detail + chat-only decisions (tax method, description fallback, unstructured metafields, product-type subset, pricing automation, PUBCODE, Hackett covers, postage).

**Discipline:** re-upload promptly after every edit. Keep nuance, not just outcomes — imprecise capture is what let two reversals go undetected for weeks.

**⚠️ KNOWN UI BUG / workflow trap (recurring, noted 7 July):** the project-knowledge copy of this file mounts into new chats **stale** (a snapshot lagging the live version), and there is **no download button** for `.md` files in the project UI, so Grant physically cannot pull the latest file the normal way — a Claude UI bug. This is the root cause of the repeated "edited the wrong (older) base" problem. **Workaround in use:** retrieve the current file from an **artifact in another chat**, then upload it into the working chat as the base. **Every session, before editing this file: (1) verify the line count against the last known-good count [**1069 as of 16 July**; prior known-good 985 as of 14 July ~5pm, 960 as of 14 July ~3:15pm. NOTE: TWO sessions ran on 14 July, so the DATE alone is NOT proof of currency — verify by CONTENT (grep for the newest artefact you know is on disk, e.g. gazelle-layout)], and (2) check the top `_Last updated:_` line — if either looks behind, stop and get the real latest before touching anything.** Do not trust the auto-mounted `/mnt/project` copy without this check.

**⚠️ THE BUG BIT AGAIN — 16 July (three stale bases in one week).** The 16 July session lost ~40 minutes hunting the correct base: five separate downloads (925 / 868 / 960 / 905 / 960-again, two byte-identical) all predated the 14 July PM work, because **two sessions ran on 14 July** — the footer session (→960, ~3:15pm) and the header/page-width session (→985, ~5:00pm). A 14-July timestamp is therefore NOT sufficient proof of currency. **The reliable test is CONTENT, not the date: grep the file for the most recent artefact you know exists on disk** (e.g. `grep -c gazelle-layout`) — a master file that doesn't know about a snippet sitting in your repo cannot be current. **⭐ THE REAL FIX (do this): move `gazelle-context-working.md` INTO THE REPO** next to `CLAUDE.md`. Git then owns versioning, staleness becomes structurally impossible, Claude Code reads it directly instead of being handed a snapshot, George gets it for free, and the whole upload/download/re-upload dance disappears. The discipline has not failed through carelessness — it has failed because the MECHANISM is broken (manual re-upload, no download button). Stop patching the discipline; fix the mechanism. **Corroborating evidence the inversion is already real:** on 16 July the DERIVED `gazelle-tech-stack.md` (13 July) was MORE accurate on Fred than this master file was — it correctly said `GazelleAvailability` while this file still said `GazelleStock, in flight`. A derived doc overtaking the source of truth is the clearest possible signal the mechanism is broken.

## The Three-Page Mockup Set

High-fidelity standalone HTML mockups built for Billy's design sign-off. **These are standalone HTML for design approval — they are NOT part of the Horizon theme yet.** They click through to each other so the set demos as a journey (product cards link to the product page).

### Files (current — "June" set)
- `gazelle-homepage-mockup-June.html`
- `gazelle-collection-page-mockup-June.html`
- `gazelle-product-page-mockup-June.html` (the product page is internally "v4")

The homepage and collection pages link through to `gazelle-product-page-mockup-June.html`.

### Design language (shared across all three)
- **Colours:** brand red `#a11f21` (accent), `#7c1516` (hover), `#ae2628` (secondary), charcoal `#1a1917` (ink / dark surfaces), `#faf7f2` (paper), `#ffffff` (surface), `#6b6760` (muted), `#e8e2d8` (border).
- **Fonts:** Trajan Pro (display/headings, base64-embedded in each file), Fraunces (serif body — titles, descriptions, prices), Figtree (UI sans — nav, buttons, labels). Fraunces + Figtree load from Google Fonts; Trajan is embedded inline so the files are self-contained.
- Page width max 1200px, centred.

### Annotation system (still present, toggleable)
Each mockup has a toggle (bottom-right) that turns on colour-coded pills showing each field's data source: green = confirmed metafield, blue = native Shopify field, amber = pending Billy's sign-off. Useful for walking Billy through field-by-field. Can be stripped for a clean "finished" look if preferred (offered, not yet actioned).

### Asset handling notes
- Trajan Pro OTF and the Gazelle logo PNG are base64-embedded inline (files work emailed around, no external dependencies for fonts/logo).
- Homepage banner images (hero "Manga & Graphic Novels", Debrett's panel, Montagud strip) were **cropped from the live dev-store screenshot** and embedded as optimised JPEGs — kept intact per Billy's instruction.
- Product **cover images load from external Schiffer URLs** (`images.bookonedatabase.com/...`), same as the original mockups. **Must be online to see the covers**; they render blank offline. Product selection on the homepage/collection is illustrative ("can be whatever").
- Open in Chrome/Safari (a modern browser) — older render engines don't support the CSS grid used for the category row, focus panels and product rail.
- **Mobile images (confirmed to Billy, ~6 July):** all images simply scale down on mobile **except the main homepage slider**, which uses a **dedicated mobile image sized 800×367px** (so the hero art stays legible rather than being letterboxed/cropped from the desktop crop).

### Supporting deliverables
- `gazelle-footer-mockup.html` — standalone preview of the new footer (same styling as the page footers).
- `footer-group.json` — drop-in Horizon footer config (see "Footer" below).

---

## Header — ✅ BUILT (14 July; native-first, ~zero custom CSS)

**Status: DONE (14 July).** Restyled/configured Horizon's native header exactly as planned — config + tokens, not a rebuild. Logo Left, inline horizontal nav (Menu Row = Top), native search/account/basket icons on the right, Scheme 1 Paper, announcement bar live ("Free UK Delivery on website orders over £20"). No custom section; may stay a genuinely **zero-CSS header** — native rendering matched the mockup closely enough that nothing was written.

**Deliberate deviations from the June mockup (flag to Billy alongside the footer's "Terms and Policies" popover note):**
- Utilities render as native **icons** (search/account/basket), not the mockup's "Account" / "Basket (0)" **text labels**. Native e-comm pattern; text labels would be pointless custom CSS. Accepted unless Billy objects.
- **GBP currency selector + localization turned OFF** (not in mockup; Gazelle is UK-only). One toggle to restore if a trade reason emerges.

**Nav labels are still the OLD Main menu placeholders** (Home / New Books / Bestsellers / **Catagories** [sic — old-site typo, do NOT ship] / Blogs / Contact). The intended placeholder set (Fiction / Non-Fiction / Art & Design / History / Children's / New Releases / Publishers) was NOT yet wired — final nav is gated on the taxonomy decision (see On The Horizon). Whatever the labels, it's an admin → Navigation job with zero theme work, so the header build doesn't wait on it.

**Mega menu:** Horizon renders one automatically when a nav item has child links — it is NOT a separate build, just a nested Navigation structure. It was never in the June mockups (all show flat nav), so its *content* is an open design question — send Billy a one-liner (links-only vs featured titles) alongside the taxonomy proposal. Don't freestyle it.

**Original build approach (kept for reference):** the mockup header is exactly what Horizon's header already ships (logo, menu, search, cart drawer, account), plus the working cart/predictive-search/mobile-menu/sticky machinery the static mockup doesn't show. The job was config + tokens (logo, colour scheme, menu, position toggles), never a custom section — and that held: it built with no custom code.

---

## Footer — ✅ BUILT & STYLED (14 July; structure decided June)

**Status: DONE (14 July).** Built exactly per the structure below, native-first, with one new style-only section (`sections/gazelle-footer-styles.liquid`) closing the typography gap. Full build record in the 14 July note (top) and the 14 July Session log. Live differences vs the June plan, all deliberate: the delivered `footer-group.json` drop-in was never used (it had been silently overwritten by the editor back to the stock preset — hand-built in the editor instead, which is now the preferred route for editor-owned config); the newsletter heading reads "Newsletter" per the mockup; policy links render as Horizon's native "Terms and Policies" popover trigger rather than four inline links (native pattern, accepted); Help/Explore menu links point at `/` until content pages exist (re-point in admin → Navigation, no theme work needed). **Go-live flags:** copyright pulls the store name (currently "Gazelle Dev"); social URLs placeholder; policy wording review with Gazelle.

### Structure (four zones + bottom bar)
- **Newsletter** — heading, one line of copy, email signup + button (native Horizon email-signup).
- **Help** — Delivery Information, Returns & Refunds, FAQs, Contact Us. (Friendly help pages, distinct from the formal legal policies.)
- **Explore** — About Us, Our Publishers, Services, Home.
- **Gazelle Book Services Ltd** — a text/company block (NOT a menu): registered address (White Cross Mills, Hightown, Lancaster, Lancashire, LA1 4XS), phone (+44 (0)1524 528500), sales email, and registered company number (02175658). Kept deliberately — UK company law requires the registered name/number/office on the site, and the old footer carried it.
- **Bottom bar** — copyright; policy links (Privacy / Terms / Refund / Shipping — pulled natively from Shopify's policy pages); social icons (Facebook / X / Instagram / LinkedIn).

This is richer than the spare "Hatchards-restraint" v3.4 footer Billy last saw, and closer to (and informed by) Gazelle's old live footer (which had Follow us / Newsletter / Company Information / Navigate / company address). Flag the tone shift to Billy as a deliberate choice.

### Native Horizon build (the actual implementation route)
Horizon's footer group is **two stacked native sections**, both block-based:
1. `footer` (top) — a block grid. The three link columns are three native **`menu` blocks**, each bound to a Shopify menu. The logo (if wanted) goes here as a `logo`/`image` block (with `inverse` on for the dark background).
2. `footer-utilities` (bottom bar) — **ships exactly as the bottom bar already**: a `footer-copyright` block, a `footer-policy-list` block (pulls Privacy/Terms/Refund/Shipping from the store's policy pages), and a `social-links` block (URLs set on the block / theme settings). Already laid out left/right with a top divider and responsive stacking.

**Prerequisites (editor + admin side):**
- Create **two** Shopify menus in admin → Navigation with handles `footer-help` and `footer-explore`. **Not** a `footer-legal` menu — the policies come from the native policy-list in the utilities bar.
- Set the social URLs on the `social-links` block.
- Ensure Privacy/Terms/Refund/Shipping pages exist under Settings → Policies so the policy-list populates itself.
- Style a charcoal colour scheme (background `#1a1917`, links/accents `#a11f21`) and apply it to both footer sections (Horizon defaults the footer to `scheme-5`).

**Known constraints / small custom bits:**
- `footer-utilities` only accepts copyright / policy-list / social blocks — **a logo cannot go in the bottom bar**. Logo lives in the main footer body instead (or the company-name block carries brand presence).
- Trajan uppercase column headings: the menu block has no per-block "uppercase" control, and **Horizon has no global custom-CSS field**. So the Trajan-uppercase heading treatment needs either a configured heading type-preset or a small scoped CSS nudge (via a small custom `gazelle-` block emitting `{% style %}`, since core files aren't edited).
- `footer-group.json` (delivered) is a drop-in that wires the three menu blocks + the utilities bar; it's config, not core code (the theme editor writes to it). Build in the editor or drop the file in and refine — the menus must be created in admin either way.

### What "native" means on this project
Bind to native Shopify objects wherever possible (menus, policy pages, social settings, product fields) rather than hardcoding. Custom markup is fine where it earns its place.

---

## Product Page — Decisions (from Billy's call transcript)

### Removed
- **Star rating / review count** from the buy box. Gazelle don't deal much with individuals; individual star reviews have no value for their trade-facing audience.
- **Format selector (HB/PB/eBook)**. Every book is a completely separate product with its own ISBN; paperback/hardback editions are NOT linked in the metadata, so a variant selector shouldn't appear. The eBook placeholder (which "threw" Billy) is gone — **Gazelle do not sell ebooks**.
- **"Save X%" tag** from the price (reaffirms the existing no-save-messaging rule).

### Added / changed
- **Clickable Publisher and Imprint** — clicking either runs through to a filtered collection of those titles. (Author was already clickable; searchable author is "something we're always asked for".)
- **Classification box** in the side rail (under Subjects) showing **Thema codes** and **BIC codes** in separate sub-blocks. Trade customers find these codes useful to have to hand. Note: these codes are *displayed* even though full subject-taxonomy *mapping* is parked.
- **Product Details additions:** spine **Depth** (dimensions now shown H × W × D) and **Illustrations** (e.g. number of black & white / colour illustrations). Both are existing BooksoniX fields.
- **Reviews reframed as "Press & Reviews"** at the bottom — editorial/trade reviews (magazine, periodical, professional organisation) from the metadata, not customer star reviews. (See the reconciliation flag below.)
- **Stock as a traffic-light system:** in stock (green) / low stock (amber) / out of stock (red).
- **New Release flag confirmed:** auto-applied to any title whose **publication date falls in the current month**, and drops off automatically the following month. Implemented via the publication_date metafield + a script. (Logic, not a manual tag.)

### Empty fields
If a metafield is missing, the field currently renders empty / "no data". Grant may try to suppress empty fields entirely (minor; not a blocker).

### Price display conflict (needs Billy — flagged 2 July)
The June product-page mockup's buy box shows a **current price alongside a struck-through RRP** (a "was £X, now £Y" treatment). That is **discount messaging**, which contradicts the **no-save / no-discount-messaging rule** above, and it overlaps the **25% pricing automation that is explicitly out of scope**. Resolve with Billy whether the struck RRP stays (RRP vs Gazelle price) or is removed **before** the product-page buy box is built. The product **card** (built) already follows the rule — native price only, no compare-at.

---

## Stock Management (RESOLVED on the call)
- **No back orders, ever.** This is the key difference from the old site (which allowed back orders). If a title is out of stock, no one can order it.
- **Out-of-stock titles stay visible** — both the product page AND on collection pages. Billy explicitly wants them displayed (if pages disappeared and reappeared, publishers would flood Gazelle with "why isn't my title showing" emails). The product page also stays as a historical link for anyone arriving via a mailer / Google / saved link.
- Out of stock = **Add to basket disabled** + an optional **"notify me when back in stock"** email capture.
- This is largely a Shopify back-end setting (whether to display out-of-stock products) plus the traffic-light display. This **resolves** the previously-open out-of-stock questions and **overrides** an earlier note that out-of-stock titles would disappear from collections.

- **Postage:** Billy has entered postage costs himself (UK & Europe only initially, as before). Independent of the integration; no clash with the BooksoniX/AS400 work.

## Pricing
- Gazelle have their own **"Gazelle price"** (a discount off RRP) for the website. This is **uploaded separately** (not sourced from BooksoniX). Initial bulk upload of the discount for the ~50,000-title backlist; thereafter new titles arrive as draft (~100/week) and Gazelle set the Gazelle price via the Shopify platform. No need for repeated big bulk loads.
- Display: **RRP with a strikethrough alongside the selling (Gazelle) price.** No "Save X%".
- **Price is create-only** from BooksoniX (RRP pushed into Shopify's Price field on create, never overwritten on update) so manual Gazelle discounts aren't silently reset by a BooksoniX re-push. When discounting, Gazelle lower Price and set Compare-at to the RRP. **Compare-at must be empty when selling at RRP** (Shopify renders a broken strikethrough otherwise).
- Store must be in **prices-include-tax** mode (BooksoniX sends RRP inclusive of tax).

## Pricing Automation — the 25% rule (OUT OF SCOPE — separate charge)
- **Rule (Billy, confirmed 15–16 June):** 25% off RRP for titles with **RRP ≥ £14.99**; titles below £14.99 stay at full RRP. **Raw two-decimal** figures (no .95/.99 tidying) unless Billy says otherwise.
- **Exclusions keyed off PUBCODE:** excluded publishers always sell at full RRP. For now exclude **only Kumon (PUBCODE CK4)** — they run a separate discount code for select customers.
- **Editable parameters:** threshold, %, and exclusion list stored as settings so they change without a rebuild. **Bulk retroactive pass** across the ~50k backlist + **automatic** application to new titles as they land.
- **Mechanism:** `Price = RRP × 0.75 where RRP ≥ £14.99 and PUBCODE not excluded; else Price = RRP`. Compare-at = RRP only when discounted (empty at full RRP). Native bulk edit can't do percentage logic and Flow is weak at calculated price updates, so it's a calculated bulk load (CSV/script) for the backlist + the same rule on new titles.
- **CRITICAL — keep this OUT of Dave's integration.** It's event-driven and re-pushes the full record on any edit, so a "recompute price on update" rule would silently wipe manual Gazelle prices the next time a title is edited in BooksoniX (same reason Price is create-only). Run the discount as a **Gazelle-side pass** that only touches titles not yet manually priced. Bonus: % / threshold changes stay our toggle, not a Dave ticket.
- **Dependency:** **PUBCODE must be surfaced as a Shopify metafield** (Dave mapping job). "Publisher" is currently a name and Vendor = Imprint, so there's nothing to key Kumon off yet.
- **Watch:** the £14.99 threshold is a hard cliff (£14.98 → nothing, £14.99 → 25% off ≈ £11.24, a ~£3.74 swing on 1p of RRP). Billy's call; flagged.
- **Commercial:** genuinely outside the Jan SOW (data flows, not a conditional discount engine). **Flag a separate quote before building.** The £3k already bundles a lot (incl. the whole AS400 workstream), so charge cleanly for real extras like this; don't nickel-and-dime borderline theme features (New Release flag, traffic-light stock, Classification box) which read as bespoke sections.


## Additional Images
- Cover image is the main product image (pushed first in the image array).
- **Additional images (interior spreads / sample content) are uploaded via CSV.** They're hosted as live links on the BooksoniX server (or a publisher server), so the route is: BooksoniX generates a file of the image paths → bulk upload to Shopify via CSV. No manual one-by-one upload.

- **Known issue — Hackett titles missing covers (Billy, ~16 June):** covers display correctly in BooksoniX but are missing in Shopify. Clustering by **publisher** points to a structural cause (mapping or host-access), NOT a timing lag. Shopify **silently drops unreachable image URLs** on its server-to-server fetch, so a host/URL problem can be invisible in Dave's logs. Grant to verify the exact products in Shopify admin first, then engage Dave if it's a mapping/host issue.

## Subject Taxonomy / Collections
- **Full-depth BIC/Thema mapping is parked** — Gazelle distributes for many publishers using mixed schemes (Thema, BISAC, BIC, proprietary, none). Mapping reliably across ~55k titles at fine grain isn't realistic.
- **Direction:** use THEMA's top-level hierarchy (~20 parent codes) as the site's main category structure, rebranded to friendly Gazelle names; implemented as automated smart collections on metafield conditions. Gap cases (non-Thema codes, no codes) handled via lookup/manual over time.
- **NEW:** the Thema and BIC **codes are displayed on the product page** (Classification box) regardless of the mapping decision — that's a display feature, separate from the navigation taxonomy.
- The collection page's **Subject filter** is in place in the mockup but **cannot be wired for real until the taxonomy mapping is finalised** — it remains the key unblocker for collection filtering, navigation, and related-products logic.
- Tags are reserved for editorial overlay (seasonal, staff picks, prize winners). NOT core taxonomy. Integration applies no tags automatically.

## Fonts / Typography (CONFIRMED 7 July — from DevTools on gazellebookservices.co.uk)
The brand (Webflow) site runs a **two-font system**, both bound to CSS variables (swappable by design):
- **Headings (h1/h2/etc.) AND buttons/CTAs:** **Trajan Pro** — `--_fonts---heading`; e.g. h2 = 40px weight 500, buttons = Trajan weight 600. Commercial Adobe font. Caps-only inscriptional face.
- **Body / paragraphs:** **Switzer** (`--_fonts---paragraph`) — Indian Type Foundry, **free for commercial use via Fontshare** (variable neo-grotesque sans). Falls back to Arial.
- **Logo only:** built with **Blair ITC Bold** + **Trajan Pro Bold** (the two OTFs Billy emailed 11 March, subject "Logo"). Blair ITC is logo-only; NOT used elsewhere on the site.

**This corrects earlier vague notes:** headings are **Trajan**, body is **Switzer** — not "Blair/ATF". **Fraunces/Figtree from the June mockups were design guesses, not Billy's brand fonts, and are dropped.**

**⚠️ Real tension to flag to Billy:** Billy asked for **less all-caps** than the mockups, but his own brand site sets **every heading and button in Trajan (caps-only)**. "Match the brand site" and "less all-caps" cannot both be fully true. **Grant's call (7 July): follow the brand and keep caps for now**; revisit with Billy later. Note the caps come from the *font* (Trajan/Cinzel have no lowercase glyphs), not a CSS transform — so "keep caps" is the zero-effort default, and genuinely reducing caps later means swapping the heading font (a token change), not toggling a case setting.

**Build decision (Grant, 7 July):**
- **Headings + buttons: CINZEL** (free, Google Fonts, **in Shopify's font picker**) as the Trajan stand-in for now — inscriptional caps, ~90% of the Trajan look, zero licensing. Set via theme editor, no code. Real Trajan needs a proper webfont licence (Adobe Fonts/Typekit does NOT cover Shopify self-hosting) — only pursue if Billy asks.
- **Body: SWITZER** — **not in Shopify's picker**, so self-host: Fontshare `woff2` as a theme asset + one scoped `@font-face` in a `gazelle-` snippet, then point Horizon's body font var at it. Small, scoped, one-time.
- Everything stays tokenised → swapping Cinzel→real Trajan, or changing case, is a token/setting change later, not a rebuild.
- **Build note (2 July, updated 7 July):** the built product card binds its fonts to Horizon's inheritable vars (`--font-body--family`, `--font-subheading--family`) with the mockup stacks as fallbacks, so it stays swappable. Theme font slots still sit on **Inter** defaults (`inter_n4/n5/n7` in `settings_data.json`) until set. So **previews render Inter until fonts are configured** — set the heading font to **Cinzel** in the editor (in the picker) and self-host **Switzer** for body (see decision above). Expected, not a bug.

## Reviews — Reconciliation Flag (needs Grant's confirmation)
There is a conflict between two records:
- An earlier capture (logged ~24 April) recorded the decision as **"no reviews system, no reviews tab at all."**
- Billy's call transcript clearly wants **editorial/press reviews kept at the bottom** (from metadata), just **not** the star/individual-review system at the top.
The June product-page mockup was built **per the transcript** (star rating removed from the top; a "Press & Reviews" editorial section kept at the bottom). **Grant to confirm which is current.** If the later decision was to drop reviews entirely, removing the bottom section is a one-line change. (This is exactly the kind of imprecise capture the context-file discipline is meant to prevent.)

---

## Data Integration (BooksoniX → Shopify)

- Source data lives in **BooksoniX** (ONIX format). **Dave** built the integration that pushes products into Shopify. Costs: £500 setup + £250/year (Billy approved).
- **Event-driven:** any edit to any field in BooksoniX pushes the **full product record** to Shopify near-instantly (not diff-based). Worth bearing in mind for rate-limit/quota planning.
- **Runs on REST API.** Dave has flagged a future migration to GraphQL (his roadmap; no action our end).
- **Token refresh:** Dave automating the client-credentials refresh server-side (was a manual 24-hour cycle).
- **New titles → draft status:** changes/new titles flow through but land as **draft** so Gazelle have oversight before anything goes live. Price/data changes pull through automatically. (Consistent with the create-only rules below.)
- **Behaviour rules (the safeguards):**
  - **Price: create-only** (see Pricing).
  - **Status/draft: create-only** — set on create, not flipped on update (an edit to a published title shouldn't revert it to draft).
  - **Status filter:** only **"Approved"** BooksoniX records sync to Shopify.
  - **Forthcoming titles:** pre-publication titles are NOT pushed live; only on-sale titles appear (filter on publication date).
  - **Archive/delete behaviour:** to confirm with Dave (and: when a publisher closes down, Gazelle close them in BooksoniX — how that ports through / whether manual removal in Shopify is needed is an open question for Dave).
  - **⚠️ NEW ISSUE (Billy flagged, ~6 July): archived BooksoniX titles are showing as Active in Shopify.** Root cause: the **Approved-only filter was never applied to the initial bulk seed**, so non-Approved/archived records got in. **Three actions on Dave:** (1) enforce the Approved-only filter on all new pushes; (2) when a title moves to **Archived** in BooksoniX, **archive** the Shopify product (not delete — preserves manual edits and is reversible; note archived products still 404 on the storefront, so this is about reversibility, not SEO); (3) **retroactively sweep** the already-seeded non-Approved titles out. This is the practical instance of the Approved-only rule that was agreed in principle but not enforced on the seed. **⚠️ Live contradiction on action (2): Dave's email (2 July) states the integration currently _deletes_ the Shopify product when a BooksoniX record is archived. Grant asked Dave (3 July) to switch to archive-not-delete; Dave has NOT yet confirmed the change. Until confirmed, archived titles are being destroyed (losing manual pricing/edits), not preserved — the exact opposite of the decision.** Also unconfirmed from Dave's 22 June/3 July replies: whether the Approved-only filter and retro-sweep (actions 1 and 3) have been actioned.
  - **Error handling:** how a failed push is reported — to confirm with Dave.
- **Tax/VAT:** taxable flag is a boolean driven by the record's own tax field (false at 0%, true for any non-zero rate). Store in prices-include-tax mode. Non-book lines (craft kits, tarot decks, calendars) are standard-rated 20% — sample data showed everything at 0% (likely stale test data). Open secondary point: whether zero-rated products should be taxable-true-at-0% vs taxable-false for VAT-return accuracy.
- **Inside spreads / sample content images: RESOLVED (Dave, ~6 July)** — interior spreads now sync correctly to Shopify **media positions** (cover first, spreads after). Note the earlier 63-title sample file only carried single covers, so it was never a valid test of this; validation is against live BooksoniX records instead. **Spot-check pending:** confirm spreads appear across **different publishers and older backlist**, not just the one title checked.
- **Tax method (SETTLED, live since 3 June):** driven by the record's own **tax field**, NOT a product_type map. Dave first built a product_type→tax-flag table (29 May) then scrapped it — product categorisation is unreliable, whereas the tax field is known-correct in both BooksoniX and the AS400 (Billy's point). Flag: `false` at 0.00%, `true` for any non-zero rate.
- **Empty tax field:** won't happen on a priced record. Books carry zero-RATE VAT (a value of 0.00%, not an absent value); ONIX validation guarantees a tax value. (Verify our end: confirm store is prices-include-tax and run a test order on a taxable line, e.g. a poster, to check VAT comes out right — Grant action, pending.)
- **Description fallback (Dave, ~28 May):** publishers populate either the main description or the long description (both valid). Integration now falls back to the long description when the main is empty.
- **Metafields arriving UNSTRUCTURED (Dave flagged 27 May):** they need defining as **structured metafield definitions** in Shopify (Settings → Custom data) so they validate/display correctly. Grant's action ("leave it with me"). **Outstanding.**
- **Product Type subset/mapping (IN PROGRESS):** Dave asked whether to push all ~58 ONIX formats or a reduced set. Billy is combining for the site (e.g. Audio formats → "Audio"; CD-Audio/CD-ROM → "CD"; DVD formats → "DVD"; Multiple-component variants → one; Paperback variants → "Paperback"; Sheet map variants → "Sheet map") and **excluding** "Digital (delivered electronically)" (no ebooks). Billy's combine list was **cut off mid-email** (stopped ~Sheet map), so it needs finishing, then Dave implements. **Outstanding (Billy to finish list → Dave to implement).**
- **Source-data integrity:** some descriptions have missing spaces/paragraph breaks (e.g. 147 Taiwanese Martyrs) — root cause is the source data, not the integration; flag to Gazelle to tidy.


---

## AS400 Order Integration (Fred / Concise Consulting)

Separate workstream from BooksoniX, owned by **Fred Mitchell**. Two directions of flow: **orders out** (Shopify → AS400 order file) and **tracking back** (AS400 → Shopify). In scope per the SOW (order export + acknowledgement ingestion). **Live deadline: AS400 goes live in ~2 weeks; Billy's top item.**

### Outbound order file (Shopify → AS400) — format
Based on Fred's existing **Debretts** precedent (`DebrettsOrder_ABC123456.csv`). Flat, **denormalised, headerless, double-quoted CSV**: text fields double-quoted, numeric fields unquoted. Two field levels — **H (header)** fields repeat on every line of an order; **D (detail)** fields are per line item. So a two-line order repeats the header block on both rows.

**⚠️ CURRENT SPEC: A–N, SHIP-TO ONLY (Fred's 30 June revision) — a REGRESSION.** Fred's latest revision **dropped the Bill To block + Company Name**, reverting to the original ship-to-only structure. This was A–V (with bill-to) on 23–27 June; Fred simplified it back down on 30 June. Structure now:

| Col | Level | Field | Max |
|---|---|---|---|
| A | H | Purchase Order Number | 14 |
| B | H | Ship To Name | 30 |
| C | H | Ship To Address 1 | 30 |
| D | H | Ship To Address 2 | 30 |
| E | H | Ship To Address 3 | 30 |
| F | H | Ship To Address 4 | 30 |
| G | H | Ship To Post Code | 8 |
| H | H | Ship To Country | 3 (ISO alpha; note EZ Exporter must convert Shopify's 2-char `GB` → 3-char `GBR`) |
| I | H | Ship To Email Address | 100 |
| J | H | Ship To Phone Number | 30 |
| K | D | Book EAN | 13 |
| L | D | Book Title | 30 |
| M | D | Quantity Ordered | 6,0 (999999) |
| N | D | Price | 6,2 (9999.99) — unit price paid |

**⚠️ OPEN — dual-address regression (needs resolution with Fred/Billy):** Billy confirmed as a **business requirement** that orders capture **both invoice (billing) and shipping address** (people order for family, gifts, etc.). Fred's A–N revision removes the ability to send the bill-to block, so as it stands the AS400 would only ever receive the delivery address. **Do not let this ship silently** — it's the exact kind of quiet reversal the file is meant to catch. A **v2 order file** was referenced in Fred's 30 June email but did not reach the chat; **Grant to review v2 first**, then re-raise the bill-to block with Fred citing Billy's requirement.

**Still-valid confirmations from Fred (22–27 June), independent of the A–N/A–V question:**
- **Hard truncation to his field sizes is fine.** Titles over 30 chars get cut; Fred rebuilds the full title from the EAN, so no data lost his end.
- **Two line items with repeating header fields** understood and OK. Headerless (position-based parser).
- Company-name question (when it existed): populate from the **shipping** address, not billing.

### Three extra fields requested back from Fred (sent 27 June)
Asked Fred to add: **shipping method**, **order notes / special instructions** (often blank), and **order date**. Status of these against the 30 June A–N revision is unconfirmed — check whether they survived the simplification when reviewing v2.

### Address mapping nuances (real, worth holding)
- Shopify stores **structured** addresses (address1, address2, city, province, zip, country), not four free-text lines. Proposed map into Fred's 4 lines: **line 1 = address1, line 2 = address2, line 3 = city, line 4 = county/province**; post code = zip; country = country_code. Applies to both Ship To and Bill To blocks.
- **Express checkouts** (Shop Pay / PayPal / Apple Pay) can occasionally return a **sparse billing address** or one equal to shipping. **Sanity-check on a real test order** before locking the spec — don't trust the sample alone. (Relevant again if/when the Bill To block is reinstated.)

### Tooling stack (no-code path — viable, with two real caveats)
- **EZ Exporter** — outbound order files. ~**$30/month (Gazelle's operational cost)**. Reads `order.billing_address.*` / `order.shipping_address.*` directly via Liquid templating, so the dual-address change is a spec/mapping job, not a build blocker. No per-publisher file splitting required, which keeps the no-code path viable.
  - **CAVEAT (confirmed 27 June): EZ Exporter runs on a SCHEDULE, not per-order/per-event.** It cannot emit one file the instant an order is placed. So the outbound cadence is a **frequent scheduled batch** (e.g. every few minutes), each file holding whatever orders are new since the last run — NOT one-file-per-order. This supersedes the earlier "one file per order is fine" note (that was Fred's *tolerance*; the tool can't actually do true per-order). Fine for the use case, but the AS400 side should expect batch files keyed by PO, not single-order files.
  - **Internal check (open):** confirm EZ Exporter exports the **discounted unit price actually paid**, not the list/compare-at price. Matters because Gazelle discount off RRP and **Kumon run a separate discount code** — col V must be the paid amount or the warehouse invoices the wrong figure.
- **Matrixify** — inbound tracking imports.
  - **CAVEAT (confirmed 27 June): the SFTP folder-watch (auto-poll a folder and import on drop) is a Big / Enterprise-plan-only feature.** Per-despatch inbound tracking that lands automatically depends on this tier. On lower tiers, imports are manual/triggered. **Plan-tier decision for Gazelle** before per-despatch auto-fulfilment is promised. (Matrixify is also handy for general bulk Shopify data ops.)

### Prerequisite before building the export
- ✅ **DONE:** ISBN-13 confirmed landing in the variant `barcode` field (Dave, ~6 July), with variants created inventory-tracked, so EZ Exporter reads the EAN natively into the detail rows. Spot-check across publishers/backlist pending.

### Inbound tracking return (AS400 → Shopify)
- **CONFIRMED v3 (Fred, 30 June):** `GazelleTracking_YYYYMMDD.csv`, **5 fields** — PO number, carrier name, tracking number, **full tracking URL**, shipment date. PO number is the **exact join key** Matrixify uses to match the fulfilment back to the order — must match the outbound PO precisely. The carrier-URL column (previously a request) is now included, so tracking links render correctly in the customer notification regardless of Shopify's carrier-name matching.
- **Cadence: RESOLVED — daily batch.** Fred sends the tracking file at **18:00 daily**; Matrixify import scheduled for **18:30**. This settles the earlier per-despatch-vs-batch question and, crucially, **removes the Matrixify folder-watch plan-tier decision entirely** — a scheduled daily import works on the current tier, so no Big/Enterprise upgrade is needed. (Trade-off accepted: customer tracking notifications go out once a day rather than per-despatch. Fine for the use case.)

### Daily availability / stock file (AS400 → Shopify) — ✅ FILE ARRIVED & CONFIRMED CLEAN (9 July)
Third file in the set, alongside orders-out and tracking-back. Keeps Shopify inventory in line with the warehouse.

**⚠️ NAME CHANGED — `GazelleAvailability_YYYYMMDD.csv`, NOT `GazelleStock_YYYYMMDD.csv`.** The proposed spec (Grant → Fred, 6–7 July) called it `GazelleStock`; Fred delivered it as **`GazelleAvailability`**. **Anyone building the Matrixify import off the old name targets a file that does not exist.** This file said `GazelleStock, in flight` for a week after the real file had landed — the derived `gazelle-tech-stack.md` had it right while this master had it wrong.

**✅ CONFIRMED CLEAN against spec (Grant + Claude inspected the actual CSV, 9 July):**
- `GazelleAvailability_20260707.csv`, **20 rows, 2 columns** — matches the format sheet (col A EAN/13, col B stock/6-digit).
- **EAN quoted as a string**, quantity a bare integer. The quoting matters: it prevents leading-zero loss and scientific-notation corruption on import.
- **8 of 20 rows are zero-stock** — so the full-snapshot-including-zeros behaviour is **proven in the data**, not merely promised. This was the single biggest oversell risk and it is now evidenced.
- **No negatives.**
- **Cadence CONFIRMED: 01:29 daily** (not the "~1am, exact time to confirm" previously recorded). **Matrixify import scheduled 02:00.**

**⚠️ Import rule (our side — STILL LOAD-BEARING):** configure Matrixify to **update only EANs present in the file and never zero out any EAN that's absent.** The two rules are a pair — *absence = leave alone* (protects forthcoming / non-warehoused titles from being wiped), *real zero arrives as an explicit `0` row*. The `0` rows are now confirmed present; the absent-EAN rule remains the safety net for the still-unanswered coverage question.

**⚠️ Availability import matches on BARCODE ONLY.** The file carries EAN and nothing else, so the Matrixify inventory update must match on **Variant Barcode**. Fine given ISBN-13 lives there — but **any variant with a missing or duplicate barcode silently fails to update**. This is exactly why the cross-publisher/backlist barcode spot-check is a go-live blocker, not a nice-to-have.

**Still open with Fred on this file:** does it cover **every** title Gazelle sells online, or only warehoused ones? (Backorder/negative handling is moot in practice — none observed — but floor-to-0 at source remains the stated ask.)

### Inbound tracking file — ✅ ALSO CONFIRMED CLEAN (9 July)
`GazelleTracking_20260707.csv` inspected against the v3 spec: **30 rows, all exactly 5 fields** (PO, carrier, tracking number, full URL, ship date). Dates ISO `YYYY-MM-DD`. Carriers are **Royal Mail / DHL / FedEx — all natively recognised by Shopify fulfilment**. Clean, nothing outstanding on the format itself.

### ⚠️ SFTP transport realities (confirmed 9 July — easy to get wrong)
- **This is SFTP, not plain FTP.** Port 22 = SSH/SFTP **despite the `ftp.` hostname**. Both EZ Exporter (export) and Matrixify (import) must be configured as **SFTP with password auth** — not FTP, not FTPS.
- **⚠️ `/Order` vs `/Orders` — UNRESOLVED.** Fred's own email lists *"3 folders available /Order, /Stock and /Tracking"* and then says *"put the files in the /Orders folder"*. **One of those is wrong.** A one-character mismatch means the order export writes into the void and nobody notices until orders don't arrive. Confirm the exact string.
- Each folder has an archive subfolder. **Grant's own action:** verify the import tool deletes files after pickup as Fred expects.

### ⚠️ THE PO ROUND-TRIP — the unconfirmed correctness lynchpin (raised 9 July)
The tracking file keys on **PO Number** (sample values `4249`, `4088`, `3595`…). **Those look like AS400-internal sequence numbers**, and Fred confirmed the samples are manually-entered historical orders. For a real Shopify-originated order, **Matrixify can only attach tracking to the right order if the PO Fred RETURNS in the tracking file is the exact value we SENT in field A of the order file.** If his system substitutes its own internal number, the join breaks and tracking lands nowhere — silently. **Pin this down explicitly with the test order: "the PO I send in field A is the PO you echo back in the tracking file."** This is not a format question; it is the thing that makes the whole round-trip correct or useless.

### ⚠️ DO NOT SEND THE TEST ORDER YET (standing decision, 9 July)
Fred asked for a test order "when you have this ready." **The order format he has built to is still A–N, ship-to only** — the reverted spec that contradicts Billy's confirmed dual-address requirement. **If we build the EZ Exporter test order to A–N and send it, we silently ratify the regression**, and it becomes far harder to unpick once Fred has parsed and validated against it. **The test order is the forcing function — hold it until the order spec is settled.** This is the same silent-reversal pattern the context file exists to catch.

### Email sent to Fred (9 July — Grant approved the draft unmodified)
Confirmed both files as clean, gave the import schedule (stock 02:00, tracking 18:30), and raised **four questions before any test order**: (1) dual-address requirement for the order file; (2) PO round-trip matching confirmation; (3) exact folder name (`/Order` vs `/Orders`); (4) one-file-per-order vs batched. **Awaiting Fred's reply.**

### Next on this workstream
- **Grant to review Fred's v2 order file** (referenced 30 June, never reached the chat), then **re-raise the Bill To block** with Fred citing Billy's confirmed dual-address requirement. This is the top open regression.
- **Fred** to confirm whether the three extra fields (shipping method, order notes, order date) survived the 30 June A–N simplification.
- **Internal:** confirm EZ Exporter exports the discounted unit price, not list (Kumon-sensitive), and converts `GB` → `GBR` for the country column.
- **⚠️ Fred to confirm the PO ROUND-TRIP** — that the PO we send in field A is echoed back verbatim in the tracking file. The correctness lynchpin; nothing else in the round-trip works without it.
- **⚠️ Fred to confirm the exact folder name** — `/Order` vs `/Orders` (his email says both).
- **Fred** to confirm availability-file **coverage** (all online titles vs warehoused only). ~~send a sample~~ **DONE — file arrived + confirmed clean 9 July** (`GazelleAvailability`, 01:29 daily).
- **Fred** to confirm one-file-per-order vs batched.
- **⚠️ DO NOT send the test order until the A–N/dual-address regression is settled** — sending it silently ratifies the regression.
- Grant to send a fresh sample order file once the order spec is re-settled (bill-to resolved + extra fields confirmed).
- **Grant's own actions:** verify the import tool deletes files after pickup; confirm both tools are set to **SFTP** (port 22, not plain FTP); **barcode spot-check across publishers/backlist** before go-live (the availability import matches on Variant Barcode ONLY — missing/duplicate barcodes fail silently).
- **End-to-end SFTP test:** a real Shopify order through to the AS400, tracking back — once format validation is confirmed. Use it to also validate express-checkout billing addresses (sparse/duplicate risk).
- ~~Move ISBN-13 → variant barcode~~ **DONE** (Dave confirmed landing; spot-check pending). ~~Matrixify plan-tier decision~~ **RESOLVED** (daily batch, no tier change).

---

## Shopify App — Setup Reference

### Where the app lives
- **App name:** BooksoniX Integration. **Lives in:** Gazelle Dev organization (same org as the store — required for the client credentials grant). Created from inside the store admin while logged in as grantsd104.
- **Active version:** `booksonix-integration-2`. **Client ID:** `5e994c135911baa59f413b9ac8d79992`. **Client Secret:** in Dev Dashboard → Settings (treat like a password; rotate once integration is confirmed stable — was exposed during debugging).
- Installed on gazelle-books-2026.myshopify.com.

### Access scopes (configured via TOML + CLI, not the Dashboard UI)
- `write_products`, `write_inventory`, `write_files` (read is implicit).
- To change scopes: edit `~/booksoni-x-integration/shopify.app.toml` `[access_scopes]`, `shopify app deploy`, then **reinstall** the app on the store (scope changes need a reinstall). Verify via the client-credentials curl `scope` field.

### Token acquisition (how Dave authenticates)
Dev Dashboard apps don't issue install-time tokens. Dave exchanges Client ID + Secret for a 24-hour token via the client credentials grant:
```bash
curl -X POST "https://gazelle-books-2026.myshopify.com/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" -d "client_id={id}" -d "client_secret={secret}"
```
Token → `X-Shopify-Access-Token` header; expires in ~24h (refresh by re-hitting the endpoint). Dave automating server-side.

### Access status
- Grant: Staff/Admin via grantsd104@gmail.com. Also Partner-org collaborator via grant@gsdworks.co.uk — but **that account cannot access the Dev Dashboard** (org-level permission). Use grantsd104 for anything app-related.
- Dave: admin access via support@booksonix.com (for the integration). Grant is the store admin.

### Orphan apps to clean up
- GSD Works Partner org: a duplicate "BooksoniX Integration" (handle `booksonix-integration-2`), 0 installs — delete.
- Gazelle Dev org: two apps Dave created ("BSX API updater" `bsx-api-updater-1`, "BSX API update" `bsx-api-update-2`), 0 installs — confirm with Dave they're stubs, then clear.

---

## Field Mapping

### Native Shopify fields (Dave maps directly)
| Shopify Field | From BooksoniX |
|---|---|
| Title | Title |
| Body HTML | Main Description |
| Product Type | Product Format (Paperback/Hardback) |
| Vendor | Imprint |
| Price | UK RRP (create-only) |
| Image Src | Media files (cover first; additional via CSV) |
| Variant Barcode | ISBN-13 (EAN) — **CONFIRMED landing here (Dave, ~6 July); variants created inventory-tracked.** Spot-check across publishers/backlist pending. |

### Metafields (`custom` namespace) — reconciled vs live export (7 July)
**The full approved set is Sheet 1 of `gazelle-field-mapping-FINAL.xlsx` (15 May, Billy-signed-off).** That list stands, but a 7 July reconciliation against the live BooksoniX export (`Shopify_Example_Titles`, 63 real titles) surfaced **type corrections the doc missed** — it specced almost everything as "single line text", which breaks date logic and renders multi-value fields with literal `|`. Definitions to create in **Settings → Custom data**:

| Metafield key | Source (BooksoniX) | Recommended type | Notes / correction |
|---|---|---|---|
| `custom.isbn` | ISBN-13 | Single line text | Also lands in native variant **barcode** (the load-bearing copy for stock/order matching). |
| `custom.subtitle` | Subtitle | Single line text | Own field, not appended to title. |
| `custom.author` | Contributors | **List.single_line_text** (or split `\|` in Liquid) | Pipe-delimited for multi-author (10/63 in sample, e.g. `Name A\|Name B`); single-line text renders a literal `\|`. Also conflates author + illustrator/editor. **No `By (author):` prefix in the export (0/63)** — confirm whether Dave strips upstream or it was never there (the product card also strips it → double-strip risk). |
| `custom.publisher` | Publishers | Single line text | Parent publisher (distinct from Vendor = Imprint). |
| `custom.language` | Languages | Single line text | |
| `custom.publication_date` | Publication Date | **Date (NOT text)** | Live data is free text `18 December 2022`. Text can't drive the New-Release "this month" rule or the forthcoming filter — needs a real Date type, or Dave pushing ISO `YYYY-MM-DD`. 5/63 future-dated. |
| `custom.series` / `custom.series_number` | Series Title / Number in Series | Single line text | ~19/63 populated. |
| `custom.pages` | Pages | **Integer** (doc said text) | Text won't sort/range-filter numerically if filters added later. |
| `custom.height_mm` / `custom.width_mm` / `custom.depth_mm` | Height/Width/Depth in mm | **Dimension/decimal** (doc said text) | Depth sparse (19/63). Display H×W×D. |
| `custom.illustrations` | Illustrations | Single line text | **Empty on all 63 sample rows** — renders blank for these; sparse source data, not a bug. |
| `custom.author_bio` | Contributor Biographies | Multi-line text | Also pipe-delimited per contributor (same `\|` issue). Duplicated by a separate `Biographical note` column in source; doc maps Contributor Biographies. |
| `custom.thema_subjects` / `custom.bic_subjects` / `custom.bisac_subjects` / `custom.main_subjects` | respective subject fields | Single line text (or list) | All pipe-delimited, mixed schemes (e.g. `main_subjects = JUV009030\|YFB`). Thema is the key for category routing + Classification box. |
| `custom.keywords` | Keywords Subjects | Single line text | Semicolon-delimited in source. |
| `custom.audience` | Audience | Single line text | |
| `custom.prize_achievements` | Prize Achievements | Multi-line text | Empty in sample. |
| `custom.reviews` | (confirm BooksoniX field) | **List.multi-line text** | Reinstated per the doc — **resolves the "drop reviews entirely" ambiguity in favour of keeping Press & Reviews.** Source splits `Review quote` (8/63) + `Review text` (0/63); confirm with Dave which maps in and whether it's a repeatable list per title. |
| `custom.tags_global` | Tags (global) | Single line text | Verbatim, **NOT** native Shopify tags. Carries `PUBCODE: BZ1 - SCHIFFER…` on 63/63 rows. |
| `custom.pubcode` | PUBCODE (inside Tags global) | Single line text | **NOT in the doc — new ask.** PUBCODE is currently a substring inside `tags_global`; the 25% pricing rule needs it discrete to key exclusions (Kumon = CK4). Either Dave surfaces a discrete `custom.pubcode`, or the rule parses `PUBCODE:\s*([A-Z0-9]+)` out of tags_global (fragile). |

**NOT mapped (Sheet 2 rule 16, confirmed):** Illustrations Type, Reading Age. (Reading Age is also corrupted in the export — Excel has coerced values like `5-10` into dates — but it's unmapped, so moot.)

**Source-data integrity flags from the live export (flag to Gazelle; not integration bugs):**
- **Weight junk:** 9/63 under 150g, seven at exactly `0.045kg` (a 256-page hardback can't be 45g). Only matters if `Weight` drives shipping — postage is Billy's flat UK/Europe table, so confirm weight isn't used for rates; if it is, clean at source.
- **Gazelle Price empty on all 63 rows** — confirms it's not sourced from BooksoniX (consistent with the manual, Gazelle-side pricing model).

Grant to create these definitions, then give Dave a mapping template for the `pubcode` + type/list changes.

### Metafield definitions — CREATED & VERIFIED (7 July, this session)
**Status: DONE.** All the above now exist in Settings → Custom data → Products. The 5 pre-existing (publication_date, isbn, author, publisher, language) were left as-is; the other **18 were bulk-created via the Shopify Admin API** (`metafieldDefinitionCreate`, API `2026-07`), not clicked in by hand.

**How (reusable):** Python script `create_gazelle_metafields.py` (in outputs) — reads a client-credentials token, creates each definition. Idempotent (re-run reports "already exists"), non-destructive (only `metafieldDefinitionCreate`, no update/delete), has a `--dry-run` that prints the plan + target shop without writing. Run: `export GAZELLE_CLIENT_ID=…; export GAZELLE_CLIENT_SECRET=…; python3 create_gazelle_metafields.py`. Result: `created=18 already-existed=0 failed=0`.
- **Credentials gotcha:** the app must be BooksoniX Integration in the **Gazelle Dev** org (1 install), NOT the same-named **0-install orphan in the GSD Works org** (still on the delete list). Live token scopes confirmed: `write_products, write_inventory, write_files`.
- **All created as text (single/multi-line) for now** — deliberately, so they ADOPT Dave's current string output cleanly. List/Date/Integer tightening is a later one-time move once Dave sends clean values; doing it now would adopt-and-flag-invalid.

**Verification spot-check — ISBN 9781610355032 ("A Lesson Plan for Woodturning", Linden Publishing).** Definitions bound to Dave's existing values with no re-push. Findings:
- ✅ **Populated & correct:** publication_date, isbn, author, publisher, language, subtitle, pages (136), depth_mm (27), illustrations, author_bio, thema_subjects, bic_subjects, main_subjects, tags_global.
- ✅ **PUBCODE confirmed landing:** `tags_global` = `PUBCODE: CE1 - LINDEN PUBLISHING INC`. Second publisher seen (CE1 Linden vs BZ1 Schiffer in the export) — the `PUBCODE: <code> - <name>` pattern holds across publishers, good for the pricing-rule parse.
- 🔴 **BUG (Dave) — width_mm & height_mm are landing as literal template placeholders:** the fields contain `%sh_width_mm%` and `%sh_height_mm%` (unresolved merge tokens) instead of numbers. Depth resolved fine (27), so it's specific to width/height on Dave's side. Repro: this ISBN.
- 🟠 **Minor (Dave) — main_subjects duplicated:** `DIY: carpentry & woodworking, DIY: carpentry and woodworking` — the `&` and `and` label variants (BIC + Thema) concatenated. Cosmetic but visible if surfaced.
- 🟡 **BISAC blank on this title** — only BIC + Thema populated. Could be genuinely absent or a mapping gap; spot-check a few more titles before concluding.
- ✅ **`publication_date` type resolved:** created as **Single line text** (shows `6 August 2024` plain, no "invalid" flag), so NO Date-type conflict now — but text still can't drive the New-Release "this month" rule or forthcoming logic. **Decision deferred to Step 3:** Dave sends ISO `YYYY-MM-DD` + switch the type, or parse the date in Liquid. Not broken, just not yet capable.

**Build order:** Step 1 (define + verify metafields) is now CLOSED. Next = Step 3: smart collections (Thema → category nav) + New-Release auto-rule (the New-Release part gated on the publication_date decision above). Pricing automation (25%) stays last, blocked on discrete `pubcode`.

---

## Front End Theme Setup

### Theme
- **Shopify Horizon v3.4.0** as the base (Shopify's default since Summer 2025; right choice for a 2026 new build). Not Dawn.
- Upgrade-safe rules: never edit Horizon core files; create new files in `sections/` and `blocks/` with a `gazelle-` prefix; use custom template JSON (e.g. `templates/product.gazelle.json`); keep custom CSS scoped per block via `{% style %}`; document overrides. Lazy-load below-the-fold; minimise JS; no page builders / third-party UI frameworks; test on mid-range Android / slow connection.

### Dev environment (set up)
- Homebrew; Node.js v22 LTS (v25 caused SSL errors); Shopify CLI 3.92.1; Git; GitHub Desktop (preferred over terminal git); VS Code (Liquid extension). **`code .` shell command not installed — use `open .` then drag into VS Code.**

### Local project locations
- **Theme:** `~/Sites/gazelle-horizon` (forked from `Shopify/horizon`; remote `github.com/gsdworks/gazelle-horizon`).
- **App CLI project** (for scope changes): `~/booksoni-x-integration` (hyphenated, Shopify auto-named). Independent of the theme; both use the `shopify` binary.

### Dev theme / preview
- Dev theme kept in sync by the CLI. Named Billy previews are created with `shopify theme push --unpublished --theme "dev theme DD-MM"` then previewed from admin → Online Store → Themes. **Always ask Grant for the current date before naming a preview theme** (convention: `dev theme DD-MM`).
- Store is behind password protection. **Billy must not touch password settings until given the green light** — the primary domain already points at the new store via the `store.gazellebooks.co.uk` subdomain, so disabling the password would expose a dev environment.

### Terminal aliases (~/.zshrc)
```
alias gazelle="cd ~/Sites/gazelle-horizon && shopify theme dev --store gazelle-books-2026.myshopify.com"
alias gazelle-pull="cd ~/Sites/gazelle-horizon && shopify theme pull --store gazelle-books-2026.myshopify.com"
alias gazelle-push="cd ~/Sites/gazelle-horizon && shopify theme push --store gazelle-books-2026.myshopify.com"
```

### Workflow
- Code changes: edit `.liquid` in VS Code → commit in GitHub Desktop. Content changes (editor): run `gazelle-pull` first to bring `templates/*.json` down, then commit. `templates/index.json` (and the footer/header group JSON) hold section/block placement + settings.
- **End-of-session routine (always): `gazelle-pull` → commit (incl. JSON) → push origin.**

### Custom homepage sections already built (live theme)
`gazelle-hero.liquid` (rotating slideshow), `gazelle-focus.liquid` (three-panel scroller), `gazelle-strip.liquid` (static banner), `gazelle-categories.liquid` (circular icon grid). Billy will supply final round-icon assets + homepage slider images (he'll make them in Canva); category icons likely stay the same set.

---


---

## Custom Sections Built (Homepage)
All sections are page-width (max-width 1200px, centred). Each has a desktop image slot and a mobile image slot (mobile slot is optional — nothing renders if empty).

| Section File | Description | Status |
|---|---|---|
| `sections/gazelle-hero.liquid` | Auto-rotating slideshow with dot indicators, configurable autoplay speed | ✅ Built |
| `sections/gazelle-focus.liquid` | Three-panel horizontal scroller with left/right arrows | ✅ Built |
| `sections/gazelle-strip.liquid` | Static full-width banner image | ✅ Built |
| `sections/gazelle-categories.liquid` | Circular icon/emoji grid linking to categories — horizontal scroll on mobile | ✅ Built |

Placeholder images currently in use (Billy's test assets — desktop sizes only, mobile images TBC):
- Hero: Manga & Graphic Novels banner
- Focus: Debrett's panels (x3 — same image placeholder, different panels to be supplied)
- Strip: Montagud Editores banner

### Holding Page
- `templates/password.liquid` customised with "New website launching soon" title and a "Back to main website" link pointing to gazellebookservices.co.uk
- Back link sits inside the newsletter signup conditional block, so visibility depends on that setting being enabled in theme editor
- Store currently behind password protection. **Billy should be briefed not to touch password settings until given the green light** — primary domain is already pointing at the new store via the `store.gazellebooks.co.uk` subdomain, so accidentally disabling the password would expose a dev environment to the public.

### Product Card Image Fix
- Horizon's default `object-fit: cover` was overridden using CSS custom property `--product-media-fit: contain` targeted on `.product-media-container`
- Image ratio set to Portrait in theme editor for Collection and Featured Collection sections
- Max-width and centring applied. Worth revisiting once real product data is populated.

---

## Front-End Liquid Build (Claude Code)

The front-end Liquid build runs through **Claude Code** (Opus 4.8) in the `gazelle-horizon` repo, with the **Shopify Dev MCP** connected for live Liquid / theme-check validation. **`CLAUDE.md`** (committed to the repo root) encodes the conventions the agent must follow; the three June mockups now live in **`_design/`** in the repo for the agent to reference (committed).

### Product card — BUILT (2 July)
- **`snippets/gazelle-product-card.liquid`** — the shared, reusable atom (collection, homepage, related-products all render it). Committed (`578c788`).
- Takes a `product` param. Renders: cover (Horizon `image_tag`, `object-fit: contain`, portrait 2/3, lazy-loaded, placeholder fallback), **format** label (`product.type`, sentence case per Billy’s less-all-caps steer), **title** (native), **author** (`custom.author`, leading `"By (author):"` stripped via `remove_first | strip`), **price** (native `| money`, no compare-at / save / percentage). **No wrapping `<a>`** — Horizon’s grid shell supplies the whole-card link; nesting anchors would be invalid.
- Scoped CSS in one `{% style %}` block; brand colours as hardcoded hex (deliberate, brand-consistent — note they do NOT follow Horizon colour schemes); fonts bound to Horizon vars (see Fonts note).
- **Reuse via** `{% render 'gazelle-product-card', product: <product> %}`.
- **Not yet wired into any template** — the snippet exists but renders nowhere until the `collection.json` wiring edit is done (next session).

### Product page files — BUILT (8 July)
- **`snippets/gazelle-book-specs.liquid`** — specs table (label/value `<dl>` rows), all confirmed metafields with `.value`, empty rows hidden, dimensions un-guarded (Dave bug visible by design). Rendered inside the detail band's Product Details tab.
- **`sections/gazelle-book-detail-band.liquid`** — the custom two-column bottom band (2fr/1fr, 48px gap, mobile stacks). Left: tabs-desktop/accordion-mobile (first custom JS — scoped IIFE, aria-correct). Right: extensible rail — Subjects + Classification cards, comma-split chips. Product resolved via `section.settings.product | default: product` (the Horizon section pattern).
- **`snippets/gazelle-cover-styles.liquid`** — scoped `{% style %}` only, rendered via a custom-liquid block in `product.json` (**block is COMMITTED — do not lose it, see pull-clobber lesson**). Contains: cover sizing (570px fixed height / natural width / contain / left-aligned / border+shadow, all `:only-child`-gated for multi-image safety), the hero 1200px `--page-width` override, the proportional hero grid, and the buy-box right-edge inset.

### The grid-override pattern (REUSE for every commerce page)
Horizon renders product cards via a **private core block** `blocks/_product-card.liquid`, rendered statically by `sections/main-collection.liquid` (`{% content_for 'block', type: '_product-card' … %}`). The card `type` and its allowed child-block whitelist are **baked into core files — never edit them.**
- To put the custom card in the stock grid: in the **template** (`collection.json` etc.), swap the `_product-card` block’s child blocks for a single **`custom-liquid` block** (which IS on Horizon’s whitelist) containing `{% render 'gazelle-product-card', product: closest.product %}`.
- `closest.product` resolves inside block-setting Liquid. This keeps Horizon’s **native faceting, sort, and pagination** intact — only the card’s insides change.
- **Verify by render** that the card shows populated data (not blank); this is the one inferred assumption in the approach.

### Toolchain / environment realities (Claude Code)
- **Always launch `claude` from inside `~/Sites/gazelle-horizon`.** From the home dir it can’t see `CLAUDE.md` or the repo and writes land in the wrong place — this caused silent no-op “builds” during setup on 2 July.
- **The `~/.zshrc` aliases (`gazelle`, `gazelle-pull`, `gazelle-push`) do NOT exist in the agent’s non-interactive shell.** The agent must call the underlying `shopify theme …` commands directly.
- **`shopify theme pull` / `push` need interactive device-auth the agent CANNOT complete.** Pulls and pushes are Grant’s job, run in an interactive terminal.
- **Trust the filesystem, not the agent’s summary.** After any “done”, verify with `git status` / `ls -la` before believing a file was written. (The agent claimed to build three times before any file existed; cause was the wrong launch directory.)
- Dev MCP added **local scope** (`claude mcp add … -e LIQUID=true`) — tied to this machine/repo, NOT committed, so George would re-add it. `LIQUID=true` is what enables Liquid/theme validation (off by default).

---

## BUILD LOG & DELIVERY PLAN (added 7 July evening — the running record)

_This is the master build tracker. Update it as things move. It exists so any new session knows exactly what's done, what's in progress, what's next, and what gates each item — without re-deriving it. Check status against email/Shopify before assuming; don't ask Grant to remember things that can be looked up._

### Delivery strategy — the ORDER Grant wants (confirmed 7 July)
The guiding sequence, deliberately chosen so Billy can be signing off in parallel rather than in series:
1. **PHASE 1 — VISUAL (next ~5 working days, THE CURRENT FOCUS):** get the **product page, collection page, homepage, header and footer** visually **80–90% there** — matching the signed-off June mockups, native-first. The goal is a storefront Billy can *see and sign off on* visually. Perfection not required; "clearly the design, working, browsable" is the bar.
2. **PHASE 2 — PRODUCT DATA:** once Billy is reviewing the visual build, Grant links up all of Dave's BooksoniX integration pushes and ties the metafield work visually into the front-end (the 18 metafields already created/verified → surfaced correctly on the pages). Verify data correctness across publishers/backlist.
3. **PHASE 3 — FEEDS (Fred / AS400):** the order-out, tracking-back, and daily stock files. Last because they're the operational plumbing, not what Billy needs to see to sign off the look.

Rationale: visual sign-off is the unblocker. Get it in front of Billy so his review runs *while* Grant does data + feeds, instead of Billy waiting for everything to be perfect first.

### Environment / current state (as of 7 July evening)
- **Working theme: "GSD Gazelle Build"** (#205873021277), created from local repo and **published live**. The old confusingly-named "dev theme 27-03" set was consolidated and deleted; **"Horizon"** (#199910359389) kept as a clean unmodified base reference. **Push target going forward = the GSD theme.**
- **Repo:** `gsdworks/gazelle-horizon`, branch `main`. Local + GitHub in sync as of end of 7 July session.
- **Tooling available in the strategy chat:** Gmail, Google Calendar, Google Drive connectors are live — **check decision status directly (Billy/Dave/Fred inbox) rather than asking Grant to recall.** Claude Code (Fable/Opus) + Shopify Dev MCP for the repo build.

### Page / component build tracker
| Item | Status | Notes / gates |
|---|---|---|
| **Fonts** (Switzer body + Cinzel headings) | ✅ DONE | Both self-hosted, committed, pushed, live. See Fonts section. |
| **Product card** snippet | ✅ BUILT | `snippets/gazelle-product-card.liquid`. Reused by collection + related rail. |
| **Brand colour schemes** | ✅ DONE (7 Jul eve) | Two schemes built in theme editor. Scheme 1 "Paper" (bg `#faf7f2`, ink/headings `#1a1917`, primary/links `#a11f21`, hover `#7c1516`, border `#e8e2d8`) used site-wide by default. Scheme 5 "Charcoal" (bg `#1a1917`, paper text/headings, red primary button, paper links w/ red hover) for the footer. Committed via pull. |
| **Collection page** | ✅ DONE (7 Jul eve) — Phase 1 | Native-first, matches June mockup with **~zero custom CSS**. Card already wired via `custom-liquid` override. Native settings done in editor: **vertical filter sidebar**, **numbered pagination**, grid gaps. Hero = native title + native description (fed per-collection from collection body text; the "Browse by Subject" eyebrow was **dropped** as unnecessary). Accepted native over mockup on: "Filters" heading (vs "Refine" — locale override not worth it) and results-count position. 3-col not offered natively; current layout accepted (Billy to flag if he cares). Subject filter still gated on taxonomy. |
| **Search & Discovery filters** | ✅ DONE (7 Jul eve) | Configured in the S&D **app** (admin, NOT theme — app-side config, needs no pull/commit). **Format** (source: Product type), **Imprint** (source: Vendor), Price kept, Availability removed. Order: Format → Price → Imprint. Subject waits on taxonomy. |
| **Product page — BOTTOM BAND** | ✅ DONE (8 Jul) | Custom `sections/gazelle-book-detail-band.liquid` (replaced the interim native accordion). LEFT column: **tabs on desktop / accordion on mobile** (Grant reversed the earlier accordion-only decision — mockup tabs won; pattern matches Waterstones et al). Tabs = Synopsis, About the Author (auto-hidden when `author_bio` empty), Product Details (renders `gazelle-book-specs` snippet). **First custom JS in the build** — scoped IIFE keyed on section.id, single markup for both patterns, aria-correct, progressive enhancement. RIGHT rail (extensible — more cards slot in later): **Subjects card** (`main_subjects.value`, comma-split chips, retail-facing) + **Classification card** (Thema/BIC/BISAC code-groups, comma-split, trade-facing — ⚠️ currently shows decoded NAMES not raw codes, Dave item). Share card dropped. Normal-case tab labels, solid red active underline. |
| **Product page — SPECS TABLE** | ✅ DONE (8 Jul) | `snippets/gazelle-book-specs.liquid`. All confirmed fields wired with `.value`: ISBN, publisher, imprint (native vendor), pub date (renders "1 March 2014" nicely), format (native type), pages, dimensions (H x W mm), illustrations, language, audience. Rows hide when empty. **Dimensions deliberately UN-guarded** — the `%sh_height_mm% x %sh_width_mm%` bug shows live on the page as concrete evidence for Dave AND to show Billy the gap is Dave-side, not build-side (Grant's call: "build it, let it show broken, chase Dave"). Semantic `<dl>` markup. |
| **Product page — COVER + HERO (top band)** | ✅ DONE (8 Jul) | `snippets/gazelle-cover-styles.liquid` (render block wired in `product.json` — COMMITTED, see pull-clobber lesson). Covers: **fixed 570px height, natural width per cover** (Grant: same height for consistency, width varies — never crop/stretch), `object-fit: contain`, **left-aligned flush to the Synopsis gutter** (`margin-inline-start: var(--gz-gutter, 24px)`), 1px charcoal `#1a1917` border + single light shadow (mockup's spine + heavy 3-layer shadow dropped — looked gimmicky on flat covers). Hero grid rebalanced to mockup's **proportional `minmax(300px,1fr) minmax(0,1.15fr)`** (was native `1fr | fixed-400px-pinned-right` = dead middle gap); hero constrained to **1200px** (`--page-width` override — theme's `page_width: narrow` = 1400, mismatching the band); buy box right edge inset 24px to align with Subjects card. **All four content edges key off `--gz-gutter` 24px** — define it globally later and everything moves together. `:only-child`-gated so multi-image galleries keep native behaviour (some books have multiple images — that's why native media block kept, not replaced). |
| **Product page — REMAINING** | ⏭ NEXT SESSION | **Buy-box supporting elements:** subtitle (`custom.subtitle.value` — confirmed real), author line (`custom.author.value`), imprint/publisher links, trust/delivery strip (native icon+text blocks, 2 per item, Grant OK'd). **⭐ Remove BISAC code-group from Classification card** (Billy 8 Jul: "BIC & THEMA are sufficient" — tiny edit to `gazelle-book-detail-band.liquid`; keep the field as data, just don't display). **New Release ribbon: Billy WANTS it — deferred, do NOT drop** (keyed on `custom.publication_date`). **Gated:** price display (Billy, struck-RRP vs no-save — build Gazelle-price-only default), Press & Reviews (reviews conflict), Subjects→filtered-collection links (taxonomy). Omitted for v1: notify-when-back-in-stock, wishlist, share. |
| **Homepage** | ⏭ QUEUED | Sections already partially built (`gazelle-hero/focus/strip/categories`). Match June mockup; Billy to supply final Canva category icons + slider images (desktop scales; **dedicated 800×367 mobile hero image**). |
| **Header** | ✅ DONE (14 Jul) | Native header restyled/configured, logo-left + inline nav + announcement bar, Scheme 1. Possibly zero-CSS. Deviations for Billy: native icons vs mockup text labels; GBP/localization off. Nav still old placeholders (incl. "Catagories" typo — do NOT ship); real labels gated on taxonomy. |
| **Page width (global)** | ✅ DONE (14 Jul) | `snippets/gazelle-layout.liquid` overrides `--page-content-width: 1200px` on `body.page-width-narrow`; Horizon's native calc derives `--page-width`. THE single global source; product-page local override removed. Narrow preset is really **1440px**, and `--page-width` lives on `<body>` not `:root`. ✅ **Featured Collection carousel containment DONE (16 Jul)** — fix lives in the same snippet (`grid-column: 2` + `--util-page-margin-offset: 0px` scoped to `.section-resource-list`); cause was native `force-full-width`, not the calc. See the 16 July note. |
| **Footer** | ✅ DONE (14 Jul) | Native four-column footer group + utilities bar, Scheme 5 Charcoal, styled to mockup via `sections/gazelle-footer-styles.liquid` (style-only section — `custom-liquid` is NOT whitelisted in the footer schema). Menus `footer-help`/`footer-explore` created; policy pages created (wording review later); company/legal text block in (three-paragraph structure is load-bearing for the CSS). Remaining cosmetics at go-live: store name in copyright, real social URLs. Help/Explore links point at `/` until content pages exist — re-point in admin Navigation, no theme work. ⚠️ Fragility note: footer text-block CSS keys off structural preset classes (`.paragraph`/`.h3`/`.rte`) and assumes ONE text block per preset in the footer — adding another footer text block of the same preset needs a more specific hook (documented in the section file's comment). |
| **Menu / navigation** | ⏭ QUEUED | Set nav in Shopify admin → Navigation. **Labels gated on subject taxonomy** (Billy) — structure can be built, final labels wait. |
| **Content / static pages** | ⏭ QUEUED | Delivery Info, Returns, FAQs, Contact, About, Our Publishers, Services. Design how these look (not yet mocked). |

#### Open items & sequencing (added 14 July PM)

**⭐ Featured Collection carousel — page-width containment — ✅ RESOLVED 16 July.** _(Kept in full: the WRONG first diagnosis is preserved deliberately as the lesson.)_
- **Why it mattered:** Billy is replicating the **Waterstones homepage** — a row of ~6 products with an arrow advancing to the next set inside a contained carousel. The June mockups copy that reference, so this was matching an approved design, NOT optional polish.
- **❌ THE 14 JULY DIAGNOSIS WAS WRONG.** It recorded: *"the carousel computes `--section-slide-width` as `(100% − gaps − peek) / column-count`, where `100%` resolves against the scroller/viewport rather than the section's 1200 content box."* That observation was **accurate but rooted in the wrong place** — it described the symptom and inferred a calc bug.
- **✅ ACTUAL ROOT CAUSE (16 July, full file trace):** `snippets/resource-list.liquid` (L98–113) **hard-codes the `force-full-width` class** onto the outer `div.resource-list.resource-list__carousel` in the carousel branch. Core `assets/base.css:510` then does `.section > .force-full-width { grid-column: 1 / -1 }`, spanning ALL THREE grid columns of `.section` (margin | centre | margin) — i.e. the viewport, not the constrained centre column. Every element in the chain down to the slides is `width: 100%`, so the calc's `100%` faithfully resolves against a viewport-width track. **The track is full-bleed BY NATIVE DESIGN. The calc was doing exactly what it should.**
- **✅ NATIVE-FIRST EXHAUSTED (not assumed):** `section_width` was set to **`page-width`** and it broke out regardless. `force-full-width` is applied **unconditionally for `layout_type: carousel`** — **there is no native setting that disables it.** This was established **in the theme editor** (Grant screenshotted the panel showing Width=Page, Columns=6, Product count=12), NOT from the file trace. **The agent never answered the "under what condition is the class applied?" question and jumped straight to a CSS override** — the config path was ruled out by a human in the editor. That check is what licensed the custom CSS; without it the override would have been native-first violated.
- **✅ THE FIX (committed + pushed + live 16 July):** added to the **EXISTING `snippets/gazelle-layout.liquid`** — deliberately NOT a new file (the agent proposed one; overruled: `gazelle-layout` is already THE single global source of width truth and already render-hooked in `theme.liquid`, and this carousel also renders in related-products on the product page, so the fix is global by nature):
```css
.section-resource-list > .resource-list__carousel.force-full-width {
  grid-column: 2;                  /* undo force-full-width: sit in the 1200px centre column */
  --util-page-margin-offset: 0px;  /* cancel the full-bleed first-slide inset + arrow padding */
}
```
- **Why each half:** `grid-column: 2` re-places the wrapper in the constrained centre column. Zeroing `--util-page-margin-offset` cancels `--gutter-slide-width` (an inline `var()` on the inner wrapper, `resource-list-carousel.liquid:19`) and the arrow padding — both sized to re-align a viewport-width track, and both would otherwise push content right again inside the now-1200 box.
- **Specificity:** `0,3,0` (`.section-resource-list` + `.resource-list__carousel` + `.force-full-width`) beats core's `0,2,0` (`.section > .force-full-width`) — **no `!important` needed.** No core file touched.
- **Peek preserved** — the 48px `--peek-next-slide-size` reservation lives INSIDE the slide-width calc, so it survives container constraint; the sliver simply relocates from the viewport edge to the 1200px edge. (Note: the reservation is container-independent, but the *apparent* sliver size shifts because each card gets smaller — don't over-claim "independent of container width".)
- **Result: 6 full cards + a peek sliver** (was ~8.5 cards running off the right edge). Verified **by render** at desktop width — the honest bar. DevTools computed-value checks (`slideshow-slides` `padding-inline-start` → 0; slide width → ~180px) were attempted but ran inside **iPad emulation at 820px**, where a 1200px constraint is meaningless. Those two values remain formally unconfirmed; if the first slide ever looks inset, that is caveat 7.1 (the `--util-page-margin-offset` inheritance not reaching the descendant's inline `var()`) and the fallback is `--gutter-slide-width: 0` on the inner wrapper.
- **⚠️ Selector scope, decided not inherited:** `.section-resource-list` catches **every** product-list carousel — including related-products on the product page. That consistency is wanted here, but it was a decision, not an accident. Revisit if a deliberately full-bleed carousel is ever added.
- **Open design point for Billy:** Waterstones does clean 6-then-6 with **no** peek of card 7. We keep the peek (Horizon's native affordance, signals scrollability). That is a visible deviation from his reference — **mention it in the next update rather than letting him spot it.**
- **Do NOT:** kill the peek or convert to a static grid.

**Build sequencing (decided 14 Jul; carousel closed 16 Jul):** header (placeholders) ✅ → carousel containment ✅ (16 Jul) → subject-distribution **analysis** off the live/sample data → **one-page taxonomy proposal to Billy** (natural top-level groupings + title counts per group + ghost-category warnings; note the subject data is still mid-sync and dirty — `main_subjects` `&`/`and` dupes, BISAC leakage — so it's a proposal INPUT not a final map) → build collections → nested Navigation lights up the mega menu. **Collections are TWO separate problems, don't bundle them:** (1) **subject taxonomy** collections (nav, breadcrumbs, product-page subject links) key off Thema/BIC/`main_subjects` — Billy's decision; (2) **homepage curation** (Focus/Highlights) keys off PUBCODE — blocked on Dave surfacing PUBCODE as a discrete metafield.
- **Mega menu content** — never mocked (all June mockups flat nav); send Billy a one-liner (links-only vs featured titles) WITH the taxonomy proposal. Smart-collection-via-metafield vs tag-based is an open choice that affects which field Dave must clean first.
- **`.blog-posts` width gap** — `sections/main-blog.liquid` redeclares `--page-content-width`/`--page-width` on its own `.blog-posts` element, so the blog listing stays at the ~1440 preset regardless of the global fix. Core file — leave it. Moot if blogs are dropped from the nav; if kept and 1200 wanted, fix via the same scoped style-section pattern (never edit the core file).
- **`gazelle-focus.liquid` theme-check errors** — pre-existing img width/height offences surfaced during the 14 Jul theme-check. Untouched file; pick up in the homepage session.

### Session log — 7 July evening (detail)

What got done, in order: **fonts** (Switzer + Cinzel, self-hosted — see Fonts section), a full **theme consolidation** onto "GSD Gazelle Build July 7th", both **brand colour schemes**, the **collection page** to Phase-1 done, and **Search & Discovery** filters. Net result: a genuinely Billy-ready collection page — brand fonts, brand colours, mockup-matching sidebar filters, real covers, numbered pagination, charcoal footer.

**Two useful discoveries banked this session:**
1. **Format-combining can be done natively in Search & Discovery "grouped values"** — the S&D filter editor lets you group multiple raw ONIX format values (Kit, Loose-leaf, Pamphlet, Poster, Spiral bound, Fold-out, Mixed-media…) under single labels (Hardback / Paperback / Other). This means the **product-type combine job may NOT need to sit inside Dave's integration** — it could be a native S&D grouping instead, which would simplify that open item. Still pending Billy's finalised combine list before we group; for now the Format filter shows all raw values (fine for the sign-off demo).
2. **Demo collection covers need curating before showing Billy.** The test catalogue has confronting covers front-and-centre (e.g. "165 Days" — masked figures) and broken-image "?" placeholders on titles without covers. The placeholders are just test data (real BooksoniX covers will fill them), but for the **sign-off screenshot/demo** curate the collection to clean, appealing covers — first impressions matter for the visual sign-off goal.

**Process/technique learnings (these feed the CLAUDE.md workflow write-up below):**
- **Read the schema, don't guess.** `config/settings_schema.json` (field definitions) and `config/settings_data.json` (values) are the source of truth for native settings. Reading the colour-scheme definition gave exact field names (7 core fields + Primary/Secondary button + Inputs + Variants groups) instead of guessing — big efficiency unlock. Do this before styling anything or instructing editor changes.
- **Colours belong in the theme editor, NOT in code.** Visual work needs live feedback, and `settings_data.json` is the #1 editor-drift file — editing it in code fights the editor. General rule that emerged: **native settings → theme editor (see-it-live); scoped CSS + custom markup → Claude Code.**
- **Most of the "last 20%" to match a mockup was native settings, not CSS.** The collection page reached ~90% of the mockup with essentially zero custom code — vertical filters, pagination, gaps were all native toggles. Native-first genuinely paid off. The agent's read-and-propose plan correctly labelled each gap as [NATIVE SETTING] / [NATIVE BLOCK] / [SCOPED CSS] and only ONE item needed CSS (facet cosmetic polish — deliberately skipped as not worth it for a trade audience / sign-off).
- **Plan-then-build with the agent.** Used read-and-propose prompts (agent reads + proposes a numbered plan, no edits) BEFORE any build prompt. Vetted the plan together, cut the over-reach. This is the leash working.
- **Editor-vs-code drift is real and must be closed each session.** Editor changes live ONLY on Shopify until pulled. End-of-session: `shopify theme pull` (from the live GSD theme) → commit → push. Tonight that banked `config/settings_data.json` (schemes) + `templates/collection.json` (filters/gaps) as commit `d39b900`.

### Session log — 8 July (detail): PRODUCT PAGE full-day build

**What got built, in order:** specs table snippet → details accordion (native, interim) → replaced by the custom `gazelle-book-detail-band` two-column section (tabs/accordion + rail) → cover treatment + hero layout (`gazelle-cover-styles`). Product page went from "flat description + variant picker" to a genuinely Billy-ready page in one day. Full component detail in the tracker above; this log captures the decisions and lessons.

**Decisions made this session (Grant's calls):**
- **Tabs, not accordion (reversal).** Yesterday's "accordion for v1" was reversed once seen rendered — stacked open sections lost the mockup's tabbed feel and buried the right rail. Final: **tabs on desktop, accordion on mobile** ("what most book sites do" — Waterstones etc). This is the FIRST custom JavaScript in the build — a deliberate, contained exception to minimal-JS, scoped inside the section.
- **Cover sizing: same HEIGHT for all covers, width natural.** Not same-box (would letterbox/crop). 570px desktop (Grant sized it up 20% from an initial 475 vs the mockup). Never crop, never stretch — `object-fit: contain`, width follows each cover's true ratio.
- **Spine + heavy shadow dropped** from the mockup's cover treatment — looked gimmicky on flat cover images. Final: 1px charcoal border + one light shadow.
- **Native media gallery KEPT (not replaced with a custom cover block)** because some books have multiple images — the custom-block route would have lost the gallery/carousel. All cover CSS is `:only-child`-gated so multi-image books keep native behaviour untouched. Zoom not needed but comes free.
- **Dimensions row deliberately un-guarded** — the `%sh_%` tokens render visibly. Grant's call: it proves the front-end works, makes the gap demonstrably Dave-side to Billy, and self-heals when Dave fixes the source. "Build it, let it show broken, chase Dave."
- **Subjects vs Classification = two audiences.** Subjects card (plain names, `main_subjects`) for retail; Classification card (Thema/BIC/BISAC) for trade/wholesale buyers who work in official codes. Built BOTH wired to their fields so whatever Dave pushes flows through automatically — but the classification fields currently hold decoded NAMES not raw codes, so the two cards duplicate each other until Dave switches the source (email sent 8 July, cc Billy).
- Rail built **extensible** — more cards (Subjects links once taxonomy lands, Share if ever wanted) slot in beneath without rework.

**⚠️ THE PULL-CLOBBER PATTERN — the day's biggest lesson (bit us THREE times):**
Custom-liquid render blocks added in the theme editor live in `templates/product.json` on Shopify only. Until pulled AND committed, every subsequent `shopify theme pull` can wipe them (pull mirrors Shopify→local, and pushing local-without-the-block wipes them Shopify-side too). Today this (1) deleted the uncommitted specs snippet, (2) reverted the committed tabs build with a stale Shopify copy, (3) silently stripped the `gazelle-cover-styles` render block so hours of cover CSS sat in a file nothing loaded — "the CSS isn't wrong, it isn't RUNNING" was the repeated failure mode. **The rules now:**
1. **Commit before EVERY pull** — committed work is always recoverable (`git restore` / `git checkout <sha> -- file`); uncommitted work is gone.
2. **After adding ANY editor block: pull + commit IMMEDIATELY.** The render block only becomes durable once it's in git.
3. **Once local is newer than Shopify and pushed — DO NOT PULL.** Pull only when the editor genuinely has changes you lack. Pulling "to be safe" is how stale Shopify copies revert newer local work.
4. **Debug checklist when custom CSS "stops working": FIRST check the render block still exists** (`grep -c "gazelle-cover-styles" templates/product.json`) before touching any CSS.

**Technical learnings (Horizon gotchas — bank these):**
- **Metafield `.value` rule:** every metafield output MUST end `.value` (`custom.author_bio.value`). Editor inline-Liquid validates hard; snippets can silently misbehave. Native fields (vendor, type) must NOT get `.value`. Applies to every metafield on every page from now on.
- **`page_width: narrow` = 1400px**, but the whole Gazelle build is on 1200. Fixed by scoping `.product-information { --page-width: calc(1200px + var(--page-margin) * 2) }`. Any future native section will have the same 1400-vs-1200 mismatch vs our bands — same fix.
- **Theme's media wrappers carry `overflow: hidden` (≥750px)** which clips box-shadows on cover images. Fix: `overflow: visible` on the inner `.product-media` wrappers (scoped, `:only-child`-gated).
- **`media_fit` is a dead setting** when a fixed aspect ratio is chosen — the code hardcodes `media-fit-cover` and never reads it. Native "contain" setting silently does nothing; that's why editor toggles couldn't fix the cover.
- **The `--gz-gutter` (24px) alignment system:** cover-left, buy-box-right, and the band's two inner edges all key off `var(--gz-gutter, 24px)`. Currently each falls back to the 24px literal; defining `--gz-gutter` globally later moves everything in lockstep. (Caveat: hero and band use different width MODELS, so edges pixel-match only ≥1280px viewport — fine for the design target.)
- **Hero grid native default is `1fr | min(50vw, var(--sidebar-width=400px))`** — cover column over-stretches, buy box pinned right as a fixed 400px strip. Mockup's proportional `1fr : 1.15fr` is the fix. If the buy box ever reads too wide with real data, the lever is the second fraction (`1fr` or `minmax(0, 520px)`).

**Method learning — DIAGNOSTIC-FIRST is now the standard for layout/CSS problems.** Every blind CSS guess today swung wrong (too big → too small → wrong edge); every read-only Claude Code diagnostic ("report exact cause + minimal fix, no edits") landed the precise one-line fix first time — including catching things guesses never would (the dead `media_fit` branch, the overflow clip at line-level, the 24px gutter as exact difference, margin-vs-padding because of an inline style shadow). The loop: **symptom → read-only diagnostic → vetted exact fix → commit → push → verify render.** Also of note: verify-by-render replaced code-review when terminal pastes failed — screenshots of the rendered page are legitimate verification.

### Session log — 14 July (detail): FOOTER build

**What got built, in order:** admin menus + policy pages → footer blocks in the editor (with mis-nesting fixed) → `sections/gazelle-footer-styles.liquid` created by Claude Code and added to the footer group → iterative CSS refinement against screenshots → final render matches the June mockup. All commits pushed to origin and the theme by session end.

**Editor build (the fiddly bits worth remembering):**
- **Final block structure (footer section, top level):** Group "Newsletter" (heading + rich-text copy + email-signup, all nested inside) | Menu → Footer Help (heading "Help") | Menu → Footer Explore (heading "Explore") | Text (company info). **Exactly 4 top-level blocks — the footer grid caps at 4; a 5th wraps to an orphan row.** Nesting the signup inside the group is what keeps it at 4.
- **Failure modes hit and fixed:** Menu/Text blocks accidentally nested INSIDE the newsletter group (drag out in the sidebar); the second menu block silently bound to Main menu (rebind to Footer Explore); block widths on Fill causing full-width stacking (set to Fit).
- **Company text block:** three-paragraph structure is LOAD-BEARING for the CSS — P1 company name alone, P2 address/phone/email with Shift+Enter line breaks, P3 the registered line. Shopify's rich-text editor stores Enter inconsistently (sometimes `<br/><br/>` inside one `<p>`, sometimes a real `</p><p>` split) — the reg-line styling only became reliable once it was a genuine separate paragraph.
- **Email-signup block settings:** corner radius 100 → 2; Integrated button OFF. The toggle alone does NOT stack input above button — the stacking is CSS (flex column on the input group).
- **Admin:** `footer-explore` menu had to be created (only `footer-help` existed). All four policy pages created from Shopify's templates so the native policy-list populates.

**The style-only-section injection pattern (NEW, reusable):**
`custom-liquid` is **not on the footer section's block whitelist** (unlike the product template), so the render-block pattern from `gazelle-cover-styles` doesn't work here. The alternative: a **section** that emits only `{% style %}` (no markup), with schema `enabled_on: {"groups": ["footer"]}` **plus a presets entry** (required or it never appears in the Add-section picker), then added to the footer group in the editor. This is the general-purpose way to inject scoped CSS into any section group whose block whitelist excludes custom-liquid.

**The selector diagnosis (the session's key debugging arc):**
First CSS attempt targeted `.text-block--<block-id>` using the block IDs from `footer-group.json` — those rules were completely dead while the class-based menu rules worked fine. Read-only diagnostic found it: **Horizon's runtime `block.id` is NOT the JSON key** — the rendered id differs, so id-based selectors never match editor-owned blocks. Fix: target **structural preset classes** instead (`.text-block.paragraph` for body text, `.text-block.h3 :is(h1,h2,h3,h4,h5,h6)` for the heading, `.text-block.rte:not(.paragraph)` for the newsletter copy), scoped to `.footer-content`. Documented assumption: ONE text block per preset in the footer. Second break in the same area: retyping the heading text flipped the inner tag h2→h3, killing a tag-specific selector — fixed tag-agnostic with `:is(h1..h6)`. Two more CSS realities: **there is no `::last-line` in CSS** (why the reg line needed its own `<p>`), and `p:first-child::first-line` works for the company name only because the explicit line break pins where the first line ends.

**⚠️ Pull-clobber, round two — it extends to OUR OWN code files.** A mid-session `gazelle-pull` reverted Claude Code's committed selector fix with the stale theme copy of `gazelle-footer-styles.liquid` — the diff showed the new work in red. Caught before commit → Discard changes in GitHub Desktop → verified with `grep -c ":is(h1" sections/gazelle-footer-styles.liquid` (returned 2) → re-pushed. **Extended rules:** (1) pull-clobber is not just an editor-owned-JSON problem — any file newer locally than on the theme gets reverted by a pull; (2) **when local is ahead, PUSH before any pull**; (3) never commit a pull-diff without reading its direction (red on your own recent work = the pull is stale, discard it). Targeted push used all session: `shopify theme push --theme 205873021277 --only sections/gazelle-footer-styles.liquid`.

**Claude Code observation:** the agent CAN commit via its own terminal (it showed the diff per CLAUDE.md and wrote a good message — commit `39f8fff` "Footer styles: target text blocks by preset class, not block id") but it does NOT push to origin — the Push origin button in GitHub Desktop is still needed after an agent commit.

**Accepted deviations + parked items:** native "Terms and Policies" popover instead of four inline policy links (popover contents left native/light); Sign up button roundness inherits the GLOBAL button style — squaring it is a site-wide decision (mockups suggest squared everywhere), parked for a deliberate pass. Go-live flags: copyright renders the store name ("© 2026 Gazelle Dev" — rename the store at launch), social URLs placeholder, policy wording review.
 
### Session log — 16 July (detail): CAROUSEL FIX + the stale-diagnostic lesson

**What happened, in order:** asked "what's next?" → reconciled against past chats (caught that the mounted file was stale and the header was already built) → carousel diagnosis → **caught the agent reasoning from a stale `index.json`** → pull → fix → verify by render → commit/push → context file (which took longer than the fix).

**The arc worth remembering.** The 14 July note said the carousel bleed was a `--section-slide-width` calc problem. The read-only diagnostic then traced it properly and found `force-full-width` — but buried the significance: its own trace line *"the force-full-width class on carousel layouts is a key lead"* appeared mid-investigation and **reframed the entire problem from bug to native design**, which the report's TL;DR did state, but only after having already been sent down a calc-shaped path by our prompt. **Our prompt carried the wrong hypothesis** ("the calc resolves against the wrong parent") and the agent partially followed it. Lesson: **a diagnostic prompt that embeds a hypothesis will bias the diagnosis.** Ask "what causes X" not "confirm that Y causes X".

**The stale-diagnostic catch (the expensive one).** The agent's report stated `columns: 4, max_products: 8` and did arithmetic on it. Grant screenshotted the editor: **Columns 6, Product count 12** — set on 14 July and never pulled. The `git diff` on the subsequent pull confirmed it exactly: `max_products: 8→12`, `columns: 4→6`. **Every number in the report was fiction, and the report was long, confident, and well-argued.** Nothing about its quality signalled the problem. Only the screenshot did. **New rule (now in Key Lessons): pull before any DIAGNOSTIC that reads editor-owned JSON, not just before edits.**

**What the pull also revealed — a genuine bonus.** Billy's real artwork had landed in the editor and nobody had recorded it: hero → BroadviewPress / Kodama / PMI; focus → Debrett's / Marian Press / Right Book (**matching his curation map exactly**: DA1 / CZ3 / CL8); strip → Montagud. All `_-_TEST.png` gone. **This quietly closed the last big Phase 1 unknown** while the tracker still said "Billy to supply assets". Also in the diff: `gap` 0→20, Bestsellers `emoji` → `""` (Grant's, kept). **Point worth holding: editor drift is not only a risk to manage, it is also information you are not receiving.** A week of unpulled editor state hid both a stale diagnostic AND a completed dependency.

**The fix itself was small** — see the corrected carousel entry in Open Items for the full technical record. Notable only for what nearly went wrong: the agent proposed a **new snippet file** (overruled — it belongs in `gazelle-layout`, the existing single source of width truth, and the carousel also renders in related-products), and it **never checked whether a native setting controlled `force-full-width`** (Grant ruled that out in the editor — Width was already set to Page and it broke out anyway). Without that human check the CSS override would have been a native-first violation dressed up as a well-traced fix.

**Verification honesty.** The DevTools checks were run in **iPad emulation at 820px**, where a 1200px constraint is meaningless — they proved nothing and were abandoned. The desktop render (**6 cards + sliver**, down from ~8.5 cut off) is the evidence. `slideshow-slides` `padding-inline-start: 0` and slide width `~180px` remain formally unconfirmed; if the first slide ever looks inset, that's caveat 7.1 and the fallback is `--gutter-slide-width: 0` on the inner wrapper.

**⚠️ The context file cost more than the build.** ~40 minutes lost across **five wrong downloads** (925 / 868 / 960 / 905 / 960-again — two byte-identical) because **two sessions ran on 14 July** and the 3:15pm one (960) looks convincingly current by timestamp. The 985 existed only as an artifact in the *other* 14 July chat. **This is the third stale base in a week.** Grant's fair point: the missing `.md` download button in projects is a real Claude UI bug and the root cause. The honest counter: the 985 *was* downloadable as an artifact and just wasn't pulled before the session closed — the bug removed the normal path, the workaround existed and got skipped. **Either way, the conclusion is the same: stop patching the discipline, fix the mechanism — move the file into the repo.**

**Git note:** `git push` over HTTPS now fails ("Password authentication is not supported" — GitHub killed it). GitHub Desktop works. Also: when git threw the `Username for 'https://github.com':` prompt, the **three commands already typed into the terminal got eaten by the prompt** and silently never ran — worth knowing, it looks like they executed.

### Ways of working with Claude Code — the collaboration loop (PREFERRED METHOD from 7 July)

This is now the default way we build, and it supersedes hand-editing everything in VS Code (VS Code / GitHub Desktop are still used, but as part of this loop, not the whole method). The loop:

1. **Claude Code reads the real repo files directly** — rather than Grant pasting files into the strategy chat or Claude guessing. When we need to understand current state (a template, the mockup, a snippet), we send Claude Code a **read-only prompt** and it reports back. It reads the *actual* committed files, so no stale/guessed context.
2. **Read-and-propose before build.** For anything non-trivial, Claude Code first proposes a **written plan** (numbered, labelling each item e.g. [NATIVE SETTING] / [NATIVE BLOCK] / [SCOPED CSS]) — **no edits yet.**
3. **Vet the plan in the strategy chat.** Grant + Claude (this chat) review the plan together, approve the sensible parts, cut over-reach, resolve judgement calls (native vs custom, what's worth doing for the sign-off bar).
4. **Claude Code executes the approved plan** — edits the files directly in the repo, one scoped task at a time. Tight, execution-only prompts.
5. **Grant verifies with `git status` / `git diff`** — NOT the agent's own summary. Trust the filesystem, not the narration. (The agent has claimed "done" before writing anything; always check.)
6. **Grant runs the interactive bits the agent can't** — `shopify theme pull`/`push` (device auth), commits, GitHub pushes. Pulls/pushes are always Grant's job.
7. **Two-surface split:** THIS strategy chat for planning, judgement, specs, email/decision checks, and context-file maintenance; **Claude Code for execution in the repo.** Each does what it's best at.

Key guardrails inside the loop: agent stops and asks if the native path isn't obvious (never invents custom when native exists); never edits Horizon core files (logged exceptions only); every "done" is verified against git, not trusted. Colours/native settings are done in the **theme editor** (live feedback), not by editing `settings_data.json` in code.

**⭐ TODO NEXT SESSION — write the detailed CLAUDE.md WORKFLOW section (Grant's request, 7 July).**
Grant wants the "how we work" process captured in detail in the repo's `CLAUDE.md`, structured so it can later be lifted into a **generic, client-agnostic Bowden Studio template** for future Shopify builds. Capture it in Gazelle's CLAUDE.md now (real + proven), extract the reusable version later. The section should cover:
- **The core loop:** native-first → **audit the existing library FIRST (see below)** → read the schema to find what's native → close gaps with scoped `gazelle-` CSS/snippets only where native genuinely can't → agent executes, human owns judgement.
- **⭐ Native-first, one level deeper — AUDIT THE LIBRARY BEFORE BUILDING CUSTOM (added 8 Jul, Grant).** Before writing ANY `gazelle-` snippet or block, inventory what the theme already ships. Horizon has a large `blocks/` + `snippets/` library; if a native block already covers the need (trust/icon rows, accordion, product-inventory, complementary products, share, badges, etc.), USE IT. Building a custom version of something that exists out-of-the-box is the exact waste native-first exists to prevent. The audit is a REQUIRED step, not optional: read the library, match against the needs list, THEN decide native-vs-custom per item. This is the first principle applied a level deeper — "don't build what the theme already gives you." **⭐ Add this to the CLAUDE.md workflow write-up too.**
- **⭐ The Claude Code collaboration loop** (read → propose → vet → execute → verify → human runs interactive bits) — the full 7-step version is written up in the "Ways of working with Claude Code" subsection above; fold it into the CLAUDE.md write-up as the preferred build method, contrasted with the older hand-edit-in-VS-Code approach.
- **Plan-then-build discipline:** read-and-propose prompts before build prompts; approve the plan first.
- **The agent leash:** execution-only, stops when the native path isn't obvious, never touches core, verify against `git status` not the agent's summary.
- **Git/theme safety rules:** commit-before-pull, pull-before-edit, ONE clean named theme, launch Claude Code from the repo dir, `GIT_PAGER=cat` to dodge the pager, two-identically-named-themes caused a mis-push (naming discipline matters).
- **The editor-vs-code split:** native settings (esp. colours) in the theme editor for live feedback; scoped CSS + custom markup via Claude Code.
- **Schema-first technique:** read `settings_schema.json` / `settings_data.json` before styling or instructing editor changes.
- **⭐ The mockup principle (Grant's insight):** draw client HTML mockups *within Horizon's native capabilities from the start* — know what the theme does natively (its card structure, filter layouts, section types, colour-scheme model) and design *to* it. Then mockup and build share ONE mental model, and the build becomes mostly config + light CSS instead of fighting the framework. This is the front-end bookend of native-first (design native-aware → build native-first → gap-close with CSS). A real competitive edge for Bowden: faster builds, fewer "we can't do that natively" surprises mid-project, and mockups honest about what'll ship.
- **Caution:** treat the whole thing as a LIVING document, revised per project. The principles (native-first, leash the agent, human judgement) are durable; the specifics (block types, setting names) drift as Horizon/Shopify update — review at the start of each build, don't blind-paste.

### PRE-LAUNCH CHECKLIST (everything that must be ticked before go-live)

**Front-end (Phase 1):**
- [ ] Product page visually complete — **~85% done 8 Jul**: ✅ cover treatment + hero layout, ✅ tabs/accordion detail band, ✅ specs table, ✅ Subjects + Classification rail. REMAINING: buy-box supporting elements (subtitle, author, imprint links, trust strip), New Release ribbon (Billy wants), price display (gated Billy), Press & Reviews (gated), Subject links (taxonomy)
- [x] **Collection page + card grid + native filters wired** ✅ (7 Jul eve — vertical filters, numbered pagination, Format/Price/Imprint via Search & Discovery, ~zero custom CSS)
- [x] **Brand colour schemes** ✅ (7 Jul eve — Paper + Charcoal)
- [ ] Curate demo collection covers before Billy sign-off (test data has confronting/broken covers)
- [ ] Homepage matching mockup with Billy's final assets — ✅ **ARTWORK LANDED (in the 16 Jul pull):** hero = BroadviewPress / Kodama / PMI; focus panels = Debrett's / Marian Press / Right Book (matches Billy's curation map DA1 / CZ3 / CL8); strip = Montagud. All `_-_TEST.png` placeholders gone. ✅ **Carousel containment fixed 16 Jul.** REMAINING: mobile hero images (dedicated 800×367), final round category icons (Bestsellers emoji currently blank), carousel section heading (currently a bare "View all" — check vs mockup), `gazelle-focus.liquid` theme-check img errors
- [x] **Header restyled (native)** ✅ (14 Jul PM — config + tokens, no custom section, possibly zero custom CSS). REMAINING: **`Catagories` typo is LIVE in the nav — do NOT ship**; real labels gated on taxonomy (admin → Navigation, no theme work)
- [x] **Footer built (native), menus created, policy-list populated** ✅ (14 Jul — styled to mockup via `gazelle-footer-styles`; go-live cosmetics remain: store name in copyright, real social URLs)
- [ ] Navigation menus set; final labels once taxonomy lands
- [ ] Content pages designed + built
- [ ] **Policy pages** (Privacy / Terms / Refund / Shipping) — ✅ all four CREATED from Shopify templates (14 Jul), footer policy-list populates. REMAINING: review wording with Gazelle before go-live.
- [ ] Cross-browser + mobile + Lighthouse + Theme Check pass
- [ ] Billy's visual sign-off

**Back-end / data (Phase 2 — Dave / BooksoniX):**
- [ ] All integration pushes verified landing correctly; 18 metafields surfaced correctly on front-end
- [ ] Fix Dave source-data bugs: `width_mm`/`height_mm` `%sh_…%` placeholders (⚠️ now LIVE on product page as evidence — **emailed Dave 8 Jul, cc Billy**); `main_subjects` `&`/`and` dup; confirm BISAC blank vs mapping gap
- [ ] **NEW (8 Jul): Thema/BIC/BISAC fields must carry RAW CODES not decoded names** — currently push subject names ("Literary studies: general") so the trade-facing Classification card duplicates the retail Subjects card. Need actual codes (e.g. AKB) for trade buyers. **Emailed Dave 8 Jul, cc Billy. ✅ BILLY CONFIRMED same day (16:49): codes not names, AND "we don't need to show BISAC, BIC & THEMA are sufficient."** Front-end already wired — self-heals when source switches. **⭐ Front-end follow-up (next session, tiny): remove the BISAC code-group from the Classification card in `gazelle-book-detail-band.liquid`** — display Thema + BIC only (Dave can keep pushing the BISAC field as data; we just don't show it).
- [ ] `author_bio` (About the Author tab) — field exists, empty; tab auto-appears when Dave populates
- [ ] `publication_date` as usable format for New-Release rule (ISO or Liquid parse)
- [ ] Approved-only filter enforced + retro-sweep of non-Approved seeded titles
- [ ] Archive-not-delete on BooksoniX archive (Dave was "looking at it" 3 Jul — chase)
- [ ] PUBCODE surfaced as metafield (dependency for 25% pricing automation — separate quote)
- [ ] Product-type combine list finalised (Billy) → implemented (Dave)
- [x] ~~Spot-check inside spreads + ISBN-13 barcode~~ ✅ **CONFIRMED 3 Jul (Dave)**: spreads syncing (Woodturning 9781610355032), barcode in variant field + inventory-tracked verified via screenshot. Wider backlist spot-check still worthwhile at data QA stage.
- [ ] prices-include-tax confirmed + test order VAT check
- [ ] Subject taxonomy mapping (Billy) — unblocks Subject filter + nav labels + product-page Subject chip links
- [ ] Pricing: Gazelle discount upload; struck-RRP display decision; 25% automation (out of scope, separate quote)

**Feeds / operational (Phase 3 — Fred / AS400):**
- [ ] Outbound order file — resolve A–N vs dual-address (bill-to) regression vs Billy's requirement
- [ ] Inbound tracking file v3 — end-to-end SFTP test (real order → AS400 → tracking back)
- [ ] Daily availability file — ✅ **file arrived + confirmed clean (9 Jul)**: `GazelleAvailability_YYYYMMDD.csv`, 01:29 daily, `0` rows proven in data, no negatives. REMAINING: confirm coverage (all vs warehoused) with Fred; configure Matrixify **update-present-only / never-zero-absent** rule
- [ ] **⚠️ PO round-trip confirmed with Fred** (PO sent in field A echoed back verbatim in tracking) — the join key for the whole round-trip
- [ ] **⚠️ Exact SFTP folder name confirmed** (`/Order` vs `/Orders` — Fred's email says both)
- [ ] Both tools configured as **SFTP** (port 22), not plain FTP — the `ftp.` hostname is misleading
- [ ] **Barcode spot-check across publishers/backlist** — availability import matches on Variant Barcode ONLY; missing/duplicate barcodes fail silently
- [ ] EZ Exporter: discounted unit price (not list), `GB`→`GBR` country conversion
- [ ] Express-checkout billing address sanity-check on a real order

**Go-live:**
- [ ] Point `store.gazellebooks.co.uk` domain at the store
- [ ] Final QA pass on the live domain

---

## Theme Dev Workflow

### How It All Fits Together

There are two types of changes when working on the Gazelle theme:

| Type | Where it happens | Saved by |
|---|---|---|
| **Code changes** | VS Code (writing .liquid files) | Committing in GitHub Desktop |
| **Content changes** | Shopify theme editor (images, section placement, settings) | Running `gazelle-pull` then committing in GitHub Desktop |

The key file to watch is **`templates/index.json`** — this stores all section placement, order, and settings (images, text, speeds etc). The `.liquid` files are the code; `index.json` is the configuration. You need both committed to Git.

Changes made in the theme editor save to Shopify automatically, but do NOT sync back to local files automatically. `gazelle-pull` is what brings them down so Git can track them. If you skip it, GitHub Desktop shows nothing to commit and the work is unprotected.

### Starting a Session
1. Open Terminal
2. Type `gazelle`
3. Open **http://127.0.0.1:9292** in browser
4. Edit files in VS Code — changes hot reload instantly
5. Press **e** in terminal to open the theme editor

### End-of-Session Routine (ALWAYS DO THIS)
1. Open a new terminal tab (Cmd + T)
2. Type `gazelle-pull`
3. Select **Development (ddc695-Grants-MacBook-Air) [yours]** when prompted
4. GitHub Desktop → commit (you'll see `templates/index.json` in the changed files) → Push origin

> **Think of this like hitting Save. Always do it before closing anything.**

### When to use gazelle-push
Only when you want to create or update a preview for Billy. Not needed after every session. Run it, then grab the preview URL from Shopify admin → Online Store → Themes.

### Adding New Sections to the Homepage
1. Drop the `.liquid` file into `~/Sites/gazelle-horizon/sections/`
2. The CLI will hot reload — the section is now available
3. Open the theme editor (press **e** in terminal)
4. Click **Add section** in the Template area and search for it
5. Configure images/settings in the editor
6. Run end-of-session routine to save to Git

### Git / GitHub Workflow
- All custom work is committed to the `gsdworks/gazelle-horizon` fork
- Shopify's upstream `Shopify/horizon` repo can be synced periodically via the **Sync fork** button on GitHub
- Golden rule: never edit Horizon's existing files if avoidable — always create new files for custom work to avoid merge conflicts on update

---

---

## App CLI Project (for future scope changes)

When scopes need to change on BooksoniX Integration (e.g. if Dave says he needs `read_customers` or similar), **don't** try to do it in the Dev Dashboard UI — it's not there. Scopes are configured via `shopify.app.toml` and deployed through the Shopify app CLI.

A local project is already set up for this:

### Location
`~/booksoni-x-integration/` — **separate from the theme project at `~/Sites/gazelle-horizon/`**. Two totally independent things, just both use the `shopify` CLI binary.

### Key file
`~/booksoni-x-integration/shopify.app.toml` — linked via `client_id = "5e994c135911baa59f413b9ac8d79992"` to BooksoniX Integration in Gazelle Dev. The `[access_scopes]` section is what to edit.

### To add/change scopes
```bash
cd ~/booksoni-x-integration
# Edit shopify.app.toml — change the scopes = "..." line under [access_scopes]
shopify app deploy
# Confirm "Yes, release this new version" when prompted
```

Then **reinstall the app on the store** — scope changes on an existing install don't take effect until reinstall. Shopify admin → Settings → Apps → BooksoniX Integration → Uninstall → then Dev Dashboard → Install app → pick Gazelle store.

Verify the new scopes are live by re-running the client credentials curl (above) and checking the `scope` field in the response.

### Gotcha — logging in with --client-id
If Shopify CLI ever asks you to log in and then shows a list of apps from the wrong org (e.g. GSD Dashboard, GSD WB Order Automation from GSD Works), you've been logged into the wrong Shopify account. Either:
- Run `shopify auth logout`, then re-auth and pick the right account, or
- Bypass the app picker entirely by passing `--client-id=5e994c135911baa59f413b9ac8d79992` to the `shopify app init` command — it jumps straight to the right app.

---

---

## Horizon Performance — Guardrails for Building Sections

Key takeaways from research (March–April 2026) into Horizon customisation best practice. Critical because the "too much code slows the site down" concern is real — Horizon is already optimised for Core Web Vitals out of the box, so our custom sections must not undo that.

### Upgrade-safe architecture (already our rule — keep doing it)
- **Never edit Horizon's core files directly.** Changes get overwritten on the next Shopify upgrade.
- Create new files in `sections/` and `blocks/` with a `gazelle-` prefix to avoid name collisions with Horizon's own files
- Use **custom template JSON files** (e.g. `templates/product.gazelle.json`) instead of modifying `templates/product.json`
- Keep custom CSS in a separate `assets/gazelle-custom.css` rather than editing Horizon's vendor CSS
- Document variable overrides in a `docs/changes.md` so we can audit what we've touched when a Horizon update lands

### Performance discipline
- **Lazy-load everything below the fold.** Custom sections that aren't immediately visible should use `IntersectionObserver` to defer initialisation, not run JS on page load.
- **Scope CSS per block.** Assign a unique ID from the block's ID and wrap all its CSS in a `{% style %}` tag using that ID as a selector prefix. Prevents style conflicts when the same block is used multiple times, and keeps per-block CSS payload scoped rather than global.
- **Minimise JS weight.** Horizon targets high Core Web Vitals scores already; every kilobyte of custom JS we add eats into that budget. Prefer CSS-only interactions where possible (e.g. the product page's hover effects, the tab switching is fine but keep the JS lean).
- **Don't layer motion effects.** Parallax + video + scroll-lock on the same page will tank performance. Horizon already has motion-safe defaults — respect them.
- **Test on mid-range Android on 3G.** Horizon looks fast on desktop Chrome. The real test is a mid-range phone on a slow connection — that's the actual customer. Use Lighthouse in "mobile + slow 4G" mode.

### Avoid external dependencies
- **No page builders.** GemPages, PageFly, Shogun etc will fight Horizon's block architecture and add render-blocking resources.
- **No third-party UI frameworks.** Don't import Bootstrap, Tailwind-via-CDN, jQuery, Alpine etc. Horizon doesn't need them and they slow first paint.
- **Use Shopify's native pixel/customer-events framework** for analytics, not inline scripts in `theme.liquid`. This avoids render-blocking and survives theme updates.

### Liquid-side performance
- **Minimise loops over large collections.** Prefer Shopify's storefront filter API to rendering and client-side filtering.
- **Use `section.settings` for merchant-controllable variables** so they can be tweaked without touching code (also makes the section reusable).
- **Avoid `preload` abuse.** Preloading a bunch of images on the product page to show off covers is tempting but kills the LCP metric.

### What this means for translating the mockups to Liquid
- The product + collection page mockups were built with performance in mind — no libraries, all CSS custom properties, one lightweight inline script, all SVG icons inline (zero extra HTTP requests)
- For the Liquid versions we'll split the mockup's inline `<style>` into `assets/gazelle-product.css` and `assets/gazelle-collection.css`, scoped with `{% style %}` wrappers per block
- The Trajan font should be preloaded once in `theme.liquid` rather than re-declared per section, to avoid font-flash on navigation

---


## Brand Identity
- **Logo:** originally `GazelleLogo__2_.png` (actually a JPEG, no transparency). A proper transparent version was worked around for the mockups; **request proper SVG brand assets from George (Bowden Studio) for production** (current file is still a JPEG with no transparency).
- **Colours / fonts:** as in the design-language section above.
- **Trajan Pro** (headings/buttons) is commercial (Adobe); **Cinzel** is the free stand-in in use for now. Body font is **answered**: the brand site pairs Trajan with **Switzer** (free via Fontshare). See the Fonts / Typography section.

---

## Key Lessons / Principles (don't repeat these)

### Today's additions (22 June)
- **AS400 outbound file is a headerless, denormalised, double-quoted CSV** with H/D field levels — header fields repeat per line. Standard for position-based AS400 parsers; the sample file is for format validation before building the live pipe.
- **Shopify holds one email + one phone per order**, not separate billing/shipping pairs — don't model the file as if it has two of each.
- **Shopify addresses are structured, not free-text lines** — map address1/2/city/county into the AS400's 4 lines deliberately, and **validate billing on a real order** (express checkouts can return sparse/duplicate billing addresses).
- **No-code AS400 path holds** (EZ Exporter + Matrixify) because no per-publisher file splitting is required.
- **ISBN-13 must live in the variant `barcode` field** for EZ Exporter to read the EAN natively — a prerequisite before building the export.

### Added 27 June (AS400 tooling realities)
- **EZ Exporter is scheduled-batch, not per-order.** It can't fire one file per order at the moment of purchase — it runs on a timer and batches new orders since the last run. Design the AS400 side for frequent batch files keyed by PO, not single-order files.
- **Matrixify folder-watch (auto-import on SFTP drop) is a Big/Enterprise-plan feature**, not on lower tiers. Per-despatch auto-fulfilment depends on it — a plan-tier cost decision for Gazelle, not a given.
- **Full carrier tracking URL beats tracking-number-only.** Shopify only auto-links recognised carrier names; a direct URL is robust and always renders in the customer notification. Ask for the URL column on any tracking-return file.
- **Export the price actually paid, not list/compare-at.** With manual Gazelle discounts off RRP plus Kumon's separate discount code, the unit-price column must be the post-discount paid amount or the warehouse invoices wrong.
- **Company Name on an order is best taken from the SHIPPING address**, not billing — it's the despatch/label-relevant value.

### Added 16 July (carousel containment + the stale-diagnostic lesson)
- **⚠️⚠️ PULL BEFORE ANY DIAGNOSTIC THAT READS EDITOR-OWNED JSON — not just before edits.** Claude Code's carousel diagnostic confidently reported `columns: 4, max_products: 8` from the local `templates/index.json` and built its entire arithmetic on it; the editor had been **6 / 12 since 14 July** and the local file had never been pulled. **Every number in a long, well-argued, file-traced report was fiction.** It was caught by an **editor screenshot**, not by the trace. Pull-clobber has always been framed as a **write-safety** rule (don't lose work). This is its mirror: it is equally a **read-accuracy** rule (don't reason from a stale mirror). **A read-only diagnostic feels safe precisely because it changes nothing — that is exactly why nobody thinks to pull first.**
- **⚠️ A file trace is not a native-first audit.** The agent traced the cause perfectly and then **never answered "under what condition is `force-full-width` applied?"** — it jumped straight to a CSS override. Whether a native setting controls the behaviour was ruled out by a **human in the theme editor**, not by the agent. **Rule: the agent must state the native-vs-custom decision EXPLICITLY and name what it checked to rule the native path out.** "I couldn't find a setting in the files" is not the same as "there is no setting."
- **⚠️ Native full-bleed is a DESIGN CHOICE, not a bug — check for it before diagnosing a calc.** Horizon's carousel layouts hard-code **`force-full-width`** on the resource-list wrapper (`snippets/resource-list.liquid`), and core does `.section > .force-full-width { grid-column: 1 / -1 }`. **`section_width: page-width` does NOT constrain a carousel** — the class is unconditional for `layout_type: carousel` and there is **no native toggle**. Any downstream `%` in a slide-width calc then resolves against a viewport-width track and looks like a calc bug. **The calc is the symptom; the grid-column breakout is the cause.** Fix pattern: `grid-column: 2` + `--util-page-margin-offset: 0px`, scoped, specificity 0,3,0 beats core's 0,2,0, no `!important`, peek survives.
- **⚠️ Two sessions in one day breaks the "check the timestamp" rule.** 14 July produced BOTH a 960-line file (footer, ~3:15pm) and a 985-line file (header/page-width, ~5:00pm). A correct-looking date is NOT proof of currency. **Verify by CONTENT: grep the file for the newest artefact you know exists on disk** (`grep -c gazelle-layout`) — a master file that doesn't know about a snippet in your repo cannot be current. Five downloads were burned on this before the right base surfaced.
- **⭐ When a discipline keeps failing, fix the MECHANISM not the discipline.** Three stale bases in one week is not carelessness — it's a broken loop (manual re-upload, no `.md` download button in the project UI). **Move the context file INTO THE REPO** next to `CLAUDE.md`: git owns versioning, staleness becomes structurally impossible, Claude Code reads it directly, George gets it free. **The tell that the mechanism is already broken: the DERIVED `gazelle-tech-stack.md` was more accurate on Fred than the master source of truth was.** When a derived doc overtakes its source, the source's update loop has failed.
- **Verify-by-render beats a half-run DevTools check.** The formal computed-value checks were attempted in **iPad emulation at 820px** — where a 1200px constraint is meaningless, so they proved nothing. The desktop render (6 cards + sliver, was 8.5) was the real evidence. **Know what viewport your verification is actually running at**, and don't let a rigorous-looking check that measured the wrong thing stand in for a plain look at the page.
- **Put a fix where the concern lives, not where the symptom appeared.** The carousel fix went into the EXISTING `gazelle-layout.liquid` rather than a new snippet: it's a width concern, `gazelle-layout` is already the single global source of width truth and already render-hooked, and the same carousel renders in related-products on the product page. A second render hook for one override is churn. **The agent proposed a new file; overruled.**
- **Decide selector scope, don't inherit it.** `.section-resource-list` catches every product-list carousel including related-products. That consistency is wanted — but it was a decision, and it got made rather than absorbed.
- **GitHub killed HTTPS password auth** — `git push` from the CLI now fails with "Password authentication is not supported". GitHub Desktop still works (holds the credential). Switch the remote to SSH or store a PAT in the keychain, or CLI pushes keep failing. **Related trap:** when git prompts `Username for 'https://github.com':`, any commands already queued in the terminal get **eaten by the prompt** and silently don't run — check what actually executed.

### Added 14 July (footer build)
- **⚠️ Runtime `block.id` ≠ the JSON key.** Selectors built on block IDs read from group/template JSON (`.text-block--<id>`) NEVER match at runtime. Target structural preset classes instead (`.text-block.paragraph`, `.text-block.h3`, `.rte:not(.paragraph)`), state the one-block-per-preset assumption, and make heading selectors tag-agnostic (`:is(h1,h2,h3,h4,h5,h6)`) — retyping heading text can flip the rendered tag.
- **`custom-liquid` is NOT whitelisted in every section.** The footer's block list excludes it (the product template's doesn't). The workaround is the **style-only section pattern**: a section emitting only `{% style %}`, with `enabled_on` scoping + a presets entry (required to appear in the Add-section picker), added via the editor. Reusable anywhere the block whitelist blocks custom-liquid.
- **⚠️ Pull-clobber extends to Claude's own code files, not just editor-owned JSON.** A pull reverts ANY file that's newer locally than on the theme. When local is ahead: **push before any pull**, and never commit a pull-diff without reading its direction (your recent work showing in red = stale pull, discard).
- **Shopify rich-text stores Enter inconsistently** — sometimes `<br/><br/>` inside one `<p>`, sometimes a real paragraph split. If CSS depends on paragraph structure (e.g. styling a last line), force a genuine `</p><p>` split in the editor. Also: **CSS has no `::last-line`**; `::first-line` only works predictably when an explicit break pins where the line ends.
- **The footer grid caps at 4 top-level blocks** — a 5th wraps to an orphan row. Nest related blocks inside a group block to stay at 4.
- **Hand-build editor-owned config in the editor; don't deliver JSON drop-ins.** The June `footer-group.json` drop-in was silently overwritten back to the stock preset by the editor. Editor-owned files belong to the editor.
- **Claude Code can commit (shows diff, writes the message) but does not push origin** — the GitHub Desktop Push origin step is still Grant's after an agent commit.
### Added 8 July (product-page build — the pull-clobber day)
- **⚠️ PULL-CLOBBER (the big one):** custom-liquid render blocks live in `product.json` and get wiped by pulls until committed. Bit us 3× in one day. Rules: commit before EVERY pull; after adding an editor block, pull+commit IMMEDIATELY; once local is newer and pushed, DO NOT pull; when custom CSS "stops working", grep for the render block FIRST.
- **Metafield `.value` rule:** every metafield output ends `.value`; native fields (vendor/type) never do.
- **Diagnostic-first for layout/CSS:** blind guesses swing wrong; read-only Claude Code diagnostics ("exact cause + minimal fix, no edits") land one-line fixes first time. Now the standard method.
- **Horizon gotchas:** `page_width: narrow` = 1400px (site is on 1200 — override per section); media wrappers clip shadows (`overflow: hidden` ≥750px); `media_fit` is dead code when a fixed aspect ratio is set; native hero grid pins the buy box right as a fixed 400px strip (mockup's proportional `1fr:1.15fr` is the fix).
- **`--gz-gutter` 24px alignment system:** all four hero/band content edges key off it — define globally to move together.
- **Verify-by-render is legitimate:** when terminal pastes fail, the rendered page screenshot IS the verification.
- **Build against broken data deliberately when it serves you:** the un-guarded dimensions row makes Dave's bug visible, proves the build is done, and self-heals. Front-end wired to correct fields + broken source showing = evidence, not embarrassment.

### Added 2 July (front-end build with Claude Code)
- **Never edit Horizon core to customise cards.** The product card is a **private core block with a baked-in child whitelist**; override by pointing the template's card block at a `custom-liquid` block that renders a `gazelle-` snippet. Core untouched, stock faceting/sort/pagination intact.
- **`closest.product` reaches the product inside block-setting Liquid** — this is what makes the custom-liquid override work in the grid.
- **A running agent is not a working agent.** Claude Code narrated "building" three times and wrote nothing; the cause was launching it from the home dir, not the repo. Always launch from `~/Sites/gazelle-horizon`, and verify every "done" against `git status` — never the agent's own summary.
- **The agent's shell can't use the zsh aliases or complete Shopify device-auth.** Theme pull/push are Grant's job in an interactive terminal; the agent calls raw `shopify theme` commands only.
- **`product.type | capitalize` mangles multi-word types** (lowercases everything after the first letter, e.g. "Hardcover Non-Fiction" — "Hardcover non-fiction"). Check the real BooksoniX `product.type` values before trusting the format label.
- **Fonts bound to theme vars render as whatever the theme is set to** — currently Inter, because brand fonts aren't configured in settings yet. Binding is correct; the Inter preview is expected, not a bug.
- **Mockups look finished but are 0% theme code.** The June product-page mockup is a design artefact; nothing on the product page is built. Don't mistake a rendered mockup for built output.

- **Tax comes from the record's own tax field, not a product_type→tax map.** Categorisation is unreliable; the tax field is known-correct in BooksoniX and the AS400. (A product_type→tax table was built then scrapped.)
- **The 25% pricing rule must run Gazelle-side**, never inside Dave's event-driven integration, or a re-push wipes manual prices (same logic as create-only Price).
- **Image issues that cluster by publisher are structural** (mapping/host access), not timing — and Shopify silently drops unreachable image URLs, so they can be invisible in the integrator's logs.
- **Metafields must be defined as structured definitions** in Shopify or they arrive unstructured.
- **Re-upload the context file to project knowledge after every update** — repeated lag is exactly why decisions went missing.

### From the June session
- **Horizon's footer is native and block-based.** The utilities bar gives copyright + policy-list (from Shopify policy pages) + socials for free; don't build a custom footer section. The logo can't go in the utilities bar.
- **Horizon has no global custom-CSS field.** Small overrides need a `gazelle-` custom block emitting `{% style %}`, or per-block scoped style — never edit core.
- **"Native" = bind to native Shopify objects** (menus, policy pages, social settings, product fields), custom markup only where it earns its place.
- **Out-of-stock nuance matters:** show everywhere, no back orders, notify-me. Previously the file had a contradictory note that out-of-stock titles vanish from collections — they don't.
- **Reviews capture imprecision** (24 April "no reviews" vs the transcript's "keep editorial reviews at the bottom") — reinforces the discipline below.
- **Mockup asset technique:** crop banner images from the live screenshot, base64 the fonts/logo, leave covers as external Schiffer URLs; pull real Horizon source from GitHub to ground native builds.
- **Books are separate products, not variants:** different ISBNs for HB/PB, not linked in metadata — so no format/variant selector on the product page.

### Carried forward
- **Context-file discipline:** decisions captured imprecisely led to two reversals going undetected for weeks. Narrative must capture nuance, not just outcomes. Re-upload the file promptly after each generated version.
- **Don't use sample data to validate live behaviour** (the sample xlsx showed 0% tax and single images across all rows — stale test data). Same logic applies to the AS400 sample order file.
- **Dave is the right source for feed-level questions** (he reads the media array / fields directly).
- Partner org vs store org: the Dev Dashboard is gated by org-level permissions; do app work as grantsd104 inside the client org. Don't recreate client apps under GSD Works (breaks the client-credentials grant).
- Dev Dashboard apps don't issue install-time tokens (client-credentials grant instead). Scopes are TOML + CLI, not Dashboard UI. CLI auth can silently pick the wrong org (use `--client-id=` or `shopify auth logout`).
- Subject data for distributors is heterogeneous — map from consistent fields (format, imprint, publisher, language) and curate top-level categories manually.
- REST handles multiple product images fine (cover first, then additional). Shopify CSV export mangles descriptions (numeric entities; doesn't round-trip).

---

## Build Philosophy — NATIVE-FIRST (confirmed by Grant, 7 July) — applies at EVERY stage
The June mockups are a **guide, not a spec to reproduce pixel-for-pixel.** The goal is to get **as close to the mockups as possible using as much out-of-the-box Horizon as we can** — native sections, blocks, theme-editor settings and config over custom code. This is a deliberate **speed + low-risk** trade on a fixed-fee build: less custom Liquid = faster delivery, smaller error surface, easier to maintain.
- **Default to native Horizon.** Only build custom where a **confirmed requirement** genuinely can't be met with Horizon's native sections/blocks/settings. Precedent: the product card — Horizon's `_product-card` couldn't be extended without core edits, so a scoped `custom-liquid` → `gazelle-` snippet was the *minimal* override. That's the bar: custom is the exception, and always the smallest change that meets the rule.
- **When custom is unavoidable:** minimal, scoped, `gazelle-` prefixed, no core edits.
- **Close-enough beats perfect.** If native Horizon gets ~90% of a mockup detail, take the 90% rather than burning hours on custom code for the last 10% — UNLESS it's a confirmed business rule (no-save messaging, no back orders, create-only price, etc.), which always wins over the mockup.
- **Agent discipline (Claude Code):** tightly scoped, execution-only prompts. Do exactly the specified task and nothing more — no refactors, no extra features, no unrequested "improvements", no core-file edits. Prefer a native setting/block over writing code. **If the native path isn't obvious, STOP and ask** rather than inventing a custom solution. This is the guardrail against the agent over-engineering and inflating build time / risk.

---

## Approach & Working Patterns
- **Surface reasoning and flag traps before drafting.** Grant engages directly when he disagrees and expects a reasoned response, not immediate capitulation.
- **Communication style (Grant's), for emails/messages on his behalf:** short, casual, direct (50–150 words). "Hey [name]" openers, "Cheers, Grant" sign-offs. Propose specific actions/times, don't offer options or re-explain tradeoffs, don't chase decisions already made. **No em dashes** in emails/messages (fine in internal docs like this one).
- **Momentum-respecting:** propose the next specific action; don't relitigate client-level decisions.
- **Scope hygiene:** the £3k SOW bundles a lot (incl. the whole AS400 workstream). Charge cleanly for genuine out-of-scope extras (pricing automation); don't nickel-and-dime borderline theme features. Grant manages the timing of raising charges with Billy himself.
- **Preview themes for Billy:** named `dev theme DD-MM` — ask Grant for the date.
- **Context file:** living markdown; normally updated via targeted `str_replace` section edits with timestamped blocks. **Always add/update the `_Last updated:_` line; ask Grant for the current time rather than guessing.**

---

## Next Actions

### Immediate — the sign-off call
- Present the three June mockups; get all three page designs approved.
- Confirm the **reviews** reconciliation (editorial "Press & Reviews" at the bottom — keep or drop entirely).
- Note to Billy: header changed to the unified design (deliberate); the footer is richer than the v3.4 one (deliberate); category icons are a placeholder line set (he'll supply final Canva assets + homepage slider images); nav labels + Subject filter await the taxonomy.

### AS400 order integration (Fred) — live deadline (~2 weeks)
- **⚠️ TOP OPEN: dual-address regression.** Fred's 30 June revision reverted the order file to **A–N (ship-to only)**, dropping the Bill To block. Contradicts Billy's confirmed dual-address requirement. **Grant to review Fred's v2 order file first** (referenced but never received), then re-raise bill-to with Fred.
- **Fred** to confirm whether the three extra fields (shipping method, order notes, order date) survived the A–N simplification.
- **Internal:** confirm EZ Exporter exports the **discounted unit price** not list (Kumon-sensitive), and converts `GB` → `GBR` for the country column.
- **Stock file (in flight):** Fred to confirm coverage (all vs warehoused), `0`-row behaviour, negatives floored to 0, and send a sample. Our side: set Matrixify to update-present-only, never zero absent EANs.
- Grant to send a fresh sample order file once the order spec is re-settled.
- **End-to-end SFTP test:** real Shopify order → AS400, tracking back; also validate express-checkout billing addresses on the live order.
- ✅ **Resolved:** tracking v3 confirmed (5 fields, daily 18:00, import 18:30); Matrixify plan-tier (daily batch, no folder-watch upgrade); ISBN-13 → variant barcode (Dave confirmed).

### Build (front-end — IN PROGRESS)
- **Product card — DONE** (`snippets/gazelle-product-card.liquid`, committed). **Next: wire it into `collection.json`** via a `custom-liquid` block (`gazelle-pull` `collection.json` first), then render-test the grid (`gazelle`) and screenshot. Expect **Inter** fonts in preview until theme fonts are configured.
- **Resolve the product-page price conflict with Billy** (struck RRP vs the no-save rule) BEFORE building the product-page buy box.
- **Configure theme fonts** (Fraunces body / Figtree subheading) in theme settings so previews stop rendering Inter — Billy-adjacent, still provisional (real target Blair/ATF).
- ~~**Footer**~~ ✅ **DONE (14 Jul)** — built + styled to mockup (menus, policies, charcoal scheme, `gazelle-footer-styles`). Go-live cosmetics remain: store name in copyright, real social URLs, policy wording. **Header is the remaining global piece:** restyle the native header (logo swap, brand tokens, nav in admin → Navigation, small CSS nudge on utility icons) — config + tokens, not a rebuild.
- **Product page** Liquid section (single `gazelle-product` section; CSS scoped; custom template JSON): wire the 5 confirmed metafields + native fields; compare-at/RRP logic; remove stars/format-selector/save; clickable publisher/imprint; Classification (Thema/BIC) box; Depth + Illustrations; Press & Reviews; traffic-light stock + no-backorder/notify; New-Release flag.
- **Collection page** Liquid + filter system (Format/Subject/Price/Imprint); Subject filter pending taxonomy.
- Integrate design tokens with Horizon CSS variables; preload Trajan once in `theme.liquid`.
- Cross-browser + mobile + Lighthouse + Theme Check.

### Data / integration (chase Dave — status check needed)
**Resolved:** core sync live; tax true/false mechanism (record tax field); description main→long fallback; compare-at clarified (manual, Gazelle-side).
**Outstanding ON Dave:**
- **⚠️ Archived-titles-showing-as-Active (Billy flagged ~6 July):** enforce Approved-only on new pushes; archive (not delete) Shopify products when a title goes Archived in BooksoniX; retroactively sweep the already-seeded non-Approved titles. (Top new Dave item.)
- Product-type subset: implement the reduced/combined format mapping once Billy finalises the combine list.
- PUBCODE metafield: surface PUBCODE as a Shopify metafield (needed for the pricing-automation exclusions).
- **Source-data bugs found on the 7 July metafield verification** (full detail in the "Metafield definitions — CREATED & VERIFIED" section): 🔴 fix `width_mm`/`height_mm` landing as literal `%sh_…%` placeholders; 🟠 `main_subjects` `&`/`and` label duplication (cosmetic); 🟡 confirm whether BISAC is genuinely blank or a mapping gap (spot-check a few titles).
- **publication_date format:** currently free text (`6 August 2024`); needs ISO `YYYY-MM-DD` if we want a Shopify Date type to drive the New-Release rule (else parse in Liquid).
- Publisher-closedown behaviour in Shopify (how a closed publisher ports through).
- Error handling: how a failed push is reported.
- Token-refresh automation: confirm it's live. Orphan BSX apps: confirm they're stubs to delete.
- Rotate the Client Secret once stable. GraphQL migration is Dave's roadmap (no action our end).
**Our side:**
- Define metafields as structured definitions in Shopify (the unstructured issue).
- prices-include-tax + test order to verify VAT on a taxable line.
- Verify Hackett covers in admin before engaging Dave.
- **Spot-check** (both now confirmed by Dave for at least one title): inside spreads syncing to media positions, and ISBN-13 in the variant barcode field with inventory-tracked variants — verify across **different publishers and older backlist**.
**✅ Resolved this window:** inside spreads syncing (Dave); ISBN-13 → variant barcode (Dave); daily stock route confirmed (AS400 → daily **`GazelleAvailability`** file → Matrixify, not a BooksoniX API pull — **file arrived + confirmed clean 9 July, 01:29 daily**; see AS400 section). ⚠️ Note the filename: it is `GazelleAvailability_YYYYMMDD.csv`, NOT `GazelleStock` as originally specced.


### Other open items
- Subject taxonomy mapping (Billy) — the key unblocker.
- **Pricing automation (25% rule):** out of scope — send Billy a separate quote before building; confirm rounding + final exclusion list; PUBCODE metafield dependency on Dave.
- **Product-type subset:** get Billy's finished combine list, then hand to Dave.
- Remaining metafields sign-off + mapping template for Dave.
- Fonts: **decided** — Cinzel (headings/buttons, free) + Switzer (body, free via Fontshare) for now; real Trajan only if Billy wants it (needs a webfont licence). Remaining: raise the less-all-caps-vs-brand-site conflict with Billy.
- Proper SVG brand assets from George (Bowden Studio).
- Zero-rated taxable-flag question for VAT-return accuracy; confirm non-book tax behaviour on live data.
