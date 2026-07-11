# Lathe — LaTeX → Typst Conversion Benchmark

A benchmark comparing **three deterministic LaTeX→Typst conversion engines** (Pandoc,
Tylax, TypeTeX) against **two AI models** (Gemini, GPT — manually prompted, no API) on
conversion fidelity, across a 48-sample corpus spanning 15 document categories.

Two independent evaluation layers are applied to every candidate output:

1. **A 6-point absolute rubric** on the generated Typst source and compile result
   (compiles, clean source, text completeness, structural elements, numbering
   correctness, typography) — see `reports/benchmark_findings.md`.
2. **Visual alignment** of the compiled candidate PDF against the pdflatex reference
   (text-block bounding-box IoU + Jaccard content matching for text documents; SSIM for
   graphics documents) — see `reports/visual_alignment_report.md`.

## Headline results

**Fair-Subset** (the 8 categories both AI models and engines were tested on, /6.0):

| Gemini | Tylax (patched) | TypeTeX (patched) | Pandoc (patched) | GPT |
|---|---|---|---|---|
| 5.88 | 5.50 | 5.38 | 4.88 | 4.25 |

**Full Corpus** (all 48 samples, engines only, /6.0):

| Engine | As-Tested | Patched Ceiling |
|---|---|---|
| Pandoc | 5.03 | 5.40 |
| TypeTeX | 5.08 | 5.44 |
| Tylax | 4.10 | 4.74 |

"Patched ceiling" = score after manually fixing two known, trivial, engine-specific
transcription bugs (Tylax's unescaped `@`, Pandoc/TypeTeX's `\hrule` → `#horizontalrule`
mistranslation). Details, caveats and all findings: `reports/benchmark_findings.pdf`.

## Repository layout

```
├── README.md                  ← you are here
├── data/                      # THE DATASET (do not modify)
│   ├── 01_prose … 15_beamer/  # 15 categories × {easy,medium,hard}.tex (+ 4 attention_* variants)
│   ├── manifest.csv           # every sample: category, filename, difficulty, path
│   ├── survivors.csv          # samples that passed the pdflatex compile gate
│   ├── reference_pdfs/        # ground-truth PDFs compiled from the .tex sources
│   └── typst_templates/       # clean/ugly Typst templates used during dataset design
├── results/                   # ENGINE OUTPUTS + PIPELINE METRICS
│   ├── <category>/<difficulty>/       # pandoc.typ/.pdf/.png, tylax.*, typetex_approx.*
│   │                                  # (+ *_patched.* where a manual patch was applied,
│   │                                  #  reference.png for visual checks)
│   ├── compile_metrics.csv    # per-sample compile flags per engine (48 rows)
│   ├── visual_metrics.csv     # early page-1 IoU/SSIM metrics (superseded by 18_*)
│   ├── human_ratings.csv      # manual engine rankings from the human-eval server
│   ├── gemini_feedback_eval/  # Gemini compile-feedback-loop experiment (round_0..2 per sample)
│   └── prompt_variant_scatter.png
├── ai_models/                 # AI MODEL OUTPUTS + CANONICAL SCORES
│   ├── <segment>/gemini|gpt|claude/output.typ/.pdf/.png   # 8 fair-subset segments
│   │                          # (claude outputs exist but are NOT scored in the benchmark)
│   ├── <segment>/engines/     # engine outputs copied for side-by-side prompting
│   ├── <segment>/prompt.txt   # the exact prompt given to the AI models
│   ├── absolute_scores.json   # ★ CANONICAL SCORES FILE — one record per (sample, candidate)
│   ├── retries.json           # compile-retry counts for AI models
│   ├── manual_human_ratings.csv
│   ├── compilation_errors.md  # captured AI compile errors
│   └── legacy_reports/        # superseded intermediate reports (historical only — stale numbers)
├── scripts/                   # THE PIPELINE (run everything from the repo root)
├── ai_api/                    # API-DRIVEN AI RUNS (scripts/22_run_gemini_api.py)
│   ├── <model>/<sample_id>/   # attempt_*.typ, attempt_*_error.txt, output.typ/.pdf/.png, meta.json
│   └── run_manifest.csv       # one row per finished sample (attempts, compiled, scores)
├── assets/                    # report imagery, generated from absolute_scores.json
│   ├── appendix_grids/        # 48 × 2x2 grids (Reference/Pandoc/Tylax/TypeTeX)
│   ├── fair_grids/            # 8 × 3x2 grids (adds Gemini/GPT)
│   └── examples/              # reference-vs-candidate pairs used in the visual report
├── reports/                   # THE DELIVERABLES (md sources + built PDFs)
│   ├── benchmark_findings.md/.pdf      # rubric findings report
│   ├── visual_alignment_report.md/.pdf # visual alignment report
│   └── appendix.md/.pdf                # full scores table + all 48 comparison grids
└── logs/                      # timestamped logs of visual-alignment runs
```

## The pipeline

All scripts run from the repo root, inside the `lathe` mamba env
(`mamba run -n lathe python …`). Requirements: Python with PyMuPDF (`fitz`),
`opencv-python`, `scikit-image`, `numpy`, `Pillow`, plus CLI tools `pdflatex`,
`pandoc`, `typst`, and Tylax's `t2l` (`~/.cargo/bin/t2l`).

