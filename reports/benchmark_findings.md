# LaTeX → Typst Conversion Benchmark: Findings Report

## Scope

Evaluated 3 deterministic engines (Pandoc, Tylax, TypeTeX) across 15 categories (48 samples),
and 2 AI models (Gemini, GPT — manually prompted, no API access) across a matched 8-category
subset. Scoring uses an absolute, per-candidate rubric (compiles, clean source, text
completeness, structural elements, numbering correctness, typography) rather than relative
ranking, so ties can mean "all correct" rather than "all failed similarly."

> **Provenance note.** Every number in this report is regenerated end-to-end from the
> on-disk artifacts by the canonical pipeline (`scripts/16_heuristic_evaluator.py` →
> `scripts/18_visual_alignment.py` → `scripts/21_report_tables.py`). Earlier drafts of this
> report carried some hand-maintained values that had drifted from the pipeline output;
> those have been replaced wholesale. Where a previously published figure changed, the
> reason is stated inline.

## Headline Numbers

### Fair-Subset (8 categories: AI Models vs Engines)
| Candidate | Average Score (out of 6.0) |
|---|---|
| Gemini | 5.88 / 6.0 |
| GPT | 4.25 / 6.0 |
| Pandoc (Patched) | 4.88 / 6.0 |
| TypeTeX (Patched) | 5.38 / 6.0 |
| Tylax (Patched) | 5.50 / 6.0 |

### Full Corpus (15 categories, Engines Only)
| Candidate | As-Tested Baseline | Patched Ceiling |
| -----------| --------------------| -----------------|
| Pandoc    | 5.03 / 6.0         | 5.40 / 6.0      |
| TypeTeX   | 5.08 / 6.0         | 5.44 / 6.0      |
| Tylax     | 4.10 / 6.0         | 4.74 / 6.0      |

**"Patched ceiling"** = score after manually fixing known, trivial, engine-specific
transcription bugs (see below) — represents each engine's structural capability once those
specific bugs are set aside, not its out-of-the-box behavior.

> **Change from previously published figures.** Earlier drafts reported Pandoc 4.90/5.29,
> TypeTeX 4.95/4.97, Tylax 4.10/4.74. Two corrections moved Pandoc and TypeTeX upward:
> (1) the `beamer_hard` records previously carried empty rubric fields that were silently
> counted as zero; the sample is now rubric-evaluated by the same script as every other
> sample. (2) Three TypeTeX patched CV records (`cv_complex_hard`, `cv_complex_medium`,
> `cv_simple_medium`) had been removed during an audit on the belief that their artifacts
> did not exist; the artifacts (`typetex_approx_patched.{typ,pdf,png}`) do in fact exist
> on disk, timestamped in the same batch as every other patched artifact, and the records
> are now regenerated from those files. Tylax's figures were unaffected and reproduce the
> previously published values exactly.

## Key Findings

**1. AI models and deterministic engines are close, not a blowout, on matched ground.**
On the 8 categories both were tested on, Gemini (5.88) leads but Tylax (5.50), TypeTeX (5.38),
and Pandoc (4.88) are competitive — this is a fair comparison only within these 8 categories;
AI models were not tested on the remaining 7 (CV, beamer, posters, PGFPlots, TikZ) due to
manual-prompting constraints, so no full-corpus AI comparison exists yet.

**2. GPT is markedly more compile-brittle than Gemini.** GPT failed to compile on 2 of 8 matched
samples (0/6 both times); Gemini compiled on all 8. Gemini's only miss was a typography defect
(doubled quotation marks), not a hard failure.

