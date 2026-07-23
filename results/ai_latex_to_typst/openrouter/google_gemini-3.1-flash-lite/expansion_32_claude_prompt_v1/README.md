# AI LaTeX-to-Typst expansion evaluation

This directory is a self-contained audit record for one prompt/model configuration.
These 32 dataset-expansion samples are a targeted post-freeze evaluation; they are excluded from the historical 30-document prompt-development and 127-document held-out claims.

## Configuration

- Model: `google/gemini-3.1-flash-lite`
- Prompt: `prompts/latex_to_typst/system_expansion_v1.txt`
- Typst: `typst 0.14.2 (unknown hash)`
- Maximum repair attempts: 1
- Reference images supplied: no
- Source graphics available during compile: yes
- OpenRouter app attribution: `Lathe`

## Results

- Recorded samples: 32/32
- Samples reaching model-output evaluation: 32
- API/provider/local runner failures: 0
- First-pass compile rate: 5/32 (15.6%)
- Repair success: 8/27 (29.6%)
- Final compile rate: 13/32 (40.6%)
- Page-count match among compiled outputs: 11/13 (84.6%)
- Prompt tokens: 301862
- Completion tokens: 102415
- API-reported cost: $0.217083
- Budget-accounted cost: $0.217083

## By category

| Category | Completed | First pass | Final | Repaired |
|---|---:|---:|---:|---:|
| `arxiv5t_paper` | 5 | 0 | 0 | 0 |
| `i2s_algorithm` | 5 | 1 | 3 | 2 |
| `i2s_equation` | 5 | 3 | 4 | 1 |
| `i2s_plot` | 5 | 0 | 1 | 1 |
| `i2s_table` | 5 | 1 | 3 | 2 |
| `neurips_paper` | 2 | 0 | 0 | 0 |
| `pubmed_table` | 5 | 0 | 2 | 2 |

## Files

- `run_config.json`: immutable run parameters and prompt hashes.
- `run_manifest.csv`: one compact row per completed sample.
- `compilation_errors.md`: grouped final failure summaries.
- `compilation_errors.csv`: every failed compile attempt in machine-readable form.
- `compilation_warnings.csv`: every compiler warning occurrence.
- `analysis.md`: interpretation of this frozen run and its conditional PDF metrics.
- `metric_v2/gate_ladder.{md,csv,json}`: non-compensating correctness gates and independent drivers.
- `system_prompt.txt`, `retry_prompt.txt`, and `split_manifest.csv`: exact run snapshots.
- `samples/<sample_id>/`: raw responses, normalized Typst, compiler logs, PDFs, and metadata.

Regenerate this report with:

```bash
mamba run -n lathe python scripts/ai/report_openrouter_typst.py results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/expansion_32_claude_prompt_v1
```
