# ADR-003 — 一致性检查收成一个可移植套件，而不是每仓一份脚本

- **Status**: Accepted
- **Date**: 2026-10-09
- **Deciders**: 用户已签（"5 个仓库全做"）
- **Supersedes**: —

## Context

archviz 家族有五个仓库，共用一套设计系统与若干约定。截至 2026-10-09，一致性检查的
分布是这样的：

| 仓库 | 版本闸门 | 调色板闸门 | 其它 |
|---|---|---|---|
| archviz-diagram | `check_version_consistency.py` | `check_palette_registry.py` | CI 11 步 |
| archviz-3d | 无 | 无 | 无 CI |
| archviz-sketch | 无 | 无 | 无 CI |
| archviz-animated | 无 | 无 | 无 CI |
| archviz-layout | 无 | 无 | 无 CI |

既有的跨仓共享约定是「**archviz-diagram 为源，其余手工同步副本**」——
`sync_theme.py` / `sync_export.py` 就存在于多个仓库，且副本已经出现内容分歧
（archviz-3d 的 `EXCLUDED` 比 archviz-diagram 多三项）。

现在要在五个仓库补齐四类检查（路由面 / 字节上限 / 计数一致性 / CJK 编码）。
如果按既有约定办，就是 **6 个脚本 × 5 个仓库 = 30 份拷贝**。

**这恰好是本仓反复在治的那一种病。** 版本号曾写在 4 处（0.6.1 修）、调色板写在 4 处
（0.6.1 修）、判定表达式写在 2 处（0.7.0 修）。再加 30 份拷贝，等于把已确诊的病灶
按仓库数放大。

## Decision

**一个可移植文件 `scripts/check_archviz.py`，每仓一份 `archviz-checks.json`。**

- 代码只有一份（每仓一个物理副本，见下方「代价」），**配置逐仓不同**——因为仓库确实不同。
- 纯 stdlib、零依赖、**不 import 本包**。家族里 archviz-animated / archviz-layout
  **没有 `.venv`**，一个跑不起来的检查器不是闸门。
- 配置驱动五个检查：`version` / `budget` / `routing` / `counts` / `cjk`。
- 自带 `--self-test`（22 个对抗性用例，含 4 个必须**不**触发的反极性用例）与
  `--self-hash`（`KIT_VERSION` + sha256，供跨仓漂移审计）。
- **豁免必须带理由**：`charset_exempt` 的每条值若是空字符串，检查直接 FAIL。
  无理由的豁免就是隐藏（沿用 `sync_theme.py` 的 `THEME_EXEMPT` 纪律）。

### 同时收掉一处重复

`check_version_consistency.py` **删除**，逻辑并入套件的 `version` 检查。
一个实现，不是两个。内容保留在 git 历史 `0a832df`。

`check_palette_registry.py` **保留**：它做的是** id 集合级**比对（engine.py / DESIGN.md /
模板 CSS 三处逐 id 对照），套件的 `counts` 只做**数量级**断言（`**11 palettes**`）。
两者粒度不同，不是重复。调色板也是 archviz-diagram 独有的，不进套件。

## Alternatives Considered

**① 按既有约定，每仓一份专用脚本（6 × 5 = 30 份拷贝）。**
*Rejected*：这就是已确诊的病灶本身。既有副本已经分歧过（archviz-3d 的 `EXCLUDED`
多三项），再复制 30 份等于把分歧面按仓库数放大。**并且**：治「同一事实写在多处」
的手段若是「再多写几处」，逻辑上自相矛盾。

**② git submodule / subtree 共享一个检查仓库。**
*Rejected*：五个仓库各自独立发布（各有自己的 `pyproject.toml` 与 skill 安装面），
submodule 会把「安装这个 skill」变成「先初始化 submodule」。对 agent 安装场景
（`npx skills add` / 直接拷 `SKILL.md`）是净负担。且 `pip install -e .` 的仓库
不该带 submodule 依赖。

**③ 发一个 pip 包 `archviz-checks`。**
*Rejected*：archviz-animated / archviz-layout **没有 `.venv` 也没有 `pyproject.toml`**，
装不了包。而且检查器必须能在**零环境**下跑——它守的是「仓库是否自洽」，
若自身需要先安装依赖才能运行，那它守不住最需要守的那两个仓库。

**④ 只放 archviz-diagram，其余仓库靠 CI 拉取远端脚本运行。**
*Rejected*：CI 需要网络且需要知道 archviz-diagram 的具体路径/分支；
本地 pre-commit 也要跑同一道闸门，否则提交时无感。检查器必须是**本地可执行文件**。

**⑤ 把 `check_palette_registry.py` 也并进套件。**
*Rejected*：粒度不同（id 集合 vs 数量），且调色板是 archviz-diagram 独有概念。
强行统一会让另外四个仓库的配置里出现一堆永远为空的 `palette` 段。
**共享的是代码，不是检查清单。**

## Consequences

**代价（真实存在，不掩饰）**：每仓仍有一个**物理副本**，五个副本会漂移。
这是「五仓库无共享依赖」这一前提下的必然结果，本 ADR 接受它，并用两个手段压住：

1. `--self-hash` 输出 `KIT_VERSION` + sha256，可机械比对。
2. 套件的 `--self-test` 是自包含的——**任何一个副本退化了，它自己的 22 个用例就会挂**。
   即：漂移会以「某个仓库的 CI 变红」的形式暴露，而不是静默。

**换来的是**：新增一类检查的成本从「改 5 个文件」降到「改 1 个文件 + 5 行配置」；
且 `archviz-animated` / `archviz-layout` 这两个没有 venv、没有 pyproject、
没有 CI 的仓库，第一次有了可运行的闸门。

**已接受的次生效应**：`check_version_consistency.py` 被删除后，
`CHANGELOG.md` §0.6.1 里「`scripts/check_version_consistency.py` → PASS」这条记录
指向的文件不再存在。**不改写历史记录**——它准确描述了 0.6.1 当时做了什么；
本版 §0.8.0 记录了并入套件这件事。
