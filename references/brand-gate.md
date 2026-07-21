# Brand Gate (G0b) — host tokens before ship

Absorbed pattern from [diagram-design onboarding](https://github.com/cathrynlavery/diagram-design): **do not silently ship default-skinned diagrams into a branded project.**

archviz difference: we **do not crawl websites**. Tokens come from host docs and local presets (text-first, offline-safe).

## When the gate fires

First diagram in a session **or** first diagram for a project path, when any of:

- Repo has `DESIGN.md`, `design-tokens*`, Aver/theme files, or `.archviz-preset.yaml`
- User mentions brand / Aver / host palette / "跟文档一致"
- Editorial card/cover deliverable (Family A–D)

Skip gate when:

- User already locked tokens this session ("用 Warm Paper")
- Pure terminal ASCII / termaid scratch with no host brand
- User said "default / 默认 / 随便"

## Pass criteria

| Check | Pass |
|---|---|
| Source of tokens identified | host DESIGN.md · `.archviz-preset.yaml` · built-in preset · **or** explicit user "use default Warm Paper" |
| Roles mapped | `surface/paper`, `text/ink`, `border/muted`, `accent` (max 1) |
| Contrast | luminance rule (G2): ink on paper readable at 12–13px |
| Not mixed | one palette system per diagram set (no IKB + Terracotta together) |

On fail: **STOP** — propose tokens (1 primary + optional 1 alt) and ask once. Do not invent a third brand mid-diagram.

## Token discovery order

```
1. Explicit user hex / preset name this turn
2. .archviz-preset.yaml in project root or cwd
3. Host DESIGN.md / DESIGN tokens table (surface, text, border, accent)
4. Aver / product theme files if path is known (e.g. Theme.swift glass — only color tokens, not glass params)
5. Built-in Warm Paper (academic) or Editorial Parchment (cards)
```

## Semantic roles (archviz names)

| Role | Warm Paper default | Editorial Parchment |
|---|---|---|
| surface / paper | `#f5f0eb` | `#f5f4ed` |
| text / ink | `#1B365D` | `#141413` |
| border / muted | `#a8a29e` | `#e8e6dc` |
| accent (max 1) | `#002FA7` IKB or none | `#c96442` Terracotta |

Full systems → `DESIGN.md`. Mermaid init must use the **same** locked values.

## First-run prompt (copy)

> 这是本项目本会话的第一张图。检测到 [host DESIGN.md / 无品牌文件]。  
> 1) 沿用 host tokens  
> 2) Warm Paper 默认  
> 3) Editorial Parchment（卡片）  
> 请选，或贴 surface/text/border/accent。

If user says「按你判断」:

- inline technical diagram → Warm Paper  
- card/cover → Editorial Parchment  
- host DESIGN.md present → host wins  

## Detect "customized"

| Signal | Treat as customized |
|---|---|
| `.archviz-preset.yaml` exists | yes |
| Host DESIGN.md lists non-default accent | yes |
| Session already ran G0b and locked tokens | yes (reuse) |
| Only defaults in play, no host file | **not** customized → gate still asks once |

## After lock

1. Write chosen tokens into output YAML frontmatter (`§8 OUTPUT TEMPLATE`)
2. Apply to Mermaid `%%{init}%%` / HTML CSS vars / Excalidraw `appState.viewBackgroundColor` + stroke colors
3. Subsequent diagrams this session **skip re-ask** unless user changes brand

## Anti-patterns

| Don't | Why |
|---|---|
| Silent default into Aver / client repo | Brand drift = AI slop |
| Crawl arbitrary marketing site for colors | Offline + fidelity risk; use host DESIGN.md |
| Two accents "because logo has three colors" | Restraint dial; pick one focal |
| Change palette mid multi-diagram set | Same doc = same palette |

## Cross-links

- Gates table → `SKILL.md` Checkpoints (G0 / G0b / G2)
- Style presets YAML → `SKILL.md` §11b
- Ecosystem engines → `ecosystem-routing.md`

Last updated: 2026-07-21
