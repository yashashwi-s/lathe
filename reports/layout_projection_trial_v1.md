# Layout projection transfer trial

Status: **TRIAL - not promoted**. This is an engineering comparison, not a
human-quality validation.

## Why the trial was necessary

The frozen v1 layout projection is the q10 of exact-token matched bounding-box
IoU. It responds strongly to controlled geometric mutations, but every one of
the 156 available AI-produced Typst PDFs received exactly `0.0`. A constant
output cannot rank or diagnose the AI corpus.

## Candidate replacement

For exact-token matches, let `d90` be the q90 Euclidean distance between token
centers after normalizing each page by its own width and height. The trial
high-is-better projection is:

`layout_center_similarity = 1 - min(1, d90 / sqrt(2))`

The scale is defined by the maximum possible normalized page-diagonal distance.
The projection preserves global displacement and does not use raster
registration. It is conditional on exact-token matches and does not measure
reading order, block topology, or semantic layout.

## Frozen observations

| Check | Exact-box IoU q10 | Center q90 trial |
|---|---:|---:|
| AI outputs scored | 156 | 156 |
| AI range | 0.000-0.000 | 0.417-0.949 |
| AI median | 0.000 | 0.791 |
| Controlled adjacent ordering | 0.883 on all 157 | 0.914 on an 11-form pilot |
| Controlled target-axis drop | 0.620 on all 157 | 0.0098 on the pilot |
| Required adjacent-order gate | 0.950 | 0.950 |

The two controlled columns use different sample sizes and are not a formal
head-to-head significance test. The pilot covers one source from each of the 11
document forms and is a stopping-rule screen.

## Decision

Do not promote either projection as a real AI layout grade. Exact-box IoU is
sensitive but non-discriminative after cross-renderer transfer. Center
proximity transfers without collapsing but is too weak and misses the pilot
ordering gate. The next implementation should test a structure-aware layout
method such as an independently reproduced LTSim/PaIRS-style assignment, while
retaining raw token-center displacement as explainable evidence.

Artifacts:

- `results/metric_research_v1/full_157_v1/controlled_validation_layout_iou.json`
- `results/metric_research_v1/layout_center_pilot_11_v1/validation_layout.json`
- `results/metric_research_v1/ai_outputs_center_q90_trial_v1/summary.json`
