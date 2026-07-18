#!/usr/bin/env python3
"""Fail-closed identity validation for a metric-v2 score table."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def _values(rows: list[dict[str, str]], name: str) -> list[float]:
    values = []
    for row in rows:
        value = row.get(name, "")
        if value == "":
            raise ValueError(f"missing {name} for {row.get('sample_id', 'unknown')}")
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"non-finite {name} for {row.get('sample_id', 'unknown')}")
        values.append(number)
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.scores.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("identity table is empty")
    word_field = "strict_word_f1" if rows[0].get("strict_word_f1", "") != "" else "word_f1"
    checks = {
        "all_rows_scored": all(row.get("v2_status") == "scored" for row in rows),
        "word_f1_exact": min(_values(rows, word_field)) == 1.0,
        "token_center_displacement_exact": max(_values(rows, "token_center_displacement_q90")) == 0.0,
        "text_ltsim_exact": min(_values(rows, "text_ltsim_page_macro")) == 1.0,
        "block_transport_exact": min(_values(rows, "block_transport_combined_similarity")) == 1.0,
        "ink_f1_exact": min(_values(rows, "unregistered_ink_f1")) == 1.0,
        "ssim_exact": min(_values(rows, "unregistered_ssim")) == 1.0,
        "page_count_delta_exact": max(abs(value) for value in _values(rows, "page_count_delta")) == 0.0,
        "canvas_exact": min(_values(rows, "canvas_exact_size_rate")) == 1.0,
    }
    result = {
        "validator": "validate_metric_v2_identity",
        "documents": len(rows),
        "unique_documents": len({row.get("sample_id") for row in rows}),
        "checks": checks,
        "status": "pass" if all(checks.values()) else "fail",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
