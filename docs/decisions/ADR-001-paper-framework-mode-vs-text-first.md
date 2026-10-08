# ADR-001: Paper Framework Mode 与 Text-First 原则的关系

- **Status**: Accepted (2026-10-08)
- **Date**: 2026-10-08
- **Deciders**: 用户（显式签署「接受」）
- **Supersedes**: —
- **Implementation**: `constitution.md` v0.3 Principle III + `SKILL.md` §9d 宪制义务 + `DESIGN.md` §1 同步；`references/gotchas.md` 补条目；skill 版本 0.6.1 → 0.6.2

## Context

`constitution.md` 在**三处**把「文本优先」定为根真理：

1. **Principle III**（L13–14）：

   > Primary artifact is always plain text (.mmd, ASCII, or structured data) that survives Obsidian, GitHub, terminal, and diffs. HTML, Python (Plotly), or 3D (Three.js) are **reserved for deliverables that earn them**. Self-contained HTML (zero external deps except verified minimal CDN) is the standard for custom flows, precise attachment, or combined multi-viz pages.

2. **Governance**（L52）：

   > This constitution **supersedes SKILL.md**, DESIGN.md, templates, and all prior practices for archviz work.

3. **Development Workflow #1**（L43）：

   > Constitution (this file) is the root truth. **Update it first for any project-level change.**

v0.6.0 加入了 **Paper Framework Mode**（`SKILL.md` §9d，L525–557），其性质与上条正面冲突：

- **它是 image-first，且是终态**：§9d 阶段表里 `S2-SKETCH-EXPLORE` 与 `S5-CANDIDATE-IMAGE` 是 IMAGE 阶段，且 `S5` 标注为「**IMAGE · 终态**」（`SKILL.md` L540、L543）。交付物落在光栅图上，不落在文本上。
- **它在模式内明令禁止文本替代**（`SKILL.md` L531）：

  > 进入后，出图环节**禁止**用 Mermaid / SVG / HTML canvas / Python(PIL/Plotly/Matplotlib) / Graphviz / TikZ / PPT / PDF / 截图 / 本地程序化光栅代替。

- **它是该技能中唯一需要生图通道的模式**（`SKILL.md` L530）。

**冲突点**：Governance 声明 constitution 优先于 SKILL.md，而 SKILL.md 现在含有一个**在自身终态上不可能产出文本交付物**的模式。

这不是新发现 —— `CHANGELOG.md` §0.6.0 Notes 已记录：

> **与 `constitution.md` 原则 III（Text-First Survivability）的张力，已识别未擅改**：本模式是 image-first。处理方式是把它定义为**显式门禁的模式**（无生图通道即不可用，且模式内禁止文本替代物），而非改变全局默认。若认为需要给 constitution 加一条修正案，请明示 —— 那是需你拍板的文档变更。

**且本仓此前没有任何决策记录机制**：`docs/` 下只有空的 `screenshots/`，无 ADR、无 decision log。所以这类「原则 vs 实现」的冲突**没有既定的裁决载体**——这正是本 ADR 存在的第二个理由。

## Decision

**采纳「按显式门禁挣得例外」的解释，并把「挣得」的判据写死进 Principle III。**

理由：Principle III 自己的措辞里**已经含了逃生舱**——`reserved for deliverables that earn them`。真正缺失的不是例外本身，而是**判据**。把这个判据补进原则，比另开一条并行规则改动更小、约束更紧。

具体地：任何以**非文本产物为终态**的交付，必须**同时**满足三条才可豁免文本优先：

1. **显式模式门禁** —— 它只能通过 `SKILL.md` 声明过的具名模式抵达，该模式有进入条件与明确边界；**永不作为某类图表的默认路径**。
2. **声明非文本终态** —— `SKILL.md` 必须**事先**写明该模式终态为非文本，且**模式内文本替代物无效**；目的是防止智能体在流程中途悄悄降级成文本产物冒充成功。
3. **降级路径** —— 所需通道（生图、浏览器等）不可用时，模式必须**具名**给出回退方案，而不是静默失败或假装成功。

三条不齐者不具豁免资格，必须保持文本优先。

### 拟改条文（供 `constitution.md` Principle III 追加）

> **Earning criterion for non-text terminal artifacts.** A deliverable may terminate in a non-text artifact (HTML, raster image, 3D scene) only when all three hold:
> 1. **Explicit mode gate** — it is reached through a named mode that SKILL.md declares, with an entry condition and a stated boundary. It is never the default path for a chart type.
> 2. **Declared non-text terminal** — SKILL.md states up front that the mode's terminal state is non-text and that in-mode text substitutes are invalid, so the agent does not silently degrade to a text artifact mid-flow.
> 3. **Degradation path** — when the required channel (image generation, browser, etc.) is unavailable, the mode names its fallback explicitly rather than failing open into a fake success.
>
> A mode that cannot satisfy all three is not eligible for the exception and must remain text-first.

