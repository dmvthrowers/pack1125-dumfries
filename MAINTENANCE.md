# Pack 1125 Website — Maintenance & Handover

How the pack website works, who owns what, and what a new maintainer needs
to take it over. The live site is https://dmvthrowers.club/pack1125-dumfries/
(source: this repo, `dmvthrowers/pack1125-dumfries`).

## Hosting

- Static site, no server and no database. Pages live in `docs/` and deploy
  to GitHub Pages. The whole site is portable: anyone with repo access can
  redeploy it from this repo alone.
- GitHub Pages source: **GitHub Actions** (Settings > Pages > Build and
  deployment). Do not switch it to "Deploy from a branch" — the workflow
  runs the checks first, and a push that fails the checks never reaches the
  live site.
- `pack1125.org` is the pack's own domain but is NOT pointed at the site
  yet (it shows a registrar "Coming Soon" page). To point it at GitHub
  Pages: apex A records `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153`, plus a `www` CNAME to
  `dmvthrowers.github.io`. Domain manager: Neville Welch (Brandon Rogers
  was added as a domain manager in October 2026).

## Deploys

- The **Build and deploy** workflow runs on every push to `main`, daily at
  06:41 UTC, and on demand (Actions tab > "Run workflow"). It runs the
  `check-site` checks first (site rules, W3C HTML validation, real-browser
  checks at 360px and 1280px), then builds and deploys.
- The browser check uses Playwright 1.56.1, which cannot install Chromium
  on the `ubuntu-latest` (26.04) runner — the browser job is pinned to
  `ubuntu-24.04` in `.github/workflows/check-site.yml` for that reason.
  If the pin is ever removed, the check fails before any page is tested.
- Vercel is not involved. There is nothing to pay for: GitHub Pages on a
  public repo is free.

## Calendar

- The Calendar page pulls events from the pack's Google Calendar at build
  time (see `scripts/sync_calendar.py` and `scripts/publish_events.py`).
  It needs a repository secret named `CALENDAR_ICS_URL` holding the
  calendar's "Secret address in iCal format". Without the secret the step
  does nothing and the page shows its static content. The sync changes only
  that build's copy of the site; nothing is committed back.

## Photos

- Gallery photos live in `docs/images/gallery/` as JPG + WebP pairs, under
  500 KB each, with metadata stripped. Add new photos there and list them
  in `docs/gallery.html`.
- Policy (`docs/privacy.html`): photos of Scouts only with written
  permission from a parent or guardian; every child's face is blurred;
  never publish a Scout's full name, school, or contact details with a
  photo. Permission is collected with the
  [photo permission form](https://docs.google.com/forms/d/e/1FAIpQLSfLMYSqmwUZk10rP2-4-G3mQDKNnuH5hnJSFoZZWpIjUpX64g/viewform)
  (opt in / opt out / removal request, one form per Scout). Photo takedown
  requests also come in by email to `admin@pack1125.org`.

## Privacy rules (do not break these)

- The site is fully public. Never put roster info, phone numbers, a
  Scout's full name, or a child's unblurred face on it.
- Adult leaders' names and contact details appear only with that leader's OK.
- Advancement lives in Scoutbook Plus (https://advancements.scouting.org),
  never on this site. Only the contact alias `admin@pack1125.org` appears
  in site text; it forwards to the committee chair.

## Checks before merging a PR

- `python3 scripts/check_site.py` — every page in `sitemap.xml` and the
  nav/footer; each page's "Page updated" date matches its sitemap
  `<lastmod>`; a changed page needs a newer `<lastmod>`.
- `python3 scripts/check_links.py` — every external link must return 200.
- The browser job opens every page at 360px and 1280px (no sideways
  scroll, no serious accessibility problems, nothing loaded from outside
  the site, no CSP errors).
- Content edits are plain HTML in `docs/`; match the existing page
  structure (head, nav, footer) when adding a page.

## Handover checklist (when the maintainer changes)

1. Repo access: add the new maintainer as a collaborator with write access
   (Settings > Collaborators). Transfer or share ownership of the
   `dmvthrowers/pack1125-dumfries` repo if the pack is leaving the account.
2. GitHub Pages: confirm the new maintainer can see the Actions tab and the
   Pages settings. The deploy needs no secret except `CALENDAR_ICS_URL`.
3. Domain: hand over domain-manager access for `pack1125.org` (registrar
   account) or move it to the pack's own registrar account.
4. Google Calendar: hand over ownership of the pack calendar (or its
   `CALENDAR_ICS_URL` secret) so events keep syncing.
5. Photo permission form: transfer the Google Form to the new maintainer's
   account (or share it with the committee chair) so responses keep flowing.
6. Contacts: `admin@pack1125.org` must point at the current committee
   chair; update the alias and the leadership names on `about.html` and
   `contact.html`.

## Key contacts

- Cubmaster: Clive Vella — clivevella1@gmail.com
- Committee Chair: Andy Tainter — activcs@gmail.com (receives `admin@pack1125.org`)
- Chartered organization: Future Kings, Inc.
- Council: National Capital Area Council (NCAC), Prince William District
