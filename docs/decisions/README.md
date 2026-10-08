# Decision Records (ADR)

本目录记录 archviz-diagram 的**架构级决策**——那些「改一次要动多处、事后没人记得为什么」的选择。

## 为什么要这个目录

`constitution.md` 的 `## Development Workflow` 第 1 条要求：

> Constitution (this file) is the root truth. **Update it first for any project-level change.**

但「先改 constitution」这条规矩本身有个缺口：**改什么、为什么改、被否掉的方案是什么** —— 这三件事 constitution 不承载。它们只活在 CHANGELOG 里，而 CHANGELOG 是**版本作用域**的日志：新版本一压上去，旧条目就滚出视野，冲突却还留在代码里。

ADR 就是补这个缺口。**CHANGELOG 记「发生了什么」，ADR 记「为什么这么定，以及为什么不那么定」。**

## 格式

每个 ADR 一个文件：`ADR-NNN-<kebab-case-短标题>.md`，编号只增不跳。

```markdown
# ADR-NNN: <标题>

- **Status**: Proposed | Accepted | Superseded by ADR-NNN | Rejected
- **Date**: YYYY-MM-DD
- **Deciders**: <谁拍的板>
- **Supersedes**: <被本决策取代的 ADR，没有就写 —>

## Context
事实与约束。只写可验证的：引用原文、文件路径、行号、实测数据。不写推测。

## Decision
一句话能说清的决定，然后展开。

## Alternatives Considered
**每个被否掉的方案都必须写明否决理由。** 这一节的价值高于 Decision 本身 ——
半年后想知道「当初为什么没走那条路」时，只有这里能回答。

## Consequences
正面后果、代价、新增的义务。以及兼容性影响。

## Compatibility
Breaking / Non-breaking。Breaking 时说明迁移路径。
```

## 状态流转

```
Proposed ──(用户签)──> Accepted ──(被新决策取代)──> Superseded by ADR-NNN
    └──(否决)──> Rejected
```

- **Proposed 的 ADR 不产生约束力**，只表示「已识别、待拍板」。
- 需要修改 `constitution.md` 的决策，**必须在 ADR 里给出拟改条文原文**，并走 `## Governance` 的修正案流程（显式记录变更 + 改 constitution + 同步 gotchas/SKILL/DESIGN + breaking 时补迁移说明）。
- **Accepted 之后**才允许改 constitution。

## 索引

| ADR | 标题 | Status | Date |
|---|---|---|---|
| [001](ADR-001-paper-framework-mode-vs-text-first.md) | Paper Framework Mode 与 Text-First 原则的关系 | Accepted | 2026-10-08 |
