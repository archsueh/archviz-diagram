# 10b. ACADEMIC TABLE (hard rules)

> 从 `SKILL.md` 原样迁出（2026-09-23 渐进式披露拆分），内容未删改。
> 何时加载：学术表格硬规则（列宽、对齐、显著性标记、跨列表头）。只在做论文表格时加载。

## 10b. ACADEMIC TABLE (hard rules)

Trigger: 论文表格、性能对比表、实验结果表、benchmark table、ablation study、comparison table.

**When to use:**
- Multi-level headers (e.g., Math Domain / Code Domain / Chat Domain)
- Row groups (e.g., Target Model → Eagle3/DFlash/DSpark)
- Bold highlighting for best values
- Print-ready, A4-friendly layout

**Template:** `templates/html/academic-table.html`

**Data structure (JSON):**
```json
{
  "title": "Table 1: Main speculative decoding results",
  "subtitle": "Accepted length τ (higher is better) across benchmarks.",
  "columnGroups": [
    { "label": "Math Domain", "span": 3 },
    { "label": "Code Domain", "span": 3 },
    { "label": "Chat Domain", "span": 3 }
  ],
  "columns": ["GSM8K", "MATH", "AIME25", "MBPP", "HumanEval", "LCB", "MT-Bench", "Alpaca", "Arena-Hard"],
  "rowGroups": [
    {
      "label": "Qwen3-4B",
      "rows": [
        { "method": "Eagle3", "values": [3.21, 2.87, 2.15, 3.45, 3.12, 2.78, 3.67, 3.89, 3.34] },
        { "method": "DFlash", "values": [3.56, 3.12, 2.45, 3.78, 3.45, 3.12, 4.01, 4.23, 3.67] },
        { "method": "DSpark", "values": [4.12, 3.78, 3.01, 4.34, 4.12, 3.67, 4.56, 4.78, 4.23], "best": true }
      ]
    }
  ],
  "footer": "τ = average accepted tokens per decoding round."
}
```

**Styling rules:**
- Multi-level header: `rowspan` for row group labels, `colspan` for column groups
- Row groups: distinct background (`--av-surface`), bold label
- Best values: `font-weight: 600`, `color: var(--av-accent)`
- Hover effect: `var(--av-accent-soft)` background
- Typography: 13px body, 12px group headers, 11px column headers
- Numbers: `font-variant-numeric: tabular-nums` for alignment

**Quality checklist:**
- [ ] All column headers visible, no truncation
- [ ] Row group labels clear and distinct
- [ ] Best values highlighted with accent color
- [ ] Numbers right-aligned, text left-aligned
- [ ] Print-friendly (test with Cmd+P)
- [ ] Theme toggle works (T key)

---
