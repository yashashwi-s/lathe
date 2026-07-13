# AI LaTeX-to-Typst prompt-development run

This directory is a self-contained audit record for one prompt/model configuration.
The 33 samples are development data; results here are not held-out benchmark claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_v0.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no

## Results

- Recorded samples: 1/33
- Samples reaching model-output evaluation: 0
- API/provider failures: 1
- First-pass compile rate: n/a
- Repair success: n/a
- Final compile rate: n/a
- Prompt tokens: 0
- Completion tokens: 0
- API-reported cost: $0.000000
- Budget-accounted cost: $0.000000

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|

## Files

- `run_config.json`: immutable run parameters and prompt hashes.
- `run_manifest.csv`: one compact row per completed sample.
- `compilation_errors.md`: grouped final failure summaries.
- `system_prompt.txt`, `retry_prompt.txt`, and `prompt_dev_33.csv`: exact run snapshots.
- `samples/<sample_id>/`: raw responses, normalized Typst, compiler logs, PDFs, and metadata.

Regenerate this report with:

```bash
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0
```
