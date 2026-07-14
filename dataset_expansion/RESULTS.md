# Dataset expansion — 1-turn sonnet (low effort) difficulty benchmark

All scores pdf_fidelity_v0.1 with **raster_v0.2**, 0-100, averaged over
*compiled* samples only (compile failures shown in the compile column —
they are the strongest difficulty signal). References for new sets were
compiled with **tectonic** (pdflatex unavailable); lathe rows use the
original pdfLaTeX references.

| set | n | compiled | overall | content | layout | typography | raster | pagination | page-mismatch | $ | note |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| lathe_overall | 11 | 6/11 | 49.7 | 89.7 | 48.9 | 79.3 | 13.2 | 79.6 | 2 | 0.64 | current benchmark, 1/category (lathe prompt_dev) |
| lathe_hard | 8 | 6/8 | 44.0 | 88.4 | 38.1 | 77.5 | 10.2 | 64.3 | 4 | 0.73 | current hard set (harness_baseline core 6+2) |
| i2s_equation | 5 | 1/5 | 57.7 | 64.4 | 68.0 | 83.5 | 24.7 | 100.0 | 0 | 0.32 | image2struct equation snippets |
| i2s_table | 5 | 3/5 | 68.1 | 92.9 | 72.8 | 85.2 | 27.2 | 100.0 | 0 | 0.36 | image2struct table snippets |
| i2s_algorithm | 5 | 5/5 | 65.3 | 87.4 | 73.6 | 84.7 | 24.8 | 99.6 | 0 | 0.29 | image2struct algorithm snippets |
| i2s_plot | 5 | 0/5 | — | — | — | — | — | — | 0 | 0.44 | image2struct TikZ/pgfplots snippets (new category) |
| pubmed_table | 5 | 2/5 | 29.8 | 81.1 | 28.3 | 68.2 | 3.2 | 33.8 | 2 | 0.45 | PubMed clinical tables (messy) |
| arxiv5t_paper | 5 | 1/5 | 4.1 | 0.9 | 23.7 | 72.9 | 0.4 | 26.1 | 1 | 1.01 | arXiv-5T full papers, real figures |
| neurips_paper | 2 | 0/2 | — | — | — | — | — | — | 0 | 0.86 | NeurIPS full papers |

## Per-sample

- `01_prose_sections_001` (lathe_overall): overall 69.6, pages 1/1
- `02_lists_formatting_024` (lathe_overall): **no compile**
- `03_math_inline_display_004` (lathe_overall): **no compile**
- `04_math_aligned_008` (lathe_overall): overall 64.1, pages 1/1
- `05_tables_simple_005` (lathe_overall): overall 38.4, pages 2/3
- `06_tables_moderate_010` (lathe_overall): overall 34.8, pages 2/3
- `07_figures_captions_001` (lathe_overall): overall 48.0, pages 1/1
- `08_crossrefs_citations_008` (lathe_overall): **no compile**
- `09_algorithms_003` (lathe_overall): overall 43.4, pages 2/2
- `10_compact_papers_015` (lathe_overall): **no compile**
- `11_forms_cv_letters_002` (lathe_overall): **no compile**
- `03_math_inline_display_004` (lathe_hard): **no compile**
- `04_math_aligned_014` (lathe_hard): overall 47.4, pages 2/1
- `05_tables_simple_005` (lathe_hard): overall 38.4, pages 2/3
- `05_tables_simple_021` (lathe_hard): overall 37.9, pages 3/2
- `05_tables_simple_023` (lathe_hard): overall 59.1, pages 3/3
- `06_tables_moderate_010` (lathe_hard): overall 39.0, pages 2/3
- `07_figures_captions_007` (lathe_hard): **no compile**
- `09_algorithms_003` (lathe_hard): overall 42.4, pages 2/2
- `i2s_equation_001` (i2s_equation): **no compile**
- `i2s_equation_003` (i2s_equation): **no compile**
- `i2s_equation_004` (i2s_equation): overall 57.7, pages 1/1
- `i2s_equation_005` (i2s_equation): **no compile**
- `i2s_equation_006` (i2s_equation): **no compile**
- `i2s_table_002` (i2s_table): overall 65.9, pages 2/2
- `i2s_table_004` (i2s_table): **no compile**
- `i2s_table_006` (i2s_table): overall 69.1, pages 2/2
- `i2s_table_007` (i2s_table): overall 69.2, pages 1/1
- `i2s_table_008` (i2s_table): **no compile**
- `i2s_algorithm_001` (i2s_algorithm): overall 64.6, pages 2/2
- `i2s_algorithm_003` (i2s_algorithm): overall 65.0, pages 2/2
- `i2s_algorithm_004` (i2s_algorithm): overall 74.1, pages 1/1
- `i2s_algorithm_005` (i2s_algorithm): overall 62.2, pages 1/1
- `i2s_algorithm_008` (i2s_algorithm): overall 60.5, pages 1/1
- `i2s_plot_001` (i2s_plot): **no compile**
- `i2s_plot_002` (i2s_plot): **no compile**
- `i2s_plot_003` (i2s_plot): **no compile**
- `i2s_plot_004` (i2s_plot): **no compile**
- `i2s_plot_005` (i2s_plot): **no compile**
- `pubmed_table_001` (pubmed_table): **no compile**
- `pubmed_table_002` (pubmed_table): **no compile**
- `pubmed_table_003` (pubmed_table): overall 32.2, pages 2/6
- `pubmed_table_004` (pubmed_table): overall 27.3, pages 2/1
- `pubmed_table_005` (pubmed_table): **no compile**
- `arxiv5t_paper_002` (arxiv5t_paper): **no compile**
- `arxiv5t_paper_006` (arxiv5t_paper): overall 4.1, pages 10/1
- `arxiv5t_paper_019` (arxiv5t_paper): **no compile**
- `arxiv5t_paper_020` (arxiv5t_paper): **no compile**
- `arxiv5t_paper_022` (arxiv5t_paper): **no compile**
- `neurips_paper_029` (neurips_paper): **no compile**
- `neurips_paper_036` (neurips_paper): **no compile**

## Agentic check — opus low, visual, harness v3 ($3 cap)

Six high-difficulty picks (short + verbose). 1-turn sonnet compiled 1/6;
the harness compiled 6/6 but plateaued 57.9-67.1 — all below the ~78 the
same harness family reaches on the lathe hard set. All runs stopped on
plateau, not budget. Side-by-side renders: `visual_review/`.

| sample | 1-turn | harness overall | content | layout | raster | pages | $ | min |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| `arxiv5t_paper_019` | nc | 57.9 | 94.5 | 63.7 | 14.3 | 5/4 | 0.70 | 2.6 |
| `i2s_equation_001` | nc | 58.6 | 60.7 | 82.6 | 22.6 | 1/1 | 0.78 | 2.5 |
| `i2s_plot_001` | nc | 67.1 | 98.4 | 91.3 | 16.6 | 1/1 | 0.80 | 2.9 |
| `neurips_paper_029` | nc | 62.4 | 83.8 | 51.9 | 31.6 | 11/11 | 2.16 | 12.3 |
| `pubmed_table_004` | 27.3 | 60.2 | 77.8 | 53.4 | 33.5 | 2/2 | 0.82 | 2.6 |
| `pubmed_table_005` | nc | 58.0 | 88.6 | 57.9 | 18.7 | 2/2 | 0.87 | 2.9 |
