"""
Asset validation sweep — compares every deployed asset against its required
outcome (cumulative Round 15 + 16 + audit spec). Reports PASS/FAIL per check.

Run: python scripts/validate-assets.py
"""

import re
import json
import sys
import urllib.request

ORIGIN = "https://productbeacon.agency"
UA = {"User-Agent": "Mozilla/5.0 (asset-validator)"}

results = []  # (severity, area, asset, check, status, detail)


def add(area, asset, check, ok, detail="", sev="P1"):
    results.append((sev, area, asset, check, "PASS" if ok else "FAIL", detail))


def fetch(path):
    url = path if path.startswith("http") else ORIGIN + path
    try:
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=20)
        return r.getcode(), r.read().decode("utf-8", "ignore"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, "", {}
    except Exception as e:
        return None, f"ERR:{e}", {}


def head_code(path):
    url = ORIGIN + path
    try:
        req = urllib.request.Request(url, headers=UA, method="GET")
        r = urllib.request.urlopen(req, timeout=20)
        return r.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


# ---- Page inventory + expected outcomes ----
SLASH = "/research/state-of-cyber-2026/"
CONTENT_PAGES = {
    "umbrella":     {"url": "/research/",                 "ogimg": "umbrella.png",     "schema": ["CollectionPage", "BreadcrumbList"], "breadcrumb": False, "axia": True},
    "methodology":  {"url": "/research/methodology.html", "ogimg": "methodology.png",  "schema": ["Article", "BreadcrumbList"],        "breadcrumb": False, "axia": True},
    "author":       {"url": "/research/author.html",      "ogimg": "landing.png",      "schema": ["Person", "BreadcrumbList"],         "breadcrumb": False, "axia": True},
    "landing":      {"url": SLASH,                         "ogimg": "landing.png",      "schema": ["CollectionPage", "BreadcrumbList"], "breadcrumb": True,  "axia": True},
    "irm":          {"url": SLASH+"irm.html",              "ogimg": "landing.png",      "schema": ["Article", "BreadcrumbList"],        "breadcrumb": True,  "axia": False},
    "dlp":          {"url": SLASH+"dlp.html",              "ogimg": "landing.png",      "schema": ["Article", "BreadcrumbList"],        "breadcrumb": True,  "axia": True},
    "dspm":         {"url": SLASH+"dspm.html",             "ogimg": "landing.png",      "schema": ["Article", "BreadcrumbList"],        "breadcrumb": True,  "axia": False},
    "convergence":  {"url": SLASH+"convergence.html",      "ogimg": "landing.png",      "schema": ["Article", "BreadcrumbList"],        "breadcrumb": True,  "axia": True},
    "pack":         {"url": SLASH+"pre-call-brief.html",   "ogimg": "pre-call-brief.png","schema": ["Report", "BreadcrumbList"],        "breadcrumb": True,  "axia": True},
    "digest":       {"url": SLASH+"synthesis.html",        "ogimg": "report-digest.png","schema": ["Report", "BreadcrumbList"],         "breadcrumb": True,  "axia": True},
}

CHANNEL_NAMES = ["GLG", "Guidepoint", "Dialectica", "Third Bridge", "AlphaSights"]

print("Fetching pages...", file=sys.stderr)
pages = {}
for name, spec in CONTENT_PAGES.items():
    code, html, hdrs = fetch(spec["url"])
    pages[name] = (code, html)
    add("status", name, "HTTP 200", code == 200, f"got {code}", sev="P0")

# ---- Per-page checks ----
for name, spec in CONTENT_PAGES.items():
    code, html = pages[name]
    if code != 200 or not html:
        continue

    # canonical present
    canon = re.search(r'rel="canonical" href="([^"]+)"', html)
    add("canonical", name, "canonical present", bool(canon), canon.group(1) if canon else "missing")

    # title length <= 60
    t = re.search(r"<title>([^<]*)</title>", html)
    if t:
        tl = len(t.group(1))
        add("meta", name, "title <=60", tl <= 60, f"{tl} chars: {t.group(1)}")

    # description 120-160
    d = re.search(r'<meta name="description" content="([^"]*)"', html)
    if d:
        dl = len(d.group(1))
        add("meta", name, "desc 120-160", 120 <= dl <= 160, f"{dl} chars")

    # OG completeness
    for prop in ["og:title", "og:description", "og:image", "og:url"]:
        add("og", name, prop, f'property="{prop}"' in html, "", sev="P2")
    for prop in ["twitter:card", "twitter:image"]:
        add("og", name, prop, f'name="{prop}"' in html, "", sev="P2")

    # OG image correct per page
    ogimg = re.search(r'property="og:image" content="[^"]*/og/([^"]+)"', html)
    if ogimg:
        add("og", name, "og:image correct", ogimg.group(1) == spec["ogimg"], f"got {ogimg.group(1)}, want {spec['ogimg']}")

    # JSON-LD parses + expected types
    blocks = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.DOTALL)
    types_found = []
    parse_ok = True
    for b in blocks:
        try:
            obj = json.loads(b.strip())
            items = obj if isinstance(obj, list) else [obj]
            for it in items:
                tt = it.get("@type")
                if isinstance(tt, list):
                    types_found.extend(tt)
                elif tt:
                    types_found.append(tt)
        except json.JSONDecodeError as e:
            parse_ok = False
            add("schema", name, "JSON-LD parses", False, str(e), sev="P0")
    if parse_ok:
        add("schema", name, "JSON-LD parses", True, f"{len(blocks)} blocks")
    for want in spec["schema"]:
        add("schema", name, f"schema {want}", want in types_found, f"found {types_found}", sev="P2")

    # breadcrumb presence per spec
    has_bc = 'aria-label="Breadcrumb"' in html
    add("breadcrumb", name, "breadcrumb" + ("" if spec["breadcrumb"] else " absent"),
        has_bc == spec["breadcrumb"], f"present={has_bc}, expected={spec['breadcrumb']}", sev="P2")

    # AXIA scope
    axia_n = html.count("AXIA")
    if spec["axia"]:
        add("axia", name, "AXIA disclosure present", axia_n >= 1, f"{axia_n} mentions", sev="P0")
    else:
        add("axia", name, "AXIA absent (non-DLP chapter)", axia_n == 0, f"{axia_n} mentions", sev="P0")

    # wrong category / title must not appear
    add("axia", name, "no 'competes in IRM'", "competes in IRM" not in html, "", sev="P0")
    add("axia", name, "no 'competes in DSPM'", "competes in DSPM" not in html, "", sev="P0")
    add("axia", name, "no 'Fractional Chief Product Officer'", "Fractional Chief Product Officer" not in html, "", sev="P1")

    # book date
    add("content", name, "no (2003)", "(2003)" not in html, "", sev="P1")

    # /about/ 404 link must not exist
    add("links", name, "no broken /about/ link", 'href="/about/"' not in html, "", sev="P1")

    # em-dash in title/description (additions)
    title_desc = (t.group(1) if t else "") + (d.group(1) if d else "")
    add("content", name, "no em-dash in title/desc", "—" not in title_desc, "", sev="P2")

    # channel-name leak
    leaked = [c for c in CHANNEL_NAMES if c in html]
    add("leak", name, "no channel names", not leaked, f"found {leaked}" if leaked else "", sev="P0")

