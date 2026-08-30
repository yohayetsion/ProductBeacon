#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const childProcess = require('child_process');

const reviewRoot = __dirname;
const repoRoot = path.resolve(reviewRoot, '..', '..');
const marker = '<!-- Provenance: DR-2026-375 decision 2; the positioning divergence on this deeper page is deliberate for this round. Do not silently reconcile it. -->';
const robots = '<meta name="robots" content="noindex, nofollow, noarchive, noai, noimageai">';
const referrer = '<meta name="referrer" content="no-referrer">';
const expectedKeyHash = '604ea19e95d54b640c0df82a15542ccf0989d6751111049fd7922d8ee61e83aa';
const failures = [];
const passes = [];

function sha(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}

function count(haystack, needle) {
  return haystack.split(needle).length - 1;
}

function visibleText(html) {
  return html.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
}

function check(condition, label, detail) {
  if (condition) passes.push(label);
  else failures.push(detail ? `${label}: ${detail}` : label);
}

function read(relativePath) {
  const full = path.join(repoRoot, relativePath);
  if (!fs.existsSync(full)) {
    failures.push(`missing file: ${relativePath}`);
    return '';
  }
  return fs.readFileSync(full, 'utf8');
}

function checkHash(filePath, expected, label) {
  if (!fs.existsSync(filePath)) {
    failures.push(`${label}: missing ${filePath}`);
    return;
  }
  const actual = sha(fs.readFileSync(filePath));
  check(actual === expected, label, `expected ${expected}, got ${actual}`);
}

const frozenInputs = [
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-relook-implementation-plan-2026-08-30.md', '997f568feb4106acd04c2d825569f5aa5a3aebdff297f2afd61761686d05676c', 'frozen relook plan hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-relook-entry-copy-contract-2026-08-30.md', 'dc195613d3b5c93aa2155076d9fc46fbe3bbebf0753a6222f5f79638d60186d9', 'frozen entry copy contract hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-relook-workforce-copy-contract-2026-08-30.md', 'b242517a5dddc4dd762ff5bb8ee0bc8afb048c49c05ee308b7a558300c6e6c70', 'frozen Workforce copy contract hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-relook-cro-acceptance-spec-2026-08-30.md', '9926f5444583a6ec181e4c58848329b25339dc152a99a215a980795f9587ccdb', 'frozen CRO acceptance spec hash'],
  ['G:/My Drive/Claude/context/decisions/2026/DR-2026-419-phase-5r-value-led-concourse-and-workforce-harness-story.md', 'd95a707eb6ba943e81494efea4b8cea49f5999f6634a679d003f5cef5ccf7192', 'frozen DR-2026-419 hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/messaging-positioning-2026-08-26.md', '316aaff00117863c9b8c51c2fb54ef260d5c99ec5e274f628cce63babd07fff0', 'frozen preserved-door copy contract hash']
];
frozenInputs.forEach(([filePath, expected, label]) => checkHash(filePath, expected, label));

const sourcePaths = [
  'index.html',
  'only-product-person/index.html',
  'covering-everything/index.html',
  'workforce.html',
  'research/index.html',
  'on-call.html'
];
const source = Object.fromEntries(sourcePaths.map(file => [file, read(file)]));
const home = source['index.html'];
const doorOne = source['only-product-person/index.html'];
const doorTwo = source['covering-everything/index.html'];
const workforce = source['workforce.html'];

