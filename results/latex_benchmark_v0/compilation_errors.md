# Engine Compilation Errors

Dataset: `data/latex_benchmark_v0`
Results: `results/latex_benchmark_v0`

## Pre/Post Patch Compile Counts

| Engine | Pre-patch compiled | Post-patch compiled | Total |
|---|---:|---:|---:|
| `pandoc` | 130 | 154 | 166 |
| `tylax` | 90 | 96 | 166 |
| `typetex` | 127 | 152 | 166 |

## General Patches Applied

- Added `#set heading(numbering: "1.")` and `#set math.equation(numbering: "1.")` to converter outputs so Pandoc-style heading/equation references can compile.
- Replaced unresolved Pandoc `@key` references/citations with visible plain text `[key]` when no matching Typst label exists.
- In the TypeTeX approximation filter, stripped `\label{...}` inside math and normalized common LaTeX math wrappers before passing math to MiTeX.
- Normalized MiTeX-hostile math macros `\d` and `\slash` to more portable forms.

## Why TypeTeX Can Fail More Than Pandoc

TypeTeX here is not a full independent engine; it is Pandoc plus a Lua filter that routes math through MiTeX. That makes text/layout mostly Pandoc-like, but math becomes stricter: formulas that Pandoc can lower into approximate Typst math may fail if MiTeX rejects a LaTeX macro such as `\slash`, `\d`, or other package-specific notation. After the general patches, TypeTeX is close to Pandoc but still fails on unsupported MiTeX math cases.

## Remaining Failures By Engine

### `pandoc`

Remaining compile failures: 12

| Error class | Count |
|---|---:|
| `typst_syntax` | 8 |
| `typst_reference_or_label` | 4 |

| Sample | Category | Class | First error |
|---|---|---|---|
| `04_math_aligned_008` | `04_math_aligned` | `typst_reference_or_label` | error: unknown variable: alphazws |
| `04_math_aligned_012` | `04_math_aligned` | `typst_reference_or_label` | error: unknown variable: mpsi |
| `04_math_aligned_015` | `04_math_aligned` | `typst_reference_or_label` | error: unknown variable: sd |
| `09_algorithms_008` | `09_algorithms` | `typst_reference_or_label` | error: unknown variable: horizontalrule |
| `10_compact_papers_003` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_007` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_013` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_014` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_015` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `01_prose_sections_002` | `01_prose_sections` | `typst_syntax` | error: unexpected closing bracket |
| `01_prose_sections_005` | `01_prose_sections` | `typst_syntax` | error: unexpected closing bracket |
| `01_prose_sections_015` | `01_prose_sections` | `typst_syntax` | error: unexpected closing bracket |

### `tylax`

Remaining compile failures: 70

| Error class | Count |
|---|---:|
| `other_typst_compile_error` | 30 |
| `typst_syntax` | 20 |
| `typst_reference_or_label` | 20 |

