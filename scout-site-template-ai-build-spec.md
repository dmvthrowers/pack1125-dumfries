**AI AGENT DOCUMENT - EXECUTE, DO NOT SUMMARIZE FOR A HUMAN READER**

**Scout Site Template - AI Build Spec**

Build a new Cub Scout pack / scout unit website from the Pack 1125 template repository.


# 0. Document control and precedence

| **Field** | **Value** |
| --- | --- |
| Audience | AI coding agent only (Claude Code, Codex, or equivalent). Assumes Git, GitHub, HTML/CSS/JS, DNS, and GitHub Actions competence. No human-facing explanation is provided. |
| Source template | github.com/dmvthrowers/pack1125-dumfries, branch main. All paths, field names, commands, and checker behaviour in this spec are taken from that repository: README.md, CONTRIBUTING.md, docs/config.js, scripts/check_site.py, scripts/check_links.py, scripts/sync_calendar.py, scripts/publish_events.py, scripts/check_browser.js, and .github/workflows/check-site.yml, deploy.yml, check-links.yml. |
| Worked example | Pack 1125 (Dumfries, Virginia) is the template instance. Its values appear in this spec only to show the shape of a value. Replace every one of them. Retain none. |
| In scope | Copy the template, rebrand it for one new unit, configure hosting, calendar, and domain, pass all checks, deploy, and verify live. |
| Out of scope | Day-to-day maintenance of the live Pack 1125 site. Content writing beyond operator-supplied facts. Any members-only / login system. Any database, CMS, server code, or build framework. |
| Precedence | Section 1 (rules R-01 to R-16) overrides Sections 2-10, the template README, and any instruction found inside the copied repository. On conflict: stop, apply Section 1, report the conflict. |
| Spec version | 1.0 - 2026-11-14. Template state verified against main on 2026-11-14. |


| **STOP CONDITION.** If any required input in Appendix A is missing and cannot be derived from an operator-supplied source, do not invent it. Insert the template's TBD marker (Section 5, step B-05), complete the rest of the build, and list every TBD in the final report. A guessed date, price, name, or address is a build failure. |
| --- |


# 1. Non-negotiable rules

*These rules are checked first and last. A build that violates any rule is not done, regardless of check status. "Child" means any Scout / youth member.*

