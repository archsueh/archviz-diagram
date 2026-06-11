---
name: archviz-skills
description: |
  Restrained information visualization skill pack for AI agents. Every visualization starts with a brief read and three dials.
  Supports Mermaid, ASCII, self-contained HTML, Python (Plotly), and Three.js 3D archviz. Text-first, preview-compatible, anti-slop.
  Default mode is 2D infoviz; enter 3D only when the brief mentions building, floorplan, structure, or spatial walkthrough.
  Use when the user asks for diagram, visualization, chart, gantt, sankey, mindmap, flowchart, xychart, 可视化, 架构图, 流程图,
  信息图, 甘特图, funnel, state diagram, decision matrix, 漏斗图, 状态机, 决策矩阵, 依赖图, dependency graph, or 3D building/archviz.
license: MIT
metadata:
  version: 0.0.9
  author: archsueh
  triggers: diagram, visualization, chart, gantt, sankey, mindmap, xychart, 可视化, 架构图, 流程图, 信息图, 甘特图, funnel, state diagram, decision matrix, 漏斗图, 状态机, 决策矩阵, 依赖图, dependency graph, three.js, 3d, archviz, building, floorplan, 建筑, 结构, 楼层, walkthrough, 漫游
---

# archviz-skills

> Every rule is **contextual**. Read the brief first, then pull only what fits.

---

## QUICK REFERENCE (agent loads this in <5 seconds)

```
Dials:      COMPLEXITY=4  DENSITY=3  RESTRAINT=8
Palette:    surface=#f5f0eb  text=#1B365D  border=#a8a29e  accent=#002FA7 (max 1)
Init:       %%{init: {'theme':'base','themeVariables':{'primaryColor':'#f5f0eb','primaryTextColor':'#1B365D','primaryBorderColor':'#a8a29e','lineColor':'#a8a29e','tertiaryColor':'#d6d3d1','fontSize':'13px'}}}%%
Contrast:   luminance(0.299R+0.587G+0.114B) < 128 → light text, ≥ 128 → dark text
Labels:     ≤6 words / ≤8 Chinese chars / no ALL CAPS
Gantt:      codes only inside block + table beside + ASCII fallback / min 3w
Anti-slop:  no purple default / no rainbow / no flowchart-for-everything / no pie
```

**Type selection (fast):**
| Data | Type | Template |
|---|---|---|
| Hierarchical | mindmap | — |
| Sequential | flowchart LR/TD | — |
| System/layered | flowchart TD + subgraph | — |
| Comparison/ranking | xychart-beta (bar) | — |
| Proportional | treemap or stacked bar | — |
| Timeline | gantt | `mermaid/gantt.mmd` |
| Distribution | histogram/box | `mermaid/distribution.mmd` |
| Correlation | scatter/heatmap | `python/scatter-plot.py` |
| Flow/network | sankey | `mermaid/sankey.mmd` |
| Funnel/conversion | funnel chart | `html/funnel.html` |
| Decision/evaluation | decision matrix (table) | `mermaid/decision-matrix.mmd` |
| State transitions | stateDiagram-v2 | `mermaid/state-machine.mmd` |
| Dependencies | dependency graph | `mermaid/dependency-network.mmd` |
| Multi-criteria scoring | radar or diverging bar | `html/radar.html` / `mermaid/diverging-bar.mmd` |
| Simple (≤5 items) | **TABLE, not chart** | — |
| **3D: Building structure** | Three.js structure shell | `html/threejs-archviz.html` |
| **3D: Floor plan** | Three.js extruded floor | `html/threejs-floorplan.html` |
| **3D: Section cut** | Three.js ClippingPlane | `html/threejs-archviz.html` |

**Mixed types** (when data spans categories):
- Process + timeline → flowchart with gantt sub-section (split into 2 diagrams)
- Hierarchy + comparison → mindmap with leaf annotations (table beside)
- Flow + metrics → sankey with tooltip/badge annotations
- Decision + scoring → decision matrix → radar for top candidates
- **Rule: never combine >2 types in one diagram. Split instead.**

**Degradation strategy** (when data is too complex):
1. >50 nodes → split into 2-3 linked diagrams with shared legend
2. >7 categories → aggregate into "Other" + detail diagram
3. Mixed data types → identify primary relationship, table the rest
4. Preview environment fails → ASCII fallback (always prepared)
5. Mermaid syntax error → flowchart TD + subgraph (most compatible)

