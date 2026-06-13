# archviz Constitution

<!-- Ratified based on DESIGN.md + SKILL.md + real session experience (2026-06 Energy Sankey + Migration consolidation) -->

## Core Principles

### I. Restraint as Dial, Not Default
Every visualization begins with a brief read + three explicit dials (COMPLEXITY / DENSITY / RESTRAINT, 1-10). Default academic: 4/3/8. Never ship on unexamined default theme, purple gradients, rainbow nodes, or centered symmetry. Restraint is the signature: structure carries the argument; decoration is absent by policy.

### II. Text-First Survivability + Earned Self-Contained Deliverables
Primary artifact is always plain text (.mmd, ASCII, or structured data) that survives Obsidian, GitHub, terminal, and diffs. HTML, Python (Plotly), or 3D (Three.js) are reserved for deliverables that earn them. Self-contained HTML (zero external deps except verified minimal CDN) is the standard for custom flows, precise attachment, or combined multi-viz pages.

### III. Exact Fidelity for Reference Replication & Flow Attachment
When replicating reference structure (e.g. LLNL Sankey image):
- Draw all flow paths/edges FIRST in SVG order, then nodes (rects/circles) on top to cleanly cover endpoints.
- Compute attach points at literal edge/perimeter: rect right-edge = left_x + width; circle = cx ± r * unit_vector (cos/sin from angle).
- Tune bezier Q controls to match reference S-curves and merges exactly.
- No creative layout changes, added decoration, or "improvements" unless explicitly requested.
Failure mode: "节点都断掉了" (visually disconnected flows). Always document math and z-order in gotchas.

### IV. Color Restraint & User-Driven Iteration
Use DESIGN.md tokens exclusively (Warm Paper #f5f0eb surface, Ink Navy #1B365D text, Stone/Pebble borders, max ONE accent #002FA7). For semantic fills prefer deep controlled earth/slate/wine/amber families (#134e2a, #0c617a, #6f1a1a, #5c1f2e, #92400e, #57534e etc.). 
Respond to "配色有点low" by deepening and unifying hue families. Stop iteration only on explicit positive feedback ("你的颜色倒是越来越对了"). Luminance rule (0.299R+0.587G+0.114B) is mandatory for text contrast. Never pair light warm surfaces with near-white text.

### V. Single Artifact Convergence
When multiple visualization attempts exist for the same or related data (different Sankey/Map versions, energy vs migration, workspace temps), expect and proactively support user demand for "combine into one version + clean the rest". Deliver exactly ONE canonical self-contained Swiss-minimal HTML artifact with shared tokens, header/footer/credits, restrained palette, and clear sections. Do not leave duplicate or orphaned files in examples/ or workspace/.

### VI. Gotchas as Living Single Source of Truth (Highest Value)
After every real delivery or complex iteration, append at least +1 high-value entry to references/gotchas.md (prioritize negative boundaries and failure symptoms). This session's lessons (exact attachment math, color feedback loop, convergence, Mermaid vs pure HTML decision, combined pages, workspace hygiene, perimeter/edge patterns) are now permanent and must be consulted before generating similar work.

## Additional Constraints
- Full visual contract lives in DESIGN.md (tokens, typography "越大越细，越小越粗", layout, anti-slop, contrast rule, editorial families).
- Execution gates live in SKILL.md (G0 brief, G1 type, G2 tokens/contrast, G5 validation-checklist, G6 caption-first).
- Mixed types: never combine >2 in one diagram unless deliberate "combined page" demonstration (see Principle V and examples/us-flows.html). Split otherwise.
- Environment: Obsidian/GitHub → Mermaid or lightweight HTML; terminal → termaid + ASCII fallback; complex/custom attachment → pure self-contained HTML (bypasses Mermaid 10.x incompatibilities).
- No flexibility for unrequested config or future-proofing. Implement only current spec.
- For "optimize" requests: improve EXISTING content only. Never delete references, templates, or supporting files unless user explicitly says "删除"/"清理"/"remove".

## Development Workflow & Quality Gates (SDD Mandatory for Non-Trivial)
1. Constitution (this file) is the root truth. Update it first for any project-level change.
2. Brief + dials + DESIGN contract before any code.
3. Spec (user stories, Given-When-Then, edge cases, non-functional) → Plan (files, models, traceability) → Implement surgically.
4. Validation checklist (pre + post) + self-healing loop required.
5. Trace every diff back to spec/plan/constitution.
6. After delivery: +1 gotchas entry + update SKILL/DESIGN/examples/README as needed.
7. All PRs/reviews must verify compliance with this constitution.

## Governance
This constitution supersedes SKILL.md, DESIGN.md, templates, and all prior practices for archviz work. Amendments require: explicit documentation of the change + update to this file + corresponding gotchas/SKILL/DESIGN entries + (if breaking) migration notes. 

**Version**: 0.1 | **Ratified**: 2026-06-13 (post 2026-06 session consolidation of attachment, color, convergence, and HTML lessons) | **Last Amended**: 2026-06-13

All agents (Claude Code, Grok, Codex, Hermes, etc.) working on or with archviz must load and obey this constitution + the latest gotchas.md.