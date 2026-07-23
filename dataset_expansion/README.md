# dataset_expansion — benchmarking candidate HF datasets for fit/difficulty

This directory preserves the PR #2 dataset-expansion experiment. Its 32
accepted samples are also imported into `data/latex_benchmark_v0/` as the
canonical expansion slice; this directory remains the source experiment and
audit record. The original goal was to measure candidate HF datasets relative
to the 157-sample base using the same cheap 1-turn Sonnet baseline and scoring
as `harness_baseline/run_oneturn.py`.

## Sample sets (`corpus/<set>/<sample_id>/{main.tex, reference.pdf, provenance.json}`)

Snippet-wrapped (same minimal-article template family as lathe builders):

- `i2s_equation`, `i2s_table`, `i2s_algorithm`, `i2s_plot` — from
  `stanford-crfm/image2struct-latex-v1` (hard/medium difficulty first).
  `i2s_plot` is TikZ/pgfplots, a category the current benchmark excludes.
- `pubmed_table` — from `deepcopy/pubmed-tables-latex-768px`; messy clinical
  tables (nested headers, footnotes).

Real full documents (the structural difficulty jump — multi-page, real
preambles, real `\includegraphics` assets shipped alongside):

- `arxiv5t_paper` — `TIGER-Lab/arxiv-latex-5T`, month 2401, papers pulled as
  `.gz` source blobs over the hub API (no bulk download).
- `neurips_paper` — `Mithilss/neurips-2025-arxiv-latex-sources` parquet.

Reference rows for comparison (not in `corpus/`):

- `lathe_overall` — 1 sample per category from the lathe prompt_dev split.
- `lathe_hard` — the harness_baseline core 6+2; 1-turn sonnet numbers reused
  from `../harness_baseline/runs/` (not rerun).

## Caveats

- **References compiled with tectonic 0.16.9 (XeTeX)**, not pdfLaTeX —
  pdflatex isn't installed locally. Font/metric drift vs the lathe canon is
  small but nonzero; fine for difficulty ranking, note it in any writeup.
- Full-paper acceptance is low (NeurIPS 2/59, arXiv-5T 5/~90): most papers
  exceed the 12-page cap or fail tectonic. Caps: main tex ≤ 60k chars
  (1-turn prompt budget), ≤ 12 pages.
- 1-turn runs get an "assets present in compile directory" note listing
  graphics files; `typst compile --root work/` has the real images available.

## Scripts

- `mamba run -n lathe python dataset_expansion/scripts/build_snippet_sets.py 5 --corpus <staging>/corpus` — build the five snippet sets.
- `env HF_HUB_DOWNLOAD_TIMEOUT=300 HF_XET_HIGH_PERFORMANCE=1 mamba run -n lathe python dataset_expansion/scripts/build_fulldoc_sets.py --n 5 --max-pages 12 --max-chars 60000 --scan 400 --neurips-shards 2 --corpus <staging>/corpus`
- `env HF_HUB_DOWNLOAD_TIMEOUT=300 HF_XET_HIGH_PERFORMANCE=1 mamba run -n lathe python dataset_expansion/scripts/rebuild_neurips_protocol.py --corpus <staging>/corpus` — restore the two PR #2 NeurIPS papers by stable arXiv ID after upstream parquet re-sharding.
- `mamba run -n lathe python scripts/dataset/merge_expansion_into_v0.py --expansion-corpus <staging>/corpus` — validate and import the accepted trees into the canonical corpus.
- `mamba run -n lathe python dataset_expansion/scripts/run_baseline.py --set <set> | --lathe <ids...>` — historical 1-turn runs (idempotent per run directory).
- `mamba run -n lathe python dataset_expansion/scripts/make_results.py` — aggregate `runs/*/summary.json` into `RESULTS.md`.

Scoring: official `lathe/scripts/evaluation/compare_pdfs.py` +
`harness_baseline/raster_v2.py` recombination (raster_v0.2).
