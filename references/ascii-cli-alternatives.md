# ASCII CLI Alternatives

**Status**: Optional enhancement only.  
**Core policy remains**: termaid for rich terminal Unicode + `templates/ascii/` plain fallback (max 80 cols, no box-drawing characters) for universal survivability.

**Agent philosophy (hard rule)**: Agents must primarily drive ASCII generation via CLI tools. CLI binaries (installable via go, brew, npm, etc.) are the only supported path for automation and repeatability. Web-based tools are explicitly disallowed for agent workflows.

Use these CLI tools only when the brief explicitly asks for decorative/presentation-grade ASCII (e.g. banners in READMEs, slide titles, image-derived art) and the plain version is still shipped alongside.

## Text-to-ASCII (Figlet / Banner style)

### common-nighthawk/go-figure
- GitHub: https://github.com/common-nighthawk/go-figure
- Language: Go
- Features: Beautiful text-to-ASCII, supports FIGlet fonts, many styles.
- Install:
  ```bash
  go install github.com/common-nighthawk/go-figure@latest
  ```
- Basic usage:
  ```bash
  go-figure "Hello World" --font big
  go-figure --list-fonts
  ```
- Integration tip: Pipe output into archviz-generated docs or use as source for `templates/ascii/` examples.

### figlet + xero/figlet-fonts
- figlet: Classic command-line ASCII text generator.
- Fonts repo: https://github.com/xero/figlet-fonts (hundreds of .flf files)
- Install (macOS example):
  ```bash
  brew install figlet
  # Then clone or copy fonts to /usr/local/share/figlet/
  git clone https://github.com/xero/figlet-fonts.git ~/figlet-fonts
  ```
- Usage:
  ```bash
  figlet -f big "archviz"
  figlet -f slant -w 80 "workflow"
  ```
- Recommended for: Consistent, font-rich banners that still output clean plain text.

## Image / Visual to ASCII

### TheZoraiz/ascii-image-converter
- GitHub: https://github.com/TheZoraiz/ascii-image-converter
- Language: Go
- Features: High-quality image and GIF to ASCII/Unicode, many options for color, contrast, width.
- Install:
  ```bash
  go install github.com/TheZoraiz/ascii-image-converter@latest
  # or
  brew install TheZoraiz/ascii-image-converter/ascii-image-converter
  ```
- Usage examples:
  ```bash
  ascii-image-converter image.png --width 80 --color
  ascii-image-converter diagram.svg -d 2  # dithering level
  ```
- Good for: Converting reference images or diagrams into ASCII when Mermaid is overkill.

## Modern Toolkit

### pigeonposse/ascii-kit
- GitHub: https://github.com/pigeonposse/ascii-kit
- Language: ESM / Node (has CLI components)
- Features: Unified toolkit for fonts, images, text art. Modular.
- Install:
  ```bash
  npm install -g @pigeonposse/ascii-kit
  # or use npx
  ```
- Usage: Check repo for CLI entrypoints (text, image, font rendering).
- Note: Best when you need a single tool covering multiple ASCII sources.

## Usage Rules Inside archviz

1. Always produce the source Mermaid (or structured data) first.
2. Render preview with termaid (`termaid ... --theme mono`).
3. For presentation output only: run selected CLI and capture the result.
4. **Always** append the plain `templates/ascii/` version (or equivalent 80-col no-box-drawing text) as fallback.
5. Document the source command in comments or accompanying table.

Example output structure in a deliverable:
```text
# Mermaid source (truth)
...
# termaid preview (terminal)
...
# CLI-enhanced (presentation only)
...
# Plain ASCII fallback (universal)
[Node] --> [Process]
...
```

## When NOT to Use CLI Alternatives
- Target is CI logs, diffs, chat, or unknown viewer → stick to termaid + plain ASCII.
- Strict academic / technical diagrams → plain templates only.
- You would introduce box-drawing or wide output without explicit user request.

See also:
- `references/termaid-routing.md`
- `references/ascii-workflow.md`
- `templates/ascii/`
- DESIGN.md (ASCII rules)