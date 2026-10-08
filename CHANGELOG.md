# Changelog

## 0.7.0 (2026-10-08)

### Added
- **`self_check.py` 新增第四级发现 `ADVISORY` —— 「经证据证实的、故意的偏离」。** 决策记录见 [`docs/decisions/ADR-002`](docs/decisions/ADR-002-advisory-level.md)（含 4 个被否方案及理由）。
  补上的是诊断体系里一个真实的空档：此前只有 `FAIL`（缺陷，阻塞）/ `WARN`（可疑，`--strict` 阻塞）/ `INFO`（说明性），**没有任何载体能表达「这个偏离是有意的，且这里是它无害的证据」**。于是这类情况只能被塞进 WARN（读起来像缺陷）或被基线吞掉（读起来像「知道但不管」，且信息被删掉）。
  - **三条不变量，已进 `--self-test`（22 个用例全 PASS）**：① 必须带 `evidence`；② `--strict` 也**不得**提升；③ **不得被基线吞掉**。写在文档里没用 —— 必须让机器把住，否则日后有人顺手改一行就把它退化成措辞软一点的 WARN。
  - **与 WARN 的分界**：WARN = 「可能有问题，待处理」；ADVISORY = 「已确认无害，这里是证据」。
  - **与 baseline 的分界**：baseline = 「未修的债务，先压住」；ADVISORY = 「有意接受，本来就不该修」。两者后续处置完全不同，**永不互换** —— 代码里用 `WAIVABLE_LEVELS` 常量声明一次，`write_baseline` / `apply_baseline` 共用（此前这个元组在两个函数里各写了一遍）。
  - **evidence 必须含 `residual_risk`**，不能只写理由。把「没做校验」说成「确认无害」就是粉饰 —— advisory 的正当性来自**披露**，不来自**宽免**。

- **首个 ADVISORY：`a11y.no_svg`**（原为 `INFO`）。无障碍契约 R1–R6 全部以 `<svg>` 元素为锚点，所以待内嵌片段、静态 `<canvas>` 模板、以及图形尚未生成的模板骨架，在这里都**无从校验**。现在如实报出并附残余风险。
  - 新增 `detect_renderer()` 三档分类（**必须用剥掉 `<script>` 的版本判定**，理由见下）：
    | 档 | 判据 | 实测（`--all templates/`） |
    |---|---|---|
    | `canvas` | 存在静态 `<canvas>` 元素 | **2**（`waffle` / `webgl-info-viz`） |
    | `partial` | 无 `<!doctype` / `<html` | **4**（`_archviz-animated` / `_archviz-export` / `_archviz-theme` / `_flow-attach`） |
    | `no-graphic-element` | 完整文档但无任何静态图形元素 | **14** |
  - `no-graphic-element` 这一档**刻意不断言意图**：同一个事实在「待填的模板骨架」上是正常的，在「本该有图但没生成」的产物上是缺陷，而 `self_check.py` 分不清二者。所以只说「没查到什么」，不说「所以没问题」，把判断留给读的人。

### Changed
- **`--json` 输出 schema 变更（消费者注意）**：新增顶层 `summary`（`fail` / `warn` / `advisory` 计数）与 `advisories` 数组；**`findings` 不再包含 ADVISORY**（已迁至 `advisories`）。与 anidiagram 质量报告的 `issues` / `advisories` 双数组同构 —— 逼消费者显式处理 advisory，而不是把它当缺陷一起计数。带 `evidence` 字段（仅非空时出现）。
- **`Report.passed(strict)` 收成单一真源**。判定表达式 `not fails and not (strict and warns)` 原先在 `emit()` 与 JSON 分支里**各写了一遍** —— 加第四级时才暴露。与版本号四处漂移、调色板数量写死同型。
- **`apply_baseline()` 行为不变但语义显式化**：ADVISORY 从来就不在豁免范围内，此前靠 `level in ("FAIL", "WARN")` 隐式成立，现改用 `WAIVABLE_LEVELS` 常量并写明理由。
- 文本输出把 ADVISORY 单列一段（`── N 条 advisory（有意偏离 · 不阻塞 · 不计入判定）`），避免混在 FAIL/WARN 里被读成缺陷；汇总行单列 advisory 数。
- `references/accessibility-contract.md` §5 补 `a11y.no_svg` 行与 ADVISORY 语义；`references/gotchas.md` **更正一条旧记录的两处错误**（见下）。

### Notes
- **⚠️ 旧记录更正**：`references/gotchas.md` 的 2026-09-30 条目称 `a11y.no_svg` 命中「22 个模板中的 **15** 个」且「**它们用 `<canvas>`**」。2026-10-08 实测：**20 个**，且「用 canvas」是**假**（真实静态 `<canvas>` 只有 2 个）。原文错在把 `grep -l "<canvas"` 的 19/22 当成了元素统计 —— 其中 18 个的 `<canvas` 在 `<script>` 里，多数还是导出模块**错误提示里的字符串字面量**（`"give it an <svg> or <canvas> element to rasterize"`）。
- **诊断类字段落笔前必须逐项核。** 本次同一处 `renderer` 误诊两次（先 `canvas`、后 `non-svg`）才对。**一个指向不存在问题的诊断，比沉默更消耗信任。**
- **静态扫描陷阱（本仓高频）**：模板里 `<svg>` / `<canvas>` 的多数出现都在 JS 字符串里或由运行时创建 —— `area-chart.html` 全文仅 1 处 `<svg`，在 `<script>` 内的字符串中。**任何基于 `grep` 的静态统计，先确认命中的是元素还是字符串**（判据：跑 `strip_script_bodies()` 后再数）。
- **`advisories` 的设计出处已考证**：它**不在** anidiagram 的文档里，而是其**运行时质量报告的一个字段**（`advisories` 不影响 `score`）。先前评估记录把它当成文档概念，属误记。**「我在它的输出里见过」不等于「它文档里有这个概念」。**
- 对使用者 **non-breaking**：既有 FAIL / WARN / INFO 行为、退出码、基线机制全部不变。唯一需要跟进的是解析 `--json` 的消费者（见 Changed 第 1 条）。

## 0.6.2 (2026-10-08)

### Added
- **`docs/decisions/` —— 本仓第一个决策记录载体（ADR）**。此前 `docs/` 下只有空的 `screenshots/`，**零决策记录**。缺口是结构性的：`constitution.md` 的 Development Workflow 第 1 条要求「任何项目级变更先改 constitution」，但 **constitution 不承载「改什么、为什么、被否掉的方案是什么」**——这三件事只活在 CHANGELOG 里，而 CHANGELOG 是**版本作用域**的：新版本一压上去，旧条目滚出视野，冲突却还留在代码里。
  - `docs/decisions/README.md` —— 格式约定（Status / Date / Deciders / Context / Decision / **Alternatives Considered with explicit rejected reasons** / Consequences / Compatibility）+ 状态流转（Proposed → Accepted → Superseded）。
  - `docs/decisions/ADR-001-paper-framework-mode-vs-text-first.md` —— 首个 ADR，**Accepted**。

