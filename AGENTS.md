# Agent Coding Notes

These notes are for Codex/agent work in this repository.

## Python Environment

Always run project Python through the `lathe` mamba environment:

```bash
mamba run -n lathe python ...
```

Examples:

```bash
mamba run -n lathe python -m py_compile scripts/dataset/texlive_corpus.py
mamba run -n lathe python scripts/dataset/texlive_corpus.py --profile simple
```

Do not use bare `python`, `python3`, or system-package assumptions for project scripts unless the user explicitly asks for a one-off system check.

## Dataset Direction

- The old 15 categories were provisional, not canonical.
- The current canonical dataset is `data/latex_benchmark_v0`.
- Older TeX Live and HF scratch corpora have been moved under `archive/dataset_intermediate_corpora_2026-07-13/`.
- Build the real dataset as cleaner slices:
  - simple isolated constructs
  - medium structured documents
  - hard mixed-layout documents
- Keep TeX Live/CTAN samples because they are human-authored and source-backed, but confirm package-level licenses before final redistribution.
- Prefer pdfLaTeX-only samples for the current dataset iteration.
- Accepted reference PDFs should be 1-3 pages.
- Preserve rejected logs; they are useful for sampler tuning.

## Dataset Review Artifacts

Each dataset slice should include:

- `accepted_manifest.csv`
- `compile_results.csv`
- `summary.md`
- `corpus/<document_form>/<sample_id>/`
- `previews/latex_benchmark_v0_preview.pdf`

Engine conversion outputs, provenance docs, comparison grids, and error reports should live under:

- `results/latex_benchmark_v0/`

The preview PDF should show one complete data point per preview page. Multi-page reference PDFs should be tiled into a grid.

## AI Conversion Experiments

- Versioned LaTeX-to-Typst prompts live in `prompts/latex_to_typst/`.
- The frozen prompt-development split is `data/latex_benchmark_v0/splits/prompt_dev_33.csv`.
- AI experiment outputs live under `results/ai_latex_to_typst/`.
- `scripts/ai/run_openrouter_typst.py` is dry-run by default. Never add
  `--execute --confirm-paid-run YES` without explicit user approval for that
  paid API test.
- Read the OpenRouter credential from `OPENROUTER` in `.env`. Never print,
  persist, or pass the key in command-line arguments.
- Prompt-development samples are development data and cannot be included in
  final held-out benchmark claims.
