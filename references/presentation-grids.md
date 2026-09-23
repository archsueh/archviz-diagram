# 9c. ARCHVIZ PRESENTATION & GRIDS (Arcviz-Layout)

> 从 `SKILL.md` 原样迁出（2026-09-23 渐进式披露拆分），内容未删改。
> 何时加载：展板/作品集版式与网格、交付前打磨清单。做**展板类**交付物时加载（日常图表不需要）。

## 9c. ARCHVIZ PRESENTATION & GRIDS (Arcviz-Layout)

Trigger: 展板、作品集、画册、网格排版、A0/A1、Portfolio, or CSS Paged Media.

- **Layout Workflow**:
  1. **Understand**: List drawing list, text blocks, and constraints (A0 vertical vs A3 landscape).
  2. **Tune**: Select 1 of 3 visual languages: Still Paper (🌿 `#F5F4ED` + Terracotta), Signal Proof (⚡ `#F5F5F4`/`#E4E8F0` + Electric Blue), or Bridge Canvas (🎬 `#141413` + Teal/Gold).
  3. **Split**: Split layout into semantic narrative zones (e.g. concept -> master plan -> render -> details).
  4. **Layout**: Fit drawings/texts into grid columns. Focus on Image-First.
  5. **Verify**: Check flowlines, margins, runts, and contrast.
- **Grids & Hierarchy**:
  - Margins: A0 = `50-80mm`; Portfolio = `6%-8%` of short side.
  - Columns: A0 vertical = `3` or `6`; A0 horizontal = `4`, `8`, or `12`; A3/A4 landscape portfolio = `6` or `12`.
  - Gutters: A0 = `20mm`; Portfolio = `8-12mm`.
  - Asset mapping: Tier 1 (Hero render) $\ge 35\%$, Tier 2 (Master plan/Section) $\ge 20\%$, Tier 3 (Drawings) $\ge 15\%$, Tier 4 (Narratives/Diagrams) $\ge 10\%$, Tier 5 (Metadata) $\le 10\%$.
  - Air bubble: Keep $\ge 1$ grid unit whitespace around Tier 1 hero renders.
- **Card & Presentation Constraints**:
  - Safe zones: 16:9 (asymmetric 2/3 text, 1/3 image); 3:4 portrait (density $\ge 75\%$ height); 9:16 vertical (top 14% logo, middle 44%-52% title, bottom 20% + right 15% interactive safety area).
  - Web-to-print: Use asymmetric `@page :left` and `@page :right` for spine margins. Suppress headers on chapter start. Avoid orphans/widows/runts.
  - AI asset brand consistency: Reserve 1/3 text zone in prompts with preservation clause. Use canonical logo plate SVG/PNG with `inputImages` reference.

---
