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
  ['G:/My Drive/Claude/ProductBeacon/Marketing/plan-fill-the-rooms-2026-08-26.md', '66e5b4f3e95b9fb5db6b764d50d266c12a66e10c96fc4f8cc9783c87552d3d38', 'frozen plan hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/messaging-positioning-2026-08-26.md', '316aaff00117863c9b8c51c2fb54ef260d5c99ec5e274f628cce63babd07fff0', 'frozen copy contract hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/backups/phase0-2026-08-29/manifests/phase6-expected-matrix.md', '776e118d6915062d5b30dc93a34a479142fd8b1d1a24cb0c316caf786bf0f369', 'frozen matrix hash']
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

check(home.includes("An organisation's worth of functions. One person can run them."), 'home H1 exact');
check(home.includes("One product person, no product team, and the founders still carry strategy."), 'Door 1 discovery exact');
check(home.includes("Whole disciplines nobody is going to be hired for, and they land on one person."), 'Door 2 discovery exact');

const teams = [
  'Product &amp; Strategy', 'Design', 'Architecture', 'Marketing', 'Finance',
  'Legal &amp; Compliance', 'Operations', 'Executive', 'Corp Dev', 'IT Governance',
  'HR / People Ops', 'Customer Success', 'Sales', 'Data Science', 'Personal Staff'
];
check(teams.every(team => home.includes(team)), 'all 15 team labels present');
check(count(home, 'class="team-item"') === 15, '15 team cells exact', `found ${count(home, 'class="team-item"')}`);

const ladderLabels = [
  'The book, the Standard, both market reports',
  'Product Org OS, open source',
  'The recorded course, how the workforce works',
  'Monthly open Q&amp;A, live',
  'The licence, all 15 teams',
  'Operator Intensive, live, about 12 seats',
  'The Room, monthly',
  'Commissioned market report',
  'On Call',
  'Fractional'
];
check(ladderLabels.every(label => home.includes(label)), 'ten ladder row labels exact');
const ladderBody = (home.match(/<tbody>[\s\S]*?<\/tbody>/) || [''])[0];
check(count(ladderBody, '<tr') === 10, 'ten ladder rows exact', `found ${count(ladderBody, '<tr')}`);
const freeValues = ['Free</td>', 'Free</td>', 'Free. Finishing it opens the licence</td>', 'Free, anyone</td>'];
check(freeValues.every((value, index) => index < 2 ? count(home, value) >= 2 : home.includes(value)), 'four free ladder values present');
const paidValues = [
  '$200 / month, first month free, compute excluded',
  '$600, founding cohort',
  '$3,500, introductory',
  '$10,000 to $15,000 / month',
  '$15,000 to $25,000 / month'
];
check(paidValues.every(value => home.includes(value)), 'five paid price values exact');
check(home.includes('Included, after the Intensive or with a licence'), 'The Room row exact');
check(!sourcePaths.some(file => source[file].includes('$1,000')), '$1,000 absent from visitor copy');

const attrPattern = /(?:href|src)="([^"]+)"/g;
const relativeHome = [];
for (const match of home.matchAll(attrPattern)) {
  const value = match[1];
  if (!value.startsWith('/') && !value.startsWith('#') && !/^[a-z][a-z0-9+.-]*:/i.test(value)) relativeHome.push(value);
}
check(relativeHome.length === 14, 'home has 14 relative same-origin links', `found ${relativeHome.length}: ${relativeHome.join(', ')}`);
check(count(home, '<a class="card door-card"') === 2, 'home door anchors retain card and door-card classes', `found ${count(home, '<a class="card door-card"')}`);
check(home.includes('<h2 class="door-card__label">I\'m employed here.</h2>') && home.includes('<h2 class="door-card__label">It\'s my business.</h2>'), 'home door labels are H2 headings');
check(home.includes('<caption class="visually-hidden">The whole offer</caption>'), 'home offer table has exact accessible caption');

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

const deepBaselines = {
  'workforce.html': 'f03e8d6e982bcfe8f787e7ade9e4279c59fc53e06f1d2d8752c8852152c39f2e',
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
  check(html.includes('Internal review candidate') && html.includes('Build 5R-20260830-c672062f') && html.includes('Unlisted and crawl-blocked, not private.'), `${file} visible immutable review stamp`);
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
