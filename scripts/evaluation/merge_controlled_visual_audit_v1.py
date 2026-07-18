#!/usr/bin/env python3
"""Merge frozen controlled blind and post-unblind audit parts into canonical manifests."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "visual_audit"


def _read(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _write(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _parts(paths: list[Path]) -> dict[str, dict[str, str]]:
    merged = {}
    for path in paths:
        _fields, rows = _read(path)
        for row in rows:
            case_id = row["case_id"]
            if case_id in merged:
                raise ValueError(f"duplicate case_id in manual parts: {case_id}")
            merged[case_id] = row
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-dir", type=Path, default=AUDIT)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    blind_parts = sorted(args.audit_dir.glob("manual_blind_part_*.csv"))
    unblind_parts = sorted(args.audit_dir.glob("manual_unblind_part_*.csv"))
    blind = _parts(blind_parts)
    unblind = _parts(unblind_parts)
    if len(blind) != 628:
        raise ValueError(f"expected 628 frozen blind judgments, found {len(blind)}")
    if len(unblind) != 628:
        raise ValueError(f"expected 628 post-unblind judgments, found {len(unblind)}")

    response_path = args.audit_dir / "blind_response_manifest.csv"
    response_fields, responses = _read(response_path)
    answer_path = args.audit_dir / "audit_answer_key.csv"
    answer_fields, answers = _read(answer_path)
    response_ids = {row["case_id"] for row in responses}
    answer_ids = {row["case_id"] for row in answers}
    if response_ids != set(blind) or answer_ids != set(unblind):
        raise ValueError("manual part case IDs do not exactly match canonical manifests")

    for row in responses:
        judgment = blind[row["case_id"]]
        row.update({
            "changed_panel": judgment.get("changed_panel", ""),
            "visible_defect_axis": judgment.get("visible_defect_axis", ""),
            "region_description": judgment.get("region_description", ""),
            "confidence": judgment.get("confidence", ""),
            "abstain": judgment.get("abstain", ""),
            "review_notes": judgment.get("notes", judgment.get("review_notes", "")),
            "reviewer": judgment.get("reviewer", "LLM_research_audit"),
        })
    for row in answers:
        judgment = unblind[row["case_id"]]
        row.update({
            "candidate_valid": judgment.get("candidate_valid", ""),
            "mutation_visible": judgment.get("mutation_visible", ""),
            "target_box_correct": judgment.get("target_box_correct", ""),
            "label_correct": judgment.get("label_correct", ""),
            "predicted_box_useful": judgment.get("predicted_box_useful", ""),
            "reviewer": judgment.get("reviewer", "LLM_research_audit"),
            "review_notes": judgment.get("review_notes", judgment.get("notes", "")),
        })
    invalid_abstain = sum(row["abstain"].lower() not in {"true", "false"} for row in responses)
    missing_post = sum(
        any(not row[field] for field in (
            "candidate_valid", "mutation_visible", "target_box_correct", "label_correct",
            "predicted_box_useful",
        )) for row in answers
    )
    if invalid_abstain or missing_post:
        raise ValueError(
            f"incomplete audit after merge: invalid_abstain={invalid_abstain}, missing_post={missing_post}"
        )
    print(
        f"ready: {len(responses)} blind and {len(answers)} post-unblind records "
        f"from {len(blind_parts)}+{len(unblind_parts)} parts"
    )
    if args.apply:
        _write(response_path, response_fields, responses)
        _write(answer_path, answer_fields, answers)


if __name__ == "__main__":
    main()
