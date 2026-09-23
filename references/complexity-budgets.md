# Complexity Budgets（逐类型复杂度预算）

**Load when:** 确定类型之后、动手画之前。用来判断「这个内容量是否还在这个类型的可读区间内」。

**为什么需要逐类型预算**：全局 soft-cap「9 nodes」对流程图成立，对甘特图毫无意义（甘特图没有节点，只有任务条），对雷达图也不成立（雷达图限制的是**轴数**不是节点数）。每个类型的「过载点」在**不同的维度**上。

> 本文件把 SKILL.md QR 里的粗粒度约束（soft-cap 9 / hard split >12 / 绝对上限 50）展开成逐类型的硬数字。全局规则仍然生效，逐类型预算是在其之上的**收紧**，不是放宽。

---

## 1. 全局预算（所有类型）

| 预算项 | 规则 |
|---|---|
| Soft cap | **9 nodes** —— 超过倾向拆图 |
| 硬拆 | **>12 nodes** 或 **>15 edges** → 概览 + 详图，绝不出一张面条图 |
| 绝对上限 | **50 nodes** —— Mermaid 布局的硬失败线 |
| 焦点 | accent 只上 **1–2** 个元素；想上 4 个说明还没决定焦点 |
| 混合类型 | 最多 **2 个类型**；混搭时只取**主导轴**，不杂交语法 |
| 图例 | 只用到的类型；超过 7 项 → 归并「其他」+ 直接标注 |
| 容器嵌套 | ≤3 层 |

**拆图的正确形态**：概览图（≤9 节点，说清主干）+ 详图（每个子系统一张）。**不要**把 30 个节点硬塞成一张然后指望读者缩放。

---

## 2. 逐类型预算表（27 类）

约束列里加粗的是该类型的**真实过载点**——先看加粗项。

| # | 类型 | 约束（加粗=主约束） | 超限处理 |
|---|---|---|---|
| 1 | Architecture | **nodes ≤9** · edges ≤14 · containers ≤3 | 按边界分区拆图 |
| 2 | Flowchart | **nodes ≤9** · edges ≤12 · 每个决策节点分支 ≤3 | 分支 >3 → 拆成子流程 |
| 3 | Sequence | **lifelines ≤5** · messages ≤12 · alt 区 ≤2 · fragment 嵌套 ≤1 | lifelines >5 → 合并同角色 |
| 4 | State machine | **states ≤9** · transitions ≤14 · 终态 ≥1 | 拆「正常路径 / 异常路径」两张 |
| 5 | ER / data model | **entities ≤8** · 每实体字段 ≤6 · 关系 ≤10 | 按域拆图；字段明细走表格 |
| 6 | Timeline | **events ≤8** · 轴跨度 ≤5 | 聚合为「阶段 + 代表事件」 |
| 7 | Swimlane | **lanes ≤5** · nodes ≤12 · 交接 ≤10 | lanes >5 → 合并同职能角色 |
| 8 | Quadrant / 2×2 | **items ≤12** · 轴固定 2 条 | items >12 → 只画前 8 + 其余归「其他」 |
| 9 | Nested | **嵌套 ≤3 层** · nodes ≤9 | 更深层级 → 改用 tree 或拆图 |
| 10 | Tree | **depth ≤4** · nodes ≤15 · 扇出 ≤5 | depth >4 → 折叠中间层 |
| 11 | Org chart | **depth ≤4** · nodes ≤12 | >12 → 只画到「部门」层，人名走表格 |
| 12 | Venn | **circles ≤3**（几何硬限）· 每圆标签 ≤5 | >3 集合 → 改用矩阵表 |
| 13 | Layer stack | **layers ≤6** · 每层 nodes ≤4 | layers >6 → 合并相邻抽象层 |
| 14 | Pyramid / funnel | **levels ≤6** · 落差标注 ≤5 | levels >6 → 只标首尾 + 最大落差 |
| 15 | Consultant 2×2 | **cells = 4**（固定）· 命名单元 ≤4 | 单元内条目 >3 → 移入 caption 表 |
| 16 | Radar / spider | **axes ≤7**（≤5 最佳）· series ≤5 · 焦点 series = 1 | axes >7 → 归并同义轴 |
| 17 | Loop / flywheel | **stations ≤8** · hub = 1 | stations >8 → 拆两个环 |
| 18 | IT current-state | **phases ≤4** · nodes ≤12 | 按阶段拆图；标清 legacy vs target |
| 19 | High-level stack | **layers 3–5** · nodes ≤12 | layers >5 → 合并，或拆成两张栈图 |
| 20 | Bar chart | **bars ≤12** | >12 → 归并「其他」或改 treemap |
| 21 | Line chart | **series ≤5** · 每系列点数 ≤20 | 点数 >20 → 抽样或改面积图 |
| 22 | Gantt | **tasks ≤12** · sections 3–6 | >12 → 按阶段分多张甘特 |
| 23 | Scatter | **points ≤30** | >30 → 抽样 / 加透明度 / 改热力图 |
| 24 | Process | **actors ≤5** · steps ≤10 | steps >10 → 按阶段拆 |
| 25 | Medallion | **tiers = 3**（bronze/silver/gold 固定）· 每层 nodes ≤4 | 每层 >4 → 只画代表 + 数量标注 |
| 26 | Data flow | **roles ≤5** · steps ≤10 · PII 边界 ≤2 | steps >10 → 按 pipeline 阶段拆 |
| 27 | DP security matrix | **roles ≤6** · 权限列 ≤8 · 优先表格 | 超限 → 按权限域拆多张表 |

