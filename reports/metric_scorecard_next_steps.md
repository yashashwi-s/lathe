# PDF fidelity metric study v0.3

Date: 2026-07-15

Status: development metric calibrated to one frozen blind LLM judge; no human
ratings and no held-out benchmark claim

## Decision

Use two related outputs, never one unlabeled percentage:

1. a deterministic fidelity profile with content, layout, typography,
   appearance, pagination, specialized structure diagnostics, and evidence
   coverage;
2. a development 0-4 ordinal grade derived from the conservative floor
   `min(content, layout, typography, pagination)` through monotonic
   calibration.

Keep strict exact-reproduction status separate from the grade. A candidate may
fail a 0.95 token gate and still receive grade 3 if the blind judge finds it
useful and visually close. Conversely, a candidate with strong text recovery
can receive grade 1 when pages collapse or tables overlap.

This replaces the old practice of treating `pdf_fidelity_v0.1`'s weighted
`overall` percentage as the benchmark target. Historical v0.1 values remain
available for reproducibility.

## Assumptions and interpretation boundary

- The reference PDF is the target rendering.
- The current calibration population is 23 compiled AI outputs on eight hard
  prompt-development references.
- One LLM judge is used because human ratings are unavailable. The review is
  blinded to model identity, protocol, and automated scores, but it is not a
  substitute for independent human validation.
- Source-known corruptions validate detector behavior and monotonicity. They do
  not define aesthetic preference or acceptable production thresholds.
- Protocol is part of the evaluated system. One-turn and agentic runs are never
  pooled under a model-family name.

## The v0.3 profile

| Axis | Implementation | Target failure | Boundary |
|---|---|---|---|
| Content | token multiset F1 plus character-sequence similarity; precision and recall exposed | omissions, additions, substitutions | PDF extraction and math encoding |
| Layout | matched-word geometry, local flow, reading order, page geometry | displacement, reflow, ordering | requires enough identical token matches |
| Typography | font size, family/class, bold, italic, color | font and emphasis drift | producer metadata differences |
| Appearance | tolerant ink F1 plus edge-distance score | global visual drift, obstruction, figures/rules | proxy, not an object metric |
| Pagination | exact page count plus rare-token-weighted ordered page alignment | inserted, missing, reordered pages | repeated pages can remain ambiguous |
| Tables | extracted table count, row/column exactness, cell-count ratio | topology damage | heuristic, not GriTS or TEDS(IoU) |
| Formula glyph proxy | math-font glyph multiset and sequence | source-known glyph erasure | producer-sensitive; diagnostic only |
| Evidence | reference/candidate matched-token coverage and applicability | survivor bias and false confidence | routes to review or abstention |

Compilation remains an external prerequisite.

### Strict status

- `fail`: a provisional exact-reproduction gate fails: token precision below
  0.95, token recall below 0.95, or page count differs.
- `review`: strict gates pass, but page sequence, typography, evidence coverage,
  appearance/layout disagreement, or table topology requires inspection.
- `pass`: no strict gate or validated review trigger fires.

Status is intentionally severe and is not a preference rank.

### Development grade

The grade input is:

```text
fidelity_core_floor = min(content, layout, typography, pagination)
```

A monotonic isotonic mapping converts the floor to the blind overall 0-4
rubric:

- 4: close reproduction;
- 3: useful reproduction with bounded visible differences;
- 2: partial reproduction with a major defect;
- 1: unusable fidelity due to severe structural or visual failure;
- 0: catastrophic or unassessable output.

The floor prevents a strong content axis from canceling a page collapse, or a
strong page count from canceling severe content loss. Appearance is reported
beside the grade but is not part of the floor until text/object decomposition
is stronger.

## Source-known augmentation study

The reproducible v0.3 study under
`results/metric_calibration/reference_perturbations_v0_3/` uses 11 real
reference PDFs and 186 comparisons. It applies:

- 1/4/12-point translation;
- increasing word deletion and addition;
- numeric replacement;
- increasing obstruction and crop;
- added, missing, and reordered pages;
- non-text erasure;
- table-row erasure where applicable;
- formula-glyph erasure where applicable.

All 55 ordered severity series are monotonic on their targeted axis. Every
registered detector check passes on every applicable example:

| Check | Result |
|---|---:|
| identity clone has no flags | 11/11 |
| 1-point translation has no hard failure | 11/11 |
| severe deletion fails recall | 11/11 |
| addition lowers precision | 11/11 |
| numeric replacement raises diagnostic | 11/11 |
| extra/missing/reordered page detected | 17/17 |
| severe obstruction raises a signal | 11/11 |
| applicable non-text erasure lowers proxy | 6/6 |
| table-row erasure changes topology | 1/1 |
| formula-glyph erasure lowers glyph recall | 7/7 |

The non-text denominator is six rather than seven because the forms sample has
insufficient non-text ink and correctly abstains.

## Blind judge protocol

The review book contains one reference-versus-candidate page for each of 24
stored outputs. Candidate IDs are anonymous. Model labels and automated metrics
remain hidden until the rubric CSV is frozen.

For each compiled candidate, the judge records 0-4 content, layout, typography,
structure, and overall scores; confidence; a strict within-reference rank; and
a concise defect note. One Sonnet one-turn output is unavailable because the
stored source does not compile. It remains in the denominator and is not
silently dropped.

