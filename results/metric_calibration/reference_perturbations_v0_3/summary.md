# Real-reference perturbation study — pdf_fidelity_scorecard_v0.3

This self-supervised calibration study applies source-known perturbations to real benchmark reference PDFs. It validates invariance and detector behavior without human preference labels.

References: 11 (one per benchmark category). Comparisons: 186.

## Detector checks

| Invariant / expected detector | Hits | Total | Rate |
|---|---:|---:|---:|
| identity clone has no flags | 11 | 11 | 100.0% |
| 1pt translation has no hard failure | 11 | 11 | 100.0% |
| 15pct deletion fails token recall | 11 | 11 | 100.0% |
| 20-word addition lowers precision | 11 | 11 | 100.0% |
| numeric change raises diagnostic | 11 | 11 | 100.0% |
| extra page fails page count | 11 | 11 | 100.0% |
| missing page fails page count | 3 | 3 | 100.0% |
| reorder lowers page sequence | 3 | 3 | 100.0% |
| severe obstruction raises structure or appearance signal | 11 | 11 | 100.0% |
| nontext erasure lowers nontext score | 6 | 6 | 100.0% |
| table row erasure changes extracted topology | 1 | 1 | 100.0% |
| formula glyph erasure lowers glyph recall | 7 | 7 | 100.0% |

## Monotonic response

| Family | Passing sample series | Total | Rate |
|---|---:|---:|---:|
| `translation` | 11 | 11 | 100.0% |
| `word_deletion` | 11 | 11 | 100.0% |
| `word_addition` | 11 | 11 | 100.0% |
| `obstruction` | 11 | 11 | 100.0% |
| `crop` | 11 | 11 | 100.0% |

## Interpretation boundary

Known corruptions can validate sensitivity, monotonicity, and exact structural gates. They cannot define aesthetic preference or an acceptable real conversion threshold. Therefore this study can justify detector revisions and abstention rules, but not a fitted overall score.

Non-monotonic series requiring inspection: 0.

## Reproduce

```bash
mamba run -n lathe python scripts/evaluation/evaluate_reference_perturbations.py
```

Raw results: `results/metric_calibration/reference_perturbations_v0_3/reference_perturbation_scores.csv`.
