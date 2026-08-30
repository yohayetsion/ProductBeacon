#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const reviewRoot = __dirname;
const repoRoot = path.resolve(reviewRoot, '..', '..');
const prefix = '/internal/fill-the-rooms-review/';
const buildStamp = '5R-20260830-c672062f';
const sourceCommit = 'c672062f9b626ef13bbdaa6a821d134d54580eda';
const robots = '<meta name="robots" content="noindex, nofollow, noarchive, noai, noimageai">';
const referrer = '<meta name="referrer" content="no-referrer">';

const pages = [
  { source: 'index.html', output: 'index.html', route: '/' },
  { source: 'only-product-person/index.html', output: 'only-product-person/index.html', route: '/only-product-person/' },
  { source: 'covering-everything/index.html', output: 'covering-everything/index.html', route: '/covering-everything/' },
  { source: 'workforce.html', output: 'workforce.html', route: '/workforce.html' },
  { source: 'research/index.html', output: 'research/index.html', route: '/research/' },
  { source: 'on-call.html', output: 'on-call.html', route: '/on-call.html' }
];

const commitPaths = [
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

const routeMap = new Map([
  ['/', prefix],
  ['/index.html', prefix],
  ['/only-product-person/', `${prefix}only-product-person/`],
  ['/only-product-person/index.html', `${prefix}only-product-person/`],
  ['/covering-everything/', `${prefix}covering-everything/`],
  ['/covering-everything/index.html', `${prefix}covering-everything/`],
  ['/workforce.html', `${prefix}workforce.html`],
  ['/research/', `${prefix}research/`],
  ['/research/index.html', `${prefix}research/`],
  ['/on-call.html', `${prefix}on-call.html`]
]);

const reviewStyle = `<style id="phase5r-review-only-style">
  body.review-candidate { padding-top: 36px; }
  body.review-candidate .phase5r-review-banner {
    position: fixed;
    inset: 0 0 auto 0;
    z-index: 10000;
    min-height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px 24px;
    padding: 7px 16px;
    border-bottom: 1px solid #78350F;
    background: #FEF3C7;
    color: #451A03;
    font: 600 12px/1.35 Inter, system-ui, sans-serif;
    text-align: center;
  }
  body.review-candidate .phase5r-review-banner span:nth-child(2) { font-family: "JetBrains Mono", monospace; }
  body.review-candidate .nav { top: 36px; }
  body.review-candidate .section-tabs { top: calc(var(--nav-height, 72px) + 36px); }
  body.review-candidate .skip-link:focus { top: 52px; }
  @media (max-width: 639px) {
    body.review-candidate { padding-top: 48px; }
    body.review-candidate .phase5r-review-banner { min-height: 48px; gap: 2px 12px; padding: 6px 10px; flex-wrap: wrap; }
    body.review-candidate .nav { top: 48px; }
    body.review-candidate .section-tabs { top: calc(var(--nav-height, 72px) + 48px); }
    body.review-candidate .skip-link:focus { top: 64px; }
  }
</style>`;

const reviewBanner = `<aside class="phase5r-review-banner" role="note" aria-label="Internal review status">
  <span>Internal review candidate</span>
  <span>Build ${buildStamp}</span>
  <span>Unlisted and crawl-blocked, not private.</span>
</aside>`;

function sha(bytes) {
  return crypto.createHash('sha256').update(bytes).digest('hex');
}

function countRelativeAttributes(html) {
  return [...html.matchAll(/(?:href|src)="([^"]+)"/g)].filter(match => {
    const value = match[1];
    return !value.startsWith('/') && !value.startsWith('#') && !/^[a-z][a-z0-9+.-]*:/i.test(value);
  }).length;
}

function stripTracking(html) {
  html = html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, block => {
    return /(googletagmanager|\bgtag\b|\bpbTrack\b|\bdataLayer\b|linkedin_partner|snap\.licdn)/i.test(block) ? '' : block;
  });
  html = html.replace(/<!--[\s\S]*?-->/g, block => {
    return /(googletagmanager|\bgtag\b|\bpbTrack\b|\bdataLayer\b|linkedin_partner|snap\.licdn)/i.test(block) ? '' : block;
  });
  html = html.replace(/\s+onclick="[^"]*\bpbTrack\b[^"]*"/gi, '');
  html = html.replace(/\s+onclick='[^']*\bpbTrack\b[^']*'/gi, '');
  return html;
}

