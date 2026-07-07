# CLAUDE.md — Gazelle Books Shopify Theme

_Last updated: 7 July 2026_

This file is read at the start of every session. It defines how to work in this repo. Read it before touching any file.

## What this is

A brand-new Shopify storefront for **Gazelle Book Services**, a book distributor carrying ~55k titles across many independent publishers. Audience is mixed trade (booksellers, libraries) and retail. Built on **Shopify Horizon v3.4.0**, forked as `gsdworks/gazelle-horizon`. Store: `gazelle-books-2026.myshopify.com`, going live under `store.gazellebooks.co.uk`.

Product data is pushed into Shopify from **BooksoniX** via an event-driven REST API. You are not responsible for that integration; you build the front end that renders the data it produces.

## Build philosophy — NATIVE-FIRST (governs every decision)

Get as close to the June mockups as possible using **as much out-of-the-box Horizon as we can**. This is a deliberate speed + low-risk trade on a fixed-fee build: less custom Liquid means faster delivery, a smaller error surface, and easier maintenance. Apply it at every stage.

**Priority order for any piece of UI:**
1. Native Horizon section / block / setting
2. Theme-editor configuration
3. A small, scoped `gazelle-` snippet
4. (Last resort) custom Liquid

Rules that follow from this:
- **Default to native Horizon.** Only build custom where a **confirmed requirement** genuinely can't be met natively. Precedent: the product card — Horizon's `_product-card` couldn't be extended without core edits, so a scoped `custom-liquid` → `gazelle-` snippet was the *minimal* override. That's the bar.
- **Any custom must be minimal, scoped, `gazelle-` prefixed, and touch no core files.** Smallest change that meets the rule.
- **Close-enough beats perfect.** If native Horizon gets ~90% of a mockup detail, take the 90% rather than burning hours on custom code for the last 10% — **unless** it's a confirmed business rule (no-save messaging, no back orders, create-only price, etc.), which always wins over the mockup.
- **This is forward-looking.** It does not mean re-doing already-built work to be "more native." Leave built sections alone (see "Already built").

## Agent execution rules (Claude Code)

- Do **exactly** the task asked. Nothing more. No refactors, no extra features, no unrequested "improvements", no tidying of unrelated files.
- Prefer a native setting or block over writing code, every time.
- **If the native path isn't obvious, STOP and ask** — do not invent a custom solution.
- Never edit Horizon core files. If a change seems to need one, stop and flag it.
- **Never push. Never commit without showing the full diff first.** Pushes and commits are Grant's decision.
- Trust the filesystem, not your own summary. After any "done", the change isn't real until `git status` / `ls -la` confirms it.

## Hard rules (do not break these)

- **Never edit Horizon core files.** All custom work is new files, so upstream `Shopify/horizon` can be synced without merge conflicts. If a change seems to need a core edit, stop and flag it.
  - **Approved core-file exceptions** (deliberate, keep this list current):
    - `layout/theme.liquid` — two lines before `</head>` (font preload + `{% render 'gazelle-fonts' %}`) to self-host the Switzer brand body font; added 7 July. Re-add these two lines if a Horizon update overwrites them.
- **Prefix all custom files `gazelle-`.** Sections: `sections/gazelle-*.liquid`. Blocks: `blocks/gazelle-*.liquid`. Custom templates: `templates/*.gazelle.json` (e.g. `templates/product.gazelle.json`).
- **Scope all custom CSS with `{% style %}`** inside the section/block that uses it. Horizon has **no global custom-CSS field**, so there is no other correct place for it. No separate stylesheet edits to core assets.
- **No page builders, no third-party UI frameworks, no CSS libraries.** Vanilla Liquid + CSS + minimal JS.
- **Lazy-load below-the-fold sections. Minimise JS.** Test on a mid-range Android on a slow connection, not just desktop.
- **Bind to native Shopify objects wherever one exists** (menus, policy pages, social settings, product fields) rather than hardcoding.
- **Do not touch password / store-visibility settings.** The store is behind a password and the primary domain already points at it. Disabling the password would expose a dev environment publicly.
- **When a spec is ambiguous or a metafield key isn't confirmed below, stop and ask.** Don't guess a key name or invent a decision.

## Design source of truth

The three high-fidelity mockups in the project (`gazelle-homepage-mockup-June.html`, `gazelle-collection-page-mockup-June.html`, `gazelle-product-page-mockup-June.html`) are the approved design and your visual reference. They are standalone HTML for sign-off, **not** part of the theme.

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

### Typography
- **Display / headings:** Trajan Pro
- **Serif body** (titles, descriptions, prices): Fraunces
- **UI sans** (nav, buttons, labels): Figtree

