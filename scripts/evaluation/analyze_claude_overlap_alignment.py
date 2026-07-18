#!/usr/bin/env python3
"""Compare blinded visual findings with raw overlap metrics, without ranking models."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from scipy.stats import spearmanr


MODEL_ROLE = {
    "Gemini 3.1 Flash Lite": "gemini",
    "Claude Sonnet 4.6": "claude_sonnet",
    "Claude Opus 4.7": "claude_opus",
}
SEVERITY = {"none": 0, "minor": 1, "moderate": 2, "major": 3}
LOSS_FIELDS = {
    "strict_content_loss": ("strict_word_f1", lambda value: 1.0 - value),
    "critical_number_loss": ("number_f1", lambda value: 1.0 - value),
    "token_center_displacement_q90": ("token_center_displacement_q90", lambda value: value),
    "text_ltsim_loss": ("text_ltsim_page_macro", lambda value: 1.0 - value),
    "font_size_log_error_q90": ("font_size_log_error_q90", lambda value: value),
    "page_count_abs_delta": ("page_count_delta", abs),
    "ink_residual_loss": ("unregistered_ink_f1", lambda value: 1.0 - value),
    "ssim_loss": ("unregistered_ssim", lambda value: 1.0 - value),
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _number(value: str) -> float | None:
    if value == "":
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def _correlation(pairs: list[tuple[float, float]]) -> dict[str, Any]:
    if len(pairs) < 3:
        return {"pairs": len(pairs), "spearman_rho": None, "p_value_descriptive": None}
    rho, p_value = spearmanr([left for left, _ in pairs], [right for _, right in pairs])
    return {
        "pairs": len(pairs),
        "spearman_rho": None if not math.isfinite(float(rho)) else float(rho),
        "p_value_descriptive": None if not math.isfinite(float(p_value)) else float(p_value),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path)
    parser.add_argument("findings", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    scores = _read(args.scores)
    findings = _read(args.findings)
    score_by_key = {(row["sample_id"], row["asset_role"]): row for row in scores}
    if len(score_by_key) != 21 or len(findings) != 21:
        raise ValueError("expected exactly 21 unique overlap scores and findings")

    merged = []
    correlations: dict[str, list[tuple[float, float]]] = defaultdict(list)
    within_sample: dict[str, dict[str, list[tuple[float, float]]]] = defaultdict(lambda: defaultdict(list))
    for finding in findings:
        role = MODEL_ROLE[finding["model"]]
        score = score_by_key[(finding["sample_id"], role)]
        severity = SEVERITY[finding["visible_defect_severity"]]
        row = dict(finding)
        row["asset_role"] = role
        row["severity_ordinal"] = severity
        for loss_name, (field, transform) in LOSS_FIELDS.items():
            value = _number(score.get(field, ""))
            loss = transform(value) if value is not None else None
            row[loss_name] = "" if loss is None else loss
            if loss is not None:
                correlations[loss_name].append((severity, loss))
                within_sample[finding["sample_id"]][loss_name].append((severity, loss))
        row["metric_evidence_json"] = score.get("v2_evidence_json", "")
        row["protocol_id"] = score.get("protocol_id", "")
        row["canvas_exact_size_rate"] = score.get("canvas_exact_size_rate", "")
        merged.append(row)

    sample_correlations: dict[str, list[float]] = defaultdict(list)
    for metric_sets in within_sample.values():
        for name, pairs in metric_sets.items():
            result = _correlation(pairs)
            rho = result["spearman_rho"]
            if rho is not None:
                sample_correlations[name].append(rho)
    result = {
        "analysis": "claude_overlap_manual_metric_alignment",
        "pairs": len(merged),
        "complete_samples": len(within_sample),
        "fair_leaderboard_eligible": False,
        "severity_counts": {
            label: sum(row["visible_defect_severity"] == label for row in findings)
            for label in SEVERITY
        },
        "global_descriptive_spearman": {
            name: _correlation(pairs) for name, pairs in correlations.items()
        },
        "within_sample_spearman_macro": {
            name: {
                "samples_with_defined_rho": len(values),
                "mean_rho": sum(values) / len(values) if values else None,
                "values": values,
            }
            for name, values in sorted(sample_correlations.items())
        },
        "interpretation": (
            "Alignment is diagnostic only: 21 outputs, one non-human reviewer, and heterogeneous "
            "generation protocols. Missing SSIM values are abstentions caused by canvas mismatch."
        ),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    output_csv = args.out_dir / "manual_metric_alignment.csv"
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(merged[0]), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged)
    (args.out_dir / "manual_metric_alignment.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
