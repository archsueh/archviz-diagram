#!/usr/bin/env python3
"""Version-consistency gate — stdlib only, zero deps.

Why this exists
---------------
The release version is written down in **four** places, and they had silently
drifted apart:

  SKILL.md            metadata.version   0.6.0   ← the release truth
  CHANGELOG.md        first "## X.Y.Z"   0.6.0
  pyproject.toml      version            0.5.3   ← stale by 4 releases
  scripts/publish-skill.py  version      0.2.5   ← stale by ~9, carried a literal
                                                   "# TODO: read from SKILL.md"

Nothing could notice. The publish script was the dangerous one: it builds the
git tag straight from its own literal, so publishing would have tagged and
released `v0.2.5` while the skill shipped as 0.6.0.

SKILL.md is authoritative. Everything else is checked against it.

Checks
------
  1. CHANGELOG.md first "## X.Y.Z" heading  ==  SKILL.md metadata.version
  2. pyproject.toml version                  ==  SKILL.md metadata.version
  3. scripts/publish-skill.py contains no hardcoded semver literal
     (it must read the version from SKILL.md at runtime)
  4. SKILL.md metadata.version is a well-formed X.Y.Z

Exit codes
----------
  0  consistent
  1  drift found
  2  usage / IO error
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKILL = ROOT / "SKILL.md"
CHANGELOG = ROOT / "CHANGELOG.md"
PYPROJECT = ROOT / "pyproject.toml"
PUBLISH = ROOT / "scripts" / "publish-skill.py"

SEMVER = r"\d+\.\d+\.\d+"

# SKILL.md: `metadata:` block, then an indented `version: X.Y.Z`.
# Anchored to the frontmatter so a later "version" mention in prose cannot match.
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
META_BLOCK_RE = re.compile(r"^metadata:\s*$(.*?)(?=^\S|\Z)", re.S | re.M)
META_VERSION_RE = re.compile(rf"^\s+version:\s*\"?({SEMVER})\"?\s*$", re.M)

CHANGELOG_RE = re.compile(rf"^##\s+({SEMVER})\b", re.M)
PYPROJECT_RE = re.compile(rf"^version\s*=\s*\"({SEMVER})\"\s*$", re.M)

BARE_SEMVER_RE = re.compile(rf"\A{SEMVER}\Z")


def code_semver_literals(src: str) -> list[tuple[int, str]]:
    """Return `(lineno, value)` for semver string literals in *code*.

    Deliberately AST-based rather than a regex over the raw text: a regex also
    matches semver mentioned in comments and docstrings, which is exactly where
    a "we used to hardcode 0.2.5 here" note belongs. Only real string constants
    that are not docstrings count as hardcoded versions.
    """
    tree = ast.parse(src)

    docstrings: set[int] = set()
    doc_owners = (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(node, doc_owners) or not body:
            continue
        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            docstrings.add(id(first.value))

    hits: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        if id(node) in docstrings:
            continue
        if BARE_SEMVER_RE.match(node.value.strip()):
            hits.append((node.lineno, node.value.strip()))
    return hits


class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def read_skill_version(rep: Report) -> str | None:
    if not SKILL.exists():
        rep.fail(f"SKILL.md not found at {SKILL}")
        return None
    text = SKILL.read_text(encoding="utf-8")

    fm = FRONTMATTER_RE.search(text)
    if not fm:
        rep.fail("SKILL.md does not start with YAML frontmatter (--- ... ---)")
        return None

    block = META_BLOCK_RE.search(fm.group(1))
    if not block:
        rep.fail("SKILL.md frontmatter has no `metadata:` block")
        return None

    m = META_VERSION_RE.search(block.group(1))
    if not m:
        rep.fail("SKILL.md frontmatter `metadata:` has no well-formed `version: X.Y.Z`")
        return None

    return m.group(1)


def check_changelog(version: str, rep: Report) -> None:
    if not CHANGELOG.exists():
        rep.fail(f"CHANGELOG.md not found at {CHANGELOG}")
        return
    m = CHANGELOG_RE.search(CHANGELOG.read_text(encoding="utf-8"))
    if not m:
        rep.fail("CHANGELOG.md has no `## X.Y.Z` heading")
        return
    found = m.group(1)
    if found != version:
        rep.fail(
            f"CHANGELOG.md top entry is {found}, but SKILL.md metadata.version is {version} "
            f"— add a `## {version}` section (or fix the version)"
        )
    else:
        rep.note(f"CHANGELOG.md top entry   {found}  ok")


def check_pyproject(version: str, rep: Report) -> None:
    if not PYPROJECT.exists():
        rep.fail(f"pyproject.toml not found at {PYPROJECT}")
        return
    m = PYPROJECT_RE.search(PYPROJECT.read_text(encoding="utf-8"))
    if not m:
        rep.fail("pyproject.toml has no `version = \"X.Y.Z\"` line")
        return
    found = m.group(1)
    if found != version:
        rep.fail(
            f"pyproject.toml version is {found}, but SKILL.md metadata.version is {version} "
            f"— the installed package metadata would misreport the skill release"
        )
    else:
        rep.note(f"pyproject.toml version   {found}  ok")


def check_publish_script(rep: Report) -> None:
    if not PUBLISH.exists():
        rep.note("scripts/publish-skill.py not present — skipped")
        return
    src = PUBLISH.read_text(encoding="utf-8")
    try:
        hits = code_semver_literals(src)
    except SyntaxError as e:
        rep.fail(f"scripts/publish-skill.py does not parse: {e}")
        return
    if hits:
        where = ", ".join(f"line {ln}: {val!r}" for ln, val in hits)
        rep.fail(
            f"scripts/publish-skill.py hardcodes a version literal ({where}) — "
            "it must read the version from SKILL.md at runtime, otherwise "
            "`git tag` / `gh release create` use a stale tag"
        )
    else:
        rep.note("scripts/publish-skill.py has no hardcoded version literal  ok")


def main() -> int:
    rep = Report()

    version = read_skill_version(rep)
    if version is None:
        for f in rep.failures:
            print(f"FAIL  {f}", file=sys.stderr)
        print("\nFAIL — 版本一致性检查未通过（无法读取 SKILL.md 版本）", file=sys.stderr)
        return 2

    check_changelog(version, rep)
    check_pyproject(version, rep)
    check_publish_script(rep)

    if rep.failures:
        for f in rep.failures:
            print(f"FAIL  {f}", file=sys.stderr)
        print(f"\nFAIL — 版本多处不一致（真源 SKILL.md = {version}）", file=sys.stderr)
        return 1

    print(f"PASS — 版本一致（{version}），真源 SKILL.md metadata.version")
    for n in rep.notes:
        print(f"  {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
