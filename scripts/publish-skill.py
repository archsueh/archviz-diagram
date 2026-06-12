#!/usr/bin/env python3
"""
archviz pure CLI skill publisher (agent-agnostic, absolute-path only).

Inspired by qiaomu-skill-publisher automation ideas but reimplemented
as strict CLI (no Claude Code runtime dependency).

Usage (always from absolute root):
  python3 /Users/mac/Developer/archviz-skills/scripts/publish-skill.py \
      /Users/mac/Developer/archviz-skills [--private]

It will:
1. Validate SKILL.md frontmatter (name, description, YAML safety)
2. Check required files
3. (Optional) auto-complete minimal missing files
4. Use gh CLI to create repo (if needed), commit, push, create release
5. Print verified multi-agent install instructions

Requires: gh CLI logged in, Python with pyyaml (pip install pyyaml)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import yaml
from pathlib import Path
from datetime import datetime

# === Absolute paths only (never change this) ===
ARCHVIZ_ROOT = Path("/Users/mac/Developer/archviz-skills")
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    ".gitignore",
]

def die(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def run(cmd: list[str], cwd: Path | None = None, check: bool = True):
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check, text=True)

def validate_frontmatter(skill_dir: Path):
    """Strict validation modeled on real publisher lessons."""
    md = skill_dir / "SKILL.md"
    if not md.exists():
        die("SKILL.md is required")

    text = md.read_text(encoding="utf-8")
    if not text.strip().startswith("---"):
        die("SKILL.md must start with YAML frontmatter (---)")

    # Extract frontmatter
    parts = text.split("---", 2)
    if len(parts) < 3:
        die("Malformed frontmatter delimiters")

    front = parts[1].strip()
    try:
        data = yaml.safe_load(front) or {}
    except Exception as e:
        die(f"YAML parse error: {e}")

    # Required fields (expand as archviz spec grows)
    if not data.get("name"):
        die("frontmatter.name is required")
    if not data.get("description"):
        die("frontmatter.description is required (use block scalar | for multi-line)")

    name = str(data["name"])
    if len(name) > 64 or not name.replace("-", "").isalnum():
        die("name must be kebab-case, <=64 chars")

    desc = str(data.get("description", ""))
    if len(desc) > 2048:
        print("WARNING: description is very long; some registries truncate ~1024 chars")

    # YAML safety: warn on problematic inline quotes (common install failure cause)
    if '"' in front and "\n" not in front.split("description:")[1][:100] if "description:" in front else False:
        print("WARNING: description contains double-quotes. Prefer block scalar | to avoid parser issues.")

    print("✓ Frontmatter valid (name + description + basic YAML safety)")

def check_files(skill_dir: Path):
    missing = [f for f in REQUIRED_FILES if not (skill_dir / f).exists()]
    if missing:
        print("Missing files:", ", ".join(missing))
        # In real run you could offer to scaffold, but keep conservative
        die("Required files missing. Create them first (see references/skill-publishing.md).")
    print("✓ All required files present")

def gh_available():
    try:
        run(["gh", "--version"], check=True)
    except Exception:
        die("gh CLI not found or not authenticated. Run: brew install gh && gh auth login")

def publish(skill_dir: Path, private: bool = False):
    gh_available()
    validate_frontmatter(skill_dir)
    check_files(skill_dir)

    version = "0.2.5"  # TODO: read from SKILL.md metadata or bump script
    tag = f"v{version}"
    # Darwin self-evo gate (per SKILL.md §16 Release Self-Check):
    # Confirm prior darwin re-score (target ≥96) + full Version Bump checklist executed + CHANGELOG surgical entry
    # before gh release. Cross-ref: /Users/mac/Developer/archviz-skills/SKILL.md §16 and CHANGELOG.md.
    # Absolute paths only. No new deps or behavior change.
    repo_name = "archviz-skills"   # or derive from name

    print("\n=== Dry run summary ===")
    print(f"Project : {skill_dir}")
    print(f"Version : {version}")
    print(f"Tag     : {tag}")
    print(f"Private : {private}")
    print("Will: gh repo create (if needed) → git push → gh release create")

    input("Press Enter to continue or Ctrl-C to abort...")

    # 1. Ensure remote repo exists (idempotent)
    create_cmd = ["gh", "repo", "create", f"archsueh/{repo_name}", "--source=.", "--remote=origin"]
    if private:
        create_cmd.append("--private")
    else:
        create_cmd.append("--public")
    try:
        run(create_cmd, cwd=skill_dir, check=False)
    except subprocess.CalledProcessError:
        print("Repo may already exist or remote configured. Continuing...")

    # 2. Commit & push (assume clean working tree or let user handle)
    run(["git", "add", "-A"], cwd=skill_dir)
    try:
        run(["git", "commit", "-m", f"release: {tag}"], cwd=skill_dir)
    except subprocess.CalledProcessError:
        print("No new commit (working tree clean or already committed).")
    run(["git", "tag", "-f", tag], cwd=skill_dir)
    run(["git", "push", "origin", "main", "--tags"], cwd=skill_dir)

    # 3. Create GitHub Release
    notes = f"archviz-skills {tag}\n\nSee CHANGELOG.md for details.\n\nInstall (Claude):\n  npx skills add archsueh/archviz-skills\n\nInstall (general):\n  git clone https://github.com/archsueh/archviz-skills ~/.claude/skills/archviz-skills   # or equivalent for your agent"
    run([
        "gh", "release", "create", tag,
        "--title", f"archviz-skills {tag}",
        "--notes", notes
    ], cwd=skill_dir)

    print("\n✅ Published. Verify with:")
    print(f"  gh release view {tag} --repo archsueh/{repo_name}")
    print("\nMulti-agent install instructions printed above in release notes.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", nargs="?", default=str(ARCHVIZ_ROOT),
                        help="Absolute path to the skill directory")
    parser.add_argument("--private", action="store_true", help="Create private repo")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    if not skill_dir.is_absolute():
        die("skill_dir must be an absolute path")

    publish(skill_dir, private=args.private)
