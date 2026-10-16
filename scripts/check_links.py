#!/usr/bin/env python3
"""Check every outside link on the Pack 1125 site. No dependencies; run: python3 scripts/check_links.py

Only links that are clearly gone fail the run: 404/410, a host name that no longer exists,
or a bad certificate. Sites that block bots, rate-limit, or time out are listed as warnings.
Runs monthly on GitHub (Actions → "Check outside links"); not on pull requests, because
outside sites can be down for reasons that have nothing to do with a change.
"""
import socket, ssl, sys, urllib.error, urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"
UA = "Mozilla/5.0 (compatible; Pack1125-link-check; +https://github.com/dmvthrowers/pack1125-dumfries)"
GONE = {404, 410}

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = set()
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src", "data-src") and v and v.startswith(("http://", "https://")):
                self.urls.add(v)

def fetch(url):
    """Return (status, problem): problem is None if fine, 'fail' if gone, 'warn' otherwise."""
    for method in ("HEAD", "GET"):   # some servers reject HEAD; retry with GET
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, None
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code not in GONE: continue
            return e.code, "fail" if e.code in GONE else "warn"
        except urllib.error.URLError as e:
            reason = e.reason
            if isinstance(reason, socket.gaierror): return "host not found", "fail"
            if isinstance(reason, ssl.SSLCertVerificationError): return "bad certificate", "fail"
            return str(reason), "warn"
        except (TimeoutError, socket.timeout): return "timed out", "warn"
        except Exception as e: return f"{type(e).__name__}: {e}", "warn"

def main():
    where = defaultdict(set)
    for page in sorted(DOCS.glob("*.html")):
        p = Links(); p.feed(page.read_text(encoding="utf-8"))
        for u in p.urls: where[u].add(page.name)
    fails, warns = [], []
    for url in sorted(where):
        status, problem = fetch(url)
        line = f"{url} -> {status} (on {', '.join(sorted(where[url]))})"
        if problem == "fail": fails.append(line)
        elif problem == "warn": warns.append(line)
    for w in warns: print("warning:", w)
    for f in fails: print("BROKEN:", f)
    print(f"{len(where)} outside links checked: {len(fails)} broken, {len(warns)} warnings.")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
