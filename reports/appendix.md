# Appendix: Complete Dataset Visual Alignment

This appendix contains the compilation status and visual-alignment scores for every candidate on every sample, followed by side-by-side 2x2 grids comparing the structural rendering of the three deterministic engines (Pandoc, Tylax, TypeTeX) against the reference PDF for all 48 samples. Both the table and the grid labels are generated programmatically from `ai_models/absolute_scores.json` by `scripts/20_generate_appendix.py` and `scripts/19_generate_report_assets.py`.

Tier definitions (text IoU): exact >= 0.70, minor 0.40-0.70, major < 0.40. `content mismatch` means the candidate compiled but no text block could be matched to the reference at the Jaccard threshold (0.3); `not applicable` means the candidate did not produce a PDF to align.

## Full Dataset Scores Table

| Sample | Candidate | Status | Type | Match | Pos | Tier |
|:--------------------------------|:----------------|:------|:---|:----|:----|:----------|
| algorithms_easy | gemini | Success | IoU | 0.50 | 0.781 | exact |
| algorithms_easy | gpt | Failed | IoU | 0.00 | 0.000 | not applicable |
| algorithms_easy | pandoc | Success | IoU | 0.00 | 0.000 | content mismatch |
| algorithms_easy | tylax | Success | IoU | 0.50 | 0.107 | major |
| algorithms_easy | typetex | Success | IoU | 0.00 | 0.000 | content mismatch |
| algorithms_medium | gemini | Success | IoU | 1.00 | 0.467 | minor |
| algorithms_medium | gpt | Success | IoU | 1.00 | 0.583 | minor |
| algorithms_medium | pandoc | Success | IoU | 0.50 | 0.000 | major |
| algorithms_medium | tylax | Success | IoU | 0.50 | 0.228 | major |
| algorithms_medium | typetex | Success | IoU | 0.50 | 0.000 | major |
| beamer_easy | pandoc | Success | IoU | 0.50 | 0.000 | major |
| beamer_easy | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| beamer_easy | typetex | Success | IoU | 0.50 | 0.000 | major |
| beamer_hard | pandoc | Success | IoU | 0.00 | 0.000 | content mismatch |
| beamer_hard | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| beamer_hard | typetex | Success | IoU | 0.00 | 0.000 | content mismatch |
| beamer_medium | pandoc | Success | IoU | 0.50 | 0.000 | major |
| beamer_medium | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| beamer_medium | typetex | Success | IoU | 0.50 | 0.000 | major |
| cv_complex_easy | pandoc | Success | IoU | 1.00 | 0.306 | major |
| cv_complex_easy | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_complex_easy | tylax_patched | Success | IoU | 1.00 | 0.306 | major |
| cv_complex_easy | typetex | Success | IoU | 1.00 | 0.306 | major |
| cv_complex_hard | pandoc | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_complex_hard | pandoc_patched | Success | IoU | 1.00 | 0.089 | major |
| cv_complex_hard | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_complex_hard | tylax_patched | Success | IoU | 1.00 | 0.000 | major |
| cv_complex_hard | typetex | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_complex_hard | typetex_patched | Success | IoU | 1.00 | 0.089 | major |
| cv_complex_medium | pandoc | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_complex_medium | pandoc_patched | Success | IoU | 1.00 | 0.146 | major |
| cv_complex_medium | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_complex_medium | tylax_patched | Success | IoU | 1.00 | 0.146 | major |
| cv_complex_medium | typetex | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_complex_medium | typetex_patched | Success | IoU | 1.00 | 0.146 | major |
| cv_simple_easy | pandoc | Success | IoU | 0.67 | 0.069 | major |
| cv_simple_easy | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_simple_easy | tylax_patched | Success | IoU | 1.00 | 0.372 | major |
| cv_simple_easy | typetex | Success | IoU | 0.67 | 0.069 | major |
| cv_simple_hard | pandoc | Success | IoU | 0.20 | 0.258 | major |
| cv_simple_hard | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_simple_hard | tylax_patched | Success | IoU | 0.60 | 0.159 | major |
| cv_simple_hard | typetex | Success | IoU | 0.20 | 0.258 | major |
| cv_simple_medium | pandoc | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_simple_medium | pandoc_patched | Success | IoU | 0.50 | 0.298 | major |
| cv_simple_medium | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_simple_medium | tylax_patched | Success | IoU | 0.50 | 0.000 | major |
| cv_simple_medium | typetex | Failed | IoU | 0.00 | 0.000 | not applicable |
| cv_simple_medium | typetex_patched | Success | IoU | 0.50 | 0.298 | major |
| eq_hard_attention_eq1 | pandoc | Success | IoU | 1.00 | 0.220 | major |
| eq_hard_attention_eq1 | tylax | Success | IoU | 0.92 | 0.244 | major |
| eq_hard_attention_eq1 | typetex | Success | IoU | 1.00 | 0.204 | major |
| eq_hard_easy | pandoc | Success | IoU | 0.60 | 0.316 | major |
| eq_hard_easy | tylax | Success | IoU | 0.40 | 0.387 | major |
| eq_hard_easy | typetex | Success | IoU | 0.60 | 0.333 | major |
| eq_hard_hard | gemini | Success | IoU | 0.80 | 0.279 | major |
| eq_hard_hard | gpt | Success | IoU | 0.80 | 0.210 | major |
| eq_hard_hard | pandoc | Success | IoU | 0.80 | 0.242 | major |
| eq_hard_hard | tylax | Success | IoU | 0.80 | 0.279 | major |
| eq_hard_hard | typetex | Success | IoU | 0.80 | 0.242 | major |
| eq_hard_medium | pandoc | Success | IoU | 0.82 | 0.089 | major |
| eq_hard_medium | tylax | Success | IoU | 0.82 | 0.089 | major |
| eq_hard_medium | typetex | Success | IoU | 0.82 | 0.093 | major |
| eq_simple_easy | pandoc | Success | IoU | 1.00 | 0.654 | minor |
| eq_simple_easy | tylax | Success | IoU | 1.00 | 0.654 | minor |
| eq_simple_easy | typetex | Success | IoU | 1.00 | 0.654 | minor |
| eq_simple_hard | gemini | Success | IoU | 0.83 | 0.182 | major |
| eq_simple_hard | gpt | Success | IoU | 0.83 | 0.120 | major |
| eq_simple_hard | pandoc | Success | IoU | 0.83 | 0.178 | major |
| eq_simple_hard | tylax | Success | IoU | 0.83 | 0.182 | major |
| eq_simple_hard | typetex | Success | IoU | 0.83 | 0.191 | major |
| eq_simple_medium | pandoc | Success | IoU | 1.00 | 0.317 | major |
| eq_simple_medium | tylax | Success | IoU | 1.00 | 0.355 | major |
| eq_simple_medium | typetex | Success | IoU | 1.00 | 0.312 | major |
| paper_full_easy | pandoc | Success | IoU | 0.22 | 0.000 | major |
| paper_full_easy | tylax | Success | IoU | 0.67 | 0.151 | major |
| paper_full_easy | typetex | Success | IoU | 0.22 | 0.000 | major |
| paper_full_hard | pandoc | Failed | IoU | 0.00 | 0.000 | not applicable |
| paper_full_hard | tylax | Failed | IoU | 0.00 | 0.000 | not applicable |
| paper_full_hard | typetex | Failed | IoU | 0.00 | 0.000 | not applicable |
| paper_full_medium | pandoc | Success | IoU | 0.75 | 0.097 | major |
| paper_full_medium | tylax | Success | IoU | 0.75 | 0.088 | major |
| paper_full_medium | typetex | Success | IoU | 0.75 | 0.097 | major |
| paper_small_easy | pandoc | Success | IoU | 0.50 | 0.424 | minor |
| paper_small_easy | tylax | Success | IoU | 0.50 | 0.432 | minor |
| paper_small_easy | typetex | Success | IoU | 0.50 | 0.424 | minor |
| paper_small_hard | pandoc | Success | IoU | 0.50 | 0.227 | major |
| paper_small_hard | tylax | Success | IoU | 0.50 | 0.218 | major |
| paper_small_hard | typetex | Success | IoU | 0.50 | 0.227 | major |
| paper_small_medium | pandoc | Success | IoU | 0.60 | 0.420 | minor |
| paper_small_medium | tylax | Success | IoU | 0.60 | 0.410 | minor |
| paper_small_medium | typetex | Success | IoU | 0.60 | 0.439 | minor |
| pgfplots_easy | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_easy | tylax | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_easy | typetex | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_hard | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_hard | tylax | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_hard | typetex | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_medium | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_medium | tylax | Success | SSIM | 1.00 | 0.000 | major |
| pgfplots_medium | typetex | Success | SSIM | 1.00 | 0.000 | major |
| posters_easy | pandoc | Success | SSIM | 1.00 | 0.005 | major |
| posters_easy | tylax | Success | SSIM | 1.00 | 0.005 | major |
| posters_easy | typetex | Success | SSIM | 1.00 | 0.005 | major |
| posters_hard | pandoc | Success | SSIM | 1.00 | 0.007 | major |
| posters_hard | tylax | Success | SSIM | 1.00 | 0.006 | major |
| posters_hard | typetex | Success | SSIM | 1.00 | 0.007 | major |
| posters_medium | pandoc | Success | SSIM | 1.00 | 0.005 | major |
| posters_medium | tylax | Success | SSIM | 1.00 | 0.006 | major |
| posters_medium | typetex | Success | SSIM | 1.00 | 0.005 | major |
| prose_attention_prose1 | pandoc | Success | IoU | 1.00 | 0.609 | minor |
| prose_attention_prose1 | tylax | Success | IoU | 1.00 | 0.609 | minor |
| prose_attention_prose1 | typetex | Success | IoU | 1.00 | 0.609 | minor |
| prose_easy | gemini | Success | IoU | 1.00 | 0.681 | minor |
| prose_easy | gpt | Success | IoU | 1.00 | 0.704 | exact |
| prose_easy | pandoc | Success | IoU | 1.00 | 0.738 | exact |
| prose_easy | tylax | Success | IoU | 1.00 | 0.738 | exact |
| prose_easy | typetex | Success | IoU | 1.00 | 0.738 | exact |
| prose_hard | gemini | Success | IoU | 0.57 | 0.093 | major |
| prose_hard | gpt | Failed | IoU | 0.00 | 0.000 | not applicable |
| prose_hard | pandoc | Failed | IoU | 0.00 | 0.000 | not applicable |
| prose_hard | tylax | Success | IoU | 0.57 | 0.082 | major |
| prose_hard | typetex | Success | IoU | 0.57 | 0.096 | major |
| prose_medium | pandoc | Success | IoU | 0.00 | 0.000 | content mismatch |
| prose_medium | tylax | Success | IoU | 0.67 | 0.023 | major |
| prose_medium | typetex | Success | IoU | 0.00 | 0.000 | content mismatch |
| tables_complex_attention_table1 | pandoc | Success | IoU | 1.00 | 0.113 | major |
| tables_complex_attention_table1 | tylax | Success | IoU | 0.00 | 0.000 | content mismatch |
| tables_complex_attention_table1 | typetex | Success | IoU | 1.00 | 0.113 | major |
| tables_complex_attention_table2 | pandoc | Success | IoU | 0.60 | 0.000 | major |
| tables_complex_attention_table2 | tylax | Success | IoU | 0.10 | 0.610 | minor |
| tables_complex_attention_table2 | typetex | Success | IoU | 0.60 | 0.000 | major |
| tables_complex_easy | gemini | Success | IoU | 1.00 | 0.471 | minor |
| tables_complex_easy | gpt | Success | IoU | 1.00 | 0.064 | major |
| tables_complex_easy | pandoc | Success | IoU | 1.00 | 0.096 | major |
| tables_complex_easy | tylax | Success | IoU | 1.00 | 0.096 | major |
| tables_complex_easy | typetex | Success | IoU | 1.00 | 0.096 | major |
| tables_complex_hard | gemini | Success | IoU | 1.00 | 0.624 | minor |
| tables_complex_hard | gpt | Success | IoU | 1.00 | 0.627 | minor |
| tables_complex_hard | pandoc | Success | IoU | 1.00 | 0.585 | minor |
| tables_complex_hard | tylax | Success | IoU | 1.00 | 0.537 | minor |
| tables_complex_hard | typetex | Success | IoU | 1.00 | 0.585 | minor |
| tables_complex_medium | pandoc | Success | IoU | 1.00 | 0.577 | minor |
| tables_complex_medium | tylax | Success | IoU | 1.00 | 0.577 | minor |
| tables_complex_medium | typetex | Success | IoU | 1.00 | 0.577 | minor |
| tables_simple_easy | pandoc | Success | IoU | 0.00 | 0.000 | content mismatch |
| tables_simple_easy | tylax | Success | IoU | 0.00 | 0.000 | content mismatch |
| tables_simple_easy | typetex | Success | IoU | 0.00 | 0.000 | content mismatch |
| tables_simple_hard | pandoc | Success | IoU | 1.00 | 0.210 | major |
| tables_simple_hard | tylax | Success | IoU | 1.00 | 0.210 | major |
| tables_simple_hard | typetex | Success | IoU | 1.00 | 0.210 | major |
| tables_simple_medium | pandoc | Success | IoU | 1.00 | 0.275 | major |
| tables_simple_medium | tylax | Success | IoU | 1.00 | 0.275 | major |
| tables_simple_medium | typetex | Success | IoU | 1.00 | 0.275 | major |
| tikz_complex_easy | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| tikz_complex_easy | tylax | Success | SSIM | 1.00 | 0.009 | major |
| tikz_complex_easy | typetex | Success | SSIM | 1.00 | 0.000 | major |
| tikz_complex_hard | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| tikz_complex_hard | tylax | Success | SSIM | 1.00 | 0.000 | major |
| tikz_complex_hard | typetex | Success | SSIM | 1.00 | 0.000 | major |
| tikz_complex_medium | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| tikz_complex_medium | tylax | Failed | SSIM | 0.00 | 0.000 | not applicable |
| tikz_complex_medium | typetex | Success | SSIM | 1.00 | 0.000 | major |
| tikz_simple_easy | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| tikz_simple_easy | tylax | Success | SSIM | 1.00 | 0.012 | major |
| tikz_simple_easy | typetex | Success | SSIM | 1.00 | 0.000 | major |
| tikz_simple_hard | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| tikz_simple_hard | tylax | Failed | SSIM | 0.00 | 0.000 | not applicable |
| tikz_simple_hard | typetex | Success | SSIM | 1.00 | 0.000 | major |
| tikz_simple_medium | pandoc | Success | SSIM | 1.00 | 0.000 | major |
| tikz_simple_medium | tylax | Success | SSIM | 1.00 | 0.697 | major |
| tikz_simple_medium | typetex | Success | SSIM | 1.00 | 0.000 | major |

