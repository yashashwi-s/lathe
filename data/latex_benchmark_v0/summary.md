# LaTeX Benchmark v0

Built: 2026-07-22

Accepted samples: 189 (157 base + 32 expansion)
Rejected generated or visual-corruption base candidates: 20

This is the canonical source-backed LaTeX benchmark directory. It preserves
the reviewed 157-sample base and imports all 32 accepted samples from the
seven-set `dataset_expansion/` PR, including TikZ plots and full multi-file
papers. Reference compilation protocol is recorded per sample.

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
| `i2s_equation` | 5 |
| `i2s_table` | 5 |
| `i2s_algorithm` | 5 |
| `i2s_plot` | 5 |
| `pubmed_table` | 5 |
| `arxiv5t_paper` | 5 |
| `neurips_paper` | 2 |

## Sources

| Source | Accepted |
|---|---:|
| `OleehyO/latex-formulas` | 33 |
| `TeX Live 2026` | 10 |
| `piushorn/arxiv-latex-tables-43k` | 36 |
| `scholarweave/arxiv-latex` | 66 |
| `stanford-crfm/image2struct-latex-v1` (all configs) | 32 |
| `deepcopy/pubmed-tables-latex-768px` | 5 |
| `TIGER-Lab/arxiv-latex-5T` | 5 |
| `Mithilss/neurips-2025-arxiv-latex-sources` | 2 |

## Page Distribution

| Pages | Accepted |
|---:|---:|
| 1 | 117 |
| 2 | 38 |
| 3 | 27 |
| 5 | 1 |
| 8 | 1 |
| 10 | 1 |
| 11 | 2 |
| 12 | 2 |

## Visual-Corruption Cleanup

- `visual_corruption_cleanup.md`: samples removed from the accepted corpus after PDF review.
- Rejected corrupted samples are retained under `rejected/<category>/<sample_id>/` for auditability.

## Rules Used

- The original 157 references use pdfLaTeX and are 1–3 pages.
- The 32 expansion references use Tectonic 0.16.9; the full-document protocol
  accepts up to 12 pages and main sources up to 60,000 characters.
- Accepted samples have `main.tex`, `reference.pdf`, `compile.log`, and
  `provenance.json`; full-document samples also retain their source assets,
  included TeX files, bibliography files, and class/style files.
- References with visible raw TeX/font macro spill are rejected even when pdfLaTeX exits successfully.
- The historical 30-document prompt-development and 127-document held-out
  splits remain unchanged. Expansion samples live in `splits/expansion_32.csv`.

## Files

```text
corpus/<category>/<sample_id>/
  main.tex
  reference.pdf
  compile.log
  provenance.json
  ... optional full-document source assets

rejected/<category>/<sample_id>/
  rejected candidates and visual-corruption rejects

manifests/
  all.csv
  accepted.csv
  rejected.csv

previews/
  latex_benchmark_v0_preview.pdf
```

The preview PDF contains one preview page per accepted data point. Multi-page
references are tiled on that preview page. The review-only preview is
size-optimized after assembly; canonical `reference.pdf` files are untouched.

The canonical provenance/review documents live in `results/latex_benchmark_v0/documents/`.

## Engine Conversion Review

The accepted samples were converted with three deterministic LaTeX-to-Typst engines:

| Engine | Converted | Typst-compiled | Total |
|---|---:|---:|---:|
| `pandoc` | 188 | 178 | 189 |
| `tylax` | 188 | 114 | 189 |
| `typetex` | 188 | 172 | 189 |

On the 32 expansion samples alone, Pandoc compiled 27, Tylax 21, and
TypeTeX 23; each converter produced source for 31/32. The original base-slice
compile counts remain 151, 93, and 149 respectively.

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
mamba run -n lathe python dataset_expansion/scripts/build_snippet_sets.py 5 --corpus <staging>/corpus
env HF_HUB_DOWNLOAD_TIMEOUT=300 HF_XET_HIGH_PERFORMANCE=1 mamba run -n lathe python dataset_expansion/scripts/build_fulldoc_sets.py --n 5 --max-pages 12 --max-chars 60000 --scan 400 --neurips-shards 2 --corpus <staging>/corpus
env HF_HUB_DOWNLOAD_TIMEOUT=300 HF_XET_HIGH_PERFORMANCE=1 mamba run -n lathe python dataset_expansion/scripts/rebuild_neurips_protocol.py --corpus <staging>/corpus
mamba run -n lathe python scripts/dataset/merge_expansion_into_v0.py --expansion-corpus <staging>/corpus
mamba run -n lathe python scripts/dataset/convert_all_v0_engines.py
mamba run -n lathe python scripts/dataset/build_review_documents.py --dataset data/latex_benchmark_v0 --engine-dir results/latex_benchmark_v0
```

The recovery command pins the two NeurIPS papers by their PR #2 source IDs;
the upstream Hugging Face dataset has since changed its parquet sharding.

The visual-corruption cleanup remains applied to the base slice. See
`visual_corruption_cleanup.md` for the removed base sample IDs and rationale,
and `expansion_import.json` for the expansion protocol/import record.