Artifacts:

- blind book: `results/metric_calibration/canonical_ai_v0_3/manual_audit/blind_review_book.pdf`;
- frozen rubric: `manual_rubric.csv`;
- anonymous map: `blind_case_map.csv`;
- unblinded joined rows: `manual_judgments_unblinded.csv`;
- validation: `manual_validation.md` and `manual_validation.json`.

## Validation result

Spearman rank correlations on the 23 compiled cases:

| Manual target | Automated metric | n | rho |
|---|---|---:|---:|
| content | content | 23 | 0.754 |
| layout | layout | 23 | 0.817 |
| layout | pagination | 23 | 0.911 |
| typography | typography | 23 | 0.401 |
| overall | layout | 23 | 0.913 |
| overall | appearance | 23 | 0.891 |
| overall | conservative floor | 23 | 0.937 |
| content | formula glyph proxy | 18 | -0.045 |

Within-reference pairwise ranking accuracy is 86.4% for content, 90.9% for
layout, 90.9% for appearance, 100% for pagination, and 95.5% for the
conservative floor.

Leave-one-reference-out monotonic calibration of the conservative floor gives:

- mean absolute error 0.260 on the 0-4 scale;
- Spearman rho 0.860;
- 73.9% exact rounded grade;
- 100% within one grade.

Each canonical automated grade is therefore produced without training on any
candidate from the same reference. Selection among candidate composites remains
development research and should be frozen before held-out use.

## Signal policy after blind validation

The following remain logged but cannot change status or grade:

- exact numeric-token multiset mismatch: fires on 30/30 prompt-development
  outputs and mixes real errors with extraction artifacts;
- local worst-cell appearance: fires on 30/30 and ties on 15/22 blind ranking
  pairs;
- masked non-text proxy: detects controlled erasure but has weak blind structure
  correlation;
- formula glyph proxy: detects controlled erasure but has rho -0.045 against
  judged content on the applicable AI cases.

This is deliberate. A diagnostic is not promoted merely because it detects its
own synthetic corruption.

## Exact-protocol AI result

Descriptive means cover different sample sets:

| Exact protocol | Compiled n | Blind overall mean | Cross-validated grade mean |
|---|---:|---:|---:|
| Gemini 3.1 Flash Lite - one-turn cascade | 8 | 1.62 | 1.73 |
| Claude Opus 4.7 - agentic v3 visual medium | 6 | 3.67 | 3.41 |
| Claude Opus 4.7 - one-turn low | 2 | 2.50 | 2.50 |
| Claude Sonnet 4.6 - agentic v1 visual low | 6 | 2.83 | 2.81 |
| Claude Sonnet 4.6 - one-turn low | 1/2 | 2.00 | 2.00 |

The paired result is stronger than the unpaired means:

- Opus agentic v3 defeats Sonnet agentic v1 on 5 of 6 shared references;
- both agentic protocols defeat Gemini on all 6 shared references;
- one-turn comparisons contain only one or two shared compiled cases and do not
  support a general model claim.

## Literature decisions

- [OmniDocBench](https://arxiv.org/abs/2412.07626): adopted as the modular
  evaluation precedent.
- [GriTS](https://arxiv.org/abs/2203.12555) and
  [TEDS(IoU)](https://arxiv.org/abs/2208.00385): recommended next table metrics
  once reliable structure extraction exists.
- [CDM](https://arxiv.org/abs/2409.03643): motivates replacing the formula glyph
  proxy with visually equivalent expression comparison.
- [SSIM](https://doi.org/10.1109/TIP.2003.819861): tested in the historical
  raster family; the non-discriminating foreground term was removed.
- [LPIPS](https://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_The_Unreasonable_Effectiveness_CVPR_2018_paper.html)
  and [DISTS](https://arxiv.org/abs/2004.07728): reviewed, not adopted without
  typeset-domain calibration.
- [LLM judge position bias](https://arxiv.org/abs/2406.07791): motivates
  anonymization, fixed presentation, and freezing before unblinding.

## Next verifiable steps

1. Freeze v0.3 before any held-out benchmark run.
2. Expand blind calibration by document form and difficulty; add independent
   judges and measure agreement.
3. Implement non-text region detection with presence, bounding-box, and region
   appearance scores.
4. Replace the formula glyph proxy with normalized formula-region comparison or
   rendered math subimage comparison and retain abstention.
5. Add GriTS or TEDS(IoU) only after table structure extraction is reliable.
6. Run the frozen evaluator on held-out data and report exact protocols,
   compiled denominators, raw axes, evidence, status, and grade together.

## Reproduction

```bash
mamba run -n lathe python -m unittest tests/test_pdf_fidelity.py
mamba run -n lathe python scripts/evaluation/evaluate_reference_perturbations.py
mamba run -n lathe python scripts/evaluation/audit_prompt_dev_scorecard.py
mamba run -n lathe python scripts/evaluation/audit_canonical_ai_models.py
mamba run -n lathe python scripts/evaluation/analyze_manual_validation.py
mamba run -n lathe python scripts/ai/build_ai_metric_study_report.py
```

Final PDF:
`output/pdf/ai_model_fidelity_metric_study_v0_3.pdf`.
