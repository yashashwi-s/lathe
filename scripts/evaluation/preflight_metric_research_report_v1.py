#!/usr/bin/env python3
"""Fail-closed release gate for the v1 PDF metric research report.

This script does not build the report.  It verifies that the report can be
derived from completed, frozen artifacts without filling missing results or
manual-audit fields.  On success it can freeze an input manifest and the exact
157-row register consumed by the eventual PDF generator.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results" / "metric_research_v1"
FULL = BASE / "full_157_v1"
AI = BASE / "ai_outputs_frozen_v1"
CONTROL_AUDIT = FULL / "visual_audit"
AI_AUDIT = AI / "visual_audit"

EXPECTED_SOURCES = 157
EXPECTED_CONTROLLED_ROWS = 16_167
EXPECTED_APPLIED = 16_142
EXPECTED_NOT_APPLICABLE = 25
EXPECTED_CONTROL_AUDIT_CASES = 628
EXPECTED_AI_OUTPUTS = 156
EXPECTED_MISSING_AI_OUTPUTS = 1
EXPECTED_MODEL_ID = "google/gemini-3.1-flash-lite"
AXES = ("content", "layout", "typography", "appearance", "structure", "pagination")

CLAIM_BOUNDARIES = {
    "study_scope": (
        "This report evaluates one AI conversion corpus against 157 accepted LaTeX "
        "reference PDFs. It does not compare multiple AI models and does not estimate "
        "human preference."
    ),
    "primary_result": (
        "The primary result is an axis vector with evidence and abstention. There is no "
        "universal quality score."
    ),
    "controlled_boxes": (
        "On controlled examples, red is the known synthetic edit region and cyan is the "
        "registered raster-residual enclosure in its labeled coordinate frame."
    ),
    "ai_boxes": (
        "AI outputs have no source-known defect box. A cyan raster-residual enclosure may "
        "be shown as diagnostic evidence; it is not semantic ground truth."
    ),
    "ratings": (
        "No human ratings were collected. Model-assisted visual audit is a research check, "
        "not ground truth."
    ),
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _pdf_pages(path: Path) -> int:
    with fitz.open(path) as document:
        return document.page_count


def _completed_control_audit(responses: list[dict[str, str]], answers: list[dict[str, str]]) -> list[str]:
    errors = []
    if len(responses) != EXPECTED_CONTROL_AUDIT_CASES:
        errors.append(f"controlled blind responses: expected 628 rows, found {len(responses)}")
    if len(answers) != EXPECTED_CONTROL_AUDIT_CASES:
        errors.append(f"controlled answer key: expected 628 rows, found {len(answers)}")
    identity_incomplete = sum(
        not row.get("confidence", "").strip() or not row.get("reviewer", "").strip()
        for row in responses
    )
    explicit_abstention_missing = sum(
        row.get("abstain", "").strip().lower() not in {"true", "false"} for row in responses
    )
    judgment_incomplete = sum(
        row.get("abstain", "").strip().lower() == "false" and (
            row.get("changed_panel", "").strip() not in {"A", "B"}
            or not row.get("visible_defect_axis", "").strip()
            or not row.get("region_description", "").strip()
        ) for row in responses
    )
    if identity_incomplete:
        errors.append(f"controlled blind responses: {identity_incomplete} confidence/reviewer records incomplete")
    if explicit_abstention_missing:
        errors.append(f"controlled blind responses: {explicit_abstention_missing} rows lack explicit true/false abstention")
    if judgment_incomplete:
        errors.append(f"controlled blind responses: {judgment_incomplete} non-abstained judgments incomplete")
    audit_fields = (
        "candidate_panel_hidden_truth", "candidate_valid", "mutation_visible",
        "target_box_correct", "label_correct", "predicted_box_useful", "reviewer",
    )
    answer_incomplete = sum(
        any(not row.get(field, "").strip() for field in audit_fields) for row in answers
    )
    if answer_incomplete:
        errors.append(f"controlled answer key: {answer_incomplete} post-unblind audit records incomplete")
    return errors


def _completed_ai_audit(responses: list[dict[str, str]], answers: list[dict[str, str]]) -> list[str]:
    errors = []
    if len(responses) != EXPECTED_AI_OUTPUTS:
        errors.append(f"AI blind responses: expected 156 rows, found {len(responses)}")
    if len(answers) != EXPECTED_AI_OUTPUTS:
        errors.append(f"AI answer key: expected 156 rows, found {len(answers)}")
    response_fields = ("severity_summary", "confidence", "review_notes", "reviewer")
    response_incomplete = sum(
        any(not row.get(field, "").strip() for field in response_fields) for row in responses
    )
    if response_incomplete:
        errors.append(f"AI blind responses: {response_incomplete} required research notes incomplete")
    answer_fields = (
        "top_residual_box_useful_after_unblind", "axis_labels_plausible_after_unblind",
        "unblind_notes", "reviewer",
    )
    answer_incomplete = sum(
        any(not row.get(field, "").strip() for field in answer_fields) for row in answers
    )
    if answer_incomplete:
        errors.append(f"AI answer key: {answer_incomplete} post-unblind audit records incomplete")
    return errors


def _register_rows(profile: list[dict[str, str]], scores: list[dict[str, str]],
                   missing: list[dict[str, str]]) -> list[dict[str, str]]:
    scores_by_sample = {row["sample_id"]: row for row in scores}
    missing_by_sample = {row["sample_id"]: row for row in missing}
    rows = []
    for source in sorted(profile, key=lambda row: row["sample_id"]):
        sample_id = source["sample_id"]
        score = scores_by_sample.get(sample_id)
        state = "compiled" if score else "missing"
        if score is None and sample_id not in missing_by_sample:
            raise ValueError(f"register has neither score nor missing record for {sample_id}")
        row = {
            "sample_id": sample_id,
            "document_form": source["category"],
            "prompt_split": source["prompt_split"],
            "metric_partition": source["metric_partition"],
            "reference_pages": source["reference_pages"],
            "ai_output_state": state,
            "ai_output_label": "AI-produced Typst PDF" if score else "AI output unavailable",
            "ai_model_id": source.get("ai_model_id", "") if score else "",
            "selected_prompt_stage": source.get("ai_selected_stage", "") if score else "",
            "page_count_match": score.get("page_count_match", "") if score else "",
            "canvas_sequence_match": score.get("canvas_match", "") if score else "",
            "missing_reason": missing_by_sample.get(sample_id, {}).get("reason", ""),
        }
        for axis in AXES:
            row[f"raw_axis_{axis}"] = score.get(f"axis_{axis}", "") if score else ""
            row[f"ai_quality_band_{axis}"] = score.get(f"band_{axis}", "") if score else ""
        rows.append(row)
    return rows


def inspect() -> tuple[dict, list[Path], list[dict[str, str]]]:
    required = [
        ROOT / "scripts" / "evaluation" / "pdf_metric_axes_v1.py",
        ROOT / "scripts" / "evaluation" / "run_metric_augmentations_v1.py",
        ROOT / "scripts" / "evaluation" / "validate_metric_research_v1.py",
        ROOT / "scripts" / "evaluation" / "analyze_llm_visual_audits_v1.py",
        ROOT / "scripts" / "evaluation" / "build_metric_research_report_v1.py",
        ROOT / "reports" / "pdf_metric_literature_v1.md",
        ROOT / "reports" / "pdf_metric_research_protocol_v1.md",
        ROOT / "reports" / "pdf_metric_red_team_resolution_v1.md",
        ROOT / "reports" / "layout_projection_trial_v1.md",
        ROOT / "reports" / "llm_visual_audit_rubric_v1.md",
        BASE / "corpus_profile_157.csv",
        BASE / "reference_visual_audit_157.csv",
        FULL / "augmentation_results.csv",
        FULL / "merged_run_summary.json",
        FULL / "controlled_validation.json",
        FULL / "controlled_validation_layout_iou.json",
        FULL / "axis_severity_bands.json",
        FULL / "determinism_validation.json",
        FULL / "determinism_case_details.csv",
        BASE / "layout_center_pilot_11_v1" / "augmentation_results.csv",
        BASE / "layout_center_pilot_11_v1" / "validation_layout.json",
        BASE / "category_audit_repeat_v1" / "augmentation_results.csv",
        BASE / "ai_outputs_center_q90_trial_v1" / "ai_output_axis_scores.csv",
        BASE / "ai_outputs_center_q90_trial_v1" / "summary.json",
        BASE / "llm_visual_audit_analysis_v1.json",
        CONTROL_AUDIT / "audit_build_summary.json",
        CONTROL_AUDIT / "blind_response_manifest.csv",
        CONTROL_AUDIT / "audit_answer_key.csv",
        CONTROL_AUDIT / "full157_blind_audit_book.pdf",
        CONTROL_AUDIT / "full157_unblinded_evidence_book.pdf",
        AI / "ai_output_axis_scores.csv",
        AI / "missing_ai_outputs.csv",
        AI / "summary.json",
        AI_AUDIT / "audit_build_summary.json",
        AI_AUDIT / "blind_ai_response_manifest.csv",
        AI_AUDIT / "ai_audit_answer_key.csv",
        AI_AUDIT / "ai_outputs_blind_audit_book.pdf",
        AI_AUDIT / "ai_outputs_unblinded_evidence_book.pdf",
    ]
    errors = [f"missing required artifact: {path.relative_to(ROOT)}" for path in required if not path.exists()]
    report = {"ready": False, "claim_boundaries": CLAIM_BOUNDARIES, "checks": {}}
    if (CONTROL_AUDIT / "blind_response_manifest.csv").exists() and (
        CONTROL_AUDIT / "audit_answer_key.csv"
    ).exists():
        errors.extend(_completed_control_audit(
            _read_csv(CONTROL_AUDIT / "blind_response_manifest.csv"),
            _read_csv(CONTROL_AUDIT / "audit_answer_key.csv"),
        ))
    if (AI_AUDIT / "blind_ai_response_manifest.csv").exists() and (
        AI_AUDIT / "ai_audit_answer_key.csv"
    ).exists():
        errors.extend(_completed_ai_audit(
            _read_csv(AI_AUDIT / "blind_ai_response_manifest.csv"),
            _read_csv(AI_AUDIT / "ai_audit_answer_key.csv"),
        ))
    if any(error.startswith("missing required artifact:") for error in errors):
        report["errors"] = errors
        return report, required, []

    profile = _read_csv(BASE / "corpus_profile_157.csv")
    reference_audit = _read_csv(BASE / "reference_visual_audit_157.csv")
    controlled = _read_csv(FULL / "augmentation_results.csv")
    merged = _read_json(FULL / "merged_run_summary.json")
    validation = _read_json(FULL / "controlled_validation.json")
    bands = _read_json(FULL / "axis_severity_bands.json")
    determinism = _read_json(FULL / "determinism_validation.json")
    control_answers = _read_csv(CONTROL_AUDIT / "audit_answer_key.csv")
    scores = _read_csv(AI / "ai_output_axis_scores.csv")
    missing = _read_csv(AI / "missing_ai_outputs.csv")
    ai_summary = _read_json(AI / "summary.json")

    sample_ids = [row["sample_id"] for row in profile]
    if len(profile) != EXPECTED_SOURCES or len(set(sample_ids)) != EXPECTED_SOURCES:
        errors.append("corpus profile must contain 157 unique sample IDs")
    if len(reference_audit) != EXPECTED_SOURCES or any(
        row.get("manual_render_check") != "pass" or not row.get("manual_note", "").strip()
        for row in reference_audit
    ):
        errors.append("reference visual audit must contain 157 completed pass records with notes")
    statuses = Counter(row.get("status", "") for row in controlled)
    if len(controlled) != EXPECTED_CONTROLLED_ROWS or len({row["sample_id"] for row in controlled}) != EXPECTED_SOURCES:
        errors.append("merged controlled results must contain 16,167 rows across 157 sources")
    if statuses != Counter({"applied": EXPECTED_APPLIED, "not_applicable": EXPECTED_NOT_APPLICABLE}):
        errors.append(f"unexpected controlled status counts: {dict(statuses)}")
    if merged.get("cases") != EXPECTED_CONTROLLED_ROWS or merged.get("retained_audit_candidates") != 628:
        errors.append("merged summary does not match the frozen all-157 accounting")
    if validation.get("rows") != EXPECTED_CONTROLLED_ROWS or validation.get("source_documents") != EXPECTED_SOURCES:
        errors.append("validation was not executed on all 16,167 rows and 157 source clusters")
    validation_status = validation.get("gate_assessment", {}).get("status")
    if validation_status not in {"passes_synthetic_projection_gates", "fails_or_incomplete"}:
        errors.append("corrected controlled-response validation has no recognized frozen status")
    determinism_complete = (
        isinstance(determinism.get("pass"), bool)
        and determinism.get("shared_cases") == 471
        and determinism.get("retained_artifact_pairs") == 157
        and determinism.get("score_and_localization_agreement") is not None
        and determinism.get("pdf_byte_agreement") is not None
        and determinism.get("render_pixel_agreement") is not None
    )
    if not determinism_complete:
        errors.append("independent score/PDF/render determinism result is incomplete")
    if any(definition.get("deploy_to_ai_outputs") is not False for definition in bands.get("axes", {}).values()):
        errors.append("synthetic severity profiles must remain disabled for AI-output labels")

    model_counts = Counter(row.get("ai_model_id", "") for row in scores)
    if len(scores) != EXPECTED_AI_OUTPUTS or model_counts != Counter({EXPECTED_MODEL_ID: EXPECTED_AI_OUTPUTS}):
        errors.append(f"AI score table must contain exactly 156 rows for {EXPECTED_MODEL_ID}")
    if len(missing) != EXPECTED_MISSING_AI_OUTPUTS:
        errors.append("AI missing-output table must contain exactly one explicit row")
    if ai_summary.get("aggregate_score") is not None or ai_summary.get("evaluated_outputs") != EXPECTED_AI_OUTPUTS:
        errors.append("AI summary must contain 156 outputs and no aggregate score")
    if any(row.get(f"band_{axis}") != "abstain" for row in scores for axis in AXES):
        errors.append("every AI severity band must be abstain; only raw axes may be reported")

    pdf_expectations = {
        CONTROL_AUDIT / "full157_blind_audit_book.pdf": EXPECTED_SOURCES,
        CONTROL_AUDIT / "full157_unblinded_evidence_book.pdf": EXPECTED_SOURCES,
        AI_AUDIT / "ai_outputs_blind_audit_book.pdf": EXPECTED_AI_OUTPUTS,
        AI_AUDIT / "ai_outputs_unblinded_evidence_book.pdf": EXPECTED_AI_OUTPUTS,
    }
    pdf_pages = {str(path.relative_to(ROOT)): _pdf_pages(path) for path in pdf_expectations}
    for path, expected in pdf_expectations.items():
        if pdf_pages[str(path.relative_to(ROOT))] != expected:
            errors.append(f"{path.relative_to(ROOT)}: expected {expected} pages")

    literature = (ROOT / "reports" / "pdf_metric_literature_v1.md").read_text(encoding="utf-8")
    required_citations = (
        "aclanthology.org/J06-4002", "arxiv.org/abs/2203.12555", "arxiv.org/abs/1911.10683",
        "arxiv.org/abs/2409.03643", "ece.uwaterloo.ca/~z70wang/publications/ssim.pdf",
        "arxiv.org/abs/2406.07791",
    )
    if any(citation not in literature for citation in required_citations) or "not implemented" not in literature:
        errors.append("literature artifact lacks a required primary citation or implementation boundary")

    try:
        register = _register_rows(profile, scores, missing)
    except ValueError as exc:
        errors.append(str(exc))
        register = []
    if len(register) != EXPECTED_SOURCES:
        errors.append("final report register must contain exactly 157 rows")

    report["checks"] = {
        "sources": len(profile),
        "reference_visual_audits": len(reference_audit),
        "controlled_rows": len(controlled),
        "controlled_status_counts": dict(statuses),
        "controlled_validation_status": validation_status,
        "determinism_pass": determinism.get("pass"),
        "controlled_audit_cases": len(control_answers),
        "ai_outputs": len(scores),
        "missing_ai_outputs": len(missing),
        "models": dict(model_counts),
        "pdf_pages": pdf_pages,
        "register_rows": len(register),
    }
    report["ready"] = not errors
    report["errors"] = errors
    return report, required, register


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write preflight JSON, including failure reasons")
    parser.add_argument("--freeze-dir", type=Path, help="write frozen manifest/register only when ready")
    args = parser.parse_args()
    report, required, register = inspect()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if not report["ready"]:
        raise SystemExit(2)
    if args.freeze_dir:
        args.freeze_dir.mkdir(parents=True, exist_ok=True)
        frozen = {
            "method": "metric_research_report_inputs_v1",
            "claim_boundaries": CLAIM_BOUNDARIES,
            "checks": report["checks"],
            "inputs": {
                str(path.relative_to(ROOT)): {"sha256": _sha256(path), "bytes": path.stat().st_size}
                for path in required
            },
        }
        (args.freeze_dir / "frozen_report_inputs.json").write_text(
            json.dumps(frozen, indent=2, sort_keys=True) + "\n", encoding="utf-8",
        )
        _write_csv(args.freeze_dir / "final_report_register_157.csv", register)


if __name__ == "__main__":
    main()
