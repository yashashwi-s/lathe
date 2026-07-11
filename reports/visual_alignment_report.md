# Visual Alignment Report

## Methodology
The visual alignment pipeline (`scripts/18_visual_alignment.py`) evaluates structural preservation by directly comparing the layout of the reference PDF and the candidate PDF.

1. **Text Bounding Boxes (IoU)**: For text-heavy categories, PyMuPDF extracts bounding boxes for all text blocks. The coordinates are normalized by page size, matched primarily by reading order (with a Jaccard text-content fallback if block counts mismatch heavily), and scored via Intersection over Union (IoU).
2. **Structural Similarity (SSIM)**: For graphics-only categories (`tikz`, `pgfplots`, `posters`) without reliable text layers, pages are rendered to images, size-padded with white space to match dimensions, and evaluated via SSIM.
3. **Text Content Match (Jaccard)**: To ensure blocks are actually matching the right content, we compute a Jaccard similarity score for text tokens. We normalize Unicode (converting mathematical-italic letters to plain ASCII via NFKD) and strip punctuation (`re.findall(r'[a-z0-9]+')`) to accurately compare words. Page-number footer blocks (bottom 20% of the page, digits only) are filtered out on both sides before matching.

### Categorical Thresholds
- **IoU (Text Position)**: `exact` (>= 0.70), `minor` (0.40 – 0.70), `major` (< 0.40)
- **SSIM (Graphics)**: `exact` (>= 0.95), `minor` (0.75 – 0.95), `major` (< 0.75)
- **Text Content Match (Jaccard)**: Tokens must have a similarity > 0.30 to be considered matching.

> **IMPORTANT — Failed generations:** If a model or engine fails to compile, fails to generate a PDF, or produces an empty/invalid file, it receives a strict `0.0` for both Position (IoU/SSIM) and Text Content Match. These zeroes **are included** in all categorical averages to accurately penalize unreliability.

> **Provenance note:** every score in this report is read from `ai_models/absolute_scores.json` as produced by the canonical pipeline run; the aggregate tables below are printed by `scripts/21_report_tables.py`, and every grid image embeds its Match/Pos labels from the same JSON at render time (`scripts/19_generate_report_assets.py`), so figures and tables cannot silently disagree.

## Aggregated Averages (Alignment Only)
### Fair-Subset Averages (AI Models vs Engines)
Averages calculated *only* over the subset of samples completed by the AI Models (8 segments).

| Candidate | Text Content Match | Text Position (Mean IoU) |
|---|---|---|
| gemini | 0.838 | 0.447 |
| gpt | 0.704 | 0.288 |
| pandoc | 0.642 | 0.230 |
| tylax | 0.776 | 0.281 |
| typetex | 0.713 | 0.243 |

> **NOTE — change from earlier drafts:** previously published fair-subset numbers (e.g. Gemini 0.683/0.372) predate two matcher fixes: NFKD unicode normalization and page-number footer filtering. Both fixes raise most candidates' content-match rates (footers no longer count as unmatched blocks) and shift IoU values. GPT's two compile failures (`algorithms_easy`, `prose_hard`) are included as 0.0 in its averages.

> **WARNING — Block-Chunking Bias:** The text alignment metric (Bounding Box IoU) structurally penalizes AI candidates for chunking layout content into fewer, larger blocks than the reference LaTeX/Pandoc engines (which emit heavily fragmented line-by-line blocks). A visually pristine AI output can score mathematically lower than an equivalent engine output. Even so, Gemini now leads both content match and position on this subset.

### Fair Subset Visual Comparisons (AI Models vs Engines)
Below are 3x2 grids comparing the reference layout to all 5 candidates for some of the 8 samples evaluated by the AI models. Panel labels show each candidate's Match / Pos scores from the scores table; failed candidates show a FAILED panel.

**Sample**: `tables_complex_hard`

![Grid tables_complex_hard](assets/fair_grids/tables_complex_hard.png){width=95%}

\newpage

**Sample**: `prose_easy`

![Grid prose_easy](assets/fair_grids/prose_easy.png){width=95%}

\newpage

**Sample**: `eq_hard_hard`

![Grid eq_hard_hard](assets/fair_grids/eq_hard_hard.png){width=95%}

\newpage

**Sample**: `algorithms_easy`

![Grid algorithms_easy](assets/fair_grids/algorithms_easy.png){width=95%}

\newpage

## Curated Examples: Content vs Position Trade-offs
These examples illustrate how the two metrics move independently.

### Simple prose: both content and position can be near-perfect
**Sample:** `prose_easy` | **Candidate:** `gpt` | **Match Rate:** `1.00` | **IoU:** `0.704`

![Curated Example 1](assets/examples/curated_1_prose_easy_gpt.png)

> On single-page prose, GPT reproduces both the text and its layout closely enough to score
> `exact` (IoU 0.704). Earlier drafts used this sample to illustrate a low position score;
> after the NFKD and page-number-filter fixes, its position score is genuinely high.

\newpage

### High Content Match, Moderate Position Score (Table Formatting Shift)
**Sample:** `tables_complex_hard` | **Candidate:** `tylax` | **Match Rate:** `1.00` | **IoU:** `0.537`

