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


if __name__ == "__main__":
    main()
