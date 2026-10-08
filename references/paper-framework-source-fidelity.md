# 论文框架图模式 · 源证据忠实性

> 本模式的图是**论文的图**，不是创意图。审稿人会用图去对照正文 —— 图里出现正文没有的模块、方向反了的箭头、
> 一符多义的符号，都是实质性错误。所以本模式把「证据」提到最高优先级。

## 1. 二选一原则（每条实体与关系都必须满足）

> 每个实体、模块、角色、空间、变量、指标、公式、符号、箭头、port、fork/merge、拓扑、数据流、模型流、控制流、评价流、生成/聚合/训练关系、视觉隐喻、文字标签 ——
> 必须**二选一**：
> ① 由论文 / 补充材料 / 用户材料 / S0 精读报告 / 风险寄存器**直接提供证据锚点**；
> ② 能由这些证据经**严格且可记录的逻辑推理**得到。

推理得到的关系**必须写明前提与推理链**。

## 2. 不许当作证据的东西

| 不能当证据 | 为什么 |
|---|---|
| 「视觉上顺畅」 | 好看 ≠ 论文这么说 |
| 「常见画法」 | 惯例 ≠ 本文结构 |
| 「图像模型可能理解」 | 模型理解 ≠ 审稿人认可 |
| 别的论文这么做 | 跨论文不构成证据 |

任何 **unsupported / contradictory / ambiguous / symbol-mixing** 的 prompt 内容，都是 **handoff blocker**。

## 3. 符号消歧（`symbol_disambiguation_audit`）

两条方向都要守：

- **一符不多义**：同一个符号 / 字母 / 颜色 / 图标 / 线型 / 边标签 / 视觉 token，不得同时表示不同论文概念。
- **多义不归一**：不同论文概念也不得被压缩成同一个符号。

**唯一例外**：prompt 里**明确说明**它们是 source-supported 的 group / aggregate，且压缩后**不改变含义**。

## 4. 变量承载：默认走边

`edge-label-first` —— 下列内容默认放在**线 / port / fork / merge / tag** 上，**不得**画成同级模块盒子：

变量 · 指标 · 权重 · 阈值 · 概率 · 精度 · 损失 · 模型参数

## 5. S0 的语义精度契约（本模式最容易被跳过、后果最重的一步）

S0 阶段的产物 `s0-semantic-precision-contract` 是**硬要求**，缺了 S0 不能关。

**问题**：论文里常有这类**含糊的视觉指令** ——
「保留角色差异」「展示多个参与者」「体现异构性」「反映交互」「区分条件」。
这些句子**不能原样传给下游**，否则下游只能猜，而猜错的代价是整张图重画。

**规则**：S0 必须把每一条含糊指令**归一化**成四件具体的东西：

| 字段 | 内容 |
|---|---|
| `ambiguous_directive_normalization` | 这条含糊话的**具体科学含义**是什么 |
| `role_visual_realization_contract` | **视觉安全**的实现方式 |
| `forbidden_misimplementation_locks` | **明令禁止**的错误实现 |
| `downstream_s1_s4_carry_forward` | 下游必须继承的约束 |

**视觉实现方式必须选一个并写死**（不得留含糊）：

| 可选实现 | 何时用 |
|---|---|
| 紧凑标记（compact markers / chips） | 差异只是属性不同 |
| 只在有差异处分支（branch-only-where-distinct） | 大部分流程相同 |
| 真并行泳道（true parallel lanes） | 确有独立流程且源证据支持 |
| 对照泳道（comparison lanes） | 要对比而非并列 |
| 拓扑/上下文 inset | 差异在环境而非流程 |
| 仅 caption 表达 | 差异不适合上图 |

**最常犯的错**：把「保留角色差异」实现成**每个角色各画一套完整流程**。

> **默认禁止**：重复的角色 / 参与者 / 条件若共享同一条规范流程，S0 必须**显式禁止**为每个角色画一套完整 workflow，
> 而应改用紧凑标记、chips、只在有差异处分支、拓扑/上下文 inset、对照泳道或仅 caption 表达。
> 只有在 contract **明确允许**且有源证据时，才可画多条完整流程。

S1/S4 必须**消费**这份契约，**不得**把 S0 的含糊措辞重新解读成「可以画重复全泳道」的许可。
契约缺失或不完整而 S0 又含高风险含糊指令时 → **S1/S4 必须停下，先修或重跑 S0**。

### 契约必含字段

`s0-semantic-precision-contract` 至少包含：

- `ambiguous_directive_normalization`
- `actor_or_condition_variation_matrix`
- `role_visual_realization_contract`
- `process_instance_budget`
- `forbidden_misimplementation_locks`
- `downstream_s1_s4_carry_forward`

## 6. S0 的风险筛查与就绪状态

S0 需检出：缺失信息、未解决的含糊指令、歧义、矛盾、无支撑的传承关系、不透明的核心模块、范围不匹配。

| 就绪状态 | 含义 |
|---|---|
| `S0_FOUNDATION_READY` | 可以往下走 |
| `S0_FOUNDATION_READY_WITH_RISK` | 带风险走，风险已登记 |
| `S0_NEEDS_AUTHOR_SUPPLEMENT` | 需要作者补充材料 |
| `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK` | 材料不足以出完整框架图 |

用户选择带风险继续时，写入**风险登记**（risk register）并锁定。

## 7. 三条铁律（复核时用）

1. **指不出证据的箭头，不画。**
2. **指不出消费者的承载量，不标。**
3. **同一符号第二个含义出现时，先停下改符号，不要「读者能看出来」。**

---

## 相关

- prompt 契约（假中继、合并线、预算）→ `paper-framework-prompt-contract.md`
- 重复实体族压缩 → `paper-framework-entity-compression.md`
- 流程与阶段职责 → `paper-framework-workflow.md`
