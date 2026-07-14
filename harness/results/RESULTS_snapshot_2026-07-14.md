# Results — methods × metrics on the hardest samples

All fidelity metrics are 0–100. Content/layout/typography/pagination are
pdf_fidelity_v0.1; **raster is raster_v0.2** (see `raster_v2.py`) — a
rescoring of the *same stored PDFs* (no reruns) with ±4 px ink tolerance,
softer edge decay, and the dead foreground-SSIM term dropped. Overall is
recombined with the unchanged v0.1 weights. Gates = frozen pass criteria
from README (G1 compile, G2 pagination, G3 token P/R ≥ .95, G4 layout ≥ 75;
gates don't depend on raster, so pass/fail is unchanged).

Metric bounds to read scores against:

- **Theoretical range** 0–100 for every component; 100 = identical PDF.
- **raster_v0.2 calibration:** identity = 100; a uniform 8 px whole-page
  shift ≈ 96; vs a blank page = 0. The old v0.1 ceiling (~25–30 for
  faithful conversions) was diagnosed as metric harshness, not fonts:
  candidates already embed New Computer Modern (per-word registered ink
  F1 ≈ 0.84 vs the pdfLaTeX reference), while v0.1's foreground SSIM sat
  at ≈ 0.03 for every real pair and its ±2 px ink tolerance was below
  unavoidable cross-engine drift. Best observed raster_v0.2 so far: 78.9.
- **Lower anchor:** the one-shot gemini flash-lite baseline row.

Total tracked spend so far: **$69.18**
(agentic + 1-turn runs with cost capture).

## Aggregate — core 6 hard samples

| model | effort | feedback | harness | overall | content | layout | typography | raster | pagination | pass | $/run | min/run | iters |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opus-4.7 | ⚡⚡ | 👁 | v3 | **81.6** | 95.0 | 80.6 | 83.5 | **58.9** | 100.0 | 2/6 | 1.18 | 3.6 | 9 |
| opus-4.7 | ⚡⚡ | 👁 | v2 | 78.2 | 96.4 | 77.2 | 83.7 | 51.7 | 99.1 | 3/6 | 1.30 | 4.2 | 8 |
| opus-4.7 | ⚡⚡⚡ | ✗ | v1 | (76.6) | (96.9) | (82.8) | (87.7) | (42.8) | (100.0) | 2/4 | 2.45 | 7.6 | 18 |
| opus-4.7 | ⚡⚡⚡ | 👁 | v1 | (76.0) | (96.9) | (77.4) | (83.6) | (42.3) | (100.0) | 3/5 | 2.65 | 8.4 | 15 |
| opus-4.7 | ⚡⚡ | 👁 | v1 | 75.1 | 96.6 | 71.4 | 81.5 | 46.8 | 99.7 | 2/6 | 1.53 | 4.4 | 10 |
| sonnet-4.6 | ⚡ | 👁 | v1 | 70.6 | 95.6 | 67.7 | 78.7 | 38.0 | 100.0 | 0/6 | 1.84 | 12.5 | 20 |
| opus-4.7 | ⚡ | 👁 | v1 | (69.9) | (95.3) | (71.7) | (77.8) | (33.5) | (100.0) | 1/2 | — | — | — |
| sonnet-4.6 | ⚡ | ✗ | v1 | (67.5) | (93.8) | (68.9) | (84.5) | (30.2) | (100.0) | 0/5 | 0.99 | 6.8 | 13 |
| opus-4.7 | ⚡⚡ | ✗ | v1 | 67.4 | 94.7 | 70.5 | 81.5 | 28.6 | 100.0 | 0/6 | **0.88** | 2.8 | 8 |
| opus-4.7 | ⚡ | ✗ | v1 | 66.8 | 94.1 | 65.0 | 84.6 | 32.7 | 92.5 | 2/6 | — | — | — |
| sonnet-4.6 | ⚡ | 1-turn | — | (43.4) | (90.1) | (34.4) | (76.2) | (10.4) | (65.4) | 0/6 | 0.10 | 0.6 | — |
| opus-4.7 | ⚡ | 1-turn | — | (41.5) | (89.4) | (34.0) | (71.4) | (9.6) | (60.0) | 0/6 | — | — | — |
| gemini-3.1-flash-lite | — | 1-turn | — | 37.0 | 83.5 | 30.6 | 76.1 | 7.3 | 56.9 | 0/6 | — | — | — |

Legend: feedback 👁 = visual diffs available, ✗ = blind (numeric metrics only), 1-turn = single prompt no tools; effort ⚡/⚡⚡/⚡⚡⚡ = low/medium/high reasoning; harness v2 adds checkpointing + sweep + fine-grained feedback; v3 additionally feeds raster_v0.2 + registered-raster into the mid-run loop (same number as final grading). Parenthesized = partial coverage (mean over samples scored so far); **bold** = best fully-covered method per column; nc = nothing compiled; $/run is the CLI's own accounting (— = cost not captured).

## Aggregate — extended set (core 6 + 2 math)

Only 1-turn methods cover the 2 extra math samples so far.

| model | effort | feedback | harness | overall | content | layout | typography | raster | pagination | pass | $/run | min/run | iters |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| opus-4.7 | ⚡⚡ | 👁 | v3 | (81.6) | (95.0) | (80.6) | (83.5) | (58.9) | (100.0) | 2/6 | 1.18 | 3.6 | 9 |
| opus-4.7 | ⚡⚡ | 👁 | v2 | (78.2) | (96.4) | (77.2) | (83.7) | (51.7) | (99.1) | 3/6 | 1.30 | 4.2 | 8 |
| opus-4.7 | ⚡⚡⚡ | ✗ | v1 | (76.6) | (96.9) | (82.8) | (87.7) | (42.8) | (100.0) | 2/4 | 2.45 | 7.6 | 18 |
| opus-4.7 | ⚡⚡⚡ | 👁 | v1 | (76.0) | (96.9) | (77.4) | (83.6) | (42.3) | (100.0) | 3/5 | 2.65 | 8.4 | 15 |
| opus-4.7 | ⚡⚡ | 👁 | v1 | (75.1) | (96.6) | (71.4) | (81.5) | (46.8) | (99.7) | 2/6 | 1.53 | 4.4 | 10 |
| sonnet-4.6 | ⚡ | 👁 | v1 | (70.6) | (95.6) | (67.7) | (78.7) | (38.0) | (100.0) | 0/6 | 1.84 | 12.5 | 20 |
| opus-4.7 | ⚡ | 👁 | v1 | (69.9) | (95.3) | (71.7) | (77.8) | (33.5) | (100.0) | 1/2 | — | — | — |
| sonnet-4.6 | ⚡ | ✗ | v1 | (67.5) | (93.8) | (68.9) | (84.5) | (30.2) | (100.0) | 0/5 | 0.99 | 6.8 | 13 |
| opus-4.7 | ⚡⚡ | ✗ | v1 | (67.4) | (94.7) | (70.5) | (81.5) | (28.6) | (100.0) | 0/6 | 0.88 | 2.8 | 8 |
| opus-4.7 | ⚡ | ✗ | v1 | (66.8) | (94.1) | (65.0) | (84.6) | (32.7) | (92.5) | 2/6 | — | — | — |
| opus-4.7 | ⚡ | 1-turn | — | (45.5) | (86.0) | (42.2) | (75.6) | (11.9) | (65.5) | 0/8 | — | — | — |
| sonnet-4.6 | ⚡ | 1-turn | — | (44.0) | (88.4) | (38.1) | (77.5) | (10.2) | (64.3) | 0/8 | 0.09 | 0.5 | — |
| gemini-3.1-flash-lite | — | 1-turn | — | 39.9 | 81.8 | 36.4 | 78.3 | 8.2 | 62.5 | 0/8 | — | — | — |

Legend: feedback 👁 = visual diffs available, ✗ = blind (numeric metrics only), 1-turn = single prompt no tools; effort ⚡/⚡⚡/⚡⚡⚡ = low/medium/high reasoning; harness v2 adds checkpointing + sweep + fine-grained feedback; v3 additionally feeds raster_v0.2 + registered-raster into the mid-run loop (same number as final grading). Parenthesized = partial coverage (mean over samples scored so far); **bold** = best fully-covered method per column; nc = nothing compiled; $/run is the CLI's own accounting (— = cost not captured).

## Per-sample breakdown

### `06_tables_moderate_010`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus agentic (visual, effort medium) [v3] | **86.4** | 99.9 | 88.4 | 88.2 | 60.6 | 100.0 | 2/2 | 1.000/0.997 | PASS | 0.66 |
| claude opus agentic (novisual, effort high) | 80.3 | 98.0 | 83.6 | 85.0 | 47.6 | 100.0 | 2/2 | 0.999/0.996 | PASS | 2.60 |
| claude opus agentic (visual, effort high) | 77.7 | 99.5 | 76.1 | 91.6 | 42.2 | 100.0 | 2/2 | 1.000/1.000 | PASS | 2.93 |
| claude opus agentic (novisual, effort low) | 76.9 | 97.8 | 77.8 | 89.9 | 40.7 | 100.0 | 2/2 | 0.991/0.991 | PASS | — |
| claude opus agentic (visual, effort medium) | 74.1 | 99.8 | 69.2 | 80.9 | 40.9 | 98.0 | 2/2 | 1.000/0.996 | FAIL(G2) | 2.65 |
| claude opus agentic (visual, effort medium) [v2] | 74.1 | 97.6 | 68.9 | 84.7 | 41.2 | 100.0 | 2/2 | 0.991/0.991 | FAIL(G4) | 0.69 |
| claude sonnet agentic (visual, effort low) | 72.8 | 98.6 | 68.5 | 75.1 | 40.3 | 100.0 | 2/2 | 1.000/0.996 | FAIL(G4) | 1.86 |
| claude sonnet agentic (novisual, effort low) | 72.5 | 98.0 | 72.2 | 88.4 | 33.4 | 100.0 | 2/2 | 0.997/0.994 | FAIL(G4) | 0.70 |
| claude opus agentic (novisual, effort medium) | 69.3 | 98.7 | 68.0 | 77.1 | 31.0 | 100.0 | 2/2 | 0.997/0.994 | FAIL(G4) | 1.12 |
| claude sonnet 1-turn (effort low) | 39.0 | 96.3 | 26.1 | 85.0 | 7.3 | 47.9 | 2/3 | 1.000/0.996 | FAIL(G2) | 0.18 |
| claude opus 1-turn (effort low) | 39.0 | 98.4 | 26.1 | 71.6 | 7.9 | 47.8 | 2/3 | 1.000/0.996 | FAIL(G2) | — |
| gemini-3.1-flash-lite (1-turn cascade) | 32.4 | 83.0 | 23.8 | 73.3 | 4.6 | 48.2 | 2/3 | 0.925/0.884 | FAIL(G2) | — |

### `05_tables_simple_023`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus agentic (visual, effort medium) [v2] | **73.3** | 98.2 | 81.7 | 83.1 | 31.1 | 100.0 | 3/3 | 0.998/0.970 | PASS | 2.83 |
| claude opus agentic (visual, effort high) | 73.2 | 100.0 | 82.1 | 87.8 | 28.7 | 100.0 | 3/3 | 1.000/1.000 | PASS | 2.92 |
| claude opus agentic (novisual, effort medium) | 70.5 | 91.0 | 79.4 | 80.2 | 31.1 | 100.0 | 3/3 | 0.868/0.989 | FAIL(G3) | 2.16 |
| claude opus agentic (novisual, effort low) | 68.4 | 91.2 | 79.2 | 87.4 | 25.2 | 100.0 | 3/3 | 0.874/0.991 | FAIL(G3) | — |
| claude sonnet agentic (novisual, effort low) | 68.3 | 91.8 | 73.1 | 88.6 | 27.2 | 100.0 | 3/3 | 0.871/0.989 | FAIL(G3) | 2.71 |
| claude opus agentic (visual, effort medium) [v3] | 64.4 | 88.2 | 57.0 | 67.1 | 36.1 | 100.0 | 3/3 | 0.842/0.962 | FAIL(G3) | 1.44 |
| claude opus agentic (novisual, effort high) | 63.7 | 92.8 | 66.5 | 85.9 | 21.6 | 100.0 | 3/3 | 0.875/0.994 | FAIL(G3) | 1.29 |
| claude sonnet agentic (visual, effort low) | 61.4 | 92.8 | 55.7 | 66.6 | 26.9 | 100.0 | 3/3 | 0.875/0.994 | FAIL(G3) | 2.69 |
| claude sonnet 1-turn (effort low) | 59.1 | 92.1 | 60.1 | 77.9 | 18.2 | 100.0 | 3/3 | 0.874/0.991 | FAIL(G3) | 0.09 |
| claude opus agentic (visual, effort low) | 57.9 | 92.8 | 52.8 | 64.4 | 21.8 | 100.0 | 3/3 | 0.875/0.994 | FAIL(G3) | — |
| claude opus agentic (visual, effort medium) | 56.6 | 92.8 | 53.3 | 70.4 | 18.1 | 100.0 | 3/3 | 0.875/0.994 | FAIL(G3) | 2.48 |
| claude opus 1-turn (effort low) | 35.4 | 92.1 | 26.4 | 64.1 | 5.6 | 50.4 | 3/2 | 0.874/0.991 | FAIL(G2) | — |
| gemini-3.1-flash-lite (1-turn cascade) | 33.7 | 83.9 | 25.6 | 77.6 | 4.8 | 50.1 | 3/2 | 0.780/0.885 | FAIL(G2) | — |

### `05_tables_simple_005`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus agentic (novisual, effort high) | **94.1** | 100.0 | 96.1 | 92.8 | 81.1 | 100.0 | 2/2 | 1.000/1.000 | PASS | 2.88 |
| claude opus agentic (visual, effort medium) [v2] | 90.8 | 99.4 | 87.7 | 89.9 | 78.9 | 100.0 | 2/2 | 0.993/0.992 | PASS | 0.98 |
| claude opus agentic (visual, effort medium) [v3] | 88.0 | 99.9 | 85.2 | 90.0 | 69.1 | 100.0 | 2/2 | 1.000/0.997 | PASS | 1.78 |
| claude opus agentic (novisual, effort low) | 82.9 | 99.9 | 78.5 | 87.5 | 57.8 | 100.0 | 2/2 | 1.000/0.997 | PASS | — |
| claude sonnet agentic (visual, effort low) | 80.7 | 99.8 | 72.4 | 87.5 | 56.2 | 100.0 | 2/2 | 1.000/0.995 | FAIL(G4) | 0.72 |
| claude sonnet agentic (novisual, effort low) | 79.7 | 99.5 | 69.7 | 87.4 | 55.8 | 100.0 | 2/2 | 1.000/0.995 | FAIL(G4) | 0.30 |
| claude opus agentic (visual, effort high) | 79.0 | 99.1 | 70.9 | 81.4 | 54.9 | 100.0 | 2/2 | 1.000/0.995 | FAIL(G4) | 1.65 |
| claude opus agentic (novisual, effort medium) | 77.2 | 99.2 | 66.6 | 83.2 | 52.4 | 100.0 | 2/2 | 0.993/0.992 | FAIL(G4) | 0.57 |
| claude opus agentic (visual, effort medium) | 71.3 | 99.9 | 58.2 | 90.1 | 38.9 | 100.0 | 2/2 | 1.000/0.997 | FAIL(G4) | 1.05 |
| claude sonnet 1-turn (effort low) | 38.4 | 86.4 | 24.8 | 65.2 | 10.1 | 52.5 | 2/3 | 0.917/0.952 | FAIL(G2) | 0.10 |
| claude opus 1-turn (effort low) | 38.0 | 86.9 | 24.6 | 65.1 | 9.6 | 53.5 | 2/3 | 0.942/0.965 | FAIL(G2) | — |
| gemini-3.1-flash-lite (1-turn cascade) | 37.3 | 86.9 | 23.2 | 65.1 | 9.5 | 52.6 | 2/3 | 0.935/0.962 | FAIL(G2) | — |

### `09_algorithms_003`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus agentic (visual, effort medium) | **87.9** | 96.8 | 92.0 | 85.4 | 67.9 | 100.0 | 2/2 | 0.969/0.954 | PASS | 1.00 |
| claude opus agentic (visual, effort medium) [v3] | 86.8 | 96.8 | 91.9 | 87.2 | 62.7 | 100.0 | 2/2 | 0.974/0.949 | FAIL(G3) | 0.59 |
| claude opus agentic (visual, effort medium) [v2] | 85.0 | 96.8 | 91.4 | 87.1 | 57.0 | 100.0 | 2/2 | 0.969/0.954 | PASS | 1.77 |
| claude opus agentic (visual, effort high) | 83.3 | 96.8 | 91.6 | 87.0 | 51.1 | 100.0 | 2/2 | 0.969/0.954 | PASS | 2.77 |
| claude sonnet agentic (visual, effort low) | 78.1 | 97.4 | 73.7 | 80.4 | 51.4 | 100.0 | 2/2 | 0.979/0.959 | FAIL(G4) | 2.18 |
| claude opus agentic (novisual, effort high) | 68.5 | 96.8 | 84.9 | 87.1 | 20.7 | 100.0 | 2/2 | 0.974/0.949 | FAIL(G3) | 3.01 |
| claude opus agentic (novisual, effort medium) | 61.8 | 94.9 | 71.2 | 80.8 | 16.9 | 100.0 | 2/2 | 0.973/0.938 | FAIL(G3) | 0.22 |
| claude sonnet agentic (novisual, effort low) | 58.8 | 94.2 | 73.7 | 84.8 | 12.2 | 100.0 | 2/2 | 0.953/0.938 | FAIL(G3) | 0.43 |
| claude opus 1-turn (effort low) | 56.5 | 75.9 | 66.7 | 82.5 | 17.1 | 100.0 | 2/2 | 0.945/0.615 | FAIL(G3) | — |
| claude opus agentic (novisual, effort low) | 46.6 | 94.1 | 36.7 | 85.3 | 10.1 | 79.9 | 2/2 | 0.939/0.949 | FAIL(G2) | — |
| claude sonnet 1-turn (effort low) | 42.4 | 90.4 | 34.4 | 80.8 | 7.7 | 78.2 | 2/2 | 0.891/0.877 | FAIL(G2) | 0.06 |
| gemini-3.1-flash-lite (1-turn cascade) | 36.5 | 82.0 | 32.1 | 84.8 | 5.5 | 42.2 | 2/1 | 0.959/0.723 | FAIL(G2) | — |

### `05_tables_simple_021`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus agentic (visual, effort medium) [v3] | **74.8** | 88.8 | 71.2 | 77.5 | 52.0 | 99.9 | 3/3 | 0.811/0.940 | FAIL(G2) | 2.01 |
| claude opus agentic (visual, effort medium) | 71.9 | 93.7 | 65.8 | 70.5 | 45.5 | 99.9 | 3/3 | 0.883/0.990 | FAIL(G3) | 1.51 |
| claude opus agentic (visual, effort high) | 66.9 | 88.9 | 66.3 | 70.4 | 34.5 | 99.9 | 3/3 | 0.812/0.943 | FAIL(G2) | 2.98 |
| claude opus agentic (novisual, effort medium) | 59.0 | 88.7 | 56.9 | 75.8 | 21.1 | 99.9 | 3/3 | 0.812/0.943 | FAIL(G2) | 0.84 |
| claude sonnet agentic (novisual, effort low) | 58.5 | 85.6 | 56.0 | 73.6 | 22.4 | 99.9 | 3/3 | 0.812/0.943 | FAIL(G2) | 0.82 |
| claude opus agentic (visual, effort medium) [v2] | 56.1 | 90.4 | 42.9 | 65.5 | 25.7 | 94.7 | 3/3 | 0.880/0.984 | FAIL(G2) | 0.76 |
| claude sonnet agentic (visual, effort low) | 54.2 | 88.8 | 52.2 | 71.4 | 15.9 | 99.9 | 3/3 | 0.812/0.943 | FAIL(G2) | 1.42 |
| claude opus agentic (novisual, effort low) | 43.9 | 85.4 | 29.0 | 66.0 | 14.8 | 75.0 | 3/3 | 0.804/0.938 | FAIL(G2) | — |
| gemini-3.1-flash-lite (1-turn cascade) | 41.3 | 83.2 | 24.6 | 67.4 | 15.9 | 48.2 | 3/2 | 0.807/0.940 | FAIL(G2) | — |
| claude opus 1-turn (effort low) | 38.6 | 93.7 | 26.1 | 73.5 | 8.0 | 48.2 | 3/2 | 0.887/0.991 | FAIL(G2) | — |
| claude sonnet 1-turn (effort low) | 37.9 | 85.5 | 26.4 | 72.2 | 8.6 | 48.3 | 3/2 | 0.812/0.943 | FAIL(G2) | 0.12 |

### `07_figures_captions_007`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus agentic (visual, effort medium) [v2] | **90.1** | 96.3 | 90.6 | 91.7 | 76.0 | 100.0 | 1/1 | 0.958/0.945 | FAIL(G3) | 0.79 |
| claude opus agentic (visual, effort medium) [v3] | 89.2 | 96.3 | 90.0 | 91.1 | 72.9 | 100.0 | 1/1 | 0.958/0.945 | FAIL(G3) | 0.60 |
| claude opus agentic (visual, effort medium) | 88.5 | 96.9 | 90.0 | 91.4 | 69.2 | 100.0 | 1/1 | 0.959/0.959 | PASS | 0.52 |
| claude opus agentic (novisual, effort low) | 81.9 | 96.3 | 88.9 | 91.7 | 47.8 | 100.0 | 1/1 | 0.958/0.945 | FAIL(G3) | — |
| claude opus agentic (visual, effort low) | 81.8 | 97.8 | 90.7 | 91.2 | 45.1 | 100.0 | 1/1 | 0.986/0.959 | PASS | — |
| claude sonnet agentic (visual, effort low) | 76.7 | 96.3 | 83.5 | 91.1 | 37.1 | 100.0 | 1/1 | 0.958/0.945 | FAIL(G3) | 2.17 |
| claude opus agentic (novisual, effort medium) | 66.6 | 95.7 | 80.6 | 91.8 | 19.0 | 100.0 | 1/1 | 0.958/0.932 | FAIL(G3) | 0.39 |
| gemini-3.1-flash-lite (1-turn cascade) | 41.0 | 81.7 | 54.5 | 88.6 | 3.6 | 100.0 | 1/1 | 0.787/0.808 | FAIL(G3) | — |
| claude opus 1-turn (effort low) | nc | nc | nc | nc | nc | nc | — | — | FAIL(G1) | — |
| claude sonnet 1-turn (effort low) | nc | nc | nc | nc | nc | nc | — | — | FAIL(G1) | 0.04 |

### `04_math_aligned_014`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus 1-turn (effort low) | **52.0** | 80.2 | 56.4 | 84.6 | 14.9 | 58.7 | 2/1 | 0.838/0.697 | FAIL(G2) | — |
| claude sonnet 1-turn (effort low) | 47.4 | 79.5 | 57.0 | 84.3 | 9.3 | 58.7 | 2/1 | 0.837/0.693 | FAIL(G2) | 0.06 |
| gemini-3.1-flash-lite (1-turn cascade) | 46.6 | 79.0 | 47.3 | 82.8 | 11.2 | 58.8 | 2/1 | 0.837/0.693 | FAIL(G2) | — |

### `03_math_inline_display_004`

| method | overall | content | layout | typography | raster | pagination | pages | token P/R | gates | $ |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| claude opus 1-turn (effort low) | **59.2** | 75.2 | 69.1 | 87.4 | 20.4 | 100.0 | 1/1 | 0.773/0.652 | FAIL(G3) | — |
| gemini-3.1-flash-lite (1-turn cascade) | 50.3 | 74.7 | 60.3 | 86.5 | 10.7 | 100.0 | 1/1 | 0.772/0.646 | FAIL(G3) | — |
| claude sonnet 1-turn (effort low) | nc | nc | nc | nc | nc | nc | — | — | FAIL(G1) | 0.06 |

