# Metric corpus profile v1

This is a corpus and evidence profile, not a PDF-fidelity score.

## Canonical corpus

- Documents: 157
- Reference pages: 239
- Page counts: {'1': 102, '2': 28, '3': 27}
- Reference canvases: {'a4': 10, 'letter': 147}
- Word counts (min / median / max): 13 / 215 / 1696

| Category | Documents |
|---|---|
| 01_prose_sections | 13 |
| 02_lists_formatting | 15 |
| 03_math_inline_display | 18 |
| 04_math_aligned | 15 |
| 05_tables_simple | 18 |
| 06_tables_moderate | 18 |
| 07_figures_captions | 15 |
| 08_crossrefs_citations | 15 |
| 09_algorithms | 12 |
| 10_compact_papers | 8 |
| 11_forms_cv_letters | 10 |

## Source and PDF signals

| Signal | Documents |
|---|---|
| has_inline_math | 57 |
| has_display_math | 60 |
| has_math_any | 110 |
| has_table_like_environment | 50 |
| has_semantic_table | 36 |
| has_figure_source | 15 |
| has_semantic_figure | 15 |
| has_list_source | 15 |
| has_algorithm_source | 12 |
| has_crossref_source | 41 |
| has_form_semantics | 10 |
| has_prose_semantics | 13 |
| has_compact_paper_semantics | 8 |

PyMuPDF's table detector finds tables in 18 documents. Semantic table applicability comes from the 36 documents in the two canonical table categories; detector misses must remain visible.

## Frozen metric-research partitions

Seed: `20260715`. exact category quotas with deterministic page-count/source-dataset interleaving; independent of the prompt-development split.

| Partition | Documents |
|---|---|
| metric_dev | 80 |
| metric_validation | 39 |
| metric_test | 38 |

These partitions are independent of the 30-row prompt-development and 127-row held-out prompt split. Metric weights and thresholds may be fit only on `metric_dev`; `metric_test` stays locked.

## Stored AI-output coverage

- Model: `google/gemini-3.1-flash-lite`
- Compiled candidates: 156/157
- Page-count matches: 129; mismatches: 27
- Candidate canvas documents: {'a4': 154, 'letter': 2}
- First-page canvas matches: 12; mismatches: 144

Canvas is its own diagnostic. Most references are Letter while most stored Typst outputs are A4; silently folding that producer default into a general layout score would make the score hard to explain.

## Augmentation applicability

Estimated controlled pairs: **16,167**. The blinded manual bundle contains 785 pairs (628 non-null), covering all 157 references.

| Family | Scope | Variants | Expected axis | Pairs |
|---|---|---|---|---|
| identity_lossless_roundtrip | all | 1 | invariant | 157 |
| canvas_translation | all | 12 | layout | 1,884 |
| uniform_scale | all | 6 | layout | 942 |
| largest_block_displacement | all | 12 | layout | 1,884 |
| text_span_deletion | all | 3 | content | 471 |
| lexical_numeric_substitution | all | 6 | content | 942 |
| typography_reflow | all | 12 | typography | 1,884 |
| edge_crop_local_occlusion | all | 15 | content+appearance | 2,355 |
| render_only_degradation | all | 9 | appearance_only | 1,413 |
| fixed_compound_defects | all | 6 | multiple | 942 |
| page_sequence_and_count | multipage | 4+2*pages | pagination | 494 |
| display_math_structure | display_math | 12 | content+layout | 720 |
| inline_math_structure | inline_math | 6 | content+typography | 342 |
| semantic_table_structure | semantic_table | 15 | content+layout | 540 |
| figure_and_caption | semantic_figure | 15 | content+layout | 225 |
| list_structure | list | 12 | content+layout | 180 |
| cross_reference_semantics | crossref | 9 | content | 369 |
| algorithm_structure | algorithm | 12 | content+layout | 144 |
| form_geometry | form | 9 | layout | 90 |
| prose_hierarchy | prose | 9 | content+layout | 117 |
| compact_paper_flow | compact | 9 | layout+pagination | 72 |

The render-only degradation lane is appearance-only. It cannot be used to teach an extraction-based content metric that rasterized PDFs have missing content.

## Provenance and licensing

- License columns in accepted manifest: []
- Per-sample provenance records with a license field: 0/157
- Sources containing explicit license text: 8/157
- Source-ID field variants: {'source_id': 12, 'source_ids': 145}
- Redistribution status: **not established by canonical metadata**

Missing research metadata includes license, original URL, authors, retrieval timestamp, and transformation record. Those gaps must be fixed before a redistributable benchmark claim.

## Files

- `corpus_profile_157.csv`: one measured row per accepted reference and stored AI result.
- `augmentation_applicability_157.csv`: per-reference augmentation lanes and pair counts.
- `corpus_summary.json`: machine-readable counts, partitions, gaps, and warnings.