\newpage

## algorithms_easy

![algorithms_easy](assets/appendix_grids/algorithms_easy.png){width=100%}

\newpage

## algorithms_medium

![algorithms_medium](assets/appendix_grids/algorithms_medium.png){width=100%}

\newpage

## beamer_easy

![beamer_easy](assets/appendix_grids/beamer_easy.png){width=100%}

\newpage

## beamer_hard

![beamer_hard](assets/appendix_grids/beamer_hard.png){width=100%}

\newpage

## beamer_medium

![beamer_medium](assets/appendix_grids/beamer_medium.png){width=100%}

\newpage

## cv_complex_easy

![cv_complex_easy](assets/appendix_grids/cv_complex_easy.png){width=100%}

\newpage

## cv_complex_hard

![cv_complex_hard](assets/appendix_grids/cv_complex_hard.png){width=100%}

\newpage

## cv_complex_medium

![cv_complex_medium](assets/appendix_grids/cv_complex_medium.png){width=100%}

\newpage

## cv_simple_easy

![cv_simple_easy](assets/appendix_grids/cv_simple_easy.png){width=100%}

\newpage

## cv_simple_hard

![cv_simple_hard](assets/appendix_grids/cv_simple_hard.png){width=100%}

\newpage

## cv_simple_medium

![cv_simple_medium](assets/appendix_grids/cv_simple_medium.png){width=100%}

