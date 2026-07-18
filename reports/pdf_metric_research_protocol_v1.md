# PDF fidelity metric research protocol v1

Status: pre-registered implementation and validation plan. This document is
written before the v1 augmentation results are inspected. It supersedes the
methodological claims in the rejected v0.3 report; the old files are retained
only as provenance until this protocol is verified end to end.

## Research question

Can a reference-based metric system compare a LaTeX reference PDF with an
AI-produced Typst PDF, identify the kind and location of visible errors, and
separate exact content fidelity from layout, reading order, typography,
pagination, and specialized structures?

The primary output is an **axis vector plus localized evidence**. There is no
universal v1 scalar. A score without its matched entities, missing/extra items,
page, and bounding box is invalid.

## Assumptions and limits

1. The 157 accepted PDFs in `data/latex_benchmark_v0` are the coverage unit.
   Every accepted reference is included in profiling, automated validation,
   and the visual extraction audit.
2. Controlled perturbations provide source-known defect type, severity, page,
   and region. They validate metric behavior; they are not synthetic AI
   conversions and cannot establish model quality by themselves.
3. The existing Gemini conversion corpus is an ecological transfer check after
   metric rules are frozen. Its 156 compiled outputs are not calibration data.
4. No human ratings are available. A blinded LLM/VLM-style visual audit is a
   secondary check, never ground truth. Known perturbation ordering is the
   primary validation signal.
5. Source-derived applicability is preferred to PDF-parser guesses. A parser
   failure produces `abstain_low_evidence`, not a false perfect or zero score.
6. Page canvas differences are reported separately. Most current AI outputs
   use A4 while most references use US Letter; this must not be silently folded
   into layout quality.
7. License/provenance completeness is audited separately from metric quality.
   Missing redistribution evidence blocks a public dataset release claim.

## Corpus audit frozen before scoring

The accepted corpus contains 157 documents and 239 reference pages:

| Document form | Documents |
|---|---:|
| Prose and sections | 13 |
| Lists and formatting | 15 |
| Inline/display mathematics | 18 |
| Aligned mathematics | 15 |
| Simple tables | 18 |
| Moderate tables | 18 |
| Figures and captions | 15 |
| Cross-references and citations | 15 |
| Algorithms | 12 |
| Compact papers | 8 |
| Forms, CVs, and letters | 10 |
| **Total** | **157** |

Page-count distribution: 102 one-page, 28 two-page, and 27 three-page
documents. Source-backed semantic signals currently indicate 110 documents
with inline or display mathematics, 36 table documents, 15 figure documents,
15 list documents, 41 cross-reference/citation documents, and 12 algorithm
documents. These flags will be emitted per sample and manually checked.

## Evidence from prior work

The metric system adopts published ideas at their validated level and labels
adaptations honestly:

