#!/usr/bin/env python3
"""Validate PDF metric behavior on controlled augmentation results.

The source PDF is the unit of inference. Higher axis scores must mean better
fidelity, and increasing non-negative severity must mean a stronger defect.
The script summarizes known relations; it does not fit a quality model.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.stats import kendalltau


BASELINE_FAMILIES = {"baseline", "identity", "identity_clone", "pristine", "reference", "self"}
EMPTY = {"", "na", "n/a", "none", "null"}


def _float(value: object) -> float | None:
    try:
        result = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _bool(value: object, default: bool = True) -> bool:
    text = str(value).strip().lower()
    if not text:
        return default
    if text in {"1", "true", "yes", "y"}:
        return True
    if text in {"0", "false", "no", "n"}:
        return False
    raise ValueError(f"invalid boolean value: {value!r}")


def _mean(values: Iterable[float | None]) -> float | None:
    finite = [value for value in values if value is not None and math.isfinite(value)]
    return float(np.mean(finite)) if finite else None


def _bbox(value: object) -> tuple[float, float, float, float] | None:
    text = str(value).strip()
    if text.lower() in EMPTY:
        return None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = [part for part in re.split(r"[\s,;]+", text) if part]
    if not isinstance(parsed, (list, tuple)) or len(parsed) != 4:
        return None
    numbers = tuple(_float(part) for part in parsed)
    if any(number is None for number in numbers):
        return None
    x0, y0, x1, y1 = numbers
    return (x0, y0, x1, y1) if x1 >= x0 and y1 >= y0 else None


def _iou(first: tuple[float, float, float, float],
         second: tuple[float, float, float, float]) -> float:
    x0 = max(first[0], second[0])
    y0 = max(first[1], second[1])
    x1 = min(first[2], second[2])
    y1 = min(first[3], second[3])
    intersection = max(0.0, x1 - x0) * max(0.0, y1 - y0)
    first_area = max(0.0, first[2] - first[0]) * max(0.0, first[3] - first[1])
    second_area = max(0.0, second[2] - second[0]) * max(0.0, second[3] - second[1])
    union = first_area + second_area - intersection
    return intersection / union if union else 0.0


def _axes_for(expected_axis: str, axis_columns: list[str]) -> list[str]:
    expected = expected_axis.strip().lower()
    if expected in EMPTY or expected in {"invariant", "none"}:
        return []
    aliases = {column.lower(): column for column in axis_columns}
    for column in axis_columns:
        short = column.lower()
        if short.startswith("axis_"):
            aliases[short[5:]] = column
        if short.endswith("_score"):
            aliases[short[:-6]] = column
    resolved = []
    for name in (part for part in re.split(r"[+|,;/]", expected) if part):
        name = name.removesuffix("_only")
        axis = aliases.get(name) or aliases.get(f"axis_{name}")
        if axis and axis not in resolved:
            resolved.append(axis)
    return resolved


def _components(row: dict[str, str]) -> list[str]:
    text = row.get("components", "").strip()
    if not text and row.get("family", "").lower().startswith("compound:"):
        text = row["family"].split(":", 1)[1]
    return [part.strip() for part in re.split(r"[+|;]", text) if part.strip()]


def _new_accumulator() -> dict:
    return {
        "adjacent_correct": 0,
        "adjacent_total": 0,
        "kendall_tau": [],
        "invariant_false": 0,
        "invariant_total": 0,
        "target_drop": [],
        "off_target_drop": [],
        "localization_hit": [],
        "localization_iou": [],
        "compound_dominance": [],
        "abstained": 0,
        "applicable": 0,
        "non_applicable": 0,
        "repeat_agreement": [],
    }


def _add(accumulator: dict, name: str, value: object = None) -> None:
    if isinstance(accumulator[name], list):
        accumulator[name].append(value)
    elif value is None:
        accumulator[name] += 1
    else:
        accumulator[name] += value


def _finalize(accumulator: dict) -> dict[str, float | int | None]:
    adjacent_total = accumulator["adjacent_total"]
    invariant_total = accumulator["invariant_total"]
    applicable = accumulator["applicable"]
    target = _mean(accumulator["target_drop"])
    off_target = _mean(accumulator["off_target_drop"])
    return {
        "adjacent_monotonic_accuracy": (
            accumulator["adjacent_correct"] / adjacent_total if adjacent_total else None
        ),
        "adjacent_pairs": adjacent_total,
        "kendall_tau_b": _mean(accumulator["kendall_tau"]),
        "invariant_false_positive_rate": (
            accumulator["invariant_false"] / invariant_total if invariant_total else None
        ),
        "invariant_cases": invariant_total,
        "target_axis_drop": target,
        "off_target_mean_drop": off_target,
        "target_selectivity_margin": (
            target - off_target if target is not None and off_target is not None else None
        ),
        "localization_hit_rate": _mean(accumulator["localization_hit"]),
        "localization_mean_iou": _mean(accumulator["localization_iou"]),
        "compound_dominance_accuracy": _mean(accumulator["compound_dominance"]),
        "abstention_rate": accumulator["abstained"] / applicable if applicable else None,
        "applicable_cases": applicable,
        "non_applicable_cases": accumulator["non_applicable"],
        "projection_repeat_agreement": _mean(accumulator["repeat_agreement"]),
        "repeat_groups": len(accumulator["repeat_agreement"]),
    }


def _merge_value(targets: Iterable[dict], name: str, value: object = None) -> None:
    for target in targets:
        _add(target, name, value)


def _baseline_scores(rows: list[dict[str, str]], axis_columns: list[str]) -> dict[str, dict[str, float]]:
    by_sample: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        severity = _float(row.get("severity"))
        if severity == 0 and _bool(row.get("applicable"), True):
            by_sample[row["sample_id"]].append(row)

    baselines: dict[str, dict[str, float]] = {}
    for sample_id, candidates in by_sample.items():
        explicit = [row for row in candidates if row["family"].strip().lower() in BASELINE_FAMILIES]
        selected = explicit or candidates
        baselines[sample_id] = {
            axis: float(np.median(values))
            for axis in axis_columns
            if (values := [_float(row.get(axis)) for row in selected])
            and (values := [value for value in values if value is not None])
        }
    return baselines


def _same_repeat(rows: list[dict[str, str]], axis_columns: list[str], tolerance: float) -> bool:
    first = rows[0]
    for row in rows[1:]:
        for column in axis_columns:
            left, right = _float(first.get(column)), _float(row.get(column))
            if (left is None) != (right is None):
                return False
            if left is not None and abs(left - right) > tolerance:
                return False
        if str(first.get("predicted_page", "")).strip() != str(row.get("predicted_page", "")).strip():
            return False
        left_bbox, right_bbox = _bbox(first.get("predicted_bbox")), _bbox(row.get("predicted_bbox"))
        if (left_bbox is None) != (right_bbox is None):
            return False
        if left_bbox and any(abs(left - right) > tolerance for left, right in zip(left_bbox, right_bbox)):
            return False
    return True


def _macro(sample_results: list[dict]) -> tuple[dict, dict]:
    metric_names = [
        "adjacent_monotonic_accuracy", "kendall_tau_b", "invariant_false_positive_rate",
        "target_axis_drop", "off_target_mean_drop", "target_selectivity_margin",
        "localization_hit_rate", "localization_mean_iou", "compound_dominance_accuracy",
        "abstention_rate", "projection_repeat_agreement",
    ]
    document_macro = {
        name: _mean(result["metrics"].get(name) for result in sample_results)
        for name in metric_names
    }
    by_category: dict[str, list[dict]] = defaultdict(list)
    for result in sample_results:
        by_category[result["category"]].append(result)
    category_values = {
        category: {
            name: _mean(result["metrics"].get(name) for result in values)
            for name in metric_names
        }
        for category, values in sorted(by_category.items())
    }
    category_macro = {
        name: _mean(values.get(name) for values in category_values.values())
        for name in metric_names
    }
    category_macro["categories"] = category_values
    return document_macro, category_macro


def _bootstrap(sample_results: list[dict], replicates: int, seed: int) -> dict:
    if replicates <= 0 or not sample_results:
        return {"replicates": replicates, "seed": seed, "document_macro": {}, "category_macro": {}}
    rng = np.random.default_rng(seed)
    by_category: dict[str, list[dict]] = defaultdict(list)
    for result in sample_results:
        by_category[result["category"]].append(result)
    draws = {"document_macro": defaultdict(list), "category_macro": defaultdict(list)}
    for _ in range(replicates):
        sampled = []
        for values in by_category.values():
            indices = rng.integers(0, len(values), size=len(values))
            sampled.extend(values[int(index)] for index in indices)
        document_macro, category_macro = _macro(sampled)
        for scope, metrics in (("document_macro", document_macro), ("category_macro", category_macro)):
            for name, value in metrics.items():
                if name != "categories" and value is not None:
                    draws[scope][name].append(value)

    intervals = {}
    for scope, metrics in draws.items():
        intervals[scope] = {
            name: {
                "low": float(np.percentile(values, 2.5)),
                "high": float(np.percentile(values, 97.5)),
            }
            for name, values in metrics.items() if values
        }
    return {"replicates": replicates, "seed": seed, **intervals}


def _scope_flags(metrics: dict) -> list[str]:
    flags = []
    if metrics.get("adjacent_monotonic_accuracy") is not None and metrics["adjacent_monotonic_accuracy"] < 0.95:
        flags.append("adjacent_monotonic_accuracy_below_0.95")
    if metrics.get("kendall_tau_b") is not None and metrics["kendall_tau_b"] < 0.70:
        flags.append("kendall_tau_b_below_0.70")
    if metrics.get("localization_hit_rate") is not None and metrics["localization_hit_rate"] < 0.90:
        flags.append("raster_residual_localization_below_0.90")
    if metrics.get("compound_dominance_accuracy") is not None and metrics["compound_dominance_accuracy"] < 0.95:
        flags.append("compound_dominance_below_0.95")
    if metrics.get("abstention_rate") is not None and metrics["abstention_rate"] > 0:
        flags.append("unexpected_projection_abstention")
    return flags


def analyze_rows(rows: list[dict[str, str]], *, axis_columns: list[str] | None = None,
                 tolerance: float = 1e-12, invariant_tolerance: float = 0.01,
                 iou_threshold: float = 0.0,
                 bootstrap_replicates: int = 2000, seed: int = 20260715) -> dict:
    """Return per-family and source-clustered validation statistics."""
    if not rows:
        raise ValueError("input CSV contains no data rows")
    required = {"sample_id", "category", "family", "severity", "seed", "applicable", "expected_axis"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"missing required columns: {', '.join(sorted(missing))}")
    if axis_columns is None:
        axis_columns = sorted(column for column in rows[0] if column.startswith("axis_"))
    if not axis_columns:
        raise ValueError("no metric axes found; use axis_* columns or pass --axis-columns")
    unknown = set(axis_columns) - set(rows[0])
    if unknown:
        raise ValueError(f"unknown axis columns: {', '.join(sorted(unknown))}")

    baselines = _baseline_scores(rows, axis_columns)
    sample_acc: dict[tuple[str, str], dict] = defaultdict(_new_accumulator)
    family_acc: dict[tuple[str, str, str], dict] = defaultdict(_new_accumulator)
    variant_acc: dict[tuple[str, str, str, str], dict] = defaultdict(_new_accumulator)

    def accumulators(row: dict[str, str]) -> tuple[dict, dict, dict]:
        sample_key = (row["sample_id"], row["category"])
        family_key = (row["family"], row["sample_id"], row["category"])
        variant = row.get("variant", "") or row["family"]
        variant_key = (variant, row["family"], row["sample_id"], row["category"])
        return sample_acc[sample_key], family_acc[family_key], variant_acc[variant_key]

    # Applicability, abstention, invariance, target response, and localization.
    invariant_by_sample: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        targets = accumulators(row)
        if not _bool(row.get("applicable"), True):
            _merge_value(targets, "non_applicable")
            continue
        _merge_value(targets, "applicable")
        axes = _axes_for(row.get("expected_axis", ""), axis_columns)
        severity = _float(row.get("severity"))
        if severity is None:
            raise ValueError(f"invalid severity for sample {row['sample_id']}: {row.get('severity')!r}")
        if axes and any(_float(row.get(axis)) is None for axis in axes):
            _merge_value(targets, "abstained")
        elif not axes and all(_float(row.get(column)) is None for column in axis_columns):
            _merge_value(targets, "abstained")

        if severity == 0:
            invariant_by_sample[row["sample_id"]].append(row)
        elif axes and row["sample_id"] in baselines:
            baseline = baselines[row["sample_id"]]
            target_drops = [
                baseline[axis] - score
                for axis in axes if axis in baseline
                and (score := _float(row.get(axis))) is not None
            ]
            if target_drops:
                _merge_value(targets, "target_drop", float(np.mean(target_drops)))
            off_drops = [
                baseline[column] - value
                for column in axis_columns
                if column not in axes and column in baseline
                and (value := _float(row.get(column))) is not None
            ]
            if off_drops:
                _merge_value(targets, "off_target_drop", float(np.mean(off_drops)))

        expected_page = _float(row.get("expected_page"))
        expected_bbox = _bbox(row.get("expected_bbox"))
        if expected_page is not None or expected_bbox is not None:
            predicted_page = _float(row.get("predicted_page"))
            predicted_bbox = _bbox(row.get("predicted_bbox"))
            page_hit = expected_page is None or predicted_page == expected_page
            overlap = _iou(expected_bbox, predicted_bbox) if expected_bbox and predicted_bbox else None
            bbox_hit = expected_bbox is None or (overlap is not None and overlap > iou_threshold)
            _merge_value(targets, "localization_hit", float(page_hit and bbox_hit))
            if expected_bbox is not None:
                _merge_value(targets, "localization_iou", overlap or 0.0)

    # Compare serialization/rendering controls with the defined projection
    # optimum, never with themselves as an estimated baseline.
    for sample_id, candidates in invariant_by_sample.items():
        controls = [row for row in candidates if row["family"].strip().lower() not in BASELINE_FAMILIES]
        for row in controls or candidates:
            compared = [
                abs(value - 1.0)
                for column in axis_columns
                if (value := _float(row.get(column))) is not None
            ]
            if not compared:
                continue
            targets = accumulators(row)
            _merge_value(targets, "invariant_total")
            if max(compared) > invariant_tolerance:
                _merge_value(targets, "invariant_false")

    # Collapse exact reruns before severity ordering.
    repeat_groups: dict[tuple, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if _bool(row.get("applicable"), True):
            key = (
                row["sample_id"], row["category"], row["family"], row.get("variant", ""),
                row["severity"], row["seed"],
            )
            repeat_groups[key].append(row)
    for repeated in repeat_groups.values():
        if len(repeated) < 2:
            continue
        agreement = float(_same_repeat(repeated, axis_columns, tolerance))
        _merge_value(accumulators(repeated[0]), "repeat_agreement", agreement)

    sequences: dict[tuple, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if _bool(row.get("applicable"), True):
            sequences[(
                row["sample_id"], row["category"], row["family"], row.get("variant", ""), row["seed"],
            )].append(row)
    for sequence in sequences.values():
        axes = next((_axes_for(row.get("expected_axis", ""), axis_columns) for row in sequence
                     if _axes_for(row.get("expected_axis", ""), axis_columns)), [])
        if not axes:
            continue
        targets = accumulators(sequence[0])
        for axis in axes:
            by_severity: dict[float, list[float]] = defaultdict(list)
            for row in sequence:
                severity, score = _float(row.get("severity")), _float(row.get(axis))
                if severity is not None and score is not None:
                    by_severity[severity].append(score)
            baseline = baselines.get(sequence[0]["sample_id"], {}).get(axis)
            if baseline is not None and 0.0 not in by_severity:
                by_severity[0.0].append(baseline)
            levels = sorted((severity, float(np.mean(scores))) for severity, scores in by_severity.items())
            if len(levels) < 2:
                continue
            for (_, previous), (_, current) in zip(levels, levels[1:]):
                _merge_value(targets, "adjacent_total")
                if current < previous - tolerance:
                    _merge_value(targets, "adjacent_correct")
            statistic = kendalltau([level[0] for level in levels], [-level[1] for level in levels]).statistic
            if math.isnan(statistic):
                statistic = 0.0
            _merge_value(targets, "kendall_tau", float(statistic))

    # Strong compound dominance: on the compound's expected axis, the compound
    # score must be no higher than either named constituent score.
    case_scores: dict[tuple[str, str, float, str], dict[str, float]] = {}
    collapsed: dict[tuple[str, str, float, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        severity = _float(row.get("severity"))
        if severity is not None and _bool(row.get("applicable"), True):
            identity = row.get("variant", "") or row["family"]
            collapsed[(row["sample_id"], identity, severity, row["seed"])].append(row)
    for key, repeated in collapsed.items():
        case_scores[key] = {
            axis: value for axis in axis_columns
            if (value := _mean(_float(row.get(axis)) for row in repeated)) is not None
        }
    for row in rows:
        components = _components(row)
        severity = _float(row.get("severity"))
        axes = _axes_for(row.get("expected_axis", ""), axis_columns)
        if len(components) < 2 or severity is None or not axes:
            continue
        for axis in axes:
            compound_score = _float(row.get(axis))
            component_scores = [
                case_scores.get((row["sample_id"], component, severity, row["seed"]), {}).get(axis)
                for component in components
            ]
            if compound_score is None or any(score is None for score in component_scores):
                continue
            success = float(compound_score <= min(component_scores) + tolerance)
            _merge_value(accumulators(row), "compound_dominance", success)

    sample_results = [
        {"sample_id": sample_id, "category": category, "metrics": _finalize(accumulator)}
        for (sample_id, category), accumulator in sorted(sample_acc.items())
    ]
    family_documents: dict[str, list[dict]] = defaultdict(list)
    for (family, sample_id, category), accumulator in family_acc.items():
        family_documents[family].append(
            {"sample_id": sample_id, "category": category, "metrics": _finalize(accumulator)}
        )
    per_family = {}
    for index, (family, documents) in enumerate(sorted(family_documents.items())):
        document_macro, category_macro = _macro(documents)
        per_family[family] = {
            "documents": len(documents),
            "document_macro": document_macro,
            "category_macro": category_macro,
            "bootstrap_95_ci": _bootstrap(documents, bootstrap_replicates, seed + index + 1),
        }
    variant_documents: dict[str, list[dict]] = defaultdict(list)
    variant_family = {}
    for (variant, family, sample_id, category), accumulator in variant_acc.items():
        variant_family[variant] = family
        variant_documents[variant].append(
            {"sample_id": sample_id, "category": category, "metrics": _finalize(accumulator)}
        )
    per_variant = {}
    for variant, documents in sorted(variant_documents.items()):
        document_macro, category_macro = _macro(documents)
        per_variant[variant] = {
            "family": variant_family[variant],
            "documents": len(documents),
            "document_macro": document_macro,
            "category_macro": category_macro,
        }

    document_macro, category_macro = _macro(sample_results)
    bootstrap = _bootstrap(sample_results, bootstrap_replicates, seed)
    tau_interval = bootstrap.get("document_macro", {}).get("kendall_tau_b", {})
    overall_gates = {
        "adjacent_monotonic_accuracy_at_least_0.95": (
            document_macro["adjacent_monotonic_accuracy"] is not None
            and document_macro["adjacent_monotonic_accuracy"] >= 0.95
        ),
        "kendall_tau_lower_95_ci_above_0.70": (
            tau_interval.get("low") is not None and tau_interval["low"] > 0.70
        ),
        "lossless_invariant_fpr_below_0.01": (
            document_macro["invariant_false_positive_rate"] is not None
            and document_macro["invariant_false_positive_rate"] < 0.01
        ),
        "raster_residual_localization_at_least_0.90": (
            document_macro["localization_hit_rate"] is not None
            and document_macro["localization_hit_rate"] >= 0.90
        ),
        "projection_repeat_confirmed": (
            document_macro["projection_repeat_agreement"] == 1.0
        ) if document_macro["projection_repeat_agreement"] is not None else None,
    }
    family_flags = {
        name: flags for name, value in per_family.items()
        if (flags := _scope_flags(value["document_macro"]))
    }
    variant_flags = {
        name: flags for name, value in per_variant.items()
        if (flags := _scope_flags(value["document_macro"]))
    }
    category_flags = {
        name: flags for name, metrics in category_macro["categories"].items()
        if (flags := _scope_flags(metrics))
    }
    mandatory_gates = {
        name: value for name, value in overall_gates.items()
        if name != "projection_repeat_confirmed"
    }
    gate_complete = all(value is not None for value in mandatory_gates.values())
    gate_pass = gate_complete and all(mandatory_gates.values()) and not (
        family_flags or variant_flags or category_flags
    )
    return {
        "method": "controlled_augmentation_validation_v1",
        "assumptions": {
            "score_direction": "higher axis values mean better fidelity",
            "severity_direction": "larger severity means a stronger defect; zero means invariant/pristine",
            "cluster_unit": "sample_id (source PDF)",
            "baseline": (
                "severity-zero identity/baseline/pristine/reference/self rows; otherwise the median "
                "of severity-zero rows"
            ),
            "projection_repeat": (
                "duplicate sample_id/category/family/severity/seed rows test equality of stored "
                "projection values and the raster bbox; artifact hashes are validated separately"
            ),
            "compound_rule": "compound score <= every named component score on the expected axis",
            "compound_components": "components column or compound:family_a+family_b family name",
            "localization_rule": (
                f"page equality and bbox IoU > {iou_threshold:g}; predicted boxes are registered "
                "raster-residual enclosures, not semantic or axis-specific defect explanations"
            ),
            "bbox_coordinates": "expected_bbox and predicted_bbox use one common coordinate system",
            "missing_values": "counted as abstentions when the expected axis is applicable",
            "multi_axis_targets": (
                "expected_axis may join axes with '+'; target response and severity ordering are "
                "evaluated on every named axis, never silently dropped"
            ),
            "invariant_control": (
                f"severity-zero lossless rewrites are compared with the defined score optimum 1.0 "
                f"at tolerance {invariant_tolerance:g}; they are not used as their own baseline"
            ),
            "ordering": (
                f"severity ordering includes the severity-zero baseline; adjacent ties and score "
                f"increases are failures beyond numerical tolerance {tolerance:g}"
            ),
            "selectivity_boundary": (
                "target/off-target drops are descriptive only because v1 lacks preregistered "
                "per-variant affected-axis and invariant-axis contracts"
            ),
        },
        "claim_boundary": {
            "validated_here": (
                "controlled-response behavior of five ad-hoc harness projections: extracted-token "
                "F1, exact-token box-IoU q10, a mixed typography diagnostic, unregistered ink F1, "
                "and a page-count/break diagnostic"
            ),
            "not_validated_here": (
                "CLEval, LTSim, PaIRS, reading-order semantics, GriTS, TEDS, CDM, SSIM, figure "
                "matching, human quality, aesthetic acceptability, or a universal scalar"
            ),
        },
        "axis_columns": axis_columns,
        "rows": len(rows),
        "source_documents": len(sample_results),
        "per_family": per_family,
        "per_variant": per_variant,
        "document_macro": document_macro,
        "category_macro": category_macro,
        "bootstrap_95_ci": bootstrap,
        "gate_assessment": {
            "status": "passes_synthetic_projection_gates" if gate_pass else "fails_or_incomplete",
            "overall": overall_gates,
            "mandatory_controlled_response_gates": list(mandatory_gates),
            "artifact_determinism": "separate SHA-256/render-repeat report required",
            "family_flags": family_flags,
            "variant_flags": variant_flags,
            "category_flags": category_flags,
            "rule": (
                "No family, variant, or category flag is averaged away. These are engineering "
                "response gates for harness projections, not proof of real-AI or human quality."
            ),
        },
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output", type=Path, help="JSON output; defaults to stdout")
    parser.add_argument("--axis-columns", help="comma-separated metric columns; default: all axis_* columns")
    parser.add_argument("--tolerance", type=float, default=1e-12)
    parser.add_argument("--invariant-tolerance", type=float, default=0.01)
    parser.add_argument("--iou-threshold", type=float, default=0.0)
    parser.add_argument("--bootstrap-replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260715)
    args = parser.parse_args()
    columns = [column.strip() for column in args.axis_columns.split(",")] if args.axis_columns else None
    result = analyze_rows(
        read_csv(args.input_csv), axis_columns=columns, tolerance=args.tolerance,
        invariant_tolerance=args.invariant_tolerance,
        iou_threshold=args.iou_threshold, bootstrap_replicates=args.bootstrap_replicates,
        seed=args.seed,
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
