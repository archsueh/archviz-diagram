
# archviz-diagram

Restrained flowcharts and framework diagrams (流程图与框架图) visualization skill pack for AI agents.

Every diagram starts with a **brief read** and **three dials** — not a default template.

> **3D spatial visualization** has been split into [archviz-3d](https://github.com/archsueh/archviz-3d).

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-0.5.3-blue.svg)

<img width="2298" height="3334" alt="screenshot-archviz-skills — Design System Preview" src="https://github.com/user-attachments/assets/f6369781-f056-41f0-be0f-658d38cadc37" />
<img width="2298" height="2838" alt="screenshot-Independent Music Revenue Flow — Müller-Brockmann Grid" src="https://github.com/user-attachments/assets/ed4c5306-fc7d-45b2-b493-55efe255d0db" />

## Screenshot Material

<img width="1280" height="633" alt="hair-dryer-exploded" src="https://github.com/user-attachments/assets/9ed240f9-81bc-4ef5-8823-550f080b974c" />
<img width="1280" height="633" alt="hair-dryer-assembled" src="https://github.com/user-attachments/assets/9793fe6a-1832-442d-a1b7-20e2e1526c64" />

Open the complete screenshot sheet:
[examples/git-push-release-workflow.html](examples/git-push-release-workflow.html)

Self-contained HTML screenshot sheet with Wes Anderson palette, command table, and Mermaid source. Open in a browser, enter full screen, and capture the final visual.

Mermaid source:
[examples/git-push-release-workflow.mmd](examples/git-push-release-workflow.mmd)

---

## What this is

A skill for AI agents (Claude Code, Hermes, Codex, etc.) that generates **rational, minimalist, restrained flowcharts and framework diagrams (流程图与框架图)**. Not just Mermaid — supports ASCII/termaid terminal rendering, self-contained HTML, Python (Plotly), Obsidian Canvas, draw.io handoff guidance, and Three.js 3D archviz.

## Design philosophy

`archviz-diagram-skills` treats every diagram as a small **DESIGN.md artifact**: a plain-text design contract that an agent can read, execute, and audit. The goal is not to make diagrams prettier by default; the goal is to make their visual language explicit enough that another agent can reproduce the same taste without guessing.

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
- Editable-handoff aware (`.drawio` guidance when Mermaid is not enough)
- Design-contract first: no template ships without tokens, intent, constraints, and validation notes

**Mode routing:**
- **Default (Flowcharts & Framework Diagrams)** — process flows, system architectures, conceptual models, state machines, relationship matrices, organizational diagrams
- **3D archviz** — only when the brief mentions building, floorplan, structure, section cut, or walkthrough → [archviz-3d](https://github.com/archsueh/archviz-3d)
- **Editable handoff** — draw.io when the diagram must keep being edited by humans (`references/drawio-output-mode.md`)
- **Sketch / workshop** — Excalidraw; promote to Mermaid once structure stabilizes
- **Engine + 27-type map** — `references/ecosystem-routing.md` · `references/structural-diagram-types.md`
- **Brand gate** — host DESIGN.md / preset before default skin (`references/brand-gate.md`)
- **Excalidraw sketch** — `templates/excalidraw/` then promote to Mermaid

---

## Quick start

```bash
git clone https://github.com/archsueh/archviz-diagram.git
# Claude Code / Codex
cp -r archviz-diagram ~/.claude/skills/archviz-diagram
# Hermes Agent
cp -r archviz-diagram ~/.hermes/skills/creative/archviz-diagram
```

---

## Structure

```
archviz-diagram/
├── SKILL.md              # Execution workflow + anti-patterns
├── DESIGN.md             # Design system, Stitch 9-section format (+ Extended: taxonomy, Aver, 3D)
├── preview.html          # Visual catalog: palettes, type scale, node/edge styles
├── README.md             # This file
├── CONTRIBUTING.md       # Contribution guide
├── CHANGELOG.md          # Version history
├── LICENSE               # MIT
├── templates/
│   ├── mermaid/          # 15 .mmd templates
│   ├── ascii/            # 4 .txt templates
│   ├── html/             # 21 .html templates (incl. threejs-archviz)
│   ├── python/           # 5 .py templates
│   ├── canvas/           # 2 canvas handoff templates
│   ├── obsidian-canvas/  # 3 Obsidian Canvas templates
│   └── excalidraw/       # 1 Excalidraw template
├── examples/
│   ├── git-push-release-workflow.html  # **图文并茂截图素材**（Wes Anderson 配色，自包含 HTML，直接打开截图）
│   ├── git-push-release-workflow.mmd   # 图文并茂 git push 发布流程 (Wes Anderson variant)
│   ├── mermaid-demo.md                 # Mermaid bar + flow + gantt
│   ├── teaching-building-3d.html       # 4-floor building walkthrough
│   ├── course-admission-flow.mmd       # Teaching funnel
│   └── python-demo.py                  # Plotly scatter + line
└── references/           # Detailed rules (gantt, style, validation, draw.io, terminal routing)
```

---

## Templates

| Category | Count | Types |
|---|---|---|
| Mermaid | 15 | gantt, sankey, distribution, diverging-bar, network, architecture, scoring, intro, closed-loop, funnel, decision-matrix, state-machine, dependency-network |
| ASCII | 4 | flowchart, architecture, gantt, icon-system |
| HTML | 21 | bubble, bullet-graph, funnel, gauge, heatmap, line, radar, sunburst, treemap, waffle, waterfall, self-contained, threejs-archviz, threejs-floorplan, plus advanced chart templates |
| Python | 5 | scatter-plot, box-plot, candlestick, parallel-coordinates, viz template |
| Canvas | 6 | canvas, Obsidian Canvas, Excalidraw handoff templates |

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

Extended sections: visualization taxonomy (Few + Shneiderman), Aver signature patterns, 3D archviz (Three.js + animejs), draw.io handoff rules, terminal routing, scene contracts, validation gates.

[preview.html](preview.html) is the visual catalog (swatches, type scale, node/edge vocabulary) — open it in a browser.

---

## Related

### Core dependencies
- [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) — Official Mermaid
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) — 10.3k stars
- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) — Swiss PPT
- [anydesign](https://github.com/archsueh/anydesign) — Design analysis

---

## License

MIT
