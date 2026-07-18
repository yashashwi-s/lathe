#!/usr/bin/env python3
"""Merge disjoint augmentation batches and reject incomplete or duplicate runs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ROOT = ROOT / "results" / "metric_research_v1" / "full_157_v1"
DEFAULT_PROFILE = ROOT / "results" / "metric_research_v1" / "corpus_profile_157.csv"


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def merge_batches(batch_files: list[Path], expected_samples: set[str],
                  expected_cases: int) -> tuple[list[str], list[dict[str, str]], dict]:
    fields: list[str] = []
    rows: list[dict[str, str]] = []
    batch_counts = {}
    for path in batch_files:
        current_fields, current_rows = _read(path)
        if fields and current_fields != fields:
            raise ValueError(f"field mismatch in {path}")
        fields = current_fields
        rows.extend(current_rows)
        batch_counts[str(path)] = len(current_rows)

    variant_ids = [row["variant_id"] for row in rows]
    duplicates = [key for key, count in Counter(variant_ids).items() if count > 1]
    if duplicates:
        raise ValueError(f"duplicate variant_id values: {duplicates[:5]}")
    actual_samples = {row["sample_id"] for row in rows}
    if actual_samples != expected_samples:
        missing = sorted(expected_samples - actual_samples)
        extra = sorted(actual_samples - expected_samples)
        raise ValueError(f"sample coverage mismatch; missing={missing}, extra={extra}")
    if len(rows) != expected_cases:
        raise ValueError(f"expected {expected_cases} rows, found {len(rows)}")

    rows.sort(key=lambda row: (
        row["category"], row["sample_id"], row["family"], row.get("variant", ""),
        int(float(row["severity"])), row["variant_id"],
    ))
    summary = {
        "method": "merge_metric_batches_v1",
        "batch_counts": batch_counts,
        "cases": len(rows),
        "unique_variant_ids": len(set(variant_ids)),
        "source_documents": len(actual_samples),
        "status_counts": dict(Counter(row["status"] for row in rows)),
        "applicable_counts": dict(Counter(row["applicable"] for row in rows)),
        "retained_audit_candidates": sum(bool(row.get("candidate_pdf")) for row in rows),
    }
    return fields, rows, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, action="append", required=True)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--expected-cases", type=int, default=16_167)
    parser.add_argument("--output", type=Path, default=DEFAULT_ROOT / "augmentation_results.csv")
    args = parser.parse_args()

    _, profile = _read(args.profile)
    fields, rows, summary = merge_batches(
        args.batch, {row["sample_id"] for row in profile}, args.expected_cases,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary_path = args.output.with_name("merged_run_summary.json")
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
