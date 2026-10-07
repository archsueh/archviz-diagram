#!/usr/bin/env python3
"""Palette-registry consistency gate — stdlib only, zero deps.

Why this exists
---------------
The palette registry is written down in **four** places, and they had silently
drifted apart:

  templates/html/_archviz-theme.html   11 ids   ← the runtime truth (CSS + toggle)
  archviz_diagram/engine.py            10 ids   ← missing `blueprint`
  DESIGN.md  (Palette Registry table)   8 rows  ← missing 4, plus a phantom row
  SKILL.md   ("N palettes" line)        6       ← stale by 5

The `engine.py` gap was the load-bearing one: `_apply_theme()` starts with
`if theme_name not in PALETTES: return html`, so `--palette blueprint` returned
the document **unchanged and with no error**. A silent no-op. v0.5.4 added
`blueprint` to the template, DESIGN.md, preview.html and all 17 templates —
`engine.py` was simply not on that list, and nothing could notice.

The template is authoritative. Everything else is checked against it.

Checks
------
  1. engine.py PALETTES ids  ==  template ids
  2. DESIGN.md registry rows ==  template ids
  3. SKILL.md declared count ==  len(template ids)
  4. every template id has a `[data-palette="<id>"]` CSS block (except CSS_EXEMPT)

Exit codes
----------
  0  consistent
  1  drift found
  2  usage / IO error
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

THEME = ROOT / "templates" / "html" / "_archviz-theme.html"
ENGINE = ROOT / "archviz_diagram" / "engine.py"
DESIGN = ROOT / "DESIGN.md"
SKILL = ROOT / "SKILL.md"

# `auto-time` deliberately has no CSS block: it resolves to another palette at
# apply time (`isDaytime ? "still-paper" : "ikb-dark"`). Everything else must
# define its own `[data-palette="..."]` block, or selecting it changes nothing.
CSS_EXEMPT = {"auto-time"}

REGISTRY_RE = re.compile(r"const PALETTES = \{(.*?)\n\s*\};", re.S)
REGISTRY_ENTRY_RE = re.compile(r'^\s*"?([\w-]+)"?:\s*\{\s*label:', re.M)

ENGINE_BLOCK_RE = re.compile(r"^PALETTES = \{(.*?)^\}", re.S | re.M)
ENGINE_ENTRY_RE = re.compile(r'^\s{4}"([^"]+)":\s*\{', re.M)

# DESIGN.md registry row: | Name | `id` | mode | accent | use |
DESIGN_ROW_RE = re.compile(r"^\|\s*[^|]+?\s*\|\s*`([\w-]+)`\s*\|", re.M)

SKILL_COUNT_RE = re.compile(r"\*\*(\d+)\s+palettes?\*\*")

CSS_BLOCK_RE = re.compile(r'\[data-palette="([\w-]+)"\]')


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def template_ids(text: str) -> list[str]:
    m = REGISTRY_RE.search(text)
    if not m:
        raise ValueError("模板里找不到 `const PALETTES = {...}` 块")
    return REGISTRY_ENTRY_RE.findall(m.group(1))


def engine_ids(text: str) -> list[str]:
    m = ENGINE_BLOCK_RE.search(text)
    if not m:
        raise ValueError("engine.py 里找不到顶层 `PALETTES = {...}` 块")
    return ENGINE_ENTRY_RE.findall(m.group(1))


def design_ids(text: str) -> list[str]:
    start = text.find("### Palette Registry")
    if start < 0:
        raise ValueError("DESIGN.md 里找不到 `### Palette Registry` 小节")
    nxt = text.find("\n### ", start + 1)
    section = text[start: nxt if nxt > 0 else len(text)]
    return DESIGN_ROW_RE.findall(section)


def skill_count(text: str) -> int | None:
    m = SKILL_COUNT_RE.search(text)
    return int(m.group(1)) if m else None


def compare(label: str, got: list[str], want: list[str]) -> list[str]:
    problems = []
    missing = [x for x in want if x not in got]
    extra = [x for x in got if x not in want]
    if missing:
        problems.append(f"{label} 缺: {', '.join(missing)}")
    if extra:
        problems.append(f"{label} 多: {', '.join(extra)}")
    if not missing and not extra and len(got) != len(want):
        problems.append(f"{label} 有重复项: {got}")
    return problems


def run(theme_text: str, engine_text: str, design_text: str, skill_text: str) -> list[str]:
    ids = template_ids(theme_text)
    if not ids:
        return ["模板注册表为空 —— 解析失败"]

    problems: list[str] = []
    problems += compare("engine.py", engine_ids(engine_text), ids)
    problems += compare("DESIGN.md", design_ids(design_text), ids)

    declared = skill_count(skill_text)
    if declared is None:
        problems.append("SKILL.md 里找不到 `**N palettes**` 声明")
    elif declared != len(ids):
        problems.append(f"SKILL.md 声明 {declared} 个，注册表实为 {len(ids)} 个")

    css = set(CSS_BLOCK_RE.findall(theme_text))
    for pid in ids:
        if pid in CSS_EXEMPT:
            continue
        if pid not in css:
            problems.append(f"模板里 {pid} 有注册表条目但没有 CSS 块")

    return problems


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "--self-test":
        return self_test()
    if len(argv) > 1 and argv[1] not in ("-h", "--help"):
        print(__doc__)
        return 2

    try:
        theme_text, engine_text = read(THEME), read(ENGINE)
        design_text, skill_text = read(DESIGN), read(SKILL)
    except OSError as exc:
        print(f"ERROR: 读取失败: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"ERROR: 非 UTF-8 文本: {exc}", file=sys.stderr)
        return 2

    try:
        ids = template_ids(theme_text)
        problems = run(theme_text, engine_text, design_text, skill_text)
    except ValueError as exc:
        print(f"FAIL — {exc}")
        return 1

    if problems:
        print(f"FAIL — 调色板注册表不一致（模板 = {len(ids)} 个 id，是唯一真源）")
        for p in problems:
            print(f"  - {p}")
        print()
        print("  真源: templates/html/_archviz-theme.html 的 ARCHVIZ_PALETTES")
        return 1

    print(f"PASS — 调色板注册表四处一致（{len(ids)} 个 id）："
          f"engine.py / DESIGN.md / SKILL.md / 模板 CSS")
    return 0


# ─────────────────────────── 自测 ───────────────────────────

GOOD_THEME = """
    const PALETTES = {
      "warm-paper": { label: "Warm Paper", mode: "light" },
      "auto-time": { label: "Auto (Time)", mode: "auto" },
    };
