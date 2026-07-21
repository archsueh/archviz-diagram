#!/bin/bash
# Pre-commit: optional venv check + theme/export sync + prettier on HTML templates
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "Checking python dependencies compatibility..."
if [ -x "$ROOT/.venv/bin/pip" ]; then
    if ! "$ROOT/.venv/bin/pip" check; then
        echo "ERROR: Broken requirements found in virtual environment. Commit aborted."
        exit 1
    fi
else
    echo "No .venv/bin/pip — skipping pip check."
fi

echo "Syncing theme and export templates..."
python3 "$ROOT/scripts/sync_theme.py"
python3 "$ROOT/scripts/sync_export.py"

echo "Formatting synced templates with Prettier..."
npx --yes prettier --write "templates/html/*.html"

# Stage HTML templates only if still inside a git commit
if git rev-parse --git-dir >/dev/null 2>&1; then
    git add templates/html/*.html 2>/dev/null || true
fi
