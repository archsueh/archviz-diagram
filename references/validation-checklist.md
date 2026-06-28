# Validation Checklist (merged from fireworks-tech-graph, gm-data-chart, archviz-skills)

## Pre-Generation (MANDATORY)
- [ ] Full Diagram Brief + 4-layer analysis (Identity/System/Components/Layout) with confidence (✅/⚠️/❓).
- [ ] Dials set (Complexity/Density/Restraint) and documented.
- [ ] Type + Output Mode chosen (Mermaid primary; ASCII for Gantt/terminal; no default).
- [ ] Tokens locked: semantic names, hex values, one accent max, contrast rule checked.
- [ ] Labels short (≤6 words English / ≤8 Chinese chars), consistent language.
  - For Gantt/sequence/any source MD: strip <br/>, avoid long descriptive inside nodes/bars/participants (use codes or " / " separators).
- [ ] For Gantt: explicit time data, categories, milestones.
  - **Hard**: inside gantt block only ultra-short codes (V1.1 etc.); full names in immediate table below; ASCII fallback included.
- [ ] For Sankey: weighted flows, semantic edge labels.
- [ ] For custom flow (Sankey/map): edges/paths drawn before nodes; verified exact edge or perimeter attachment (no visual gaps/"断掉"). Test with reference image overlay if replicating (LLNL etc.).
- [ ] "Why" and design intervention visible.
- [ ] Matches existing document style/palette.
- [ ] If recurring concept: plan variation per DESIGN.md.
- [ ] Editorial: Family A/B/C/D chosen; G3 ask gate passed if ambiguous.
- [ ] Editorial: judgment + promise + one evidence (Family A); serif ≤500; no `#ffffff` canvas.

## Post-Generation
### Mermaid
- [ ] **Structure pre-check passes (MANDATORY, before claiming done):**
      `python3 scripts/validate-mermaid.py <file.md|file.mmd>` — exit 0.
      Catches orphan `end`, unbalanced subgraph/end, tokens glued to `end`
      (`]end`), and broken/unterminated ```mermaid fences. These are the
      recurring "Syntax error in text" failures a render-only check misses.
- [ ] **Subgraph ID 纯 ASCII（MANDATORY）**：所有 subgraph 标题若含中文或空格，
      必须用 `subgraph id["标签文字"]` 格式。直接写 `subgraph 中文名` 或
      `subgraph name with spaces` 在 Mermaid 11.x 报 `got 'UNICODE_TEXT'`。
      搜索文件中所有 `subgraph `，确认 id 段无空格无汉字。
- [ ] **节点文字不溢出**：单行 ≤12 汉字 / ≤20 英文字符；超长用 `\n` 分行，
      每行 ≤10 汉字；Gantt bar 内只用代码（V1.1 等），全名放旁表。
- [ ] Renders cleanly in target (Obsidian, GitHub, Mermaid live editor).
- [ ] No syntax errors.

### ASCII
- [ ] Columns aligned in mono font.
- [ ] No wrapping in 80 columns.
- [ ] Legend clear.

### SVG / Hybrid (if rendered via pretty-mermaid or external)
- [ ] Syntax valid (rsvg-convert or equivalent passes).
- [ ] No arrow-node collisions, text overflows, or overlaps.
- [ ] Arrow labels have background rects (opacity 0.95).
- [ ] Legend present if >2 arrow types.
- [ ] Visual self-review (if images readable): clean routing, sufficient spacing, readable text (>=11px, good contrast).
## 3D post-gen}: CDN imports resolve? Console clean? Resize works? Camera limits set? Touch/mobile tested?

## Educational Flat (Demo Section)

- [ ] Brief follows Educational Flat contract (reference/educational-flat-system.md)
- [ ] Background: `#ffffff`, text: `#000000`, border: `#000000`
- [ ] Only ONE ramp hue used; hierarchy via lightness within that ramp
- [ ] Font system: system-ui / PingFang SC / Noto Sans SC
- [ ] No gradients, no shadows, no glassmorphism, no decorations
- [ ] Legend included when >1 edge type is used
- [ ] No diagrams are academic

---







## Error Recovery
- Syntax fail: Simplify or switch type/mode.
- Visual issues: Widen gutters, add jump-over arcs (for SVG), background rects, or use ASCII.
- Generic look: Re-run brief; enforce variation.
- Always document confidence and cite exact values.

## Quality (from anydesign/gm)
- Cite hex/px/specifics.
- Infer semantic roles.
- Never invent tokens or assume palette.
- Self-contained for papers (caption first = finding).

Run this before shipping any diagram.

## Export & Theme (Phase 1 — HTML templates only)
- [ ] Template includes `_archviz-theme.html` (CSS vars + toggle button)
- [ ] Template includes `_archviz-export.html` (export menu + keyboard shortcuts)
- [ ] All hardcoded hex replaced with `--av-*` CSS variables
- [ ] `class="archviz-export-target"` on main chart/canvas element
- [ ] Canvas charts listen for `archviz-theme-changed` event and redraw
- [ ] T key cycles through 4 palettes (visual change confirmed)
- [ ] E→P exports PNG at 4× resolution (text sharp, no pixelation)
- [ ] E→S exports SVG with current theme vars injected
- [ ] E→C copies to clipboard (or logs fallback)
- [ ] `prefers-color-scheme: dark` auto-applies IKB Dark palette
- [ ] Export matches current theme (dark export = dark colors)
- [ ] File header: `<!-- archviz-skills upgrade Phase 1 | 2026-06-13 -->`