| Sample | Category | Class | First error |
|---|---|---|---|
| `03_math_inline_display_001` | `03_math_inline_display` | `typst_syntax` | error: unexpected underscore |
| `03_math_inline_display_002` | `03_math_inline_display` | `typst_syntax` | error: unexpected hat |
| `03_math_inline_display_003` | `03_math_inline_display` | `typst_reference_or_label` | error: unknown variable: chifrac |
| `03_math_inline_display_004` | `03_math_inline_display` | `other_typst_compile_error` | error: missing argument: denom |
| `03_math_inline_display_005` | `03_math_inline_display` | `typst_syntax` | error: unexpected slash |
| `03_math_inline_display_006` | `03_math_inline_display` | `other_typst_compile_error` | error: missing argument: denom |
| `03_math_inline_display_008` | `03_math_inline_display` | `other_typst_compile_error` | error: unclosed delimiter |
| `03_math_inline_display_009` | `03_math_inline_display` | `typst_syntax` | error: expected expression |
| `03_math_inline_display_010` | `03_math_inline_display` | `typst_reference_or_label` | error: unknown variable: overrightarrow |
| `03_math_inline_display_011` | `03_math_inline_display` | `typst_syntax` | error: unexpected underscore |
| `03_math_inline_display_012` | `03_math_inline_display` | `typst_syntax` | error: expected content, found array |
| `03_math_inline_display_013` | `03_math_inline_display` | `typst_reference_or_label` | error: unknown variable: rsum |
| `03_math_inline_display_014` | `03_math_inline_display` | `other_typst_compile_error` | error: unclosed delimiter |
| `03_math_inline_display_015` | `03_math_inline_display` | `typst_syntax` | error: unexpected hat |
| `03_math_inline_display_016` | `03_math_inline_display` | `typst_reference_or_label` | error: unknown variable: over |
| `03_math_inline_display_017` | `03_math_inline_display` | `typst_reference_or_label` | error: unknown variable: over |
| `03_math_inline_display_018` | `03_math_inline_display` | `typst_syntax` | error: unexpected underscore |
| `04_math_aligned_001` | `04_math_aligned` | `typst_syntax` | error: unexpected hat |
| `04_math_aligned_002` | `04_math_aligned` | `other_typst_compile_error` | error: unclosed delimiter |
| `04_math_aligned_003` | `04_math_aligned` | `other_typst_compile_error` | error: unclosed delimiter |
| `04_math_aligned_004` | `04_math_aligned` | `other_typst_compile_error` | error: unclosed delimiter |
| `04_math_aligned_005` | `04_math_aligned` | `other_typst_compile_error` | error: unclosed delimiter |
| `04_math_aligned_006` | `04_math_aligned` | `typst_reference_or_label` | error: unknown variable: rfrac |
| `04_math_aligned_007` | `04_math_aligned` | `typst_reference_or_label` | error: unknown variable: scriptstyle |
| `04_math_aligned_008` | `04_math_aligned` | `typst_syntax` | error: unexpected underscore |
| `04_math_aligned_009` | `04_math_aligned` | `typst_reference_or_label` | error: unknown variable: scriptstyle |
| `04_math_aligned_010` | `04_math_aligned` | `typst_syntax` | error: unexpected hat |
| `04_math_aligned_011` | `04_math_aligned` | `other_typst_compile_error` | error: missing argument: amount |
| `04_math_aligned_012` | `04_math_aligned` | `other_typst_compile_error` | error: unclosed delimiter |
| `04_math_aligned_013` | `04_math_aligned` | `typst_reference_or_label` | error: unknown variable: over |
| `04_math_aligned_014` | `04_math_aligned` | `other_typst_compile_error` | error: missing argument: denom |
| `04_math_aligned_015` | `04_math_aligned` | `typst_syntax` | error: unexpected underscore |
| `10_compact_papers_001` | `10_compact_papers` | `typst_syntax` | error: expected expression |
| `08_crossrefs_citations_001` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `10_compact_papers_003` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_008` | `10_compact_papers` | `other_typst_compile_error` | error: unclosed raw text |
| `10_compact_papers_013` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_014` | `10_compact_papers` | `other_typst_compile_error` | error: unclosed raw text |
| `08_crossrefs_citations_002` | `08_crossrefs_citations` | `typst_reference_or_label` | error: unclosed label |
| `08_crossrefs_citations_003` | `08_crossrefs_citations` | `typst_syntax` | error: unexpected underscore |
| `08_crossrefs_citations_004` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `01_prose_sections_005` | `01_prose_sections` | `typst_syntax` | error: unexpected closing bracket |
| `08_crossrefs_citations_005` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `08_crossrefs_citations_006` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `08_crossrefs_citations_007` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `01_prose_sections_010` | `01_prose_sections` | `typst_reference_or_label` | error: unknown variable: ws |
| `08_crossrefs_citations_008` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `08_crossrefs_citations_009` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `08_crossrefs_citations_010` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `02_lists_formatting_002` | `02_lists_formatting` | `typst_syntax` | error: expected colon |
| `08_crossrefs_citations_011` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `01_prose_sections_015` | `01_prose_sections` | `other_typst_compile_error` | error: unclosed raw text |
| `08_crossrefs_citations_012` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `08_crossrefs_citations_013` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `08_crossrefs_citations_014` | `08_crossrefs_citations` | `other_typst_compile_error` | error: unclosed delimiter |
| `08_crossrefs_citations_015` | `08_crossrefs_citations` | `other_typst_compile_error` | error: the document does not contain a bibliography |
| `02_lists_formatting_008` | `02_lists_formatting` | `other_typst_compile_error` | error: missing argument: radicand |
| `07_figures_captions_002` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `07_figures_captions_003` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `02_lists_formatting_018` | `02_lists_formatting` | `typst_syntax` | error: expected colon |
| `07_figures_captions_004` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `02_lists_formatting_020` | `02_lists_formatting` | `typst_syntax` | error: unexpected underscore |
| `02_lists_formatting_021` | `02_lists_formatting` | `typst_reference_or_label` | error: unknown variable: over |
| `07_figures_captions_006` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `07_figures_captions_007` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `07_figures_captions_009` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `07_figures_captions_011` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `07_figures_captions_012` | `07_figures_captions` | `typst_reference_or_label` | error: unknown variable: ws |
| `11_forms_cv_letters_001` | `11_forms_cv_letters` | `other_typst_compile_error` | error: unclosed delimiter |
| `11_forms_cv_letters_002` | `11_forms_cv_letters` | `other_typst_compile_error` | error: missing argument: amount |

### `typetex`

Remaining compile failures: 14

| Error class | Count |
|---|---:|
| `typst_syntax` | 8 |
| `mitex_math_macro` | 5 |
| `typst_reference_or_label` | 1 |

| Sample | Category | Class | First error |
|---|---|---|---|
| `03_math_inline_display_009` | `03_math_inline_display` | `mitex_math_macro` | error: plugin errored with: error: unknown command: \sp |
| `03_math_inline_display_017` | `03_math_inline_display` | `mitex_math_macro` | error: plugin errored with: error: unknown command: \sp |
| `04_math_aligned_002` | `04_math_aligned` | `mitex_math_macro` | error: plugin errored with: error: unknown command: \makebox |
| `04_math_aligned_005` | `04_math_aligned` | `mitex_math_macro` | error: plugin errored with: error: unknown command: \mbox |
| `04_math_aligned_009` | `04_math_aligned` | `mitex_math_macro` | error: plugin errored with: error: unknown command: \medskip |
| `09_algorithms_008` | `09_algorithms` | `typst_reference_or_label` | error: unknown variable: horizontalrule |
| `10_compact_papers_003` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_007` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_013` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_014` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `10_compact_papers_015` | `10_compact_papers` | `typst_syntax` | error: unexpected closing bracket |
| `01_prose_sections_002` | `01_prose_sections` | `typst_syntax` | error: unexpected closing bracket |
| `01_prose_sections_005` | `01_prose_sections` | `typst_syntax` | error: unexpected closing bracket |
| `01_prose_sections_015` | `01_prose_sections` | `typst_syntax` | error: unexpected closing bracket |

