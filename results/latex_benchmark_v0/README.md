# LaTeX Benchmark v0 Results

Built: 2026-07-22

This directory contains deterministic LaTeX-to-Typst conversion outputs for
all 189 accepted samples in `data/latex_benchmark_v0`, including the 32-sample
HF expansion slice.

## Engine Summary

| Engine | Converted | Typst-compiled | Total |
|---|---:|---:|---:|
| `pandoc` | 188 | 178 | 189 |
| `tylax` | 189 | 116 | 189 |
| `typetex` | 188 | 172 | 189 |

Expansion-only compilation is 27/32 for Pandoc, 23/32 for Tylax, and 23/32
for TypeTeX. Pandoc and TypeTeX emitted output for 31/32 expansion samples;
Tylax emitted output for 32/32.

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

- `compilation_errors.md`: human-readable summary of remaining engine compilation failures.
- `compilation_errors.csv`: machine-readable per-engine failure list.
- `prepatch_engine_manifest.csv` and `prepatch_summary.json`: saved baseline before the general patches.

## General Patches Applied

- Enabled Typst heading and equation numbering for converter outputs.
- Converted unresolved Pandoc-style `@key` references/citations to visible plain text `[key]` when no matching Typst label exists.
- Normalized TypeTeX/MiTeX math input by stripping LaTeX labels and equation wrappers inside math.
- Rewrote common MiTeX-hostile math macros `\d` and `\slash` to portable forms.

## Dataset scope

The original 157-sample base retains its visual-corruption cleanup. The
32-sample expansion is evaluated as a separate post-freeze slice while sharing
this deterministic-engine artifact tree. See
`data/latex_benchmark_v0/visual_corruption_cleanup.md` and
`data/latex_benchmark_v0/expansion_import.json`.
