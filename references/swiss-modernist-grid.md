# Swiss Modernist & Vignelli Canon Grid Systems

This reference distills the typesetting and visual layout discipline of **Josef Müller-Brockmann** (modular grid systems, baseline grids, Helvetica typography, optical alignment) and **Massimo Vignelli** Distilled Canon (semantics/syntactics/pragmatics, Helvetica, primary color as identifier, rulers, two-size scale). Use this when the user requests Swiss modernism, editorial grid systems, transit wayfinding signage, or high-fidelity page typesetting.

---

## 1. Core Principles (The Discipline)

| Principle | Meaning for archviz |
|---|---|
| **Objective Order** | The grid organizes the page; the system (not the designer's ego) decides layout. Asymmetric compositions held in tension. |
| **Flush-Left Sans** | Grotesque typography (Helvetica / Inter / Liberation Sans) flush-left, ragged-right. **Never justify** text. |
| **Max Two Sizes** | Limit typography to two active sizes per page (heading ≈ 2× body). Scale and weight provide contrast, not size chaos. |
| **Primary Color as Identifier** | Accent colors identify structure or branding, not decoration. Canon Vermilion (`#f04e23`), Swiss Red (`#e4002b`), or Signal Blue (`#0039a6`). Max 1 accent. |
| **Type Hangs from Rulers** | Use hairline dividers (0.5–2pt) as structured anchors. Type sits directly under or hangs from these rulers. |
| **Generous Silence** | White space is the protagonist. Do not clutter modules. |

---

## 2. Load-Bearing Web Grid Engineering

To make modular grids load-bearing on the web and prevent typical alignment bugs:

### 2.1 One Source of Truth
Define all grid variables under `:root` in CSS. Never hardcode margins/gutters separately in subcomponents:
```css
:root {
  --cols: 12;
  --bl: 8px;                       /* Baseline unit */
  --lh: 24px;                      /* Leading = 3 x Baseline */
  --gutter: 24px;                  /* Gutter (multiple of baseline) */
  --margin: 72px;                  /* Margin (multiple of baseline) */
  --maxw: 1296px;                  /* Max page width */
  --paper: #ffffff;
  --ink: #111111;
  --accent: #e4002b;               /* Swiss Red */
}
```

### 2.2 Content-Box Overlay (Prevent Viewport Drift)
**The Pitfall**: Placing the grid-toggle overlay as a full-width viewport sibling to centered content. On viewports wider than `--maxw`, centered content alignment drifts relative to the overlay.
**The Fix**: Place the `.guides` overlay **inside the same wrapper** as the content, and draw column lines utilizing the exact same CSS variables:
```css
.guides {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 100;
  opacity: 0;
  transition: opacity 0.25s ease;
}
body.grid-on .guides { opacity: 1; }

.guides .cols {
  position: absolute;
  top: 0;
  bottom: 0;
  left: var(--margin);
  right: var(--margin);
  display: grid;
  grid-template-columns: repeat(var(--cols), 1fr);
  column-gap: var(--gutter);
}
.guides .col {
  background: rgba(228, 0, 43, 0.05);
  box-shadow: inset 1px 0 0 rgba(228, 0, 43, 0.25), inset -1px 0 0 rgba(228, 0, 43, 0.25);
}
```

### 2.3 Subgrid Bands (Element Placement)
Instead of eyeballing column offsets, span elements along column lines utilizing grid-column lines:
```css
.grid {
  display: grid;
  grid-template-columns: repeat(var(--cols), 1fr);
  column-gap: var(--gutter);
  row-gap: var(--lh);
}

.band {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: subgrid;
  column-gap: var(--gutter);
  align-items: start;
}
@supports not (grid-template-columns: subgrid) {
  .band { grid-template-columns: repeat(var(--cols), 1fr); }
}

/* Placed strictly on grid column lines */
.text-module { grid-column: 1 / 6; }
.image-module { grid-column: 6 / 13; }
```

### 2.4 Baseline Rhythm Lock
- **Line Heights**: Always px-multiples of `--bl` (e.g., `line-height: var(--lh)`). **Never use unitless line-heights for large display type** (e.g. `line-height: 1.2`), as it introduces rounding drift.
- **Spacing**: Margins, paddings, gaps must be multiples of `--bl`.
- **Media Heights**: Set media elements (images/videos) to px heights that are multiples of `--lh` (e.g., 240px, 360px) so both the top and bottom edge align perfectly to baselines.

### 2.5 Optical Alignment (Ink-on-Line, Not Box-on-Line)
Large display letterforms have a left side-bearing built into the font file. A headline placed exactly at column line 1 will look visually misaligned (indented). 
Solve this in the browser by measuring glyph side-bearings via Canvas and applying a negative margin nudge:
```javascript
(function() {
  const cvs = document.createElement('canvas'), ctx = cvs.getContext('2d');
  const sel = '.masthead, .numeral, .shead h2, .v-display-title';
  function align() {
    document.querySelectorAll(sel).forEach(el => {
      el.style.marginLeft = '0px';
      const cs = getComputedStyle(el);
      let ch = (el.textContent || '').trim().charAt(0);
      if (!ch) return;
      if (cs.textTransform === 'uppercase') ch = ch.toUpperCase();
      ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
      ctx.textAlign = 'left';
      const abl = ctx.measureText(ch).actualBoundingBoxLeft; // positive means ink overhangs left
      if (isFinite(abl)) {
        el.style.marginLeft = `${(-abl).toFixed(2)}px`; // nudge left so ink touches line
      }
    });
  }
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(align);
  }
  align();
  window.addEventListener('resize', align);
})();
```

---

## 3. Production & Headless Rendering (Helvetica Fallback Trap)

When exporting layouts to PDF/PNG in headless environments (e.g., Puppeteer, Playwright):
- **The Issue**: Standard fonts like Helvetica/Neue Haas Grotesk are often missing. The browser silently falls back to Noto Sans or Arial, causing column/baseline offsets to drift.
- **The Fix**: Prioritize **Liberation Sans** (exact metric-compatible grotesque) in the font-family declaration:
  ```css
  font-family: "Helvetica Neue", Helvetica, Arial, "Liberation Sans", sans-serif;
  ```
- **Webfont Embedding**: For bulletproof verification, embed the font as an base64 or local TTF `@font-face` within the stylesheet.

---

## 4. Wayfinding & Signage Logic (Massimo Vignelli)

For wayfinding signage models and transit layouts, follow Vignelli's Grandi Stazioni guidelines:
1. **Color Scheme**: White Helvetica on a signal-blue panel (`#0039a6`).
2. **Layout**: Flush-left text. Pictograms and navigation arrows must share the exact height (cap-box) of the uppercase letters.
3. **Platform Flags**: Large double-sided square flag with platform number centered.
4. **Hierarchy**: Hanging elements below a 2pt rule for secondary information.
