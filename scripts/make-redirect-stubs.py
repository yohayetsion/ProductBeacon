"""
Round 16 audit P1-B/P1-E workaround — meta-refresh redirect stubs.

The CF Pages `_redirects` + `_worker.js` mechanisms are inert on this project
(repo-root files not processed). Meta-refresh stubs ARE plain static HTML, which
CF serves correctly, so this is the working repo-only redirect for retired URLs.

Replaces the stale duplicate `reports/*.html` tree + `brief.html` with tiny
stubs that redirect to their canonical `research/` equivalents. Removes the
stale wrong-category AXIA disclosure content from those duplicate pages.

PDFs (reports/*.pdf, brief.pdf) + citations.md can't meta-refresh; left as-is.

Reproducible: `python scripts/make-redirect-stubs.py`.
"""

from pathlib import Path

REPO = Path(__file__).parent.parent
ORIGIN = "https://productbeacon.agency"

STUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url={origin}{dest}">
<link rel="canonical" href="{origin}{dest}">
<meta name="robots" content="noindex, follow">
<title>Page moved | ProductBeacon Research</title>
</head>
<body style="font-family: system-ui, -apple-system, sans-serif; background:#0F172A; color:#F1F5F9; padding:48px; text-align:center; line-height:1.6;">
<p>This page has moved to <a href="{origin}{dest}" style="color:#F59E0B;">{origin}{dest}</a>.</p>
<script>location.replace("{origin}{dest}");</script>
</body>
</html>
"""

# reports/state-of-cyber-2026/{name} -> research/state-of-cyber-2026/{name}
REPORTS_DIR = REPO / "reports" / "state-of-cyber-2026"
REPORTS_HTML = [
    "irm.html", "dlp.html", "dspm.html", "convergence.html",
    "irm-podcast.html", "dlp-podcast.html", "dspm-podcast.html", "convergence-podcast.html",
    "launch-strategy.html",
]

# special-case: research/.../brief.html -> pre-call-brief.html
SPECIAL = {
    REPO / "research" / "state-of-cyber-2026" / "brief.html":
        "/research/state-of-cyber-2026/pre-call-brief.html",
}

# Operator-intensive migration Phase 5 dispositions (2026-06-08).
# Retired marketing surfaces -> canonical Version A targets. These OVERWRITE the
# retired pages with noindex meta-refresh stubs. CF Bulk Redirects (real 301s)
# take precedence at the edge; these are the repo-only belt-and-suspenders.
# insights/index.html is the HUB only -- the ~14 article index.html pages STAY live.
DISPOSITIONS = {
    REPO / "services.html": "/on-call.html",
    REPO / "axia-offer.html": "/",
    REPO / "gtm-engine.html": "/",
    REPO / "strategic-infrastructure.html": "/",
    REPO / "insights" / "index.html": "/research/",
}


def write_wem_stubs():
    """Keep the former WFO report addresses working after the WEM URL migration.

    The deployed host does not execute _redirects. Instant meta refresh is the
    HTML fallback; JavaScript additionally preserves query strings and fragments.
    Legacy PDFs/images remain available because HTML cannot redirect binaries.
    """
    canonical_dir = REPO / "research" / "state-of-wem-2026"
    if not canonical_dir.is_dir():
        return
    for target in sorted(canonical_dir.rglob("*.html")):
        relative = target.relative_to(canonical_dir)
        destination = "/research/state-of-wem-2026/" + relative.as_posix()
        if relative.as_posix() == "index.html":
            destination = "/research/state-of-wem-2026/"
        elif relative.as_posix() == "brief.html":
            destination = "/research/state-of-wem-2026/pre-call-brief.html"
        final_file = REPO / destination.lstrip("/")
        if destination.endswith("/"):
            final_file = final_file / "index.html"
        if not final_file.is_file():
            raise RuntimeError(f"Missing WEM redirect destination: {destination}")
        legacy = REPO / "research" / "state-of-wfo-2026" / relative
        legacy.parent.mkdir(parents=True, exist_ok=True)
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="0; url={destination}">
<link rel="canonical" href="{ORIGIN}{destination}">
<meta name="robots" content="noindex, follow">
<title>Page moved | ProductBeacon Research</title>
<script>location.replace("{destination}" + location.search + location.hash);</script>
</head>
<body>
<p>This report has moved to <a href="{destination}">its new address</a>.</p>
</body>
</html>
'''
        legacy.write_text(html, encoding="utf-8")
        print(f"stub: {legacy.relative_to(REPO)} -> {destination}")


def write_stub(path: Path, dest: str):
    path.write_text(STUB.format(origin=ORIGIN, dest=dest), encoding="utf-8")
    print(f"stub: {path.relative_to(REPO)} -> {dest}")


def main():
    for name in REPORTS_HTML:
        src = REPORTS_DIR / name
        if not src.exists():
            print(f"SKIP (missing): {src.relative_to(REPO)}")
            continue
        dest = f"/research/state-of-cyber-2026/{name}"
        # verify destination exists locally before pointing at it
        dest_local = REPO / "research" / "state-of-cyber-2026" / name
        if not dest_local.exists():
            print(f"WARN: dest missing for {name} ({dest_local.relative_to(REPO)}) - stub still written")
        write_stub(src, dest)

    for path, dest in SPECIAL.items():
        if path.exists():
            write_stub(path, dest)
        else:
            print(f"SKIP (missing): {path.relative_to(REPO)}")

    print("--- migration dispositions (2026-06-08) ---")
    for path, dest in DISPOSITIONS.items():
        if path.exists():
            write_stub(path, dest)
        else:
            print(f"SKIP (missing): {path.relative_to(REPO)}")

    write_wem_stubs()


if __name__ == "__main__":
    main()
