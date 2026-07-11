# Lathe scoring, explained

How `ai_models/absolute_scores.json` gets built and what each number means.
Two independent evaluation layers run on every `(sample, candidate)` record:
the 6-point rubric (`scripts/16_heuristic_evaluator.py`) and visual alignment
(`scripts/18_visual_alignment.py`).

## 1. The 6-point rubric (`16_heuristic_evaluator.py`, `evaluate_candidate()`)

All heuristic, run directly on the `.typ` source text — no rendering
involved. Aggregation lives in `scripts/scoring_utils.py:13-30`
(`get_score`/`get_max_score`): if the file didn't compile, score is 0 out of
6; otherwise sum these 6 booleans (5 if `text_completeness` is N/A for
tikz/pgfplots samples).

1. **`compiles`** (line 55) — binary: did a `.png`/`.pdf` get produced at
   all. If not, the record short-circuits to a "does not compile" note and
   every other field stays 0.
2. **`no_leaked_source`** (lines 59-62) — regex `\\[a-zA-Z]+` finds any raw
   LaTeX command left un-translated in the Typst output (e.g. a stray
   `\section`). 1 if none found.
3. **`text_completeness`** (lines 64-79) — word-bag overlap. `get_latex_words()`
   (line 6) strips LaTeX commands with `\[a-zA-Z]+(\[.*?\])?(\{.*?\})?` and
   keeps words ≥4 letters; same regex is run on the Typst output. Score is 1
   if `|intersection| / |latex_words| >= 0.6`. Set to `"N/A"` entirely for
   `tikz`/`pgfplots` samples (no meaningful body text to compare) — this is
   why max score drops to 5 for those.
4. **`structural_elements`** (lines 81-92) — did each LaTeX structural marker
   survive translation: `\begin{tabular}` → `#table`/`table(`,
   `\begin{figure}` → `#figure`, `\section` → any `=` heading marker,
   `\begin{equation}` → any `$`. All required ones must be present.
5. **`numbering_correctness`** (lines 94-102) — if the source has
   sections/equations/figures (which Typst auto-numbers by default), checks
   the output didn't disable it via an explicit `numbering:` call. Presence
   of `numbering:` counts as *correct* here — it's checking "numbering
   wasn't left broken," not a specific format.
6. **`typography_correctness`** (lines 115-120) — flags common
   quote-escaping mistakes (`\"`, `` `` ``, doubled `""`, `''`, or a
   `#quote[...]` opening with a straight quote) that Typst mishandles
   differently from LaTeX.

Two more fields are **recorded but not scored** — informational only:

- `font_match` (lines 104-110) — "match" / "sans_swap" / "serif_swap"
  depending on whether the output kept New Computer Modern or swapped
  fonts. Not part of the 6-point sum.
- `alignment_deviation` — set to `"not_implemented"` here and only gets a
  real value later, overwritten by stage 18.

## 2. The visual alignment layer (`18_visual_alignment.py`)

Renders the reference PDF (from `pdflatex`) and the candidate PDF (from
`typst compile`) and compares pixels/text-blocks. It picks one of two metric
families depending on category, and one of those families computes two
sub-scores — 3 numeric outputs in total.

**A. SSIM** (`evaluate_ssim`, lines 63-112) — used only for
`GRAPHICS_CATEGORIES = ["tikz", "pgfplots", "posters"]` (line 31), where
there's no real "text block" structure to compare, just rendered graphics.

- Rasterizes page 1 of both PDFs to grayscale at 150 DPI, pads both to the
  larger canvas size (white-padded), then runs
  `skimage.metrics.structural_similarity`.
- Masks out pixels white in *both* images so blank margins don't inflate the
  score, and forces score to 0.0 if the candidate page is entirely blank.
- Output `alignment_score` = mean masked SSIM across pages; `content_match_rate`
  is hardcoded to `1.0` here (SSIM has no separate "did the content exist"
  signal).

**B. IoU + Jaccard** (`evaluate_iou`, lines 114-239) — used for every
text-bearing category. Produces two distinct numbers:

