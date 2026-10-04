# Cub Scout Pack 1125 Website

Static website for **Cub Scout Pack 1125 — "Leaders and Trailblazers"**, Dumfries, Virginia.

No build step, no frameworks: pure HTML/CSS/JS served directly from `docs/`, ready for GitHub Pages.

## Structure

```
docs/
├── index.html      — home: hero, four pillars, quick info, coming up
├── about.html      — what Cub Scouting is, about the pack, leadership
├── join.html       — who can join, 3 steps, dues, uniform
├── dens.html       — Lion → Arrow of Light den cards
├── calendar.html   — Google Calendar embed + meeting rhythm
├── gallery.html    — photo placeholders (replace with real photos)
├── resources.html  — NCAC, ScoutBook, Scout Shop, training links
├── contact.html    — contact card
├── style.css       — full theme (navy/gold/forest/cream)
├── config.js       — single source of truth for pack facts + mobile nav
├── images/        — logo-pack1125.png (pack emblem) and rank badges,
│                     cropped from the official Pack 1125 flyer
└── README.md       — this file
```

## Branding

Colors are drawn from the official Pack 1125 flyer: deep navy, gold, red,
and forest green. The pack emblem and rank badges in `images/` are cropped
from the flyer artwork.

## Editing

- Pack facts live in `config.js` (`CONFIG` object). Some copy is also inline in the
  HTML pages — keep both in sync when facts change.
- Unknowns are marked as `<!-- TBD: ... -->` HTML comments in the pages.
- Colors and fonts are CSS variables at the top of `style.css`.

## Deploy with Claude Code

Paste this prompt to Claude Code:

"Deploy this static site to GitHub Pages: in the pack1125-site folder, create a new repo named pack1125-dumfries, push the docs/ folder to main, enable GitHub Pages from the /docs folder, and verify the live site loads. No build step — it's static HTML."
