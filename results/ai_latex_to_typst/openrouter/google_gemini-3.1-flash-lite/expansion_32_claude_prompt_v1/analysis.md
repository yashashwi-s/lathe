# Expansion evaluation analysis

This is a post-freeze difficulty evaluation on the 32 imported expansion
samples. It is not pooled with the historical 127-sample held-out result and is
not a Claude-versus-Gemini comparison.

## Outcome

- All 32 samples reached model-output evaluation; there were no API, provider,
  or local runner failures.
- Five outputs compiled on the first attempt. Eight of the 27 retry
  opportunities compiled after the single compiler-feedback repair, producing
  a final compile rate of 13/32 (40.6%).
- Eleven of the 13 compiled outputs matched the reference page count.
- The API reported 301,862 prompt tokens, 102,415 completion tokens, and
  $0.217083 total cost.
- The request headers attributed the run to the OpenRouter app title `Lathe`;
  the exact attribution URL and title are frozen in `run_config.json`.

## Difficulty by slice

| Slice | Final compile |
|---|---:|
| `i2s_equation` | 4/5 |
| `i2s_table` | 3/5 |
| `i2s_algorithm` | 3/5 |
| `i2s_plot` | 1/5 |
| `pubmed_table` | 2/5 |
| `arxiv5t_paper` | 0/5 |
| `neurips_paper` | 0/2 |

All seven full papers failed both attempts, while 10/15 equation, table, and
algorithm snippets compiled finally. TikZ/PGFPlots also remained difficult at
1/5. This supports treating full papers and programmatic plots as ceiling-raising
slices instead of silently folding them into the historical base claim.

Across the 46 failed compilation attempts, the automatic classifier recorded
22 unknown-symbol/function errors and 18 general-syntax errors. The one-repair
protocol fixed eight attempts but did not overcome long-document syntax and
source-structure failures.

## Conditional PDF fidelity

Metric v2 scored every one of the 13 compiled outputs with no evaluator
failures. These means are conditional on compilation and therefore must not be
reported as full-denominator model scores:

| Axis | Mean |
|---|---:|
| Strict word F1 | 0.6162 |
| Compatibility word F1 | 0.7201 |
| Number F1 | 0.8473 |
| Operator F1 | 0.9470 |
| Matched-word reference coverage | 0.6935 |
| Block-transport combined similarity | 0.5471 |
| Text-LTSim page macro | 0.7131 |
| Registered ink F1 | 0.2709 |
| Registered SSIM | 0.7683 |
| Page-break F1 | 0.8128 |

The evaluator intentionally emits no aggregate score. Exact per-pair evidence
is in `metric_v2/evidence/`, with the flat result table in
`metric_v2/metric_v2_scores.csv`.

## Gate-first interpretation

The metric-harness report showed that a blended visual/content number can hide
wrong text or numbers. Applying its non-compensating ladder to these 13
compiled expansion outputs gives:

- Exact page count: 11/13.
- Strict token recall >= 0.95: 3/13.
- Strict token precision >= 0.95: 3/13.
- Number F1 = 1 when numbers are present: 0/13.
- All four gates: 0/13.

This is stricter—and more useful—than saying the PDFs merely look similar.
Three outputs passed the first three gates and missed only exact numeric
content. The independent driver means were 0.2709 registered ink F1, 0.7131
Text-LTSim, and 0.2327 token-center q90. SSIM, page-break F1, and strict word F1
remain diagnostics rather than optimization targets. The per-output evidence is
in `metric_v2/gate_ladder.md`, `.csv`, and `.json`.
