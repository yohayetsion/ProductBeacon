#!/usr/bin/env node
'use strict';
// Static gate for the SITE-DOORS-20260909 review candidate (DR-2026-469; DR-2026-412 gate).
// Usage: node internal/fill-the-rooms-review/site-doors-gate.js [--staged]
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const reviewRoot = __dirname;
const repoRoot = path.resolve(reviewRoot, '..', '..');
const prefix = '/internal/fill-the-rooms-review/';
const OS = 'https://yohayetsion.github.io/product-org-os/';
const expectedKeyHash = '604ea19e95d54b640c0df82a15542ccf0989d6751111049fd7922d8ee61e83aa';
const failures = [];
const passes = [];

const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const read = file => fs.readFileSync(path.join(repoRoot, file), 'utf8');
const check = (ok, label) => (ok ? passes : failures).push(label);
const bodyText = html => (html.match(/<main[\s\S]*<\/main>/) || [html])[0]
  .replace(/<script[\s\S]*?<\/script>/g, '')
  .replace(/<[^>]*>/g, ' ');

const routes = ['/', '/only-product-person/', '/covering-everything/', '/vision-to-value/', '/workforce.html', '/research/', '/on-call.html'];
const files = {
  '/': 'index.html',
  '/only-product-person/': 'only-product-person/index.html',
  '/covering-everything/': 'covering-everything/index.html',
  '/vision-to-value/': 'vision-to-value/index.html',
  '/workforce.html': 'workforce.html',
  '/research/': 'research/index.html',
  '/on-call.html': 'on-call.html'
};
const inSet = new Set([...routes, '/index.html', '/covering-everything/index.html', '/only-product-person/index.html', '/vision-to-value/index.html', '/research/index.html']);
const review = {};
const source = {};
for (const route of routes) {
  review[route] = read('internal/fill-the-rooms-review/' + files[route]);
  source[route] = read(files[route]);
}

// Review directives on every review page
for (const route of routes) {
  const html = review[route];
  check(html.includes('<meta name="robots" content="noindex, nofollow, noarchive, noai, noimageai">'), `${route} review page carries noindex`);
  check(html.includes('<meta name="referrer" content="no-referrer">'), `${route} review page carries no-referrer`);
  check(!/googletagmanager|\bgtag\(|\bpbTrack\b|dataLayer/.test(html), `${route} review page has tracking stripped`);
  if (route !== '/only-product-person/') {
    check(html.includes('class="phase5r-review-banner"') && /class="[^"]*review-candidate/.test(html), `${route} review page carries the banner`);
    check(!html.includes('only-product-person'), `${route} review page carries no Door 1 link`);
  }
  const bare = [...html.matchAll(/\b(?:href|action)="(\/[^"]*)"/g)].map(m => m[1].split(/[?#]/)[0]).filter(v => inSet.has(v));
  check(bare.length === 0, `${route} review page has every in-set route remapped under ${prefix} (bare: ${bare.join(', ') || 'none'})`);
}

