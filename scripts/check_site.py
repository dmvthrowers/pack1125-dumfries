#!/usr/bin/env python3
"""Static checks for the Pack 1125 site in docs/. No dependencies; run: python3 scripts/check_site.py

Checks every page for: broken internal links and image paths, missing alt text,
images without width/height, invalid JSON-LD, missing <title>/description/canonical,
a skip link, main#main-content, that every page is in sitemap.xml and the nav/footer,
and that the header, footer, and closing scripts are identical on every page.
Security: every page has the Content Security Policy and referrer meta tags, with no
'unsafe-inline', no inline styles or event handlers, no executable inline scripts,
and no plain-http:// links.
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
        self.csp = None; self.security = []   # security problems found while parsing
    def handle_starttag(self, tag, attrs):
        # HTMLParser lower-cases tag and attribute names and handles any quoting style,
        # so <SCRIPT>, ONCLICK= and single-quoted attributes are all caught.
        a = dict(attrs)
        self._security(tag, a)
        if "id" in a: self.ids.add(a["id"])
        for k in ("href", "src"):
            if k in a and tag != "iframe": self.refs.append(a[k])
        if "srcset" in a: self.refs += [p.split()[0] for p in a["srcset"].split(",")]
        if tag == "img": self.imgs.append(a)
        if tag == "script" and (a.get("type") or "").lower() == "application/ld+json": self._ld = True; self.ld.append("")
        if tag == "title": self.title = True
        if tag == "meta" and a.get("name"): self.meta[a["name"].lower()] = a.get("content", "")
        if tag == "link" and "rel" in a: self.links[a["rel"]] = a.get("href", "")
    def _security(self, tag, a):
        if tag == "meta" and (a.get("http-equiv") or "").lower() == "content-security-policy":
            self.csp = a.get("content") or ""
        if tag == "style": self.security.append("inline <style> block (blocked by CSP; use style.css)")
        for k, v in a.items():
            if k == "style": self.security.append(f"inline style on <{tag}> (blocked by CSP; use a class in style.css)")
            elif k.startswith("on"): self.security.append(f"inline event handler {k}= on <{tag}> (blocked by CSP; use a .js file)")
            elif k in ("href", "src", "action", "formaction") and v:
                scheme = v.strip().lower()
                if scheme.startswith("http:"): self.security.append(f"insecure http:// link: {v}")
                elif scheme.startswith("javascript:"): self.security.append(f"javascript: URL on <{tag}>")
        if tag == "script" and "src" not in a and (a.get("type") or "").lower() != "application/ld+json":
            self.security.append("inline <script> (blocked by CSP; use a .js file)")
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
    # --- security ---
    if p.csp is None: err("missing Content-Security-Policy meta tag")
    elif "unsafe-inline" in p.csp.lower() or "unsafe-eval" in p.csp.lower(): err("CSP allows unsafe-inline/unsafe-eval")
    if not p.meta.get("referrer"): err("missing referrer meta tag")
    for problem in p.security: err(problem)
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

# Consistency: header (logo, burger, menu), footer, and closing scripts must be identical on
# every page, ignoring which link is marked current and 404.html's absolute /pack1125-dumfries/ paths.
def shared_block(html, start, end):
    i = html.find(start); j = html.find(end, i)
    chunk = html[i:j + len(end)] if i >= 0 and j >= 0 else ""
    chunk = re.sub(r' (class="active"|aria-current="page")', "", chunk).replace(BASE, "")
    return re.sub(r"\s+", " ", chunk).strip()
reference = (DOCS / "about.html").read_text(encoding="utf-8")
for label, start, end in (("header", "<header", "</header>"), ("footer", "<footer", "</footer>"),
                          ("closing scripts", "</footer>", "</html>")):
    want = shared_block(reference, start, end)
    for page in pages:
        if shared_block(page.read_text(encoding="utf-8"), start, end) != want:
            errors.append(f"{page.name}: {label} differs from about.html (copy it from about.html)")

for f in DOCS.rglob("*"):
    if f.is_file() and f.stat().st_size > 500_000: errors.append(f"{f.relative_to(DOCS)}: {f.stat().st_size // 1024} KB (keep files under 500 KB)")

if errors:
    print(f"{len(errors)} problem(s):"); [print("  -", e) for e in errors]; sys.exit(1)
print(f"OK: {len(pages)} pages checked, no problems found.")