\newpage

## eq_hard_attention_eq1

![eq_hard_attention_eq1](assets/appendix_grids/eq_hard_attention_eq1.png){width=100%}

\newpage

## eq_hard_easy

![eq_hard_easy](assets/appendix_grids/eq_hard_easy.png){width=100%}

\newpage

## eq_hard_hard

![eq_hard_hard](assets/appendix_grids/eq_hard_hard.png){width=100%}

\newpage

## eq_hard_medium

![eq_hard_medium](assets/appendix_grids/eq_hard_medium.png){width=100%}

\newpage

## eq_simple_easy

![eq_simple_easy](assets/appendix_grids/eq_simple_easy.png){width=100%}

\newpage

## eq_simple_hard

![eq_simple_hard](assets/appendix_grids/eq_simple_hard.png){width=100%}

\newpage

## eq_simple_medium

![eq_simple_medium](assets/appendix_grids/eq_simple_medium.png){width=100%}

\newpage

## paper_full_easy

![paper_full_easy](assets/appendix_grids/paper_full_easy.png){width=100%}

\newpage

## paper_full_hard

![paper_full_hard](assets/appendix_grids/paper_full_hard.png){width=100%}

\newpage

## paper_full_medium

![paper_full_medium](assets/appendix_grids/paper_full_medium.png){width=100%}

