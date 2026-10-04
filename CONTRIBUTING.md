# Contributing to the Pack 1125 Website

Every change goes through a **pull request (PR)**: you propose the change, the automatic
site check runs, someone reviews it, and once it's merged the live site updates in about a minute.
Nothing goes live until it's merged into `main`.

Live site: https://dmvthrowers.club/pack1125-dumfries/

## The quick way: edit in your browser

No software needed.

1. Open the file on GitHub. Pages live in `docs/`, for example
   [`docs/index.html`](docs/index.html) for the home page.
2. Click the **pencil icon** (Edit this file).
3. Make your change. Only change the words between the tags; leave the `<...>` parts alone.
4. Click **Commit changes…**, choose **"Create a new branch for this commit and start a pull
   request"**, give it a short name, and click **Propose changes**.
5. On the next screen, fill in the PR checklist and click **Create pull request**.
6. Wait for the **Check site** test to show a green check. A red X means something broke,
   like a typo in a link. Click **Details** to see what.
7. A reviewer approves it and clicks **Merge**. The site updates within a minute.

## Common changes

| To change… | Edit this file | Notes |
| --- | --- | --- |
| Coming Up events | `docs/index.html` | Also update `activities` in `docs/config.js` |
| Meeting times, place, dues | the page that shows them + `docs/config.js` | Home, Join, Calendar, FAQ, and Contact repeat some facts; search for the old text |
| Leaders | `docs/about.html` and `docs/contact.html` | Get the person's OK before listing them |
| FAQ answers | `docs/faq.html` | Each answer appears twice: visible, and in the JSON-LD at the top. Change both |
| Photos | send to admin@pack1125.org | Photos are resized and cleaned of location data before posting |

## Rules

- **Youth protection:** only post photos of Scouts with written parent/guardian permission.
  Never name a Scout or give their school or contact details. Don't attach photos to issues
  or PRs (this repository is public); email them instead.
- **Facts:** double-check dates, times, places, and costs. When something isn't decided,
  write "to be announced" rather than guessing.
- **One topic per PR** keeps reviews quick.

## Asking for a change without editing

Open an issue using the **Site update request** form (Issues → New issue) and describe what
should change. Someone with edit access will make the PR.

## For technical editors

```sh
python3 scripts/check_site.py                       # links, images, metadata, nav, sitemap
for f in docs/*.js; do node --check "$f"; done      # JavaScript syntax
cd docs && python3 -m http.server 8000              # preview at http://localhost:8000/
```

Work on a branch, open a PR against `main`, and keep `main` deployable. See the
[README](README.md) for site structure and conventions.
