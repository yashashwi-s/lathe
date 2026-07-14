# Compilation errors

This report includes every failed Typst compilation attempt, including
attempts later repaired by the model. API and local infrastructure failures
are reported separately and do not count as model compilation failures.

- Failed compilation attempts: 23
- Repaired failed attempts: 7
- Samples with final compilation failure: 8
- Compiler warning occurrences: 21
- Infrastructure failures: 0

## Error classes

| Error class | Failed attempts |
|---|---:|
| `general_syntax` | 11 |
| `math_syntax` | 2 |
| `reference_or_label` | 5 |
| `unknown_symbol_or_function` | 5 |

## Compilation attempts

| Sample | Category | Attempt | Error class | Result | Error | Log |
|---|---|---:|---|---|---|---|
| `02_lists_formatting_024` | `02_lists_formatting` | 1 | `general_syntax` | `final_failure` | error: expected content, found array | [`log`](samples/02_lists_formatting_024/attempt_1_compile.log) |
| `02_lists_formatting_024` | `02_lists_formatting` | 2 | `general_syntax` | `final_failure` | error: expected content, found array | [`log`](samples/02_lists_formatting_024/attempt_2_compile.log) |
| `02_lists_formatting_026` | `02_lists_formatting` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: su2 | [`log`](samples/02_lists_formatting_026/attempt_1_compile.log) |
| `03_math_inline_display_014` | `03_math_inline_display` | 1 | `math_syntax` | `final_failure` | error: unknown symbol modifier | [`log`](samples/03_math_inline_display_014/attempt_1_compile.log) |
| `03_math_inline_display_014` | `03_math_inline_display` | 2 | `math_syntax` | `final_failure` | error: unknown symbol modifier | [`log`](samples/03_math_inline_display_014/attempt_2_compile.log) |
| `04_math_aligned_012` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: widehat | [`log`](samples/04_math_aligned_012/attempt_1_compile.log) |
| `04_math_aligned_012` | `04_math_aligned` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: stack | [`log`](samples/04_math_aligned_012/attempt_2_compile.log) |
| `05_tables_simple_023` | `05_tables_simple` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/05_tables_simple_023/attempt_1_compile.log) |
| `06_tables_moderate_010` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/06_tables_moderate_010/attempt_1_compile.log) |
| `06_tables_moderate_010` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/06_tables_moderate_010/attempt_2_compile.log) |
| `07_figures_captions_001` | `07_figures_captions` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: Sp | [`log`](samples/07_figures_captions_001/attempt_1_compile.log) |
| `07_figures_captions_007` | `07_figures_captions` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: bigcirc | [`log`](samples/07_figures_captions_007/attempt_1_compile.log) |
| `08_crossrefs_citations_008` | `08_crossrefs_citations` | 1 | `reference_or_label` | `final_failure` | error: label `<Mart>` does not exist in the document | [`log`](samples/08_crossrefs_citations_008/attempt_1_compile.log) |
| `08_crossrefs_citations_008` | `08_crossrefs_citations` | 2 | `reference_or_label` | `final_failure` | error: label `<Mart>` does not exist in the document | [`log`](samples/08_crossrefs_citations_008/attempt_2_compile.log) |
| `08_crossrefs_citations_012` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference metadata | [`log`](samples/08_crossrefs_citations_012/attempt_1_compile.log) |
| `08_crossrefs_citations_013` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference text | [`log`](samples/08_crossrefs_citations_013/attempt_1_compile.log) |
| `09_algorithms_003` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_003/attempt_1_compile.log) |
| `09_algorithms_003` | `09_algorithms` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_003/attempt_2_compile.log) |
| `09_algorithms_005` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_005/attempt_1_compile.log) |
| `09_algorithms_005` | `09_algorithms` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_005/attempt_2_compile.log) |
| `09_algorithms_021` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_021/attempt_1_compile.log) |
| `09_algorithms_021` | `09_algorithms` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_021/attempt_2_compile.log) |
| `10_compact_papers_015` | `10_compact_papers` | 1 | `reference_or_label` | `repaired` | error: cannot reference equation without numbering | [`log`](samples/10_compact_papers_015/attempt_1_compile.log) |

## Infrastructure failures

No API, provider, or local runner failures have been recorded.

## Compiler warnings

| Warning | Occurrences |
|---|---:|
| unknown font family: linux libertine | 7 |
| `angle.l` is deprecated, use `chevron.l` instead | 4 |
| `angle.r` is deprecated, use `chevron.r` instead | 2 |
| label `<Mart>` is not attached to anything | 2 |
| label `<HosNak>` is not attached to anything | 2 |
| label `<Visser>` is not attached to anything | 2 |
| label `<HosNak2>` is not attached to anything | 2 |
