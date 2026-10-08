# ADR-002: 新增 ADVISORY 等级，而非复用 WARN 或 baseline

- **Status**: Accepted (2026-10-08)
- **Date**: 2026-10-08
- **Deciders**: 用户（指令「继续」，承接 anidiagram 评估保留项 #1）
- **Supersedes**: —
- **Implementation**: `scripts/self_check.py`（`Finding.evidence` / `Report.passed()` / `WAIVABLE_LEVELS` / `detect_renderer()`）；`references/accessibility-contract.md` §5；skill 版本 0.6.2 → 0.7.0

## Context

`self_check.py` 此前有三级发现：

| 等级 | 语义 | 阻塞？ |
|---|---|---|
| `FAIL` | 缺陷 | 是（退出码 1） |
| `WARN` | 可疑，待处理 | 默认否，`--strict` 下是 |
| `INFO` | 说明性（跳过了什么） | 否 |

**缺的那一格是「这个偏离是有意的，且这里是它无害的证据」。** 现实里存在这类情况，但没有任何载体能表达它，于是只能二选一地塞进已有的格子里：

- 塞进 `WARN` → 读起来像缺陷（它说的是「可能有问题」）；
- 或用 `baseline` 压住 → 读起来像「知道但不管」，而且**信息被删掉了**（`apply_baseline` 直接从 `findings` 里移除）。

**触发本次决策的具体案例**：`a11y.no_svg`（原 `INFO`）。无障碍契约 R1–R6 全部以 `<svg>` 元素为锚点，所以待内嵌片段、静态 `<canvas>` 模板、图形尚未生成的骨架，在这里都**无从校验**。实测 `--all templates/` 命中 **20/22**。这不是缺陷（契约结构性不适用），但也不是「没问题」（**根本没做校验**）—— 原有的三级表达不了这个区别。

**外部参考（已考证出处）**：anidiagram 的**运行时质量报告**用 `issues` / `advisories` 双数组，`advisories` 不影响 `score`（实测：`score=100` 仍可带 2 条 advisory）。⚠️ 注意它**不在 anidiagram 的文档里** —— 我先前把它记成文档概念是误记，见 `references/gotchas.md`。

## Decision

**新增第四级 `ADVISORY`，并给它三条不变量。** 不复用 `WARN`，也不用 `baseline` 顶替。

三条不变量（已进 `--self-test`，**机器把住而非文档约定**）：

1. **必须带 `evidence`** —— 没证据的 advisory 只是措辞软一点的 WARN。
2. **`--strict` 也不得提升** —— 这是它与 WARN 的分界线。WARN 是「还没处理」，advisory 是「已确认，不必处理」。
3. **不得被基线吞掉** —— `baseline` 是「未修的债务，先压住」，advisory 是「有意接受，本来就不该修」。两者后续处置完全不同，**永不互换**。

外加一条措辞纪律：**`evidence` 必须含 `residual_risk`**，不能只写理由。

## Alternatives Considered

1. **把 `a11y.no_svg` 降为 `WARN` 就够。**
   *Rejected*：`WARN` 的语义是「可能有问题，待处理」，而这里**没有待处理的事** —— 契约不适用就是终态。用 WARN 会导致两种坏结果：`--strict` 下 20 个文件全挂（而它们本无缺陷）；或团队为了让它过而写一条 baseline，于是又回到「信息被删掉」。

2. **保持 `INFO`，不加等级。**
   *Rejected*：`INFO` 是**无判定含义**的说明（「跳过了什么」）。而「契约在这里不适用，残余风险是 X」是一个**需要读者做判断的结论**，不是流水账。INFO 不带 `evidence`、不单列成段、也不出现在 `summary` 计数里 —— 20 个文件的覆盖空洞会被淹没在输出里。**这次改动前后最大的差别就是它从「看不见」变成「看得见且被计数」。**

3. **用 `baseline` 压住，不新增等级。**
   *Rejected*：`baseline` 按 `rule + 每文件计数` 删除 findings —— **有损**。压住之后你看不到覆盖空洞有多大，也看不到它是否在扩大。而且 `baseline` 的语义是「历史遗留，欠着」，把「有意接受」混进去会污染这个信号。ADR 落地时 `write_baseline` 对 advisory 写入 **0 个文件 · 0 项豁免**，正是这条否决的实测证据。

4. **复用 `INFO` 但给它加 `evidence` 字段。**
   *Rejected*：`INFO` 里还有 `io.not_text` / `io.not_html` 这类**真正的流水账**（「这个文件不是 HTML」）。给它们加 `evidence` 是给不需要证据的东西套上证据义务 —— 字段一旦可选就会退化，义务一旦普遍就不被遵守。

5. **（采纳）新增第四级 + 三条不变量。**

## Consequences

**正面**
- 诊断体系从三级变四级，覆盖了此前无法表达的一格。
- 20 个模板的 a11y 覆盖空洞**从不可见变为可见、被计数、带残余风险**。
- `detect_renderer()` 三档分类让「为什么没查到」这个诊断**可验证**（`canvas` 2 / `partial` 4 / `no-graphic-element` 14，与逐文件实测吻合）。
- 三条不变量由 `--self-test` 把住，日后误改会立刻失败。

**代价 / 新增义务**
- `--json` **schema 变更**：`findings` 不再含 ADVISORY（迁至 `advisories`），新增 `summary`。解析方需跟进。
- 新增一条自我约束：以后每加一个 advisory，都要写得出 `residual_risk`。写不出，说明它其实是个 WARN。
- 分级增加到四级，**心智负担上升** —— 这是本决策的主要代价，靠 `SKILL.md` / `accessibility-contract.md` §5 / `--help` 三处写清语义来抵。

**顺带收掉一处重复**：判定表达式 `not fails and not (strict and warns)` 原先在 `emit()` 与 JSON 分支**各写了一遍**，加第四级时才暴露 → 收成 `Report.passed(strict)`。与「版本号硬编码在 4 处」「调色板数量写死」同型。

## Compatibility

对使用者 **non-breaking**：既有 FAIL / WARN / INFO 行为、退出码、基线机制全部不变。
**仅 `--json` 消费者需跟进**（`findings` 不含 ADVISORY）。无迁移路径需要 —— 旧字段语义未变，只是不再承载新等级。
