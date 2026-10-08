# ATTRIBUTION — `assets/paper-figure/`

本目录下的资产**原样取自**上游开源项目，按主题归入 archviz-diagram。此文件登记来源与许可。

## 上游项目

| 项 | 值 |
|---|---|
| 项目 | `paper-framework-figure-studio-pro` |
| 仓库 | https://github.com/c-narcissus/paper-framework-figure-studio-pro |
| 版本 | `v3.2.15f`（skill 包内 `VERSION` 文件） |
| 打包日期 | 2026-07-09 |
| 转载日期 | 2026-10-08 |
| 转载范围 | 该 skill 包的 `assets/` 目录**全量** |

## 上游许可

skill 包内自带 `LICENSE`：

```text
MIT No Attribution
Copyright 2026 OpenAI
```

**MIT No Attribution（MIT-0）**：允许使用、复制、修改、合并、发布、分发、再许可与出售，
**且不要求署名**。因此本目录随 archviz-diagram（MIT）一同分发是合规的；
本 ATTRIBUTION 文件属**自愿登记**，便于日后溯源。

> 注意：上游**仓库根目录没有 LICENSE 文件**（GitHub 因此显示 "no license"），
> 许可只存在于发行的 skill 包 zip 内。溯源时以 zip 内的 LICENSE 为准。

## 目录内的第三方素材

`vector-library/iclr_reference_library/` 里的图标**不是**全部由上游生成 —— 其中一部分来自第三方图标库。
**每张 icon card 的 `license` 字段逐条记录了该图标的真实来源与许可**，随卡一同分发。

按 `icon_cards/*.json` 的 `license` / `source_lineage.source` 字段统计（采集于 2026-10-08）：

| 来源 | 许可 | 占比 |
|---|---|---|
| 上游项目自生成（`generated_deep_learning_svg_icons`） | 随上游 MIT-0 | 最多 |
| `@tabler/icons` | **MIT** — https://github.com/tabler/tabler-icons | 次多 |
| 论文派生 motif 抽象（`paper_framework_figure_motif_extraction`） | 随上游 MIT-0 | 100 条 |
| 本地抽取（`local_extracted_svg_icons`） | `local_project_asset`（无外部许可声明） | 少量 |
| `lucide-static` | **ISC** — https://github.com/lucide-icons/lucide | 少量 |

**重新统计**（数字会随上游版本变化，勿引用旧值）：

```bash
python3 - <<'PY'
import json, glob, collections
c = collections.Counter()
for f in glob.glob('assets/paper-figure/vector-library/iclr_reference_library/icon_cards/*.json'):
    L = (json.load(open(f)).get('license') or {})
    c['%s (%s)' % (L.get('name'), L.get('license'))] += 1
for k, v in c.most_common(): print('%-52s %d' % (k, v))
PY
```

### 关于 Tabler / Lucide

两者的许可（MIT / ISC）均允许再分发与再许可，**要求保留版权与许可声明**。
该声明已逐条存在于各 `icon_cards/*.json` 的 `license` 与 `source_lineage` 字段中，
**请勿删除这些字段**。

### 关于「论文派生 motif」（100 条）

`paper_derived_icon_cards/` 与 `paper_derived_icon_refinement/` 中的 100 条，
是上游从已发表论文的图里**抽象出的几何 motif**（非图形复制），随上游 MIT-0 分发。
引用时按通用视觉语言使用，**不构成对原论文事实的引用**。

### 关于 `local_project_asset`（少量）

这部分的 icon card 未声明外部许可，视同上游项目自产内容，随 MIT-0 分发。

## 使用纪律

见 `references/paper-framework-icon-library.md`：
图标是**通用视觉语言**，不承载论文事实；概念标签必须在出图前替换为目标论文有源证据支持的标签。