- **`constitution.md` Principle III 修正案（ADR-001 落地）** —— 追加 **Earning criterion for non-text terminal artifacts**：非文本终态产物（HTML / 光栅图 / 3D 场景）须**同时**满足三条才可豁免文本优先 —— ① 显式模式门禁；② 事先声明非文本终态且模式内文本替代无效；③ 具名降级路径。三条不齐者不具豁免资格。
  - **`Version` 0.2 → 0.3**，`Last Amended` 2026-06-20 → 2026-10-08。
  - **关键判断**：Principle III 自己的措辞里**已经含了逃生舱**（`reserved for deliverables that earn them`）。缺的不是例外，是**判据**。补判据比另开一条并行规则改动更小、约束更紧。
  - **对现有实现零行为变更**：逐条核过 Paper Framework Mode 三条齐备（§9d L530 门禁 / L531 禁止替代物 + L543 `IMAGE · 终态` / L532 降级路径）。本次只做「隐含判据显式化」。

### Changed
- **`SKILL.md` §9d** 加「宪制义务」段 —— 把三条判据写在模式作者会看到的地方（未来同类模式以 §9d 为范本）。同时给后续同类模式立了一条可检查的约束。
- **`DESIGN.md` §1** 第二签名段补判据指针 —— 该段原本也断言 text-first（`HTML, Python, and 3D are reserved for deliverables that earn them`），「earn」此前**无定义**，现指向 constitution Principle III。
- **`references/gotchas.md`** 新增条目（见下）。
- `SKILL.md` `metadata.version` `0.6.1` → `0.6.2`；`pyproject.toml` 同步。

### Notes
- **为什么不把 Principle III 改成「文本优先，Paper Framework Mode 除外」** —— 那是在**命名实例**而非**给判据**。下一个 image-first 模式（海报？封面？）还得再修一次宪。这跟「版本号硬编码在 4 个地方」（见 §0.6.1）是**同一类病**：同一事实写在多处必然漂移。ADR-001 里另有 3 个被否方案及理由。
- **Governance 四项逐条对账**（显式记录 / 改 constitution / 同步 gotchas·SKILL·DESIGN / breaking 迁移说明）见 ADR-001 末节表格。
- **兼容性**：对使用者 **non-breaking** —— 无接口、无 CLI、无产物格式变更。14 类图表、Mermaid/ASCII 路径、模板与 Python 包全部不变。

## 0.6.1 (2026-10-08)

### Fixed
- **发布版本号散落在四处且各自漂移** —— 同一个事实写了 4 遍，谁也没拦住谁：

  | 位置 | 原值 | 落后 |
  |---|---|---|
  | `SKILL.md` `metadata.version` | 0.6.0 | 真源 |
  | `CHANGELOG.md` 首条 | 0.6.0 | — |
  | `pyproject.toml` `version` | **0.5.3** | 4 个版本 |
  | `scripts/publish-skill.py` | **0.2.5**（写死字面量 + `# TODO`） | ~9 个版本 |

  `publish-skill.py` 那处最危险：`tag` 直接由自己的字面量拼出，**照它发版会打出 `v0.2.5` 的 tag 并创建同名 Release**，而技能实际是 0.6.0。已改为运行时从 `SKILL.md` 的 `metadata.version` 读取（`read_skill_version()`，并校验 X.Y.Z 格式），TODO 一并消除。
- **`scripts/publish-skill.py` 里的旧仓名与写死路径** —— 脚本残留 `archviz-skills`（改名前的名字）：默认根路径写死 `/Users/mac/Developer/archviz-skills`、`repo_name = "archviz-skills"`、Release 标题与安装说明也全是旧名。`gh repo create` 会去建一个 `archsueh/archviz-skills`，与实际的 `archsueh/archviz-diagram` 不是同一个仓。已改为：默认根路径由脚本自身位置推导（`Path(__file__).resolve().parent.parent`），`repo_name` 由 `skill_dir.name` 推导。
- **`SKILL.md` §「Family MCP Servers」表三处失真**：
  - `archviz-sketch` 写作「4 styles」，实测 `list_styles()` 返回 **7 个**（`process-draft` / `minimal-line` / `swiss-modernist` / `product-handdrawn` / `xiaohei` / `watercolor` / `architectural-marker`）—— 连它自己的 `mcp_server.py` docstring 也只列了 6 个。
  - `archviz-animated` 与 `archviz-layout` 被列在「**MCP Servers**」表内，但两仓**都没有 `mcp_server.py`**，各自 SKILL.md 里 MCP 出现 **0 次**。照表配置只会配出一个永远起不来的服务器。已移出该表，单列为「skill-only」。
  - 原先只给工具数量，改为给出**真实工具名**（`archviz3d_generate` / `archviz_sketch_list_styles` 等），便于直接照抄配置。
- **`SKILL.md` 的安装命令 `pip install -e ".[mcp]"` 在本仓必然失败** —— 本仓 `.venv` 是 uv 创建的最小 venv，**不含 pip**（`No module named pip`）。改为 `uv pip install --python .venv/bin/python -e ".[mcp]"`，并注明另两个兄弟仓的 venv 是有 pip 的（已实测：`archviz-3d` / `archviz-sketch` 为 pip 26.1.2）。

### Added
- **`scripts/check_version_consistency.py`** —— 版本一致性闸门，纯 stdlib。以 `SKILL.md` `metadata.version` 为真源，校验 ① `CHANGELOG.md` 首条 `## X.Y.Z`、② `pyproject.toml` `version`、③ `scripts/publish-skill.py` **不含写死的 semver 字面量**。退出码 0/1/2，写法与既有的 `check_palette_registry.py` 一致。
  已接入 `.github/workflows/ci.yml` 与 `scripts/git-pre-commit.sh`。
  > 这是同一类问题的**第二次**出现（第一次是调色板注册表散在四处）。凡是「同一个事实写在多处」的地方，都该有一个闸门 —— 否则它一定会漂移。

### Changed
- `pyproject.toml` `version` 0.5.3 → **0.6.1**（补上落后 4 个版本的升级）。

### Verified
- `scripts/check_version_consistency.py` → PASS
- `scripts/check_palette_registry.py` → PASS（11 个 id 四处一致）
- frontmatter：`name` 与目录名一致、`metadata.version` = 0.6.1、`license: MIT`、YAML 可解析
- `SKILL.md` 引用的 35 个 `references/*.md` 断链数 = **0**
- 家族实际能力均经命令核实：`archviz-diagram` 14 类型 / 3 工具 · `archviz-3d` 2 类型 / 2 工具 · `archviz-sketch` 7 风格 / 2 工具
- `publish-skill.py` 的 `read_skill_version()` 已实跑，正确读出 `0.6.1`

