# PDF fidelity evaluator v2: implementable research note

Status: methodology decision record, not a benchmark result. This note separates
published metrics that can be reproduced from the evidence currently extracted by
`pdf_metric_axes_v1.py` from useful adaptations and unsupported claims.

## Decision in one page

The next evaluator should be a **non-compensatory scorecard with atomic evidence**,
not a single page-similarity number. The current research prototype supports:

1. exact NFC whitespace-token inventory and edit evidence, with a separate NFKC
   compatibility view and a partial critical-symbol inventory;
2. inputs suitable for a future official CLEval conformance test, but no released
   CLEval score yet;
3. raw, content-matched word/block geometry and conditional reading-order tau;
4. text-only LTSim as a trial, explicitly not full semantic-layout LTSim;
5. exact page count and dimensions, with page assignment/boundary outputs retained
   only as conditional diagnostics;
6. typography residuals from matched text spans; and
7. fail-closed same-canvas SSIM plus a legacy resized-canvas tolerant-ink diagnostic
   whose residual enclosure is translation-registered. Neither is a semantic grade.

The current extractor does **not** provide semantic layout labels, table cell grids,
or normalized HTML trees. Full semantic LTSim, GriTS, and TEDS must therefore
abstain. Inferring their required structures and then reporting the published metric
name as if the inference were ground truth would confound model error with evaluator
error.

No universal scalar should be released. Individual components should not become
benchmark grades until they pass controlled
identity, monotonicity, selectivity, localization, directionality, invariance,
symmetry, and determinism tests on held-out documents. In the absence of human
ratings, controlled perturbation truth and blinded forensic review validate
mechanical behavior; they do not establish perceptual validity.

## What the repository actually exposes

`pdf_metric_axes_v1.py` extracts, through PyMuPDF:

- page width, height, and sorted page text;
- character boxes and font metadata;
- word boxes, text, block/line/word indices, and font metadata; and
- native text blocks made by grouping PyMuPDF words.

It does not extract or validate figures, drawings, table regions/cells, formula
regions/tokens, semantic block classes, or an authoritative reading order. The
current `_text_grounding_axis` is correctly labeled an exact-word adaptation; it is
not CLEval. The current block matcher is a one-to-one Hungarian assignment with a
text-similarity threshold, not optimal transport and not LTSim. The current raster
path resizes and optionally translation-registers candidate pages; those results are
useful diagnostics but must not become the fidelity grade because resizing erases
canvas differences and registration can erase real layout shifts.

## Metric-by-metric specification

### 1. Exact content: implement now

Use two frozen text views and never silently discard a mismatch:

- **strict view:** Unicode NFC, normalized line endings, and collapsed whitespace;
- **compatibility view:** Unicode NFKC plus the same whitespace rule, used to flag
  encoding/ligature equivalences rather than to conceal them.

For token multiplicities `r(t)` and `c(t)`, let

`M = sum_t min(r(t), c(t))`, `P = M / sum_t c(t)`,
`R = M / sum_t r(t)`, and `F1 = 2PR/(P+R)`.

Publish precision and recall separately, plus every strict missing and added token.
This strict whitespace-token inventory is document-level and does not itself carry
boxes. A separate NFKC PDF-word matcher supplies page/box evidence and must not be
conflated with the strict multiset. Also report character normalized edit similarity

`NES(a,b) = 1 - Lev(a,b) / max(|a|, |b|, 1)`.

This is a benchmark-defined exactness module, not a claim of semantic equivalence.
The implemented **partial critical inventory** covers regex numbers, a fixed set of
operator characters, and restricted citation-like markers. Units and general
punctuation are not yet implemented. For every implemented class, emit exact NFKC
multiset P/R/F1 and concrete missing/added values. A single wrong digit must remain
visible even when document-level F1 rounds to 1.000. Embedding or paraphrase metrics
are inappropriate because the task requires preservation rather than semantic
similarity.

### 2. CLEval: feedable, but release is pending conformance

CLEval was designed to handle split/merge text detections and partial recognition.
For a reference word box with `l` characters, it places pseudo-character centers
along the line between the left- and right-edge midpoints:

`p_k = ((2k-1)/(2l)) p_left + (1-(2k-1)/(2l)) p_right`.

A candidate box is a match when it contains at least one reference pseudo-character
center and its area precision exceeds 0.5. For end-to-end evaluation, matched
candidate transcriptions are serialized spatially; a longest-common-subsequence
elimination procedure assigns each recognized character once. Recall and precision
use

