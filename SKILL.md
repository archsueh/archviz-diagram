---
name: archviz-diagram
description: |
  Restrained flowcharts and framework diagrams (流程图与框架图/系统架构图/概念模型) visualization skill pack for AI agents. Every visualization starts with a brief read and three dials.
  Token-aware: prefers Mermaid/ASCII/compact HTML, defers heavy self-contained HTML to when interaction is required.
  Supports Mermaid, ASCII, self-contained HTML, Python (Plotly). Text-first, preview-compatible, anti-slop.
  For 3D spatial visualization (building, floorplan, exploded view) → use archviz-3d.
  Use when the user asks for flowchart, architecture diagram, framework diagram, diagram, visualization, state diagram, process flow, 流程图, 架构图, 框架图, 结构图, 关系图, 状态机, 决策矩阵, 依赖图, dependency graph, workflow, concept map.
license: MIT
metadata:
  version: 0.5.3
  source: https://github.com/archsueh/archviz-diagram
  risk: safe
  author: archsueh
  triggers: flowchart, architecture diagram, framework diagram, diagram, visualization, state diagram, process flow, sequence, swimlane, quadrant, 流程图, 架构图, 框架图, 结构图, 关系图, 状态机, 决策矩阵, 依赖图, 序列图, 泳道图, dependency graph, workflow, concept map
---

# archviz-diagram-skills

> Every rule is **contextual**. Read the brief first, then pull only what fits.

## When to Use

- Inline diagrams in Markdown/Obsidian/GitHub (Mermaid, ASCII, embedded SVG/HTML).
- Architecture, flow, timeline, comparison, state, dependency, or 3D spatial briefs.
- Editorial HTML cards/covers when the deliverable stays **text-first or self-contained HTML** (not Playwright PNG pipeline).
- Host-document palette matching (Warm Paper, Aver cinnabar, Editorial Parchment).

**Good:** "用 archviz-diagram 给这份产品全案 §2 画 V1 闭环图" · "Gantt + 任务表 + ASCII fallback" · "内嵌 Warm Paper SVG 到 Obsidian 笔记"

**Good:** "帮我生成小红书 PNG 并截图上传" → archviz-diagram HTML 模板内置导出（E→P 4× PNG），无需外部工具。若需复杂排版，可搭配 `claude-design-card` 使用 archviz-diagram 输出的 HTML 骨架。

## When NOT to Use

- Full marketing site / landing page UI → `design-taste-frontend`, `frontend-design`, or `huashu-design`.
- PNG card batch export with fixed platform specs → `claude-design-card`.
- Mermaid-only aesthetic variants without data reasoning → `mermaid-arc-skills` (lighter, Mermaid-focused).
- Arbitrary image generation without structure → `imagegen` / fal MCP.

## Skill Boundaries (curation map)

