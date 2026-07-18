from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluation.analyze_publication_results import (
    AXES,
    METRIC_FIELDS,
    analyze,
)
from scripts.evaluation.preflight_publication_v0 import (
    EXPECTED_PRIMARY_PROTOCOLS,
    EXPECTED_SYSTEMS,
    SCORECARD_FIELDS,
    sha256,
    validate_metric_rows,
    validate_primary_rows,
    validate_recorded_hashes,
    validate_split_contract,
    validate_statistics_artifacts,
)


def _scorecard_rows() -> list[dict[str, str]]:
    rows = []
    for system in EXPECTED_SYSTEMS:
        row = {field: "value" for field in SCORECARD_FIELDS}
        row.update(
            system_id=system,
            display_label=system,
            protocol_id=EXPECTED_PRIMARY_PROTOCOLS[system],
            protocol_label="frozen first pass" if system == "gemini_first_pass" else "fixed protocol",
            candidate_stage="first_pass" if system == "gemini_first_pass" else "after_one_repair",
            universe_n="127",
            compiled_n="100",
            compile_rate=str(100 / 127),
            page_exact_n="80",
            page_exact_rate_all=str(80 / 127),
            canvas_exact_n="60",
            canvas_exact_rate_compiled="0.6",
            strict_word_f1_median="0.8",
            compatibility_word_f1_median="0.82",
            reference_coverage_median="0.81",
            center_displacement_q90_median="0.2",
            text_ltsim_median="0.75",
            ssim_eligible_n="0",
            ssim_median="",
            fidelity_population="compiled PDFs",
        )
        if system in {"pandoc", "tylax", "typetex"}:
            row["candidate_stage"] = "deterministic_engine"
        rows.append(row)
    return rows


def _metric_fixture(tmp_path: Path) -> tuple[dict[str, str], Path, Path]:
    candidate = tmp_path / "candidate.pdf"
    candidate.write_bytes(b"candidate")
    evidence = tmp_path / "evidence.json"
    evidence_value = {
        "inputs": {"candidate_pdf": "candidate.pdf"},
        "axes": {
            "content": {"status": "scored"},
            "geometry": {"status": "scored"},
            "text_ltsim": {"status": "scored"},
            "pagination": {"status": "scored"},
            "canvas": {"status": "scored"},
            "raster_perceptual": {
                "status": "abstain",
                "evidence": {"pages": [{"reason": "physical canvases differ"}]},
            },
        },
    }
    evidence.write_text(json.dumps(evidence_value), encoding="utf-8")
    row = {
        "system_id": "pandoc",
        "sample_id": "sample_1",
        "candidate_pdf": "candidate.pdf",
        "candidate_pdf_resolved": "candidate.pdf",
        "v2_status": "scored",
        "v2_error": "",
        "v2_evidence_json": "evidence.json",
        "strict_word_f1": "0.8",
        "compatibility_word_f1": "0.82",
        "matched_word_reference_coverage": "0.75",
        "token_center_displacement_q90": "0.2",
        "text_ltsim_page_macro": "0.7",
        "page_count_delta": "0",
        "canvas_exact_size_rate": "0",
        "unregistered_ssim": "",
        "registered_ssim": "",
        "unregistered_multiscale_ssim_diagnostic": "",
        "registered_multiscale_ssim_diagnostic": "",
    }
    return row, candidate, evidence


def _statistics_fixture(tmp_path: Path) -> tuple[Path, list[dict[str, str]]]:
    fields = (
        "sample_id",
        "category",
        "system_id",
        "display_label",
        "compiled",
        *METRIC_FIELDS,
    )
    labels = {
        "gemini_first_pass": "Gemini first pass",
        "gemini_after_one_repair": "Gemini after one repair",
        "pandoc": "Pandoc",
        "tylax": "Tylax",
        "typetex": "TypeTeX",
    }
    rows: list[dict[str, str]] = []
    for system_id in EXPECTED_SYSTEMS:
        row = {field: "" for field in fields}
        row.update(
            sample_id="sample_1",
            category="prose",
            system_id=system_id,
            display_label=labels[system_id],
            compiled="True",
        )
        for axis, _ in AXES:
            if axis == "token_center_displacement_q90":
                row[axis] = "0.1" if system_id == "gemini_after_one_repair" else "0.2"
            else:
                row[axis] = "0.8" if system_id == "gemini_after_one_repair" else "0.7"
        rows.append(row)
    path = tmp_path / "per_sample_scores.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path, rows