---

## 3. 非节点型约束（最容易漏的一类）

有些类型的过载点**完全不是节点数**。以下维度单独设限：

| 维度 | 适用类型 | 上限 |
|---|---|---|
| 生命线 | Sequence | 5 |
| 泳道 | Swimlane | 5 |
| 轴数 | Radar | 7（建议 ≤5） |
| 系列数 | Radar / Line | 5 |
| 圆数 | Venn | 3 |
| 层数 | Layer stack / Pyramid / High-level | 6 / 6 / 5 |
| 阶段数 | Timeline / IT state / Gantt section | 5 / 4 / 6 |
| 甘特任务 | Gantt | 12 |
| 散点数 | Scatter | 30 |
| 柱数 | Bar | 12 |
| 实体数 | ER | 8 |
| 树深 / 组织深 | Tree / Org | 4 / 4 |
| 角色数 | Process / Data flow / Security matrix | 5 / 5 / 6 |
| 色阶档位 | 任何用色阶的 | 6 |

---

## 4. 超限时的处理决策树

```
内容量超预算
  │
  ├─ 属于「节点/元素太多」
  │    └─ 走 output-dials.md §2 的降级阶梯（装饰 → 重复 → 叶簇 → 基础设施）
  │        └─ 降到位仍超 → 拆图（概览 + 详图）
  │
  ├─ 属于「维度太多」（轴/系列/泳道/生命线）
  │    └─ 归并同义项（轴合并、系列合并、角色合并）
  │        └─ 归并不了 → 换类型（如 radar 轴 >7 → 改 diverging bar）
  │
  └─ 属于「类型本身装不下」
       └─ 换类型，不是硬塞
            · 权限网格 → 表格，不是图
            · ≤5 项比较 → 表格
            · 一对多层级 >4 层 → tree 换 nested 或拆
```

**任何降级/拆图之后，必须出保真账本**（`output-dials.md` §4）。

---

## 5. 与门禁的关系

| 门禁 | 关系 |
|---|---|
| **G1 Type** | 本文件是 G1 的判定依据：G1 通过 = 类型选对 **且** 在预算内 |
| **G5 Validate** | 预算超限未处理 = G5 不通过 |
| **QR 硬规则** | QR 的「≤5 items → TABLE」优先级高于本文件——先判该不该画，再判预算 |

**Iron rule 追加一条**：**超预算但没拆图、也没出账本的产出，不算通过 G1。**

---

## 6. 检查清单

- [ ] 选了哪个类型？该类型的主约束（表里加粗项）是什么？
- [ ] 主约束的实际数值是多少？在限内吗？
- [ ] 该类型有没有**非节点型约束**（轴/系列/泳道/生命线/层数/阶段数）？各自在限内吗？
- [ ] 全局预算（soft-cap 9 / hard split >12 / 绝对 50）也满足吗？
- [ ] accent 只上了 1–2 个元素？
- [ ] 超限的话，走的是降级阶梯还是换类型？**有没有硬塞？**
- [ ] 降级/拆图之后出保真账本了吗？
