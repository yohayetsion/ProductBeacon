#!/usr/bin/env python3
"""Relight report figure SVGs from the dark-web theme to a light (print) theme,
in place, for every *.html in the given build directory.

Hue-preserving luminance flip:  light text -> dark text, dark card fills -> light
pastels, bright strokes -> dark. Tag-aware (text vs shapes) so it never inverts
the wrong element. Only figure SVGs (viewBox "0 0 800 ...") are touched; the
28/32px logo + favicon SVGs are left alone.

Usage:  python scripts/pdf-relight.py <build_dir>
Pairs with scripts/pdf-render.js to produce the light-theme + cover-page chapter PDFs.
"""
import colorsys, re, os, sys, glob

BUILD = sys.argv[1]

def h2rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def rgb2h(r, g, b): return '#%02X%02X%02X' % (round(r * 255), round(g * 255), round(b * 255))
def lum(h):
    r, g, b = h2rgb(h); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def relight(h, L, Smax):
    r, g, b = h2rgb(h); hh, l, s = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, L, min(s, Smax)); return rgb2h(r, g, b)
def text_dark(h):  return relight(h, 0.22, 0.85)   # light text  -> dark text
def card_light(h): return relight(h, 0.92, 0.45)   # dark card   -> light pastel
def stroke_dark(h):return relight(h, 0.42, 0.90)   # bright stroke -> dark stroke

def fix_tag(tagname, tag):
    is_text = (tagname == 'text')
    def fill_attr(m):
        hx = m.group(2)
        if is_text:
            return m.group(1) + (text_dark(hx) if lum(hx) > 0.5 else hx) + m.group(3)
        return m.group(1) + (card_light(hx) if lum(hx) < 0.42 else hx) + m.group(3)
    tag = re.sub(r'(fill=")(#[0-9a-fA-F]{3,6})(")', fill_attr, tag)
    def fill_style(m):
        hx = m.group(2)
        new = (text_dark(hx) if (is_text and lum(hx) > 0.5) else
               card_light(hx) if (not is_text and lum(hx) < 0.42) else hx)
        return m.group(1) + new + m.group(3)
    tag = re.sub(r'(style="[^"]*fill:\s*)(#[0-9a-fA-F]{3,6})([^"]*")', fill_style, tag)
    if not is_text:
        def stroke_attr(m):
            hx = m.group(2)
            return m.group(1) + (stroke_dark(hx) if lum(hx) > 0.55 else hx) + m.group(3)
        tag = re.sub(r'(stroke=")(#[0-9a-fA-F]{3,6})(")', stroke_attr, tag)
    return tag

TAG_RE = re.compile(r'<(text|rect|circle|ellipse|polygon|path|polyline|line)\b[^>]*>')

def fix_style_block(m):
    body = m.group(0)
    def rule(rm):
        cls = rm.group(1).lower(); decl = rm.group(2)
        is_card = cls.endswith('box') or cls in ('node', 'panel')   # NOT 'wildcard'
        def f(fm):
            hx = fm.group(1)
            if is_card: return 'fill: ' + (card_light(hx) if lum(hx) < 0.42 else hx)
            return 'fill: ' + (text_dark(hx) if lum(hx) > 0.5 else hx)
        decl = re.sub(r'fill:\s*(#[0-9a-fA-F]{3,6})', f, decl)
        def s(sm):
            hx = sm.group(1)
            return 'stroke: ' + (stroke_dark(hx) if lum(hx) > 0.55 else hx)
        decl = re.sub(r'stroke:\s*(#[0-9a-fA-F]{3,6})', s, decl)
        return '.' + rm.group(1) + ' {' + decl + '}'
    return re.sub(r'\.([\w-]+)\s*\{([^}]*)\}', rule, body)

STYLE_RE = re.compile(r'<style>.*?</style>', re.DOTALL)
FIG_RE = re.compile(r'<svg\b[^>]*viewBox="0 0 800[^>]*>.*?</svg>', re.DOTALL)

def fix_figure(svg):
    svg = STYLE_RE.sub(fix_style_block, svg)
    svg = TAG_RE.sub(lambda m: fix_tag(m.group(1).lower(), m.group(0)), svg)
    # market-map: light rgba axis/border lines -> dark so they show on white
    svg = svg.replace('stroke="rgba(226,232,240,0.28)"', 'stroke="rgba(15,23,42,0.45)"')
    svg = svg.replace('stroke="rgba(148,163,184,0.18)"', 'stroke="rgba(15,23,42,0.22)"')
    svg = svg.replace('stroke="rgba(148,163,184,0.20)"', 'stroke="rgba(15,23,42,0.25)"')
    return svg

for fn in sorted(glob.glob(os.path.join(BUILD, '*.html'))):
    s = open(fn, encoding='utf-8').read()
    n = len(FIG_RE.findall(s))
    s = FIG_RE.sub(lambda m: fix_figure(m.group(0)), s)
    open(fn, 'w', encoding='utf-8').write(s)
    print(f"  relit {os.path.basename(fn)}: {n} figures")