def test_split_contract_rejects_duplicate_id() -> None:
    accepted = [{"sample_id": "a", "status": "accepted"}, {"sample_id": "b", "status": "accepted"}]
    dev = [{"sample_id": "a"}, {"sample_id": "a"}]
    heldout = [{"sample_id": "b"}]
    errors = validate_split_contract(
        accepted,
        dev,
        heldout,
        expected_accepted=2,
        expected_prompt_dev=2,
        expected_heldout=1,
    )
    assert any("duplicate sample_id" in error for error in errors)


def test_split_and_primary_table_reject_leakage_and_wrong_stage() -> None:
    accepted = [{"sample_id": "a", "status": "accepted"}, {"sample_id": "b", "status": "accepted"}]
    errors = validate_split_contract(
        accepted,
        [{"sample_id": "a"}],
        [{"sample_id": "a"}],
        expected_accepted=2,
        expected_prompt_dev=1,
        expected_heldout=1,
    )
    assert any("split leakage" in error for error in errors)

    rows = _scorecard_rows()
    rows[0]["candidate_stage"] = "adaptive_v3_prompt_dev"
    rows[0]["protocol_id"] = "adaptive_cascade"
    errors = validate_primary_rows(rows)
    assert any("development/adaptive/Claude" in error for error in errors)
    assert any("wrong protocol_id" in error for error in errors)


def test_metric_gate_rejects_missing_evidence_and_candidate(tmp_path: Path) -> None:
    row, candidate, _ = _metric_fixture(tmp_path)
    candidate.unlink()
    row["v2_evidence_json"] = "missing.json"
    errors = validate_metric_rows(
        [row],
        expected_candidates={("pandoc", "sample_1"): candidate},
        root=tmp_path,
        flatten_evidence=lambda evidence: {},
    )
    assert any("candidate artifact is missing" in error for error in errors)
    assert any("metric evidence artifact is missing" in error for error in errors)


def test_metric_gate_rejects_nonfinite_value(tmp_path: Path) -> None:
    row, candidate, _ = _metric_fixture(tmp_path)
    row["strict_word_f1"] = "nan"
    errors = validate_metric_rows(
        [row],
        expected_candidates={("pandoc", "sample_1"): candidate},
        root=tmp_path,
        flatten_evidence=lambda evidence: {"strict_word_f1": 0.8},
    )
    assert any("nonfinite metric strict_word_f1" in error for error in errors)


def test_metric_gate_rejects_stale_evidence_value(tmp_path: Path) -> None:
    row, candidate, _ = _metric_fixture(tmp_path)
    row["strict_word_f1"] = "0.7"
    errors = validate_metric_rows(
        [row],
        expected_candidates={("pandoc", "sample_1"): candidate},
        root=tmp_path,
        flatten_evidence=lambda evidence: {"strict_word_f1": 0.8},
    )
    assert any("stale metric value for strict_word_f1" in error for error in errors)


def test_hash_gate_rejects_stale_sha256(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("frozen", encoding="utf-8")
    document = {"artifacts": {"input": {"path": "artifact.txt", "sha256": sha256(artifact)}}}
    errors, recorded = validate_recorded_hashes(document, root=tmp_path)
    assert errors == []
    assert artifact.resolve() in recorded

    artifact.write_text("changed", encoding="utf-8")
    errors, _ = validate_recorded_hashes(document, root=tmp_path)
    assert any("stale SHA-256" in error for error in errors)


def test_statistics_gate_recomputes_frozen_artifacts(tmp_path: Path) -> None:
    per_sample_path, per_sample_rows = _statistics_fixture(tmp_path)
    analyze(per_sample_path, tmp_path, expected_universe_n=1)
    document = json.loads((tmp_path / "publication_statistics.json").read_text())
    with (tmp_path / "paired_axis_results.csv").open(newline="", encoding="utf-8") as handle:
        paired_rows = list(csv.DictReader(handle))
    with (tmp_path / "category_results.csv").open(newline="", encoding="utf-8") as handle:
        category_rows = list(csv.DictReader(handle))

    errors = validate_statistics_artifacts(
        document,
        paired_rows,
        category_rows,
        per_sample_rows=per_sample_rows,
        root=tmp_path,
        per_sample_path=per_sample_path,
        paired_path=tmp_path / "paired_axis_results.csv",
        category_path=tmp_path / "category_results.csv",
        expected_universe_n=1,
    )
    assert errors == []

    paired_rows[0]["ci_low"] = "999"
    errors = validate_statistics_artifacts(
        document,
        paired_rows,
        category_rows,
        per_sample_rows=per_sample_rows,
        root=tmp_path,
        per_sample_path=per_sample_path,
        paired_path=tmp_path / "paired_axis_results.csv",
        category_path=tmp_path / "category_results.csv",
        expected_universe_n=1,
    )
    assert any("ci_low" in error for error in errors)
