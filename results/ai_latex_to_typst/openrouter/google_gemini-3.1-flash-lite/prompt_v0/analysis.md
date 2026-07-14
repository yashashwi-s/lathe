# Prompt v0 analysis

This report is filtered after the visual-corruption cleanup. Three invalid reference samples were removed from the original 33-sample development split: `01_prose_sections_015`, `10_compact_papers_003`, and `10_compact_papers_014`.

## Clean results

- Clean samples: 30
- Final compiled outputs: 22/30
- First-pass compiled outputs: 15/30
- Repairs: 7/15 retry opportunities
- Page-count matches among compiled outputs: 17/22
- API/provider/local infrastructure failures: 0
- API-reported cost after filtering: $0.092409

## Main remaining failure patterns

| Pattern | Examples | Note |
|---|---|---|
| Algorithm/pseudocode structure | `09_algorithms_003`, `09_algorithms_005`, `09_algorithms_021` | The model often emits unbalanced blocks or delimiters for algorithmic layouts. |
| Typst math symbol naming | `03_math_inline_display_014`, `04_math_aligned_012`, `07_figures_captions_001` | Failures include LaTeX-style names such as `widehat`, `bigcirc`, or unsupported symbol modifiers. |
| Cross-reference handling | `08_crossrefs_citations_008`, repaired cases in `08_crossrefs_citations_012` and `08_crossrefs_citations_013` | References need stricter rules for creating labels before using `@key`. |
| Array/content syntax | `02_lists_formatting_024`, `06_tables_moderate_010` | The model sometimes uses array-like structures in positions where Typst expects content. |

## Interpretation

Prompt v0 is a useful baseline after bad references are removed: prose, forms, simple tables, and figures mostly compile, while algorithms and some math-heavy samples remain brittle. Do not compare this filtered report directly against the earlier unfiltered 33-sample numbers.
