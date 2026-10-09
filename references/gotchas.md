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
- **a11y 契约对无静态 `<svg>` 的产物结构性跳过**：`self_check.py --all templates/` 对 **22 个模板中的 20 个**报 `a11y.no_svg` —— 契约在这 91% 的模板上无从校验。
  - **旧记录（2026-09-30）此处有两处错，已更正**：① 数量写「15 个」，实测 **20 个**；② 归因写「它们用 `<canvas>`」，**假**。
  - **实测分布（2026-10-08）**：静态 `<canvas>` 元素 **2 个**（`waffle` / `webgl-info-viz`）、待内嵌片段 **4 个**（`_archviz-animated` / `_archviz-export` / `_archviz-theme` / `_flow-attach`）、**其余 14 个是完整文档但没有任何静态图形元素**（模板骨架，图形待生成）。
  - **2026-10-08 起由 INFO 改为 ADVISORY**（附残余风险、不阻塞、`--strict` 不提升），见 `accessibility-contract.md` §5。

## 2026-10-08 session (constitution 修正案 + 决策记录机制)

- **「计数别写死」这条教训此前没泛化 —— 写 ADR 时又踩了一次。** 初稿写「其余 **13** 类图表」，跑 `archviz_diagram_list_types` 实测 **14** 类（stacked-bar / area-chart / line-chart / sunburst / treemap / radar / funnel / gauge / heatmap / bubble / waffle / waterfall / bullet-graph / editorial-card）。这与上面 §2026-09-30 的「调色板数量别写死」（11 写成 4）**同型**。**纪律**：任何要写进文档的计数，落笔前跑一次命令取真值；取不到就写「见 XXX 注册表」，不要给数。**数字没有「大概对」这回事。**

- **行号引用 = 可验证声明。** ADR 里引了 8 处行号（constitution L13/L14/L43/L52；SKILL.md L530/L531/L532/L540/L543/L557），逐条 `Read` 确认后才落笔。**别从摘要/记忆里抄行号** —— 抄错即失据，且比不引更糟（读者会以为核过了）。

- **本仓曾有一个结构性缺口：没有决策记录载体。** `docs/` 下长期只有空的 `screenshots/`。后果是「原则 vs 实现」的冲突**只能活在 CHANGELOG 注记里**（如 §0.6.0 Notes 那条 Principle III 张力），而 CHANGELOG 是版本作用域的 —— 新版本一压上去就滚出视野，**代码路径却还在**。已于本次建 `docs/decisions/`（格式与状态流转见该目录 README）。**推论：任何「已识别未擅改」的张力，都不该只留 CHANGELOG 注记 —— 要么修，要么立 ADR。**

- **修宪的判据优于修宪的例外。** Principle III 原文已含 `reserved for deliverables that earn them` —— **缺的是「earn」的定义，不是例外本身**。给判据（三条：显式门禁 / 声明非文本终态 / 降级路径）后，现有 Paper Framework Mode 逐条核过全部符合，**零行为变更**。反面做法是写成「文本优先，Paper Framework Mode 除外」—— 命名实例而非给判据，下一个同类模式还得再修一次宪。**这与「版本号硬编码在 4 处」同型。**

- **`constitution.md` 的 Governance 要求修正案四项齐备**（显式记录变更 / 改 constitution / 同步 gotchas·SKILL·DESIGN / breaking 时补迁移说明）。本次逐条对账落在 ADR-001 末节表格里。**注意第 ③ 项要真去找**：`DESIGN.md` §1 也断言了 text-first，差点漏掉 —— 用 `grep -niE "text-first|plain text|文本优先"` 扫一遍比凭印象可靠。

## 2026-10-08 session（ADVISORY 等级 + 静态扫描的三个陷阱）

- **诊断不准比不报更糟 —— 本次同一处误诊了两次。** 给 `a11y.no_svg` 写 evidence 时，先写 `renderer=canvas`（因为 20/22 个原始文件含 `<canvas`）。实测才发现：**18 个的 `<canvas` 在 `<script>` 里**，而且多数根本不是元素 —— 是导出模块错误提示里的**字符串字面量**（`"give it an <svg> or <canvas> element to rasterize"`）。真实静态 `<canvas>` 元素只有 **2 个**。第二次改成 `non-svg` 仍不准，因为那 14 个是「完整文档但图形未生成」。
  **纪律：诊断类字段落笔前，逐项跑命令核；一次核不对就再核一次。** 一个指向不存在问题的诊断，比沉默更消耗信任。

