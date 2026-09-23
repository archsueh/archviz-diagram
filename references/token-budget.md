# 15. COMPRESSION & TOKEN BUDGET (Headroom inspired)

> 从 `SKILL.md` 原样迁出（2026-09-23 渐进式披露拆分），内容未删改。
> 何时加载：Token 预算分档、输入/输出侧压缩、可逆缓存类比（CCR）。只在**输出超长或成本敏感**时加载。

## 15. COMPRESSION & TOKEN BUDGET (Headroom inspired)

Archviz output competes for context window with prompt, tool results, and system memory.
Render this section as operational rules, not aspirational goals.

### 15.1 Input side (before generation)

| Rule | Why |
|------|-----|
| Flatten JSON arrays to `[{label,value}]` before passing to chart | Whitespace and nesting are the token killers headroom targets |
| Strip decorative prose from data payloads; keep only numeric/label fields | Tool output cost dominates when agent re-reads the same data |
| One source of truth per diagram; deduplicate cross-references with `key` fields | Duplicate labels break max-1-accent and waste tokens |
| ASCII fallback prepared in parallel, not after render failure | Avoid the expensive "generate big HTML → fail → retry" loop |

### 15.2 Output side (after generation)

| Rule | Target |
|------|--------|
| Embed self-contained HTML only when interactivity/animation is required | Static saves tokens; Mermaid + image export replaces heavy HTML for static deliverables |
| Export system (E→P/S/W/C) de-prioritizes re-render; use SVG for single-shape, PNG only when client demands raster | PNG at 4× is expensive in output tokens and base64 |
| Embed dedup: if same diagram appears in 2 notes, link to one canonical HTML; second brief becomes a `[view]` reference | Avoids shipping duplicate 30KB assets |
| Self-healing loop ≤2 rounds; third failure ships ASCII fallback + documented warning | Prevents the model from "fixing" forever and bloating the conversation |

### 15.3 Output shaping for model-written text

- **Terse by default**: Every archviz output block should use finding-first captions, not description restatements.
- **Max 15 words for caption**: `"V1 closed loop; 3 feedback paths, 1 integration gap"`, not `"This diagram illustrates the closed loop of V1 with three feedback paths and one integration gap"`.
- **Skip decorative transitions**: No "Great, let me now show you…", no "I've generated the diagram above for your reference".
- **Evidence-first body**: Chart itself is the evidence; caption is the claim. Model text explains nothing the chart doesn't already show.

### 15.4 Reversible caching analog (CCR)

Archviz does not have a full CCR reversibility layer, but inherit the principle:

1. **Golden copy**: First successful render of a template is cached at `templates/html/` or `exports/`.
2. **Rollback contract**: If the self-healing loop or a later edit breaks a diagram, revert to last known good. Do not ship a broken diagram with a "fix in progress" note.
3. **Audit log**: `CHANGELOG.md` records the before/after state for every major diagram change.

### 15.5 Practical budget tiers

| Context | Allowed format budget |
|---------|----------------------|
| Terminal / CLI chat | Mermaid ≤ 30 nodes, ASCII fallback |
| Obsidian note | Self-contained HTML ≤ 200KB, Mermaid inline |
| Deliverable PNG | SVG → PNG (4×), no base64 embeds in chat |
| Batch export | Use `headroom-wrap` for Mermaid/HTML before model re-reads; expect 40–90% token reduction on tool outputs |


---
