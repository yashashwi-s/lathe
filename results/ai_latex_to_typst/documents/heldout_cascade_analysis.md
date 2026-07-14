# Held-out cascade analysis

Clean held-out samples: 127
Final compiled after v1-v3 cascade: 126/127
Page-count matches among compiled outputs: 106
API-reported cost: $0.784436

## Stage summaries

| Stage | Samples run | First-pass compiled | Final compiled | Repaired | Cost |
|---|---:|---:|---:|---:|---:|
| `v1` | 127 | 46 | 77 | 31 | $0.486724 |
| `v2` | 50 | 17 | 39 | 22 | $0.241949 |
| `v3` | 11 | 6 | 10 | 4 | $0.055763 |

## Selected final stage

| Stage | Samples |
|---|---:|
| `failed` | 1 |
| `v1` | 77 |
| `v2` | 39 |
| `v3` | 10 |

## By category

| Category | Compiled | Total |
|---|---:|---:|
| `01_prose_sections` | 11 | 11 |
| `02_lists_formatting` | 12 | 12 |
| `03_math_inline_display` | 15 | 15 |
| `04_math_aligned` | 12 | 12 |
| `05_tables_simple` | 15 | 15 |
| `06_tables_moderate` | 14 | 15 |
| `07_figures_captions` | 12 | 12 |
| `08_crossrefs_citations` | 12 | 12 |
| `09_algorithms` | 9 | 9 |
| `10_compact_papers` | 7 | 7 |
| `11_forms_cv_letters` | 7 | 7 |

## Remaining failures

| Sample | Category | Last stage |
|---|---|---|
| `06_tables_moderate_030` | `06_tables_moderate` | `v3` |

## Interpretation

v1 is the broad held-out run. v2 and v3 are targeted rescue prompts written after observing failure patterns, so the cascade result should be reported separately from the single-prompt v1 held-out result.
