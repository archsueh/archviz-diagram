# archviz-skills



Restrained information visualization skill pack for AI agents.

Every visualization starts with a **brief read** and **three dials** — not a default template.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-0.0.7-blue.svg)

---

## What this is

A skill for AI agents (Claude Code, Hermes, Codex, etc.) that generates **rational, minimalist, restrained visualizations**. Not just Mermaid — supports ASCII, self-contained HTML, Python (Plotly), and Three.js 3D archviz.

**Core principles:**
- Brief-first, anti-slop
- Text-first, preview-compatible
- One accent max, contrast-checked
- Environment-aware (Obsidian / terminal / deliverables / 3D)

**Mode routing:**
- **Default (2D infoviz)** — charts, flowcharts, gantt, sankey, tables, teaching diagrams
- **3D archviz** — only when the brief mentions building, floorplan, structure, section cut, or walkthrough (`templates/html/threejs-*.html`)

---

## Quick start

```bash
git clone https://github.com/archsueh/archviz-skills.git
# Claude Code / Codex
cp -r archviz-skills ~/.claude/skills/
# Hermes Agent
cp -r archviz-skills ~/.hermes/skills/creative/archviz-skills
```

---

## Structure

```
archviz-skills/
├── SKILL.md              # Execution workflow + anti-patterns
├── agents/openai.yaml    # Codex UI metadata
├── DESIGN.md             # Design system + visualization taxonomy (+ §3D)
├── README.md             # This file
├── CONTRIBUTING.md       # Contribution guide
├── CHANGELOG.md          # Version history
├── LICENSE               # MIT
├── templates/
│   ├── mermaid/          # 15 .mmd templates
│   ├── ascii/            # 4 .txt templates
│   ├── html/             # 14 .html templates (incl. threejs-archviz)
│   └── python/           # 5 .py templates
├── examples/
│   ├── mermaid-demo.md   # Mermaid bar + flow + gantt
│   ├── teaching-building-3d.html  # 4-floor building walkthrough
│   ├── course-admission-flow.mmd  # Teaching funnel
│   └── python-demo.py    # Plotly scatter + line
├── references/           # Detailed rules (gantt, style, validation)
└── research/             # Visualization taxonomy research
```

---

## Templates

| Category | Count | Types |
|---|---|---|
| Mermaid | 15 | gantt, sankey, distribution, diverging-bar, network, architecture, scoring, intro, closed-loop, funnel, decision-matrix, state-machine, dependency-network |
| ASCII | 4 | flowchart, architecture, gantt, icon-system |
| HTML | 14 | bubble, bullet-graph, funnel, gauge, heatmap, line, radar, sunburst, treemap, waffle, waterfall, self-contained, threejs-archviz, threejs-floorplan |
| Python | 5 | scatter-plot, box-plot, candlestick, parallel-coordinates, viz template |

---

## Design system

See [DESIGN.md](DESIGN.md) for:
- Token system (5 palette presets)
- Contrast rule (luminance-based)
- Typography hierarchy (越大越细)
- Visualization taxonomy (Few + Shneiderman)
- 3D architectural visualization (Three.js + animejs)
- Anti-homogenization rules

---

## Related

- [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) — Official Mermaid
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) — 10.3k stars
- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) — Swiss PPT
- [anydesign](https://github.com/archsueh/anydesign) — Design analysis

---

## License

MIT
