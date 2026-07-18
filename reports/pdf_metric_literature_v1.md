# Rendered PDF fidelity metrics: evidence matrix and v1 design

Status: research specification. This document defines metric candidates and does not report benchmark results.

Important: `ADOPT` below means adopted as a target design requirement, not
implemented or validated in the current code. The executed all-157 study uses
five simpler harness projections. CLEval, LTSim, PaIRS, GriTS, TEDS, CDM,
SSIM/MS-SSIM, and validated figure matching are not implemented in v1 and must
be labeled `not_implemented` in any result report.

## Scope and notation

The target is reference-based comparison of a LaTeX reference PDF and a PDF rendered from an AI-produced Typst conversion. Exact content, spatial organization, reading order, typography, tables, formulas, figures, and pagination are separate observables.

Notation:

- `R`, `C`: reference and candidate.
- `N_R`, `N_C`: reference and candidate entity counts.
- `m`: matched entity mass or count.
- `P = m / N_C`, `Q = m / N_R`: precision and recall. `F1 = 2PQ / (P + Q)`.
- `Lev(a,b)`: Levenshtein distance.
- `LCS(a,b)`: longest common subsequence length.
- `IoU(A,B) = area(A intersect B) / area(A union B)`.
- `GIoU(A,B) = IoU(A,B) - area(E \ (A union B)) / area(E)`, where `E` is the smallest enclosing box.
- All page coordinates are divided by page width and height before comparison.
- `not_applicable` and `abstain_low_evidence` are distinct from a score of zero.

Decision labels:

- **ADOPT**: include in the v1 core scorecard.
- **TRIAL**: implement and calibrate, but do not use as a grading gate until it passes the validation contract.
- **REJECT**: do not use for grading; a narrowly defined diagnostic use may remain.

## Evidence matrix

