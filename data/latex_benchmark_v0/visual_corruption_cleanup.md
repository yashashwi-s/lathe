# Visual corruption cleanup

Date: 2026-07-13

These samples were removed from the accepted corpus because their reference PDFs compile but visibly contain raw TeX/font macro fragments. They are retained under `data/latex_benchmark_v0/rejected/` for auditability.

- Removed from accepted corpus: 9
- Accepted corpus after cleanup: 157

## Rejected samples

| Sample | Reason |
|---|---|
| `01_prose_sections_005` | cm* font declarations/raw @ macro spill in rendered reference |
| `01_prose_sections_015` | raw FILE banner and cm* font declarations visible in rendered reference |
| `10_compact_papers_003` | magscale/raw @ macro/font-token spill in rendered reference |
| `10_compact_papers_007` | cm* font scaled declarations visible in rendered reference |
| `10_compact_papers_008` | raw FILE banner/harvmac text visible in rendered reference |
| `10_compact_papers_009` | raw @ macro spill in rendered reference |
| `10_compact_papers_010` | cm* font scaled declarations visible in rendered reference |
| `10_compact_papers_013` | magscale/raw @ macro/font-token spill in rendered reference |
| `10_compact_papers_014` | raw FILE banner and cm* font declarations visible in rendered reference |

## Moved directories

| Sample | From | To |
|---|---|---|
| `10_compact_papers_003` | `data/latex_benchmark_v0/corpus/10_compact_papers/10_compact_papers_003` | `data/latex_benchmark_v0/rejected/10_compact_papers/10_compact_papers_003` |
| `10_compact_papers_007` | `data/latex_benchmark_v0/corpus/10_compact_papers/10_compact_papers_007` | `data/latex_benchmark_v0/rejected/10_compact_papers/10_compact_papers_007` |
| `10_compact_papers_008` | `data/latex_benchmark_v0/corpus/10_compact_papers/10_compact_papers_008` | `data/latex_benchmark_v0/rejected/10_compact_papers/10_compact_papers_008` |
| `10_compact_papers_009` | `data/latex_benchmark_v0/corpus/10_compact_papers/10_compact_papers_009` | `data/latex_benchmark_v0/rejected/10_compact_papers/10_compact_papers_009` |
| `10_compact_papers_010` | `data/latex_benchmark_v0/corpus/10_compact_papers/10_compact_papers_010` | `data/latex_benchmark_v0/rejected/10_compact_papers/10_compact_papers_010` |
| `10_compact_papers_013` | `data/latex_benchmark_v0/corpus/10_compact_papers/10_compact_papers_013` | `data/latex_benchmark_v0/rejected/10_compact_papers/10_compact_papers_013` |
| `10_compact_papers_014` | `data/latex_benchmark_v0/corpus/10_compact_papers/10_compact_papers_014` | `data/latex_benchmark_v0/rejected/10_compact_papers/10_compact_papers_014` |
| `01_prose_sections_005` | `data/latex_benchmark_v0/corpus/01_prose_sections/01_prose_sections_005` | `data/latex_benchmark_v0/rejected/01_prose_sections/01_prose_sections_005` |
| `01_prose_sections_015` | `data/latex_benchmark_v0/corpus/01_prose_sections/01_prose_sections_015` | `data/latex_benchmark_v0/rejected/01_prose_sections/01_prose_sections_015` |

## Filtered split/report rows

| File | Rows removed |
|---|---:|
| `data/latex_benchmark_v0/splits/prompt_dev_33.csv` | 3 |
| `data/latex_benchmark_v0/splits/prompt_v1_v0_failures_10.csv` | 2 |
| `results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/prompt_dev_33.csv` | 3 |
| `results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/split_manifest.csv` | 3 |
| `results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_v0_failures/split_manifest.csv` | 2 |

## Updated accepted counts

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

## Notes

- Stale engine output directories and AI sample output directories for rejected samples were removed.
- Stale AI comparison grid files were removed and rebuilt from the cleaned split.