- Exact text inventory precision/recall/F1 and block normalized edit similarity
  are core content measures. Spatial grounding is an adaptation of
  [CLEval](https://openaccess.thecvf.com/content_CVPRW_2020/html/w34/Baek_CLEval_Character-Level_Evaluation_for_Text_Detection_and_Recognition_Tasks_CVPRW_2020_paper.html)
  using actual digital-PDF characters or words when extraction is reliable.
- Layout matching trials a strict-label variant inspired by
  [LTSim](https://arxiv.org/abs/2407.12356). It will not be called LTSim unless
  the published optimal-transport definition is implemented exactly.
- Pairwise token relations are a trial diagnostic inspired by PaIRS in
  [SAVIOR](https://openaccess.thecvf.com/content/WACV2026W/VisionDocs/html/Bhat_SAVIOR_Sample-efficient_Adaptation_of_Vision-Language_Models_for_OCR_Representation_WACVW_2026_paper.html).
  The paper is a WACV 2026 workshop publication and its transfer from OCR
  representation to clean PDF fidelity must be demonstrated here.
- Reading order reports matched-block coverage and Kendall tau, following
  [Lapata (2006)](https://aclanthology.org/J06-4002/) and informed by later
  work showing that document order can be relational rather than one total
  sequence ([Zhang et al., 2024](https://aclanthology.org/2024.emnlp-main.540/)).
- Tables require separate topology, content, and location evidence. The target
  definitions are [GriTS](https://arxiv.org/abs/2203.12555) and, when a common
  table tree is available, [TEDS](https://arxiv.org/abs/1911.10683). Row or
  column counts are not substitutes.
- Formula scoring remains a trial until both LaTeX and Typst can be mapped to a
  validated common representation. [CDM](https://arxiv.org/abs/2409.03643)
  provides the target concept. The 2026 Image Matching Score
  [IMS](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_From_Pixel_to_Precision_Enhancing_Handwritten_Mathematical_Expression_Recognition_with_CVPR_2026_paper.html)
  is relevant but was validated on isolated handwritten expressions, so a
  full-page projection proxy cannot become a formula grade here.
- SSIM is a localized raster diagnostic, not a quality grade, because blank
  background and subpixel rendering dominate page averages
  ([Wang et al., 2004](https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf)).
- Robustness corruptions and three-level severity design follow the precedent
  of [RoDLA](https://openaccess.thecvf.com/content/CVPR2024/html/Chen_RoDLA_Benchmarking_the_Robustness_of_Document_Layout_Analysis_Models_CVPR_2024_paper.html).
- The render-diagnose-repair-verify loop and typed defect records are consistent
  with [PaperFit](https://arxiv.org/abs/2605.10341), a May 2026 preprint. Its VLM
  quality score is not imported as ground truth.
- LLM/VLM judges are order-sensitive. Any audit comparison is counterbalanced,
  repeated, evidence-citing, and allowed to abstain
  ([Shi et al., 2024](https://arxiv.org/abs/2406.07791)).

The detailed adopted/trial/rejected evidence matrix is in
`reports/pdf_metric_literature_v1.md`.

## Frozen v1 output contract

### Eligibility and evidence state

Every pair begins with compile status, page counts and dimensions, extractor
coverage, source applicability, and one of `scored`, `not_applicable`, or
`abstain_low_evidence` for each module.

### Core axes

| Axis | Required observables | Interpretation |
|---|---|---|
| Content | Token inventory P/R/F1; ordered normalized edit similarity; missing/extra tokens, digits, operators, units, and citations | Exact material preserved, independent of page position |
| Text grounding | Matched character/word coverage; misses, false positives, splits/merges when supported | Extracted text is connected to the correct rendered region |
| Geometry | Matched-entity center displacement q50/q90, width/height log error, IoU, baseline residual | Where preserved entities moved or resized |
| Layout relations | Block presence, matched IoU, strict-label matching trial, pairwise horizontal/vertical relation agreement | Two-dimensional organization without hiding canvas mismatch |
| Reading order | Matched-block coverage, Kendall tau, relational inversions | Flow among content-bearing blocks |
| Pagination | Page delta, matched-block page assignment, page-boundary precision/recall/F1 | Flow across pages, not merely number of pages |
| Typography | Matched span size, line-height, baseline, weight/style, hierarchy observables | Typesetting appearance without requiring PDF font names to match |
| Tables | GriTS topology/content/location and TEDS only when reliable common structures exist | Table structure, text, and placement separately |
| Formula | Applicability and localized formula-region diagnostics; CDM/IMS-derived trials only after independent validation | No formula grade from font codes or regex counts |
| Figures/objects | Presence P/R/F1, geometry IoU, matched-crop edge/SSIM diagnostics | Object existence, placement, and appearance separately |
| Raster residual | Registered content-region structural similarity, tolerant ink overlap, top residual boxes | Debugging evidence; never the main grade |
| Canvas | Page size/aspect mismatch | A confound and explicit failure mode, not hidden inside layout |

All normalized axis scores use the direction `1 = closer fidelity`, `0 = worse`
only when a justified transform exists. Raw residuals are retained. Trial axes
cannot gate a model ranking.

### Implementation boundary for this run

The literature table is a design target, not a claim that every published
method was executed. The all-157 augmentation run validates only five harness
projections: extracted-token inventory F1; q10 IoU over exact-token matches; a
mixed typography weakest-link diagnostic; unregistered tolerant ink F1; and a
page-count/page-break diagnostic. The raw evaluator also emits additional
atomic evidence, but the following remain `not_implemented` or `trial` rather
than validated: CLEval split/merge scoring, LTSim, PaIRS, semantic reading-order
ground truth, GriTS, TEDS, CDM, SSIM/MS-SSIM, figure matching, hierarchy and
line-height fidelity, and a complete entity explanation manifest.

In particular, the current layout projection omits match coverage, typography
mixes content coverage with font/baseline residuals, and pagination depends on
a matched subset. These projections can be studied for controlled response but
cannot become AI-quality grades in v1. Specialized table, formula, and figure
modules abstain.

### Explanation record

Each scored document must retain:

- reference/candidate page and entity match records;
- unmatched reference and candidate entities;
- normalized page coordinates, source text, match method, and confidence;
- per-axis atomic contributions;
- top defects with page, bounding box, reason, and affected axis;
- overlay/heatmap paths generated from the same evidence;
- renderer, extractor, metric version, configuration, and seed.

## Controlled augmentation matrix

All mutation is deterministic by `(sample_id, family, severity, seed)`. Every
planned row is written even when not applicable or failed. Non-applicable rows
are not counted as successful tests.

### Universal probes

| Family | Levels | Target / invariant |
|---|---:|---|
| Identity and lossless rewrite | baseline plus deterministic rewrite | All semantic and structural axes invariant |
| Global translation | four directions x three severities | Geometry/layout; content invariant |
| Global scale | shrink/grow x three severities | Geometry/typography; content invariant |
| Local block displacement | four directions x three severities | Local geometry/layout and localization |
| Text deletion | three severities | Content recall and local evidence |
| Lexical and numeric corruption | two types x three severities | Content; geometry outside target invariant |
| Font size and line spacing | four variants x three severities | Typography and reflow; content invariant |
| Crop and occlusion | targeted sides/regions x three severities | Local content/geometry/raster evidence |
| Blur, downsample, JPEG | three types x three severities | Appearance diagnostics; semantic axes invariant when extraction survives |
| Compounds | six fixed combinations | Must be no better than either component on the targeted axis |

### Category-aware probes

- multipage: move a block across a boundary, add/remove a break, compress flow;
- math: replace digit/operator/variable, remove script or aligned line, alter
  delimiter, and local occlusion around a source-backed math region;
- tables: row/column deletion or swap, cell-text corruption, rule removal,
  split/merge and localized table movement when extraction supports it;
- figures: delete, translate, resize, crop, substitute, caption detach/swap;
- lists: marker removal, indentation change, item reorder;
- cross-references: label/number/citation corruption and target movement;
- algorithms: line removal/reorder, indentation and rule changes;
- forms: field/value deletion, label/value displacement, alignment change;
- prose: paragraph/heading reorder, column-width and spacing changes;
- compact papers: float/page-break/column-gap stress tests.

The frozen planning profile contains 16,167 possible controlled pairs. This
corrects the prior 16,176 hand estimate: comment-stripped parsing found 41
genuine cross-reference-bearing documents, not 42. A planned pair is not a
successful evaluation; applied, non-applicable, and failed counts remain
separate in the run manifest.

The operation names are engineering shorthand and do not establish ecological
realism. In the current generator, edge “crop” erases content while preserving
the MediaBox; most local/category “occlusions” add black ink; figure
“substitution” is a black rectangle; and typography variants redraw text with
an approximate Helvetica baseline. Translation or growth can clip, and PDF
heuristics—not semantic annotations—select many math, table, figure, form, and
algorithm regions. Manual mutation-validity checks therefore gate example use,
and these probes validate sensitivity to the implemented edits only. They are
not synthetic Typst training data or faithful samples of the AI-error
distribution.

## Split and leakage controls

1. Assign each source document once to `metric_dev`, `metric_validation`, or
   `metric_test`, stratified by category, page count, and source family with a
   fixed seed. This split is separate from prompt development.
2. Every derivative of a reference remains in the reference's source cluster.
3. Use metric development only to debug transforms and extraction thresholds.
4. Freeze code, thresholds, expected responses, and the audit sample before
   inspecting metric test outcomes.
5. Report document-macro and category-macro results. Use a stratified
   source-cluster bootstrap; never resample perturbation rows as independent
   observations.
6. The 156 real Gemini outputs are evaluated only after the augmentation
   validation is frozen. Prompt-development samples remain excluded from final
   model-quality claims even though their references participate in evaluator
   robustness work.

## Validation harness

For every family and axis, compute:

1. identity optimum;
2. adjacent severity-order accuracy and Kendall tau-b;
3. targeted-axis drop versus off-target leakage;
4. expected-region localization hit and IoU;
5. insertion/deletion directionality where applicable;
6. symmetry for metrics declared symmetric;
7. invariant false-positive rate;
8. deterministic repeat agreement;
9. honest abstention and non-applicability behavior;
10. compound dominance and tail-defect visibility.

`Target selectivity margin` is descriptive only in this run. A causal
selectivity gate requires a preregistered affected-axis and invariant-axis set
for every variant; treating every unnamed axis as invariant is invalid because
many edits have physical collateral effects. Likewise, localization refers
only to overlap between a known edit region and the registered raster-residual
enclosure. It is not semantic or axis-specific explanation accuracy.

Project acceptance criteria are deliberately demanding but are not literature
standards:

- at least 95% correct adjacent severity ordering overall;
- lower 95% source-cluster bootstrap bound for targeted Kendall tau-b above
  0.70;
- semantic/structural invariant false-positive rate below 1%;
- expected-region localization hit rate at least 90%;
- deterministic rerun agreement 100%;
- no document form with an unexplained sign reversal or collapsed coverage;
- every unsupported specialized module abstains rather than fabricating a
  score.

A failure does not get averaged away. It triggers a metric revision, a narrowed
claim, or removal of the axis from v1 grading, followed by a complete rerun.
Ordering includes the severity-zero baseline; ties count as failures rather
than successes. Lossless controls are compared with the analytic projection
optimum of 1.0 rather than being used as their own baseline. Family-, variant-,
and category-level failures are listed explicitly even when the overall mean
passes.

### Controlled-defect-equivalent bands

Raw axis values remain the primary result. For readability, a secondary label
may map an axis to `reference_like`, `mild`, `moderate`, or `severe`, but those
words mean similarity to the controlled perturbation levels—not human quality
or acceptability.

For each source and axis, average applicable variants at each known severity.
On `metric_dev` only, take the document median at severities 0–3 and place the
three thresholds halfway between adjacent medians. Non-monotone, collapsed, or
missing development anchors make the axis `trial` or `abstain` immediately.
Only variants available at all three severities are included, and each variant
receives equal weight within a document so compounds and one-level pagination
probes cannot distort the anchors. Thresholds are then frozen. An internal
synthetic profile passes only if both `metric_validation` and the one-time
`metric_test` confirmation reach at least 50% exact four-band accuracy, at
least 90% within-one-band accuracy, and at most 0.50 mean absolute band error.
Even a passing profile is not applied as an AI-output quality label: the
perturbation families have no common human or task-utility scale. AI outputs
retain raw axis observables and explicit abstention instead.

## Blinded visual audit

Every one of the 157 references contributes four controlled variants: content,
geometry/layout, appearance, and one category-aware probe. Phase A shuffles
cases across sources, balances the candidate between panels A and B, hides
mutation/metric/box identity, and writes judgments to a truth-free response
manifest. Phase B groups the same cases by source and reveals the answer key,
the known edit region, and the raster-residual enclosure for explanation QA.
The audit records:

- extraction correctness for the clean reference;
- visible defect type and severity order;
- page and bounding box of the first material defect;
- whether the automatic explanation overlaps that region;
- confidence and an explicit abstention option.

Scores and mutation identities are revealed only after judgments are frozen.
The audit is a model-assisted research check in the absence of human ratings;
the report will state this limitation plainly.

## Staged execution and stopping rule

1. Generate the exact dry-run matrix and inspect applicability counts.
2. Run a category-stratified pilot and repair only demonstrated evaluator or
   mutation failures.
3. Re-run the pilot until it satisfies contracts or the failing metric is
   removed/narrowed.
4. Freeze v1 and run all 157 source clusters.
5. Build and inspect all 157 blinded audit pages; record judgments before
   revealing automatic scores.
6. Run validation statistics and sensitivity checks.
7. Evaluate the existing 156 compiled AI outputs without retuning.
8. Produce the final report from frozen artifacts.

The final document will distinguish verified findings, trial diagnostics,
failed ideas, and next steps. It will not present planned work as completed
research.
