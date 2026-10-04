# Security & Privacy Policy

This is the website for Cub Scout Pack 1125 (Dumfries, Virginia): a static site with no
logins, forms, databases, cookies, or analytics, served by GitHub Pages.

## Reporting a problem

Email **admin@pack1125.org** with a description and, if possible, the page address.
Please **don't** open a public GitHub issue for:

- a security problem with the site or this repository,
- a photo or detail that identifies a Scout and should come down,
- personal information that shouldn't be public.

We aim to reply within 3 days, and to remove any youth-identifying content as soon as we read
your message.

## What we do

- Every page has a strict Content Security Policy: no inline scripts or styles, and outside
  content limited to Google Fonts and the pack's Google Calendar.
- Every change goes through a pull request and an automated check (`scripts/check_site.py`)
  that enforces those rules, plus link, image, and accessibility checks.
- GitHub Actions are pinned to exact versions and kept current by Dependabot.
- Photos are resized and stripped of location and camera metadata before posting, and only
  posted with written parent/guardian permission. See [`docs/privacy.html`](docs/privacy.html).
- No secrets (passwords, API keys, tokens) belong in this repository. GitHub secret scanning
  and push protection watch for them.
