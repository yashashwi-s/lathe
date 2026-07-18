#!/usr/bin/env python3
"""Summarize raw metric-v2 components without constructing an aggregate score."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


METRICS = {
    "strict_word_f1": "higher_is_better",
    "strict_document_edit_similarity": "higher_is_better",
    "compatibility_word_f1": "higher_is_better",
    "token_center_displacement_q90": "lower_is_better",
    "token_bbox_iou_q10": "higher_is_better",
    "text_ltsim_page_macro": "higher_is_better",
    "text_ltsim_worst_page": "higher_is_better",
    "block_transport_geometry_similarity": "higher_is_better_adaptation",
    "reading_order_tau": "higher_is_better_conditional",
    "style_coverage_hmean": "higher_is_better_diagnostic",
    "font_size_log_error_q90": "lower_is_better_diagnostic",
    "baseline_displacement_q90": "lower_is_better_diagnostic",
    "unregistered_ink_f1": "higher_is_better_raster_diagnostic",
    "unregistered_ssim": "higher_is_better_raster_diagnostic",
    "unregistered_multiscale_ssim_diagnostic": "higher_is_better_raster_diagnostic",
    "page_count_delta": "zero_is_best",
    "page_break_f1": "higher_is_better",
    "canvas_exact_size_rate": "one_is_exact",
}


def _number(value: str) -> float | None:
    if value == "":
        return None
    try:
        result = float(value)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def _stats(rows: list[dict[str, str]], name: str) -> dict[str, Any]:
    values = [_number(row.get(name, "")) for row in rows]
    numeric = np.asarray([value for value in values if value is not None], dtype=np.float64)
    if not len(numeric):
        return {"direction": METRICS[name], "count": 0, "abstained_or_missing": len(rows)}
    return {
        "direction": METRICS[name],
        "count": int(len(numeric)),
        "abstained_or_missing": len(rows) - int(len(numeric)),
        "q10": float(np.quantile(numeric, 0.10)),
        "median": float(np.median(numeric)),
        "q90": float(np.quantile(numeric, 0.90)),
        "min": float(numeric.min()),
        "max": float(numeric.max()),
    }


def _critical(rows: list[dict[str, str]], name: str) -> dict[str, Any]:
    applicable = []
    for row in rows:
        left = _number(row.get(f"reference_{name}_count", ""))
        right = _number(row.get(f"candidate_{name}_count", ""))
        if left is None or right is None or (left == 0 and right == 0):
            continue
        exact = row.get(f"{name}_exact", "").strip().lower()
        if exact in {"true", "false"}:
            applicable.append(exact == "true")
    return {
        "applicable_pairs": len(applicable),
        "exact_pairs": sum(applicable),
        "exact_rate": sum(applicable) / len(applicable) if applicable else None,
    }


def _summarize_group(rows: list[dict[str, str]]) -> dict[str, Any]:
    page_exact = []
    for row in rows:
        delta = _number(row.get("page_count_delta", ""))
        if delta is not None:
            page_exact.append(abs(delta) < 1e-12)
    return {
        "pairs": len(rows),
        "scored": sum(row.get("v2_status") == "scored" for row in rows),
        "failed": sum(row.get("v2_status") != "scored" for row in rows),
        "page_count_exact_rate": sum(page_exact) / len(page_exact) if page_exact else None,
        "ssim_scored_pairs": sum(_number(row.get("unregistered_ssim", "")) is not None for row in rows),
        "specialized_status_counts": {
            axis: dict(Counter(row.get(f"{axis}_status", "") for row in rows))
            for axis in ("table", "formula", "figure")
        },
        "critical_inventories": {
            name: _critical(rows, name) for name in ("number", "operator", "citation")
        },
        "metrics": {name: _stats(rows, name) for name in METRICS},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path)
    parser.add_argument("--group-field")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with args.scores.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("score table is empty")
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    if args.group_field:
        for row in rows:
            groups[row.get(args.group_field, "unknown")].append(row)
    else:
        groups["all"] = rows
    result = {
        "summarizer": "summarize_metric_v2_scores",
        "source": str(args.scores.resolve()),
        "aggregate_score": None,
        "group_field": args.group_field,
        "groups": {name: _summarize_group(group) for name, group in sorted(groups.items())},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
