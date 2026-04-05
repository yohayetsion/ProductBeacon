#!/bin/bash
# inject-nav.sh — Replaces <nav>...</nav> blocks in all HTML files with
# the canonical nav from _includes/nav.html, adjusting relative paths.
#
# Usage: bash scripts/inject-nav.sh
# Run from the ProductBeacon repo root.

SITE_ROOT="C:/dev/ProductBeacon"
NAV_TEMPLATE="$SITE_ROOT/_includes/nav.html"

GA4_SNIPPET='<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TC1LMMGQGV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('"'"'js'"'"', new Date());
  gtag('"'"'config'"'"', '"'"'G-TC1LMMGQGV'"'"');
</script>'

inject_nav() {
  local file="$1"
  local root_prefix="$2"

  # Read template and replace {{ROOT}} with the correct relative path
  local nav_content
  nav_content=$(sed "s|{{ROOT}}|${root_prefix}|g" "$NAV_TEMPLATE")

  # Use Python for reliable multi-line replacement
  python3 -c "
import re, sys

with open('$file', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace nav block
nav_pattern = r'<!-- ====== NAV ====== -->.*?</nav>\s*\n\s*<div class=\"nav__mobile\".*?</div>\s*\n</nav>'
# More flexible pattern
nav_pattern = r'<nav class=\"nav\".*?</nav>\s*\n\s*<div class=\"nav__mobile\".*?</div>\s*\n</nav>'
# Simplest: match from nav opening comment to the closing </nav>
nav_content = '''$(echo "$nav_content" | sed "s/'/\\\\'/g")'''

# Replace everything between <!-- ====== NAV ====== --> and the last </nav> before main content
import re
pattern = r'<!-- ====== NAV ====== -->\s*<nav.*?</nav>\s*\n\s*<div class=\"nav__mobile\".*?</div>\s*\n</nav>'
# Try simpler approach: find <nav and match to second </nav>
content_new = re.sub(
    r'(<!-- ====== NAV ====== -->\n)?<nav class=\"nav\"[^>]*>.*?</nav>\s*\n\s*<div class=\"nav__mobile\"[^>]*>.*?</div>\s*\n</nav>',
    nav_content,
    content,
    count=1,
    flags=re.DOTALL
)

with open('$file', 'w', encoding='utf-8') as f:
    f.write(content_new)
" 2>/dev/null

  echo "  Injected nav into: $file"
}

echo "=== Nav Injection Script ==="
echo "Template: $NAV_TEMPLATE"
echo ""

# Root-level pages (prefix: empty)
for f in "$SITE_ROOT"/*.html; do
  [ -f "$f" ] && inject_nav "$f" ""
done

# insights/ hub (prefix: ../)
[ -f "$SITE_ROOT/insights/index.html" ] && inject_nav "$SITE_ROOT/insights/index.html" "../"

# insights/cybersecurity/ (prefix: ../../)
[ -f "$SITE_ROOT/insights/cybersecurity/index.html" ] && inject_nav "$SITE_ROOT/insights/cybersecurity/index.html" "../../"

# insights/{slug}/ pages (prefix: ../../)
for dir in "$SITE_ROOT"/insights/*/; do
  slug=$(basename "$dir")
  [ "$slug" = "cybersecurity" ] && continue
  [ -f "$dir/index.html" ] && inject_nav "$dir/index.html" "../../"
done

echo ""
echo "Done."
