# Prompt-development split

This directory contains the frozen development split used to improve the LaTeX-to-Typst system prompt before the held-out benchmark is run.

## Split contract

- Clean samples after visual-corruption cleanup: 30
- Original target before cleanup: 33 samples, 11 categories, 3 samples per category
- AI outputs are not used during selection.
- These samples are development data and must not contribute to final held-out benchmark claims.

## Current category counts

| Category | Samples |
|---|---:|
| `01_prose_sections` | 2 |
| `02_lists_formatting` | 3 |
| `03_math_inline_display` | 3 |
| `04_math_aligned` | 3 |
| `05_tables_simple` | 3 |
| `06_tables_moderate` | 3 |
| `07_figures_captions` | 3 |
| `08_crossrefs_citations` | 3 |
| `09_algorithms` | 3 |
| `10_compact_papers` | 1 |
| `11_forms_cv_letters` | 3 |

## Complexity bands

| Band | Samples |
|---|---:|
| `low` | 10 |
| `medium` | 10 |
| `high` | 10 |

## Selection method

Samples were originally ranked within each category using a documented complexity score:

| Component | Weight |
|---|---:|
| Source characters | 0.30 |
| Structural LaTeX constructs | 0.25 |
| Nonblank source lines | 0.15 |
| Reference page count | 0.15 |
| Failed deterministic Typst engines | 0.15 |

Rows with visually corrupted reference PDFs were removed after review rather than replaced, so this split remains an audit of the original prompt-development run with invalid references filtered out.

`prompt_dev_33.csv` is retained as the filename for continuity, but it now contains only clean rows.
