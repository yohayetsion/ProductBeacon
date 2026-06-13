#!/usr/bin/env python3
"""
verify-migration.py — ProductBeacon migration GATE (QA Engineer).

SOURCE OF TRUTH: ProductBeacon/Product/migration-phase1-spec-2026-06-08.md (§9)
                 + operator-intensive-site-migration-plan-2026-06-08.md (§2, §8 SEO gates)
Owner: ✅ QA Engineer. Verifies Phase 3 (chrome migration) and is the reusable
per-phase + Phase-6 gate. Exit non-zero on ANY violation.

DESIGN PRINCIPLES (NON-NEGOTIABLE):
  - Allowlist-driven. The in-scope page set is IMPORTED from migrate-chrome.py
    (single source of truth) so the gate can NEVER drift from what was migrated.
  - NEVER scans prospects/ planning/ reports/ research/state-of-cyber-2026/.
    The allowlist is explicit; a recursive glob is never used to pick pages.
  - CHROME-ONLY gate. This gate verifies NAV + FOOTER + GA4 + link/anchor
    integrity (the chrome). It deliberately does NOT fail on Phase-4 BODY
    residuals (body "Book a Call" CTA buttons, body "Fractional CPO" copy,
    contact.html copy alignment) — those are owned by Phase 4 (Content/Copy).
    The chrome gate must be able to PASS while body items remain.

RESEARCH GROUP (DR-2026-062): the research section was moved off its own `topnav`
chrome onto the GLOBAL `.nav`/`.footer` (reversing the June-8 separation). Those
pages are gated by check_research_group_page(): exactly 1 <nav class="nav"> +
Version-A signature; 0 × class="topnav"; 0 × topnav-brand; 0 × page-local
.footer{ / .footer-blocks / .footer-inner CSS; exactly 1 × /css/style.css; exactly
1 × class="nav__inner"; 0 × inverted <strong>Product</strong>Beacon wordmark;
exactly 1 Research a.active on research/index.html (0 on inactive pages).
NOT gated on .nav__logo-text (false-positives on the valid footer brand logo).

CHECKS (per in-scope page):
  1. Exactly ONE nav block (class="nav" + research groups: <nav class="nav">;
     legacy topnav group: <nav class="topnav">).
  2. Version A signature present:
       - class="nav": "The Operator Intensive" + "The Workforce" + "On Call"
         + ">Apply</a>"  (the §1 canonical link set).
       - topnav: the §1b link set (Home / Research / On Call / About).
  3. Zero retired CHROME markers:
       - "Book a Call" INSIDE a <nav>...</nav> block  (body CTAs are Phase 4).
       - a nav link whose text is exactly ">Services<" or ">Insights<".
       - any link to "/services.html" or "services.html#..." (anywhere — the
         footer must not point at the retired page; body links to it are also
         chrome-adjacent and would 404 post-retire).
       - "{{ROOT}}" template token (anywhere).
       - bare href="#intensive" / href="#path" (must be /index.html#...).
  4. GA4 (G-TC1LMMGQGV) present.
  5. Footer canonical: no stale "/services.html#fractional" and no
     "Fractional CPO" text INSIDE the <footer>...</footer> block.
       (Body "Fractional CPO" copy — e.g. on-call.html — is Phase 4, NOT checked.)
  6. Internal link + in-page anchor resolution across the in-scope tree:
       - root-absolute links (/foo.html, /research/) resolve to an existing
         file in the repo.
       - #anchors resolve to an id= / name= in the TARGET page.
       - relative links (foo.html) resolve relative to the page's directory.

SEO GATE (Phase 6, owned by SEO Specialist — spec §8): a SEPARATE gate from the
chrome gate. Per in-scope page: self-referential canonical; OG (title/desc/type/
url/image) + twitter:card; og:image resolves to an existing asset; required
JSON-LD @type per page (Organization+FAQPage on home, Book on vtv hub, Person on
about, DefinedTerm|TechArticle on DPS) and all JSON-LD parses. Plus site-level:
sitemap purity (all live in-scope URLs present, zero retired/operational URLs,
well-formed), robots (AI bots allowed + operational dirs disallowed + state-of-
cyber NOT blocked + Sitemap line), redirect-stub resolution (each retired page
noindex meta-refreshes + canonicals to the CORRECT target), og-image.png is
1200x630, and on-call.html carries the fractional ranking-heir terms in H1/H2.

USAGE:
  python scripts/verify-migration.py            # chrome gate only
  python scripts/verify-migration.py --seo      # chrome gate + SEO gate
  python scripts/verify-migration.py --seo-only # SEO gate only
  python scripts/verify-migration.py --verbose  # per-page PASS lines too
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# --- Import the allowlist + canonical constants from migrate-chrome.py --------
# Single source of truth: the gate verifies exactly what the migrator targets.
sys.path.insert(0, str(REPO / "scripts"))
try:
    import importlib

    mc = importlib.import_module("migrate-chrome")
except Exception as e:  # pragma: no cover - defensive
    print(f"ABORT: cannot import migrate-chrome.py for the allowlist: {e}",
          file=sys.stderr)
    sys.exit(2)

NAV_GROUP = mc.NAV_GROUP
TOPNAV_GROUP = mc.TOPNAV_GROUP            # dict: relpath -> canonical topnav (LEGACY, now empty)
RESEARCH_GROUP = mc.RESEARCH_GROUP        # dict: relpath -> "active"|"inactive" (DR-2026-062)
ALLOWLIST = mc.ALLOWLIST
GA4_ID = mc.GA4_ID
FORBIDDEN_PREFIXES = mc.FORBIDDEN_PREFIXES
RETIRE_PAGES = mc.RETIRE_PAGES
SOC_CARVE_OUTS = getattr(mc, "SOC_CARVE_OUTS", set())

# --- Regexes -----------------------------------------------------------------
NAV_BLOCK_RE = re.compile(r'<nav class="nav"[\s\S]*?</nav>')
TOPNAV_BLOCK_RE = re.compile(r'<nav class="topnav"[\s\S]*?</nav>')
ANY_NAV_RE = re.compile(r'<nav\b[\s\S]*?</nav>', re.IGNORECASE)
FOOTER_BLOCK_RE = re.compile(r'<footer class="footer">[\s\S]*?</footer>')

# id="..." / name="..." (for anchor resolution)
ID_RE = re.compile(r'\bid="([^"]+)"')
NAME_RE = re.compile(r'\bname="([^"]+)"')

# href="..." extraction (double-quoted only — the canonical uses double quotes)
HREF_RE = re.compile(r'href="([^"]*)"')

# Version A class="nav" signature substrings (per §9 / §1 canonical)
NAV_SIGNATURE = [
    "The Operator Intensive",
    "The Workforce",
    "On Call",
    ">Apply</a>",
]
# topnav signature (per §1b)
TOPNAV_SIGNATURE = [">Home<", ">Research<", ">On Call<", ">About<"]


# --- Violation collector -----------------------------------------------------
class Report:
    def __init__(self):
        self.violations = []  # (relpath, check, detail) — GATING (exit 1)
        self.warnings = []    # (relpath, check, detail) — NON-gating (reported)

    def fail(self, relpath, check, detail):
        self.violations.append((relpath, check, detail))

    def warn(self, relpath, check, detail):
        self.warnings.append((relpath, check, detail))

    def ok(self):
        return not self.violations


def read(relpath):
    return (REPO / relpath).read_text(encoding="utf-8", errors="replace")


# --- Anchor index (built once across the in-scope + always-live targets) -----
def build_id_index():
    """Map normalized target path -> set of ids/names defined in that file.
    Indexes every in-scope page plus the always-live root targets that the
    canonical chrome links to (index/workforce/on-call live pages are in the
    allowlist already)."""
    index = {}
    targets = set(ALLOWLIST)
    for rel in targets:
        p = REPO / rel
        if not p.exists():
            continue
        content = p.read_text(encoding="utf-8", errors="replace")
        ids = set(ID_RE.findall(content)) | set(NAME_RE.findall(content))
        index[rel.replace("\\", "/")] = ids
    return index


def resolve_link_target(href, page_relpath):
    """Return (target_relpath_or_None, anchor_or_None, kind).
    kind: 'internal' (resolvable file), 'external'/'special' (skip),
          'anchor-only' (same-page #foo).
    """
    href = href.strip()
    # skip external / non-navigational schemes
    if (href.startswith("http://") or href.startswith("https://")
            or href.startswith("mailto:") or href.startswith("tel:")
            or href.startswith("data:") or href.startswith("javascript:")
            or href == "" or href == "#"):
        return None, None, "external"

    anchor = None
    if "#" in href:
        path_part, anchor = href.split("#", 1)
    else:
        path_part = href

    # strip query string for file resolution (?intent=apply etc.)
    if "?" in path_part:
        path_part = path_part.split("?", 1)[0]

    # same-page anchor
    if path_part == "":
        return page_relpath.replace("\\", "/"), anchor, "anchor-only"

    # resolve to a repo-relative path
    if path_part.startswith("/"):
        rel = path_part.lstrip("/")
    else:
        # relative to the page's directory
        base = Path(page_relpath).parent
        rel = (base / path_part).as_posix()
        # normalize ../ etc.
        rel = Path(rel).as_posix()
        # collapse any .. by resolving against repo (string-level)
        parts = []
        for seg in rel.split("/"):
            if seg == "..":
                if parts:
                    parts.pop()
            elif seg in ("", "."):
                continue
            else:
                parts.append(seg)
        rel = "/".join(parts)

    # directory link -> index.html
    if rel.endswith("/") or rel == "":
        rel = (rel + "index.html") if rel else "index.html"
    elif (REPO / rel).is_dir():
        rel = rel.rstrip("/") + "/index.html"

    return rel.replace("\\", "/"), anchor, "internal"


# --- Per-page checks ---------------------------------------------------------
def check_nav_group_page(relpath, content, rep):
    # 1. exactly one nav
    n = len(NAV_BLOCK_RE.findall(content))
    if n != 1:
        rep.fail(relpath, "nav-count", f'<nav class="nav"> count = {n} (expected 1)')
        nav_block = ""
    else:
        nav_block = NAV_BLOCK_RE.search(content).group(0)

    # 2. Version A signature
    for sig in NAV_SIGNATURE:
        if sig not in nav_block:
            rep.fail(relpath, "nav-signature", f"missing signature: {sig!r}")


def check_topnav_group_page(relpath, content, rep):
    n = len(TOPNAV_BLOCK_RE.findall(content))
    if n != 1:
        rep.fail(relpath, "topnav-count", f'<nav class="topnav"> count = {n} (expected 1)')
        nav_block = ""
    else:
        nav_block = TOPNAV_BLOCK_RE.search(content).group(0)
    for sig in TOPNAV_SIGNATURE:
        if sig not in nav_block:
            rep.fail(relpath, "topnav-signature", f"missing signature: {sig!r}")


def check_research_group_page(relpath, content, rep):
    """Global-.nav gate for a research page (DR-2026-062, plan §3).

    Per in-scope research page:
      - exactly 1 <nav class="nav"> block carrying the Version-A signature;
      - 0 × class="topnav";
      - 0 × topnav-brand;
      - 0 × page-local chrome CSS (.footer { / .footer-blocks / .footer-inner);
      - exactly 1 × /css/style.css link;
      - exactly 1 × class="nav__inner";
      - exactly 1 × the inverted topnav wordmark <strong>Product</strong>Beacon -> 0;
      - active state: research/index.html has exactly 1 Research a.active in the nav;
        inactive pages have 0.
      - (NOT gated: .nav__logo-text — it false-positives on the valid footer logo.)
    """
    # exactly one global nav block
    n = len(NAV_BLOCK_RE.findall(content))
    if n != 1:
        rep.fail(relpath, "nav-count", f'<nav class="nav"> count = {n} (expected 1)')
        nav_block = ""
    else:
        nav_block = NAV_BLOCK_RE.search(content).group(0)

    # Version A signature inside the nav
    for sig in NAV_SIGNATURE:
        if sig not in nav_block:
            rep.fail(relpath, "nav-signature", f"missing signature: {sig!r}")

    # zero legacy topnav residue
    nt = content.count('class="topnav"')
    if nt != 0:
        rep.fail(relpath, "topnav-residue", f'class="topnav" count = {nt} (expected 0)')
    ntb = content.count("topnav-brand")
    if ntb != 0:
        rep.fail(relpath, "topnav-brand-residue", f'topnav-brand count = {ntb} (expected 0)')

    # zero page-local chrome CSS rule definitions
    if re.search(r'\.footer\s*\{', content):
        rep.fail(relpath, "page-local-footer-css", 'page-local ".footer {" CSS rule present')
    if ".footer-blocks" in content:
        rep.fail(relpath, "page-local-footer-blocks",
                 '".footer-blocks" CSS present (legacy chrome)')
    if ".footer-inner" in content:
        rep.fail(relpath, "page-local-footer-inner",
                 '".footer-inner" CSS present (legacy chrome)')

    # exactly one global stylesheet link
    ncss = content.count("/css/style.css")
    if ncss != 1:
        rep.fail(relpath, "style-link-count",
                 f'/css/style.css link count = {ncss} (expected 1)')

    # exactly one nav__inner (proves the global nav markup, not just a class string)
    nni = content.count('class="nav__inner"')
    if nni != 1:
        rep.fail(relpath, "nav-inner-count",
                 f'class="nav__inner" count = {nni} (expected 1)')

    # inverted topnav wordmark must be gone
    nbad = content.count("<strong>Product</strong>Beacon")
    if nbad != 0:
        rep.fail(relpath, "inverted-wordmark",
                 f'"<strong>Product</strong>Beacon" count = {nbad} (expected 0)')

    # active state on the Research anchor
    active_re = re.compile(r'<a href="/research/" class="active">Research</a>')
    n_active = len(active_re.findall(nav_block)) if nav_block else 0
    state = RESEARCH_GROUP.get(relpath.replace("\\", "/"))
    if state == "active":
        if n_active != 1:
            rep.fail(relpath, "research-active",
                     f'Research a.active count = {n_active} (expected 1 for active page)')
    else:
        if n_active != 0:
            rep.fail(relpath, "research-active-unexpected",
                     f'Research a.active count = {n_active} (expected 0 for inactive page)')


def check_retired_chrome_markers(relpath, content, rep):
    # "Book a Call" INSIDE any <nav> block (body CTAs are Phase 4, allowed)
    for nav_block in ANY_NAV_RE.findall(content):
        if "Book a Call" in nav_block:
            rep.fail(relpath, "retired-nav-bookacall",
                     '"Book a Call" found inside a <nav> block')
        if ">Services<" in nav_block:
            rep.fail(relpath, "retired-nav-services",
                     '">Services<" nav link present')
        if ">Insights<" in nav_block:
            rep.fail(relpath, "retired-nav-insights",
                     '">Insights<" nav link present')

    # links to the retired services.html (chrome must not point at it)
    for href in HREF_RE.findall(content):
        h = href.strip()
        if h == "/services.html" or h.startswith("/services.html#") \
                or h == "services.html" or h.startswith("services.html#"):
            rep.fail(relpath, "retired-services-link", f"link to retired page: {href}")

    # {{ROOT}} template token anywhere
    if "{{ROOT}}" in content:
        rep.fail(relpath, "root-token", '"{{ROOT}}" template token present')

    # bare same-page anchors that must be absolute off-index
    if re.search(r'href="#intensive"', content):
        rep.fail(relpath, "bare-anchor-intensive",
                 'bare href="#intensive" (must be /index.html#intensive)')
    if re.search(r'href="#path"', content):
        rep.fail(relpath, "bare-anchor-path",
                 'bare href="#path" (must be /index.html#path)')


def check_ga4(relpath, content, rep):
    if GA4_ID not in content:
        rep.fail(relpath, "ga4-missing", f"GA4 id {GA4_ID} not present")


def check_footer_canonical(relpath, content, rep):
    m = FOOTER_BLOCK_RE.search(content)
    if not m:
        return  # 0-footer is allowed (reported by migrator, not a gate fail)
    footer = m.group(0)
    if "/services.html#fractional" in footer or "services.html#fractional" in footer:
        rep.fail(relpath, "footer-stale-services",
                 'stale "services.html#fractional" link in FOOTER')
    if "Fractional CPO" in footer:
        rep.fail(relpath, "footer-stale-fractional-cpo",
                 '"Fractional CPO" text in FOOTER (body copy is Phase 4, not this)')


def _chrome_region(content):
    """Concatenated nav + footer block text — the chrome the gate owns.
    A broken link/anchor INSIDE this region is GATING; outside it (page body)
    is a NON-gating warning (body links/CTAs are Phase 4 territory)."""
    parts = []
    for block_re in (ANY_NAV_RE, FOOTER_BLOCK_RE):
        for m in block_re.finditer(content):
            parts.append(m.group(0))
    return "\n".join(parts)


def check_links_and_anchors(relpath, content, id_index, rep):
    chrome = _chrome_region(content)
    own_ids = id_index.get(relpath.replace("\\", "/"), set())

    for href in HREF_RE.findall(content):
        target, anchor, kind = resolve_link_target(href, relpath)
        # Is this specific href occurrence inside the chrome region?
        in_chrome = (f'href="{href}"' in chrome)
        report = rep.fail if in_chrome else rep.warn
        scope = "" if in_chrome else " [BODY/Phase-4]"

        if kind == "external":
            continue
        if kind == "anchor-only":
            if anchor and anchor not in own_ids:
                report(relpath, "anchor-unresolved",
                       f'same-page #{anchor} has no matching id/name{scope}')
            continue
        # internal file link
        tnorm = (target or "").replace("\\", "/")
        if not (REPO / tnorm).exists():
            report(relpath, "link-unresolved",
                   f'broken internal link: {href} -> {tnorm}{scope}')
            continue
        # anchor on another page
        if anchor:
            target_ids = id_index.get(tnorm)
            if target_ids is None:
                tp = REPO / tnorm
                try:
                    tc = tp.read_text(encoding="utf-8", errors="replace")
                    target_ids = set(ID_RE.findall(tc)) | set(NAME_RE.findall(tc))
                    id_index[tnorm] = target_ids
                except Exception:
                    target_ids = set()
            if anchor not in target_ids:
                report(relpath, "cross-anchor-unresolved",
                       f'#{anchor} not found in {tnorm} (from link {href}){scope}')


# =============================================================================
# SEO GATE (Phase 6) — owned by 🔍 SEO Specialist.
# Spec: migration-seo-workstream-2026-06-08.md §8.
#
# This is a SEPARATE gate from the chrome gate. The chrome gate (Phase 3) must
# be able to PASS while body/Phase-4 items remain; the SEO gate (Phase 6) is the
# launch-readiness gate for discovery scaffolding. Run via:
#     python scripts/verify-migration.py --seo
# Both gates can run together (default runs chrome; --seo runs the SEO gate too).
# Each exits non-zero on any of ITS OWN violations.
# =============================================================================

SITE = "https://productbeacon.agency"

# Pages that MUST carry a specific JSON-LD @type (spec §5 / §8).
REQUIRED_JSONLD = {
    "index.html": {"Organization", "FAQPage"},
    "vision-to-value/index.html": {"Book"},
    "about.html": {"Person"},
    "decision-provenance-standard.html": {"DefinedTerm", "TechArticle"},  # either is acceptable
}
# For DPS, EITHER DefinedTerm OR TechArticle satisfies the gate.
JSONLD_ANY_OF = {"decision-provenance-standard.html"}

# Retired/redirected/operational URL fragments that must NEVER appear in sitemap.
SITEMAP_FORBIDDEN_SUBSTR = [
    "/services.html",
    "/axia-offer.html",
    "/gtm-engine.html",
    "/strategic-infrastructure.html",
    "/insights/index.html",
    "/reports/",          # legacy duplicate tree (now stubs)
    "/prospects/",
    "/planning/",
    "/analysis/",
    "/brief.html",        # old state-of-cyber brief -> pre-call-brief
]

# Expected redirect-stub targets (spec §1.2): retired page -> canonical 301 target path.
EXPECTED_STUB_TARGETS = {
    "services.html": "/on-call.html",
    "axia-offer.html": "/",
    "gtm-engine.html": "/",
    "strategic-infrastructure.html": "/",
    "insights/index.html": "/research/",
}

JSONLD_RE = re.compile(
    r'<script[^>]+type="application/ld\+json"[^>]*>([\s\S]*?)</script>', re.I)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', re.I)
META_PROP_RE = re.compile(
    r'<meta[^>]+(?:property|name)="([^"]+)"[^>]+content="([^"]*)"', re.I)
REFRESH_RE = re.compile(
    r'<meta[^>]+http-equiv="refresh"[^>]+content="\s*\d+\s*;\s*url=([^"]+)"', re.I)


def _expected_canonical(relpath):
    """Self-referential canonical URL for an in-scope page.
    Directory index.html canonicalizes to the directory form with trailing
    slash (matches the deployed scaffolding convention)."""
    rel = relpath.replace("\\", "/")
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[:-len("index.html")]  # keep trailing slash
    return SITE + "/" + rel


def _jsonld_types(content):
    """Return (set_of_types, list_of_parse_errors) for all JSON-LD blocks."""
    import json
    types = set()
    errors = []
    for block in JSONLD_RE.findall(content):
        try:
            data = json.loads(block)
        except Exception as e:  # noqa: BLE001
            errors.append(str(e))
            continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            if isinstance(it, dict):
                t = it.get("@type")
                if isinstance(t, list):
                    types.update(t)
                elif t:
                    types.add(t)
    return types, errors


def seo_check_page(relpath, content, rep):
    """Per-page SEO scaffolding gate (spec §8)."""
    rel = relpath.replace("\\", "/")

    # 1. Self-referential canonical: exactly one, correct target, no fragment/query.
    canons = CANONICAL_RE.findall(content)
    if len(canons) == 0:
        rep.fail(rel, "seo-canonical-missing", "no <link rel=canonical>")
    elif len(canons) > 1:
        rep.fail(rel, "seo-canonical-multiple",
                 f"{len(canons)} canonical tags (expected 1)")
    else:
        c = canons[0].strip()
        if "#" in c or "?" in c:
            rep.fail(rel, "seo-canonical-dirty",
                     f"canonical has fragment/query: {c}")
        elif c != _expected_canonical(rel):
            rep.fail(rel, "seo-canonical-wrong",
                     f"canonical {c} != self {_expected_canonical(rel)}")

    # 2. OG + Twitter card.
    metas = dict(META_PROP_RE.findall(content))
    for need in ("og:title", "og:description", "og:type", "og:url", "og:image"):
        if need not in metas:
            rep.fail(rel, "seo-og-missing", f"missing {need}")
    if "twitter:card" not in metas:
        rep.fail(rel, "seo-twitter-missing", "missing twitter:card")

    # 3. og:image must point at the existing asset (resolve to a repo file).
    ogimg = metas.get("og:image", "")
    if ogimg:
        if ogimg.startswith(SITE):
            img_rel = ogimg[len(SITE):].lstrip("/")
        elif ogimg.startswith("/"):
            img_rel = ogimg.lstrip("/")
        else:
            img_rel = ogimg
        img_rel = img_rel.split("#")[0].split("?")[0]
        if img_rel and not (REPO / img_rel).exists():
            rep.fail(rel, "seo-ogimage-404",
                     f"og:image asset not found in repo: {ogimg}")

    # 4. og:url should match the canonical (self URL).
    ogurl = metas.get("og:url", "")
    if ogurl and ogurl.strip() != _expected_canonical(rel):
        rep.fail(rel, "seo-ogurl-mismatch",
                 f"og:url {ogurl} != self {_expected_canonical(rel)}")

    # 5. Required JSON-LD per page + validity of all blocks.
    types, errors = _jsonld_types(content)
    for err in errors:
        rep.fail(rel, "seo-jsonld-parse", f"JSON-LD parse error: {err}")
    if rel in REQUIRED_JSONLD:
        need = REQUIRED_JSONLD[rel]
        if rel in JSONLD_ANY_OF:
            if not (need & types):
                rep.fail(rel, "seo-jsonld-required",
                         f"need ONE of {sorted(need)}; found {sorted(types)}")
        else:
            missing = need - types
            if missing:
                rep.fail(rel, "seo-jsonld-required",
                         f"missing JSON-LD @type {sorted(missing)}; "
                         f"found {sorted(types)}")

    # 6. No noindex on a page that should be indexed (in-scope = indexable).
    robots_meta = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]*)"',
                            content, re.I)
    if robots_meta and "noindex" in robots_meta.group(1).lower():
        rep.fail(rel, "seo-unexpected-noindex",
                 f'in-scope page carries noindex: {robots_meta.group(1)}')


def seo_check_sitemap(rep):
    """sitemap.xml purity (spec §3.1 / §8): all live in-scope URLs present,
    zero retired/operational URLs, well-formed XML."""
    p = REPO / "sitemap.xml"
    if not p.exists():
        rep.fail("sitemap.xml", "seo-sitemap-missing", "sitemap.xml not found")
        return
    raw = p.read_text(encoding="utf-8", errors="replace")
    # well-formed
    try:
        import xml.etree.ElementTree as ET
        ET.fromstring(raw)
    except Exception as e:  # noqa: BLE001
        rep.fail("sitemap.xml", "seo-sitemap-malformed", f"XML parse error: {e}")
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", raw)
    locset = set(locs)

    # 6a. No forbidden / retired URLs present.
    for loc in locs:
        for bad in SITEMAP_FORBIDDEN_SUBSTR:
            if bad in loc:
                rep.fail("sitemap.xml", "seo-sitemap-forbidden",
                         f"retired/operational URL in sitemap: {loc}")
                break

    # 6b. Every live in-scope page must be present (as its canonical URL).
    for rel in ALLOWLIST:
        want = _expected_canonical(rel)
        if want not in locset:
            rep.fail("sitemap.xml", "seo-sitemap-missing-url",
                     f"in-scope page absent from sitemap: {want} ({rel})")

    # 6c. Homepage must be present.
    if (SITE + "/") not in locset:
        rep.fail("sitemap.xml", "seo-sitemap-no-home",
                 "homepage URL missing from sitemap")


def seo_check_robots(rep):
    """robots.txt (spec §3.2 / §8): AI crawlers allowed; operational dirs
    disallowed; sitemap line present; state-of-cyber NOT disallowed."""
    p = REPO / "robots.txt"
    if not p.exists():
        rep.fail("robots.txt", "seo-robots-missing", "robots.txt not found")
        return
    txt = p.read_text(encoding="utf-8", errors="replace")
    low = txt.lower()

    for bot in ("gptbot", "claudebot", "google-extended", "perplexitybot"):
        if bot not in low:
            rep.fail("robots.txt", "seo-robots-aibot",
                     f"AI crawler not declared: {bot}")

    for d in ("/prospects/", "/planning/", "/analysis/", "/reports/"):
        if f"disallow: {d}".lower() not in low:
            rep.fail("robots.txt", "seo-robots-disallow",
                     f"missing Disallow: {d}")

    # state-of-cyber must NOT be disallowed (it's the public sub-brand).
    if re.search(r"disallow:\s*/research/state-of-cyber-2026/", low):
        rep.fail("robots.txt", "seo-robots-soc-blocked",
                 "/research/state-of-cyber-2026/ wrongly disallowed")

    if "sitemap:" not in low:
        rep.fail("robots.txt", "seo-robots-sitemap-line",
                 "Sitemap: line missing")


def seo_check_redirect_stubs(rep):
    """Each retired page is a noindex meta-refresh to the CORRECT canonical
    target (spec §1.2 / §8). services->on-call; orphans->/; insights idx->/research/."""
    for stub_rel, target_path in EXPECTED_STUB_TARGETS.items():
        p = REPO / stub_rel
        if not p.exists():
            rep.fail(stub_rel, "seo-stub-missing",
                     "expected redirect stub file does not exist")
            continue
        c = p.read_text(encoding="utf-8", errors="replace")
        want_url = SITE + target_path

        # meta-refresh target
        m = REFRESH_RE.search(c)
        if not m:
            rep.fail(stub_rel, "seo-stub-no-refresh",
                     "no <meta http-equiv=refresh> redirect")
        elif m.group(1).strip() != want_url:
            rep.fail(stub_rel, "seo-stub-wrong-target",
                     f"meta-refresh -> {m.group(1).strip()} (expected {want_url})")

        # canonical points at the target
        cm = CANONICAL_RE.search(c)
        if not cm:
            rep.fail(stub_rel, "seo-stub-no-canonical", "stub has no canonical")
        elif cm.group(1).strip() != want_url:
            rep.fail(stub_rel, "seo-stub-wrong-canonical",
                     f"canonical -> {cm.group(1).strip()} (expected {want_url})")

        # noindex,follow present
        rm = re.search(r'<meta[^>]+name="robots"[^>]+content="([^"]*)"', c, re.I)
        if not rm or "noindex" not in rm.group(1).lower():
            rep.fail(stub_rel, "seo-stub-no-noindex",
                     "stub missing noindex robots meta")


def seo_check_ogimage_asset(rep):
    """og-image.png exists at repo root and is 1200x630 (spec §8)."""
    p = REPO / "og-image.png"
    if not p.exists():
        rep.fail("og-image.png", "seo-ogimage-missing",
                 "og-image.png not found at repo root")
        return
    # read PNG IHDR dimensions without PIL dependency
    try:
        import struct
        with open(p, "rb") as f:
            data = f.read(26)
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            rep.fail("og-image.png", "seo-ogimage-notpng", "not a valid PNG")
            return
        w, h = struct.unpack(">II", data[16:24])
        if (w, h) != (1200, 630):
            rep.fail("og-image.png", "seo-ogimage-dims",
                     f"og-image.png is {w}x{h} (expected 1200x630)")
    except Exception as e:  # noqa: BLE001
        rep.fail("og-image.png", "seo-ogimage-read", f"cannot read PNG: {e}")


def seo_check_oncall_heir(rep):
    """on-call.html is the fractional ranking heir: visible H1/H2 must carry
    the preserved fractional terms; services.html stub must 301 to it (spec §2/§8)."""
    p = REPO / "on-call.html"
    if not p.exists():
        rep.fail("on-call.html", "seo-oncall-missing", "on-call.html not found")
        return
    c = p.read_text(encoding="utf-8", errors="replace")
    heads = " ".join(re.findall(r'<h[12][^>]*>([\s\S]*?)</h[12]>', c, re.I))
    heads_text = re.sub(r"<[^>]+>", " ", heads).lower()
    if "fractional" not in heads_text:
        rep.fail("on-call.html", "seo-oncall-no-fractional",
                 'no "fractional" term in any visible H1/H2 (equity heir)')
    if "product leadership" not in heads_text:
        rep.fail("on-call.html", "seo-oncall-no-prodleadership",
                 'no "product leadership" term in any visible H1/H2')


def run_seo_gate(verbose=False):
    """Full Phase-6 SEO gate. Returns a Report."""
    rep = Report()
    print(f"verify-migration SEO gate: {len(ALLOWLIST)} in-scope pages")

    for rel in ALLOWLIST:
        p = REPO / rel
        if not p.exists():
            rep.fail(rel, "seo-page-missing", "in-scope page does not exist")
            continue
        content = p.read_text(encoding="utf-8", errors="replace")
        before = len(rep.violations)
        seo_check_page(rel, content, rep)
        if verbose and len(rep.violations) == before:
            print(f"  SEO PASS  {rel}")

    seo_check_sitemap(rep)
    seo_check_robots(rep)
    seo_check_redirect_stubs(rep)
    seo_check_ogimage_asset(rep)
    seo_check_oncall_heir(rep)
    return rep


# --- Driver ------------------------------------------------------------------
def run_chrome_gate(verbose=False):
    rep = Report()

    # Defensive: allowlist must not contain forbidden dirs or retire pages —
    # EXCEPT the three soc pages individually carved out of the directory guard
    # (DR-2026-062). Mirrors migrate-chrome.py's _check_allowlist_safety().
    for rel in ALLOWLIST:
        nr = rel.replace("\\", "/")
        if nr in SOC_CARVE_OUTS:
            continue
        for pref in FORBIDDEN_PREFIXES:
            if nr.startswith(pref):
                print(f"ABORT: allowlist contains forbidden path: {rel}", file=sys.stderr)
                sys.exit(2)
        if nr in RETIRE_PAGES:
            print(f"ABORT: allowlist contains retire-bucket page: {rel}", file=sys.stderr)
            sys.exit(2)

    # existence
    missing = [rel for rel in ALLOWLIST if not (REPO / rel).exists()]
    if missing:
        for rel in missing:
            rep.fail(rel, "missing-file", "allowlisted file does not exist")

    id_index = build_id_index()

    print(f"verify-migration: {len(ALLOWLIST)} in-scope pages "
          f"({len(NAV_GROUP)} class=\"nav\" + {len(RESEARCH_GROUP)} research "
          f"+ {len(TOPNAV_GROUP)} legacy-topnav)")

    for rel in NAV_GROUP:
        if (REPO / rel).exists():
            content = read(rel)
            before = len(rep.violations)
            check_nav_group_page(rel, content, rep)
            check_retired_chrome_markers(rel, content, rep)
            check_ga4(rel, content, rep)
            check_footer_canonical(rel, content, rep)
            check_links_and_anchors(rel, content, id_index, rep)
            if verbose and len(rep.violations) == before:
                print(f"  PASS  {rel}")

    for rel in RESEARCH_GROUP:
        if (REPO / rel).exists():
            content = read(rel)
            before = len(rep.violations)
            check_research_group_page(rel, content, rep)
            check_retired_chrome_markers(rel, content, rep)
            check_ga4(rel, content, rep)
            check_footer_canonical(rel, content, rep)
            check_links_and_anchors(rel, content, id_index, rep)
            if verbose and len(rep.violations) == before:
                print(f"  PASS  {rel}")

    for rel in TOPNAV_GROUP:
        if (REPO / rel).exists():
            content = read(rel)
            before = len(rep.violations)
            check_topnav_group_page(rel, content, rep)
            check_retired_chrome_markers(rel, content, rep)
            check_ga4(rel, content, rep)
            check_footer_canonical(rel, content, rep)
            check_links_and_anchors(rel, content, id_index, rep)
            if verbose and len(rep.violations) == before:
                print(f"  PASS  {rel}")
    return rep


def _report_gate(name, rep, show_warnings=False):
    print("-" * 64)
    if show_warnings and rep.warnings:
        print(f"NON-GATING WARNINGS (body / Phase-4 — do NOT block the chrome gate): "
              f"{len(rep.warnings)}")
        for relpath, check, detail in rep.warnings:
            print(f"  WARN [{check}] {relpath}: {detail}")
        print("-" * 64)
    if rep.ok():
        print(f"{name} GATE PASS: 0 violations.")
        return 0
    print(f"{name} GATE FAIL: {len(rep.violations)} violation(s):")
    for relpath, check, detail in rep.violations:
        print(f"  [{check}] {relpath}: {detail}")
    return 1


def main():
    verbose = "--verbose" in sys.argv
    seo_only = "--seo-only" in sys.argv
    run_seo = seo_only or ("--seo" in sys.argv)

    exit_code = 0

    if not seo_only:
        print(f"verify-migration: {len(ALLOWLIST)} in-scope pages "
              f"({len(NAV_GROUP)} class=\"nav\" + {len(TOPNAV_GROUP)} topnav)")
        chrome_rep = run_chrome_gate(verbose=verbose)
        exit_code |= _report_gate("CHROME", chrome_rep, show_warnings=True)

    if run_seo:
        seo_rep = run_seo_gate(verbose=verbose)
        exit_code |= _report_gate("SEO", seo_rep)

    sys.exit(1 if exit_code else 0)


if __name__ == "__main__":
    main()
