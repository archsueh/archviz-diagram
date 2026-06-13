# Export Patterns 参考手册

## 导出流水线架构

三级降级策略，优先级从高到低：

```
1. SVG 原生导出 ──→ 直接序列化 DOM，零损失
2. Canvas 重渲染 ──→ 用 JS 重绘 SVG 到 <canvas>，可控制像素
3. html2canvas 降级 ──→ 截屏式捕获，兼容性兜底
```

```js
async function exportImage(svgEl, opts = {}) {
  try {
    return exportSVGNative(svgEl);              // 最优
  } catch {
    try {
      return await exportViaCanvas(svgEl, opts); // 可控
    } catch {
      return await exportHtml2canvas(svgEl);      // 兜底
    }
  }
}
```

## 4× 栅格化技术

核心：**放大的是 viewBox，不是位图**。SVG 内部坐标不变，输出分辨率翻 4 倍。

```js
function svgToRaster(svgEl, scale = 4) {
  const vb = svgEl.viewBox.baseVal;
  const w = vb.width;
  const h = vb.height;
  const canvas = document.createElement('canvas');
  canvas.width = w * scale;
  canvas.height = h * scale;
  const ctx = canvas.getContext('2d');

  const clone = svgEl.cloneNode(true);
  clone.setAttribute('width', w * scale);
  clone.setAttribute('height', h * scale);
  // viewBox 不变 → 内容自动缩放

  const blob = new Blob([clone.outerHTML], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const img = new Image();
  img.src = url;
  return new Promise(resolve => {
    img.onload = () => {
      ctx.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);
      resolve(canvas);
    };
  });
}
```

## 双主题 SVG 策略

三种方案，按场景选择：

### 方案 A：@media 适配（推荐，单文件）

```css
/* SVG 内嵌样式 */
@media (prefers-color-scheme: dark) {
  .bg { fill: #1a1a2e; }
  .text { fill: #e0e0e0; }
}
@media (prefers-color-scheme: light) {
  .bg { fill: #ffffff; }
  .text { fill: #1a1a2e; }
}
```

### 方案 B：双文件输出

```bash
diagram-light.svg  # 固定浅色
diagram-dark.svg   # 固定深色
```

适合：GitHub README（不支持 @media 切换）。

### 方案 C：Host CSS 变量穿透

```svg
<svg xmlns="http://www.w3.org/2000/svg">
  <style>
    .node { fill: var(--arch-node, #4a90d9); }
  </style>
  ...
</svg>
```

宿主页面通过 `:root { --arch-node: #e74c3c; }` 控制。仅内嵌 `<object>` / `<iframe>` 时有效，`<img>` 标签不继承。

## GitHub SVG 清洗器行为

GitHub 渲染 SVG 时会 **strip** 以下内容：

| 被移除 | 替代方案 |
|---|---|
| `<script>` | 无，必须去掉 |
| `<foreignObject>` | 改用 `<text>` |
| `onclick` 等事件 | 无 |
| 外部 `href` (http) | 内联 data URI |
| CSS `@import` | 内联 `<style>` |
| `<use>` 跨文件引用 | 内联复制 |

**工作区**：输出前运行 sanitize 预检，确认 GitHub 渲染一致。

## 剪贴板 API 兼容

```js
async function copyToClipboard(canvas) {
  if (window.ClipboardItem) {
    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
    await navigator.clipboard.write([
      new ClipboardItem({ 'image/png': blob })
    ]);
  } else {
    // Fallback：下载文件
    const a = document.createElement('a');
    a.download = 'export.png';
    a.href = canvas.toDataURL('image/png');
    a.click();
  }
}
```

兼容性：ClipboardItem 仅 Chromium 76+、Safari 13.1+。Firefox 127+ 才支持。

## 键盘快捷键设计

原则：**单键触发高频操作，两键组合触发低频操作**。

```
T       → 切换主题 (light/dark)
E       → 导出当前视图
Shift+E → 导出 4× 高清
Ctrl+E  → 复制到剪贴板 (macOS: ⌘E)
?       → 显示快捷键提示
```

实现注意：焦点在输入框时禁用，用 `event.target.tagName` 判断。

## 跨平台测试矩阵

| 环境 | SVG | PNG | 备注 |
|---|---|---|---|
| Chrome 120+ | ✅ | ✅ | 基准 |
| Safari 17+ | ✅ | ✅ | font-family fallback 注意 |
| Firefox 121+ | ✅ | ⚠️ | ClipboardItem 晚期支持 |
| `file://` | ⚠️ | ❌ | CSP 阻止 canvas |
| `http-server` | ✅ | ✅ | 开发基准 |
| GitHub README | ✅ | — | 需 sanitize |
| Obsidian 预览 | ✅ | — | `<img>` 标签加载 |
| 微信公众号 | ❌ | ✅ | 必须用 PNG，SVG 被过滤 |

## 已知坑

### CSP 阻止 html2canvas
`Content-Security-Policy` 设置了 `img-src` 限制时，html2canvas 的 data URI 转换会静默失败。
→ 解决：检测 CSP，降级为 canvas 手绘。

### 字体 fallback
SVG 内嵌的 `font-family: "Inter"` 在导出环境可能不存在。
→ 解决：导出前 `@font-face` 内联 base64，或 fallback 到 `system-ui, sans-serif`。

### Canvas DPR 问题
`canvas.toBlob()` 输出的 DPI 固定 96，不跟随 `devicePixelRatio`。
→ 解决：手动 `ctx.scale(dpr, dpr)`，并在 PNG 元数据中写入 pHYs chunk（需要库支持）。

### Safari SVG 渲染差异
Safari 对 `dominant-baseline`、`text-anchor` 的渲染与 Chrome 有 1-2px 偏移。
→ 解决：关键对齐用 `dy` 手动微调，不依赖 baseline 属性。
