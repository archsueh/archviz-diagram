"""
archviz-diagram MCP server — exposes flowchart and framework diagram tools for AI agents.

Run: .venv/bin/python -m archviz_diagram.mcp_server
Or: archviz-diagram serve (via CLI)

Tools:
  - archviz_diagram_generate: Generate a self-contained HTML flowchart or diagram
  - archviz_diagram_list_types: List all supported diagram types
  - archviz_diagram_list_palettes: List available color palettes
"""

import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .engine import render, list_types, list_palettes, get_palette

mcp = FastMCP("archviz-diagram")


@mcp.tool()
def archviz_diagram_generate(type: str, data: dict, options: dict | None = None) -> str:
    """Generate a self-contained HTML flowchart or diagram.

    Scope: this tool renders the self-contained HTML chart types only (the subset in
    the engine type registry). The wider archviz skill also covers Mermaid, ASCII, and
    Python (Plotly) output — those are produced from the skill docs/templates, not from
    this MCP tool. Call archviz_list_types() for the exact set this tool supports.

    Args:
        type: HTML chart type (stacked-bar, area-chart, line-chart, sunburst, treemap, radar, funnel, gauge, heatmap, bubble, waffle, waterfall, bullet-graph, editorial-card)
        data: Chart data (schema varies by type — call archviz_list_types for details)
        options: Optional overrides (theme: warm-paper|swiss-neutral|editorial-parchment|ikb-dark, title: str, restraint: 1-10)

    Returns:
        Complete self-contained HTML string. Save to .html and open in browser.
    """
    options = options or {}
    try:
        html = render(type, data, options)
        return html
    except (ValueError, FileNotFoundError) as e:
        return f"Error: {e}"


@mcp.tool()
def archviz_diagram_list_types() -> str:
    """List all supported diagram types with data schemas and examples.

    Returns detailed information about each chart type including:
    - Type name and description
    - Data schema (what fields are required)
    - Example data structure
    """
    types = list_types()
    result = []
    for t in types:
        result.append(f"### {t['type']}\n{t['description']}\n\n**Schema:**\n```json\n{json.dumps(t['schema'], indent=2, ensure_ascii=False)}\n```\n\n**Example:**\n```json\n{json.dumps(t.get('example', {}), indent=2, ensure_ascii=False)}\n```\n")
    return "\n".join(result)


@mcp.tool()
def archviz_diagram_list_palettes() -> str:
    """List available color palettes with their hex values.

    Returns palette definitions for: warm-paper, swiss-neutral, editorial-parchment, ikb-dark
    """
    palettes = {}
    for name in list_palettes():
        p = get_palette(name)
        if p:
            palettes[name] = {k: v for k, v in p.items() if k != "chart"}
    return json.dumps(palettes, indent=2)


def main():
    """Run the MCP server on stdio."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