**3. At the patched ceiling, TypeTeX and Pandoc are nearly indistinguishable — and TypeTeX's
remaining weakness is source cleanliness, not compilation.** With the `\hrule` patch applied,
TypeTeX compiles 47 of 48 samples (97.9%); the only remaining failure is `paper_full_hard`,
which no engine compiles. Its patched ceiling (5.44) slightly exceeds Pandoc's (5.40). What
keeps it from pulling further ahead is its clean-source rate (68.8% vs. Pandoc's 95.8%): the
MiTeX delegation strategy embeds raw LaTeX math inside `#mitex(...)` calls, which the rubric
counts as leaked source. This is an inherent trade-off of the delegation approach, not a
transcription bug. *(An earlier draft claimed the TypeTeX CV patches were never successfully
applied and reported a 4.97 ceiling; that claim originated from an audit that checked the
wrong filename — `typetex_patched.pdf` instead of the on-disk `typetex_approx_patched.pdf` —
and is withdrawn.)*

**4. Tylax is the consistent structural outlier, and it's not just the CV bug.** Even after
patching, Tylax remains lowest (4.74 vs. ~5.4 for the other two). It shows a recurring
"clean source" failure pattern (leaked or malformed output) across multiple unrelated categories,
indicating a broader structural weakness beyond any single fixable bug.
(Note: Tylax's fair-subset competitiveness doesn't extend to the full corpus, where CV/beamer-specific
failures pull its average down; the two tables are not measuring the same category mix.)

**5. Two specific, generalizable engine bugs were found and isolated (Patched Information):**
   - **Reserved-character leakage (Tylax only):** unescaped `@` in plain text (e.g. email
     addresses) breaks compilation, because Typst reserves `@` for label references. Audited
     across the full corpus — confirmed limited to 6 CV samples, not a wider issue. We patched
     these files to use `\@`, which immediately resolved the crashes.
   - **Macro mistranslation (Pandoc & TypeTeX):** `\hrule` is translated to a non-existent Typst
     command (`#horizontalrule`), crashing the compiler. Affects `cv_complex_hard` and both
     `cv_*_medium` variants specifically. This was patched to `#line(length: 100%)` to restore structure.

**6. TypeTeX's math pipeline (via its Lua filter) initially crashed outright on standalone equation
categories** — a confirmed software defect in the filter itself (traversal error on certain math
components). This was patched at the engine level in this run, meaning its equations now compile
natively and properly reflect its true capability without artificial crashes.

**7. Beamer content undergoes structural flattening in all three deterministic engines — and
the rubric alone would not have caught it.** The `beamer_hard` sample (a multi-frame slide deck
with `\titlepage`, `\block`, and `\alertblock` environments) exposes a systematic gap: none of
the three engines preserve beamer's frame/block hierarchy. Pandoc and TypeTeX silently discard
the title page entirely, producing output one page shorter than the two-page reference. Tylax's
conversion step completes without error, but the generated Typst references an undefined
variable (`#slide`); the file fails to compile and produces no output. Notably, Pandoc and
TypeTeX pass all six source-level rubric checks on this sample (6/6) — the dropped title page
does not remove enough prose to trip the text-completeness threshold — while the visual
alignment stage scores them `content_mismatch` (0.0 content match, zero position credit)
because of the page-count shift. This is a concrete case where the two evaluation layers
disagree, and the visual layer is the one telling the truth about the reader-visible output.

> *Methodological note on `beamer_hard`:* this sample was added as sample 48 after the main
> conversion batch. Its compile flags were appended to `results/compile_metrics.csv`
> (`pandoc=1, tylax=0, typetex=1`, matching the on-disk artifacts in `results/15_beamer/hard/`),
> and its rubric and alignment records are produced by the same two canonical scripts
> (`16_heuristic_evaluator.py`, `18_visual_alignment.py`) that score the other 47 samples.
> The only remaining asymmetry is that its conversion step was run separately from the
> original `03_convert_engines.py` batch.

## Metric-Level Pass Rates

The absolute rubric evaluates candidates across 6 independent binary metrics. Below are the average pass rates across the evaluated corpus (using the "patched ceiling" for deterministic engines).

### Fair-Subset (8 AI-Tested Categories)
| Candidate | Compiles | Clean Source | Text Complete | Structs | Num Correct | Typography |
|---|---|---|---|---|---|---|
| Gemini | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 87.5% |
| GPT | 75.0% | 75.0% | 75.0% | 75.0% | 62.5% | 62.5% |
| Pandoc (Patched) | 87.5% | 87.5% | 62.5% | 87.5% | 75.0% | 87.5% |
| Tylax (Patched) | 100.0% | 75.0% | 100.0% | 100.0% | 100.0% | 75.0% |
| TypeTeX (Patched) | 100.0% | 50.0% | 100.0% | 100.0% | 100.0% | 87.5% |

### Full Corpus (15 Categories, Engines Only)
| Candidate | Compiles | Clean Source | Text Complete | Structs | Num Correct | Typography |
|---|---|---|---|---|---|---|
| Pandoc (Patched) | 95.8% | 95.8% | 87.2% | 87.5% | 77.1% | 95.8% |
| Tylax (Patched) | 87.5% | 60.4% | 80.5% | 75.0% | 87.5% | 83.3% |
| TypeTeX (Patched) | 97.9% | 68.8% | 94.9% | 89.6% | 97.9% | 95.8% |

<div style="page-break-before: always;"></div>

## Methodology: Absolute Rubric Definitions

The evaluation avoids relative ranking in favor of a 6-point absolute rubric. For each metric, a candidate scores `1` if it satisfies the requirement, and `0` otherwise. If a candidate fails to compile, it scores `0` across all metrics. The overall score is out of `6.0` (or `5.0` if Text Completeness is not applicable).

**1. Compiles (`compiles`)**
Does the provided Typst source code successfully compile using the Typst CLI without fatal errors? If the candidate does not compile or produces no output, it fails this baseline check and receives `0` for all subsequent metrics.

**2. Clean Source (`no_leaked_source`)**
Is the generated Typst code free of leaked, raw LaTeX commands? This is evaluated by scanning the `.typ` file for common unresolved LaTeX macro patterns (e.g., `\textbf`, `\section`, `\begin{...}`). If raw LaTeX syntax is found floating in the output, it fails.

**3. Text Completeness (`text_completeness`)**
Does the compiled document retain the original prose? This compares alphabetic word bags between the source and the candidate. A score is awarded if at least 60% of the source's textual content is matched in the output. *(Note: This metric is marked as `N/A` for pure-graphics categories like TikZ/PGFPlots to avoid false penalties).* This ensures text wasn't dropped during translation.

**4. Structural Elements (`structural_elements`)**
Did the engine correctly identify and convert structural boundaries? This involves a heuristic check to ensure headings, paragraphs, lists, equations, tables, and semantic blocks were correctly transformed into their Typst equivalents (e.g. `#table`, `#figure`, `$`), rather than just flattened into plain text.

**5. Numbering Correctness (`numbering_correctness`)**
Are figures, tables, and equations numbered appropriately, and do internal references properly point to them? Evaluates if the candidate used native Typst numbering and referencing logic (e.g., `@label` and `#figure`) instead of hardcoding the numbers as raw text strings.

**6. Typography (`typography_correctness`)**
Does the candidate respect the visual styling intents of the original LaTeX? Evaluates if bolding, italics, monospace blocks, margins, and intended font declarations were preserved. In particular, it penalizes unescaped straight quotes `""` or LaTeX-style doubled quotes which render improperly in Typst compared to its native smart quotes.
