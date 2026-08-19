# Build manual — Gazelle Books Shopify Theme

_Last updated: 11 August 2026. Split out of CLAUDE.md on 30 July 2026 when the STATUS/DONE context system was installed; auto-loaded by CLAUDE.md via `@docs/build-manual.md`._

This file defines how to work in this repo. Read it before touching any file.

## What this is

A brand-new Shopify storefront for **Gazelle Book Services**, a book distributor carrying ~55k titles across many independent publishers. Audience is mixed trade (booksellers, libraries) and retail. Built on **Shopify Horizon v3.4.0**, forked as `gsdworks/gazelle-horizon`. Store: `gazelle-books-2026.myshopify.com`, going live under `shop.gazellebookservices.co.uk`.

Product data is pushed into Shopify from **BooksoniX** via an event-driven REST API. You are not responsible for that integration; you build the front end that renders the data it produces.

## Build philosophy — NATIVE-FIRST (governs every decision)

Get as close to the June mockups as possible using **as much out-of-the-box Horizon as we can**. This is a deliberate speed + low-risk trade on a fixed-fee build: less custom Liquid means faster delivery, a smaller error surface, and easier maintenance. Apply it at every stage.

**Priority order for any piece of UI:**
1. Native Horizon section / block / setting
2. Theme-editor configuration
3. A small, scoped `gazelle-` snippet
4. (Last resort) custom Liquid

Rules that follow from this:
- **Audit the library BEFORE building custom.** Horizon ships a large `blocks/` + `snippets/` library. If a native block already covers the need (accordion, icon rows, product-inventory, complementary products, share, badges), **USE IT**. Building a custom version of something that exists out-of-the-box is the exact waste native-first prevents. **The audit is required, not optional.**
- **Default to native Horizon.** Only build custom where a **confirmed requirement** genuinely can't be met natively. Precedent: the product card — Horizon's `_product-card` couldn't be extended without core edits, so a scoped `custom-liquid` → `gazelle-` snippet was the *minimal* override. That's the bar.
- **Any custom must be minimal, scoped, `gazelle-` prefixed, and touch no core files.** Smallest change that meets the rule.
- **Close-enough beats perfect.** If native Horizon gets ~90% of a mockup detail, take the 90% rather than burning hours on custom code for the last 10% — **unless** it's a confirmed business rule (no-save messaging, no back orders, create-only price), which always wins over the mockup.
- **This is forward-looking.** It does not mean re-doing already-built work to be "more native." Leave built sections alone (see "Already built").

## Credentials — which app the scripts run under

- **All `scripts/` run under the "GSD Gazelle Scripts" custom app** (client ID `9c1cdb65353e42b36432a5d185e24199` — an identifier, not a secret; 26 scopes, installed on `gazelle-books-2026`). Client-credentials grant, short-lived token per run, no static `shpat_`.
- **⚠️ NEVER run our scripts under the "BooksoniX Integration" app.** That one is **Dave's**, and it **lacks `write_publications`** — it cannot publish a collection to the Online Store channel, so a collection run under it would create unpublished collections. The 11 Aug collection run must therefore have used a different app than its docstring named.
- Env vars are standardised across every script: **`SHOPIFY_STORE`** (full `*.myshopify.com` domain), **`GAZELLE_CLIENT_ID`**, **`GAZELLE_CLIENT_SECRET`**.
- **⚠️ 19 Aug: the BooksoniX Integration client id AND secret were found exported in the environment Claude Code inherits.** `verify_l2.py` hard-refuses to run if it sees that client id. Check what a terminal is carrying before running anything: the app a script authenticates as is decided by whatever happens to be exported, not by intent.

## Billy's task sheet — `docs/BILLY-TASKS.csv`

Billy's live task sheet is published as CSV and **re-fetched by `./build-context.sh` on every run**, then embedded verbatim in `PROJECT-CONTEXT.md`. It is a generated file: never hand-edit `docs/BILLY-TASKS.csv`, the next context build overwrites it.

- **Rows are matched by the `Page` column.** That column is the key everything else keys off — **do NOT reorder rows**, and do not rename a `Page` value, or the status columns stop lining up with the item they describe.
- **Columns D and E are status columns** — **D = Billy**, **E = Grant Notes**. Their headers sit on the sheet's *second* row, not the first, so a naive CSV read shows columns D/E as unnamed.
- The fetch is **deliberately non-fatal**: `build-context.sh` runs under `set -e`, and a network failure must not stop `PROJECT-CONTEXT.md` regenerating. On failure the previously fetched copy is kept and a warning printed — so **check for that warning** before trusting the sheet in the context file to be current.

## Working principles — asks of third parties

**Minimise asks of Dave Hyman.** He was paid roughly **£500** for the BooksoniX integration, it has dragged on for months, and he is frustrated. Every additional question spends goodwill we may need for something genuinely blocking.

- **Before putting anything to Dave, check whether it can be done Shopify-side by script.** Most of what looks like a source-data ask (handle renames, `thema_top` backfill, archiving, exclusions) is ours to do with the Admin API and the "GSD Scripts" app.
- **Only put things to him that genuinely cannot be done our side** — cause-of-defect questions, things that must change in BooksoniX itself.
- **Keep those asks minimal and non-cumulative.** Do not append a new question to a still-unanswered list; a growing tail of asks reads as an escalating demand and lowers the chance any of them gets answered.
- Prefer parking a nice-to-have over asking. `pubcode` exclusion at source was parked on exactly this basis — Grant's sweep covers it.

## Agent execution rules (Claude Code)

