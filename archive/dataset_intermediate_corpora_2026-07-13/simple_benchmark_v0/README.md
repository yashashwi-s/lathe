# Simple Benchmark v0

Built: 2026-07-13

This is the first Hugging Face-backed slice of the replacement LaTeX benchmark. It is intentionally small and categorical, meant for early conversion/evaluation work before adding prose, citations, algorithms, and compact papers.

## Current Categories

| Category | Accepted | Source |
|---|---:|---|
| `03_math_inline_display` | 10 | `OleehyO/latex-formulas` |
| `04_math_aligned` | 10 | `OleehyO/latex-formulas` |
| `05_tables_simple` | 10 | `piushorn/arxiv-latex-tables-43k` |
| `06_tables_moderate` | 10 | `piushorn/arxiv-latex-tables-43k` |

Total accepted samples: 40.

## Rules Used

- `pdflatex` only.
- Accepted PDFs must be 1-3 pages.
- Formula rows are grouped into 5-formula documents so samples are not one-line formulas.
- Table rows are grouped into 2-table documents so samples are not one-line tables.
- Table `simple` vs `moderate` was stratified by structural heuristics over the source table, because early rows in the HF dataset are all labeled `simple` even when they contain moderate structures such as `\multicolumn`, booktabs rules, or `\Xhline`.

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

The preview PDF contains one preview page per accepted data point. If a reference PDF has multiple pages, they are tiled into a grid on that preview page.

## Build Command

```bash
mamba run -n lathe python scripts/dataset/build_simple_benchmark_v0.py --out data/simple_benchmark_v0 --math-samples 10 --table-samples 10 --formula-scan-limit 500 --table-scan-limit 500 --timeout 20
```

