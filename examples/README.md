# archviz-skills Examples

Each example demonstrates a different output mode and diagram type.

## Files

| File | Mode | Diagram Type | Use Case |
|---|---|---|---|
| `mermaid-demo.md` | Mermaid | Bar + Flowchart + Gantt | Obsidian/GitHub preview |
| `mermaid-funnel-demo.md` | Mermaid | Conversion funnel | Teaching / admissions pipeline |
| `course-admission-flow.mmd` | Mermaid | Funnel + subgraph (32 courses) | Course admission workflow |
| `course-evaluation-matrix.mmd` | Mermaid / table | Decision matrix + radar notes | Course evaluation comparison |
| `ascii-demo.txt` | ASCII | Flowchart + Gantt + Architecture | Terminal / plain text |
| `html-demo.html` | Self-contained HTML | Interactive bar chart | Browser / OB HTML block |
| `python-demo.py` | Python (Plotly) | Scatter + Line | Deliverables / export |
| `deliverables-python-bar.py` | Python (Plotly) | Ranking bar — full-Python deliverable path | 落作品；pairs with the OB version below |
| `ob-lightweight-bar.md` | Mermaid (`xychart-beta`) + ASCII | Same ranking bar, no Python | OB / Obsidian preview of the same brief |
| `academic-table-data.json` | Data (JSON) | Grouped academic table: columnGroups / rowGroups / footer | Input for `references/academic-table-rules.md` |
| `aver-v1-architecture-semantic.html` | Self-contained HTML | Semantic-color architecture diagram (Aver V1) | Demo for `references/semantic-component-colors.md` |
| `us-population-migration-2024.html` | Self-contained HTML | US population by state, 2024 | Map / choropleth demo |
| `git-push-release-workflow.mmd` | Mermaid (Wes Anderson variant) | Release pipeline + highlighted git push | Skill publishing / git push teaching & checklist |
| `git-push-release-workflow.html` | Self-contained HTML (Wes Anderson palette) | **图文并茂可视化**（推荐直接打开截图用） | 发布流程演示 + 好截图素材 |
| `us-flows.html` | Self-contained HTML (restrained Swiss / archviz tokens) | **Combined Energy Sankey (LLNL exact) + Migration geo-flow map** (interactive perimeter-attach curves, panel, corridors) | Canonical for custom flow attachment + multi-viz consolidation in one Swiss page. Open directly for demo / export. |

> This table is the index for `examples/`. Five files were missing from it until
> 2026-10-09 — four of them named by nothing anywhere in the repo, so no agent
> could find them. Adding a file here is the cheapest way to keep that from
> recurring; there is no gate on this file yet.

## Quick test

```bash
# Mermaid (default or Wes Anderson palette): paste git-push-release-workflow.mmd or mermaid-demo.md into Obsidian / GitHub
# Terminal rich render: termaid /Users/mac/Developer/archviz-skills/examples/git-push-release-workflow.mmd --theme mono
# ASCII fallback: see templates/ascii/ or run with --ascii
# HTML: open html-demo.html
# Python: python3 python-demo.py
# Python deliverable variant: python3 deliverables-python-bar.py
```

**图文并茂 tip**: 
- 打开 `git-push-release-workflow.html` （自包含，使用 Wes Anderson 调色）直接浏览器全屏截图（推荐！已内置截图提示）。
- 或 `git-push-release-workflow.mmd` 在 Obsidian/GitHub 渲染查看。
- 打开 `us-flows.html`：单一文件内同时呈现精确 LLNL Sankey（paths-first attach）+ Census migration 地图（perimeter curves + highlight）。展示 archviz 复杂 flow 收敛能力 + restrained Swiss 风格。
