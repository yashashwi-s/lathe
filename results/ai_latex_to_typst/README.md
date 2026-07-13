# AI LaTeX-to-Typst experiments

This directory contains source-only LLM conversion experiments for
`data/latex_benchmark_v0`. It is separate from the deterministic engine results
in `results/latex_benchmark_v0`.

## Evaluation protocol

1. Send the versioned system prompt and complete `main.tex` source.
2. Preserve the raw model response.
3. Remove only outer Markdown code fences, if present.
4. Compile the normalized source with Typst 0.14.2.
5. On failure, send the exact sanitized compiler output once and request the
   complete corrected document.
6. Report first-pass compilation, repair success, and final compilation
   separately.

Reference images are not supplied. This keeps the task a source-to-source
LaTeX-to-Typst conversion benchmark rather than a multimodal reconstruction
task.

## Development and test separation

`data/latex_benchmark_v0/splits/prompt_dev_33.csv` is used to develop prompts.
It contains three samples from every category. These 33 samples must not be
included in final held-out benchmark claims. The remaining dataset is reserved
until the prompt and runtime parameters are frozen.

## Layout

```text
results/ai_latex_to_typst/
  README.md
  openrouter/<model>/<prompt_version>/
    README.md
    run_config.json
    system_prompt.txt
    retry_prompt.txt
    prompt_dev_33.csv
    run_manifest.csv
    summary.json
    compilation_errors.md
    samples/<sample_id>/
      request_1.json
      response_1.json
      attempt_1.raw.txt
      attempt_1.typ
      attempt_1_compile.log
      attempt_1_api_error.log          # instead, if the request itself failed
      request_2.json                 # only after a compile failure
      response_2.json
      attempt_2.raw.txt
      attempt_2.typ
      attempt_2_compile.log
      output.typ                     # only after a successful compile
      output.pdf
      meta.json
```

No authorization header or API key is written to these artifacts.
If an API response omits its cost field, the budget guard uses token counts and
the configured maximum input/output prices as a conservative fallback.

## Commands

Build the deterministic development split:

```bash
mamba run -n lathe python scripts/ai/build_prompt_dev_split.py
```

Inspect the planned paid run without loading the API key:

```bash
mamba run -n lathe python scripts/ai/run_openrouter_typst.py
```

The dry-run writes the immutable run configuration and empty report scaffold,
but does not load `.env` or access the network.

Paid execution requires both `--execute` and `--confirm-paid-run YES`. Run that
command only after explicit approval for the intended sample count and budget.
Completed model runs are skipped by default. Samples ending in an API/provider
error are automatically retried on the next execution; `--force` is only needed
to replace a completed model run.
