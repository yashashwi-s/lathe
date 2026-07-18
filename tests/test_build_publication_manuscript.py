from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from build_publication_manuscript import SYSTEM_IDS, build  # noqa: E402


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fields = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _fixture(tmp_path: Path) -> Path:
    input_dir = tmp_path / "publication_v0"
    input_dir.mkdir()
    labels = {
        "gemini_first_pass": "Gemini — first pass",
        "gemini_after_one_repair": "Gemini — after repair",
        "pandoc": "Pandoc",
        "tylax": "Tylax",
        "typetex": "TypeTeX",
    }
    per_sample: list[dict[str, object]] = []
    scorecard: list[dict[str, object]] = []
    for system in SYSTEM_IDS:
        protocol = f"frozen_{system}"
        for sample_id, compiled in (("sample_a", True), ("sample_b", False)):
            per_sample.append({
                "sample_id": sample_id,
                "category": "prose",
                "system_id": system,
                "display_label": labels[system],
                "protocol_id": protocol,
                "protocol_label": "fixture protocol",
                "candidate_stage": "as tested",
                "compiled": compiled,
                "compile_status": "compiled" if compiled else "failed",
                "compile_failure_class": "" if compiled else "compile_error",
                "attempts_used": "1",
                "repair_attempted": "false",
                "reference_pdf": f"references/{sample_id}.pdf",
                "reference_sha256": "a" * 64,
                "candidate_pdf": f"candidates/{system}_{sample_id}.pdf" if compiled else "",
                "candidate_sha256": "b" * 64 if compiled else "",
                "metric_source_csv": "metrics.csv" if compiled else "",
                "metric_source_evidence_json": "evidence.json" if compiled else "",
                "metric_v2_status": "scored" if compiled else "not_scored_uncompiled",
                "strict_word_f1": "0.8" if compiled else "",
                "compatibility_word_f1": "0.9" if compiled else "",
                "number_f1": "1" if compiled else "",
                "operator_f1": "1" if compiled else "",
                "citation_f1": "" if compiled else "",
                "matched_word_reference_coverage": "0.75" if compiled else "",
                "token_center_displacement_q90": "0.1" if compiled else "",
                "block_transport_combined_similarity": "0.7" if compiled else "",
                "text_ltsim_page_macro": "0.7" if compiled else "",
                "reading_order_tau": "1" if compiled else "",
                "style_coverage_hmean": "0.8" if compiled else "",
                "unregistered_ink_f1": "0.8" if compiled else "",
                "unregistered_ssim": "",
                "page_count_delta": "0" if compiled else "",
                "page_break_f1": "1" if compiled else "",
                "canvas_exact_size_rate": "1" if compiled else "",
            })
        scorecard.append({
            "system_id": system,
            "display_label": labels[system],
            "protocol_id": protocol,
            "protocol_label": "fixture protocol",
            "candidate_stage": "as tested",
            "universe_n": 2,
            "compiled_n": 1,
            "compile_rate": 0.5,
            "page_exact_n": 1,
            "page_exact_rate_all": 0.5,
            "canvas_exact_n": 1,
            "canvas_exact_rate_compiled": 1.0,
            "strict_word_f1_median": 0.8,
            "compatibility_word_f1_median": 0.9,
            "reference_coverage_median": 0.75,
            "center_displacement_q90_median": 0.1,
            "text_ltsim_median": 0.7,
            "ssim_eligible_n": 0,
            "ssim_median": None,
            "fidelity_population": "compiled PDFs only",
            "candidate_set_sha256": "c" * 64,
        })

    per_sample_path = input_dir / "per_sample_scores.csv"
    scorecard_path = input_dir / "scorecard.csv"
    _write_csv(per_sample_path, per_sample)
    _write_csv(scorecard_path, scorecard)
    document = {
        "schema_version": "publication_scorecard_v0.1",
        "benchmark": {
            "name": "Fixture benchmark",
            "universe_n": 2,
            "split": "splits/heldout.csv",
            "compile_denominator": "all fixture references",
            "fidelity_population": "compiled fixture PDFs",
            "overall_scalar_score": None,
        },
        "provenance": {
            "inputs": {
                "heldout_split": {"path": "splits/heldout.csv", "sha256_raw_bytes": "d" * 64},
                "system_prompt": {"path": "prompts/system.txt", "sha256_raw_bytes": "e" * 64},
                "metric_v2_implementation": {"path": "scripts/pdf_metric_axes_v2.py"},
            },
            "gemini": {
                "requested_model_routes": ["fixture/model"],
                "resolved_model_routes": ["fixture/model"],
                "model_identity_limit": "route only",
                "temperature": 0,
                "max_repairs": 1,
                "source_only": True,
                "reference_images_supplied": False,
                "typst_version": "fixture",
            },
            "metric": {"evaluator": "pdf_metric_axes_v2", "render_dpi": 96, "aggregate_score": None},
        },
        "validation": {
            "prompt_dev_overlap_n": 0,
            "adaptive_v0_v2_v3_rows_used": 0,
            "claude_rows_used": 0,
            "first_pass_compiled_n": 1,
            "repair_attempted_n": 1,
            "repair_success_n": 0,
            "after_one_repair_compiled_n": 1,
            "actual_compiled_n": {system: 1 for system in SYSTEM_IDS},
            "metric_rows_cover_every_compiled_pdf": True,
            "failed_outputs_have_empty_fidelity_axes": True,
        },
        "artifacts": {
            "per_sample_scores": {
                "path": "results/publication_v0/per_sample_scores.csv",
                "sha256_raw_bytes": _sha256(per_sample_path),
            },
            "scorecard_csv": {
                "path": "results/publication_v0/scorecard.csv",
                "sha256_raw_bytes": _sha256(scorecard_path),
            },
        },
        "scorecard": scorecard,
    }
    (input_dir / "scorecard.json").write_text(json.dumps(document), encoding="utf-8")
    return input_dir


def test_build_is_deterministic_and_data_driven(tmp_path: Path) -> None:
    input_dir = _fixture(tmp_path)
    output = tmp_path / "report.md"

    first = build(input_dir, output)
    second = build(input_dir, output)

    assert first == second == output.read_text(encoding="utf-8")
    assert "Gemini — first pass | 1/2 (50.0%)" in first
    assert "compile_error: 1" in first
    assert "universal grade" in first
    assert "No paired interval is emitted" in first
    assert "scripts/evaluation/analyze_publication_results.py" in first


def test_missing_input_fails_without_replacing_output(tmp_path: Path) -> None:
    input_dir = _fixture(tmp_path)
    (input_dir / "per_sample_scores.csv").unlink()
    output = tmp_path / "report.md"
    output.write_text("keep me\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required publication files"):
        build(input_dir, output)

    assert output.read_text(encoding="utf-8") == "keep me\n"


def test_partial_statistics_fail_closed(tmp_path: Path) -> None:
    input_dir = _fixture(tmp_path)
    (input_dir / "publication_statistics.json").write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="publication statistics are partial"):
        build(input_dir, tmp_path / "report.md")
