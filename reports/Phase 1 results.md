# Exploratory Task 1 Results

With the human evaluation complete, we have computed the aggregated scores for the deterministic engines. However, the score table alone masks the most important finding of this task: **content and text almost always survive conversion intact, while layout mechanics (grids, borders, flow direction, positioning) are where every engine breaks down.**

## Scoring Methodology
Each engine was scored out of a maximum of **1.0 point** per sample:
- **0.5 points** awarded if the engine successfully compiled the sample (did not crash or timeout).
- **0.5 points** awarded for 1st place visually, **0.25** for 2nd, **0.1** for 3rd, and **0.0** for 4th.
- If a sample was marked "All are Rubbish", the visual score was nullified for all engines (0 points).

> [!WARNING]
> **Sample Size & Rater Caveat**
> The visual rankings (1st/2nd/3rd/4th) came from human judgment by a single rater on a small exploratory sample size (n=30-45). This lacks inter-rater reliability checks and statistical rigor. These results are for pipeline validation and qualitative signaling only, not definitive evaluation.

## Aggregated Score Table

| Category | Pandoc | Tylax | TypeTeX |
|----------|--------|-------|---------|
| 01_prose | 0.58 | 1.00 | 0.58 |
| 02_eq_simple | 0.83 | 1.00 | 0.33 |
| 03_eq_hard | 0.75 | 1.00 | 0.00 |
| 04_paper_full | 0.25 | 0.88 | 0.25 |
| 05_paper_small | 0.75 | 1.00 | 0.75 |
| 06_tables_simple | 1.00 | 1.00 | 1.00 |
| 07_tables_complex | 1.00 | 1.00 | 1.00 |
| 08_algorithms | 0.50 | 0.50 | 0.50 |
| 09_tikz_simple | 0.50 | 0.42 | 0.50 |
| 10_tikz_complex | 0.50 | 0.37 | 0.50 |
| 11_pgfplots | 0.50 | 0.50 | 0.50 |
| 12_cv_simple | 0.80 | 0.00 | 0.80 |
| 13_cv_complex | 0.60 | 0.00 | 0.60 |
| 14_posters | 0.60 | 0.75 | 0.60 |
| 15_beamer | 0.67 | 0.00 | 0.67 |
| **OVERALL** | **0.67** | **0.67** | **0.58** |

### Table Anomalies & Caveats
- **Pandoc vs Tylax (0.67):** The identical overall score masks opposite risk profiles. **Tylax is high-variance**: dominant on standard documents, but scores a total zero on unsupported classes (CV/Beamer). **Pandoc is low-variance**: it rarely outputs a perfect visual layout, but it consistently produces *something* across all categories without crashing.

## Failure Taxonomy
The qualitative observation that "formatting > content" provides our most reusable artifact for the pipeline. Here is the explicit breakdown of how layout mechanics fail:

| Failure type | Where it shows up | Engines affected |
|---|---|---|
| Grid/border styling lost | CV tables, complex tables | most engines |
| Flow direction wrong (L→R becomes top→down) | Posters | all engines, structurally |
| Color/theme not preserved | Beamer | all engines |
| Geometric/positional fidelity lost | TikZ, PGFPlots | all engines, worst category |
| Structural formatting lost (line numbers, indentation, keyword styling) | Algorithms | all engines, reduced to plain lines |

## Key Takeaways for AI Feedback Loops
These findings fundamentally shift how we should construct the deterministic feedback loops for our AI agents:

> [!IMPORTANT]
> **Feedback modalities must be split by category type.**
> Because content/text preservation is generally fine, and failures are overwhelmingly isolated to layout mechanics (which bounding boxes and compile-diffs cannot fully capture), image-based feedback is not an "expensive nice-to-have." It is the **primary signal** for layout-heavy categories. 
> 
> The golden rule for the AI feedback loop:
> - **Structural/textual diffing** for content-preservation categories (prose, basic equations, algorithms).
> - **Image diffing (Visual LLM / SSIM / Pixel Diff)** for layout-mechanic categories (posters, TikZ/PGFPlots, Beamer, complex tables).