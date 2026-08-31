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

function normalizedText(html) {
  return html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

function sectionByMarker(html, attribute, value) {
  const escaped = value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return (html.match(new RegExp(`<section\\b[^>]*${attribute}="${escaped}"[^>]*>[\\s\\S]*?<\\/section>`)) || [''])[0];
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
  ['G:/My Drive/Claude/context/decisions/2026/DR-2026-422-productbeacon-product-leadership-at-scale-system-hierarchy.md', '5678d7490c9a5b59a7957941cde865b7c6e4c1f5609b0d68488da269910c585e', 'frozen DR-2026-422 hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-product-leadership-at-scale-design-2026-08-30.md', 'f64fa1061d745a1abcac527d10fdd04ecf287d87aecb4a2c39a463d36cc1e069', 'frozen Product Leadership design hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-product-leadership-at-scale-copy-contract-2026-08-30.md', '86ad001d1897a7082c9c6f7c3614bff34cfe8d94f73ff60368b58e30f2925f99', 'frozen Product Leadership copy contract hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-product-leadership-at-scale-design-handoff-2026-08-30.md', '67bdcd16ab16fad2a2990b4e6f0c88b7797c022e22d49cd63d7d5421baf8de7d', 'frozen Product Leadership design handoff hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-product-leadership-at-scale-implementation-plan-2026-08-30.md', '41e1bad9c7a64baeefa9a546883dbe2226fd1440e625b4a6726d6b3b7b337ead', 'frozen Product Leadership implementation plan hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-plas-route-merge-and-ledger-copy-contract-delta-2026-08-30.md', '2768af2c2280699e2ba1ffccd55d96f8c3093b90ddd53e1ab63cd59d60a31b54', 'frozen route-merge copy contract delta hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-plas-route-merge-and-ledger-design-delta-2026-08-30.md', '34a0e56c84d19af6a7ae318409e09d43e1bbebcb3dc4aa2f0a43115cb2a3e42d', 'frozen route-merge design delta hash'],
  ['G:/My Drive/Claude/ProductBeacon/Marketing/phase5r/relook/phase5r-plas-route-merge-reconciliation-2026-08-30.md', '34bc71dc86c350130e08f92b0fd24dde72ed67a3c98e165411dc32d3e3faeab7', 'frozen route-merge reconciliation hash']
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

const entrySections = ['leadership-hero', 'leadership-stakes', 'value-loop-blueprint', 'system-map', 'responsibility-routes', 'workforce-proof'];
check(home.includes('<main id="main-content" class="entry-main" data-phase5r-page="entry" tabindex="-1">'), 'entry main marker exact');
check(entrySections.every(value => count(home, `data-phase5r-section="${value}"`) === 1) && count(home, 'data-phase5r-section=') === entrySections.length, 'entry section markers exact once');
check(count(home, 'data-phase5r-section="workforce-ledger"') === 0 && count(home, 'data-phase5r-section="human-leadership-services"') === 0, 'the standalone Ledger section and the redundant closing band are gone');
check(count(home, 'ledger-rail') === 0 && count(home, 'ledger-row') === 0 && count(home, 'ledger-action') === 0 && count(home, 'data-ledger-item') === 0 && count(home, 'human-close') === 0, 'their markup and CSS are gone with them');
check(strictlyIncreasing(markerPositions(home, 'data-phase5r-section', entrySections)), 'entry section markers ordered');
const entryHero = (home.match(/<[^>]+data-phase5r-section="leadership-hero"[\s\S]*?<\/section>/) || [''])[0];
check(count(entryHero, '<h1') === 1 && count(home, '<h1') === 1, 'entry single H1 inside hero');
check(!/(\$|\/ month|first month|compute excluded|finish it and the licence opens)/i.test(visibleText(entryHero)), 'entry hero has no price or access-condition tokens');
check(entryHero.includes('href="#choose-your-route"') && entryHero.includes('href="/workforce.html"'), 'entry hero primary and Workforce routes');
check(visibleText(entryHero).includes('Choose your route'), 'entry hero primary CTA label exact');
check(visibleText(entryHero).includes('Product Leadership, At Scale.'), 'entry hero H1 exact');
check(/<h1 id="home-title"><span class="hero-lead">Product Leadership,<\/span> At Scale\.<\/h1>/.test(home), 'entry hero keeps Leadership on the first line');
check(/\.hero-lead\s*\{[^}]*white-space:\s*nowrap/s.test(home), 'the hero lead phrase is held on one line by CSS');

const systemLayers = ['blueprint', 'decision-infrastructure', 'workforce-editions', 'operating-foundation'];
check(systemLayers.every(value => count(home, `data-system-layer="${value}"`) === 1), 'four system layers exact once');
check(count(home, 'data-workforce-edition="one-product-team"') === 1 && count(home, 'data-workforce-edition="full-enterprise"') === 1, 'two workforce editions exact once');
check(count(home, 'data-human-decision-seam') === 1, 'system map human decision seam exact once');
const responsibilityRoutes = ['run-one-product-team', 'extend-across-the-enterprise', 'productbeacon-carries-the-outcome'];
check(responsibilityRoutes.every(value => count(home, `data-route="${value}"`) === 1), 'three responsibility routes exact once');
check(count(home, 'data-proof-kind="workforce-delivery"') === 2, 'two workforce delivery proof artifacts exact');
check(count(home, 'data-proof-kind="workforce-operating-record"') === 1, 'the Ledger sits inside the proof section as one operating-record artifact');
const responsibilitySection = sectionByMarker(home, 'data-phase5r-section', 'responsibility-routes');
const proofSection = sectionByMarker(home, 'data-phase5r-section', 'workforce-proof');
check(count(home, 'data-phase5r-section="ways-to-use"') === 0 && count(home, 'class="use-card"') === 0 && count(home, 'use-card__') === 0 && count(home, 'id="ways-to-use"') === 0, 'merged: the duplicate ways-to-use section and its cards are gone');
check(count(home, '#ways-to-use') === 0, 'merged: no link anywhere still targets the removed anchor');
check(count(home, 'class="use-grid"') === 0 && count(home, '.use-grid') === 0 && count(home, '.route-heading') === 0 && count(home, 'class="route-heading"') === 0, 'merged: dead use-grid and route-heading rules removed');
check(Boolean(responsibilitySection) && responsibilitySection.includes('id="choose-your-route"') && count(responsibilitySection, 'data-route=') === 3, 'responsibility routes are a separate anchored section');
check(count(home, 'class="door-grid"') === 1 && count(home, 'data-route=') === 3, 'exactly one three-card grid remains on the homepage');
check(count(proofSection, 'data-proof-class="finished-delivery"') === 1, 'the proof section is marked as the finished-delivery class');
check(count(proofSection, 'class="report-proof"') === 3, 'the proof section carries exactly three artifacts');
const ledgerCard = (proofSection.match(/<article\b[^>]*data-proof-kind="workforce-operating-record"[\s\S]*?<\/article>/) || [''])[0];
const ledgerCardExact = [
  'The operating record',
  'The Governed Workforce Ledger',
  'The recurring record of how the governed workforce actually ran: what it produced, which decisions a named human affirmed, and what was sent back. Published on the ProductBeacon LinkedIn page.',
  'Read the latest Ledger'
];
check(Boolean(ledgerCard), 'the Ledger proof card is present');
check(Boolean(ledgerCard) && ledgerCardExact.every(value => visibleText(ledgerCard).includes(value)), 'Ledger proof card copy exact', ledgerCardExact.filter(value => !visibleText(ledgerCard).includes(value)).join(' | '));
check(Boolean(ledgerCard) && ledgerCard.includes('src="/ledger/july-2026-cover.png"') && /alt="Cover of the Governed Workforce Ledger, Issue 02, July 2026"/.test(ledgerCard), 'the Ledger card shows the latest published cover, described');
check(Boolean(ledgerCard) && count(ledgerCard, 'href="https://www.linkedin.com/posts/productbeacon_the-governed-workforce-ledger-activity-7493372347987701760--rBa"') === 1 && count(ledgerCard, '<a ') === 1, 'the Ledger card has exactly one link and it is the published issue');
check(Boolean(ledgerCard) && !/\d/.test(visibleText(ledgerCard)), 'the Ledger card copy states no figure of any kind', visibleText(ledgerCard));
check(Boolean(ledgerCard) && !/target="_blank"|href="#"|aria-disabled/.test(ledgerCard), 'the Ledger card has no placeholder, disabled or new-window control');
// Issue 01 (June) and Issue 02 (July) are both published, so naming the latest
// issue is now accurate. What must still never appear is a cadence claim the
// LinkedIn page cannot evidence on the day a reader arrives, or a reference to
// an issue that has not gone out.
check(!/published every month|monthly since|every month since|Issue 03/i.test(visibleText(home)), 'the homepage makes no cadence claim and names no unpublished issue');
const exactRouteCards = [
  {
    id: 'run-one-product-team',
    href: '/only-product-person/',
    mode: 'One Product team',
    modeSlug: 'one-product-team',
    heading: 'I lead Product inside a company.',
    body: 'For product leaders, product department heads, and the only Product person. Begin with one Product team and grow from there.',
    cta: 'See my Product route'
  },
  {
    id: 'extend-across-the-enterprise',
    href: '/covering-everything/',
    mode: 'The wider workforce',
    modeSlug: 'the-wider-workforce',
    heading: 'I carry several functions or clients.',
    body: 'For founders, operators, solo executives, fractional leaders, and services owners. Begin with the wider workforce.',
    cta: 'See my operator route'
  },
  {
    id: 'productbeacon-carries-the-outcome',
    href: '/on-call.html',
    mode: 'ProductBeacon operated',
    modeSlug: 'productbeacon-operated',
    heading: 'I want ProductBeacon to carry the work.',
    body: 'For commissioned work or product leadership capacity without operating the workforce yourself.',
    cta: 'See On Call &amp; Fractional'
  }
];
for (const route of exactRouteCards) {
  const card = (responsibilitySection.match(new RegExp(`<a\\b[^>]*data-route="${route.id}"[^>]*>[\\s\\S]*?<\\/a>`)) || [''])[0];
  check(Boolean(card) && card.includes(`href="${route.href}"`), `route ${route.id} whole-surface link and target exact`);
  check(Boolean(card) && normalizedText(card) === `${route.mode} ${route.heading} ${route.body} ${route.cta}`, `route ${route.id} contains only contracted copy`, normalizedText(card));
  check(Boolean(card) && count(card, `data-operating-mode="${route.modeSlug}"`) === 1, `route ${route.id} carries its operating-mode marker exactly once`);
  check(Boolean(card) && new RegExp(`<span class="route-card__mode">${route.mode}</span>`).test(card), `route ${route.id} mode label is sentence-case in the DOM`);
}
check(/\.route-card:active\s*\{[^}]*transform:\s*none[^}]*border-color:\s*var\(--amber-dim\)/s.test(home), 'responsibility routes define contracted pressed state');
check(count(home, 'data-operating-mode=') === 3 && count(responsibilitySection, 'data-operating-mode=') === 3, 'three operating-mode labels, all inside the route section');
check(/\.route-card__mode\s*\{[^}]*text-transform:\s*uppercase/s.test(home), 'operating-mode labels are uppercased by CSS, not by the DOM');
check(/\.route-card__mode\s*\{[^}]*color:\s*var\(--secondary\)/s.test(home), 'operating-mode labels use secondary, keeping amber for action');
check(count(home, 'id="intensive"') === 1 && /id="intensive"[^>]*data-operating-mode="the-wider-workforce"|data-operating-mode="the-wider-workforce"[^>]*id="intensive"/.test(home), 'the frozen Operator Intensive nav target resolves to the wider-workforce route card');
check(/<a[^>]*data-route="extend-across-the-enterprise"[^>]*id="intensive"|<a[^>]*id="intensive"[^>]*data-route="extend-across-the-enterprise"/.test(home), 'the Operator Intensive anchor lands on a focusable link');
check(!home.includes('data-offer-journey=') && !home.includes('data-router-step='), 'legacy journey and questionnaire structure absent');
check(!home.includes('class="offer-table"'), 'old offer table absent');
check(!/(testimonial|customer-logo|review-score|performance-result)/i.test(entryHero), 'hero contains no invented proof component');
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
  'Get the free product team'
];
check(!/LANTERN/i.test(doorOne), 'Door 1 no longer carries the LANTERN prompt');
check(count(doorOne, 'door-optional') === 0, 'the optional-prompt paragraph is gone with it');
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

