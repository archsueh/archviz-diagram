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

## 2026-09-30 session (theme header comment + hardcoded palette count)

- **`sync_theme.py` 的锚点是 `<style id="archviz-theme-vars">`** → 紧贴它**上面**那行 `<!-- Provides: ... -->` 头注释**不在被同步的块内**。改 partial 里的注释**不会**传播到模板，必须逐文件改（当时 5 处各存一份副本）。推论：**任何会漂的信息都不该写进这行注释**。
- **调色板数量别写死**：`toggleTheme()` 的 `order` 数组当时有 **11** 项，而 `DESIGN.md`、`references/validation-checklist.md` 与 5 处头注释都写着 **4**（数字停在只有 4 套的年代，此后无人发现）。要说数量就写「见 `ARCHVIZ_PALETTES` 注册表」，不要给数。
- **`scripts/sync_*.py --help` 会真的执行同步**（没有 argparse）—— 想「看用法」会直接改盘上 18 个模板。补救路径：`prettier --write` 之后 `git diff --exit-code` 应回到 0；2026-09-30 复验该不动点成立。
- **a11y 契约对 canvas 模板结构性跳过**：`self_check.py --all` 对 **22 个模板中的 15 个**报「文档里没有 `<svg>`，跳过无障碍检查」——它们用 `<canvas>`，而 `accessibility-contract.md` 的 R1–R6 全是 `<svg>` 专属。契约在这 ~68% 的模板上是空转的（**未修**，属设计决策）。

## 2026-10-08 session (constitution 修正案 + 决策记录机制)

- **「计数别写死」这条教训此前没泛化 —— 写 ADR 时又踩了一次。** 初稿写「其余 **13** 类图表」，跑 `archviz_diagram_list_types` 实测 **14** 类（stacked-bar / area-chart / line-chart / sunburst / treemap / radar / funnel / gauge / heatmap / bubble / waffle / waterfall / bullet-graph / editorial-card）。这与上面 §2026-09-30 的「调色板数量别写死」（11 写成 4）**同型**。**纪律**：任何要写进文档的计数，落笔前跑一次命令取真值；取不到就写「见 XXX 注册表」，不要给数。**数字没有「大概对」这回事。**

- **行号引用 = 可验证声明。** ADR 里引了 8 处行号（constitution L13/L14/L43/L52；SKILL.md L530/L531/L532/L540/L543/L557），逐条 `Read` 确认后才落笔。**别从摘要/记忆里抄行号** —— 抄错即失据，且比不引更糟（读者会以为核过了）。

- **本仓曾有一个结构性缺口：没有决策记录载体。** `docs/` 下长期只有空的 `screenshots/`。后果是「原则 vs 实现」的冲突**只能活在 CHANGELOG 注记里**（如 §0.6.0 Notes 那条 Principle III 张力），而 CHANGELOG 是版本作用域的 —— 新版本一压上去就滚出视野，**代码路径却还在**。已于本次建 `docs/decisions/`（格式与状态流转见该目录 README）。**推论：任何「已识别未擅改」的张力，都不该只留 CHANGELOG 注记 —— 要么修，要么立 ADR。**

- **修宪的判据优于修宪的例外。** Principle III 原文已含 `reserved for deliverables that earn them` —— **缺的是「earn」的定义，不是例外本身**。给判据（三条：显式门禁 / 声明非文本终态 / 降级路径）后，现有 Paper Framework Mode 逐条核过全部符合，**零行为变更**。反面做法是写成「文本优先，Paper Framework Mode 除外」—— 命名实例而非给判据，下一个同类模式还得再修一次宪。**这与「版本号硬编码在 4 处」同型。**

- **`constitution.md` 的 Governance 要求修正案四项齐备**（显式记录变更 / 改 constitution / 同步 gotchas·SKILL·DESIGN / breaking 时补迁移说明）。本次逐条对账落在 ADR-001 末节表格里。**注意第 ③ 项要真去找**：`DESIGN.md` §1 也断言了 text-first，差点漏掉 —— 用 `grep -niE "text-first|plain text|文本优先"` 扫一遍比凭印象可靠。
