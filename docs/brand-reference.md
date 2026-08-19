# Brand reference — gazellebookservices.co.uk

_Extracted 19 August 2026 from the live brand site (George's Webflow build) and its
stylesheet `cdn.prod.website-files.com/698d1c67253f91d1c7f97359/css/gazellebookservices-staged.webflow.shared.e08a2e55c.css`.
Read-only evidence, not a decision record. Where this disagrees with a decision already
taken for the theme, the decision wins unless Billy has asked otherwise._

## Typography — CONFIRMS the theme's existing decision

The brand site declares exactly two faces, as CSS variables:

```css
--_fonts---heading   : Trajanpro, Arial, sans-serif
--_fonts---paragraph : "Switzer Variable", Arial, sans-serif
```

- **Headings: Trajan Pro.** The theme uses **Cinzel** as the free stand-in — correct, and now evidenced rather than remembered. Real Trajan needs a webfont licence; only pursue if Billy asks.
- **Body: Switzer Variable.** The theme self-hosts **Switzer** via `snippets/gazelle-fonts.liquid`. Agrees.
- **Fraunces / Figtree / Blair appear nowhere.** The 7 July correction stands.
- **Do not change the type stack on this evidence.** It confirms what is already built.

Type scale on the brand site (for reference only — the theme has its own):
`h1 2.5–4rem, h2 2.25–2.5rem, h3 2–2.5rem, h4 1.75–2rem, h5 1.5rem, h6 1.25rem`,
paragraph `0.75 / 0.875 / 1 / 1.125 / 1.25rem`.

## Colour — the four reds are NAMED variables

```css
--main-red  : #940000
--light-red : #b92b2f
--alt-red   : #aa1f22
--dark-red  : #670c0e
```

Where each is used on the brand site:

| Variable | Value | Used for |
|---|---|---|
| `--main-red` | `#940000` | primary button fill (`.button-2.is-red`, `.nav-cta`), red uppercase subheadings (`.rl-text-style-subheading`) |
| `--light-red` | `#b92b2f` | button **hover** fill, footer link hover, the `-2` subheading variant |
| `--alt-red` | `#aa1f22` | secondary button hover, FAQ question text |
| `--dark-red` | `#670c0e` | a dark section background (`.options-section`), muted small text |

### Against the theme's tokens

| Theme token | Theme value | Nearest brand | Brand value | Verdict |
|---|---|---|---|---|
| Accent (brand red) | `#a11f21` | `--alt-red` | `#aa1f22` | one digit apart — close enough to look intentional, different enough to be wrong |
| Accent hover | `#7c1516` | `--dark-red` | `#670c0e` | theme is lighter and less brown |
| Secondary red | `#ae2628` | `--light-red` | `#b92b2f` | close |
| Ink / text | `#1a1917` | `--text-color--text-primary` | `#000` | brand uses pure black |
| Paper | `#faf7f2` | `--base-color-brand--soft-sand` | `#f7f4f0` | very close; brand also has beige `#fbf9f8` |
| Cover panel | `#f3efe8` | (no direct equivalent) | — | theme-only |

**Nothing matches exactly.** The theme palette reads as a hand-picked approximation of the
brand palette rather than a copy of it. Note the brand's *primary* button red is
`#940000` — materially deeper than any red the theme currently uses.

### ⚠️ Footer background — this is not a shade adjustment

```css
.section_footer { background-color: #f2f2f2 }   /* --lighter-grey */
```

**The corporate footer is light grey.** The theme's footer is **Scheme 5 "Charcoal"
(`#1a1917`), dark.** Billy's sheet row "Footer: background colour to match corporate
site" therefore means **inverting the footer from dark to light**, not nudging a value.
That is a visible identity change to a component that was built and signed off on 14 July.
**Confirm before building it.**

### ⚠️ Footer heading red — the brand site does NOT do this

Billy's row reads "Footer: category headings red like corporate site". On the brand site:

- Footer **links** hover to `--light-red` (`.footer_menu:hover`, `.footer-link:hover`).
- Footer **headings carry no red at all**.
- The red-uppercase-heading pattern he is probably describing lives elsewhere on the site:
  `.rl-text-style-subheading { color: var(--main-red); text-transform: uppercase }`
  and its `-2` variant using `--light-red`.

So the ask is reasonable but the reference does not literally exist. **Needs a pick
between `#940000` and `#b92b2f`** — do not guess it into the footer.

## Other conventions

- **Border radius** is generous: `--radius-small .75em`, `medium 1.25em`, `large 2em`,
  `round 3em` (pill buttons). The theme is much squarer (2px on the cover panel). A real
  divergence, but not something Billy has raised — leave it.
- **Neutrals:** black `#000`, `#111`, `#3b3b3b`, `#444`, `#666`, `#aaa`, `#ccc`, `#fff`.
- Several Webflow/Relume library defaults survive in the stylesheet (`--base-color-brand--lavender`,
  `mint-teal`, `dusty-plum`, `light-yellow`). **These are template leftovers, not Gazelle
  brand colours** — `.section_footer` even carries a lavender background that is overridden
  later by `#f2f2f2`. Do not treat any of them as brand values.

## What to adopt, and what not to

Per the brief: adopt the brand site's red and footer colour values *because Billy has
explicitly asked the footer to match*. Everything else here is reference.

- **Adopt (pending the two confirmations above):** footer background `#f2f2f2`, footer
  heading red — `#940000` or `#b92b2f`, Billy's pick.
- **Do not adopt:** the type stack (already decided, and it agrees anyway), the radius
  convention, any Webflow library colour.
- **Open question:** whether the theme's accent should move from `#a11f21` to the brand's
  `--alt-red #aa1f22`, or to `--main-red #940000` which is what the brand's buttons
  actually use. A one-token change with site-wide effect — Grant's call, not automatic.