const workforceStory = ['role-based-specialists', 'governed-spawn', 'full-harness', 'human-decision-seam', 'loop-and-learn', 'distributed-company-brain'];
check(/<main\b[^>]*id="main-content"[^>]*data-phase5r-page="workforce"[^>]*>/.test(workforce), 'Workforce main marker exact');
check(workforceStory.every(value => count(workforce, `data-workforce-story="${value}"`) === 1), 'six Workforce story markers exact once');
check(strictlyIncreasing(markerPositions(workforce, 'data-workforce-story', workforceStory)), 'Workforce story markers ordered');
check(workforceStory.every(value => workforce.indexOf(`data-workforce-story="${value}"`) < workforce.indexOf('data-workforce-view="team-map"')), 'Workforce story precedes team map');
check(count(workforce, 'data-workforce-view="team-map"') === 1 && count(workforce, 'data-workforce-view="specialist-roster"') === 1, 'one Workforce team map and one specialist roster');
check(workforce.indexOf('data-workforce-view="team-map"') < workforce.indexOf('data-workforce-view="specialist-roster"'), 'Workforce team map precedes roster');
check(!visibleText(workforce).includes('Here is what you ask for, and here is what comes back.'), 'old request-output heading absent');
check(!visibleText(workforce).includes('From request to deliverable.'), 'old request-to-deliverable heading absent');

