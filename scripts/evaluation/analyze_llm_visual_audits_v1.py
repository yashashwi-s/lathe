#!/usr/bin/env python3
"""Analyze frozen LLM visual audits without creating an overall quality grade."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results" / "metric_research_v1"
CONTROL = BASE / "full_157_v1" / "visual_audit"
AI = BASE / "ai_outputs_frozen_v1"
AI_AUDIT = AI / "visual_audit"
TRIAL = BASE / "ai_outputs_center_q90_trial_v1"
ISSUE_LEVELS = {"none": 0, "minor": 1, "moderate": 2, "major": 3}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _bool(value: str) -> bool | None:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def _rate(values: list[bool | None]) -> dict:
    scored = [value for value in values if value is not None]
    return {
        "true": sum(scored),
        "false": len(scored) - sum(scored),
        "missing": len(values) - len(scored),
        "rate": sum(scored) / len(scored) if scored else None,
    }


def _ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    start = 0
    while start < len(order):
        end = start + 1
        while end < len(order) and values[order[end]] == values[order[start]]:
            end += 1
        rank = (start + end - 1) / 2 + 1
        for index in order[start:end]:
            ranks[index] = rank
        start = end
    return ranks


def _spearman(left: list[float], right: list[float]) -> float | None:
    if len(left) < 3 or len(left) != len(right):
        return None
    x = _ranks(left)
    y = _ranks(right)
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    numerator = sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y))
    denominator = math.sqrt(
        sum((a - x_mean) ** 2 for a in x) * sum((b - y_mean) ** 2 for b in y)
    )
    return numerator / denominator if denominator else None


def _controlled(responses: list[dict[str, str]], answers: list[dict[str, str]]) -> dict:
    answer_by_case = {row["case_id"]: row for row in answers}
    abstained = [row for row in responses if row["abstain"].lower() == "true"]
    judged = [row for row in responses if row["abstain"].lower() == "false"]
    panel_correct = []
    axis_correct = []
    for row in judged:
        answer = answer_by_case[row["case_id"]]
        panel_correct.append(row["changed_panel"] == answer["candidate_panel_hidden_truth"])
        expected = answer["expected_axis"].replace("_only", "")
        axis_correct.append(row["visible_defect_axis"] in expected.split("+"))
    post_fields = (
        "candidate_valid", "mutation_visible", "target_box_correct", "label_correct",
        "predicted_box_useful",
    )
    by_variant: dict[str, list[bool]] = defaultdict(list)
    for row in judged:
        answer = answer_by_case[row["case_id"]]
        by_variant[answer["variant"]].append(
            row["changed_panel"] == answer["candidate_panel_hidden_truth"]
        )
    return {
        "cases": len(responses),
        "judged": len(judged),
        "abstained": len(abstained),
        "coverage": len(judged) / len(responses) if responses else None,
        "changed_panel_accuracy": sum(panel_correct) / len(panel_correct) if panel_correct else None,
        "axis_label_accuracy": sum(axis_correct) / len(axis_correct) if axis_correct else None,
        "post_unblind": {
            field: _rate([_bool(row[field]) for row in answers]) for field in post_fields
        },
        "variant_panel_accuracy": {
            variant: {"cases": len(values), "accuracy": sum(values) / len(values)}
            for variant, values in sorted(by_variant.items())
        },
    }


def _ai(
    responses: list[dict[str, str]], answers: list[dict[str, str]],
    scores: list[dict[str, str]], trial_scores: list[dict[str, str]],
) -> dict:
    answer_by_case = {row["audit_case_id"]: row for row in answers}
    score_by_sample = {row["sample_id"]: row for row in scores}
    trial_by_sample = {row["sample_id"]: row for row in trial_scores}
    issue_fields = {
        "content": "content_issue", "layout": "layout_issue",
        "typography": "typography_issue", "pagination": "pagination_issue",
        "structure": "specialized_issue",
    }
    axes = {}
    for axis, issue_field in issue_fields.items():
        pairs = []
        grouped: dict[str, list[float]] = defaultdict(list)
        for response in responses:
            label = response[issue_field].strip().lower()
            if label not in ISSUE_LEVELS:
                continue
            sample = answer_by_case[response["audit_case_id"]]["sample_id"]
            source = trial_by_sample[sample] if axis == "layout" else score_by_sample[sample]
            value = source.get(f"axis_{axis}", "")
            if value == "":
                continue
            score = float(value)
            pairs.append((score, float(ISSUE_LEVELS[label])))
            grouped[label].append(score)
        axes[axis] = {
            "cases": len(pairs),
            "score_source": (
                "center_displacement_q90 trial" if axis == "layout" else "frozen v1 raw axis"
            ),
            "spearman_score_vs_issue_severity": _spearman(
                [pair[0] for pair in pairs], [pair[1] for pair in pairs]
            ),
            "expected_direction": "negative: higher fidelity score, lower visible issue severity",
            "median_score_by_issue": {
                label: median(values) for label, values in sorted(grouped.items())
            },
            "issue_counts": dict(Counter(
                row[issue_field].strip().lower() for row in responses
            )),
        }
    return {
        "cases": len(responses),
        "axes": axes,
        "residual_box_useful_after_unblind": _rate([
            _bool(row["top_residual_box_useful_after_unblind"]) for row in answers
        ]),
        "axis_labels_plausible_after_unblind": _rate([
            _bool(row["axis_labels_plausible_after_unblind"]) for row in answers
        ]),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=BASE / "llm_visual_audit_analysis_v1.json")
    args = parser.parse_args()
    result = {
        "method": "llm_visual_audit_analysis_v1",
        "claim_boundary": (
            "Model-assisted visual audit can falsify projections and check visible association; "
            "it is not human ground truth and does not define an overall quality grade."
        ),
        "controlled": _controlled(
            _read(CONTROL / "blind_response_manifest.csv"),
            _read(CONTROL / "audit_answer_key.csv"),
        ),
        "ai_outputs": _ai(
            _read(AI_AUDIT / "blind_ai_response_manifest.csv"),
            _read(AI_AUDIT / "ai_audit_answer_key.csv"),
            _read(AI / "ai_output_axis_scores.csv"),
            _read(TRIAL / "ai_output_axis_scores.csv"),
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
