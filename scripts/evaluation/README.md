# PDF fidelity evaluation

## Metric system v2 (current research recommendation)

`pdf_metric_axes_v2.py` is the current evidence-first evaluator. It emits no
universal score. Its retained components are strict-NFC and compatibility-NFKC
text views, exact number/operator/citation inventories, raw token geometry,
published LTSim equations on the per-page all-text subset, conditional reading
order, pagination, typography residuals, and fixed-protocol raster diagnostics.
SSIM abstains when physical canvases or raster grids differ. Tables, formulas,
figures, and full semantic LTSim abstain until both PDFs have validated common
structures.

Compare one pair:

```bash
mamba run -n lathe python scripts/evaluation/pdf_metric_axes_v2.py \
  reference.pdf candidate.pdf --pretty
```

Evaluate a reference/candidate manifest:

```bash
mamba run -n lathe python scripts/evaluation/evaluate_metric_v2_manifest.py \
  pairs.csv --out-dir results/metric_research_v2/run --workers 4
```

The frozen research artifacts are under `results/metric_research_v2/`; the
methodology report source is `reports/pdf_fidelity_metric_system_v2.typ`.
Controlled mutations validate metric mechanics, and blinded LLM review audits
evidence behavior. Neither is a substitute for human perceptual ratings.

The evaluator compares rendered PDFs without requiring their LaTeX or Typst
sources. It reports content and visual fidelity separately and emits labeled
word-box overlays plus raster difference images.

## Compare two PDFs

```bash
mamba run -n lathe python scripts/evaluation/compare_pdfs.py \
  reference.pdf candidate.pdf --out-dir results/pdf_comparison
```

The output contains `metrics.json`, `metric_config.json`,
`scorecard_config.json`, and per-page PNGs.

`metrics.json` retains the historical `pdf_fidelity_v0.1` weighted scores for
reproducibility and also includes `pdf_fidelity_scorecard_v0.3`. The
development scorecard reports content, layout, typography, appearance proxy,
pagination, evidence coverage, and specialized diagnostics independently. It
applies explicit strict gates and does not emit a replacement aggregate score.

## Rebuild the 30-sample calibration report

```bash
mamba run -n lathe python scripts/evaluation/evaluate_prompt_dev_pdf_fidelity.py
```

This writes machine-readable results under
`results/ai_latex_to_typst/metrics/prompt_dev_30/` and the A3 review PDF at
`output/pdf/prompt_dev_30_pdf_fidelity_report.pdf`.

Project dependencies are PyMuPDF, NumPy, SciPy, scikit-image, OpenCV, Pillow,
and ReportLab. Run all project commands through the `lathe` mamba environment.

The metric is currently `pdf_fidelity_v0.1`. Its weights are calibration
weights, frozen in the generated `metric_config.json`; they are not yet fitted
to human ratings and must not be presented as held-out benchmark results.

## Controlled scorecard study

```bash
mamba run -n lathe python scripts/evaluation/evaluate_controlled_metric_scorecard.py
```

This regenerates the source-known corruption study under
`results/metric_calibration/controlled_v0_2/`. It checks monotonic response to
translation, deletion, wrong numbers, font changes, obstruction, added/missing
pages, and page reordering. These checks validate engineering behavior only;
they do not define aesthetic preference or an overall ranking score.

Audit the same scorecard on the 30 clean prompt-development conversions with:

```bash
mamba run -n lathe python scripts/evaluation/audit_prompt_dev_scorecard.py
```

The audit is development-only and identifies real gate/review disagreements.

Run the no-rating calibration matrix on one real reference from every benchmark
category with:

```bash
mamba run -n lathe python scripts/evaluation/evaluate_reference_perturbations.py
```

This writes 186 source-known comparisons under
`results/metric_calibration/reference_perturbations_v0_3/`. The study checks
identity and small-shift invariance, detector recall, severity monotonicity,
non-text erasure, table-row erasure, and formula-glyph erasure. It can support
detector and review-threshold revisions, but cannot define preference by itself.

## Blind AI validation and development grade

Evaluate the 24 exact-protocol canonical AI outputs, join the already frozen
blind rubric, and rebuild the final study with:

```bash
mamba run -n lathe python scripts/evaluation/audit_canonical_ai_models.py
mamba run -n lathe python scripts/evaluation/analyze_manual_validation.py
mamba run -n lathe python scripts/ai/build_ai_metric_study_report.py
```

The analysis maps the conservative floor
`min(content, layout, typography, pagination)` to the blind 0-4 overall rubric
with monotonic calibration. Canonical case grades are leave-one-reference-out.
This is calibrated to one blind LLM judge, not human ratings, and remains a
development result. The PDF and 24-row case manifest are written under
`output/pdf/`.
