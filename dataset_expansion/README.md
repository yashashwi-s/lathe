# dataset_expansion — benchmarking candidate HF datasets for fit/difficulty

Scratch experiment (sibling of `harness_baseline/`, outside the `lathe/`
repo). Goal: measure how hard candidate HF datasets are relative to the
current lathe benchmark, using a cheap 1-turn sonnet (low effort) baseline —
the same prompt/scoring as `harness_baseline/run_oneturn.py` — so a later
rerun with the best opus harness is directly comparable.

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

- `scripts/build_snippet_sets.py [n]` — build the five snippet sets.
- `scripts/build_fulldoc_sets.py --n N --max-pages P [--only arxiv5t|neurips]`
- `scripts/run_baseline.py --set <set> | --lathe <ids...>` — 1-turn runs
  (idempotent per run dir; use lathe env python: `~/mamba/envs/lathe/bin/python`).
- `scripts/make_results.py` — aggregate `runs/*/summary.json` → `RESULTS.md`.

Scoring: official `lathe/scripts/evaluation/compare_pdfs.py` +
`harness_baseline/raster_v2.py` recombination (raster_v0.2).