**Paper Framework Mode 对这三条的符合性（逐条核过，均为「符合」）**：

| 判据 | 证据 | 结论 |
|---|---|---|
| 1 显式模式门禁 | `SKILL.md` L530 前置条件 + L557 边界段 | ✅ |
| 2 声明非文本终态 | `SKILL.md` L531 禁止替代物 + L543 `IMAGE · 终态` | ✅ |
| 3 降级路径 | `SKILL.md` L532 → `references/paper-framework-workflow.md` 降级路径 | ✅ |

即：**现有实现已满足新判据，本次修正案只做「把隐含判据显式化」，不改任何行为。**

## Alternatives Considered

1. **不作为，保留 CHANGELOG 里的已识别注记。**
   *Rejected*：注记活在**版本作用域**里。0.6.0 一滚出顶部，冲突就不可见了，而代码路径还在。**CHANGELOG 是日志，不是决策记录** —— 日志会被后续版本淹掉，决策记录不会。

2. **把 Principle III 改成「文本优先，Paper Framework Mode 除外」。**
   *Rejected*：这是在**命名实例**而非**给判据**。下一个 image-first 模式（海报？封面？）还得再修一次宪。这跟「把版本号硬编码在 4 个地方」是同一类病 —— 同一个事实写在多处，必然漂移。

3. **删掉 Paper Framework Mode，或用代码优先重写它。**
   *Rejected*：会毁掉这个模式存在的唯一理由 —— 论文框架图的验收标准是**渲染出来的视觉质量**，上游契约的价值恰恰在 S0→S5 的「先出候选、人工筛选、人工定稿」协作流。且该吸收是用户明确要求的。

4. **把 image-first 提升为并列原则。**
   *Rejected*：为**一个**模式，反转**整技能**的默认。`archviz_diagram_list_types` 实测的 **14 类**图表与全部 Mermaid/ASCII 路径都是文本优先，应当保持。

5. **（采纳）扩充「earned」子句，补上显式判据 + 门禁要求。**

## Consequences

**正面**
- Principle III 获得一条**具名、可核**的判据；该模式的豁免从「隐含」变为「可审计」。
- 冲突从 CHANGELOG 注记升格为常驻决策记录，且有了裁决载体（本目录）。

**代价 / 新增义务**
- 未来任何以非文本为终态的模式，都**必须**在 SKILL.md 里写清挣得理由与进入门禁。这是一条小且可检查的规矩。
- 修正案本身要走 Governance 流程：改 `constitution.md` + 同步 `gotchas`/`SKILL`/`DESIGN` 相应条目。

**不变的部分**
- **14 类**既有图表、Mermaid/ASCII 路径、所有模板与 Python 包**零行为变更**。
- 本 ADR 签署（2026-10-08）前，`constitution.md` 曾保持原样，冲突状态维持现状（已在 CHANGELOG 显式登记，不是隐性债）。**签署后已按 Governance 落地**，见下方清单。

## Compatibility

**Non-breaking**（对使用者）。无接口、无 CLI、无产物格式变更。

对**文档**是 breaking 的：`constitution.md` 文本变更，按 Governance 需走修正案流程 + 补迁移说明（本 ADR 即为该说明的载体）。

## Governance 落地清单（2026-10-08 签署后）

`constitution.md` `## Governance` 要求修正案须四项齐备。逐项对账：

| 要求 | 落地物 |
|---|---|
| ① 显式记录变更 | 本 ADR（Status: Accepted）+ `CHANGELOG.md` §0.6.2 |
| ② 更新 constitution | `constitution.md` Principle III 追加挣得判据；**Version 0.2 → 0.3**，`Last Amended` 2026-06-20 → 2026-10-08 |
| ③ 同步 gotchas / SKILL / DESIGN | `references/gotchas.md` 新增条目；`SKILL.md` §9d 加「宪制义务」段；`DESIGN.md` §1 第二签名段补判据指针 |
| ④ breaking 时补迁移说明 | 无 breaking。对使用者零接口变更；`constitution.md` 文本变更为文档级 breaking，迁移说明即本 ADR |

**迁移路径**：无。既有 14 类图表、Mermaid/ASCII 路径、模板与 Python 包行为不变。唯一新增的是一条约未来约束 —— 后续任何非文本终态模式须同样满足三条判据。

**本次不新增决策记录之外的机制**：ADR 目录本身即本仓第一个决策记录载体，`docs/decisions/README.md` 定义格式与状态流转。
