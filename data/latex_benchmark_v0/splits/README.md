# Prompt-development split

This directory contains the frozen development split used to improve the
LaTeX-to-Typst system prompt before the held-out benchmark is run.

## Split contract

- Total samples: 33
- Categories: 11
- Samples per category: 3
- Complexity bands: low=11, medium=11, high=11
- AI outputs are not used during selection.
- These samples are development data and must not contribute to final held-out
  benchmark claims.

## Selection method

Samples are ranked within each category using a documented complexity score:

| Component | Weight |
|---|---:|
| Source characters | 0.30 |
| Structural LaTeX constructs | 0.25 |
| Nonblank source lines | 0.15 |
| Reference page count | 0.15 |
| Failed deterministic Typst engines | 0.15 |

The selected rows are closest to the 15th, 50th, and 85th percentile rank in
each category. The score is only meaningful within a category.

`prompt_dev_33.csv` is the canonical ordered manifest. Rebuilding it with the
same dataset and deterministic engine manifest must produce the same rows.