const roleLayers = ['identity', 'remit', 'skills', 'knowledge', 'boundaries'];
check(roleLayers.every(value => count(workforce, `data-role-layer="${value}"`) === 1), 'five role layers exact once');
check(count(workforce, 'data-harness-step') === 7, 'seven governed spawn steps exact');
const loopSteps = ['frame', 'plan', 'execute', 'audit', 'review', 'record'];
check(loopSteps.every(value => count(workforce, `data-loop-step="${value}"`) === 1), 'Loop and Learn steps exact once');
check(strictlyIncreasing(markerPositions(workforce, 'data-loop-step', loopSteps)), 'Loop and Learn steps ordered');
check(count(workforce, 'data-human-gate="frame"') === 1 && count(workforce, 'data-human-gate="review"') === 1, 'Loop and Learn human gates exact');
const memoryRecords = ['decisions', 'bets', 'assumptions', 'feedback', 'learnings', 'documents'];
check(memoryRecords.every(value => count(workforce, `data-memory-record="${value}"`) === 1), 'Distributed Company Brain records exact once');
check(count(workforce, 'data-human-gate') >= 3 && /Only the named accountable owner can affirm it closed/.test(workforce), 'visible human gates preserved across run, DPS and loop');

const teamMap = (workforce.match(/<[^>]+data-workforce-view="team-map"[\s\S]*?<\/section>/) || [''])[0];
const roster = (workforce.match(/<[^>]+data-workforce-view="specialist-roster"[\s\S]*?<\/section>/) || [''])[0];
check(count(teamMap, 'class="org-tile"') === 15, 'Workforce team map has 15 tiles', `found ${count(teamMap, 'class="org-tile"')}`);
check(count(teamMap, 'class="role-card"') === 0, 'Workforce team map has no role cards');
check(count(roster, 'class="function-block"') === 15, 'Workforce roster has 15 function blocks', `found ${count(roster, 'class="function-block"')}`);
check(count(roster, 'class="roster-row"') === 96, 'Workforce roster has 96 specialist rows', `found ${count(roster, 'class="roster-row"')}`);
const mapIdentity = [...teamMap.matchAll(/<a class="org-tile" href="#([^"]+)"><h3>([\s\S]*?)<\/h3>/g)]
  .map(match => ({ id: match[1], team: normalizedText(match[2]) }));
