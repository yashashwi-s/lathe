# AI LaTeX-to-Typst prompt-development run

This directory is a self-contained audit record for one prompt/model configuration.
The 11 clean filtered samples are development data; results here are not held-out benchmark claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_v3.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no

## Results

- Recorded samples: 11/11
- Samples reaching model-output evaluation: 11
- API/provider/local runner failures: 0
- First-pass compile rate: 6/11 (54.5%)
- Repair success: 4/5 (80.0%)
- Final compile rate: 10/11 (90.9%)
- Page-count match among compiled outputs: 6/10 (60.0%)
- Prompt tokens: 57956
- Completion tokens: 27516
- API-reported cost: $0.055763
- Budget-accounted cost: $0.055763

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|
| `04_math_aligned` | 1 | 1 | 1 | 0 |
| `05_tables_simple` | 3 | 3 | 3 | 0 |
| `06_tables_moderate` | 3 | 0 | 2 | 2 |
| `08_crossrefs_citations` | 1 | 1 | 1 | 0 |
| `09_algorithms` | 1 | 1 | 1 | 0 |
| `10_compact_papers` | 2 | 0 | 2 | 2 |

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
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v3_heldout_v2_failures
```
