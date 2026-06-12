# archviz Skill Publishing Norm (Pure CLI, Agent-Agnostic)

**Core Principle**: Publishing must be fully CLI-driven, repeatable, and respect archviz rules (absolute paths, no root temp files, no bloat, cross-agent compatibility, text-first).

This norm is inspired by automation ideas from qiaomu-skill-publisher but re-implemented as pure CLI (no Claude Code dependency). Use local Python + `gh` CLI only.

## When to Use
- Preparing a new release or major update of archviz-skills.
- User explicitly says "publish this skill", "push to GitHub", "release", or equivalent.
- Before any GitHub push of the skill itself.

## Prerequisites (CLI only)
```bash
# One-time
brew install gh          # or apt/yum equivalent
gh auth login            # GitHub token with repo scope

# Python (standard library + pyyaml for strict frontmatter)
python3 -c "import yaml" || pip3 install pyyaml
```

## The Pipeline (always run via CLI)
1. **cd to absolute project root** (never relative):
   ```bash
   cd /Users/mac/Developer/archviz-skills
   ```

2. **Validate & complete** (run the validation script below):
   - Strict YAML frontmatter check on `SKILL.md`
   - File existence checklist
   - Auto-generate missing LICENSE / basic README updates if needed (never overwrite user content)

3. **Dry-run summary** (print what will happen).

4. **Execute**:
   - `gh repo create` (if repo not linked) — support `--private` flag
   - Commit + push (use conventional commit)
   - Create GitHub Release + tag (vX.Y.Z)
   - Verify install path (print exact commands for different agents)

5. **Post-publish**:
   - Update local CHANGELOG.md (if not already)
   - Print final install instructions for Claude / Grok / Codex etc.

## Required SKILL.md Frontmatter Fields (strict validation)
From archviz current + lessons from external publishers:

```yaml
---
name: archviz-skills
description: |
  Restrained information visualization skill pack for AI agents. ...
version: "0.1.7"
license: MIT
metadata:
  source: https://github.com/archsueh/archviz-skills
  risk: safe
  author: archsueh
triggers: diagram, visualization, ...   # comma or list
---
```

**Validation rules** (enforced by script):
- `name`: required, kebab-case, ≤64 chars
- `description`: required, ≤1024 chars recommended (use block scalar `|` for multi-line)
- No inline double-quotes in simple strings (use block scalars for safety)
- `version` recommended
- `triggers` recommended for discoverability
- YAML must be parseable by strict loaders (no tabs, consistent indentation)

**Error examples to reject** (inspired by real publishers):
- `description: "contains "quotes""` → force block scalar
- Missing name/description → fail fast

## File Checklist (must exist before publish)
- SKILL.md (with valid frontmatter)
- README.md (with install instructions for multiple agents)
- LICENSE (MIT or matching)
- .gitignore (standard + no temp files)
- references/ (at least the core ones)
- templates/ (core)
- CHANGELOG.md (updated)
- (optional but recommended) examples/, docs/

The validation script should list missing items and offer to create minimal stubs.

## Recommended CLI Tooling (pure, no web)
- Python script for validation + orchestration (see proposed `scripts/publish-skill.py` below)
- `gh` for all GitHub operations
- `git` for local commit/tag

**Never** rely on web UIs, npx skills add as the only path, or Claude-specific directories.

## Absolute Path Discipline (non-negotiable)
All commands and scripts must use full absolute paths when referencing the skill (e.g. `/Users/mac/Developer/archviz-skills`).

No `cd <project root>` placeholders in final docs.

## Verification Step
After push/release, the script must output ready-to-copy install commands for:
- Claude Code (npx / direct clone)
- Grok / other agents (direct git clone into skill dir)
- Manual tarball path (if using old packaging)

## Anti-Patterns (Red Lines)
- Publishing without frontmatter validation
- Using relative paths in any release instruction
- Depending on Claude Code runtime for the publisher itself
- Skipping the plain fallback / text-first install instructions
- Creating temp files in ~ or root

## Proposed Implementation (the "patch")

Create `scripts/publish-skill.py` (pure Python + subprocess for gh/git).

Core functions:
- `validate_frontmatter(skill_dir)` — load SKILL.md, check required fields + YAML safety
- `check_files(skill_dir)` — return missing list
- `run_publish(skill_dir, private=False)` — orchestrate gh create/push/release

Example skeleton (to be implemented):

```python
#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path
import subprocess

ROOT = Path("/Users/mac/Developer/archviz-skills")  # absolute

def validate_frontmatter(skill_dir: Path):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit("SKILL.md missing")
    content = skill_md.read_text()
    if not content.startswith("---"):
        raise SystemExit("Missing YAML frontmatter")
    # parse frontmatter ...
    # check name, description, etc.
    # enforce block scalar for multi-line description
    print("✓ Frontmatter valid")

# ... similar for other checks and gh calls
```

Run as:
```bash
python3 /Users/mac/Developer/archviz-skills/scripts/publish-skill.py /Users/mac/Developer/archviz-skills --private
```

This replaces ad-hoc packaging while keeping everything CLI and absolute-path strict.

## Relation to Existing Files
- Complements (and can eventually replace) the old PACKAGING.md approach.
- Cross-reference from SKILL.md Resources.
- Keep `references/ascii-cli-alternatives.md` and workflow docs separate (they are for viz output, this is for skill meta-publishing).

## Maintenance
- Update this norm when frontmatter spec evolves (add new fields from SKILL.md).
- Run the validator in CI if possible.
- When adding new reference projects, note their publishing patterns here.

**Final rule**: The skill must be installable and discoverable by following only the printed CLI instructions after running this flow. No manual GitHub web steps allowed in the release process.
```

**Status of parallel execution**:
- SKILL.md reference addition: done (see edit above).
- New norm document: created at the path above.
- Analysis + patch: the document above contains the detailed analysis of qiaomu-skill-publisher (frontmatter name+description + YAML safety rules, auto file completion, gh automation, install verification) + concrete pure-CLI proposal for archviz (scripts/publish-skill.py skeleton + exact run commands using absolute paths).

You can now `mkdir -p /Users/mac/Developer/archviz-skills/scripts` and implement the Python script based on the skeleton. Let me know if you want the full executable version of `publish-skill.py` written next.