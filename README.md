# Lathe

Lathe is a source-only LaTeX-to-Typst conversion benchmark. The canonical
corpus contains 157 human- or dataset-sourced LaTeX documents with reviewed
pdfLaTeX references. It is designed to answer two separate questions:

1. Does a conversion produce a valid Typst document?
2. When it does, what does the rendered PDF preserve or change?

The project does **not** collapse those questions into one universal score.
Compilation is reported over the full assigned set; PDF fidelity is a vector of
content, layout, reading-order, pagination, typography, and raster evidence,
with explicit abstentions when a comparison is not valid.

## Frozen benchmark contract

| Item | Canonical state |
|---|---|
| Dataset | `data/latex_benchmark_v0`: 157 accepted, 1–3 page, pdfLaTeX references in 11 document categories |
| Prompt development | `data/latex_benchmark_v0/splits/prompt_dev_33.csv`: 30 clean documents; excluded from held-out claims |
| Primary AI test | `data/latex_benchmark_v0/splits/heldout_clean_127.csv`: 127 documents |
| Primary AI protocol | Gemini 3.1 Flash Lite, frozen prompt v1, source only, temperature 0, one compiler-feedback repair at most |
| Deterministic baselines | Pandoc, Tylax, and TypeTeX over all 157 documents |
| PDF metric | `pdf_metric_axes_v2.py`; a coverage-aware evidence vector, not a scalar rank |

The primary AI result is the single frozen v1 run on all 127 held-out
documents. Later v2/v3 rescue prompts form an adaptive cascade and are reported
only as exploratory debugging evidence. The available seven-case Claude overlap
used heterogeneous collection protocols; it is useful for case studies, not a
fair model leaderboard.

## What the metric reports

The evaluator separates transport failure from fidelity:

- **Transport:** conversion status, Typst compilation, repair use, and page
  availability. An uncompiled document remains in every full-denominator rate.
- **Content:** strict and compatibility text views plus exact inventories for
  numbers, operators, and citations.
- **Layout:** raw token geometry, published Text-LTSim on eligible page text,
  and conditional reading-order evidence.
- **Page and style:** pagination, canvas agreement, typography residuals, ink
  coverage, and fixed-protocol SSIM where the raster comparison is valid.

Every conditional statistic is paired with its eligible count. SSIM abstains
when page canvases or raster grids are incompatible. Structure-dependent table,
formula, figure, and semantic metrics abstain until both PDFs expose validated
common structures. Controlled corruptions test whether individual axes respond
to known changes; they do not create aesthetic ground truth.

## Artifact map

| Path | Role |
|---|---|
| `data/latex_benchmark_v0/` | Canonical sources, reference PDFs, manifests, provenance, rejects, preview, and frozen splits |
| `results/latex_benchmark_v0/` | Deterministic-engine Typst/PDF outputs, compile manifests, error reports, and review grids |
| `prompts/latex_to_typst/` | Versioned model prompts |
| `results/ai_latex_to_typst/` | Recorded model requests, raw and normalized outputs, compile logs, run configuration, and comparison grids |
| `results/metric_research_v2/` | Per-pair metric evidence, controlled mutations, audits, and research scorecards |
| `results/publication_v0/` | Frozen publication inputs: primary scorecard, per-sample rows, provenance, and uncertainty artifacts |
| `reports/benchmark_paper_blog.md` | Generated readable research manuscript; numeric claims come from `results/publication_v0/` |
| `reports/pdf_fidelity_metric_system_v3.typ` | Detailed metric-methodology report source |

Each accepted datum is stored as:

```text
data/latex_benchmark_v0/corpus/<category>/<sample_id>/
  main.tex
  reference.pdf
  compile.log
  provenance.json
```

Rejected candidates and their logs are retained under the dataset directory so
selection and sampler behavior remain auditable.

## Reproduction map

Run project Python only through the `lathe` mamba environment.

Evaluate one compiled reference/candidate pair:

```bash
mamba run -n lathe python scripts/evaluation/pdf_metric_axes_v2.py \
  reference.pdf candidate.pdf --pretty
```

Evaluate a CSV manifest of PDF pairs:

```bash
mamba run -n lathe python scripts/evaluation/evaluate_metric_v2_manifest.py \
  pairs.csv --out-dir results/metric_research_v2/run --workers 4
```

Regenerate and validate the publication artifacts from their frozen inputs:

```bash
mamba run -n lathe python scripts/evaluation/build_publication_scorecard_v0.py
mamba run -n lathe python scripts/evaluation/analyze_publication_results.py
mamba run -n lathe python scripts/evaluation/build_publication_manuscript.py
mamba run -n lathe python scripts/evaluation/preflight_publication_v0.py --check-only
```

The manuscript builder validates required files and fields before writing. See
[`reports/README.md`](reports/README.md) for the publication contract and
[`scripts/evaluation/README.md`](scripts/evaluation/README.md) for the metric
research commands.

The AI runner is dry-run by default:

```bash
mamba run -n lathe python scripts/ai/run_openrouter_typst.py
```

Paid execution requires both `--execute` and `--confirm-paid-run YES` and must
not be run without explicit authorization. The API key is read from
`OPENROUTER` in `.env`; it must never appear in a command or artifact.

## Provenance, licensing, and citation

Dataset origin is recorded per sample and in the accepted manifest. TeX Live
and CTAN-derived material is source-backed, but redistribution still requires a
package-level license review; inclusion in this research workspace is not a
blanket relicensing statement. Consult:

- `data/latex_benchmark_v0/manifests/accepted.csv`
- `data/latex_benchmark_v0/corpus/*/*/provenance.json`
- `results/latex_benchmark_v0/documents/dataset_provenance.pdf`

The older 48-sample, 15-category reports and their heuristic `/6` ratings are
historical artifacts. They are not the current dataset, metric, or evidence base
and should not be cited as Lathe's benchmark result.
