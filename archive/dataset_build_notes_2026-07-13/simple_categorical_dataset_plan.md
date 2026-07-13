# Simple Categorical LaTeX Dataset Plan

Date: 2026-07-13

## Reset

The first serious benchmark dataset should be simpler and more categorical than the current TeX Live seed corpora. The old generated dataset had the right *shape* because categories were understandable and targeted, but it had three major problems:

1. Samples were too short.
2. Samples were AI-generated rather than source-backed.
3. Some categories were too ambitious or too visually difficult for a first benchmark.

The new first-pass dataset should keep the old clarity, but use real LaTeX sources and make each data point long enough to matter. Target 120-180 accepted samples first, not 300. Each sample should render to 1-3 pages and be easy to inspect.

The literature-backed rationale for these categories is in `docs/literature_backed_dataset_rationale.md`.

Additional Hugging Face source research for missing categories is in `docs/hf_more_category_sources.md`.

## What Not To Do First

- Do not center the initial dataset on TikZ/PGFPlots/diagrams. They are genuinely hard and will dominate failure analysis before we understand simpler conversion behavior.
- Do not use the current TeX Live balanced seed as the main dataset. Keep it as a mixed/hard diagnostic pool.
- Do not use huge full papers as the first target. Use compact paper-like samples or self-contained excerpts.
- Do not let Hugging Face datasets trick us into formula/table-only benchmark tunnel vision.

## Better Category Set

Use clear categories that map to LaTeX constructs and can be sourced from real data:

| Category | Target accepted | What it tests | Main source |
|---|---:|---|---|
| `01_prose_sections` | 12-18 | paragraphs, sections, emphasis, quotes, footnotes | arXiv source excerpts, TeX Live simple docs |
| `02_lists_formatting` | 10-15 | itemize/enumerate/description, bold/italic/mono | TeX Live docs, The Stack/TeX files if accessible |
| `03_math_inline_display` | 15-20 | inline math plus display equations in prose | HF formula data + arXiv/TeX wrappers |
| `04_math_aligned` | 10-15 | align/gather/multline/cases/matrices | HF formula data, arXiv snippets |
| `05_tables_simple` | 15-20 | regular tabular grids, captions | HF arXiv LaTeX Tables 43k |
| `06_tables_moderate` | 15-20 | booktabs, multicolumn headers, clines | HF arXiv LaTeX Tables 43k |
| `07_figures_captions` | 10-15 | includegraphics/rules/placeholders, captions | arXiv source, TeX Live class samples |
| `08_crossrefs_citations` | 12-18 | labels, refs, cites, bibliography | arXiv source excerpts |
| `09_algorithms` | 8-12 | algorithm/pseudocode environments | arXiv source corpus filtered by env |
| `10_compact_papers` | 12-18 | 2-3 page article-like docs combining simple features | arXiv source archives, class templates |
| `11_forms_cv_letters` | 8-12 | non-paper structured layouts | TeX Live/CTAN templates |

This gives roughly 127-183 accepted samples. It is enough to understand behavior and metrics without being swallowed by diagrams.

## Sample Length Rules

Each accepted sample should be:

- 1-3 rendered PDF pages.
- Preferably at least 20 nonblank source lines, unless it is a deliberate short construct sample.
- Not just a one-line formula or one-line table.
- If sourced from a formula/table dataset, wrap multiple related examples into one source-backed document so the data point has substance.

Suggested minimums:

| Type | Minimum content |
|---|---|
| prose/list/citation sample | 250-800 words or 1-3 pages |
| formula sample | 4-8 formulas plus short source-backed/context prose where possible |
| table sample | 2-4 related tables or one substantial table with caption |
| compact paper | title, abstract, 2-4 sections, at least one equation/table/figure/ref |
| algorithm sample | one algorithm plus surrounding explanatory prose |

## Hugging Face Source Assessment

### Strong: `piushorn/arxiv-latex-tables-43k`

Use this for table categories. It is the cleanest HF source found for the immediate benchmark.

Useful facts from the dataset card:

- 43,651 tables.
- Extracted from arXiv papers from December 2025.
- Complexity labels: simple, moderate, complex.
- Dataset says all tables compile with `pdflatex`.
- Fields include `tabular` and `complexity`.
- Tables were extracted from redistributable Creative Commons arXiv papers.

Use:

- `05_tables_simple`
- `06_tables_moderate`
- Later hard/stress category for complex tables, but not first headline.

Important caveat:

- Complexity labels were produced by GPT-5-mini, so use them as sampling strata, not ground-truth evaluation labels.

Source: https://huggingface.co/datasets/piushorn/arxiv-latex-tables-43k

### Useful but narrow: `OleehyO/latex-formulas`

Use this for math categories, but not as standalone one-line samples.

Useful facts from the dataset card:

- Has `cleaned_formulas` and `raw_formulas`.
- `cleaned_formulas` has about 552k rows; raw has about 1.01M rows.
- Rows include `latex_formula` and rendered image data.
- Examples include real `align*` formulas.

Use:

- `03_math_inline_display`
- `04_math_aligned`

Important caveat:

- This is image-to-LaTeX/OCR-style data, not document-level LaTeX.
- Build document-level samples by grouping formulas into small pdfLaTeX documents.
- Prefer formulas that compile cleanly and avoid very exotic macros for the first pass.

