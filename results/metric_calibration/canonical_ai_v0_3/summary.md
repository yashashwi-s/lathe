# Canonical AI audit - pdf_fidelity_scorecard_v0.3

Each row is one exact model/run protocol on one canonical hard sample. Agentic and one-turn protocols are not pooled. No aggregate fidelity score is computed.

## Protocol results

| Protocol | Available | Pass | Review | Fail | Mean token P/R | Mean layout | Mean appearance |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gemini_prompt_stage_cascade` | 8/8 | 0 | 0 | 8 | 85.1/81.9 | 36.4 | 8.2 |
| `opus_agentic_v3_visual_medium` | 6/6 | 1 | 1 | 4 | 93.1/96.5 | 80.6 | 58.9 |
| `opus_one_turn_low` | 2/2 | 0 | 0 | 2 | 80.6/67.8 | 62.5 | 17.6 |
| `sonnet_agentic_v1_visual_low` | 6/6 | 2 | 1 | 3 | 93.7/97.2 | 67.7 | 38.0 |
| `sonnet_one_turn_low` | 1/2 | 0 | 0 | 1 | 84.4/70.8 | 57.8 | 10.3 |

## Interpretation

Status is a gate-and-review outcome, not a preference ranking. Axis means are descriptive within one protocol only. Formula and table diagnostics are extraction-dependent proxies. Manual visual audit is required for disagreements and low-evidence cases.

## Reproduce

```bash
mamba run -n lathe python scripts/evaluation/audit_canonical_ai_models.py
```
