#!/usr/bin/env python3
"""Join the frozen blind review with automated scorecard values."""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULT = ROOT / "results/metric_calibration/canonical_ai_v0_3"


def number(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def mean_present(*values: float | None) -> float | None:
    present = [value for value in values if value is not None]
    return float(np.mean(present)) if present else None


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def correlation(rows: list[dict], metric: str, judgment: str) -> dict:
    pairs = [
        (row[metric], row[judgment])
        for row in rows
        if row.get(metric) is not None and row.get(judgment) is not None
    ]
    if len(pairs) < 3:
        return {"n": len(pairs), "rho": None, "p_value": None}
    rho, p_value = spearmanr([pair[0] for pair in pairs], [pair[1] for pair in pairs])
    return {"n": len(pairs), "rho": float(rho), "p_value": float(p_value)}


def pairwise_rank_accuracy(rows: list[dict], metric: str) -> dict:
    correct = 0
    evaluated = 0
    ties = 0
    by_sample: dict[str, list[dict]] = {}
    for row in rows:
        if row.get(metric) is not None and row.get("manual_rank") is not None:
            by_sample.setdefault(row["sample_id"], []).append(row)
    for sample_rows in by_sample.values():
        for left_index, left in enumerate(sample_rows):
            for right in sample_rows[left_index + 1:]:
                if left["manual_rank"] == right["manual_rank"]:
                    continue
                delta = left[metric] - right[metric]
                evaluated += 1
                if abs(delta) < 1e-12:
                    ties += 1
                    continue
                manual_prefers_left = left["manual_rank"] < right["manual_rank"]
                metric_prefers_left = delta > 0
                correct += int(manual_prefers_left == metric_prefers_left)
    return {
        "pairs": evaluated,
        "correct": correct,
        "ties": ties,
        "accuracy": correct / evaluated if evaluated else None,
    }


def isotonic_fit(x_values: list[float], y_values: list[float]) -> list[dict]:
    ordered = sorted(zip(x_values, y_values))
    groups: list[dict] = []
    for x_value, y_value in ordered:
        if groups and abs(groups[-1]["x_sum"] / groups[-1]["weight"] - x_value) < 1e-12:
            groups[-1]["x_sum"] += x_value
            groups[-1]["y_sum"] += y_value
            groups[-1]["weight"] += 1
        else:
            groups.append({"x_sum": x_value, "y_sum": y_value, "weight": 1})
    index = 0
    while index < len(groups) - 1:
        left = groups[index]
        right = groups[index + 1]
        if left["y_sum"] / left["weight"] <= right["y_sum"] / right["weight"]:
            index += 1
            continue
        left["x_sum"] += right["x_sum"]
        left["y_sum"] += right["y_sum"]
        left["weight"] += right["weight"]
        groups.pop(index + 1)
        index = max(0, index - 1)
    return [
        {
            "x": group["x_sum"] / group["weight"],
            "y": group["y_sum"] / group["weight"],
            "weight": group["weight"],
        }
        for group in groups
    ]


def isotonic_predict(knots: list[dict], value: float) -> float:
    return float(np.interp(value, [knot["x"] for knot in knots], [knot["y"] for knot in knots]))


def leave_one_sample_out_calibration(rows: list[dict], metric: str) -> dict:
    predictions: list[float] = []
    observed: list[float] = []
    for sample_id in sorted({row["sample_id"] for row in rows}):
        training = [row for row in rows if row["sample_id"] != sample_id]
        testing = [row for row in rows if row["sample_id"] == sample_id]
        knots = isotonic_fit(
            [row[metric] for row in training],
            [row["manual_overall"] for row in training],
        )
        predictions.extend(isotonic_predict(knots, row[metric]) for row in testing)
        observed.extend(row["manual_overall"] for row in testing)
    rho, p_value = spearmanr(predictions, observed)
    rounded = [min(4, max(0, round(value))) for value in predictions]
    return {
        "n": len(observed),
        "mae": float(np.mean(np.abs(np.asarray(predictions) - np.asarray(observed)))),
        "rho": float(rho),
        "p_value": float(p_value),
        "rounded_exact": float(np.mean(np.asarray(rounded) == np.asarray(observed))),
        "rounded_within_one": float(np.mean(np.abs(np.asarray(rounded) - np.asarray(observed)) <= 1)),
        "full_fit_knots": isotonic_fit(
            [row[metric] for row in rows], [row["manual_overall"] for row in rows]
        ),
    }


def attach_cross_validated_grade(rows: list[dict], metric: str) -> None:
    for sample_id in sorted({row["sample_id"] for row in rows}):
        training = [row for row in rows if row["sample_id"] != sample_id]
        testing = [row for row in rows if row["sample_id"] == sample_id]
        knots = isotonic_fit(
            [row[metric] for row in training],
            [row["manual_overall"] for row in training],
        )
        for row in testing:
            grade = isotonic_predict(knots, row[metric])
            row["cv_grade_continuous_0_4"] = grade
            row["cv_grade_rounded_0_4"] = min(4, max(0, round(grade)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result-dir", type=Path, default=DEFAULT_RESULT)
    args = parser.parse_args()

    result_dir = args.result_dir
    audit_dir = result_dir / "manual_audit"
    manual = {row["blind_id"]: row for row in read_rows(audit_dir / "manual_rubric.csv")}
    blind_map = read_rows(audit_dir / "blind_case_map.csv")
    scorecard = {
        (row["sample_id"], row["candidate_key"]): row
        for row in read_rows(result_dir / "canonical_ai_scorecard.csv")
    }

    joined: list[dict] = []
    for case in blind_map:
        judgment = manual[case["blind_id"]]
        automated = scorecard[(case["sample_id"], case["candidate_key"])]
        if automated["candidate_state"] != "ok":
            continue
        row = {
            "blind_id": case["blind_id"],
            "sample_id": case["sample_id"],
            "display_label": case["display_label"],
            "model_id": case["model_id"],
            "protocol_id": case["protocol_id"],
            "manual_content": number(judgment["content_0_4"]),
            "manual_layout": number(judgment["layout_0_4"]),
            "manual_typography": number(judgment["typography_0_4"]),
            "manual_structure": number(judgment["structure_0_4"]),
            "manual_overall": number(judgment["overall_0_4"]),
            "manual_rank": number(judgment["within_sample_rank"]),
            "manual_confidence": judgment["confidence_low_medium_high"],
            "manual_notes": judgment["notes"],
            "auto_content": number(automated["content"]),
            "token_precision": number(automated["token_precision"]),
            "token_recall": number(automated["token_recall"]),
            "auto_layout": number(automated["layout"]),
            "layout_coverage": number(automated["layout_coverage_min"]),
            "auto_typography": number(automated["typography"]),
            "appearance_proxy": number(automated["appearance_proxy"]),
            "appearance_local_q10": number(automated["appearance_local_q10"]),
            "nontext_score": number(automated["nontext_score"]),
            "auto_pagination": number(automated["pagination"]),
            "table_row_exact": number(automated["table_row_exact_rate"]),
            "table_column_exact": number(automated["table_column_exact_rate"]),
            "table_cell_ratio": number(automated["table_cell_count_ratio"]),
            "formula_character_f1": number(automated["formula_character_f1"]),
            "scorecard_status": automated["scorecard_status"],
            "failed_gates": automated["failed_gates"],
            "review_flags": automated["review_flags"],
            "diagnostic_flags": automated.get("diagnostic_flags", ""),
        }
        row["visual_core_mean"] = mean_present(
            row["auto_layout"], row["auto_typography"], row["auto_pagination"]
        )
        row["visual_core_floor"] = min(
            row["auto_layout"], row["auto_typography"], row["auto_pagination"]
        )
        row["fidelity_core_floor"] = min(
            row["auto_content"], row["auto_layout"], row["auto_typography"],
            row["auto_pagination"]
        )
        row["all_axis_mean"] = mean_present(
            row["auto_content"], row["auto_layout"], row["auto_typography"],
            row["appearance_proxy"], row["auto_pagination"]
        )
        joined.append(row)

    attach_cross_validated_grade(joined, "fidelity_core_floor")
    fields = list(joined[0])
    with (audit_dir / "manual_judgments_unblinded.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(joined)

    targets = {
        "content": ["auto_content", "token_precision", "token_recall", "formula_character_f1"],
        "layout": ["auto_layout", "layout_coverage", "auto_pagination", "appearance_proxy"],
        "typography": ["auto_typography", "appearance_proxy"],
        "structure": ["nontext_score", "auto_pagination", "table_row_exact", "table_column_exact", "table_cell_ratio"],
        "overall": ["auto_content", "auto_layout", "auto_typography", "appearance_proxy", "auto_pagination", "visual_core_mean", "visual_core_floor", "fidelity_core_floor", "all_axis_mean"],
    }
    correlations = {
        target: {
            metric: correlation(joined, metric, f"manual_{target}")
            for metric in metrics
        }
        for target, metrics in targets.items()
    }
    ranking_metrics = [
        "auto_content", "auto_layout", "auto_typography", "appearance_proxy",
        "appearance_local_q10", "auto_pagination", "visual_core_mean",
        "visual_core_floor", "fidelity_core_floor", "all_axis_mean",
    ]
    rankings = {metric: pairwise_rank_accuracy(joined, metric) for metric in ranking_metrics}
    calibration_metrics = [
        "auto_layout", "appearance_proxy", "auto_pagination", "visual_core_mean",
        "visual_core_floor", "fidelity_core_floor", "all_axis_mean",
    ]
    calibration = {
        metric: leave_one_sample_out_calibration(joined, metric)
        for metric in calibration_metrics
    }
    by_protocol: dict[str, list[dict]] = {}
    for row in joined:
        by_protocol.setdefault(row["protocol_id"], []).append(row)
    protocol_summary = {
        protocol_id: {
            "display_label": protocol_rows[0]["display_label"],
            "n": len(protocol_rows),
            "samples": sorted(row["sample_id"] for row in protocol_rows),
            "manual_overall_mean": float(np.mean([row["manual_overall"] for row in protocol_rows])),
            "cross_validated_grade_mean": float(np.mean([row["cv_grade_continuous_0_4"] for row in protocol_rows])),
            "manual_grade_counts": {
                str(grade): sum(row["manual_overall"] == grade for row in protocol_rows)
                for grade in range(5)
            },
        }
        for protocol_id, protocol_rows in sorted(by_protocol.items())
    }
    head_to_head = []
    for left_id, right_id in combinations(sorted(by_protocol), 2):
        left_by_sample = {row["sample_id"]: row for row in by_protocol[left_id]}
        right_by_sample = {row["sample_id"]: row for row in by_protocol[right_id]}
        shared = sorted(set(left_by_sample) & set(right_by_sample))
        if not shared:
            continue
        left_wins = right_wins = ties = 0
        for sample_id in shared:
            left_rank = left_by_sample[sample_id]["manual_rank"]
            right_rank = right_by_sample[sample_id]["manual_rank"]
            if left_rank < right_rank:
                left_wins += 1
            elif right_rank < left_rank:
                right_wins += 1
            else:
                ties += 1
        head_to_head.append({
            "left_protocol": left_id,
            "left_label": left_by_sample[shared[0]]["display_label"],
            "right_protocol": right_id,
            "right_label": right_by_sample[shared[0]]["display_label"],
            "shared_samples": len(shared),
            "left_wins": left_wins,
            "right_wins": right_wins,
            "ties": ties,
        })
    result = {
        "manual_cases": len(joined),
        "samples": len({row["sample_id"] for row in joined}),
        "method": "Frozen blind rubric judgments joined only after scoring; Spearman correlations are exploratory on a small, non-independent convenience sample.",
        "selected_grade": {
            "input": "fidelity_core_floor = min(content, layout, typography, pagination)",
            "calibration": "monotonic isotonic mapping to the blind overall 0-4 rubric",
            "selection_reason": "lowest leave-one-sample-out MAE among the tested interpretable composites; the floor prevents one strong axis from cancelling a severe failure",
            "deployment_warning": "The full-fit knots are development calibration only. Report held-out prompt-dev or benchmark results separately before making model claims.",
        },
        "correlations": correlations,
        "within_sample_pairwise_ranking": rankings,
        "leave_one_sample_out_isotonic_calibration": calibration,
        "protocol_summary": protocol_summary,
        "blind_head_to_head": head_to_head,
    }
    (audit_dir / "manual_validation.json").write_text(json.dumps(result, indent=2) + "\n")

    lines = [
        "# Blind manual validation", "",
        f"- Rated compiled cases: {len(joined)} across {result['samples']} samples",
        "- The reviewer saw only anonymous candidate IDs until the rubric CSV was frozen.",
        "- Correlations are diagnostic, not population estimates: candidates within a sample share one reference and n is small.",
        "", "## Spearman correlations", "",
        "| Manual target | Automated metric | n | rho | p |", "|---|---:|---:|---:|---:|",
    ]
    for target, metric_results in correlations.items():
        for metric, values in metric_results.items():
            rho = "NA" if values["rho"] is None else f"{values['rho']:.3f}"
            p_value = "NA" if values["p_value"] is None else f"{values['p_value']:.3f}"
            lines.append(f"| {target} | {metric} | {values['n']} | {rho} | {p_value} |")
    lines.extend(["", "## Within-sample pairwise ranking", "", "| Metric | Correct / pairs | Ties | Accuracy |", "|---|---:|---:|---:|"])
    for metric, values in rankings.items():
        accuracy = "NA" if values["accuracy"] is None else f"{values['accuracy']:.1%}"
        lines.append(f"| {metric} | {values['correct']} / {values['pairs']} | {values['ties']} | {accuracy} |")
    lines.extend([
        "", "## Leave-one-sample-out monotonic calibration", "",
        "Each held-out sample is graded by a monotonic mapping fitted without any candidate from that reference.",
        "", "| Input | MAE on 0-4 | rho | Rounded exact | Within one |",
        "|---|---:|---:|---:|---:|",
    ])
    for metric, values in calibration.items():
        lines.append(
            f"| {metric} | {values['mae']:.3f} | {values['rho']:.3f} | "
            f"{values['rounded_exact']:.1%} | {values['rounded_within_one']:.1%} |"
        )
    lines.extend([
        "", "## Exact-protocol summaries", "",
        "Means are descriptive only because protocols cover different sample sets.",
        "", "| Exact protocol | n | Blind overall mean | Cross-validated grade mean |",
        "|---|---:|---:|---:|",
    ])
    for values in protocol_summary.values():
        lines.append(
            f"| {values['display_label']} | {values['n']} | "
            f"{values['manual_overall_mean']:.2f} | {values['cross_validated_grade_mean']:.2f} |"
        )
    lines.extend([
        "", "## Blind head-to-head on shared references", "",
        "| Left protocol | Right protocol | Shared | Left wins | Right wins | Ties |",
        "|---|---|---:|---:|---:|---:|",
    ])
    for values in head_to_head:
        lines.append(
            f"| {values['left_label']} | {values['right_label']} | {values['shared_samples']} | "
            f"{values['left_wins']} | {values['right_wins']} | {values['ties']} |"
        )
    (audit_dir / "manual_validation.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