function splitUrl(value) {
  const match = value.match(/^([^?#]*)([?#][\s\S]*)?$/);
  return { pathname: match ? match[1] : value, suffix: match && match[2] ? match[2] : '' };
}

function remapRootAbsolute(value) {
  const parts = splitUrl(value);
  return routeMap.has(parts.pathname) ? `${routeMap.get(parts.pathname)}${parts.suffix}` : value;
}

function rewriteAttributeUrl(value, sourceRoute) {
  if (value.startsWith('#') || /^[a-z][a-z0-9+.-]*:/i.test(value) || value.startsWith('//')) return value;
  if (value.startsWith('/')) return remapRootAbsolute(value);
  const base = new URL(sourceRoute, 'https://productbeacon.agency');
  const resolved = new URL(value, base);
  return remapRootAbsolute(`${resolved.pathname}${resolved.search}${resolved.hash}`);
}

function rewriteLinks(html, sourceRoute) {
  return html.replace(/\b(href|src|action)="([^"]+)"/gi, (whole, attribute, value) => {
    return `${attribute}="${rewriteAttributeUrl(value, sourceRoute)}"`;
  });
}

function addReviewDirectives(html) {
  const viewport = /<meta name="viewport"[^>]*>/i;
  if (!viewport.test(html)) throw new Error('review source has no viewport meta');
  html = html.replace(viewport, match => `${match}\n${robots}\n${referrer}`);
  html = html.replace('</head>', `${reviewStyle}\n</head>`);
  html = html.replace(/<body([^>]*)>/i, (whole, attributes) => {
    if (/\bclass="/i.test(attributes)) return `<body${attributes.replace(/class="([^"]*)"/i, 'class="$1 review-candidate"')}>`;
    return `<body${attributes} class="review-candidate">`;
  });
  html = html.replace(/<body[^>]*>/i, match => `${match}\n${reviewBanner}`);
  return html;
}

function buildPage(page) {
  const sourcePath = path.join(repoRoot, page.source);
  let html = fs.readFileSync(sourcePath, 'utf8');
  if (page.source === 'index.html' && countRelativeAttributes(html) !== 14) {
    throw new Error(`home relative-link invariant failed: expected 14, got ${countRelativeAttributes(html)}`);
  }
  html = stripTracking(html);
  html = rewriteLinks(html, page.route);
  html = addReviewDirectives(html);
  const outputPath = path.join(reviewRoot, page.output);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, html, 'utf8');
  return {
    source_path: page.source,
    source_sha256: sha(fs.readFileSync(sourcePath)),
    review_path: `internal/fill-the-rooms-review/${page.output}`,
    review_sha256: sha(Buffer.from(html, 'utf8'))
  };
}

const builtPages = pages.map(buildPage);
const hashedPaths = [
  'internal/fill-the-rooms-review/build-review.js',
  'internal/fill-the-rooms-review/covering-everything/index.html',
  'internal/fill-the-rooms-review/index.html',
  'internal/fill-the-rooms-review/on-call.html',
  'internal/fill-the-rooms-review/only-product-person/index.html',
  'internal/fill-the-rooms-review/phase5r-gate.js',
  'internal/fill-the-rooms-review/research/index.html',
  'internal/fill-the-rooms-review/workforce.html'
];

const manifest = {
  schema_version: 1,
  candidate: 'ProductBeacon Fill the Rooms Phase 5R',
  build_stamp: buildStamp,
  source_commit: sourceCommit,
  review_prefix: prefix,
  transform_command: 'node internal/fill-the-rooms-review/build-review.js',
  commit_paths: commitPaths,
  source_to_review: builtPages,
  files: hashedPaths.map(file => ({ path: file, sha256: sha(fs.readFileSync(path.join(repoRoot, file))) })),
  meta_files: [
    'internal/fill-the-rooms-review/manifest.json',
    'internal/fill-the-rooms-review/manifest.sha256'
  ],
  external_shared_dependencies: [
    '/css/style.css',
    '/js/main.js',
    '/research/favicon-research.svg',
    'https://fonts.googleapis.com',
    'https://fonts.gstatic.com'
  ],
  review_directives: {
    robots: 'noindex, nofollow, noarchive, noai, noimageai',
    referrer: 'no-referrer',
    tracking: 'stripped from review HTML; Web3Forms is the only permitted form processor request'
  }
};

const manifestBytes = Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
fs.writeFileSync(path.join(reviewRoot, 'manifest.json'), manifestBytes);
fs.writeFileSync(path.join(reviewRoot, 'manifest.sha256'), `${sha(manifestBytes)}\n`, 'utf8');
console.log(`Built ${builtPages.length} review pages with stamp ${buildStamp}.`);
console.log(`Manifest SHA-256 ${sha(manifestBytes)}`);
