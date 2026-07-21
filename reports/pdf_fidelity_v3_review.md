# Review: `pdf_fidelity_metric_system_v3.pdf`

*(source: `reports/pdf_fidelity_metric_system_v3.typ`, built to `output/pdf/pdf_fidelity_metric_system_v3.pdf`, 45 pages)*

## Bottom line

**The methodology is correct and unusually rigorous.** I read the full report, read the actual Python code that computes every metric it describes, and then cross-checked about 20 specific numbers printed in the report (identity-check results, controlled-mutation statistics, AUC values, agreement/kappa scores, a specific "17 false-positive citations" example, an SSIM value, and both full result tables) against the raw JSON/CSV files those numbers are supposedly drawn from. **Every single one matched exactly.** The formulas described in prose (Text-LTSim, Kendall's tau, the four-scale SSIM diagnostic, the word-matching cost function) also match the code line-for-line.

This is not a "vibe-coded" document dressed up with fake precision — it's the opposite of that. Its whole design philosophy is to *refuse* to overclaim: it never produces a single overall score, it labels every sub-metric as used / conditional / diagnostic / pending / abstained, and it repeatedly points out its own weak spots (small sample sizes, unstable auto-review labels, metrics that structurally can't go below a certain value, etc.). That kind of self-criticism is a good sign, not a bad one.

The one thing worth actually fixing operationally: **the code's default render resolution (120 DPI) does not match the 96 DPI baked into every number in this report.** The report flags this itself on the last page, but it's a real trap — if you or a future agent reruns the evaluator without explicitly passing `--render-dpi 96`, you'll get different SSIM/raster numbers and think something broke.

---

## What this project actually is (you said you're vibecoding — here's the context)

**Lathe** is a benchmark for testing tools that convert LaTeX documents into **Typst** (a newer, simpler document-typesetting language meant to replace parts of LaTeX). The benchmark has 157 real LaTeX documents with known-correct reference PDFs, and it runs different converters against them — an AI model (Gemini, tried against 127 held-out documents plus some development documents), Claude models (only tested on 7 documents, informally), and three "deterministic" (non-AI, rule-based) converters: Pandoc, Tylax, TypeTeX.

For any conversion, there are two separate questions:

1. **Did it even compile?** (Did the converter produce something that turns into a valid PDF at all?)
2. **If it compiled, how faithful is the resulting PDF to the original?** — same words, same layout, same page breaks, same look?

This particular report — "PDF fidelity evaluation, v3" — is entirely about question 2: it documents, in detail, *how* the project measures "faithfulness," what it currently trusts, what it doesn't trust yet, and why. It is a methodology/audit document, not the project's headline results (that's a separate file, `reports/benchmark_paper_blog.md`, per the README).

---

## How I verified it

1. Read all 45 pages of the report (extracted the text page-by-page from the PDF).
2. Read the actual scoring code: `scripts/evaluation/pdf_metric_axes_v2.py` (617 lines) and the shared helpers it calls in `pdf_metric_axes_v1.py`.
3. For every formula the report describes in words, I found the matching code and checked it computes what's claimed (word-matching cost function, Text-LTSim optimal-transport formula, Kendall's tau, four-scale SSIM diagnostic, SSIM parameters, ink threshold).
4. For specific numbers printed in tables and callout boxes, I opened the underlying result files in `results/metric_research_v2/...` and recomputed/compared directly.

## Specific numbers I checked (all matched)

| Claim in report | Where | Source file checked | Result |
|---|---|---|---|
| 157 self-identity pairs, all 9 checks pass | p.23 | `identity_157_final/identity_validation.json` | exact match |
| 628 controlled mutations, 530 valid+visible, 98 invalid | p.23–24 | `controlled_retained_628/validation/validation_summary.json` | exact match |
| No-op trigger rates: content 40.8%, layout 82.7%, raster 99.0%, typography 16.3% | p.24 | same file | exact match (to 3 sig figs) |
| Box usefulness 496 full / 23 partial / 109 none (79.0%) | p.25 | raw manual-review CSVs (had to merge inconsistent `true/yes` and `no/false` labels — did so and it summed correctly) | exact match |
| Second-audit agreement 83.7%, kappa 0.734, axis-label agreement 14.6%, 82 both-commit | p.25 | `reaudit/reaudit_agreement.json` | exact match |
| Gemini content-issue AUC 0.550 | p.6 | `gemini_frozen_156/analysis/ai_manual_metric_alignment.json` | 0.5497 → matches |
| Gemini typography AUC 0.535 | p.16 | same file | exact match |
| Claude Opus `05_tables_simple_023`: 17 false-positive bracketed citations | p.9 | `claude_overlap/metric_v2/evidence/...claude_opus.json` | exact match |
| Claude Opus `05_tables_simple_005`: SSIM 0.571 | p.17, p.33 | same evidence set | 0.5711 → matches |
| Both full scorecard tables (7-doc and 157-doc) | p.28–29 | `results/metric_research_v2/scorecards/scorecards.json` | exact match, every cell |
| Code default DPI is 120 vs. 96 used here | p.45 | `pdf_metric_axes_v1.py`, `DEFAULT_RENDER_DPI = 120` | confirmed true — real discrepancy, correctly self-flagged |
| Ink threshold 245, tolerance 2px | p.45 | same file constants | exact match |
| Text-LTSim can't score below ≈0.607 for text-only pages | p.12 | derived from the cost formula in `pdf_metric_axes_v2.py` | mathematically verified true |

