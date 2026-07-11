# Full-Corpus Evaluation Report

## Summary Metrics

- **Fair-subset comparison (AI Models vs Engines)**: AI 5.06/6.0 vs Engines 5.05/6.0
- **Full-corpus engine average**: 4.71/6.0
- **Not-run count (Engines Full-corpus)**: 7

## Fair-Subset: AI Models & Deterministic Engines (8 segments)
| Sample | Candidate | Status | Compiles | Retries | Clean Source | Text Complete | Structs | Num Correct | Font | Alignment | Typography | Score (x/6) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| algorithms_easy | gemini | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| algorithms_easy | gpt | ran | ❌ | 1 | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. erro... |
| algorithms_easy | pandoc | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 | Missing text overlap (0/2 matched).  |
| algorithms_easy | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ❌ | 4/6 |  |
| algorithms_easy | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| algorithms_medium | gemini | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| algorithms_medium | gpt | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ❌ | 5/6 |  |
| algorithms_medium | pandoc | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 | Missing text overlap (0/1 matched).  |
| algorithms_medium | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ❌ | 4/6 |  |
| algorithms_medium | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| eq_hard_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_hard | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_hard | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | N/A | TypeTeX Lua filter crashes on equations (object... |
| eq_simple_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_simple_hard | gpt | ran | ✅ | 1 | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| eq_simple_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| eq_simple_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_simple_hard | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | N/A | TypeTeX Lua filter crashes on equations (object... |
| prose_easy | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| prose_easy | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | exact | ✅ | 6/6 |  |
| prose_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | exact | ✅ | 6/6 |  |
| prose_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | exact | ✅ | 6/6 |  |
| prose_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | exact | ✅ | 6/6 |  |
| prose_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ❌ | 5/6 |  |
| prose_hard | gpt | ran | ❌ | 1 | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. erro... |
| prose_hard | pandoc | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| prose_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| prose_hard | typetex | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tables_complex_easy | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_complex_easy | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_complex_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_complex_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_complex_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_complex_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_complex_hard | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_complex_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_complex_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_complex_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |

## Full-Corpus: Deterministic Engines (Remaining Segments)
| Sample | Candidate | Status | Compiles | Retries | Clean Source | Text Complete | Structs | Num Correct | Font | Alignment | Typography | Score (x/6) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| beamer_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| beamer_easy | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| beamer_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| beamer_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| beamer_medium | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| beamer_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_complex_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_complex_easy | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_complex_easy | tylax_patched | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| cv_complex_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_complex_hard | pandoc | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_complex_hard | pandoc_patched | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_complex_hard | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_complex_hard | tylax_patched | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| cv_complex_hard | typetex | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_complex_hard | typetex_patched | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_complex_medium | pandoc | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_complex_medium | pandoc_patched | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_complex_medium | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_complex_medium | tylax_patched | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| cv_complex_medium | typetex | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_complex_medium | typetex_patched | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_simple_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_simple_easy | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_simple_easy | tylax_patched | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_simple_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| cv_simple_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| cv_simple_hard | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_simple_hard | tylax_patched | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| cv_simple_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| cv_simple_medium | pandoc | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_simple_medium | pandoc_patched | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| cv_simple_medium | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_simple_medium | tylax_patched | ran | ✅ | N/A | ❌ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 4/6 |  |
| cv_simple_medium | typetex | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | explicitly declared | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. [Roo... |
| cv_simple_medium | typetex_patched | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| eq_hard_attention_eq1 | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| eq_hard_attention_eq1 | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_attention_eq1 | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | N/A | TypeTeX Lua filter crashes on equations (object... |
| eq_hard_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_easy | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | N/A | TypeTeX Lua filter crashes on equations (object... |
| eq_hard_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_hard_medium | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | N/A | TypeTeX Lua filter crashes on equations (object... |
| eq_simple_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| eq_simple_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| eq_simple_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| eq_simple_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| eq_simple_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| eq_simple_medium | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | N/A | TypeTeX Lua filter crashes on equations (object... |
| paper_full_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| paper_full_easy | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| paper_full_easy | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 4/6 |  |
| paper_full_hard | pandoc | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| paper_full_hard | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| paper_full_hard | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | N/A | Source file missing. |
| paper_full_medium | pandoc | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| paper_full_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| paper_full_medium | typetex | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| paper_small_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | minor | ✅ | 5/6 |  |
| paper_small_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| paper_small_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | minor | ✅ | 5/6 |  |
| paper_small_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| paper_small_hard | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| paper_small_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| paper_small_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | minor | ✅ | 5/6 |  |
| paper_small_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| paper_small_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | minor | ✅ | 5/6 |  |
| pgfplots_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| pgfplots_easy | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 4/5 |  |
| pgfplots_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| pgfplots_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| pgfplots_hard | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 4/5 |  |
| pgfplots_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| pgfplots_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| pgfplots_medium | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 4/5 |  |
| pgfplots_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| posters_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| posters_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| posters_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| posters_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| posters_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| posters_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| posters_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| posters_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| posters_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| prose_attention_prose1 | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| prose_attention_prose1 | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| prose_attention_prose1 | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 5/6 |  |
| prose_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| prose_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| prose_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | major | ✅ | 5/6 |  |
| tables_complex_attention_table1 | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_complex_attention_table1 | tylax | ran | ✅ | N/A | ✅ | ❌ | ❌ | ✅ | explicitly declared | content_mismatch | ✅ | 4/6 | Missing text overlap (0/13 matched).  |
| tables_complex_attention_table1 | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| tables_complex_attention_table2 | pandoc | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 | Missing text overlap (9/19 matched).  |
| tables_complex_attention_table2 | tylax | ran | ✅ | N/A | ✅ | ❌ | ❌ | ✅ | explicitly declared | minor | ✅ | 4/6 | Missing text overlap (1/19 matched).  |
| tables_complex_attention_table2 | typetex | ran | ✅ | N/A | ❌ | ❌ | ✅ | ✅ | explicitly declared | major | ✅ | 4/6 | Missing text overlap (10/19 matched).  |
| tables_complex_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_complex_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_complex_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | minor | ✅ | 6/6 |  |
| tables_simple_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | content_mismatch | ✅ | 6/6 |  |
| tables_simple_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | content_mismatch | ✅ | 6/6 |  |
| tables_simple_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | content_mismatch | ✅ | 6/6 |  |
| tables_simple_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_simple_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_simple_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_simple_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_simple_medium | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 6/6 |  |
| tables_simple_medium | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/6 |  |
| tikz_complex_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_complex_easy | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 4/5 |  |
| tikz_complex_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_complex_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_complex_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_complex_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_complex_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_complex_medium | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tikz_complex_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_simple_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_simple_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_simple_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_simple_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_simple_hard | tylax | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_applicable | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tikz_simple_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_simple_medium | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |
| tikz_simple_medium | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 4/5 |  |
| tikz_simple_medium | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | major | ✅ | 5/5 |  |