# AI LaTeX-to-Typst prompt-development run

This directory is a self-contained audit record for one prompt/model configuration.
The 30 clean filtered samples are development data; results here are not held-out benchmark claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_v0.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no

## Results

- Recorded samples: 30/30
- Samples reaching model-output evaluation: 30
- API/provider/local runner failures: 0
- First-pass compile rate: 15/30 (50.0%)
- Repair success: 7/15 (46.7%)
- Final compile rate: 22/30 (73.3%)
- Page-count match among compiled outputs: 17/22 (77.3%)
- Prompt tokens: 91831
- Completion tokens: 46301
- API-reported cost: $0.092409
- Budget-accounted cost: $0.092409

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|
| `01_prose_sections` | 2 | 2 | 2 | 0 |
| `02_lists_formatting` | 3 | 1 | 2 | 1 |
| `03_math_inline_display` | 3 | 2 | 2 | 0 |
| `04_math_aligned` | 3 | 2 | 2 | 0 |
| `05_tables_simple` | 3 | 2 | 3 | 1 |
| `06_tables_moderate` | 3 | 2 | 2 | 0 |
| `07_figures_captions` | 3 | 1 | 3 | 2 |
| `08_crossrefs_citations` | 3 | 0 | 2 | 2 |
| `09_algorithms` | 3 | 0 | 0 | 0 |
| `10_compact_papers` | 1 | 0 | 1 | 1 |
| `11_forms_cv_letters` | 3 | 3 | 3 | 0 |

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
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0
```
