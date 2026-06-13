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
