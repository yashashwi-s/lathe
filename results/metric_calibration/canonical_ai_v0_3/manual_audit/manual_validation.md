# Blind manual validation

- Rated compiled cases: 23 across 8 samples
- The reviewer saw only anonymous candidate IDs until the rubric CSV was frozen.
- Correlations are diagnostic, not population estimates: candidates within a sample share one reference and n is small.

## Spearman correlations

| Manual target | Automated metric | n | rho | p |
|---|---:|---:|---:|---:|
| content | auto_content | 23 | 0.754 | 0.000 |
| content | token_precision | 23 | 0.515 | 0.012 |
| content | token_recall | 23 | 0.636 | 0.001 |
| content | formula_character_f1 | 18 | -0.045 | 0.859 |
| layout | auto_layout | 23 | 0.817 | 0.000 |
| layout | layout_coverage | 23 | 0.697 | 0.000 |
| layout | auto_pagination | 23 | 0.911 | 0.000 |
| layout | appearance_proxy | 23 | 0.825 | 0.000 |
| typography | auto_typography | 23 | 0.401 | 0.058 |
| typography | appearance_proxy | 23 | 0.598 | 0.003 |
| structure | nontext_score | 23 | 0.318 | 0.139 |
| structure | auto_pagination | 23 | 0.694 | 0.000 |
| structure | table_row_exact | 12 | 0.577 | 0.050 |
| structure | table_column_exact | 12 | 0.279 | 0.380 |
| structure | table_cell_ratio | 12 | 0.353 | 0.260 |
| overall | auto_content | 23 | 0.689 | 0.000 |
| overall | auto_layout | 23 | 0.913 | 0.000 |
| overall | auto_typography | 23 | 0.517 | 0.011 |
| overall | appearance_proxy | 23 | 0.891 | 0.000 |
| overall | auto_pagination | 23 | 0.813 | 0.000 |
| overall | visual_core_mean | 23 | 0.909 | 0.000 |
| overall | visual_core_floor | 23 | 0.937 | 0.000 |
| overall | fidelity_core_floor | 23 | 0.937 | 0.000 |
| overall | all_axis_mean | 23 | 0.931 | 0.000 |

## Within-sample pairwise ranking

| Metric | Correct / pairs | Ties | Accuracy |
|---|---:|---:|---:|
| auto_content | 19 / 22 | 1 | 86.4% |
| auto_layout | 20 / 22 | 0 | 90.9% |
| auto_typography | 18 / 22 | 0 | 81.8% |
| appearance_proxy | 20 / 22 | 0 | 90.9% |
| appearance_local_q10 | 7 / 22 | 15 | 31.8% |
| auto_pagination | 22 / 22 | 0 | 100.0% |
| visual_core_mean | 21 / 22 | 0 | 95.5% |
| visual_core_floor | 21 / 22 | 0 | 95.5% |
| fidelity_core_floor | 21 / 22 | 0 | 95.5% |
| all_axis_mean | 21 / 22 | 0 | 95.5% |

## Leave-one-sample-out monotonic calibration

Each held-out sample is graded by a monotonic mapping fitted without any candidate from that reference.

| Input | MAE on 0-4 | rho | Rounded exact | Within one |
|---|---:|---:|---:|---:|
| auto_layout | 0.289 | 0.858 | 69.6% | 100.0% |
| appearance_proxy | 0.318 | 0.854 | 78.3% | 100.0% |
| auto_pagination | 0.490 | 0.779 | 47.8% | 100.0% |
| visual_core_mean | 0.349 | 0.866 | 65.2% | 100.0% |
| visual_core_floor | 0.260 | 0.860 | 73.9% | 100.0% |
| fidelity_core_floor | 0.260 | 0.860 | 73.9% | 100.0% |
| all_axis_mean | 0.270 | 0.898 | 69.6% | 100.0% |

## Exact-protocol summaries

Means are descriptive only because protocols cover different sample sets.

| Exact protocol | n | Blind overall mean | Cross-validated grade mean |
|---|---:|---:|---:|
| Gemini 3.1 Flash Lite - one-turn cascade | 8 | 1.62 | 1.73 |
| Claude Opus 4.7 - agentic v3 visual medium | 6 | 3.67 | 3.41 |
| Claude Opus 4.7 - one-turn low | 2 | 2.50 | 2.50 |
| Claude Sonnet 4.6 - agentic v1 visual low | 6 | 2.83 | 2.81 |
| Claude Sonnet 4.6 - one-turn low | 1 | 2.00 | 2.00 |

## Blind head-to-head on shared references

| Left protocol | Right protocol | Shared | Left wins | Right wins | Ties |
|---|---|---:|---:|---:|---:|
| Gemini 3.1 Flash Lite - one-turn cascade | Claude Opus 4.7 - agentic v3 visual medium | 6 | 0 | 6 | 0 |
| Gemini 3.1 Flash Lite - one-turn cascade | Claude Opus 4.7 - one-turn low | 2 | 0 | 2 | 0 |
| Gemini 3.1 Flash Lite - one-turn cascade | Claude Sonnet 4.6 - agentic v1 visual low | 6 | 0 | 6 | 0 |
| Gemini 3.1 Flash Lite - one-turn cascade | Claude Sonnet 4.6 - one-turn low | 1 | 0 | 1 | 0 |
| Claude Opus 4.7 - agentic v3 visual medium | Claude Sonnet 4.6 - agentic v1 visual low | 6 | 5 | 1 | 0 |
| Claude Opus 4.7 - one-turn low | Claude Sonnet 4.6 - one-turn low | 1 | 1 | 0 | 0 |
