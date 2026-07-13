# Simple Benchmark v0 160

Built: 2026-07-13

This is the first larger Hugging Face-backed slice of the replacement LaTeX benchmark. It contains 160 accepted, source-backed, pdfLaTeX-compiled samples.

## Accepted Categories

| Category | Accepted | Source |
|---|---:|---|
| `03_math_inline_display` | 40 | `OleehyO/latex-formulas` |
| `04_math_aligned` | 40 | `OleehyO/latex-formulas` |
| `05_tables_simple` | 40 | `piushorn/arxiv-latex-tables-43k` |
| `06_tables_moderate` | 40 | `piushorn/arxiv-latex-tables-43k` |

Total accepted samples: 160.

Rejected candidate groups: 55.

## Page Distribution

| Pages | Accepted samples |
|---:|---:|
| 1 | 61 |
| 2 | 56 |
| 3 | 43 |

## Rules Used

- `pdflatex` only.
- Accepted PDFs must be 1-3 pages.
- Formula rows are grouped into 5-formula documents.
- Table rows are grouped into 2-table documents.
- Table `simple` vs `moderate` is stratified by structural heuristics over source tables.
- Every accepted sample has `main.tex`, `reference.pdf`, `compile.log`, and `provenance.json`.

## Files

```text
corpus/<category>/<sample_id>/
  main.tex
  reference.pdf
  compile.log
  provenance.json

manifests/
  all.csv
  accepted.csv
  rejected.csv

previews/
  simple_benchmark_v0_preview.pdf
```

The preview PDF contains one preview page per accepted data point. Multi-page reference PDFs are tiled into a grid on that preview page.

## Build Command

```bash
mamba run -n lathe python scripts/dataset/build_simple_benchmark_v0.py --out data/simple_benchmark_v0_160 --math-samples 40 --table-samples 40 --formula-scan-limit 2200 --table-scan-limit 3000 --timeout 20
```

