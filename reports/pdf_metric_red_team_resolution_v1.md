# PDF metric v1 red-team resolution log

Status: methodology corrections applied; post-correction execution and visual
audit remain required. This log prevents the final report from inheriting
claims that the implementation does not support.

| Red-team finding | Resolution in v1 | Verification required |
|---|---|---|
| The harness validates five projections, not the full literature scorecard. | Report the run as a controlled-response study of extracted-token F1, exact-token box-IoU q10, mixed typography diagnostic, unregistered ink F1, and page-count/break diagnostic. Mark CLEval, LTSim, PaIRS, GriTS, TEDS, CDM, SSIM, and figure matching `not_implemented`. | Final method-status table and claim-boundary page. |
| Lossless invariant FPR compared a row with itself. | Compare severity-zero lossless projections with their analytic optimum of 1.0. | Rerun validation on all 157 sources. |
| Pilot did not test determinism; 0.01 tolerance was not exact. | Use `projection_repeat_agreement` only for stored score/bbox equality at 1e-12. Require a separate same-seed run with score equality, PDF SHA-256 equality, and rendered-pixel equality. | 471 repeat cases and 157 retained artifact pairs. |
| Monotonicity excluded baseline and counted ties as successes. | Add the severity-zero source baseline to every 1–3 sequence; a tie is a failure. | Recompute adjacent accuracy and Kendall tau-b. |
| Overall means hid variant failures. | Emit family-, variant-, and category-level flags; none can be averaged away by an overall pass. | Full gate assessment with source-cluster intervals. |
| Off-target selectivity treated every unnamed axis as invariant. | Keep target/off-target drops descriptive only until every variant has a preregistered affected-axis and invariant-axis contract. | Future response-contract version. |
| Localization was described as semantic explanation accuracy. | Rename cyan evidence to `registered raster-residual enclosure`. Measure only overlap with the known synthetic edit region in the reference frame. | Correct box routing and two-phase visual audit. |
| Global severity bands pooled incomparable and unbalanced edits. | Fit internal profiles only from variants present at severities 1, 2, and 3, equally weighted within source. Never deploy the bands as AI-quality labels. | Development fit plus held internal check; AI labels must remain `abstain`. |
| The intended audit exposed labels, boxes, truth, and repeated references. | Phase A uses shuffled cross-source A/B cases, exactly balanced candidate side, no labels/boxes/scores, and a truth-free response manifest. Phase B uses a separate answer key and unblinded overlay atlas. | 628 controlled cases across 157 sources. |
| Residual boxes were drawn on raw candidates although paired boxes live in a registered reference frame. | Route paired/reference-only residuals to the reference panel; candidate-only residuals to the candidate panel. Persist frame, side, and registration shift. | Visual QA of AI and controlled audit books. |
| Several augmentation names overstated realism. | Disclose that edge crops are white erasure, occlusions/substitution add black ink, typography redraws approximate Helvetica text, and many specialized targets are PDF heuristics. Treat mutation validity as a manual audit field. | Report validity and abstention counts; exclude invalid examples. |
| The AI corpus was presented as a model comparison. | Limit claims to the recorded `google/gemini-3.1-flash-lite` adaptive source-to-source pipeline: 156/157 stored compiled outputs, 126/127 prompt-heldout compiled outputs, no cross-model ranking. | Post-freeze descriptive scorecard; prompt and metric splits shown separately. |

## AI-corpus claim boundary

The current corpus contains one near-complete AI route. Prompt development has
30 sources; prompt heldout has 127. The heldout conversion pipeline selected
the earliest successful output from v1, targeted v2, and v3 rescue stages; v2
and v3 were designed after earlier failure patterns were observed. The result
is an adaptive rescue-pipeline audit, not a frozen single-prompt benchmark.

The strongest reference subset jointly marked prompt-heldout and metric-test
contains 30 compiled candidates. This separation does not remove the adaptive
prompt-development history, so it remains descriptive. Page canvas is a major
confound: 147 references are Letter and 10 A4, while 154 compiled candidates
are A4 and 2 Letter; only 11/156 full page-size sequences match.

## Stopping rule

The final report may call a projection `verified` only after the corrected
all-source validation, exact repeat run, and manual mutation-validity audit all
pass their stated gates. Otherwise it is `trial`. Unsupported specialized
modules remain `abstaining` or `not_implemented`. No failure is converted to a
zero score, hidden in an average, or repaired using held results.
