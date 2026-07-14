# AI LaTeX-to-Typst prompt-development run

This directory is a self-contained audit record for one prompt/model configuration.
The 2 clean filtered samples are development data; results here are not held-out benchmark claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_v3.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no

## Results

- Recorded samples: 2/2
- Samples reaching model-output evaluation: 2
- API/provider/local runner failures: 0
- First-pass compile rate: 2/2 (100.0%)
- Repair success: n/a
- Final compile rate: 2/2 (100.0%)
- Page-count match among compiled outputs: 2/2 (100.0%)
- Prompt tokens: 2900
- Completion tokens: 1222
- API-reported cost: $0.002558
- Budget-accounted cost: $0.002558

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|
| `09_algorithms` | 2 | 2 | 2 | 0 |

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
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v3_prompt_dev_failures
```