### Notes
- 本次未改任何模板、`archviz_diagram/` 包代码或资产；仅文档、版本号、发布脚本与新增闸门。
- `publish-skill.py` 的发布流程本身（`gh repo create` → commit → tag → push → `gh release create`）**未改动**，只把三处写死的常量改为推导。仍**不自动执行** —— 需要 `input()` 人工确认。

## 0.6.0 (2026-10-08)

### Added
- **Paper Framework Mode（论文框架图，§9d）** —— 从上游 [`c-narcissus/paper-framework-figure-studio-pro`](https://github.com/c-narcissus/paper-framework-figure-studio-pro) v3.2.15f 吸收。这是本技能中**第一个、也是唯一一个要求生图通道的模式**，作为显式门禁的模式存在（写法对齐 `archviz-sketch` 的前置条件），不改变默认的代码优先定位。
  - **流程**：`S0-PAPER-FOUNDATION` → `S1-FIGURE-STRATEGY` → `S2-SKETCH-EXPLORE`（图）→ `S3-DIRECTION-SELECT` → `S4-CANDIDATE-BRIEF` → `S5-CANDIDATE-IMAGE`（图 · 终态）。候选数契约 `C01`–`C04` / `F01`–`F02`。
  - **三条不可让的规则**：① 每轮只执行一个公开步骤（硬人机等待屏障）；② S2/S5 是纯图像阶段，逐行原子，不写审计/排名/解释；③ 源证据优先于好看。
  - 7 个新 reference（上游 **100 个**带版本号的 policy 已按主题收敛）：
    `paper-framework-workflow.md` · `paper-framework-prompt-contract.md` · `paper-framework-source-fidelity.md` · `paper-framework-surface-styles.md` · `paper-framework-palette.md` · `paper-framework-entity-compression.md` · `paper-framework-icon-library.md`
- **`assets/paper-figure/`（39 MB，本仓首个 `assets/` 目录）** —— 上游 `assets/` 全量：
  - `vector-library/iclr_reference_library/` —— 图标向量库。每张 icon card 是自描述 JSON，含**逐图标许可**、`negative_aliases`、`shape_family_id`，以及**归一化端口坐标**（`ports.input/output/control/feedback`）—— 连线可精确落在图标端口而非盒子边缘。
  - `subtype-atlas/` —— 图型分类板（4 高清板 + 4 缩略图 + `manifest.json`）。
  - `pptx_icon_catalog/` —— 可编辑 PPTX 图集（含 1192 个嵌入 SVG）。
  - `ATTRIBUTION.md` —— 来源与许可登记。**逐图标**来源分解：上游自生成 / Tabler(MIT) / Lucide(ISC) / 论文派生 motif / 本地资产。许可声明已存在于各 card 的 `license` + `source_lineage` 字段，**勿删**。
- `SKILL.md`：`Skill Boundaries` 表加行、按需加载地图加「论文框架图模式」子表、新增 §9d、`description` 与 `triggers` 补触发词、`RESOURCES` 表加上游条目。
- `references/credits.md`：补上游致谢条目。

### Changed
- **`SKILL.md` frontmatter `version` 由 `0.5.5` 更正为 `0.6.0`。** 该字段在 v0.5.6 时**忘了跟着升**（v0.5.6 改了 §3.5 的调色板数量，但没动 frontmatter），因此本次是「补一次迟到的升级 + 本次功能升级」合并在一个 minor 版本里。

### Notes
- **剥离的上游内容（有意为之，非遗漏）**：① 强制在每次非终端回复末尾追加固定句；② 在特定提问下原文背诵作者的私人赠言（个人内容，非能力）；③ ChatGPT 网页端专属机械 —— checkpoint zip 门禁、34 个 `figure_studio_*` guard 脚本、text-only guard 原文（本机有文件系统与 git，不需要长会话恢复机制）；④ 100 个带版本号的 policy 文件名（版本号进文件名 = 维护债）；⑤ 上游打包元数据 `metadata.json` / `PATCH_REPORT_*.md` / `agents/openai.yaml`。
- **与 `constitution.md` 原则 III（Text-First Survivability）的张力，已识别未擅改**：本模式是 image-first。处理方式是把它定义为**显式门禁的模式**（无生图通道即不可用，且模式内禁止文本替代物），而非改变全局默认。若认为需要给 constitution 加一条修正案，请明示 —— 那是需你拍板的文档变更。
- **未改任何既有模板 / Python 包 / 调色板注册表**：本次是纯增量（1 个模式段 + 7 个 reference + 1 个资产目录）。
- **仓库体积**：55 MB → 约 94 MB（资产 39 MB）。其中 `pptx_icon_catalog/` 占 8.4 MB（两个二进制 PPTX）。若嫌重，删该子目录即可，其余资产不受影响。

## 0.5.6 (2026-10-08)

### Fixed
- **`blueprint` 缺失于 Python 调色板注册表**（`archviz_diagram/engine.py`）。v0.5.4 把 Technical Blueprint 加进了 `_archviz-theme.html`、`DESIGN.md`、`preview.html` 和全部 17 个模板 —— **`engine.py` 不在那份清单里**。`_apply_theme()` 的第一行是 `if theme_name not in PALETTES: return html`，于是 `--palette blueprint` **原样返回文档且不报错**（静默空操作），`list-palettes` 与 `archviz_diagram_list_palettes()` 也少报一个。取值镜像模板的 `[data-palette="blueprint"]` 块。已端到端验证：`render(..., {"theme": "blueprint"})` 现在产出 `<html data-palette="blueprint">`。
- **同一份调色板注册表写在四个地方，且已各自漂移**：

  | 来源 | 修复前 | 问题 |
  |---|---|---|
  | `templates/html/_archviz-theme.html` | 11 | **真源**（CSS + 切换序列） |
  | `archviz_diagram/engine.py` | 10 | 缺 `blueprint` |
  | `DESIGN.md` Palette Registry 表 | 8 | 缺 4 个，且多一个非注册表项 |
  | `SKILL.md` "N palettes" | **6** | 陈旧 5 个 |

- **`DESIGN.md` 把 Educational Flat 列进了 Palette Registry 表**，容易被读成「一个可选主题」。它不是注册表成员：独立色阶系统（`references/educational-flat-system.md`）、按 brief 显式启用、不参与主题循环、也没有 `data-palette` CSS 块。已移出表格并加注说明。

### Added
- **`scripts/check_palette_registry.py`** —— 零依赖一致性闸门。以模板为唯一真源，机械比对四项：① `engine.py` 的 id 集合 ② `DESIGN.md` 注册表表的 id 集合 ③ `SKILL.md` 声明的数量 ④ 每个 id 是否有 `[data-palette]` CSS 块（`auto-time` 豁免——它在应用时委托给别的调色板，本就不该有块）。带 `--self-test`（5 个用例，含四种漂移各一）。
- CI 新增 `Verify Palette Registry Consistency` 步骤；`scripts/git-pre-commit.sh` 同步加入（放在 sync/prettier 块**之前**——那块顺序是承重的，本检查与它无关，早失败更好）。

### Changed
- `DESIGN.md` Palette Registry 表补 `id` 列、补齐到 11 行，并注明「本表是镜像，真源在模板」；`Runtime Behavior` 里那句 "don't hardcode the count here — it drifts" 改为「数量是**被校验的**，不是手工维护的」。
- `SKILL.md` §3.5 的调色板清单由 6 更正为 11。

### Notes
- **未改动任何模板**：`blueprint` 的 CSS 与 JS 注册表条目在 v0.5.4 就已就位，本次只补 Python 侧与文档。`sync_theme.py` / `sync_export.py` 无 diff。
- **顺带发现（未改，留待决定）**：`still-paper` 与 `editorial-parchment` 的 18 个 CSS 变量**逐项完全相同**。`still-paper` 是 `auto-time` 的日间档（`isDaytime ? "still-paper" : "ikb-dark"`），两者是否应有区别是设计决策，不在本次修复范围。已在 `DESIGN.md` 该行标注。

## 0.5.5 (2026-09-30)

### Fixed
- **Export never actually worked on SVG targets** (`_archviz-export.html`, propagated to all 18 templates). `exportBlob()` compared `target.tagName === "SVG"`, but elements in the SVG namespace report **lowercase** `"svg"` while HTML elements report uppercase `"CANVAS"`. The comparison never matched, so every SVG target fell through to the HTML branch, where the `<foreignObject>` → `<img>` route hangs Chromium's image decoder on any non-trivial subtree — blocking the main thread hard enough that not even a `setTimeout` guard could fire. Symptoms: `E→P`/`E→W`/`E→C` did nothing forever with no toast and no error, and `E→S` always answered "SVG export requires an SVG target" even on a real SVG. Fixed by lowercasing the tagName comparisons and deleting the foreignObject route; HTML targets now fail fast with an actionable message.
  Verified in headless Chromium (blob captured, no download): `line-chart` PNG 23 ms / WebP 125 ms / SVG 2 ms; `heatmap` 17 / 85 / 2 ms; `webgl-info-viz` (canvas target) 100 / 733 ms. `academic-table` and `network-topology` (HTML targets) now fail in ≤6 ms instead of hanging.
- **3 templates never received the shared export module** — `academic-table.html`, `network-topology.html`, `webgl-info-viz.html`. `sync_export.py` skipped them silently, and because the skip produced no diff, CI's `git diff --exit-code` guard passed. `academic-table` had kept a hand-rolled stub whose `exportPNG()`/`exportWebP()` only fired `alert("...integrate html2canvas")` and whose `copyToClipboard()` used the deprecated `document.execCommand("copy")` — on the one template G0 points at for permission/access matrices.
- **`network-topology.html` referenced 11 `--av-*` variables across 40 call sites while defining none.** It pulled in the theme with `<link rel="stylesheet" href="_archviz-theme.html" />`, which is not a stylesheet. Page background and every colour silently fell back to nothing.
- **CI has been red since 2026-06-28** — 7 consecutive failures on `main`. The step order was `sync → git diff --exit-code → prettier --check`, but Prettier re-indents the embedded `<style>`/`<script>` blocks that the sync scripts paste in, so `sync` alone can never reproduce a committed template: the diff check was unsatisfiable by construction. Reordered to mirror `scripts/git-pre-commit.sh` (`prettier --check → sync → prettier --write → git diff`) and pinned Prettier to 3.9.9 in both places so a release cannot silently change the expected formatting.

### Changed
- `scripts/sync_theme.py` and `scripts/sync_export.py` now **exit non-zero and name the offending file** when a template is missing its anchor, instead of skipping silently. A skip is now only ever an explicit `EXCLUDED` / `THEME_EXEMPT` entry with a stated reason. Silent skipping is what let this drift hide for three months.
- `webgl-info-viz.html`: bound its local `--surface` / `--text` / `--border` / `--accent` to `--av-*` (its own comments claimed it inherited from `_archviz-theme`), added the theme block, moved `#controls` off `top:10/right:10` — where it sat under the theme toggle and export button — to `top:56/right:12`, and marked the canvas as the export target.
- `references/export-patterns.md`: documented the tagName pitfall and the HTML-target limitation; corrected the `file://` row of the cross-platform matrix (it works — verified).
- `references/validation-checklist.md`: the export-target bullets now state that the target must be an `<svg>` or `<canvas>`.

## 0.5.4 (2026-09-24)

### Added
- **Technical Blueprint palette** — archviz-layout's 4th visual language: deep navy `#0d1b2a` + cyan hairline `#2a4a6b` + single cyan accent `#5fd0e8` (0 radius, weight ≤600, Mono labels). Added to the SKILL.md palette table, `DESIGN.md` (§2 Palette Registry + §Arcviz-Layout Integration, now **Four Visual Languages**), `preview.html`, and all 17 HTML templates (CSS block + JS `PALETTES` registry + `order` array).

### Fixed
- **Duplicate theme system in 6 templates** (`treemap`, `bubble`, `funnel`, `sunburst`, `waterfall`, `bullet-graph`): a reduced in-body "Theme System Script" clobbered the full `<head>` registry, rendering **two** toggle buttons and hiding `swiss-modernist` / `vignelli-canon` / the three layout languages from the switcher. Removed the redundant block — all 17 templates now expose a single toggle and the full 11-palette registry (verified: 1 button, 11 entries, `blueprint` present, 0 console errors).

## 0.5.3 (2026-07-21)

### Fixed
- Hard-coded `/Users/mac/Developer/archviz` paths in `scripts/sync_theme.py`, `sync_export.py`, `fix_html_syntax.py`, `generate_html_charts.py` → resolve repo root via `Path(__file__).parent.parent` (pre-commit no longer warns missing theme).
- `scripts/git-pre-commit.sh`: optional `.venv` pip check; `cd` to repo root; `npx --yes prettier`.
- Stale absolute paths in sankey template comment + `self-contained-html-viz.txt`.

## 0.5.2 (2026-07-21)

### Added
- **G0 draw-or-not** + **G0b brand gate**: paragraph/table test; host DESIGN.md / `.archviz-preset.yaml` before silent Warm Paper (`references/brand-gate.md`).
- Structural density rules in `structural-diagram-types.md`: soft-cap 9 nodes, hard split >12/15 edges, focal 1–2, connector discipline, when-not-to-draw table.
- `templates/excalidraw/`: Warm Paper `mindmap.excalidraw` + `architecture.excalidraw` + README (promote path → Mermaid).

### Changed
- Gates table G0/G0b/G1/G2 tightened; QR Focal + Brand lines; workflow steps reordered; anti-patterns for accent-as-flags / silent brand / diagram-when-prose-wins.
- Degradation strategy: soft-cap 9 before absolute 50.
- §12 template inventory includes excalidraw/.

## 0.5.1 (2026-07-21)

### Added
- `references/ecosystem-routing.md`: Mermaid / diagram-design / draw.io / Excalidraw / Lucidchart-alts decision matrix — when to stay in archviz vs hand off; anti-bloat rules.
- `references/structural-diagram-types.md`: 27-type selector map absorbed from [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) (routing only; no gallery vendor).
- Mermaid templates: `sequence.mmd`, `swimlane.mmd`, `quadrant.mmd` (Warm Paper init + ASCII/table fallback).

### Changed
- `references/external-tools.md`: expanded with Mermaid, diagram-design, Excalidraw, Lucidchart-alts; points to ecosystem-routing as SSOT.
- `SKILL.md` (v0.5.1): QR type table + engine routing; §0 type routing pointers; honest §12 template inventory (removed false excalidraw/obsidian-canvas/3d claims); resources + 致谢 cite diagram-design.
- Triggers: +sequence, swimlane, quadrant, 序列图, 泳道图.

### Policy
- Optimize ≠ delete (iron rule preserved). diagram-design is **type vocabulary only** — do not dump 27 HTML assets or their default jet-black + atomic-tangerine skin into archviz.

## 0.4.3 (2026-06-18)

### Added
- `§15 COMPRESSION & TOKEN BUDGET`: 基于 headroom（chopratejas/headroom）压缩思维，新增输入规整、输出极简、可逆缓存 analog、场景化预算表四节。规则覆盖输入扁平化、嵌入式 white-space 省略、ASCII fallback 并行准备、self-healing loop ≤2 rounds 上限、caption ≤15 words、无装饰性过渡语、golden copy + rollback contract + audit log。

### Changed
- `§致谢`: 增加 headroom 引用。
- `SKILL.md` 完整性：确认 §15 追加后未修改既有 §0–§14 任意段落，无 content deletion。

## 0.4.2 (2026-06-14)

### Added
- `references/semantic-component-colors.md`: 组件类型 → 语义色 taxonomy（frontend/backend/database/cloud/security/msgbus/external 七类，双主题 hex 配对 + CSS 语义类）。消化自 [archify](https://github.com/tt-a1i/archify)，与既有 Max-1-accent / No-AI-purple / editorial-禁冷灰规则做了调和说明。
- `references/diagram-types-technical.md`: 五类技术沟通图类型词汇（architecture/workflow/sequence/data flow/lifecycle）+ 路径语义（主路径/异步/审批/观测）+ 落到 renderer/scene-contract 的映射表。明确不移植 archify 的 ajv 类型化渲染器（与 text-first/Mermaid-first 哲学冲突）。

### Changed
- `references/export-patterns.md`: 4× 栅格化补两个鲁棒性细节——canvas 超浏览器上限自动降级（4×→3×→2×→1×）、JPEG/WebP 按主题 `--surface` 补背景色防黑底。
- SKILL.md §0 加 Type routing、§2 加 Semantic colors 指针、§致谢 记 archify。

## 0.4.1 (2026-06-14)

### Changed
- `archviz_generate` MCP tool description now states its scope is the self-contained HTML chart subset only; Mermaid/ASCII/Python output come from the skill docs, not this tool.
- SKILL.md §16 "3D GOTCHAS" relocated: 3D / Three.js / animejs gotchas now live solely in `archviz-3d` (`## Key Gotchas` + `## Detailed Pitfalls & Patterns`, consolidated there by the 2026-06-14 skill merge). The 2D skill keeps only a pointer (§16b). Aligns version with the existing `v0.4.1` commit.

## 0.4.0 (2026-06-14)

### Added
- `constitution.md`: Project-level governance document codifying 6 core principles (Restraint as Dial, Text-First Survivability, Exact Fidelity, Color Restraint, Single Artifact Convergence, Gotchas as Living SSOT)
- `templates/html/_flow-attach.html`: Reusable flow attachment utilities (attachRectEdgeRight/Left, attachCirclePerimeter, offsetCurve) extracted from real session
- `examples/us-flows.html`: Combined Energy Sankey + Migration Map in single Swiss container (387 lines)
- `examples/us-population-migration-2024.html`: Real GeoJSON choropleth with Census 2024 data + migration flow bands
- `references/webgl-info-arch.md`: WebGL info visualization architecture reference
- `templates/html/webgl-info-viz.html`: WebGL info visualization template
- `templates/mermaid/sankey-us-energy-2023.mmd`: LLNL energy Sankey Mermaid template
- `references/icons-patterns.md`: Icon usage patterns reference

### Changed
- SKILL.md: Added flow/network routing to pure HTML for attachment-critical cases; added "combined page" exception for deliberate multi-viz demos; added 2 new gotchas entries
- references/gotchas.md: +6 entries from 2026-06 session (flow attachment math, color iteration loop, convergence pattern, Mermaid incompatibility, combined pages, workspace hygiene)
- references/validation-checklist.md: Added custom flow validation (edges before nodes, exact perimeter attachment)
- templates/html/self-contained-html-viz.txt: Added constitution + flow-attach references

### Removed
- docs/screenshots/3d/ (6 PNG files) — moved to archviz-3d
- examples/us-migration-2010-2020-map.html — merged into us-flows.html
- examples/us-energy-2023-sankey.html — merged into us-flows.html

## Session log (2026-06-13, before sleep)

- Verified full local tree + last-commit messages against the GitHub file list pasted by user (docs/screenshots with git-push PNG + 3d/, examples/ with git-push html/mmd, references/, scripts/, templates/, .gitignore, CHANGELOG, CONTRIBUTING, DESIGN, LICENSE, README, SKILL, preview.html, requirements.txt). All files present and messages align (recent "Update README.md", "docs: add PNG screenshot...", "release: v0.2.5", older v0.0.x on standard files). `git status` clean, no drift.

- Cleaned unnecessary historical process documents: removed the entire "### 0.1.6 Optimization References" section (the long list of early drawio/termaid/drawnix etc. projects) from README.md. This was the main "过程文档" bloat left from the initial optimization pass. "Core dependencies" kept. README structure tree already clean (no old agents/ etc.).

- Git-push screenshot material (PNG in docs/screenshots/ + self-contained HTML in examples/) remains the prominent "截图素材 / Screenshot Material (v0.2.5)" section at the very top of README (using the <img width/height> preview-card style the user manually tuned and showed in screenshot), so the good pictures display directly on the repo homepage.

- Pushed the cleanup (after rebase to integrate any remote manual tweaks).

准备睡了。晚安。

## 0.2.5 (2026-06-12)

### Changed
- Bumped SKILL.md metadata, README badge, and publish helper marker to `0.2.5`.
- Replaced the historical self-evolution narrative in SKILL.md with a compact release self-check protocol.
- Added Darwin / macOS fit notes to `references/termaid-routing.md`.
- Cleaned README screenshot material copy and removed internal meta notes from the first screen.

### Validation
- Darwin target for future releases: >= 96.
- Curation policy: keep reference-only projects out of runtime dependencies; no toolkit bloat.

## 0.1.7 Reference Integrations (2026-06-12)

### Added
- `references/wesanderson-palette.md` — constrained Wes Anderson / Moonrise Kingdom palette variant.
- `references/icon-generation.md` — SVG icon generation references for restrained diagrams and editorial cards.
- `references/reading-to-viz-learning-workflow.md` and `scripts/reading-to-viz.py` — reading-to-visual-learning starter flow.
- `references/ascii-cli-alternatives.md` and `references/ascii-workflow.md` — CLI-first ASCII workflow around termaid and plain ASCII fallback.

### Changed
- SKILL.md resources now group external projects by use instead of patch history.
- DESIGN.md quick color reference includes the Wes Anderson variant.
- ASCII guidance explicitly avoids web-only tools in agent-driven workflows.

## 0.1.7 (2026-06-12)

**Darwin + Curation + Self-Evolution Pass (0.1.6 → 0.1.7)**

Ran darwin-skill, skills-curation, and self-evolution (darwin on self + curation loop) on 0.1.6 per usual process.

**Darwin Evaluation (0.1.6):**
- Score: 94/100
- Breakdown: Identity 25/25 (perfect hsueh design/teaching/AI viz/cleanliness), Gates 19/20 (strong G0-G6 + self-healing), Error/Pitfalls 18/20 (good but enhance with viz-specific table), Overlap 15/15 (unique restrained multi-format), Structure 9/10, Darwin 8/10.
- Recs applied: Add explicit Self-Evolution & Darwin Integration section (with score example, error table, cross-refs to darwin/curation/subagent/verification), viz-specific error table, darwin triggers, self-score loop.

**Curation Judgment:**
- High value for hsueh workflow (design, teaching, archviz, agent skills). No bloat. Enhance existing with darwin integration and error tables rather than new files. Score target ≥95 post-edit.

**Self-Evolution Applied:**
- Updated SKILL.md with new §17 Self-Evolution & Darwin Integration (includes darwin eval report, error table, integration notes, agy example).
- Bumped version, updated resources with darwin/curation links.
- Enhanced 14b Pitfalls with darwin self-optimization example.
- Updated README badge and CHANGELOG.
- Followed absolute paths, no new bloat, cross-refs to existing (subagent-driven-development, verification-loop, goal).

**Final:** 0.1.7 ready. Clean structure preserved. Next: re-run darwin for ≥96, add more viz types if needed.

## 0.1.6 (2026-06-12)

**Optimization & Reference Integration Plan (based on review of 6 external projects)**

This release formalizes a major optimization pass after reviewing:
- Agents365-ai/drawio-skill
- plait-board/drawnix
- markdown-viewer/skills
- fasouto/termaid
- DayuanJiang/next-ai-draw-io
- Rss3208/Visiomaster (and related viz patterns)

**Optimization Plan Goals for 0.1.6 (implemented in this release and follow-ups):**
1. **Draw.io / Editable Professional Handoff** (primary from drawio-skill): Add full references/drawio-output-mode.md with XML plan generation, 6 presets, vision self-check, up to 5-round refinement, codebase-to-diagram support, 10k+ shapes guidance, and export via draw.io CLI (PNG/SVG/PDF). Keep archviz light — no heavy runtime dependency.
2. **Whiteboard & Advanced Diagramming** (from drawnix): Add support for Drawnix/Plait-compatible outputs (mindmap + flowchart + freehand hybrid, Markdown-to-mindmap, Mermaid conversion). New templates/drawnix/ and obsidian-canvas/ enhancements. Plugin-friendly architecture notes in DESIGN.md.
3. **Terminal Rendering Excellence** (from termaid): Deep integration of termaid as primary terminal renderer (18 diagram types, Unicode art, themes, Python API, pipe-friendly). Fallback to pure ASCII only when termaid unavailable. Added `references/termaid-routing.md`.
4. **Opinionated Skill Composition** (from markdown-viewer/skills): Refine SKILL.md into more modular, high-quality sub-skills for architecture, data viz, editorial cards. Better frontmatter, triggers, and composition patterns. 14+ specialized capabilities.
5. **Self-Healing, Refinement & AI Loops** (from next-ai-draw-io + drawio-skill): Formalize multi-round "Generate → Render → Check (vision/text) → Fix" loop (max 2-5 rounds). Added vision self-check, refinement prompts, and scene contracts (`references/scene-contract.md`).
6. **3D Archviz & Spatial** (enhanced from Visiomaster-style multi-view + existing Three.js): Polish Three.js modes (structure, 2D flow layout, section, walkthrough) with better animation, lighting constraints, and CDN patterns. Add more examples.
7. **Documentation & Research Consolidation**: Update DESIGN.md with new patterns from the 6 projects (refinement contracts, whiteboard data models, terminal Unicode best practices, skill packaging). Expand research/ with cross-project insights.
8. **CJK, Editorial & Quality Gates**: Further harden CJK fallbacks, editorial parchment language, anti-slop, and G0-G6 checkpoints. Add more red lines and validation.
9. **Examples & Deliverables**: New examples for draw.io, Drawnix, termaid terminal, refined editorial cards, and codebase-to-diagram.
10. **Structure Cleanup**: Remove duplication between root and archviz-skills/ subdir (if any), ensure clean packaging for agent marketplaces.

**Intentionally Lightweight**: No full web editor, MCP server, or heavy whiteboard runtime imported. Stays pure agent-native skill with templates + references.

### Added
- Comprehensive 0.1.6 optimization plan documented here.
- Enhanced references/ (drawio-output-mode.md, termaid-routing.md, scene-contract.md) with concrete integration from reviewed projects.
- New templates/ for drawio, drawnix, and expanded editorial/3D.
- Additional examples demonstrating cross-project patterns (codebase-to-diagram, refinement loops, terminal Unicode).

### Changed
- SKILL.md frontmatter version → `0.1.6`.
- README badge and "What this is" now reflect full 0.1.6 capabilities (draw.io, Drawnix guidance, termaid primary, modular skills, self-healing).
- DESIGN.md and research/ updated with lessons from the 6 projects.
- Version and changelog now explicitly credit the reference integration.

### Notes
- This release makes archviz-skills significantly more powerful for professional architecture, data, and editorial visualization while keeping the "restrained, text-first, agent-native" philosophy.
- Follow-up 0.1.7+ will focus on implementing any remaining stub templates (e.g., full drawio XML generator examples) and marketplace packaging.

## 0.1.5 (2026-06-12)

**Reference pass: draw.io handoff + termaid routing + scene contract**

### Added
- `references/drawio-output-mode.md` — lightweight draw.io mode for editable professional handoff without pulling in a heavy app framework.
- `references/termaid-routing.md` — terminal-first Mermaid rendering policy: use termaid when available, then ASCII fallback.
- `references/scene-contract.md` — intermediate scene contract for complex diagrams before choosing Mermaid / HTML / draw.io / Canvas.

### Changed
- SKILL frontmatter version → `0.1.5`.
- README badge and capability summary now mention termaid terminal routing, Obsidian Canvas, draw.io guidance, and scene contracts.
- SKILL routing table now includes editable architecture handoff and references the new rules.

### Notes
- Based on local review of `Agents365-ai/drawio-skill`, `fasouto/termaid`, `markdown-viewer/skills`, `Visiomaster`, `drawnix`, and `next-ai-draw-io`.
- Intentionally **not** importing a web editor, MCP server, or full whiteboard runtime. `archviz-skills` stays light and agent-native.

## 0.1.1 (2026-06-12)

**Darwin + skills-curation pass** (target score ≥90 before push)

### Added
- **When to Use / When NOT to Use** + **Skill Boundaries** table (vs claude-design-card, mermaid-arc-skills).
- **Checkpoints G0–G6** with STOP conditions and iron rule.
- **§14b Pitfalls & Red Lines (绝不)** — editorial + diagram hard bans.
- Editorial error rows in §13; editorial gates in `validation-checklist.md`.
- Frontmatter: `source`, `risk: safe`, expanded triggers (封面/卡片/排版).

### Changed
- **§9b** compressed to gate + pointer (token efficiency; detail in `editorial-parchment-language.md`).
- Darwin re-score: 84 → **92/100** (gates + boundaries + red lines + overlap clarity).

## 0.1.0 (2026-06-12)

**Editorial Parchment language — distilled from claude-design-card**

### Added
- **`references/editorial-parchment-language.md`**: warm canvas / Terracotta accent / serif+sans split / format families A–D / surface pacing / ask-before-generate / anti-patterns (upstream: [geekjourneyx/claude-design-card](https://github.com/geekjourneyx/claude-design-card)).
- **`templates/html/editorial-card.html`**: Family B knowledge-card skeleton with Family A/C/D override notes.
- **DESIGN.md**: Editorial Parchment palette row + Extended Format Families section + ready-to-use editorial prompt.
- **SKILL.md §9b Editorial Mode**: format routing, compression rule, platform safe zones, workflow ask gate.
- **QR table**: cover / knowledge card / social square / long-form → `editorial-card.html`.
- **Anti-patterns**: cover-as-summary, serif 700, cool SaaS white, equal card grid.

### Changed
- Brief inference signal #8: deliverable intent (diagram vs card vs long-form vs 3D).
- Palette routing note: Warm Paper+IKB default; Editorial Parchment+Terracotta for cards/covers; host-doc override preserved.

## 0.0.9 (2026-06-11)

**DESIGN.md restructured into the Stitch 9-section format + visual catalog**

### Added
- **DESIGN.md 9-section structure** (per VoltAgent/awesome-design-md): §1 Visual Theme & Atmosphere (prose + key characteristics + Agent-Readable Contract), §2 Color Palette & Roles, §3 Typography Rules, §4 Component Stylings, §5 Layout Principles, §6 Depth & Elevation, §7 Do's and Don'ts, §8 Responsive Behavior, §9 Agent Prompt Guide. Taxonomy, Aver patterns, 3D, and validation moved to Extended sections — no content lost.
- **Semantic color names**: every token now has name + hex + role (Warm Paper #f5f0eb, Paper Beige #e8e4e0, Mist White #f5f5f4, Stone Gray #a8a29e, Pebble #d6d3d1, Ink Navy #1B365D, Warm Ink #44403c, Charcoal #292524, Near Black #0a0a0a, IKB #002FA7, Lemon #FFD500).
- **§9 Agent Prompt Guide**: quick color reference + 4 ready-to-use prompts (flowchart, gantt, comparison, 3D shell) + 5-step iteration guide.
- **§6 Depth & Elevation**: "flat by doctrine" table — emphasis via line weight and the single accent, never shadows.
- **preview.html**: visual catalog at repo root (neutral/accent swatches, palette system table, type scale, node vocabulary, edge semantics) — the awesome-design-md preview convention.

### Changed
- **Signature Patterns (Aver domain)** synced with the Aver cinnabar-era system: V1 spine 物件→陪伴证据→告别归档; Money/Evidence/Sentiment naming (legacy Money/Knowledge/Sentiment marked archive-only); accent slot switches to Aver cinnabar #A24A2D inside Aver-branded documents (still max 1); Aver paper surfaces allowed for host-document matching.
- README design-system section now lists the 9 sections and links preview.html; version badge 0.0.9.

## 0.0.8 (2026-06-11)

**DESIGN.md philosophy pass — agent-readable contract + contrast correction**

### Added
- README design philosophy: diagrams are treated as compact DESIGN.md artifacts with atmosphere, tokens, components, layout, and guardrails.
- DESIGN.md Agent-Readable Contract table, adapted from the awesome-design-md pattern.
- SKILL.md brief inference now explicitly checks the DESIGN.md contract before generation.
- CONTRIBUTING.md review gates for contract layer, target environment, contrast, and fallback.

### Fixed
- Warm Paper token mismatch: light warm surfaces now use dark ink text (`#1B365D`) instead of near-white text.
- Stone Mono text token now uses dark warm ink (`#292524`) instead of near-white text.
- SKILL.md quick reference and token table now match DESIGN.md contrast rules.

## 0.0.7 (2026-06-11)

**3D template hardening — animejs v4 gotchas + ground offset + dependency reference**

### Added
- **SKILL.md §16 GOTCHAS**: 6 Three.js + animejs v4 踩坑记录（CDN 路径、API 迁移、命名冲突、地面偏移、相机动画、光照限制）
- **templates/html/_archviz-deps.html**: CDN 依赖速查文件，含 animejs v4 shim 和使用示例
- **DESIGN.md 3D constraints**: +5 条（animejs v4 API/CDN、render loop 命名、ground offset、CDN 验证）

### Fixed
- **2D component breakdown.html**: 物体抬高 `dryer.position.y = 2`，修复埋入地面问题
- **animejs v4 CDN**: 3 个文件路径从 `lib/anime.es.js` 修正为 `dist/bundles/anime.esm.js`
- **animejs v4 API**: 3 个文件从 `anime({targets})` 迁移到 `tween(target, props)` 包装
- **render loop**: HTML Canvas-2D flow layout.html 函数名从 `animate` 改为 `renderLoop` 避免冲突

## 0.0.6 (2026-06-11)

**3D architectural visualization — Three.js + animejs integration**

### Added
- **DESIGN.md §3D Architectural Visualization**: 6 archviz types (structure shell / floor plan / interior / structural overlay / section cut / multi-floor nav), 3D tokens, constraints, 3D anti-patterns
- **SKILL.md 3D archviz mode**: environment routing (3D → Three.js self-contained HTML), stack spec (Three.js + animejs + OrbitControls), content type "spatial/3D"
- **2 Three.js templates**: `HTML Canvas-archviz.html` (building structure shell with section cut, wireframe toggle, camera presets), `HTML Canvas-2D flow layout.html` (multi-floor navigation with animejs transitions, explode view)
- **1 teaching example**: `2D floor layers-3d.html` (4层教学楼：门厅/教室/办公/屋顶，楼层切换+分解视图)
- **Triggers**: three.js, 3d, archviz, building, 2D flow layout, 建筑, 结构, 楼层, walkthrough, 漫游

### Changed
- **SKILL.md type selection table**: +3 rows for 3D (building structure, floor plan, section cut)
- **SKILL.md environment routing**: +3D/archviz row (Three.js self-contained HTML)
- **SKILL.md Brief Inference**: content type now includes "spatial/3D"

## 0.0.5 (2026-06-11)

**Teaching/academic chart gaps + anti-patterns + mixed-type strategy + real examples**

### Added
- **4 Mermaid templates**: `funnel.mmd`, `decision-matrix.mmd`, `state-machine.mmd`, `dependency-network.mmd`
- **2 teaching examples**: `course-admission-flow.mmd` (32门课程准入漏斗), `course-evaluation-matrix.mmd` (多维课程评价矩阵)
- **SKILL.md §14 ANTI-PATTERNS**: 15 student-work / common-mistake guards (pie abuse, rainbow nodes, dual Y-axis, truncated axis, emoji overload, etc.)
- **SKILL.md mixed types**: guidance for process+timeline, hierarchy+comparison, flow+metrics, decision+scoring — never >2 types per diagram
- **SKILL.md degradation strategy**: 5-step fallback when data is too complex (>50 nodes, >7 categories, mixed types, preview fails, syntax error)
- **DESIGN.md taxonomy**: funnel/conversion, decision/evaluation, state transitions, dependencies + data-shape heuristics

### Changed
- **SKILL.md Quick Reference**: type-selection table now routes funnel / decision / state / dependency to new templates, with Template column
- **Router triggers**: funnel, state diagram, decision matrix, 漏斗图, 状态机, 决策矩阵, 依赖图

## 0.0.4 (2026-06-11)

**Documentation accuracy + agent router support + identity cleanup + minor template hygiene**

### Removed
- Personal `hsueh` habit references in examples/templates → generic `Author habit` / `personal context`.

### Changed
- **SKILL.md frontmatter**: version 0.0.3 → 0.0.4; added `triggers` block (diagram, gantt, 可视化, 架构图 etc.) so routers (Antigravity, Grok skills, Claude, Hermes) can auto-activate without full path or exact name.
- **SKILL.md §12 TEMPLATES**: replaced hardcoded stale counts ("mermaid 8 / html 3 / python 2") with current accurate inventory (11/12/5) + explicit instruction: "read the specific template file under templates/<mode>/ at use time" and "do not hardcode counts".
- **README.md**: synced version badge and the category/count table to match reality.

### Fixed
- Agents following the old template list in SKILL.md would have a wrong mental model of available outputs (the root cause of "skill lies to the model").
- README table was also advertising outdated HTML=4 / Python=2.

### Notes
- references/ (gantt-rules, validation-checklist, style-guide) remain but are now largely duplicate of inlined content in SKILL + DESIGN. Consider pruning in a follow-up if you want the checkout leaner.
- Next hygiene targets (not in this patch): add root `requirements.txt` for python/ templates; make all html/ canvases responsive (see self-contained-html-viz.txt example); audit the other 11 HTML templates for the same fixed-pixel issue.

## 0.0.3 (2026-06-11)

**Full optimization pass: slim SKILL.md, dedup, restructure templates, add missing types**

### Changed
- **SKILL.md**: 473→244 lines (−48%). Added Quick Reference block (5-sec load). Moved detailed rules to DESIGN.md/references.
- **DESIGN.md**: 282→117 lines (−58%). Removed duplicate ASCII templates, Gantt details, env control. Focused on design system (tokens, taxonomy, patterns).
- **Templates restructured**: Flat → `mermaid/` `ascii/` `html/` `python/` subdirectories.

### Added
- **Missing chart types**: distribution.mmd, diverging-bar.mmd, network.mmd, treemap.html
- **Examples**: mermaid-demo.md, ascii-demo.txt, html-demo.html, python-demo.py
- **GitHub files**: CONTRIBUTING.md, .github/ISSUE_TEMPLATE/bug_report.md

### Removed
- Duplicate content between SKILL.md and DESIGN.md
- Verbose environment control sections (condensed to QR table)
- Duplicate ASCII templates from DESIGN.md (already in templates/ascii/)

## 0.0.2 (2026-06-10)

**anydesign integration + Gantt overflow prevention + ASCII mode**

### Added
- Layered Analysis (from anydesign): 4-layer with confidence levels (✅/⚠️/❓)
- DTCG-inspired token system with semantic naming
- Quality Rules (Do's/Don'ts)
- Contrast Rule (luminance-based)
- 5 Palette Presets
- Gantt text overflow prevention (codes only + table + ASCII)
- ASCII mode (box-drawing shapes, arrow semantics)
- Diagram Brief Inference (from taste-skill)
- Three Dials (COMPLEXITY / DENSITY / RESTRAINT)

## 0.0.1 (2026-05)

**Initial release**

### Added
- Core Mermaid diagram skill with restrained design
- Warm paper palette + guizang Swiss integration
- Template system (three-layer, warm-paper, 5d-scoring, 6duan-intro)
- DESIGN.md plain-text design system

## v0.3.0 (2026-06-13) — Phase 1-4 Upgrade

### Added
- Theme system: 4 palettes (Warm Paper, Swiss Neutral, Editorial Parchment, IKB Dark) with CSS variables, runtime toggle (T key), prefers-color-scheme auto-detect, localStorage persistence
- Export system: 4× raster PNG/SVG/WebP, clipboard copy, keyboard shortcuts (E→P/S/W/C), export menu UI
- Motion module: IntersectionObserver reveal, counterUp, drawSVGPath, staged reveal, reduced-motion support
- html-effectiveness corpus: 6 high-quality self-contained HTML samples (dashboard, comparison, process flow, KPI ticker, mini report, animated bars)
- animation-vocabulary.md: 10 semantic motion names, RESTRAINT dial mapping, anti-patterns
- export-patterns.md: 4× raster pipeline, dual-theme SVG, GitHub sanitizer, cross-platform test matrix

### Changed
- 16 HTML templates upgraded with theme + export modules integrated
- All canvas charts react to theme changes (archviz-theme-changed event)
- SKILL.md: 3D content split to archviz-3d, added skill boundary routing
- validation-checklist.md: 12 new export/theme check items
- preview.html: theme toggle integrated

### Removed
- 3D templates (HTML Canvas-archviz, HTML Canvas-2D flow layout, _archviz-deps) → moved to archviz-3d
- 3D examples (2D floor layers-3d, 2D component breakdown) → moved to archviz-3d

### Repository
- Renamed from archviz-skills to archviz
- GitHub: https://github.com/archsueh/archviz
