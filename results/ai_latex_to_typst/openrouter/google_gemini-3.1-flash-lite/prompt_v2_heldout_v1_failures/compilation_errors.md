# Compilation errors

This report includes every failed Typst compilation attempt, including
attempts later repaired by the model. API and local infrastructure failures
are reported separately and do not count as model compilation failures.

- Failed compilation attempts: 44
- Repaired failed attempts: 22
- Samples with final compilation failure: 11
- Compiler warning occurrences: 6
- Infrastructure failures: 0

## Error classes

| Error class | Failed attempts |
|---|---:|
| `general_syntax` | 23 |
| `math_syntax` | 3 |
| `reference_or_label` | 3 |
| `unknown_symbol_or_function` | 15 |

## Compilation attempts

| Sample | Category | Attempt | Error class | Result | Error | Log |
|---|---|---:|---|---|---|---|
| `01_prose_sections_002` | `01_prose_sections` | 1 | `reference_or_label` | `repaired` | error: label `<t>` does not exist in the document | [`log`](samples/01_prose_sections_002/attempt_1_compile.log) |
| `03_math_inline_display_001` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: paragraph | [`log`](samples/03_math_inline_display_001/attempt_1_compile.log) |
| `03_math_inline_display_002` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: langle | [`log`](samples/03_math_inline_display_002/attempt_1_compile.log) |
| `03_math_inline_display_012` | `03_math_inline_display` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: dt | [`log`](samples/03_math_inline_display_012/attempt_1_compile.log) |
| `04_math_aligned_001` | `04_math_aligned` | 1 | `math_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/04_math_aligned_001/attempt_1_compile.log) |
| `04_math_aligned_007` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: paragraph | [`log`](samples/04_math_aligned_007/attempt_1_compile.log) |
| `04_math_aligned_007` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: amma | [`log`](samples/04_math_aligned_007/attempt_2_compile.log) |
| `04_math_aligned_009` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: paragraph | [`log`](samples/04_math_aligned_009/attempt_1_compile.log) |
| `04_math_aligned_015` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: paragraph | [`log`](samples/04_math_aligned_015/attempt_1_compile.log) |
| `05_tables_simple_001` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_001/attempt_1_compile.log) |
| `05_tables_simple_001` | `05_tables_simple` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_001/attempt_2_compile.log) |
| `05_tables_simple_002` | `05_tables_simple` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: qrt | [`log`](samples/05_tables_simple_002/attempt_1_compile.log) |
| `05_tables_simple_006` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unexpected hat | [`log`](samples/05_tables_simple_006/attempt_1_compile.log) |
| `05_tables_simple_007` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unexpected hat | [`log`](samples/05_tables_simple_007/attempt_1_compile.log) |
| `05_tables_simple_011` | `05_tables_simple` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: elta | [`log`](samples/05_tables_simple_011/attempt_1_compile.log) |
| `05_tables_simple_014` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unexpected underscore | [`log`](samples/05_tables_simple_014/attempt_1_compile.log) |
| `05_tables_simple_017` | `05_tables_simple` | 1 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/05_tables_simple_017/attempt_1_compile.log) |
| `05_tables_simple_017` | `05_tables_simple` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_017/attempt_2_compile.log) |
| `05_tables_simple_018` | `05_tables_simple` | 1 | `math_syntax` | `final_failure` | error: expected identifier | [`log`](samples/05_tables_simple_018/attempt_1_compile.log) |
| `05_tables_simple_018` | `05_tables_simple` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/05_tables_simple_018/attempt_2_compile.log) |
| `05_tables_simple_027` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/05_tables_simple_027/attempt_1_compile.log) |
| `05_tables_simple_028` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/05_tables_simple_028/attempt_1_compile.log) |
| `06_tables_moderate_012` | `06_tables_moderate` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: elta | [`log`](samples/06_tables_moderate_012/attempt_1_compile.log) |
| `06_tables_moderate_014` | `06_tables_moderate` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_014/attempt_1_compile.log) |
| `06_tables_moderate_017` | `06_tables_moderate` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_017/attempt_1_compile.log) |
| `06_tables_moderate_019` | `06_tables_moderate` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: ho | [`log`](samples/06_tables_moderate_019/attempt_1_compile.log) |
| `06_tables_moderate_029` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_029/attempt_1_compile.log) |
| `06_tables_moderate_029` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_029/attempt_2_compile.log) |
| `06_tables_moderate_030` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_030/attempt_1_compile.log) |
| `06_tables_moderate_030` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_030/attempt_2_compile.log) |
| `06_tables_moderate_031` | `06_tables_moderate` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_031/attempt_1_compile.log) |
| `06_tables_moderate_033` | `06_tables_moderate` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: parrow | [`log`](samples/06_tables_moderate_033/attempt_1_compile.log) |
| `06_tables_moderate_033` | `06_tables_moderate` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: igma | [`log`](samples/06_tables_moderate_033/attempt_2_compile.log) |
| `07_figures_captions_006` | `07_figures_captions` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: ma | [`log`](samples/07_figures_captions_006/attempt_1_compile.log) |
| `08_crossrefs_citations_003` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: label `<eq:source-demo>` does not exist in the document | [`log`](samples/08_crossrefs_citations_003/attempt_1_compile.log) |
| `08_crossrefs_citations_010` | `08_crossrefs_citations` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/08_crossrefs_citations_010/attempt_1_compile.log) |
| `08_crossrefs_citations_010` | `08_crossrefs_citations` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/08_crossrefs_citations_010/attempt_2_compile.log) |
| `09_algorithms_001` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_001/attempt_1_compile.log) |
| `09_algorithms_001` | `09_algorithms` | 2 | `reference_or_label` | `final_failure` | error: unclosed label | [`log`](samples/09_algorithms_001/attempt_2_compile.log) |
| `09_algorithms_017` | `09_algorithms` | 1 | `general_syntax` | `repaired` | error: expected expression | [`log`](samples/09_algorithms_017/attempt_1_compile.log) |
| `10_compact_papers_006` | `10_compact_papers` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: SU | [`log`](samples/10_compact_papers_006/attempt_1_compile.log) |
| `10_compact_papers_006` | `10_compact_papers` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/10_compact_papers_006/attempt_2_compile.log) |
| `10_compact_papers_011` | `10_compact_papers` | 1 | `math_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/10_compact_papers_011/attempt_1_compile.log) |
| `10_compact_papers_011` | `10_compact_papers` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/10_compact_papers_011/attempt_2_compile.log) |

## Infrastructure failures

No API, provider, or local runner failures have been recorded.

## Compiler warnings

| Warning | Occurrences |
|---|---:|
| `angle.l` is deprecated, use `chevron.l` instead | 3 |
| `angle.r` is deprecated, use `chevron.r` instead | 3 |
