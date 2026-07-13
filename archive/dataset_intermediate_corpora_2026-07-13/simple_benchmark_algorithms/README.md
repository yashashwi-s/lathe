# Simple Benchmark Algorithms Slice

Built: 2026-07-13

This slice adds a source-backed algorithm/pseudocode category to the simple LaTeX benchmark. It contains 30 accepted samples from `stanford-crfm/image2struct-latex-v1`, all compile-gated with `pdflatex`.

## Accepted Category

| Category | Accepted | Source |
|---|---:|---|
| `09_algorithms` | 30 | `stanford-crfm/image2struct-latex-v1` |

Rejected candidate groups: 25.

## Rules Used

- `pdflatex` only.
- Accepted PDFs must be 1-3 pages.
- Source rows must contain non-trivial algorithmic pseudocode.
- Rows are wrapped in a minimal article document using `algorithm` and `algpseudocode`.
- Rows requiring external assets or unsafe/external input commands are skipped.
- Every accepted sample has `main.tex`, `reference.pdf`, `compile.log`, and `provenance.json`.

## Files

```text
corpus/09_algorithms/<sample_id>/
  main.tex
  reference.pdf
  compile.log
  provenance.json

manifests/
  all.csv
  accepted.csv
  rejected.csv

previews/
  algorithms_preview.pdf
```

The preview PDF contains one preview page per accepted data point. Multi-page reference PDFs are tiled into a grid on that preview page.

## Build Command

```bash
mamba run -n lathe python scripts/dataset/build_image2struct_algorithms.py --out data/simple_benchmark_algorithms --samples 30 --scan-limit 800 --timeout 20
```

