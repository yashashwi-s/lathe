#!/usr/bin/env python3
"""Summarize metric-v2 evidence with the metric-harness gate ladder.

The ladder is intentionally non-compensatory: visual polish cannot make up for
wrong pagination, missing text, invented text, or incorrect numbers.  This
script reports gates and drivers separately and never constructs a scalar
benchmark score.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TOKEN_THRESHOLD = 0.95
EPSILON = 1e-12


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def get(value: dict[str, Any], dotted_path: str) -> Any:
    current: Any = value
    for part in dotted_path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def evidence_for(row: dict[str, str]) -> dict[str, Any]:
    evidence_path = row.get("v2_evidence_json", "")
    if not evidence_path:
        raise ValueError(f"{row.get('sample_id', 'unknown')}: missing v2_evidence_json")
    path = resolve(evidence_path)
    if not path.exists():
        raise FileNotFoundError(f"{row.get('sample_id', 'unknown')}: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def driver_mean(ink_f1: float | None, ltsim: float | None,
                center_q90: float | None) -> float | None:
    """Convenience summary used by the harness, not a metric-v2 score."""
    if ink_f1 is None or ltsim is None or center_q90 is None:
        return None
    return mean((ink_f1, ltsim, 1.0 - center_q90))


def summarize_row(row: dict[str, str]) -> dict[str, Any]:
    evidence = evidence_for(row)
    strict_inventory = get(
        evidence, "axes.content.metrics.strict_nfc_token_inventory"
    ) or {}
    precision = number(strict_inventory.get("precision"))
    recall = number(strict_inventory.get("recall"))
    page_delta = number(row.get("page_count_delta"))
    number_f1 = number(row.get("number_f1"))
    reference_number_count = number(row.get("reference_number_count"))
    number_applicable = bool(
        reference_number_count is not None and reference_number_count > 0
    )

    gate_page = page_delta is not None and abs(page_delta) <= EPSILON
    gate_recall = recall is not None and recall + EPSILON >= TOKEN_THRESHOLD
    gate_precision = precision is not None and precision + EPSILON >= TOKEN_THRESHOLD
    gate_number = (
        not number_applicable
        or (number_f1 is not None and abs(number_f1 - 1.0) <= EPSILON)
    )
    gates = (gate_page, gate_recall, gate_precision, gate_number)
    failed = [
        name
        for name, passed in zip(
            ("page_count", "token_recall", "token_precision", "number_f1"),
            gates,
        )
        if not passed
    ]

    ink_f1 = number(row.get("registered_ink_f1"))
    ltsim = number(row.get("text_ltsim_page_macro"))
    center_q90 = number(row.get("token_center_displacement_q90"))
    return {
        "sample_id": row.get("sample_id", ""),
        "category": row.get("category", ""),
        "gates_passed": sum(gates),
        "all_gates_passed": all(gates),
        "failed_gates": ",".join(failed),
        "g1_page_count_exact": gate_page,
        "page_count_delta": page_delta,
        "g2_token_recall_at_least_0_95": gate_recall,
        "strict_token_recall": recall,
        "g3_token_precision_at_least_0_95": gate_precision,
        "strict_token_precision": precision,
        "g4_number_f1_exact_when_applicable": gate_number,
        "number_gate_applicable": number_applicable,
        "number_f1": number_f1,
        "registered_ink_f1": ink_f1,
        "text_ltsim_page_macro": ltsim,
        "token_center_displacement_q90": center_q90,
        "driver_mean_diagnostic": driver_mean(ink_f1, ltsim, center_q90),
        "registered_ssim_report_only": number(row.get("registered_ssim")),
        "page_break_f1_report_only": number(row.get("page_break_f1")),
        "strict_word_f1_report_only": number(row.get("strict_word_f1")),
    }


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    gate_counts = {
        "page_count_exact": sum(record["g1_page_count_exact"] for record in records),
        "token_recall_at_least_0_95": sum(
            record["g2_token_recall_at_least_0_95"] for record in records
        ),
        "token_precision_at_least_0_95": sum(
            record["g3_token_precision_at_least_0_95"] for record in records
        ),
        "number_f1_exact_when_applicable": sum(
            record["g4_number_f1_exact_when_applicable"] for record in records
        ),
        "all_four": sum(record["all_gates_passed"] for record in records),
    }
    driver_fields = (
        "registered_ink_f1",
        "text_ltsim_page_macro",
        "token_center_displacement_q90",
    )
    driver_means = {}
    for field in driver_fields:
        values = [record[field] for record in records if record[field] is not None]
        driver_means[field] = mean(values) if values else None
    return {
        "method": "metric_harness_gate_ladder_v1",
        "source_report": "metric_research/report/metric_harness_report.pdf",
        "aggregate_score": None,
        "pairs": len(records),
        "token_threshold": TOKEN_THRESHOLD,
        "gate_counts": gate_counts,
        "gates_passed_distribution": dict(
            sorted(Counter(record["gates_passed"] for record in records).items())
        ),
        "number_gate_applicable_pairs": sum(
            record["number_gate_applicable"] for record in records
        ),
        "driver_means": driver_means,
        "driver_mean_diagnostic": mean(
            record["driver_mean_diagnostic"]
            for record in records
            if record["driver_mean_diagnostic"] is not None
        ),
        "report_only_axes": [
            "registered_ssim",
            "page_break_f1",
            "strict_word_f1",
        ],
    }


def render_markdown(summary: dict[str, Any],
                    records: list[dict[str, Any]]) -> str:
    gates = summary["gate_counts"]
    total = summary["pairs"]
    drivers = summary["driver_means"]
    lines = [
        "# Metric-v2 gate-ladder summary",
        "",
        "This applies the non-compensating interpretation validated by the metric",
        "harness report. There is no aggregate benchmark score: correctness gates",
        "are reported first, followed by independent visual/layout drivers.",
        "",
        "## Correctness gates",
        "",
        f"- Exact page count: {gates['page_count_exact']}/{total}",
        f"- Strict token recall >= 0.95: {gates['token_recall_at_least_0_95']}/{total}",
        f"- Strict token precision >= 0.95: {gates['token_precision_at_least_0_95']}/{total}",
        f"- Number F1 = 1 when applicable: "
        f"{gates['number_f1_exact_when_applicable']}/{total}",
        f"- All four gates: {gates['all_four']}/{total}",
        "",
        "## Independent drivers",
        "",
        f"- Mean registered ink F1 (higher is better): "
        f"{drivers['registered_ink_f1']:.4f}",
        f"- Mean Text-LTSim page macro (higher is better): "
        f"{drivers['text_ltsim_page_macro']:.4f}",
        f"- Mean token center q90 (lower is better): "
        f"{drivers['token_center_displacement_q90']:.4f}",
        "",
        "SSIM, page-break F1, and strict word F1 remain report-only diagnostics.",
        "",
        "## Per compiled output",
        "",
        "| Sample | Gates | Failed gates | Ink F1 | LTSim | Center q90 |",
        "|---|---:|---|---:|---:|---:|",
    ]
    for record in records:
        failed = record["failed_gates"] or "none"
        lines.append(
            f"| `{record['sample_id']}` | {record['gates_passed']}/4 | "
            f"{failed} | {record['registered_ink_f1']:.4f} | "
            f"{record['text_ltsim_page_macro']:.4f} | "
            f"{record['token_center_displacement_q90']:.4f} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    with args.scores.resolve().open(newline="", encoding="utf-8") as handle:
        rows = [
            row for row in csv.DictReader(handle)
            if row.get("v2_status") == "scored"
        ]
    if not rows:
        raise SystemExit("score table contains no scored rows")
    records = [summarize_row(row) for row in rows]
    summary = aggregate(records)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    fields = list(records[0])
    with (args.output_dir / "gate_ladder.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    (args.output_dir / "gate_ladder.json").write_text(
        json.dumps(
            {"summary": summary, "records": records},
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "gate_ladder.md").write_text(
        render_markdown(summary, records),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
