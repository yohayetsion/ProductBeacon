#!/usr/bin/env python3
"""
migrate-chrome.py — ProductBeacon chrome migration.

SOURCE OF TRUTH (v2, 2026-06-13): live `index.html` nav (lines 115-152) + footer
(lines 491-530), captured byte-faithfully in
`.backups/chrome-unify-2026-06-13/CONTRACT.md`. The pre-existing `_includes/nav.html`
and the OLD migrator `CANONICAL_NAV`/`CANONICAL_FOOTER` constants were STALE (both
missing the "The Standard" nav item) and are NOT trusted — they were regenerated
from index.html in Phase 1.

Original (June-8) spec: ProductBeacon/Product/migration-phase1-spec-2026-06-08.md.
Owner: Frontend Dev executes the apply; Tech Lead owns the tooling + the spec.

------------------------------------------------------------------------------
DECISION REVERSAL — DR-2026-062 (2026-06-13)
------------------------------------------------------------------------------
The June-8 migration DELIBERATELY kept the research section on its own `topnav`
chrome (dedicated CANONICAL_TOPNAV blocks; `research/state-of-cyber-2026/` on a
never-touch list). Per Yohay's 2026-06-13 directive, EVERY public page — research
included — must carry the SAME global `.nav`/`.footer` chrome. This reverses that
choice: research pages move from the TOPNAV path to the global-`.nav` path.

The old CANONICAL_TOPNAV* constants are retained below for historical reference
ONLY; the research group no longer uses them. The state-of-cyber-2026 decks
(dlp/dspm/irm/convergence/*-podcast) remain a genuinely separate, chrome-free
surface and stay guarded — only three soc pages (index, synthesis, pre-call-brief)
are individually carved out.
------------------------------------------------------------------------------

What it does (single pass, allowlist-driven — NEVER a recursive glob):
  - NAV_GROUP (class="nav" marketing/vtv/insights pages): anchored replace of the
    nav block with §1 canonical; anchored replace of the footer with §2 canonical;
    GA4 injection.
  - RESEARCH_GROUP (the global-`.nav` path, NEW): per-page swap of the legacy
    `<nav class="topnav">` (or INSERT after <body> where no chrome exists) with the
    global `.nav` carrying the correct per-page active state; ADD-or-REPLACE the
    global `.footer`; ensure `/css/style.css` link ABOVE the inline <style>; ensure
    `/js/main.js` before </body>; inject the fixed-nav hero offset on the page's
    content wrapper; seed CHROME markers; GA4.
  - TOPNAV_GROUP (LEGACY, now empty): retained structurally; the research pages it
    used to hold have moved to RESEARCH_GROUP. process_topnav_file() is kept for
    reference but is no longer reachable via the allowlist.

Hard rules (NON-NEGOTIABLE):
  - Exactly-1-match assertion per anchored nav/topnav/footer replace. 0 or >1 -> abort
    that file, print the path, exit non-zero. No error swallowing.
  - Footer add-or-replace: research pages without a global footer get one ADDED
    (exactly once); pages with an existing <footer class="footer"> get it REPLACED
    (exactly once). Either way the result has exactly 1 footer.
  - GA4: after injection, content must contain G-TC1LMMGQGV at least once.
  - Idempotent: re-running on an already-migrated file is a no-op (CHROME markers
    detected -> replace canonical with itself, still exactly 1; css/js/offset
    insertions are guarded on a presence check). Self-test: run twice -> zero diff.
  - Abort if a file carries more than one CHROME:NAV:START marker.
  - Final gate: migrated_count == allowlist_count or the run is a failure.
  - NEVER touch prospects/ planning/ reports/ the state-of-cyber-2026 DECKS, etc.
  - NEVER touch retire-bucket pages (axia-offer, gtm-engine,
    strategic-infrastructure, services.html).
"""

import re
import sys
from pathlib import Path

# Repo root = parent of scripts/
REPO = Path(__file__).resolve().parent.parent

