# WebGL / HTML for Interactive Information Architecture (archviz 2D focus)

WebGL (via lightweight Canvas + Three.js CDN overlay where useful) is highly suitable for information architecture in 2D info viz outputs.

## Why it fits archviz
- Interactive exploration of complex relationships (clickable nodes, hover details, animated flows, filtering)
- Maintains the restrained, exportable nature of self-contained HTML
- Static fallback always available via _archviz-export (4x raster PNG/SVG)
- Perfect for architecture diagrams, dependency networks, layered systems, decision flows that benefit from user-driven navigation

## Implementation Rules (restraint + quality)
- Base layer always clean SVG or 2D Canvas for core structure (guaranteed crisp export)
- WebGL/Three overlay only for interaction (camera controls limited to 2D pan/zoom/rotate in plane, or simple 2.5D)
- No heavy 3D models or realistic rendering — those go to archviz-3d
- Theme integration: colors from _archviz-theme (Warm Paper / Swiss / Editorial palettes)
- Performance: dpr capped at 2, frustum culling if using Three, simple geometries
- Accessibility: full keyboard + screen-reader fallback to static SVG version
- Export menu: "Static PNG (4x)", "Interactive HTML", "SVG (vector)"

## Example Use Cases in 2D Info Viz
- Force-directed graph for dependency networks (from mermaid network.mmd data)
- Layered architecture with clickable layers revealing details
- Sankey or flow with time-scrub animation and node selection
- Decision matrix with interactive weighting sliders
- Multi-level system map with zoomable sub-systems

## File Pattern
Extend templates/html/ with webgl-info-viz.html (already added as base).
Load data from the same structured sources used for static versions (JSON/Mermaid data).

## Gotchas
- Overusing 3D perspective in 2D info viz breaks restraint — keep perspective subtle or flat
- Interaction must not be required for core understanding (always have static view)
- Mobile: simplify interactions, larger hit areas
- Export consistency: test that the "static" render matches the visual hierarchy of the interactive state

This makes archviz outputs more powerful for teaching, documentation, and presentations while staying true to the restrained, high-quality, self-contained philosophy.

See templates/html/webgl-info-viz.html for the starting implementation (Canvas + simple interaction, ready to extend with Three.js for more complex graphs).
