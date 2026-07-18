# Four-PDF overlap visual audit

This directory contains evidence artifacts, not a model ranking or a public report.

## Artifacts

- `overlap_visual_comparison.pdf`: seven A2 landscape vector sheets, one complete sample per page.
- `sheet_01_*.png` through `sheet_07_*.png`: 300 dpi renders of the seven sheets (7016 x 4961 pixels).
- `manual_visual_findings.csv`: one visual-only judgment for each of the 21 candidate PDFs.

Every sheet uses the same fixed order: Reference, Gemini 3.1 Flash Lite, Claude Sonnet 4.6, Claude Opus 4.7. All source pages are shown in full and multi-page documents are tiled within their quadrant. The model and exact protocol ID are printed above each output. The styling is intentionally limited to white, gray, and black.

## Manual review method

The PDF paths and hashes were frozen first in `../overlap_manifest.csv`. The reviewer then inspected every sheet and all 21 candidates against its reference without consulting automatic metric scores. Ambiguous table and caption details were checked with separate page renders at 140-180 dpi. The findings record the most consequential visible defect per candidate; they are not claimed to enumerate every glyph difference.

`candidate_valid=true` means the stored PDF opened, rendered, and contained enough visible material to assess. It does not mean the output is faithful.

Severity is used as follows:

- `none`: no clear defect visible at the inspected resolution.
- `minor`: localized numbering, rule-weight, page-furniture, or small placement difference without structural damage.
- `moderate`: clear page-flow, layout, or content-presentation change while the output remains readable.
- `major`: visible content addition/loss, structural relabeling, unreadable overlap, exposed source markup, or comparable document-level failure.

When present, `normalized_bbox` is `[x0,y0,x1,y1]` in candidate-page coordinates with the origin at the top left. Boxes are included only for visible regions that can be localized defensibly. Document-wide pagination changes and absent elements intentionally have blank boxes.

## Why this is not a fair leaderboard

The generation protocols are heterogeneous:

- Gemini used a source-only OpenRouter prompt-stage run with no reference images and at most one repair. Five cases use prompt v0; two use a targeted v1 retry run.
- The math sample uses one-turn, low-effort Claude runs with no visual feedback.
- The other six Sonnet cases use an agentic v1 visual compile-score-revise loop at low effort.
- The other six Opus cases use an agentic v3 visual compile-score-revise loop at medium effort.

Most Claude candidates therefore received reference and candidate page images plus iterative revision opportunities that Gemini did not receive. The sheets are valid for checking whether an evaluation metric agrees with concrete visible defects. They cannot isolate model capability, and no cross-model rank should be inferred from them.

The audit also has one reviewer and no human ratings. It should be treated as traceable research evidence for metric development, not ground-truth preference data.

## Reproduction

```bash
mamba run -n lathe python scripts/evaluation/build_claude_overlap_visual_audit_v1.py
```
