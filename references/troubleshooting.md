# 13. TROUBLESHOOTING

> 从 `SKILL.md` 原样迁出（2026-09-23 渐进式披露拆分），内容未删改。
> 何时加载：按症状查表（渲染空白、字体回退、导出失败、Mermaid 不兼容）。**只在报错时加载**。

## 13. TROUBLESHOOTING

| Issue | Fix |
|---|---|
| Editorial wrong palette | Host doc wins; else Editorial Parchment `#f5f4ed` + Terracotta `#c96442` — never mix with IKB |
| Cover too dense | Family A: drop to judgment + promise + one evidence; move rest to Family B |
| Card needs PNG export | Built-in: press E→P for 4× raster PNG, E→S for SVG, E→C for clipboard. See §Export System. |
| Mindmap fails | Use flowchart/subgraph |
| Architecture-beta lexer error | Use flowchart TD + subgraph (preview-compatible) |
| Mermaid trailing end error | Never close graph/flowchart TD blocks with end; only subgraph blocks require end |
| Gantt text overflow | Codes only + table + ASCII fallback |
| Theme too flashy | Force solarized-light/nord-light |
| Text unreadable | Check contrast rule (QR) |
| Too many nodes | Split into subgraphs |
| Canvas blank (Three.js) | Check console for CDN 404 / import errors |
| animejs not animating | v4 API: `animate(target, props)` not `anime({targets})` |
| Render loop stops | Don't name loop function `animate` (conflicts with animejs import) |
| Custom flow nodes "断掉" / bad attach | Paths drawn after nodes or wrong endpoint math | Draw all flow <path> first, then <rect>/<circle> on top. Compute attach = center ± (half-size or r) * unit vector from angle. See examples/us-flows.html + gotchas. |
| Multiple viz files for same data | User eventually demands "combine into one + clean the rest" | Converge early to single canonical Swiss HTML (shared tokens, one container). Pure attachment + restrained color from energy iteration. |
| Grid overlay drifts (viewport shift) | Content-box alignment mismatch | Place `.guides` overlay in the SAME container box as the centered content, sharing margins and templates (see `references/swiss-modernist-grid.md`) |
| CJK text side-bearing offset | Display letters look slightly indented | Implement browser optical alignment to nudge display elements using canvas measurements |
| Headless Helvetica rendering fallback | System lacks real font, fallback to Arial/Noto | Prioritize `Liberation Sans` in the CSS font stack to preserve metric-compatible grotesque spacing, or embed the webfont directly |

---