"""
GOOD_THEME += '\n  [data-palette="warm-paper"] {\n    --av-surface: #fff;\n  }\n'

GOOD_ENGINE = """
PALETTES = {
    "warm-paper": {
        "surface": "#fff",
    },
    "auto-time": {
        "surface": "auto",
    },
}
"""

GOOD_DESIGN = """
### Palette Registry

| Palette | id | Mode | Accent | Use |
|---|---|---|---|---|
| Warm Paper | `warm-paper` | light | IKB | Default |
| Auto (Time) | `auto-time` | auto | — | Time-based |

### Next section
"""

GOOD_SKILL = "- **2 palettes**: Warm Paper, Auto (Time)\n"


def self_test() -> int:
    cases = [
        ("consistent", GOOD_THEME, GOOD_ENGINE, GOOD_DESIGN, GOOD_SKILL, 0),
        ("engine_missing_id", GOOD_THEME,
         GOOD_ENGINE.replace('    "auto-time": {\n        "surface": "auto",\n    },\n', ""),
         GOOD_DESIGN, GOOD_SKILL, 1),
        ("design_missing_id", GOOD_THEME, GOOD_ENGINE,
         GOOD_DESIGN.replace("| Auto (Time) | `auto-time` | auto | — | Time-based |\n", ""),
         GOOD_SKILL, 1),
        ("skill_count_stale", GOOD_THEME, GOOD_ENGINE, GOOD_DESIGN,
         GOOD_SKILL.replace("**2 palettes**", "**6 palettes**"), 1),
        ("css_block_missing", GOOD_THEME.replace(
            '  [data-palette="warm-paper"] {\n    --av-surface: #fff;\n  }\n', ""),
         GOOD_ENGINE, GOOD_DESIGN, GOOD_SKILL, 1),
    ]
    failures = 0
    for name, t, e, d, s, want in cases:
        try:
            got = 1 if run(t, e, d, s) else 0
        except ValueError:
            got = 1
        ok = got == want
        if not ok:
            failures += 1
        print(f"  {'PASS' if ok else 'MISMATCH':<9} {name:<20} 期望 rc={want} 实际 rc={got}")
    print()
    if failures:
        print(f"自测失败: {failures}/{len(cases)} 个用例行为不符")
        return 1
    print(f"自测通过: {len(cases)}/{len(cases)} 个用例行为符合预期")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
