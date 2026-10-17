#!/usr/bin/env node
// Browser checks for every page in docs/, at a 360px phone and a 1280px desktop.
//
//   node scripts/check_browser.js     # needs Node, Playwright with Chromium, and axe-core (see check-site.yml)
//
// Fails on any page that:
//   - scrolls sideways (page wider than the screen),
//   - has an accessibility problem axe rates "serious" or "critical" (low contrast, a link or button with no name...),
//   - asks for anything outside this site (the site loads no outside fonts, scripts or trackers; the Google Calendar
//     frame only loads after a click, so nothing counts as outside on page load), or
//   - logs a Content Security Policy error (a blocked style, script or image).
// The site is served under /pack1125-dumfries/ like the live address, so 404.html's absolute links work.
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');
const axeSource = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

const BASE = '/pack1125-dumfries/';
const root = path.resolve(process.argv[2] || path.join(__dirname, '..', 'docs'));
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.xml': 'text/xml',
  '.txt': 'text/plain', '.woff2': 'font/woff2', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json', '.pdf': 'application/pdf' };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (p.startsWith(BASE)) p = p.slice(BASE.length - 1);
  let file = path.join(root, p);
  if (!file.startsWith(root)) { res.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!fs.existsSync(file)) { res.writeHead(404, { 'Content-Type': 'text/plain' }).end('not found'); return; }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

const pages = fs.readdirSync(root).filter(f => f.endsWith('.html')).sort();
const VIEWS = [{ name: '360px', width: 360, height: 780 }, { name: '1280px', width: 1280, height: 900 }];

(async () => {
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const origin = `http://127.0.0.1:${server.address().port}`;
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const failures = [];
  for (const view of VIEWS) {
    // bypassCSP only lets axe inject its script; the CSP check below reads the page's own console errors first.
    const ctx = await browser.newContext({ viewport: { width: view.width, height: view.height }, bypassCSP: false });
    for (const name of pages) {
      const page = await ctx.newPage();
      const where = msg => failures.push(`${name} at ${view.name}: ${msg}`);
      const outside = new Set();
      page.on('request', r => { if (!r.url().startsWith(origin) && !r.url().startsWith('data:')) outside.add(new URL(r.url()).host); });
      await page.route('**/*', route => route.request().url().startsWith(origin) || route.request().url().startsWith('data:')
        ? route.continue() : route.abort());
      page.on('console', m => { if (/Content Security Policy|Refused to/.test(m.text())) where(`CSP error: ${m.text().slice(0, 120)}`); });
      await page.goto(`${origin}${BASE}${name}`, { waitUntil: 'load' });
      const width = await page.evaluate(() => Math.max(document.documentElement.scrollWidth, document.body.scrollWidth));
      if (width > view.width + 1) where(`scrolls sideways (page is ${width}px wide)`);
      if (outside.size) where(`asks for outside hosts: ${[...outside].join(', ')}`);
      await page.close();
    }
    await ctx.close();
    // axe needs to inject its script, which the site's strict CSP blocks, so it runs in a second pass without the CSP.
    const axeCtx = await browser.newContext({ viewport: { width: view.width, height: view.height }, bypassCSP: true });
    for (const name of pages) {
      const page = await axeCtx.newPage();
      await page.route('**/*', route => route.request().url().startsWith(origin) || route.request().url().startsWith('data:')
        ? route.continue() : route.abort());
      await page.goto(`${origin}${BASE}${name}`, { waitUntil: 'load' });
      await page.evaluate(axeSource);
      const result = await page.evaluate(() => axe.run(document, { resultTypes: ['violations'] }));
      for (const v of result.violations.filter(v => v.impact === 'serious' || v.impact === 'critical')) {
        failures.push(`${name} at ${view.name}: axe ${v.impact}: ${v.id} (${v.help}); e.g. ${v.nodes[0].target.join(' ')}`);
      }
      await page.close();
    }
    await axeCtx.close();
  }
  await browser.close();
  server.close();
  if (failures.length) {
    console.log(failures.join('\n'));
    console.log(`\nFAILED: ${failures.length} problem(s).`);
    process.exit(1);
  }
  console.log(`OK: ${pages.length} pages checked at 360px and 1280px: no sideways scroll, no serious axe problems, nothing loaded from outside, no CSP errors.`);
})().catch(e => { console.error(e); process.exit(1); });
