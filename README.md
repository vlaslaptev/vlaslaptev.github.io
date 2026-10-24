# Vlas Laptev — project showcase

Static portfolio for GitHub Pages. This repository contains **website files only**.
It does not include the source or installation packages of the featured applications.

## Local preview

```sh
python3 tools/build.py
python3 tools/check.py
python3 -m http.server 8767 --bind 127.0.0.1
```

English is the default at `http://127.0.0.1:8767/`; Russian is available at `/ru/`.
Every project card, including on the Russian showcase, opens its English landing.
Translations remain explicit choices; the site never redirects based on browser language.
Use Python 3.9 or later. No package installation or frontend build system is needed.
Serving locally does not publish anything. This revision has no deployment workflow.

## Add a project

1. Put the finished landing and its web assets in `projects/<slug>/`.
2. Add a record to `content/projects.json`. Use the existing records as examples:
   a unique slug, name, display order, platform, EN/RU descriptions and status,
   localized page URLs, and one or more images with EN/RU alt text.
   The `card` object supplies a small `icon`, an `interface` screenshot (with optional
   `{lang}` placeholder) and a short EN/RU `description`.
   Set `availability` to `available` for a public release, `beta` for a verified
   public TestFlight beta, or `development` until either is available. The card
   shows the corresponding EN/RU status.
3. Choose a card theme (`tabs`, `beewbe`, `battery`, `pet`, `garnet`, or add a named style)
   for its background. Unstyled cards use a white background. All cards have equal
   width: four columns on desktop, two on tablet and one on phones. New records
   automatically flow into the next row; eight cards fit in two rows on Full HD.
4. Run `python3 tools/build.py`, then `python3 tools/check.py`.

## Card design

The home page uses the `concept` treatment: a small decorative composition inspired
by each project, in a colored header occupying at most one quarter of the card.
Each project appears once, without comparison numbers.

`content/showcase.json` selects the treatment through `card_variants`. The optional
`icon` and `interface` treatments remain available for local design comparisons.
Listing multiple treatments renders each project in each treatment and adds numbered
labels; the catalog itself is not duplicated.
Concept compositions are defined in `card_visual()` in `tools/build.py` and styled
in `assets/showcase.css`. Unknown themes receive a generic icon composition.

The concept cards use dedicated thumbnails in `assets/card-thumbnails/` (WebP with
PNG fallback, at 1x/2x/3x). Their logical sizes are 54px for the side beewbe pets,
72px for the center pet and 44px for Pet Project. Product pages retain their original images as full-size links and PNG fallbacks.
Their inline previews use pre-generated WebP variants from `content/image-variants.json`. Thumbnail assets are pre-generated; the normal Python build needs no image
library. Keep the pixel-art thumbnail lossless and preserve image transparency.

The showcase defaults to dark colors. An explicit system light preference activates
the light palette through CSS; changes apply live, without JavaScript or a saved
override. Product landings keep their own themes.

`assets/showcase.js` plays a short header animation when a card first enters view,
and on pointer or keyboard interaction. Tabs fan out, beewbe pets blink, battery
rings fade in and the pixel star twinkles. There are no continuous loops. The
system reduced-motion preference disables these sequences, including when changed
while the page is open. Without JavaScript the compositions remain visible and static.

The build produces real HTML cards. Navigation and content do not depend on JavaScript.
An existing landing can live independently of the generator. If desired, add body
templates at `templates/<slug>.en.html` and `templates/<slug>.ru.html`: the generator
will add shared navigation, metadata and the footer using the catalog URLs.
The two URLs must be distinct when using two templates. For an English-only landing,
point both catalog URLs to it and supply a Russian `link_note`, as BatteryGrid does.
The note is visible on the card and included in its accessible description.
All project cards pass `?from=en` or `?from=ru` to the small return-navigation
script. It preserves the showcase language across reloads, new tabs and explicit
product-language switches, without cookies or automatic language redirects. Without
JavaScript, product language switches and the normal static return links still work;
BatteryGrid additionally exposes both showcase links.