- Do **exactly** the task asked. Nothing more. No refactors, no extra features, no unrequested "improvements", no tidying of unrelated files.
- Prefer a native setting or block over writing code, every time.
- **If the native path isn't obvious, STOP and ask** — do not invent a custom solution.
- Never edit Horizon core files. If a change seems to need one, stop and flag it.
- **git commit + push is done by `/update-context`, with Grant's yes at the diff-stat.** Show `git diff --stat`, wait for explicit approval — "ok", "yes", "do it", "go" — then commit and push. Ambiguous or adjacent messages are not approval; if unsure, ask. **`shopify theme pull` / `push` remain Grant-only interactive steps** (device auth the agent cannot complete).
- Trust the filesystem, not your own summary. After any "done", the change isn't real until `git status` / `ls -la` confirms it.

### Ruling out the native path — say what you checked

When proposing ANY custom code, **state explicitly what you checked to rule out the native path, and name it.** A file trace is not a native-first audit.

- ❌ "I couldn't find a setting for this in the files."
- ✅ "`section_width` controls X but not Y; `force-full-width` is applied unconditionally at `resource-list.liquid:98` with no setting in its control path; therefore no native toggle exists."

If a class or behaviour is applied conditionally, **name the condition**. If you cannot determine whether a setting controls it, **say so and ask** — do not let "I didn't find one" silently become "there isn't one".

_Why this rule exists: on 16 July the carousel diagnostic traced the cause perfectly and then jumped straight to a CSS override without ever asking whether a section setting governed the behaviour. Grant ruled it out in the theme editor. Without that human check the override would have been a native-first violation dressed up as a well-traced fix._

### Reading editor-owned state — pull first, ALWAYS

**Before any task that reads editor-owned JSON — including read-only diagnostics — confirm a pull has happened this session.**

Editor-owned files: `templates/*.json`, `config/settings_data.json`, `sections/*-group.json`.

These mirror Shopify, not the repo. Editor changes do not reach local until someone pulls. **A file that hasn't been pulled is a stale mirror, and reasoning from it produces confident, well-argued, entirely fictional output.**

- If you do not know whether a pull has happened, **say so before reporting** rather than presenting the values as current.
- When a diagnostic depends on a setting value, **quote the value AND flag that it is only as current as the last pull.**
- Never do arithmetic on an unpulled setting value without flagging it.

_Why this rule exists: on 16 July a read-only carousel diagnostic reported `columns: 4, max_products: 8` from a stale `templates/index.json` and built its entire analysis on those numbers. The theme editor had said **6 / 12 since 14 July**. Every figure in a long, well-argued, file-traced report was fiction, and nothing about its quality signalled the problem — an editor screenshot caught it, not the trace._

**The general principle: pull-clobber is not only a write-safety rule (don't lose work). It is equally a read-accuracy rule (don't reason from a stale mirror). A read-only diagnostic FEELS safe because it changes nothing — which is exactly why nobody thinks to pull first.**

### Diagnostic prompts — ask what causes X, not "confirm Y causes X"

A diagnostic prompt that embeds a hypothesis will bias the diagnosis. If a prompt hands you a suspected cause, **treat it as a hypothesis to test, not a premise to confirm**, and say so if the evidence points elsewhere.

_Why: the 16 July carousel prompt asserted "the calc resolves `100%` against the wrong parent". The agent partially followed that framing. The real cause (`force-full-width`) surfaced mid-trace as an aside and its significance — this is native design, not a bug — was nearly buried under the calc-shaped narrative it had been pointed at._

## Hard rules (do not break these)

- **Never edit Horizon core files.** All custom work is new files, so upstream `Shopify/horizon` can be synced without merge conflicts. If a change seems to need a core edit, stop and flag it.
  - **Approved core-file exceptions** (deliberate — keep current, re-add after any Horizon update):
    - `layout/theme.liquid` — font preload + `{% render 'gazelle-fonts' %}` before `</head>` (self-hosts Switzer; added 7 July).
    - `layout/theme.liquid` — `{% render 'gazelle-layout' %}` adjacent to the fonts hook (global page width; added 14 July).

- **⚠️ PULL-CLOBBER — the most expensive recurring failure on this project** (bit us 3× on 8 July, again on 14 July, again on 16 July).
  `shopify theme pull` mirrors Shopify → local. It will **overwrite ANY local file newer than the theme copy** — not just editor-owned JSON, but Claude's own committed section files.
  1. **Commit before EVERY pull.** Committed work is recoverable (`git restore`, `git checkout <sha> -- file`). Uncommitted work is gone.
  2. **After adding ANY block in the theme editor: pull + commit IMMEDIATELY.** A custom-liquid render block only becomes durable once it's in git.
  3. **When local is AHEAD of the theme: PUSH before any pull.** Never pull "to be safe" — that is how a stale Shopify copy reverts newer local work.
  4. **Never commit a pull-diff without reading its direction.** Your own recent work showing in red = the pull is stale. Discard it.
  5. **When custom CSS "stops working", grep for the render block FIRST** (`grep -c "gazelle-cover-styles" templates/product.json`) before touching any CSS. The CSS usually isn't wrong — it isn't running.
  6. **Pull before diagnostics too, not just before edits** (see Agent execution rules).

- **Prefix all custom files `gazelle-`.** Sections: `sections/gazelle-*.liquid`. Blocks: `blocks/gazelle-*.liquid`. Snippets: `snippets/gazelle-*.liquid`. Custom templates: `templates/*.gazelle.json`.
- **Scope all custom CSS with `{% style %}`** inside the section/snippet that uses it. No separate stylesheet edits to core assets.
  - **⚠️ CORRECTION (18 Aug 2026):** this rule previously justified itself with "Horizon has no global custom-CSS field". **That was wrong.** Shopify has a **platform-level Custom CSS field**, stored at `config/settings_data.json` → `platform_customizations.custom_css` and injected as an inline `<style>` at the **end of `<body>`** — invisible to anyone reading the theme's files. The scoping rule stands; its stated reason did not.
  - **NEVER use the platform Custom CSS field.** On 18 Aug three `!important` rules found living there (`max-width: 220px` on every `.product-media-container`, a forced `text-align: center` on every left-aligned text block) had been silently overriding `gazelle-cover-styles` and every editor alignment setting, and cost a full session to find. **If layout misbehaves inexplicably, check that field FIRST.** Clearing it in the editor did not take — push it with `shopify theme push --only config/settings_data.json`.
