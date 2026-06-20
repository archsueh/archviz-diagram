"""
archviz rendering core — zero-dependency, template-driven flowchart and framework diagram engine.
Optional post-render compression via headroom CLI (separate venv).
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Any

# Resolve templates directory relative to this file
TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "html"
THEME_MODULE = TEMPLATES_DIR / "_archviz-theme.html"
EXPORT_MODULE = TEMPLATES_DIR / "_archviz-export.html"

# Headroom binary path (separate venv, keep engine zero-dep)
HEADROOM_CLI = Path.home() / "Developer" / "_envs" / "headroom" / "bin" / "headroom"

# === Type Registry ===
# Each type maps to a template file + data schema description
TYPE_REGISTRY = {
    "stacked-bar": {
        "template": "stacked-bar.html",
        "description": "Stacked bar chart — part-to-whole comparison across categories",
        "schema": {
            "labels": "list[str] — category labels (e.g. ['Q1','Q2','Q3','Q4'])",
            "datasets": "list[dict] — each has 'label', 'values' (list of numbers), optional 'color'",
        },
        "example": {
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [
                {"label": "Product", "values": [30, 35, 28, 40]},
                {"label": "Service", "values": [20, 25, 22, 18]},
                {"label": "Other", "values": [15, 10, 18, 12]},
            ],
        },
    },
    "area-chart": {
        "template": "area-chart.html",
        "description": "Area chart — cumulative trends over time",
        "schema": {
            "labels": "list[str] — time labels",
            "datasets": "list[dict] — each has 'label', 'data' (list of numbers), optional 'color'",
        },
        "example": {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
            "datasets": [
                {"label": "Series A", "data": [10, 25, 18, 32, 28, 45, 38, 52, 48, 60]},
                {"label": "Series B", "data": [5, 12, 20, 15, 28, 22, 35, 30, 42, 38]},
            ],
        },
    },
    "line-chart": {
        "template": "line-chart.html",
        "description": "Line chart — trends over time",
        "schema": {
            "labels": "list[str] — x-axis labels",
            "datasets": "list[dict] — each has 'label', 'data' (list of numbers), optional 'color'",
        },
        "example": {
            "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "datasets": [
                {"label": "Revenue", "data": [120, 200, 150, 80, 70, 110, 130]},
            ],
        },
    },
    "sunburst": {
        "template": "sunburst.html",
        "description": "Sunburst chart — hierarchical composition",
        "schema": {
            "name": "str — root label",
            "value": "number — root total",
            "children": "list[dict] — each has 'name', 'value', optional 'children' (nested), optional 'color'",
        },
        "example": {
            "name": "Root",
            "value": 100,
            "children": [
                {"name": "Product", "value": 45, "children": [
                    {"name": "A", "value": 25},
                    {"name": "B", "value": 20},
                ]},
                {"name": "Service", "value": 30},
                {"name": "Other", "value": 25},
            ],
        },
    },
    "treemap": {
        "template": "treemap.html",
        "description": "Treemap — part-to-whole, hierarchical composition",
        "schema": {
            "items": "list[dict] — each has 'label', 'value', optional 'color'",
        },
        "example": {
            "items": [
                {"label": "Product A", "value": 45},
                {"label": "Product B", "value": 25},
                {"label": "Product C", "value": 18},
                {"label": "Product D", "value": 12},
            ],
        },
    },
    "radar": {
        "template": "radar.html",
        "description": "Radar chart — multi-criteria comparison",
        "schema": {
            "axes": "list[str] — axis labels",
            "datasets": "list[dict] — each has 'label', 'values' (list of numbers 0-100), optional 'color'",
        },
        "example": {
            "axes": ["Speed", "Quality", "Cost", "Usability", "Scalability", "Design"],
            "datasets": [
                {"label": "Product A", "values": [80, 90, 60, 85, 70, 95]},
            ],
        },
    },
    "funnel": {
        "template": "funnel.html",
        "description": "Funnel chart — conversion/step visualization",
        "schema": {
            "steps": "list[dict] — each has 'label' and 'value'",
        },
        "example": {
            "steps": [
                {"label": "Visitors", "value": 10000},
                {"label": "Signups", "value": 3000},
                {"label": "Active", "value": 1200},
                {"label": "Paid", "value": 400},
            ],
        },
    },
    "gauge": {
        "template": "gauge.html",
        "description": "Gauge chart — single metric display",
        "schema": {
            "value": "number — current value",
            "max": "number — maximum value",
            "label": "str — metric name",
            "unit": "str — optional unit suffix",
        },
        "example": {"value": 73, "max": 100, "label": "Score", "unit": "%"},
    },
    "heatmap": {
        "template": "heatmap.html",
        "description": "Heatmap — matrix visualization",
        "schema": {
            "rows": "list[str] — row labels",
            "cols": "list[str] — column labels",
            "values": "list[list[number]] — 2D data matrix",
        },
        "example": {
            "rows": ["Mon", "Tue", "Wed"],
            "cols": ["9am", "12pm", "3pm", "6pm"],
            "values": [[10, 20, 30, 15], [25, 35, 40, 20], [15, 25, 35, 30]],
        },
    },
    "bubble": {
        "template": "bubble.html",
        "description": "Bubble chart — 3-variable comparison",
        "schema": {
            "items": "list[dict] — each has 'label', 'x', 'y', 'size', optional 'color'",
        },
        "example": {
            "items": [
                {"label": "A", "x": 30, "y": 50, "size": 20},
                {"label": "B", "x": 60, "y": 30, "size": 35},
                {"label": "C", "x": 45, "y": 70, "size": 15},
            ],
        },
    },
    "waffle": {
        "template": "waffle.html",
        "description": "Waffle chart — proportion visualization",
        "schema": {
            "segments": "list[dict] — each has 'label', 'value' (percentage), 'color'",
            "total_cells": "int — total grid cells (default 100)",
        },
        "example": {
            "segments": [
                {"label": "Product", "value": 45, "color": "#002FA7"},
                {"label": "Service", "value": 30, "color": "#94a3b8"},
                {"label": "Other", "value": 25, "color": "#a8a29e"},
            ],
        },
    },
    "waterfall": {
        "template": "waterfall.html",
        "description": "Waterfall chart — cumulative breakdown",
        "schema": {
            "items": "list[dict] — each has 'label', 'value' (positive or negative)",
        },
        "example": {
            "items": [
                {"label": "Revenue", "value": 100},
                {"label": "COGS", "value": -40},
                {"label": "Marketing", "value": -15},
                {"label": "Operations", "value": -20},
                {"label": "Profit", "value": 25, "is_total": True},
            ],
        },
    },
    "bullet-graph": {
        "template": "bullet-graph.html",
        "description": "Bullet graph — performance vs target",
        "schema": {
            "items": "list[dict] — each has 'label', 'value', 'target', 'ranges' (list of 3 numbers)",
        },
        "example": {
            "items": [
                {"label": "Revenue", "value": 85, "target": 90, "ranges": [60, 80, 100]},
            ],
        },
    },
    "editorial-card": {
        "template": "editorial-card.html",
        "description": "Editorial knowledge card — Swiss minimalist layout",
        "schema": {
            "kicker": "str — category label",
            "headline": "str — main title",
            "promise": "str — subtitle/promise",
            "evidence": "str — evidence cue",
            "evidence_value": "str — highlighted value",
            "dark_band": "str — optional dark band text",
            "footer": "str — footer caption",
        },
        "example": {
            "kicker": "Design System · 2024",
            "headline": "Primary judgment headline",
            "promise": "One supporting promise — what the reader gains.",
            "evidence": "one evidence cue only",
            "evidence_value": "42%",
            "dark_band": "Supporting context or code snippet",
            "footer": "Caption = finding · archviz",
        },
    },
}

# === Theme Palettes ===
PALETTES = {
    "warm-paper": {
        "surface": "#f5f0eb", "surface-alt": "#e8e4e0", "surface-raised": "#faf9f5",
        "text-primary": "#1B365D", "text-secondary": "#5e5d59", "text-tertiary": "#87867f",
        "border": "#d6d3d1", "accent": "#002FA7",
        "chart": ["#002FA7", "#94a3b8", "#a8a29e", "#d6d3d1", "#c96442", "#5e5d59"],
    },
    "swiss-neutral": {
        "surface": "#f8f8f6", "surface-alt": "#efeeec", "surface-raised": "#ffffff",
        "text-primary": "#1a1a18", "text-secondary": "#5f5e5a", "text-tertiary": "#88877f",
        "border": "#d9d8d4", "accent": "#185FA5",
        "chart": ["#185FA5", "#0F6E56", "#534AB7", "#993C1D", "#854F0B", "#5F5E5A"],
    },
    "editorial-parchment": {
        "surface": "#f5f4ed", "surface-alt": "#e8e6dc", "surface-raised": "#faf9f5",
        "text-primary": "#141413", "text-secondary": "#5e5d59", "text-tertiary": "#87867f",
        "border": "#c9c7bc", "accent": "#c96442",
        "chart": ["#c96442", "#5e5d59", "#87867f", "#b0aea5", "#141413", "#d6d3d1"],
    },
    "swiss-modernist": {
        "surface": "#ffffff", "surface-alt": "#f0f0f0", "surface-raised": "#ffffff",
        "text-primary": "#111111", "text-secondary": "#5e5d59", "text-tertiary": "#87867f",
        "border": "#111111", "accent": "#e4002b",
        "chart": ["#e4002b", "#111111", "#5e5d59", "#87867f", "#d6d3d1", "#f5f4ed"],
    },
    "vignelli-canon": {
        "surface": "#f4f1ea", "surface-alt": "#eae6db", "surface-raised": "#ffffff",
        "text-primary": "#0a0a0a", "text-secondary": "#5e5d59", "text-tertiary": "#87867f",
        "border": "#0a0a0a", "accent": "#f04e23",
        "chart": ["#f04e23", "#0a0a0a", "#5e5d59", "#87867f", "#d6d3d1", "#f5f4ed"],
    },
    "still-paper": {
        "surface": "#f5f4ed", "surface-alt": "#e8e6dc", "surface-raised": "#faf9f5",
        "text-primary": "#141413", "text-secondary": "#5e5d59", "text-tertiary": "#87867f",
        "border": "#c9c7bc", "accent": "#c96442",
        "chart": ["#c96442", "#5e5d59", "#87867f", "#b0aea5", "#141413", "#d6d3d1"],
    },
    "signal-proof": {
        "surface": "#f5f5f4", "surface-alt": "#e4e8f0", "surface-raised": "#ffffff",
        "text-primary": "#0a0a0a", "text-secondary": "#475569", "text-tertiary": "#64748b",
        "border": "#94a3b8", "accent": "#0039a6",
        "chart": ["#0039a6", "#475569", "#64748b", "#94a3b8", "#0a0a0a", "#e2e8f0"],
    },
    "bridge-canvas": {
        "surface": "#141413", "surface-alt": "#292524", "surface-raised": "#1c1917",
        "text-primary": "#e8e4e0", "text-secondary": "#a8a29e", "text-tertiary": "#78716c",
        "border": "#44403c", "accent": "#ffd500",
        "chart": ["#0d9488", "#d97706", "#e8e4e0", "#78716c", "#44403c", "#292524"],
    },
    "ikb-dark": {
        "surface": "#1a1a2e", "surface-alt": "#252540", "surface-raised": "#2a2a45",
        "text-primary": "#e8e6de", "text-secondary": "#b4b2a9", "text-tertiary": "#888780",
        "border": "rgba(255,255,255,0.15)", "accent": "#6B8AFF",
        "chart": ["#6B8AFF", "#5DCAA5", "#AFA9EC", "#F0997B", "#EF9F27", "#b4b2a9"],
    },
    "auto-time": {
        "surface": "auto", "surface-alt": "auto", "surface-raised": "auto",
        "text-primary": "auto", "text-secondary": "auto", "text-tertiary": "auto",
        "border": "auto", "accent": "auto",
        "chart": ["auto"],
    },
}


def list_types() -> list[dict]:
    """Return all supported visualization types with schemas and examples."""
    return [
        {"type": t, "description": info["description"], "schema": info["schema"], "example": info.get("example")}
        for t, info in TYPE_REGISTRY.items()
    ]


def render(viz_type: str, data: dict, options: dict | None = None) -> str:
    """
    Render a visualization as self-contained HTML.

    Args:
        viz_type: Visualization type (e.g. 'stacked-bar', 'sunburst', 'editorial-card')
        data: Chart data (schema varies by type)
        options: Optional overrides — theme, width, height, restraint, title, interactive

          compress: bool — If True, send payload through headroom compression and
                  replace the HTML with the compressed result.
                  Defaults to False; the engine remains zero-cost by default.
        Returns:
            Self-contained HTML string, optionally compressed.
    """
    if viz_type not in TYPE_REGISTRY:
        available = ", ".join(TYPE_REGISTRY.keys())
        raise ValueError(f"Unknown type '{viz_type}'. Available: {available}")

    options = options or {}
    template_info = TYPE_REGISTRY[viz_type]
    template_path = TEMPLATES_DIR / template_info["template"]

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    html = template_path.read_text(encoding="utf-8")

    # Inject data into template
    html = _inject_data(html, viz_type, data)

    # Apply theme overrides if specified
    if "theme" in options:
        html = _apply_theme(html, options["theme"])

    # Apply title override
    if "title" in options:
        html = re.sub(r"<title>.*?</title>", lambda m: f"<title>{options['title']}</title>", html, count=1)

    if options.get("compress"):
        html = _compress_text_via_headroom(_strip_html_for_compression(html), size_ratio=0.5)

    return html


def _inject_data(html: str, viz_type: str, data: dict) -> str:
    """Replace hardcoded data in template with user-provided data."""
    data_json = json.dumps(data, ensure_ascii=False)

    # Common pattern: find `const data = {...}` or `const data = [...]` and replace
    # Each template type has a different data variable name and structure

    if viz_type in ("stacked-bar", "area-chart", "line-chart"):
        # These use `const data = [...]` or `const series = [...]`
        # We need to construct the JS data structure from the simplified API
        labels = data.get("labels", [])
        datasets = data.get("datasets", [])

        if viz_type == "stacked-bar":
            # Convert to internal format: [{label, values: [...]}]
            js_data = json.dumps(
                [{"label": ds["label"], "values": ds["values"]} for ds in datasets],
                ensure_ascii=False,
            )
            html = re.sub(r"const data\s*=\s*\[.*?\];", lambda m: f"const data = {js_data};", html, flags=re.DOTALL)
            # Also replace colors array
            colors = []
            for ds in datasets:
                if "color" in ds:
                    colors.append(ds["color"])
            if colors:
                html = re.sub(r"const colors\s*=\s*\[.*?\];", lambda m: f"const colors = {json.dumps(colors, ensure_ascii=False)};", html, flags=re.DOTALL)

        elif viz_type in ("area-chart", "line-chart"):
            js_data = json.dumps(
                [{"label": ds["label"], "data": ds["data"], "color": ds.get("color", "")} for ds in datasets],
                ensure_ascii=False,
            )
            html = re.sub(r"const series\s*=\s*\[.*?\];", lambda m: f"const series = {js_data};", html, flags=re.DOTALL)

        # Replace labels
        if labels:
            html = re.sub(r"const labels\s*=\s*\[.*?\];", lambda m: f"const labels = {json.dumps(labels, ensure_ascii=False)};", html, flags=re.DOTALL)

    elif viz_type == "sunburst":
        html = re.sub(r"const data\s*=\s*\{.*?\};", lambda m: f"const data = {data_json};", html, flags=re.DOTALL)

    elif viz_type == "treemap":
        items = data.get("items", [])
        js_data = json.dumps(items, ensure_ascii=False)
        html = re.sub(r"const data\s*=\s*\[.*?\];", lambda m: f"const data = {js_data};", html, flags=re.DOTALL)

    elif viz_type == "radar":
        axes = data.get("axes", [])
        datasets = data.get("datasets", [])
        # Replace axes
        html = re.sub(r"const axes\s*=\s*\[.*?\];", lambda m: f"const axes = {json.dumps(axes, ensure_ascii=False)};", html, flags=re.DOTALL)
        # Replace datasets
        if datasets:
            html = re.sub(r"const datasets\s*=\s*\[.*?\];", lambda m: f"const datasets = {json.dumps(datasets, ensure_ascii=False)};", html, flags=re.DOTALL)

    elif viz_type == "funnel":
        steps = data.get("steps", [])
        html = re.sub(r"const steps\s*=\s*\[.*?\];", lambda m: f"const steps = {json.dumps(steps, ensure_ascii=False)};", html, flags=re.DOTALL)

    elif viz_type == "gauge":
        for key in ("value", "max", "label", "unit"):
            if key in data:
                val = json.dumps(data[key], ensure_ascii=False) if isinstance(data[key], str) else data[key]
                html = re.sub(rf"const {key}\s*=\s*[^;]+;", lambda m: f"const {key} = {val};", html, count=1)

    elif viz_type in ("heatmap", "bubble", "waffle", "waterfall", "bullet-graph", "editorial-card"):
        # Generic: replace `const data = {...}` with user data
        html = re.sub(r"const data\s*=\s*[\{{\[].*?[\}}\]];", lambda m: f"const data = {data_json};", html, flags=re.DOTALL)

    return html


def _apply_theme(html: str, theme_name: str) -> str:
    """Apply a named palette to the HTML."""
    if theme_name not in PALETTES:
        return html

    palette = PALETTES[theme_name]
    # Add data-palette attribute to <html> tag
    html = re.sub(r"<html([^>]*)>", lambda m: f'<html data-palette="{theme_name}"{m.group(1)}>', html, count=1)
    return html



def get_palette(name: str) -> dict | None:
    """Return palette definition by name."""
    return PALETTES.get(name)


def list_palettes() -> list[str]:
    """Return available palette names."""
    return list(PALETTES.keys())


# === Headroom compression integration (optional, zero default cost) ===
def _strip_html_for_compression(html: str) -> str:
    """Heuristic payload shrinker: extract data payload only, drop chrome/theme/script scaffolds.

    Headroom targets structured text (JSON, logs, tool outputs). This function attempts
    to surface the structured payload, not the chrome, before compression.
    """
    try:
        markers = [m.start() for m in re.finditer(r"const\s+(data|series|labels|steps|axes|datasets)\s*=\s*[\[{]", html)]
        if markers:
            start = markers[0]
            end = html.find("</script>", start)
            if end != -1:
                return "// Payload from archviz template\n" + html[start:end].strip()
    except Exception:
        pass
    return html


def _compress_text_via_headroom(text: str, size_ratio: float = 0.5) -> str:
    """Invoke headroom CLI via memory compression path.

    Falls back to raw text if headroom is not installed or returns non-zero.
    """
    if not HEADROOM_CLI.exists():
        return text
    try:
        env_dotenv = (Path.home() / ".headroom" / ".env")
        env = {}
        if env_dotenv.exists():
            for line in env_dotenv.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    env[key.strip()] = value.strip()
        cmd = [str(HEADROOM_CLI), "compress", "--stdin", f"--target-ratio={size_ratio}"]
        proc = subprocess.run(
            cmd,
            input=text,
            capture_output=True,
            check=False,
            env={**__import__("os").environ, **env},
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.decode("utf-8", errors="replace")
    except Exception:
        pass
    return text

