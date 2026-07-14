# AI LaTeX-to-Typst prompt-development run

This directory is a self-contained audit record for one prompt/model configuration.
The 127 clean filtered samples are development data; results here are not held-out benchmark claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_v1.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no

## Results

- Recorded samples: 127/127
- Samples reaching model-output evaluation: 127
- API/provider/local runner failures: 0
- First-pass compile rate: 46/127 (36.2%)
- Repair success: 31/81 (38.3%)
- Final compile rate: 77/127 (60.6%)
- Page-count match among compiled outputs: 70/77 (90.9%)
- Prompt tokens: 526251
- Completion tokens: 237385
- API-reported cost: $0.486724
- Budget-accounted cost: $0.486724

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|
| `01_prose_sections` | 11 | 7 | 9 | 2 |
| `02_lists_formatting` | 12 | 9 | 11 | 2 |
| `03_math_inline_display` | 15 | 2 | 6 | 4 |
| `04_math_aligned` | 12 | 0 | 4 | 4 |
| `05_tables_simple` | 15 | 2 | 4 | 2 |
| `06_tables_moderate` | 15 | 4 | 7 | 3 |
| `07_figures_captions` | 12 | 9 | 11 | 2 |
| `08_crossrefs_citations` | 12 | 2 | 8 | 6 |
| `09_algorithms` | 9 | 4 | 6 | 2 |
| `10_compact_papers` | 7 | 0 | 4 | 4 |
| `11_forms_cv_letters` | 7 | 7 | 7 | 0 |

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
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_heldout_clean
```
