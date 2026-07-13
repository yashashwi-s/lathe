# LaTeX Benchmark v0 Results

Built: 2026-07-13

This directory contains deterministic LaTeX-to-Typst conversion outputs for `data/latex_benchmark_v0`.

## Engine Summary

| Engine | Converted | Typst-compiled | Total |
|---|---:|---:|---:|
| `pandoc` | 166 | 154 | 166 |
| `tylax` | 166 | 96 | 166 |
| `typetex` | 166 | 152 | 166 |

`typetex` is the existing project approximation: Pandoc Typst output with math routed through the MiTeX Typst package via `scripts/dataset/typetex_filter.lua`.

## Documents

- `documents/dataset_provenance.pdf`: one section per category, one page per sample, with rendered reference and source-origin metadata.
- `documents/engine_comparison_grid.pdf`: one section per category, one page per sample, with all pages from each available PDF tiled into the cell.

The comparison grid uses:

- Reference PDF
- Pandoc-rendered Typst PDF
- Tylax-rendered Typst PDF
- TypeTeX-rendered Typst PDF

Missing cells indicate conversion or Typst compilation failure; exact statuses are in `engine_manifest.csv`.

## Error Reports

- `compilation_errors.md`: human-readable summary of remaining engine compilation failures and general patches applied.
- `compilation_errors.csv`: machine-readable per-engine failure list.
- `prepatch_engine_manifest.csv` and `prepatch_summary.json`: saved baseline before the general patches.

## General Patches Applied

- Enabled Typst heading and equation numbering for converter outputs.
- Converted unresolved Pandoc-style `@key` references/citations to visible plain text `[key]` when no matching Typst label exists.
- Normalized TypeTeX/MiTeX math input by stripping LaTeX labels and equation wrappers inside math.
- Rewrote common MiTeX-hostile math macros `\d` and `\slash` to portable forms.
