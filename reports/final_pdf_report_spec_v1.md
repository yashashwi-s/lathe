# Final PDF metric research report - frozen production specification

Status: production specification only. It contains no benchmark result that is
not already present in a frozen artifact.

## Release gate

The PDF must not be built until this succeeds:

```bash
mamba run -n lathe python scripts/evaluation/preflight_metric_research_report_v1.py \
  --output results/metric_research_v1/final_report_preflight.json \
  --freeze-dir results/metric_research_v1/final_report_inputs_v1
```

Success freezes file hashes and writes `final_report_register_157.csv`. Failure
must stop report generation. Missing validation or determinism results, missing
audit fields, contradictory accounting, an incomplete 157-row register, an AI
band other than `abstain`, or more than one model ID are release blockers.
Completed validation or determinism failures do not block an honest report;
their exact frozen status must appear prominently and the affected projection
must remain `TRIAL` rather than being silently omitted.

## Exact claim boundary

Use these sentences verbatim near the front of the report:

> This report evaluates one AI conversion corpus against 157 accepted LaTeX
> reference PDFs. It does not compare multiple AI models and does not estimate
> human preference.

> The primary result is an axis vector with evidence and abstention. There is
> no universal quality score.

The controlled study covers five harness projections: extracted-token
inventory F1, exact-token matched-box IoU q10, a mixed typography diagnostic,
unregistered tolerant ink F1, and a page-count/page-break diagnostic. CLEval,
LTSim, PaIRS, GriTS, TEDS, CDM, SSIM/MS-SSIM, and validated figure matching are
`NOT IMPLEMENTED`, not implied by a generic method name.

The AI material is the recorded adaptive `google/gemini-3.1-flash-lite`
LaTeX-to-Typst route. Prompt-development rows and the adaptive heldout rescue
route must be labeled separately. Raw axes are descriptive. No global AI grade,
quality band, cross-model rank, human-preference claim, or causal attribution is
permitted.

## Document architecture

Target approximately 42-46 landscape pages. Keep the scientific argument in
the first 28-30 pages; place complete accounting in the appendix.

1. Cover and one-sentence conclusion.
2. How to read status labels and boxes.
3. Executive findings derived from the frozen manifest.
4. Claim boundary and non-claims.
5. Corpus: 157 references, document forms, pages, prompt/metric splits.
6. Evaluated AI route: exact model ID, provider path, stages, and denominators.
7. Pair contract: reference PDF versus AI-produced Typst PDF.
8. Metric architecture: raw evidence, projections, abstention, no scalar.
9. Five implemented projections with equations and known limitations.
10. Published methods table: `IMPLEMENTED`, `TRIAL`, `ABSTAINING`, or
    `NOT IMPLEMENTED` only.
11. Augmentation design and realism limits.
12. Source-cluster split and leakage controls.
13. Corrected validation gates and bootstrap results.
14. Family-, variant-, and category-level failures; no averaging away.
15. Internal severity-profile result; explicitly disabled on AI outputs.
16. Byte, render, score, and localization determinism.
17. Blind controlled audit design and completion accounting.
18. Controlled examples selected only from completed, valid audit records.
19. AI visual-audit protocol; no human ratings.
20. AI raw-axis distributions and denominators.
21. Prompt split x metric split breakdown.
22. Page-count and canvas-confound accounting.
23. Category distributions and explicit abstentions.
24. AI examples selected after the audit freeze and labeled with exact model and
    prompt stage.
25. Failure modes and negative results.
26. What is verified now.
27. What remains trial or not implemented.
28. Next experiments with a verifiable stopping rule.
29. Primary references and repository artifact map.
30. Complete 157-row register, about 12 rows per landscape page.

## Visual evidence rules

- Every comparison panel must say `REFERENCE PDF` or `AI-PRODUCED TYPST PDF`.
- Every AI panel must show exact model ID and selected prompt stage outside the
  image, never inside a crowded score badge.
- On controlled examples only, red is the known synthetic edit region. Cyan is
  the registered raster-residual enclosure in the stated reference/candidate
  coordinate frame. The legend appears on every such page.
- AI examples have no red source-known box. Cyan may show the diagnostic raster
  residual only when the panel also states its coordinate frame and that it is
  not semantic ground truth.
- Do not reuse the dense token-by-token rainbow boxes from the v0.3 case book.
  They obscure the document and make unsupported correspondence look precise.
- Show the full one-to-three-page document, tiled without cropping. A magnified
  inset may accompany it, but never replace the complete page view.

## 157-row register contract

The appendix register is generated only by the preflight freezer. It includes:

- sample ID and document form;
- prompt split and metric partition;
- reference page count;
- AI output state and exact model/stage when compiled;
- page-count and canvas-sequence match;
- six raw axes, with blanks preserved as abstentions;
- six AI quality-band columns, which must all read `abstain` for compiled rows;
- the explicit reason for the single missing AI output.

Programmatic checks must confirm exactly 157 unique sample IDs, 156 compiled AI
rows, one missing row, and one model ID. The PDF may abbreviate repeated model
text visually only if the full exact identity remains in the row or repeated
page header.

## Citation floor

Use primary sources near the relevant method, not a detached bibliography-only
claim: Lapata (2006) for order; CLEval; LTSim; GriTS; TEDS/PubTabNet; CDM;
SSIM; RoDLA; the 2024 position-bias study; and the PaperFit preprint only as a
2026 workflow precedent. Each citation must state whether the method was
implemented, used as a design target, or rejected for grading.

## Reusable and rejected prior components

Reusable visual components:

- the restrained navy/off-white/orange palette and large titles from
  `pdf_similarity_methodologies_research_deck.pdf`;
- the consistent top rule, page number, compact status table, and two-panel
  alignment from `ai_model_fidelity_metric_study_v0_3.pdf`;
- the one-complete-document-per-record tiling logic from
  `scripts/ai/build_full_corpus_comparison.py`.

Replace completely:

- all hard-coded v0.3 statistics and 0-4 grade language;
- multi-model/protocol registry and head-to-head pages;
- claims based on the obsolete 24-case blind rubric;
- dense token boxes and miniature ten-badge headers;
- largely empty category separator pages in the 157-grid report;
- any statement that controlled corruptions are realistic Typst training data.

## Render and inspection gate

Write the final artifact to
`output/pdf/rendered_pdf_fidelity_research_report_v1.pdf`. Render every page to
`tmp/pdfs/rendered_pdf_fidelity_research_report_v1/`, inspect all pages, and
verify: no clipped text, no overlaps, no black/blank pages, readable tables at
100% zoom, complete page labels, stable page numbering, live human-readable
citations, and exactly 157 register rows. A PDF is not releasable merely because
its generator exits successfully.
