# Changelog

## 0.0.7 (2026-06-11)

**skill-creator compliance + documentation sync**

### Fixed
- **SKILL.md frontmatter**: `triggers`/`version`/`author` moved into `description` + `metadata` (passes Codex `quick_validate.py`)
- **§12 template list**: removed nonexistent `flowchart.mmd`/`mindmap.mmd`; noted inline generation
- **README**: version badge 0.0.5 → 0.0.7, HTML count 14, 3D mode routing, examples index

### Added
- **agents/openai.yaml**: Codex UI metadata (`display_name`, `default_prompt`, `brand_color`)

## 0.0.6 (2026-06-11)

**3D architectural visualization — Three.js + animejs integration**

### Added
- **DESIGN.md §3D Architectural Visualization**: 6 archviz types (structure shell / floor plan / interior / structural overlay / section cut / multi-floor nav), 3D tokens, constraints, 3D anti-patterns
- **SKILL.md 3D archviz mode**: environment routing (3D → Three.js self-contained HTML), stack spec (Three.js + animejs + OrbitControls), content type "spatial/3D"
- **2 Three.js templates**: `threejs-archviz.html` (building structure shell with section cut, wireframe toggle, camera presets), `threejs-floorplan.html` (multi-floor navigation with animejs transitions, explode view)
- **1 teaching example**: `teaching-building-3d.html` (4层教学楼：门厅/教室/办公/屋顶，楼层切换+分解视图)
- **Triggers**: three.js, 3d, archviz, building, floorplan, 建筑, 结构, 楼层, walkthrough, 漫游

### Changed
- **SKILL.md type selection table**: +3 rows for 3D (building structure, floor plan, section cut)
- **SKILL.md environment routing**: +3D/archviz row (Three.js self-contained HTML)
- **SKILL.md Brief Inference**: content type now includes "spatial/3D"

## 0.0.5 (2026-06-11)

**Teaching/academic chart gaps + anti-patterns + mixed-type strategy + real examples**

### Added
- **4 Mermaid templates**: `funnel.mmd`, `decision-matrix.mmd`, `state-machine.mmd`, `dependency-network.mmd`
- **2 teaching examples**: `course-admission-flow.mmd` (32门课程准入漏斗), `course-evaluation-matrix.mmd` (多维课程评价矩阵)
- **SKILL.md §14 ANTI-PATTERNS**: 15 student-work / common-mistake guards (pie abuse, rainbow nodes, dual Y-axis, truncated axis, emoji overload, etc.)
- **SKILL.md mixed types**: guidance for process+timeline, hierarchy+comparison, flow+metrics, decision+scoring — never >2 types per diagram
- **SKILL.md degradation strategy**: 5-step fallback when data is too complex (>50 nodes, >7 categories, mixed types, preview fails, syntax error)
- **DESIGN.md taxonomy**: funnel/conversion, decision/evaluation, state transitions, dependencies + data-shape heuristics

### Changed
- **SKILL.md Quick Reference**: type-selection table now routes funnel / decision / state / dependency to new templates, with Template column
- **Router triggers**: funnel, state diagram, decision matrix, 漏斗图, 状态机, 决策矩阵, 依赖图

## 0.0.4 (2026-06-11)

**Documentation accuracy + agent router support + identity cleanup + minor template hygiene**

### Removed
- Personal `hsueh` habit references in examples/templates → generic `Author habit` / `personal context`.

### Changed
- **SKILL.md frontmatter**: version 0.0.3 → 0.0.4; added `triggers` block (diagram, gantt, 可视化, 架构图 etc.) so routers (Antigravity, Grok skills, Claude, Hermes) can auto-activate without full path or exact name.
- **SKILL.md §12 TEMPLATES**: replaced hardcoded stale counts ("mermaid 8 / html 3 / python 2") with current accurate inventory (11/12/5) + explicit instruction: "read the specific template file under templates/<mode>/ at use time" and "do not hardcode counts".
- **README.md**: synced version badge and the category/count table to match reality.

### Fixed
- Agents following the old template list in SKILL.md would have a wrong mental model of available outputs (the root cause of "skill lies to the model").
- README table was also advertising outdated HTML=4 / Python=2.

### Notes
- references/ (gantt-rules, validation-checklist, style-guide) remain but are now largely duplicate of inlined content in SKILL + DESIGN. Consider pruning in a follow-up if you want the checkout leaner.
- Next hygiene targets (not in this patch): add root `requirements.txt` for python/ templates; make all html/ canvases responsive (see self-contained-html-viz.txt example); audit the other 11 HTML templates for the same fixed-pixel issue.

## 0.0.3 (2026-06-11)

**Full optimization pass: slim SKILL.md, dedup, restructure templates, add missing types**

### Changed
- **SKILL.md**: 473→244 lines (−48%). Added Quick Reference block (5-sec load). Moved detailed rules to DESIGN.md/references.
- **DESIGN.md**: 282→117 lines (−58%). Removed duplicate ASCII templates, Gantt details, env control. Focused on design system (tokens, taxonomy, patterns).
- **Templates restructured**: Flat → `mermaid/` `ascii/` `html/` `python/` subdirectories.

### Added
- **Missing chart types**: distribution.mmd, diverging-bar.mmd, network.mmd, treemap.html
- **Examples**: mermaid-demo.md, ascii-demo.txt, html-demo.html, python-demo.py
- **GitHub files**: CONTRIBUTING.md, .github/ISSUE_TEMPLATE/bug_report.md

### Removed
- Duplicate content between SKILL.md and DESIGN.md
- Verbose environment control sections (condensed to QR table)
- Duplicate ASCII templates from DESIGN.md (already in templates/ascii/)

## 0.0.2 (2026-06-10)

**anydesign integration + Gantt overflow prevention + ASCII mode**

### Added
- Layered Analysis (from anydesign): 4-layer with confidence levels (✅/⚠️/❓)
- DTCG-inspired token system with semantic naming
- Quality Rules (Do's/Don'ts)
- Contrast Rule (luminance-based)
- 5 Palette Presets
- Gantt text overflow prevention (codes only + table + ASCII)
- ASCII mode (box-drawing shapes, arrow semantics)
- Diagram Brief Inference (from taste-skill)
- Three Dials (COMPLEXITY / DENSITY / RESTRAINT)

## 0.0.1 (2026-05)

**Initial release**

### Added
- Core Mermaid diagram skill with restrained design
- Warm paper palette + guizang Swiss integration
- Template system (three-layer, warm-paper, 5d-scoring, 6duan-intro)
- DESIGN.md plain-text design system
