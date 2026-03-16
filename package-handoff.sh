#!/usr/bin/env bash
# package-handoff.sh — sync and zip Handoff-File-Drop
#
# Copies all current source files into Handoff-File-Drop, then zips it.
# Run this from the Timeline-JEL root before sending the handoff.
#
# Usage:
#   bash package-handoff.sh

set -e
HANDOFF="Handoff-File-Drop"

echo "Syncing files into $HANDOFF…"

# App code
cp index.html                         "$HANDOFF/index.html"
cp utilities/cv-utilities.js          "$HANDOFF/utilities/cv-utilities.js"
cp utilities/orcid-utilities.js       "$HANDOFF/utilities/orcid-utilities.js"

# Static assets
cp image/logo.png                     "$HANDOFF/image/logo.png"

# Data
cp data/taglines.js                   "$HANDOFF/data/taglines.js"
cp data/people-images.js              "$HANDOFF/data/people-images.js"
cp data/cv-data/cv-data-public.js     "$HANDOFF/data/cv-data/cv-data-public.js"
cp data/cv-data/pub-images.js         "$HANDOFF/data/cv-data/pub-images.js"

# Re-apply handoff-specific index.html patches:
#   1. Remove timeline-data.js and mode-public script tags from <head>
#   2. Replace auto-load block to always load cv-data-public.js
python3 - "$HANDOFF/index.html" <<'PYEOF'
import sys, re

path = sys.argv[1]
html = open(path, encoding='utf-8').read()

# 1. Remove timeline-data.js and mode-public lines from <head>
html = re.sub(r'\n<script src="data/timeline-data/timeline-data\.js"></script>', '', html)
html = re.sub(r'\n<script>if \(location\.search\.includes\(\'public\'\)\).*?</script>', '', html)

# 2. Replace auto-load block
old = re.search(
    r'// ── Auto-load ──.*?(?=\n// ── Synthetic test data)',
    html, re.DOTALL
).group(0)
new = (
    '// ── Auto-load ─────────────────────────────────────────────────────────────\n'
    '// Always load cv-data-public.js as the default data source.\n'
    'const _s = document.createElement(\'script\');\n'
    '_s.src = \'data/cv-data/cv-data-public.js\';\n'
    '_s.onload = () => parse(window.__TIMELINE_DATA__);\n'
    'document.head.appendChild(_s);'
)
html = html.replace(old, new)

open(path, 'w', encoding='utf-8').write(html)
print('  Patched index.html')
PYEOF

# Zip
ZIP="Handoff-File-Drop.zip"
rm -f "$ZIP"
zip -r "$ZIP" "$HANDOFF" --exclude "*.DS_Store"
echo "✓ Created $ZIP"
