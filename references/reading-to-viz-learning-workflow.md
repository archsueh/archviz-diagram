# Reading-to-Viz Learning Workflow (archviz adaptation)

**Core principle**: While consuming content (web docs, articles, English/tech reading), use agents + archviz to auto-extract key concepts and generate restrained visualizations as durable learning artifacts. Combine with spaced repetition for retention. Pure CLI/agent-native, absolute paths, no bloat.

Inspired by qiaomu-english-learn (Read Frog fork + Claude Code customization for vocab capture during immersive reading → Ebbinghaus flashcards). Adapt the pattern: consumption → extraction → viz output (instead of/in addition to text cards) → review loop.

## The Pipeline (CLI-first, repeatable)

1. **Capture reading session** (absolute paths):
   - Use proxies or tools (e.g. qiaomu-markdown-proxy style or browser export) to get clean Markdown/text from URLs.
   - Command example:
     ```bash
     python3 /Users/mac/.agents/skills/qiaomu-markdown-proxy/scripts/fetch.py "https://example.com/tech-article" > /tmp/reading-session.md
     ```

2. **Agent extraction** (via Claude Code / Grok / Codex prompt or dedicated skill):
   - Prompt: "From the following text, extract 5-10 key concepts/vocab items with short definitions and relationships. Output as structured list for visualization."
   - Or use NotebookLM-style processing (from other qiaomu refs) for synthesis.
   - Save to: /Users/mac/Developer/archviz-skills/inputs/reading-concepts.json (or .md)

3. **Generate archviz outputs** (restrained, text-first):
   - Use archviz to turn concepts into:
     - Mermaid mindmap/flowchart for concept relationships.
     - ASCII cards or simple tables for quick review (80-col plain).
     - HTML editorial cards or bullet graphs for spaced-rep style (one concept per card).
     - xychart or distribution if data-heavy (e.g. word frequency).
   - Example commands (adapt from existing templates):
     ```bash
     # Assume a small archviz CLI or direct prompt in agent
     archviz --type mindmap --input /tmp/concepts.json --output /Users/mac/Developer/archviz-skills/outputs/reading-mindmap.mmd
     # Or via skill: "Use archviz to create concept diagram from this list..."
     ```
   - Always produce plain ASCII/Markdown fallback + optional polished HTML.

4. **Export to review system**:
   - Anki/Obsidian: Convert cards to .apkg or Markdown with frontmatter.
   - Canvas/Obsidian: Embed the .mmd or .html directly.
   - Spaced repetition hook: Tag with due dates based on Ebbinghaus (simple Python script or existing tool).

5. **Review + iterate**:
   - During review, if gaps appear, re-run extraction on related content.
   - Self-evolution: Log what viz types helped retention most (update archviz templates).

## Adaptation Rules for archviz

- **Restraint first**: No rainbow, no excessive icons. Use Warm Paper or Editorial Parchment tokens. Max 1 accent.
- **CLI/agent-native**: All steps scriptable. No browser-only dependencies for core flow (use proxies for capture).
- **Multi-format survivability**: Always ship Mermaid source + termaid preview + plain ASCII + HTML (for cards).
- **Learning-specific dials**: For education briefs, set COMPLEXITY=5 (clear hierarchy), DENSITY=4 (scannable cards), RESTRAINT=9 (minimal).
- **Integration with existing**:
  - Reuse ascii-cli-alternatives for quick text cards.
  - Use ascii-workflow for terminal review of concepts.
  - reading-to-viz complements skill-publishing (publish the generated learning viz as its own mini-skill or note).

## Example Output Structure (in /outputs/)

```
reading-2026-06-12/
├── source.md                  # original captured text
├── concepts.json              # extracted (name, def, relations)
├── concept-mindmap.mmd        # archviz Mermaid
├── concept-mindmap-ascii.txt  # plain fallback
├── vocab-cards.html           # self-contained editorial cards for review
└── review-log.md              # what stuck, what needs re-viz
```

Run the full pipeline with one agent prompt or shell script (see proposed scripts/reading-to-viz.py).

## Anti-Patterns
- Treating viz as one-off decoration instead of reviewable artifact.
- Skipping plain fallback (breaks when copying to Anki or terminal review).
- Over-extracting (keep ≤10 items per session for focus).
- Browser-only capture (breaks agent repeatability).

## Maintenance & Evolution
- When new qiaomu-style content tools appear, add here.
- Update archviz templates/ for common learning outputs (e.g. new "vocab-card" HTML variant).
- Track retention metrics in review-log to self-optimize dials/prompts.
- Darwin/curation: Score this workflow periodically for your (hsueh) design/teaching/AI-engineering identity.

See also:
- references/skill-publishing.md (for publishing generated learning materials)
- references/ascii-workflow.md
- qiaomu-anything-to-notebooklm (for upstream synthesis)
- DESIGN.md (restraint tokens for educational viz)
