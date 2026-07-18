#!/usr/bin/env python3
"""Validate Text-LTSim severity response for all-157 block displacements."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import kendalltau


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _bool(value: str) -> bool | None:
    value = (value or "").strip().lower()
    if value in {"true", "yes", "1"}:
        return True
    if value in {"false", "no", "0"}:
        return False
    return None


def _summary(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        return {"documents": 0}
    drops = np.asarray([float(row["score_drop_s1_to_s3"]) for row in rows])
    taus = [float(row["kendall_tau_severity_vs_score"]) for row in rows]
    return {
        "documents": len(rows),
        "adjacent_nonincreasing_rate": sum(bool(row["adjacent_nonincreasing"]) for row in rows) / len(rows),
        "strict_total_decrease_rate": sum(bool(row["strict_total_decrease"]) for row in rows) / len(rows),
        "kendall_tau_document_macro": sum(taus) / len(taus),
        "score_drop_s1_to_s3": {
            "q10": float(np.quantile(drops, 0.10)),
            "median": float(np.median(drops)),
            "q90": float(np.quantile(drops, 0.90)),
            "min": float(drops.min()),
            "max": float(drops.max()),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_csv", nargs="+", type=Path)
    parser.add_argument("--manual-manifest", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    rows = [row for path in args.batch_csv for row in _read(path)]
    rows = [row for row in rows if row.get("variant") == "block_right"]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("status") != "applied":
            raise ValueError(f"unscored block_right row: {row}")
        grouped[row["sample_id"]].append(row)
    if len(grouped) != 157 or len(rows) != 471:
        raise ValueError(f"expected 157 documents / 471 rows, found {len(grouped)} / {len(rows)}")

    manual = {
        row["sample_id"]: row
        for row in _read(args.manual_manifest)
        if row.get("variant") == "block_right"
    }
    if len(manual) != 157:
        raise ValueError(f"expected 157 manual block_right rows, found {len(manual)}")

    details = []
    for sample_id, group in sorted(grouped.items()):
        by_severity = {int(row["severity"]): float(row["axis_layout"]) for row in group}
        if set(by_severity) != {1, 2, 3}:
            raise ValueError(f"{sample_id}: severities are not 1,2,3")
        scores = [by_severity[severity] for severity in (1, 2, 3)]
        tau_raw = float(kendalltau([1, 2, 3], scores).statistic)
        tau = tau_raw if math.isfinite(tau_raw) else 0.0
        review = manual[sample_id]
        valid_visible = (
            _bool(review.get("candidate_valid", "")) is True
            and _bool(review.get("mutation_visible", "")) is True
        )
        details.append(
            {
                "sample_id": sample_id,
                "category": group[0]["category"],
                "score_severity_1": scores[0],
                "score_severity_2": scores[1],
                "score_severity_3": scores[2],
                "adjacent_nonincreasing": scores[0] + 1e-12 >= scores[1] and scores[1] + 1e-12 >= scores[2],
                "strict_total_decrease": scores[0] > scores[2] + 1e-12,
                "kendall_tau_severity_vs_score": tau,
                "score_drop_s1_to_s3": scores[0] - scores[2],
                "manual_severity2_valid_visible": valid_visible,
            }
        )

    valid = [row for row in details if row["manual_severity2_valid_visible"]]
    invalid = [row for row in details if not row["manual_severity2_valid_visible"]]
    result = {
        "validator": "validate_text_ltsim_severity_v2",
        "metric": "published LTSim equations on the per-page all-text subset",
        "perturbation": "block_right, severities 1/2/3",
        "rows": len(rows),
        "all_documents": _summary(details),
        "manual_severity2_valid_visible_documents": _summary(valid),
        "manual_severity2_invalid_or_invisible_documents": _summary(invalid),
        "interpretation": (
            "Monotonic response validates mechanical sensitivity, not perceptual band thresholds. "
            "The manual label exists only for severity 2 and is not a human rating."
        ),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "severity_case_details.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(details[0]))
        writer.writeheader()
        writer.writerows(details)
    (args.out_dir / "severity_validation.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
