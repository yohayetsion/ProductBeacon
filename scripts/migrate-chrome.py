#!/usr/bin/env python3
"""
migrate-chrome.py — ProductBeacon Phase 2/3 chrome migration.

SOURCE OF TRUTH: ProductBeacon/Product/migration-phase1-spec-2026-06-08.md
Owner: Frontend Dev (executes Phase 2/3 against the Tech Lead LOCKED spec).

What it does (single pass, allowlist-driven — NEVER a recursive glob):
  - class="nav" group: anchored replace of the nav block with the §1 canonical,
    anchored replace of the footer block with the §2.2 canonical.
  - topnav group (research/): anchored replace of the topnav block with the §1b canonical.
  - GA4 injection (G-TC1LMMGQGV) on any in-scope page missing it, placed
    immediately after the first <link rel="stylesheet" ...> line in <head>.

Hard rules (NON-NEGOTIABLE, per spec §3):
  - Exactly-1-match assertion per anchored nav/topnav replace. 0 or >1 -> abort
    that file, print the path, exit non-zero. No 2>/dev/null error swallowing.
  - Footer count is 0-or-1 (1 = replaced, 0 = reported, never silent).
  - GA4: after injection, content must contain G-TC1LMMGQGV at least once.
  - Idempotent: re-running on an already-migrated file replaces canonical with
    itself (still exactly 1 match) -> safe.
  - Final gate: migrated_count == allowlist_count or the run is a failure.
  - NEVER touch prospects/ planning/ reports/ research/state-of-cyber-2026/ etc.
  - NEVER touch retire-bucket pages (axia-offer, gtm-engine,
    strategic-infrastructure, services.html) — those are Phase 5 redirects.
"""

import re
import sys
from pathlib import Path

# Repo root = parent of scripts/
REPO = Path(__file__).resolve().parent.parent

GA4_ID = "G-TC1LMMGQGV"

# --------------------------------------------------------------------------
# §1 CANONICAL class="nav" block (root-absolute, Version A, Apply button)
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
    <a href="/research/" role="menuitem">Research</a>
    <a href="/about.html" role="menuitem">About</a>
    <a href="/contact.html?intent=apply" class="btn btn--primary" style="margin-top:12px; text-align:center;" role="menuitem" onclick="pbTrack &amp;&amp; pbTrack('apply_click',{location:'nav-mobile'})">Apply</a>
  </div>
