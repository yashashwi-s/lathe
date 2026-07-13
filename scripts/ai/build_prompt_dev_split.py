"""Build the frozen 33-sample prompt-development split.

Three samples are selected from every category at low, middle, and high
within-category complexity. Complexity uses only source/reference properties and
deterministic converter outcomes; it never uses AI model results.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data" / "latex_benchmark_v0"
DEFAULT_OUT = DATASET / "splits" / "prompt_dev_33.csv"

TARGETS = (("low", 0.15), ("medium", 0.50), ("high", 0.85))
STRUCTURAL_PATTERN = re.compile(
    r"\\(?:begin|section|subsection|paragraph|item|caption|label|ref|cite|"
    r"footnote|multicolumn|cline|includegraphics|bibliography)\b|"
    r"\\\[|\\\]|\\\(|\\\)|\$\$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--engine-manifest", type=Path,
                        default=ROOT / "results" / "latex_benchmark_v0" / "engine_manifest.csv")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def minmax(value: float, values: list[float]) -> float:
    lo, hi = min(values), max(values)
    return 0.0 if hi == lo else (value - lo) / (hi - lo)


def load_engine_failures(path: Path) -> dict[str, int]:
    failures: dict[str, int] = defaultdict(int)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row["compile_status"] != "ok":
                failures[row["sample_id"]] += 1
    return failures


def build_rows(dataset: Path, engine_manifest: Path) -> list[dict[str, object]]:
    failures = load_engine_failures(engine_manifest)
    accepted = list(csv.DictReader((dataset / "accepted_manifest.csv").open(newline="")))
    by_category: dict[str, list[dict[str, object]]] = defaultdict(list)

    for row in accepted:
        sample_dir = ROOT / row["sample_dir"]
        source = (sample_dir / "main.tex").read_text(errors="replace")
        provenance = json.loads((sample_dir / "provenance.json").read_text())
        by_category[row["category"]].append({
            **row,
            "source_path": str((sample_dir / "main.tex").relative_to(ROOT)),
            "reference_pdf": str((sample_dir / "reference.pdf").relative_to(ROOT)),
            "structural_constructs": len(STRUCTURAL_PATTERN.findall(source)),
            "engine_failures": failures.get(row["sample_id"], 0),
            "source_dataset": provenance.get("source_dataset", row["source_dataset"]),
        })

    selected: list[dict[str, object]] = []
    for category in sorted(by_category):
        rows = by_category[category]
        chars = [float(row["source_chars"]) for row in rows]
        lines = [float(row["nonblank_lines"]) for row in rows]
        pages = [float(row["page_count"]) for row in rows]
        constructs = [float(row["structural_constructs"]) for row in rows]
        for row in rows:
            row["complexity_score"] = (
                0.30 * minmax(float(row["source_chars"]), chars)
                + 0.15 * minmax(float(row["nonblank_lines"]), lines)
                + 0.25 * minmax(float(row["structural_constructs"]), constructs)
                + 0.15 * minmax(float(row["page_count"]), pages)
                + 0.15 * (float(row["engine_failures"]) / 3.0)
            )
        rows.sort(key=lambda item: (float(item["complexity_score"]), str(item["sample_id"])))

        used: set[str] = set()
        for band, target in TARGETS:
            target_index = round(target * (len(rows) - 1))
            candidates = sorted(
                enumerate(rows),
                key=lambda pair: (abs(pair[0] - target_index), pair[0], str(pair[1]["sample_id"])),
            )
            _, chosen = next(pair for pair in candidates if str(pair[1]["sample_id"]) not in used)
            used.add(str(chosen["sample_id"]))
            selected.append({
                "sample_id": chosen["sample_id"],
                "category": category,
                "complexity_band": band,
                "complexity_score": f"{float(chosen['complexity_score']):.6f}",
                "page_count": chosen["page_count"],
                "source_chars": chosen["source_chars"],
                "nonblank_lines": chosen["nonblank_lines"],
                "structural_constructs": chosen["structural_constructs"],
                "deterministic_engine_failures": chosen["engine_failures"],
                "source_family": chosen["source_family"],
                "source_dataset": chosen["source_dataset"],
                "source_ids": chosen["source_ids"],
                "source_path": chosen["source_path"],
                "reference_pdf": chosen["reference_pdf"],
                "selection_basis": f"closest to within-category {target:.0%} complexity quantile",
            })
    return selected


def write_readme(path: Path, rows: list[dict[str, object]]) -> None:
    counts = defaultdict(int)
    for row in rows:
        counts[str(row["complexity_band"])] += 1
    text = f"""# Prompt-development split

This directory contains the frozen development split used to improve the
LaTeX-to-Typst system prompt before the held-out benchmark is run.

## Split contract

- Total samples: {len(rows)}
- Categories: {len({row['category'] for row in rows})}
- Samples per category: 3
- Complexity bands: low={counts['low']}, medium={counts['medium']}, high={counts['high']}
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
"""
    path.write_text(text)


def main() -> None:
    args = parse_args()
    rows = build_rows(args.dataset.resolve(), args.engine_manifest.resolve())
    if len(rows) != 33:
        raise SystemExit(f"expected 33 selected samples, found {len(rows)}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_readme(args.out.parent / "README.md", rows)
    print(f"wrote {len(rows)} samples to {args.out}")


if __name__ == "__main__":
    main()