I did not find a single fabricated or mismatched number anywhere I checked.

## Real limitations (these are honestly disclosed in the report itself, not things I'm catching them out on)

- **No human ratings exist anywhere in this validation.** All the "does the metric behave sensibly" evidence comes from self-identity tests, synthetic damage, and an LLM reviewing screenshots — not real people judging real documents. The report says this outright.
- **The automated "second opinion" LLM auditor is not very self-consistent.** Re-running it on the same cases only agrees on the specific defect category 14.6% of the time, even though it agrees on the coarser pass/fail 83.7% of the time. That's why the report says to trust the raw text/box evidence over any category label.
- **Several diagnostics are described as "raw" and not yet gated by confidence thresholds** — e.g., pagination boundary F1 "can equal 1 vacuously when neither side has a page break," reading-order tau can look artificially high on low-coverage matches, and the raster (ink-overlap) detector false-triggers on 99% of unrelated cases, so it's a blunt instrument.
- **SSIM (pixel-level image comparison) is only usable on a tiny slice of the data** — 2 out of 156 Gemini documents — because most AI outputs use a different physical page size (Letter vs A4) than the reference, which makes direct pixel comparison invalid. This isn't a flaw in the metric; it's a real, correctly-handled limitation of the underlying data.
- **The 7-document "four-way" Gemini/Sonnet/Opus comparison is explicitly not a leaderboard.** Gemini was run once, source-only; Claude got 6 out of 7 documents with multiple agentic tries and visual feedback. Comparing raw scores across that would be unfair, and the report says so repeatedly, in bold, on multiple pages.
- **Citation-marker detection uses a narrow, hand-picked pattern** and will misfire on anything bracketed (shown concretely: 17 false "citations" in one table-heavy document), so it's manually restricted to documents where citations are actually expected.
- **DPI mismatch (mentioned above)** — an operational reproducibility risk, not a scoring error.

None of these are "the methodology is wrong." They're the kind of caveats a careful researcher lists so nobody downstream over-trusts a number. If anything, the amount of self-auditing here is more thorough than most benchmark write-ups you'll see.

---

## Page-by-page walkthrough, in plain language

**p.1 — Cover.** States the report's thesis up front: this tool never returns one overall grade. It returns a bundle of hard facts, raw per-axis scores, and visual evidence (highlighted boxes on the actual PDF pages).

**p.2 — The pipeline.** A flowchart of the process: open both PDFs → check page count and physical paper size → check exact text/number/citation preservation → (if applicable) check spatial layout and pixel-level image similarity → package everything into an evidence report. Three ground rules are stated: page size is never "normalized away" (Letter vs A4 stays a real difference), a looser text-matching pass never overrides a stricter mismatch, and if a metric can't be computed, it says "abstain" instead of guessing.

**p.3 — Worked example.** Shows one real result: a sender's address block from a reference PDF and from Gemini's converted output, with colored boxes marking where the text actually sits. Four scores are shown side by side — word survival (0.969, basically all words present), how far matched words moved (0.671, a lot), a layout-similarity score (0.671), and whether numbers survived (0.667, a date got mangled). The point: high content-preservation and bad layout-preservation can both be true at once — that's why one grade wouldn't work.

**p.4 — Status board.** A legend of every sub-metric, bucketed into "used now" (hard facts and exact text stats), "conditional/diagnostic" (reported with caveats, not fully trusted), and "pending/abstain/rejected" (not ready, or deliberately not built — like a single universal score, which was explicitly rejected). Also gives corpus sizes: 157 reference documents, 156 Gemini outputs that compiled, 7 documents where all four systems (reference + Gemini + Claude Sonnet + Claude Opus) exist for comparison.

