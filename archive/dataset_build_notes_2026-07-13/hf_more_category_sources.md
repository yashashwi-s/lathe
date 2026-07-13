# Additional Hugging Face Sources For More Categories

Date: 2026-07-13

This note expands beyond the current 160-sample HF-backed slice, which only covers math and tables. The goal is to identify credible Hugging Face sources for the remaining simple benchmark categories.

## Current Built Dataset

The current canonical first-pass dataset is `data/simple_benchmark_all_v0`.

It contains 166 accepted samples across the 11 intended simple categories, with one sectioned review PDF:

- Preview: `data/simple_benchmark_all_v0/previews/simple_benchmark_all_v0_preview.pdf`
- Manifest: `data/simple_benchmark_all_v0/manifests/accepted.csv`

Accepted source distribution:

- `scholarweave/arxiv-latex`: 75
- `piushorn/arxiv-latex-tables-43k`: 36
- `OleehyO/latex-formulas`: 33
- `stanford-crfm/image2struct-latex-v1`: 12
- `TeX Live 2026`: 10

## Earlier Built Slices

`data/simple_benchmark_v0_160` currently has:

- `03_math_inline_display`: 40
- `04_math_aligned`: 40
- `05_tables_simple`: 40
- `06_tables_moderate`: 40

`data/simple_benchmark_algorithms` currently has:

- `09_algorithms`: 30

Sources:

- `OleehyO/latex-formulas`
- `piushorn/arxiv-latex-tables-43k`
- `stanford-crfm/image2struct-latex-v1`

## Strong Next Source: `stanford-crfm/image2struct-latex-v1`

HF page: https://huggingface.co/datasets/stanford-crfm/image2struct-latex-v1

Why it matters:

- It is explicitly categorized.
- It has `equation`, `table`, `algorithm`, `plot`, and `wild` parquet splits.
- The dataset card says the subjects are collected from arXiv and include `eess`, `cs`, `stat`, `math`, `physics`, `econ`, `q-bio`, and `q-fin`.
- The card says four automatically collected categories are equations, tables, algorithms, and code; `wild` comes from Wikipedia equation screenshots.
- Rows include LaTeX `text`, source/arXiv metadata, category, difficulty, and image assets.

Best use for us:

- Add `09_algorithms`.
- Possibly add a small later `figures_plots_stress` category, but not in v0.
- Do not duplicate existing equation/table categories yet unless we want a second-source validation set.

Schema probe result:

```text
algorithm/validation-00000-of-00001.parquet:
  text = \begin{algorithmic} ... \end{algorithmic}

equation/validation-00000-of-00001.parquet:
  text = \begin{align*} ... \end{align*}

table/validation-00000-of-00001.parquet:
  text = \begin{table} ... \begin{tabular} ... \end{tabular}
```

Built result:

- `data/simple_benchmark_algorithms` contains 30 accepted algorithm samples.
- 25 candidates were rejected by the local compile/page gate.
- Preview PDF: `data/simple_benchmark_algorithms/previews/algorithms_preview.pdf`

Recommendation:

- Treat this as the first algorithm slice.
- Keep it separate from the 160-sample math/table slice until the final benchmark manifest is assembled.
- Wrap each algorithm in a small article with `algorithm` and `algpseudocode`.
- Keep easy/medium first; reserve hard examples for a stress slice.

## Strong Source For Prose / Compact Papers: `scholarweave/arxiv-latex`

HF page: https://huggingface.co/datasets/scholarweave/arxiv-latex

Why it matters:

- Dataset viewer reports 3.09M rows.
- Rows include arXiv metadata and actual `latex` source.
- Schema includes `id`, `authors`, `title`, `categories`, `license`, `abstract`, and `latex`.
- The card describes it as a mirror of arXiv LaTeX source files aligned with official metadata.

Best use for us:

- `01_prose_sections`
- `07_figures_captions` only for non-diagram includegraphics/rule/placeholder cases
- `08_crossrefs_citations`
- `10_compact_papers`

Important caveats:

- Many sources are old/plain TeX, use custom formats, or require assets.
- License field must be checked. Prefer CC licenses where available.
- Full papers are often too long; extract self-contained sections or generate compact wrappers from source-backed excerpts.

Recommendation:

- Use as source discovery, not direct blind inclusion.
- Filter rows for modern `\documentclass`, `\section`, `\label`, `\cite`, `thebibliography`, and limited asset needs.
- Compile-gate extracted samples.

