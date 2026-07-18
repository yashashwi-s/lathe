#!/usr/bin/env python3
"""Evaluate available AI PDF outputs with frozen, axis-specific methodology."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

from pdf_metric_axes_v1 import evaluate_pdf_pair
from run_metric_augmentations_v1 import _flatten_metric


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROFILE = ROOT / "results" / "metric_research_v1" / "corpus_profile_157.csv"
DEFAULT_BANDS = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "axis_severity_bands.json"
DEFAULT_OUTPUT = ROOT / "results" / "metric_research_v1" / "ai_outputs_frozen_v1"
AXES = ("content", "layout", "typography", "appearance", "structure", "pagination")


def _bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _band(score: float | None, definition: dict) -> str:
    if score is None or definition.get("deploy_to_ai_outputs") is not True:
        return "abstain"
    thresholds = definition["thresholds"]
    if score >= thresholds["reference_like_min"]:
        return "reference_like"
    if score >= thresholds["mild_min"]:
        return "mild"
    if score >= thresholds["moderate_min"]:
        return "moderate"
    return "severe"


def _applicability(row: dict[str, str]) -> dict:
    return {
        "tables": {"reference": _bool(row["has_semantic_table"]), "candidate": None},
        "formulas": {"reference": _bool(row["has_math_any"]), "candidate": None},
        "figures": {"reference": _bool(row["has_semantic_figure"]), "candidate": None},
    }


def _ai_provenance(candidate: Path) -> dict[str, object]:
    """Read the prompt and run identity beside an existing output PDF."""
    sample_dir = candidate.parent
    run_dir = sample_dir.parents[1]
    run_config_path = run_dir / "run_config.json"
    meta_path = sample_dir / "meta.json"
    run_config = json.loads(run_config_path.read_text(encoding="utf-8"))
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return {
        "ai_requested_model": meta.get("requested_model", run_config.get("model", "")),
        "ai_resolved_model": meta.get("resolved_model", ""),
        "ai_model_checkpoint": "not_recorded_api_route_only",
        "ai_prompt_path": run_config.get("prompt_path", ""),
        "ai_system_prompt_sha256": run_config.get("system_prompt_sha256", ""),
        "ai_retry_prompt_path": run_config.get("retry_prompt_path", ""),
        "ai_retry_prompt_sha256": run_config.get("retry_prompt_sha256", ""),
        "ai_temperature": run_config.get("temperature", ""),
        "ai_typst_version": run_config.get("typst_version", ""),
        "ai_attempts": meta.get("attempts", ""),
        "ai_final_attempt": next(
            (
                attempt.get("attempt", "")
                for attempt in reversed(meta.get("attempt_records", []))
                if attempt.get("compile_ok") is True
            ),
            "",
        ),
        "ai_repaired": meta.get("repaired", ""),
        "ai_response_id": meta.get("response_id", ""),
        "ai_run_config": str(run_config_path),
        "ai_sample_meta": str(meta_path),
    }


def _summary(
    rows: list[dict[str, str]], band_definitions: dict,
    layout_projection: str = "bbox_iou_q10",
) -> dict:
    by_axis = {}
    for axis in AXES:
        values = [
            float(row[f"axis_{axis}"])
            for row in rows
            if row[f"axis_{axis}"] not in (None, "")
        ]
        labels = Counter(row[f"band_{axis}"] for row in rows)
        by_axis[axis] = {
            "band_status": band_definitions.get(f"axis_{axis}", {}).get("status", "absent"),
            "scored_outputs": len(values),
            "raw_min": min(values) if values else None,
            "raw_median": median(values) if values else None,
            "raw_max": max(values) if values else None,
            "band_counts": dict(labels),
        }
    category_counts: dict[str, Counter] = defaultdict(Counter)
    for row in rows:
        for axis in AXES:
            category_counts[row["category"]][f"{axis}:{row[f'band_{axis}']}"] += 1
    return {
        "method": "frozen_axis_transfer_to_ai_outputs_v1",
        "layout_projection": layout_projection,
        "aggregate_score": None,
        "policy": (
            "AI outputs were not used to fit thresholds. Each raw axis remains visible; any synthetic "
            "profile means controlled-defect equivalence, not human quality or preference. Global AI severity "
            "labels are disabled. The selected outputs come from an adaptive v1-v3 repair cascade, "
            "not one frozen prompt or a cross-model leaderboard."
        ),
        "evaluated_outputs": len(rows),
        "models": dict(Counter(row["ai_model_id"] for row in rows)),
        "resolved_models": dict(Counter(row["ai_resolved_model"] for row in rows)),
        "model_identity_limitation": (
            "The recorded identity is an API model route and resolved route; no immutable provider "
            "checkpoint hash was returned or persisted."
        ),
        "system_prompt_sha256": sorted({row["ai_system_prompt_sha256"] for row in rows}),
        "selected_prompt_stages": dict(Counter(row["ai_selected_stage"] for row in rows)),
        "final_attempts": dict(Counter(row["ai_final_attempt"] for row in rows)),
        "analysis_roles": dict(Counter(row["analysis_role"] for row in rows)),
        "page_count_mismatches": sum(row["page_count_match"] == "false" for row in rows),
        "canvas_mismatches": sum(row["canvas_match"] == "false" for row in rows),
        "axes": by_axis,
        "category_band_counts": {key: dict(value) for key, value in sorted(category_counts.items())},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--bands", type=Path, default=DEFAULT_BANDS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--layout-projection",
        choices=("bbox_iou_q10", "center_displacement_q90"),
        default="bbox_iou_q10",
    )
    args = parser.parse_args()
    with args.profile.open(newline="", encoding="utf-8") as handle:
        profile = list(csv.DictReader(handle))
    band_document = json.loads(args.bands.read_text(encoding="utf-8"))
    band_definitions = band_document["axes"]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = args.out_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    output = []
    missing = []
    for index, row in enumerate(profile, 1):
        candidate = ROOT / Path(row["ai_candidate_pdf"]) if row["ai_candidate_pdf"] else None
        if not candidate or not candidate.exists():
            missing.append({
                "sample_id": row["sample_id"],
                "category": row["category"],
                "metric_partition": row["metric_partition"],
                "prompt_split": row["prompt_split"],
                "ai_model_id": row["ai_model_id"],
                "ai_selected_stage": row["ai_selected_stage"],
                "reason": "AI candidate PDF missing",
            })
            continue
        result = evaluate_pdf_pair(
            ROOT / row["reference_pdf"], candidate,
            applicability=_applicability(row),
        )
        ai_provenance = _ai_provenance(candidate)
        projections, predicted_page, predicted_bbox = _flatten_metric(
            result, layout_projection=args.layout_projection
        )
        residual = result["axes"]["raster_diagnostic"]["evidence"].get("top_difference_bbox") or {}
        evidence_path = evidence_dir / f"{row['sample_id']}.json"
        evidence_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        record = {
            "sample_id": row["sample_id"],
            "category": row["category"],
            "metric_partition": row["metric_partition"],
            "prompt_split": row["prompt_split"],
            "analysis_role": (
                "prompt_development_descriptive_only"
                if row["prompt_split"] == "prompt_dev"
                else "prompt_heldout_metric_test_adaptive_pipeline"
                if row["metric_partition"] == "metric_test"
                else "prompt_heldout_non_test_adaptive_pipeline"
            ),
            "ai_model_id": row["ai_model_id"],
            "ai_selected_stage": row["ai_selected_stage"],
            **ai_provenance,
            "reference_pdf": row["reference_pdf"],
            "candidate_pdf": row["ai_candidate_pdf"],
            "reference_pages": row["reference_pages"],
            "candidate_pages": row["ai_candidate_pages"],
            "page_count_match": row["ai_page_count_match_measured"].lower(),
            "canvas_match": row["ai_page_size_sequence_match"].lower(),
            "top_difference_page": "" if predicted_page is None else predicted_page,
            "top_difference_bbox": "" if predicted_bbox is None else json.dumps(predicted_bbox),
            "top_difference_side": residual.get("unpaired_side") or "paired_reference_frame",
            "top_difference_coordinate_frame": residual.get("coordinate_frame", ""),
            "registration_translation_px": json.dumps(residual.get("registration_translation_px")),
            "evidence_json": str(evidence_path),
        }
        for axis in AXES:
            value = projections.get(f"axis_{axis}")
            record[f"axis_{axis}"] = "" if value is None else value
            record[f"band_{axis}"] = _band(value, band_definitions.get(f"axis_{axis}", {}))
        output.append(record)
        if index % 20 == 0:
            print(f"progress {index}/{len(profile)}", flush=True)

    if not output:
        raise ValueError("no AI candidate PDFs resolved from the corpus profile")
    fields = list(output[0])
    with (args.out_dir / "ai_output_axis_scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)
    with (args.out_dir / "missing_ai_outputs.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "sample_id", "category", "metric_partition", "prompt_split",
            "ai_model_id", "ai_selected_stage", "reason",
        ])
        writer.writeheader()
        writer.writerows(missing)
    summary = _summary(output, band_definitions, args.layout_projection)
    summary["missing_outputs"] = len(missing)
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
