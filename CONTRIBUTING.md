# Contributing to archviz-skills

Thanks for your interest in contributing!

## How to contribute

1. **Fork** the repo
2. **Create a branch** (`git checkout -b feature/my-addition`)
3. **Make changes** following the design system in DESIGN.md
4. **Test** your templates render correctly in Obsidian/GitHub
5. **Submit a PR** with a clear description

## Guidelines

- All templates must follow DESIGN.md tokens (Warm Paper or IKB, max 1 accent)
- Mermaid templates must be preview-compatible (no architecture-beta in .md source)
- ASCII templates must fit 80 columns
- Keep labels short (≤6 words / ≤8 Chinese chars)
- No emoji in labels or node names

## Adding templates

Place in the correct subdirectory:
- `templates/mermaid/` — .mmd files
- `templates/ascii/` — .txt files  
- `templates/html/` — .html files (self-contained, no deps)
- `templates/python/` — .py files (Plotly/Matplotlib)

Include a comment header with: diagram type, use case, env, dials.

## Reporting issues

Use the issue template. Include: what you expected, what happened, which environment (Obsidian/GitHub/terminal).
