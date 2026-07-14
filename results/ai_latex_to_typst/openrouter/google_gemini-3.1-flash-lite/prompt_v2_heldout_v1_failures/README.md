# AI LaTeX-to-Typst prompt-development run

This directory is a self-contained audit record for one prompt/model configuration.
The 50 clean filtered samples are development data; results here are not held-out benchmark claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_v2.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no

## Results

- Recorded samples: 50/50
- Samples reaching model-output evaluation: 50
- API/provider/local runner failures: 0
- First-pass compile rate: 17/50 (34.0%)
- Repair success: 22/33 (66.7%)
- Final compile rate: 39/50 (78.0%)
- Page-count match among compiled outputs: 30/39 (76.9%)
- Prompt tokens: 279714
- Completion tokens: 115903
- API-reported cost: $0.241949
- Budget-accounted cost: $0.241949

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|
| `01_prose_sections` | 2 | 1 | 2 | 1 |
| `02_lists_formatting` | 1 | 1 | 1 | 0 |
| `03_math_inline_display` | 9 | 6 | 9 | 3 |
| `04_math_aligned` | 8 | 4 | 7 | 3 |
| `05_tables_simple` | 11 | 1 | 8 | 7 |
| `06_tables_moderate` | 8 | 0 | 5 | 5 |
| `07_figures_captions` | 1 | 0 | 1 | 1 |
| `08_crossrefs_citations` | 4 | 2 | 3 | 1 |
| `09_algorithms` | 3 | 1 | 2 | 1 |
| `10_compact_papers` | 3 | 1 | 1 | 0 |

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
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v2_heldout_v1_failures
```
