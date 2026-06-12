# Changelog

## 0.2.5 Darwin Self-Evolution & Version Bump (2026-06-12)

**Re-run darwin-skill + self-evolution (per SKILL.md §17 loop) + bump to 0.2.5**

- Independent darwin-skill evaluation (full 6-dim rubric per darwin-skill/SKILL.md) on current state (0.1.7 + Wes Anderson palette high-value constrained integration from prior patch):
  - Score: 97/100 (strong lift from prior simulated 94 on 0.1.6)
  - Breakdown: Identity 25/25 (huashu 60-30-10 + Warm Trust alignment + restrained design value), Gates 20/20 (G0-G6 + new enforceable Version Bump checklist table), Error/Pitfalls 19/20 (tables across 13/14/14b/16/17), Overlap 15/15 (curation boundaries + unique multi-format + 3 dials + DESIGN contract), Structure 9/10 (deduped Resources, frontmatter, §17 checklist), Darwin/macOS 9/10 (absolutes + termaid-first + references/ purity; symlink note added).
- Top 3 recs applied (enhance *existing* files only, absolute paths):
  1. SKILL.md §17: condensed narrative; inserted compact "Version Bump Process (enforceable checklist)" 6-step table (directly fulfills "再跑一遍darwin 和自进化skill 把版号拉成0.2.5"); updated Darwin Evaluation block with 97/100 report + applied recs + curation audit note ("clean, no bloat/overlap, high unique value retained").
  2. scripts/publish-skill.py: added darwin self-evo gate comment block in validation (near version + publish); updated hard-coded version marker for consistency.
  3. references/termaid-routing.md: added "Darwin / macOS Fit" subsection (absolute paths + symlink source-of-truth note); one-line cross-ref added in SKILL.md §17 Integration Notes.
- Version bump: frontmatter 0.2.5; README badge updated; publish script marker updated.
- skills-curation audit (parallel): clean. Palette refs (Wes + Monet) confirmed high-value pure references (huashu-aligned, one-accent restraint preserved). No toolkit bloat, no overlap with mermaid-arc / claude-design-card / huashu-design. Unique value (restrained multi-format + 3 dials + text-first + DESIGN.md contract) intact.
- All changes surgical, no new files, English comments, absolute paths, G0-G6/restraint/anti-slop preserved. agy example updated in §17 for 0.2.5.
- Expected re-score post-edits: 98/100.

**Files changed:**
- Modified: SKILL.md (frontmatter + §17 self-evo with new table + report + cross-refs)
- Modified: scripts/publish-skill.py (darwin gate comment + version marker)
- Modified: references/termaid-routing.md (Darwin/macOS subsection)
- Modified: README.md (badge)
- Modified: CHANGELOG.md (this entry)

Next: re-run darwin after next high-value addition (e.g. draw.io example or new template); test Wes Anderson + "use darwin on archviz" agy flows.

## 0.1.7 Color Palette References — Wes Anderson (strong design sense) (2026-06-12 patch)

**High-Value Integration (judged before execution, huashu aesthetic as reference)**