| Stage | Script | What it does |
|---|---|---|
| 1 | `01_generate_dataset.py` | Writes the 15-category LaTeX corpus + `data/manifest.csv` |
| 2 | `02_compile_gate.py` | Compiles every sample with pdflatex → `data/reference_pdfs/`, `data/survivors.csv` |
| 3 | `03_convert_engines.py` | Runs Pandoc / Tylax / TypeTeX (= Pandoc + MiTeX Lua filter `typetex_filter.lua`) on all survivors, Typst-compiles the outputs → `results/…`, `results/compile_metrics.csv` |
| 4 | `04_compute_metrics.py` | Early page-1 IoU/SSIM screen → `results/visual_metrics.csv` (superseded by stage 18 for reporting) |
| 5 | `08_human_eval_server.py` + `09_compute_final_scores.py` | Local Flask UI for manual ranking → `results/human_ratings.csv` → aggregate table |
| 6 | `10_score_structural.py` | Standalone structural-quality scorer for a single `.typ` file |
| 7 | `13_run_gemini_eval.py` + `12_feedback_utils.py` + `14_score_gemini_loop.py` | Gemini compile-feedback-loop experiment (`results/gemini_feedback_eval/`) |
| 8 | `setup_ai_models.py` | Creates `ai_models/<segment>/` folders + prompts for manual AI prompting |
| 9 | `16_heuristic_evaluator.py` | **Rubric evaluation.** Scans `ai_models/` and `results/` and writes one record per (sample, candidate) to `ai_models/absolute_scores.json`. Detects patched variants on disk and emits both the as-tested (failure) and `_patched` records |
| 10 | `18_visual_alignment.py` | **Visual alignment.** Adds IoU/SSIM/Jaccard fields to every record in `absolute_scores.json` in place; logs to `logs/` |
| 11 | `19_generate_report_assets.py` | Renders all grids/examples in `assets/` with Match/Pos labels read from the JSON |
| 12 | `20_generate_appendix.py` | Emits `reports/appendix.md` (scores table + grid figures) from the JSON |
| 13 | `21_report_tables.py` | Prints every aggregate table used in the two main reports |
| 14 | `build_reports.sh` | Builds the three PDFs from markdown via pandoc/xelatex |
| 15 | `22_run_gemini_api.py` | **API-driven Gemini run** over all 48 samples, toughest categories first. Visual-fidelity system prompt with a Typst-vs-LaTeX cheat sheet (reference render attached), at most one retry fed the exact compiler error, 8-key rotation with per-day-quota detection (clean abort when all keys are spent), resume-safe (`--redo-failed` re-runs only failures). Outputs to `ai_api/<model>/<sample>/`, manifest at `ai_api/run_manifest.csv`, logs in `logs/gemini_api_*.log`. The system prompt injects `scripts/prompt_pitfalls.md` — append every newly discovered failure mode there |

`scoring_utils.py` holds the shared scoring rules: Option B averaging (failures stay in
the denominator), the patched-ceiling blend (patched record substituted where one
exists, base record otherwise — always exactly 48 records per engine), and per-metric
pass rates. `scripts/archive/` holds superseded one-off helpers.

### Reproducing the numbers

```bash
mamba run -n lathe python scripts/16_heuristic_evaluator.py    # rubric  → absolute_scores.json
mamba run -n lathe python scripts/18_visual_alignment.py       # alignment (in-place)
mamba run -n lathe python scripts/21_report_tables.py          # prints all report tables
mamba run -n lathe python scripts/19_generate_report_assets.py # regenerates assets/
mamba run -n lathe python scripts/20_generate_appendix.py      # regenerates reports/appendix.md
bash scripts/build_reports.sh                                  # builds the three PDFs
```

Stages 9–10 are deterministic given the on-disk artifacts; re-running them reproduces
`absolute_scores.json` exactly. Stages 1–3 would re-run the actual conversions and are
**not** needed to reproduce the reports (and should not be re-run casually — the engine
outputs in `results/` are the frozen experimental artifacts, including the manual
`*_patched.typ` files).

## Candidates