- **No page builders, no third-party UI frameworks, no CSS libraries.** Vanilla Liquid + CSS + minimal JS.
- **Lazy-load below-the-fold sections. Minimise JS.** Test on a mid-range Android on a slow connection, not just desktop.
- **Bind to native Shopify objects wherever one exists** (menus, policy pages, social settings, product fields) rather than hardcoding.
- **Do not touch password / store-visibility settings.** The store is behind a password and the primary domain already points at it. Disabling the password would expose a dev environment publicly.
- **When a spec is ambiguous or a metafield key isn't confirmed below, stop and ask.** Don't guess a key name or invent a decision.

## Design source of truth

The three high-fidelity mockups in `_design/` (`gazelle-homepage-mockup-June.html`, `gazelle-collection-page-mockup-June.html`, `gazelle-product-page-mockup-June.html`) are the approved design and your visual reference. They are standalone HTML for sign-off, **not** part of the theme.

Treat them as a **guide, not a pixel-spec** (see Build philosophy). Hit the colour tokens and max width below **exactly** — they're cheap and high-impact. For layout and spacing, get **close** using native Horizon sections and settings rather than writing custom CSS to chase the last few pixels.

### Colour tokens
- Accent (brand red): `#a11f21`
- Accent hover: `#7c1516`
- Secondary red: `#ae2628`
- Ink / dark surfaces (charcoal): `#1a1917`
- Paper (page bg): `#faf7f2`
- Surface (cards): `#ffffff`
- Muted text: `#6b6760`
- Border: `#e8e2d8`

Built as theme colour schemes: **Scheme 1 "Paper"** site-wide, **Scheme 5 "Charcoal"** footer. Set in the theme editor — do not hand-edit `settings_data.json`.

### Typography — CONFIRMED 7 July, do not revert

The brand (Webflow) site runs a two-font system, confirmed via DevTools:
- **Headings + buttons: Trajan Pro** → we use **Cinzel** (Google Fonts) as the free stand-in. Real Trajan needs a webfont licence; only pursue if Billy asks.
- **Body: Switzer** (Fontshare, free for commercial use) — **self-hosted** via `snippets/gazelle-fonts.liquid`.
- **Blair ITC is logo-only.** Not used anywhere else.

**⚠️ Corrections to earlier records — these were wrong and must not creep back:**
- **Fraunces and Figtree are DROPPED.** They were design guesses in the June mockups, not Billy's brand fonts.
- **"Blair / ATF" is NOT the target.** That was an imprecise earlier note.
- **All-caps: keep them.** Billy asked for "less all-caps" but his own brand site sets every heading and button in Trajan, which is caps-only. Both cannot be true. **Grant's call (7 July): follow the brand, keep caps, revisit later.** The caps come from the *font* (Cinzel/Trajan have no lowercase glyphs), not a CSS transform — so keeping them is zero-effort, and reducing them later means swapping the heading font (a token change), not toggling a case setting.

Keep the stack tokenised: bind to `--font-body--family` / `--font-heading--family`, never hardcode a family.

### Layout
- **Page width max 1200px, centred.** Enforced globally by `snippets/gazelle-layout.liquid` — see the platform gotchas below. **Do not add per-section width overrides;** that snippet is the single source of truth.

## Metafield contract

All book metafields live in the **`custom`** namespace. Bind to the key path (e.g. `product.metafields.custom.author.value`).

**⚠️ ALL 23 DEFINITIONS ARE CREATED AND LIVE** (5 pre-existing + 18 bulk-created via Admin API, 7 July; `created=18 failed=0`). **The old "pending — do not wire" list is obsolete. Wire any of these freely.**

`isbn`, `subtitle`, `author`, `publisher`, `language`, `publication_date`, `series`, `series_number`, `pages`, `height_mm`, `width_mm`, `depth_mm`, `illustrations`, `author_bio`, `thema_subjects`, `bic_subjects`, `bisac_subjects`, `main_subjects`, `keywords`, `audience`, `prize_achievements`, `reviews`, `tags_global`

**⚠️ `.value` RULE — the one that bites:** every metafield output MUST end `.value` (`custom.author_bio.value`). Native fields (`product.vendor`, `product.type`) must **NOT**. The editor's inline-Liquid validates hard; snippets fail silently.

**ISBN-13 is not a metafield.** It lives in the native **variant barcode** field (`product.selected_or_first_available_variant.barcode`), confirmed landing there with variants inventory-tracked. Do not create or bind an `isbn13` metafield.

