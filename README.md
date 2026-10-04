# Cub Scout Pack 1125 Website

Static website for **Cub Scout Pack 1125 — "Leaders and Trailblazers"**, Dumfries, Virginia.

**Live site:** https://dmvthrowers.club/pack1125-dumfries/

No build step, no frameworks: plain HTML/CSS/JS in `docs/`, served by GitHub Pages
(Settings → Pages → branch `main`, folder `/docs`). Every push to `main` redeploys in about a minute.

## Structure

```
README.md            — this file (not published)
LICENSE              — code license + content/trademark exclusions
docs/                — everything in here is the public website
├── index.html       — home: hero, four pillars, quick info, coming up
├── about.html       — what Cub Scouting is, about the pack, leadership
├── join.html        — who can join, 3 steps, dues, uniform
├── dens.html        — Lion → Arrow of Light den cards
├── calendar.html    — Google Calendar embed + meeting rhythm
├── gallery.html     — photo placeholders (replace with real photos)
├── resources.html   — NCAC, ScoutBook, Scout Shop, training links
├── contact.html     — contact card
├── 404.html         — "page not found" (links are absolute: /pack1125-dumfries/…)
├── style.css        — full theme (navy/gold/forest/cream)
├── config.js        — pack facts + mobile nav toggle
├── images/          — pack emblem, rank badges (PNG + WebP), icons, social card
├── favicon.ico, site.webmanifest
├── robots.txt, sitemap.xml
└── .nojekyll        — tells GitHub Pages to serve files as-is
```

## Editing

- **Pack facts** live in `docs/config.js` (`CONFIG` object). Most copy is also inline in the
  HTML pages — keep both in sync when facts change.
- **Unknowns** are marked as `<!-- TBD: ... -->` HTML comments in the pages.
- **Colors and fonts** are CSS variables at the top of `docs/style.css`.
- **"Coming Up"** on `index.html` is hand-maintained — update it after each event.
- **Every page repeats** the same header, nav, and footer. When you add or rename a page,
  update the nav and footer links on every page, plus `sitemap.xml`.
- **Each page's `<head>`** carries a canonical URL, Open Graph/Twitter preview tags, and a
  JSON-LD breadcrumb. Update them when you add a page. If the site moves to a new address
  (for example `pack1125.org`), search-and-replace `https://dmvthrowers.club/pack1125-dumfries/`
  across `docs/`, and update the `/pack1125-dumfries/` paths in `404.html`.
- **Content Security Policy:** each page has a CSP `<meta>` tag allowing only this site,
  Google Fonts, and the Google Calendar embed. Adding a new embed (form, video, map) means
  adding its domain to that tag on every page that uses it.
- **Images:** add both a `.png` and a `.webp`, wrap them in `<picture>`, and always set
  `width`, `height`, and descriptive `alt` text. Keep files under 500 KB.

## Youth protection and photos

Follow Scouting America's Youth Protection and digital privacy guidelines:

- Only post photos of Scouts with written parent/guardian permission.
- Never publish a Scout's full name, school, or contact details alongside a photo.
- Adult leader names and contact details go on the site only with that leader's OK.

## Preview locally

```sh
cd docs && python3 -m http.server 8000
# open http://localhost:8000/
```

## Branding

Colors are drawn from the official Pack 1125 flyer: deep navy, gold, red, and forest green.
The pack emblem and rank badges in `docs/images/` are cropped from the flyer artwork.

## License

Code is MIT-licensed; text, photos, the pack emblem, and Scouting America insignia are not.
See [LICENSE](LICENSE).