\newpage

## paper_small_easy

![paper_small_easy](assets/appendix_grids/paper_small_easy.png){width=100%}

\newpage

## paper_small_hard

![paper_small_hard](assets/appendix_grids/paper_small_hard.png){width=100%}

\newpage

## paper_small_medium

![paper_small_medium](assets/appendix_grids/paper_small_medium.png){width=100%}

\newpage

## pgfplots_easy

![pgfplots_easy](assets/appendix_grids/pgfplots_easy.png){width=100%}

\newpage

## pgfplots_hard

![pgfplots_hard](assets/appendix_grids/pgfplots_hard.png){width=100%}

\newpage

## pgfplots_medium

![pgfplots_medium](assets/appendix_grids/pgfplots_medium.png){width=100%}

\newpage

## posters_easy

![posters_easy](assets/appendix_grids/posters_easy.png){width=100%}

\newpage

## posters_hard

![posters_hard](assets/appendix_grids/posters_hard.png){width=100%}

\newpage

## posters_medium

![posters_medium](assets/appendix_grids/posters_medium.png){width=100%}

\newpage

## prose_attention_prose1

![prose_attention_prose1](assets/appendix_grids/prose_attention_prose1.png){width=100%}

\newpage

## prose_easy

![prose_easy](assets/appendix_grids/prose_easy.png){width=100%}