| Candidate | What it is |
|---|---|
| `pandoc` | `pandoc -f latex -t typst` |
| `tylax` | the `t2l` Rust converter |
| `typetex` | "TypeTeX approximation": pandoc with a Lua filter that delegates all math to MiTeX (`#mi(...)` / `#mitex(...)`). Stored on disk as `typetex_approx.*` |
| `*_patched` | the same output after a targeted manual fix (CV samples only; see findings #5). TypeTeX's patched files are `typetex_approx_patched.*` on disk but appear as `typetex_patched` in the scores JSON |
| `gemini`, `gpt` | manually prompted via chat UIs with `prompt.txt`; compile-retry counts in `retries.json` |
| `claude` | outputs collected but **excluded from scoring** (kept for possible future work) |

## Data & methodology caveats (read before citing numbers)

- **`beamer_hard` provenance.** Sample 48 was added after the main conversion batch. Its
  compile row was appended to `compile_metrics.csv` by inspecting the artifacts in
  `results/15_beamer/hard/`; its rubric and alignment records come from the same
  canonical scripts as all other samples. Only the conversion step itself was run
  separately.
- **Patched-ceiling semantics.** "Patched" fixes exactly two transcription bugs (Tylax
  `@`-escaping; Pandoc/TypeTeX `\hrule`). It is a capability ceiling, not out-of-the-box
  behavior.
- **Rubric is heuristic and source-level.** It scans `.typ` source with regex heuristics
  (e.g. text completeness = ≥60% word-bag overlap with the LaTeX source). It can pass a
  document whose rendered layout is broken — `beamer_hard` is the documented example
  (rubric 6/6, visual alignment 0.0). The two layers are intentionally complementary.
- **Known alignment-metric artifact.** When a reference PDF emits a whole table as one
  text block but the candidate emits per-row blocks (`tables_simple_easy`), no block
  pair clears the 0.3 Jaccard threshold and the sample scores `content mismatch`
  despite visually identical text. Left in the data, not hand-corrected.
- **Block-chunking bias.** Bounding-box IoU structurally penalizes candidates that emit
  fewer, larger text blocks (AI models especially). See the warning box in the visual
  report.
- **History.** Earlier drafts of the reports contained hand-maintained numbers that had
  drifted from the pipeline output, and an audit at one point removed three TypeTeX
  patched CV records in the mistaken belief their artifacts didn't exist (the audit
  checked `typetex_patched.pdf` instead of the on-disk `typetex_approx_patched.pdf`).
  Everything now published is regenerated end-to-end from the artifacts; the reports
  disclose each changed figure inline. `ai_models/legacy_reports/` retains the
  superseded snapshots for the record — do not cite them.

## Reports

- `reports/benchmark_findings.pdf` — scope, headline tables, 7 key findings, metric
  pass rates, rubric definitions.
- `reports/visual_alignment_report.pdf` — methodology, fair-subset and full-corpus
  alignment tables, curated visual examples, limitations.
- `reports/appendix.pdf` — the full 172-row scores table and all 48 comparison grids.

All three are built from their markdown sources by `scripts/build_reports.sh`; the
tables and grid labels are generated from `ai_models/absolute_scores.json`, so the
documents cannot silently disagree with the data.

## API-driven AI evaluation (in progress)

`scripts/22_run_gemini_api.py` replaces manual chat prompting with an automated,
reproducible protocol: visual-fidelity system prompt (the reference render is attached
to the request), at most one retry fed the exact compiler error, results and full
provenance under `ai_api/<model>/`.

The system prompt embeds two things that grow with every run:

- `scripts/prompt_pitfalls.md` — a living log of every conversion failure mode we've
  observed. When a new run fails in a new way, the lesson gets appended here.
- A **verified package allowlist** (test-compiled against the local Typst CLI, currently
  0.14.2): `cetz:0.3.2`, `cetz-plot:0.1.1`, `lovelace:0.3.0`, `algo:0.3.4`. Models
  hallucinate `@preview` package names and versions if left unconstrained — pinning a
  verified list eliminated an entire failure class. Re-verify the list when Typst or
  the packages update (compile a one-line `#import` per package).

First full run (2026-07-09, `gemini-2.5-flash`, v1 prompt): 9/48 compiled, but where it
compiled it beat every engine on the hard categories (e.g. `cv_complex_hard` IoU 0.536
vs. 0.089 for the best patched engine; `beamer_hard` preserved the title page that all
engines drop). The dominant failure class — LaTeX math syntax outside `$...$` — drove
the v2 prompt's Typst-vs-LaTeX cheat sheet. Free-tier quota is per-day/per-project/
per-model; the runner detects exhaustion and resumes cleanly the next day
(`--redo-failed` re-runs only failures).

## Roadmap

1. **Prompt iteration loop (now):** re-run failures with each improved prompt
   (`--redo-failed`), mine the new errors, extend the pitfalls file. Once compile rates
   stabilize, do one clean `--force` run so every sample sees the same prompt version,
   and only cite that run.
2. **Engine-assisted AI conversion (planned, decided):** the AI models will receive the
   best deterministic engine output as a draft alongside the LaTeX source and reference
   render, and refine it toward visual parity. Engines stop being competitors and
   become tooling — the measured quantity is the marginal value the model adds over the
   engine scaffold.
3. **The real benchmark (planned, decided):** the headline competition will be
   AI-vs-AI on genuinely hard, real-world LaTeX — full arXiv papers, complex beamer
   decks, posters — not synthetic snippets. The current 48-sample corpus becomes the
   calibration/regression suite; recent real documents double as
   contamination-resistant test data.
4. **Conversion tool:** an automated fixup layer over engine output (the findings are
   its spec: `@`-escaping, `\hrule`, beamer frames, CV templates), evaluated by the
   same IoU/SSIM pipeline; the as-tested → patched-ceiling gap (5.03 → 5.40) is the
   score it must close automatically.
5. **Paper:** written alongside; methodology sections derive from this README, the
   findings report, and the failure taxonomy.
