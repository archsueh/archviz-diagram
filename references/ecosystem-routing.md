# Ecosystem Routing — when to stay in archviz vs hand off

Sources considered (2026-07): [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid), [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) (≈2.8k★), [jgraph/drawio](https://github.com/jgraph/drawio), [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw), [github.com/topics/diagram](https://github.com/topics/diagram).

**Iron rule:** archviz remains **text-first + restrained**. External tools are engines, not a second design system. Always apply Warm Paper / host tokens / max-1-accent on top of whatever engine you pick.

## Decision matrix (pick one primary engine)

| Need | Primary | Why | Fallback |
|---|---|---|---|
| Inline in Markdown / Obsidian / GitHub | **Mermaid** | Native preview, greppable, reviewable | ASCII / termaid |
| Terminal chat / CLI review | **termaid** → Mermaid source | Renders `.mmd` in TTY | Plain ASCII |
| Editorial structural HTML (quadrant, venn, pyramid, flywheel, org) with brand skin | **archviz HTML** first; if type missing → absorb pattern from diagram-design | Same restraint dial + export (E→P) | diagram-design skill as reference-only |
| Editable engineering handoff (AWS/GCP icons, long-lived rework) | **draw.io** (`.drawio` XML) | Shape library + human edit | Mermaid outline + note |
| Hand-drawn whiteboard / workshop / brainstorm | **Excalidraw** (`.excalidraw`) | Freeform + sketchy | ASCII board |
| Quantitative charts (sankey, radar, heatmap, multi-series) | **archviz HTML / Python** | Data accuracy > freeform | Vega-Lite if transforms needed |
| 3D / spatial | **archviz-3d** | Out of 2D skill scope | — |
| Lucidchart-like collab whiteboard | Out of scope | Real-time multiplayer ≠ agent artifact | Excalidraw file or Mermaid |

## What each upstream is good for (borrow patterns, don't bloat runtime)

### Mermaid (mermaid-js/mermaid) — default text engine
- **Use:** flowchart, sequence, state, class, er, gantt, sankey, mindmap, xychart
- **Avoid as default:** `architecture-beta` (preview lexer pain) → prefer `flowchart TD + subgraph`
- **archviz contract:** always `%%{init: theme base + Warm Paper vars}%%`; no default purple theme

### diagram-design (cathrynlavery) — 27 editorial types reference
- **Stars / form:** ~2.8k★ · self-contained HTML+SVG · light / dark / full-editorial variants
- **Steal:** type taxonomy (architecture, sequence, ER, swimlane, quadrant, venn, pyramid, loop/flywheel, org, nested, layers, medallion, IT current-state…); brand-onboarding gate; density target ~4/10; "highest-quality move is deletion"
- **Do not:** ship their jet-black + atomic-tangerine defaults into archviz docs; do not duplicate 27 full HTML galleries
- **Map:** see `structural-diagram-types.md` for archviz engine choice per type

### Draw.io / diagrams.net (jgraph/drawio)
- **Use:** editable professional diagrams, cloud icon packs, PDF/SVG export via CLI
- **archviz path:** `references/drawio-output-mode.md` + self-healing loop (generate → export → VLM check ≤2 rounds)
- **When not:** quick notes, data charts, terminal-only sessions

### Excalidraw
- **Use:** sketchy whiteboard, teaching board, early exploration before formalizing to Mermaid
- **archviz path:** produce minimal `.excalidraw` JSON or Excalidraw Markdown when user asks 手绘/白板/workshop; then optionally **promote** to Mermaid once structure stabilizes
- **Restraint:** still max 1 accent, short labels, no rainbow sticky notes

### Lucidchart alternatives (topic: diagram)
- Treat as discovery surface, not a dependency. Prefer tools that produce **files** agents can write (Mermaid, drawio XML, Excalidraw JSON, self-contained HTML).

## Routing algorithm (agent, 10 seconds)

```
1. Environment?
   terminal → termaid/Mermaid
   markdown note → Mermaid
   editable handoff → draw.io
   sketch/workshop → Excalidraw
   publishable card / data chart → HTML/Python

2. Relationship type? → structural-diagram-types.md or QR table

3. Still ambiguous?
   default Mermaid flowchart TD + subgraph
   prepare ASCII fallback in parallel

4. Apply tokens (DESIGN.md) + G2 contrast + caption = finding
```

## Anti-bloat

| Temptation | Verdict |
|---|---|
| Vendor all 27 diagram-design HTML assets | ❌ Reference taxonomy only |
| Make draw.io the default for everything | ❌ Breaks text-first survivability |
| Ship Excalidraw for formal architecture docs | ❌ Promote to Mermaid/draw.io after sketch |
| Add Lucidchart clone runtime | ❌ Out of scope |

Last updated: 2026-07-21