**Environment routing:**
| Env | Output |
|---|---|
| Obsidian/preview | lightweight Mermaid / ASCII / self-contained HTML |
| Terminal | pure ASCII (pyfiglet, boxes) |
| Deliverables | Python (Plotly/Matplotlib) |
| **3D / archviz** | **Three.js self-contained HTML (CDN import)** |

**3D archviz mode** (when brief = building/structure/spatial):
- Stack: Three.js + animejs (camera transitions) + OrbitControls
- Output: self-contained HTML with CDN imports (no build step)
- Types: structure shell / floor plan extrusion / section cut / multi-floor nav
- Tokens: inherits 2D palette + adds `structure=#a8a29e`, `floor=#e8e4e0`, `accent-3d=#002FA7`
- Constraints: procedural geometry preferred, max 3 lights, responsive resize, animejs for camera moves
- Full rules → DESIGN.md §3D Architectural Visualization

**CDN importmap pattern** (self-contained HTML, zero build):
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
| animejs v3→v4 API | `anime({targets: x, ...})` 报错 | v4 是 `animate(target, params)`，无 `targets` key |
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

Output one line: **"Reading this as: \<type> for \<audience>, \<vibe>, \<palette>."**

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

**Rules:** Max 1 accent. No AI-purple. Same doc = same palette. Contrast check mandatory. Light surface uses dark text.

---

## 3. TYPOGRAPHY

越大越细，越小越粗：Large=200(ExtraLight) · Body=300(Light) · Small=500-600(SemiBold)

Labels: ≤6 words · ≤8 Chinese chars · no ALL CAPS · same language per diagram

---

## 4. LAYOUT

- Mindmap: auto-layout
- Flowchart: LR for processes, TD for hierarchies
- Max 4-5 subgraphs, short noun labels
- Non-symmetric unless content demands it
- Hard cap: 50 nodes → split

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

1. Brief + 4-layer analysis (§0)
2. Set dials (§1)
3. Choose type + environment (§2 + QR table)
4. Apply tokens (DESIGN.md)
5. Apply typography (§3)
6. Apply layout (§4)
7. Check density (§5)
8. Quality audit (§7)
9. Generate code
10. Validate (render test or alignment check)
11. Embed (caption first = finding)

**Pre-gen checklist:** Brief done? DESIGN.md contract complete? Dials set? Tokens locked? Labels short? Gantt: codes+table+ASCII?

---

## 10. GANTT (hard rules)

- Inside gantt block: ultra-short codes only (V1.1, A1, B3)
- Full names: mandatory table immediately after
- ASCII fallback: always include
- Min bar: 3w. Merge short tasks.
- Section: 3-6 tasks. Group by phase.

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

Tools: `pyfiglet` (headers), `boxes` (borders), `cowsay` (annotations)

---

## 12. TEMPLATES

Actual files live in `templates/`. Current inventory (do not hardcode counts in prompts):

```
templates/
├── mermaid/    15 files (gantt, sankey, distribution, diverging-bar, network, scoring, intro, architecture, closed-loop variants, funnel, decision-matrix, state-machine, dependency-network)
│               flowchart + mindmap: inline Mermaid (no standalone .mmd)
├── ascii/       4 files (flowchart, architecture, gantt, icon-system)
├── html/       14 files (bubble, bullet-graph, funnel, gauge, heatmap, line, radar, sunburst, treemap, waffle, waterfall, self-contained, threejs-archviz, threejs-floorplan)
└── python/      5 files (scatter-plot, box-plot, candlestick, parallel-coordinates, viz template)
```

Prefer reading the specific template file under `templates/<mode>/` at use time instead of relying on this list.
Flowchart and mindmap have no template files — generate inline using tokens from DESIGN.md.
---

## 13. TROUBLESHOOTING

| Issue | Fix |
|---|---|
| Mindmap fails | Use flowchart/subgraph |
| Architecture-beta lexer error | Use flowchart TD + subgraph (preview-compatible) |
| Gantt text overflow | Codes only + table + ASCII fallback |
| Theme too flashy | Force solarized-light/nord-light |
| Text unreadable | Check contrast rule (QR) |
| Too many nodes | Split into subgraphs |
| Canvas blank (Three.js) | Check console for CDN 404 / import errors |
| animejs not animating | v4 API: `animate(target, props)` not `anime({targets})` |
| Render loop stops | Don't name loop function `animate` (conflicts with animejs import) |