Source: https://huggingface.co/datasets/OleehyO/latex-formulas

### Useful as source pool, not direct final data: `KiteFishAI/arxiv-tex-corpus-full`

Use this as a large source-backed candidate pool for prose, algorithms, crossrefs, citations, and compact papers.

Useful facts from the dataset card:

- About 80GB structured JSONL.
- Contains LaTeX source extracted from arXiv.
- Restricted to `math`, `cs`, `hep-th`, `hep-ph`, `quant-ph`, `stat.ML`, `stat.TH`.
- Fields include `paper_id`, `category`, and `latex`.
- No semantic cleaning, no LaTeX normalization, and no compilation validation were enforced.
- Licensing varies by original paper.

Use:

- Discover candidate snippets and compact papers.
- Filter by regex for `\section`, `\begin{abstract}`, `\cite`, `\label`, `algorithm`, `theorem`, etc.
- Compile-gate everything locally.

Important caveat:

- Do not redistribute raw samples blindly. Verify license or fetch source from arXiv using license-filtered IDs.

Source: https://huggingface.co/datasets/KiteFishAI/arxiv-tex-corpus-full

### Good license/ID source, not direct LaTeX: `common-pile/arxiv_papers`

Use this for arXiv IDs and license-filtering, not for direct benchmark `.tex`.

Useful facts from the dataset card:

- Includes papers under CC BY, CC BY-SA, and CC0.
- Pipeline downloaded LaTeX source from arXiv, converted it with LaTeXML to HTML, then converted HTML to plaintext.
- Dataset has 321,336 documents and 21GB UTF-8 text.

Use:

- Discover redistributable arXiv IDs.
- Fetch actual source archives from arXiv separately.

Important caveat:

- The dataset content is plaintext, not original `.tex`.

Source: https://huggingface.co/datasets/common-pile/arxiv_papers

### Lower priority: `bigcode/the-stack`

The Stack includes `tex` as one of its languages and has file-level provenance/licensing metadata, but it is gated and code-repository oriented.

Use only if needed for:

- templates
- class examples
- assignments/problem sheets
- letters/CVs from permissively licensed repos

Important caveat:

- Access requires accepting dataset terms.
- TeX files from GitHub may be noisy and duplicated.
- It is not as clean as tables/formulas/arXiv for this benchmark.

Source: https://huggingface.co/datasets/bigcode/the-stack

## Recommended First Dataset Build

Build `data/simple_benchmark_v0`, separate from current TeX Live seeds.

The current canonical first-pass dataset is `data/simple_benchmark_all_v0` with 166 accepted, source-backed, `pdflatex`-validated samples across the 11 intended simple categories:

- 15 `01_prose_sections`
- 15 `02_lists_formatting`
- 18 `03_math_inline_display`
- 15 `04_math_aligned`
- 18 `05_tables_simple`
- 18 `06_tables_moderate`
- 15 `07_figures_captions`
- 15 `08_crossrefs_citations`
- 12 `09_algorithms`
- 15 `10_compact_papers`
- 10 `11_forms_cv_letters`

Preview: `data/simple_benchmark_all_v0/previews/simple_benchmark_all_v0_preview.pdf`

The preview PDF is sectioned by category and contains one preview page per accepted data point. Older split slices remain useful as source pools, but should not be treated as the canonical v0 dataset.

```text
data/simple_benchmark_v0/
  corpus/
    01_prose_sections/
    02_lists_formatting/
    03_math_inline_display/
    04_math_aligned/
    05_tables_simple/
    06_tables_moderate/
    07_figures_captions/
    08_crossrefs_citations/
    09_algorithms/
    10_compact_papers/
    11_forms_cv_letters/
  manifests/
    candidates.csv
    accepted.csv
    rejected.csv
    sources.csv
  previews/
    simple_benchmark_v0_preview.pdf
```

Each accepted sample folder:

```text
<sample_id>/
  main.tex
  reference.pdf
  compile.log
  provenance.json
  source_assets/
```

## Selection Logic

1. Start with tables and formulas because HF sources are clean and easy to sample.
2. Build arXiv compact/excerpt categories using Common Pile IDs for license filtering where possible.
3. Use KiteFish only as a candidate source when Common Pile does not expose enough original `.tex`.
4. Use TeX Live/CTAN only for gaps: lists, forms, letters, CVs, simple figures.
5. Defer TikZ/PGFPlots/complex diagrams to a later hard dataset.

## Quality Gates

Accept only if:

- `pdflatex` compiles locally.
- PDF is 1-3 pages.
- PDF is not blank and text can be extracted where text is expected.
- Source is not trivially tiny unless explicitly categorized as a short construct sample.
- Provenance and license status are recorded.
- The sample has a clear category and a single primary difficulty reason.

Reject if:

- requires shell escape
- requires LuaLaTeX/XeLaTeX for v0
- missing assets
- too diagram-heavy
- too long
- too short without a clear reason
- unclear source/license

## Why This Is Better

This gives the old dataset's clarity without its credibility problem:

- categories are readable and benchmarkable
- samples are longer than a few lines
- tables and formulas come from known HF datasets
- prose/citation/paper categories come from real arXiv/TeX sources
- diagrams are not allowed to dominate the first benchmark
- hard mixed TeX Live examples remain available as a later stress set