const rosterIdentity = [...roster.matchAll(/<div class="function-block" id="([^"]+)">([\s\S]*?)(?=\s*<div class="function-block" id="|\s*<\/section>)/g)]
  .map(match => ({
    id: match[1],
    team: normalizedText((match[2].match(/<h3>([\s\S]*?)<\/h3>/) || ['', ''])[1]),
    specialists: [...match[2].matchAll(/<details class="roster-row"><summary><h4>([\s\S]*?)<\/h4>/g)].map(role => normalizedText(role[1]))
  }));
const rosterIdentityHash = sha(Buffer.from(JSON.stringify({ map: mapIdentity, roster: rosterIdentity }), 'utf8'));
check(rosterIdentityHash === 'fe060d5c41c6dad33ff574e262f23adcea9fb26e5c90f44f176ecec25fc01035', 'Workforce ordered team and specialist identity hash exact', rosterIdentityHash);
check(mapIdentity.every((team, index) => rosterIdentity[index] && team.id === rosterIdentity[index].id && team.team.replace(/\s*Supervised$/, '') === rosterIdentity[index].team.replace(/\s*Available under supervised terms$/, '')), 'Workforce team map and roster identities align in order');
check(workforce.includes('id="the-skills"') && !workforce.includes('id="skills-grid"') && !workforce.includes('id="libs-grid"'), 'compact depth proof replaces exhaustive catalogue');
check(/qualified human|qualified professional/i.test(visibleText(workforce)) && /not legal advice/i.test(visibleText(workforce)), 'Workforce supervised-domain boundary retained');
check(!workforce.includes("'IntersectionObserver' in window || true") && !workforce.includes('[data-expand-target]'), 'dead catalogue controller code absent');
check(!workforce.includes('style="margin-top:48px"') && !/\.skip-link\s*\{[^}]*padding:\s*12px 18px/s.test(workforce), 'Workforce live spacing literals replaced with tokens');
const memoryCore = (workforce.match(/<div class="memory-core"[^>]*>([\s\S]*?)<\/div><p class="diagram-caption">/) || ['', ''])[1];
check(count(memoryCore, 'class="memory-node"') === 4 && count(memoryCore, 'class="route-arrow"') === 3, 'Distributed Company Brain has four stages and three arrows');
check(/\.memory-core\s*\{[^}]*grid-template-columns:\s*minmax\(0,\s*1fr\)\s+auto\s+minmax\(0,\s*1fr\)\s+auto\s+minmax\(0,\s*1fr\)\s+auto\s+minmax\(0,\s*1fr\)/s.test(workforce), 'Distributed Company Brain desktop rail declares seven intentional tracks');

