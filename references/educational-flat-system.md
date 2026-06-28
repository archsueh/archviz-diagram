# Educational Flat Mode Reference

"像教科书 / textbook-style" 教学图的默认模式。吸收自上游 concept-diagrams 的 9 色阶系统，适配 archviz 的 constitution 与 DESIGN.md。

## When to Use

- Physics, chemistry, biology, engineering 教学图
- 概念解释图（concept diagram）
- 用户明确说 "像教科书" / "textbook-style" / "teaching diagram"
- 用户说 "Educational Flat"

## Contrast Rule

Always compute:
```
luminance = 0.299 R + 0.587 G + 0.114 B
```

For dark fills (>128) use white text. For light fills (<128) use black text.

## Typography

- **Fonts:** system-ui, PingFang SC, Noto Sans SC (same stack)
- **Body:** 14px, weight 400
- **Label:** 12–13px, weight 500–600
- **Legend:** 12px
- **Caption:** 11–13px, weight 500, below diagram
- **Max label:** 8 Chinese chars

## Node Shapes (Flat Doctrine)

Flat fill only. No gradients, no shadows, no glassmorphism.

| Shape | Mermaid | Use |
|---|---|---|
| Rect (flat) | `[rect]` | Process, component, concept |
| Circle (flat) | `((circle))` | Emphasis, key concept |
| Stadium | `([stadium])` | Start/end, boundary |
| Diamond | `{diamond}` | Decision |
| Subroutine | `[[sub]]` | Sub-process |

Border: 1px `#000000` for normal, 2px ramp color for emphasized.

## Edge Styles

| Type | Style | Use |
|---|---|---|
| Solid | `----►` or `-->` | Main flow |
| Dashed | `- - -►` | Auxiliary / feedback |
| Dotted | `······►` | Conditional |
| Thick | `════►` | Single accent edge |

Legend required if >1 edge type appears.

## 9-Ramp Palette Usage

| Ramp key | Base hex | Light/medium/dark fills | Domain inference |
|---|---|---|---|
| `c-purple` | `#7C3AED` | `#EDE9FE` / `#DDD6FE` / `#7C3AED` | Math, abstract |
| `c-teal` | `#14B8A6` | `#CCFBF1` / `#99F6E4` / `#14B8A6` | Physics, energy, waves |
| `c-coral` | `#F97316` | `#FFEDD5` / `#FED7AA` / `#F97316` | Chemistry, reactions |
| `c-blue` | `#3B82F6` | `#DBEAFE` / `#BFDBFE` / `#3B82F6` | Engineering, structures |
| `c-green` | `#22C55E` | `#DCFCE7` / `#BBF7D0` / `#22C55E` | Biology, life cycles |
| `c-amber` | `#F59E0B` | `#FEF3C7` / `#FDE68A` / `#F59E0B` | Warning, attention |
| `c-red` | `#EF4444` | `#FEE2E2` / `#FECACA` / `#EF4444` | Error, danger, stop |
| `c-pink` | `#EC4899` | `#FDF2F8` / `#FBCFE8` / `#EC4899` | Highlight, emphasis |
| `c-gray` | `#6B7280` | `#F3F4F6` / `#E5E7EB` / `#6B7280` | Neutral, grouping |

**Rule:** exactly ONE ramp per diagram. Use black for secondary context, one ramp for the main subject. Never mix ramps in the same diagram.

**Auto inference:** no domain clue → ask one clarifying question. Do not guess.

## Hierarchy via Lightness Only

Use the same ramp's lightness scale to create depth:

- Background / container: lightest fill
- Secondary / supporting nodes: medium fill
- Primary / focus nodes: base + dark
- Emphasized single node: base + 2px border

This keeps hue discipline while still expressing importance visually.

## Mermaid Init Token

```
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#ffffff',
  'primaryTextColor':'#000000',
  'primaryBorderColor':'#000000',
  'lineColor':'#000000',
  'tertiaryColor':'#f3f4f6',
  'fontSize':'13px'
}}}%%
```

Subgraphs: 1px border, no fill, label size 12px.

## Anti-Patterns Specific to Educational Flat

1. ❌ Mix English display font with Chinese body font
2. ❌ More than ONE ramp color in one diagram
3. ❌ Gradients, shadows, glassmorphism
4. ❌ More than 8 Chinese chars in a label
5. ❌ Thin borders on light backgrounds
6. ❌ Emoji or decorative icons
7. ❌ ALL CAPS labels
8. ❌ Mix canvas-only or JS-only features (educational flat = static Mermaid/ASCII fallback)
9. ❌ Dark background with dark text
10. ❌ Rainbow legend >3 entries

## Output Contract

**YAML header:**
```yaml
---
diagram: [name]
type: [flowchart|mindmap|...]
context: textbook|lecture|exam
palette: Educational Flat / [ramp]
dials: {complexity: N, density: N, restraint: 9}
---
```

**Mandatory sections:**
1. One-sentence brief
2. Mermaid + ASCII fallback
3. Legend (if >2 edge types)
4. Caption stating the finding