- **`content_match_rate`** — fraction of reference text blocks that found
  *any* matching candidate block. "Matching" is decided by **Jaccard
  word-set similarity** (`jaccard_similarity`, lines 51-61: lowercased,
  normalized, `[a-z0-9]+` tokenized, `|intersection|/|union|`) against a
  `threshold = 0.3` (line 127). Two block-pairing strategies are used
  depending on how well block *counts* line up (lines 185-222): if
  ref/candidate have similar block counts, blocks are matched by sorted
  reading order; if counts diverge a lot, it falls back to a greedy
  best-Jaccard-match search across all pairs (`"text_content_fallback"`
  strategy).
- **`alignment_score`** (position/IoU) — for each matched block pair, both
  bounding boxes are normalized (offset-subtracted, then divided by page
  width/height) so absolute page position/margins don't matter, and plain
  bounding-box IoU (`get_iou`, lines 33-49) is computed. The mean over all
  matched pairs is the alignment score — purely geometric, only computed
  *after* a text match was found.

Both families feed `map_score_to_deviation()` (lines 241-261), which buckets
the score into `exact` / `minor` / `major` (different thresholds for
graphics vs. text; `content_mismatch` if `content_match_rate == 0`,
`extraction_failed` if a PDF is unreadable) — that's the tier shown in
reports.

So the 3 visual numbers per record are: **`alignment_score`** (IoU or SSIM
depending on category), **`content_match_rate`** (Jaccard-block-match rate,
text categories only), and the derived **`alignment_deviation`** tier.

## Text matching in both layers — and the difference

Text matching happens twice, with different purpose and math:

| | Rubric `text_completeness` (stage 16) | Visual alignment Jaccard (stage 18) |
|---|---|---|
| Compares | Whole-document word bag: all LaTeX source words vs. all Typst source words | Per-block text: one reference PDF text block vs. one candidate PDF text block |
| Input | Raw **source code** (`.tex` and `.typ` text) | **Rendered PDF** text extraction (`page.get_text("dict")`) |
| Metric | Overlap ratio `\|A∩B\| / \|A\|` (asymmetric — did the Typst source retain the LaTeX words) | Jaccard `\|A∩B\| / \|A∪B\|` (symmetric) |
| Threshold | ≥ 0.6 → pass/fail (1 bit) | ≥ 0.3 → "is this the same block" (used to *pair* blocks, not scored directly) |
| Purpose | "Did content survive translation at all" — coarse gate | "Which reference block corresponds to which candidate block" — a matching step, whose *result* (match rate) becomes a score, and only matched pairs proceed to IoU |
| Failure mode | Passes even if layout is completely broken (source-level only) | Exactly the counterpart: catches `beamer_hard`-style cases where source "has" the words but rendering collapsed |

This is deliberate (README.md:148-151): the rubric is source-level and
heuristic, so it can pass documents with broken rendered layout; visual
alignment is the layer that catches that. They're designed to disagree
sometimes, not to double-check each other. Example: `beamer_hard` scores
rubric 6/6 but visual alignment 0.0.

## The 3 visual asset outputs (`19_generate_report_assets.py`)

Separate from the metrics, 3 kinds of images are generated for the reports,
all built from `absolute_scores.json` so labels can't drift from the data:

1. **`assets/appendix_grids/`** — one 2×2 PNG per sample (all 48 samples):
   Reference / Pandoc / Tylax / TypeTeX, each panel showing the rendered
   page 1 with **text-block bounding boxes drawn on it**
   (`render_panel`, lines 81-129 — visualizing the same blocks IoU is
   computed over) and a label of `Match: x.xx | Pos: x.xxx` read straight
   from the JSON (`score_text`, lines 153-162).
2. **`assets/fair_grids/`** — one 3×2 PNG per fair-subset sample (the 8
   categories both AI models and engines were tested on): adds Gemini/GPT
   panels alongside the 3 engines.
3. **`assets/examples/`** — 8 hand-curated 1×2 reference-vs-one-candidate
   pairs (`EXAMPLE_PAIRS`, lines 30-39) used inline in
   `visual_alignment_report.md` to illustrate specific findings (e.g.
   `curated_1_prose_easy_gpt`, `negative_2_...typetex`).

Any candidate whose record has `compiles == 0` gets a hardcoded red "FAILED
TO COMPILE" panel (`failed_panel`, lines 132-139) regardless of what stray
files might exist on disk — so the images can never show a success where
the score says failure.
