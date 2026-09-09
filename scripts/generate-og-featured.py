"""
OG / social cards for the three LinkedIn "Featured" links (2026-09-08).

Renders 1200x630 PNGs with Playwright headless Chromium into og/ (site root):
  og/vision-to-value.png   - the book page, with the real hardcover front cover
  og/workforce.png         - the workforce page (15 teams, 96 specialists)
  og/research.png          - the research hub (State of Cyber 2026 + State of WEM 2026)
  og/home.png              - the homepage (Product Leadership, At Scale); also copied over
                             og-image.png, the fallback card every other page reuses

Brand tokens: slate-900 #0F172A bg, amber #F59E0B accent, Inter + JetBrains Mono
(same tokens as scripts/generate-og-images.py).

The book cover is cropped from the KDP hardcover wrap PDF (front panel, bleed
trimmed) and embedded as a data URI so the card is reproducible from this file
plus the wrap PDF. Run from repo root:  python scripts/generate-og-featured.py
"""

import base64
import io
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).parent.parent
OUT_DIR = REPO / "og"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COVER_WRAP_PDF = Path(
    r"G:\My Drive\Claude\Vision to Value\Content\Book\print-production\v2v-cover-hardcover-6x9-343pp.pdf"
)


def front_cover_data_uri() -> str:
    """Render page 1 of the hardcover wrap, crop the front panel, return a PNG data URI."""
    import fitz  # PyMuPDF
    from PIL import Image

    doc = fitz.open(str(COVER_WRAP_PDF))
    pix = doc[0].get_pixmap(dpi=150)  # 2194 x 1563 for this wrap
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    # Front panel sits right of the spine (spine ends at ~x=1175 at 150 dpi); trim 0.125in bleed.
    bleed = 19
    front = img.crop((1180, bleed, pix.width - bleed, pix.height - bleed))
    front = front.resize((int(front.width * 0.55), int(front.height * 0.55)), Image.LANCZOS)
    buf = io.BytesIO()
    front.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1200px; height: 630px; overflow: hidden; }