## Possible Source: `Mithilss/neurips-2025-arxiv-latex-sources`

HF page: https://huggingface.co/datasets/Mithilss/neurips-2025-arxiv-latex-sources

Why it matters:

- Domain-specific, modern ML/NeurIPS-adjacent LaTeX source corpus.
- Likely useful for compact paper and algorithm/citation examples.

Caveats:

- Probe was slow on first parquet shard.
- License is `other`; must inspect before redistribution.
- May be too homogeneous for broad representation.

Recommendation:

- Lower priority than `scholarweave/arxiv-latex`.
- Use later if we need modern ML paper style specifically.

## Possible Source: `Kyudan/arXiv_latex`

HF page: https://huggingface.co/datasets/Kyudan/arXiv_latex

Why it matters:

- CSV files split by broad fields: CS, math, physics, stat.
- Tags indicate Apache-2.0 on the dataset page.

Caveats:

- Need schema inspection before use.
- CSV may be large/noisy.
- Dataset license does not automatically solve underlying paper-source redistribution.

Recommendation:

- Use only if `scholarweave` is too cumbersome.

## Possible Source: `TIGER-Lab/arxiv-latex-5T`

HF page: https://huggingface.co/datasets/TIGER-Lab/arxiv-latex-5T

Why it matters:

- Modern arXiv source files and assets are exposed in a repository-like layout.
- Files include `main.tex`, images, and PDFs for recent papers.

Caveats:

- Large, file-tree oriented, and likely harder to stream into a simple builder.
- Better for compact full-paper reproduction than simple category extraction.

Recommendation:

- Good later source for `10_compact_papers`.
- Not the fastest way to expand v0 categories.

## Lower Priority / Not v0

### `JosselinSom/Latex-VLM`

HF page: https://huggingface.co/datasets/JosselinSom/Latex-VLM

Likely related to Image2Struct and useful for VLM tasks, but asset-heavy and diagram/figure-heavy. Defer.

### `CodexParas/table-detection-dataset-latex`

HF page: https://huggingface.co/datasets/CodexParas/table-detection-dataset-latex

Image/table detection oriented. We already have a better table source for LaTeX conversion v0.

### `yuntian-deng/im2latex-100k`

HF page: https://huggingface.co/datasets/yuntian-deng/im2latex-100k

Classic image-to-LaTeX formula style data. It is useful literature-wise, but `OleehyO/latex-formulas` is already enough for formula categories.

### `KiteFishAI/arxiv-tex-corpus-medium/full`

HF pages:

- https://huggingface.co/datasets/KiteFishAI/arxiv-tex-corpus-medium
- https://huggingface.co/datasets/KiteFishAI/arxiv-tex-corpus-full

The medium row probe showed fields `id` and `text`, where `text` looked like title/abstract/plain text rather than direct raw `.tex`. It may still help with source discovery, but `scholarweave/arxiv-latex` is more direct because it exposes a `latex` field.

## Recommended Expansion Order

1. Add `09_algorithms` from `stanford-crfm/image2struct-latex-v1`.
   - Target: 20-30 accepted.
   - Keep easy/medium first.

2. Add `01_prose_sections` from `scholarweave/arxiv-latex`.
   - Target: 20-30 accepted.
   - Extract simple section/prose samples with emphasis, lists, and footnotes.

3. Add `08_crossrefs_citations` from `scholarweave/arxiv-latex`.
   - Target: 20-30 accepted.
   - Require labels, refs, cites, and bibliography/thebibliography.

4. Add `10_compact_papers` from `scholarweave/arxiv-latex` or `TIGER-Lab/arxiv-latex-5T`.
   - Target: 20 accepted.
   - Compile full source only if 1-3 pages; otherwise build self-contained source-backed excerpts.

5. Add `11_forms_cv_letters` from TeX Live/CTAN, not HF.
   - HF search did not reveal a clean dataset for forms/CVs/letters.

6. Keep diagrams/plots out of v0.
   - `image2struct` has plot data, but this should be a later stress category.

## Practical Target After Expansion

Starting from 160 current samples:

- +25 algorithms
- +25 prose sections
- +25 crossrefs/citations
- +20 compact papers
- +10 forms/CV/letters from TeX Live

Likely next total: about 265 accepted samples, still category-readable and much less chaotic than the mixed TeX Live seed.