// Door 1 retirement
const home = source['/'];
const workforce = source['/workforce.html'];
const stub = source['/only-product-person/'];
check((home.match(/data-route="run-one-product-team"[^>]*href="([^"]+)"/) || [])[1] === OS, 'home card 1 goes to the Product Org OS site');
check(/data-route="run-one-product-team"[^>]*aria-label="Get Product Org OS, opens the Product Org OS site"/.test(home), 'home card 1 has the external aria-label');
check(home.includes('<span class="route-surface__cta">Get Product Org OS &#8599;</span>'), 'home card 1 CTA reads Get Product Org OS with the outbound glyph');
check(!home.includes('/only-product-person/'), 'home has no Door 1 link');
check(!home.includes('See my Product route'), 'old CTA string gone from home');
check(workforce.includes(`href="${OS}" rel="noopener" aria-label="Run one Product team, opens the Product Org OS site">Run one Product team &#8599;</a>`) && !workforce.includes('/only-product-person/'), 'workforce.html button repointed to the Product Org OS site');
check(!read('sitemap.xml').includes('only-product-person'), 'sitemap has no Door 1 entry');
check(stub.includes(`<meta http-equiv="refresh" content="0; url=${OS}">`) && stub.includes('<meta name="robots" content="noindex, follow">') && stub.includes(`<link rel="canonical" href="${OS}">`), 'Door 1 is a meta-refresh stub to the Product Org OS site, noindex/follow');

// Door 2
const doorTwo = source['/covering-everything/'];
const doorTwoText = bodyText(doorTwo);
const key = (doorTwo.match(/name="access_key" value="([^"]+)"/) || [])[1];
check(Boolean(key) && sha(Buffer.from(key, 'utf8')) === expectedKeyHash, 'Door 2 Web3Forms access key hash exact (Gmail-registered key)');
for (const id of ['course-name', 'course-email', 'course-linkedin', 'course-question']) check(doorTwo.includes(`id="${id}"`), `Door 2 dialog field ${id} present`);
check(doorTwo.includes('id="open-course-dialog">Register for the free course</button>'), 'Door 2 primary action is the registration button');
const affirmedStrings = [
  'Free. Recorded. Finish it and the licence opens.',
  '$200 a month, first month free. Runs on your own Claude plan (not included).',
  '$600, founding cohort. Live, about 12 seats.',
  'After step two or step three: the Room.',
  'One live session a month, for everyone who finished the Intensive or holds a licence.',
  'Included, after the Intensive or with a licence.',
  'Every month: the open question-and-answer session, live.',
  'Free. Open to anyone.',
  'A commissioned market report: a written analysis of your own market, segment or competitive position, produced by the workforce.',
  'Fractional: Yohay leads product inside your company, with the workforce behind him.',
  'Report $3,500, introductory. On Call $10,000 to $15,000 a month. Fractional $15,000 to $25,000 a month.',
  'written by this workforce. Free, in full.',
  'from a function you cover alone. It takes about an afternoon.',
  'You do not need the licence to join.',
  'after eight at night',
  'Who this is not for.',
  'Your registration goes to Yohay. He reads it and replies personally.'
];
for (const s of affirmedStrings) check(doorTwoText.includes(s), `Door 2 carries the reviewed string: ${s}`);
const forbidden = [
  [/\$750|\$8,000|\$2,000|\$500\b/, 'withdrawn figures'],
  [/\bper seat\b|\bone user\b|\bone organisation\b/i, 'licence unit or scope'],
  [/\bboth\b/i, 'the word both'],
  [/\u2014/, 'em dash'],
  [/\bcoming soon\b|\bshortly\b|\bsoon\b/i, 'a date promise'],
  [/\b(January|February|March|April|May|June|July|August|September|October|November|December)\b/, 'a month name'],
  [/\b96\b|\b92\b|\b104\b/, 'a specialist count'],
  [/with a call to walk you through it|end to end/, 'a withdrawn claim']
];
const doorTwoTextNoPrivacy = doorTwoText.replace(/Web3Forms processes[\s\S]*?contact page\s*\./, '');
for (const [re, label] of forbidden) check(!re.test(doorTwoTextNoPrivacy), `Door 2 body has no ${label}`);
check(!/mailing list|newsletter|subscribe/i.test(doorTwoTextNoPrivacy), 'Door 2 body has no mailing-list wording outside the privacy line');
const gate = cp.spawnSync('python', ['G:\\My Drive\\Claude\\ProductBeacon\\Marketing\\method-denylist-check.py', 'internal/fill-the-rooms-review/covering-everything/index.html'], { cwd: repoRoot, encoding: 'utf8' });
check(gate.status === 0, `Door 2 review page passes the D11 mechanical gate (exit ${gate.status})`);

// Vision to Value
const book = source['/vision-to-value/'];
check(book.includes('Yohay Etsion spent a decade leading world-class product organizations at NICE and Cognyte (NASDAQ: NICE, CGNT) in charge of product portfolios $250M/year with over 30 product pros. He is the author of <em>Leading the Charge</em> and runs ProductBeacon, a product leadership practice.'), 'Vision to Value bio is the owner text verbatim');
check(book.includes('<section class="section" style="padding-top:0">\n  <div class="container">\n    <div class="book-blurb">'), 'Vision to Value blurb section has the reduced top spacing');

// Manifest
const manifest = JSON.parse(read('internal/fill-the-rooms-review/manifest.json'));
check(read('internal/fill-the-rooms-review/manifest.sha256').trim() === sha(fs.readFileSync(path.join(repoRoot, 'internal/fill-the-rooms-review/manifest.json'))), 'manifest.sha256 matches manifest.json');
check(manifest.build_stamp === 'SITE-DOORS-20260909', 'manifest build stamp is SITE-DOORS-20260909');
for (const f of manifest.files) check(sha(fs.readFileSync(path.join(repoRoot, f.path))) === f.sha256, `manifest hash matches disk: ${f.path}`);
for (const p of manifest.source_to_review) check(sha(fs.readFileSync(path.join(repoRoot, p.source_path))) === p.source_sha256, `manifest source hash matches disk: ${p.source_path}`);

if (process.argv.includes('--staged')) {
  const staged = cp.execFileSync('git', ['diff', '--cached', '--name-only'], { cwd: repoRoot, encoding: 'utf8' }).trim().split(/\r?\n/).filter(Boolean).sort();
  check(JSON.stringify(staged) === JSON.stringify([...manifest.commit_paths].sort()), `staged set equals manifest commit_paths (staged ${staged.length}, expected ${manifest.commit_paths.length})`);
}

console.log(`PASS ${passes.length}  FAIL ${failures.length}`);
for (const f of failures) console.log('FAIL ' + f);
process.exit(failures.length ? 1 : 0);
