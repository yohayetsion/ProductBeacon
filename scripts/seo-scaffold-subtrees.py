#!/usr/bin/env python3
"""
seo-scaffold-subtrees.py — Phase-6 SEO scaffolding for the two in-scope subtrees
the Phase-3 chrome migration did NOT cover: the Vision to Value book reader
(vision-to-value/reader/*) and the insights/* article cluster.

Owned by 🔍 SEO Specialist. Spec: migration-seo-workstream-2026-06-08.md §4/§8.

For each target page it injects (idempotently) into <head>, right after <title>:
  - self-referential <link rel="canonical">  (directory index -> dir form)
  - og:type / og:site_name / og:title / og:description / og:url / og:image
  - twitter:card / twitter:title / twitter:description / twitter:image

Title is derived from the page's existing <title> (brand suffix trimmed for OG).
Description: reuse the page's <meta name=description> if present, else a sensible
subtree default. og:image: per-page insights/<co>/og.png if it EXISTS in the
repo, else the root /og-image.png (so the og:image always resolves -> no 404).

Run:  python scripts/seo-scaffold-subtrees.py            # apply
      python scripts/seo-scaffold-subtrees.py --dry-run  # preview only
"""
import re
import sys
from html import escape, unescape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = "https://productbeacon.agency"
DRY = "--dry-run" in sys.argv

READER_DESC = ("Vision to Value by Yohay Etsion frames the product organization "
               "as a decision system. Read this section of the book online, free. "
               "Book text licensed CC-BY 4.0.")
INSIGHTS_DESC = ("A ProductBeacon product-strategy insight: a public read of one "
                 "company's product positioning, market, and leadership signals.")

CANONICAL_RE = re.compile(r'<link[^>]+rel="canonical"', re.I)
TITLE_RE = re.compile(r'<title>([\s\S]*?)</title>', re.I)
DESC_RE = re.compile(
    r'<meta[^>]+name="description"[^>]+content="([^"]*)"', re.I)
OGANY_RE = re.compile(r'<meta[^>]+property="og:', re.I)


def expected_canonical(rel):
    rel = rel.replace("\\", "/")
    if rel.endswith("/index.html"):
        return SITE + "/" + rel[:-len("index.html")]
    return SITE + "/" + rel


def og_title(raw_title):
    """Trim a trailing ' <sep> Vision to Value' / ' <sep> ProductBeacon' brand."""
    t = unescape(raw_title).strip()
    # split on the last separator char (en/em dash, hyphen, bullet, pipe) + brand
    t = re.sub(r'\s*[|–—·\-]\s*(Vision to Value|ProductBeacon)\s*$',
               '', t).strip()
    return t or unescape(raw_title).strip()


def _present(content, prop):
    """True if a meta property/name (or canonical) is already on the page."""
    if prop == "canonical":
        return bool(CANONICAL_RE.search(content))
    return bool(re.search(
        r'<meta[^>]+(?:property|name)="' + re.escape(prop) + r'"', content, re.I))


def build_block(rel, content, og_image):
    """Build a <head> injection containing ONLY the tags this page is missing,
    so pages that already have some OG tags (insights/*) don't get duplicates."""
    canon = expected_canonical(rel)
    tm = TITLE_RE.search(content)
    raw_title = tm.group(1).strip() if tm else "ProductBeacon"
    title = og_title(raw_title)
    dm = DESC_RE.search(content)
    if dm and dm.group(1).strip():
        desc = unescape(dm.group(1).strip())
    elif rel.startswith("vision-to-value/reader/"):
        desc = f"{title}. {READER_DESC}"
    else:
        desc = f"{title}. {INSIGHTS_DESC}"
    ogtype = "book" if rel.startswith("vision-to-value/reader/") else "article"
    t = escape(title, quote=True)
    d = escape(desc, quote=True)
    img = og_image

    candidates = [
        ("canonical", f'<link rel="canonical" href="{canon}">'),
        ("og:type", f'<meta property="og:type" content="{ogtype}">'),
        ("og:site_name", '<meta property="og:site_name" content="ProductBeacon">'),
        ("og:title", f'<meta property="og:title" content="{t}">'),
        ("og:description", f'<meta property="og:description" content="{d}">'),
        ("og:url", f'<meta property="og:url" content="{canon}">'),
        ("og:image", f'<meta property="og:image" content="{img}">'),
        ("twitter:card", '<meta name="twitter:card" content="summary_large_image">'),
        ("twitter:title", f'<meta name="twitter:title" content="{t}">'),
        ("twitter:description", f'<meta name="twitter:description" content="{d}">'),
        ("twitter:image", f'<meta name="twitter:image" content="{img}">'),
    ]
    missing = [tag for prop, tag in candidates if not _present(content, prop)]
    return ("\n" + "\n".join(missing)) if missing else ""


def resolve_og_image(rel):
    """insights/<co>/og.png if it exists in repo, else root /og-image.png."""
    if rel.startswith("insights/"):
        co_dir = Path(rel).parent
        if (REPO / co_dir / "og.png").exists():
            return f"{SITE}/{co_dir.as_posix()}/og.png"
    return f"{SITE}/og-image.png"


def targets():
    out = []
    out += sorted(p.relative_to(REPO).as_posix()
                  for p in (REPO / "vision-to-value/reader").glob("*.html"))
    out += sorted(p.relative_to(REPO).as_posix()
                  for p in (REPO / "insights").glob("*/index.html"))
    return out


def main():
    changed = 0
    skipped = 0
    for rel in targets():
        p = REPO / rel
        content = p.read_text(encoding="utf-8")
        og_image = resolve_og_image(rel)
        orig = content

        # Step 1: repair any EXISTING og:image / twitter:image that points at a
        # non-resolving asset (the relative/missing per-page og.png case).
        def _fix_img(m):
            cur = m.group(2)
            # resolve current target to a repo path
            if cur.startswith(SITE):
                r = cur[len(SITE):].lstrip("/")
            elif cur.startswith("/"):
                r = cur.lstrip("/")
            else:  # relative to page dir
                r = (Path(rel).parent / cur).as_posix()
            r = r.split("#")[0].split("?")[0]
            if r and (REPO / r).exists():
                return m.group(0)  # already resolves -> leave it
            return m.group(1) + og_image + m.group(3)

        content = re.sub(
            r'(<meta[^>]+(?:property|name)="(?:og:image|twitter:image)"[^>]+content=")([^"]*)(")',
            _fix_img, content)

        # Step 2: inject ONLY the missing tags.
        block = build_block(rel, content, og_image)
        if block:
            if "</title>" in content:
                content = content.replace("</title>", "</title>" + block, 1)
            else:
                content = re.sub(r'(<head[^>]*>)', r'\1' + block, content, count=1)

        if content != orig:
            if not DRY:
                p.write_text(content, encoding="utf-8")
            action = "SCAFFOLD" if block else "REPAIR"
            print(f"  {action}  {rel}  (img={og_image.split('/')[-1]})")
            changed += 1
        else:
            skipped += 1

    print("-" * 60)
    print(f"{'DRY-RUN: would change' if DRY else 'changed'}: {changed}, skipped: {skipped}")


if __name__ == "__main__":
    main()
