#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const reviewRoot = __dirname;
const repoRoot = path.resolve(reviewRoot, '..', '..');
const prefix = '/internal/fill-the-rooms-review/';
const buildStamp = '5R-RELOOK-20260830-DR419';
const sourceCommit = 'fe3b677807b97a59b26edd15b5a3499b6eeb2ffc';
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
  body.review-candidate .phase5r-footer-heading,
  body.review-candidate .footer__bottom > span { color: #94A3B8; }
  body.review-candidate .metric__label,
  body.review-candidate .org-tile__roles,
  body.review-candidate .coming-card-label,
  body.review-candidate .coming-card-body { color: #94A3B8 !important; }
  body.review-candidate .split p a { text-decoration: underline; text-underline-offset: 2px; }
  body.review-candidate .phase5r-footer-heading {
    margin-bottom: 16px;
    font-size: .75rem;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
  }
  body.review-candidate .privacy-notice a { text-decoration: underline; text-underline-offset: 2px; }
  body.review-candidate .section-tabs { top: calc(var(--nav-height, 72px) + 36px); }
  body.review-candidate .skip-link:focus { top: 52px; }
  body.review-candidate .course-dialog[open] {
    top: 44px;
    bottom: auto;
    max-height: calc(100vh - 52px);
    margin: 0 auto 8px;
  }
  body.review-candidate .entry-main section { scroll-margin-top: calc(var(--nav-height, 72px) + 60px); }
  body.review-candidate #the-work,
  body.review-candidate #the-team,
  body.review-candidate #the-skills,
  body.review-candidate #role-based,
  body.review-candidate #full-harness,
  body.review-candidate #loop-and-learn,
  body.review-candidate #company-brain,
  body.review-candidate .function-block { scroll-margin-top: calc(var(--nav-height, 72px) + 88px); }
  @media (max-width: 639px) {
    body.review-candidate { padding-top: 48px; }
    body.review-candidate .phase5r-review-banner { min-height: 48px; gap: 2px 12px; padding: 6px 10px; flex-wrap: wrap; }
    body.review-candidate .nav { top: 48px; }
    body.review-candidate .section-tabs { top: calc(var(--nav-height, 72px) + 48px); }
    body.review-candidate .skip-link:focus { top: 64px; }
    body.review-candidate .course-dialog[open] {
      top: 64px;
      max-height: calc(100vh - 72px);
    }
    body.review-candidate .entry-main section { scroll-margin-top: calc(var(--nav-height, 72px) + 72px); }
    body.review-candidate #the-work,
    body.review-candidate #the-team,
    body.review-candidate #the-skills,
    body.review-candidate #role-based,
    body.review-candidate #full-harness,
    body.review-candidate #loop-and-learn,
    body.review-candidate #company-brain,
    body.review-candidate .function-block { scroll-margin-top: calc(var(--nav-height, 72px) + 100px); }
  }
</style>`;

const reviewBanner = `<aside class="phase5r-review-banner" aria-label="Internal review status">
  <span>Internal review candidate</span>
  <span>Build ${buildStamp}</span>
  <span>Unlisted and crawl-blocked, not private.</span>
</aside>`;

const reviewBehavior = `<script id="phase5r-review-only-behavior">
(function(){
  'use strict';
  document.addEventListener('click', function(event) {
    var link = event.target.closest && event.target.closest('a.skip-link[href^="#"]');
    if (!link) return;
    var href = link.getAttribute('href');
    var target = href && document.querySelector(href);
    if (!target) return;
    event.preventDefault();
    event.stopImmediatePropagation();
    if (window.location.hash !== href) window.history.pushState(null, '', href);
    target.focus({ preventScroll: true });
    target.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
  }, true);
  document.addEventListener('submit', function(event) {
    if (!event.target || event.target.id !== 'course-form') return;
    window.requestAnimationFrame(function() {
      var dialog = document.getElementById('course-dialog');
      if (dialog && dialog.open && dialog.querySelector('[aria-invalid="true"]')) dialog.scrollTop = 0;
    });
  }, true);
})();
</script>`;

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

function addReviewDirectives(html, source) {
  const viewport = /<meta name="viewport"[^>]*>/i;
  if (!viewport.test(html)) throw new Error('review source has no viewport meta');
  if (source === 'on-call.html') {
    html = html.replace('</nav>', '</nav>\n<main id="main-content" tabindex="-1">');
    html = html.replace(/<footer\b/i, '</main>\n<footer');
    html = html
      .replace(/<h4([^>]*)>Engagement Details<\/h4>/gi, '<h3$1>Engagement Details</h3>');
  }
  html = html.replace(/<footer\b[^>]*class="[^"]*\bfooter\b[^"]*"[^>]*>[\s\S]*?<\/footer>/gi, footer => {
    return footer
      .replace(/<h4>/gi, '<p class="phase5r-footer-heading">')
      .replace(/<\/h4>/gi, '</p>');
  });
  html = html.replace(viewport, match => `${match}\n${robots}\n${referrer}`);
  html = html.replace('</head>', `${reviewStyle}\n</head>`);
  html = html.replace(/<body([^>]*)>/i, (whole, attributes) => {
    if (/\bclass="/i.test(attributes)) return `<body${attributes.replace(/class="([^"]*)"/i, 'class="$1 review-candidate"')}>`;
    return `<body${attributes} class="review-candidate">`;
  });
  html = html.replace(/<body[^>]*>/i, match => `${match}\n${reviewBanner}`);
  html = html.replace('</body>', `${reviewBehavior}\n</body>`);
  return html;
}

function buildPage(page) {
  const sourcePath = path.join(repoRoot, page.source);
  let html = fs.readFileSync(sourcePath, 'utf8');
  if (page.source === 'index.html' && countRelativeAttributes(html) !== 20) {
    throw new Error(`home relative-link invariant failed: expected 20, got ${countRelativeAttributes(html)}`);
  }
  html = stripTracking(html);
  html = rewriteLinks(html, page.route);
  html = addReviewDirectives(html, page.source);
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
  candidate: 'ProductBeacon Fill the Rooms Phase 5R relook',
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
