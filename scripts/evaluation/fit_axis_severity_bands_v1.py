#!/usr/bin/env python3
"""Fit axis-specific controlled-defect severity bands on metric development only.

The bands describe equivalence to deterministic perturbation levels. They are
not human preference labels and are never combined into a universal score.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "augmentation_results.csv"
DEFAULT_PROFILE = ROOT / "results" / "metric_research_v1" / "corpus_profile_157.csv"
DEFAULT_OUTPUT = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "axis_severity_bands.json"
BAND_NAMES = ("reference_like", "mild", "moderate", "severe")
HELD_GATE = {
    "minimum_exact_accuracy": 0.50,
    "minimum_within_one_accuracy": 0.90,
    "maximum_mean_absolute_band_error": 0.50,
}


def _float(value: object) -> float | None:
    try:
        number = float(str(value))
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _target_axes(value: str, axis_columns: list[str]) -> list[str]:
    names = {column.removeprefix("axis_"): column for column in axis_columns}
    return [names[name.removesuffix("_only")] for name in re.split(r"[+|,;/]", value)
            if name.removesuffix("_only") in names]


def _document_levels(rows: list[dict[str, str]], partitions: dict[str, str],
                     axis_columns: list[str]) -> dict[tuple[str, str, int, str], float]:
    baselines: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    variants: dict[tuple[str, str, str, int, str], list[float]] = defaultdict(list)
    for row in rows:
        if row.get("status") != "applied" or row.get("applicable", "true").lower() != "true":
            continue
        severity = int(float(row["severity"]))
        partition = partitions[row["sample_id"]]
        axes = axis_columns if severity == 0 else _target_axes(row.get("expected_axis", ""), axis_columns)
        for axis in axes:
            score = _float(row.get(axis))
            if score is not None:
                if severity == 0:
                    baselines[(row["sample_id"], axis, partition)].append(score)
                elif severity in (1, 2, 3):
                    variant = row.get("variant", "") or row.get("family", "")
                    variants[(row["sample_id"], axis, variant, severity, partition)].append(score)

    averaged = {key: sum(scores) / len(scores) for key, scores in variants.items()}
    by_sample_axis: dict[tuple[str, str, str], dict[str, dict[int, float]]] = defaultdict(
        lambda: defaultdict(dict)
    )
    for (sample, axis, variant, severity, partition), score in averaged.items():
        by_sample_axis[(sample, axis, partition)][variant][severity] = score
    levels = {
        (sample, axis, 0, partition): sum(scores) / len(scores)
        for (sample, axis, partition), scores in baselines.items()
    }
    for (sample, axis, partition), candidate_variants in by_sample_axis.items():
        balanced = [values for values in candidate_variants.values() if set(values) == {1, 2, 3}]
        for severity in (1, 2, 3):
            if balanced:
                levels[(sample, axis, severity, partition)] = sum(
                    values[severity] for values in balanced
                ) / len(balanced)
    return levels


def _thresholds(anchors: list[float]) -> list[float]:
    return [round((left + right) / 2, 12) for left, right in zip(anchors, anchors[1:])]


def _predict(score: float, thresholds: list[float]) -> int:
    if score >= thresholds[0]:
        return 0
    if score >= thresholds[1]:
        return 1
    if score >= thresholds[2]:
        return 2
    return 3


def _validation(records: list[tuple[float, int]], thresholds: list[float]) -> dict:
    if not records:
        return {"cases": 0, "exact_accuracy": None, "within_one_accuracy": None,
                "mean_absolute_band_error": None, "confusion": {}}
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    errors = []
    for score, expected in records:
        predicted = _predict(score, thresholds)
        confusion[BAND_NAMES[expected]][BAND_NAMES[predicted]] += 1
        errors.append(abs(predicted - expected))
    return {
        "cases": len(records),
        "exact_accuracy": sum(error == 0 for error in errors) / len(errors),
        "within_one_accuracy": sum(error <= 1 for error in errors) / len(errors),
        "mean_absolute_band_error": sum(errors) / len(errors),
        "confusion": {expected: dict(predicted) for expected, predicted in sorted(confusion.items())},
    }


def _passes_gate(evaluation: dict) -> bool:
    return bool(evaluation["cases"]) and (
        evaluation["exact_accuracy"] >= HELD_GATE["minimum_exact_accuracy"]
        and evaluation["within_one_accuracy"] >= HELD_GATE["minimum_within_one_accuracy"]
        and evaluation["mean_absolute_band_error"] <= HELD_GATE["maximum_mean_absolute_band_error"]
    )


def fit_bands(rows: list[dict[str, str]], partitions: dict[str, str],
              axis_columns: list[str] | None = None) -> dict:
    if not rows:
        raise ValueError("augmentation results are empty")
    axis_columns = axis_columns or sorted(column for column in rows[0] if column.startswith("axis_"))
    levels = _document_levels(rows, partitions, axis_columns)
    result = {}
    for axis in axis_columns:
        by_partition: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
        for (_sample, record_axis, severity, partition), score in levels.items():
            if record_axis == axis and severity in range(4):
                by_partition[partition][severity].append(score)
        dev = by_partition["metric_dev"]
        missing = [severity for severity in range(4) if not dev[severity]]
        if missing:
            result[axis] = {
                "status": "abstain", "reason": f"metric_dev lacks severity levels {missing}",
                "aggregate_score": None, "deploy_to_ai_outputs": False,
            }
            continue
        anchors = [median(dev[severity]) for severity in range(4)]
        monotone = all(right <= left + 1e-12 for left, right in zip(anchors, anchors[1:]))
        collapsed = any(abs(left - right) < 1e-9 for left, right in zip(anchors, anchors[1:]))
        if not monotone or collapsed:
            result[axis] = {
                "status": "trial", "reason": "development anchors are non-monotone or collapsed",
                "development_anchor_medians": dict(zip(BAND_NAMES, anchors)),
                "development_document_counts": {BAND_NAMES[s]: len(dev[s]) for s in range(4)},
                "aggregate_score": None, "deploy_to_ai_outputs": False,
            }
            continue
        thresholds = _thresholds(anchors)
        axis_result = {
            "status": "thresholds_frozen_pending_held_gate",
            "meaning": "controlled-defect equivalent band; higher raw axis score is better",
            "development_anchor_medians": dict(zip(BAND_NAMES, anchors)),
            "development_document_counts": {BAND_NAMES[s]: len(dev[s]) for s in range(4)},
            "thresholds": {
                "reference_like_min": thresholds[0],
                "mild_min": thresholds[1],
                "moderate_min": thresholds[2],
                "severe_below": thresholds[2],
            },
            "aggregate_score": None,
            "evaluation": {},
        }
        for partition in ("metric_validation", "metric_test"):
            records = [(score, severity) for severity, scores in by_partition[partition].items()
                       for score in scores if severity in range(4)]
            axis_result["evaluation"][partition] = _validation(records, thresholds)
        validation_pass = _passes_gate(axis_result["evaluation"]["metric_validation"])
        test_pass = _passes_gate(axis_result["evaluation"]["metric_test"])
        axis_result["held_gate"] = {
            "criteria": HELD_GATE,
            "metric_validation_pass": validation_pass,
            "metric_test_confirmation_pass": test_pass,
        }
        axis_result["status"] = "synthetic_internal_pass" if validation_pass and test_pass else "trial"
        axis_result["deploy_to_ai_outputs"] = False
        axis_result["external_validity"] = (
            "not established: no human/task ratings and heterogeneous defect families have no common utility scale"
        )
        if axis_result["status"] == "trial":
            axis_result["reason"] = "frozen development thresholds did not pass both held-partition gates"
        result[axis] = axis_result
    return {
        "method": "axis_severity_bands_v1",
        "fit_partition": "metric_dev",
        "held_partitions": ["metric_validation", "metric_test"],
        "labels": list(BAND_NAMES),
        "held_gate": HELD_GATE,
        "policy": (
            "Each axis is graded independently against controlled perturbation anchors. "
            "Only variants present at all three severities receive equal weight. These profiles are "
            "internal synthetic diagnostics and are never applied as AI-quality labels. No universal "
            "scalar, model ranking weight, or human-preference claim is made."
        ),
        "axes": result,
    }


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    profile = _read(args.profile)
    partitions = {row["sample_id"]: row["metric_partition"] for row in profile}
    result = fit_bands(_read(args.results), partitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({axis: value["status"] for axis, value in result["axes"].items()}, indent=2))


if __name__ == "__main__":
    main()
