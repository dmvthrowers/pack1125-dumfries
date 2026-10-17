# Cub Scout Pack 1125 Website

Static website for **Cub Scout Pack 1125 — "Leaders and Trailblazers"**, Dumfries, Virginia.

**Live site:** https://dmvthrowers.club/pack1125-dumfries/

No build step, no frameworks: plain HTML/CSS/JS in `docs/`, published to GitHub Pages by the
"Build and deploy" workflow (Settings → Pages → Source: **GitHub Actions**). Every push to `main` runs
the site checks and, if they pass, redeploys in about a minute.

## Structure

```
README.md            — this file (not published)
CONTRIBUTING.md      — how to propose a change (pull requests, browser editing, photo rules)
LICENSE              — code license + content/trademark exclusions
scripts/check_site.py  — site checker (links, images, metadata, nav, sitemap, freshness)
scripts/check_links.py — outside-link checker (monthly)
.github/workflows/   — check-site (every push and PR), deploy (main → GitHub Pages),
                       check-links (1st of each month)
.github/             — PR template, CODEOWNERS (reviewers), issue form for update requests
docs/                — everything in here is the public website
├── index.html       — home: hero, four pillars, quick info, coming up
├── about.html       — what Cub Scouting is, about the pack, leadership
├── join.html        — who can join, 3 steps, dues, uniform
├── families.html    — new families: first meeting, first month, forms, uniform basics
├── dens.html        — Lion → Arrow of Light den cards
├── calendar.html    — upcoming events (filled in at publish time), Google Calendar (loads on click), meeting rhythm
├── gallery.html     — photo sets (images/gallery/) + "Coming Soon" placeholders
├── resources.html   — NCAC, Scoutbook Plus, financial aid, Scout Shop, training links
├── faq.html         — new-family FAQ (native <details> accordion + FAQPage JSON-LD)
├── contact.html     — contact card
├── privacy.html     — privacy & youth-protection photo policy (footer link only)
├── 404.html         — "page not found" (links are absolute: /pack1125-dumfries/…)
├── style.css        — full theme (navy/gold/forest/cream)
├── config.js        — pack facts, mobile nav toggle, click-to-load calendar
├── fonts/           — self-hosted Inter + Montserrat (WOFF2) and their licenses
├── images/          — pack emblem, rank badges, Cub Scouts / NCAC / Future Kings logos (PNG + WebP), icons, social card
├── favicon.ico, site.webmanifest
├── robots.txt       — only used if the site moves to its own domain (see the file)
├── sitemap.xml      — one <lastmod> per page; matches each page's "Page updated" line
└── .nojekyll        — tells GitHub Pages to serve files as-is
```

## Making changes

All changes go through pull requests. See [CONTRIBUTING.md](CONTRIBUTING.md), including how
to edit right in the browser. The **Check site** test runs on every PR.

**Protecting `main`** (repo owner, one time): Settings → Rules → Rulesets → New branch ruleset.
- Name: `Protect main`. Enforcement: **Active**. Target branches: **Include default branch**.
- Bypass list: add **Repository admin** (so the owner can still fix an emergency).
- Turn on: **Restrict deletions**, **Block force pushes**, **Require a pull request before
  merging** (1 required approval once a second reviewer is a collaborator; 0 until then),
  and **Require status checks to pass** → add `check`, `validate` and `browser`.

## Editing

- **Pack facts** live in `docs/config.js` (`CONFIG` object). Most copy is also inline in the
  HTML pages — keep both in sync when facts change.
- **Unknowns** are marked as `<!-- TBD: ... -->` HTML comments in the pages.
- **Colors and fonts** are CSS variables at the top of `docs/style.css`.
- **"Coming Up"** on `index.html` is hand-maintained — update it after each event. The same
  events are listed as `Event` JSON-LD at the top of `index.html` (for Google and AI search);
  add new ones there and remove past ones. The checker warns about past events.
- **"Page updated"** at the bottom of each page must match that page's `<lastmod>` in
  `sitemap.xml`. When you change a page, set both to today. On pull requests the checker
  fails if a changed page still has an old date.
- **Every page repeats** the same header, nav, and footer. When you add or rename a page,
  update the nav and footer links on every page (including the absolute links in `404.html`),
  plus `sitemap.xml`. The checker will tell you if you missed one.
- **FAQ:** each answer appears twice in `faq.html` — once visible, once in the `FAQPage`
  JSON-LD at the top. Change both.
- **Each page's `<head>`** carries a canonical URL, Open Graph/Twitter preview tags, and a
  JSON-LD breadcrumb. Update them when you add a page. If the site moves to a new address
  (for example `pack1125.org`), search-and-replace `https://dmvthrowers.club/pack1125-dumfries/`
  across `docs/`, and update the `/pack1125-dumfries/` paths in `404.html`.
- **Content Security Policy:** each page has a CSP `<meta>` tag allowing only this site
  (fonts are self-hosted in `docs/fonts/`); only `calendar.html` also allows the Google
  Calendar frame. Adding a new embed (form, video, map) means adding its domain to that tag
  on the page that uses it, and to the privacy page's list of outside services.