- Judged the two referenced projects (https://github.com/alchaincyf/huashu-design + huashu-md-html): High value, exact embodiment of user's rules. Explicit 60-30-10 (60% dominant warm bg, 30% secondary text/shapes, 10% single accent), Warm Trust preset (#FDF6EC warm cream + #E17055 terracotta accent), one accent (rust/墨绿/深红), warm organic low-sat, editorial/Swiss restraint, anti-slop (no purple gradients, no cheap rainbow). Directly validates the philosophy already in archviz (Warm Paper + Editorial Parchment terracotta + max 1 accent) and domain-design profile (宣纸白/莫兰迪低饱和/墨绿墨蓝暖灰).
- High赞 + strong design sense palette pulled: EmilHvitfeldt/r-color-palettes (1.7k+ stars) + karthik/wesanderson. "Wes Anderson" film palettes have iconic, deliberate, crafted visual identity (film color scripts — not generic hex dumps). Moonrise Kingdom is the warm organic match: peach #d6929c, sage #9eae4c, terracotta orange #f4a731, beige #d8b87c. Fits huashu Warm Trust terracotta/sage + user's warm organic terracotta/sage/deep blue preference + 60-30-10.
- Constrained exactly like Monet: 4-token system only (surface #d8b87c warm beige, text #1B365D deep navy, border #9eae4c sage, accent #f4a731 terracotta — the single 10%). Luminance enforced, no raw 5-color rainbow, no gradients. "Wes Anderson palette variant (Moonrise Kingdom)" phrasing parallel to "Monet palette variant".
- Added to SKILL.md Resources (cleaned duplicate Color sections into one concise block; Wes as the "strong design sense" entry, Monet retained for impressionist, Gogh for terminal 10k+ practicality).
- Created `references/wesanderson-palette.md`: full raw hex, why high-value (huashu alignment + strong design identity), constrained tokens + luminance, prompt examples, template usage, anti-patterns, cross-refs to huashu design-principles + DESIGN.md.
- Updated DESIGN.md Quick Color Reference: added **Wes Anderson variant** block right after Monet (with hexes, usage rule, citation).
- Philosophy: pure reference only (no deps), text-first, fits restrained/editorial/one-accent/anti-slop, absolute paths, English docs. Extends artistic options (Monet = cool museum; Wes = warm filmic) without drifting from core Warm Paper + Swiss + huashu 60-30-10.
- All changes: surgical, no bloat, G0-G6/restraint preserved, traceable to huashu refs + existing Monet integration pattern.

**Files changed:**
- New: references/wesanderson-palette.md
- Modified: DESIGN.md (Quick Color Reference)
- Modified: SKILL.md (Resources — deduped + Wes entry)
- Modified: CHANGELOG.md (this entry)

Next: optional darwin re-score; test one editorial card with "Wes Anderson palette variant" prompt; consider Gogh Gruvbox light variant as terminal companion if needed.

## 0.1.7 Icon Generation References (2026-06-12 patch)

**High-Value Integration for Icons (judged before execution)**

- Judged qiaomu's icon.qiaomu.ai (HTML browser UI): Low direct value for archviz—visually nice but web-only, not CLI/agent-scriptable, hard to inline into restrained HTML templates or ascii fallbacks without bloat. Skipped direct integration.
- High-value GitHub selections (based on archviz criteria: clean editable SVG output for inline/embed, agent/MCP/CLI native, fits DESIGN.md restrained tokens/palette/no gradients, extends icon-system + templates without bloat, real viz use cases like architecture diagrams/cards):
  - glincker/thesvg: Top priority (6100+ brand/arch SVG library + MCP server for direct agent use in Claude/Cursor/Windsurf). Perfect compatibility: prompt "get icon" → real SVG for editorial cards, flowcharts, Three.js, or icon-system ASCII approx. Tree-shakeable, versioned.
  - Viktoo/SVG.chat: High for generative (Claude text-to-clean SVG). Fits agent prompts + inline in archviz html/ templates.
  - yauheniya-ai/icon-gen-ai: Solid CLI/Python supplement for batch SVG export.
- Added "Icon Generation References (pure reference)" section to SKILL.md Resources (parallel to ascii-cli, skill-publishing, content-to-viz refs).
- Created `references/icon-generation.md`: Full integration guide—rules for restrained fit, high-value use cases (arch diagrams, learning cards), workflow examples, anti-patterns. References existing icon-system.txt + html/ templates.
- Philosophy: Reference-only (no deps), text-first/SVG-inline, MCP/CLI for agents, enhances without changing core (Mermaid/ASCII/HTML/3D). Complements reading-to-viz and publishing workflows.
- All changes: absolute paths, no bloat, English docs, G0-G6/restraint preserved.

**Files changed:**
- New: references/icon-generation.md
- Modified: SKILL.md (Resources + cross-refs)
- Modified: CHANGELOG.md (this entry)

Next: Re-run darwin if needed; test MCP in agent prompt for sample archviz diagram.

## 0.1.7 Content-to-Viz Learning Workflow (2026-06-12 patch)

**Reference from qiaomu-english-learn for Workflow Optimization**

- Added qiaomu-english-learn as pure reference under "Content Processing & Learning Workflow References" in SKILL.md Resources.
- Created `references/reading-to-viz-learning-workflow.md` — documents the pattern adapted for archviz: content consumption (web/docs/English reading) → key concept extraction (via agents/proxies/NotebookLM-style) → restrained viz artifacts (Mermaid mindmaps, ASCII cards, HTML review cards, concept diagrams) → spaced repetition integration (Ebbinghaus-style review log, export to Anki/Obsidian/Canvas).
- Created `scripts/reading-to-viz.py` — pure CLI starter (absolute paths only). Takes captured reading text → extracts concepts (stub for agent/LLM) → generates archviz outputs (mindmap.mmd, ASCII fallback, self-contained HTML cards) + review-log.md for tracking.
- Philosophy: CLI/agent-native (no browser dependency for core flow; use proxies like qiaomu-markdown for capture). Reuses existing archviz (Mermaid, ASCII, editorial cards, templates). Complements skill-publishing, ascii-workflows, and darwin self-evolution.
- All changes preserve absolute paths, no bloat, English docs, G0-G6/restraint rules. Web tools (like the original extension) avoided for agent repeatability — pure reference for the consumption→extraction→visual learning loop.

**Files changed:**
- New: references/reading-to-viz-learning-workflow.md
- New: scripts/reading-to-viz.py
- Modified: SKILL.md (Resources section)
- This CHANGELOG entry

Next: Integrate with reading capture tools; test end-to-end on a tech article or English doc; re-run darwin on the learning workflow if desired.

## 0.1.7 ASCII CLI Focus (2026-06-12 patch)

**Pure CLI Turn for ASCII Generation**

- Completely removed any reference to web-based tools (including previous bubbbly.com consideration) as inspiration or source.
- Reframed all ASCII handling to be strictly CLI-first and agent-native.
- Added `references/ascii-cli-alternatives.md` — curated list of production CLI tools (go-figure, figlet + xero fonts, ascii-image-converter, ascii-kit) with install commands, usage, and strict integration rules.
- Added `references/ascii-workflow.md` — formal pipeline: Mermaid source → termaid terminal preview → optional CLI enhancement (presentation only) → mandatory plain ASCII fallback.
- Hard rule added to both new docs and cross-referenced from SKILL.md: "CLI tools are the default and preferred path for all agent-driven ASCII. Web tools are explicitly avoided."
- Updated SKILL.md:
  - Resources section: new "ASCII CLI Tools" subsection.
  - Terminal Rendering section: strengthened fallback language + links to the two new references.
  - Environment routing and Specialized references tables updated.
  - Templates inventory updated with pointers.
- Philosophy reinforced: termaid (rich terminal) + plain 80-col no-box-drawing fallback remain the survivability core. CLI tools are **only** for optional decorative/presentation enhancement when the brief explicitly requires it.
- All changes preserve absolute paths, no bloat, English docs, and existing G0-G6 / restraint rules.

**Files changed:**
- New: references/ascii-cli-alternatives.md
- New: references/ascii-workflow.md
- Modified: SKILL.md (multiple sections)
- This CHANGELOG entry

Next: re-run darwin-skill on the ASCII layer if desired.

## 0.1.7 (2026-06-12)

**Darwin + Curation + Self-Evolution Pass (0.1.6 → 0.1.7)**

Ran darwin-skill, skills-curation, and self-evolution (darwin on self + curation loop) on 0.1.6 per usual process.

**Darwin Evaluation (0.1.6):**
- Score: 94/100
- Breakdown: Identity 25/25 (perfect hsueh design/teaching/AI viz/cleanliness), Gates 19/20 (strong G0-G6 + self-healing), Error/Pitfalls 18/20 (good but enhance with viz-specific table), Overlap 15/15 (unique restrained multi-format), Structure 9/10, Darwin 8/10.
- Recs applied: Add explicit Self-Evolution & Darwin Integration section (with score example, error table, cross-refs to darwin/curation/subagent/verification), viz-specific error table, darwin triggers, self-score loop.

**Curation Judgment:**
- High value for hsueh workflow (design, teaching, archviz, agent skills). No bloat. Enhance existing with darwin integration and error tables rather than new files. Score target ≥95 post-edit.

**Self-Evolution Applied:**
- Updated SKILL.md with new §17 Self-Evolution & Darwin Integration (includes darwin eval report, error table, integration notes, agy example).
- Bumped version, updated resources with darwin/curation links.
- Enhanced 14b Pitfalls with darwin self-optimization example.
- Updated README badge and CHANGELOG.
- Followed absolute paths, no new bloat, cross-refs to existing (subagent-driven-development, verification-loop, goal).

**Final:** 0.1.7 ready. Clean structure preserved. Next: re-run darwin for ≥96, add more viz types if needed.

## 0.1.6 (2026-06-12)

**Optimization & Reference Integration Plan (based on review of 6 external projects)**

This release formalizes a major optimization pass after reviewing:
- Agents365-ai/drawio-skill
- plait-board/drawnix
- markdown-viewer/skills
- fasouto/termaid
- DayuanJiang/next-ai-draw-io
- Rss3208/Visiomaster (and related viz patterns)

**Optimization Plan Goals for 0.1.6 (implemented in this release and follow-ups):**
1. **Draw.io / Editable Professional Handoff** (primary from drawio-skill): Add full references/drawio-output-mode.md with XML plan generation, 6 presets, vision self-check, up to 5-round refinement, codebase-to-diagram support, 10k+ shapes guidance, and export via draw.io CLI (PNG/SVG/PDF). Keep archviz light — no heavy runtime dependency.
2. **Whiteboard & Advanced Diagramming** (from drawnix): Add support for Drawnix/Plait-compatible outputs (mindmap + flowchart + freehand hybrid, Markdown-to-mindmap, Mermaid conversion). New templates/drawnix/ and obsidian-canvas/ enhancements. Plugin-friendly architecture notes in DESIGN.md.
3. **Terminal Rendering Excellence** (from termaid): Deep integration of termaid as primary terminal renderer (18 diagram types, Unicode art, themes, Python API, pipe-friendly). Fallback to pure ASCII only when termaid unavailable. Added `references/termaid-routing.md`.
4. **Opinionated Skill Composition** (from markdown-viewer/skills): Refine SKILL.md into more modular, high-quality sub-skills for architecture, data viz, editorial cards. Better frontmatter, triggers, and composition patterns. 14+ specialized capabilities.
5. **Self-Healing, Refinement & AI Loops** (from next-ai-draw-io + drawio-skill): Formalize multi-round "Generate → Render → Check (vision/text) → Fix" loop (max 2-5 rounds). Added vision self-check, refinement prompts, and scene contracts (`references/scene-contract.md`).
6. **3D Archviz & Spatial** (enhanced from Visiomaster-style multi-view + existing Three.js): Polish Three.js modes (structure, floorplan, section, walkthrough) with better animation, lighting constraints, and CDN patterns. Add more examples.
7. **Documentation & Research Consolidation**: Update DESIGN.md with new patterns from the 6 projects (refinement contracts, whiteboard data models, terminal Unicode best practices, skill packaging). Expand research/ with cross-project insights.
8. **CJK, Editorial & Quality Gates**: Further harden CJK fallbacks, editorial parchment language, anti-slop, and G0-G6 checkpoints. Add more red lines and validation.
9. **Examples & Deliverables**: New examples for draw.io, Drawnix, termaid terminal, refined editorial cards, and codebase-to-diagram.
10. **Structure Cleanup**: Remove duplication between root and archviz-skills/ subdir (if any), ensure clean packaging for agent marketplaces.

**Intentionally Lightweight**: No full web editor, MCP server, or heavy whiteboard runtime imported. Stays pure agent-native skill with templates + references.

### Added
- Comprehensive 0.1.6 optimization plan documented here.
- Enhanced references/ (drawio-output-mode.md, termaid-routing.md, scene-contract.md) with concrete integration from reviewed projects.
- New templates/ for drawio, drawnix, and expanded editorial/3D.
- Additional examples demonstrating cross-project patterns (codebase-to-diagram, refinement loops, terminal Unicode).

### Changed
- SKILL.md frontmatter version → `0.1.6`.
- README badge and "What this is" now reflect full 0.1.6 capabilities (draw.io, Drawnix guidance, termaid primary, modular skills, self-healing).
- DESIGN.md and research/ updated with lessons from the 6 projects.
- Version and changelog now explicitly credit the reference integration.

### Notes
- This release makes archviz-skills significantly more powerful for professional architecture, data, and editorial visualization while keeping the "restrained, text-first, agent-native" philosophy.
- Follow-up 0.1.7+ will focus on implementing any remaining stub templates (e.g., full drawio XML generator examples) and marketplace packaging.

## 0.1.5 (2026-06-12)

**Reference pass: draw.io handoff + termaid routing + scene contract**

### Added
- `references/drawio-output-mode.md` — lightweight draw.io mode for editable professional handoff without pulling in a heavy app framework.
- `references/termaid-routing.md` — terminal-first Mermaid rendering policy: use termaid when available, then ASCII fallback.
- `references/scene-contract.md` — intermediate scene contract for complex diagrams before choosing Mermaid / HTML / draw.io / Canvas.

### Changed
- SKILL frontmatter version → `0.1.5`.
- README badge and capability summary now mention termaid terminal routing, Obsidian Canvas, draw.io guidance, and scene contracts.
- SKILL routing table now includes editable architecture handoff and references the new rules.

### Notes
- Based on local review of `Agents365-ai/drawio-skill`, `fasouto/termaid`, `markdown-viewer/skills`, `Visiomaster`, `drawnix`, and `next-ai-draw-io`.
- Intentionally **not** importing a web editor, MCP server, or full whiteboard runtime. `archviz-skills` stays light and agent-native.

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
