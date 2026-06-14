# Technical Diagram Types

五类"技术沟通图"的类型词汇。消化自 archify（[tt-a1i/archify](https://github.com/tt-a1i/archify)）的类型化输出，落到 archviz 的 renderer + scene-contract + 语义配色上。

核心区分：**workflow 不是通用流程图的替代**，它是"技术沟通图"——有泳道、有语义色、有主路径和异步/审批/观测旁路。选对类型，图才说清楚事。

## 五类

| 类型 | 适合画什么 | 关键语义（描述时要交代） |
|---|---|---|
| **Architecture** | 系统组件、云资源、数据库、缓存、服务边界、安全组 | 组件 + 连接关系 + 技术栈 + 边界 |
| **Workflow** | 请求生命周期、审批流、工具调用、CI/CD、runbook、事故响应 | 参与方（泳道）+ 步骤顺序 + 主路径 + 分支（审批/异步/观测） |
| **Sequence** | API 调用链、缓存回源、鉴权、异步 trace、服务交互 | 谁调用谁 + 先后顺序 + 返回路径 + 同步/异步 |
| **Data Flow** | 数据管线、ETL/ELT、埋点、PII 隔离、仓库同步、血缘、下游消费 | 数据来源 + 处理阶段 + 存储位置 + 敏感边界 + 消费方 |
| **Lifecycle** | 状态机、订单/任务/部署/Agent run 生命周期、等待态、重试、取消、超时 | 有哪些状态 + 哪些事件触发转移 + 哪些是终态 |

## 路径语义（workflow / sequence 通用）

一张技术沟通图里同时有几种路径，用样式区分，别全用实线黑箭头：

- **主路径** — 实线 + accent，正常成功流。
- **异步路径** — 虚线，fire-and-forget / 消息队列 / 后台。
- **审批/人工** — 加 gate 节点（菱形或带锁标记），停等态。
- **观测路径** — 浅色细线，trace / metrics / log 旁路，不抢主路径注意力。

## 落到 archviz 怎么做

| 类型 | 首选 renderer | scene-contract role | 配色 |
|---|---|---|---|
| Architecture | HTML 卡片 + SVG overlay / Mermaid `flowchart` | `container` 分层 + `process`/`store` 节点 | `semantic-component-colors.md` 七类 |
| Workflow | Mermaid `flowchart` + 泳道 subgraph / HTML | `container`=泳道，`process`=步骤，`decision`=gate | 主路径 accent，旁路降饱和 |
| Sequence | Mermaid `sequenceDiagram` | 参与方=`actor`，消息=`edge` 带 style | 同步实线 / 异步虚线 |
| Data Flow | Mermaid `flowchart LR` / Sankey（量级） | `source`/`process`/`store`/`sink` + PII `container` | 数据库紫 / 消息总线橙 / 边界玫红 |
| Lifecycle | Mermaid `stateDiagram-v2` / `state-machine.mmd` 模板 | `state` + 终态标记 | 终态玫红，等待态石灰，活跃态翠绿 |

## Gate（渲染前校验，接 scene-contract）

复杂图先过 `scene-contract.md` 的中间 JSON，再选 renderer。校验"结构合法"早于"语法正确"——这正是 archify 用 schema 做、archviz 用 scene-contract + `validate-mermaid.py` 做的同一件事：

1. 每条 edge 两端节点都存在。
2. Lifecycle 至少有一个终态，无孤立状态。
3. Data Flow 有明确 source 和 sink，PII 边界标出。
4. Workflow 主路径单一可追，旁路标明类型。
5. Mermaid 输出再过 `validate-mermaid.py` 查 subgraph/end 结构平衡（防"Syntax error in text"）。

> 不要为这五类各写一个 ajv 类型化渲染器（archify 那套）——archviz 是 text-first / Mermaid-first，scene-contract + validate-mermaid 已覆盖结构安全。类型词汇用来**选对图、交代对语义**，渲染仍走既有管线。