# DLP/Convergence must say "competes in DLP"
for name in ["dlp", "convergence"]:
    _, html = pages[name]
    add("axia", name, "says 'competes in DLP'", "competes in DLP" in html, "", sev="P1")

# ---- OG images ----
for img in ["landing.png", "pre-call-brief.png", "report-digest.png", "umbrella.png", "methodology.png"]:
    code = head_code("/research/og/" + img)
    add("ogimg", img, "loads 200", code == 200, f"got {code}", sev="P1")

# ---- Stubs ----
STUBS = ["irm.html", "dlp.html", "dspm.html", "convergence.html",
         "irm-podcast.html", "dlp-podcast.html", "dspm-podcast.html", "convergence-podcast.html",
         "launch-strategy.html"]
for s in STUBS:
    code, html, _ = fetch("/reports/state-of-cyber-2026/" + s)
    ok200 = code == 200
    redirects = ("http-equiv=\"refresh\"" in html and "/research/state-of-cyber-2026/" + s in html)
    add("stub", "reports/"+s, "serves 200", ok200, f"got {code}")
    add("stub", "reports/"+s, "meta-refresh to research/", redirects, "", sev="P1")
    add("stub", "reports/"+s, "no stale AXIA in stub", "AXIA" not in html, "")

# brief.html stub
code, html, _ = fetch(SLASH + "brief.html")
add("stub", "brief.html", "serves 200", code == 200, f"got {code}")
add("stub", "brief.html", "redirects to pre-call-brief", "pre-call-brief.html" in html and 'http-equiv="refresh"' in html, "", sev="P1")
add("stub", "brief.html", "no stale AXIA", "AXIA" not in html, "")

