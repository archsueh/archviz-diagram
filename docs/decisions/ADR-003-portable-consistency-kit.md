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
- 配置驱动：`version` / `budget` / `routing` / `counts` / `coverage` / `deps` /
  `pycompile` / `cjk`（`palette` 仅 archviz-diagram 启用）。
  **具体清单不写在这里** —— `python3 scripts/check_archviz.py --list` 是唯一真源。
- 自带 `--self-test`（对抗性用例，**每个检查都跑双向极性**，含必须**不**触发的反极性
  用例）与 `--self-hash`（`KIT_VERSION` + sha256，供跨仓漂移审计）。
  **用例数量不写在这里**：`--self-test` 自己会报，写死必然过期（本 ADR 第一版就写死过）。
- **豁免必须带理由**：`charset_exempt` / `coverage.exempt` / `deps.exempt` /
  `deps.unused_exempt` / `pycompile.exempt` 的每条值若是空字符串，检查直接 FAIL。
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
2. 套件的 `--self-test` 是自包含的——**任何一个副本退化了，它自己的对抗性用例就会挂**
   （数量不在此处写死：`--self-test` 自己会报，写死必然过期，本 ADR 第一版就
   写死过 "22 个用例"，到 2026-10-09 已经是 23 个了）。
   即：漂移会以「某个仓库的 CI 变红」的形式暴露，而不是静默。

**这个代价已经真实发生过一次，不是假想（2026-10-09）**：
`mentions()` 的 CJK 别名修正（`\b手绘\b` 在 `手绘风格` 里永远匹配不上，
所以 CJK 别名必须走子串匹配）连同第 23 个 fixture 只落在了**工作区**，
没有提交。结果是 **archviz-diagram 自己的 CI 在用旧版 22 用例的套件**，
而它派生出去的四个副本全都带着新版 —— 源仓库落后于自己的副本。
五个工作区副本当时 hash 一致（`a2e25010d4965b14…`），
只有 archviz-diagram 的 HEAD 停在 `24cb497c3fc1cb98…`。
**结论：`--self-hash` 只能比对副本，比对不了「副本 vs 源仓库的 HEAD」——
后者要靠提交纪律，不能靠工具。** 这条是本次实测补上的，属于本 ADR 的已知盲区。

**换来的是**：新增一类检查的成本从「改 5 个文件」降到「改 1 个文件 + 5 行配置」；
且 `archviz-animated` / `archviz-layout` 这两个没有 venv、没有 pyproject、
没有 CI 的仓库，第一次有了可运行的闸门。

**已接受的次生效应**：`check_version_consistency.py` 被删除后，
`CHANGELOG.md` §0.6.1 里「`scripts/check_version_consistency.py` → PASS」这条记录
指向的文件不再存在。**不改写历史记录**——它准确描述了 0.6.1 当时做了什么；
本版 §0.8.0 记录了并入套件这件事。

---

## Update — kit v2（2026-10-09，同日第二次修订）

第一版跑完并落地五仓之后，又做了一轮「先测再答」的探针，测出三类闸门**视野之外**的
缺陷。**注意：当时五仓 7 项检查全绿 —— 也就是说这三个缺陷没有一个能被现有检查看见。**

### 新增 `pycompile`（第 8 项）

`archviz-diagram/examples/deliverables-python-bar.py` **从来不是一个 Python 文件**：它是
被存成 `.py` 的 markdown 片段（收尾 ``` 围栏 + markdown 列表），自 `41c50aa`（v0.0.4）
起在仓库里，**从未编译过一次**，且没有任何文件引用它。

为什么没有闸门看见它：`deps` 对每个文件调 `ast.parse`，**解析失败的文件被静默跳过** ——
对 `deps` 这是对的（解析不了就没有 import 可核对），作为闸门是致命的。所以新增
`pycompile`：递归扫全仓 `.py`，用内建 `compile()` 逐文件编译。

同时收掉一个反模式：CI/hook 里原有的 `compileall -q scripts <pkg>`
**只覆盖两个目录**，而全族唯一的坏文件在第三个目录（`examples/`）里；并且 `compileall`
会往工作树写 `__pycache__`（曾两次把 `.pyc` 带进提交）。`compile()` 在进程内执行，
不写任何东西。**这不是「多一道保险」，是替换掉一道假保险。**

### `deps` 增加反方向核对

正向检查（import → 必须有声明）对「从代码里删掉、却留在 `requirements.txt` 里」的包
**结构性失明**。实测 archviz-diagram 的 `seaborn>=0.12`，全仓唯一出现处是**被注释掉的**
`plt.style.use('seaborn-v0_8-whitegrid')`。

豁免走 `deps.unused_exempt`，必须带理由。`termaid` 是这条豁免的教科书案例：它被当 CLI
调用（`cat x.mmd | termaid --theme mono`），**从不 import**，所以任何基于 AST 的检查都
看不见它 —— 这属于检查的已知盲区，不是缺陷，必须**显式记录**而不是靠调低闸门放过。

顺带修掉一个连带的误报：`_declared_distributions` 原先用宽松正则扫整个 `pyproject.toml`，
会把 `[build-system] requires = ["hatchling"]` 与 `[tool.hatch.*] packages = [...]`
也当成运行时依赖 —— 反方向检查会把**构建后端**报成死依赖。现改为按 TOML 段落取值。

### 非递归 glob 的洞

`coverage` / `counts` / `cjk.scan` 的 glob 写的是 `references/*.md`（**非递归**），
于是 `references/` 下的子目录整体在保护之外。实测两处真内容被漏掉：

| 文件 | 字节 | 被谁点名 |
|---|---|---|
| `archviz-3d/references/3d/boundary-declaration.md` | 2,505 | 只有 `CHANGELOG.md` 一行 |
| `archviz-diagram/references/html-effectiveness/`（7 个文件） | — | INDEX.md 无人点名 |

archviz-3d 的闸门当时报「5 个文件全部可从 SKILL.md 到达」，而目录里实际有 6 个。
两个 glob 都改成 `references/**/*.md`（diagram 另加 `references/**/*.html`），新覆盖的
文件各自补上入口。**这一条特别值得记：闸门报的「全部可达」是真的，只是它的宇宙里少了
一个文件 —— 覆盖范围本身就是需要被检查的事实，而它当时没有任何检查。**

### 一条关于「计数」的教训（第二次同型）

archviz-sketch 的 `SKILL.md` 里「8 套模板」是错的（真值 7），而同一个数**此前已经被
修正过一次** —— 当时修的是另外两处文本，漏了第三处，因为第三处不在 `counts` 的断言里。
**一处断言只锁一处文本。修完要全仓 grep 那个数。** 现已改成 7 并把
`(\d+)\s*套模板` 加进 `counts`。

### 本轮之后仍然成立的结论

- 五仓副本仍逐字节一致（本轮 `0f366b13c6d5120f`）。
- **`--self-hash` 只能比对副本，比对不了「副本 vs 源仓库的 HEAD」** —— 上一节那条盲区
  依然存在，本轮未解决，靠提交纪律。
- 闸门数量的权威来源是 `--list`，不是本文档，也不是任何 CI 注释。CI/hook 里写死的
  「five checks」「seven checks」已全部删除并改成指向 `--list`。
