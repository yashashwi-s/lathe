# Publication benchmark scorecard v0

This is the primary frozen 127-reference held-out comparison. Gemini uses only the source-only `prompt_v1_heldout_clean` run. Its first pass and cumulative result after at most one compiler-error repair are reported separately. Claude and the adaptive v0/v2/v3 cascade are excluded.

## Compile and exact-document outcomes

| System | Compiled / 127 | Page count exact / 127 | Canvas exact / compiled |
|---|---:|---:|---:|
| Gemini 3.1 Flash Lite — first pass | 46/127 (36.2%) | 41/127 | 2/46 |
| Gemini 3.1 Flash Lite — after ≤1 repair | 77/127 (60.6%) | 70/127 | 2/77 |
| Pandoc | 124/127 (97.6%) | 81/127 | 0/124 |
| Tylax | 75/127 (59.1%) | 39/127 | 0/75 |
| TypeTeX | 120/127 (94.5%) | 79/127 | 0/120 |

## Fidelity medians on compiled PDFs

| System | Strict text F1 ↑ | NFKC text F1 ↑ | Reference coverage ↑ | Center q90 ↓ | Text-LTSim ↑ | SSIM ↑ (eligible n) |
|---|---:|---:|---:|---:|---:|---:|
| Gemini 3.1 Flash Lite — first pass | 0.905 | 0.922 | 0.919 | 0.284 | 0.701 | 0.669 (2) |
| Gemini 3.1 Flash Lite — after ≤1 repair | 0.870 | 0.879 | 0.876 | 0.295 | 0.704 | 0.669 (2) |
| Pandoc | 0.479 | 0.587 | 0.520 | 0.252 | 0.672 | — (0) |
| Tylax | 0.512 | 0.512 | 0.489 | 0.142 | 0.708 | — (0) |
| TypeTeX | 0.495 | 0.621 | 0.554 | 0.273 | 0.672 | — (0) |

## Reading the table

Compilation and exact-page counts always retain all 127 references. Fidelity medians are conditional on that system producing a compiled PDF, so they are not a paired ranking and are never collapsed into one overall score. SSIM abstains when page canvas sizes are incompatible.

Split text SHA-256: `bdf928c6a69745477523f25a83cec89d417c875ce6edf910f19a2364a467f1cc`  
System prompt SHA-256: `0877384cc89636ecbb3cf27b41de3201d9d9a483d8a6aba120a771cb8b4af08d`  
Metric: `pdf_metric_axes_v2` at 96 DPI.

Exact per-reference statuses, hashes, metrics, and evidence paths are in `per_sample_scores.csv`; complete protocol hashes and validation gates are in `scorecard.json`.
