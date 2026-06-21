"""
archviz-diagram CLI — command-line interface for the flowchart and diagram engine.

Usage:
    archviz-diagram list                          # List all diagram types
    archviz-diagram list-palettes                 # List color palettes
    archviz-diagram render --type stacked-bar --data data.json --output chart.html
    archviz-diagram render --type stacked-bar --data data.json --theme ikb-dark --output chart.html
    archviz-diagram serve                         # Start MCP server
"""

import argparse
import json
import sys
from pathlib import Path

from .engine import render, list_types, list_palettes, get_palette


def cmd_list(args):
    """List all visualization types."""
    types = list_types()
    for t in types:
        print(f"  {t['type']:20s} {t['description']}")
    print(f"\n{len(types)} types available.")


def cmd_list_palettes(args):
    """List color palettes."""
    for name in list_palettes():
        p = get_palette(name)
        if p:
            print(f"  {name:25s} surface={p['surface']}  accent={p['accent']}")


def cmd_render(args):
    """Render a visualization to HTML."""
    # Load data
    if args.data == "-":
        data = json.load(sys.stdin)
    elif args.data:
        data_path = Path(args.data)
        if not data_path.exists():
            print(f"Error: data file not found: {args.data}", file=sys.stderr)
            sys.exit(1)
        data = json.loads(data_path.read_text(encoding="utf-8"))
    else:
        # Use example data from registry
        types = {t["type"]: t for t in list_types()}
        if args.type in types and "example" in types[args.type]:
            data = types[args.type]["example"]
            print(f"Using example data for {args.type}", file=sys.stderr)
        else:
            print(f"Error: --data required (no example available for {args.type})", file=sys.stderr)
            sys.exit(1)

    # Build options
    options = {}
    if args.theme:
        options["theme"] = args.theme
    if args.title:
        options["title"] = args.title
    if args.compress:
        options["compress"] = True

    # Render
    try:
        html = render(args.type, data, options)
        reason = ""
        if args.compress and "HEADROOM" in html:
            reason = " (compressed)"
        elif args.compress:
            reason = " (raw fallback)"
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(html, encoding="utf-8")
        print(f"Written to {output_path} ({len(html)} chars)")
    else:
        print(html)


def cmd_serve(args):
    """Start MCP server."""
    from .mcp_server import main
    main()


def main():
    parser = argparse.ArgumentParser(
        prog="archviz-diagram",
        description="Restrained flowchart and framework diagram engine",
    )
    sub = parser.add_subparsers(dest="command")

    # list
    sub.add_parser("list", help="List visualization types")

    # list-palettes
    sub.add_parser("list-palettes", help="List color palettes")

    # render
    p_render = sub.add_parser("render", help="Render a visualization")
    p_render.add_argument("--type", "-t", required=True, help="Visualization type")
    p_render.add_argument("--data", "-d", help="JSON data file (or - for stdin, omit for example)")
    p_render.add_argument("--theme", help="Palette name (warm-paper, swiss-neutral, editorial-parchment, ikb-dark)")
    p_render.add_argument("--title", help="Page title override")
    p_render.add_argument("--output", "-o", help="Output file (default: stdout)")
    p_render.add_argument("--compress", action="store_true", help="Send payload through headroom compression (opt-in, falls back to raw)")

    # serve
    sub.add_parser("serve", help="Start MCP server (stdio transport)")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "list-palettes":
        cmd_list_palettes(args)
    elif args.command == "render":
        cmd_render(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
