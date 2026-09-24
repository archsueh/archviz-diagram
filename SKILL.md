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
- Architectural diagrams (2D only), flow, timeline, comparison, state, dependency briefs.
  (3D spatial → `archviz-3d`；动态 GIF 技术图 → `archviz-animated`。)
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

**先判静态还是动态**，再按内容类型选：

| Need | Use |
|---|---|
| **静态** 2D 流程图 / 框架图（process flows, architecture, concepts） | **archviz-diagram** (this skill) |
| **动态** 技术图（GIF 动效 + Excalidraw 可编辑源，纯代码生成、结果可复现，**无需 image API**） | [archviz-animated](https://github.com/archsueh/archviz-animated) |
| 3D spatial (building, exploded, mechanical) | [archviz-3d](https://github.com/archsueh/archviz-3d) |
| Dark tech infrastructure diagrams | **archviz-diagram** Dark Mode (built-in, see DESIGN.md §Palette: IKB Dark) |
| Educational flat diagrams (physics, chemistry, engineering) | **archviz-diagram** Educational Flat Mode (built-in, see DESIGN.md §Palette: Educational Flat) |
| Article illustrations / sketches（**前置条件：需要 image_generate 工具**） | [archviz-sketch](https://github.com/archsueh/archviz-sketch) + `sketch-image-pipeline` skill |
| 编号手绘（041号 / 手绘风格库 / 不会描述画风） | `handdraw-style-prompter` —— **不要**用 archviz-sketch 猜编号 |
| Presentation board / portfolio / 展板排版 / 交付前打磨 | [archviz-layout](https://github.com/archsueh/archviz-layout) |
| DESIGN.md for a product brand | anydesign + host DESIGN.md |

**静态 vs 动态判据**：交付物需要**随时间变化**（模块 pulse、流光、状态流转）→ archviz-animated；只需一张能看懂的图 → archviz-diagram。不确定时先出静态图，动效是额外成本而非默认。

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
| `archviz-animated` | 3 deliverables (excalidraw / PNG / GIF) | `~/Developer/archviz-animated` |
| `archviz-layout` | board layout & pre-delivery polish | `~/Developer/archviz-layout` |

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

## 按需加载地图 (Progressive Disclosure Map)

本文件只保留**路由 + 设计系统 + 门禁**。下列文件按触发条件加载 —— **不要预读全部**。

| 触发条件 | 加载 | 得到什么 |
|---|---|---|
| 任何要交付的图 | `references/accessibility-contract.md` | 无障碍 6 条硬规则、对比度真算公式、色盲安全、检查清单 |
| 图里有连接线 | `references/connector-geometry.md` | 折线 / 跨桥 / 扇形展开 / 标签间隙 6 条铁律 |
| 定位节点或间距 | `references/grid-and-spacing.md` | 4px 网格允许取值表、圆角语义、字号阶梯 |
| 交付前定规格 | `references/output-dials.md` | Format / Size / Detail / Audience 四拨盘 + 保真账本 |
| 类型选不准 | `references/semantic-patterns.md` | 10 个行为模式（**先判行为，再选类型**） |
| 元素可能超量 | `references/complexity-budgets.md` | 27 类逐类型预算 + 超限决策树 |
| 生成前扫一遍 | `references/anti-patterns.md` | 反模式表 + 红线（绝不） |
| 报错时 | `references/troubleshooting.md` | 按症状查表 |
| 输出超长 / 成本敏感 | `references/token-budget.md` | 压缩策略与预算分档 |
| 做学术表格 | `references/academic-table-rules.md` | 列宽 / 对齐 / 显著性 / 跨列表头 |
| 做展板 / 作品集 | `references/presentation-grids.md` | 版式网格 + 交付前打磨清单 |
| 查某条规则的出处 | `references/credits.md` | 上游来源与致谢 |

**以下 6 个此前是孤儿文件**（内容存在但全仓库无入口），现纳入地图：

| 触发条件 | 加载 | 得到什么 |
|---|---|---|
| 甘特图 / 时间线 | `references/gantt-rules.md` | 轴与条、里程碑、标签防溢出 |
| 暗色模式 | `references/dark-mode-tokens.md` | 暗色 token 全套对照 |
| 教学图 / "像教科书" | `references/educational-flat-system.md` | Educational Flat 9 色阶系统与适用判据 |
| HTML 模板加动效 | `references/animation-vocabulary.md` | **共享运动词汇表** —— 命名与时长必须照用，不得自创 |
| Mermaid init / pretty-mermaid 主题 | `references/style-guide.md` | 主题搭配与描边/圆角约定 |
| 找素材 / 背景图案 / 图标资源 | `references/design-resources-curated.md` | 从 445 条里筛出的可用资源 |

**可执行校验**：`python3 scripts/self_check.py <file.html>` —— 跑无障碍 / 单文件安全 / 4px 网格 / 对比度 / 连接线几何五类，**退出码非零即不合格**。改完图跑一次，比人眼可靠。

---

## QUICK REFERENCE (agent loads this in <5 seconds)

```
Dials:      COMPLEXITY=4  DENSITY=3  RESTRAINT=8
Palette:    surface=#f5f0eb  text=#1B365D  border=#a8a29e  accent=#002FA7 (max 1)
Init:       %%{init: {'theme':'base','themeVariables':{'primaryColor':'#f5f0eb','primaryTextColor':'#1B365D','primaryBorderColor':'#a8a29e','lineColor':'#a8a29e','tertiaryColor':'#d6d3d1','fontSize':'13px'}}}%%
Contrast:   luminance(0.299R+0.587G+0.114B) < 128 → light text, ≥ 128 → dark text（**仅判明暗**；AA 合规要真算，见 references/accessibility-contract.md）
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

**行为路由（先于类型）：** 类型是*词汇*，行为是*路由*。「要表达审批/回滚/异步/观测/禁止/借道」这类判断 → `references/semantic-patterns.md`（10 个模式 × 触发条件/语义原语/预算/反模式/静态回退）。**先判行为再选类型**，能避免「类型对了但语义错了」。

**Type routing (结构图 27 类):** quadrant / venn / pyramid / org / swimlane / loop 等 → `references/structural-diagram-types.md`（密度 4/10、焦点 1–2、soft-cap 9 nodes）。

**超量处理:** 元素数接近上限、或非节点型维度（生命线/泳道/轴/系列/层/阶段）吃紧时 → `references/complexity-budgets.md`（27 类逐类型预算 + 超限决策树：降级 / 拆图 / 归并 / 换类型）。

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

**风格拨盘 ≠ 交付拨盘。** 上面三个是*风格*（图长什么样）；交付规格（Format / Size / Detail / Audience，含 Size 决定字号阶梯、Detail 的四步降级阶梯、保真账本）见 `references/output-dials.md`。两者并存，不互相替代。

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

> **按需加载** → `references/presentation-grids.md`
> 展板/作品集版式与网格、交付前打磨清单。做**展板类**交付物时加载（日常图表不需要）。

## 10. GANTT (hard rules)

- Inside gantt block: ultra-short codes only (V1.1, A1, B3)
- Full names: mandatory table immediately after
- Terminal rendering: `termaid gantt.mmd --theme mono` (preferred) or plain text fallback
- Min bar: 3w. Merge short tasks.
- Section: 3-6 tasks. Group by phase.

---

## 10b. ACADEMIC TABLE (hard rules)

> **按需加载** → `references/academic-table-rules.md`
> 学术表格硬规则（列宽、对齐、显著性标记、跨列表头）。只在做论文表格时加载。

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

> **按需加载** → `references/troubleshooting.md`
> 按症状查表（渲染空白、字体回退、导出失败、Mermaid 不兼容）。**只在报错时加载**。

## 14. ANTI-PATTERNS (student work + common mistakes)

> **按需加载** → `references/anti-patterns.md`
> 反模式表 + 红线（绝不）。**生成前扫一眼能省一次返工**，但不需要每次全文读。

## 致谢

> **按需加载** → `references/credits.md`
> 上游来源与致谢。需要追溯某条规则的出处时加载。

## 15. COMPRESSION & TOKEN BUDGET (Headroom inspired)

> **按需加载** → `references/token-budget.md`
> Token 预算分档、输入/输出侧压缩、可逆缓存类比（CCR）。只在**输出超长或成本敏感**时加载。

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
