# CLAUDE.md — Gazelle Books Shopify Theme

_Last updated: 2 July 2026_

This file is read at the start of every session. It defines how to work in this repo. Read it before touching any file.

## What this is

A brand-new Shopify storefront for **Gazelle Book Services**, a book distributor carrying ~55k titles across many independent publishers. Audience is mixed trade (booksellers, libraries) and retail. Built on **Shopify Horizon v3.4.0**, forked as `gsdworks/gazelle-horizon`. Store: `gazelle-books-2026.myshopify.com`, going live under `store.gazellebooks.co.uk`.

Product data is pushed into Shopify from **BooksoniX** via an event-driven REST API. You are not responsible for that integration; you build the front end that renders the data it produces.

## Hard rules (do not break these)

- **Never edit Horizon core files.** All custom work is new files, so upstream `Shopify/horizon` can be synced without merge conflicts. If a change seems to need a core edit, stop and flag it instead.
- **Prefix all custom files `gazelle-`.** Sections: `sections/gazelle-*.liquid`. Blocks: `blocks/gazelle-*.liquid`. Custom templates: `templates/*.gazelle.json` (e.g. `templates/product.gazelle.json`).
- **Scope all custom CSS with `{% style %}`** inside the section/block that uses it. Horizon has **no global custom-CSS field**, so there is no other correct place for it. No separate stylesheet edits to core assets.
- **No page builders, no third-party UI frameworks, no CSS libraries.** Vanilla Liquid + CSS + minimal JS.
- **Lazy-load below-the-fold sections. Minimise JS.** Test on a mid-range Android on a slow connection, not just desktop.
- **Bind to native Shopify objects wherever one exists** (menus, policy pages, social settings, product fields) rather than hardcoding. Custom markup only where it earns its place.
- **Do not touch password / store-visibility settings.** The store is behind a password and the primary domain already points at it. Disabling the password would expose a dev environment publicly.
- **When a spec is ambiguous or a metafield key isn't confirmed below, stop and ask.** Don't guess a key name or invent a decision.

## Design source of truth

The three high-fidelity mockups in the project (`gazelle-homepage-mockup-June.html`, `gazelle-collection-page-mockup-June.html`, `gazelle-product-page-mockup-June.html`) are the approved design. They are standalone HTML for sign-off, **not** part of the theme. Your job on the page builds is to translate them faithfully into Liquid. Match layout, spacing, and the tokens below.

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

**ISBN-13 is not a metafield.** It lives in the native **variant barcode** field (`product.selected_or_first_available_variant.barcode`). Do not create or bind an `isbn13` metafield for it.

## Native field map (what's native vs metafield)

| Displayed as | Source |
|---|---|
| Title | native `product.title` |
| Description | native `product.description` (body HTML) |
| Format (Paperback/Hardback) | native `product.type` |
| Imprint | native `product.vendor` |
| Price (UK RRP) | native price |
| Cover image | native, first image |
| ISBN-13 (EAN) | native `variant.barcode` |

## Product page requirements (Billy's decisions)

Build the layout and structure freely; wire only confirmed metafields, stub the rest.

**Do NOT include:**
- Star ratings or customer review counts in the buy box. Gazelle's audience is trade; individual star reviews add nothing.
- A format/edition selector (HB/PB/eBook). Every book is a separate product with its own ISBN; editions are not linked. Gazelle do not sell ebooks — no ebook option anywhere.
- Any "Save X%" or discount-percentage messaging on price.

**Do include:**
- **Clickable Publisher and Imprint** — each links through to a filtered collection of those titles. (Author is already clickable.)
- **Classification box** in the side rail, under Subjects: Thema codes and BIC codes in separate sub-blocks. These codes are *displayed* even though full subject-taxonomy mapping is parked — display only, not navigation.
- **Product Details:** dimensions shown as H × W × D (depth included), plus Illustrations.
- **Stock as a traffic light:** in stock (green) / low stock (amber) / out of stock (red).
- **New Release flag:** applied automatically when `publication_date` falls in the current month, drops off the following month. Logic driven by the metafield, not a manual tag.

**Pending — do not build yet, confirm with Grant first:**
- "**Press & Reviews**" block at the bottom (editorial/trade reviews from metadata, not customer stars). There is an unresolved conflict in the record: an earlier decision was "no reviews system at all." Treat as undecided until Grant confirms.
- Suppressing empty metafield fields entirely (currently they render empty / "no data"). Minor, not a blocker.

## Collection page requirements

- Use Horizon's **stock collection section** for faceting, sort, and pagination. Drop the custom product card into it; do not hand-roll commerce plumbing.
- **Format filter** maps to native product type.
- The **Subject filter cannot be wired for real yet** — it depends on the subject-taxonomy mapping, which is still pending Billy's sign-off. Leave it as a visual placeholder or omit until the mapping lands. Do not fake it against guessed data.
- **Tags are reserved for editorial overlay** (seasonal, staff picks, prize winners), never core taxonomy. The integration applies no tags automatically.

## Already built — do not rebuild or touch

- **Homepage sections (live):** `gazelle-hero` (rotating slideshow), `gazelle-focus` (three-panel scroller), `gazelle-strip` (static banner), `gazelle-categories` (circular icon grid).
- **Footer:** `footer-group.json` delivered (config, wires three menu blocks + utilities bar). Menus are created in admin.
- **Holding page:** `templates/password.liquid` customised.
- **Product card image fix:** `--product-media-fit: contain` on `.product-media-container`, portrait ratio, centred. Revisit once real data is in, but don't undo it.

If the header, footer, or homepage need to change to match the June mockups, raise it with Grant first — default is leave them alone and build only what's missing (product page, collection page, shared product card, book-specs block, content/PDF pages).

## Build strategy

- **Stock Horizon sections for commerce-critical functionality** (faceting, sort, pagination, cart). **Custom `gazelle-` sections/blocks only for bespoke visual pieces.**
- The **shared product card** is the reusable atom (homepage, collection, related products). Build and stabilise it before the pages that consume it.

## Workflow

- **Code changes:** edit `.liquid` → commit in GitHub Desktop.
- **Content/editor changes:** run `gazelle-pull` first to bring `templates/*.json` down, then commit. `templates/index.json` and the header/footer group JSON hold section placement + settings.
- **End of every session (always):** `gazelle-pull` → commit (including JSON) → push origin. Treat this like hitting Save.
- **Local dev:** `gazelle` alias runs `shopify theme dev`; preview at `http://127.0.0.1:9292`; press `e` in the terminal to open the theme editor.
- **Previews for Billy:** `shopify theme push --unpublished --theme "dev theme DD-MM"` — ask Grant for the current date before naming it. Not needed after every session.
- Repo: `github.com/gsdworks/gazelle-horizon`. Sync upstream `Shopify/horizon` periodically via GitHub's Sync fork button.
