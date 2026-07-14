"""Freeze the final failures from one AI run as a retry-experiment split."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE_SPLIT = ROOT / "data" / "latex_benchmark_v0" / "splits" / "prompt_dev_33.csv"
DEFAULT_RUN_MANIFEST = (
    ROOT / "results" / "ai_latex_to_typst" / "openrouter"
    / "google_gemini-3.1-flash-lite" / "prompt_v0" / "run_manifest.csv"
)
DEFAULT_OUT = (
    ROOT / "data" / "latex_benchmark_v0" / "splits"
    / "prompt_v1_v0_failures_10.csv"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-split", type=Path, default=DEFAULT_SOURCE_SPLIT)
    parser.add_argument("--run-manifest", type=Path, default=DEFAULT_RUN_MANIFEST)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_rows = list(csv.DictReader(args.source_split.open(newline="")))
    outcomes = {row["sample_id"]: row for row in csv.DictReader(args.run_manifest.open(newline=""))}
    failed = [
        row for row in source_rows
        if outcomes.get(row["sample_id"], {}).get("final_compiled") == "False"
    ]
    if not failed:
        raise SystemExit("source run has no final compilation failures")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(failed[0]))
        writer.writeheader()
        writer.writerows(failed)
    print(f"wrote {len(failed)} frozen failures to {args.out}")


if __name__ == "__main__":
    main()

