# Phase A — is the v2 evidence vector informative? (no API spend)

Rescored **69 already-compiled candidate PDFs** (representative hard-lathe + dsx
samples, baseline 1-turn + agentic methods) with `pdf_metric_axes_v2` at **96 DPI**
(report's frozen config; code default is 120). Script: `rescore_v2.py`. Per-run
vectors saved as `<run>/metric_v2.json`; flat table in `phase_a_v2_scores.csv`.

## Sanity anchors
- **Identity holds:** reference-vs-itself → strict_f1 = ink_f1 = ssim = 1.0, pagΔ = 0.
- **Structure axes abstain 69/69** (tables/formulas/figures) — expected: generic
  PDF words are not validated cell grids / formula tokens. Not zeros, abstentions.

## Headline: the vector separates failure modes the v0.1 scalar smeared together

The clearest win is **content-vs-pagination decoupling**. Under v0.1 a table that
reflowed onto the wrong number of pages got a single low `overall` (~32–36) that
looked like a *content* failure. v2 shows the truth:

| sample / method | v01 overall | strict_f1 | pagΔ | ltsim |
|---|---:|---:|---:|---:|
| 06_tables_moderate_010 · opus 1-turn | 35.4 | **0.992** | **+1** | 0.665 |
| 06_tables_moderate_010 · sonnet 1-turn | 35.8 | **0.986** | **+1** | 0.660 |
| 05_tables_simple_023 · opus 1-turn | 32.9 | 0.907 | **−1** | 0.671 |

Content is essentially perfect; the entire defect is **pagination** (pages off by
one). v0.1 hid that behind one number. v2 says "content PASS, pagination FAIL" —
exactly the non-compensatory behaviour the report promised, and exactly the
human-objectionable failure the harness README flagged as must-be-perfect.

## Which axes carry signal (Pearson r vs the old v0.1 overall, n=69)

| axis | r | reading |
|---|---:|---|
| `ink_f1_reg` (raster ink) | **+0.87** | tracks overall; the dominant visual driver |
| `ltsim_macro` (text transport) | **+0.84** | tracks overall closely |
| `center_q90` (word displacement) | **−0.64** | strong (negative = more displacement → worse) |
| `page_break_f1` | +0.54 | moderate but **noisy** (see caveat) |
| `kendall_tau` (reading order) | +0.53 | moderate |
| `ssim_reg` | +0.41 | weaker; eligible only when canvas matches |
| `number_f1` | +0.34 | mostly independent — catches numeric drops others miss |
| `typo_style_hmean` | +0.28 | largely independent |
| `strict_f1` | **+0.20** | **nearly orthogonal to overall** |

**Interpretation:** `strict_f1` at r=+0.20 is the key result — content correctness
and visual quality are almost independent signals, so collapsing them into one
weighted scalar (as v0.1 does) destroys information. The axes are complementary,
not redundant: `r(strict_f1, ink_f1_reg) = +0.08`. Raster-ink and text-LTSim *are*
partly redundant (r=+0.84) — a candidate for down-weighting one if we ever build a
composite.

## Caveats surfaced (the metric's own warnings, confirmed empirically)
- **`page_break_f1` is unreliable — use `page_count_delta`.** On `pubmed_table_004`
  1-turn the page count is wrong (pagΔ=−1) yet break-F1 = **1.0** (vacuous, exactly
  the report's warning). Meanwhile `06_tables` with pagΔ=+1 gives break-F1 = 0.0–0.15.
  → For gating, trust `page_count_delta` + `matched_block_page_assignment_accuracy`,
  not `page_break_f1`.
- **`i2s_equation_001` strict_f1 = 0.18** but overall looked fine (58.6): single-line
  equation, PDF tokenizes math differently — a content-axis artifact, not a real
  content loss. Confirms the report's "extraction tokenizes math differently" limit.

## Implication for the harness reward (answering your weighting question)
A defensible feedback signal for Phase B, mirroring prior harness weights but on v2
axes, and **gate-first** rather than blended:
1. **Hard gates** (must pass, human-objectionable if not): `page_count_delta == 0`,
   strict token precision & recall ≥ 0.95, `number_f1 == 1` where numbers present.
2. **Continuous drivers** to hill-climb once gated: `ink_f1_reg`, `ltsim_macro`,
   `center_q90` (the three highest-|r| independent visual axes).
3. **Report but don't optimize:** `ssim_reg` (abstains often), `page_break_f1`
   (noisy), structure axes (abstain).

This keeps the "pass all breakdowns, not one weighted number" design you asked for,
while still giving the agent something monotonic to climb.