![Curated Example 2](assets/examples/curated_2_tables_complex_hard_tylax.png)

> Tylax renders the table and its text is fully matched (1.00). However, the spatial dimensions and column widths of the generated table differ from the reference PDF, leading to a moderate position IoU (0.537) despite the content being intact.

\newpage

### The Impact of Patching CVs
**Sample:** `cv_complex_hard` | **Candidate:** `tylax_patched` | **Match Rate:** `1.00` | **IoU:** `0.000`

![Curated Example 3](assets/examples/curated_3_cv_complex_hard_tylax_patched.png)

> Tylax failed to compile this CV natively (unescaped `@`). After patching, it compiles and all text content is recovered (match 1.00), but the layout is so drastically rearranged that no matched block pair overlaps at all — position IoU 0.0. Patching restores content, not geometry.

\newpage

### Pandoc's Equation Handling
**Sample:** `eq_simple_hard` | **Candidate:** `pandoc` | **Match Rate:** `0.83` | **IoU:** `0.178`

![Curated Example 4](assets/examples/curated_4_eq_simple_hard_pandoc.png)

> Pandoc outputs Unicode Math characters (mathematical italics) instead of styled ASCII; NFKD normalization lets these match the reference words fairly (match 0.83). The equations themselves land in visibly different vertical positions, so the position score stays low (0.178).

\newpage

### Full-Corpus Averages (Engines Only)
Averages calculated over the entire evaluation dataset of **48 samples**. Compile failures are included as 0.0 in all averages. Text Content Match averages over all 48 samples (a compiled graphics sample counts 1.0, since whole-image SSIM implies the full structure is present); Text Position averages over the 36 text samples; Graphics Alignment averages over the 12 graphics samples.

| Candidate | Text Content Match | Text Position (Mean IoU) | Graphics Alignment (Mean SSIM) |
|---|---|---|---|
| pandoc | 0.679 | 0.195 | 0.001 |
| tylax | 0.586 | 0.211 | 0.061 |
| typetex | 0.691 | 0.199 | 0.001 |

> **NOTE:** The near-zero SSIM values are expected: none of the three engines can translate TikZ/PGFPlots drawing commands, so the "graphics" pages compile as (near-)blank pages, and blank candidate pages are scored 0.0 by design. Tylax's nonzero SSIM comes from partial TikZ output, dominated by `tikz_simple_medium` (SSIM 0.697).

### Note on "Patched" Candidates
Some candidate engines failed to compile CV formats natively and were manually patched (appearing as `pandoc_patched`, `tylax_patched`, and `typetex_patched`; TypeTeX's patched artifacts are stored as `typetex_approx_patched.*` on disk).

> **NOTE — Absence of Patched SSIM:** The patched variants are excluded from the visual alignment table above. The manual patches were applied only to CV samples (which contain no graphics and receive no SSIM scores), so a raw average for the patched variants would yield a mechanical `0.000` SSIM purely from an absence of graphical samples. The meaningful structural comparison for patched candidates is in `benchmark_findings.md`.

\newpage

## Visual Examples
### Positive Examples (High Alignment Score)

**Sample**: `prose_easy` | **Candidate**: `pandoc` | **IoU Score**: `0.738` | **Match Rate**: `1.00`

![Positive Example 1](assets/examples/positive_1_prose_easy_pandoc.png){width=100%}

\newpage

**Sample**: `eq_simple_easy` | **Candidate**: `pandoc` | **IoU Score**: `0.654` | **Match Rate**: `1.00`

![Positive Example 2](assets/examples/positive_2_eq_simple_easy_pandoc.png){width=100%}

\newpage

### Negative Examples (Low Alignment Score)

**Sample**: `paper_full_easy` | **Candidate**: `typetex` | **IoU Score**: `0.000` | **Match Rate**: `0.22`

![Negative Example 1](assets/examples/negative_1_paper_full_easy_typetex.png){width=100%}

\newpage

**Sample**: `tables_complex_attention_table2` | **Candidate**: `typetex` | **IoU Score**: `0.000` | **Match Rate**: `0.60`

![Negative Example 2](assets/examples/negative_2_tables_complex_attention_table2_typetex.png){width=100%}

## Limitations
While this visual comparison is much more robust than the previous heuristic, it does not capture:
- Subtle font variations and kerning differences (unless they shift text blocks significantly).
- Color mismatches (SSIM is computed in grayscale to focus on structure).
- The actual reason for a mismatch (e.g. if a table overflows, the IoU score will just reflect the displacement).
- Single-block references: when a reference PDF emits an entire table as one text block while the candidate emits per-row blocks (e.g. `tables_simple_easy`), no block pair can clear the Jaccard threshold and the sample scores a content mismatch even though the rendered text is visually identical. This is a known metric artifact and is left in the data rather than hand-corrected.

## Appendix
The complete per-sample scores table and all 48 comparison grids are in `appendix.pdf`, generated by `scripts/20_generate_appendix.py`.

**Full execution log of the scoring run used here:** `logs/visual_alignment_20260709_220740.log`