**Typography is provisional — keep the font stack tokenised and swappable.** Trajan Pro is a commercial Adobe font used only as a placeholder in the mockups. **Cinzel** (Google Fonts) is the free Trajan stand-in if needed before licensing is sorted. Billy's eventual target is the brand site's **Blair / ATF** display font, not in hand yet. Also: Billy wants **less all-caps** than the current mockup treatment. Do not hardcode Trajan as final or bake in uppercase everywhere.

### Layout
- Page width max **1200px**, centred.

## Metafield contract

All book metafields live in the **`custom`** namespace. Bind to the key path (e.g. `product.metafields.custom.author`) — the page renders empty until BooksoniX populates data, which is expected and fine. The only thing that forces a rebuild is a key name changing, so treat this list as the contract.

**Confirmed keys (safe to wire now):**
- `custom.isbn`
- `custom.author` — strip the `"By (author):"` prefix on display
- `custom.publisher`
- `custom.language`
- `custom.publication_date`
- `custom.subtitle` — its own field, do not append to the title

**Pending (do NOT wire yet — Grant is locking these; leave explicit `{# TODO #}` stubs):**
`depth`, `illustrations`, `series`, `pages`, `dimensions`, `weight`, `audience`, Thema codes, BIC codes.

**ISBN-13 is not a metafield.** It lives in the native **variant barcode** field (`product.selected_or_first_available_variant.barcode`), confirmed landing there from BooksoniX with variants created inventory-tracked. Do not create or bind an `isbn13` metafield for it.

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

Build the layout and structure freely (native-first); wire only confirmed metafields, stub the rest.

**Do NOT include:**
- Star ratings or customer review counts in the buy box. Gazelle's audience is trade; individual star reviews add nothing.
- A format/edition selector (HB/PB/eBook). Every book is a separate product with its own ISBN; editions are not linked. Gazelle do not sell ebooks — no ebook option anywhere.
- Any "Save X%" or discount-percentage messaging on price.

**Do include:**
- **Clickable Publisher and Imprint** — each links through to a filtered collection of those titles. (Author is already clickable.)
- **Classification box** in the side rail, under Subjects: Thema codes and BIC codes in separate sub-blocks. These codes are *displayed* even though full subject-taxonomy mapping is parked — display only, not navigation.
- **Product Details:** dimensions shown as H × W × D (depth included), plus Illustrations.
- **New Release flag:** applied automatically when `publication_date` falls in the current month, drops off the following month. Logic driven by the metafield, not a manual tag.

### Stock & buy box (confirmed on Billy's call)
- **No back orders, ever.** If a title is out of stock, it cannot be ordered.
- **Out-of-stock titles stay visible** — on the product page *and* on collection pages. They must not disappear (publishers would flood Gazelle with "why isn't my title showing" emails; the page also stays as a link for anyone arriving via mailer/Google).
- Out of stock = **Add to basket disabled** + an optional **"notify me when back in stock"** email capture.
- **Traffic-light stock indicator:** in stock (green) / low stock (amber) / out of stock (red). Largely a back-end setting plus the display.

### Price display (confirmed mechanic)
- Show the native price. A compare-at strikethrough appears **only when Gazelle have actively discounted** a title (compare-at = RRP, price = the lower Gazelle price).
- **Compare-at MUST be empty when selling at RRP**, or Shopify renders a broken/empty strikethrough.
- Never show "Save X%" or any discount-percentage messaging.

**Pending — do not build yet, confirm with Grant first:**
- **Struck-through RRP shown alongside the price by default** (the June mockup's "was £X, now £Y" treatment). This conflicts with the no-discount-messaging rule above and overlaps the out-of-scope 25% pricing automation. **Undecided — needs Billy.** Do not build the buy box's price block until resolved.
- "**Press & Reviews**" block at the bottom (editorial/trade reviews from metadata, not customer stars). There is an unresolved conflict in the record: an earlier decision was "no reviews system at all." Treat as undecided until Grant confirms.
- Suppressing empty metafield fields entirely (currently they render empty / "no data"). Minor, not a blocker.

## Collection page requirements

- Use Horizon's **stock collection section** for faceting, sort, and pagination. Drop the custom product card into it via the grid-override pattern below; do not hand-roll commerce plumbing.
- **Format filter** maps to native product type.
- The **Subject filter cannot be wired for real yet** — it depends on the subject-taxonomy mapping, which is still pending Billy's sign-off. Leave it as a visual placeholder or omit until the mapping lands. Do not fake it against guessed data.
- **Tags are reserved for editorial overlay** (seasonal, staff picks, prize winners), never core taxonomy. The integration applies no tags automatically.

## The grid-override pattern (CRITICAL — reuse for every commerce page)

Horizon's product card (`blocks/_product-card.liquid`) and the collection section (`sections/main-collection.liquid`) are CORE — never edit them. The card `type` and its child-block whitelist are baked in.

- To put a custom card in the stock grid: in the *template* (`collection.json` etc.), swap the `_product-card` block's child blocks for a single `custom-liquid` block (which IS on Horizon's whitelist) containing `{% render 'gazelle-product-card', product: closest.product %}`.
- `closest.product` resolves inside block-setting Liquid. This keeps Horizon's native faceting, sort, and pagination intact.
- **VERIFY it renders populated data (not blank)** — this is the one inferred assumption. If `closest.product` doesn't resolve in the grid's block structure, stop and flag it rather than restructuring the section.

