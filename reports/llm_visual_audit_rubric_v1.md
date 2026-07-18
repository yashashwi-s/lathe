# LLM visual-audit rubric v1

Status: frozen research audit protocol. The reviewer is an LLM inspecting
rendered comparisons. These records are not human ratings or perceptual ground
truth.

## Blind controlled-perturbation audit

The reviewer sees two unlabeled candidate/reference panels with perturbation,
metric, score, and answer identity hidden. For every case it records:

- changed panel: `A`, `B`, or blank when abstaining;
- visible defect axis: `content`, `layout`, `typography`, `appearance`,
  `pagination`, `structure`, or `unclear`;
- a concrete page-region description;
- confidence in `[0,1]`;
- an explicit `true`/`false` abstention flag;
- a short observation, not an inferred generator label.

After the blind file is frozen, the reviewer may see the answer key and
unblinded overlay. It separately records whether the candidate is valid, the
mutation is visible, the recorded target box is correct, the generator label is
correct, and the cyan raster-residual box is useful. Blind judgments are never
rewritten after unblinding.

## Blind AI-output audit

The reviewer sees a complete `REFERENCE PDF` beside the complete
`AI-PRODUCED TYPST PDF`. Model route, prompt stage, raw axes, synthetic profiles,
and residual evidence are hidden. Each issue field uses exactly one label:

- `none`: no visible defect on this axis;
- `minor`: local difference that preserves the document's function;
- `moderate`: clear multi-region or important local defect, but the document
  remains usable;
- `major`: omission, corruption, severe reflow, clipping, wrong page structure,
  or specialized-content failure that materially changes the document;
- `unclear`: image resolution or ambiguity prevents a defensible judgment.

Axis instructions:

- **Content:** missing, added, corrupted, reordered, or visibly unrendered text,
  numbers, symbols, citations, and raw markup.
- **Layout:** positions, grouping, margins, alignment, columns, overlap, clipping,
  or substantial reflow. Styling alone is not layout.
- **Typography:** font size, weight, style, hierarchy, line spacing, baseline, and
  glyph appearance. Do not penalize a different family name unless visibly
  different.
- **Pagination:** page-count, page-break, orphaned, duplicated, or missing-page
  defects. A one-page restyle is not pagination damage.
- **Specialized structure:** tables, formulas, figures, algorithms, forms,
  captions, cross-references, or lists whose rendered relationships are wrong.

`severity_summary` is a short evidence-based sentence, not a scalar overall
grade. `confidence` is in `[0,1]`. `review_notes` must cite at least one visible
region, even for an all-`none` result.

After unblinding, the reviewer records whether the cyan registered-raster
residual is useful and whether the raw axis labels are plausible. A useful cyan
box localizes visible change; it does not establish semantic cause or human
importance.

## Analysis boundary

Controlled detection accuracy and AI issue/axis association are reported with
coverage and abstentions. The audit may falsify a projection or identify a
failure mode. It cannot validate human preference, acceptability, or a universal
quality score.
