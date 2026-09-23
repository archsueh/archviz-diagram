#!/usr/bin/env python3
"""archviz self_check — 生成物自检器（stdlib only，无第三方依赖）。

校验生成出来的 HTML/SVG 是否满足 archviz 的硬契约：
  a11y      无障碍 SVG 契约        → references/accessibility-contract.md
  safety    单文件安全 / 离线可用
  grid      4px 基网格与取值表      → references/grid-and-spacing.md
  contrast  对比度（WCAG AA 实算）
  geometry  连接线几何六铁律        → references/connector-geometry.md

用法:
    python3 scripts/self_check.py output/diagram.html
    python3 scripts/self_check.py --all examples/ templates/
    python3 scripts/self_check.py --only a11y output/diagram.html
    python3 scripts/self_check.py --json output/diagram.html
    python3 scripts/self_check.py --strict output/diagram.html      # WARN 也算失败
    python3 scripts/self_check.py --self-test                       # 检查这个检查器本身

基线模式（历史遗留豁免，新违规仍失败）:
    python3 scripts/self_check.py --all templates/ --write-baseline .self-check-baseline.json
    python3 scripts/self_check.py --all templates/ --baseline .self-check-baseline.json

退出码:
    0  通过（可能有 WARN，或全部被基线豁免）
    1  有 FAIL（含超出基线的新违规）
    2  用法错误 / 文件不可读
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Iterable, Iterator

# ─────────────────────────── 常量 ───────────────────────────

CATEGORIES = ("a11y", "safety", "grid", "contrast", "geometry")

FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")

ALLOWED_NODE_W = {80, 96, 112, 120, 128, 140, 160, 180, 200, 240, 320}
ALLOWED_NODE_H = {40, 44, 48, 56, 64, 72, 80, 96, 112, 128}
ALLOWED_RADIUS = {0, 4, 8}
MIN_FONT_SIZE = 9.0
MAX_FONT_TIERS = 4
TITLE_MAX = 60
DESC_MAX = 200

GEOMETRIC_WORDS = re.compile(
    r"(矩形|圆形|方形|上方|下方|左侧|右侧|箭头|线条|方块|"
    r"a rectangle|a circle|a square|above|below|to the left|to the right|"
    r"boxes? (?:are|is) (?:connected|drawn)|arrows? (?:are|is) drawn)",
    re.I,
)

EXEC_ATTRS = ("onclick", "onload", "onerror", "onmouseover", "onfocus", "srcdoc", "formaction")

# CDN 路径里带 @x / @x.y / @x.y.z 视为已锁版本；没有 @ 视为未锁（CDN 发新版即静默失效）
VERSION_PIN_RE = re.compile(r"@[^/?]*\d")


def is_version_pinned(url: str) -> bool:
    """判断 CDN URL 是否锁定了版本。

    只认路径里的 ``@`` 段且其中含数字（``mermaid@10`` ✓、``chart.js`` ✗）。
    查询串里的 ``?v=`` 不算 —— 那是缓存破坏参数，不是版本锁定。
    """
    return bool(VERSION_PIN_RE.search(url.split("?", 1)[0]))


# 判定「这份文本是不是 HTML/SVG」。旧实现要求文件**开头**就是 <!doctype 或含 <svg，
# 于是「首行是 HTML 注释 + 不含 <svg」的文件（webgl-info-viz.html、academic-table.html）
# 被整份跳过 —— 连带漏掉了它们真实的 onclick= 违规。改为按标记出现判定。
MARKUP_MARKERS = (
    "<!doctype", "<html", "<svg", "<body", "<div", "<span", "<table", "<tr",
    "<article", "<section", "<canvas", "<figure", "<button", "<style", "<p ", "<p>",
)


def looks_like_markup(text: str) -> bool:
    """文本里是否出现任一 HTML/SVG 标记（不要求出现在开头）。"""
    low = text.lower()
    return any(marker in low for marker in MARKUP_MARKERS)

# <script> 的内容是 JS，不是 HTML 属性/样式 —— 必须先剥掉再扫属性，否则会误报
SCRIPT_BODY_RE = re.compile(r"(<script\b[^>]*>)(.*?)(</script\s*>)", re.S | re.I)

# ─────────────────────────── 数据结构 ───────────────────────────


@dataclass
class Finding:
    level: str          # FAIL | WARN | INFO
    category: str
    rule: str           # 稳定标识，基线按它计数
    message: str
    file: str = ""
    where: str = ""

    def render(self) -> str:
        loc = f" [{self.where}]" if self.where else ""
        return f"  {self.level:<4} {self.category:<8} {self.message}{loc}"


@dataclass
class Report:
    file: str
    findings: list[Finding] = field(default_factory=list)
    checked: dict[str, int] = field(default_factory=dict)
    skipped: list[str] = field(default_factory=list)

    def add(self, level: str, category: str, rule: str, message: str, where: str = "") -> None:
        self.findings.append(Finding(level, category, rule, message, self.file, where))

    @property
    def fails(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "FAIL"]

    @property
    def warns(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "WARN"]


@dataclass
class Element:
    name: str
    attrs: dict[str, str]
    order: int
    parent_chain: tuple[str, ...]


# ─────────────────────────── 解析 ───────────────────────────

TAG_RE = re.compile(
    r"<(?P<name>[a-zA-Z][\w:.-]*)(?P<attrs>(?:\"[^\"]*\"|'[^']*'|[^>\"'])*?)(?P<close>/?)>",
    re.S,
)
ATTR_RE = re.compile(
    r"""([\w:.-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+))""",
    re.S,
)
SVG_RE = re.compile(
    r"<svg\b(?P<attrs>(?:\"[^\"]*\"|'[^']*'|[^>\"'])*?)>(?P<body>.*?)</svg\s*>", re.S | re.I
)
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr", "path", "circle", "rect", "line",
    "polygon", "polyline", "ellipse", "use", "stop",
}


def strip_script_bodies(html: str) -> str:
    """把 <script> 的内容清空，保留标签本身（以便仍能检查 src=）。"""
    return SCRIPT_BODY_RE.sub(lambda m: m.group(1) + m.group(3), html)


def parse_attrs(raw: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in ATTR_RE.finditer(raw or ""):
        key = m.group(1).lower()
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[key] = val or ""
    return out


def iter_elements(html: str) -> Iterator[Element]:
    stack: list[str] = []
    order = 0
    for m in TAG_RE.finditer(html):
        name = m.group("name").lower()
        if name.startswith("!"):
            continue
        yield Element(name, parse_attrs(m.group("attrs")), order, tuple(stack))
        order += 1
        if m.group("close") != "/" and name not in VOID_TAGS:
            stack.append(name)
            if re.search(rf"</{re.escape(name)}\s*>", html[m.end():], re.I) is None:
                stack.pop()


def find_elements(html: str, tag: str) -> list[Element]:
    return [e for e in iter_elements(html) if e.name == tag]


def split_svgs(html: str) -> list[tuple[dict[str, str], str, str]]:
    return [(parse_attrs(m.group("attrs")), m.group("body"), m.group(0))
            for m in SVG_RE.finditer(html)]


def svg_text(body: str, tag: str) -> str:
    m = re.search(rf"<{tag}\b[^>]*>(.*?)</{tag}\s*>", body, re.S | re.I)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


# ─────────────────────────── 颜色 ───────────────────────────

HEX_RE = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGB_RE = re.compile(r"rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)")
NAMED = {
    "white": "#ffffff", "black": "#000000", "red": "#ff0000", "green": "#008000",
    "blue": "#0000ff", "gray": "#808080", "grey": "#808080",
    "transparent": None, "none": None, "currentcolor": None, "inherit": None,
}


def parse_color(value: str | None, css_vars: dict[str, str]) -> tuple[int, int, int] | None:
    if not value:
        return None
    v = value.strip().lower()
    m = re.match(r"var\(\s*(--[\w-]+)\s*(?:,\s*(.+?))?\s*\)$", v)
    if m:
        resolved = css_vars.get(m.group(1))
        if resolved is None and m.group(2):
            resolved = m.group(2).strip()
        return parse_color(resolved, css_vars) if resolved else None
    if v in NAMED:
        nv = NAMED[v]
        return parse_color(nv, css_vars) if nv else None
    if v.startswith(("url(", "linear-gradient", "radial-gradient")):
        return None
    m = HEX_RE.match(v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    m = RGB_RE.match(v)
    if m:
        return int(float(m.group(1))), int(float(m.group(2))), int(float(m.group(3)))
    return None


def _lin(c: float) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_lum(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def extract_css_vars(html: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;{}]+);", html):
        out.setdefault(m.group(1), m.group(2).strip())
    return out


def extract_page_bg(html: str, css_vars: dict[str, str]) -> tuple[int, int, int]:
    for m in re.finditer(r"(?:^|[;{])\s*background(?:-color)?\s*:\s*([^;{}]+)", html, re.I):
        parts = m.group(1).split()
        c = parse_color(parts[0] if parts else None, css_vars)
        if c:
            return c
    for key in ("--av-surface", "--surface", "--paper", "--color-background-primary"):
        if key in css_vars:
            c = parse_color(css_vars[key], css_vars)
            if c:
                return c
    return (255, 255, 255)


# ─────────────────────────── 几何 ───────────────────────────

NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def num(attrs: dict[str, str], key: str, default: float | None = None) -> float | None:
    v = attrs.get(key)
    if v is None:
        return default
    m = NUM_RE.search(v)
    return float(m.group(0)) if m else default


def css_num(attrs: dict[str, str], prop: str) -> float | None:
    m = re.search(rf"{prop}\s*:\s*(-?[\d.]+)", attrs.get("style", ""))
    return float(m.group(1)) if m else None


def bbox(el: Element) -> tuple[float, float, float, float] | None:
    a = el.attrs
    if el.name == "rect":
        x, y = num(a, "x", 0.0), num(a, "y", 0.0)
        w, h = num(a, "width"), num(a, "height")
        return None if w is None or h is None else (x, y, x + w, y + h)
    if el.name == "circle":
        cx, cy, r = num(a, "cx", 0.0), num(a, "cy", 0.0), num(a, "r")
        return None if r is None else (cx - r, cy - r, cx + r, cy + r)
    if el.name == "ellipse":
        cx, cy, rx, ry = num(a, "cx", 0.0), num(a, "cy", 0.0), num(a, "rx"), num(a, "ry")
        return None if rx is None or ry is None else (cx - rx, cy - ry, cx + rx, cy + ry)
    return None


def overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def off_grid(v: float | None) -> bool:
    return False if v is None else abs(v - round(v / 4) * 4) > 0.01


# ─────────────────────────── 检查器 ───────────────────────────


def check_a11y(report: Report, html: str, stripped: str) -> None:
    # 只在剥掉 <script> 内容的版本上扫 —— 导出模块用 JS 模板字符串拼 <svg>（含
    # foreignObject）做 HTML→图片序列化，那不是文档里的图形，不适用无障碍契约。
    svgs = split_svgs(stripped)
    report.checked["a11y"] = len(svgs)
    if not svgs:
        report.add("INFO", "a11y", "a11y.no_svg", "文档里没有 <svg>，跳过无障碍检查")
        return

    for idx, (attrs, body, _raw) in enumerate(svgs, 1):
        where = f"svg#{idx}"
        role = attrs.get("role", "")
        labelled = attrs.get("aria-labelledby", "")
        aria_hidden = attrs.get("aria-hidden", "").lower() == "true"
        titles = find_elements(body, "title")
        descs = find_elements(body, "desc")

        if aria_hidden and not titles:
            continue
        if not titles and not labelled and not role:
            report.add("WARN", "a11y", "a11y.svg_untitled",
                       "svg 既无 <title> 也无 aria-hidden —— 装饰图形应标 aria-hidden，"
                       "信息图形应有 <title>", where)
            continue

        if role != "img":
            report.add("FAIL", "a11y", "a11y.missing_role",
                       f'svg 缺少 role="img"（当前 role="{role}"）', where)

        ids_in_svg = {e.attrs.get("id", "") for e in iter_elements(body)}
        ids_in_svg.discard("")
        title_ids = {t.attrs.get("id", "") for t in titles}
        if not labelled:
            report.add("FAIL", "a11y", "a11y.missing_labelledby", "svg 缺少 aria-labelledby", where)
        else:
            refs = [r for r in labelled.split() if r]
            dangling = [r for r in refs if r not in ids_in_svg]
            if dangling:
                report.add("FAIL", "a11y", "a11y.dangling_labelledby",
                           f"aria-labelledby 指向不存在的 id: {', '.join(dangling)}", where)
            elif titles and not any(r in title_ids for r in refs):
                report.add("FAIL", "a11y", "a11y.labelledby_not_title",
                           "aria-labelledby 没有指向本图的 <title>", where)

        if titles:
            first = next(iter_elements(body), None)
            if first is None or first.name != "title":
                got = first.name if first else "(空)"
                report.add("FAIL", "a11y", "a11y.title_not_first",
                           f"<title> 不是 <svg> 第一个子元素（第一个是 <{got}>）"
                           f" —— 位置错误可能被辅助技术忽略", where)
            tid = titles[0].attrs.get("id", "")
            if tid in ("title", ""):
                report.add("FAIL", "a11y", "a11y.title_id_bare",
                           f'<title> 的 id 是 "{tid or "(缺失)"}" —— 必须带图名前缀，'
                           f"否则同页多图会互相串名", where)
            text = svg_text(body, "title")
            if not text:
                report.add("FAIL", "a11y", "a11y.title_empty", "<title> 内容为空", where)
            elif len(text) > TITLE_MAX:
                report.add("FAIL", "a11y", "a11y.title_too_long",
                           f"<title> {len(text)} 字，超过 {TITLE_MAX} 字上限（应为主题短名）", where)

        if not descs:
            report.add("FAIL", "a11y", "a11y.missing_desc", "svg 缺少 <desc>", where)
        else:
            did = descs[0].attrs.get("id", "")
            if did in ("desc", ""):
                report.add("FAIL", "a11y", "a11y.desc_id_bare",
                           f'<desc> 的 id 是 "{did or "(缺失)"}" —— 必须带图名前缀', where)
            dtext = svg_text(body, "desc")
            if not dtext:
                report.add("FAIL", "a11y", "a11y.desc_empty", "<desc> 内容为空", where)
            else:
                if len(dtext) > DESC_MAX:
                    report.add("WARN", "a11y", "a11y.desc_too_long",
                               f"<desc> {len(dtext)} 字，超过 {DESC_MAX} 字（应为一句话）", where)
                if GEOMETRIC_WORDS.search(dtext):
                    report.add("WARN", "a11y", "a11y.desc_geometric",
                               "<desc> 像是在描述几何（含「矩形/上方/箭头」等词）"
                               "—— 应描述内容而非形状", where)


def check_safety(report: Report, html: str, stripped: str) -> None:
    checks = 0
    # 只扫剥掉 <script> 内容的版本 —— JS 里的 img.onload / url(blob) 不是 HTML 属性
    for m in re.finditer(r"<script\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", stripped, re.I):
        checks += 1
        url = m.group(1)
        if not url.startswith(("http://", "https://", "//")):
            continue
        # 契约原文（constitution.md）："zero external deps except verified minimal CDN"
        # → 锁了版本的 CDN 是「被允许但需确认」；没锁版本的 CDN 是必然失效，直接 FAIL。
        if is_version_pinned(url):
            report.add("WARN", "safety", "safety.remote_script_pinned",
                       f"引用了已锁版本的远程脚本: {url} —— 离线 / file:// 下会失效，"
                       f"交付前确认是否需内联")
        else:
            report.add("FAIL", "safety", "safety.remote_script",
                       f"引用了未锁版本的远程脚本: {url} —— CDN 发新版即静默失效，"
                       f"必须内联或锁定版本")
    for attr in EXEC_ATTRS:
        if re.search(rf"<[^>]*\b{attr}\s*=", stripped, re.I):
            checks += 1
            report.add("FAIL", "safety", "safety.exec_attr",
                       f"HTML 属性里出现可执行属性 {attr}= —— "
                       f"GitHub 清洗器会移除且无替代（export-patterns.md），必须改用 addEventListener")
    if re.search(r"@import\b", stripped, re.I):
        checks += 1
        report.add("FAIL", "safety", "safety.css_import", "CSS 使用了 @import —— 会引入外部依赖")
    for m in re.finditer(r"url\(\s*[\"']?([^\"')]+)", stripped, re.I):
        checks += 1
        u = m.group(1).strip()
        if u.startswith(("#", "data:")):
            continue
        report.add("FAIL", "safety", "safety.non_fragment_url",
                   f"CSS url() 指向非 fragment 资源: {u}")
    # <script src> 已由上面单独判定，这里先摘掉 script 开标签，避免同一处重复报两条
    no_script_tags = re.sub(r"<script\b[^>]*>", "", stripped, flags=re.I)
    for m in re.finditer(r"\b(?:src|href)\s*=\s*[\"'](https?:)?//([^\"'/]+)", no_script_tags, re.I):
        checks += 1
        host = m.group(2).lower()
        if host in FONT_HOSTS:
            continue
        report.add("FAIL", "safety", "safety.remote_resource",
                   f"引用了远程资源: {host}（仅允许字体 CDN {'/'.join(FONT_HOSTS)}）")
    report.checked["safety"] = checks


def check_grid(report: Report, html: str, stripped: str) -> None:
    checked = 0
    radii: set[float] = set()
    font_sizes: set[float] = set()

    for _attrs, body, _raw in split_svgs(stripped):
        for el in iter_elements(body):
            derived = "data-derived" in el.attrs
            if el.name == "rect" and "stroke" in el.attrs:
                checked += 1
                rx = num(el.attrs, "rx", 0.0)
                if rx is not None:
                    radii.add(round(rx, 2))
                if not derived:
                    for key in ("x", "y", "width", "height"):
                        v = num(el.attrs, key)
                        if off_grid(v):
                            report.add("WARN", "grid", "grid.off_grid",
                                       f"rect 的 {key}={v:g} 不在 4px 网格上",
                                       el.attrs.get("id", ""))
                    w, h = num(el.attrs, "width"), num(el.attrs, "height")
                    if w is not None and w not in ALLOWED_NODE_W:
                        report.add("WARN", "grid", "grid.width_not_allowed",
                                   f"rect 宽度 {w:g} 不在允许取值表内", el.attrs.get("id", ""))
                    if h is not None and h not in ALLOWED_NODE_H:
                        report.add("WARN", "grid", "grid.height_not_allowed",
                                   f"rect 高度 {h:g} 不在允许取值表内", el.attrs.get("id", ""))
            if el.name == "text":
                fs = num(el.attrs, "font-size")
                if fs is None:
                    fs = css_num(el.attrs, "font-size")
                if fs is not None:
                    checked += 1
                    font_sizes.add(round(fs, 1))
                    if fs < MIN_FONT_SIZE:
                        report.add("FAIL", "grid", "grid.font_too_small",
                                   f"字号 {fs:g}px 小于 {MIN_FONT_SIZE:g}px 下限")

    nonzero = {r for r in radii if r > 0}
    if len(nonzero) > 1 or (nonzero and 0 in radii):
        report.add("FAIL", "grid", "grid.radius_mixed",
                   f"同一张图混用了多种圆角 {sorted(radii)} —— 圆角是语义通道，不得混用")
    if len(font_sizes) > MAX_FONT_TIERS:
        report.add("WARN", "grid", "grid.font_tiers",
                   f"字号有 {len(font_sizes)} 档（{sorted(font_sizes)}），"
                   f"超过 {MAX_FONT_TIERS} 档上限")
    report.checked["grid"] = checked


def check_contrast(report: Report, html: str, stripped: str) -> None:
    """对比度检查。

    背景解析策略：对每个 <text>，用它自身的锚点坐标去找**包含该点的最小 rect**
    （最内层盒子）作为底色，而不是笼统地用「SVG 里第一个 rect」。
    这能正确处理「浅色文字压在深色 chip 上」这类情况；只有整图都没有可用 rect 时
    才退回页面底色。

    已知局限：不处理渐变填充、clip-path、opacity 叠加、以及文字溢出盒子边界的情况。
    """
    css_vars = extract_css_vars(html)
    page_bg = extract_page_bg(html, css_vars)
    checked = 0
    unresolved = 0

    for _attrs, body, _raw in split_svgs(stripped):
        # 收集所有带可解析填充色的 rect，按面积升序（便于取最内层）
        filled: list[tuple[float, tuple[float, float, float, float], tuple[int, int, int]]] = []
        for el in iter_elements(body):
            if el.name != "rect":
                continue
            c = parse_color(el.attrs.get("fill"), css_vars)
            if c is None:
                # style 里的 fill
                m = re.search(r"fill\s*:\s*([^;]+)", el.attrs.get("style", ""))
                c = parse_color(m.group(1), css_vars) if m else None
            if c is None:
                continue
            bb = bbox(el)
            if bb is None:
                continue
            area = (bb[2] - bb[0]) * (bb[3] - bb[1])
            filled.append((area, bb, c))
        filled.sort(key=lambda t: t[0])

        for el in iter_elements(body):
            if el.name != "text":
                continue
            fill_raw = el.attrs.get("fill")
            if fill_raw is None:
                m = re.search(r"fill\s*:\s*([^;]+)", el.attrs.get("style", ""))
                fill_raw = m.group(1) if m else None
            fg = parse_color(fill_raw, css_vars)
            if fg is None:
                unresolved += 1
                continue

            fs = num(el.attrs, "font-size")
            if fs is None:
                fs = css_num(el.attrs, "font-size") or 13.0

            # 文字的视觉中心点
            tx = num(el.attrs, "x", 0.0) or 0.0
            ty = num(el.attrs, "y", 0.0) or 0.0
            anchor = el.attrs.get("text-anchor", "start")
            if anchor == "middle":
                px = tx
            elif anchor == "end":
                px = tx - 10.0
            else:
                px = tx + 10.0
            py = ty - fs * 0.35

            # 找包含该点的最小 rect
            bg = page_bg
            for _area, bb, c in filled:
                if bb[0] <= px <= bb[2] and bb[1] <= py <= bb[3]:
                    bg = c
                    break

            need = 7.0 if fs <= 11 else 4.5
            ratio = contrast_ratio(fg, bg)
            checked += 1
            if ratio < need:
                label = (el.attrs.get("id") or "")[:24]
                report.add("FAIL", "contrast", "contrast.low",
                           f"对比度 {ratio:.2f}:1 低于 {need:g}:1（字号 {fs:g}px）"
                           f" fill={fill_raw} bg=rgb{bg}"
                           + (f" 文本 id={label}" if label else ""))

    report.checked["contrast"] = checked
    if unresolved:
        report.skipped.append(
            f"contrast: {unresolved} 个 text 的填充色无法解析"
            f"（currentColor / 未定义 CSS 变量 / 渐变），已跳过"
        )


def check_geometry(report: Report, html: str, stripped: str) -> None:
    checked = 0
    for _attrs, body, _raw in split_svgs(stripped):
        elements = list(iter_elements(body))
        checked += len(elements)

        for el in elements:
            if el.name == "line":
                x1, y1 = num(el.attrs, "x1"), num(el.attrs, "y1")
                x2, y2 = num(el.attrs, "x2"), num(el.attrs, "y2")
                if None in (x1, y1, x2, y2):
                    continue
                if abs(x1 - x2) >= 0.5 and abs(y1 - y2) >= 0.5:
                    report.add("FAIL", "geometry", "geometry.diagonal_line",
                               "斜线 <line>：两端 x/y 都不相同 —— 必须走圆角直角折线 (C1)")

        seen: dict[str, int] = {}
        for el in elements:
            if el.name == "path":
                d = re.sub(r"\s+", " ", el.attrs.get("d", "")).strip()
                if d:
                    seen[d] = seen.get(d, 0) + 1
        for d, count in seen.items():
            if count > 1:
                report.add("FAIL", "geometry", "geometry.duplicate_path",
                           f"{count} 条 <path> 的 d 完全相同 —— 连接线重叠 (C3): {d[:48]}…")

        boxes: list[tuple[int, tuple[float, float, float, float], str]] = []
        for el in elements:
            if el.name == "rect" and "stroke" in el.attrs:
                bb = bbox(el)
                if bb:
                    boxes.append((el.order, bb, el.attrs.get("id", "")))
        for el in elements:
            if el.name != "rect" or "stroke" in el.attrs:
                continue
            fill = (el.attrs.get("fill") or "").lower()
            if fill in ("none", "transparent", ""):
                continue
            bb = bbox(el)
            if not bb or (bb[2] - bb[0]) > 200 or (bb[3] - bb[1]) > 30:
                continue
            for border, bbb, bid in boxes:
                if border > el.order and overlaps(bb, bbb):
                    report.add("FAIL", "geometry", "geometry.label_mask_over_node",
                               "标签 mask 压住了后画的节点（会被节点填充裁掉）(C6)",
                               bid or f"rect@{border}")
                    break

        endpoints: dict[tuple[float, float], int] = {}
        for el in elements:
            if el.name != "path":
                continue
            for m in re.finditer(r"[ML]\s*(-?[\d.]+)[ ,]+(-?[\d.]+)", el.attrs.get("d", "")):
                key = (round(float(m.group(1)), 1), round(float(m.group(2)), 1))
                endpoints[key] = endpoints.get(key, 0) + 1
        for key, count in endpoints.items():
            if count > 2:
                report.add("WARN", "geometry", "geometry.shared_attach",
                           f"{count} 条连接线共用接点 {key} —— 应扇形展开 ≥12px 间距 (C4)")

    report.checked["geometry"] = checked


CHECKS = {
    "a11y": check_a11y,
    "safety": check_safety,
    "grid": check_grid,
    "contrast": check_contrast,
    "geometry": check_geometry,
}


def check_file(path: str, only: Iterable[str] | None = None) -> Report:
    report = Report(file=path)
    try:
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
    except OSError as exc:
        report.add("FAIL", "io", "io.unreadable", f"无法读取文件: {exc}")
        return report
    except UnicodeDecodeError:
        report.add("INFO", "io", "io.not_text", "非 UTF-8 文本，跳过（可能是二进制）")
        return report

    if not looks_like_markup(html):
        report.add("INFO", "io", "io.not_html", "看起来不是 HTML/SVG 文件，跳过")
        return report

    stripped = strip_script_bodies(html)
    for cat in (list(only) if only else list(CATEGORIES)):
        fn = CHECKS.get(cat)
        if fn:
            fn(report, html, stripped)
    return report


# ─────────────────────────── 基线 ───────────────────────────


def load_baseline(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_baseline(path: str, reports: list[Report], base_dir: str) -> None:
    files: dict[str, dict[str, int]] = {}
    for r in reports:
        counts = collections.Counter(f.rule for f in r.findings if f.level in ("FAIL", "WARN"))
        if counts:
            files[os.path.relpath(r.file, base_dir)] = dict(sorted(counts.items()))
    payload = {"version": 1, "files": files}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    total = sum(sum(v.values()) for v in files.values())
    print(f"已写入基线: {path}（{len(files)} 个文件 · {total} 项豁免）")


def apply_baseline(reports: list[Report], baseline: dict, base_dir: str) -> None:
    allowed_files = baseline.get("files", {})
    for r in reports:
        rel = os.path.relpath(r.file, base_dir)
        allowed = allowed_files.get(rel, {})
        seen: collections.Counter[str] = collections.Counter()
        kept: list[Finding] = []
        waived = 0
        for f in r.findings:
            if f.level in ("FAIL", "WARN"):
                seen[f.rule] += 1
                if seen[f.rule] <= allowed.get(f.rule, 0):
                    waived += 1
                    continue
            kept.append(f)
        r.findings = kept
        if waived:
            r.skipped.append(f"baseline: {waived} 项历史遗留已豁免（不在本次判定内）")


# ─────────────────────────── 输出 ───────────────────────────


def emit(report: Report, strict: bool, quiet: bool) -> bool:
    fails, warns = report.fails, report.warns
    passed = not fails and not (strict and warns)
    if quiet:
        return passed
    counts = " ".join(f"{k}={v}" for k, v in report.checked.items())
    print(f"[{'OK' if passed else 'FAIL'}] {report.file}" + (f"  ({counts})" if counts else ""))
    for f in report.findings:
        print(f.render())
    for s in report.skipped:
        print(f"  SKIP {s}")
    if not report.findings and not report.skipped:
        print("  所有检查通过")
    return passed


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="self_check",
        description="archviz 生成物自检器（无障碍 / 单文件安全 / 4px 网格 / 对比度 / 连接线几何）",
    )
    p.add_argument("files", nargs="*", help="待检查的 HTML/SVG 文件")
    p.add_argument("--all", nargs="+", metavar="PATH", help="递归检查目录下的 .html/.svg")
    p.add_argument("--only", nargs="+", choices=CATEGORIES, help="只跑指定分类")
    p.add_argument("--json", action="store_true", help="输出 JSON")
    p.add_argument("--strict", action="store_true", help="WARN 也算失败")
    p.add_argument("--quiet", action="store_true", help="只输出汇总行")
    p.add_argument("--self-test", action="store_true", help="检查这个检查器本身")
    p.add_argument("--baseline", metavar="FILE", help="按基线豁免历史遗留，只报新增违规")
    p.add_argument("--write-baseline", metavar="FILE", help="把当前结果写为基线")
    args = p.parse_args(argv)

    if args.self_test:
        return run_self_test()

    targets: list[str] = list(args.files)
    for root in args.all or []:
        if os.path.isfile(root):
            targets.append(root)
            continue
        for dirpath, _dirs, names in os.walk(root):
            if any(part in dirpath.split(os.sep) for part in (".git", "node_modules", ".venv")):
                continue
            for n in sorted(names):
                if n.lower().endswith((".html", ".htm", ".svg")):
                    targets.append(os.path.join(dirpath, n))

    if not targets:
        p.error("没有指定文件。用法: self_check.py <file> 或 --all <dir>")

    reports = [check_file(t, args.only) for t in targets]

    if args.write_baseline:
        base_dir = os.path.dirname(os.path.abspath(args.write_baseline)) or os.getcwd()
        write_baseline(args.write_baseline, reports, base_dir)
        return 0

    if args.baseline:
        if not os.path.exists(args.baseline):
            print(f"基线文件不存在: {args.baseline}\n"
                  f"先运行: self_check.py --all <dir> --write-baseline {args.baseline}",
                  file=sys.stderr)
            return 2
        base_dir = os.path.dirname(os.path.abspath(args.baseline)) or os.getcwd()
        apply_baseline(reports, load_baseline(args.baseline), base_dir)

    if args.json:
        payload = [{
            "file": r.file,
            "passed": not r.fails and not (args.strict and r.warns),
            "checked": r.checked,
            "skipped": r.skipped,
            "findings": [{"level": f.level, "category": f.category, "rule": f.rule,
                          "message": f.message, "where": f.where} for f in r.findings],
        } for r in reports]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if all(x["passed"] for x in payload) else 1

    ok = True
    for r in reports:
        if not emit(r, args.strict, args.quiet):
            ok = False

    if len(reports) > 1:
        n_fail = sum(1 for r in reports if r.fails)
        n_warn = sum(1 for r in reports if r.warns and not r.fails)
        print(f"\n汇总: {len(reports)} 个文件 · {len(reports) - n_fail - n_warn} 通过 · "
              f"{n_warn} 仅警告 · {n_fail} 失败")
    return 0 if ok else 1


# ─────────────────────────── 自测 ───────────────────────────

GOOD_SVG = """<!DOCTYPE html>
<html><head><style>:root{--av-surface:#f5f0eb;}</style></head><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="pipeline-title pipeline-desc">
  <title id="pipeline-title">订单履约链路</title>
  <desc id="pipeline-desc">订单从下单到签收经过库存、支付、风控三道校验，风控失败会旁路到人工复核。</desc>
  <defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
    <polygon points="0 0, 8 3, 0 6" fill="#a8a29e"/></marker></defs>
  <rect width="400" height="200" fill="#f5f0eb"/>
  <line x1="80" y1="100" x2="200" y2="100" stroke="#a8a29e" stroke-width="1" marker-end="url(#arrow)"/>
  <rect x="200" y="80" width="120" height="40" rx="0" fill="#ffffff" stroke="#1B365D" stroke-width="1"/>
  <text x="260" y="104" text-anchor="middle" font-size="13" fill="#1B365D">支付网关</text>
</svg></body></html>
"""

BAD_A11Y = """<html><body>
<svg viewBox="0 0 400 200">
  <defs><marker id="arrow"/></defs>
  <title id="title">A diagram</title>
  <desc id="desc">上方一个矩形，下方五个矩形，用箭头连接。</desc>
  <rect x="200" y="80" width="120" height="40" fill="#fff" stroke="#000"/>
  <text x="260" y="104" font-size="13" fill="#000">x</text>
</svg></body></html>
"""

BAD_GEOMETRY = """<html><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="g-title g-desc">
  <title id="g-title">Geometry</title>
  <desc id="g-desc">示例。</desc>
  <line x1="40" y1="40" x2="200" y2="160" stroke="#000"/>
  <rect x="40" y="40" width="80" height="40" rx="0" fill="#fff" stroke="#000"/>
  <rect x="200" y="120" width="80" height="40" rx="8" fill="#fff" stroke="#000"/>
</svg></body></html>
"""

BAD_SAFETY = """<html><head><style>@import url("https://evil.example/x.css");</style></head><body>
<svg viewBox="0 0 10 10" role="img" aria-labelledby="s-title s-desc">
  <title id="s-title">T</title><desc id="s-desc">D.</desc>
</svg>
<script src="https://cdn.example/x.js"></script>
<div onclick="alert(1)">x</div>
<img src="https://tracker.example/p.gif">
</body></html>
"""

BAD_CONTRAST = """<html><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="c-title c-desc">
  <title id="c-title">Contrast</title>
  <desc id="c-desc">低对比度示例。</desc>
  <rect width="400" height="200" fill="#ffffff"/>
  <text x="40" y="40" font-size="13" fill="#eeeeee">几乎看不见</text>
</svg></body></html>
"""

# 回归：首行是 HTML 注释、且不含 <svg 的 HTML —— 旧守卫会整份跳过，漏掉真实违规
SAFETY_COMMENT_HEAD_NO_SVG = """<!-- archviz template | 2026-06-28 -->
<!doctype html>
<html><head><title>Table</title><style>td{border:1px solid #ccc}</style></head>
<body>
<table><tr><td>a</td></tr></table>
<button onclick="exportPNG()">PNG</button>
</body></html>
"""

# 已锁版本的 CDN 脚本：契约允许（"verified minimal CDN"），只应 WARN 不应 FAIL
SAFETY_PINNED_CDN_OK = """<html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head><body>
<svg viewBox="0 0 10 10" role="img" aria-labelledby="p-title p-desc">
  <title id="p-title">Pinned</title><desc id="p-desc">锁版本的 CDN 示例。</desc>
</svg>
</body></html>
"""

# 回归：导出模块用 JS 模板字符串拼 <svg>（含 foreignObject）做 HTML→图片序列化，
# 那不是文档里的图形，无障碍契约不适用 —— 旧实现会对它误报 svg_untitled
A11Y_SVG_IN_SCRIPT_OK = """<html><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="sc-title sc-desc">
  <title id="sc-title">Real diagram</title>
  <desc id="sc-desc">文档里真正的图形，无障碍契约适用。</desc>
  <rect width="400" height="200" fill="#ffffff"/>
  <text x="40" y="40" font-size="13" fill="#1B365D">ok</text>
</svg>
<script>
  function serialize(target, w, h) {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">
      <foreignObject width="100%" height="100%">
        <div xmlns="http://www.w3.org/1999/xhtml">${target.outerHTML}</div>
      </foreignObject>
    </svg>`;
  }
</script>
</body></html>
"""

BAD_GRID = """<html><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="r-title r-desc">
  <title id="r-title">Grid</title>
  <desc id="r-desc">网格漂移示例。</desc>
  <rect x="41" y="43" width="123" height="46" rx="0" fill="#fff" stroke="#000"/>
  <rect x="200" y="43" width="120" height="44" rx="8" fill="#fff" stroke="#000"/>
  <text x="60" y="60" font-size="7" fill="#000">太小</text>
</svg></body></html>
"""

# 浅字压深色 chip —— 应通过（背景应解析为 chip 而非页面底色）
CONTRAST_CHIP_OK = """<html><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="chip-title chip-desc">
  <title id="chip-title">Chip</title>
  <desc id="chip-desc">浅色文字压在深色标签上，对比度充足。</desc>
  <rect width="400" height="200" fill="#ffffff"/>
  <rect x="40" y="40" width="120" height="40" rx="0" fill="#1B365D" stroke="#1B365D"/>
  <text x="100" y="64" text-anchor="middle" font-size="13" fill="#f5f0eb">深底浅字</text>
</svg></body></html>
"""

# 回归：文档里第一个 rect 是深色装饰条，文字实际在浅色底上 —— 旧实现会误报
CONTRAST_ORDER_REGRESSION = """<html><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="ord-title ord-desc">
  <title id="ord-title">Order</title>
  <desc id="ord-desc">顶部深色装饰条，正文在浅色底上。</desc>
  <rect x="0" y="0" width="400" height="20" fill="#1B365D" stroke="#1B365D"/>
  <rect width="400" height="200" fill="#f5f0eb"/>
  <text x="40" y="120" font-size="13" fill="#1B365D">在浅底上</text>
</svg></body></html>
"""

# JS 里的 img.onload / url(blob) 是合法代码，不得误报
JS_NOT_AN_ATTR = """<html><body>
<svg viewBox="0 0 400 200" role="img" aria-labelledby="js-title js-desc">
  <title id="js-title">Export</title>
  <desc id="js-desc">导出模块示例。</desc>
  <rect width="400" height="200" fill="#ffffff"/>
  <text x="40" y="40" font-size="13" fill="#111111">ok</text>
</svg>
<script>
  const img = new Image();
  img.onload = () => { canvas.toBlob(b => { const u = url(svgBlob); }); };
  img.onerror = () => {};
</script>
</body></html>
"""


def run_self_test() -> int:
    import tempfile

    cases: list[tuple[str, str, str | None, bool]] = [
        ("good", GOOD_SVG, "a11y", True),
        ("bad_a11y", BAD_A11Y, "a11y", False),
        ("bad_geometry", BAD_GEOMETRY, "geometry", False),
        ("bad_safety", BAD_SAFETY, "safety", False),
        ("bad_contrast", BAD_CONTRAST, "contrast", False),
        ("bad_grid", BAD_GRID, "grid", False),
        ("js_onload_not_attr", JS_NOT_AN_ATTR, "safety", True),
        ("js_onload_a11y_ok", JS_NOT_AN_ATTR, "a11y", True),
        ("contrast_chip_bg", CONTRAST_CHIP_OK, "contrast", True),
        ("contrast_rect_order", CONTRAST_ORDER_REGRESSION, "contrast", True),
        ("comment_head_onclick", SAFETY_COMMENT_HEAD_NO_SVG, "safety", False),
        ("pinned_cdn_warns_only", SAFETY_PINNED_CDN_OK, "safety", True),
        ("a11y_svg_in_script", A11Y_SVG_IN_SCRIPT_OK, "a11y", True),
    ]
    failures = 0
    with tempfile.TemporaryDirectory() as td:
        for name, content, category, should_pass in cases:
            path = os.path.join(td, f"{name}.html")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
            report = check_file(path, only=[category] if category else None)
            got_pass = not report.fails
            ok = got_pass == should_pass
            if not ok:
                failures += 1
            detail = ""
            if not ok:
                detail = " | ".join(f.message for f in report.fails[:2]) or "(无 FAIL)"
            print(f"  {'PASS' if ok else 'MISMATCH':<9} {name:<20} category={str(category):<9} "
                  f"期望{'通过' if should_pass else '失败'} 实际{'通过' if got_pass else '失败'}"
                  + (f"  ← {detail}" if detail else ""))

        # 基线机制自测：先写基线，再校验应全通过
        bpath = os.path.join(td, "baseline.json")
        rep = [check_file(os.path.join(td, "bad_a11y.html"))]
        write_baseline(bpath, rep, td)
        rep2 = [check_file(os.path.join(td, "bad_a11y.html"))]
        apply_baseline(rep2, load_baseline(bpath), td)
        base_ok = not rep2[0].fails
        if not base_ok:
            failures += 1
        print(f"  {'PASS' if base_ok else 'MISMATCH':<9} {'baseline_waives':<20} "
              f"category=baseline  期望通过 实际{'通过' if base_ok else '失败'}")

        # 新增违规必须穿透基线（追加一个必定 FAIL 的 svg：有 role 无 desc）
        with open(os.path.join(td, "bad_a11y.html"), "a", encoding="utf-8") as fh:
            fh.write('<svg viewBox="0 0 10 10" role="img" aria-labelledby="n-title">'
                     '<title id="n-title">N</title></svg>')
        rep3 = [check_file(os.path.join(td, "bad_a11y.html"))]
        apply_baseline(rep3, load_baseline(bpath), td)
        new_ok = bool(rep3[0].fails)
        if not new_ok:
            failures += 1
        print(f"  {'PASS' if new_ok else 'MISMATCH':<9} {'baseline_new_fails':<20} "
              f"category=baseline  期望失败 实际{'失败' if new_ok else '通过'}")

    print()
    total = len(cases) + 2
    if failures:
        print(f"自测失败: {failures}/{total} 个用例行为不符")
        return 1
    print(f"自测通过: {total}/{total} 个用例行为符合预期")
    return 0


if __name__ == "__main__":
    sys.exit(main())
