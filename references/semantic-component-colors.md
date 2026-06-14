# Semantic Component Colors

组件类型 → 语义色的固定映射。和 `monet-palette.md` / `wesanderson-palette.md` 的**美学**调色板分工不同：那些管"好不好看"，这张管"一眼看出这是什么组件"。技术架构/数据流图里，颜色承载语义，不是装饰。

消化自 archify（[tt-a1i/archify](https://github.com/tt-a1i/archify)）的 7 类语义配色，hex 对齐 archviz 的双主题 token 体系。

## 七类语义角色

| 角色 | 色系 | Light | Dark | 用途 |
|---|---|---|---|---|
| Frontend | 青 cyan | `#0891b2` | `#22d3ee` | 客户端 / UI / 终端设备 |
| Backend | 翠绿 emerald | `#059669` | `#34d399` | 服务 / API / 后台进程 |
| Database | 紫罗兰 violet | `#7c3aed` | `#a78bfa` | 数据库 / 存储 / AI·ML |
| Cloud | 琥珀 amber | `#d97706` | `#fbbf24` | 托管云服务 / 基础设施 |
| Security | 玫红 rose | `#e11d48` | `#fb7185` | 鉴权 / 安全组 / 加密 |
| Message Bus | 橙 orange | `#ea580c` | `#fb923c` | Kafka / 队列 / 事件总线 |
| External | 石灰 stone | `#78716c` | `#a8a29e` | 第三方 / 通用外部系统 |

每类的 light/dark 配对随 `data-theme` 同步切换，配色逻辑见 `dark-mode-tokens.md`。

## CSS 语义类（HTML/SVG 模板用）

节点引用语义 class，不写死 `fill`。切主题只改 `:root` 变量，整图跟着变。

```css
:root {
  --c-frontend: #0891b2; --c-backend: #059669; --c-database: #7c3aed;
  --c-cloud: #d97706;    --c-security: #e11d48; --c-msgbus:  #ea580c;
  --c-external: #78716c;
}
@media (prefers-color-scheme: dark) {
  :root {
    --c-frontend: #22d3ee; --c-backend: #34d399; --c-database: #a78bfa;
    --c-cloud: #fbbf24;    --c-security: #fb7185; --c-msgbus:  #fb923c;
    --c-external: #a8a29e;
  }
}
.c-frontend { fill: var(--c-frontend); }
.c-backend  { fill: var(--c-backend); }
/* …其余同理 */
```

Mermaid 用 `classDef`：`classDef frontend fill:#0891b2,stroke:#0e7490,color:#fff;`，深色模式整套换 dark 列。

## 与 archviz 既有规则的调和（不要照搬 archify）

- **"Max 1 accent" vs 7 类语义色**：单色调强调（accent）规则管的是**装饰性高亮**——一张图最多一个抓眼强调点。语义色是**功能性图例**，7 类各司其职、图里有 legend 说明，不算 accent。两者不冲突：语义色铺底，accent 仍只给"主路径/关键节点"一个。
- **"No AI-purple" vs Database 用紫**：被禁的是那种当万能装饰的 slop 紫（`#8b5cf6` 糊一切）。这里紫是 7 选 1 的**数据库类别色**，有明确语义和图例，是刻意选择，允许。别用紫做无意义强调。
- **Editorial / Parchment 模式禁冷灰**：External 默认用暖石灰 `#78716c`/`#a8a29e`（stone 系），本身就暖，进 editorial 模式可直接用；其余冷色系（cyan/violet）在 editorial 模式应降饱和或换 `editorial-parchment-language.md` 的暖映射。
- **同文档同图例**：一份交付里语义色一次定义、全程复用。换一张图不要换映射。

## 何时用 / 何时不用

- **用**：架构图、数据流图、组件拓扑——颜色要表达"这是什么"。配合 `diagram-types-technical.md` 的五类图。
- **不用**：纯美学卡片、封面、editorial 排版——那些走 monet/wesanderson/parchment，颜色表达情绪不表达类别。