- **静态扫描 vs 运行时构建 —— 这是本仓最容易踩的一类坑。** 模板里 `<svg>` 与 `<canvas>` 的**多数出现都在 JS 字符串里或由运行时创建**：`area-chart.html` 全文只有 1 处 `<svg`，在 `<script>` 内的字符串里；`grep -l "<canvas"` 数出 19/22，但剥掉 `<script>` 后只剩 2 个。**任何基于 `grep` 的静态统计，先确认命中的是元素还是字符串。** 判据：跑 `strip_script_bodies()` 后再数。

- **ADVISORY 的 evidence 必须写 `residual_risk`，不能只写理由。** 把「没做校验」说成「确认无害」就是粉饰。advisory 的正当性来自**披露**，不来自**宽免** —— 所以每条都要如实写下「因此失去了什么校验」。

- **advisory 与 WARN / baseline 的分界线必须由机器把住，写在文档里没用。** 三条不变量已进 `--self-test`：① 必须带 evidence；② `--strict` 也不得提升；③ 不得被基线吞掉。**第 ③ 条尤其重要**：baseline = 「未修的债务，先压住」，advisory = 「有意接受，本来就不该修」，两者后续处置完全不同，永不互换。代码里用 `WAIVABLE_LEVELS` 常量把这条声明一次，`write_baseline` 与 `apply_baseline` 共用。

- **`passed(strict)` 收成了单一真源。** 判定表达式 `not fails and not (strict and warns)` 原先在 `emit()` 与 JSON 分支里**各写了一遍** —— 加第四级时才发现，正好是「同一事实写在多处必然漂移」的现场（与版本号四处漂移、调色板数量写死同型）。**加等级时顺手查一遍：这个判定还有别处也在算吗？**

- **`advisories` 这个设计的出处要考证。** 我先前把它记成「anidiagram 文档里的概念」—— **错**。它在 anidiagram 里是**运行时质量报告的一个字段**（`{"issues": [...], "advisories": [...], "score": ...}`，`advisories` 不影响 `score`），文档里根本没提。**教训：引用外部实现的设计前必须回到原文核；「我在它的输出里见过」不等于「它文档里有这个概念」。** 二手摘要会把观察到的现象升格成设计原则。

- **`description` 是路由面，不是简介 —— 它决定 skill 会不会被加载。** 2026-10-09 实测：`description` 里 **0/14** 个 MCP 图表类型被点名。用户说「画个热力图」「画个瀑布图」「画个雷达图」时，agent 在加载 skill **之前**读的就是这段文本，里面没有这些词，就没有词法钩子。参考项目 `diagram-design` 的 ADR 0004 记录过同一起事故（他们删掉 27 个类型名后 CI 才拦住）。**纪律：`description` 必须点名注册表里的每一个类型（可用别名），这条优先于字节上限 —— 路由面永远不为正文让路。**

- **裸 `grep` 数字做计数校验会假阳性。** `references/structural-diagram-types.md` 有一行 `| 14 | Pyramid / funnel |`，那个 14 是**行序号**。任何 `grep "14"` 式校验都会把它当成「14 类图表」的断言。**所有计数断言必须用语义正则**（`27 类逐类型预算` / `Structural diagram types (27,`），不能只匹配数字。已实测验证：行序号不被任何断言命中。

- **「检查器」本身必须有对抗性测试，而且必须包含「不该触发」的反极性用例。** 只测「坏样例被抓」不够 —— 一个永远返回 FAIL 的检查器也能通过那种测试。套件的 `--self-test` 22 个用例里有 4 个是**必须不触发**的：docstring 里的 semver 不算硬编码、别名可以满足路由、带理由的 charset 豁免合法、`| 14 |` 行序号不是计数。**反极性用例才是把「检查器」和「永远报警的摆设」区分开的东西。**

- **豁免必须留理由，且无理由的豁免应当判 FAIL。** 套件首跑抓出 3 个未声明 charset 的文件，核实后全是待内嵌片段（`_archviz-theme` / `_flow-attach` / `_archviz-animated`，本就没有自己的 `<head>`）—— 这是**分类问题不是缺陷**，所以登记豁免。但豁免写进配置时必须带理由字符串，空理由直接 FAIL。**同时**：`_archviz-export.html` 同为片段却**已声明 charset**，因此**没有**给它加豁免 —— 多余的豁免就是隐藏。这与 `sync_theme.py` 的 `THEME_EXEMPT` 是同一套纪律。