**p.5 — Method: the hard gate.** Before comparing anything else, the tool checks whether each PDF opened, how many pages it has, and the exact physical size of each page in points. This matters because Letter (612×792pt) and A4 (595×842pt) look similar on a screen but are different real-world sizes — so this check has to come first, and any later pixel-level comparison is skipped if sizes don't match. Only 2 of 156 Gemini documents pass this exactly.

**p.6 — Method: strict text preservation.** Pulls the actual text out of both PDFs, lightly normalizes it (merges whitespace, standard Unicode form), and scores word-level precision/recall/F1 plus a character-edit-distance score. This is the main "did the content survive" number. Caveat: PDF text extraction can chop up math/formulas differently between renderers, which can drag this score down even when the formula displays identically.

**p.7 — Method: looser word matching.** A second, more forgiving pass that folds together visually-equivalent Unicode characters and lines up individual words by position, so it can list exactly which words are missing (with coordinates). This never overwrites the stricter score from p.6 — it's extra evidence, not a replacement.

**p.8 — Method: numbers and math symbols.** A narrow, high-stakes check: does every number and math operator (=, +, ∇, etc.) from the reference also show up in the candidate? This catches a wrong date or a garbled equation that a whole-document text score would hide inside a sea of otherwise-correct text.

**p.9 — Method: citation markers.** Same idea for reference markers like "[1]" — checking they weren't replaced with something else (like a raw bibliography key). Only turned on for documents that actually contain citations, because bracketed numbers in a table can trigger false alarms (a real example is shown: 17 false hits in one document).

**p.10 — Method: word movement.** For every word that matched exactly between the two PDFs, how far did its position move and did its size change? Reported as median/90th-percentile displacement.

**p.11 — Method: box overlap and size.** More raw geometry stats: how much matched-word boxes overlap, font-size ratio, vertical offset. Notably discards one specific statistic because it's zero for literally every document in the corpus and therefore useless.

**p.12 — Method: Text-LTSim.** Implements a real published metric: treats each page's text blocks as "mass" that has to be moved to align with the other page, computes the cheapest way to do that (optimal transport), and turns the cost into a similarity score. I verified this is mathematically bounded — for this text-only setup it can never score below about 0.607, which the report states and which checks out from the code.

**p.13 — Method: two more transport-style diagnostics.** Explicitly labeled as "not the published metric, just inspired by it": one blends position and text-content similarity (65/35 weighted), the other labels matched blocks as left/right/above/below each other and checks if that relationship survives.

**p.14 — Method: pagination.** Checks page-count match (trusted) and, separately, whether the same page-breaks land in the same place (marked "raw, not fully trustworthy yet"). Good example given: a formula that moved from page 2 to page 1 is a different failure than a formula that's simply gone, and the tool can tell the difference.

