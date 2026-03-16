#!/usr/bin/env bash
# package-handoff-people.sh — build a self-contained People timeline handoff
#
# Produces Handoff/Handoff-People/ and Handoff/Handoff-People.zip.
# Auto-loads ra-team-data.js (the AbTeC People / RA team data).
#
# Usage:
#   bash package-handoff-people.sh

set -e
DEST="Handoff/Handoff-People"

echo "Building $DEST…"
rm -rf "$DEST"

# Directory structure
mkdir -p "$DEST/utilities"
mkdir -p "$DEST/image/abtec-team"
mkdir -p "$DEST/data/timeline-data"

# App code
cp index.html                         "$DEST/index.html"
cp utilities/cv-utilities.js          "$DEST/utilities/cv-utilities.js"
cp utilities/orcid-utilities.js       "$DEST/utilities/orcid-utilities.js"

# Static assets
cp image/logo.png                     "$DEST/image/logo.png"
cp image/abtec-team/*                 "$DEST/image/abtec-team/"

# Data
cp data/taglines.js                   "$DEST/data/taglines.js"
cp data/people-images.js              "$DEST/data/people-images.js"
cp data/timeline-data/ra-team-data.js "$DEST/data/timeline-data/ra-team-data.js"

# Patch index.html:
#   1. Swap timeline-data.js → ra-team-data.js in <head>
#   2. Remove mode-public script tag
python3 - "$DEST/index.html" <<'PYEOF'
import sys, re

path = sys.argv[1]
html = open(path, encoding='utf-8').read()

# 1. Swap the auto-load <script src> to ra-team-data.js
html = html.replace(
    '<script src="data/timeline-data/timeline-data.js"></script>',
    '<script src="data/timeline-data/ra-team-data.js"></script>'
)

# 2. Remove the mode-public script tag
html = re.sub(r'\n<script>if \(location\.search\.includes\(\'public\'\)\).*?</script>', '', html)

open(path, 'w', encoding='utf-8').write(html)
print('  Patched index.html')
PYEOF

# Zip
ZIP="Handoff/Handoff-People.zip"
rm -f "$ZIP"
zip -r "$ZIP" "$DEST" --exclude "*.DS_Store"
echo "✓ Created $ZIP"