</nav>'''

# --------------------------------------------------------------------------
# §2.2 CANONICAL footer block (root-absolute, one block every in-scope page)
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
        <a href="/on-call.html#fractional">Fractional Product Leadership</a>
        <a href="/on-call.html#build">Product Build</a>
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
# §1b CANONICAL topnav block (research/ group)
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

# topnav variant for pages where Research is NOT the active page
# (per spec §1b: remove `active` from Research on author.html / methodology.html;
#  none of those links match those pages, so simply no `active` flag).
CANONICAL_TOPNAV_INACTIVE = CANONICAL_TOPNAV.replace(
    '<li><a href="/research/" class="active">Research</a></li>',
    '<li><a href="/research/">Research</a></li>',
)

# --------------------------------------------------------------------------
# GA4 snippet (§4) — injected after first <link rel="stylesheet"> in <head>
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
# ANCHORED-REPLACE REGEXES (per spec §3)
# --------------------------------------------------------------------------
# §3.2 nav: optional leading comment marker + <nav class="nav"...> ... first </nav>
NAV_RE = re.compile(
    r'(?:<!-- ====== NAV[^\n]*-->\s*)?<nav class="nav"[\s\S]*?</nav>'
)
# §3.3 footer
FOOTER_RE = re.compile(r'<footer class="footer">[\s\S]*?</footer>')
# §3.4 topnav
TOPNAV_RE = re.compile(r'<nav class="topnav"[\s\S]*?</nav>')
# GA4 placement: first stylesheet <link ...> in head, regardless of attribute order
# (class="nav" pages use `<link rel="stylesheet" href=...>`; research/ pages use
#  `<link href="...fonts..." rel="stylesheet">`). Match any <link> tag whose
#  attributes include rel="stylesheet". Fallback anchor: just before </head>.
STYLESHEET_RE = re.compile(r'<link\b[^>]*\brel="stylesheet"[^>]*>')
HEAD_CLOSE_RE = re.compile(r'</head>', re.IGNORECASE)

# --------------------------------------------------------------------------
# ALLOWLISTS (explicit — NEVER a recursive glob)
# --------------------------------------------------------------------------
# class="nav" group: marketing root pages + vtv (index + reader) + insights index pages.
# Includes the 3 live Version A root pages (index/on-call/workforce) — per spec §0
# correction #1 they are re-canonicalized to root-absolute (they still carry
# >Services< and on-call still carries "Book a Call", so they MUST be migrated).
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

# topnav group: research/ pages using class="topnav".
# research/index.html keeps Research active; author/methodology get the inactive variant.
# collaterals.html uses an "other" nav and is excluded from the assertion batch (§3.4) —
# it is hand-aligned separately, NOT processed here.
TOPNAV_GROUP = {
    "research/index.html": CANONICAL_TOPNAV,         # active Research
    "research/author.html": CANONICAL_TOPNAV_INACTIVE,
    "research/methodology.html": CANONICAL_TOPNAV_INACTIVE,
}

ALLOWLIST = NAV_GROUP + list(TOPNAV_GROUP.keys())

# Defensive: paths that must NEVER appear in the allowlist (assert at runtime).
FORBIDDEN_PREFIXES = (
    "prospects/", "planning/", "reports/",
    "research/state-of-cyber-2026/",
    "reports/state-of-cyber-2026/",
)
# Retire-bucket pages — Phase 5 redirects, never migrate.
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
        # Fallback per spec intent: place GA4 in <head>, immediately before </head>.
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


def process_nav_file(path, relpath):
    content = path.read_text(encoding="utf-8")

    # nav: exactly 1
    content = replace_once(content, NAV_RE, CANONICAL_NAV, relpath, "nav")

    # footer: 0-or-1 (1=replaced, 0=reported)
    footer_count = len(FOOTER_RE.findall(content))
    if footer_count > 1:
        fail(f"{relpath}: footer match count == {footer_count} (expected 0 or 1)")
    if footer_count == 1:
        content = FOOTER_RE.sub(lambda _m: CANONICAL_FOOTER, content, count=1)
        footer_status = 1
    else:
        footer_status = 0
        print(f"  NOTICE {relpath}: no <footer class=\"footer\"> found — footer skipped (reported, not error)")

    # GA4
    content, ga4_status = inject_ga4(content, relpath)

    path.write_text(content, encoding="utf-8")
    print(f"OK nav=1 footer={footer_status} ga4={ga4_status} {relpath}")
    return ga4_status


def process_topnav_file(path, relpath, canonical):
    content = path.read_text(encoding="utf-8")

    # topnav: exactly 1
    content = replace_once(content, TOPNAV_RE, canonical, relpath, "topnav")

    # research/ pages may not have a standard footer — 0-or-1, never forced
    footer_count = len(FOOTER_RE.findall(content))
    if footer_count > 1:
        fail(f"{relpath}: footer match count == {footer_count} (expected 0 or 1)")
    if footer_count == 1:
        content = FOOTER_RE.sub(lambda _m: CANONICAL_FOOTER, content, count=1)
        footer_status = 1
    else:
        footer_status = 0
        print(f"  NOTICE {relpath}: no <footer class=\"footer\"> found — footer skipped (reported, not error)")

    # GA4
    content, ga4_status = inject_ga4(content, relpath)

    path.write_text(content, encoding="utf-8")
    print(f"OK topnav=1 footer={footer_status} ga4={ga4_status} {relpath}")
    return ga4_status


def main():
    dry_run = "--dry-run" in sys.argv

    # Defensive allowlist sanity checks (no forbidden dirs, no retire pages).
    for rel in ALLOWLIST:
        normrel = rel.replace("\\", "/")
        for pref in FORBIDDEN_PREFIXES:
            if normrel.startswith(pref):
                fail(f"allowlist contains forbidden path: {rel}")
        if normrel in RETIRE_PAGES:
            fail(f"allowlist contains retire-bucket page: {rel}")

    print(f"Allowlist: {len(ALLOWLIST)} pages "
          f"({len(NAV_GROUP)} class=\"nav\" + {len(TOPNAV_GROUP)} topnav)")
    if dry_run:
        for rel in ALLOWLIST:
            exists = (REPO / rel).exists()
            print(f"  {'EXISTS' if exists else 'MISSING'}  {rel}")
        sys.exit(0)

    migrated = 0
    ga4_added = 0
    nav_pages = 0
    topnav_pages = 0

    # Process class="nav" group
    for rel in NAV_GROUP:
        path = REPO / rel
        if not path.exists():
            fail(f"allowlisted file does not exist: {rel}")
        status = process_nav_file(path, rel)
        nav_pages += 1
        migrated += 1
        if status == "added":
            ga4_added += 1

    # Process topnav group
    for rel, canonical in TOPNAV_GROUP.items():
        path = REPO / rel
        if not path.exists():
            fail(f"allowlisted file does not exist: {rel}")
        status = process_topnav_file(path, rel, canonical)
        topnav_pages += 1
        migrated += 1
        if status == "added":
            ga4_added += 1

    print("-" * 60)
    print(f"class=\"nav\" pages updated: {nav_pages}")
    print(f"topnav pages updated:      {topnav_pages}")
    print(f"GA4 injected (new):        {ga4_added}")
    print(f"migrated_count: {migrated}  allowlist_count: {len(ALLOWLIST)}")

    # Final gate (§3.5)
    if migrated != len(ALLOWLIST):
        fail(f"migrated_count ({migrated}) != allowlist_count ({len(ALLOWLIST)})")
    print("GATE PASS: migrated_count == allowlist_count")


if __name__ == "__main__":
    main()
