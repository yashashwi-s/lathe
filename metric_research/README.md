# metric_research — does the v2 evidence vector help *inside* the harness?

The published PDF-fidelity **v2** evaluator (`scripts/evaluation/pdf_metric_axes_v2.py`)
deliberately emits **no single score** — it is a non-compensatory *evidence vector*
(hard facts, content, geometry, transport, raster, structures) where axes abstain
when their representation is absent, and a high score on one axis never cancels a
failure on another.

The agentic LaTeX→Typst harness, however, needs *something* to hill-climb on. This
folder asks: **does feeding the agent the v2 vector (gate-first) beat the old v0.1
blended scalar as mid-loop feedback?** Two phases, both grading every candidate with
the same `pdf_metric_axes_v2` at **96 DPI** (the report's frozen config; note the code
default is 120 DPI).

Deliverable: [`report/metric_harness_report.pdf`](report/metric_harness_report.pdf)
(slide deck with 3-way reference / v0.1 / v2 render comparisons, evidence-drawn
bounding boxes, and per-gate callouts).

## Phase A — is the vector informative? (no API spend)

Rescored 69 already-compiled candidates (hard lathe + dataset-expansion samples,
baseline + agentic). Findings in [`PHASE_A_RESULTS.md`](PHASE_A_RESULTS.md); flat
table in [`results/phase_a_v2_scores.csv`](results/phase_a_v2_scores.csv). Headline:

- The vector **decouples failures the v0.1 scalar fused** — a table that reflows onto
  the wrong page count reads as content≈perfect + pagination FAIL, not one low blob.
- `strict_f1` is **nearly orthogonal** to the old v0.1 overall (Pearson r = +0.20):
  content correctness and visual quality are near-independent, so one weighted number
  cannot represent both. Strong, mostly-independent drivers: `ink_f1_reg` (+0.87),
  `ltsim_macro` (+0.84), `center_q90` (−0.64).
- Confirmed caveats: `page_break_f1` is vacuously 1.0 on some page-count failures
  (use `page_count_delta`); `strict_f1` drops on math/pseudocode the PDF tokenizes
  oddly (not real content loss).

## Phase B — does it help in the loop? (A/B, ~$22)

Same model (opus), effort (medium), visual on, $2 cap, 6 hard samples (3 lathe +
3 dataset-expansion). The **only** difference between arms is the mid-loop feedback:

- **Arm A (v0.1):** one blended `overall = content^.35 · visual^.65` (compensatory).
- **Arm B (v2):** a HARD-GATE ladder (page-count delta, token P/R, number-F1) then
  independent drivers (`ink_f1`, `ltsim`, `center_q90`).

| avg over 6 samples | baseline (1-turn) | Arm A (v0.1) | Arm B (v2) |
|---|:--:|:--:|:--:|
| **gates passed / 4** | 1.2 | 2.0 | **3.2** |

Arm B ≥ Arm A on gates in **6/6** samples, strictly better in **5/6**, and closed
exact `number_f1` to **1.000** in 5/6 (Arm A stalled at 0.989–0.998). Arm A tends to
buy slightly more raster polish (drivers higher in 4/6, by ~0.02–0.08) while letting a
single wrong number or off-by-one page slip inside the average — the compensatory
failure the v2 report warned about. The verbose full paper (`arxiv5t_paper_019`) is
the shared ceiling (both 1/4). On `09_algorithms_003` gate-first feedback pushed Arm B
from 1/4 → 4/4, showing the strict token gate is *harder, not impossible*.

**Conclusion:** as feedback, the non-compensatory v2 vector redirects agent effort to
the human-objectionable exactness (correct numbers, page count) that a single scalar
hides — early but consistent evidence that the metric belongs in the loop as a gate
ladder, not a blended reward.

## Layout

```
metric_research/
  README.md                     this file
  PHASE_A_RESULTS.md            Phase A informativeness analysis
  results/phase_a_v2_scores.csv 69-candidate v2 rescore (flat)
  report/metric_harness_report.pdf
  scripts/
    feedback_v4.py    v2 score tool for the harness loop (gate ladder + drivers); repo-relative
    rescore_v2.py     Phase A: rescore stored candidate PDFs with v2
    run_phaseb.py     Phase B v2-feedback arm (wraps the claude CLI)
    run_ab_batch.sh   parallel A/B batch driver
    make_report.py    regenerate the deck
```

## Reproduce

Grading tool is in-repo; `feedback_v4.py` is self-contained:

```bash
# score any candidate as the v2 gate ladder + drivers (run from a work dir with
# main.tex, reference.pdf, output.typ):
mamba run -n lathe python metric_research/scripts/feedback_v4.py score
```

`rescore_v2.py`, `run_phaseb.py`, `run_ab_batch.sh`, `make_report.py` are the scratch
experiment drivers; they assume the external workspace layout described in the report
(sibling `harness_baseline/`, `dataset_expansion/`, per-run dirs) and are included for
provenance. Requires the `lathe` env plus `rapidfuzz` (a v2-evaluator dependency).

## Caveats

- Small n (6 samples, one seed per cell; `06_tables_moderate_010` agreed across 2 seeds:
  A 3/4, B 4/4). Mechanism evidence, **not** a model leaderboard. No human ratings exist.
- dataset-expansion references are tectonic/XeTeX, not pdfLaTeX — expect more canvas/SSIM
  abstentions (that is signal, not breakage).
- v2, its gates, and the driver reward were left **untouched**; this PR only adds the
  harness-side feedback experiment and its findings.