## Already built — do not rebuild or touch

- **Product card (the reusable atom):** `snippets/gazelle-product-card.liquid` — done, reviewed, committed. Takes a `product` param, renders cover/format/title/author/price, no wrapping `<a>`, no compare-at/discount messaging. Reuse everywhere via `{% render 'gazelle-product-card', product: <product> %}`. Fonts bound to Horizon vars (`--font-body--family`, `--font-subheading--family`) with mockup fallbacks; colours are hardcoded brand hex (deliberate).
- **Homepage sections (live):** `gazelle-hero` (rotating slideshow — uses a **dedicated mobile image at 800×367px**; do not strip it, the desktop crop doesn't work on mobile), `gazelle-focus` (three-panel scroller), `gazelle-strip` (static banner), `gazelle-categories` (circular icon grid).
- **Footer:** `footer-group.json` delivered (config, wires three menu blocks + utilities bar). Menus are created in admin.
- **Holding page:** `templates/password.liquid` customised.
- **Product card image fix:** `--product-media-fit: contain` on `.product-media-container`, portrait ratio, centred. Revisit once real data is in, but don't undo it.

If the header, footer, or homepage need to change to match the June mockups, raise it with Grant first — default is leave them alone and build only what's missing (product page, collection page, book-specs block, content/PDF pages).

## Working with Claude Code in THIS repo (environment limits — read before agent work)

- **ALWAYS launch `claude` from inside `~/Sites/gazelle-horizon`.** Launching from the home dir means it can't see CLAUDE.md or the repo, and file writes land in the wrong place. (This caused silent no-op "builds" on 2 July.)
- `.zshrc` aliases (`gazelle`, `gazelle-pull`, `gazelle-push`) do NOT exist in the agent's non-interactive shell. Call the underlying `shopify theme ...` commands directly.
- `shopify theme pull` / `push` require interactive device-auth the agent CANNOT complete. Pulls and pushes are Grant's job, run in an interactive terminal.
- Trust the filesystem, not the agent's summary. After any "done", verify with `git status` / `ls -la` before believing a file was written or edited.

## Workflow

- **Code changes:** edit `.liquid` → commit in GitHub Desktop.
- **Content/editor changes:** run `gazelle-pull` first to bring `templates/*.json` down, then commit. `templates/index.json` and the header/footer group JSON hold section placement + settings.
- **End of every session (always):** `gazelle-pull` → commit (including JSON) → push origin. Treat this like hitting Save.
- **Local dev:** `gazelle` alias runs `shopify theme dev`; preview at `http://127.0.0.1:9292`; press `e` in the terminal to open the theme editor.
- **Previews for Billy:** `shopify theme push --unpublished --theme "dev theme DD-MM"` — ask Grant for the current date before naming it. Not needed after every session.
- Repo: `github.com/gsdworks/gazelle-horizon`. Sync upstream `Shopify/horizon` periodically via GitHub's Sync fork button.

## Open caveats to revisit

- **`product.type | capitalize`** only capitalises the first letter of the whole string, so multi-word product types get mangled (e.g. "Hardcover Non-Fiction" → "Hardcover non-fiction"). Check the real BooksoniX `product.type` values before trusting it; fix if they're ever multi-word.
- **Product-page struck-RRP price decision** is unresolved (see Product page → Price display). Blocks the buy-box price block.
- **Forthcoming-titles behaviour is unresolved.** The spec conflicts on whether pre-publication titles are pushed live with a "coming soon" badge, or held back until on-sale. Do not build a coming-soon badge until confirmed.
- Card `alt` text is just the title; consider "{{ product.title }} cover" for screen readers (minor).

## Current build step

Wiring `snippets/gazelle-product-card.liquid` into `collection.json` via the grid-override pattern above. Next after that: configure the brand fonts in theme settings (moves previews off Inter), then header restyle + footer config.