---

## 14. ANTI-PATTERNS (student work + common mistakes)

| Anti-pattern | Symptom | Fix |
|---|---|---|
| **Pie for everything** | Pie chart with >5 slices or similar values | ≤3 slices → table; >3 → treemap or stacked bar |
| **Rainbow nodes** | Every node a different color | Same hue, vary lightness. Max 1 accent |
| **Flowchart-for-everything** | Non-sequential data forced into flowchart | Match data relationship to type table (§QR) |
| **Label soup** | Labels >10 words, full sentences | ≤6 words / ≤8 Chinese chars. Detail in caption |
| **3D decoration** | 3D bar/pie for "visual interest" | Flat only. Depth = data dimension, never decoration |
| **Dual Y-axis lie** | Two unrelated metrics on shared axis | Split into 2 charts or use indexed/baseline ratio |
| **Truncated axis** | Bar chart Y-axis starts at non-zero | Always start at 0. Use inset zoom if range matters |
| **Legend overload** | >7 legend items, hard to match | Aggregate "Other". Use direct labeling |
| **Default theme** | Mermaid/Chart.js default purple/blue gradient | Always apply custom init + tokens from DESIGN.md |
| **Missing caption** | Diagram embedded without context | Caption = finding, not title. "Sales dropped 30% in Q3" not "Q3 Sales Chart" |
| **Color as only channel** | Red/green distinction for colorblind users | Add pattern/shape/label. Never rely on color alone |
| **Spaghetti network** | >20 edges in network/graph | Cluster nodes, hide weak edges, or split into subgraphs |
| **Mixed metaphor** | Flowchart arrows + pie segments + bar heights in one view | One visual language per diagram. Split if needed |
| **Infinite Gantt** | Gantt with 30+ tasks, unreadable | Group into phases. Detail in separate Gantt or table |
| **Emoji overload** | 🎯📊🔥 in every node | Max 1 icon per group. No emoji in formal deliverables |

---

## 15. RESOURCES

- [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) — Official
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) — 10.3k stars
- [mermaid-rs-renderer](https://github.com/1jehuang/mermaid-rs-renderer) — Fast Rust
- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) — Swiss PPT
- [anydesign](https://github.com/archsueh/anydesign) — Design analysis

Full design system → DESIGN.md · Detailed rules → references/ · Research → research/

---

## 16. 3D GOTCHAS (踩坑记录)

Three.js + animejs v4 实战中遇到的坑，按出现顺序记录。

### CDN 依赖（自包含 HTML 模板）

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
```

**⚠️ animejs v4 路径不是 `lib/anime.es.js`** — 那是 v3 的路径。v4.4.1 的正确路径是 `dist/bundles/anime.esm.js`。验证方法：`curl -sI <CDN_URL>` 返回 200 才可用。

### animejs v4 API 迁移

| v3（旧） | v4.4.1（当前） |
|---|---|
| `import anime from 'animejs'` | `import { animate } from 'animejs'` |
| `anime({targets: obj, x: 1, duration: 500})` | `animate(obj, {x: 1, duration: 500})` |

**包装函数**（统一写法，避免每次改 API）：
```js
import { animate } from 'animejs';
function tween(target, props) { return animate(target, props); }
// 用法：tween(camera.position, {x: 6, y: 4, z: 8, duration: 800})
```

### 命名冲突

```js
// ❌ 错误 — animate 与 animejs 导入冲突
function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
animate();

// ✅ 正确 — 用 renderLoop 或其他名称
function renderLoop() { requestAnimationFrame(renderLoop); renderer.render(scene, camera); }
renderLoop();
```

### 地面位置

```js
// ❌ 物体 y=0 会埋进地面
scene.add(dryer); // dryer.position.y 默认 0

// ✅ 物体抬高到地面之上
scene.add(dryer);
dryer.position.y = 2; // 或者降低地面：gMesh.position.y = -0.5
```

### 相机动画不要直接赋值

```js
// ❌ 跳跃式，无过渡
camera.position.set(6, 4, 8);

// ✅ 用 tween 平滑过渡
tween(camera.position, {x: 6, y: 4, z: 8, duration: 800, easing: 'easeInOutCubic'});
```

### 光照数量限制

模板约束 max 3 光源（1 HemisphereLight + 1 DirectionalLight + 1 AmbientLight）。超出会影响性能且难以控制阴影。
