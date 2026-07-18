#!/usr/bin/env python3
"""Align all-156 blinded visual issue labels with metric-v2 components."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any, Callable

import numpy as np
from scipy.stats import rankdata, spearmanr


SEVERITY = {"none": 0, "minor": 1, "moderate": 2, "major": 3, "unclear": None}
AXES: dict[str, tuple[str, Callable[[dict[str, str]], float | None]]] = {}


def _number(row: dict[str, str], name: str) -> float | None:
    value = row.get(name, "")
    if value == "":
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def _one_minus(name: str) -> Callable[[dict[str, str]], float | None]:
    def function(row: dict[str, str]) -> float | None:
        value = _number(row, name)
        return None if value is None else 1.0 - value
    return function


AXES.update({
    "content": ("content_issue", _one_minus("strict_word_f1")),
    "layout_text_ltsim": ("layout_issue", _one_minus("text_ltsim_page_macro")),
    "layout_token_displacement": ("layout_issue", lambda row: _number(row, "token_center_displacement_q90")),
    "typography": ("typography_issue", lambda row: _number(row, "font_size_log_error_q90")),
    "pagination_page_count": ("pagination_issue", lambda row: abs(_number(row, "page_count_delta") or 0.0)),
    "pagination_boundary": ("pagination_issue", _one_minus("page_break_f1")),
})


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _bool(value: str) -> bool:
    return value.strip().lower() == "true"


def _auc(labels: list[int], losses: list[float]) -> float | None:
    positives = sum(labels)
    negatives = len(labels) - positives
    if not positives or not negatives:
        return None
    ranks = rankdata(losses, method="average")
    rank_sum_positive = sum(rank for rank, label in zip(ranks, labels) if label)
    return float((rank_sum_positive - positives * (positives + 1) / 2) / (positives * negatives))


def _axis_analysis(rows: list[dict[str, str]], issue_field: str, loss_function: Callable[[dict[str, str]], float | None]) -> dict[str, Any]:
    values = []
    for row in rows:
        severity = SEVERITY.get(row.get(issue_field, "unclear"))
        loss = loss_function(row)
        if severity is not None and loss is not None:
            values.append((severity, loss))
    if len(values) < 3:
        return {"pairs": len(values), "spearman_rho": None, "issue_auc": None}
    rho, p_value = spearmanr([item[0] for item in values], [item[1] for item in values])
    labels = [int(severity > 0) for severity, _ in values]
    return {
        "pairs": len(values),
        "manual_issue_pairs": sum(labels),
        "manual_none_pairs": len(labels) - sum(labels),
        "spearman_rho": None if not math.isfinite(float(rho)) else float(rho),
        "p_value_descriptive": None if not math.isfinite(float(p_value)) else float(p_value),
        "issue_auc": _auc(labels, [item[1] for item in values]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path)
    parser.add_argument("blind_audit", type=Path)
    parser.add_argument("answer_key", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    scores = {row["sample_id"]: row for row in _read(args.scores)}
    answers = {row["audit_case_id"]: row for row in _read(args.answer_key)}
    audits = _read(args.blind_audit)
    if len(scores) != 156 or len(answers) != 156 or len(audits) != 156:
        raise ValueError("expected 156 score/audit/answer rows")
    merged = []
    for audit in audits:
        answer = answers[audit["audit_case_id"]]
        score = scores[answer["sample_id"]]
        row = {**audit, **answer}
        for name in (
            "strict_word_f1", "number_f1", "token_center_displacement_q90",
            "text_ltsim_page_macro", "font_size_log_error_q90", "unregistered_ink_f1",
            "unregistered_ssim", "page_count_delta", "page_break_f1", "canvas_exact_size_rate",
            "v2_evidence_json",
        ):
            row[name] = score.get(name, "")
        numeric_severities = [
            SEVERITY.get(audit[field])
            for field in ("content_issue", "layout_issue", "typography_issue", "pagination_issue", "specialized_issue")
        ]
        row["maximum_issue_severity_ordinal"] = max(
            (value for value in numeric_severities if value is not None), default=""
        )
        merged.append(row)

    result = {
        "analysis": "ai_visual_alignment_v2",
        "pairs": len(merged),
        "reviewer_type": "LLM research audit; no human ratings",
        "aggregate_score": None,
        "axis_alignment": {
            name: _axis_analysis(merged, issue_field, loss_function)
            for name, (issue_field, loss_function) in AXES.items()
        },
        "specialized_structure": {
            "manual_issue_pairs": sum(row["specialized_issue"] not in {"none", "unclear"} for row in merged),
            "automatic_metric": "abstain for all 156; no validated common table/formula/figure extraction",
        },
        "post_unblind": {
            "top_residual_box_useful_rate": sum(_bool(row["top_residual_box_useful_after_unblind"]) for row in merged) / len(merged),
            "axis_labels_plausible_rate": sum(_bool(row["axis_labels_plausible_after_unblind"]) for row in merged) / len(merged),
            "canvas_confound_rate": sum(_bool(row["canvas_confound"]) for row in merged) / len(merged),
        },
        "interpretation": (
            "AUC and rho assess consistency with one blinded LLM visual audit, not perceptual validity. "
            "AUC 0.5 is chance and 1.0 perfect directionality. Canvas-confounded SSIM abstentions remain missing."
        ),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    with (args.out_dir / "ai_manual_metric_alignment.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(merged[0]), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged)
    (args.out_dir / "ai_manual_metric_alignment.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