body {
  font-family: 'Inter', system-ui, sans-serif;
  background: #0F172A;
  color: #F1F5F9;
  position: relative;
  padding: 56px 72px;
  display: flex; flex-direction: column; justify-content: space-between;
}
body::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 6px;
  background: linear-gradient(90deg, #F59E0B 0%, #FBBF24 50%, #F59E0B 100%);
}
body::after {
  content: ''; position: absolute; top: -260px; right: -260px; width: 700px; height: 700px;
  border-radius: 50%; background: radial-gradient(circle, rgba(245,158,11,0.16), transparent 70%);
  pointer-events: none;
}
.brand { display: flex; align-items: center; gap: 12px; font-family: 'JetBrains Mono', monospace;
  font-size: 16px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #F59E0B; }
.brand-dot { width: 10px; height: 10px; background: #F59E0B; border-radius: 50%; }
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 17px; font-weight: 500;
  letter-spacing: 0.18em; text-transform: uppercase; color: #FBBF24; margin-bottom: 16px; }
h1 { font-size: 62px; font-weight: 800; line-height: 1.05; letter-spacing: -0.025em; color: #F8FAFC; margin-bottom: 20px; }
h1 .amber { color: #F59E0B; }
.subtitle { font-size: 26px; font-weight: 400; line-height: 1.35; color: #CBD5E1; }
.footer { display: flex; justify-content: space-between; align-items: flex-end; position: relative; z-index: 1; }
.byline { font-size: 20px; font-weight: 500; color: #E2E8F0; }
.byline-meta { display: block; font-size: 15px; color: #94A3B8; margin-top: 4px;
  font-family: 'JetBrains Mono', monospace; letter-spacing: 0.04em; }
.tag { display: inline-block; padding: 8px 16px; background: rgba(245,158,11,0.12);
  border: 1px solid rgba(245,158,11,0.4); border-radius: 6px; font-family: 'JetBrains Mono', monospace;
  font-size: 14px; font-weight: 500; color: #FBBF24; letter-spacing: 0.08em; }
.mid { position: relative; z-index: 1; }

/* book */
.book-layout { display: grid; grid-template-columns: 1fr 340px; gap: 48px; align-items: center; height: 100%; }
.cover { width: 340px; height: 521px; border-radius: 6px; overflow: hidden;
  box-shadow: 0 30px 60px rgba(0,0,0,0.55), 0 0 0 1px rgba(255,255,255,0.08);
  position: absolute; right: 72px; top: 54px; }
.cover img { width: 100%; height: 100%; display: block; }
.book-lines { font-size: 22px; color: #CBD5E1; line-height: 1.5; margin-top: 22px; }
.book-lines span { color: #F59E0B; font-weight: 600; }

/* workforce */
.chips { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 26px; max-width: 1000px; }
.chip { font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 500; letter-spacing: 0.04em;
  color: #E2E8F0; background: rgba(148,163,184,0.10); border: 1px solid rgba(148,163,184,0.28);
  border-radius: 999px; padding: 7px 14px; }
.stats { display: flex; gap: 40px; margin-top: 6px; }
.stat b { display: block; font-size: 44px; font-weight: 800; letter-spacing: -0.02em; color: #F59E0B; line-height: 1; }
.stat span { display: block; font-size: 15px; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.08em;
  text-transform: uppercase; color: #94A3B8; margin-top: 8px; }

/* home */
.layers { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 16px; margin-top: 26px; max-width: 900px; }
.layer { display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 600; color: #E2E8F0; }
.layer i { width: 12px; height: 12px; border-radius: 50%; background: #F59E0B; flex: none; }
.layer small { font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: #94A3B8; display: block; font-weight: 500; }

/* research */
.reports { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 8px; }
.report { background: rgba(15,23,42,0.6); border: 1px solid rgba(148,163,184,0.25); border-left: 4px solid #F59E0B;
  border-radius: 10px; padding: 24px 26px; }
.report .k { font-family: 'JetBrains Mono', monospace; font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; color: #FBBF24; }
.report h2 { font-size: 34px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.1; margin: 10px 0 12px; color: #F8FAFC; }
.report p { font-size: 18px; line-height: 1.4; color: #CBD5E1; }
</style>
"""


def shell(body: str) -> str:
    return f"<!doctype html><html><head><meta charset='utf-8'>{BASE_CSS}</head><body>{body}</body></html>"


def book_card(cover_uri: str) -> str:
    return shell(f"""
  <div class="brand"><span class="brand-dot"></span>ProductBeacon</div>
  <div class="mid" style="max-width:700px">
    <div class="eyebrow">The book · read online free</div>
    <h1>Vision <span class="amber">to</span> Value</h1>
    <p class="subtitle">A Blueprint for Product Organizations. How to build, scale, and sustain a winning product organization, written from the top seat.</p>
    <p class="book-lines"><span>Free online</span> · PDF &amp; EPUB · Hardcover on Amazon</p>
  </div>
  <div class="footer">
    <div class="byline">Yohay Etsion<span class="byline-meta">productbeacon.agency / vision-to-value</span></div>
  </div>
  <div class="cover"><img src="{cover_uri}" alt=""></div>
""")


TEAMS = [
    "Product", "Design", "Architecture", "Development", "Marketing", "Sales", "Customer Success",
    "Finance", "Legal", "HR", "Operations", "Data", "IT Governance", "Corp Dev", "Executive",
]


def workforce_card() -> str:
    chips = "".join(f'<span class="chip">{t}</span>' for t in TEAMS)
    return shell(f"""
  <div class="brand"><span class="brand-dot"></span>ProductBeacon</div>
  <div class="mid">
    <div class="eyebrow">The ProductBeacon AI Workforce</div>
    <h1>A workforce you govern. <span class="amber">Every specialist named.</span></h1>
    <div class="stats">
      <div class="stat"><b>15</b><span>teams</span></div>
      <div class="stat"><b>96</b><span>specialists</span></div>
      <div class="stat"><b>250</b><span>skills</span></div>
      <div class="stat"><b>120</b><span>knowledge libraries</span></div>
    </div>
    <div class="chips">{chips}</div>
  </div>
  <div class="footer">
    <div class="byline">Yohay Etsion<span class="byline-meta">productbeacon.agency / workforce</span></div>
    <div class="tag">FINISHED WORK IN HOURS · DECISIONS STAY YOURS</div>
  </div>
""")


def research_card() -> str:
    return shell("""
  <div class="brand"><span class="brand-dot"></span>ProductBeacon Research</div>
  <div class="mid">
    <div class="eyebrow">Independent market research · 2026</div>
    <div class="reports">
      <div class="report">
        <div class="k">Cybersecurity</div>
        <h2>State of Cyber 2026</h2>
        <p>Eight fronts across two parts: the data battlegrounds (IRM, DLP, DSPM) and the platform wars (SOC, Edge, AI Security, Identity). 596 citations.</p>
      </div>
      <div class="report">
        <div class="k">Workforce Engagement Management</div>
        <h2>State of WEM 2026</h2>
        <p>Five graded markets plus a Convergence synthesis: WFO / WEM collapsing onto one AI engine and re-pricing from per-seat to per-outcome. 223 sources.</p>
      </div>
    </div>
  </div>
  <div class="footer">
    <div class="byline">Yohay Etsion<span class="byline-meta">productbeacon.agency / research</span></div>
    <div class="tag">EVERY CLAIM CITED · ZERO VENDOR SPONSORS</div>
  </div>
""")


def home_card() -> str:
    return shell("""
  <div class="brand"><span class="brand-dot"></span>ProductBeacon</div>
  <div class="mid">
    <h1>Product Leadership, <span class="amber">At Scale.</span></h1>
    <p class="subtitle" style="max-width:960px">A published product-leadership blueprint, a governed AI workforce, and experienced human leadership, so one accountable person can hold the whole loop from vision to delivered value.</p>
    <div class="layers">
      <div class="layer"><i></i><div><small>Blueprint</small>Vision to Value</div></div>
      <div class="layer"><i></i><div><small>Human decision bridge</small>The Decision Provenance Standard</div></div>
      <div class="layer"><i></i><div><small>Workforce</small>96 governed specialists, 15 teams</div></div>
      <div class="layer"><i></i><div><small>Foundation</small>Durable organisational context</div></div>
    </div>
  </div>
  <div class="footer">
    <div class="byline">Yohay Etsion<span class="byline-meta">productbeacon.agency</span></div>
    <div class="tag">A NAMED HUMAN REMAINS ACCOUNTABLE</div>
  </div>
""")


def render_all():
    cards = {
        "vision-to-value.png": book_card(front_cover_data_uri()),
        "workforce.png": workforce_card(),
        "research.png": research_card(),
        "home.png": home_card(),
    }
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, html in cards.items():
            page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
            page.set_content(html, wait_until="networkidle")
            page.wait_for_timeout(900)
            out = OUT_DIR / name
            page.screenshot(path=str(out), full_page=False, type="png")
            print(f"wrote {out} ({out.stat().st_size} bytes)")
            page.close()
        browser.close()
    # The homepage card doubles as the site-wide fallback every other page reuses.
    import shutil
    shutil.copyfile(OUT_DIR / "home.png", REPO / "og-image.png")
    print("copied og/home.png -> og-image.png")


if __name__ == "__main__":
    render_all()
