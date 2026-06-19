#!/bin/bash
# Pre-commit hook to sync theme and export styles in archviz
echo "Checking python dependencies compatibility..."
.venv/bin/pip check
if [ $? -ne 0 ]; then
    echo "ERROR: Broken requirements found in virtual environment. Commit aborted."
    exit 1
fi

echo "Syncing theme and export templates..."
python3 scripts/sync_theme.py
python3 scripts/sync_export.py
git add templates/html/*.html

