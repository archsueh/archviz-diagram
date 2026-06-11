# archviz-skills

<img width="1568" height="907" alt="68747470733a2f2f69696c692e696f2f664c45575435782e706e67" src="https://github.com/user-attachments/assets/19051e35-7745-4cd8-bb8e-b97a45e999b0" />

Restrained information visualization skill pack for AI agents.

Every visualization starts with a **brief read** and **three dials** — not a default template.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-0.0.4-blue.svg)

---

## What this is

A skill for AI agents (Claude Code, Hermes, Codex, etc.) that generates **rational, minimalist, restrained visualizations**. Not just Mermaid — supports ASCII, self-contained HTML, and Python output modes.

**Core principles:**
- Brief-first, anti-slop
- Text-first, preview-compatible
- One accent max, contrast-checked
- Environment-aware (Obsidian / terminal / deliverables)

---

## Quick start

```bash
git clone https://github.com/archsueh/archviz-skills.git
cp -r archviz-skills ~/.claude/skills/
```

---

## Structure

```
archviz-skills/
├── SKILL.md              # Execution workflow (244 lines)
├── DESIGN.md             # Design system (117 lines)
├── README.md             # This file
├── CONTRIBUTING.md       # Contribution guide
├── CHANGELOG.md          # Version history
├── LICENSE               # MIT
├── templates/
│   ├── mermaid/          # 11 .mmd templates
│   ├── ascii/            # 4 .txt templates
│   ├── html/             # 4 .html templates
│   └── python/           # 2 .py templates
├── examples/
│   ├── mermaid-demo.md   # 3 Mermaid diagrams
│   ├── ascii-demo.txt    # ASCII flowchart + gantt
│   ├── html-demo.html    # Self-contained bar chart
│   └── python-demo.py    # Plotly scatter + line
├── references/           # Detailed rules (gantt, style, validation)
└── research/             # Visualization taxonomy research
```

---

## Templates

| Category | Count | Types |
|---|---|---|
| Mermaid | 11 | flowchart, mindmap, gantt, sankey, distribution, diverging-bar, network, architecture, scoring, intro, closed-loop |
| ASCII | 4 | flowchart, architecture, gantt, icon-system |
| HTML | 12 | bubble, bullet-graph, funnel, gauge, heatmap, line, radar, sunburst, treemap, waffle, waterfall, self-contained |
| Python | 5 | scatter-plot, box-plot, candlestick, parallel-coordinates, viz template |

---

## Design system

See [DESIGN.md](DESIGN.md) for:
- Token system (5 palette presets)
- Contrast rule (luminance-based)
- Typography hierarchy (越大越细)
- Visualization taxonomy (Few + Shneiderman)
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
