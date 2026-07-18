# Prompt-development audit — pdf_fidelity_scorecard_v0.2-dev

This is development data used to find gate disagreements for automated stress testing. It is not a held-out benchmark result.

## Status distribution

| Status | Samples |
|---|---:|
| `pass` | 0 |
| `review` | 9 |
| `fail` | 21 |

## Failed critical gates

| Gate | Samples |
|---|---:|
| `token_recall` | 20 |
| `token_precision` | 15 |
| `page_count` | 7 |

## Review triggers

| Trigger | Samples |
|---|---:|
| `numeric_token_mismatch` | 30 |
| `appearance_layout_disagreement` | 22 |
| `low_page_sequence_alignment` | 18 |

## Status by document form

| Category | Pass | Review | Fail |
|---|---:|---:|---:|
| `01_prose_sections` | 0 | 1 | 1 |
| `02_lists_formatting` | 0 | 1 | 2 |
| `03_math_inline_display` | 0 | 0 | 3 |
| `04_math_aligned` | 0 | 0 | 3 |
| `05_tables_simple` | 0 | 0 | 3 |
| `06_tables_moderate` | 0 | 2 | 1 |
| `07_figures_captions` | 0 | 1 | 2 |
| `08_crossrefs_citations` | 0 | 3 | 0 |
| `09_algorithms` | 0 | 0 | 3 |
| `10_compact_papers` | 0 | 1 | 0 |
| `11_forms_cv_letters` | 0 | 0 | 3 |

## Calibration use

Prioritize automated perturbation checks for: (1) samples where a critical gate fails despite strong smooth axes, (2) samples with appearance/layout disagreement, and (3) category-specific clusters. The exact numeric mismatch trigger must be audited separately on math-heavy PDFs before it can become a gate.

## Reproduce

```bash
mamba run -n lathe python scripts/evaluation/audit_prompt_dev_scorecard.py
```
