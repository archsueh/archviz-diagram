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
