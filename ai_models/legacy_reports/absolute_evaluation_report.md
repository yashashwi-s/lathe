# Absolute Scoring Evaluation Report

This report evaluates AI models and Deterministic Engines strictly on the V2 Absolute Scoring Rubric.
Scoring was conducted heuristically directly on the `.typ` source mappings versus the original LaTeX reference.

## AI Models Evaluation
| Candidate | Sample | Status | Compiles | Retries | Clean Source | Text Complete | Structs | Num Correct | Font | Alignment | Typography | Score (x/6) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini | tables_complex_easy | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | tables_complex_easy | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gemini | algorithms_medium | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | algorithms_medium | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ❌ | 5/6 |  |
| gemini | eq_hard_hard | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | eq_hard_hard | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gemini | tables_complex_hard | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | tables_complex_hard | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gemini | prose_easy | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | prose_easy | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gemini | algorithms_easy | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | algorithms_easy | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gemini | eq_simple_hard | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | eq_simple_hard | ran | ✅ | 1 | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| gemini | prose_hard | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| gpt | prose_hard | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
**Average Binary Score:** 5.88 / 6.0
**Not Run / Missing Count:** 0

## Deterministic Engines Evaluation
| Candidate | Sample | Status | Compiles | Retries | Clean Source | Text Complete | Structs | Num Correct | Font | Alignment | Typography | Score (x/6) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pandoc | algorithms_easy | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/2 matched).  |
| tylax | algorithms_easy | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ❌ | 4/6 |  |
| typetex | algorithms_easy | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | algorithms_medium | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/1 matched).  |
| tylax | algorithms_medium | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ❌ | 4/6 |  |
| typetex | algorithms_medium | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | cv_complex_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | cv_complex_easy | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | cv_complex_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | cv_complex_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tylax | cv_complex_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | cv_complex_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| pandoc | cv_complex_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tylax | cv_complex_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | cv_complex_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| pandoc | beamer_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | beamer_easy | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | beamer_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | beamer_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | beamer_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | beamer_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | beamer_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | beamer_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | beamer_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | pgfplots_easy | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/4 matched).  |
| tylax | pgfplots_easy | ran | ✅ | N/A | ❌ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (0/4 matched).  |
| typetex | pgfplots_easy | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/4 matched).  |
| pandoc | pgfplots_hard | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/11 matched).  |
| tylax | pgfplots_hard | ran | ✅ | N/A | ❌ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (0/11 matched).  |
| typetex | pgfplots_hard | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/11 matched).  |
| pandoc | pgfplots_medium | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/8 matched).  |
| tylax | pgfplots_medium | ran | ✅ | N/A | ❌ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (0/8 matched).  |
| typetex | pgfplots_medium | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/8 matched).  |
| pandoc | cv_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | cv_simple_easy | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | cv_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | cv_simple_hard | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | cv_simple_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | cv_simple_hard | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | cv_simple_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tylax | cv_simple_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | cv_simple_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| pandoc | tables_complex_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tables_complex_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | tables_complex_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | tables_complex_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tables_complex_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | tables_complex_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | tables_complex_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tables_complex_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | tables_complex_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | tables_complex_attention_table1 | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tables_complex_attention_table1 | ran | ✅ | N/A | ✅ | ❌ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (0/13 matched).  |
| typetex | tables_complex_attention_table1 | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | tables_complex_attention_table2 | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (9/19 matched).  |
| tylax | tables_complex_attention_table2 | ran | ✅ | N/A | ✅ | ❌ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (1/19 matched).  |
| typetex | tables_complex_attention_table2 | ran | ✅ | N/A | ❌ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (10/19 matched).  |
| pandoc | paper_full_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | paper_full_easy | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| typetex | paper_full_easy | ran | ✅ | N/A | ❌ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 4/6 |  |
| pandoc | paper_full_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tylax | paper_full_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | paper_full_hard | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| pandoc | paper_full_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tylax | paper_full_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | paper_full_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| pandoc | tikz_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tikz_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | tikz_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | tikz_simple_hard | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/7 matched).  |
| tylax | tikz_simple_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | tikz_simple_hard | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/7 matched).  |
| pandoc | tikz_simple_medium | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/2 matched).  |
| tylax | tikz_simple_medium | ran | ✅ | N/A | ❌ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (1/2 matched).  |
| typetex | tikz_simple_medium | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/2 matched).  |
| pandoc | eq_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | eq_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | eq_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | eq_simple_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | eq_simple_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | eq_simple_hard | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| pandoc | eq_simple_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | eq_simple_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | eq_simple_medium | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| pandoc | posters_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | posters_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | posters_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | posters_hard | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | posters_hard | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| typetex | posters_hard | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | posters_medium | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | posters_medium | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| typetex | posters_medium | ran | ✅ | N/A | ✅ | ✅ | ❌ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | eq_hard_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | eq_hard_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | eq_hard_easy | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| pandoc | eq_hard_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | eq_hard_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | eq_hard_hard | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| pandoc | eq_hard_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | eq_hard_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | eq_hard_medium | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| pandoc | eq_hard_attention_eq1 | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | eq_hard_attention_eq1 | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | eq_hard_attention_eq1 | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| pandoc | paper_small_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | paper_small_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | paper_small_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | paper_small_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | paper_small_hard | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| typetex | paper_small_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | paper_small_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | paper_small_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | paper_small_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | prose_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | prose_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | prose_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | prose_attention_prose1 | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | prose_attention_prose1 | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | prose_attention_prose1 | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | prose_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tylax | prose_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | prose_hard | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| pandoc | prose_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| tylax | prose_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | prose_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| pandoc | tikz_complex_easy | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/10 matched).  |
| tylax | tikz_complex_easy | ran | ✅ | N/A | ❌ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 4/6 | Missing text overlap (2/10 matched).  |
| typetex | tikz_complex_easy | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/10 matched).  |
| pandoc | tikz_complex_hard | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/3 matched).  |
| tylax | tikz_complex_hard | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/3 matched).  |
| typetex | tikz_complex_hard | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/3 matched).  |
| pandoc | tikz_complex_medium | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/19 matched).  |
| tylax | tikz_complex_medium | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| typetex | tikz_complex_medium | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/19 matched).  |
| pandoc | tables_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tables_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | tables_simple_easy | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | tables_simple_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tables_simple_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | tables_simple_hard | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| pandoc | tables_simple_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tylax | tables_simple_medium | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| typetex | tables_simple_medium | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
*(Engine average score scoped strictly to the 8 segments the AI models were tested on)*
**Average Binary Score:** 5.05 / 6.0
**Not Run / Missing Count:** 7