const homeIds = new Set([...home.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]));
const linkedHomeHashes = sourcePaths.flatMap(file => [...source[file].matchAll(/href="\/index\.html#([^"]+)"/g)].map(match => ({ file, id: match[1] })));
check(linkedHomeHashes.every(link => homeIds.has(link.id)), 'source home hash links resolve', linkedHomeHashes.filter(link => !homeIds.has(link.id)).map(link => `${link.file}#${link.id}`).join(', '));

function markerPositions(html, attribute, values) {
  return values.map(value => html.indexOf(`${attribute}="${value}"`));
}

function strictlyIncreasing(values) {
  return values.every((value, index) => value !== -1 && (index === 0 || value > values[index - 1]));
}

const entrySections = ['entry-hero', 'entry-shift', 'offer-journeys', 'entry-proof', 'buyer-router', 'entry-final-route'];
check(home.includes('<main id="main-content" class="entry-main" data-phase5r-page="entry" tabindex="-1">'), 'entry main marker exact');
check(entrySections.every(value => count(home, `data-phase5r-section="${value}"`) === 1), 'entry section markers exact once');
check(strictlyIncreasing(markerPositions(home, 'data-phase5r-section', entrySections)), 'entry section markers ordered');
check(count(home, 'data-clarity="outcome"') === 1 && count(home, 'data-clarity="difference"') === 1 && count(home, 'data-clarity="choice"') === 1, 'hero clarity markers exact');
const entryHero = (home.match(/<[^>]+data-phase5r-section="entry-hero"[\s\S]*?<\/section>/) || [''])[0];
check(count(entryHero, '<h1') === 1 && count(home, '<h1') === 1, 'entry single H1 inside hero');
check(!/(\$|\/ month|first month|compute excluded|finish it and the licence opens)/i.test(visibleText(entryHero)), 'entry hero has no price or access-condition tokens');
check(entryHero.includes('href="#find-my-route"') && entryHero.includes('href="workforce.html"'), 'entry hero primary and Workforce routes');
check(entryHero.includes('Carry more of the company without carrying every function alone.'), 'entry hero H1 exact');

const journeys = ['inspect-method', 'learn-to-operate', 'run-workforce', 'delegate-work'];
check(journeys.every(value => count(home, `data-offer-journey="${value}"`) === 1), 'four offer journeys exact');
check(count(home, 'data-offer-journey="') === 4, 'four offer journeys only', `found ${count(home, 'data-offer-journey="')}`);
check(count(home, 'data-journey-part="value"') === 4 && count(home, 'data-journey-part="offers"') === 4 && count(home, 'data-journey-part="actions"') === 4, 'journey value offer action anatomy exact');
check(count(home, 'data-journey-visual="') === 4, 'four distinct journey visuals');
check(!home.includes('class="offer-table"') && !home.includes('<caption class="visually-hidden">The whole offer</caption>'), 'old offer table absent');
const offerLabels = [
  'Vision to Value', 'Decision Provenance Standard', 'Both published market reports', 'Product Org OS',
  'The recorded course', 'Monthly open Q&amp;A', 'The licence, all 15 teams', 'Operator Intensive', 'The Room',
  'Commissioned market report', 'On Call', 'Fractional'
];
check(offerLabels.every(label => home.includes(label)), 'governed offer breadth present');
check(count(home, 'id="intensive"') === 1, 'Operator Intensive anchor exact once');

const proofKinds = ['published-method', 'published-standard', 'open-system', 'published-output'];
check(proofKinds.every(value => count(home, `data-proof-kind="${value}"`) === 1), 'four inspectable proof kinds exact');
check(count(home, 'data-proof-visual="') === 4 && home.includes('src="/research/og/report-digest.png"'), 'proof uses four visual previews including published report art');
check(home.indexOf('data-phase5r-section="entry-proof"') < home.indexOf('data-phase5r-section="buyer-router"'), 'proof precedes buyer router');
check(!/(testimonial|customer-logo|review-score|performance-result)/i.test(entryHero), 'hero contains no invented proof component');

check(count(home, 'data-router-step="1"') === 1 && count(home, 'data-router-step="2"') === 1, 'router has one first step and one conditional second-step panel');
check(count(home, 'data-route-mode="operate"') === 1 && count(home, 'data-route-direct="delegate"') === 1 && !home.includes('data-route-mode="delegate"'), 'router operate mode and direct delegate route exact');
check(count(home, 'data-route-choice="product-inside-company"') === 1 && count(home, 'data-route-choice="several-functions-or-clients"') === 1 && count(home, 'data-route-choice="productbeacon-carries-work"') === 1, 'router destinations exact');
check(home.includes('id="route-operate-options" data-router-step="2" data-route-panel="operate" hidden') && !home.includes('data-route-panel="delegate"'), 'router conditional panel initially hidden');
check(count(home, '<div class="router-status" data-router-status') === 1 && home.includes('role="status"') && home.includes('aria-live="polite"'), 'router status region present');
check(home.includes('<noscript><h3>Choose the route that sounds most like your work.</h3>'), 'router no-script heading exact');
check(home.includes('href="only-product-person/"') && home.includes('href="covering-everything/"') && home.includes('href="on-call.html"'), 'entry final routes use existing destinations');
check(!sourcePaths.some(file => source[file].includes('$1,000')), '$1,000 absent from visitor copy');

const frozenNavLabels = [
  'The Operator Intensive', 'The Workforce', 'On Call &amp; Fractional',
  'The Standard', 'Research', 'About', 'Apply'
];
for (const file of ['index.html', 'only-product-person/index.html', 'covering-everything/index.html']) {
  const navMatch = source[file].match(/<nav class="nav"[\s\S]*?<\/nav>/);
  const nav = navMatch ? navMatch[0] : '';
  check(frozenNavLabels.every(label => nav.includes(`>${label}<`)), `${file} frozen global navigation labels`);
  check(!nav.includes('/only-product-person/') && !nav.includes('/covering-everything/'), `${file} door links excluded from global navigation`);
}

const doorOneExact = [
  'The deadline work wins: the demo, the deck, the release.',
  'The half without a date never gets a slot.',
  'You know exactly what a product organisation does because you have been inside one.',
  'On your own, you get to about a third of it.',
  'Product Org OS gives you the other two thirds: a free product team you can download and run this week on one real decision.',
  'No email. No call. It is a download.',
  'Get the free product team',
  'Trying it on one real decision? Send LANTERN on LinkedIn.'
];
check(doorOneExact.every(value => visibleText(doorOne).includes(value)), 'Door 1 exact copy and CTA');
check(!/workaround|substitut/i.test(doorOne), 'Door 1 has no workaround or substitute language');
const doorOneSectionHeadings = [
  'The deadline work wins: the demo, the deck, the release.',
  'You know exactly what a product organisation does because you have been inside one.',
  'Product Org OS gives you the other two thirds: a free product team you can download and run this week on one real decision.'
];
check(doorOneSectionHeadings.every(value => doorOne.includes(`<h2>${value}</h2>`)), 'Door 1 uses approved existing copy for section H2 headings');

const privacy = 'Web3Forms processes the details you submit so Yohay can register you for the free course and follow up personally. This is course registration, not a mailing list, and no automated email is sent. To ask us to delete your details, use the ProductBeacon contact page.';
check(visibleText(doorTwo).includes(privacy), 'Door 2 privacy copy exact');
check(doorTwo.includes('<a href="/contact.html">ProductBeacon contact page</a>'), 'Door 2 deletion route exact');
check(!doorTwo.includes('mailto:'), 'Door 2 has no mailto deletion route');
check(doorTwo.includes('action="https://api.web3forms.com/submit"') && doorTwo.includes('method="POST"'), 'Web3Forms endpoint and method');

const keyMatch = doorTwo.match(/name="access_key" value="([^"]+)"/);
check(Boolean(keyMatch), 'Web3Forms hidden access key exists');
if (keyMatch) check(sha(Buffer.from(keyMatch[1], 'utf8')) === expectedKeyHash, 'Web3Forms access key hash exact');
const fields = [
  ['name', 'required'], ['email', 'required'], ['linkedin', 'optional'], ['question', 'required']
];
fields.forEach(([name, requirement]) => {
  const input = doorTwo.match(new RegExp(`<[^>]+name="${name}"[^>]*>`));
  check(Boolean(input), `form field ${name} exists`);
  if (input) check(requirement === 'required' ? /\srequired(?:\s|>)/.test(input[0]) : !/\srequired(?:\s|>)/.test(input[0]), `form field ${name} ${requirement}`);
});
const emailInput = doorTwo.match(/<input[^>]+name="email"[^>]*>/);
check(Boolean(emailInput && /inputmode="email"/.test(emailInput[0])), 'email field declares email input mode');
check(/name="botcheck"[^>]+style="display:\s*none"/.test(doorTwo), 'honeypot hidden');
check(doorTwo.includes('name="subject" value="ProductBeacon free course registration"'), 'form subject exact');
check(doorTwo.includes('name="from_name" value="ProductBeacon"'), 'form from_name exact');
check(doorTwo.includes('<dialog') && doorTwo.includes('aria-labelledby="course-dialog-title"') && doorTwo.includes('aria-describedby="course-dialog-description course-dialog-privacy"') && doorTwo.includes('id="course-dialog-privacy"'), 'dialog is described by intro and privacy');
const privacyPosition = doorTwo.indexOf('id="course-dialog-privacy"');
const submitPosition = doorTwo.indexOf('id="course-submit"');
check(privacyPosition !== -1 && submitPosition !== -1 && privacyPosition < submitPosition, 'privacy notice appears before submit');
check(/\.course-form input,[\s\S]{0,80}\.course-form textarea\s*\{[\s\S]{0,300}border:\s*1px solid var\(--secondary\)/.test(doorTwo), 'Door 2 idle input boundaries use secondary');
check(doorTwo.includes("status.setAttribute('role', 'alert')") && doorTwo.includes("status.setAttribute('aria-live', 'assertive')") && doorTwo.includes("status.setAttribute('aria-live', 'polite')") && doorTwo.includes("status.removeAttribute('role')") && doorTwo.includes('tabindex="-1"'), 'failure output is a focusable alert and success remains polite');
const statuses = [
  'Please enter your name.',
  'Please enter a valid email address.',
  'Please enter a valid LinkedIn address or leave it blank.',
  'Please tell us what you are covering alone right now.',
  'Sending...',
  'Thanks. Your registration has been sent to Yohay. He will follow up personally.',
  'Something went wrong. Please try again or use the ProductBeacon contact page.',
  'Registration is not available right now. Please use the ProductBeacon contact page.'
];
check(statuses.every(value => doorTwo.includes(value)), 'all form state copy exact');
check(doorTwo.includes('function clearFieldError(field)') && doorTwo.includes("field.removeAttribute('aria-invalid')") && doorTwo.includes('function clearFieldIfValid(rule)') && doorTwo.includes("rule.field.addEventListener('input'") && doorTwo.includes('clearFieldIfValid(rule)') && !doorTwo.includes("rule.field.addEventListener('input', clearErrors)"), 'each valid field clears only its own error immediately');
check(doorTwo.includes('var submitting = false;') && doorTwo.includes('if (submitting) return;'), 'duplicate form requests are prevented');
check(doorTwo.includes("form.setAttribute('aria-busy', 'true')") && doorTwo.includes("form.setAttribute('aria-busy', 'false')"), 'form submission sets and clears aria-busy');
check(doorTwo.includes('submitButton.textContent = messages.sending;') && doorTwo.includes('submitButton.textContent = submitLabel;'), 'submit label becomes exact Sending... and restores');
check(/if\s*\(payload\s*&&\s*payload\.success\)[\s\S]*?form\.reset\(\)/.test(doorTwo), 'form resets only in success branch');
check(!/\.catch\([\s\S]{0,400}form\.reset\(\)/.test(doorTwo), 'form preserves values on failure');

const doorTwoSectionHeadings = [
  'The work is important.',
  'The workforce covers those functions: the positioning, the pricing, the competitive read.'
];
check(doorTwoSectionHeadings.every(value => doorTwo.includes(`<h2>${value}</h2>`)), 'Door 2 uses approved existing copy for section H2 headings');

for (const [file, html] of [['index.html', home], ['only-product-person/index.html', doorOne], ['covering-everything/index.html', doorTwo]]) {
  check(html.includes('<footer class="footer entry-footer">') && /\.entry-footer \.footer__bottom\s*\{\s*color:\s*var\(--secondary\);\s*\}/.test(html), `${file} entry footer meaningful text uses secondary`);
  const reducedMotion = html.match(/@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{[\s\S]*?\n\s*\}/);
  check(Boolean(reducedMotion && /transition:\s*none\s*!important/.test(reducedMotion[0]) && /transform:\s*none\s*!important/.test(reducedMotion[0])), `${file} reduced motion removes transitions and transforms`);
}

const workforceStory = ['role-based-specialists', 'full-harness', 'loop-and-learn', 'distributed-company-brain'];
check(/<main\b[^>]*id="main-content"[^>]*data-phase5r-page="workforce"[^>]*>/.test(workforce), 'Workforce main marker exact');
check(workforceStory.every(value => count(workforce, `data-workforce-story="${value}"`) === 1), 'four Workforce story markers exact once');
check(strictlyIncreasing(markerPositions(workforce, 'data-workforce-story', workforceStory)), 'Workforce story markers ordered');
check(workforceStory.every(value => workforce.indexOf(`data-workforce-story="${value}"`) < workforce.indexOf('data-workforce-view="team-map"')), 'Workforce story precedes team map');
check(count(workforce, 'data-workforce-view="team-map"') === 1 && count(workforce, 'data-workforce-view="specialist-roster"') === 1, 'one Workforce team map and one specialist roster');
check(workforce.indexOf('data-workforce-view="team-map"') < workforce.indexOf('data-workforce-view="specialist-roster"'), 'Workforce team map precedes roster');
check(!visibleText(workforce).includes('Here is what you ask for, and here is what comes back.'), 'old request-output heading absent');
check(!visibleText(workforce).includes('From request to deliverable.'), 'old request-to-deliverable heading absent');

const harnessNodes = ['request-context', 'role-methods-knowledge-limits', 'specialist', 'structured-output-evidence'];
check(harnessNodes.every(value => count(workforce, `data-harness-node="${value}"`) === 1), 'Full Harness nodes exact once');
check(strictlyIncreasing(markerPositions(workforce, 'data-harness-node', harnessNodes)), 'Full Harness nodes ordered');
const loopSteps = ['frame', 'plan', 'execute', 'audit', 'review', 'record'];
check(loopSteps.every(value => count(workforce, `data-loop-step="${value}"`) === 1), 'Loop and Learn steps exact once');
check(strictlyIncreasing(markerPositions(workforce, 'data-loop-step', loopSteps)), 'Loop and Learn steps ordered');
check(count(workforce, 'data-human-gate="frame"') === 1 && count(workforce, 'data-human-gate="review"') === 1, 'Loop and Learn human gates exact');
const memoryRecords = ['documents', 'decisions', 'bets', 'assumptions', 'learnings', 'feedback'];
check(memoryRecords.every(value => count(workforce, `data-memory-record="${value}"`) === 1), 'Distributed Company Brain records exact once');

const teamMap = (workforce.match(/<[^>]+data-workforce-view="team-map"[\s\S]*?<\/section>/) || [''])[0];
const roster = (workforce.match(/<[^>]+data-workforce-view="specialist-roster"[\s\S]*?<\/section>/) || [''])[0];
check(count(teamMap, 'class="org-tile"') === 15, 'Workforce team map has 15 tiles', `found ${count(teamMap, 'class="org-tile"')}`);
check(count(teamMap, 'class="role-card"') === 0, 'Workforce team map has no role cards');
check(count(roster, 'class="function-block"') === 15, 'Workforce roster has 15 function blocks', `found ${count(roster, 'class="function-block"')}`);
check(count(roster, 'class="role-card"') === 96, 'Workforce roster has 96 role cards', `found ${count(roster, 'class="role-card"')}`);
check(workforce.includes('id="the-skills"') && workforce.includes('id="skills-grid"') && workforce.includes('id="libs-grid"') && count(workforce, 'data-expand-target=') === 2, 'Workforce skills and libraries controls retained');
check(/qualified human|qualified professional/i.test(visibleText(workforce)) && /not legal advice/i.test(visibleText(workforce)), 'Workforce supervised-domain boundary retained');

const forbiddenClaims = [
  'every request becomes a team', 'router always finds', 'never re-explain your business',
  'every session makes the system smarter', 'model retrains itself', 'automatically gets smarter',
  'full harness guarantees', 'guaranteed correct', 'replaces your lawyer',
  'replaces a human team', 'licensed professional agent'
];
const visitorText = `${visibleText(home)} ${visibleText(workforce)}`.toLowerCase();
check(forbiddenClaims.every(fragment => !visitorText.includes(fragment)), 'forbidden public claim fragments absent');

const workforceMarker = '<!-- Provenance: DR-2026-419; substantive Phase 5R Workforce relook approved by Yohay Etsion 2026-08-30. -->';
check(count(workforce, workforceMarker) === 1, 'workforce DR-2026-419 provenance marker exact once', `found ${count(workforce, workforceMarker)}`);

const deepBaselines = {
  'research/index.html': '7a6100f724b843becfb879fae5a225670df97ba31b7ed266061f9bf79bd7bd19',
  'on-call.html': 'd31057fdaf8998ca1a7a929395d4045c4dd8c009bdcc7a2d80b2ec112e33131f'
};
for (const [file, baseline] of Object.entries(deepBaselines)) {
  check(count(source[file], marker) === 1, `${file} D8 marker exact once`, `found ${count(source[file], marker)}`);
  const withoutMarker = source[file].replace(`${marker}\r\n`, '').replace(`${marker}\n`, '').replace(marker, '');
  check(sha(Buffer.from(withoutMarker, 'utf8')) === baseline, `${file} changed only by marker (plus preserved D39 where applicable)`);
}

const expectedReviewPages = [
  'index.html',
  'only-product-person/index.html',
  'covering-everything/index.html',
  'workforce.html',
  'research/index.html',
  'on-call.html'
];
const reviewHtml = Object.fromEntries(expectedReviewPages.map(file => [file, read(path.join('internal/fill-the-rooms-review', file))]));
for (const [file, html] of Object.entries(reviewHtml)) {
  check(count(html, robots) === 1, `${file} exact robots meta once`, `found ${count(html, robots)}`);
  check(count(html, referrer) === 1, `${file} exact referrer meta once`, `found ${count(html, referrer)}`);
  check(html.includes('Internal review candidate') && html.includes('Build 5R-RELOOK-20260830-DR419') && html.includes('Unlisted and crawl-blocked, not private.'), `${file} visible immutable review stamp`);
  check(!/(googletagmanager|\bgtag\s*\(|\bpbTrack\b|\bdataLayer\b|linkedin_partner|snap\.licdn)/i.test(html), `${file} tracking stripped`);
  const attrs = [...html.matchAll(/(?:href|src|action)="([^"]+)"/g)].map(match => match[1]);
  const relative = attrs.filter(value => !value.startsWith('/') && !value.startsWith('#') && !/^[a-z][a-z0-9+.-]*:/i.test(value));
  check(relative.length === 0, `${file} contains no relative same-origin links`, relative.join(', '));
  const escapedInSet = attrs.filter(value => ['/index.html', '/only-product-person/', '/covering-everything/', '/workforce.html', '/research/', '/on-call.html'].some(route => value === route || value.startsWith(`${route}#`) || value.startsWith(`${route}?`)));
  check(escapedInSet.length === 0, `${file} in-set links remain inside review prefix`, escapedInSet.join(', '));
}

const manifestPath = path.join(reviewRoot, 'manifest.json');
const manifestHashPath = path.join(reviewRoot, 'manifest.sha256');
if (!fs.existsSync(manifestPath)) {
  failures.push('missing review manifest.json');
} else {
  let manifest;
  try { manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8')); }
  catch (error) { failures.push(`manifest JSON invalid: ${error.message}`); }
  if (manifest) {
    const expectedCommitPaths = [
      'internal/fill-the-rooms-review/build-review.js',
      'internal/fill-the-rooms-review/covering-everything/index.html',
      'internal/fill-the-rooms-review/index.html',
      'internal/fill-the-rooms-review/manifest.json',
      'internal/fill-the-rooms-review/manifest.sha256',
      'internal/fill-the-rooms-review/on-call.html',
      'internal/fill-the-rooms-review/only-product-person/index.html',
      'internal/fill-the-rooms-review/phase5r-gate.js',
      'internal/fill-the-rooms-review/research/index.html',
      'internal/fill-the-rooms-review/workforce.html'
    ];
    check(JSON.stringify(manifest.commit_paths) === JSON.stringify(expectedCommitPaths), 'review commit path manifest exact');
    check(Array.isArray(manifest.files) && manifest.files.length === 8, 'review hash scope has eight non-meta files');
    if (Array.isArray(manifest.files)) {
      manifest.files.forEach(entry => {
        const full = path.join(repoRoot, entry.path);
        check(fs.existsSync(full), `manifest path exists: ${entry.path}`);
        if (fs.existsSync(full)) check(sha(fs.readFileSync(full)) === entry.sha256, `manifest hash exact: ${entry.path}`);
      });
    }
    check(Array.isArray(manifest.external_shared_dependencies) && manifest.external_shared_dependencies.includes('/css/style.css') && manifest.external_shared_dependencies.includes('/js/main.js'), 'shared dependencies inventoried');
  }
}
if (!fs.existsSync(manifestHashPath) || !fs.existsSync(manifestPath)) {
  failures.push('missing review manifest hash sidecar');
} else {
  const sidecar = fs.readFileSync(manifestHashPath, 'utf8').trim();
  check(sidecar === sha(fs.readFileSync(manifestPath)), 'single manifest SHA-256 exact');
}

const staged = childProcess.execFileSync('git', ['diff', '--cached', '--name-only'], { cwd: repoRoot, encoding: 'utf8' }).trim();
check(staged === '', 'Git index remains empty', staged);

if (process.argv.includes('--determinism') && fs.existsSync(path.join(reviewRoot, 'build-review.js'))) {
  const allPaths = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath, 'utf8')).commit_paths : [];
  const snapshot = Object.fromEntries(allPaths.filter(file => fs.existsSync(path.join(repoRoot, file))).map(file => [file, sha(fs.readFileSync(path.join(repoRoot, file)))]));
  childProcess.execFileSync(process.execPath, [path.join(reviewRoot, 'build-review.js')], { cwd: repoRoot, stdio: 'inherit' });
  const after = Object.fromEntries(allPaths.filter(file => fs.existsSync(path.join(repoRoot, file))).map(file => [file, sha(fs.readFileSync(path.join(repoRoot, file)))]));
  check(JSON.stringify(after) === JSON.stringify(snapshot), 'deterministic transform rerun is byte-identical');
}

passes.forEach(label => console.log(`PASS ${label}`));
failures.forEach(label => console.error(`FAIL ${label}`));
console.log(`RESULT ${passes.length} passed, ${failures.length} failed`);
if (failures.length) process.exit(1);