GA4_ID = "G-TC1LMMGQGV"

# Marker comments delimiting the stamped chrome (idempotency anchors).
NAV_START = "<!-- CHROME:NAV:START -->"
NAV_END = "<!-- CHROME:NAV:END -->"
FOOTER_START = "<!-- CHROME:FOOTER:START -->"
FOOTER_END = "<!-- CHROME:FOOTER:END -->"

# Root-absolute global asset links (research pages currently link neither).
STYLE_LINK = '<link rel="stylesheet" href="/css/style.css">'
SCRIPT_TAG = '<script src="/js/main.js"></script>'

# Hero offset: the global .nav is position:fixed, 72px tall (--nav-height). Without
# this, the fixed nav clips the research H1. Applied to each page's content wrapper.
HERO_OFFSET_STYLE = "padding-top: var(--nav-height);"

# --------------------------------------------------------------------------
# §1 CANONICAL class="nav" block (root-absolute, 7 items incl. "The Standard")
# Byte-faithful to index.html L115-152 (CONTRACT.md §1). The INACTIVE variant —
# the active variant adds class="active" to the Research <a> (desktop list only).
# --------------------------------------------------------------------------
CANONICAL_NAV = '''<!-- ====== NAV ====== -->
<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav__inner">
    <a href="/index.html" class="nav__logo" aria-label="ProductBeacon home">
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="32" height="32" rx="6" fill="#0F172A"/>
        <circle cx="16" cy="12" r="4" fill="#F59E0B"/>
        <path d="M10 18 L16 28 L22 18" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      </svg>
      <span class="nav__logo-text">Product<strong>Beacon</strong></span>
    </a>
    <ul class="nav__links">
      <li><a href="/index.html#intensive">The Operator Intensive</a></li>
      <li><a href="/workforce.html">The Workforce</a></li>
      <li><a href="/on-call.html">On Call &amp; Fractional</a></li>
      <li><a href="/decision-provenance-standard.html">The Standard</a></li>
      <li><a href="/research/">Research</a></li>
      <li><a href="/about.html">About</a></li>
      <li><a href="/contact.html?intent=apply" class="btn btn--primary btn--lg" onclick="pbTrack &amp;&amp; pbTrack('apply_click',{location:'nav'})">Apply</a></li>
    </ul>
    <button class="nav__hamburger" aria-label="Toggle menu" aria-expanded="false">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="3" y1="6" x2="21" y2="6"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
        <line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    </button>
  </div>
  <div class="nav__mobile" role="menu">
    <a href="/index.html#intensive" role="menuitem">The Operator Intensive</a>
    <a href="/workforce.html" role="menuitem">The Workforce</a>
    <a href="/on-call.html" role="menuitem">On Call &amp; Fractional</a>
    <a href="/decision-provenance-standard.html" role="menuitem">The Standard</a>
    <a href="/research/" role="menuitem">Research</a>
    <a href="/about.html" role="menuitem">About</a>
    <a href="/contact.html?intent=apply" class="btn btn--primary" style="margin-top:12px; text-align:center;" role="menuitem" onclick="pbTrack &amp;&amp; pbTrack('apply_click',{location:'nav-mobile'})">Apply</a>
  </div>
</nav>'''

# ACTIVE variant: only research/index.html. Adds class="active" to the desktop
# Research anchor (rendered bright via css/style.css .nav__links a.active).
CANONICAL_NAV_ACTIVE = CANONICAL_NAV.replace(
    '<li><a href="/research/">Research</a></li>',
    '<li><a href="/research/" class="active">Research</a></li>',
)
assert CANONICAL_NAV_ACTIVE != CANONICAL_NAV, "active-variant substitution failed"

