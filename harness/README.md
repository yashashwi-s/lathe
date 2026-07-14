# harness/ — agentic LaTeX→Typst conversion baseline

Self-contained study (2026-07-14) of what an *iterative* agent adds over
one-shot LLM conversion, run on the 6 hardest `latex_benchmark_v0` samples.
Full deck: `output/pdf/harness_baseline_report.pdf`. Full score tables:
`results/RESULTS_snapshot_2026-07-14.md`.

## Headline result

On samples where every one-shot model (gemini flash-lite, opus-4.7,
sonnet-4.6) scores 31–38/100, a compile+score feedback loop with the same
models reaches **67–82 mean overall**, fixes every page-count mismatch, and
passes the frozen human-defensible gates on up to 3/6 samples. Total study
cost ≈ $70, ~$0.6–1.8 per document for the best configurations.

| upgrade (one factor at a time)        | Δ mean overall (core 6) | takeaway |
|---|---|---|
| 1-turn → agentic harness (blind, opus low) | **+25**  | the feedback loop is the big win; model scale alone adds ~0 at 1 turn |
| effort low → medium                    | ≈ 0–1    | buys reliability/speed, not peak score |
| blind → visual feedback                | +2–8     | helps most on layout-heavy samples; costs more turns |
| harness v1 → v2 (tools)                | +3       | checkpoint makes regressions free; runs that used `sweep` posted the best scores |
| harness v2 → v3 (fix mid-run reward)   | +3 and −$0.12/run | agent stops chasing a saturated metric; unlocked the two stuck samples (+12, +19) |

Other lessons:

- **Spend has diminishing returns:** best value at $0.5–1.0/doc; runs that
  grind to the $3 budget cap oscillate ±1 point around a plateau.
- **What agents fix vs not:** page counts, content recall, table sizing get
  fixed reliably (they're checkable); residual gap is fine layout drift and
  cross-engine rendering differences.
- **Metric lesson (raster_v0.2):** v0.1's raster component had a ~25–30
  ceiling for *all* real conversions — not font mismatch (candidates already
  embed New Computer Modern) but metric harshness (dead SSIM term, ±2 px ink
  tolerance below unavoidable engine drift). `raster_v2.py` re-scores stored
  renders with `0.70·inkF1(±4px) + 0.30·exp(−edge/10)`; identity still = 100,
  orderings preserved. Feeding the *corrected* number back mid-run (v3) is
  what unlocked the stuck samples — reward quality matters as much as tooling.

## Method

- `run_oneturn.py` — 1-turn baseline: single prompt (LaTeX source in, Typst
  out), no tools; compiled and scored with the official comparator.
- `run_task.py` — agentic run: isolated workdir per sample with `main.tex`,
  `reference.pdf`, `./score.sh` (typst compile + `scripts/evaluation/`
  comparator); wraps the `claude` CLI (`-p`, budget cap, `--effort`); the
  agent edits `output.typ` and re-scores freely. Full step transcript saved
  (`claude_transcript.jsonl`), cost/turns/iterations recorded in
  `summary.json`. Prompts are embedded in this file (PROMPT_TEMPLATE + mode
  extras). Conditions: `--visual` (reference PNGs + labeled diff images) vs
  `--no-visual` (numeric metrics only, image reads disallowed);
  `--harness v1|v2|v3`:
  - **v1** score.sh prints overall/component scores only.
  - **v2** adds best-so-far auto-checkpointing (final grade = best of last
    edit and checkpoint), `./sweep.sh` deterministic grid search over
    `typst --input` values, fine-grained per-component and per-page report,
    registered-raster diagnostic (`feedback_v2.py`).
  - **v3** = v2 but mid-run scores use the raster_v0.2 recombination — the
    same number as final grading.
- Frozen pass gates (chosen before any run): G1 compiles; G2 page count and
  pagination perfect; G3 token precision AND recall ≥ 0.95; G4 layout ≥ 75.
- `make_results.py` / `make_report.py` — regenerate the score tables and the
  slide deck from `runs/*/summary.json`.

## Reproduce

```bash
cd harness   # inside the lathe env; needs the claude CLI on PATH
python run_oneturn.py 05_tables_simple_023 --model opus --effort low   # ~$0.05
python run_task.py 05_tables_simple_023 --visual --harness v3 \
    --model opus --effort medium          # ~$0.7-1.8, ~3-5 min, cap $3
./run_queue.sh my_queue.txt               # sequential batch, one arg-line per run
python make_results.py                    # RESULTS.md + cost/score scatter
python make_report.py                     # slide-style PDF report
```

Paid runs launch the `claude` CLI — same approval etiquette as OpenRouter
runs (see `AGENTS.md`). Run artifacts land in `harness/runs/` (gitignored
PDFs; keep summaries/transcripts as needed).

## Layout

- `run_oneturn.py`, `run_task.py`, `run_queue.sh` — runners (prompts inside `run_task.py`)
- `feedback_v2.py` — v2/v3 score + sweep tooling given to the agent
- `raster_v2.py` — raster_v0.2 re-scoring of stored runs (+ `--check` suite)
- `make_results.py`, `make_report.py` — tables/plots/deck generators
- `results/` — frozen snapshot: score tables, one-shot baseline CSV,
  raster_v0.2 baseline rescoring, cost-vs-score scatter
- Development history (all runs, transcripts, queue logs) lives outside the
  repo in the workspace `harness_baseline/` folder.

## Next steps

Repeat runs to size run-to-run noise (single runs differ by a few points);
prompt v3.1 to always sweep before manual nudges and keep iterating while
under budget; human-calibrate metric weights; then RL hill-climbing against
the same deterministic reward.
