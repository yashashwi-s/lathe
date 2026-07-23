# Compilation errors

This report includes every failed Typst compilation attempt, including
attempts later repaired by the model. API and local infrastructure failures
are reported separately and do not count as model compilation failures.

- Failed compilation attempts: 46
- Repaired failed attempts: 8
- Samples with final compilation failure: 19
- Compiler warning occurrences: 41
- Infrastructure failures: 0

## Error classes

| Error class | Failed attempts |
|---|---:|
| `general_syntax` | 18 |
| `other_compile_error` | 5 |
| `reference_or_label` | 1 |
| `unknown_symbol_or_function` | 22 |

## Compilation attempts

| Sample | Category | Attempt | Error class | Result | Error | Log |
|---|---|---:|---|---|---|---|
| `arxiv5t_paper_002` | `arxiv5t_paper` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/arxiv5t_paper_002/attempt_1_compile.log) |
| `arxiv5t_paper_002` | `arxiv5t_paper` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: igma | [`log`](samples/arxiv5t_paper_002/attempt_2_compile.log) |
| `arxiv5t_paper_006` | `arxiv5t_paper` | 1 | `other_compile_error` | `final_failure` | error: file not found (searched at ./results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/expansion_32_claude_prompt_v1/samples/arxiv5t_paper_006/src/authors.tex) | [`log`](samples/arxiv5t_paper_006/attempt_1_compile.log) |
| `arxiv5t_paper_006` | `arxiv5t_paper` | 2 | `other_compile_error` | `final_failure` | error: file not found (searched at ./results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/expansion_32_claude_prompt_v1/samples/arxiv5t_paper_006/src/0-abstract.tex) | [`log`](samples/arxiv5t_paper_006/attempt_2_compile.log) |
| `arxiv5t_paper_019` | `arxiv5t_paper` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: otimes | [`log`](samples/arxiv5t_paper_019/attempt_1_compile.log) |
| `arxiv5t_paper_019` | `arxiv5t_paper` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: supp | [`log`](samples/arxiv5t_paper_019/attempt_2_compile.log) |
| `arxiv5t_paper_020` | `arxiv5t_paper` | 1 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/arxiv5t_paper_020/attempt_1_compile.log) |
| `arxiv5t_paper_020` | `arxiv5t_paper` | 2 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/arxiv5t_paper_020/attempt_2_compile.log) |
| `arxiv5t_paper_022` | `arxiv5t_paper` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/arxiv5t_paper_022/attempt_1_compile.log) |
| `arxiv5t_paper_022` | `arxiv5t_paper` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/arxiv5t_paper_022/attempt_2_compile.log) |
| `i2s_algorithm_001` | `i2s_algorithm` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/i2s_algorithm_001/attempt_1_compile.log) |
| `i2s_algorithm_001` | `i2s_algorithm` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: hspace | [`log`](samples/i2s_algorithm_001/attempt_2_compile.log) |
| `i2s_algorithm_003` | `i2s_algorithm` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: section | [`log`](samples/i2s_algorithm_003/attempt_1_compile.log) |
| `i2s_algorithm_005` | `i2s_algorithm` | 1 | `reference_or_label` | `final_failure` | error: unclosed delimiter | [`log`](samples/i2s_algorithm_005/attempt_1_compile.log) |
| `i2s_algorithm_005` | `i2s_algorithm` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/i2s_algorithm_005/attempt_2_compile.log) |
| `i2s_algorithm_008` | `i2s_algorithm` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: section | [`log`](samples/i2s_algorithm_008/attempt_1_compile.log) |
| `i2s_equation_003` | `i2s_equation` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: GNN | [`log`](samples/i2s_equation_003/attempt_1_compile.log) |
| `i2s_equation_004` | `i2s_equation` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/i2s_equation_004/attempt_1_compile.log) |
| `i2s_equation_004` | `i2s_equation` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/i2s_equation_004/attempt_2_compile.log) |
| `i2s_plot_001` | `i2s_plot` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/i2s_plot_001/attempt_1_compile.log) |
| `i2s_plot_001` | `i2s_plot` | 2 | `other_compile_error` | `final_failure` | error: panicked with: "Failed to resolve coordinate: (328.41, 104.55)" | [`log`](samples/i2s_plot_001/attempt_2_compile.log) |
| `i2s_plot_002` | `i2s_plot` | 1 | `general_syntax` | `repaired` | error: expected length or auto, found float | [`log`](samples/i2s_plot_002/attempt_1_compile.log) |
| `i2s_plot_003` | `i2s_plot` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: canvas | [`log`](samples/i2s_plot_003/attempt_1_compile.log) |
| `i2s_plot_003` | `i2s_plot` | 2 | `other_compile_error` | `final_failure` | error: panicked with: "Failed to resolve coordinate: (52.05, 101.79)" | [`log`](samples/i2s_plot_003/attempt_2_compile.log) |
| `i2s_plot_004` | `i2s_plot` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/i2s_plot_004/attempt_1_compile.log) |
| `i2s_plot_004` | `i2s_plot` | 2 | `general_syntax` | `final_failure` | error: expected relative length, found float | [`log`](samples/i2s_plot_004/attempt_2_compile.log) |
| `i2s_plot_005` | `i2s_plot` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/i2s_plot_005/attempt_1_compile.log) |
| `i2s_plot_005` | `i2s_plot` | 2 | `other_compile_error` | `final_failure` | error: panicked with: "Failed to resolve coordinate: (31.05, 33.189750000000004)" | [`log`](samples/i2s_plot_005/attempt_2_compile.log) |
| `i2s_table_002` | `i2s_table` | 1 | `general_syntax` | `final_failure` | error: unexpected dots | [`log`](samples/i2s_table_002/attempt_1_compile.log) |
| `i2s_table_002` | `i2s_table` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/i2s_table_002/attempt_2_compile.log) |
| `i2s_table_004` | `i2s_table` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/i2s_table_004/attempt_1_compile.log) |
| `i2s_table_004` | `i2s_table` | 2 | `general_syntax` | `final_failure` | error: unexpected argument: offset | [`log`](samples/i2s_table_004/attempt_2_compile.log) |
| `i2s_table_007` | `i2s_table` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: section | [`log`](samples/i2s_table_007/attempt_1_compile.log) |
| `i2s_table_008` | `i2s_table` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: section | [`log`](samples/i2s_table_008/attempt_1_compile.log) |
| `neurips_paper_029` | `neurips_paper` | 1 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/neurips_paper_029/attempt_1_compile.log) |
| `neurips_paper_029` | `neurips_paper` | 2 | `general_syntax` | `final_failure` | error: unexpected hat | [`log`](samples/neurips_paper_029/attempt_2_compile.log) |
| `neurips_paper_036` | `neurips_paper` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/neurips_paper_036/attempt_1_compile.log) |
| `neurips_paper_036` | `neurips_paper` | 2 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: SE | [`log`](samples/neurips_paper_036/attempt_2_compile.log) |
| `pubmed_table_001` | `pubmed_table` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: section | [`log`](samples/pubmed_table_001/attempt_1_compile.log) |
| `pubmed_table_002` | `pubmed_table` | 1 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/pubmed_table_002/attempt_1_compile.log) |
| `pubmed_table_002` | `pubmed_table` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/pubmed_table_002/attempt_2_compile.log) |
| `pubmed_table_003` | `pubmed_table` | 1 | `unknown_symbol_or_function` | `final_failure` | error: unknown variable: section | [`log`](samples/pubmed_table_003/attempt_1_compile.log) |
| `pubmed_table_003` | `pubmed_table` | 2 | `general_syntax` | `final_failure` | error: unexpected argument: rowspan | [`log`](samples/pubmed_table_003/attempt_2_compile.log) |
| `pubmed_table_004` | `pubmed_table` | 1 | `unknown_symbol_or_function` | `repaired` | error: unknown variable: section | [`log`](samples/pubmed_table_004/attempt_1_compile.log) |
| `pubmed_table_005` | `pubmed_table` | 1 | `general_syntax` | `final_failure` | error: unexpected dots | [`log`](samples/pubmed_table_005/attempt_1_compile.log) |
| `pubmed_table_005` | `pubmed_table` | 2 | `general_syntax` | `final_failure` | error: unclosed delimiter | [`log`](samples/pubmed_table_005/attempt_2_compile.log) |

## Infrastructure failures

No API, provider, or local runner failures have been recorded.

## Compiler warnings

| Warning | Occurrences |
|---|---:|
| unknown font family: serif | 10 |
| `angle.l` is deprecated, use `chevron.l` instead | 10 |
| `angle.r` is deprecated, use `chevron.r` instead | 9 |
| unknown font family: linux libertine | 7 |
| `times.circle` is deprecated, use `times.o` instead | 2 |
| unknown font family: linux libertine o | 2 |
| unknown font family: computer modern | 1 |