| Dimension | Metric and exact definition | Primary evidence | Decision | Failure modes and required controls |
|---|---|---|---|---|
| Content inventory | Normalize text with a frozen Unicode/whitespace policy. Preserve digits, operators, punctuation, citations, and case unless an explicit case-insensitive view is also reported. With token multiplicities `c_R(t)` and `c_C(t)`, `m = sum_t min(c_R(t), c_C(t))`; report `P = m / N_C`, `Q = m / N_R`, and `F1`. | Modular content evaluation is used by [OmniDocBench](https://arxiv.org/abs/2412.07626); F-score aggregation is also used by [GriTS](https://arxiv.org/abs/2203.12555) and [CDM](https://arxiv.org/abs/2409.03643). | **ADOPT** | Ignores order and location; repeated tokens are indistinguishable. Never report it without spatial grounding and reading order. Publish the exact normalization policy and both precision and recall so hallucination and omission remain distinct. |
| Block text | For each matched text block, `S_NED = 1 - Lev(s_R,s_C) / max(|s_R|,|s_C|,1)`. Aggregate blocks by unweighted macro mean and by reference-character-weighted mean; report both. | [OmniDocBench](https://github.com/opendatalab/OmniDocBench) uses normalized edit distance for text blocks. | **ADOPT** | A whole-page string conflates recognition, segmentation, and order. Character-weighted means let long prose hide sparse errors; macro means overemphasize short blocks. Block matching confidence and both aggregates are required. |
| Text recognition and localization | Adapt CLEval. Published CLEval generates evenly spaced pseudo-character centers inside each ground-truth word box, matches boxes that contain at least one center subject to an area-precision filter, supports one-to-many and many-to-one matches, evaluates recognized content with LCS, and computes `Score = (CorrectNum - GranularityPenalty) / TotalNum`. Report character recall, precision, H-mean, split, merge, miss, overlap, and false-positive counts. For digital PDFs, use actual character quads when reliably exposed; otherwise use the published pseudo-centers. | [CLEval paper and equations](https://openaccess.thecvf.com/content_CVPRW_2020/papers/w34/Baek_CLEval_Character-Level_Evaluation_for_Text_Detection_and_Recognition_Tasks_CVPRW_2020_paper.pdf); [official code](https://github.com/clovaai/CLEval). | **ADOPT**, with PDF-character adaptation | Published pseudo-centers assume approximately uniform character placement, which is weak for proportional fonts and math. PDF character extraction can be corrupted by ligatures, font encodings, or missing ToUnicode maps. Emit extraction coverage and abstain when character evidence is unreliable. |
| Text geometry | On CLEval-matched characters or tokens, report median and 90th percentile normalized center displacement, `|log(w_C/w_R)|`, `|log(h_C/h_R)|`, baseline displacement, and box IoU. A summary score may be `exp(-q90_displacement / tau)` only after `tau` is fixed on calibration perturbations. | The localization requirement follows CLEval. Position-aware bipartite matching is also used by [CDM](https://arxiv.org/abs/2409.03643) and [LTSim](https://arxiv.org/abs/2407.12356). | **ADOPT** atomic residuals; **TRIAL** scalar transform | Repeated strings create ambiguous matches. Constrain candidate matches by page, block, and local order. Do not let a global page registration erase real layout shifts. Always retain the per-entity match manifest. |
| Semantic block layout | LTSim represents each element as `e_i = (b_i,c_i)`. Optimal transport finds `gamma* = argmin_gamma sum_ij gamma_ij mu(e_i,e_j)` subject to uniform source and target mass. `delta_bbox = (1 + GIoU(b_i,b_j)) / 2`; `delta_label = 1[c_i=c_j]`; `mu = 1 - (delta_bbox + delta_label)/2`; `EMD = sum_ij gamma*_ij mu_ij`; `LTSim = exp(-EMD/sigma)`, with `sigma = 1` for layout-level comparison. | [LTSim, equations 4-10](https://arxiv.org/pdf/2407.12356). | **TRIAL** | Standard LTSim gives partial spatial credit across different labels, which is reasonable for generation but permissive for faithful conversion. Evaluate both published LTSim and a strict-label variant with cross-label cost fixed to one. Promote only if missing, extra, split, merge, and relabel perturbations are correctly ordered. |
| Alternative layout measures | DocSim uses maximum-weight one-to-one element matching with a weight based on smaller element area and exponential center/shape differences. MaxIoU averages IoU over maximum-weight matches and requires identical label multisets. MeanIoU rasterizes each semantic class and averages class IoU. | Comparative analysis and failure examples in [LTSim](https://arxiv.org/pdf/2407.12356). | **REJECT** DocSim and MaxIoU as general grades; **TRIAL** MeanIoU diagnostic | DocSim has an inconsistent scale and can reward removal of small elements. MaxIoU can exclude most predictions when label multisets differ. MeanIoU gives a fixed zero for a missing class and loses instance identity. |
| Reading order | After content-based block matching, let `pi` and `sigma` be two permutations of the same `N` matched block IDs. If `S(pi,sigma)` is the number of adjacent swaps/inversions required to transform one into the other, `tau = 1 - 2S(pi,sigma) / [N(N-1)/2]`. Report `tau`, matched-block coverage, and inversion examples. | [Automatic Evaluation of Information Ordering](https://aclanthology.org/J06-4002.pdf) defines the measure and validates it against human ratings and reading time. | **ADOPT** | Kendall's tau ignores unmatched items and assumes one reference order. Pair it with content coverage. Mark pages with genuinely non-linear or ambiguous order and do not force an arbitrary total order without annotation. |
| Reading-order string diagnostic | Normalized Indel Similarity: `NID = 1 - IndelDistance(s_R,s_C) / (|s_R| + |s_C|)`. `NID-S` first removes tables. | [OpenDataLoader benchmark metric definition](https://github.com/opendataloader-project/opendataloader-bench). | **TRIAL** diagnostic | Text substitutions, omissions, and order changes are entangled. It must not replace matched-block Kendall tau. |
| Layout object presence | For reference and candidate regions labeled as text, title, list, table, figure, formula, caption, and algorithm, report class-aware box precision, recall, F1, matched IoU, and dataset-level COCO AP over IoU thresholds `0.50:0.05:0.95`. | [DocLayNet](https://arxiv.org/abs/2206.01062) provides human-annotated 11-class document boxes and reports COCO-style mAP against inter-annotator agreement. | **TRIAL** | A learned detector makes detector error part of the metric. Prefer source-backed or manually verified reference regions. Record detector version, confidence, and coverage; abstain for classes below validation reliability. Detection AP measures presence/localization, not crop fidelity. |
| Tables: GriTS | Represent each table as a grid-cell matrix. Select monotone row and column subsequences of `R` and `C` maximizing aligned cell similarity. If `M_f` is the sum of cell similarities in the best valid 2D substructure, `P_f = M_f / |C|`, `Q_f = M_f / |R|`, and `GriTS_f = 2M_f / (|R| + |C|)`. `GriTS_Top` uses IoU of cell boxes expressed in grid coordinates; `GriTS_Con` uses `2 LCS(a,b)/(|a|+|b|)` for cell text; `GriTS_Loc` uses IoU of cell boxes in page coordinates. | [GriTS paper](https://arxiv.org/abs/2203.12555); [official Table Transformer code](https://github.com/microsoft/table-transformer). | **ADOPT** when cell extraction is reliable | Topology alone is necessary but insufficient. Content depends on text extraction; location depends on table detection and page alignment. Report all three variants, precision, recall, approximation bound gap, and extraction coverage. Never substitute row/column counts for GriTS. |
| Tables: TEDS | Parse normalized HTML tables as trees. `TEDS = 1 - TreeEditDistance(T_R,T_C) / max(|T_R|,|T_C|,1)`. In TEDS, unequal tags cost one; equal non-cell tags cost zero; cell substitution cost is the normalized Levenshtein distance between cell texts. TEDS-S removes cell text and evaluates structure only. | [PubTabNet/TEDS paper](https://arxiv.org/abs/1911.10683); concise formula and TEDS-S definition in [OpenDataLoader benchmark](https://github.com/opendataloader-project/opendataloader-bench). | **ADOPT** cross-check when common HTML is available | Requires a deterministic LaTeX/Typst-to-HTML table normalization. Tree representation can respond differently to missing rows and columns and can mix function/header labeling with structure. Use GriTS as the primary table decomposition. |
| Formulas: CDM | Normalize source tokens; render every token in a unique color to obtain token boxes. Hungarian matching minimizes `sum_i L_match`, where `L_match = W_t L_t + W_p L_p + W_o L_o`; `L_t` is token mismatch cost, `L_p = ||b_i-b_j||_1 / D_b`, and `L_o = ||o_i-o_j||_1 / D_o`. Remove token-inconsistent matches and matches that violate a translation/scale model using RANSAC. `CDM = 2TP / (2TP + FP + FN)`. | [CDM paper, equations 2-8](https://arxiv.org/pdf/2409.03643); [official implementation](https://github.com/opendatalab/UniMERNet/tree/main/cdm). | **TRIAL** | The published implementation expects LaTeX on both sides. Direct Typst-vs-LaTeX source comparison is invalid. Establish a common canonical token representation, or implement and separately validate a rendered-glyph adaptation. Until then, CDM-derived results are diagnostic and must not grade formulas. |
| Formula source metrics | Exact match, BLEU, or edit distance over source strings. BLEU is `BP * exp(sum_n w_n log p_n)` over clipped n-gram precisions. | [BLEU](https://aclanthology.org/P02-1040/); CDM documents source-syntax failures for equivalent rendered formulas. | **REJECT** for cross-language grading | LaTeX and Typst are different languages, and multiple LaTeX strings render identically. Source similarity measures syntax rather than rendered mathematical correctness. |
| Figures and non-text objects | Match annotated figure/object regions by class and geometry. Report object P/R/F1 and IoU. For matched crops, compare fixed-resolution edge maps and SSIM maps; retain the crop and defect heatmap. | Object localization follows [DocLayNet](https://arxiv.org/abs/2206.01062); SSIM evidence is below. | **TRIAL** | A PDF drawing/image detector can confuse table rules, formulas, ornaments, and figures. Crop appearance can be changed by resampling without changing meaning, while a small wrong label can be critical. Keep presence, geometry, and crop appearance separate. |
| Pagination | Match ordered block IDs first. A page break is a boundary between two adjacent matched reference blocks. Report page-break precision, recall, F1; block-to-page assignment accuracy; page-count delta; and orphan/widow or clipped-block defects. | No established published metric was found for reference-based LaTeX-to-Typst pagination. This is a benchmark-specific observable. | **ADOPT** atomic metrics | Page count alone cannot distinguish a near-boundary reflow from two-page compression. Boundary F1 requires reliable block matches and a policy for blocks split across pages. Publish the matched boundary list. |
| Typography | For matched spans, report font size `|log(size_C/size_R)|`, baseline displacement, line-height error, weight/style agreement, and heading-level consistency. Compare rendered glyph crops for appearance; do not require PDF font-family names to match. | No established, validated typeset-PDF typography fidelity metric was found in the reviewed primary literature. | **ADOPT** direct observables; **TRIAL** any scalar | PDF font names, subsets, encodings, ligatures, and producer choices are not visual identity. A learned scalar would require domain-specific calibration. Font metadata or math-font glyph extraction alone must not become a gate. |
| Raster structure | With local means `mu`, variances `sigma^2`, and covariance `sigma_RC`, common SSIM is `[(2mu_R mu_C + C1)(2sigma_RC + C2)] / [(mu_R^2 + mu_C^2 + C1)(sigma_R^2 + sigma_C^2 + C2)]`. MS-SSIM combines luminance at the coarsest scale with contrast and structure across scales: `l_M^alpha_M product_j c_j^beta_j s_j^gamma_j`. | [SSIM primary paper](https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf); [MS-SSIM primary source](https://ece.uwaterloo.ca/~z70wang/publications/msssim.html). | **TRIAL** diagnostic, not a grading gate | White background dominates a page average. Font rasterization and sub-pixel shifts can outweigh semantic importance. Use fixed renderer, DPI, colorspace, and page size; report local heatmaps and content-region summaries, not only a page mean. |
| Deep perceptual raster distance | LPIPS computes `d(R,C) = sum_l [1/(H_l W_l)] sum_hw ||w_l elementwise (yhat_R,lhw - yhat_C,lhw)||_2^2`, where feature activations are channel-normalized and `w_l` are learned channel weights. | [LPIPS primary paper, equation 1](https://openaccess.thecvf.com/content_cvpr_2018/papers/Zhang_The_Unreasonable_Effectiveness_CVPR_2018_paper.pdf). | **REJECT** as a grade; **TRIAL** crop diagnostic | LPIPS was calibrated using natural-image patch judgments and ImageNet-family features, not dense typeset pages. Learned invariance can under-penalize a wrong glyph, digit, operator, or thin rule. Promotion requires document-domain perturbation and judge validation. |
| Deep structure/texture distance | DISTS is `1 - sum_ij [alpha_ij l(x_ij,y_ij) + beta_ij s(x_ij,y_ij)]`, using VGG feature maps, correlations of spatial means for texture, feature-map correlations for structure, non-negative learned weights, and weights summing to one. | [DISTS primary paper](https://arxiv.org/abs/2004.07728). | **REJECT** as a grade; **TRIAL** page/crop diagnostic | DISTS is deliberately tolerant of texture resampling and mild geometric transformations, uses global statistics, and provides no native defect map. Those properties can hide typesetting errors. |
| Pixel error | `MSE = mean((R-C)^2)`; `PSNR = 10 log10(MAX^2/MSE)`. | Limitations motivate both [SSIM](https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf) and [LPIPS](https://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_The_Unreasonable_Effectiveness_CVPR_2018_paper.html). | **REJECT**, except deterministic renderer regression | Extremely sensitive to translation and antialiasing; large blank areas dominate; no entity-level explanation. |
| Semantic text similarity | BERTScore greedily matches contextual token embeddings and reports embedding-similarity P/R/F1. METEOR permits stem, synonym, and paraphrase matches. | [BERTScore](https://arxiv.org/abs/1904.09675); [METEOR project and papers](https://www.cs.cmu.edu/~alavie/METEOR/index.html). | **REJECT** for fidelity grading | These metrics intentionally reward paraphrase or semantic proximity. The conversion task requires exact preservation of wording, numbers, units, citations, and symbols. |
| Overall parsing average | OmniDocBench reports `Overall = [(1 - TextEditDistance)*100 + TableTEDS + FormulaCDM] / 3`. | [OmniDocBench official evaluation](https://github.com/opendatalab/OmniDocBench). | **REJECT** as the PDF-fidelity aggregate | It is suitable for parsing coverage but omits page geometry, typography, figures, and pagination. Arithmetic compensation lets strong text hide a severe layout failure. Retain it only for direct comparability with parsing benchmarks. |
| LLM/VLM judge | Blind pairwise or rubric evaluation with model identity and automatic scores hidden. Counterbalance A/B order; rerun swapped; require atomic defect locations, confidence, and an order-consistency result. | [MT-Bench judge study](https://arxiv.org/abs/2306.05685) documents position, verbosity, and self-enhancement biases; [systematic position-bias study](https://arxiv.org/abs/2406.07791). | **TRIAL**, validation only | A judge is not ground truth. It can inherit provider/style preferences, miss small visual facts, and change under ordering or prompt wording. Freeze judgments before unblinding and compare them with known perturbation severity. |

## Recommended modular v1 scorecard

### 1. Eligibility and evidence

These are reported before any score:

1. Candidate compile success and compile log classification.
2. Reference and candidate page counts and page dimensions.
3. Extracted text/character coverage.
4. Semantic-region extraction coverage by class.
5. Applicable specialized modules: table, formula, figure, algorithm.
6. Evidence state for every module: `scored`, `not_applicable`, or `abstain_low_evidence`.

A compile failure is a benchmark failure but must retain its cause. An extraction failure is evaluator abstention, not candidate score zero.

### 2. Core axes

| Axis | Required v1 outputs | Score use |
|---|---|---|
| Content | Token inventory P/R/F1; macro and character-weighted block NED; numeric/operator/citation mismatch lists linked to spans | Core |
| Text grounding | CLEval-adapted character P/R/H-mean; split, merge, miss, overlap, FP; match coverage | Core |
| Geometry | Matched-character/token q50 and q90 center displacement; size, baseline, and IoU residuals; per-block residuals | Core atomic evidence; calibrated transform only after validation |
| Block layout | Strict-label LTSim trial; class presence P/R/F1; matched block IoU | Trial until calibrated |
| Reading order | Kendall tau, matched-block coverage, inversion list | Core |
| Pagination | Page-break P/R/F1; block-to-page accuracy; page-count delta; clipped/orphan defect list | Core |
| Typography | Font-size, line-height, baseline, style/weight, and hierarchy residuals | Core direct observables; no unvalidated scalar |
| Tables | GriTS_Top, GriTS_Con, GriTS_Loc with P/R; TEDS and TEDS-S; extraction evidence | Core when applicable and reliable |
| Formulas | CDM-derived trial after common tokenization; formula-region defect list | Trial; no grading gate until cross-language validation |
| Figures/objects | Object P/R/F1, matched IoU, crop SSIM/edge diagnostics | Presence and geometry trial; crop appearance diagnostic |
| Raster residual | Content-region SSIM distribution and localized heatmaps | Diagnostic only |

### 3. Aggregation

The primary result is the axis vector plus applicability and confidence. Dataset reporting must include:

- Per-document scores and defect manifests.
- Macro means by document form, difficulty, and specialized-content attribute.
- Overall macro mean, median, 10th percentile, and failure/abstention rate for every axis.
- Paired model differences with document-level bootstrap confidence intervals.
- Counts of documents on which each model wins, ties, or loses per axis.

No arithmetic overall score is part of v1.

If an operational scalar is later required, trial the non-compensatory geometric mean

`G = exp[sum_{k in applicable} w_k log(max(epsilon,S_k)) / sum_k w_k]`

and always publish `G`, the full axis vector, `min_k S_k`, the weights, and all abstentions. Weights and axis transforms must be frozen using calibration data and validated on held-out documents before the scalar is used for ranking.

### 4. Explainability contract

Every scored document must emit:

1. Reference-to-candidate page and entity match tables.
2. Unmatched reference and candidate entities.
3. Entity labels, normalized coordinates, text, and match costs.
4. Per-axis atomic contributions.
5. Top defects ordered by severity, each with a page, region, and reason.
6. Overlay and heatmap images derived from the same match manifest.
7. Extractor, renderer, metric, normalization, and configuration versions.

A score without its entity-level evidence is invalid for the benchmark report.

## Validation and augmentation contract

### Dataset use

Evaluate all 157 references, but do not tune and claim on the same observations. Freeze a stratified calibration, validation, and held-out assignment by document form, difficulty, page count, and specialized-content attributes. If a form is too sparse for a fixed split, use leave-one-form-out validation and keep a final untouched document subset for reporting.

### Perturbation families

Apply generic perturbations to every reference at three or more deterministic severities. Apply specialized perturbations only to references whose manifests establish applicability.

| Family | Required perturbations | Expected primary response | Expected invariants |
|---|---|---|---|
| Content | Delete, duplicate, insert, or substitute a word, line, paragraph, digit, operator, citation, or unit | Inventory P/R/F1, NED, CLEval content | Geometry for unaffected matched entities |
| Order | Adjacent-block swap, column-order swap, caption reorder, footnote reorder | Kendall tau and inversion list | Content inventory |
| Geometry | Translate or resize one block; change margin, column gap, wrap width, or line spacing; introduce clipping or overlap | CLEval localization residuals, strict LTSim, object IoU | Content inventory unless clipping removes ink/text |
| Pagination | Insert/delete a break; move one block across a page; compress or expand page flow | Boundary F1, block-to-page accuracy, page delta | Content inventory for pure reflow |
| Typography | Change font size, line height, weight, style, family, heading level, or math style | Typography residuals and crop diagnostics | Content and reading order |
| Table | Remove, duplicate, or swap a row/column; merge/split a cell; alter span, cell text, or rule | GriTS variants and TEDS variants | Non-table axes outside the table region |
| Formula | Replace operator/digit/variable; drop numerator, denominator, subscript, or superscript; alter delimiter or aligned-line structure | CDM-derived trial and localized formula diagnostics | Non-formula axes outside the formula region |
| Figure/object | Delete, duplicate, substitute, crop, translate, resize, or swap/detach a caption | Object P/R, IoU, crop diagnostic, caption relation | Text content outside affected regions |
| Renderer invariance | Change PDF metadata, object order, font subsetting/encoding, lossless compression, raster DPI, antialiasing, or color profile without changing intended appearance/content | No material change in semantic, order, or geometry axes | All core semantic/structural axes |
| Real-world image robustness | Rotation, warp, keystone, watermark/background, illumination, ink bleed/holdout, defocus/motion blur, speckle, texture | Diagnostic robustness response | Not part of clean rendered-PDF fidelity grade |

The real-world robustness list follows [RoDLA](https://arxiv.org/abs/2403.14442), which defines 12 perturbation types across five groups and three severities. Semantic-versus-formatting separation follows [OHRBench](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_OCR_Hinders_RAG_Evaluating_the_Cascading_Impact_of_OCR_on_ICCV_2025_paper.html). Controlled structural perturbation precedents also appear in GriTS, TEDS, and CLEval.

### Required validation properties

For every metric and perturbation family, report:

1. **Identity:** reference versus itself reaches the defined optimum.
2. **Monotonicity:** increasing known severity changes the targeted metric in the expected direction; report Kendall or Spearman rank correlation and violations.
3. **Selectivity:** targeted-axis effect exceeds off-target leakage; publish the full perturbation-by-metric response matrix.
4. **Localization:** the top reported defect overlaps the known modified region; report hit rate and region IoU/coverage.
5. **Directionality:** insertion affects precision more than recall; deletion affects recall more than precision.
6. **Symmetry:** metrics claimed to be symmetric give equal results under input reversal.
7. **Invariance:** renderer-only negative controls do not materially change semantic or structural axes.
8. **Determinism:** repeated runs with identical versions and seeds are identical.
9. **Evidence behavior:** unsupported modules abstain instead of silently returning zero or one.
10. **Tail behavior:** localized severe defects are visible in entity evidence and tail summaries even when page means remain high.

### Manual or LLM audit

- Inspect extraction correctness for all 157 unperturbed references.
- Pre-register a stratified augmented audit sample by family, severity, form, and difficulty.
- Hide model, perturbation, and metric identities.
- Use a fixed atomic rubric: content, geometry, order, typography, specialized structure, pagination, and overall acceptability.
- Counterbalance reference/candidate placement and repeat swapped comparisons.
- Freeze judgments before revealing perturbation or automatic scores.
- Validate automatic metrics against known severity and blinded ordinal judgments separately.
- Record judge version, prompt, image resolution, confidence, position consistency, and cited defect regions.

## Explicit exclusions from v1 grading

- A single global raster similarity.
- Pixel MSE or PSNR.
- LPIPS or DISTS without typeset-document calibration.
- BLEU, METEOR, BERTScore, or source-string similarity for LaTeX-versus-Typst correctness.
- Formula-font-name or PDF glyph-code equality.
- Row/column count heuristics in place of GriTS or TEDS.
- Raw page count in place of pagination boundary evidence.
- DocSim or MaxIoU as a general layout score.
- LLM/VLM judgment as ground truth.
- Any aggregate whose weights or transforms were selected on the reported held-out documents.
