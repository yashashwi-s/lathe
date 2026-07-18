#!/usr/bin/env python3
"""Validate v2 component behavior on the manually reviewed retained panel.

The binary triggers here are smoke-test thresholds, not released quality bands.
Raw values remain the reportable measurements.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TRIGGER_POLICY = {
    "content": "strict_word_f1 < 1 or a nonempty critical inventory differs",
    "layout": "token center q90 > .005 or Text-LTSim < .9999 (change detector, not grade band)",
    "typography": "font-size log error q90 > .01, baseline q90 > .002, or style coverage < .99",
    "raster_residual": "resized-canvas tolerant-ink F1 < .995 or fail-closed SSIM < .9999",
    "pagination": "page-count delta != 0 or page-break F1 < .999",
}


def _float(value: str) -> float | None:
    if value == "" or value is None:
        return None
    try:
        result = float(value)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def _bool(value: str) -> bool | None:
    normalized = (value or "").strip().lower()
    if normalized in {"true", "yes", "1"}:
        return True
    if normalized in {"false", "no", "0"}:
        return False
    return None


def _rate(values: list[bool]) -> float | None:
    return sum(values) / len(values) if values else None


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _critical_diff(row: dict[str, str], name: str) -> bool:
    exact = _bool(row.get(f"{name}_exact", ""))
    reference_count = _float(row.get(f"reference_{name}_count", ""))
    candidate_count = _float(row.get(f"candidate_{name}_count", ""))
    if reference_count is None or candidate_count is None:
        # Older v2 batch tables omitted counts; an inexact flag is still usable,
        # while an exact empty inventory is not treated as positive evidence.
        return exact is False
    return (reference_count > 0 or candidate_count > 0) and exact is False


def triggers(row: dict[str, str]) -> dict[str, bool]:
    word_f1 = _float(row.get("strict_word_f1", row.get("word_f1", "")))
    center_q90 = _float(row.get("token_center_displacement_q90", ""))
    ltsim = _float(row.get("text_ltsim_page_macro", ""))
    size_error = _float(row.get("font_size_log_error_q90", ""))
    baseline = _float(row.get("baseline_displacement_q90", ""))
    style_coverage = _float(row.get("style_coverage_hmean", ""))
    ink_f1 = _float(row.get("unregistered_ink_f1", ""))
    ssim = _float(row.get("unregistered_ssim", ""))
    page_delta = _float(row.get("page_count_delta", ""))
    break_f1 = _float(row.get("page_break_f1", ""))
    return {
        "content": (
            (word_f1 is not None and word_f1 < 1.0 - 1e-9)
            or _critical_diff(row, "number")
            or _critical_diff(row, "operator")
            or _critical_diff(row, "citation")
        ),
        "layout": (
            (center_q90 is not None and center_q90 > 0.005)
            or (ltsim is not None and ltsim < 0.9999)
        ),
        "typography": (
            (size_error is not None and size_error > 0.01)
            or (baseline is not None and baseline > 0.002)
            or (style_coverage is not None and style_coverage < 0.99)
        ),
        "raster_residual": (
            (ink_f1 is not None and ink_f1 < 0.995)
            or (ssim is not None and ssim < 0.9999)
        ),
        "pagination": (
            (page_delta is not None and abs(page_delta) > 1e-9)
            or (break_f1 is not None and break_f1 < 0.999)
        ),
    }


def expected_modules(expected_axis: str) -> set[str]:
    axes = set(expected_axis.split("+"))
    modules = set()
    if "content" in axes:
        modules.add("content")
    if "layout" in axes:
        modules.add("layout")
    if "typography" in axes:
        modules.add("typography")
    if "pagination" in axes:
        modules.add("pagination")
    if "appearance" in axes:
        modules.add("raster_residual")
    return modules


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--manual-manifest", type=Path)
    args = parser.parse_args()
    rows = _read(args.scores)
    if not rows:
        raise SystemExit("score table is empty")
    if args.manual_manifest:
        manual_by_id = {row["case_id"]: row for row in _read(args.manual_manifest)}
        score_ids = {row.get("case_id") for row in rows}
        if score_ids != set(manual_by_id):
            raise ValueError("score/manual case IDs differ")
        for row in rows:
            manual = manual_by_id[row["case_id"]]
            for field in (
                "candidate_valid",
                "mutation_visible",
                "target_box_correct",
                "label_correct",
                "predicted_box_useful",
            ):
                row[field] = manual.get(field, "")

    details = []
    expected_detection: dict[str, list[bool]] = defaultdict(list)
    valid_expected_detection: dict[str, list[bool]] = defaultdict(list)
    invalid_response: dict[str, list[bool]] = defaultdict(list)
    response_matrix: dict[str, dict[str, list[bool]]] = defaultdict(lambda: defaultdict(list))
    status_counts = Counter()
    for row in rows:
        status_counts[row.get("v2_status", "")] += 1
        row_triggers = triggers(row)
        expected = expected_modules(row.get("expected_axis", ""))
        target_detected = bool(expected) and any(row_triggers[module] for module in expected)
        expected_detection[row.get("expected_axis", "unknown")].append(target_detected)
        for module, value in row_triggers.items():
            response_matrix[row.get("expected_axis", "unknown")][module].append(value)
        candidate_valid = _bool(row.get("candidate_valid", ""))
        mutation_visible = _bool(row.get("mutation_visible", ""))
        if candidate_valid is True and mutation_visible is True:
            valid_expected_detection[row.get("expected_axis", "unknown")].append(target_detected)
        elif candidate_valid is False or mutation_visible is False:
            for module, value in row_triggers.items():
                invalid_response[module].append(value)
        details.append(
            {
                "case_id": row.get("case_id", ""),
                "sample_id": row.get("sample_id", ""),
                "variant": row.get("variant", ""),
                "expected_axis": row.get("expected_axis", ""),
                **{f"trigger_{name}": str(value).lower() for name, value in row_triggers.items()},
                "target_component_detected": str(target_detected).lower(),
                "manual_candidate_valid": "" if candidate_valid is None else str(candidate_valid).lower(),
                "manual_mutation_visible": "" if mutation_visible is None else str(mutation_visible).lower(),
            }
        )

    manual_rows = [row for row in rows if _bool(row.get("candidate_valid", "")) is not None]
    valid_visible_rows = [
        row for row in manual_rows
        if _bool(row.get("candidate_valid", "")) is True
        and _bool(row.get("mutation_visible", "")) is True
    ]
    invalid_or_invisible_rows = [
        row for row in manual_rows
        if _bool(row.get("candidate_valid", "")) is False
        or _bool(row.get("mutation_visible", "")) is False
    ]
    summary: dict[str, Any] = {
        "validator": "validate_metric_v2_retained",
        "scope": "retained controlled mid-severity panel; four cases per each of 157 documents",
        "rows": len(rows),
        "unique_documents": len({row.get("sample_id") for row in rows}),
        "score_status_counts": dict(status_counts),
        "trigger_policy": TRIGGER_POLICY,
        "trigger_policy_status": "diagnostic smoke thresholds, not quality grades",
        "expected_component_detection_rate": {
            axis: {"cases": len(values), "rate": _rate(values)}
            for axis, values in sorted(expected_detection.items())
        },
        "valid_visible_expected_component_detection_rate": {
            axis: {"cases": len(values), "rate": _rate(values)}
            for axis, values in sorted(valid_expected_detection.items())
        },
        "invalid_or_invisible_trigger_rate": {
            module: {"cases": len(values), "trigger_rate": _rate(values)}
            for module, values in sorted(invalid_response.items())
        },
        "response_matrix": {
            axis: {
                module: {"cases": len(values), "trigger_rate": _rate(values)}
                for module, values in sorted(modules.items())
            }
            for axis, modules in sorted(response_matrix.items())
        },
        "manual_post_unblind": {
            "rows_with_review": len(manual_rows),
            "valid_and_visible_rows": len(valid_visible_rows),
            "invalid_or_invisible_rows": len(invalid_or_invisible_rows),
            "candidate_valid_rate": _rate([
                value for row in manual_rows if (value := _bool(row.get("candidate_valid", ""))) is not None
            ]),
            "mutation_visible_rate": _rate([
                value for row in manual_rows if (value := _bool(row.get("mutation_visible", ""))) is not None
            ]),
            "target_box_correct_rate": _rate([
                value for row in manual_rows if (value := _bool(row.get("target_box_correct", ""))) is not None
            ]),
            "label_correct_rate": _rate([
                value for row in manual_rows if (value := _bool(row.get("label_correct", ""))) is not None
            ]),
            "predicted_box_useful_rate": _rate([
                value for row in manual_rows if (value := _bool(row.get("predicted_box_useful", ""))) is not None
            ]),
            "predicted_box_partial_count": sum(
                row.get("predicted_box_useful", "").strip().lower() == "partial"
                for row in manual_rows
            ),
        },
        "release_decision": {
            "universal_scalar": "rejected",
            "component_vector": "research prototype: retain raw values with evidence and abstentions",
            "specialized_structure": "abstain until common validated table/formula/figure extraction",
        },
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "validation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (args.out_dir / "case_detection_matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(details[0]))
        writer.writeheader()
        writer.writerows(details)
    print(json.dumps(summary, indent=2))
    return 0 if status_counts.get("failed", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
