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
- The current canonical dataset is `data/latex_benchmark_v0`: the reviewed
  157-sample base plus the 32 accepted `dataset_expansion/` samples (189 total).
- Older TeX Live and HF scratch corpora have been moved under `archive/dataset_intermediate_corpora_2026-07-13/`.
- Treat the canonical corpus as protocol-aware slices:
  - simple isolated constructs
  - medium structured documents
  - hard mixed-layout documents
  - full multi-file papers and TikZ/PGFPlots stress cases
- Keep TeX Live/CTAN samples because they are human-authored and source-backed, but confirm package-level licenses before final redistribution.
- Preserve each sample's declared compilation protocol. The original 157
  `latex_benchmark_v0` references use pdfLaTeX; the 32 imported expansion
  references use Tectonic 0.16.9. Never recompile one slice with the other's
  engine and present it as the same reference.
- Do not apply a universal page-count cap. Follow the versioned dataset
  protocol; the dataset-expansion full-document probe accepts references up to
  12 pages.
- Preserve rejected logs; they are useful for sampler tuning.
- Rerun expansion builders into a staging corpus, then merge with
  `scripts/dataset/merge_expansion_into_v0.py`; do not point a destructive
  builder directly at the canonical 189-sample corpus.

## Dataset Review Artifacts

Each dataset slice should include:

- `accepted_manifest.csv`
- `compile_results.csv`
- `summary.md`
- `corpus/<document_form>/<sample_id>/`
- `previews/latex_benchmark_v0_preview.pdf`

Engine conversion outputs, provenance docs, comparison grids, and error reports should live under:

- `results/latex_benchmark_v0/`

The preview PDF should show one complete data point per preview page. Multi-page
reference PDFs should be tiled into a grid. Size optimization may be applied to
the review-only preview, but never to canonical `reference.pdf` files.

## AI Conversion Experiments

- Versioned LaTeX-to-Typst prompts live in `prompts/latex_to_typst/`.
- The frozen prompt-development split is `data/latex_benchmark_v0/splits/prompt_dev_33.csv`.
- The imported expansion evaluation split is
  `data/latex_benchmark_v0/splits/expansion_32.csv`. It is separate from the
  historical prompt-development and 127-document held-out claims.
- AI experiment outputs live under `results/ai_latex_to_typst/`.
- `scripts/ai/run_openrouter_typst.py` is dry-run by default. Never add
  `--execute --confirm-paid-run YES` without explicit user approval for that
  paid API test.
- Read the OpenRouter credential from `OPENROUTER` in `.env`. Never print,
  persist, or pass the key in command-line arguments.
- Prompt-development samples are development data and cannot be included in
  final held-out benchmark claims.
- OpenRouter requests must attribute the app with
  `HTTP-Referer: https://github.com/yashashwi-s/lathe` and
  `X-OpenRouter-Title: Lathe`.
- The canonical Gemini expansion run uses `google/gemini-3.1-flash-lite`,
  `prompts/latex_to_typst/system_expansion_v1.txt`,
  `prompts/latex_to_typst/retry_v1.txt`, and the `expansion_32.csv` split. Its
  prompt intentionally derives from the PR's Claude one-turn visual-fidelity
  prompt while keeping the model and provider protocol separate.
- Interpret metric-v2 results with the non-compensating ladder validated by
  `metric_research/report/metric_harness_report.pdf`: exact page count, strict
  token recall >= 0.95, strict token precision >= 0.95, then number F1 = 1
  when numbers are present. Only after those gates report registered ink F1
  and Text-LTSim (higher is better) plus token-center q90 (lower is better).
  SSIM, page-break F1, and strict word F1 are report-only diagnostics.
- Never replace the metric-v2 evidence vector with a blended overall score.
  `driver_mean` is permitted only as a clearly labeled harness/checkpoint
  convenience value after gate count, never as a benchmark claim.

## Canonical Rebuild Order

```bash
mamba run -n lathe python dataset_expansion/scripts/build_snippet_sets.py 5 --corpus <staging>/corpus
env HF_HUB_DOWNLOAD_TIMEOUT=300 HF_XET_HIGH_PERFORMANCE=1 mamba run -n lathe python dataset_expansion/scripts/build_fulldoc_sets.py --n 5 --max-pages 12 --max-chars 60000 --scan 400 --neurips-shards 2 --corpus <staging>/corpus
env HF_HUB_DOWNLOAD_TIMEOUT=300 HF_XET_HIGH_PERFORMANCE=1 mamba run -n lathe python dataset_expansion/scripts/rebuild_neurips_protocol.py --corpus <staging>/corpus
mamba run -n lathe python scripts/dataset/merge_expansion_into_v0.py --expansion-corpus <staging>/corpus
mamba run -n lathe python scripts/dataset/convert_all_v0_engines.py --split data/latex_benchmark_v0/splits/expansion_32.csv
mamba run -n lathe python scripts/dataset/build_review_documents.py
```

The stable NeurIPS recovery step is required because the upstream dataset was
re-sharded after PR #2. It restores the PR's accepted arXiv IDs instead of
silently accepting new positional rows.

## Repo Hygiene

- After one-off data repair or migration scripts have served their purpose,
  remove them or archive the result in a documented artifact instead of leaving
  stale maintenance entry points in `scripts/`.
- Keep reusable scripts only when they regenerate a current dataset/report or
  support an active benchmark workflow.

## Skills / External Agent Notes

- Reference for future Codex skill-style workflow ideas:
  https://github.com/multica-ai/andrej-karpathy-skills
