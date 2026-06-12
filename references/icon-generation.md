# Icon Generation for archviz (High-Value References)

**Status**: Pure reference only. No runtime bloat. Focus on agent-native (MCP/CLI) + clean SVG output that fits archviz's restrained design system (DESIGN.md tokens: Warm Paper #f5f0eb surface, #1B365D text, #a8a29e border, max 1 accent like #002FA7; no gradients, minimal, text-first).

qiaomu's icon.qiaomu.ai (HTML browser UI) is visually appealing for quick previews but incompatible with archviz principles: not CLI/agent-scriptable, produces web-heavy output hard to inline into self-contained HTML templates or ascii fallbacks, risks bloat.

## High-Value GitHub References (judged for archviz fit)
Prioritized by:
- Clean, editable SVG output (inline in archviz html/ templates, editorial cards, Three.js assets, or diagrams).
- Agent/CLI/MCP support (fits archviz's Claude/Grok/Cursor workflows, text prompts, no browser dependency for core use).
- Scalable for viz (architecture icons, custom nodes, brand marks in cards).
- Low bloat (libraries or generative, not full UIs).
- Can extend existing icon-system (templates/ascii/icon-system.txt) or html/ templates.

1. **glincker/thesvg** (https://github.com/glincker/thesvg, thesvg.org)
   - 6100+ brand + architecture/cloud SVG icons (tree-shakeable, versioned).
   - npm, CLI, CDN, **MCP server** (Claude Code/Cursor/Windsurf: "get the GitHub icon" or "search cloud architecture icons" returns real SVG + metadata).
   - **Why high-value for archviz**: MCP is agent gold—prompt directly in archviz flows to fetch/inline SVGs into html/editorial-card.html or Mermaid diagrams (e.g., custom node icons in flowcharts). Fits restrained: use with DESIGN.md tokens for color/stroke. Extend icon-system.txt with ASCII approximations. Architecture icons align with archviz's core (diagrams, 3D).
   - Integration: In agent prompt: "Use thesvg MCP to get minimal SVG for database, inline in archviz template with Warm Paper palette." Output stays text-first + self-contained.

2. **Viktoo/SVG.chat** (https://github.com/Viktoo/SVG.chat)
   - AI (Claude 3.7 Sonnet) text-to-clean editable SVG icon/art generator.
   - Browser tool but full source open; pure prompt-based.
   - **Why high-value**: Generative for custom icons on-demand (e.g., "restrained line icon for API gateway, no gradients"). SVG outputs inline perfectly into archviz HTML (editorial cards, dashboards) or Three.js. Prompt engineering fits archviz's agent use (brief + dials). Reference for extending icon-system with AI-generated variants.
   - Integration: Prompt archviz agent with DESIGN.md tokens: "Generate SVG icon matching Swiss/Editorial style for use in mindmap node." Avoids qiaomu's HTML lock-in.

3. **yauheniya-ai/icon-gen-ai** (https://github.com/yauheniya-ai/icon-gen-ai)
   - CLI + Python API for AI icon gen (from Iconify/URLs/local files), with animation support, exports SVG/PNG/WebP/ICO.
   - **Why medium-high value**: Pure CLI for batch workflows (e.g., generate icon sets for a full architecture diagram project). SVG exports feed directly into archviz templates. Good supplement for thesvg when needing generative from existing bases.
   - Integration: Scriptable in archviz's reading-to-viz or publishing flows: "Generate SVG icons for concepts, embed in HTML cards."

## Integration Rules (to keep high-value, no bloat)
- **Output priority**: Always prefer clean SVG (inline `<svg>` in html/ templates with DESIGN.md tokens for fill/stroke). Provide ASCII fallback (extend templates/ascii/icon-system.txt).
- **Agent-native**: Use MCP (thesvg) or prompts (SVG.chat) in archviz brief → generate/embed. No web UIs in core flows.
- **Design fit**: Match restrained (sharp 0 radius, 1px lines, max 1 accent, Warm Paper palette). Test contrast/luminance per DESIGN.md.
- **Templates reuse**: Inline SVGs in html/editorial-card.html, html/dashboard.html, etc. For ascii: simple text representations. For diagrams: custom node icons in Mermaid (via labels or external assets).
- **Anti-patterns**: Avoid full browser generators in production (qiaomu-style). No rainbow/gradients. Don't add new heavy deps—reference only or light CLI wrappers.
- **High-value use cases in archviz**:
  - Architecture diagrams: Custom icons for services/nodes (thesvg MCP + archviz flowchart).
  - Editorial cards/knowledge: Brand or concept icons in cards (SVG inline + restrained).
  - Learning/reading-to-viz: Icons for vocab/concept cards (from qiaomu-english-learn pattern).
  - 3D: Texture or label icons in Three.js scenes.
  - ASCII/terminal: Fallback approximations.

## Workflow Example (agent prompt)
"Brief: Generate restrained architecture diagram for API system. Use thesvg MCP to fetch 'database' and 'cloud' SVGs. Inline into archviz html template with Warm Paper tokens. Provide Mermaid source + ASCII fallback."

See also:
- DESIGN.md (tokens, restrained rules, icon roles in viz).
- templates/ascii/icon-system.txt (base for ASCII icons).
- templates/html/ (embed SVGs here).
- references/reading-to-viz-learning-workflow.md (icons for learning artifacts).
- references/ascii-cli-alternatives.md (CLI icon tools).

This keeps archviz lightweight while adding high-value icon capability via references and agent prompts. Re-evaluate via darwin if adding more.