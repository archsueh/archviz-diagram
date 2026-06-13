# html-effectiveness — Sample Corpus

Six self-contained HTML examples demonstrating high-quality data visualization patterns. Each file uses the archviz theme system, works standalone (zero dependencies), and stays under 200 lines.

| # | File | Teaches |
|---|------|---------|
| 1 | `data-dashboard.html` | Combining KPI cards + bar chart in a CSS grid layout |
| 2 | `comparison-cards.html` | Side-by-side decision cards with accent highlight for recommended option |
| 3 | `process-flow.html` | Horizontal step-by-step flowchart using flexbox (no SVG) |
| 4 | `kpi-ticker.html` | Editorial large-number display with animated counter + CSS sparkline |
| 5 | `mini-report.html` | Compact report mixing prose, data table, and callout block |
| 6 | `animated-bar-race.html` | Bar chart with CSS transition animation triggered by IntersectionObserver |

## Shared conventions

- **Theme**: `:root` light + `.dark` override using `--av-*` CSS variables
- **Toggle**: every file includes a ◐ Theme button (top-right corner)
- **Typography**: `Noto Sans SC` → `system-ui` fallback stack
- **No dependencies**: no CDN, no build step, no external assets
- **Timestamp**: first line comment `<!-- archviz-skills html-effectiveness sample | 2026-06-13 -->`
