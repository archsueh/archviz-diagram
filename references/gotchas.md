# Gotchas (Highest Value Content — 2D Info Viz)

## Restraint & Tokens
- 模型爱加紫色渐变/emoji/大 blur：SKILL.md 硬性负面 + 模板里只暴露已验证 token 列表。
- Warm Paper / Editorial Parchment 表面上用 Mist White 文字会对比失败：永远先算 luminance。

## Export
- 4x raster 时字体 fallback 模糊：强制 JetBrains Mono 或系统等宽 + canvas 2x 预渲染测试。
- SVG 双主题 @media 在 GitHub sanitizer 下常被 strip：同时提供 light/dark 独立导出或宿主注入变量方案。

## 2D Specific
- Sankey/flowchart 节点太多 (>50)：策略阶段必须 split 或 aggregate "Other"。
- Gantt 文字溢出：代码只进 block，完整名必须有旁表 + ASCII fallback。
- 卡片类 (editorial) 文字层 >3：Family A 必须压缩到 judgment + promise + one evidence。

**追加规则**：每次真实交付后至少 +1 条。优先负面边界。

## 2026-06 session (Energy Sankey + Migration Map consolidation)
- Exact reference replication (LLNL Sankey): flows/paths MUST be drawn first in SVG, then nodes/rects/circles on top to cover endpoints cleanly. Compute attach at literal edge (rect right = x+width; circle = cx ± r * cos/sin). Tune Q bezier controls to match reference S-curves/merges. Symptom of failure: "节点都断掉了". Replicate structure 1:1; no creative layout changes unless asked.
- Color "low" feedback loop: user says "配色有点low" → iterate to deeper controlled tones from DESIGN chart variants (deep green #134e2a, teal #0c617a, burgundy #6f1a1a, wine #5c1f2e, amber #92400e, warm-ink gray #57534e). Stop only when "你的颜色倒是越来越对了". Avoid any high-chroma primaries or rainbow; max one semantic hue family per role + luminance contrast.
- Viz attempt proliferation + convergence: multiple files for same/similar brief (energy-sankey, migration-map, workspace "sankey"/choropleth, different palettes) will trigger explicit "三个结合一下 我只需要一个版本 其余帮我清理掉". Converge proactively to ONE canonical self-contained Swiss HTML; keep only the best attachment/style/data synthesis.
- Mermaid 10.x incompatibility for custom flows: experimental sankey syntax or precise edge attachment often breaks in bundled renderers (Obsidian ~10.9.6 "Syntax error"). Default to pure self-contained SVG + JS (paths + perimeter math) for any diagram needing reliable node-edge connection. Retain .mmd only as text-first fallback.
- Combined multi-viz page pattern: Sankey + interactive geo-flow map (or similar) in single restrained Swiss container (shared Warm Paper tokens, one header/legend/footer, section titles, generous whitespace) produces high-signal deliverable. See examples/us-flows.html. Prefer this over separate files when user wants "both".
- Workspace temp hygiene: .hermes/workspace/* files are transient. On explicit "清理掉" of listed artifacts, rm -f them immediately (they are not part of permanent examples/). Do not leave orphans.

## 2026-06-24 session (Mermaid subgraph ID + node text overflow)
- **Subgraph ID 不能含中文或空格**：`subgraph Obsidian 知识库 cognitive-kernel` → parser 报 `got 'UNICODE_TEXT'`（Mermaid 11.x）。**强制写法**：`subgraph kb["Obsidian 知识库 · cognitive-kernel"]`——id 纯 ASCII，显示文字放 `["..."]` 引号里。所有含中文或空格的 subgraph 标题必须用此格式，无例外。
- **Mermaid 节点文字溢出**：`[长中文\n长中文]` 在 Obsidian 渲染时节点宽度固定，文字不换行只截断。对策：单行 ≤12 汉字；超长描述用 `\n` 分行且每行 ≤10 汉字；或改用旁注表格代替节点内嵌文字。Gantt bar 内文字同理（bar 太窄时 label 完全消失），已有规则见上方 Gantt 条目。
- **validate-mermaid.py 不捕获此类错误**：脚本只查结构（subgraph/end 平衡、fence 完整性），不做词法校验。中文 subgraph ID 的报错只有渲染时才出现。目前无自动检测方案，依赖 Pre-Generation 人工 checklist 规则（见 validation-checklist.md）。

## 2026-06-14 session (Mermaid structural pre-flight)
- Recurring "Syntax error in text" in shipped Mermaid (e.g. `... --> F3[label]end` / `got 'end'`) is almost always a STRUCTURE defect, not a grammar one: an orphan `end` (no open subgraph), an unbalanced subgraph/end count, a token glued to `end` (`]end` with no newline), or a broken/unterminated ```mermaid fence. A "renders cleanly" eyeball check misses these until the doc renders.
- Fix: run `python3 scripts/validate-mermaid.py <file.md|file.mmd>` (exit 0 required) BEFORE claiming a Mermaid diagram done. It is a grammar-agnostic structure check — does not replace rendering, stops the cheap mistakes early. Now MANDATORY in validation-checklist.md → Post-Generation → Mermaid.
- Note: a stray `end` often survives hand-edits of generated blocks. The subgraph may already be closed mid-block; a second `end` at the tail is the classic orphan. Count opens vs closes, not just "looks fine".
