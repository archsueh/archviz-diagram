# 论文框架图模式 · 表面风格

> **表面风格只约束渲染层**，不改变候选图的论文语义、布局骨架、连线证据和密度预算。
> 它不是候选方案的差异来源 —— 候选方案的差异来自**叙事角色 / 布局语法 / 语义焦点 / 密度 / 细节策略 / 视觉修辞 / 连线层次**。

## 两轮的默认

| 轮次 | 阶段 | 默认表面风格 | 谁来定 |
|---|---|---|---|
| 第一轮探索 | S2 | **正式出版风格**（`formal_publication_schematic`） | S1 记录；除非用户在 S1 请求里显式覆盖或取消 |
| 第二轮正式 | S5 | 由 S4 按论文需要设置 | S4 拥有并注入 |

**第一轮的默认是「正式出版风格」而非手绘风** —— 因为用户常在第一轮之后就开始自己动手画，手绘风不适合拿去做 PPT。

## 可选项（12 种）

正式出版风格 · 低保真草图 · 白板线框 · 干净扁平极简线稿 · 正式 schematic 布局草案 · 轻量蓝图精密稿 · 轻量科学插画 · 轻量界面隐喻 · 轻量等距结构 · 轻量信息图板 · 手绘故事板 · ACM/IEEE/AAAI 双栏论文 line-art schematic

**第一轮 vs 第二轮的适用差异**：
低保真草图、白板线框、手绘故事板**默认只适合第一轮探索**。若要用于第二轮，必须在 S4 请求里明确说明它仍需保持 formal candidate 的可读性。

## 激活与记录

表面风格**默认不激活**，只有用户在对应请求里显式写入才生效。S0 的提示只是**告知选项存在**，本身不激活。

激活时 S1 或 S4 必须记录：

```json
{
  "style_id": "acm_ieee_aaai_line_art_schematic",
  "style_label": "ACM/IEEE/AAAI 双栏论文 line-art schematic",
  "style_family": "publication_line_art",
  "stage_scope": "first_round_s2_or_second_round_s5"
}
```

- 用户要求**整轮**用某风格 → 应用到该轮**每个** prompt 包
- 用户只要求**部分行** → 只应用到那些行，并记录行级 scope

**职责划分（第二轮）**：S3 只负责把选项提醒给用户（让用户能把风格意图写进下一次 S4 请求），**不**创建 S5 prompt 包、**不**拥有第二轮风格记录；S4 才拥有正式候选矩阵、S5 prompt 包与风格注入。

## ACM/IEEE/AAAI 双栏 line-art schematic

**依据说明**：这是**风格综合**，不代表 ACM/IEEE/AAAI 规定了某个统一视觉模板。

综合的公开指引要点：

| 来源 | 要点 |
|---|---|
| IEEE Author Center | 尽量用矢量图；黑白线稿若非矢量需高分辨率；建议检查灰阶可读性，不依赖颜色区分 |
| Nature 终稿指引 | 无衬线字体，优先 Helvetica / Arial，全文图字体一致 |
| PLOS 图件指引 | 给出生产默认值参考（如 8 pt 文字、0.2 mm 线宽） |
| Wiley 图件指引 | 把流程图/示意图视为 line art，倾向 PDF/EPS 式处理 |
| AAAI 投稿要求 | 双栏高分辨率；字体须可读（非 Type 3）；插图标签不小于九点 |

参考链接：
- https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/
- https://www.nature.com/nature/for-authors/final-submission
- https://journals.plos.org/plosone/s/figures
- https://authors.wiley.com/author-resources/Journal-Authors/Prepare/manuscript-preparation-guidelines.html/figure-preparation.html
- https://aaai.org/conference/aaai/aaai-26/submission-instructions/

**注入到生图 prompt 的风格块**：

```text
Style treatment: ACM/IEEE/AAAI double-column paper line-art schematic.
Create a white-background, vector-like line-art schematic suitable for ACM/IEEE/AAAI two-column
research papers. Use thin but print-safe strokes, sparse color, minimal icons, and compact labels.
Prefer Arial/Helvetica-like sans-serif labeling with consistent small text; keep labels legible at
double-column paper scale. Use line style, shape, brightness, grouping, and pattern as redundant
encodings so meaning is not carried by color alone. Keep the drawing close to publication line art:
simple boxes, arrows, ports, braces, small callouts, and precise paper-grounded connectors.
Avoid gradients, drop shadows, poster-like large titles, design-principle panels, decorative photo
thumbnails, glossy illustrations, dense dashboards, marketing graphics, and unsupported icons.
Preserve all source-grounded semantics, arrow directions, variable-on-edge rules, modular hierarchy,
prompt-index IDs, and S1/S4 negative constraints.
```

**负约束**：不得用这个风格选项绕过论文证据；不得加装饰性图标、图库缩略图、与论文无关的视觉隐喻、纯颜色区分、大块说明性标题面板。
若该风格与某篇论文的源保真可读性冲突，S1/S4 必须**记录冲突**，并**收窄风格范围**或**请用户在 S2/S5 前取舍**。

## 交接提醒规则（防误复制）

表面风格的选项清单必须出现在**可复制提示词块之外**，避免用户把可选项一起复制进默认提示词。

| 交接 | 是否给提醒 | 关键说明 |
|---|---|---|
| S0 → S1 | ✅ 给（非复制散文） | 说明第一轮默认是正式出版风格；要改请在**下一次 S1 请求**里写 |
| S1 → S2 | ✅ 给（非复制散文） | 说明 S2 只按 S1 的 prompt-index 走；**改第一轮风格要重跑 S1，不是改 S2 提示词** |
| S3 → S4 | ✅ 给（非复制散文） | 说明第二轮风格由 S4 拥有；要指定请写进**下一次 S4 请求** |
| S4 → S5 | ❌ **不给** | S4 只给 S5 的纯生图提示词，不加风格提醒 |

提醒**非阻塞** —— 不得为问风格而暂停当前阶段。

## 风格必须与其他维度组合

一个候选的风格 ≠ 表面风格。S1 必须把表面风格与下列维度**组合**：

叙事角色 · 布局语法 · 语义焦点 · 密度 · 细节策略 · 视觉修辞 · 连线层次 · 源证据约束

**S1 的组合选法**：先规划 **8 个**互补且内部不矛盾的风格组合 → 全部评分 → 取最高的 **4 个** → 说明每个入选组合**为何互补而非矛盾** → 只把这 4 个映射到 `C01`–`C04`。

---

## 相关

- 配色（反 AI 味）→ `paper-framework-palette.md`
- prompt 契约 → `paper-framework-prompt-contract.md`
- 流程与阶段职责 → `paper-framework-workflow.md`
