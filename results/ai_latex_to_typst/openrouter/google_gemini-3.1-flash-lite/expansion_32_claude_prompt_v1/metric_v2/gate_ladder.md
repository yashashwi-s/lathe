# Metric-v2 gate-ladder summary

This applies the non-compensating interpretation validated by the metric
harness report. There is no aggregate benchmark score: correctness gates
are reported first, followed by independent visual/layout drivers.

## Correctness gates

- Exact page count: 11/13
- Strict token recall >= 0.95: 3/13
- Strict token precision >= 0.95: 3/13
- Number F1 = 1 when applicable: 0/13
- All four gates: 0/13

## Independent drivers

- Mean registered ink F1 (higher is better): 0.2709
- Mean Text-LTSim page macro (higher is better): 0.7131
- Mean token center q90 (lower is better): 0.2327

SSIM, page-break F1, and strict word F1 remain report-only diagnostics.

## Per compiled output

| Sample | Gates | Failed gates | Ink F1 | LTSim | Center q90 |
|---|---:|---|---:|---:|---:|
| `i2s_algorithm_003` | 0/4 | page_count,token_recall,token_precision,number_f1 | 0.1730 | 0.7289 | 0.4782 |
| `i2s_algorithm_004` | 1/4 | token_recall,token_precision,number_f1 | 0.4157 | 0.7045 | 0.1841 |
| `i2s_algorithm_008` | 1/4 | token_recall,token_precision,number_f1 | 0.3076 | 0.7338 | 0.2740 |
| `i2s_equation_001` | 1/4 | token_recall,token_precision,number_f1 | 0.3662 | 0.7175 | 0.1324 |
| `i2s_equation_003` | 1/4 | token_recall,token_precision,number_f1 | 0.4828 | 0.7789 | 0.0518 |
| `i2s_equation_005` | 1/4 | token_recall,token_precision,number_f1 | 0.0811 | 0.7063 | 0.1362 |
| `i2s_equation_006` | 1/4 | token_recall,token_precision,number_f1 | 0.2228 | 0.7456 | 0.1280 |
| `i2s_plot_002` | 1/4 | token_recall,token_precision,number_f1 | 0.0966 | 0.6734 | 0.3746 |
| `i2s_table_006` | 1/4 | token_recall,token_precision,number_f1 | 0.3352 | 0.6962 | 0.1124 |
| `i2s_table_007` | 3/4 | number_f1 | 0.3463 | 0.7418 | 0.0904 |
| `i2s_table_008` | 3/4 | number_f1 | 0.3764 | 0.6887 | 0.1247 |
| `pubmed_table_001` | 3/4 | number_f1 | 0.1582 | 0.6714 | 0.5282 |
| `pubmed_table_004` | 0/4 | page_count,token_recall,token_precision,number_f1 | 0.1599 | 0.6828 | 0.4103 |
