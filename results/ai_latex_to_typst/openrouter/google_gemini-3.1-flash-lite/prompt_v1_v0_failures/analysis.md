# Prompt v1 targeted-retry analysis

This run is filtered after the visual-corruption cleanup. Two invalid retry samples were removed: `01_prose_sections_015` and `10_compact_papers_003`.

## Clean results

- Clean targeted retries: 8
- Final compiled outputs: 6/8
- First-pass compiled outputs: 3/8
- Repairs: 3/5 retry opportunities
- Page-count matches among compiled outputs: 4/6
- API/provider/local infrastructure failures: 0
- API-reported cost after filtering: $0.023088

## Rescued from prompt v0

`02_lists_formatting_024`, `03_math_inline_display_014`, `04_math_aligned_012`, `06_tables_moderate_010`, `08_crossrefs_citations_008`, and `09_algorithms_003` compiled in the targeted retry run.

## Still failing

| Sample | Pattern |
|---|---|
| `09_algorithms_005` | unclosed delimiter after retry |
| `09_algorithms_021` | unclosed delimiter first, then invalid `GNN` symbol/content usage |

## Interpretation

Prompt v1 improved repair behavior on clean failures, especially references and several math/table cases. The remaining hard point is algorithm layout: the prompt needs more explicit Typst block/list rules or a constrained algorithm-rendering pattern before this should become the held-out benchmark prompt.