`Score = (CorrectNum - GranulPenalty) / TotalNum`,

with ground-truth split penalty `G_i-1` and detection merge penalty `D_j-1`.
Dataset recall/precision sum numerators and denominators before division. Report the
H-mean together with split, merge, miss, overlap, and false-positive counts. These
definitions are from the [CLEval paper](https://openaccess.thecvf.com/content_CVPRW_2020/papers/w34/Baek_CLEval_Character-Level_Evaluation_for_Text_Detection_and_Recognition_Tasks_CVPRW_2020_paper.pdf),
and the [official implementation](https://github.com/clovaai/CLEval) should be used
as the conformance oracle.

The repository can feed reference and candidate word rectangles and transcriptions
into the published CLEval interface. That is not sufficient to claim a faithful
implementation. A released score must first agree with the official implementation
on split, merge, crop, insertion, deletion, overlap, and recognition property tests.
Until then, CLEval is **pending**, not scored. The repository may additionally trial a
**CLEval-PDF-char** adaptation that substitutes reliable reference character centers
for pseudo-centers. That adaptation is attractive for proportional fonts but must be
named separately and compared against official CLEval. It must abstain when
character-to-word extraction consistency is below a frozen coverage threshold,
because ligatures, missing ToUnicode maps, and math-font encodings can corrupt PDF
character evidence.

### 3. Word and block geometry: implement as atomic residuals

After exact-token occurrence matching, normalize each box by its own page width and
height and report, without an arbitrary score transform:

- reference and candidate match coverage;
- center displacement q50, q90, and maximum;
- box IoU q10/q50;
- `|log(w_C/w_R)|` and `|log(h_C/h_R)|` q90;
- baseline displacement and page-assignment mismatches; and
- the complete match manifest and worst localized pairs.

Repeated tokens make the assignment ambiguous. Candidate edges should be constrained
by page and local block/order context, and each match needs a cost, runner-up cost,
and ambiguity margin. Scores derived from low-margin assignments must abstain or be
reported as low-confidence. Canvas size mismatch remains a separate finding; page
normalization must not make Letter and A4 look equivalent.

### 4. LTSim: exact formula, limited applicability

Published LTSim represents a layout as elements `e_i=(b_i,c_i)`, where `b_i` is a
normalized box and `c_i` a semantic category. For layouts of `m` and `n` elements,
optimal transport solves

`gamma* = argmin_gamma sum_ij gamma_ij mu(e_i,e'_j)`

subject to nonnegative `gamma`, row mass `1/m`, and column mass `1/n`. Its costs are

`delta_bbox = (1 + GIoU(b_i,b'_j))/2`,

`delta_label = 1[c_i=c'_j]`,

`mu = 1 - (delta_bbox + delta_label)/2`,

`EMD = sum_ij gamma*_ij mu_ij`, and `LTSim = exp(-EMD/sigma)` with `sigma=1`
for layout-level comparison. This is the exact definition in the
[LTSim paper, equations 4--10](https://arxiv.org/pdf/2407.12356).

The current data support only **Text-LTSim**: use text blocks on one page and assign
every element the label `text`. The optimal-transport equations are then faithful on
that subset, but the result is not full semantic layout fidelity. Compute it per
paired page; show page macro, element-weighted, and worst-page values separately.
Missing-page behavior and empty-layout behavior require an explicit benchmark rule
because the published transport problem assumes non-empty element sets.

Important limitations:

- with every label equal, Text-LTSim measures geometry and segmentation only;
- uniform mass gives every extracted block equal importance;
- producer-dependent block splitting changes the mass distribution; and
- published LTSim grants positional credit even across wrong labels. A strict-label
  cost of one for cross-label transport can be trialed once reliable labels exist,
  but it is a benchmark adaptation, not published LTSim.

Full semantic LTSim must abstain until both PDFs have validated boxes and labels for
at least text/title/list/table/figure/formula/caption/algorithm. Learned detections
must expose detector version, confidence, and classwise validation; detector failure
cannot silently become candidate failure. The LTSim authors themselves validate
metric behavior primarily through controlled perturbation properties and note that
subjective layout-similarity validation can be unreliable, rather than treating the
metric as perceptual truth.

### 5. Reading order: conditional implementation

For the same `N` content-matched block IDs in reference order `pi` and candidate
order `sigma`, let `S(pi,sigma)` be the minimum adjacent swaps (the inversion count).
Then

`tau = 1 - 2 S(pi,sigma) / [N(N-1)/2]`.

This ranges from -1 to 1 and is the definition validated against ordering judgments
and reading time by [Lapata (2006)](https://aclanthology.org/J06-4002.pdf). Publish
`N`, both-side block coverage, the inversion count, and concrete inversion examples.
Use tau-b when the chosen order representation contains ties.

PyMuPDF `sort=True` supplies a geometric top-left ordering, not authoritative reading
order. Therefore the module is scored only when block matching is high-confidence
and the document form has a validated total-order policy. It should abstain on
ambiguous multi-column, floating-object, or side-by-side layouts unless source-backed
order annotations exist. Tau on a small matched subset can look perfect while most
content is missing, so coverage is never optional.

### 6. GriTS and TEDS: formulas retained, scores must abstain today

GriTS compares table **grid-cell matrices**, not generic text blocks. It selects
monotone row and column subsequences maximizing cell similarity. If the aligned-cell
similarity mass is `M_f`, then

`GriTS_f = 2 M_f / (|A|+|B|)`,

`Recall_f = M_f/|A|`, and `Precision_f = M_f/|B|`.

`GriTS_Top` uses IoU of span boxes in grid coordinates, `GriTS_Con` uses normalized
LCS of cell strings, and `GriTS_Loc` uses page-coordinate cell-box IoU. The exact
2D most-similar-substructure problem is NP-hard; the published factored dynamic
program gives lower and upper bounds, and the lower bound is reported as GriTS.
See the [GriTS paper](https://arxiv.org/pdf/2203.12555) and
[official Table Transformer implementation](https://github.com/microsoft/table-transformer).

TEDS requires normalized HTML trees containing `thead`, `tbody`, `tr`, and `td`
nodes with row span, column span, and content. Insertion/deletion cost one;
the paper assigns node-substitution cost one whenever either node is not `td`.
For two `td` nodes, substitution costs one when spans differ; otherwise it is the
normalized Levenshtein cost on cell text. The score is

`TEDS(T_A,T_B) = 1 - EditDist(T_A,T_B)/max(|T_A|,|T_B|)`.

See the [PubTabNet/TEDS paper](https://arxiv.org/pdf/1911.10683) and
[official code](https://github.com/ibm-aur-nlp/PubTabNet).

Neither metric can be computed from the current words/blocks. GriTS requires a
validated table region, row/column grid, cell spans, cell boxes, and cell text on
both sides; TEDS requires a deterministic common HTML normalization. A detector or
heuristic parser may be evaluated as a future extractor, but until its cell-level
error is manually/source-validated, emit `abstain_low_evidence`, not zero, one, row
count agreement, or a metric bearing the GriTS/TEDS name.

### 7. SSIM and MS-SSIM: localized diagnostic only

For aligned local grayscale patches, the standard simplified SSIM is

`SSIM(x,y) = ((2 mu_x mu_y + C1)(2 sigma_xy + C2)) /
             ((mu_x^2 + mu_y^2 + C1)(sigma_x^2 + sigma_y^2 + C2))`,

with `C1=(K1 L)^2`, `C2=(K2 L)^2`, conventionally `K1=0.01`, `K2=0.03`.
The original implementation uses an 11x11 Gaussian window with sigma 1.5 and
uniformly averages the local map for MSSIM. See the
[SSIM primary paper](https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf).

MS-SSIM repeatedly low-pass filters and downsamples by two. It uses luminance at
the coarsest scale and contrast/structure at every scale:

`MS-SSIM = l_M^alpha_M product_j c_j^beta_j s_j^gamma_j`.

The published five-scale weights are
`[0.0448, 0.2856, 0.3001, 0.2363, 0.1333]`, calibrated with eight observers on
small natural-image distortions, not typeset pages. See the
[MS-SSIM primary paper](https://ece.uwaterloo.ca/~z70wang/publications/msssim.pdf).

Target implementation contract for a benchmark release:

- freeze renderer, version, grayscale conversion, physical DPI, antialiasing, and
  dynamic range;
- do not resize a candidate to the reference canvas for a grading value;
- use unregistered pages for fidelity evidence; a translation-registered result may
  be shown only as a renderer-noise diagnostic;
- when physical page canvases differ, report the canvas failure and abstain from
  ordinary same-grid SSIM, or use a clearly named common-physical-canvas adaptation;
- retain the full local map and report active-ink-window q10/median plus worst boxes;
  a white-background page mean is insufficient; and
- report non-finite values rather than silently clamping a component.

The present v2 prototype satisfies the fail-closed canvas/grid rule only for SSIM
and its explicitly named multiscale adaptation. Its tolerant-ink F1 still resizes the
candidate canvas to the reference raster, and its residual enclosure is computed
after translation registration. Those two outputs are therefore legacy diagnostics,
not unregistered fidelity evidence. This limitation explains why tolerant-ink values
exist for all 156 frozen Gemini comparisons while same-canvas SSIM is eligible for
only 2/156.

SSIM measures local raster statistics, not text correctness, reading order, or table
structure. The original paper says cross-image and cross-distortion testing is
critical. A later primary analysis shows unexpected/nonintuitive cases and warns
against treating SSIM as reliable perceptual truth; see
[Nilsson and Akenine-Moller (2020)](https://arxiv.org/pdf/2006.13846). Thus SSIM,
MS-SSIM, tolerant ink F1, edge residuals, and heatmaps are complementary diagnostics,
never the final grade.

## Applicability matrix for v2

| Component | Required evidence | Current status | Permitted report label |
|---|---|---|---|
| Exact token/character content | extracted words/text | available | scored |
| Critical numbers/operators/citations | extracted text plus frozen tokenizer | partially available | scored for implemented classes only |
| Published CLEval | word boxes and transcriptions | feedable; unconformed | pending |
| CLEval-PDF-char | reliable char boxes | conditional | trial / abstain-low-coverage |
| Word geometry | high-confidence exact-token matches | conditional | scored with coverage/confidence |
| Text-LTSim | native text blocks | conditional | trial; explicitly text-only |
| Full semantic LTSim | validated semantic boxes/labels | unavailable | abstain |
| Reading-order tau | common matched blocks + validated total order | gate not yet complete | conditional diagnostic |
| GriTS | table grid cells/spans/boxes/text | unavailable | abstain |
| TEDS | common normalized HTML trees | unavailable | abstain |
| Typography residuals | matched styled words/spans | conditional | raw diagnostic |
| SSIM/multiscale adaptation | aligned fixed-protocol rasters | available conditionally | raster diagnostic only |
| Tolerant-ink F1/residual box | resized and translation-registered rasters | legacy diagnostic | never physical-fidelity evidence |
| Pagination boundaries | reliable matched blocks + document-form gate | gate not yet complete | conditional diagnostic |

## Validation contract before any metric becomes a grade

The validation design should follow the property-based precedents in CLEval, GriTS,
TEDS, LTSim, and SSIM rather than selecting a metric because it looks plausible on a
few model outputs. CLEval tests crop, split, overlap, insertion, deletion, and
replacement severities. GriTS tests missing rows/columns and explicitly requires task
isolation, cell isolation, two-dimensional order preservation, row/column
equivalence, and cell-position invariance. TEDS compares its response under
increasing structural and cell-content perturbations. LTSim tests metric responses
to controlled layout changes. SSIM calls for cross-image and cross-distortion tests.

For every document and applicable perturbation family, record:

1. **Identity:** exact PDF self-comparison reaches the mathematical optimum and
   yields an empty defect manifest.
2. **Monotonicity:** increasing known severity worsens the target observable; report
   Kendall tau-b, adjacent-severity violation count, and every violating case.
3. **Selectivity:** publish the complete perturbation-by-axis response matrix; target
   effect must be distinguished from off-target leakage.
4. **Directionality:** insertion reduces precision more than recall; deletion does
   the reverse. Added/missing critical tokens must be named.
5. **Localization:** the highest-ranked defect overlaps the known mutation region;
   report hit rate, IoU, and region coverage, not only a binary pass.
6. **Symmetry:** symmetric quantities agree under input reversal; asymmetric P/R
   swap as expected.
7. **Invariance:** metadata/object order, lossless compression, font subsetting, and
   other render-preserving controls leave semantic/geometry metrics unchanged.
8. **Determinism:** independent repetitions produce byte-identical metric JSON or an
   explicitly bounded numeric tolerance with version/seed provenance.
9. **Evidence behavior:** missing extraction evidence produces abstention, never a
   silent best/worst score.
10. **Tail behavior:** local digit, rule, clipping, or overlap defects remain visible
    in the entity ledger and low-quantile/worst-region summaries.

Thresholds such as “95% adjacent ordering” are benchmark engineering decisions, not
values established by these papers. They must be preregistered on a calibration split,
then evaluated once on held-out documents. Run controlled perturbations over all 157
documents for coverage, but tune transforms/thresholds on a frozen development split
and report final claims on the held-out split. Bootstrap model differences by document,
not by augmented variant, because variants of the same source are dependent.

With no human ratings, the defensible validation targets are known mutation truth,
source-backed entity evidence, blind visual defect audits, and cross-metric
consistency. An LLM/VLM audit can help find failures, but it must be blinded to model
identity and automatic scores, counterbalanced in presentation order, required to cite
page/region evidence, and treated as an audit—not ground truth or a training target.

## Empirical audit completed for this prototype

The evidence scope must not be collapsed into a single headline count:

- The v1 harness planned 16,167 controlled variants over all 157 sources; 16,142
  applied, 25 were not applicable, and none failed. This is broad harness evidence,
  not a v2 validation run.
- The current v2 evaluator rescored 628 retained mid-severity cases (four per source).
  A blinded then post-unblind LLM forensic pass marked 530 valid and visible and
  rejected 98 as invalid, invisible, or not assessable. Diagnostic thresholds fired
  on many rejected cases: content 40.8%, layout 82.7%, tolerant ink 99.0%, and
  typography 16.3%. Mechanical change detection is therefore not visible severity.
- On those 628 cases, predicted boxes were fully useful in 496, partially useful in
  23, and not useful in 109. The percentages must use all 628 as the denominator.
- A second blinded LLM pass covered the 208-case first slice. Exact
  panel/A/B-abstain agreement was 83.7% (Cohen kappa 0.734). When both passes
  committed, changed-panel agreement was 98.8%, but defect-axis agreement was only
  14.6% across 82 cases. The first pass abstained on 98 and the second on 121. This
  negative result rejects the old axis taxonomy as stable ground truth.
- The strict current-code identity run passed all nine implemented checks on all 157
  references. A separate 471-row Text-LTSim series moved one block right at three
  severities for every source: scores decreased monotonically for 157/157 documents,
  but only 97/157 severity-2 changes were valid and visible in the LLM audit. The
  median severity-1-to-3 score drop was 0.00183. This validates mechanical
  sensitivity for one transform, not a perceptual threshold.
- All 156 available frozen Gemini PDFs received v2 scores and a blinded LLM forensic
  review. Same-canvas/grid SSIM was eligible for only 2/156; table, formula, and
  figure structure axes abstained for all 156. Against the same non-human labels,
  page-count and boundary diagnostics had AUC 0.909 and 0.953, while strict-token and
  typography AUC were 0.550 and 0.535. Layout AUC was undefined because every output
  was labeled with some layout issue.
- Seven complete four-way sets provide 21 candidate comparisons for Reference,
  Gemini, Claude Sonnet, and Claude Opus. Their protocols differ: Gemini was
  source-only while six Claude cases used iterative visual feedback. The grids are
  diagnostic examples, not a model leaderboard. Pooled rank associations over 21
  clustered rows and one LLM reviewer are exploratory only.

These results support a research prototype with inspectable raw diagnostics. They do
not support universal quality bands, a 0–100 grade, a fair model ranking, or human
perceptual claims.

## Recommended v2 report surface

For every model/document pair, show:

- eligibility, extraction coverage, page/canvas facts, and every abstention reason;
- strict NFC content P/R/F1, document NES, partial critical-inventory mismatches,
  and a separate NFKC boxed-word view;
- matched geometry quantiles and the Text-LTSim trial; show order and boundary
  outputs only when their conditional gates pass;
- raw typography residuals, fail-closed SSIM, and clearly labeled legacy raster
  diagnostics;
- complete top-defect rows with page, box, reference text, candidate text, and cause;
- visual overlays/heatmaps generated from the same entity manifest; and
- evaluator, renderer, extractor, tokenizer, configuration, and artifact hashes.

Across documents, publish each axis independently: macro mean, median, q10, failure
rate, abstention rate, document-level paired differences with bootstrap intervals,
and win/tie/loss counts. Do not average an abstention as zero, and do not let strong
content compensate for failed layout, pagination, or specialized structure.
