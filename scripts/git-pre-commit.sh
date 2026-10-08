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

# Independent of the sync/prettier block below (whose order is load-bearing),
# so it runs first: fail fast on a drifted palette registry rather than after
# a formatting pass. Mirrors the same-named CI step.
echo "Checking palette registry consistency..."
python3 "$ROOT/scripts/check_palette_registry.py"

# Same class of problem, same placement: fail fast before the sync/prettier
# block. SKILL.md metadata.version is the truth; CHANGELOG.md, pyproject.toml
# and publish-skill.py must agree with it.
echo "Checking version consistency..."
python3 "$ROOT/scripts/check_version_consistency.py"

# Order is load-bearing and must match .github/workflows/ci.yml:
#   sync modules -> prettier --write -> stage
# Prettier re-indents the embedded <style>/<script> blocks that the sync
# scripts paste in, so a sync-only commit can never satisfy CI's
# `git diff --exit-code` check. Both sync scripts exit non-zero if a template
# is missing its anchor, which aborts the commit on purpose.
echo "Syncing theme and export templates..."
python3 "$ROOT/scripts/sync_theme.py"
python3 "$ROOT/scripts/sync_export.py"

echo "Formatting synced templates with Prettier..."
npx --yes prettier@3.9.9 --write "templates/html/*.html"

# Stage HTML templates only if still inside a git commit
if git rev-parse --git-dir >/dev/null 2>&1; then
    git add templates/html/*.html 2>/dev/null || true
fi
