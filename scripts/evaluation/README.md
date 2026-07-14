# PDF fidelity evaluation

The evaluator compares rendered PDFs without requiring their LaTeX or Typst
sources. It reports content and visual fidelity separately and emits labeled
word-box overlays plus raster difference images.

## Compare two PDFs

```bash
mamba run -n lathe python scripts/evaluation/compare_pdfs.py \
  reference.pdf candidate.pdf --out-dir results/pdf_comparison
```

The output contains `metrics.json`, `metric_config.json`, and per-page PNGs.

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
