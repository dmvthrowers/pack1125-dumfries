#!/usr/bin/env python3
"""Static checks for the Pack 1125 site in docs/. No dependencies; run: python3 scripts/check_site.py

Checks every page for: broken internal links and image paths, missing alt text,
images without width/height, invalid JSON-LD, missing <title>/description/canonical,
a skip link, main#main-content, and that every page is in sitemap.xml and the nav/footer.
Exits non-zero if anything fails.
"""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

DOCS = Path(__file__).resolve().parent.parent / "docs"
BASE = "/pack1125-dumfries/"          # GitHub Pages project path, used by 404.html
SITE = "https://dmvthrowers.club" + BASE
errors = []

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []; self.imgs = []; self.ids = set()
        self.ld = []; self._ld = False; self.title = False; self.meta = {}; self.links = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        for k in ("href", "src"):
            if k in a and tag != "iframe": self.refs.append(a[k])
        if "srcset" in a: self.refs += [p.split()[0] for p in a["srcset"].split(",")]
        if tag == "img": self.imgs.append(a)
        if tag == "script" and a.get("type") == "application/ld+json": self._ld = True; self.ld.append("")
        if tag == "title": self.title = True
        if tag == "meta" and "name" in a: self.meta[a["name"]] = a.get("content", "")
        if tag == "link" and "rel" in a: self.links[a["rel"]] = a.get("href", "")
    def handle_endtag(self, tag):
        if tag == "script": self._ld = False
    def handle_data(self, d):
        if self._ld: self.ld[-1] += d

pages = sorted(DOCS.glob("*.html"))
content_pages = [p for p in pages if p.name != "404.html"]
sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")

for page in pages:
    html = page.read_text(encoding="utf-8")
    p = Page(); p.feed(html); name = page.name
    err = lambda msg: errors.append(f"{name}: {msg}")
    if not p.title: err("missing <title>")
    if not p.meta.get("description"): err("missing meta description")
    if "main-content" not in p.ids: err('missing <main id="main-content">')
    if 'class="skip-link"' not in html: err("missing skip link")
    for block in p.ld:
        try: json.loads(block)
        except ValueError as e: err(f"invalid JSON-LD: {e}")
    for img in p.imgs:
        if "alt" not in img: err(f"img without alt: {img.get('src')}")
        if not (img.get("width") and img.get("height")): err(f"img without width/height: {img.get('src')}")
    for ref in p.refs:
        u = urlparse(ref)
        if u.scheme in ("http", "https", "mailto", "tel", "data") or ref.startswith("#"):
            continue
        path = unquote(u.path)
        if path.startswith(BASE): path = path[len(BASE):]
        elif path.startswith("/"): err(f"absolute path outside site: {ref}"); continue
        target = DOCS / (path or "index.html")
        if not target.exists(): err(f"broken link: {ref}")
        elif u.fragment and target.suffix == ".html" and target != page:
            if f'id="{u.fragment}"' not in target.read_text(encoding="utf-8"): err(f"missing anchor: {ref}")
        elif u.fragment and target == page and u.fragment not in p.ids: err(f"missing anchor: {ref}")
    if name != "404.html":
        canon = p.links.get("canonical", "")
        want = SITE if name == "index.html" else SITE + name
        if canon != want: err(f"canonical is {canon!r}, expected {want!r}")
        if f"<loc>{want}</loc>" not in sitemap: err("not listed in sitemap.xml")
    footer = html[html.find("<footer"):]
    for other in content_pages:
        if other.name not in ("privacy.html",) and f'href="{other.name}"' not in html.split("<main")[0] and name != "404.html":
            err(f"main nav missing {other.name}")
        if f'{other.name}"' not in footer: err(f"footer missing {other.name}")

for f in DOCS.rglob("*"):
    if f.is_file() and f.stat().st_size > 500_000: errors.append(f"{f.relative_to(DOCS)}: {f.stat().st_size // 1024} KB (keep files under 500 KB)")

if errors:
    print(f"{len(errors)} problem(s):"); [print("  -", e) for e in errors]; sys.exit(1)
print(f"OK: {len(pages)} pages checked, no problems found.")
