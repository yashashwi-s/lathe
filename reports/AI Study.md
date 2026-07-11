# AI Models Evaluation Results

With the manual human evaluation complete, we have computed the aggregated scores for the AI models: **Gemini** and **GPT**. 

## Scoring Methodology
Each model was scored out of a maximum of **1.0 point** per segment:
- **0.5 points** awarded for compilation success. For every compilation failure (retry), **0.1 points** were deducted from this baseline.
- **0.5 points** awarded for **1st place** visual layout.
- **0.25 points** awarded for **2nd place** visual layout.
- **0 points** awarded if the visual layout was ranked 0th (complete failure or "rubbish").

> [!WARNING]
> **Sample Size & Rater Caveat**
> The visual rankings (1st/2nd) came from human judgment by a single rater on a small exploratory subset of 8 complex segments. These results are for pipeline validation and qualitative signaling only, not definitive statistical evaluation.

## Aggregated Score Table

| Segment | Gemini Rank | Gemini Retries | **Gemini Score** | GPT Rank | GPT Retries | **GPT Score** |
|---------|-------------|----------------|------------------|----------|-------------|---------------|
| `algorithms_easy` | 1st | 1 | **0.90** | 2nd | 1 | 0.65 |
| `algorithms_medium` | 1st | 1 | **0.90** | 2nd | 1 | 0.65 |
| `eq_hard_hard` | 2nd | 0 | 0.75 | 1st | 0 | **1.00** |
| `eq_simple_hard` | 1st | 0 | **1.00** | 2nd | 1 | 0.65 |
| `prose_easy` | *0* | 0 | 0.50 | *0* | 0 | 0.50 |
| `prose_hard` | 1st | 0 | **1.00** | 2nd | 1 | 0.65 |
| `tables_complex_easy` | 2nd | 0 | 0.75 | 1st | 0 | **1.00** |
| `tables_complex_hard` | 1st | 0 | **1.00** | 2nd | 0 | 0.75 |
| **OVERALL AVERAGE** | | | **0.85** | | | **0.73** |

## Key Takeaways

### 1. Compilation Robustness
**Gemini** demonstrated superior syntax handling, achieving a zero-shot compile on 6 out of 8 segments. Its failures were isolated to algorithmic blocks where it struggled with variable binding rules (e.g., missing the `#` prefix for `#counter`).
**GPT** struggled significantly more with Typst's compiler, failing on 4 out of 8 segments. GPT often hallucinated macros (e.g. attempting to use `#equation[]` which does not exist) or failed to properly encapsulate variables.

### 2. Visual Quality
**Gemini** won 1st place in 5 segments, compared to GPT's 2 wins. Neither model was capable of perfectly formatting `prose_easy` (resulting in a 0 rank for both). GPT excelled at cleanly structuring complex tables and deep matrix equations, taking 1st place in `eq_hard_hard` and `tables_complex_easy`. 

### 3. Failure Taxonomy
When the models failed to compile, the errors were overwhelmingly related to:
- **Missing Variable Hashes:** (e.g., `$counter <- 0$` instead of `$#counter <- 0$`).
- **Hallucinated Blocks:** (e.g., `#equation[...]`).
- **Unescaped Syntax:** (e.g., mismatched delimiters or treating plain text as a reference `[sec:methodology]`).

These findings indicate that while LLMs are incredibly capable at predicting structural translations from LaTeX to Typst, they still require a robust, automated compiler feedback loop to fix minor syntax hallucinations before the output is usable.