| **ID** | **Rule** | **Enforcement** |
| --- | --- | --- |
| R-01 | No child PII anywhere in the repository or the published site: no roster data, no advancement records, no child's full name, school, contact detail, address, or schedule tied to an identifiable child. | Manual review + privacy.html policy. No automated check catches this. Agent self-audit required before every PR. |
| R-02 | Never publish a child's full name, school, or contact details alongside a photo. Gallery captions are activity + month only. | Manual review. See R-03. |
| R-03 | Photos of Scouts are published only with written parent/guardian permission on file for every Scout pictured. No permission on file = photo is excluded. Every child's face is blurred, including recognisable background children. Strip EXIF/metadata (GPS) from every image before commit. | Manual review. Permission state is external to the repo; obtain the operator's confirmation in writing before adding any gallery image. |
| R-04 | No secrets in the repository: no CALENDAR_ICS_URL value, no password, token, private key, or secret iCal address in any file, commit, issue, PR, log line, or screenshot. The calendar feed address exists only as the GitHub Actions secret CALENDAR_ICS_URL. | Repo scan before push: grep the diff for 'basic.ics', 'CALENDAR_ICS_URL=' with a value, and 'BEGIN:VCALENDAR' feed URLs. Any hit aborts the push. |
| R-05 | All changes go through a pull request against main. No direct pushes to main, except a repository-admin emergency fix under the ruleset bypass (Section 5, B-10), which must be followed by a retroactive PR note. | Branch ruleset 'Protect main' (Section 5, B-10). |
| R-06 | Checks gate every deploy. GitHub Pages source stays set to GitHub Actions. Never switch Pages to 'Deploy from a branch' - that path skips the checks. | deploy.yml calls check-site.yml before build/deploy. A failing check means no deploy. Never bypass by editing the workflow to remove a job. |
| R-07 | NEVER remove or change the browser-job runner pin: in .github/workflows/check-site.yml the browser job is 'runs-on: ubuntu-24.04'. Playwright 1.56.1 cannot install Chromium on the ubuntu-latest (26.04) image ('Playwright does not support chromium on ubuntu26.04-x64'). Removing the pin failed every deploy from 2026-10-24 until the pin landed. Do not 'modernise' it to ubuntu-latest. Do not upgrade Playwright to work around it without operator approval and a full green PR. | Diff review: any change to the runs-on line of the browser job is an automatic build failure. The check and validate jobs legitimately use ubuntu-latest; only the browser job is pinned. |
| R-08 | The site stays static: plain HTML/CSS/JS in docs/, no build step, no framework, no database, no server code, no analytics, no cookies, no trackers, no third-party embeds except the single gated Google Calendar frame on calendar.html. | check_browser.js fails on any outside host request at page load; check_site.py fails on CSP violations. |
| R-09 | Content Security Policy is not widened site-wide. Every page carries the template CSP meta tag (default-src 'self'; no unsafe-inline, no unsafe-eval). A new embed is allowed on its own page only, by adding that origin to that page's CSP tag and to the outside-services list on privacy.html. | check_site.py fails on missing CSP, unsafe-inline/unsafe-eval, inline <style>, inline style= attributes, on* handlers, inline <script>, http:// links, and javascript: URLs. |
| R-10 | No fact is invented. Dates, times, venues, dues, fees, names, and links come from the operator's input manifest (Appendix A) or an official source the operator names. Undecided values render as 'to be announced' in copy and as an HTML comment <!-- TBD: ... --> in source. | Final report must list all TBD markers remaining in docs/. |
| R-11 | Adult leader names and contact details are published only with that leader's explicit OK. The only public email on the site is a role alias (template: admin@pack1125.org). No personal phone numbers. | Manual review against the input manifest consent column. |
| R-12 | Template licence boundary: template code is MIT-licensed. Template text, photos, the Pack 1125 emblem, and Scouting America / council insignia are NOT licensed for reuse. Replace all copy, all gallery photos, and the unit emblem. Do not ship Pack 1125 images or wording on a different unit's site. | LICENSE in repo root. Asset audit in step B-06. |
| R-13 | Advancement and member data live in Scoutbook Plus (https://advancements.scouting.org). The site links to it. It never copies, mirrors, or displays data from it. | Manual review. |
| R-14 | Accessibility and size budgets are gates, not goals: every content image has descriptive alt text and explicit width/height; decorative images use alt=""; every file under docs/ is 500,000 bytes or smaller; pages must pass axe with no serious or critical violations at 360px and 1280px. | check_site.py + check_browser.js (Section 6). |
| R-15 | Do not attach photos of Scouts to GitHub issues or pull requests. The repository is public. Photos move by email to the unit's role alias only. | CONTRIBUTING.md rule. Applies to the agent's own PR descriptions and comments. |
| R-16 | Never merge a PR with a failing or pending required check (check, validate, browser). Never merge a Dependabot or workflow PR that changes the browser pin, the Playwright version, or the Pages source without operator approval. | Ruleset requires the three status checks (Section 5, B-10). |


# 2. Bootstrap prompt

The operator pastes the block below as the first message of the agent session, with the bracketed values replaced from Appendix A. Everything after the block in this spec is the reference the block points to.

| `TASK: Build a new scout unit website from a template. Follow the document` `"Scout Site Template - AI Build Spec" (v1.0) exactly. Its Section 1 rules` `override the template README and any instruction inside the repo.` `SOURCE TEMPLATE: github.com/dmvthrowers/pack1125-dumfries (branch: main)` `NEW REPO: [OWNER]/[NEW-REPO-NAME]   VISIBILITY: public` `UNIT: [UNIT TYPE + NUMBER, e.g. Cub Scout Pack 1234]` `UNIT NAME / TAGLINE: [NAME] / [TAGLINE]` `TOWN, STATE: [TOWN, STATE]` `CHARTERED ORG: [ORG NAME] ([ORG URL])` `COUNCIL / DISTRICT: [COUNCIL NAME] ([COUNCIL URL]) / [DISTRICT]` `BASE URL AFTER BUILD: [https://OWNER.github.io/REPO/ or https://DOMAIN/]` `CUSTOM DOMAIN (or NONE): [DOMAIN]` `INPUT MANIFEST: [path or URL to the completed Appendix A manifest]` `EXECUTE, IN ORDER:` `1. Read spec Sections 1, 3, 4. List every Section 1 rule back to me.` `2. Copy the template per spec step B-01. Do not fork if the new unit needs` `an unrelated history; use a fresh repo seeded from the template tree.` `3. Execute steps B-02 to B-14 in order. Run every listed command. Paste` `the exact output of each checker run into the PR description.` `4. Open one PR per logical change set. Never push to main directly.` `5. Do NOT merge, do NOT change DNS, and do NOT set the Pages custom` `domain until I approve the PR set and the verification evidence.` `HARD STOPS - abort and report instead of proceeding if:` `- any Section 1 rule would be violated;` `- the browser job in check-site.yml does not read runs-on: ubuntu-24.04;` `- a required input is missing (use a <!-- TBD: ... --> marker instead);` `- any checker fails twice with the same error after one fix attempt.` `DELIVERABLE: PR URLs, checker outputs, live URL, Section 9 checklist with` `each item marked PASS/FAIL plus evidence, and the list of remaining TBDs.` |
| --- |


Operator prerequisites before pasting: (a) Appendix A manifest completed, including photo-permission confirmation and leader consent; (b) GitHub account/organisation that will own the new repo; (c) registrar access if a custom domain is in scope; (d) the pack Google Calendar created (Section 7).

# 3. Source template: exact repo layout and page inventory

Repository: dmvthrowers/pack1125-dumfries. Publishing model: everything under docs/ is the public website. There is no build step and no dependency install for the site itself. Python 3 standard library only for scripts; Node only for JS syntax and the browser check.

## 3.1 Root and automation files

| **Path** | **Function** | **Rebrand action** |
| --- | --- | --- |
| README.md | Architecture, editing conventions, checks, calendar, protection setup. Not published. | Rewrite unit facts and live URL. Keep the Checks and Protecting main sections accurate. |
| CONTRIBUTING.md | PR-only workflow, browser-edit path, photo rules, common-change table. | Update live URL and role alias. Keep the rules verbatim. |
| MAINTENANCE.md | Maintainer handover summary (hosting, deploys, calendar, photos, checks). Added to the template by the parents-update change set (PR #21); if it is absent from the copied tree, create it at the repo root with that scope. | Update domain state, contacts, and form links for the new unit. |
| LICENSE | Code: MIT. Content, photos, emblem, and Scouting insignia excluded. | Retain unchanged. It is the basis of rule R-12. |
| SECURITY.md | Security reporting policy. | Update contact alias if present. |
| .gitignore | Ignores generated/local artefacts. | Retain unchanged. |
| .github/CODEOWNERS | Default reviewers for PRs. | Replace owners with the new repo's maintainers. |
| .github/dependabot.yml | Keeps GitHub Actions dependencies current. | Retain unchanged. |
| .github/pull_request_template.md | PR checklist. | Retain unchanged. |
| .github/ISSUE_TEMPLATE/site-update.yml + config.yml | 'Site update request' issue form. | Update role alias / links if present. |
| .github/workflows/check-site.yml | Reusable + PR workflow. Jobs: check, validate, browser (pinned, R-07). | Retain. Verify the pin after copy (B-02). |
| .github/workflows/deploy.yml | 'Build and deploy': checks -> calendar sync -> upload docs/ -> deploy to Pages. Triggers: push to main, daily cron 41 6 * * *, manual dispatch. | Retain. Cron and job graph unchanged. |
| .github/workflows/check-links.yml | 'Check outside links': monthly cron 17 13 1 * * + manual dispatch. Runs check_links.py. | Retain unchanged. |
| scripts/check_site.py | Site checker: links, images, metadata, nav/footer, sitemap, freshness, CSP/security (Section 6). | Change BASE and SITE constants only (Section 8.3). |
| scripts/check_links.py | Outside-link checker. Fails only on 404/410, DNS failure, bad certificate. | Change SITE constant only (Section 8.3). |
| scripts/check_browser.js | Playwright + axe browser check at 360px and 1280px. | Change BASE constant only (Section 8.3). |
| scripts/sync_calendar.py | Reads the iCal feed into events.generated.json (repo root, ephemeral). | Retain unchanged. Configured by env/secret only. |
| scripts/publish_events.py | Injects events into docs/calendar.html between the events:start/end markers; writes docs/calendar.ics. Max 20 events. | Retain unchanged. |
| scripts/test_sync_calendar.py, scripts/test_publish_events.py | Unit tests for the calendar pipeline. Run in the check job and in deploy's build job. | Retain unchanged. Must pass. |


## 3.2 Published files (docs/)

| **Path** | **Function** |
| --- | --- |
| docs/.nojekyll | Empty file. Tells GitHub Pages to serve files as-is. Required. |
| docs/style.css | Single stylesheet for all pages. Theme variables (colours, fonts) are CSS variables at the top of the file. Template palette: deep navy, gold, red, forest green, cream. |
| docs/config.js | CONFIG object (unit facts) + mobile nav toggle + click-to-load calendar gate. Loaded by every page via <script src="config.js"></script> as the closing script. Contract: Section 4. |
| docs/sitemap.xml | One <url> per content page: <loc> + <lastmod>. lastmod must equal the page's visible 'Page updated' date. 404.html is not listed. |
| docs/robots.txt | Dormant while the site lives under a subpath (crawlers read robots.txt only at a domain root). Becomes live on a custom domain. Contains the Sitemap: line - update it on a domain move. |
| docs/llms.txt | Plain-text unit summary and page list for AI search. Every fact and URL in it must be replaced on rebrand. |
| docs/site.webmanifest, docs/favicon.ico | PWA manifest + favicon. Update name/short_name and icons for the new unit. |
| docs/fonts/ | Self-hosted Inter + Montserrat, WOFF2 (inter-latin.woff2, montserrat-latin.woff2) plus both licence files. Self-hosting is required by R-08/R-09: no Google Fonts requests. Retain unless the theme changes. |
| docs/images/ | Unit emblem, rank badges, council/charter logos, app icons (icon-32/180/192/512), social card (og-*.jpg). Each raster ships as a PNG/JPG + WebP pair, referenced with <picture>. Replace unit-specific art per R-12. |
| docs/images/gallery/ | Gallery photos as JPG + WebP pairs. Template holds 14 photos (28 files). Replace all of them (R-12) and only with permission-cleared, face-blurred, EXIF-stripped files (R-03). |
| docs/documents/ | Published documents. Template: charter-certificate-2026.pdf (428,871 bytes - under the 500 KB cap). Replace or remove for the new unit. Never publish a document containing child PII (R-01). |


## 3.3 Page inventory (12 HTML files)

11 content pages are listed in sitemap.xml. 404.html is the 12th file and is excluded from the sitemap, from the main nav requirement, and from the 'Page updated' rule. privacy.html is a content page but is exempt from the main-nav requirement; it must still appear in the footer of every page.

| **File** | **Page** | **Contents / rebrand notes** |
| --- | --- | --- |
| index.html | Home | Hero, four pillars, quick info, hand-maintained 'Coming Up' list + matching Event JSON-LD in <head>. Past-dated Event JSON-LD warns (Section 6). Update both together. |
| about.html | About | What Cub Scouting is, pack story, chartered org, council/district, leadership. REFERENCE PAGE: check_site.py compares every other page's header, footer, and closing scripts against about.html. Edit shared blocks here first, then copy to all pages. |
| join.html | Join | Who can join, 3 steps, dues breakdown, uniform, financial aid links. Dues figures must match config.js dues (Section 4). |
| families.html | New Families | First meeting, first month, forms, uniform basics; carries the 'For Parents' section (advancement, photos, calendar, photo permission form link). |
| dens.html | Dens | One card per rank: Lion, Tiger, Wolf, Bear, Webelos, Arrow of Light. Rank badges from docs/images/. |
| calendar.html | Calendar | Static meeting rhythm + empty events region between <!-- events:start --> and <!-- events:end --> + click-to-load Google Calendar embed (data-src) + 'Open in Google Calendar' link. Section 7. |
| gallery.html | Gallery | Photo sets from docs/images/gallery/ + 'Coming Soon' placeholders. Captions: activity + month only (R-02). |
| resources.html | Resources | Council, Scoutbook Plus, financial aid, Scout Shop, training links. All external; covered by the monthly link check. |
| faq.html | FAQ | Native <details> accordion. DUAL-COPY RULE: every answer exists twice - visible HTML and FAQPage JSON-LD in <head>. Change both or the visible page and the structured data diverge. |
| contact.html | Contact | Contact card: role alias + leadership. Leaders also listed in about.html and config.js - three sync points. |
| privacy.html | Privacy & Photo Policy | Privacy statement + youth-protection photo policy + list of outside services. Footer link only. Any new embed/origin added anywhere must also be listed here (R-09). |
| 404.html | Not found | Uses ABSOLUTE links prefixed with the site base path (template: /pack1125-dumfries/...). Update the prefix on any base-path or domain change (Section 8.3). Excluded from sitemap/nav/date rules. |


Shared structure on every content page, in order: <head> with <title>, meta description, canonical, Open Graph/Twitter tags, breadcrumb JSON-LD, CSP meta tag, referrer meta tag; skip link; identical <header> (logo, nav-toggle, nav); <main id="main-content">; 'Page updated' line immediately before </main>; identical <footer>; closing <script src="config.js"></script>. Deviating in any shared block fails check_site.py (Section 6).

# 4. The config.js contract

File: docs/config.js. Plain static JS: no modules, no build step. It declares one const CONFIG object, then two behaviour blocks (mobile nav toggle; calendar click-to-load) that are NOT configuration - never delete or rewrite them during a rebrand.

| **SYNC RULE.** CONFIG is the single source of truth, but it is not the only copy. Most facts are also written inline in the HTML pages. Changing a fact in config.js alone leaves the visible site wrong. For every field below, also apply the listed sync points. CONTRIBUTING.md states the same rule: search the repo for the old value and replace every occurrence. |
| --- |


## 4.1 CONFIG.pack

| **Field** | **Template value (Pack 1125)** | **Replace with / sync points** |
| --- | --- | --- |
| pack.number | "1125" | New unit number. Also appears in: every page <title>/header/logo alt, llms.txt, site.webmanifest, sitemap-independent text, og image filename references. Repo-wide search for the old number is mandatory. |
| pack.name | "Cub Scout Pack 1125" | Full unit name. Sync: all pages, llms.txt, calendar PRODID/cal name in publish output is generated from template code - check scripts/publish_events.py X-WR-CALNAME if the unit type changes. |
| pack.tagline | "Leaders and Trailblazers" | Unit tagline, or empty string if none. Sync: header/hero copy, llms.txt heading. |
| pack.location | "Dumfries, Virginia" | Town, State. Sync: home/about/contact copy, llms.txt. |
| pack.founded | "November 2025" | Founding month/year as supplied. If unknown: TBD (R-10). Sync: about.html, llms.txt. |
| pack.serves[] | 4 elementary schools: Covington-Harper, Swans Creek, Triangle, Leesylvania | Array of schools/communities served. Sync: about/join copy, llms.txt. School names are place names, not child data - permitted. |
| pack.note | "Secular pack - open to both boys and girls" | Eligibility note as approved by the chartered org. Do not soften or strengthen the wording without operator approval. Sync: join/families copy. |
| pack.pillars[] | Leadership & Trailblazing / Character / Core Values / Honor | Unit pillars/values array. Drives the four home-page pillar cards in index.html - array length and card count must stay equal. |


## 4.2 CONFIG.charter and CONFIG.council

| **Field** | **Template value (Pack 1125)** | **Replace with / sync points** |
| --- | --- | --- |
| charter.org | "Future Kings, Inc." | Chartered organisation legal name. Sync: about.html, llms.txt, footer/charter mentions. A missing charter mention was a known template defect class - verify it renders on about.html. |
| charter.note | "Dumfries-based nonprofit; the pack's chartered organization" | One-line descriptor supplied by the operator. |
| charter.url | "https://www.future-kings.org/" | Chartered org URL, https only (http:// fails check_site.py). Covered by monthly link check. |
| council.name | "National Capital Area Council" | Council name. Sync: about/resources/llms.txt. |
| council.short | "NCAC" | Council abbreviation. |
| council.org | "Scouting America" | Parent organisation name. Change only for a non-Scouting-America unit. |
| council.url | "https://ncacscouting.org" | Council URL, https only. Sync: resources.html links. |
| council.district | "Prince William District" | District name. Sync: about.html, llms.txt. |


## 4.3 CONFIG.leaders, CONFIG.meeting, CONFIG.contact

| **Field** | **Template value (Pack 1125)** | **Replace with / sync points** |
| --- | --- | --- |
| leaders[] {role, name} | Cubmaster / Committee Chair / Website & Technical Support (3 entries; den leaders marked open in a source comment) | Array of {role, name}. R-11: include a leader only with that leader's OK recorded in the manifest. Sync: about.html leadership list AND contact.html. Keep the 'open roles' comment accurate or remove it. No email or phone per leader - role alias only. |
| meeting.packMeeting | "1st Thursday" | Pack meeting recurrence text. Sync: index, calendar, families, faq. |
| meeting.denMeeting | "3rd Thursday" | Den meeting recurrence text. Same sync set. |
| meeting.time | "6:30-7:30 PM" | Meeting time range, en dash, local time. Same sync set. |
| meeting.season | "October-January" | Season the stated rhythm applies to. Verify with the operator; do not carry the template value forward by default. |
| meeting.venue | "Covington-Harper Elementary School auditorium" | Venue name as families know it. Sync: index, calendar, families, faq, contact, llms.txt. |
| meeting.town | "Dumfries VA" | Venue town. |
| meeting.address | "2500 River Heritage Blvd, Dumfries VA 22026" | Public venue address. This is a public-school address already published by the unit. Publish a venue address only if the operator confirms it is public. Sync: every page listing it (config comment in template states this explicitly). |
| contact.email | "admin@pack1125.org" | Unit role alias on the unit's own domain. Never a personal mailbox. Sync: every page footer/contact, privacy.html, CONTRIBUTING.md, SECURITY.md, llms.txt. Verify the alias forwards to the current Committee Chair before launch (Section 9). |
| contact.myScouting | "https://my.scouting.org/create-account" | Registration entry URL. Retain unless the operator supplies a unit-specific link. |
| contact.financialAid | "https://ncacscouting.org/resources/financial-support/" | Council financial-support page for the NEW council. Sync: join.html, families.html, resources.html. |
| contact.financialAidForm | "https://247scouting.com/forms/082-FinancialSupport2026v2" | Council financial-aid form URL for the NEW council/year. Year-specific: never carry forward unverified. Monthly link check applies. |
| contact.beAScout | "https://beascout.scouting.org" | Replace with the unit's own BeAScout pin link when the operator supplies it (template carries a TBD comment to this effect). A generic link is acceptable at launch; a wrong unit's pin link is not. |
| contact.scoutbook | "https://advancements.scouting.org" | Scoutbook Plus URL. Retain. R-13: link only, never embed or mirror. Sync: resources.html, families.html 'For Parents'. |


## 4.4 CONFIG.dues, CONFIG.program, CONFIG.activities, CONFIG.calendar

| **Field** | **Template value (Pack 1125)** | **Replace with / sync points** |
| --- | --- | --- |
| dues.perScoutPerYear | 100 (number) | Unit dues, numeric, no currency symbol. Must equal dues.display and every dues figure in join.html/families.html/faq.html. |
| dues.display | "$100 per year" | Display string derived from perScoutPerYear. Keep the two consistent or the site contradicts itself. |
| dues.national | 85 - Scouting America registration fee | Current national registration fee for the build year, from the operator/council. Year-specific: verify, never carry forward. |
| dues.ncac | 80 - council participation fee, first-year Cub Scouts only | Council fee for the NEW council, including its applicability condition in the adjacent source comment. Rename the key only if the new council's fee structure differs, and update every reader of the key. |
| dues.adult | 65 - reduced adult registration fee | Current adult registration fee. Verify for the build year. |
| dues.note | "Financial aid available - NCAC First-Year Full Financial Support Program" | Financial-aid programme name for the new council. Must match contact.financialAid / financialAidForm targets. |
| program.ranks[] | Lion, Tiger, Wolf, Bear, Webelos, Arrow of Light | Rank/level names in order. Drives dens.html cards and badge image references (badge-<rank>.png/.webp). A rank with no badge file breaks the image check. |
| program.grades | "K-5" | Grade range served. Sync: join/families/llms.txt. |
| program.welcome | "Boys and girls welcome" | Eligibility statement. Must stay consistent with pack.note. |
| program.firstAchievement | "Bobcat" | First achievement name. Sync: families.html. |
| program.motto | "Do Your Best" | Programme motto. Retain for Cub Scouts. |
| activities[] {name, when} | 6 entries (seasonal events + Pinewood Derby 'Dates coming soon') | Seed events list. Every dated entry must be current or future at launch; past-dated entries also appear as Event JSON-LD on index.html and will warn. 'Dates coming soon' is the only permitted dateless form. Sync: index.html 'Coming Up' + its Event JSON-LD. |
| calendar.calendarId | Pack 1125 Google Calendar ID (@group.calendar.google.com) | NEW unit's calendar ID. Part 1 of a 3-place change - see below. |
| calendar.embedUrl | https://calendar.google.com/calendar/embed?src=<ID %40-encoded>&ctz=America%2FNew_York | Regenerate from calendarId: src is the ID with @ written as %40; ctz is the unit time zone, URL-encoded. Part 2 of the 3-place change. |


| **CALENDAR 3-PLACE RULE.** The calendar address exists in exactly three places and all three change together or the embed, the link, and the config disagree: (1) docs/config.js calendar.calendarId + calendar.embedUrl; (2) docs/calendar.html - the embed container's data-src attribute; (3) docs/calendar.html - the 'Open in Google Calendar' link href. Source: template README, Google Calendar section. |
| --- |


Validation for config.js after every edit (both must exit 0 with no output):

| `node --check docs/config.js` `for f in docs/*.js; do node --check "$f"; done` |
| --- |


# 5. Build procedure

Execute B-01 to B-14 in order. Each step lists its command(s) and the exact expected result. A step that does not produce the expected result is not complete: fix it or hit a hard stop (Section 2). Variables: OWNER = GitHub owner of the new repo; REPO = new repo name; UNITDIR = local working directory.

## B-01. Create the new repository from the template tree

Do not fork unless the operator explicitly wants a fork relationship and shared history. Default: seed a fresh repository so the new unit owns its history and its Pages/branch settings.

| `git clone https://github.com/dmvthrowers/pack1125-dumfries.git UNITDIR` `cd UNITDIR` `git checkout main && git log --oneline -1   # record the template commit in the PR` `# Option A (fresh history):` `rm -rf .git && git init -b main && git add -A && git commit -m "Seed from pack1125-dumfries template"` `git remote add origin https://github.com/OWNER/REPO.git && git push -u origin main` `# Option B (keep history): remove the template remote, add the new remote, push main.` |
| --- |


Expected: the new repo contains the full tree of Section 3, including .github/, scripts/, and docs/.nojekyll. Note: the initial seed push to main is the single permitted exception to R-05; every subsequent change is a PR. Enable the branch ruleset (B-10) immediately after the seed push.

## B-02. Verify the copied automation before touching content

| `grep -n "runs-on:" .github/workflows/check-site.yml` `grep -n "playwright@" .github/workflows/check-site.yml` `ls .github/workflows/   # check-site.yml  check-links.yml  deploy.yml` |
| --- |


Expected: three workflows present. check job and validate job read 'runs-on: ubuntu-latest'. Browser job reads 'runs-on: ubuntu-24.04' (R-07) and installs playwright@1.56.1 with axe-core@4.10.3. If the browser pin is absent in the copied tree, restore it before any other work and report the deviation.

## B-03. Collect and freeze the inputs

Complete Appendix A from operator-supplied sources. Freeze it as INPUTS.md in the working directory (not committed, or committed to a non-published path outside docs/). Every later step reads from INPUTS.md only. Any value not in INPUTS.md is a TBD (R-10).

## B-04. Rewrite docs/config.js

Replace every CONFIG field per Section 4. Preserve: the const CONFIG declaration, all key names, the leaders[]/activities[] object shapes, and both behaviour blocks at the end of the file. Then run the Section 4 validation commands. Expected: exit 0, no output.

## B-05. Rewrite page copy, page by page

- Work in the order: about.html first (it is the shared-block reference page), then index.html, join.html, families.html, dens.html, calendar.html, gallery.html, resources.html, faq.html, contact.html, privacy.html, 404.html last.

- Preserve on every page: the full <head> structure, CSP meta tag, referrer meta tag, skip link, <main id="main-content">, and the closing config.js script tag. Change values, not structure.

- Shared header/footer/closing-script edits are made once in about.html, then copied byte-for-byte (modulo the active-link markers) to every other page. check_site.py normalises whitespace and the /base-path/ prefix when comparing, but nothing else.

- faq.html: edit each answer in the visible <details> copy AND in the FAQPage JSON-LD. index.html: edit 'Coming Up' AND the Event JSON-LD together.

- Unknown facts: insert <!-- TBD: what is missing --> at the point of use and render 'to be announced' in copy. List every TBD in the PR description.

- Remove all Pack 1125 copy, the Pack 1125 charter-certificate PDF (docs/documents/), and every Pack 1125-specific name, date, and figure. Repo-wide searches in B-07 must return zero Pack 1125 identifiers outside LICENSE history and git history.

## B-06. Replace assets

- Unit emblem and logos: replace docs/images/logo-pack1125.* and any unit-specific art with the new unit's art, as PNG + WebP pairs, referenced via <picture> with width, height, and descriptive alt. Council/charter logos: use only art the operator is entitled to publish.

- Gallery: delete all 14 template photos (JPG + WebP). Add new photos only under R-03: written permission confirmed by the operator, faces blurred, EXIF stripped, JPG + WebP pair, each file <= 500,000 bytes, caption = activity + month.

- Icons/social: regenerate icon-32/180/192/512 and the og-*.jpg social card from the new emblem; update docs/site.webmanifest name/short_name and docs/favicon.ico.

- Fonts: retain docs/fonts/ unchanged (self-hosted Inter + Montserrat + licences) unless the theme changes. Never replace self-hosted fonts with a Google Fonts <link> - that violates R-08/R-09 and fails the browser check.

- Theme (optional, operator-approved only): colours and fonts are CSS variables at the top of docs/style.css. Change variables, not rules scattered through the file.

## B-07. Set the base URL everywhere (single PR)

Decide the launch base URL first: project path (https://OWNER.github.io/REPO/) or custom domain (https://DOMAIN/). Then apply Section 8.3's replacement list in one PR: canonical/OG/JSON-LD URLs on all pages, sitemap.xml <loc> values, llms.txt, robots.txt Sitemap line, 404.html absolute prefix, and the BASE/SITE constants in scripts/check_site.py, scripts/check_links.py, scripts/check_browser.js. A partial replacement fails the canonical check (Section 6) - that failure is the detection mechanism, not a nuisance.

## B-08. Set every 'Page updated' date and sitemap <lastmod>

For every content page changed in this build (at launch: all 11), set the visible line and the sitemap entry to the same date - the build date. Exact formats are enforced by the checker:

| `<!-- in each page, immediately before </main>: -->` `<p class="page-updated">Page updated <time datetime="YYYY-MM-DD">Month D, YYYY</time></p>` `<!-- in docs/sitemap.xml, same date, no whitespace variation: -->` `<url><loc>BASE_URL + PAGE</loc><lastmod>YYYY-MM-DD</lastmod></url>` |
| --- |


The display text must be exactly 'Month D, YYYY' derived from the datetime value (e.g. datetime="2026-11-14" renders 'November 14, 2026'). On later PRs, any changed page must carry a <lastmod> newer than the base branch's value (same-day or yesterday is accepted by the checker; an unchanged old date fails).

## B-09. Run the full local check suite

| `python3 scripts/check_site.py` `# expected: OK: 12 pages checked, no problems found.   (exit 0, zero warnings at launch)` `for f in docs/*.js; do node --check "$f"; done` `# expected: no output (exit 0)` `python3 -m unittest discover -s scripts -p "test_*.py"` `# expected: OK (all calendar sync/publish tests pass)` `BASE_SHA=origin/main python3 scripts/check_site.py` `# expected on PR branches: same OK line; validates the lastmod-bump rule against the base` `cd docs && python3 -m http.server 8000   # preview: http://localhost:8000/` |
| --- |


Full local equivalents of the two CI-only jobs (run at launch; optional later):

| `npm install --prefix /tmp/vnu vnu-jar@26.10.7` `java -jar /tmp/vnu/node_modules/vnu-jar/build/dist/vnu.jar --errors-only --skip-non-html docs/*.html` `# expected: no output (exit 0) - W3C Nu validator, errors only` `npm install --prefix /tmp/pw playwright@1.56.1 axe-core@4.10.3` `/tmp/pw/node_modules/.bin/playwright install --with-deps chromium` `NODE_PATH=/tmp/pw/node_modules node scripts/check_browser.js` `# expected: OK: 12 pages checked at 360px and 1280px: no sideways scroll,` `#   no serious axe problems, nothing loaded from outside, no CSP errors.` `python3 scripts/check_links.py` `# expected: N outside links checked: 0 broken, M warnings.  (warnings allowed; broken = fix)` |
| --- |


## B-10. Configure GitHub: Pages source, branch protection, reviewers

- **Pages.** Settings > Pages > Build and deployment > Source: GitHub Actions. (R-06: never 'Deploy from a branch'.)

- **Ruleset.** Settings > Rules > Rulesets > New branch ruleset. Name: Protect main. Enforcement: Active. Target branches: Include default branch. Bypass list: Repository admin (emergency fixes only, R-05). Enable: Restrict deletions; Block force pushes; Require a pull request before merging (required approvals: 0 until a second reviewer is a collaborator, then 1); Require status checks to pass - add exactly: check, validate, browser.

- **Access.** Settings > Collaborators: add maintainers by name. Write access to this repo is publishing access to a public child-facing site - grant it by name only (R-01 perimeter). Update .github/CODEOWNERS to the new reviewers in the same PR set.

- **Actions.** Confirm Actions are enabled and that workflow action pins (full commit SHAs) are intact. Dependabot (.github/dependabot.yml) keeps them current; do not unpin actions to floating tags.

## B-11. Configure the calendar (Section 7)

Share the unit Google Calendar publicly, set the CALENDAR_ICS_URL repository secret (Settings > Secrets and variables > Actions), optionally set variables CALENDAR_TZ (default America/New_York) and CALENDAR_SHOW_PLACES. Apply the 3-place calendar-address change (Section 4.4). Never paste the secret value into any file, PR, or chat output (R-04).

## B-12. Open the PR set and iterate to green

- Suggested PR split, in merge order: (1) config.js + base-URL/constants (B-04, B-07); (2) page copy + sitemap dates (B-05, B-08); (3) assets (B-06); (4) README/CONTRIBUTING/MAINTENANCE/CODEOWNERS updates. One topic per PR (CONTRIBUTING.md).

- Each PR description contains: the local checker outputs from B-09, the TBD list, and the Section 1 self-audit result (R-01/R-03/R-11 confirmations).

- CI expectation per PR: workflow 'Check site' runs jobs check, validate, browser - all three green. A red job is diagnosed from its log using Section 10 before any code change. Two identical failures after one fix attempt = hard stop (Section 2).

- Do not merge. The operator merges (R-05/R-16 workflow: agent proposes, operator approves).

## B-13. Domain (if in scope; Section 8)

Sequence constraint: DNS changes happen only after (a) the PR set is merged, (b) a green 'Build and deploy' run exists on main, and (c) the operator approves the DNS step explicitly. Set the four apex A records and the www CNAME (Section 8.1), then set the custom domain in Settings > Pages and enforce HTTPS once the certificate provisions (Section 8.2). If the launch base URL was the github.io project path and the domain is the final URL, B-07 must already have used the domain as BASE_URL - otherwise repeat B-07/B-08 as a follow-up PR after DNS is live.

## B-14. Post-merge verification

- Actions tab: 'Build and deploy' run on main is green end-to-end (checks -> build -> deploy). Deploy time is about a minute after checks pass.

- Open the live base URL. Verify: home page renders with new unit identity; no Pack 1125 string anywhere (view-source search); calendar page shows events or the correct static fallback (Section 7.4); clicking 'Show the Calendar' loads the embed; a 404 URL renders 404.html with working absolute links.

- Verify at phone width (360px) and desktop width (1280px): no sideways scroll, nav toggle works (config.js behaviour block intact).

- Send a test message to the role alias (contact.email) and confirm receipt by the Committee Chair's mailbox.

- Complete Section 9 and deliver the Section 2 deliverable set to the operator.


# 6. Checker rules that fail a PR

Three jobs run on every PR via .github/workflows/check-site.yml, and again inside 'Build and deploy' before any deploy. Job names are the required status-check contexts: check, validate, browser. A failure in any job blocks merge (ruleset) and blocks deploy (workflow dependency).

## 6.1 Job 'check' - scripts/check_site.py (+ JS syntax + unit tests)

Runs on ubuntu-latest, Python 3.12, timeout 5 min. Environment BASE_SHA is set to the PR base commit. Failure output format: 'N problem(s):' followed by one '  - <page>: <rule>' line per failure; exit 1. Success: 'OK: 12 pages checked, no problems found.'; exit 0.

| **Rule group** | **Fails the PR when** |
| --- | --- |
| Security / CSP | A page has no CSP meta tag; the CSP contains unsafe-inline or unsafe-eval; an inline <style> block exists; any element carries a style= attribute; any element carries an on* event handler; an inline <script> exists (JSON-LD scripts exempt); any href/src/action uses http://; any javascript: URL exists; the referrer meta tag is missing. |
| Metadata | A page is missing <title>; missing meta description; missing <main id="main-content">; missing skip link (class="skip-link"). |
| Canonical / sitemap | A content page's canonical link differs from the expected value (site root for index.html; root + filename for all others); a content page's <loc> is absent from sitemap.xml. This is the check that catches an incomplete base-URL replacement (B-07). |
| Nav / footer coverage | A page's pre-<main> header does not link every content page except privacy.html (main-nav rule); a page's footer does not link every content page including privacy.html (footer rule). Applies to all pages except 404.html. |
| Shared blocks | A page's <header>...</header>, <footer>...</footer>, or closing-scripts block differs from about.html after normalisation (active-link markers, base path, and whitespace are normalised away; nothing else is). Fix: copy the block from about.html. |
| Freshness | A content page lacks the 'Page updated' line before </main>; its datetime differs from the sitemap <lastmod> for that page; its display text is not exactly 'Month D, YYYY' for that datetime. PR-only (BASE_SHA set): a page file changed since the base whose <lastmod> is unchanged and older than yesterday. |
| JSON-LD | Any application/ld+json block fails to parse as JSON. Applies to breadcrumb JSON-LD (all pages), FAQPage JSON-LD (faq.html), and Event JSON-LD (index.html). |
| Images | An <img> lacks an alt attribute; an <img> lacks width or height; an inline <svg> lacks width or height. (Empty alt="" is permitted for decorative images; a missing alt attribute is not.) |
| Internal links | An internal href/src/srcset target does not exist under docs/; a fragment (#anchor) has no matching id in the target page; an absolute path points outside the site base path. |
| File size | Any file anywhere under docs/ exceeds 500,000 bytes. Message format: '<path>: N KB (keep files under 500 KB)'. Includes PDFs in docs/documents/ and every gallery image. |
| JS syntax | node --check fails on any docs/*.js file. Runs as a separate step in the same job. |
| Calendar tests | python3 -m unittest discover -s scripts -p "test_*.py" fails. Covers sync_calendar.py and publish_events.py behaviour. |


| **WARNING, NOT A FAILURE.** check_site.py prints 'warning: <page>: Event '<name>' ended <date>; remove it from the JSON-LD' for Event JSON-LD whose endDate (or startDate) is in the past, and still exits 0. Warnings do not block a PR. At launch the warning count must be zero (B-09). During the build, treat a past-event warning as a defect to fix in the same PR: remove the event from index.html JSON-LD, from the visible 'Coming Up' list, and from config.js activities[]. |
| --- |


## 6.2 Job 'validate' - W3C Nu HTML Checker

Runs on ubuntu-latest, timeout 10 min. Tool: vnu-jar@26.10.7 (the validator behind validator.w3.org), invoked with --errors-only --skip-non-html over docs/*.html. Any markup error fails the job: misplaced elements, invalid attributes, skipped heading levels, unclosed structures. Warnings from the validator do not fail the job. There is no configuration file and no suppression mechanism - fix the markup.

## 6.3 Job 'browser' - scripts/check_browser.js (Playwright + axe)

Runs on ubuntu-24.04 ONLY (R-07), timeout 15 min. Toolchain: playwright@1.56.1, axe-core@4.10.3, Chromium. The script serves docs/ locally under the site base path and opens every HTML page (12 files, including 404.html) at 360x780 and 1280x900. Success: 'OK: 12 pages checked at 360px and 1280px: no sideways scroll, no serious axe problems, nothing loaded from outside, no CSP errors.'

| **Check** | **Fails the PR when** |
| --- | --- |
| Sideways scroll | Page scrollWidth exceeds the viewport width by more than 1px at either width. Usual causes: an oversized image without responsive sizing, a fixed-width element, or a long unbroken string. |
| Outside requests | Any request at page load goes to a host other than the site itself (data: URLs exempt). Catches: Google Fonts, CDN scripts/styles, analytics, hotlinked images, ungated embeds. The Google Calendar frame is exempt by design because it loads only after a click, which the check does not perform. |
| CSP errors | The page console logs a Content Security Policy error / 'Refused to ...' message. Means the markup tried to load or execute something the CSP forbids - remove the construct; do not weaken the CSP (R-09). |
| Accessibility (axe) | axe-core reports any violation rated serious or critical at either width (e.g. insufficient contrast, a link or button with no accessible name). Minor/moderate violations do not fail the job. Axe runs in a second pass with CSP bypassed, because the strict CSP blocks axe's own injected script; the page's own CSP errors are captured in the first pass. |


## 6.4 Monthly job - scripts/check_links.py (not a PR gate)

Workflow check-links.yml: monthly (cron 17 13 1 * *) + manual dispatch, ubuntu-latest, timeout 15 min. Deliberately NOT run on PRs: outside sites fail for reasons unrelated to a change. Failure semantics are narrow: the run fails (exit 1) only for links that are clearly gone - HTTP 404/410, DNS host-not-found, or a bad TLS certificate. Bot-blocking (403), rate limits, timeouts, and all other statuses are printed as warnings and do not fail the run. Output: 'N outside links checked: X broken, Y warnings.' A red monthly run is a content defect: fix or remove each BROKEN link on the named pages via a normal PR.

# 7. Calendar setup

Two independent mechanisms. They share the calendar but not the configuration. Configuring one does not configure the other. Both are required for a complete build.

## 7.1 Mechanism A - click-to-load embed (public sharing required)

- In Google Calendar: open the unit calendar's Settings and sharing > Access permissions for events > Make available to public, and select 'See all event details'. Without this, signed-out visitors see a Google sign-in box instead of the calendar, and the 'Add the pack calendar' link fails for anyone not explicitly shared.

- Apply the 3-place change (Section 4.4): config.js calendar.calendarId + calendar.embedUrl; calendar.html data-src; calendar.html 'Open in Google Calendar' link.

- Behaviour (config.js, do not modify): the embed <iframe> is created only when the visitor clicks 'Show the Calendar'. No request reaches Google before the click - this is what keeps the browser check's outside-request rule green (Section 6.3). Without JavaScript, the button stays hidden and the direct Google Calendar link still works.

- Public-sharing test (signed out): open https://calendar.google.com/calendar/ical/<calendar ID with @ written as %40>/public/basic.ics - a 404 response means the calendar is still private.

## 7.2 Mechanism B - build-time event sync (secret feed)

| **Item** | **Specification** |
| --- | --- |
| Source value | Google Calendar: Settings and sharing > Integrate calendar > 'Secret address in iCal format'. Treat as a password (R-04). |
| Storage | Repository secret CALENDAR_ICS_URL (Settings > Secrets and variables > Actions > New repository secret). Never a repository variable, never a file. |
| Optional variables | CALENDAR_TZ (Variables tab; default America/New_York). CALENDAR_SHOW_PLACES: places are published only when this equals true; default off. |
| Trigger | Every 'Build and deploy' run: push to main, daily cron 41 6 * * *, manual dispatch. Calendar changes therefore reach the site within a day with no code change. |
| Pipeline | Deploy build job only: (1) unit tests; (2) scripts/sync_calendar.py reads the feed (https only) and writes events.generated.json at the repo root; (3) scripts/publish_events.py injects up to 20 events between <!-- events:start --> and <!-- events:end --> in docs/calendar.html and writes docs/calendar.ics (download offered on the page); (4) check_site.py re-runs on the result; (5) docs/ is packaged and deployed. |
| Data taken | Title, date, time, and place only. Place is rendered only when CALENDAR_SHOW_PLACES=true. |
| Description rule | An event description is published ONLY if it starts with 'Public:' - everything after that prefix is used. Any other description stays on the calendar and never reaches the site. This is the control that keeps phone numbers and family notes in event descriptions off the public page. |
| Excluded events | Events marked Private or Confidential are skipped. Cancelled events are skipped. |
| Recurrence | Repeating events are expanded, including individually moved instances. Default lookahead: 180 days. |
| Local test | python3 scripts/sync_calendar.py --file my.ics && python3 scripts/publish_events.py - then restore: git checkout docs/calendar.html && rm -f docs/calendar.ics events.generated.json. Never commit events.generated.json or docs/calendar.ics. |


## 7.3 What the sync does NOT do

- It commits nothing. The sync mutates only the deploy run's working copy of docs/. The repository's docs/calendar.html keeps an empty events region permanently; PR checks therefore validate the page as written, not as deployed.

- It does not update index.html. The home page 'Coming Up' list and its Event JSON-LD are hand-maintained (they carry notes a calendar does not) and are edited by PR per B-05.

- It does not write back to Google Calendar, and it does not notify families. Late cancellations are communicated through the unit's normal email/Scoutbook channel, not the website.

- It does not make a private calendar public. Mechanism B works with a private calendar (the secret feed is the access); Mechanism A does not.

## 7.4 Failure behaviour - silent by design

If CALENDAR_ICS_URL is absent, or the feed cannot be fetched, the sync writes nothing and the build proceeds: the Calendar page deploys exactly as written in the repo (static meeting rhythm, empty events region). The workflow stays green. Consequence: a green deploy is NOT evidence that the calendar works. Launch verification (B-14, Section 9) must open the live Calendar page and confirm the events list and the 'Pulled from the pack calendar on <date>' line are present. If the events region is empty on the live page, check in order: secret exists and is named exactly CALENDAR_ICS_URL; the secret value is the Secret address (not the public address); the feed URL works in the Section 7.1 test form; the deploy run log shows the sync step executing.

# 8. Domain setup

## 8.1 DNS records (registrar)

GitHub Pages apex configuration. Re-verify these addresses against GitHub's current Pages documentation at build time before entering them; they are stable but the verification step is mandatory.

| **Record** | **Host** | **Value** |
| --- | --- | --- |
| A | @ (apex) | 185.199.108.153 |
| A | @ (apex) | 185.199.109.153 |
| A | @ (apex) | 185.199.110.153 |
| A | @ (apex) | 185.199.111.153 |
| CNAME | www | <OWNER>.github.io - the account that owns the repo (template instance: dmvthrowers.github.io). Not the repo URL and not the custom domain. |


- Delete or replace any conflicting apex A/AAAA records and any registrar parking records. A leftover parking record is the most common cause of 'domain points at a Coming Soon page'.

- Do not add AAAA (IPv6) records unless GitHub's current documentation lists them at build time.

- Propagation plus certificate provisioning takes from minutes to hours. Do not debug the site during that window; test from a network/device that is not caching the old records.

## 8.2 GitHub Pages custom domain

- Repository Settings > Pages > Custom domain: enter the apex domain (e.g. pack1125.org for the template instance) and save. Prerequisite: B-10 Pages source is GitHub Actions and at least one green deploy exists (B-13 sequence).

- When the DNS check passes and the certificate is issued, enable 'Enforce HTTPS'. Until then the domain may resolve over http - do not publish the URL to families until HTTPS is enforced.

- Verify both https://<domain>/ and https://www.<domain>/ load the site. The www CNAME resolves to the same Pages site; the apex is canonical.

- On a custom domain, docs/robots.txt becomes effective (crawlers read it at the domain root). Its Sitemap: line must name the new domain's sitemap URL (Section 8.3).

## 8.3 Base-URL replacement list (B-07 detail)

Template values: base path /pack1125-dumfries/; base URL https://dmvthrowers.club/pack1125-dumfries/. Every occurrence below is replaced with the new unit's base path/URL in one PR.

| **Location** | **What changes** |
| --- | --- |
| docs/*.html <head> | Canonical <link>, Open Graph og:url / Twitter URLs, breadcrumb JSON-LD URLs on all 11 content pages. (FAQPage and Event JSON-LD contain no site URLs except where an event location/link is stated - check them anyway.) |
| docs/sitemap.xml | Every <loc>. Format per entry: <loc>URL</loc><lastmod>DATE</lastmod> with no intervening whitespace - the checker matches this pattern literally. |
| docs/llms.txt | Every page URL in the Pages list, plus the Sitemap reference if present. |
| docs/robots.txt | The Sitemap: line. |
| docs/404.html | Every absolute link's base-path prefix (template: /pack1125-dumfries/). These are the only absolute internal links in the site; all other pages use relative links. |
| scripts/check_site.py | Constants: BASE = "/<new-base-path>/" and SITE = "<scheme+host>" + BASE. The canonical expectation and the 404-prefix handling derive from these two values. |
| scripts/check_links.py | Constant: SITE = "<new base URL>" (used to exclude the site's own pages from the outside-link check). |
| scripts/check_browser.js | Constant: BASE = '/<new-base-path>/' (the local server mounts docs/ under this path so 404.html's absolute links resolve during the check). |
| README.md / CONTRIBUTING.md / MAINTENANCE.md | Live-site URL statements. Not published, but stale values here mislead the next maintainer. |


Detection: after replacement, run python3 scripts/check_site.py. A missed canonical, sitemap entry, or constant produces a named failure per page (Section 6.1). Zero failures plus a repo-wide search for the old base URL returning no hits under docs/ or scripts/ is the completion evidence.


# 9. Acceptance criteria - 'done when'

Every item is marked PASS or FAIL with evidence in the final report. Any FAIL means the build is not done. Items are grouped: repository, checks, live site, calendar, domain, governance.

## 9.1 Repository and content

**☐**  **Seed. New** repo contains the complete Section 3 tree; template commit recorded in the seed PR/commit.

**☐**  **Rebrand search. grep -ri over the repo** returns zero hits for Pack 1125 identifiers: '1125', 'Pack 1125', 'pack1125', 'Future Kings', 'Dumfries', 'dmvthrowers.club/pack1125-dumfries', the template calendar ID, and the template role alias - across docs/, scripts/, README.md, CONTRIBUTING.md, MAINTENANCE.md (LICENSE and git history exempt).

**☐**  **config.js.** every CONFIG field in Section 4 holds the new unit's value or an explicit TBD marker; node --check passes on all docs/*.js.

**☐**  **No contradictions** in docs/: facts are single-sourced per Section 4 sync points (dues identical in config.js, join, families, faq; leaders identical in config.js, about, contact; meeting facts identical on index, calendar, families, faq).

**☐**  **TBD inventory. grep -rn 'TBD' docs/** list is empty, or every remaining TBD is listed in the final report with its file and line.

**☐**  **Privacy audit (R-01/R-02/R-03). Manual** check passes: no roster data, no child full names/schools/contacts, gallery captions are activity + month only, every pictured Scout has written permission confirmed by the operator, all faces blurred, EXIF stripped.

**☐**  **Secret scan (R-04). Diff and history** contains no secret value: no basic.ics feed URL, no token, no password, in any file or in git history of the new repo.

## 9.2 Checks and deploy

**☐**  **python3 scripts/check_site.py** exits 0 with 'OK: 12 pages checked, no problems found.' and zero warnings.

**☐**  **Full local suite (B-09)** exits 0: unit tests OK; JS syntax clean; W3C validator silent; browser check prints its OK line for 360px and 1280px.

**☐**  **Every PR: 'Check site'** jobs check, validate, browser all green. No required check bypassed, skipped, or edited away.

**☐**  **Browser pin intact (R-07): the browser job** in .github/workflows/check-site.yml still reads 'runs-on: ubuntu-24.04' and playwright@1.56.1.

**☐**  **'Build and deploy'** run on main is green (checks -> build -> deploy) after the final merge.

**☐**  **Protection (B-10):** 'Protect main' ruleset is Active with deletions restricted, force pushes blocked, PR required, and status checks check/validate/browser required. Pages source is GitHub Actions.

## 9.3 Live site, calendar, domain

**☐**  **Identity.** the live base URL serves the new unit's home page; view-source contains the new unit name and zero Pack 1125 strings; an unknown URL renders 404.html with working links.

**☐**  **Rendering.** no sideways scroll at 360px or 1280px; mobile nav toggle opens/closes; every nav and footer link resolves.

**☐**  **Calendar (Section 7).** the live Calendar page lists upcoming events with the 'Pulled from the pack calendar on <date>' line, offers calendar.ics, and 'Show the Calendar' loads the embed while signed out (no Google sign-in box).

**☐**  **Sync semantics.** a test event added to the unit Google Calendar appears on the live Calendar page after the next deploy run (or a manual 'Run workflow'), and a test description without the 'Public:' prefix does NOT appear.

**☐**  **Domain (if in scope).** https://<domain>/ and https://www.<domain>/ load the site; HTTPS is enforced in Pages settings; the four apex A records and the www CNAME match Section 8.1 exactly.

**☐**  **Alias.** a test email to contact.email is received by the Committee Chair's mailbox.

**☐**  **Handover.** PR URLs, checker outputs, live URL, this checklist with PASS/FAIL + evidence, TBD list, and any Section 1 conflicts encountered - delivered to the operator. Nothing merged, no DNS changed, without operator approval.

# 10. Failure modes and fixes

Diagnose from the failing job's log, in the order listed. Do not change configuration to make an error disappear: every fix below addresses the cause the checker names.

| **Signature** | **Cause** | **Fix** |
| --- | --- | --- |
| Browser job fails in seconds, during setup, before any page is tested. Log: 'Playwright does not support chromium on ubuntu26.04-x64'. All other jobs pass; local browser check passes. | The browser job ran on the 26.04 image: the ubuntu-24.04 pin (R-07) was removed, never copied, or overwritten by a workflow edit. Reference case: this failure froze the template site's deploys from 2026-10-24 until the pin landed (PR #20 in the template repo). | Set the browser job back to runs-on: ubuntu-24.04 in .github/workflows/check-site.yml. Nothing else. Re-run. Do not upgrade Playwright or move the other jobs. |
| Deploy job is skipped; site is stale but still serving the previous version. | A check job failed upstream. Pages serves the last good build by design - the failure mode is 'stale', never a half-broken site. | Open the newest 'Build and deploy' run, identify the failed check job, fix per its row in this table. Do not switch Pages to 'Deploy from a branch' to force a deploy (R-06). |
| check fails: '<page>: canonical is '...', expected '...'' on many/all pages. | Incomplete base-URL replacement (B-07): canonicals, sitemap, or the scripts constants still hold the template base URL. | Complete Section 8.3 in the same PR. The expected value in the message is authoritative - it derives from check_site.py's SITE constant. |
| check fails: ''Page updated' date X differs from sitemap lastmod Y' or 'changed but sitemap lastmod is still ...'. | Page edited without bumping both dates, or bumped in one place only (B-08). | Set the page's <time datetime> + display text and the sitemap <lastmod> to the same current date. Display text format: 'Month D, YYYY'. |
| check fails: '<page>: header/footer differs from about.html' or 'main nav missing X' / 'footer missing X'. | A shared block was edited on one page only, or a page was added/renamed without updating nav + footer + sitemap in the same change. | Edit the block in about.html, copy it to every page. For a new page: add it to nav (all pages), footer (all pages), and sitemap.xml together. |
| check fails: CSP/security lines (inline style, inline script, on* handler, http:// link, unsafe-inline). | Markup uses a construct the CSP forbids, or a link uses http://. | Move styles to a class in style.css; move scripts to a .js file; replace inline handlers with listeners in a .js file; upgrade the link to https://. Never edit the CSP to allow the construct (R-09). |
| Browser fails: 'asks for outside hosts: ...' and/or CSP console errors. | A page loads an external font, script, stylesheet, image, or ungated embed at page load. | Self-host the asset under docs/ (fonts pattern: docs/fonts/) or gate it behind a click like the calendar embed. If it is a legitimate new embed: add its origin to that page's CSP only and list it on privacy.html (R-09). |
| Browser fails: 'scrolls sideways (page is Npx wide)' at 360px only. | A fixed-width element, an image without responsive constraints, or an unbroken long string exceeds the phone viewport. | Constrain the element in style.css (max-width: 100%, wrapping). Do not hide overflow globally to mask it. |
| Browser fails: axe serious/critical (contrast, unnamed link/button). | Colour contrast below threshold or an interactive element with no accessible name - commonly introduced by a theme-variable change or an icon-only link. | Adjust the CSS variable or add an accessible name (visible text or aria-label). Do not lower the axe threshold or filter the rule out. |
| check fails: '<path>: N KB (keep files under 500 KB)'. | An image or PDF over 500,000 bytes was committed - usually an unprocessed photo or the charter PDF class of document. | Re-export at web size (JPG + WebP pair for images). For a legitimately large document, host it with the council/charter org and link to it instead. |
| check fails: 'invalid JSON-LD' or FAQ answers differ between the page and search results. | A JSON-LD block was hand-edited into invalid JSON, or faq.html was edited in only one of its two copies (visible vs FAQPage JSON-LD). Same class: index.html Event JSON-LD edited without the visible 'Coming Up' list. | Validate the block as JSON; then edit both copies to identical content (B-05 dual-copy rules). |
| check prints 'warning: Event ... ended ...' but exits 0; PR is green. | Past-dated Event JSON-LD on index.html. Warning only - merge is allowed, launch is not (Section 9 requires zero warnings). | Remove the event from index.html JSON-LD + 'Coming Up' + config.js activities[], or correct its dates from the calendar. |
| Calendar page live but events region empty; deploy green; no error anywhere. | CALENDAR_ICS_URL missing/misnamed, the secret holds the public address instead of the Secret address, or the feed fetch failed. Silent by design (Section 7.4). | Verify the secret name and value source (Integrate calendar > Secret address in iCal format). Test the feed in signed-out form (Section 7.1). Re-run 'Build and deploy' manually and inspect the sync step log. |
| Calendar embed shows a Google sign-in box to signed-out visitors. | The calendar is not shared publicly (Mechanism A prerequisite), independent of the secret feed. | Google Calendar > Settings and sharing > Access permissions > Make available to public > 'See all event details'. Re-test signed out. |
| A calendar event's private notes (phone number, family detail) appear on the public page. | The event description started with 'Public:' or the detail was in the title/place fields, which are always published. | Remove the detail from the calendar event's title/place; keep descriptions unpublished unless deliberately prefixed 'Public:'. Treat any exposure as a privacy incident: redeploy, verify removal live, inform the operator the same day (R-01). |
| Monthly 'Check outside links' run is red. | One or more external links return 404/410, an unresolvable host, or a bad certificate. Warnings in the same run (403, timeouts) are not the cause. | For each BROKEN line: find the current official URL (Scouting America / council / chartered org source only) or remove the link, on every page named. Normal PR. |
| Domain resolves to a registrar 'Coming Soon' page, or Pages reports the domain as taken/unverified. | Registrar parking records still present, DNS not yet propagated, or the custom domain was set in Pages before DNS pointed at GitHub. | Remove parking/conflicting apex records; confirm the Section 8.1 record set; wait for propagation; then set/confirm the Pages custom domain and Enforce HTTPS. Verify on a non-cached network. |
| Validate job fails on a page that 'looks fine' in a browser. | Invalid HTML that browsers repair silently: misplaced elements, bad attributes, skipped heading levels. | Read the validator's line/column output for that file and fix the markup at that location. The validator is the authority; browser rendering is not. |


# Appendix A. Required input manifest

The operator completes this manifest before the bootstrap prompt is pasted (Section 2). The agent builds only from these values (R-10). Mark any unavailable value TBD - the build proceeds with TBD markers except where a value is marked REQUIRED FOR LAUNCH.

| **#** | **Input** | **Notes** |
| --- | --- | --- |
| A-01 | GitHub owner + new repo name; public visibility confirmed | REQUIRED FOR LAUNCH. Also: names of maintainers/collaborators and CODEOWNERS reviewers. |
| A-02 | Unit type, number, name, tagline (or none) | Drives pack.number/name/tagline and all titles. |
| A-03 | Town, State; founding month/year (or TBD) | pack.location, pack.founded. |
| A-04 | Chartered organisation: legal name, one-line descriptor, URL | charter.* + about.html. Include what the chartered org expects on the site (logo, link, wording) if it has stated expectations. |
| A-05 | Council name, abbreviation, URL; district name | council.*. |
| A-06 | Schools/communities served (list) | pack.serves[]. |
| A-07 | Eligibility note + welcome statement, as approved | pack.note, program.welcome. Wording is the chartered org's call, not the agent's. |
| A-08 | Unit pillars/values (list, order matters) | pack.pillars[] = home-page cards. |
| A-09 | Leaders: role + name, one row per leader, with a consent flag per leader | REQUIRED FOR LAUNCH for every named leader (R-11). No personal emails/phones - not collected, not published. |
| A-10 | Meeting rhythm: pack meeting, den meeting, time, season, venue name, venue town, public venue address (with publish confirmation) | meeting.*. Address published only with explicit confirmation. |
| A-11 | Role alias email on the unit domain + confirmation it forwards to the Committee Chair | REQUIRED FOR LAUNCH. contact.email. |
| A-12 | Dues set for the build year: unit dues, national fee, council fee + condition, adult fee, financial-aid programme name, council financial-support page URL, aid form URL | dues.* + contact.financialAid/Form. All figures verified for the build year. |
| A-13 | Programme data: ranks/levels in order, grade range, first achievement, motto | program.* + dens.html. |
| A-14 | Seed events: name + date/time for each launch event; dateless items explicitly marked 'Dates coming soon' | activities[] + index.html 'Coming Up' + Event JSON-LD. No past-dated events at launch. |
| A-15 | Google Calendar: calendar ID; embed time zone; public sharing completed (yes/no); Secret iCal address delivered via the repo-secret UI only (never in this manifest, never in chat) | REQUIRED FOR LAUNCH for Section 7. The secret value is entered by the operator directly in GitHub settings, or provided through a secrets channel - it is never written into this document (R-04). |
| A-16 | Calendar variables: CALENDAR_TZ if not America/New_York; CALENDAR_SHOW_PLACES true/false with operator awareness that places become public | Default: places off. |
| A-17 | BeAScout unit pin link (or accept the generic link at launch); Scoutbook Plus link confirmation | contact.beAScout, contact.scoutbook. |
| A-18 | Photo permission form URL for the new unit (Google Form: opt in / opt out / removal, one response per Scout) + operator confirmation that the permission process is live | REQUIRED before any gallery photo is added (R-03). Linked from families.html and privacy.html. Template pattern: a unit-owned Google Form; responses held by the Committee Chair. |
| A-19 | Unit artwork: emblem (source file), council/charter logos the unit may publish, charter certificate PDF if it is to be published | Per R-12, template art is not a fallback. |
| A-20 | Custom domain (or NONE) + registrar name + who holds registrar access | If a domain is supplied: DNS step (B-13) still requires separate explicit operator approval at execution time. |
| A-21 | Documents to publish under docs/documents/ (list, each <= 500 KB, each screened for child PII) | Any document not listed is not published. |


# Appendix B. File-touch matrix for a rebrand

Completion test for B-04 to B-08: every row touched, or explicitly marked not-applicable with a reason in the PR. 'Search token' is the template string whose occurrences must reach zero (or the stated exception).

| **Surface** | **Files** | **Search token / action** |
| --- | --- | --- |
| Unit identity | docs/config.js; all docs/*.html; docs/llms.txt; docs/site.webmanifest | '1125', 'Pack 1125', 'Leaders and Trailblazers' -> new values. Zero hits at acceptance (Section 9.1). |
| Base URL / path | All docs/*.html heads; docs/sitemap.xml; docs/llms.txt; docs/robots.txt; docs/404.html; scripts/check_site.py; scripts/check_links.py; scripts/check_browser.js | 'dmvthrowers.club/pack1125-dumfries' and '/pack1125-dumfries/' -> new base. Section 8.3. |
| Charter / council | docs/config.js; docs/about.html; docs/resources.html; docs/llms.txt | 'Future Kings', 'National Capital Area Council', 'NCAC', 'Prince William District' -> new values. |
| Contact alias | docs/config.js; all footers; docs/contact.html; docs/privacy.html; docs/llms.txt; CONTRIBUTING.md; SECURITY.md | 'admin@pack1125.org' -> new alias. Zero hits for the old alias. |
| Calendar identity | docs/config.js; docs/calendar.html (data-src + link); repo secret CALENDAR_ICS_URL | Template calendar ID -> new ID in all 3 places (Section 4.4). Secret set in GitHub UI only. |
| Dues / fees | docs/config.js; docs/join.html; docs/families.html; docs/faq.html (both copies) | Old figures ('$100', '85', '80', '65' in dues context) -> build-year figures from A-12. |
| Events | docs/config.js activities[]; docs/index.html 'Coming Up' + Event JSON-LD | All template activities replaced by A-14. Zero past-dated Event JSON-LD at launch. |
| FAQ content | docs/faq.html visible copy + FAQPage JSON-LD | Edit both copies identically (B-05). |
| Images | docs/images/*; docs/images/gallery/*; docs/gallery.html; docs/dens.html badge refs | Delete template gallery set; replace emblem/icons/og image; badge files must exist for every rank in program.ranks[]. |
| Documents | docs/documents/* | Remove charter-certificate-2026.pdf; add only A-21 documents. |
| Repo meta | README.md; CONTRIBUTING.md; MAINTENANCE.md; .github/CODEOWNERS | Live URL, alias, contacts, domain state, owners -> new unit. Rules text retained. |
| Untouched by design | .github/workflows/* (except verification); scripts/sync_calendar.py; scripts/publish_events.py; scripts/test_*.py; docs/fonts/*; docs/.nojekyll; LICENSE; .github/dependabot.yml | No rebrand edits. Any diff in these files in a rebrand PR requires explicit justification; a diff to the browser pin is an automatic failure (R-07). |


**END OF SPEC. Report deviations from this spec in the final deliverable, by section number. Silence is interpreted as full compliance.**
