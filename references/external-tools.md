# External Tools Reference

Tools from the broader diagram ecosystem that complement archviz-diagram.
Primary routing table → **`ecosystem-routing.md`**. Structural type map → **`structural-diagram-types.md`**.

## Terminal Rendering

### termaid
- **Repo**: https://github.com/fasouto/termaid
- **Install**: `pip install termaid`
- **Usage**: `termaid diagram.mmd --theme mono` or `cat diagram.mmd | termaid`
- **What it does**: Pure Python Mermaid renderer for terminals. 18 diagram types, 6 color themes, ASCII fallback, terminal-width auto-fit.
- **When to use**: Instead of hand-crafting ASCII diagrams. Prefer termaid when available.
- **Integration**: ASCII templates are for environments without termaid.

## Text Engines

### Mermaid (mermaid-js/mermaid)
- **Repo**: https://github.com/mermaid-js/mermaid
- **Role**: **Default** text engine for Markdown / Obsidian / GitHub.
- **archviz contract**: custom `%%{init}%%` Warm Paper tokens; never ship default purple theme; avoid `architecture-beta` in favor of flowchart + subgraph.
- **Templates**: `templates/mermaid/` (gantt, sequence, swimlane, quadrant, state, sankey, …).

## Editorial Structural Gallery (reference)

### diagram-design (cathrynlavery)
- **Repo**: https://github.com/cathrynlavery/diagram-design (≈2.8k★)
- **What it does**: 27 editorial diagram types as self-contained HTML+SVG; brand onboarding from a website; light / dark / full-editorial variants.
- **Borrow**: type taxonomy, deletion bias, density ~4/10, first-run style-guide gate.
- **Do not**: dump their 27-asset gallery into this repo; do not adopt their default jet-black + atomic-tangerine skin into archviz docs.
- **Map**: `structural-diagram-types.md` routes each type to Mermaid / HTML / table.

## Diagram Generation (Draw.io)

### drawio-skill
- **Repo**: https://github.com/Agents365-ai/drawio-skill
- **What it does**: Generates .drawio XML, exports to PNG/SVG/PDF/JPG via draw.io CLI. Self-check loop, style presets.
- **Key mechanism — Self-healing loop**: Generate → render PNG → VLM → fix → re-render (archviz caps at **2 rounds**).
- **When to use**: Precise layout, branded cloud shapes, long-lived editable diagrams.
- **archviz path**: `drawio-output-mode.md`.

### next-ai-draw-io
- **Repo**: https://github.com/DayuanJiang/next-ai-draw-io
- **What it does**: Web app + MCP for natural language → drawio XML; image replication; version history.
- **MCP**: `npx @next-ai-drawio/mcp-server@latest`
- **When to use**: Interactive editing or screenshot → diagram replication.

### Draw.io desktop (jgraph/drawio)
- **Repo**: https://github.com/jgraph/drawio
- **Export**:
  ```bash
  drawio --export --format png diagram.drawio
  drawio --export --format svg diagram.drawio
  ```

## Hand-drawn / Whiteboard

### Excalidraw
- **Repo**: https://github.com/excalidraw/excalidraw
- **When to use**: Workshop boards, sketchy exploration, teaching whiteboards.
- **archviz path**: emit `.excalidraw` JSON or Excalidraw Markdown when user asks 手绘/白板; promote to Mermaid/draw.io once structure stabilizes.
- **Restraint**: still max-1-accent, short labels; no rainbow stickies.

## Multi-Engine Skills

### markdown-viewer/skills
- **Repo**: https://github.com/markdown-viewer/skills
- **Engines**: Vega-Lite, Mermaid, PlantUML, D2, Excalidraw.
- **When**: Mermaid chart types too limited; need Vega-Lite transforms.

### Lucidchart alternatives
- **Topic**: https://github.com/topics/diagram
- Discovery only. Prefer file formats agents can write (`.mmd`, `.drawio`, `.excalidraw`, self-contained HTML).

## Decision Matrix (compact)

| Need | Tool | archviz handles? |
|---|---|---|
| Diagram in .md | Mermaid (inline) | ✅ Primary |
| Terminal preview | termaid | ⚠️ Prefer termaid |
| 27 editorial type pick | structural-diagram-types map | ✅ Routing |
| Professional editable export | draw.io | ⚠️ Mode doc + CLI |
| Interactive draw.io MCP | next-ai-draw-io | ❌ Hand off MCP |
| Sketch whiteboard | Excalidraw | ⚠️ On request |
| Complex data charts | HTML / Python / Vega-Lite | ✅ HTML+Python |
| 3D archviz | archviz-3d | ✅ Separate skill |
| Editorial cards | HTML self-contained | ✅ templates/html |

Last updated: 2026-07-21
