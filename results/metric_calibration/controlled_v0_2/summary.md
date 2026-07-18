# Controlled metric study — pdf_fidelity_scorecard_v0.2-dev

This development study exercises the five-axis scorecard on synthetic, source-known PDF failures. It validates detector behavior but does not define aesthetic preference.

## Outcome

| Failure family | Target axis | Monotonic | Scores from identity → severe |
|---|---|---:|---|
| `translation` | `layout` | yes | 99.4 → 97.6 → 95.9 → 92.8 → 87.3 |
| `text_deletion` | `content_recall` | yes | 100.0 → 96.5 → 93.0 → 86.0 |
| `wrong_numbers` | `content` | yes | 100.0 → 99.1 → 98.1 → 96.0 |
| `font_substitution` | `typography` | yes | 100.0 → 91.3 → 85.3 → 77.8 |
| `obstruction` | `appearance_proxy` | yes | 100.0 → 95.8 → 92.9 → 89.7 |
| `extra_pages` | `pagination` | yes | 100.0 → 75.0 → 60.0 → 50.0 |
| `missing_pages` | `pagination` | yes | 100.0 → 66.7 → 33.3 |

## Gate behavior

- Every wrong-number case tripped the numeric-token review trigger: True.
- Every added or missing-page case tripped the exact page-count gate.
- Page reordering kept exact page count but reduced sequence alignment to 66.7 and produced status `review`.
- Obstruction leaves PDF text extraction intact; the appearance proxy is therefore the targeted signal.

## Interpretation

The scorecard now exposes directional evidence and explicit failure gates without inventing a new overall percentage. Thresholds remain provisional. The next calibration step is the stratified real-reference perturbation matrix in `reference_perturbations_v0_1`.

## Reproduce

```bash
mamba run -n lathe python scripts/evaluation/evaluate_controlled_metric_scorecard.py
```

Raw results: `results/metric_calibration/controlled_v0_2/controlled_scores.csv`.
