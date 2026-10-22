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
for (const id of ['course-name', 'course-email', 'course-linkedin', 'course-question', 'intensive-name', 'intensive-email', 'intensive-linkedin', 'intensive-question']) check(doorTwo.includes(`id="${id}"`), `Door 2 dialog field ${id} present`);
check(doorTwo.includes('id="open-course-dialog">Register for the Operator Briefing</button>'), 'Door 2 primary action is the registration button');
check(doorTwo.includes('id="open-intensive-dialog">Join the Intensive waiting list</button>'), 'Door 2 Intensive row carries the waiting-list button');
check(!doorTwo.includes('<div class="door-actions">'), 'Door 2 bottom action block removed; the button lives in the free-course row');
check(doorTwo.includes('value="ProductBeacon Intensive waiting list"') && doorTwo.includes('value="ProductBeacon Operator Briefing registration"'), 'the two forms carry distinct subjects');
check((doorTwo.match(/name="access_key" value="([^"]+)"/g) || []).length === 2 && new Set([...doorTwo.matchAll(/name="access_key" value="([^"]+)"/g)].map(m => m[1])).size === 1, 'both forms use the one Gmail-registered key');
check(!/<input[^>]*type="date"/.test(doorTwo), 'no date field in either dialog');
const licenceRow = (doorTwo.match(/<h2>Step two: the licence\.<\/h2>[\s\S]*?<\/div>/) || [''])[0];
check(licenceRow && !/\bseat/i.test(licenceRow), 'the word seat never appears in the licence row');
const mainHtml = (doorTwo.match(/<main[\s\S]*<\/main>/) || [''])[0];
check((mainHtml.match(/href="https:\/\/yohayetsion\.github\.io\/product-org-os\/"/g) || []).length === 1, 'Door 2 body links the Product Org OS site exactly once (licence row)');
check(/aria-label="Get Product Org OS, opens the Product Org OS site">Get Product Org OS &#8599;<\/a>/.test(mainHtml), 'the Product Org OS link carries the outbound cue and aria-label');
check(mainHtml.includes('<p class="door-note door-note--link"><a href="https://yohayetsion.github.io/product-org-os/"'), 'the Product Org OS link sits on its own line');
check((mainHtml.match(/class="door-beat /g) || []).length === 4, 'Door 2 carries exactly four ladder rows after round 3');
check(mainHtml.includes('<a href="/research/">Read two full reports the workforce wrote</a>') && mainHtml.includes('<a href="/workforce.html">The Workforce</a>'), 'secondary links carry the proof and the Workforce');
check(!doorTwo.includes('It lands here, after everything else') && !doorTwo.includes('ProductBeacon built an AI workforce that covers those functions'), 'the two intro beats are removed');
const affirmedStrings = [
  'You carry the positioning, the pricing and the competitive read. There is nobody else for it.',
  'Recorded. No fee. Finish it and the licence opens.',
  'Your registration goes to Yohay. He reads it and replies personally.',
  '$200 a month, first month free.',
  'Need only the Product team? That one is free and open source.',
  'The Intensive is about how you govern the workforce effectively, leading them to do the work. You do not need the licence to join.',
  'Two seatings, two hours each. $600 per cohort of up to 5 seats. Live.',
  'Cohorts open in order of registration.',
  'Every month: office hours, live.',
  'One live session a month. Bring a question about your own work or about the workforce, and ask it. You do not need the Operator Briefing or the licence.',
  'Free. Open to anyone.',
  'The recorded part of the Operator Intensive: short videos on how the workforce runs.',
  'Read two full reports the workforce wrote'
];
for (const s of affirmedStrings) check(doorTwoText.includes(s), `Door 2 carries the reviewed string: ${s}`);
// Operator Briefing rename (DR-2026-636, closed 22 Oct 2026): each approved v3 string, word for word,
// in every Door 2 place; the two hands-on bullets gone (Decision 5); no "course" in visible text or meta.
const doorTwoCount = needle => doorTwo.split(needle).length - 1;
const briefingExact = [
  [3, "content=\"For the person carrying the positioning, the pricing and the competitive read: the Operator Briefing first, with no fee, then the licence and the Intensive.\""],
  [1, "<meta name=\"description\" content=\"For the person carrying the positioning, the pricing and the competitive read: the Operator Briefing first, with no fee, then the licence and the Intensive.\">"],
  [1, "<meta property=\"og:description\" content=\"For the person carrying the positioning, the pricing and the competitive read: the Operator Briefing first, with no fee, then the licence and the Intensive.\">"],
  [1, "<meta name=\"twitter:description\" content=\"For the person carrying the positioning, the pricing and the competitive read: the Operator Briefing first, with no fee, then the licence and the Intensive.\">"],
  [1, "<h2>Step one: the Operator Briefing.</h2>"],
  [1, "<p>The recorded part of the Operator Intensive: short videos on how the workforce runs.</p>"],
  [1, "<ul class=\"door-agenda\" aria-label=\"Operator Briefing agenda\"><li>What the Operator's job is, once an AI workforce does the work.</li><li>Meet the teams and understand the roles, skills and knowledge behind each specialist.</li><li>Follow a task through planning, specialist work and review.</li></ul>"],
  [1, "<p class=\"door-cost\">Recorded. No fee. Finish it and the licence opens.</p>"],
  [1, "<p id=\"course-dialog-description\">Recorded. No fee. Finish it and the licence opens.</p>"],
  [1, "id=\"open-course-dialog\">Register for the Operator Briefing</button>"],
  [1, "<h2 id=\"course-dialog-title\">Register for the Operator Briefing</h2>"],
  [1, "id=\"course-submit\" type=\"submit\">Register for the Operator Briefing</button>"],
  [1, "name=\"subject\" value=\"ProductBeacon Operator Briefing registration\""],
  [1, "<p>The whole workforce, all 15 teams, yours to run. It opens when you finish the Operator Briefing.</p>"],
  [1, "and ask it. You do not need the Operator Briefing or the licence.</p>"],
  [1, "id=\"course-dialog-privacy\">Web3Forms processes the details you submit so Yohay can register you for the Operator Briefing and follow up personally. This is a registration, not a mailing list, and no automated email is sent. To ask us to delete your details, use the <a href=\"/contact.html\">ProductBeacon contact page</a>.</p>"],
  [1, "aria-label=\"Close the registration form\""]
];
for (const [n, s] of briefingExact) check(doorTwoCount(s) === n, `Door 2 Operator Briefing string x${n} (found ${doorTwoCount(s)}): ${s}`);
for (const s of ["Set up a practice workforce and give it the relevant company context.", "Produce one finished deliverable from a function you cover alone."]) check(!doorTwo.includes(s), `Door 2 hands-on agenda bullet removed (Decision 5): ${s}`);
const doorTwoVisible = doorTwo.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<style[\s\S]*?<\/style>/g, ' ').replace(/<!--[\s\S]*?-->/g, ' ').replace(/<[^>]*>/g, ' ');
const doorTwoAttrs = [...doorTwo.matchAll(/\b(?:content|aria-label|title|alt|placeholder)="([^"]*)"/g)].map(m => m[1]).join(' | ');
const courseHits = [...`${doorTwoVisible} | ${doorTwoAttrs}`.matchAll(/.{0,30}\bcourse\b.{0,30}/gi)].map(m => m[0].replace(/\s+/g, ' ').trim());
check(courseHits.length === 0, `Door 2 visible text and meta carry no "course" (found: ${courseHits.join(' / ') || 'none'})`);
const forbidden = [
  [/\$750|\$8,000|\$2,000|\$500\b|\$3,500|\$10,000|\$15,000|\$25,000/, 'withdrawn or removed figures'],
  [/\bper seat\b|\bone user\b|\bone organisation\b/i, 'licence unit or scope'],
  [/\bboth\b/i, 'the word both'],
  [/\u2014/, 'em dash'],
  [/\bcoming soon\b|\bshortly\b|\bsoon\b/i, 'a date promise'],
  [/\b(January|February|March|April|May|June|July|August|September|October|November|December)\b/, 'a month name'],
  [/\b96\b|\b92\b|\b104\b/, 'a specialist count'],
  [/with a call to walk you through it|end to end/, 'a withdrawn claim'],
  [/about 12|one day|\blicense\b|Nobody is going to be hired|after eight|founding|Runs on your own Claude plan|a seat, founding/, 'a round-2 or round-3 withdrawn string'],
  [/next cohort|keep you posted|subscribe|updates\b/i, 'a waiting-list date or list promise'],
  [/the Room|Every week|weekly|Or ProductBeacon carries it|Read the work before you believe|Who this is not for|Included, after the Intensive/, 'a round-3 removed string'],
  [/about a seat|Seats open in order/, 'per-seat waiting-list wording under the cohort unit'],
  [/Yohay replies personally/, 'the removed reply line']
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
  const outside = staged.filter(f => !manifest.commit_paths.includes(f));
  check(outside.length === 0, `nothing staged outside manifest commit_paths (outside: ${outside.join(', ') || 'none'})`);
  const unstagedDirty = manifest.commit_paths.filter(f => !staged.includes(f) && cp.spawnSync('git', ['diff', '--quiet', 'HEAD', '--', f], { cwd: repoRoot }).status !== 0);
  check(unstagedDirty.length === 0, `every unstaged commit_path is identical to HEAD (dirty: ${unstagedDirty.join(', ') || 'none'})`);
  check(staged.length > 0, `at least one candidate file is staged (staged ${staged.length} of ${manifest.commit_paths.length})`);
}

console.log(`PASS ${passes.length}  FAIL ${failures.length}`);
for (const f of failures) console.log('FAIL ' + f);
process.exit(failures.length ? 1 : 0);