\newpage

## prose_hard

![prose_hard](assets/appendix_grids/prose_hard.png){width=100%}

\newpage

## prose_medium

![prose_medium](assets/appendix_grids/prose_medium.png){width=100%}

\newpage

## tables_complex_attention_table1

![tables_complex_attention_table1](assets/appendix_grids/tables_complex_attention_table1.png){width=100%}

\newpage

## tables_complex_attention_table2

![tables_complex_attention_table2](assets/appendix_grids/tables_complex_attention_table2.png){width=100%}

\newpage

## tables_complex_easy

![tables_complex_easy](assets/appendix_grids/tables_complex_easy.png){width=100%}

\newpage

## tables_complex_hard

![tables_complex_hard](assets/appendix_grids/tables_complex_hard.png){width=100%}

\newpage

## tables_complex_medium

![tables_complex_medium](assets/appendix_grids/tables_complex_medium.png){width=100%}

\newpage

## tables_simple_easy

![tables_simple_easy](assets/appendix_grids/tables_simple_easy.png){width=100%}

\newpage

## tables_simple_hard

![tables_simple_hard](assets/appendix_grids/tables_simple_hard.png){width=100%}

\newpage

## tables_simple_medium

![tables_simple_medium](assets/appendix_grids/tables_simple_medium.png){width=100%}

\newpage

## tikz_complex_easy

![tikz_complex_easy](assets/appendix_grids/tikz_complex_easy.png){width=100%}

\newpage

## tikz_complex_hard

![tikz_complex_hard](assets/appendix_grids/tikz_complex_hard.png){width=100%}

\newpage

## tikz_complex_medium

![tikz_complex_medium](assets/appendix_grids/tikz_complex_medium.png){width=100%}

\newpage

## tikz_simple_easy

![tikz_simple_easy](assets/appendix_grids/tikz_simple_easy.png){width=100%}

\newpage

## tikz_simple_hard

![tikz_simple_hard](assets/appendix_grids/tikz_simple_hard.png){width=100%}

\newpage

## tikz_simple_medium

![tikz_simple_medium](assets/appendix_grids/tikz_simple_medium.png){width=100%}