## Pages and ownership

| Route | Content |
| --- | --- |
| `/`, `/ru/` | Generated project showcase and contact links |
| `/projects/project-tab-icons/` + `ru/` | New EN/RU landing with public project screenshots and external GitHub links |
| `/projects/pet-project/` + `ru/` | New EN/RU landing with native app preview images |
| `/projects/garnet/` + `ru/` | EN/RU cycle diary landing with native calendar and statistics screenshots |
| `/projects/beewbe/` | Existing landing and privacy pages, all 12 original languages |
| `/projects/batterygrid/` | Existing English macOS landing |

Edit the portfolio text in `tools/build.py`, cards in `content/projects.json`, and new
product bodies in `templates/`. `assets/site.css` and `assets/site.js` belong only to
the portfolio and new landings. `assets/showcase.css` styles only the compact catalog.
Imported pages keep independent styles and scripts.

Garnet's 12 screenshots were captured on 24 October 2026 from a fresh local-source
build on an iPhone 18 Pro Max simulator running iOS 27.0, at 1320×2868 pixels.
Calendar, statistics and partner access each have EN/RU light/dark captures. All diary data
and connections are isolated demonstration fixtures. Dated image filenames avoid
reusing old browser image caches; keep the original PNG captures unchanged and
regenerate their responsive WebP variants when replacing them.
`_config.yml` excludes authoring files from GitHub Pages. Do not add `.nojekyll`
without providing an equivalent publishing allowlist.

## Deliberate adaptations of imported pages

- **beewbe:** original composition, illustrations and translated policy text retained.
  Added return navigation and metadata, optimized previews, scalable text, improved
  contrast and touch targets, and a language menu that fits short viewports.
- **BatteryGrid:** original composition and full-resolution images retained. Added return navigation,
  metadata and `responsive.css`; changed the fixed 770px viewport to device width.
  The existing desktop mosaic remains intact. On phones, examples reflow into pairs.
  Palettes and density use native fieldsets and CSS `:has()` state; the mobile table
  includes a scroll hint and pinned row labels. Release status is visible in the hero.
  Download and checksum links to local DMGs were replaced with availability/contact
  information. No DMG, checksum, payment integration or app source was imported.
- Existing image credits remain with their product. Screenshots show native previews;
  illustrative readings and game states are described as such, not as live demos.

Project Tab Icons has a verified public repository and download link. Garnet has a
public TestFlight beta: https://testflight.apple.com/join/5rTFRqQG (verified on
24 October 2026). Other projects have an explicit development/availability status. Do not
invent App Store, TestFlight, source or download links. Update release information
only when the corresponding public URL is available.

## Responsive product images

`tools/images.py` renders the saved WebP variants with accurate `sizes`, intrinsic
dimensions and PNG fallbacks. `tools/optimize_images.py` is an optional authoring step
requiring Pillow; normal site builds require only Python’s standard library. It never
changes original PNGs. UI screenshots and pixel art use lossless WebP; beewbe’s pet
illustrations use quality 90 with transparency preserved. After replacing an image,
regenerate its variants and update imported page source sets if its dimensions change.

`tools/build.py` also refreshes content hashes in CSS/JS references in all pages,
including imported ones, so updates do not reuse stale browser resources. It preserves
the imported page content.

## Verification and publication

`tools/check.py` verifies local resources and fragments, metadata, alt attributes,
unique IDs and the website file boundary. Browser QA also covers phone/tablet/desktop
layouts, EN/RU, Arabic RTL, product switches, keyboard focus and no-JavaScript content.

The preview and QA captures are not part of the site. Never copy application
repositories, `.git` directories, build results, internal reports, credentials or
installation packages into `projects/`. Review `git status` and the diff before any
future commit or publication. Publishing is a separate step from local preview.
