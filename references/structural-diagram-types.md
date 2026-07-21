# Structural Diagram Types — 27-type routing map

Absorbed as a **type selector** from [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) (27 editorial types).  
archviz does **not** re-implement their gallery; it maps each type to an existing archviz engine + template.

Philosophy borrowed (compatible with archviz restraint):
- Highest-quality move is usually **deletion**
- Accent reserved for **1–2 focal items only** (not a flag system)
- Target density ≈ 4/10 (maps to dials DENSITY≈3–4, RESTRAINT≈8)
- Diagram is done when **nothing can be removed**, not when everything is added

## G0 adjunct — when NOT to draw

Before generating, answer: *Would the reader learn more from this visual than from a well-written paragraph or a 3-column table?*

| Situation | Prefer instead of a diagram |
|---|---|
| List of things / options | Table or bullets |
| Simple before/after (2 cells) | Table or prose |
| One-shape "diagram" | Just write the sentence |
| ≤5 comparable numbers | **TABLE** (archviz QR rule) |
| Permissions / access grid | Table (`academic-table.html`) |
| Quick terminal sketch only | ASCII / termaid, not HTML gallery |

If no → **do not draw**. Ship prose/table and stop (G0 fail is success when the answer is "don't diagram").

## Density & split budget (structural)

| Budget | Rule |
|---|---|
| Soft cap | **9 nodes** on one structural schematic → prefer split |
| Hard split | **>12 nodes** or **>15 edges** → overview + detail (never one spaghetti) |
| Absolute | 50 nodes still hard-fail for Mermaid layout (legacy QR) |
| Focal | Accent on **1–2 nodes max**; if tempted by 4, you have not chosen a focus |
| Hybrid | Combining two types → pick **dominant axis** only; don't hybridize grammars |

## Connector discipline (any engine)

| Rule | Why |
|---|---|
| Prefer orthogonal elbows over free diagonals | Traceable paths |
| No two connectors sharing one attach point | Fan attach ≥12px apart (HTML: `_flow-attach.html`) |
| Arrow labels need gap/mask from the stroke | Avoid line-through-text |
| Async / optional → dashed; main path → solid accent or ink | Path semantics |
| Reroute around non-endpoint boxes | No accidental "through" nodes |

## Type → engine map

| # | Type | When to use | Preferred engine | Template / pattern |
|---|---|---|---|---|
| 1 | Architecture | Components + connections + boundaries | Mermaid flowchart TD + subgraph · or HTML | semantic colors; `diagram-types-technical.md` |
| 2 | Flowchart | Decision logic, branches | Mermaid flowchart | inline; ASCII fallback |
| 3 | Sequence | Messages over time, API handshake | Mermaid `sequenceDiagram` | `mermaid/sequence.mmd` |
| 4 | State machine | States + transitions + terminal | Mermaid stateDiagram-v2 | `mermaid/state-machine.mmd` |
| 5 | ER / data model | Entities + fields + relations | Mermaid `erDiagram` | inline (short field names) |
| 6 | Timeline | Events on an axis | Mermaid timeline / gantt | `mermaid/gantt.mmd` or HTML line |
| 7 | Swimlane | Cross-functional process | Mermaid flowchart + subgraph lanes | `mermaid/swimlane.mmd` |
| 8 | Quadrant / 2×2 | Impact×effort, scenario matrix | Mermaid quadrantChart · or HTML | `mermaid/quadrant.mmd` |
| 9 | Nested | Hierarchy by containment | Mermaid flowchart subgraph nest · HTML nested cards | max 3 nest levels |
| 10 | Tree | Parent → children | Mermaid flowchart TD · mindmap | mindmap if shallow |
| 11 | Org chart | Ownership + routing | Mermaid flowchart TD | short titles; split if >15 nodes |
| 12 | Venn | Set overlap (≤3 sets) | HTML SVG preferred · Mermaid limited | pure HTML if exact overlap needed |
| 13 | Layer stack | Stacked abstractions | Mermaid flowchart TD subgraphs | bottom=infra top=UI |
| 14 | Pyramid / funnel | Ranked hierarchy or drop-off | HTML funnel · Mermaid funnel | `html/funnel.html` / `mermaid/funnel.mmd` |
| 15 | Consultant 2×2 | Named cells, scenarios | Mermaid quadrantChart + caption table | `mermaid/quadrant.mmd` |
| 16 | Radar / spider | Multi-axis comparison ≤7 | HTML radar | `html/radar.html` |
| 17 | Loop / flywheel | Stations around a hub | Mermaid flowchart circular · HTML | hub node + return edges |
| 18 | IT current-state | Legacy landscape, modernization | Mermaid flowchart + semantic colors | mark legacy vs target |
| 19 | High-level stack | End-to-end on a cluster | Mermaid flowchart LR layers | 3–5 layers max |
| 20 | Bar chart | Categorical comparison | Mermaid xychart-beta · HTML | ≤12 bars |
| 21 | Line chart | Trends over time | HTML line · Python | `html/line-chart.html` |
| 22 | Gantt | Tasks and phases | Mermaid gantt | codes+table hard rules |
| 23 | Scatter | Distribution / correlation | Python / HTML | `python/scatter-plot.py` |
| 24 | Process | Multi-actor sequential workflow | Swimlane or sequence | pick by "messages?" vs "lanes?" |
| 25 | Medallion | Multi-tier data storage (bronze/silver/gold) | Mermaid flowchart LR | tier subgraphs |
| 26 | Data flow | Role-scoped pipeline | Mermaid flowchart LR / Sankey | `diagram-types-technical.md` Data Flow |
| 27 | DP security matrix | Per-role access | **Table first** · HTML academic table | `html/academic-table.html` |

## Gaps vs diagram-design (honest)

| Gap | Status | Plan |
|---|---|---|
| Brand-onboarding from website crawl | **Host-first gate** | `brand-gate.md` (DESIGN.md / preset; no silent default into branded repos) |
| Full-editorial HTML gallery for all 27 | No | On-demand type only; no asset dump |
| Sketchy / terminal primitives | ASCII + termaid + **Excalidraw templates** | `templates/excalidraw/` |
| Venn exact geometry | Weak in Mermaid | HTML SVG when needed |

## Selection heuristics

1. **Messages between actors over time?** → Sequence  
2. **Multiple orgs / roles own steps?** → Swimlane  
3. **Two continuous axes to position items?** → Quadrant  
4. **States with events?** → State machine (not flowchart)  
5. **Entities + attributes?** → ER  
6. **Part-to-whole drop-off?** → Funnel/pyramid, not pie  
7. **Permissions grid?** → Table, not graph  
8. **≤5 simple items?** → Table, not chart  
9. **Reader learns more from a paragraph?** → Don't draw  

## Cross-links

- Technical five-class (architecture/workflow/sequence/data flow/lifecycle) → `diagram-types-technical.md`
- Engine handoff (Mermaid / draw.io / Excalidraw) → `ecosystem-routing.md`
- Brand / first-run tokens → `brand-gate.md`
- Component semantic colors → `semantic-component-colors.md`

Last updated: 2026-07-21
