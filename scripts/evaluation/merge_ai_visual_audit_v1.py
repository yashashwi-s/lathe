#!/usr/bin/env python3
"""Merge frozen three-part AI visual audits into canonical manifests."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DIR = ROOT / "results" / "metric_research_v1" / "ai_outputs_frozen_v1" / "visual_audit"
ISSUE_FIELDS = ("content_issue", "layout_issue", "typography_issue", "pagination_issue", "specialized_issue")
ISSUE_VALUES = {"none", "minor", "moderate", "major", "unclear"}
UNBLIND_FIELDS = ("top_residual_box_useful_after_unblind", "axis_labels_plausible_after_unblind", "canvas_confound")


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _parts(paths: list[Path]) -> dict[str, dict[str, str]]:
    merged = {}
    for path in paths:
        _, rows = _read(path)
        for row in rows:
            case_id = row["audit_case_id"]
            if case_id in merged:
                raise ValueError(f"duplicate audit_case_id: {case_id}")
            merged[case_id] = row
    return merged


def _write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    blind = _parts(sorted(args.audit_dir.glob("manual_ai_blind_part_*.csv")))
    unblind = _parts(sorted(args.audit_dir.glob("manual_ai_unblind_part_*.csv")))
    if len(blind) != 156 or len(unblind) != 156:
        raise ValueError(f"expected 156 blind/unblind rows, found {len(blind)}/{len(unblind)}")

    response_path = args.audit_dir / "blind_ai_response_manifest.csv"
    response_fields, responses = _read(response_path)
    answer_path = args.audit_dir / "ai_audit_answer_key.csv"
    answer_fields, answers = _read(answer_path)
    ids = {row["audit_case_id"] for row in responses}
    if ids != set(blind) or ids != set(unblind) or ids != {row["audit_case_id"] for row in answers}:
        raise ValueError("manual IDs do not exactly match canonical manifests")

    for row in responses:
        judgment = blind[row["audit_case_id"]]
        for field in (*ISSUE_FIELDS, "severity_summary", "confidence", "review_notes", "reviewer"):
            row[field] = judgment.get(field, "")
        if any(row[field] not in ISSUE_VALUES for field in ISSUE_FIELDS):
            raise ValueError(f"invalid issue label in {row['audit_case_id']}")
        if not row["severity_summary"] or not row["review_notes"]:
            raise ValueError(f"incomplete blind rationale in {row['audit_case_id']}")
        confidence = float(row["confidence"])
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"invalid confidence in {row['audit_case_id']}")
    for row in answers:
        judgment = unblind[row["audit_case_id"]]
        for field in (*UNBLIND_FIELDS, "reviewer", "unblind_notes"):
            row[field] = judgment.get(field, "")
        if any(row[field].lower() not in {"true", "false"} for field in UNBLIND_FIELDS):
            raise ValueError(f"invalid post-unblind boolean in {row['audit_case_id']}")
        if not row["unblind_notes"]:
            raise ValueError(f"missing post-unblind rationale in {row['audit_case_id']}")
    print(f"ready: {len(responses)} blind + {len(answers)} post-unblind AI judgments")
    if args.apply:
        _write(response_path, response_fields, responses)
        _write(answer_path, answer_fields, answers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
