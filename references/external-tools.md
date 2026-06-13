# External Tools Reference

Tools from the broader diagram ecosystem that complement archviz-skills.

## Terminal Rendering

### termaid
- **Repo**: https://github.com/fasouto/termaid
- **Install**: `pip install termaid`
- **Usage**: `termaid diagram.mmd --theme mono` or `cat diagram.mmd | termaid`
- **What it does**: Pure Python Mermaid renderer for terminals. 18 diagram types, 6 color themes, ASCII fallback, terminal-width auto-fit.
- **When to use**: Instead of hand-crafting ASCII diagrams. `termaid` renders actual Mermaid syntax in the terminal — much higher fidelity than manual ASCII.
- **Integration point**: archviz-skills ASCII templates are for environments without termaid. When termaid is available, prefer it over manual ASCII.

## Diagram Generation (Draw.io)

### drawio-skill
- **Repo**: https://github.com/Agents365-ai/drawio-skill
- **What it does**: Generates .drawio XML, exports to PNG/SVG/PDF/JPG via draw.io CLI. 10,000+ shape library, self-check loop, style presets.
- **Key mechanism — Self-healing loop**: Generate → render PNG → read PNG with VLM → find overlaps/clipped labels → fix XML → re-render. Up to 5 rounds.
- **When to use**: When the diagram needs precise layout, branded shapes (AWS/GCP/Azure), or exportable images with embedded XML.
- **What archviz-skills borrows**: The self-healing pattern (generate → validate → fix → re-render) as a quality gate.

### next-ai-draw-io
- **Repo**: https://github.com/DayuanJiang/next-ai-draw-io
- **What it does**: Web app + MCP server for AI-powered draw.io diagrams. Natural language → drawio XML, image-based replication, version history.
- **MCP Server**: `npx @next-ai-drawio/mcp-server@latest`
- **Key mechanisms**:
  - Image → diagram replication (upload screenshot → AI recreates it)
  - VLM-based validation (screenshot → check → fix)
  - Animated connectors for better visualization
  - Version history with restore
- **When to use**: As an MCP tool for interactive diagram editing, or when you need to replicate an existing diagram from an image.

## Multi-Engine Skills

### markdown-viewer/skills
- **Repo**: https://github.com/markdown-viewer/skills
- **What it does**: 14 skills covering 5 rendering engines (Vega-Lite, Mermaid, PlantUML, D2, Excalidraw).
- **Key skill — Vega-Lite**: `vega-lite` code fence for data-driven charts (bar, line, scatter, heatmap, area, radar, word cloud). More powerful than Mermaid xychart-beta for complex data viz.
- **When to use**: When Mermaid's chart types are too limited and you need Vega-Lite's data transformation capabilities.

## Decision Matrix

| Need | Tool | archviz-skills handles? |
|---|---|---|
| Diagram in .md | Mermaid (inline) | ✅ Primary |
| Terminal preview | termaid | ⚠️ Recommend termaid |
| Professional export (PNG/SVG/PDF) | drawio-skill | ❌ Out of scope → drawio |
| Interactive editing | next-ai-draw-io MCP | ❌ Out of scope → MCP |
| Complex data charts | Vega-Lite | ⚠️ Consider for future |
| 3D archviz | Three.js (inline HTML) | ✅ templates/html/ |
| Editorial cards | HTML (self-contained) | ✅ templates/html/ |