# --------------------------------------------------------------------------
# §2 CANONICAL footer block (byte-faithful to index.html L491-530, CONTRACT.md §2)
# Live footer uses BARE /on-call.html for Fractional + Build (the OLD constant's
# #fractional / #build anchors were stale).
# --------------------------------------------------------------------------
CANONICAL_FOOTER = '''<footer class="footer">
  <div class="container">
    <div class="footer__inner">
      <div class="footer__brand">
        <a href="/index.html" class="nav__logo" style="margin-bottom:8px;">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="6" fill="#0F172A"/><circle cx="16" cy="12" r="4" fill="#F59E0B"/><path d="M10 18 L16 28 L22 18" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
          <span class="nav__logo-text">Product<strong>Beacon</strong></span>
        </a>
        <p>Run an AI workforce, or have us run it for you.</p>
      </div>
      <div class="footer__col">
        <h4>Services</h4>
        <a href="/on-call.html">ProductBeacon On Call</a>
        <a href="/on-call.html">Fractional Product Leadership</a>
        <a href="/on-call.html">Product Build</a>
        <a href="/on-call.html#org">Product Org Services</a>
      </div>
      <div class="footer__col">
        <h4>Capabilities</h4>
        <a href="/index.html#intensive">The Operator Intensive</a>
        <a href="/workforce.html">The Workforce</a>
        <a href="/index.html#path">The Operator's Private Line</a>
      </div>
      <div class="footer__col">
        <h4>Resources</h4>
        <a href="/case-studies.html">Case Studies</a>
        <a href="/vision-to-value/" target="_blank" rel="noopener">Vision to Value (the book)</a>
        <a href="https://decisionprovenancestandard.org" target="_blank" rel="noopener">The Decision Provenance Standard</a>
      </div>
    </div>
    <div class="footer__bottom">
      <span>ProductBeacon is a brand of Etsion Brands Ltd, Israel. productbeacon.agency</span>
      <div class="footer__social">
        <a href="https://www.linkedin.com/in/yohayetsion/" target="_blank" rel="noopener" aria-label="LinkedIn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>'''

# --------------------------------------------------------------------------
# §1b LEGACY topnav block (research/ group) — RETAINED FOR REFERENCE ONLY.
# Per DR-2026-062 the research group no longer uses this; kept so the historical
# spec is legible and the regexes that DETECT a legacy topnav (to swap it out)
# remain documented.
# --------------------------------------------------------------------------
CANONICAL_TOPNAV = '''<nav class="topnav" aria-label="Primary">
  <a href="/" class="topnav-brand" aria-label="ProductBeacon home">
    <span class="topnav-brand-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="8" r="4" fill="#0F172A"/>
        <path d="M6 14 L12 22 L18 14 Z" fill="#0F172A"/>
      </svg>
    </span>
    <span class="topnav-brand-wordmark"><strong>Product</strong>Beacon</span>
  </a>
  <ul class="topnav-links">
    <li><a href="/">Home</a></li>
    <li><a href="/research/" class="active">Research</a></li>
    <li><a href="/on-call.html">On Call</a></li>
    <li><a href="/about.html">About</a></li>
  </ul>
</nav>'''
CANONICAL_TOPNAV_INACTIVE = CANONICAL_TOPNAV.replace(
    '<li><a href="/research/" class="active">Research</a></li>',
    '<li><a href="/research/">Research</a></li>',
)

