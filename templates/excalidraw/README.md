# Excalidraw templates (archviz-diagram)

Warm Paper sketch boards for workshop / teaching. **Not** the default engine — promote to Mermaid when structure stabilizes (`references/ecosystem-routing.md`).

## Files

| File | Use |
|---|---|
| `mindmap.excalidraw` | Radial idea map, short labels |
| `architecture.excalidraw` | Layered system boxes + orthogonal-ish arrows |

## How to use

1. Open in [excalidraw.com](https://excalidraw.com) → **Open** → pick the `.excalidraw` file  
   or embed via Obsidian Excalidraw plugin / VS Code extension.
2. Replace placeholder labels; keep **≤9 nodes** on one board (soft cap).
3. Accent only **1–2** focal boxes (default IKB stroke `#002FA7` on focal; rest stone `#a8a29e`).
4. When structure is stable → regenerate as Mermaid (`flowchart TD + subgraph`) for git review.

## Agent generation contract

When emitting a new board (not just copying a template):

```text
appState.viewBackgroundColor = surface (#f5f0eb Warm Paper)
stroke for default nodes = border (#a8a29e)
fill for default nodes = surface or paper-2 (#e8e4e0)
stroke for focal (1–2) = accent (#002FA7)
text = ink (#1B365D)
roughness = 1 (sketchy) unless user asks "clean"
```

Prefer **rectangle + arrow** over freehand scribbles for architecture.  
Ship `.excalidraw` JSON valid for Excalidraw schema v2 (`type: "excalidraw"`).

## Promote path

```
Excalidraw workshop board
  → Mermaid flowchart/sequence (source of truth in git)
  → optional draw.io if long-lived human edit needed
```
