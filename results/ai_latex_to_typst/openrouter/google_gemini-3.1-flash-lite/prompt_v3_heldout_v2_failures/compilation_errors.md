# Compilation errors

This report includes every failed Typst compilation attempt, including
attempts later repaired by the model. API and local infrastructure failures
are reported separately and do not count as model compilation failures.

- Failed compilation attempts: 6
- Repaired failed attempts: 4
- Samples with final compilation failure: 1
- Compiler warning occurrences: 0
- Infrastructure failures: 0

## Error classes

| Error class | Failed attempts |
|---|---:|
| `general_syntax` | 3 |
| `math_syntax` | 1 |
| `reference_or_label` | 1 |
| `unknown_symbol_or_function` | 1 |

## Compilation attempts

| Sample | Category | Attempt | Error class | Result | Error | Log |
|---|---|---:|---|---|---|---|
| `06_tables_moderate_029` | `06_tables_moderate` | 1 | `general_syntax` | `repaired` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_029/attempt_1_compile.log) |
| `06_tables_moderate_030` | `06_tables_moderate` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_030/attempt_1_compile.log) |
| `06_tables_moderate_030` | `06_tables_moderate` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/06_tables_moderate_030/attempt_2_compile.log) |
| `06_tables_moderate_033` | `06_tables_moderate` | 1 | `reference_or_label` | `repaired` | error: label `<20>` does not exist in the document | [`log`](samples/06_tables_moderate_033/attempt_1_compile.log) |
| `10_compact_papers_006` | `10_compact_papers` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: SU | [`log`](samples/10_compact_papers_006/attempt_1_compile.log) |
| `10_compact_papers_011` | `10_compact_papers` | 1 | `math_syntax` | `repaired` | error: invalid number suffix: B | [`log`](samples/10_compact_papers_011/attempt_1_compile.log) |

## Infrastructure failures

No API, provider, or local runner failures have been recorded.

## Compiler warnings

No compiler warnings have been recorded.
