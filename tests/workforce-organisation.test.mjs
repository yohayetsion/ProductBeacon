import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const page = readFileSync(new URL('../workforce.html', import.meta.url), 'utf8');
const teamSection = page.slice(
  page.indexOf('<section class="section section--surface" id="the-team">'),
  page.indexOf('<section class="section section--accent" id="cta">'),
);
const mapStyles = page.slice(
  page.indexOf('/* ---- Organisation map ---- */'),
  page.indexOf('/* ---- NEW: skills & libraries richness'),
);
const directory = teamSection.slice(teamSection.indexOf('data-workforce-view="team-directory"'));

const teams = [
  ['Executive Leadership', 'Sets direction and makes the trade-offs that shape everything below.'],
  ['Corporate Development', "Deals, investments, and the partnerships that change your company's shape."],
  ['Finance', 'Keeps the numbers honest and the decisions paid for.'],
  ['Legal &amp; Compliance', 'First-pass drafting and triage on the things that usually make you wait days for an answer.'],
  ['Human Resources', 'Hiring, onboarding, performance, and pay: drafted and structured, decided by you.'],
  ['IT Governance', 'Keeps systems, data, and security policies in order as you grow.'],
  ['Personal Staff', 'Your own office: daily support and research on call.'],
  ['Product &amp; Strategy', 'Decides what to build, how to position it, and where to place your bets.'],
  ['Marketing', 'A full marketing department, on call.'],
  ['Sales', 'The motion that turns interest into signed business.'],
  ['Customer Success', 'Keeps customers after you win them.'],
  ['Development', 'Builds, tests, deploys, and improves the software behind the product.'],
  ['Data Science', 'Turns what is happening in your business into something you can act on.'],
  ['Operations', 'Makes sure the work actually ships and keeps shipping.'],
  ['Architecture', 'The technical calls that keep what you build sound, secure, and ready to scale.'],
  ['Design', 'Makes the work come out looking like a real studio produced it.'],
];

test('presents one complete organisation map as grouped static team cards', () => {
  assert.match(teamSection, /class="organisation-map(?:\s|")/);
  assert.match(teamSection, /Enterprise Leadership &amp; Governance/);
  assert.match(teamSection, /Product, Growth &amp; Customer/);
  assert.match(teamSection, /Technology, Delivery &amp; Experience/);
  assert.equal([...teamSection.matchAll(/class="organisation-map__group"/g)].length, 3);
  assert.equal([...teamSection.matchAll(/class="team-card"/g)].length, 16);

  for (const [team, description] of teams) {
    assert.match(teamSection, new RegExp(`<h4>${team}<\\/h4>`));
    assert.match(teamSection, new RegExp(description.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  }

  assert.doesNotMatch(teamSection, /Corp Dev/);
});

test('removes the duplicate chart, specialist roster, and expandable controls', () => {
  assert.doesNotMatch(teamSection, /organisation-chart/);
  assert.doesNotMatch(teamSection, /specialist-roster/);
  assert.doesNotMatch(teamSection, /workforce-roster/);
  assert.doesNotMatch(teamSection, /<details\b/);
  assert.doesNotMatch(teamSection, /<summary\b/);
  assert.doesNotMatch(teamSection, /roster-row/);
  assert.doesNotMatch(teamSection, /Ask it for:/);
});

test('puts a complete, static team directory below the organisation map', () => {
  assert.ok(teamSection.indexOf('data-workforce-view="organisation-map"') < teamSection.indexOf('data-workforce-view="team-directory"'));
  assert.match(teamSection, /class="team-directory(?:\s|")/);
  assert.doesNotMatch(teamSection, /class="team-directory fade-in"/);
  assert.equal([...directory.matchAll(/class="team-directory__branch"/g)].length, 3);
  assert.equal([...directory.matchAll(/class="team-directory__team"/g)].length, 16);
  assert.equal([...directory.matchAll(/class="agent-row"/g)].length, 102);

  for (const [team, description] of teams) {
    assert.match(directory, new RegExp(`<h4>${team}<\\/h4>`));
    assert.match(directory, new RegExp(description.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  }

  for (const [agent, description] of [
    ['Chief Product Officer', 'The senior product voice: strategy, portfolio, and the hardest calls.'],
    ['Marketing Director', 'Runs the marketing org and its budget calls.'],
    ['Finance Director', 'Runs the finance function day to day.'],
    ['Legal Director', 'Runs the legal drafting-and-triage work, under supervised terms.'],
    ['Chief Architect', 'Holds the technical big picture together.'],
    ['Tech Lead', 'Technical direction, code quality, and cross-team delivery.'],
    ['Sales Director', 'Pipeline, quota, and the sales operating rhythm.'],
    ['Personal Assistant', 'Day-to-day support.'],
  ]) {
    assert.match(directory, new RegExp(`<h5>${agent}<\\/h5>`));
    assert.match(directory, new RegExp(description.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  }

  assert.doesNotMatch(directory, /<details\b/);
  assert.doesNotMatch(directory, /<summary\b/);
  assert.doesNotMatch(directory, /Ask it for:/);
  assert.doesNotMatch(directory, /You stay in control of:/);
});

test('lays out the detailed directory as responsive team panels with quiet agent rows', () => {
  assert.match(mapStyles, /\.team-directory__teams \{ display: grid; grid-template-columns: repeat\(2, minmax\(0, 1fr\)\); gap: var\(--space-6\); align-items: start; \}/);
  assert.match(mapStyles, /\.agent-row \{ padding: var\(--space-4\); border-top: 1px solid var\(--border\); \}/);
  assert.match(mapStyles, /@media \(max-width: 639px\) \{[\s\S]*?\.team-directory__teams \{ grid-template-columns: 1fr; \}/);
});

test('uses the existing spacing tokens for the organisation map and responsive group layout', () => {
  assert.match(mapStyles, /\.organisation-map \{ margin-top: var\(--space-8\); \}/);
  assert.match(mapStyles, /grid-template-columns: repeat\(3, minmax\(0, 1fr\)\); gap: var\(--space-6\);/);
  assert.match(mapStyles, /grid-template-columns: repeat\(2, minmax\(0, 1fr\)\);/);
  assert.match(mapStyles, /@media \(max-width: 1199px\) \{[\s\S]*?\.organisation-map__groups \{ grid-template-columns: 1fr; gap: 0; \}/);
  assert.match(mapStyles, /@media \(max-width: 639px\) \{[\s\S]*?\.organisation-map__teams \{ grid-template-columns: 1fr; \}/);
  assert.doesNotMatch(mapStyles, /var\(--space-(?:5|10)\)/);
});
