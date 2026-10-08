# 论文框架图模式 · 图标资产库

> 落点：`assets/paper-figure/`（**39 MB**，随本仓库分发）
> 来源：`c-narcissus/paper-framework-figure-studio-pro` v3.2.15f 的 `assets/`，原样保留。
> 许可与出处登记 → `assets/paper-figure/ATTRIBUTION.md`

## 目录结构

```
assets/paper-figure/
├── ATTRIBUTION.md                       来源与许可登记
├── architecture/                        工作流架构图 SVG（中英各一）
├── subtype-atlas/                       图型分类板
│   ├── manifest.json                    分类板的权威索引（覆盖角度、显示规则）
│   ├── boards/                          4 张高清板 PNG
│   └── thumbnails/                      4 张缩略图 PNG
└── vector-library/iclr_reference_library/
    ├── curated_icons/                   ★ 首选入口：3 个 jsonl 索引 + 交接契约
    ├── icon_cards/                      每个图标的完整元数据卡（JSON）
    ├── icons/{raw,tight,variants}/      三种 SVG 变体
    ├── neural_network_ppt_primitives/   神经网络原语（cards + ppt_safe）
    ├── paper_derived_icon_cards/        论文派生的 motif 卡
    ├── paper_derived_icon_refinement/   派生 motif 的精修件（cut_svg / 提示词 / 接触印相）
    └── pptx_icon_catalog/               可编辑 PPTX 图集（含嵌入 SVG）
```

## ★ 首选入口：三个精选索引

**不要**直接遍历 `icon_cards/`（688 个文件）。按 `curated_icons/curated_icon_handoff_contract.json` 的指示，下游检索优先用这三个 jsonl：

| 索引 | 内容 |
|---|---|
| `curated_icons/curated_icon_canonical_index.jsonl` | 精选独立图标（保留 `keep_publication_core` / `keep_support`） |
| `curated_icons/curated_neural_ppt_primitive_index.jsonl` | 精选神经网络原语 |
| `curated_icons/curated_paper_derived_motif_index.jsonl` | 精选论文派生 motif |

契约同时给出**默认排除**的图标数（`excluded_from_default_icon_use`）—— 这些不进默认图标池。

> 计数会随上游版本变化。**需要确切数字时现场统计，不要引用本文件的数字**：
> ```bash
> ls assets/paper-figure/vector-library/iclr_reference_library/icon_cards/*.json | wc -l
> cat assets/paper-figure/vector-library/iclr_reference_library/curated_icons/curated_icon_handoff_contract.json
> ```

## Icon card 字段

每个 `icon_cards/<icon_id>.json` 是一张自描述卡：

| 字段 | 用途 |
|---|---|
| `concept_id` / `icon_id` | 概念 id 与图标 id（**必须原样保留**，用于溯源） |
| `primary_meaning` | 主要含义 |
| `aliases` | 别名（检索用） |
| **`negative_aliases`** | **明确不是**什么（见下方纪律） |
| `shape_family_id` | 形状族 —— 同族图标可互换而不破坏视觉一致 |
| `style_variant` | 风格变体（`tabler_outline` / `generated_outline` / `paper_derived_refined_outline` / `lucide_outline` / `local_outline`） |
| `domain_tags` | 领域标签 |
| `recommended_use` / `avoid_use` | 推荐 / 避免用途 |
| `source_lineage` | 上游来源与是否被改过 |
| `license` | **逐图标的许可**（名称 / 包 / 版本 / 许可类型 / 仓库） |
| `files` | 三个变体的相对路径 |
| `anchors` / `ports` | 归一化锚点与端口坐标（center / top / right / bottom / left / baseline；input / output / control / feedback） |
| `vector_quality` | 是否有 viewBox、是否内嵌光栅、是否有烘焙文字、是否 PPT 安全、sha1 |

**`ports` 字段是本库最有价值的部分**：它给出每个图标四向端口的归一化坐标，连线可以精确落在图标端口上，而不是「大概连到盒子边缘」。

## ⚠️ 使用纪律：图标是视觉语言，不是论文证据

这是本库自带契约里最硬的一条，且与 `paper-framework-source-fidelity.md` 完全一致：

> `curated_icon_handoff_contract.json`：
> *"Curated icons are generic visual language only; **they do not transfer source-paper facts**."*

每条 card 的 `negative_aliases` 都含：`paper-specific metric`、`dataset value`、`source-paper claim`；
`avoid_use` 含：`paper factual evidence without target support`。

**落地含义**：

- 图标**只能**用来表达通用视觉语言（「这是一个模块」「这是一个数据流」）。
- **绝不**用图标暗示论文里没有的实体、指标或结论。
- 图标里的概念标签**必须替换**为目标论文有源证据支持的标签（PPTX 图集的 Use Policy 也这么写）。

## 三种 SVG 变体怎么选

| 变体 | 路径 | 何时用 |
|---|---|---|
| `raw` | `icons/raw/` | 需要原始 viewBox（如自行做几何变换） |
| `tight` | `icons/tight/` | **默认选它** —— viewBox 已按可见几何裁切（含描边出血），对齐最省事 |
| `ppt_safe` | `icons/variants/*.ppt_safe.svg` | 进 PPT 用 —— 描边色显式写出，不依赖继承 |

## 图型分类板（subtype-atlas）

4 张板，`manifest.json` 定义默认显示顺序与覆盖角度：

| 板 | 回答什么 |
|---|---|
| `subtype-overview` | 图型总览 |
| `visual-grammar-layout` | 布局语法与骨架 |
| `reader-role-detail` | 读者角色 |
| `visual-communication-styles` | 视觉沟通风格 |

**显示规则（来自 manifest）**：
- 回复里只要提到图型、类别、布局语法、视觉风格、读者角色、沟通风格、密度、隐喻、建模模式、候选方案差异或最终内容架构 → **必须**立即用 Markdown 图片语法把对应板显示出来。**只提文字不算满足。**
- 提到视觉结构、布局骨架、面板编排、模块拓扑、箭头语法、候选板结构、局部精修几何或内容架构 → 同样必须立即显示对应板。
- `boards/` 是高清板（单张 ~1.4–1.9 MB），`thumbnails/` 是缩略图（~180–220 KB）—— 日常展示用缩略图，需要看清细节时用高清板。
- **目标论文的候选图/终图不得内嵌在文本回复里**（这是本库的硬规则）。

## PPTX 图集

`pptx_icon_catalog/` 含两个可编辑 PPTX：

| 文件 | 用途 |
|---|---|
| `pfos_curated_icon_master_catalog_embedded_svg.pptx` | 浏览与直接复制嵌入的 SVG 图标 |
| `pfos_high_level_editable_neural_concepts.pptx` | 图需要**可编辑的内部结构**时用 |

Use Policy：最终出图前**必须**把所有概念标签换成目标论文有源证据支持的标签。

---

## 相关

- 源证据忠实性 → `paper-framework-source-fidelity.md`
- 内部机制约定（何时该用图标）→ `paper-framework-prompt-contract.md` §6
- 既有图标规则 → `icons-patterns.md` · `icon-generation.md`
- 素材资源 → `design-resources-curated.md`