const forbiddenClaims = [
  'every request becomes a team', 'router always finds', 'never re-explain your business',
  'every session makes the system smarter', 'model retrains itself', 'automatically gets smarter',
  'full harness guarantees', 'guaranteed correct', 'replaces your lawyer',
  'you can audit', 'anyone can audit', 'audit each one', 'audit our records',
  'replaces a human team', 'licensed professional agent'
];
const visitorText = `${normalizedText(home)} ${normalizedText(workforce)}`.toLowerCase();
check(forbiddenClaims.every(fragment => !visitorText.includes(fragment)), 'forbidden public claim fragments absent');

const negativeCopy = [
  'Inspect Product Org OS',
  'Inspect it. Learn it. Run it. Or hand ProductBeacon the work.',
  'Finished in hours instead of weeks',
  'The middle runs itself',
  'The model learns from every run',
  'Every session makes the AI smarter',
  'The system remembers everything',
  'Every agent can access the whole company brain',
  'Every request becomes a team',
  'The Audit Block proves the answer is correct',
  'Human review makes errors impossible',
  'Use the system at the level you want to own.',
  'Start with one Product team, extend the workforce across the company, or ask ProductBeacon to carry the outcome with you.',
  'See the Product team route',
  'See the wider workforce route',
  'Choose how to use it',
  'before choosing a route',
  'Issue 02',
  'latest issue',
  'published every month',
  'monthly since'
];
check(negativeCopy.every(fragment => !visitorText.includes(fragment.toLowerCase())), 'negative-copy manifest absent');

