#!/usr/bin/env python3
"""Measure agreement between two blinded LLM passes on the controlled audit."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _bool(value: str) -> bool:
    return value.strip().lower() == "true"


def _kappa(left: list[str], right: list[str]) -> float | None:
    if len(left) != len(right) or not left:
        return None
    observed = sum(a == b for a, b in zip(left, right)) / len(left)
    labels = set(left) | set(right)
    left_counts = Counter(left)
    right_counts = Counter(right)
    expected = sum(
        (left_counts[label] / len(left)) * (right_counts[label] / len(right))
        for label in labels
    )
    return (observed - expected) / (1.0 - expected) if expected < 1.0 else 1.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    first_rows = _read(args.first)
    second_rows = _read(args.second)
    first = {row["case_id"]: row for row in first_rows}
    second = {row["case_id"]: row for row in second_rows}
    if len(first) != 208 or len(second) != 208 or set(first) != set(second):
        raise ValueError("expected two exact 208-case audit sets")

    details = []
    state_left = []
    state_right = []
    both_nonabstain = []
    for case_id in [row["case_id"] for row in first_rows]:
        left = first[case_id]
        right = second[case_id]
        left_state = "abstain" if _bool(left["abstain"]) else left["changed_panel"]
        right_state = "abstain" if _bool(right["abstain"]) else right["changed_panel"]
        state_left.append(left_state)
        state_right.append(right_state)
        if left_state != "abstain" and right_state != "abstain":
            both_nonabstain.append((left, right))
        details.append(
            {
                "case_id": case_id,
                "first_state": left_state,
                "second_state": right_state,
                "state_agreement": str(left_state == right_state).lower(),
                "first_axis": left["visible_defect_axis"],
                "second_axis": right["visible_defect_axis"],
                "axis_agreement": str(left["visible_defect_axis"] == right["visible_defect_axis"]).lower(),
                "first_confidence": left["confidence"],
                "second_confidence": right["confidence"],
            }
        )
    result = {
        "analysis": "controlled_reaudit_agreement",
        "cases": 208,
        "first_abstain_count": sum(state == "abstain" for state in state_left),
        "second_abstain_count": sum(state == "abstain" for state in state_right),
        "panel_or_abstain_exact_agreement": sum(a == b for a, b in zip(state_left, state_right)) / 208,
        "panel_or_abstain_cohen_kappa": _kappa(state_left, state_right),
        "both_nonabstain_cases": len(both_nonabstain),
        "changed_panel_agreement_when_both_nonabstain": (
            sum(left["changed_panel"] == right["changed_panel"] for left, right in both_nonabstain) / len(both_nonabstain)
            if both_nonabstain else None
        ),
        "axis_agreement_when_both_nonabstain": (
            sum(left["visible_defect_axis"] == right["visible_defect_axis"] for left, right in both_nonabstain) / len(both_nonabstain)
            if both_nonabstain else None
        ),
        "interpretation": "Agreement between two blinded LLM passes is an audit-repeatability diagnostic, not human perceptual ground truth.",
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "reaudit_case_agreement.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(details[0]))
        writer.writeheader()
        writer.writerows(details)
    (args.out_dir / "reaudit_agreement.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
