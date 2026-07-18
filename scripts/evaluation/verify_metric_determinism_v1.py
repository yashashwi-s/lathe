#!/usr/bin/env python3
"""Compare an independent rerun against frozen augmentation results."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REFERENCE = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "augmentation_results.csv"
DEFAULT_REPEAT = ROOT / "results" / "metric_research_v1" / "determinism_repeat_text_deletion" / "augmentation_results.csv"
DEFAULT_OUTPUT = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "determinism_validation.json"
COMPARE_FIELDS = (
    "status", "applicable", "expected_page", "expected_bbox", "target_page", "target_bbox",
    "predicted_page", "predicted_bbox", "axis_content", "axis_layout", "axis_typography",
    "axis_appearance", "axis_structure", "axis_pagination",
)


def _read(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["variant_id"]: row for row in rows}


def _equal(left: str, right: str, tolerance: float) -> bool:
    if left == right:
        return True
    try:
        a, b = float(left), float(right)
    except (TypeError, ValueError):
        return False
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= tolerance


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _render_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with fitz.open(path) as document:
        for page in document:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            digest.update(pixmap.samples)
    return digest.hexdigest()


def compare(reference: dict[str, dict[str, str]], repeat: dict[str, dict[str, str]],
            tolerance: float) -> tuple[list[dict[str, str]], dict]:
    shared = sorted(set(reference) & set(repeat))
    details = []
    score_agreements = 0
    byte_agreements = 0
    render_agreements = 0
    artifact_pairs = 0
    for variant_id in shared:
        first, second = reference[variant_id], repeat[variant_id]
        mismatched = [field for field in COMPARE_FIELDS if not _equal(first.get(field, ""), second.get(field, ""), tolerance)]
        score_equal = not mismatched
        score_agreements += score_equal
        byte_equal = render_equal = ""
        if first.get("candidate_pdf") and second.get("candidate_pdf"):
            artifact_pairs += 1
            first_path, second_path = Path(first["candidate_pdf"]), Path(second["candidate_pdf"])
            byte_equal = str(_sha256(first_path) == _sha256(second_path)).lower()
            render_equal = str(_render_sha256(first_path) == _render_sha256(second_path)).lower()
            byte_agreements += byte_equal == "true"
            render_agreements += render_equal == "true"
        details.append({
            "variant_id": variant_id,
            "sample_id": first["sample_id"],
            "variant": first["variant"],
            "severity": first["severity"],
            "score_and_localization_equal": str(score_equal).lower(),
            "mismatched_fields": ";".join(mismatched),
            "pdf_bytes_equal": byte_equal,
            "render_pixels_equal": render_equal,
        })
    summary = {
        "method": "independent_same_seed_rerun",
        "shared_cases": len(shared),
        "reference_only_cases": len(set(reference) - set(repeat)),
        "repeat_only_cases": len(set(repeat) - set(reference)),
        "score_and_localization_agreement": score_agreements / len(shared) if shared else None,
        "retained_artifact_pairs": artifact_pairs,
        "pdf_byte_agreement": byte_agreements / artifact_pairs if artifact_pairs else None,
        "render_pixel_agreement": render_agreements / artifact_pairs if artifact_pairs else None,
        "tolerance": tolerance,
        "pass": (
            bool(shared) and score_agreements == len(shared)
            and byte_agreements == artifact_pairs and render_agreements == artifact_pairs
        ),
    }
    return details, summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--repeat", type=Path, default=DEFAULT_REPEAT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--expected-shared", type=int, default=471)
    parser.add_argument("--tolerance", type=float, default=1e-12)
    args = parser.parse_args()
    details, summary = compare(_read(args.reference), _read(args.repeat), args.tolerance)
    if summary["shared_cases"] != args.expected_shared:
        raise ValueError(f"expected {args.expected_shared} shared cases, found {summary['shared_cases']}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    details_path = args.output.with_name("determinism_case_details.csv")
    with details_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(details[0]))
        writer.writeheader()
        writer.writerows(details)
    print(json.dumps(summary, indent=2))
    if not summary["pass"]:
        raise SystemExit("determinism gate failed")


if __name__ == "__main__":
    main()
