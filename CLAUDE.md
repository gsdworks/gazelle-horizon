# CLAUDE.md — Gazelle Books Shopify Theme

_Last updated: 16 July 2026_

This file is read at the start of every session. It defines how to work in this repo. Read it before touching any file.

## What this is

A brand-new Shopify storefront for **Gazelle Book Services**, a book distributor carrying ~55k titles across many independent publishers. Audience is mixed trade (booksellers, libraries) and retail. Built on **Shopify Horizon v3.4.0**, forked as `gsdworks/gazelle-horizon`. Store: `gazelle-books-2026.myshopify.com`, going live under `store.gazellebooks.co.uk`.

Product data is pushed into Shopify from **BooksoniX** via an event-driven REST API. You are not responsible for that integration; you build the front end that renders the data it produces.

## The project context file

**`gazelle-context-working.md` (repo root) is the master source of truth** for this project — decisions, state, open items, hard-won lessons. This file (CLAUDE.md) is the operating manual; that file is the record.

- **The repo copy is canonical.** Any copy in Claude project knowledge is a convenience snapshot and **may be stale — never edit from it.**
- **Read it before any non-trivial task.** It records why things are the way they are, and what has already been decided and must not be silently reversed.
- Edits are **surgical (`str_replace`), additive, never overwrite confirmed decisions**, and always update the `_Last updated:_` line.
- **⚠️ Verify currency by CONTENT, not date.** Two sessions ran on 14 July producing two different "14 July" files (960 and 985 lines) — a correct-looking date proves nothing. **Grep for the newest artefact you know exists on disk** (e.g. `grep -c gazelle-layout gazelle-context-working.md`). A master file that doesn't know about a snippet sitting in this repo cannot be current.

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

## Agent execution rules (Claude Code)

- Do **exactly** the task asked. Nothing more. No refactors, no extra features, no unrequested "improvements", no tidying of unrelated files.
- Prefer a native setting or block over writing code, every time.
- **If the native path isn't obvious, STOP and ask** — do not invent a custom solution.
- Never edit Horizon core files. If a change seems to need one, stop and flag it.
- **Never push. Never commit without showing the full diff first.** Pushes and commits are Grant's decision. Only an explicit approval counts — "ok", "yes", "do it", "go". Ambiguous or adjacent messages are not approval; if unsure, ask.
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
- **Scope all custom CSS with `{% style %}`** inside the section/snippet that uses it. Horizon has **no global custom-CSS field**, so there is no other correct place for it. No separate stylesheet edits to core assets.
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
- `thema_subjects` / `bic_subjects` currently carry **decoded names, not raw codes**. Front end is already wired correctly and self-heals when Dave switches the source.

**`custom.pubcode` does not exist yet.** PUBCODE is currently only a substring inside `tags_global` (`PUBCODE: CE1 - LINDEN PUBLISHING INC`). Do not build anything that depends on a discrete pubcode metafield.

**Data expectations:** many fields render empty until BooksoniX populates them. That is expected and fine. Empty rows hide.

## Native field map (what's native vs metafield)

| Displayed as | Source |
|---|---|
| Title | native `product.title` |
| Description | native `product.description` (body HTML) |
| Format (Paperback/Hardback) | native `product.type` |
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
- **Filters are configured in the Search & Discovery APP** (admin), not the theme: **Format** ← product type, **Imprint** ← vendor, **Price**. Availability removed. App-side config needs no pull or commit.
- **S&D "grouped values" can combine formats natively** — may remove that job from Dave entirely. Pending Billy's finalised combine list.
- The **Subject filter cannot be wired yet** — depends on the subject-taxonomy mapping, pending Billy. Do not fake it against guessed data.
- **Tags are reserved for editorial overlay** (seasonal, staff picks, prize winners), never core taxonomy. The integration applies no tags automatically.

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
- **Native hero grid pins the buy box right as a fixed 400px strip.** The mockup's proportional `minmax(300px,1fr) minmax(0,1.15fr)` is the fix.
- **`--gz-gutter` (24px)** — cover-left, buy-box-right and both band inner edges key off it. Define globally to move them together.
- **`product.type | capitalize` mangles multi-word types** ("Hardcover Non-Fiction" → "Hardcover non-fiction"). Check the real BooksoniX values before trusting it.

**Shopify editor**
- **Rich text stores Enter inconsistently** — sometimes `<br/><br/>` inside one `<p>`, sometimes a real paragraph split. If CSS depends on paragraph structure, force a genuine split. **CSS has no `::last-line`**; `::first-line` only works predictably when an explicit break pins where the line ends.
- **Colours and native settings belong in the theme editor**, not in code. `settings_data.json` is the #1 editor-drift file — editing it in code fights the editor.
- **Read the schema, don't guess.** `config/settings_schema.json` (definitions) + `config/settings_data.json` (values) are the source of truth for native settings. Read them before styling or instructing editor changes.

## Already built — do not rebuild or touch

**Global**
- `snippets/gazelle-fonts.liquid` — self-hosts Switzer (woff2) + Cinzel; overrides `--font-body--family` / `--font-heading--family`. Render-hooked in `theme.liquid`.
- `snippets/gazelle-layout.liquid` — **THE single global source of page width** (1200px via `--page-content-width` on `body.page-width-narrow`), plus the carousel containment fix. Render-hooked in `theme.liquid`.
- **Colour schemes** — Scheme 1 Paper (site-wide), Scheme 5 Charcoal (footer). In the theme editor.

**Components**
- `snippets/gazelle-product-card.liquid` — the reusable atom. Takes a `product` param; renders cover/format/title/author/price. No wrapping `<a>` (Horizon's grid shell supplies the link). No compare-at/discount messaging. Reuse via `{% render 'gazelle-product-card', product: <product> %}`.
- `snippets/gazelle-book-specs.liquid` — specs table (`<dl>`), all confirmed metafields with `.value`, empty rows hidden, **dimensions deliberately un-guarded**.
- `sections/gazelle-book-detail-band.liquid` — two-column bottom band. Tabs desktop / accordion mobile (first custom JS — scoped IIFE, a11y-correct). Subjects + Classification cards.
- `snippets/gazelle-cover-styles.liquid` — cover sizing (570px fixed height, natural width, contain, left-aligned, border+shadow), hero grid, buy-box inset. **Rendered via a custom-liquid block in `product.json` — that block is COMMITTED, do not lose it.**
- `sections/gazelle-footer-styles.liquid` — style-only section, footer typography.

**Pages**
- **Collection page** — DONE Phase 1 (7 Jul). Native-first, ~zero custom CSS.
- **Product page** — ~85% (8 Jul). Remaining: buy-box supporting elements, New Release ribbon, price display (gated), Press & Reviews (gated), Subject links (taxonomy).
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
- **Push target:** "GSD Gazelle Build July 7th" (#205873021277), published live. "Horizon" (#199910359389) is a clean unmodified base reference — do not push to it.
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

## Current build step

**Carousel containment DONE (16 July)** — `gazelle-layout.liquid` now contains the Featured Collection track to 1200px (6 cards + peek).

**Next:** subject-distribution **analysis** off the live data → **one-page taxonomy proposal to Billy** → build collections → nested Navigation lights up the (never-mocked) mega menu.

**Note:** collections are TWO separate problems — don't bundle them. (1) **Subject taxonomy** collections key off Thema/BIC/`main_subjects` — Billy's decision. (2) **Homepage curation** (Focus/Highlights) keys off PUBCODE — blocked on Dave surfacing PUBCODE as a discrete metafield.