# ---- robots + sitemap ----
code, robots, _ = fetch("/robots.txt")
add("infra", "robots.txt", "200", code == 200, f"got {code}")
add("infra", "robots.txt", "has sitemap pointer", "Sitemap:" in robots, "")
code, sm, _ = fetch("/sitemap.xml")
add("infra", "sitemap.xml", "200", code == 200, f"got {code}")
add("infra", "sitemap.xml", "author.html listed", "author.html" in sm, "")
add("infra", "sitemap.xml", "lastmod all 2026-05-28", sm.count("2026-05-28") >= 10 and not re.search(r"2026-05-(19|25|27)", sm), f"{sm.count('2026-05-28')} dated 05-28")
add("infra", "sitemap.xml", "brief.html NOT listed", "/brief.html" not in sm, "", sev="P2")

# ---- PDFs (live 200) ----
for p in ["irm.pdf", "dlp.pdf", "dspm.pdf", "convergence.pdf", "synthesis.pdf", "pre-call-brief.pdf"]:
    code = head_code(SLASH + p)
    add("pdf", p, "loads 200", code == 200, f"got {code}", sev="P2")

# ---- About page ----
add("links", "about.html", "resolves 200", head_code("/about.html") == 200, "", sev="P1")

# ---- "About the author" cross-link on 9 surfaces ----
AUTHOR_LINK_SURFACES = ["umbrella", "methodology", "landing", "irm", "dlp", "dspm", "convergence", "pack", "digest"]
for name in AUTHOR_LINK_SURFACES:
    _, html = pages[name]
    has = "/research/author.html" in html
    add("xlink", name, "author bio cross-link", has, "", sev="P1")

# ---- 3 audience doors on landing (id="audience-doors" > ul.doors-list > 3 li) ----
_, landing_html = pages["landing"]
doors_block = re.search(r'id="audience-doors".*?</section>', landing_html, re.DOTALL)
db = doors_block.group(0) if doors_block else ""
li_n = len(re.findall(r"<li", db))
add("audience", "landing", "audience-doors section present", bool(doors_block), "", sev="P1")
add("audience", "landing", "3 audience doors (li)", li_n >= 3, f"{li_n} doors", sev="P1")
# the 3 audience segments incl. the restored fractional-founder door
for seg, label in [("PE analyst", "analyst/investor"), ("CISO", "ciso"), ("founder", "fractional-founder")]:
    add("audience", "landing", f"door: {label}", seg.lower() in db.lower(), "", sev="P2")

# ---- SVG diagram titles per chapter ----
SVG_EXPECT = {"irm": 5, "dlp": 6, "dspm": 5, "convergence": 3}
for name, want in SVG_EXPECT.items():
    _, html = pages[name]
    n = len(re.findall(r"<title id=", html))
    add("svg", name, f"diagram titles ({want})", n >= want, f"{n} titled (want >={want})", sev="P2")

# ---- presentations repo assets ----
PRES = "https://yohayetsion.github.io/presentations/"
code, ai, _ = fetch(PRES + "asset-index.html")
add("pres", "asset-index", "200", code == 200, f"got {code}")
add("pres", "asset-index", "no em-dash", "—" not in ai, "", sev="P2")
add("pres", "asset-index", "Set G present", "Set G" in ai or "Deployed" in ai, "")
add("pres", "asset-index", "Internal Assets section", "Internal Assets" in ai, "")
code = head_code if False else None
ca_code, _, _ = fetch(PRES + "state-of-cyber-2026-call-answers.html")
add("pres", "call-answers", "200", ca_code == 200, f"got {ca_code}", sev="P2")

# ==== Report ====
fails = [r for r in results if r[4] == "FAIL"]
p0 = [r for r in fails if r[0] == "P0"]
p1 = [r for r in fails if r[0] == "P1"]
p2 = [r for r in fails if r[0] == "P2"]

print(f"\n{'='*70}\nASSET VALIDATION SWEEP\n{'='*70}")
print(f"Total checks: {len(results)}  |  PASS: {len(results)-len(fails)}  |  FAIL: {len(fails)}")
print(f"  P0 fails: {len(p0)}   P1 fails: {len(p1)}   P2 fails: {len(p2)}\n")

if fails:
    print("FAILURES:")
    for sev in ["P0", "P1", "P2"]:
        for r in [x for x in fails if x[0] == sev]:
            print(f"  [{r[0]}] {r[1]}/{r[2]} :: {r[3]} -- {r[5]}")
else:
    print("ALL CHECKS PASS.")