**Known source-data bugs (Dave's side — do NOT work around them in Liquid):**
- `width_mm` / `height_mm` land as literal `%sh_width_mm%` placeholder tokens. **The dimensions row is deliberately un-guarded so this shows live** — it's evidence for Dave and proof the front end works. Leave it.
- `main_subjects` duplicates `&`/`and` label variants.
- **⚠️ 11 Aug: the remaining source-data defects are ONE stale cohort of 1,057 products, not four separate bugs.** Overlapping membership: 934 blank Product Type, 548 Thema-as-names, 529 placeholder dimensions, 342 `__line:` series tokens. A single re-push by Dave clears all four. Re-push list emailed 11 Aug. Everything below is that cohort unless stated.
- `series` arrives as an internal token (`__line:the_frean_chronicles`), not the series name, on **342 products** (was 3,786 on 3 Aug — the re-pushed majority has healed). Do not parse the token in Liquid — the rest self-heals when Dave re-pushes the cohort.
- `thema_subjects` / `bic_subjects` — codes are the norm now; **548 records still in name format**, all inside the stale cohort. Front end was already wired correctly; nothing to change.
- **`product.type` HAS LANDED — 98.1% COVERAGE as of 11 Aug, values verified against Billy's 28 May combine list.** This reverses the 3 Aug entry that said it was empty on 98.1% (the numbers are a coincidence — that was 98.1% *blank*, this is 98.1% *populated*). **The Format filter is live.** Residual: 934 blank (stale cohort), plus value decisions pending with Billy — `Mixed-media product` ×126 (absent from his combine list), `Undefined` ×12, `Pamphlet` ×1 (should be Paperback).

**`custom.pubcode` EXISTS as of 19 Aug — but is EMPTY.** `single_line_text_field`, **created by us** on 19 Aug via `scripts/create_gazelle_metafields.py` (recorded in DONE.md — if anyone later finds it in admin and wonders where it came from, that is the answer), with `smartCollectionCondition` enabled and `adminFilterable` switched on in admin. **Dave has not mapped it yet, so it is blank on every product.** Value spec given to him: **bare code only** (`CE1`), not the `CE1 - LINDEN PUBLISHING INC` form, key lowercase `custom.pubcode`. **Until his first push populates it, the `tags_global` substring parse (`PUBCODE: CE1 - LINDEN PUBLISHING INC`) remains the working source** — keep it. When the first populated push lands, **spot-check the actual value format before wiring the discount rule or any exclusion collection to it**; a value arriving in the long form silently breaks an equals-based smart collection.

**`custom.thema_top` — a 24th field, OURS not Dave's (created 11 Aug).** `list.single_line_text_field` with the `smartCollectionCondition` capability, holding the top-level letters derived from the Thema codes. It exists because **smart-collection metafield conditions support ONLY "is equal to"** — prefix matching is impossible, so the value you want to match has to be derived and stored. (Equals against a list field matches if any entry matches.) Backfilled onto 47,247 products by `scripts/populate_thema_top.py`. **It is NOT self-maintaining:** products arriving from Dave have no `thema_top` and silently miss the subject collections until the script is re-run. The fix is Dave pushing the field natively — until then, re-run the script after any significant load. Reuse this derive-then-equals pattern for any future taxonomy collection.

**Data expectations:** many fields render empty until BooksoniX populates them. That is expected and fine. Empty rows hide.

### Data pipeline — confirmed facts (19 Aug, from Dave)

- **Dave does not set `handle`.** Shopify derives it from the title on create. Two consequences: **a bulk handle rename is safe from clobber** (an update push will not overwrite it), and **the `-1` duplicate handles are a create-collision symptom**, not a handle-generation choice.
- **Only Approved BooksoniX records sync.** Anything not Approved his side never reaches Shopify.
- **`custom.pubcode` exists** (see the metafield contract above) — created our side, empty until Dave maps it.
- **`scripts/create_gazelle_metafields.py` now lives in `scripts/` and is committed.** It was previously loose in Downloads. Re-runnable and idempotent (existing definitions report `TAKEN` and are skipped); `--dry-run` prints the plan with no API calls.
- **⚠️ EXPORT INTEGRITY RULE — check before trusting ANY export.** The **unique Handle count must equal the All Books count in admin.** The 18 Aug export held **32,708 of 50,523** products and looked perfectly healthy; it was discarded. The 19 Aug export verified at 50,523 = 50,523. `populate_thema_top.py` prints both figures at the top of every run.
- **⚠️ `metafieldsSet` accepts at most 25 metafields per call.** Two metafields per product therefore means **12 products per batch**, not 25. A full backfill is ~4,200 batches and **~55 minutes** (50,202 products written, 0 errors, 3,202s on 19 Aug). Raising the batch size silently truncates the write.

## Native field map (what's native vs metafield)

| Displayed as | Source |
|---|---|
| Title | native `product.title` |
| Description | native `product.description` (body HTML) |
| Format (Paperback/Hardback) | native `product.type` — **populated on 98.1% of products as of 11 Aug; the Format filter is live** |
| Imprint | native `product.vendor` |
| Price (UK RRP) | native price |
| Cover image | native, first image |
| Interior spreads / sample content | native product media, after the cover |
| ISBN-13 (EAN) | native `variant.barcode` |

## Product page requirements (Billy's decisions)

**Do NOT include:**
- Star ratings or customer review counts in the buy box. Gazelle's audience is trade; individual star reviews add nothing.
- A format/edition selector (HB/PB/eBook). Every book is a separate product with its own ISBN; editions are not linked. Gazelle do not sell ebooks — no ebook option anywhere.
- Any "Save X%" or discount-percentage messaging on price.

**Do include:**
- **Clickable Publisher and Imprint** — each links to a filtered collection of those titles. (Author already clickable.)
- **Classification box** in the side rail, under Subjects. **⚠️ Thema and BIC ONLY — Billy confirmed 8 July: "we don't need to show BISAC, BIC & THEMA are sufficient."** Keep the BISAC field as data; do not display it. Display only, not navigation.
- **Product Details:** dimensions as H × W × D, plus Illustrations.
- **New Release flag:** applied automatically when `publication_date` falls in the current month, drops off the following month. Metafield-driven, not a manual tag. **Billy WANTS this — deferred, do not drop.** Currently blocked: `publication_date` is stored as text (`6 August 2024`), not a Date type, so it can't drive the rule until Dave sends ISO or we parse in Liquid.

### Stock & buy box (confirmed on Billy's call)
- **No back orders, ever.** If a title is out of stock, it cannot be ordered.
- **Out-of-stock titles stay visible** — product page *and* collection pages. They must not disappear (publishers would flood Gazelle with "why isn't my title showing" emails; the page also stays as a link for anyone arriving via mailer/Google).
- Out of stock = **Add to basket disabled** + optional **"notify me when back in stock"** capture.
- **Traffic-light stock indicator:** in stock (green) / low stock (amber) / out of stock (red).

### Price display (confirmed mechanic)
- Show the native price. A compare-at strikethrough appears **only when Gazelle have actively discounted** (compare-at = RRP, price = the lower Gazelle price).
- **Compare-at MUST be empty when selling at RRP**, or Shopify renders a broken strikethrough.
- Never show "Save X%" or any discount-percentage messaging.

**Pending — do not build yet, confirm with Grant first:**
- **Struck-through RRP shown alongside the price by default** (the June mockup's "was £X, now £Y"). Conflicts with the no-discount-messaging rule and overlaps the out-of-scope 25% pricing automation. **Undecided — needs Billy.** Build Gazelle-price-only as the default.
- **"Press & Reviews"** block at the bottom (editorial/trade reviews from metadata, not customer stars). Unresolved conflict in the record: an earlier decision was "no reviews system at all." Treat as undecided until Grant confirms.
- **Subject chip links** → filtered collections. Gated on the taxonomy decision.

## Collection page requirements

- Use Horizon's **stock collection section** for faceting, sort, and pagination. Drop the custom card in via the grid-override pattern; do not hand-roll commerce plumbing.
- **Filters are configured in the Search & Discovery APP** (admin), not the theme: **Format** ← product type, **Imprint** ← vendor, **Price**. Availability removed. App-side config needs no pull or commit. **Format is live as of 11 Aug** (`product.type` populated on 98.1%). Note the Imprint filter will show **three separate Nova Science entries** — the publisher name has 3 spelling variants across ~20k products, a source-normalisation issue, not a filter fault.
- **S&D "grouped values" can combine formats natively** — may remove that job from Dave entirely. Pending Billy's finalised combine list.
- The **Subject filter** now has real data behind it via `custom.thema_top` (see the metafield contract). Labels are pending Billy's sign-off — do not rename collections ahead of that call.
- **Tags are reserved for editorial overlay** (seasonal, staff picks, prize winners), never core taxonomy. The integration applies no tags automatically.
- **⚠️ Collections are TWO separate problems — don't bundle them.** (1) **Subject taxonomy** — **BUILT 11 Aug, extended to two tiers 19 Aug**: **150 collections live** = All Books + Home page + 4 merch smart collections on Product Type + **20 top-level** subject collections on `custom.thema_top` + **124 level-2** sub-collections on `custom.thema_l2`, all created by `scripts/create_gazelle_collections.py`. **It is 20 top-level, not 18** — the earlier "18" was wrong wherever it appeared. Remaining is Billy's sign-off on labels and nav picks. Note **Thema has no `B` top level** — biography is `DN*` under `D`, and the L2 tier now covers it as `literature-biography`, so no new letter is needed. (2) **Homepage curation** (Focus/Highlights) keys off PUBCODE — still blocked on Dave populating `custom.pubcode`. Different owners, different blockers; solving one does not advance the other.

### The level-2 sub-collection tier (built 19 Aug)

- **124 sub-collections on `custom.thema_l2`**, one per Thema 2-character group holding **≥24 products** (`keep == True` in the counts CSV). 140 groups exist; 16 fell below the threshold.
- **`custom.thema_l2`** — `list.single_line_text_field` with `smartCollectionCondition`, the first two characters of each valid Thema code. Same derive-then-equals pattern as `thema_top`, for the same reason: metafield rules support **only "is equal to"**.
- **`custom.parent_handle`** — a COLLECTION-level `single_line_text_field` holding the parent's handle, so a template can find a parent's children without a hardcoded map.
- **Handles are hand-curated in `HANDLE_OVERRIDES`, never derived from the EDItEUR heading.** Deriving produced 85-character URLs like `childrens-young-adult-children-s-picture-books-activity-books-early-learning-concepts`. Rule: `<parent-short>-<child-slug>`, under 40 chars, URL-safe, unique. **`PARENT_SHORT` is a fixed map, deliberately not derived from the parent handle**, so a parent can be renamed without moving 124 child URLs.
- **⚠️ Child slugs and parent handles come from the same vocabulary, so a child can land exactly on its parent.** Five did on the first run (`medicine-nursing`, `philosophy-religion`, `history-archaeology`, `language-linguistics`, `reference-interdisciplinary`) and skipped as handle-exists. `validate_handles()` now rejects any handle equal to a top-level or merch handle, before any write.
- **Titles start from EDItEUR Thema 1.6 English headings**, overridden in `TITLE_OVERRIDES` where the heading reads as a codelist entry. The codelist is **vendored** at `scripts/thema_labels_en_v1.6.json` so runs are reproducible offline. **Matching is on HANDLE, never title** — Billy can retitle in admin and a re-run will not create duplicates.
- **`scripts/verify_l2.py`** runs the five post-build checks, read-only.

### Maintenance routine — this tier is NOT self-maintaining

1. After **any** Dave load, re-run `python3 scripts/populate_thema_top.py <export folder> --full`. New products arrive with no `thema_top` / `thema_l2` and silently miss every subject collection until it runs.
2. Each run writes `scripts/out/thema_l2_counts.csv`. **Read it.** If a group crosses 24, create that collection by hand; if one drops below, decide by hand.
3. **24 is a create-time rule, not a delete trigger.** An existing collection falling under 24 is not automatically removed — a live URL should not disappear because a count drifted.
4. **Standing ask to Dave, once Billy signs off:** push `thema_top` and `thema_l2` natively, derived the same way, and the backfill retires.

## The grid-override pattern (CRITICAL — reuse for every commerce page)

Horizon's product card (`blocks/_product-card.liquid`) and the collection section (`sections/main-collection.liquid`) are CORE — never edit them. The card `type` and its child-block whitelist are baked in.

- To put a custom card in the stock grid: in the *template* (`collection.json` etc.), swap the `_product-card` block's child blocks for a single `custom-liquid` block (which IS on Horizon's whitelist) containing `{% render 'gazelle-product-card', product: closest.product %}`.
- `closest.product` resolves inside block-setting Liquid. This keeps native faceting, sort, and pagination intact.
- **VERIFY it renders populated data (not blank).** If `closest.product` doesn't resolve, stop and flag it rather than restructuring the section.
- **⚠️ `custom-liquid` is NOT whitelisted in every section** — the footer's block list excludes it. Check the schema first; where it's blocked, use the style-only-section pattern below.

## Horizon platform gotchas (v3.4 — verified on this build, bank these)

**Layout / width**
- **`--page-width` is declared on `<body>` via the `.page-width-*` class, NOT on `:root`.** A `:root` override is **completely inert** — an element-level declaration beats an inherited one. Target `body.page-width-narrow`.
- **Override `--page-content-width`, not `--page-width`.** Horizon's native `calc()` derives page-width from content-width; override the derived value and the two disagree, and edge-aligned components drift.
- **`page_width: narrow` = 90rem = 1440px**, not the ~1400 previously assumed. The whole Gazelle build is 1200.
- **`snippets/gazelle-layout.liquid` is THE single global source of page width.** Width fixes belong there, not in new per-section snippets.
- **`.blog-posts` redeclares width on its own element** (`sections/main-blog.liquid`) so the blog listing ignores the global fix. Core file — leave it unless blogs are kept and 1200 is wanted, then use the style-only-section pattern.

**Carousels / resource lists**
- **⚠️ Carousel layouts opt OUT of page width, unconditionally, BY DESIGN.** `snippets/resource-list.liquid` hard-codes **`force-full-width`** on the carousel wrapper, and core `base.css:510` does `.section > .force-full-width { grid-column: 1 / -1 }` — spanning all three grid columns (margin | centre | margin), i.e. the viewport. **`section_width: page-width` does NOT constrain a carousel. There is no native toggle.**
- Any `%` in a downstream slide-width calc then resolves against a viewport-width track and **looks exactly like a calc bug**. It isn't. **The calc is the symptom; the grid-column breakout is the cause.** Check for `force-full-width` before diagnosing a calc.
- **The containment fix** (already in `gazelle-layout.liquid`, 16 July): `grid-column: 2` + `--util-page-margin-offset: 0px`, scoped to `.section-resource-list`. Specificity 0,3,0 beats core's 0,2,0 — no `!important`. Peek survives (the `--peek-next-slide-size` reservation lives inside the slide-width calc).
- **The img `sizes` attribute is hardcoded viewport-relative** (`100/columns` vw). With a constrained track it over-fetches one srcset step. Core-generated, negligible, not worth chasing.

**Blocks / sections**
- **⚠️ Runtime `block.id` ≠ the JSON key.** Selectors built on IDs read from group/template JSON (`.text-block--<id>`) **NEVER match at runtime.** Target structural preset classes instead (`.text-block.paragraph`, `.text-block.h3`, `.rte:not(.paragraph)`) and state the one-block-per-preset assumption.
- **Heading selectors must be tag-agnostic** — `:is(h1,h2,h3,h4,h5,h6)`. Retyping heading text in the editor can flip the rendered tag (h2→h3) and kill a tag-specific selector.
- **The style-only-section pattern** (use wherever `custom-liquid` is blocked): a section emitting only `{% style %}`, no markup, `enabled_on: {"groups": [...]}` **plus a presets entry** (required or it never appears in Add section), added via the editor. See `sections/gazelle-footer-styles.liquid`.
- **The footer grid caps at 4 top-level blocks.** A 5th wraps to an orphan row. Nest related blocks inside a group.
- **Hand-build editor-owned config IN the editor. Never deliver JSON drop-ins** — the June `footer-group.json` was silently overwritten back to the stock preset. Editor-owned files belong to the editor.

**Product / media**
- **Media wrappers carry `overflow: hidden` ≥750px** — clips box-shadows on cover images. Fix with scoped `overflow: visible`, `:only-child`-gated.
- **`media_fit` is dead code when a fixed aspect ratio is set** — the native "contain" toggle silently does nothing.
- **Native hero grid pins the buy box right as a fixed 400px strip.** Current override (18 Aug, final): `460px minmax(0, 520px)` + `column-gap: 48px` + **`justify-content: start`** — that last one is load-bearing, since the tracks total 1028px inside the 1200px column and without it the leftover 172px is distributed between the tracks instead of parked on the right. Earlier values (`minmax(300px,1fr) minmax(0,1.15fr)`, then `minmax(280px,400px) minmax(0,1fr)`, then the shared `--gz-grid-columns`) are history, not current.
- **`--gz-gutter` (24px)** — cover-left, buy-box-right and both band inner edges key off it. Define globally to move them together.
- **`product.type | capitalize` mangles multi-word types** ("Hardcover Non-Fiction" → "Hardcover non-fiction"). Check the real BooksoniX values before trusting it.

**Product / buy box (v3.4 — banked 18 Aug)**
- **The media gallery is ALREADY sticky, natively.** `<media-gallery>` carries `sticky-content` unconditionally (`snippets/product-media-gallery-content.liquid:338`) and `base.css:2574` gives it `position: sticky`. Never re-implement it. The only gap is `--sticky-header-offset`, which core assigns to `.product-details` only — retarget it at the gallery or the cover slides under a sticky header.
- **`buy-buttons` is a CONTAINER**, carrying Quantity, Add to cart and Accelerated checkout as children. The standalone `quantity` block is redundant alongside it.
- **There is no `icon-with-text` block.** Assemble `group` (Direction: Horizontal) + `icon` + `text`. Inner groups need Width **FIT** — Fill splits the row into equal thirds and wraps the longest item.
- **Never set a group's `Link` on a group containing the cart form** — `snippets/group.liquid:34` wraps all children in an `<a href>`.
- **`text` and `price` expose `font`, `font_size`, `letter_spacing`, `case`, `color` natively** — uppercase tracked labels and price weight need no CSS. But `text`'s colour offers only foreground / foreground-heading / primary: **no muted**. Text Width (Fit/Fill) and Max width (Narrow/Normal/None) interact — **Fill + None** for a full measure. Price size is a **px** dropdown; text size is **rem**.
- **⚠️ The rich-text field strips Liquid.** It (a) removes Liquid-built `<a href>` anchors and (b) parses `{{ }}` as a dynamic source and errors on any filter chain ("Change or remove the dynamic source(s) with errors"), leaving stray `">` fragments. **Anything needing a Liquid-built link or a filter must be a `custom-liquid` block** — which forfeits that block's native typography settings and pushes styling into a scoped snippet. Plain single-metafield dynamic sources (`{{ closest.product.metafields.custom.subtitle.value }}`) work fine.

**Shopify editor**
- **Rich text stores Enter inconsistently** — sometimes `<br/><br/>` inside one `<p>`, sometimes a real paragraph split. If CSS depends on paragraph structure, force a genuine split. **CSS has no `::last-line`**; `::first-line` only works predictably when an explicit break pins where the line ends.
- **Colours and native settings belong in the theme editor**, not in code. `settings_data.json` is the #1 editor-drift file — editing it in code fights the editor.
- **Read the schema, don't guess.** `config/settings_schema.json` (definitions) + `config/settings_data.json` (values) are the source of truth for native settings. Read them before styling or instructing editor changes.

## Already built — do not rebuild or touch

**Global**
- `snippets/gazelle-fonts.liquid` — self-hosts Switzer (woff2) + Cinzel; overrides `--font-body--family` / `--font-heading--family`. Render-hooked in `theme.liquid`.
- `snippets/gazelle-layout.liquid` — **THE single global source of page width** (1200px via `--page-content-width` on `body.page-width-narrow`), the carousel containment fix, and the shared column split `--gz-grid-columns: minmax(0, 1.4fr) minmax(0, 1fr)` / `--gz-grid-gap: 48px` (on plain `body`, so the theme editor's page-width control cannot silently change the ratio). **The band consumes those tokens; the hero deliberately does not** — see the cover-styles entry. Render-hooked in `theme.liquid`.
- **Colour schemes** — Scheme 1 Paper (site-wide), Scheme 5 Charcoal (footer). In the theme editor.

**Components**
- `snippets/gazelle-product-card.liquid` — the reusable atom. Takes a `product` param; renders cover/format/title/author/price. No wrapping `<a>` (Horizon's grid shell supplies the link). No compare-at/discount messaging. Reuse via `{% render 'gazelle-product-card', product: <product> %}`.
- `snippets/gazelle-book-specs.liquid` — specs table (`<dl>`), all confirmed metafields with `.value`, empty rows hidden, **dimensions deliberately un-guarded**.
- `sections/gazelle-book-detail-band.liquid` — two-column bottom band, spanning rail to rail. Tabs desktop / accordion mobile (first custom JS — scoped IIFE, a11y-correct). Subjects + Classification cards. Width and split come from `--page-content-width` / `--page-margin` / `--gz-grid-columns` / `--gz-grid-gap` — **no hardcoded 1200**, because this is a bare `<section>`, not a Horizon `.section`, so it never gets the section grid and has to reproduce that column itself. `--gz-tab-row-height` (75px) offsets the rail so the first card meets the first synopsis line; it is metric-dependent and carries its derivation in a comment.
- `snippets/gazelle-cover-styles.liquid` — the **fixed cover panel** (460×560, `#f3efe8`, radius 2px, flush to the left rail, image centred both axes at `max-height: 480px`, natural width, contain, 1px border + shadow), the hero grid, and the sticky-header offset retarget. Same panel for every book whatever the cover's aspect ratio. Centring the image inside it needs **three** rules — container `align-items`/`justify-content`, the `.constrain-height` override (core re-asserts its own at 0,4,0), and `flex: 0 0 auto` on `.product-media` (`base.css:1902` sets it `flex: 1` and it would otherwise stretch, leaving the image hard left). Below 750px the panel goes `width: 100%` / `aspect-ratio: 4/5` / image `max-height: 100%`. The file's header comment carries the full alignment history — **read it before changing how the cover sits**, it has flipped three times. **Rendered via a custom-liquid block in `product.json` — that block is COMMITTED, do not lose it.**
- `sections/gazelle-footer-styles.liquid` — style-only section, footer typography.

**Pages**
- **Collection page** — DONE Phase 1 (7 Jul). Native-first, ~zero custom CSS.
- **Product page** — buy box BUILT 18 Aug, entirely from native blocks, in the theme editor; hero reworked to the fixed-panel Fitzcarraldo pattern the same day, and the duplicate buy-box accordion removed (its three rows repeated the detail band from identical sources). Remaining: `gazelle-buy-box-styles` (`.gz-imprint`, `.gz-author` — the only custom CSS left), stock-indicator brand colour tokens, hero/band vertical air, New Release ribbon (blocked on `publication_date` type), price display (gated), Press & Reviews (gated), Subject links (taxonomy).
- **Footer** — BUILT + STYLED (14 Jul). Native four-column + utilities bar, Charcoal. **`footer-group.json` was NEVER used** — it had been silently overwritten by the editor; hand-built instead.
- **Header** — BUILT (14 Jul), native config + tokens, no custom section. **⚠️ The nav still carries the old Main menu including a `Catagories` typo — do NOT ship.** Real labels gated on taxonomy (admin → Navigation, zero theme work).
- **Homepage sections:** `gazelle-hero` (slideshow — uses a **dedicated mobile image at 800×367px**, do not strip it), `gazelle-focus` (three-panel scroller), `gazelle-strip` (banner), `gazelle-categories` (icon grid). **Billy's real artwork is in as of 16 July.**
- **Holding page:** `templates/password.liquid` customised.

If the header, footer, or homepage need to change to match the June mockups, **raise it with Grant first** — default is leave them alone.

## Working with Claude Code in THIS repo (environment limits — read before agent work)

- **ALWAYS launch `claude` from inside `~/Sites/gazelle-horizon`.** From the home dir it can't see CLAUDE.md or the repo and writes land in the wrong place. (Caused silent no-op "builds" on 2 July.)
- `.zshrc` aliases (`gazelle`, `gazelle-pull`, `gazelle-push`) do NOT exist in the agent's non-interactive shell. Call the underlying `shopify theme ...` commands directly.
- `shopify theme pull` / `push` require interactive device-auth the agent CANNOT complete. **Pulls and pushes are Grant's job**, run in an interactive terminal.
- **The agent CAN commit** (it will show the diff and write the message) **but does NOT push origin.** GitHub Desktop's "Push origin" is always Grant's step.
- **`git push` over HTTPS now FAILS** — GitHub killed password auth ("Password authentication is not supported"). **Use GitHub Desktop.** _To fix properly: switch the remote to SSH, or store a PAT in the keychain._
- **Terminal trap:** when git throws the `Username for 'https://github.com':` prompt, any commands already typed get **eaten by the prompt and silently never run.** Check what actually executed.
- **Trust the filesystem, not the agent's summary.** After any "done", verify with `git status` / `ls -la`.
- **`GIT_PAGER=cat`** to dodge the pager on diffs.
- **Run git in a separate terminal tab** — the `gazelle` dev server captures single keystrokes including `g`.
- **Targeted push:** `shopify theme push --theme 205873021277 --only sections/<file>.liquid`.
- Dev MCP is added at **local scope** (`claude mcp add … -e LIQUID=true`) — tied to this machine, not committed. George would re-add it. `LIQUID=true` is what enables Liquid/theme validation.

## The Claude Code collaboration loop (preferred method)

1. **Read the real repo files** — never work from pasted or guessed context.
2. **Read-and-propose before build.** For anything non-trivial, propose a numbered plan labelling each item `[NATIVE SETTING]` / `[NATIVE BLOCK]` / `[SCOPED CSS]` — **no edits yet.**
3. **Grant vets the plan** in the strategy chat; over-reach gets cut.
4. **Execute the approved plan** — one scoped task at a time.
5. **Grant verifies with `git status` / `git diff`** — not the agent's summary.
6. **Grant runs the interactive bits** — pulls, pushes, commits.
7. **Two-surface split:** strategy chat for planning/judgement/context-file; Claude Code for execution.

## The diagnostic-first method (standard for any layout/CSS problem)

**Established 8 July, reconfirmed 14 and 16 July: every blind CSS guess swung wrong; every read-only diagnostic landed the exact fix first time.**

The loop: **symptom → read-only diagnostic ("report exact cause + minimal fix, NO edits") → vet the plan → approved exact fix → commit → push → verify render.**

- **Confirm a pull has happened** before any diagnostic touching editor-owned JSON. This is the step that failed on 16 July.
- **Don't embed your hypothesis in the prompt.** Ask what causes X.
- **Require the native-vs-custom decision to be stated explicitly**, with what was checked to rule out native.
- **Verify by render.** A screenshot of the rendered page IS legitimate verification — often better than a computed-value check.
- **⚠️ Know what viewport your verification is running at.** On 16 July the DevTools checks ran in **iPad emulation at 820px**, where a 1200px constraint is meaningless — they proved nothing while looking rigorous. Don't let a check that measured the wrong thing stand in for a plain look at the page.

## Workflow

- **Code changes:** edit `.liquid` → commit in GitHub Desktop.
- **Content/editor changes:** run `gazelle-pull` first to bring `templates/*.json` down, then commit. `templates/index.json` and the header/footer group JSON hold section placement + settings.
- **End of every session (always):** `gazelle-pull` → commit (including JSON) → push origin. Treat this like hitting Save.
- **Local dev:** `gazelle` alias runs `shopify theme dev`; preview at `http://127.0.0.1:9292`; press `e` in the terminal to open the theme editor.
- **Push target:** "GSD Gazelle Build" (#205873021277), published live. "Horizon" (#199910359389) is a clean unmodified base reference — do not push to it.
- **Previews for Billy:** `shopify theme push --unpublished --theme "dev theme DD-MM"` — ask Grant for the current date before naming it.
- Repo: `github.com/gsdworks/gazelle-horizon`. Sync upstream `Shopify/horizon` periodically via GitHub's Sync fork button.

## Open caveats to revisit

- **Struck-RRP price decision** unresolved (see Price display). Blocks the buy-box price block.
- **Forthcoming-titles behaviour unresolved.** The spec conflicts on whether pre-publication titles go live with a "coming soon" badge or are held back. **Do not build a coming-soon badge until confirmed.**
- **Reviews conflict unresolved** — "no reviews at all" (24 April) vs "keep editorial Press & Reviews at the bottom" (Billy's call transcript). Needs Grant.
- **`publication_date` is text, not a Date type** — can't drive the New-Release rule until Dave sends ISO or we parse in Liquid.
- **`gazelle-focus.liquid` has pre-existing img width/height theme-check errors** — untouched file, pick up in a homepage session.
- Card `alt` text is just the title; consider "{{ product.title }} cover" (minor).
- **Carousel peek deviates from Billy's Waterstones reference** — Waterstones does clean 6-then-6 with no peek of card 7; we keep Horizon's native peek affordance. Visible deviation, flag to Billy rather than let him spot it.