**p.15 — Method: reading order.** After matching corresponding text blocks, checks whether they're still in the same order using Kendall's tau, a standard statistic (correctly cited, and the code's formula matches the textbook one exactly).

**p.16 — Method: typography.** Font size, vertical baseline position, and bold/italic/font-family agreement for matched words.

**p.17 — Method: pixel-level image comparison (SSIM).** Only runs when both pages are physically identical size and resolution — true for just 2 of 156 Gemini documents. Good honesty here: one Claude example scored a "bad" 0.571 SSIM even though a reviewer found nothing visibly wrong, because plain white background can dominate the math. So a low SSIM number alone isn't proof of a real visible problem.

**p.18 — Method: four-scale SSIM.** Runs the same image comparison at 4 different zoom levels and averages them. Explicitly *not* claimed to be the "real" published multi-scale SSIM (which weights scales differently) — labeled as a custom diagnostic.

**p.19 — Method: older ink-overlap check.** A cruder approach: threshold each page to black/white "ink" and measure overlap. Requires forcibly resizing one image to match the other, which was judged an unfair comparison in 145 of 156 Gemini cases — kept only as a rough, low-trust signal.

**p.20 — Method: CLEval (pending).** Explains that a well-known published text-recognition metric would be a more rigorous replacement for the word-matching on pages 6–7, but it hasn't been properly implemented yet — honestly marked "pending" instead of faked.

**p.21 — Method: table/formula/figure structure metrics (abstained).** Three more published metrics (for tables, HTML-table structure, and formulas/figures) are turned off for every document, because the current PDF extraction doesn't yet produce the structured data (e.g., an actual table grid) those metrics need. Key point restated: "abstain" means "can't measure this yet," not "score of zero."

**p.22 — No single score, on purpose.** States the core design decision: scores are never combined into one number, and cites a real methodological reference (an OECD/JRC handbook on building composite indices) to justify why — combining requires weighting and missing-data choices that haven't been validated, so the team reports the whole set of scores side by side instead of guessing.

**p.23 — How the tool itself was checked (overview).** Four validation layers: (1) comparing every reference PDF to a copy of itself (sanity check — should score perfectly); (2) 628 documents with a known, artificial defect injected, to see if the tool notices; (3) documents damaged at 3 increasing severity levels, to check scores move in the right direction; (4) real AI/converter outputs reviewed by an LLM to sanity-check the tool's findings against what's actually visible.

**p.24 — Controlled damage detail.** Four kinds of injected damage: delete text, shift a block, locally corrupt something, or break a specific construct (table/formula/etc.). Good news: on the 530 cases confirmed both valid and visible, the intended detector fired 100% of the time. Honest caveat: 98 of 628 cases turned out invalid or not actually visible on review, and the raster/pixel detector is very trigger-happy (fires on 99% of unrelated cases), so it's not precise by itself.

**p.25 — Manual review quality.** Of 628 cases, the tool's evidence box was fully useful 496 times, partially useful 23, not useful 109 (79% fully useful). A second independent re-review checked consistency: solid agreement on pass/fail (83.7%, "substantial" by standard stats), but weak agreement on the specific defect category (14.6%) — so the report says trust the raw evidence over any broad label.

**p.26 — Current limits, stated plainly.** A clean "what's defensible now" vs "what's not defensible now" list. Defensible: hard facts, literal text checks, word-position evidence, transport diagnostics with their limits disclosed, side-by-side examples. Not defensible: any single overall grade, any claim about human preference, structure-based scores, or ranking models from the small 7-document set. Ends with a 6-item research roadmap.

**p.27 — Intro to the seven-document comparison.** Explains the legend for the worked examples that follow (which color box means what) and states plainly: don't rank the models from these seven documents — Gemini was run once, Claude got multiple tries with visual feedback on 6 of 7, so it's not a fair comparison.

**p.28 — The seven-document results table.** Side-by-side numbers for Gemini, Claude Sonnet, Claude Opus, and three non-AI converters (Pandoc, Tylax, TypeTeX) — compile rate, exact page match, exact paper size match, and the various fidelity scores. Repeats: descriptive only, not a leaderboard.

**p.29 — The full 157-document results table.** Same idea, scaled to the whole corpus, but only for Gemini and the three deterministic converters (Claude was only ever run on the small 7-document set). Flags that this "Gemini" run is a development/debugging cascade with multiple retry attempts, not the project's official frozen single-shot benchmark result — so treat this table as internal engineering data, not the paper's headline number.

**p.30–43 — Seven worked examples (two report-pages each).** Each pair of pages walks through one real shared document across all three AI/model outputs, with actual before/after screenshots and colored boxes: a two-page math document compressed to one page everywhere; a table's last row surviving but visually colliding with other text in Gemini's output; a table caption landing on a different page depending on the converter; invented extra rows appearing in a table that don't exist in the original; a repeated table row getting visually squashed; a figure caption showing literal unrendered math text instead of the symbol; and an algorithm box mislabeled as "Figure 1" by Gemini. Throughout, the report keeps pointing out cases where two scores *disagree* (e.g., a numerically "worse" layout score for a visually cleaner page) — deliberately proving, with real examples, why no single number here can be trusted alone.

**p.44 — References.** A real academic-style source list — Unicode normalization, Levenshtein distance, the Hungarian assignment algorithm, GIoU, CLEval, LTSim, Kendall's tau, SSIM, multi-scale SSIM, GriTS, TEDS, the PDF spec, and the OECD composite-indicator handbook — all with real DOIs. States the citation policy: a published name is only used when the actual required data/math is present; otherwise it's labeled an "adaptation."

**p.45 — Reproducibility appendix.** Exact file paths for every dataset behind every number in the report, the exact frozen settings used (96 DPI, ink threshold 245, SSIM window/sigma, etc.), and a self-flagged warning that the code's *default* DPI is actually 120 — different from the 96 baked into this report — so re-running without explicitly passing `--render-dpi 96` won't reproduce these exact numbers. Ends with the literal shell commands to rebuild the whole report from scratch.

---

## If you want to act on anything

The only concrete fix I'd suggest is making `--render-dpi 96` the explicit, impossible-to-miss default for anyone (human or agent) re-running this evaluator against this report's frozen results, since the current code default silently disagrees with what's documented here. Everything else is a documented, intentional limitation rather than a mistake.
