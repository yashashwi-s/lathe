#!/usr/bin/env python3
"""Build a metric-v2 PDF-pair manifest for one OpenRouter conversion run."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIELDS = [
    "comparison_id",
    "sample_id",
    "category",
    "requested_model",
    "resolved_model",
    "protocol",
    "reference_pdf",
    "candidate_pdf",
]


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.resolve()
    output = args.out.resolve() if args.out else run_dir / "metric_v2_pairs.csv"
    rows = []
    for meta_path in sorted((run_dir / "samples").glob("*/meta.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        candidate = meta_path.parent / "output.pdf"
        if not meta.get("final_compiled") or not candidate.exists():
            continue
        rows.append({
            "comparison_id": f"{meta['sample_id']}__gemini_flash_final",
            "sample_id": meta["sample_id"],
            "category": meta["category"],
            "requested_model": meta.get("requested_model", ""),
            "resolved_model": meta.get("resolved_model", ""),
            "protocol": "Claude-baseline-derived visual prompt; at most one compiler repair",
            "reference_pdf": meta["reference_pdf"],
            "candidate_pdf": relative(candidate),
        })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"metric pairs: {len(rows)}")
    print(f"manifest: {relative(output)}")


if __name__ == "__main__":
    main()
