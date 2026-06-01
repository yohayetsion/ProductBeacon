/**
 * Render the (relit) light-theme report chapter HTML to a paginated light PDF
 * with a cover page. Pairs with scripts/pdf-relight.py.
 *
 * Usage:  node scripts/pdf-render.js <build_dir> <out_dir>
 * Renders every *.html in <build_dir> to <out_dir>/<basename>.pdf.
 * Requires puppeteer + a local Chrome.
 */
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const BUILD = process.argv[2];
const OUT = process.argv[3];
const CHROME = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const DATE = 'June 2026';
const AUTHOR = 'Yohay Etsion';
const ROLE = 'Managing Director, ProductBeacon';

const LIGHT_CSS = `
  :root {
    --bg-dark:#ffffff !important; --bg:#ffffff !important; --bg-deep:#ffffff !important;
    --bg-card:#f8fafc !important; --bg-elevated:#f1f5f9 !important;
    --text-primary:#1f2937 !important; --text:#1f2937 !important;
    --text-secondary:#475569 !important; --text-muted:#6b7280 !important; --border:rgba(0,0,0,0.12) !important;
  }
  html, body { background:#ffffff !important; color:#1f2937 !important; }
  .slide, .review-slide-content { background:transparent !important; color:#1f2937 !important; }
  .slide::before { display:none !important; }
  h1,h2,h3,h4 { color:#1f2937 !important; }
  p, li, td, th, em, strong, .subtitle, blockquote { color:#1f2937 !important; }
  .section-label, .pattern-claim-title, .deck-breadcrumb a, a { color:#b45309 !important; }
  figcaption { color:#6b7280 !important; }
  .card, blockquote.card, .pattern-claim-callout, .insight-table, table { background:#f8fafc !important; color:#1f2937 !important; }
  .card *, blockquote *, .pattern-claim-callout * { color:#1f2937 !important; }
  code, pre, .mono, kbd { background:#eef2f7 !important; color:#1f2937 !important; }
  [style*="background:#0"], [style*="background: #0"], [style*="background:var(--bg"] { background:#f1f5f9 !important; }
  .slide { display:block !important; min-height:auto !important; height:auto !important;
           overflow:visible !important; page-break-after:auto !important; padding:6px 40px 14px !important; }
  .slide .brand-bar { display:none !important; }
  h1,h2,h3 { page-break-after:avoid; page-break-inside:avoid; }
  svg, .inline-diagram, figure, table, blockquote, .card, .pattern-claim-callout { page-break-inside:avoid; }
  .nav-bar, #navSections, #navDots, #jumpOverlay, .slide-jump-box,
  .comment-popover, .comment-badge, .toast, .format-selector,
  .review-slide-content .submit-area, nav.site-nav, header.site-header { display:none !important; }
  .commentable::after, .commentable:hover::after { content:none !important; display:none !important; }
  .commentable { border:none !important; background:transparent !important; }
  * { transition:none !important; animation:none !important; }
  .pdf-cover { page-break-after:always; min-height:248mm; display:flex; flex-direction:column;
               align-items:center; justify-content:center; text-align:center; padding:30mm 18mm; background:#fff; }
  .pdf-cover .rule { width:62%; height:3px; background:#F59E0B; margin-bottom:42px; }
  .pdf-cover .pb { font-family:'JetBrains Mono',monospace; letter-spacing:0.22em; font-size:12px; color:#b45309; font-weight:700; margin-bottom:40px; }
  .pdf-cover h1.cov { font-size:30px; line-height:1.28; color:#92400E; font-weight:800; max-width:84%; margin:0 0 40px; }
  .pdf-cover .auth { font-weight:700; color:#1f2937; font-size:15px; }
  .pdf-cover .org { color:#6b7280; font-size:13px; margin-top:4px; }
  .pdf-cover .date { color:#9ca3af; font-size:12px; margin-top:20px; font-family:'JetBrains Mono',monospace; }
`;

(async () => {
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });
  const files = fs.readdirSync(BUILD).filter(f => f.endsWith('.html'));
  const b = await puppeteer.launch({ headless: 'new', executablePath: CHROME, args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: 1100, height: 1500, deviceScaleFactor: 1 });
  for (const f of files) {
    const url = 'file://' + path.resolve(BUILD, f).replace(/\\/g, '/');
    await p.goto(url, { waitUntil: 'load' });
    await new Promise(r => setTimeout(r, 1400));
    await p.addStyleTag({ content: LIGHT_CSS });
    await p.evaluate((date, author, role) => {
      const hero = document.querySelector('.hero-title');
      if (!hero) return;
      const title = hero.textContent.trim();
      const s1 = document.querySelector('.slide'); if (s1) s1.style.display = 'none';
      const cover = document.createElement('div');
      cover.className = 'pdf-cover';
      cover.innerHTML = '<div class="rule"></div><div class="pb">PRODUCTBEACON RESEARCH</div>' +
        '<h1 class="cov">' + title + '</h1>' +
        '<div class="auth">' + author + '</div><div class="org">' + role + '</div>' +
        '<div class="date">' + date + '</div>';
      document.body.insertBefore(cover, document.body.firstChild);
    }, DATE, AUTHOR, ROLE);
    await new Promise(r => setTimeout(r, 300));
    const out = path.join(OUT, f.replace(/\.html$/, '.pdf'));
    await p.pdf({ path: out, printBackground: true, format: 'A4',
                  margin: { top: '16mm', bottom: '16mm', left: '14mm', right: '14mm' } });
    console.log('  rendered', path.basename(out), '(' + Math.round(fs.statSync(out).size / 1024) + ' KB)');
  }
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