|| Need | Use |
|---|---|
|| Flowcharts & Framework Diagrams (process flows, architecture, concepts) | **archviz-diagram** (this skill) |
|| 3D spatial (building, exploded, mechanical) | [archviz-3d](https://github.com/archsueh/archviz-3d) (specialized extension) |
|| Dark tech infrastructure diagrams | **archviz-diagram** Dark Mode (built-in, see DESIGN.md §Palette: IKB Dark) |
|| Educational flat diagrams (physics, chemistry, engineering) | **archviz-diagram** Educational Flat Mode (built-in, see DESIGN.md §Palette: Educational Flat) |
|| Article illustrations / sketches | [archviz-sketch](https://github.com/archsueh/archviz-sketch) + `sketch-image-pipeline` skill |
|| DESIGN.md for a product brand | anydesign + host DESIGN.md |

**Absorbed capabilities (2026-06):** Dark Mode infrastructure diagram rules and Educational Flat 9-ramp color system were absorbed from the upstream `architecture-diagram` and `concept-diagrams` skills into this skill's DESIGN.md. No external skill routing required for these modes — they are first-class citizens here.

## MCP Server (programmatic access)

archviz-diagram exposes a Python MCP server for AI agents. Any LLM can call it directly.

```bash
# Install
cd ~/Developer/archviz-diagram && pip install -e ".[mcp]"

# CLI usage
archviz-diagram list                           # list 14 types
archviz-diagram render -t stacked-bar -o chart.html
archviz-diagram render -t sunburst -d data.json --theme ikb-dark -o chart.html

# MCP server (stdio transport)
archviz-diagram serve
```

### Tools
| Tool | Description |
|---|---|
| `archviz_diagram_generate(type, data, options)` | Generate self-contained HTML flowchart or diagram |
| `archviz_diagram_list_types()` | List all types with schemas and examples |
| `archviz_diagram_list_palettes()` | List available color palettes |

### Family MCP Servers
| Server | Tools | Location |
|---|---|---|
| `archviz-diagram` | 14 types (2D charts) | `~/Developer/archviz-diagram` |
| `archviz-3d` | 2 types (building, floorplan) | `~/Developer/archviz-3d` |
| `archviz-sketch` | 4 styles (prompt generation) | `~/Developer/archviz-sketch` |

### Sketch → Image Pipeline
For hand-drawn illustrations: `archviz_sketch_generate` → Grok `image_generate` → `vision_analyze` QA.
See `sketch-image-pipeline` skill for full workflow.

## Checkpoints & Gates

| Gate | Pass criteria | On fail |
|---|---|---|
| G0 Brief | One-line "Reading this as…" + dials set; **would a paragraph/table teach more? if yes → don't draw** | STOP — prose/table, or infer brief from host doc |
| G0b Brand | Tokens source locked (host DESIGN.md / `.archviz-preset.yaml` / explicit default) — see `references/brand-gate.md` | STOP — ask once; never silent default into branded repo |
| G1 Type | QR / structural map match; ≤2 types per deliverable; structural soft-cap **9 nodes** | STOP — split diagram |
| G2 Tokens | Palette locked; contrast computed; accent on **1–2 focal nodes max** | STOP — fix init/CSS |
| G3 Editorial ask | If card/cover ambiguous: 1 primary + 2 alt OR user said "your call" | STOP — do not guess platform |
| G4 Generate | Template read if path exists | Fallback: flowchart TD + subgraph |
| G5 Validate | `references/validation-checklist.md` pre+post | STOP — ASCII fallback + document ⚠️ |
| G6 Embed | Caption = finding first | Revise caption before ship |

**Iron rule:** No ship without G2 contrast check. No Family A cover with >3 text layers. No silent default skin when host brand files exist (G0b).

### ⚠️ ClawHub 发布流程
**Trigger:** 用户要求发布 skill 到技能商城
**Rule:** `hermes skills publish` 有安全扫描误报（表格 `| Env | Output |` 被判为 exfiltration）。备用方案：
1. `hermes skills tap add owner/repo` — 添加为 tap 源（但 search 可能不生效）
2. 手动提交 https://clawhub.ai/submit — 需要 GitHub OAuth 登录
3. `hermes skills snapshot export` — 导出本地 skill 快照（仅含 official skills，不含 local）

### ⚠️ NEVER delete references when asked to "optimize"
**Trigger:** User says "优化" (optimize), "美化" (beautify), "fix", "improve"
**Rule:** Optimize = improve the EXISTING content. Do NOT delete SVG references, template paths, external links, or supporting files unless the user explicitly says "删除" (delete), "清理" (clean up), or "remove".
**Failure example:** User asked to "优化一下图表". Agent deleted all SVG references and template paths. User: "谁让你清理 回退 我只是让你优化" (Who told you to clean up? Revert! I only asked you to optimize).
**Correct approach:** Read the request literally. "优化" = make better. "清理" = remove. These are different operations. When in doubt, ask.

**Self-healing loop** (from drawio-skill pattern, optional for complex diagrams):
1. Generate diagram
2. Render to image (Mermaid CLI / termaid / browser screenshot)
3. Read image with VLM → check for overlaps, clipped labels, unreadable text
4. If issues found → fix source → re-render (max 2 rounds)
5. Ship or document remaining ⚠️

**Self-healing validation checklist** (check after every render):
- Text overflow? (labels clipped, bars too narrow)
- Node overlap? (elements on top of each other)
- Arrow crossing? (lines through nodes)
- Contrast fail? (text unreadable on background)
- Missing legend? (>2 arrow types without legend)
- Gantt overflow? (task names wider than bars)

---

## QUICK REFERENCE (agent loads this in <5 seconds)

```
Dials:      COMPLEXITY=4  DENSITY=3  RESTRAINT=8
Palette:    surface=#f5f0eb  text=#1B365D  border=#a8a29e  accent=#002FA7 (max 1)
Init:       %%{init: {'theme':'base','themeVariables':{'primaryColor':'#f5f0eb','primaryTextColor':'#1B365D','primaryBorderColor':'#a8a29e','lineColor':'#a8a29e','tertiaryColor':'#d6d3d1','fontSize':'13px'}}}%%
Contrast:   luminance(0.299R+0.587G+0.114B) < 128 → light text, ≥ 128 → dark text
Labels:     ≤6 words / ≤8 Chinese chars / no ALL CAPS
Gantt:      codes only inside block + table beside / min 3w / termaid for terminal
Anti-slop:  no purple default / no rainbow / no flowchart-for-everything / no pie
Focal:      accent on 1–2 nodes max · structural soft-cap 9 nodes · delete before add
Brand gate: host DESIGN.md / .archviz-preset.yaml first — `references/brand-gate.md`
Dark mode:  surface=#1a1814 text=#e8e4e0 accent=#58a6ff (see §11c)
Editorial:  Parchment=#f5f4ed  ink=#141413  terracotta=#c96442 (max 1)  serif 500 not 700
Swiss Grid: surface=#ffffff text=#111111 border=#111111 accent=#e4002b (Swiss Red) modular baseline-locked (12-col+8px)
Vignelli:   surface=#f4f1ea text=#0a0a0a border=#0a0a0a accent=#f04e23 (Vermilion) max two sizes (heading ≈ 2x body)
```

**Engine routing (fast):** Mermaid default · draw.io if editable handoff · Excalidraw if sketch/workshop · HTML/Python if data/export. Full matrix → `references/ecosystem-routing.md`.

**Type selection (fast):** full 27-type map → `references/structural-diagram-types.md`
| Data | Type | Template |
|---|---|---|
| Hierarchical | mindmap | — |
| Sequential process | flowchart LR/TD | — |
| **Messages over time** | sequenceDiagram | `mermaid/sequence.mmd` |
| **Cross-functional / roles** | swimlane (subgraph lanes) | `mermaid/swimlane.mmd` |
| **2×2 / impact×effort** | quadrantChart | `mermaid/quadrant.mmd` |
| System/layered | flowchart TD + subgraph | — |
| Comparison/ranking | xychart-beta (bar) | — |
| Proportional | treemap or stacked bar | — |
| Timeline | gantt | `mermaid/gantt.mmd` |
| Distribution | histogram/box | `mermaid/distribution.mmd` |
| Correlation | scatter/heatmap | `python/scatter-plot.py` |
| Flow/network | sankey (or pure SVG/JS) | `mermaid/sankey.mmd` or examples/us-flows.html |
| Funnel/conversion | funnel chart | `html/funnel.html` |
| Decision/evaluation | decision matrix (table) | `mermaid/decision-matrix.mmd` |
| State transitions | stateDiagram-v2 | `mermaid/state-machine.mmd` |
| Dependencies | dependency graph | `mermaid/dependency-network.mmd` |
| Multi-criteria scoring | radar or diverging bar | `html/radar.html` / `mermaid/diverging-bar.mmd` |
| Entities + fields | erDiagram | inline (short fields) |
| Permissions / access grid | **TABLE** | `html/academic-table.html` |
| Simple (≤5 items) | **TABLE, not chart** | — |
| **Academic table** | Multi-header table with row groups | `html/academic-table.html` |
| **Cover / hero (click promise)** | Editorial Family A HTML | `html/editorial-card.html` |
| **Knowledge card (saveable)** | Editorial Family B HTML | `html/editorial-card.html` |
| **Social square (quote/data)** | Editorial Family C HTML | `html/editorial-card.html` |
| **Long-form article layout** | Editorial Family D HTML | `html/editorial-card.html` |
| **Swiss modular layout / poster** | Modular Grid HTML | `html/swiss-modernist-grid.html` |
| **Network topology** | SSH / tunnel / protocol diagram | `html/network-topology.html` |
| **Editable engineering handoff** | draw.io XML | `references/drawio-output-mode.md` |
| **Sketch / workshop board** | Excalidraw | `templates/excalidraw/` + promote to Mermaid |

**Mixed types** (when data spans categories):
- Process + timeline → flowchart with gantt sub-section (split into 2 diagrams)
- Hierarchy + comparison → mindmap with leaf annotations (table beside)
- Flow + metrics → sankey with tooltip/badge annotations
- Decision + scoring → decision matrix → radar for top candidates
- **Rule: never combine >2 types in one diagram. Split instead.**
- Exception for demonstration: deliberate "combined page" (one Swiss container HTML with 2 related high-fidelity vizs, e.g. Sankey + geo-flow map, shared tokens/credits) is allowed and valuable when user wants breadth in single artifact (see examples/us-flows.html and gotchas "consolidation"). Still apply restraint: shared palette, minimal prose, clear section titles.

**Degradation strategy** (when data is too complex):
1. **Structural soft-cap 9 nodes** → prefer overview + detail (see `structural-diagram-types.md`)
2. >12 nodes / >15 edges → must split; >50 nodes still absolute fail for Mermaid layout
3. >7 categories → aggregate into "Other" + detail diagram
4. Mixed data types → identify primary relationship, table the rest
5. Preview environment fails → ASCII fallback (always prepared)
6. Mermaid syntax error → flowchart TD + subgraph (most compatible)
7. Reader learns more from paragraph/table → **don't draw** (G0)

**Environment routing:**
| Env | Output |
|---|---|
| Obsidian/preview | lightweight Mermaid / self-contained HTML |
| Terminal | **termaid** (`termaid diagram.mmd --theme mono`) — 18图类型，6套主题 |
| Deliverables | Python (Plotly/Matplotlib) |
| **3D / spatial** | → **archviz-3d** skill (Three.js self-contained HTML) |

**3D archviz**: 已拆分为独立 skill → [archviz-3d](https://github.com/archsueh/archviz-3d)。当 brief 提到 building/floorplan/structure/spatial/exploded/3D 时，路由到 archviz-3d。
```html
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/",
    "animejs": "https://cdn.jsdelivr.net/npm/animejs@4.4.1/dist/bundles/anime.esm.js"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { animate } from 'animejs';  // v4: named export, NOT default
</script>
```

**Tech stack pitfalls (硬规则，已踩坑验证):**

| Pitfall | Symptom | Fix |
|---|---|---|
| animejs CDN 404 | Canvas blank, no errors | v4.4.1 路径是 `dist/bundles/anime.esm.js`，不是 `lib/anime.es.js` |
| animejs default import | `import anime from 'animejs'` → undefined | v4 是 named export: `import { animate } from 'animejs'` |
| animejs v3→v4 API | `anime({targets: x, ...})` 报错 | v4 是 `animate(target, params)`，无 `targets` key。详见 archviz-3d |
| `animate` 命名冲突 | 渲染循环函数也叫 `animate` → 覆盖 import | 渲染循环用 `renderLoop` 或 `tick`，不要用 `animate` |
| Three.js CatmullRom | `CatmullRomCurvePath` 不存在 | 用 `CatmullRomCurve3`（3D 曲线） |

Full rules → DESIGN.md. Templates → templates/.

---

## 0. BRIEF INFERENCE

Before generating, read these signals:

1. **Context** — paper, design log, PPT, product doc, personal note
2. **Content type** — hierarchical, sequential, relational, quantitative, temporal, **spatial/3D**
3. **Audience** — reviewers, clients, dev team, self
4. **Vibe** — "restrained", "clean", "academic", "playful"
5. **Existing style** — match palette/font/layout already established
6. **Constraints** — accessibility, print, projection, dark mode
7. **Environment** — Obsidian, terminal, deliverables
8. **Deliverable intent** — inline diagram · card/cover · long-form · 3D spatial

Output one line: **"Reading this as: \<type> for \<audience>, \<vibe>, \<palette>."**

**G0 — draw or not:** *Would the reader learn more from this than a paragraph or 3-column table?* If no → ship prose/table, skip generation.

**Palette routing + G0b:** academic default → Warm Paper + IKB · editorial/card → Editorial Parchment + Terracotta · **host DESIGN.md / `.archviz-preset.yaml` always wins when present**. First diagram in branded project → `references/brand-gate.md` (ask once; never silent default).

**Type routing (技术图):** architecture / workflow / sequence / data flow / lifecycle 五类各有该交代的语义（泳道、主路径/旁路、PII 边界、终态）。选对类型 + 路径语义 → `references/diagram-types-technical.md`. workflow ≠ 通用流程图。

**Type routing (结构图 27 类):** quadrant / venn / pyramid / org / swimlane / loop 等 → `references/structural-diagram-types.md`（密度 4/10、焦点 1–2、soft-cap 9 nodes）。

**Engine routing:** Mermaid ↔ draw.io ↔ Excalidraw ↔ HTML → `references/ecosystem-routing.md`。

**4-layer analysis** (from anydesign): Identity → System → Components → Layout. Mark confidence: ✅/⚠️/❓.

**DESIGN.md contract** (from awesome-design-md): Atmosphere → Tokens → Components → Layout → Guardrails. If any layer is unknown, state the assumption before generating.

**Anti-default:** No purple gradients, no rainbow nodes, no centered symmetry, no flowchart-for-everything, no default theme.

---

## 1. THREE DIALS

| Dial | Default | Range |
|---|---|---|
| COMPLEXITY | 4 | 1(minimal)–10(dense) |
| DENSITY | 3 | 1(airy)–10(packed) |
| RESTRAINT | 8 | 1(expressive)–10(austere) |

Inference: "academic" → 3-5/2-3/9-10 · "playful" → 5-8/3-5/3-5 · "data report" → 6-8/6-8/5-7

---

## 2. TOKENS

Defined in DESIGN.md. Summary:

| Token | Warm Paper | Swiss | IKB |
|---|---|---|---|
| surface | #f5f0eb | #f5f5f4 | #e4e8f0 |
| text | #1B365D | #1B365D | #0a0a0a |
| border | #a8a29e | #d6d3d1 | #94a3b8 |
| accent | — | — | #002FA7 |
| **Still Paper (静纸)** | `#f5f4ed` | `#141413` | `#e8e6dc` | `#c96442` |
| **Signal Proof (实证)** | `#f5f5f4` | `#0a0a0a` | `#94a3b8` | `#0039a6` |
| **Bridge Canvas (图桥)**| `#141413` | `#e8e4e0` | `#44403c` | `#ffd500` |
| **Editorial Parchment** | `#f5f4ed` | `#141413` | `#e8e6dc` | `#c96442` |
| **Swiss Modernist** | `#ffffff` | `#111111` | `#111111` | `#e4002b` |
| **Vignelli Canon** | `#f4f1ea` | `#0a0a0a` | `#0a0a0a` | `#f04e23` |

**Rules:** Max 1 accent. No AI-purple. Same doc = same palette. Contrast check mandatory. Light surface uses dark text. Editorial mode: serif display **500 max**, no `#ffffff` canvas, no cool `#64748b` grays. Full rules → `references/editorial-parchment-language.md`. Still Paper, Signal Proof, and Bridge Canvas inherit specific typographic/layout constraints.

**Semantic colors (技术架构/数据流图):** 组件类型 → 固定语义色（frontend 青 / backend 绿 / database 紫 / cloud 琥珀 / security 玫红 / msgbus 橙 / external 石灰），双主题配对。颜色表达"这是什么组件"，和美学调色板分工。与 Max-1-accent / No-AI-purple 的调和见 → `references/semantic-component-colors.md`.

---

## 3. TYPOGRAPHY

越大越细，越小越粗：Large=200(ExtraLight) · Body=300(Light) · Small=500-600(SemiBold)

Labels: ≤6 words · ≤8 Chinese chars · no ALL CAPS · same language per diagram

---

## 3.5. THEME & EXPORT SYSTEM (Phase 1 upgrade)

All self-contained HTML templates include two core modules:

### Theme System (`_archviz-theme.html`)
- **6 palettes**: Warm Paper, Swiss Neutral, Editorial Parchment, Swiss Modernist, Vignelli Canon, IKB Dark
- **Auto-time theme**: By default (no saved preference), pages display Editorial Parchment during the day (6:00 AM – 6:00 PM) and switch to IKB Dark at night (6:00 PM – 6:00 AM). The `auto-time` palette selection is also cycleable.
- **CSS variables**: `--av-surface`, `--av-text-primary`, `--av-accent`, `--av-chart-1..6` etc.
- **Auto-detect**: `prefers-color-scheme: dark` → IKB Dark (when `auto-time` is not used)
- **Runtime toggle**: click button (top-right) or press **T** to cycle palettes
- **Persistence**: `localStorage('archviz-palette')`

### Export System (`_archviz-export.html`)
- **Keyboard shortcuts**: **T** = cycle theme, **E** = export menu, **E→P** = PNG, **E→S** = SVG, **E→W** = WebP, **E→C** = clipboard
- **4× raster**: SVG uses native viewBox scaling (not bitmap upscale), canvas uses `renderAtScale()` hook or upscale fallback
- **SVG export**: injects current CSS vars into cloned SVG → standalone file
- **Clipboard**: `ClipboardItem` API with console fallback
- **Export target**: `.archviz-export-target` class on main element, or auto-detect SVG/canvas/article

### Template Integration Rules
1. Every new HTML template MUST include both modules (paste full content)
2. All hardcoded hex → CSS variables (`#f5f0eb` → `var(--av-surface)`, `#1B365D` → `var(--av-text-primary)`)
3. Chart colors → `--av-chart-1` through `--av-chart-6`
4. Canvas charts MUST listen for `archviz-theme-changed` event to redraw
5. Add `class="archviz-export-target"` to main chart/canvas element
6. Reference: `references/export-patterns.md`

---

## 4. LAYOUT

- Mindmap: auto-layout
- Flowchart: LR for processes, TD for hierarchies
- Max 4-5 subgraphs, short noun labels
- Non-symmetric unless content demands it
- Structural soft-cap: **9 nodes** → prefer split; hard split **>12 nodes / >15 edges**
- Absolute Mermaid layout cap: 50 nodes → must split
- Focal accent: **1–2 nodes** only

---

## 5. CONTENT DENSITY

| Data | Format |
|---|---|
| 2-3 items | Table |
| 4-8 items | Bar chart |
| Proportional | Treemap/stacked |
| Sequential | Flowchart |
| Hierarchical | Mindmap |
| Timeline | Gantt |

Simple comparison (≤5 items) → TABLE, not chart.

---

## 6. SHAPE CONSISTENCY

- Border radius: sharp (0) by default. Never mix.
- Line weight: 1px default, 2px accent. No 3px+.
- Icons: sparingly (1 per group max). No emoji.

---

## 7. QUALITY RULES

**Do:** Cite hex/px · Infer semantic roles · Mark confidence (✅/⚠️/❓) · Match document style

**Don't:** Generic descriptions · Colors without hex · Invent tokens · Ignore context

---

## 8. OUTPUT TEMPLATE

```yaml
---
diagram: [name]
type: [mindmap|flowchart|xychart-beta|gantt|...]
context: [paper|log|PPT|note]
dials: {complexity: N, density: N, restraint: N}
tokens: {surface: "#f5f0eb", text: "#1B365D", border: "#a8a29e", accent: "#002FA7"}
confidence: {palette: "✅", layout: "✅", nodes: "⚠️"}
---
```

---

## 9. WORKFLOW

1. Brief + 4-layer analysis (§0) + **G0 draw-or-not**
2. **G0b brand gate** if first diagram / host brand files (`brand-gate.md`)
3. Set dials (§1)
4. Choose type + environment (§2 + QR / structural map)
5. **If ambiguous card/cover/platform** → state 1 primary format + 2 alternatives, ask ≤3 questions (§Editorial Mode); skip for clear Mermaid/ASCII requests
6. Apply tokens (locked palette)
7. Apply typography (§3)
8. Apply layout (§4) — soft-cap 9 structural nodes
9. Check density (§5)
10. Quality audit (§7)
11. Generate code
12. Validate (render test or alignment check)
13. Embed (caption first = finding)

**Pre-gen checklist:** G0 draw-or-not? G0b brand locked? Brief done? Dials set? Tokens locked? Labels short? ≤9 structural nodes or split plan? Gantt: codes+table+ASCII? Card/cover: judgment+promise+one evidence?

---

## 9b. EDITORIAL MODE

Trigger: 封面、卡片、信息卡、小红书、公众号、分享图、排版、knowledge card, or publishable HTML.

**Load:** `references/editorial-parchment-language.md` + `templates/html/editorial-card.html`.

**Gate G3:** platform/read-vs-share unclear → 1 primary + 2 alternatives + ≤3 questions. User says「按你判断」→ Family B default.

**Families:** A cover · B knowledge 1080×1440 · C square · D long-form width-led. Full sizes/safe-zones → reference file.

---

## 9c. ARCHVIZ PRESENTATION & GRIDS (Arcviz-Layout)

Trigger: 展板、作品集、画册、网格排版、A0/A1、Portfolio, or CSS Paged Media.

- **Layout Workflow**:
  1. **Understand**: List drawing list, text blocks, and constraints (A0 vertical vs A3 landscape).
  2. **Tune**: Select 1 of 3 visual languages: Still Paper (🌿 `#F5F4ED` + Terracotta), Signal Proof (⚡ `#F5F5F4`/`#E4E8F0` + Electric Blue), or Bridge Canvas (🎬 `#141413` + Teal/Gold).
  3. **Split**: Split layout into semantic narrative zones (e.g. concept -> master plan -> render -> details).
  4. **Layout**: Fit drawings/texts into grid columns. Focus on Image-First.
  5. **Verify**: Check flowlines, margins, runts, and contrast.
- **Grids & Hierarchy**:
  - Margins: A0 = `50-80mm`; Portfolio = `6%-8%` of short side.
  - Columns: A0 vertical = `3` or `6`; A0 horizontal = `4`, `8`, or `12`; A3/A4 landscape portfolio = `6` or `12`.
  - Gutters: A0 = `20mm`; Portfolio = `8-12mm`.
  - Asset mapping: Tier 1 (Hero render) $\ge 35\%$, Tier 2 (Master plan/Section) $\ge 20\%$, Tier 3 (Drawings) $\ge 15\%$, Tier 4 (Narratives/Diagrams) $\ge 10\%$, Tier 5 (Metadata) $\le 10\%$.
  - Air bubble: Keep $\ge 1$ grid unit whitespace around Tier 1 hero renders.
- **Card & Presentation Constraints**:
  - Safe zones: 16:9 (asymmetric 2/3 text, 1/3 image); 3:4 portrait (density $\ge 75\%$ height); 9:16 vertical (top 14% logo, middle 44%-52% title, bottom 20% + right 15% interactive safety area).
  - Web-to-print: Use asymmetric `@page :left` and `@page :right` for spine margins. Suppress headers on chapter start. Avoid orphans/widows/runts.
  - AI asset brand consistency: Reserve 1/3 text zone in prompts with preservation clause. Use canonical logo plate SVG/PNG with `inputImages` reference.

---

## 10. GANTT (hard rules)

- Inside gantt block: ultra-short codes only (V1.1, A1, B3)
- Full names: mandatory table immediately after
- Terminal rendering: `termaid gantt.mmd --theme mono` (preferred) or plain text fallback
- Min bar: 3w. Merge short tasks.
- Section: 3-6 tasks. Group by phase.

---

## 10b. ACADEMIC TABLE (hard rules)

Trigger: 论文表格、性能对比表、实验结果表、benchmark table、ablation study、comparison table.

**When to use:**
- Multi-level headers (e.g., Math Domain / Code Domain / Chat Domain)
- Row groups (e.g., Target Model → Eagle3/DFlash/DSpark)
- Bold highlighting for best values
- Print-ready, A4-friendly layout

**Template:** `templates/html/academic-table.html`

**Data structure (JSON):**
```json
{
  "title": "Table 1: Main speculative decoding results",
  "subtitle": "Accepted length τ (higher is better) across benchmarks.",
  "columnGroups": [
    { "label": "Math Domain", "span": 3 },
    { "label": "Code Domain", "span": 3 },
    { "label": "Chat Domain", "span": 3 }
  ],
  "columns": ["GSM8K", "MATH", "AIME25", "MBPP", "HumanEval", "LCB", "MT-Bench", "Alpaca", "Arena-Hard"],
  "rowGroups": [
    {
      "label": "Qwen3-4B",
      "rows": [
        { "method": "Eagle3", "values": [3.21, 2.87, 2.15, 3.45, 3.12, 2.78, 3.67, 3.89, 3.34] },
        { "method": "DFlash", "values": [3.56, 3.12, 2.45, 3.78, 3.45, 3.12, 4.01, 4.23, 3.67] },
        { "method": "DSpark", "values": [4.12, 3.78, 3.01, 4.34, 4.12, 3.67, 4.56, 4.78, 4.23], "best": true }
      ]
    }
  ],
  "footer": "τ = average accepted tokens per decoding round."
}
```

**Styling rules:**
- Multi-level header: `rowspan` for row group labels, `colspan` for column groups
- Row groups: distinct background (`--av-surface`), bold label
- Best values: `font-weight: 600`, `color: var(--av-accent)`
- Hover effect: `var(--av-accent-soft)` background
- Typography: 13px body, 12px group headers, 11px column headers
- Numbers: `font-variant-numeric: tabular-nums` for alignment

**Quality checklist:**
- [ ] All column headers visible, no truncation
- [ ] Row group labels clear and distinct
- [ ] Best values highlighted with accent color
- [ ] Numbers right-aligned, text left-aligned
- [ ] Print-friendly (test with Cmd+P)
- [ ] Theme toggle works (T key)

---

## 11. ASCII MODE

Plain text only. Max 80 columns. **No box-drawing characters** (┌─┐╔═╗╰─╯等)——在多数终端、聊天窗口、非等宽字体环境下会乱码。

**允许的符号：**
| 元素 | 符号 |
|---|---|
| 节点 | `[文本]` 或 `(文本)` |
| 重要节点 | `[[文本]]` 或 `((文本))` |
| 决策 | `{文本}` |
| 箭头 | `-->` `-->` `==>` |
| 虚线 | `--->` |
| 竖线 | `\|` |
| 分隔 | `---` `===` |

**示例：**
```
[Input] --> [Process] --> [Output]
                |
                v
           {Decision}
           /        \
      [Path A]    [Path B]
```

**Preferred**: `termaid` (`pip install termaid`) — renders actual Mermaid syntax in terminal. Use `termaid diagram.mmd --theme mono` instead of hand-crafting ASCII when available. 6 themes: default, terra, neon, mono, amber, phosphor. 18 diagram types.

**Fallback tools** (when termaid not installed): `pyfiglet` (headers), `boxes` (borders), `cowsay` (annotations)

**External tool integration**: See `references/external-tools.md` + `ecosystem-routing.md` for Mermaid, diagram-design (type map only), draw.io, Excalidraw, termaid, next-ai-draw-io MCP, Vega-Lite.

---

## 11b. STYLE PRESETS (from drawio-skill)

Save and reuse visual styles across diagrams. Preset format (YAML):

```yaml
# .archviz-preset.yaml
name: warm-paper-restrained
tokens: {surface: "#f5f0eb", text: "#1B365D", border: "#a8a29e", accent: "#002FA7"}
mermaid_init: "%%{init: {'theme':'base','themeVariables':{'primaryColor':'#f5f0eb',...}}}%%"
dials: {complexity: 4, density: 3, restraint: 8}
```

**Extract from existing diagram**: Read `%%{init:...}%%` block → parse themeVariables → save as preset.

**Built-in presets**: warm-paper (default), swiss-neutral, ikb-accent, lemon-accent, stone-mono, editorial-parchment, warm-paper-dark, ikb-dark.

---

## 11c. DARK MODE TOKENS

Mirror every light palette with a dark counterpart. Same accent, inverted surface/text.

| System | surface | text | border | accent |
|---|---|---|---|---|
| Warm Paper Dark | `#1a1814` | `#e8e4e0` | `#44403c` | — |
| IKB Accent Dark | `#0d1117` | `#c9d1d9` | `#30363d` | `#58a6ff` |

**Rules**: Same accent hue, lighter tint. Surface = near-black with warm undertone (never pure `#000000`). Text = light gray (never pure `#ffffff`). Auto-detect via `prefers-color-scheme: dark` for HTML; manual toggle for Mermaid.

**Mermaid dark init:**
```
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#1a1814', 'primaryTextColor': '#e8e4e0', 'primaryBorderColor': '#44403c', 'lineColor': '#58a6ff', 'tertiaryColor': '#2a2520', 'fontSize': '13px'}}}%%
```

---

## 12. TEMPLATES

Actual files live in `templates/`. Prefer reading the specific file at use time (do not hardcode counts).

```
templates/
├── mermaid/     gantt, sequence, swimlane, quadrant, sankey, state-machine, …
│                flowchart + mindmap + erDiagram: generate inline with DESIGN.md tokens
├── ascii/       flowchart, architecture, gantt, icon-system
├── html/        charts + editorial-card + swiss-modernist-grid + network-topology + theme/export
├── python/      scatter-plot, box-plot, candlestick, parallel-coordinates
└── excalidraw/  mindmap.excalidraw, architecture.excalidraw (Warm Paper sketch; promote → Mermaid)
```

**Route out (no empty dirs):**
- Obsidian Canvas → generate `.canvas` JSON only if user asks
- 3D Three.js → **archviz-3d** skill
- draw.io → `drawio-output-mode.md`
---

## 13. TROUBLESHOOTING

| Issue | Fix |
|---|---|
| Editorial wrong palette | Host doc wins; else Editorial Parchment `#f5f4ed` + Terracotta `#c96442` — never mix with IKB |
| Cover too dense | Family A: drop to judgment + promise + one evidence; move rest to Family B |
| Card needs PNG export | Built-in: press E→P for 4× raster PNG, E→S for SVG, E→C for clipboard. See §Export System. |
| Mindmap fails | Use flowchart/subgraph |
| Architecture-beta lexer error | Use flowchart TD + subgraph (preview-compatible) |
| Mermaid trailing end error | Never close graph/flowchart TD blocks with end; only subgraph blocks require end |
| Gantt text overflow | Codes only + table + ASCII fallback |
| Theme too flashy | Force solarized-light/nord-light |
| Text unreadable | Check contrast rule (QR) |
| Too many nodes | Split into subgraphs |
| Canvas blank (Three.js) | Check console for CDN 404 / import errors |
| animejs not animating | v4 API: `animate(target, props)` not `anime({targets})` |
| Render loop stops | Don't name loop function `animate` (conflicts with animejs import) |
| Custom flow nodes "断掉" / bad attach | Paths drawn after nodes or wrong endpoint math | Draw all flow <path> first, then <rect>/<circle> on top. Compute attach = center ± (half-size or r) * unit vector from angle. See examples/us-flows.html + gotchas. |
| Multiple viz files for same data | User eventually demands "combine into one + clean the rest" | Converge early to single canonical Swiss HTML (shared tokens, one container). Pure attachment + restrained color from energy iteration. |
| Grid overlay drifts (viewport shift) | Content-box alignment mismatch | Place `.guides` overlay in the SAME container box as the centered content, sharing margins and templates (see `references/swiss-modernist-grid.md`) |
| CJK text side-bearing offset | Display letters look slightly indented | Implement browser optical alignment to nudge display elements using canvas measurements |
| Headless Helvetica rendering fallback | System lacks real font, fallback to Arial/Noto | Prioritize `Liberation Sans` in the CSS font stack to preserve metric-compatible grotesque spacing, or embed the webfont directly |

---

## 14. ANTI-PATTERNS (student work + common mistakes)

| Anti-pattern | Symptom | Fix |
|---|---|---|
| **Pie for everything** | Pie chart with >5 slices or similar values | ≤3 slices → table; >3 → treemap or stacked bar |
| **Rainbow nodes** | Every node a different color | Same hue, vary lightness. Max 1 accent |
| **Accent as flag system** | 4+ nodes all in accent | Focal 1–2 only; rest ink/muted |
| **Diagram when prose wins** | One-shape or ≤5 items forced into chart | G0: table or sentence |
| **Silent default brand** | Warm Paper into Aver/client repo without ask | G0b brand gate |
| **Flowchart-for-everything** | Non-sequential data forced into flowchart | Match data relationship to type table (§QR) |
| **Label soup** | Labels >10 words, full sentences | ≤6 words / ≤8 Chinese chars. Detail in caption |
| **3D decoration** | 3D bar/pie for "visual interest" | Flat only. Depth = data dimension, never decoration |
| **Dual Y-axis lie** | Two unrelated metrics on shared axis | Split into 2 charts or use indexed/baseline ratio |
| **Truncated axis** | Bar chart Y-axis starts at non-zero | Always start at 0. Use inset zoom if range matters |
| **Legend overload** | >7 legend items, hard to match | Aggregate "Other". Use direct labeling |
| **Default theme** | Mermaid/Chart.js default purple/blue gradient | Always apply custom init + tokens from DESIGN.md |
| **Mermaid block end** | Append end keyword to close flowchart/graph block | Never close graph/flowchart TD with end; end is exclusively for subgraphs |
| **Missing caption** | Diagram embedded without context | Caption = finding, not title. "Sales dropped 30% in Q3" not "Q3 Sales Chart" |
| **Color as only channel** | Red/green distinction for colorblind users | Add pattern/shape/label. Never rely on color alone |
| **Spaghetti network** | >20 edges in network/graph | Cluster nodes, hide weak edges, or split into subgraphs |
| **Mixed metaphor** | Flowchart arrows + pie segments + bar heights in one view | One visual language per diagram. Split if needed |
| **Infinite Gantt** | Gantt with 30+ tasks, unreadable | Group into phases. Detail in separate Gantt or table |
| **Emoji overload** | 🎯📊🔥 in every node | Max 1 icon per group. No emoji in formal deliverables |
| **Cover as summary slide** | 4–6 bullets on a platform cover | Family A: judgment + promise + one evidence only |
| **Editorial serif 700** | Headlines feel bombastic / off-brand | Georgia/Newsreader at 500; enlarge size instead |
| **Cool SaaS white** | `#ffffff` + `#64748b` on cards | Parchment `#f5f4ed` + Near-Black `#141413` |
| **Equal card grid** | Every module same weight | One hero + hierarchy via type scale |

---

## 14b. Pitfalls & Red Lines (绝不)

| 绝不 | Why |
|---|---|
| Ship Mermaid default theme | Reads as AI slop; always custom init |
| Two accents in one set (IKB + Terracotta + cinnabar) | Breaks restraint dial |
| `font-weight: 700` on editorial serif | Off-brand; enlarge type instead |
| `#ffffff` canvas or `#64748b` UI gray | Violates warm editorial contract |
| Box-drawing in ASCII | Garbles in chat/non-mono viewers |
| Pie chart >3 slices | Use table or treemap |
| Skip ASCII fallback when target env unknown | Text-first survivability |
| Embed diagram without finding-caption | Violates G6 |
| Duplicate claude-design-card Playwright pipeline inside archviz | Toolkit bloat — boundary in §When NOT |

---

## 致谢

本项目参考了以下开源项目：

| 项目 | 作者 | 借鉴内容 |
|---|---|---|
| [next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io) | DayuanJiang | 自愈循环机制 |
| [drawio-skill](https://github.com/Agents365-ai/drawio-skill) | Agents365-ai | 样式预设系统 |
| [termaid](https://github.com/fasouto/termaid) | fasouto | 终端Mermaid渲染 |
| [archify](https://github.com/tt-a1i/archify) | tt-a1i | 语义化组件配色 + 五类技术图类型词汇（`references/semantic-component-colors.md` · `diagram-types-technical.md`）|
| [diagram-design](https://github.com/cathrynlavery/diagram-design) | cathrynlavery | 27 类类型词汇 + 删除偏好 + 密度 4/10 + 首跑 brand gate 模式（`structural-diagram-types.md` · `brand-gate.md`）|
| [headroom](https://github.com/chopratejas/headroom) | chopratejas (Netflix) | Compression mindset: input normalization, terse output shaping, reversible caching for iterative refinement |

---

## 15. COMPRESSION & TOKEN BUDGET (Headroom inspired)

Archviz output competes for context window with prompt, tool results, and system memory.
Render this section as operational rules, not aspirational goals.

### 15.1 Input side (before generation)

| Rule | Why |
|------|-----|
| Flatten JSON arrays to `[{label,value}]` before passing to chart | Whitespace and nesting are the token killers headroom targets |
| Strip decorative prose from data payloads; keep only numeric/label fields | Tool output cost dominates when agent re-reads the same data |
| One source of truth per diagram; deduplicate cross-references with `key` fields | Duplicate labels break max-1-accent and waste tokens |
| ASCII fallback prepared in parallel, not after render failure | Avoid the expensive "generate big HTML → fail → retry" loop |

### 15.2 Output side (after generation)

| Rule | Target |
|------|--------|
| Embed self-contained HTML only when interactivity/animation is required | Static saves tokens; Mermaid + image export replaces heavy HTML for static deliverables |
| Export system (E→P/S/W/C) de-prioritizes re-render; use SVG for single-shape, PNG only when client demands raster | PNG at 4× is expensive in output tokens and base64 |
| Embed dedup: if same diagram appears in 2 notes, link to one canonical HTML; second brief becomes a `[view]` reference | Avoids shipping duplicate 30KB assets |
| Self-healing loop ≤2 rounds; third failure ships ASCII fallback + documented warning | Prevents the model from "fixing" forever and bloating the conversation |

### 15.3 Output shaping for model-written text

- **Terse by default**: Every archviz output block should use finding-first captions, not description restatements.
- **Max 15 words for caption**: `"V1 closed loop; 3 feedback paths, 1 integration gap"`, not `"This diagram illustrates the closed loop of V1 with three feedback paths and one integration gap"`.
- **Skip decorative transitions**: No "Great, let me now show you…", no "I've generated the diagram above for your reference".
- **Evidence-first body**: Chart itself is the evidence; caption is the claim. Model text explains nothing the chart doesn't already show.

### 15.4 Reversible caching analog (CCR)

Archviz does not have a full CCR reversibility layer, but inherit the principle:

1. **Golden copy**: First successful render of a template is cached at `templates/html/` or `exports/`.
2. **Rollback contract**: If the self-healing loop or a later edit breaks a diagram, revert to last known good. Do not ship a broken diagram with a "fix in progress" note.
3. **Audit log**: `CHANGELOG.md` records the before/after state for every major diagram change.

### 15.5 Practical budget tiers

| Context | Allowed format budget |
|---------|----------------------|
| Terminal / CLI chat | Mermaid ≤ 30 nodes, ASCII fallback |
| Obsidian note | Self-contained HTML ≤ 200KB, Mermaid inline |
| Deliverable PNG | SVG → PNG (4×), no base64 embeds in chat |
| Batch export | Use `headroom-wrap` for Mermaid/HTML before model re-reads; expect 40–90% token reduction on tool outputs |


---

## 16. RESOURCES

| Project | Role for archviz |
|---|---|
| [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) | Default text engine |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 27-type taxonomy reference (not vendored) |
| [jgraph/drawio](https://github.com/jgraph/drawio) | Editable professional export |
| [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw) | Sketch / workshop boards |
| [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) | Alt Mermaid render |
| [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | Swiss PPT |
| [anydesign](https://github.com/archsueh/anydesign) | Design analysis |
| [claude-design-card](https://github.com/geekjourneyx/claude-design-card) | Editorial Parchment lineage |

Routing → `ecosystem-routing.md` · Types → `structural-diagram-types.md` · Brand → `brand-gate.md` · Full design → DESIGN.md

---

## 16b. 3D — see archviz-3d

3D / Three.js 实现细节与 animejs v4 踩坑全部归属 archviz-3d。
权威落点：`archviz-3d/SKILL.md` → `## Key Gotchas` + `## Detailed Pitfalls & Patterns`
（importmap、API 迁移、`renderLoop` 命名冲突、相机 tween、DPR cap、光照/explode 约束）。
本仓库只保留 2D 信息可视化；3D brief → 路由到 archviz-3d。