// Homepage-scoped only. The route-merge delta section 10.1 is explicit that
// 'Run one Product team' and 'Extend beyond Product' remain valid CTA labels in
// the Workforce page's final action, so these must never be checked across both
// pages the way the shared manifest above is.
const homepageNegativeCopy = [
  'Choose the responsibility',
  'Run one Product team.',
  'Extend beyond Product.',
  'Have ProductBeacon carry the outcome.',
  'Open Product Org OS',
  'one human',
  'one named human',
  'Read the Ledger'
];
const homepageText = normalizedText(home).toLowerCase();
check(homepageNegativeCopy.every(fragment => !homepageText.includes(fragment.toLowerCase())), 'homepage-scoped negative copy absent', homepageNegativeCopy.filter(fragment => homepageText.includes(fragment.toLowerCase())).join(' | '));
check(count(visibleText(home), 'A named human remains accountable.') === 1 && visibleText(home).includes('ProductBeacon keeps a named human at the centre'), 'the homepage says a named human, never one named human');
check(visibleText(home).includes('You can read the work and its supporting method before you decide.'), 'report aside no longer assumes the routes come after it');
const homeMain = (home.match(/<main\b[\s\S]*?<\/main>/) || [''])[0];
const expectedHrefCounts = [
  ['#choose-your-route', 1], ['#ways-to-use', 0],
  ['/only-product-person/', 1], ['/covering-everything/', 1], ['/on-call.html', 1],
  ['/workforce.html', 2], ['https://github.com/yohayetsion/product-org-os', 2],
  ['/vision-to-value/', 3], ['/decision-provenance-standard.html', 2],
  ['/research/state-of-cyber-2026/', 1], ['/research/state-of-wfo-2026/', 1],
  ['/research/', 1], ['/contact.html', 1],
  ['https://www.linkedin.com/posts/productbeacon_the-governed-workforce-ledger-activity-7493372347987701760--rBa', 1]
];
expectedHrefCounts.forEach(([target, expected]) => {
  const actual = count(homeMain, `"${target}"`);
  check(actual === expected, `homepage main carries ${expected} link(s) to ${target}`, `found ${actual}`);
});
const homeLd = (home.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/) || ['',''])[1];
check(Boolean(homeLd), 'homepage carries structured data');
let homeGraph = null;
try { homeGraph = JSON.parse(homeLd); } catch (error) { failures.push(`homepage structured data is not valid JSON: ${error.message}`); }
if (homeGraph) {
  const nodes = homeGraph['@graph'] || [];
  const org = nodes.find(node => node['@type'] === 'Organization');
  const person = nodes.find(node => node['@type'] === 'Person');
  check(Boolean(org) && org['@id'] === 'https://productbeacon.agency/#productbeacon' && Boolean(org.logo), 'organisation node carries an identifier and a logo');
  check(Boolean(org) && Array.isArray(org.sameAs) && org.sameAs.includes('https://www.linkedin.com/company/productbeacon') && org.sameAs.includes('https://www.linkedin.com/in/yohayetsion/'), 'organisation node ties both LinkedIn identities to the practice');
  check(Boolean(person) && person['@id'] === 'https://productbeacon.agency/#yohay-etsion' && Boolean(org) && org.founder && org.founder['@id'] === person['@id'], 'the founder link resolves to the person node');
  check(!JSON.stringify(homeGraph).includes('governed operator') && !JSON.stringify(homeGraph).includes('professional-services firms'), 'structured data carries the current positioning, not the superseded one');
}
check(!/\u2014/.test(visibleText(home)), 'homepage visible copy carries no em dash');
check(!/250 ready-made skills|120 knowledge libraries/.test(visibleText(workforce)), 'the retired unreconcilable skill and library counts are gone');
check(visibleText(workforce).includes('over 300 ready-made skills and knowledge libraries'), 'the Workforce page states one reconcilable combined figure');
check(!/(\$\s*[\d,]+|\d+\s*\/\s*month|first month free)/i.test(`${visibleText(home)} ${visibleText(workforce)}`), 'homepage and Workforce narrative contain no prices');
check(!/(--space-5\b|--space-10\b)/.test(`${home}\n${workforce}`), 'undefined spacing tokens absent from source pages');
check(sourcePaths.every(file => !/(href|src|action)="\/internal\//.test(source[file])), 'production source has no internal links', sourcePaths.filter(file => /(href|src|action)="\/internal\//.test(source[file])).join(', '));

const workforceMarker = '<!-- Provenance: DR-2026-422; Product Leadership, At Scale Workforce candidate approved for review by Yohay Etsion 2026-08-30. -->';
check(count(workforce, workforceMarker) === 1, 'workforce DR-2026-422 provenance marker exact once', `found ${count(workforce, workforceMarker)}`);

for (const file of ['research/index.html', 'on-call.html']) {
  check(count(source[file], marker) === 1, `${file} D8 marker exact once`, `found ${count(source[file], marker)}`);
  check(count(source[file], '<a class="skip-link" href="#main-content">Skip to main content</a>') === 1, `${file} has one source skip link`);
  check(/<main\b[^>]*id="main-content"[^>]*tabindex="-1"[^>]*>/.test(source[file]), `${file} has focusable main target`);
  check(/@media\s*\(prefers-reduced-motion:\s*reduce\)\s*\{[\s\S]*?transition:\s*none\s*!important[\s\S]*?transform:\s*none\s*!important/.test(source[file]), `${file} source reduced-motion controls exact`);
}
check(/@media\s*\(max-width:\s*639px\)\s*\{[\s\S]*?\.start-here-grid[^}]*grid-template-columns:\s*minmax\(0,\s*1fr\)/.test(source['research/index.html']), 'Research start-here grids explicitly reflow at 320px');
check(/\.email-action\s*\{[^}]*white-space:\s*normal[^}]*overflow-wrap:\s*anywhere/s.test(source['on-call.html']), 'On Call email action can wrap inside 320px gutter');

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
  check(html.includes('Internal review candidate') && html.includes('Build 5R-PLAS-ROUTEMERGE-20260830-DR425') && html.includes('Unlisted and crawl-blocked, not private.'), `${file} visible immutable review stamp`);
  check(!/(googletagmanager|\bgtag\s*\(|\bpbTrack\b|\bdataLayer\b|linkedin_partner|snap\.licdn)/i.test(html), `${file} tracking stripped`);
  const attrs = [...html.matchAll(/(?:href|src|action)="([^"]+)"/g)].map(match => match[1]);
  const relative = attrs.filter(value => !value.startsWith('/') && !value.startsWith('#') && !/^[a-z][a-z0-9+.-]*:/i.test(value));
  check(relative.length === 0, `${file} contains no relative same-origin links`, relative.join(', '));
  const escapedInSet = attrs.filter(value => ['/index.html', '/only-product-person/', '/covering-everything/', '/workforce.html', '/research/', '/on-call.html'].some(route => value === route || value.startsWith(`${route}#`) || value.startsWith(`${route}?`)));
  check(escapedInSet.length === 0, `${file} in-set links remain inside review prefix`, escapedInSet.join(', '));
  check(html.includes('data-phase5r-review-anchor-behavior="capture"'), `${file} review contains capture-phase reduced-motion anchor handling`);
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

if (!process.argv.includes('--no-determinism') && fs.existsSync(path.join(reviewRoot, 'build-review.js'))) {
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
