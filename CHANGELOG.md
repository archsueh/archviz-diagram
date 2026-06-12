# Changelog

## 0.1.1 (2026-06-12)

**Darwin + skills-curation pass** (target score ≥90 before push)

### Added
- **When to Use / When NOT to Use** + **Skill Boundaries** table (vs claude-design-card, mermaid-arc-skills).
- **Checkpoints G0–G6** with STOP conditions and iron rule.
- **§14b Pitfalls & Red Lines (绝不)** — editorial + diagram hard bans.
- Editorial error rows in §13; editorial gates in `validation-checklist.md`.
- Frontmatter: `source`, `risk: safe`, expanded triggers (封面/卡片/排版).

### Changed
- **§9b** compressed to gate + pointer (token efficiency; detail in `editorial-parchment-language.md`).
- Darwin re-score: 84 → **92/100** (gates + boundaries + red lines + overlap clarity).

## 0.1.0 (2026-06-12)

**Editorial Parchment language — distilled from claude-design-card**

### Added
- **`references/editorial-parchment-language.md`**: warm canvas / Terracotta accent / serif+sans split / format families A–D / surface pacing / ask-before-generate / anti-patterns (upstream: [geekjourneyx/claude-design-card](https://github.com/geekjourneyx/claude-design-card)).
- **`templates/html/editorial-card.html`**: Family B knowledge-card skeleton with Family A/C/D override notes.
- **DESIGN.md**: Editorial Parchment palette row + Extended Format Families section + ready-to-use editorial prompt.
- **SKILL.md §9b Editorial Mode**: format routing, compression rule, platform safe zones, workflow ask gate.
- **QR table**: cover / knowledge card / social square / long-form → `editorial-card.html`.
- **Anti-patterns**: cover-as-summary, serif 700, cool SaaS white, equal card grid.

### Changed
- Brief inference signal #8: deliverable intent (diagram vs card vs long-form vs 3D).
- Palette routing note: Warm Paper+IKB default; Editorial Parchment+Terracotta for cards/covers; host-doc override preserved.

## 0.0.9 (2026-06-11)

**DESIGN.md restructured into the Stitch 9-section format + visual catalog**

### Added
- **DESIGN.md 9-section structure** (per VoltAgent/awesome-design-md): §1 Visual Theme & Atmosphere (prose + key characteristics + Agent-Readable Contract), §2 Color Palette & Roles, §3 Typography Rules, §4 Component Stylings, §5 Layout Principles, §6 Depth & Elevation, §7 Do's and Don'ts, §8 Responsive Behavior, §9 Agent Prompt Guide. Taxonomy, Aver patterns, 3D, and validation moved to Extended sections — no content lost.
- **Semantic color names**: every token now has name + hex + role (Warm Paper #f5f0eb, Paper Beige #e8e4e0, Mist White #f5f5f4, Stone Gray #a8a29e, Pebble #d6d3d1, Ink Navy #1B365D, Warm Ink #44403c, Charcoal #292524, Near Black #0a0a0a, IKB #002FA7, Lemon #FFD500).
- **§9 Agent Prompt Guide**: quick color reference + 4 ready-to-use prompts (flowchart, gantt, comparison, 3D shell) + 5-step iteration guide.
- **§6 Depth & Elevation**: "flat by doctrine" table — emphasis via line weight and the single accent, never shadows.
- **preview.html**: visual catalog at repo root (neutral/accent swatches, palette system table, type scale, node vocabulary, edge semantics) — the awesome-design-md preview convention.

### Changed
- **Signature Patterns (Aver domain)** synced with the Aver cinnabar-era system: V1 spine 物件→陪伴证据→告别归档; Money/Evidence/Sentiment naming (legacy Money/Knowledge/Sentiment marked archive-only); accent slot switches to Aver cinnabar #A24A2D inside Aver-branded documents (still max 1); Aver paper surfaces allowed for host-document matching.
- README design-system section now lists the 9 sections and links preview.html; version badge 0.0.9.

## 0.0.8 (2026-06-11)

**DESIGN.md philosophy pass — agent-readable contract + contrast correction**

### Added
- README design philosophy: diagrams are treated as compact DESIGN.md artifacts with atmosphere, tokens, components, layout, and guardrails.
- DESIGN.md Agent-Readable Contract table, adapted from the awesome-design-md pattern.
- SKILL.md brief inference now explicitly checks the DESIGN.md contract before generation.
- CONTRIBUTING.md review gates for contract layer, target environment, contrast, and fallback.

### Fixed
- Warm Paper token mismatch: light warm surfaces now use dark ink text (`#1B365D`) instead of near-white text.
- Stone Mono text token now uses dark warm ink (`#292524`) instead of near-white text.
- SKILL.md quick reference and token table now match DESIGN.md contrast rules.

## 0.0.7 (2026-06-11)

**3D template hardening — animejs v4 gotchas + ground offset + dependency reference**

### Added
- **SKILL.md §16 GOTCHAS**: 6 Three.js + animejs v4 踩坑记录（CDN 路径、API 迁移、命名冲突、地面偏移、相机动画、光照限制）
- **templates/html/_archviz-deps.html**: CDN 依赖速查文件，含 animejs v4 shim 和使用示例
- **DESIGN.md 3D constraints**: +5 条（animejs v4 API/CDN、render loop 命名、ground offset、CDN 验证）

### Fixed
- **hair-dryer-exploded.html**: 物体抬高 `dryer.position.y = 2`，修复埋入地面问题
- **animejs v4 CDN**: 3 个文件路径从 `lib/anime.es.js` 修正为 `dist/bundles/anime.esm.js`
- **animejs v4 API**: 3 个文件从 `anime({targets})` 迁移到 `tween(target, props)` 包装
- **render loop**: threejs-floorplan.html 函数名从 `animate` 改为 `renderLoop` 避免冲突

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