# --------------------------------------------------------------------------
# GA4 snippet — injected after first <link rel="stylesheet"> in <head>
# --------------------------------------------------------------------------
GA4_SNIPPET = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TC1LMMGQGV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-TC1LMMGQGV');
</script>'''

# --------------------------------------------------------------------------
# ANCHORED-REPLACE REGEXES
# --------------------------------------------------------------------------
NAV_RE = re.compile(
    r'(?:<!-- ====== NAV[^\n]*-->\s*)?<nav class="nav"[\s\S]*?</nav>'
)
FOOTER_RE = re.compile(r'<footer class="footer">[\s\S]*?</footer>')
TOPNAV_RE = re.compile(r'<nav class="topnav"[\s\S]*?</nav>')
STYLESHEET_RE = re.compile(r'<link\b[^>]*\brel="stylesheet"[^>]*>')
HEAD_CLOSE_RE = re.compile(r'</head>', re.IGNORECASE)
BODY_OPEN_RE = re.compile(r'<body[^>]*>')
BODY_CLOSE_RE = re.compile(r'</body>', re.IGNORECASE)
INLINE_STYLE_OPEN_RE = re.compile(r'<style\b[^>]*>')
# First <main ...> or the collaterals <div class="wrap"> content wrapper.
MAIN_OPEN_RE = re.compile(r'<main\b([^>]*)>')
WRAP_OPEN_RE = re.compile(r'<div class="wrap">')

# Wrapped (marker-delimited) chrome regexes — used for idempotent re-stamping.
WRAPPED_NAV_RE = re.compile(
    re.escape(NAV_START) + r'[\s\S]*?' + re.escape(NAV_END)
)
WRAPPED_FOOTER_RE = re.compile(
    re.escape(FOOTER_START) + r'[\s\S]*?' + re.escape(FOOTER_END)
)

# --------------------------------------------------------------------------
# ALLOWLISTS (explicit — NEVER a recursive glob)
# --------------------------------------------------------------------------
INSIGHTS_SLUGS = [
    "accure", "aikido-security", "blackwall", "cloover", "cybersecurity",
    "embankment", "eolas-medical", "flower-labs", "keepnet", "maia-technology",
    "netbird", "orbem", "orbital-witness", "qibb", "united-manufacturing-hub",
]
VTV_READER = [
    "appendix-a-installation-guide-a-first-90-days-sequence",
    "appendix-b-decision-system-blueprints-and-economic-artifacts-templates",
    "appendix-c-function-specific-decision-interface-charters",
    "appendix-d-glossary",
    "appendix-e-further-resources",
    "chapter-1-end-to-end-product-organizations",
    "chapter-2-the-strategic-process-and-operational-focus-areas",
    "chapter-3-structure-and-scope",
    "chapter-4-decision-interfaces-and-the-architecture",
    "chapter-5-scaling-as-design-problem",
    "chapter-6-people-at-scale",
    "chapter-7-the-executive-altitude",
    "chapter-8-the-eight-operating-principles",
    "conclusion-from-vision-to-value",
    "index",
    "introduction",
    "preface",
]

NAV_GROUP = (
    [
        "about.html",
        "case-studies.html",
        "contact.html",
        "decision-provenance-standard.html",
        "index.html",
        "on-call.html",
        "workforce.html",
        "vision-to-value/index.html",
    ]
    + [f"vision-to-value/reader/{name}.html" for name in VTV_READER]
    + [f"insights/{slug}/index.html" for slug in INSIGHTS_SLUGS]
)

# RESEARCH_GROUP (NEW per DR-2026-062): research pages on the global-.nav path.
# Value = "active" (Research nav highlighted) or "inactive".
RESEARCH_GROUP = {
    "research/index.html": "active",
    "research/author.html": "inactive",
    "research/methodology.html": "inactive",
    "research/state-of-cyber-2026/index.html": "inactive",
    "research/collaterals.html": "inactive",        # no existing chrome -> ADD nav
    "research/state-of-cyber-2026/synthesis.html": "inactive",
    "research/state-of-cyber-2026/pre-call-brief.html": "inactive",
}

# TOPNAV_GROUP is now EMPTY — research pages moved to RESEARCH_GROUP (DR-2026-062).
# Retained as a dict so any downstream importer that references it keeps working.
TOPNAV_GROUP = {}

ALLOWLIST = NAV_GROUP + list(RESEARCH_GROUP.keys()) + list(TOPNAV_GROUP.keys())

# Defensive: paths that must NEVER appear in the allowlist (assert at runtime),
# EXCEPT the three soc pages individually carved out of the directory guard.
FORBIDDEN_PREFIXES = (
    "prospects/", "planning/", "reports/",
    "research/state-of-cyber-2026/",
    "reports/state-of-cyber-2026/",
)
# Individual carve-outs from the research/state-of-cyber-2026/ directory guard
# (DR-2026-062). Everything else under that dir (the dlp/dspm/irm/convergence/
# *-podcast decks + brief.html stub) stays guarded.
SOC_CARVE_OUTS = {
    "research/state-of-cyber-2026/index.html",
    "research/state-of-cyber-2026/synthesis.html",
    "research/state-of-cyber-2026/pre-call-brief.html",
}
RETIRE_PAGES = {
    "axia-offer.html", "gtm-engine.html",
    "strategic-infrastructure.html", "services.html",
}


def fail(msg):
    print(f"ABORT: {msg}", file=sys.stderr)
    sys.exit(1)


def inject_ga4(content, relpath):
    """Idempotent GA4 injection after the first stylesheet link. Returns (content, status)."""
    if GA4_ID in content:
        return content, "present"
    m = STYLESHEET_RE.search(content)
    if m:
        insert_at = m.end()
        new = content[:insert_at] + "\n" + GA4_SNIPPET + content[insert_at:]
    else:
        hm = HEAD_CLOSE_RE.search(content)
        if not hm:
            fail(f"{relpath}: GA4 needed but no stylesheet <link> and no </head> found for placement")
        insert_at = hm.start()
        new = content[:insert_at] + GA4_SNIPPET + "\n" + content[insert_at:]
        print(f"  NOTICE {relpath}: no rel=\"stylesheet\" link — GA4 placed before </head>")
    if new.count(GA4_ID) < 1:
        fail(f"{relpath}: GA4 injection produced 0 occurrences (post-assert failed)")
    return new, "added"


def replace_once(content, regex, replacement, relpath, what):
    """Anchored replace with exactly-1-match assertion. Aborts on 0 or >1."""
    new, count = regex.subn(lambda _m: replacement, content)
    if count != 1:
        fail(f"{relpath}: {what} match count == {count} (expected exactly 1)")
    return new


def ensure_style_link(content, relpath):
    """Ensure exactly one /css/style.css link exists, placed ABOVE the inline
    <style> (so page :root tokens/body rules win the cascade). Idempotent."""
    if "/css/style.css" in content:
        return content, "present"
    m = INLINE_STYLE_OPEN_RE.search(content)
    if m:
        insert_at = m.start()
        new = content[:insert_at] + STYLE_LINK + "\n" + content[insert_at:]
    else:
        # Fallback: place before </head>.
        hm = HEAD_CLOSE_RE.search(content)
        if not hm:
            fail(f"{relpath}: cannot place style link — no inline <style> and no </head>")
        insert_at = hm.start()
        new = content[:insert_at] + STYLE_LINK + "\n" + content[insert_at:]
        print(f"  NOTICE {relpath}: no inline <style> — style.css placed before </head>")
    if new.count("/css/style.css") != 1:
        fail(f"{relpath}: style.css link count != 1 after insertion")
    return new, "added"


def ensure_main_js(content, relpath):
    """Ensure exactly one /js/main.js <script> before </body>. Idempotent."""
    if "/js/main.js" in content:
        return content, "present"
    m = BODY_CLOSE_RE.search(content)
    if not m:
        fail(f"{relpath}: cannot place main.js — no </body> found")
    insert_at = m.start()
    new = content[:insert_at] + SCRIPT_TAG + "\n" + content[insert_at:]
    if new.count("/js/main.js") != 1:
        fail(f"{relpath}: main.js count != 1 after insertion")
    return new, "added"


def ensure_hero_offset(content, relpath):
    """Inject `padding-top: var(--nav-height)` onto the page's content wrapper so
    the fixed 72px nav doesn't clip the hero. The wrapper is the first <main> on
    topnav-derived pages, or <div class="wrap"> on collaterals. Idempotent: skip
    if the offset token is already on that wrapper. Returns (content, status)."""
    if HERO_OFFSET_STYLE in content:
        return content, "present"

    # Prefer <main>; fall back to <div class="wrap"> (collaterals has no <main>).
    m = MAIN_OPEN_RE.search(content)
    if m:
        attrs = m.group(1)  # e.g. '' or ' class="x"' or ' style="..."'
        style_m = re.search(r'\bstyle="([^"]*)"', attrs)
        if style_m:
            existing = style_m.group(1).rstrip()
            sep = "" if existing.endswith(";") or existing == "" else ";"
            new_style = f'{existing}{sep} {HERO_OFFSET_STYLE}'.strip()
            new_attrs = attrs[:style_m.start()] + f'style="{new_style}"' + attrs[style_m.end():]
        else:
            new_attrs = attrs + f' style="{HERO_OFFSET_STYLE}"'
        new_tag = f'<main{new_attrs}>'
        new = content[:m.start()] + new_tag + content[m.end():]
        return new, "main"

    wm = WRAP_OPEN_RE.search(content)
    if wm:
        new_tag = f'<div class="wrap" style="{HERO_OFFSET_STYLE}">'
        new = content[:wm.start()] + new_tag + content[wm.end():]
        return new, "wrap"

    fail(f"{relpath}: cannot place hero offset — no <main> and no <div class=\"wrap\">")


def stamp_research_nav(content, relpath, state):
    """Swap a legacy <nav class="topnav"> for the global .nav (active or inactive),
    OR INSERT the global .nav right after <body> where no chrome exists
    (collaterals). The stamped nav is wrapped in CHROME:NAV markers for idempotent
    re-stamping. Returns content. Aborts on >1 START marker."""
    canonical = CANONICAL_NAV_ACTIVE if state == "active" else CANONICAL_NAV
    wrapped = f"{NAV_START}\n{canonical}\n{NAV_END}"

    n_start = content.count(NAV_START)
    if n_start > 1:
        fail(f"{relpath}: {n_start} CHROME:NAV:START markers (expected 0 or 1)")

    if n_start == 1:
        # Idempotent re-stamp: replace the marker-wrapped block with itself.
        content, c = WRAPPED_NAV_RE.subn(lambda _m: wrapped, content)
        if c != 1:
            fail(f"{relpath}: wrapped-nav re-stamp count == {c} (expected 1)")
        return content

    # First stamp. Two cases:
    n_topnav = len(TOPNAV_RE.findall(content))
    if n_topnav == 1:
        # Swap the legacy topnav for the wrapped global nav (exactly-1).
        content = replace_once(content, TOPNAV_RE, wrapped, relpath, "topnav->nav")
        return content
    if n_topnav > 1:
        fail(f"{relpath}: topnav count == {n_topnav} (expected 0 or 1)")

    # No topnav (collaterals): INSERT the wrapped nav immediately after <body>.
    m = BODY_OPEN_RE.search(content)
    if not m:
        fail(f"{relpath}: no <nav class=\"topnav\"> and no <body> to insert nav after")
    insert_at = m.end()
    content = content[:insert_at] + "\n" + wrapped + content[insert_at:]
    return content


def stamp_research_footer(content, relpath):
    """ADD-or-REPLACE the global footer, wrapped in CHROME:FOOTER markers.
    - existing marker -> idempotent re-stamp (exactly 1).
    - existing <footer class="footer"> (possibly a NON-global author-bio footer,
      e.g. soc/index) -> REPLACE it (exactly 1).
    - no footer -> ADD before </body> (after a main.js script if present, the
      marker block goes before </body> regardless).
    Returns content. End state: exactly 1 CHROME:FOOTER block, 1 <footer>."""
    wrapped = f"{FOOTER_START}\n{CANONICAL_FOOTER}\n{FOOTER_END}"

    n_start = content.count(FOOTER_START)
    if n_start > 1:
        fail(f"{relpath}: {n_start} CHROME:FOOTER:START markers (expected 0 or 1)")
    if n_start == 1:
        content, c = WRAPPED_FOOTER_RE.subn(lambda _m: wrapped, content)
        if c != 1:
            fail(f"{relpath}: wrapped-footer re-stamp count == {c} (expected 1)")
        return content

    n_footer = len(FOOTER_RE.findall(content))
    if n_footer > 1:
        fail(f"{relpath}: footer count == {n_footer} (expected 0 or 1)")
    if n_footer == 1:
        content = replace_once(content, FOOTER_RE, wrapped, relpath, "footer-replace")
        return content

    # ADD before </body>.
    m = BODY_CLOSE_RE.search(content)
    if not m:
        fail(f"{relpath}: no footer and no </body> to add footer before")
    insert_at = m.start()
    content = content[:insert_at] + wrapped + "\n" + content[insert_at:]
    return content


def process_nav_file(path, relpath):
    content = path.read_text(encoding="utf-8")
    content = replace_once(content, NAV_RE, CANONICAL_NAV, relpath, "nav")
    footer_count = len(FOOTER_RE.findall(content))
    if footer_count > 1:
        fail(f"{relpath}: footer match count == {footer_count} (expected 0 or 1)")
    if footer_count == 1:
        content = FOOTER_RE.sub(lambda _m: CANONICAL_FOOTER, content, count=1)
        footer_status = 1
    else:
        footer_status = 0
        print(f"  NOTICE {relpath}: no <footer class=\"footer\"> found — footer skipped (reported, not error)")
    content, ga4_status = inject_ga4(content, relpath)
    path.write_text(content, encoding="utf-8")
    print(f"OK nav=1 footer={footer_status} ga4={ga4_status} {relpath}")
    return ga4_status


def process_research_file(path, relpath, state):
    """Global-.nav path for a research page (DR-2026-062). Returns a status dict."""
    content = path.read_text(encoding="utf-8")

    content = stamp_research_nav(content, relpath, state)
    content = stamp_research_footer(content, relpath)
    content, style_status = ensure_style_link(content, relpath)
    content, js_status = ensure_main_js(content, relpath)
    content, offset_status = ensure_hero_offset(content, relpath)
    content, ga4_status = inject_ga4(content, relpath)

    path.write_text(content, encoding="utf-8")
    print(f"OK research nav={state} footer=1 css={style_status} js={js_status} "
          f"offset={offset_status} ga4={ga4_status} {relpath}")
    return {"ga4": ga4_status}


def plan_research_file(content, relpath, state):
    """Dry-run: compute the post-transform content WITHOUT writing, returning
    (new_content, summary). Used for --dry-run diff + idempotency proof."""
    c = stamp_research_nav(content, relpath, state)
    c = stamp_research_footer(c, relpath)
    c, style_status = ensure_style_link(c, relpath)
    c, js_status = ensure_main_js(c, relpath)
    c, offset_status = ensure_hero_offset(c, relpath)
    c, ga4_status = inject_ga4(c, relpath)
    summary = (f"nav={state} footer=add/replace css={style_status} js={js_status} "
               f"offset={offset_status} ga4={ga4_status}")
    return c, summary


# Kept for reference (no longer reachable via allowlist; TOPNAV_GROUP is empty).
def process_topnav_file(path, relpath, canonical):  # pragma: no cover
    content = path.read_text(encoding="utf-8")
    content = replace_once(content, TOPNAV_RE, canonical, relpath, "topnav")
    footer_count = len(FOOTER_RE.findall(content))
    if footer_count > 1:
        fail(f"{relpath}: footer match count == {footer_count} (expected 0 or 1)")
    if footer_count == 1:
        content = FOOTER_RE.sub(lambda _m: CANONICAL_FOOTER, content, count=1)
        footer_status = 1
    else:
        footer_status = 0
    content, ga4_status = inject_ga4(content, relpath)
    path.write_text(content, encoding="utf-8")
    print(f"OK topnav=1 footer={footer_status} ga4={ga4_status} {relpath}")
    return ga4_status


def _check_allowlist_safety():
    """Forbidden-dir + retire-page guard, with the SOC carve-out exception."""
    for rel in ALLOWLIST:
        normrel = rel.replace("\\", "/")
        if normrel in SOC_CARVE_OUTS:
            continue  # individually carved out of the directory guard (DR-2026-062)
        for pref in FORBIDDEN_PREFIXES:
            if normrel.startswith(pref):
                fail(f"allowlist contains forbidden path: {rel}")
        if normrel in RETIRE_PAGES:
            fail(f"allowlist contains retire-bucket page: {rel}")


def _dry_run():
    print(f"Allowlist: {len(ALLOWLIST)} pages "
          f"({len(NAV_GROUP)} class=\"nav\" + {len(RESEARCH_GROUP)} research "
          f"+ {len(TOPNAV_GROUP)} legacy-topnav)")
    print("\n--- existence ---")
    for rel in ALLOWLIST:
        exists = (REPO / rel).exists()
        print(f"  {'EXISTS' if exists else 'MISSING'}  {rel}")

    print("\n--- research-group intended transforms (no writes) ---")
    plans = {}
    for rel, state in RESEARCH_GROUP.items():
        path = REPO / rel
        if not path.exists():
            print(f"  MISSING {rel} — cannot plan")
            continue
        content = path.read_text(encoding="utf-8")
        new1, summary = plan_research_file(content, rel, state)
        plans[rel] = new1
        changed = "CHANGED" if new1 != content else "no-op"
        print(f"  {rel}: {summary}  [{changed}]")

    print("\n--- idempotency proof (apply plan twice -> second pass zero diff) ---")
    all_idem = True
    for rel, state in RESEARCH_GROUP.items():
        if rel not in plans:
            continue
        once = plans[rel]
        twice, _ = plan_research_file(once, rel, state)
        if twice == once:
            print(f"  IDEMPOTENT  {rel}")
        else:
            all_idem = False
            print(f"  NOT-IDEMPOTENT  {rel} — second pass differs!")
    print("-" * 60)
    print(f"idempotency: {'ALL IDEMPOTENT' if all_idem else 'FAILURE — see above'}")
    if not all_idem:
        sys.exit(1)


def main():
    dry_run = "--dry-run" in sys.argv
    _check_allowlist_safety()

    if dry_run:
        _dry_run()
        sys.exit(0)

    print(f"Allowlist: {len(ALLOWLIST)} pages "
          f"({len(NAV_GROUP)} class=\"nav\" + {len(RESEARCH_GROUP)} research)")

    migrated = 0
    ga4_added = 0
    nav_pages = 0
    research_pages = 0

    for rel in NAV_GROUP:
        path = REPO / rel
        if not path.exists():
            fail(f"allowlisted file does not exist: {rel}")
        status = process_nav_file(path, rel)
        nav_pages += 1
        migrated += 1
        if status == "added":
            ga4_added += 1

    for rel, state in RESEARCH_GROUP.items():
        path = REPO / rel
        if not path.exists():
            fail(f"allowlisted file does not exist: {rel}")
        res = process_research_file(path, rel, state)
        research_pages += 1
        migrated += 1
        if res["ga4"] == "added":
            ga4_added += 1

    print("-" * 60)
    print(f"class=\"nav\" pages updated: {nav_pages}")
    print(f"research pages updated:    {research_pages}")
    print(f"GA4 injected (new):        {ga4_added}")
    print(f"migrated_count: {migrated}  allowlist_count: {len(ALLOWLIST)}")

    if migrated != len(ALLOWLIST):
        fail(f"migrated_count ({migrated}) != allowlist_count ({len(ALLOWLIST)})")
    print("GATE PASS: migrated_count == allowlist_count")


if __name__ == "__main__":
    main()
