# Compilation errors

This report includes every failed Typst compilation attempt, including
attempts later repaired by the model. API and local infrastructure failures
are reported separately and do not count as model compilation failures.

- Failed compilation attempts: 7
- Repaired failed attempts: 3
- Samples with final compilation failure: 2
- Compiler warning occurrences: 12
- Infrastructure failures: 0

## Error classes

| Error class | Failed attempts |
|---|---:|
| `general_syntax` | 4 |
| `reference_or_label` | 1 |
| `unknown_symbol_or_function` | 2 |

## Compilation attempts

| Sample | Category | Attempt | Error class | Result | Error | Log |
|---|---|---:|---|---|---|---|
| `02_lists_formatting_024` | `02_lists_formatting` | 1 | `general_syntax` | `repaired` | error: expected content, found array | [`log`](samples/02_lists_formatting_024/attempt_1_compile.log) |
| `04_math_aligned_012` | `04_math_aligned` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: section | [`log`](samples/04_math_aligned_012/attempt_1_compile.log) |
| `08_crossrefs_citations_008` | `08_crossrefs_citations` | 1 | `reference_or_label` | `repaired` | error: cannot reference equation without numbering | [`log`](samples/08_crossrefs_citations_008/attempt_1_compile.log) |
| `09_algorithms_005` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_005/attempt_1_compile.log) |
| `09_algorithms_005` | `09_algorithms` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_005/attempt_2_compile.log) |
| `09_algorithms_021` | `09_algorithms` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/09_algorithms_021/attempt_1_compile.log) |
| `09_algorithms_021` | `09_algorithms` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: GNN | [`log`](samples/09_algorithms_021/attempt_2_compile.log) |

## Infrastructure failures

No API, provider, or local runner failures have been recorded.

## Compiler warnings

| Warning | Occurrences |
|---|---:|
| `angle.l` is deprecated, use `chevron.l` instead | 6 |
| `angle.r` is deprecated, use `chevron.r` instead | 6 |
