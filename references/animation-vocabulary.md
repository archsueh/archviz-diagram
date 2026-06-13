# 动画词汇表 / Animation Vocabulary

Shared motion vocabulary for archviz HTML templates. All semantic names below
map to exact CSS/JS properties — agents MUST use these names and durations
as-is. No deviation without updating RESTRAINT.

---

## 运动词汇表 / Motion Vocabulary Table

| 语义名 | Transform | Opacity | Easing | Duration |
|--------|-----------|---------|--------|----------|
| `rise-in-fast` | `translateY(20px → 0)` | `0 → 1` | `ease-out` | 300ms |
| `rise-in-slow` | `translateY(40px → 0)` | `0 → 1` | `ease-out` | 600ms |
| `fade-in` | none | `0 → 1` | `ease` | 400ms |
| `slide-in-left` | `translateX(-30px → 0)` | `0 → 1` | `ease-out` | 350ms |
| `slide-in-right` | `translateX(30px → 0)` | `0 → 1` | `ease-out` | 350ms |
| `scale-in` | `scale(0.8 → 1)` | `0 → 1` | `ease-out` | 400ms |
| `pop-in` | `scale(0 → 1.05 → 1)` | `0 → 1` | `cubic-bezier(0.34,1.56,0.64,1)` | 500ms |
| `stagger` | (applied to sequence) | — | — | 60ms per item |
| `draw-line` | SVG `stroke-dashoffset` | — | `linear` | length-dependent |
| `counter-up` | JS number interpolation | — | `ease-out` | 800ms default |

### 关键帧示例 / Keyframe Examples

```css
/* rise-in-fast */
@keyframes rise-in-fast {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.anim-rise-in-fast {
  animation: rise-in-fast 300ms ease-out forwards;
}

/* pop-in */
@keyframes pop-in {
  0%   { opacity: 0; transform: scale(0); }
  70%  { opacity: 1; transform: scale(1.05); }
  100% { opacity: 1; transform: scale(1); }
}
.anim-pop-in {
  animation: pop-in 500ms cubic-bezier(0.34,1.56,0.64,1) forwards;
}

/* stagger — apply per-item delay via JS */
[data-reveal] > * {
  opacity: 0;
  transform: translateY(20px);
}
[data-reveal].revealed > *:nth-child(1) { animation-delay: 0ms; }
[data-reveal].revealed > *:nth-child(2) { animation-delay: 60ms; }
/* ...generate nth-child rules via JS for n items */

/* draw-line (SVG) */
.draw-line path {
  stroke-dasharray: var(--path-length);
  stroke-dashoffset: var(--path-length);
  transition: stroke-dashoffset 800ms linear;
}
.draw-line.revealed path {
  stroke-dashoffset: 0;
}
```

---

## 分阶段揭示序列 / Staged Reveal Sequences

| 属性值 | 逻辑 | 适用场景 |
|--------|------|----------|
| `data-reveal` | 按 DOM 顺序依次进入（默认） | 表格行、列表 |
| `center-out` | 中间元素先出现，边缘最后 | 时间轴、对称布局 |
| `priority` | 高数值/高权重项先出现 | 排行榜、KPI 卡片 |
| `category` | 按分类分组，组内 stagger | 多维度仪表板 |

```js
// center-out 排序
function centerOutOrder(items) {
  const mid = Math.floor(items.length / 2);
  const left = [], right = [];
  items.forEach((el, i) => {
    if (i < mid) left.push({ el, i });
    else if (i > mid) right.push({ el, i });
    else { el.dataset.staggerIdx = 0; } // center = 0
  });
  left.reverse().forEach((item, j) => {
    item.el.dataset.staggerIdx = j + 1;
  });
  right.forEach((item, j) => {
    item.el.dataset.staggerIdx = j + 1;
  });
}
```

---

## 克制刻度映射 / RESTRAINT Dial Mapping

| RESTRAINT 值 | 允许的动画 | 最大单元素时长 | 允许 transform |
|---------------|-----------|---------------|----------------|
| **8–10** | `fade-in` only | 200ms | ❌ 无 |
| **5–7** | `rise-in` + `stagger` | 400ms | ✅ translateY only |
| **1–4** | 全编排（`scale-in`, `pop-in`, `draw-line`） | 800ms | ✅ 全部 |

**选择规则**：先读取上下文中的 RESTRAINT 值（默认 7），再查此表决定可用动画。
若 RESTRAINT 未定义，假设值为 7。

---

## 实现模式 / Implementation Patterns

### 模式 A：纯 CSS（推荐用于简单页面）

```js
// IntersectionObserver 触发 CSS transition
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('revealed');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
```

### 模式 B：animejs v4（推荐用于复杂编排）

```js
import { animate, stagger, onScroll } from 'animejs';

// CDN: https://cdn.jsdelivr.net/npm/animejs@4/dist/bundles/anime.esm.js
// UMD: https://cdn.jsdelivr.net/npm/animejs@4/dist/bundles/anime.umd.js

animate('.card', {
  y: [20, 0],
  opacity: [0, 1],
  ease: 'outExpo',
  duration: 400,
  delay: stagger(60),
  autoplay: onScroll({ threshold: 0.15 }),
});
```

### 模式 C：Canvas（requestAnimationFrame）

```js
// 自定义 easing 函数
const easeOutCubic = t => 1 - Math.pow(1 - t, 3);

function animateValue(from, to, duration, onFrame) {
  const start = performance.now();
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    onFrame(from + (to - from) * easeOutCubic(t));
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
```

---

## 禁忌 / Anti-Patterns

| ❌ 禁止 | 原因 |
|---------|------|
| 数据图表上使用无限循环动画 | 干扰数据读取，浪费 CPU |
| print / `@media print` 下触发动画 | 打印无意义，影响渲染 |
| 忽略 `prefers-reduced-motion` | 无障碍违规 |

```css
/* 强制规则 — 所有模板必须包含 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

@media print {
  * { animation: none !important; transition: none !important; }
}
```

**硬性限制**：任何单元素动画时长 ≤ 800ms。超时视为错误。
