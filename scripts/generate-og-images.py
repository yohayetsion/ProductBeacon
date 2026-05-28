"""
Round 15 P0-1 — OG image generator for State of Cyber 2026 launch surfaces.

Renders 3 PNGs at 1200x630 (landing.png, pre-call-brief.png, report-digest.png)
into research/og/ using Playwright headless Chromium.

Brand tokens: slate-900 #0F172A bg, amber #F59E0B accent, Inter + JetBrains Mono.
Reproducible: run from repo root: `python scripts/generate-og-images.py`.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path(__file__).parent.parent
OUT_DIR = REPO / "research" / "og"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1200px; height: 630px; overflow: hidden; }
body {
  font-family: 'Inter', system-ui, sans-serif;
  background: #0F172A;
  color: #F1F5F9;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 64px 80px;
  position: relative;
}
body::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 6px;
  background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 50%, #F59E0B 100%);
}
.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #F59E0B;
}
.brand-dot {
  width: 10px;
  height: 10px;
  background: #F59E0B;
  border-radius: 50%;
}
.eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #FBBF24;
  margin-bottom: 18px;
}
h1 {
  font-size: 64px;
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.025em;
  color: #F8FAFC;
  margin-bottom: 24px;
}
.subtitle {
  font-size: 28px;
  font-weight: 400;
  line-height: 1.35;
  color: #CBD5E1;
  max-width: 980px;
}
.footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.byline {
  font-size: 20px;
  font-weight: 500;
  color: #E2E8F0;
}
.byline-meta {
  display: block;
  font-size: 15px;
  font-weight: 400;
  color: #94A3B8;
  margin-top: 4px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.04em;
}
.tag {
  display: inline-block;
  padding: 8px 16px;
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.4);
  border-radius: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 500;
  color: #FBBF24;
  letter-spacing: 0.08em;
}
.chapters {
  font-family: 'JetBrains Mono', monospace;
  font-size: 22px;
  font-weight: 500;
  color: #94A3B8;
  letter-spacing: 0.06em;
  margin-top: 18px;
}
.chapters span { color: #F59E0B; }
</style>
"""


def template(eyebrow: str, title: str, subtitle: str, chapters_line: str = "", tag: str = "") -> str:
    eyebrow_html = f'<div class="eyebrow">{eyebrow}</div>' if eyebrow else ""
    chapters_html = f'<div class="chapters">{chapters_line}</div>' if chapters_line else ""
    tag_html = f'<div class="tag">{tag}</div>' if tag else ""
    return f"""<!doctype html>
<html><head><meta charset="utf-8">{BASE_CSS}</head>
<body>
  <div>
    <div class="brand"><span class="brand-dot"></span>ProductBeacon Research</div>
  </div>
  <div>
    {eyebrow_html}
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    {chapters_html}
  </div>
  <div class="footer">
    <div class="byline">
      Yohay Etsion
      <span class="byline-meta">productbeacon.agency / research</span>
    </div>
    {tag_html}
  </div>
</body></html>
"""


IMAGES = [
    {
        "name": "landing.png",
        "eyebrow": "",
        "title": "State of Cyber Security Markets 2026",
        "subtitle": "Independent research on Insider Risk, Data Loss Prevention, DSPM, and the Convergence Synthesis.",
        "chapters_line": "<span>IRM</span> &nbsp;·&nbsp; <span>DLP</span> &nbsp;·&nbsp; <span>DSPM</span> &nbsp;·&nbsp; <span>Convergence</span>",
        "tag": "280 CITATIONS / ZERO VENDOR SPONSORS",
    },
    {
        "name": "pre-call-brief.png",
        "eyebrow": "Pre-Call Briefing Pack",
        "title": "State of Cyber 2026",
        "subtitle": "Three Pattern Claims. Three buyer choices. Falsifiable tests on DSPM consolidation, Thoma Bravo Proofpoint, and agentic AI data security.",
        "chapters_line": "",
        "tag": "ANALYST PRE-READ",
    },
    {
        "name": "report-digest.png",
        "eyebrow": "Report Digest · 14 pages",
        "title": "State of Cyber 2026",
        "subtitle": "Chapter-by-chapter synthesis: Insider Risk Management, Data Loss Prevention, DSPM, and the Convergence Synthesis.",
        "chapters_line": "<span>IRM</span> &nbsp;·&nbsp; <span>DLP</span> &nbsp;·&nbsp; <span>DSPM</span> &nbsp;·&nbsp; <span>Convergence</span>",
        "tag": "280 CITATIONS",
    },
    {
        "name": "umbrella.png",
        "eyebrow": "",
        "title": "Independent Cyber & Product Research",
        "subtitle": "Market analysis with every claim cited. No vendor sponsors, no paywalled data, no analyst-firm reuse.",
        "chapters_line": "",
        "tag": "ZERO VENDOR SPONSORS",
    },
    {
        "name": "methodology.png",
        "eyebrow": "Methodology",
        "title": "How the research is built",
        "subtitle": "Sourcing rules, citation discipline, the Verifiable Proxy Rule, and a quarterly refresh cadence.",
        "chapters_line": "",
        "tag": "OPEN-WEB SOURCED",
    },
]


def render_all():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for img in IMAGES:
            html = template(
                eyebrow=img["eyebrow"],
                title=img["title"],
                subtitle=img["subtitle"],
                chapters_line=img["chapters_line"],
                tag=img["tag"],
            )
            page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
            page.set_content(html, wait_until="networkidle")
            page.wait_for_timeout(800)
            out = OUT_DIR / img["name"]
            page.screenshot(path=str(out), full_page=False, omit_background=False, type="png")
            print(f"wrote {out} ({out.stat().st_size} bytes)")
            page.close()
        browser.close()


if __name__ == "__main__":
    render_all()