- **Images:** add both a `.png` and a `.webp`, wrap them in `<picture>`, and always set
  `width`, `height`, and descriptive `alt` text. Keep files under 500 KB.

## Google Calendar

The Calendar page embeds the pack's Google Calendar. It only shows events to the public if the
calendar is shared publicly: in Google Calendar, open the pack calendar's **Settings and sharing →
Access permissions for events → Make available to public** (choose "See all event details").
Until then, signed-out visitors see a Google sign-in box instead of events, and the "Add the pack calendar to your Google Calendar" link
on the Calendar page fails for anyone the calendar isn't shared with. You can test it: while signed out, open
`https://calendar.google.com/calendar/ical/<calendar id, with @ written as %40>/public/basic.ics`; a 404 means the calendar is still private.

The embed loads only when a visitor clicks **Show the Calendar**, so no page contacts Google
until then (see `config.js`). The calendar address lives in `calendar.html` (`data-src` and
the "Open in Google Calendar" link) and in `config.js`; change all three together.

### Events on the page automatically (optional)

The site can list the calendar's upcoming events on the Calendar page itself, with times, and offer them as a
`calendar.ics` download. Visitors never contact Google; the pull happens when the site is published, every
morning. It works even while the calendar is private.

1. In Google Calendar, open the pack calendar's **Settings and sharing → Integrate calendar** and copy the
   **Secret address in iCal format**. Treat it like a password.
2. In this repository: **Settings → Secrets and variables → Actions → New repository secret**, named
   `CALENDAR_ICS_URL`, with that address. (Optional, on the **Variables** tab: `CALENDAR_TZ`, default
   `America/New_York`; `CALENDAR_SHOW_PLACES` = `true` to show each event's place.)
3. **Actions → Build and deploy → Run workflow**. Calendar changes then show up within a day.

What is used: each event's title, date, time and place only (places stay off unless `CALENDAR_SHOW_PLACES` is
`true`). A description stays on the calendar unless it starts with `Public:`, then the rest is shown, so a
phone number in the notes never leaks. Private and cancelled events are skipped. Repeating events (like every 1st
and 3rd Thursday) are expanded, including moved ones. Without the secret, or if Google can't be reached, the page
stays exactly as written in `docs/calendar.html`.

How it works: `scripts/sync_calendar.py` reads the feed into `events.generated.json`, then
`scripts/publish_events.py` fills the spot between the `events:start` and `events:end` comments in
`docs/calendar.html` and writes `docs/calendar.ics`. This happens on the workflow's own copy of the files, so
nothing is committed and the checks that run on pull requests see the page as written. The home page's "Coming Up"
list and its Event data stay hand-written, because they carry notes a calendar doesn't. Try it locally with
`python3 scripts/sync_calendar.py --file my.ics && python3 scripts/publish_events.py`, and run
`git checkout docs/calendar.html && rm docs/calendar.ics` afterwards.

## Checks

Run before pushing (Python 3, no installs needed):

```sh
python3 scripts/check_site.py
for f in docs/*.js; do node --check "$f"; done   # JavaScript syntax (needs Node)
```

`check_site.py` checks every page for broken internal links and images, missing alt text or image sizes,
invalid JSON-LD, missing titles/descriptions/canonical URLs, the skip link, nav and footer
links, sitemap coverage, "Page updated" dates, and files over 500 KB.

Three checks run on GitHub for every pull request (Actions tab → "Check site"), and again before every
deploy, so a push that fails any of them never reaches the live site:

| Job | What it catches |
| --- | --- |
| `check` | Everything above: links, images, metadata, nav, sitemap, security rules, JavaScript syntax. |
| `validate` | Invalid HTML, using the W3C Nu HTML Checker (the validator behind validator.w3.org). |
| `browser` | Opens every page in Chromium at 360px (phone) and 1280px (desktop): no sideways scroll, no serious accessibility problems (axe), nothing loaded from outside the site, no Content Security Policy errors. |

To run the pull-request date check locally: `BASE_SHA=origin/main python3 scripts/check_site.py`.
To run the other two locally you need Java (validator) or Node with Playwright and axe-core (browser check):

```sh
npm install --prefix /tmp/vnu vnu-jar@26.10.7
java -jar /tmp/vnu/node_modules/vnu-jar/build/dist/vnu.jar --errors-only --skip-non-html docs/*.html
node scripts/check_browser.js
```

Outside links (NCAC, Scouting America, forms) are checked on the 1st of each month
(Actions → "Check outside links", or run `python3 scripts/check_links.py`). Only links that
are clearly gone fail it; sites that block bots or time out are listed as warnings.

## Youth protection and photos

Follow Scouting America's Youth Protection and digital privacy guidelines:

- Only post photos of Scouts with written parent/guardian permission.
- Never publish a Scout's full name, school, or contact details alongside a photo.
- Adult leader names and contact details go on the site only with that leader's OK.

These rules are published for families on `privacy.html`.

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
