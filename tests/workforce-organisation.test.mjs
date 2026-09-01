import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const page = readFileSync(new URL('../workforce.html', import.meta.url), 'utf8');
const teamSection = page.slice(
  page.indexOf('<section class="section section--surface" id="the-team">'),
  page.indexOf('<section class="section section--accent" id="cta">'),
);
const chartStyles = page.slice(
  page.indexOf('/* ---- Organisation map ---- */'),
  page.indexOf('/* ---- function blocks + role cards ---- */'),
);

test('maps the workforce as a grouped organisation', () => {
  assert.match(teamSection, /class="organisation-chart(?:\s|")/);
  assert.match(teamSection, /Enterprise Leadership &amp; Governance/);
  assert.match(teamSection, /Product, Growth &amp; Customer/);
  assert.match(teamSection, /Technology, Delivery &amp; Experience/);

  for (const team of [
    'Executive Leadership',
    'Corporate Development',
    'Finance',
    'Legal &amp; Compliance',
    'Human Resources',
    'IT Governance',
    'Personal Staff',
    'Product &amp; Strategy',
    'Marketing',
    'Sales',
    'Customer Success',
    'Development',
    'Data Science',
    'Operations',
    'Architecture',
    'Design',
  ]) {
    assert.match(teamSection, new RegExp(`<li>${team}</li>`));
  }

  assert.doesNotMatch(teamSection, /Corp Dev/);
  assert.doesNotMatch(teamSection, /class="org-tile"/);
});

test('keeps the detailed team directory beneath the organisation map', () => {
  assert.match(teamSection, /id="team-directory-title">Explore every team and its specialists\./);
  assert.match(teamSection, /data-workforce-view="specialist-roster"/);
  assert.match(teamSection, /<h3>Development<\/h3>/);
  assert.equal([...teamSection.matchAll(/class="function-block"/g)].length, 16);
  assert.equal([...teamSection.matchAll(/class="roster-row"/g)].length, 102);

  for (const role of [
    'Tech Lead',
    'Frontend Developer',
    'Backend Developer',
    'DevOps Engineer',
    'Quality Assurance Engineer',
    'Automation Engineer',
    'Chief Product Officer',
    'Marketing Director',
    'Legal Director',
    'Personal Assistant',
  ]) {
    assert.match(teamSection, new RegExp(`<h4>${role}(?:<|/)`));
  }

  assert.match(teamSection, /Ask it for:/);
  assert.doesNotMatch(teamSection, /<h3>Corp Dev<\/h3>/);
});

test('uses only defined spacing tokens for the organisation chart', () => {
  assert.match(chartStyles, /\.organisation-chart \{ margin-top: var\(--space-8\); \}/);
  assert.match(chartStyles, /grid-template-columns: repeat\(3, minmax\(0, 1fr\)\); gap: var\(--space-4\);/);
  assert.match(chartStyles, /margin-top: var\(--space-6\); padding: var\(--space-4\);/);
  assert.doesNotMatch(chartStyles, /var\(--space-(?:5|10)\)/);
});
