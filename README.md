# archviz-skills



Restrained information visualization skill pack for AI agents.

Every visualization starts with a **brief read** and **three dials** — not a default template.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-0.0.9-blue.svg)

---

## What this is

A skill for AI agents (Claude Code, Hermes, Codex, etc.) that generates **rational, minimalist, restrained visualizations**. Not just Mermaid — supports ASCII, self-contained HTML, Python (Plotly), and Three.js 3D archviz.

## Design philosophy

`archviz-skills` treats every diagram as a small **DESIGN.md artifact**: a plain-text design contract that an agent can read, execute, and audit. The goal is not to make diagrams prettier by default; the goal is to make their visual language explicit enough that another agent can reproduce the same taste without guessing.

Every output should expose five things:

| Layer | What it answers | Required evidence |
|---|---|---|
| Atmosphere | What should this feel like? | Palette + density + restraint |
| Tokens | What exact values are allowed? | Hex values, line weights, type scale |
| Components | What recurring pieces exist? | Nodes, arrows, legends, labels |
| Layout | How does information collapse? | Direction, caps, fallbacks |
| Guardrails | What must never happen? | Anti-patterns + validation gates |

This is adapted from the `awesome-design-md` pattern: `DESIGN.md` is the visual truth source, `SKILL.md` is the execution protocol, and examples prove the contract works.

**Core principles:**
- Brief-first, anti-slop
- Text-first, preview-compatible
- One accent max, contrast-checked
- Environment-aware (Obsidian / terminal / deliverables / 3D)
- Design-contract first: no template ships without tokens, intent, constraints, and validation notes

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
├── DESIGN.md             # Design system, Stitch 9-section format (+ Extended: taxonomy, Aver, 3D)
├── preview.html          # Visual catalog: palettes, type scale, node/edge styles
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

[DESIGN.md](DESIGN.md) follows the Stitch DESIGN.md 9-section format (per [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)):

1. Visual Theme & Atmosphere (+ Agent-Readable Contract)
2. Color Palette & Roles — semantic names + hex + role, 5 palette systems, luminance contrast gate
3. Typography Rules (越大越细 hierarchy)
4. Component Stylings — nodes, edges, groups, gantt, tables, Mermaid init
5. Layout Principles — three dials + whitespace philosophy
6. Depth & Elevation — flat by doctrine
7. Do's and Don'ts
8. Responsive Behavior + degradation strategy
9. Agent Prompt Guide — quick color reference + ready-to-use prompts

Extended sections: visualization taxonomy (Few + Shneiderman), Aver signature patterns, 3D archviz (Three.js + animejs), validation gates.

[preview.html](preview.html) is the visual catalog (swatches, type scale, node/edge vocabulary) — open it in a browser.

---

## Related

- [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) — Official Mermaid
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) — 10.3k stars
- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) — Swiss PPT
- [anydesign](https://github.com/archsueh/anydesign) — Design analysis

---

## License

MIT
