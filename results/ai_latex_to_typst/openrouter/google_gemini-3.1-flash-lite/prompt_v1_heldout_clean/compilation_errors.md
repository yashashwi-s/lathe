# Compilation errors

This report includes every failed Typst compilation attempt, including
attempts later repaired by the model. API and local infrastructure failures
are reported separately and do not count as model compilation failures.

- Failed compilation attempts: 131
- Repaired failed attempts: 31
- Samples with final compilation failure: 50
- Compiler warning occurrences: 52
- Infrastructure failures: 0

## Error classes

| Error class | Failed attempts |
|---|---:|
| `general_syntax` | 31 |
| `math_syntax` | 17 |
| `other_compile_error` | 4 |
| `reference_or_label` | 14 |
| `unknown_symbol_or_function` | 65 |

## Compilation attempts

| Sample | Category | Attempt | Error class | Result | Error | Log |
|---|---|---:|---|---|---|---|
| `01_prose_sections_002` | `01_prose_sections` | 1 | `math_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/01_prose_sections_002/attempt_1_compile.log) |
| `01_prose_sections_002` | `01_prose_sections` | 2 | `reference_or_label` | `final_failure` | error: label `<t>` does not exist in the document | [`log`](samples/01_prose_sections_002/attempt_2_compile.log) |
| `01_prose_sections_003` | `01_prose_sections` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/01_prose_sections_003/attempt_1_compile.log) |
| `01_prose_sections_006` | `01_prose_sections` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: SU | [`log`](samples/01_prose_sections_006/attempt_1_compile.log) |
| `01_prose_sections_012` | `01_prose_sections` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: SU | [`log`](samples/01_prose_sections_012/attempt_1_compile.log) |
| `01_prose_sections_012` | `01_prose_sections` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: texttt | [`log`](samples/01_prose_sections_012/attempt_2_compile.log) |
| `02_lists_formatting_006` | `02_lists_formatting` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: hi | [`log`](samples/02_lists_formatting_006/attempt_1_compile.log) |
| `02_lists_formatting_006` | `02_lists_formatting` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: hi | [`log`](samples/02_lists_formatting_006/attempt_2_compile.log) |
| `02_lists_formatting_015` | `02_lists_formatting` | 1 | `other_compile_error` | `repaired` | error: unknown symbol modifier | [`log`](samples/02_lists_formatting_015/attempt_1_compile.log) |
| `02_lists_formatting_020` | `02_lists_formatting` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: check | [`log`](samples/02_lists_formatting_020/attempt_1_compile.log) |
| `03_math_inline_display_001` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: circ | [`log`](samples/03_math_inline_display_001/attempt_1_compile.log) |
| `03_math_inline_display_001` | `03_math_inline_display` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: dV | [`log`](samples/03_math_inline_display_001/attempt_2_compile.log) |
| `03_math_inline_display_002` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: vartheta | [`log`](samples/03_math_inline_display_002/attempt_1_compile.log) |
| `03_math_inline_display_002` | `03_math_inline_display` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: vartheta | [`log`](samples/03_math_inline_display_002/attempt_2_compile.log) |
| `03_math_inline_display_005` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: cl | [`log`](samples/03_math_inline_display_005/attempt_1_compile.log) |
| `03_math_inline_display_005` | `03_math_inline_display` | 2 | `math_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/03_math_inline_display_005/attempt_2_compile.log) |
| `03_math_inline_display_007` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: varsigma | [`log`](samples/03_math_inline_display_007/attempt_1_compile.log) |
| `03_math_inline_display_007` | `03_math_inline_display` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: varsigma | [`log`](samples/03_math_inline_display_007/attempt_2_compile.log) |
| `03_math_inline_display_008` | `03_math_inline_display` | 1 | `math_syntax` | `final_failure` | error: unknown symbol modifier | [`log`](samples/03_math_inline_display_008/attempt_1_compile.log) |
| `03_math_inline_display_008` | `03_math_inline_display` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: wedge | [`log`](samples/03_math_inline_display_008/attempt_2_compile.log) |
| `03_math_inline_display_009` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: biggl | [`log`](samples/03_math_inline_display_009/attempt_1_compile.log) |
| `03_math_inline_display_010` | `03_math_inline_display` | 1 | `math_syntax` | `repaired` | error: unknown symbol modifier | [`log`](samples/03_math_inline_display_010/attempt_1_compile.log) |
| `03_math_inline_display_012` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: dt | [`log`](samples/03_math_inline_display_012/attempt_1_compile.log) |
| `03_math_inline_display_012` | `03_math_inline_display` | 2 | `math_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/03_math_inline_display_012/attempt_2_compile.log) |
| `03_math_inline_display_013` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: hbar | [`log`](samples/03_math_inline_display_013/attempt_1_compile.log) |
| `03_math_inline_display_013` | `03_math_inline_display` | 2 | `math_syntax` | `final_failure` | error: unknown symbol modifier | [`log`](samples/03_math_inline_display_013/attempt_2_compile.log) |
| `03_math_inline_display_015` | `03_math_inline_display` | 1 | `math_syntax` | `final_failure` | error: expected content, found array | [`log`](samples/03_math_inline_display_015/attempt_1_compile.log) |
| `03_math_inline_display_015` | `03_math_inline_display` | 2 | `math_syntax` | `final_failure` | error: expected content, found array | [`log`](samples/03_math_inline_display_015/attempt_2_compile.log) |
| `03_math_inline_display_016` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: varpi | [`log`](samples/03_math_inline_display_016/attempt_1_compile.log) |
| `03_math_inline_display_016` | `03_math_inline_display` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: varpi | [`log`](samples/03_math_inline_display_016/attempt_2_compile.log) |
| `03_math_inline_display_017` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: sf | [`log`](samples/03_math_inline_display_017/attempt_1_compile.log) |
| `03_math_inline_display_018` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: wedge | [`log`](samples/03_math_inline_display_018/attempt_1_compile.log) |
| `04_math_aligned_001` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: hskip | [`log`](samples/04_math_aligned_001/attempt_1_compile.log) |
| `04_math_aligned_001` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: hskip | [`log`](samples/04_math_aligned_001/attempt_2_compile.log) |
| `04_math_aligned_002` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: none | [`log`](samples/04_math_aligned_002/attempt_1_compile.log) |
| `04_math_aligned_002` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: left | [`log`](samples/04_math_aligned_002/attempt_2_compile.log) |
| `04_math_aligned_003` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: wedge | [`log`](samples/04_math_aligned_003/attempt_1_compile.log) |
| `04_math_aligned_003` | `04_math_aligned` | 2 | `math_syntax` | `final_failure` | error: unknown symbol modifier | [`log`](samples/04_math_aligned_003/attempt_2_compile.log) |
| `04_math_aligned_004` | `04_math_aligned` | 1 | `math_syntax` | `repaired` | error: expected content, found array | [`log`](samples/04_math_aligned_004/attempt_1_compile.log) |
| `04_math_aligned_005` | `04_math_aligned` | 1 | `math_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/04_math_aligned_005/attempt_1_compile.log) |
| `04_math_aligned_005` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: wedge | [`log`](samples/04_math_aligned_005/attempt_2_compile.log) |
| `04_math_aligned_006` | `04_math_aligned` | 1 | `math_syntax` | `repaired` | error: unexpected argument | [`log`](samples/04_math_aligned_006/attempt_1_compile.log) |
| `04_math_aligned_007` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: prod | [`log`](samples/04_math_aligned_007/attempt_1_compile.log) |
| `04_math_aligned_007` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: table | [`log`](samples/04_math_aligned_007/attempt_2_compile.log) |
| `04_math_aligned_009` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: ijk | [`log`](samples/04_math_aligned_009/attempt_1_compile.log) |
| `04_math_aligned_009` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: ij | [`log`](samples/04_math_aligned_009/attempt_2_compile.log) |
| `04_math_aligned_010` | `04_math_aligned` | 1 | `math_syntax` | `repaired` | error: unknown symbol modifier | [`log`](samples/04_math_aligned_010/attempt_1_compile.log) |
| `04_math_aligned_011` | `04_math_aligned` | 1 | `math_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/04_math_aligned_011/attempt_1_compile.log) |
| `04_math_aligned_013` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: none | [`log`](samples/04_math_aligned_013/attempt_1_compile.log) |
| `04_math_aligned_013` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: otimes | [`log`](samples/04_math_aligned_013/attempt_2_compile.log) |
| `04_math_aligned_015` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: lesssim | [`log`](samples/04_math_aligned_015/attempt_1_compile.log) |
| `04_math_aligned_015` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: lesssim | [`log`](samples/04_math_aligned_015/attempt_2_compile.log) |
| `05_tables_simple_001` | `05_tables_simple` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: qrt | [`log`](samples/05_tables_simple_001/attempt_1_compile.log) |
| `05_tables_simple_001` | `05_tables_simple` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: qrt | [`log`](samples/05_tables_simple_001/attempt_2_compile.log) |
| `05_tables_simple_002` | `05_tables_simple` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: qrt | [`log`](samples/05_tables_simple_002/attempt_1_compile.log) |
| `05_tables_simple_002` | `05_tables_simple` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: qrt | [`log`](samples/05_tables_simple_002/attempt_2_compile.log) |
| `05_tables_simple_006` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_006/attempt_1_compile.log) |
| `05_tables_simple_006` | `05_tables_simple` | 2 | `general_syntax` | `final_failure` | error: expected length, color, gradient, tiling, dictionary, stroke, or none, found function | [`log`](samples/05_tables_simple_006/attempt_2_compile.log) |
| `05_tables_simple_007` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/05_tables_simple_007/attempt_1_compile.log) |
| `05_tables_simple_007` | `05_tables_simple` | 2 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/05_tables_simple_007/attempt_2_compile.log) |
| `05_tables_simple_011` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unexpected keys "top" and "bottom", valid keys are "paint", "thickness", "cap", "join", "dash", and "miter-limit" | [`log`](samples/05_tables_simple_011/attempt_1_compile.log) |
| `05_tables_simple_011` | `05_tables_simple` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: elta | [`log`](samples/05_tables_simple_011/attempt_2_compile.log) |
| `05_tables_simple_012` | `05_tables_simple` | 1 | `other_compile_error` | `final_failure` | error: unknown symbol modifier | [`log`](samples/05_tables_simple_012/attempt_1_compile.log) |
| `05_tables_simple_012` | `05_tables_simple` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: down | [`log`](samples/05_tables_simple_012/attempt_2_compile.log) |
| `05_tables_simple_014` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unexpected underscore | [`log`](samples/05_tables_simple_014/attempt_1_compile.log) |
| `05_tables_simple_014` | `05_tables_simple` | 2 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/05_tables_simple_014/attempt_2_compile.log) |
| `05_tables_simple_015` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unexpected hat | [`log`](samples/05_tables_simple_015/attempt_1_compile.log) |
| `05_tables_simple_017` | `05_tables_simple` | 1 | `math_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/05_tables_simple_017/attempt_1_compile.log) |
| `05_tables_simple_017` | `05_tables_simple` | 2 | `math_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/05_tables_simple_017/attempt_2_compile.log) |
| `05_tables_simple_018` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unexpected keys "top" and "bottom", valid keys are "paint", "thickness", "cap", "join", "dash", and "miter-limit" | [`log`](samples/05_tables_simple_018/attempt_1_compile.log) |
| `05_tables_simple_018` | `05_tables_simple` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: igma | [`log`](samples/05_tables_simple_018/attempt_2_compile.log) |
| `05_tables_simple_025` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/05_tables_simple_025/attempt_1_compile.log) |
| `05_tables_simple_027` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_027/attempt_1_compile.log) |
| `05_tables_simple_027` | `05_tables_simple` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_027/attempt_2_compile.log) |
| `05_tables_simple_028` | `05_tables_simple` | 1 | `reference_or_label` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_028/attempt_1_compile.log) |
| `05_tables_simple_028` | `05_tables_simple` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/05_tables_simple_028/attempt_2_compile.log) |
| `06_tables_moderate_007` | `06_tables_moderate` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: idetilde | [`log`](samples/06_tables_moderate_007/attempt_1_compile.log) |
| `06_tables_moderate_012` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_012/attempt_1_compile.log) |
| `06_tables_moderate_012` | `06_tables_moderate` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: elta | [`log`](samples/06_tables_moderate_012/attempt_2_compile.log) |
| `06_tables_moderate_013` | `06_tables_moderate` | 1 | `other_compile_error` | `repaired` | error: cannot multiply integer with auto | [`log`](samples/06_tables_moderate_013/attempt_1_compile.log) |
| `06_tables_moderate_014` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_014/attempt_1_compile.log) |
| `06_tables_moderate_014` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_014/attempt_2_compile.log) |
| `06_tables_moderate_015` | `06_tables_moderate` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_015/attempt_1_compile.log) |
| `06_tables_moderate_017` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_017/attempt_1_compile.log) |
| `06_tables_moderate_017` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_017/attempt_2_compile.log) |
| `06_tables_moderate_019` | `06_tables_moderate` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: ho | [`log`](samples/06_tables_moderate_019/attempt_1_compile.log) |
| `06_tables_moderate_019` | `06_tables_moderate` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: cm | [`log`](samples/06_tables_moderate_019/attempt_2_compile.log) |
| `06_tables_moderate_029` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_029/attempt_1_compile.log) |
| `06_tables_moderate_029` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_029/attempt_2_compile.log) |
| `06_tables_moderate_030` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_030/attempt_1_compile.log) |
| `06_tables_moderate_030` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_030/attempt_2_compile.log) |
| `06_tables_moderate_031` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: expected auto, relative length, or fraction, found integer | [`log`](samples/06_tables_moderate_031/attempt_1_compile.log) |
| `06_tables_moderate_031` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_031/attempt_2_compile.log) |
| `06_tables_moderate_033` | `06_tables_moderate` | 1 | `other_compile_error` | `final_failure` | error: unknown symbol modifier | [`log`](samples/06_tables_moderate_033/attempt_1_compile.log) |
| `06_tables_moderate_033` | `06_tables_moderate` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: up | [`log`](samples/06_tables_moderate_033/attempt_2_compile.log) |
| `07_figures_captions_006` | `07_figures_captions` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: ma | [`log`](samples/07_figures_captions_006/attempt_1_compile.log) |
| `07_figures_captions_006` | `07_figures_captions` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: circ | [`log`](samples/07_figures_captions_006/attempt_2_compile.log) |
| `07_figures_captions_008` | `07_figures_captions` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: an | [`log`](samples/07_figures_captions_008/attempt_1_compile.log) |
| `07_figures_captions_012` | `07_figures_captions` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: athcal | [`log`](samples/07_figures_captions_012/attempt_1_compile.log) |
| `08_crossrefs_citations_002` | `08_crossrefs_citations` | 1 | `reference_or_label` | `final_failure` | error: unclosed label | [`log`](samples/08_crossrefs_citations_002/attempt_1_compile.log) |
| `08_crossrefs_citations_002` | `08_crossrefs_citations` | 2 | `reference_or_label` | `final_failure` | error: cannot reference heading without numbering | [`log`](samples/08_crossrefs_citations_002/attempt_2_compile.log) |
| `08_crossrefs_citations_003` | `08_crossrefs_citations` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: sl | [`log`](samples/08_crossrefs_citations_003/attempt_1_compile.log) |
| `08_crossrefs_citations_003` | `08_crossrefs_citations` | 2 | `reference_or_label` | `final_failure` | error: cannot reference heading without numbering | [`log`](samples/08_crossrefs_citations_003/attempt_2_compile.log) |
| `08_crossrefs_citations_005` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference equation without numbering | [`log`](samples/08_crossrefs_citations_005/attempt_1_compile.log) |
| `08_crossrefs_citations_006` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference equation without numbering | [`log`](samples/08_crossrefs_citations_006/attempt_1_compile.log) |
| `08_crossrefs_citations_007` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference heading without numbering | [`log`](samples/08_crossrefs_citations_007/attempt_1_compile.log) |
| `08_crossrefs_citations_009` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference heading without numbering | [`log`](samples/08_crossrefs_citations_009/attempt_1_compile.log) |
| `08_crossrefs_citations_010` | `08_crossrefs_citations` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: aff | [`log`](samples/08_crossrefs_citations_010/attempt_1_compile.log) |
| `08_crossrefs_citations_010` | `08_crossrefs_citations` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: su | [`log`](samples/08_crossrefs_citations_010/attempt_2_compile.log) |
| `08_crossrefs_citations_011` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference heading without numbering | [`log`](samples/08_crossrefs_citations_011/attempt_1_compile.log) |
| `08_crossrefs_citations_014` | `08_crossrefs_citations` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/08_crossrefs_citations_014/attempt_1_compile.log) |
| `08_crossrefs_citations_014` | `08_crossrefs_citations` | 2 | `reference_or_label` | `final_failure` | error: cannot reference equation without numbering | [`log`](samples/08_crossrefs_citations_014/attempt_2_compile.log) |
| `08_crossrefs_citations_015` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference equation without numbering | [`log`](samples/08_crossrefs_citations_015/attempt_1_compile.log) |
| `09_algorithms_001` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_001/attempt_1_compile.log) |
| `09_algorithms_001` | `09_algorithms` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_001/attempt_2_compile.log) |
| `09_algorithms_008` | `09_algorithms` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: Ord | [`log`](samples/09_algorithms_008/attempt_1_compile.log) |
| `09_algorithms_009` | `09_algorithms` | 1 | `reference_or_label` | `repaired` | error: label `<Outer_Loop:eq>` does not exist in the document | [`log`](samples/09_algorithms_009/attempt_1_compile.log) |
| `09_algorithms_017` | `09_algorithms` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: Min | [`log`](samples/09_algorithms_017/attempt_1_compile.log) |
| `09_algorithms_017` | `09_algorithms` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: append | [`log`](samples/09_algorithms_017/attempt_2_compile.log) |
| `09_algorithms_018` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_018/attempt_1_compile.log) |
| `09_algorithms_018` | `09_algorithms` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: uu | [`log`](samples/09_algorithms_018/attempt_2_compile.log) |
| `10_compact_papers_001` | `10_compact_papers` | 1 | `general_syntax` | `repaired` | error: expected expression | [`log`](samples/10_compact_papers_001/attempt_1_compile.log) |
| `10_compact_papers_002` | `10_compact_papers` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: riangle | [`log`](samples/10_compact_papers_002/attempt_1_compile.log) |
| `10_compact_papers_004` | `10_compact_papers` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: math | [`log`](samples/10_compact_papers_004/attempt_1_compile.log) |
| `10_compact_papers_005` | `10_compact_papers` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: um | [`log`](samples/10_compact_papers_005/attempt_1_compile.log) |
| `10_compact_papers_005` | `10_compact_papers` | 2 | `reference_or_label` | `final_failure` | error: cannot reference equation without numbering | [`log`](samples/10_compact_papers_005/attempt_2_compile.log) |
| `10_compact_papers_006` | `10_compact_papers` | 1 | `general_syntax` | `final_failure` | error: expected expression | [`log`](samples/10_compact_papers_006/attempt_1_compile.log) |
| `10_compact_papers_006` | `10_compact_papers` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: SU | [`log`](samples/10_compact_papers_006/attempt_2_compile.log) |
| `10_compact_papers_011` | `10_compact_papers` | 1 | `math_syntax` | `final_failure` | error: invalid number suffix: B | [`log`](samples/10_compact_papers_011/attempt_1_compile.log) |
| `10_compact_papers_011` | `10_compact_papers` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: SL | [`log`](samples/10_compact_papers_011/attempt_2_compile.log) |
| `10_compact_papers_012` | `10_compact_papers` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: hi | [`log`](samples/10_compact_papers_012/attempt_1_compile.log) |

## Infrastructure failures

No API, provider, or local runner failures have been recorded.

## Compiler warnings

| Warning | Occurrences |
|---|---:|
| `angle.l` is deprecated, use `chevron.l` instead | 25 |
| `angle.r` is deprecated, use `chevron.r` instead | 24 |
| unknown font family: monospace | 2 |
| unknown font family: consolas | 1 |
