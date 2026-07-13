# TeX Live Seed Corpus

This is the first local, human-authored source pool for the replacement LaTeX benchmark. It uses examples shipped with TeX Live / CTAN package documentation, discovered under:

```text
/usr/local/texlive/2026/texmf-dist/doc
```

The current simple review build is the better starting point for dataset inspection. The earlier 60-sample balanced review build is useful for inspecting the pipeline and hard/mixed TeX Live examples, but it is not yet a good final dataset: many samples combine several constructs and are too dense for a clean benchmark taxonomy. Build simpler, cleaner slices first, then add medium and hard slices after.

## Acceptance Rules

- Compile with `pdflatex` only.
- Accept only valid reference PDFs with 1-3 pages.
- Reject sources requiring shell escape, network access, unavailable assets, non-pdfLaTeX engines, or unclear local source trees.
- Keep tiny one-line examples, but cap them so they do not dominate.
- Prefer a balanced mix of document forms, source packages, size buckets, and construct tags.
- Enforce accepted-time caps by package and document form so one easy package cannot dominate the review set.
- Use sampler profiles:
  - `simple`: cleaner isolated constructs and short/medium examples.
  - `balanced`: broad mixed review set.
  - `hard`: dense mixed-layout/package examples.

## Sampling Structure

Each accepted sample records:

- `source_family`: currently `texlive_ctan_doc`
- `document_form`: broad form such as `compact_paper`, `table`, `figure_diagram_plot`, `presentation`, `cv_resume`, or `letter_form_teaching`
- `construct_tags`: many-to-many tags such as `display_math`, `complex_table`, `tikz`, `pgfplots`, `crossrefs`, `custom_macros`, and `beamer_frames`
- `size_bucket`: `tiny`, `short`, `medium`, or `large`
- original TeX Live path, package name, source/PDF hashes, page count, compile command, and compile log

## Preview Document

The generated preview PDF is the review surface for the dataset. It contains one preview page per accepted data point. If the reference PDF has multiple pages, all pages are tiled into a grid on that one preview page.

Expected output:

```text
data/texlive_seed_review/
  candidates.csv
  selected_candidates.csv
  compile_results.csv
  accepted_manifest.csv
  summary.md
  corpus/<document_form>/<sample_id>/
    main.tex
    reference.pdf
    compile.log
    provenance.json
    source_tree/
  previews/texlive_seed_preview.pdf
```

## Commands

Discover, sample, compile, and build the preview:

```bash
mamba run -n lathe python scripts/dataset/texlive_corpus.py
```

Build a simpler review set:

```bash
mamba run -n lathe python scripts/dataset/texlive_corpus.py --profile simple --out data/texlive_seed_simple --candidate-target 180 --max-accept 40 --timeout 15
```

Build the current 60-sample structured review set:

```bash
mamba run -n lathe python scripts/dataset/texlive_corpus.py --profile balanced --out data/texlive_seed_review --candidate-target 300 --max-accept 60 --timeout 15
```

Run a smaller smoke pass:

```bash
mamba run -n lathe python scripts/dataset/texlive_corpus.py --profile simple --out data/texlive_seed_smoke --candidate-target 40 --max-accept 20 --timeout 15
```

Rebuild only the preview from existing compile results:

```bash
mamba run -n lathe python scripts/dataset/texlive_corpus.py --preview-only
```

## Current Review Artifact

The current simple local review build is:

```text
data/texlive_seed_simple/previews/texlive_seed_preview.pdf
```

It contains 40 accepted pdfLaTeX samples, one preview page per data point. Multi-page references are tiled into a grid on the same preview page. This is the preferred artifact to inspect first.

The mixed/hard diagnostic build is:

```text
data/texlive_seed_review/previews/texlive_seed_preview.pdf
```

It contains 60 accepted pdfLaTeX samples. Treat this as a mixed/hard diagnostic artifact, not the final dataset.
