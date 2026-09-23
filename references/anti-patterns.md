# 14. ANTI-PATTERNS (student work + common mistakes)

> 从 `SKILL.md` 原样迁出（2026-09-23 渐进式披露拆分），内容未删改。
> 何时加载：反模式表 + 红线（绝不）。**生成前扫一眼能省一次返工**，但不需要每次全文读。

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
