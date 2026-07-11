# Absolute Scoring Evaluation Report

This report evaluates AI models and Deterministic Engines strictly on the V2 Absolute Scoring Rubric.
Scoring was conducted heuristically directly on the `.typ` source mappings versus the original LaTeX reference.

## Combined Evaluation (AI Models & Deterministic Engines)
| Sample | Candidate | Status | Compiles | Retries | Clean Source | Text Complete | Structs | Num Correct | Font | Alignment | Typography | Score (x/6) | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| algorithms_easy | gemini | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| algorithms_easy | gpt | ran | ❌ | 1 | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. erro... |
| algorithms_easy | pandoc | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/2 matched).  |
| algorithms_easy | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ❌ | 4/6 |  |
| algorithms_easy | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| algorithms_medium | gemini | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| algorithms_medium | gpt | ran | ✅ | 1 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ❌ | 5/6 |  |
| algorithms_medium | pandoc | ran | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 | Missing text overlap (0/1 matched).  |
| algorithms_medium | tylax | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ❌ | 4/6 |  |
| algorithms_medium | typetex | ran | ✅ | N/A | ❌ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| eq_hard_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| eq_hard_hard | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| eq_hard_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| eq_hard_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| eq_hard_hard | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| eq_simple_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| eq_simple_hard | gpt | ran | ✅ | 1 | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| eq_simple_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ❌ | explicitly declared | not_implemented | ✅ | 5/6 |  |
| eq_simple_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| eq_simple_hard | typetex | not_run | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | N/A | Source file missing. |
| prose_easy | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| prose_easy | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| prose_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| prose_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| prose_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| prose_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| prose_hard | gpt | ran | ❌ | 1 | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. erro... |
| prose_hard | pandoc | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| prose_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| prose_hard | typetex | ran | ❌ | N/A | ❌ | ❌ | ❌ | ❌ | implicit default | not_implemented | ❌ | 0/6 | Does not compile. Rendered output missing. |
| tables_complex_easy | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_easy | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_easy | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_easy | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_easy | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_hard | gemini | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_hard | gpt | ran | ✅ | 0 | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_hard | pandoc | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_hard | tylax | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |
| tables_complex_hard | typetex | ran | ✅ | N/A | ✅ | ✅ | ✅ | ✅ | explicitly declared | not_implemented | ✅ | 6/6 |  |

**Average Binary Score (AI Models):** 5.12 / 6.0
**Average Binary Score (Engines):** 5.05 / 6.0
**Not Run / Missing Count (Engines):** 2