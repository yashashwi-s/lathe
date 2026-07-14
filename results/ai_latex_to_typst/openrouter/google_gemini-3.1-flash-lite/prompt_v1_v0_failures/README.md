# AI LaTeX-to-Typst prompt-development run

This directory is a self-contained audit record for one prompt/model configuration.
The 8 clean filtered samples are development data; results here are not held-out benchmark claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_v1.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no

## Results

- Recorded samples: 8/8
- Samples reaching model-output evaluation: 8
- API/provider/local runner failures: 0
- First-pass compile rate: 3/8 (37.5%)
- Repair success: 3/5 (60.0%)
- Final compile rate: 6/8 (75.0%)
- Page-count match among compiled outputs: 4/6 (66.7%)
- Prompt tokens: 26244
- Completion tokens: 11018
- API-reported cost: $0.023088
- Budget-accounted cost: $0.023088

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|
| `02_lists_formatting` | 1 | 0 | 1 | 1 |
| `03_math_inline_display` | 1 | 1 | 1 | 0 |
| `04_math_aligned` | 1 | 0 | 1 | 1 |
| `06_tables_moderate` | 1 | 1 | 1 | 0 |
| `08_crossrefs_citations` | 1 | 0 | 1 | 1 |
| `09_algorithms` | 3 | 1 | 1 | 0 |

## Files

- `run_config.json`: immutable run parameters and prompt hashes.
- `run_manifest.csv`: one compact row per completed sample.
- `compilation_errors.md`: grouped final failure summaries.
- `compilation_errors.csv`: every failed compile attempt in machine-readable form.
- `compilation_warnings.csv`: every compiler warning occurrence.
- `analysis.md`: interpreted failure patterns and prompt-development recommendations.
- `system_prompt.txt`, `retry_prompt.txt`, and `split_manifest.csv`: exact run snapshots.
- `samples/<sample_id>/`: raw responses, normalized Typst, compiler logs, PDFs, and metadata.

Regenerate this report with:

```bash
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_v0_failures
```
