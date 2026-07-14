# Model and engine comparison documents

## Files

- `full_157_ai_engine_comparison_grid.pdf`: 169-page corpus-wide visual review
  document containing a cover, one divider per category, and one comparison
  page for every accepted sample. It combines the 30 prompt-development and
  127 held-out outputs without treating the development subset as held-out.
- `full_157_ai_engine_comparison_manifest.csv`: one row per accepted sample
  recording the source split, selected AI stage, compile statuses, and exact
  page location in the full report.
- `heldout_v1_v2_v3_cascade_engine_comparison_grid.pdf`: 139-page held-out
  review document containing a cover, one divider per category, and one
  comparison page for each of the 127 clean held-out samples.
- `heldout_v1_v2_v3_cascade_manifest.csv`: one row per held-out sample recording
  the selected AI stage, compile status, page counts, and deterministic-engine
  statuses used in the PDF.
- `heldout_cascade_analysis.md`: summary of v1, v2, and v3 cascade results,
  remaining failures, costs, and category-level outcomes.
- `prompt_clean_v0_v1_v3_engine_comparison_grid.pdf`: 42-page review document
  containing a cover, one divider for each of the 11 categories, and one
  comparison page for each of the 30 clean prompt-development samples.
- `prompt_clean_v0_v1_v3_engine_comparison_manifest.csv`: one row per sample recording
  the AI prompt source, compile status, page counts, and deterministic-engine
  statuses used in the PDF.

## Grid layout

Each sample page shows the complete available PDFs in a fixed 2-by-3 grid:

1. pdfLaTeX reference
2. Gemini 3.1 Flash Lite output
3. status and source provenance
4. Pandoc output
5. Tylax output
6. TypeTeX output

Every page of a multi-page PDF is tiled inside its cell. Failed conversions are
kept as labeled failure cells rather than omitted.

## AI selection policy

For the held-out cascade, prompt v1 ran on all 127 clean held-out samples. Prompt
v2 ran only on the 50 v1 final failures. Prompt v3 ran only on the 11 v2 final
failures. The final selected AI cell uses the earliest successful stage; the one
remaining final failure is shown as a labeled failure cell.

For the prompt-development grid:

The 22 clean samples that compiled under prompt v0 use their v0 output. Six of
the clean filtered v0 failures use the targeted prompt-v1 retry result. The two
remaining prompt-development failures use the targeted prompt-v3 rescue result.
This gives 30 compiled AI PDFs across the 30 clean development samples, but it
is not a held-out result: later prompts were written after examining earlier
failures and were run only on those failures.

Regenerate with:

```bash
mamba run -n lathe python scripts/ai/build_model_engine_grid.py
mamba run -n lathe python scripts/ai/build_heldout_cascade_reports.py
mamba run -n lathe python scripts/ai/build_full_corpus_comparison.py
```
