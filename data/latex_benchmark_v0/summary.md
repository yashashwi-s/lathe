# LaTeX Benchmark v0

Built: 2026-07-13

Accepted samples: 157
Rejected generated or visual-corruption candidates: 20

This is the first unified source-backed LaTeX benchmark directory. It keeps the 11 simple categories together and excludes references that compile but visibly render raw TeX/font macro fragments.

## Accepted Categories

| Category | Accepted |
|---|---:|
| `01_prose_sections` | 13 |
| `02_lists_formatting` | 15 |
| `03_math_inline_display` | 18 |
| `04_math_aligned` | 15 |
| `05_tables_simple` | 18 |
| `06_tables_moderate` | 18 |
| `07_figures_captions` | 15 |
| `08_crossrefs_citations` | 15 |
| `09_algorithms` | 12 |
| `10_compact_papers` | 8 |
| `11_forms_cv_letters` | 10 |

## Sources

| Source | Accepted |
|---|---:|
| `OleehyO/latex-formulas` | 33 |
| `TeX Live 2026` | 10 |
| `piushorn/arxiv-latex-tables-43k` | 36 |
| `scholarweave/arxiv-latex` | 66 |
| `stanford-crfm/image2struct-latex-v1` | 12 |

## Page Distribution

| Pages | Accepted |
|---:|---:|
| 1 | 102 |
| 2 | 28 |
| 3 | 27 |

## Visual-Corruption Cleanup

- `visual_corruption_cleanup.md`: samples removed from the accepted corpus after PDF review.
- Rejected corrupted samples are retained under `rejected/<category>/<sample_id>/` for auditability.

## Deferred Categories

- `12_diagrams_plots_stress`: Deferred by design; TikZ/PGFPlots/diagram categories should be a later stress set, not the first simple benchmark.

## Rules Used

- `pdflatex` only.
- Accepted PDFs must be 1-3 pages.
- All accepted samples have `main.tex`, `reference.pdf`, `compile.log`, and `provenance.json`.
- Full arXiv papers are not compiled blind; this build extracts smaller self-contained snippets or metadata-backed wrappers.
- Diagram-heavy categories are deferred to a later stress benchmark.
- References with visible raw TeX/font macro spill are rejected even when pdfLaTeX exits successfully.

## Files

```text
corpus/<category>/<sample_id>/
  main.tex
  reference.pdf
  compile.log
  provenance.json

rejected/<category>/<sample_id>/
  rejected candidates and visual-corruption rejects

manifests/
  all.csv
  accepted.csv
  rejected.csv

previews/
  latex_benchmark_v0_preview.pdf
```

The preview PDF contains one preview page per accepted data point. Multi-page references are tiled on that preview page.

The canonical provenance/review documents live in `results/latex_benchmark_v0/documents/`.

## Engine Conversion Review

The accepted samples were converted with three deterministic LaTeX-to-Typst engines:

| Engine | Converted | Typst-compiled | Total |
|---|---:|---:|---:|
| `pandoc` | 157 | 151 | 157 |
| `tylax` | 157 | 93 | 157 |
| `typetex` | 157 | 149 | 157 |

Engine artifacts:

```text
results/latex_benchmark_v0/
  engine_manifest.csv
  compilation_errors.md
  compilation_errors.csv
  summary.json
  documents/
    dataset_provenance.pdf
    engine_comparison_grid.pdf
  <category>/<sample_id>/
    pandoc.typ
    pandoc.pdf
    pandoc.log
    tylax.typ
    tylax.pdf
    tylax.log
    typetex.typ
    typetex.pdf
    typetex.log
```

The engine comparison PDF has one section per category and one page per sample. Each sample page is a labeled 2x2 grid: reference, Pandoc, Tylax, and TypeTeX.

## Build Command

```bash
mamba run -n lathe python scripts/dataset/build_all_categories_v0.py --out data/latex_benchmark_v0
mamba run -n lathe python scripts/dataset/build_review_documents.py --dataset data/latex_benchmark_v0 --engine-dir results/latex_benchmark_v0
```

The visual-corruption cleanup has already been applied to this dataset version.
See `visual_corruption_cleanup.md` for the removed sample IDs and rationale.
