from __future__ import annotations

import sys
from pathlib import Path

import fitz
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluation import evaluate_metric_v2_manifest as manifest_v2  # noqa: E402
from scripts.evaluation import pdf_metric_axes_v2 as metric_v2  # noqa: E402
from scripts.evaluation.pdf_metric_axes_v2 import evaluate_pdf_pair  # noqa: E402


def _write_pdf(path: Path, rows: list[tuple[float, float, str, float]]) -> None:
    document = fitz.open()
    page = document.new_page(width=300, height=400)
    for x, y, text, size in rows:
        page.insert_text((x, y), text, fontsize=size, fontname="helv")
    document.save(path)
    document.close()


def test_identity_has_exact_critical_content_and_transport(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    rows = [(40, 80, "Mass = 12.5 [3]", 12), (40, 180, "Second block", 12)]
    _write_pdf(reference, rows)
    _write_pdf(candidate, rows)

    result = evaluate_pdf_pair(reference, candidate, render_dpi=72)

    assert result["evaluator"]["aggregate_score"] is None
    critical = result["axes"]["critical_content"]["metrics"]
    assert result["axes"]["content"]["metrics"]["strict_nfc_token_inventory"]["f1"] == 1.0
    assert critical["numbers"]["exact_match"] is True
    assert critical["numbers"]["f1"] == 1.0
    assert critical["operators"]["exact_match"] is True
    assert critical["citation_markers"]["exact_match"] is True
    transport = result["axes"]["block_transport"]["metrics"]
    assert transport["combined_transport_cost"] == pytest.approx(0.0, abs=1e-12)
    assert transport["combined_transport_similarity_exp"] == pytest.approx(1.0)
    assert result["axes"]["text_ltsim"]["metrics"]["text_ltsim_page_macro"] == pytest.approx(1.0)
    raster = result["axes"]["raster_perceptual"]["metrics"]
    assert raster["unregistered_ssim_macro"] == pytest.approx(1.0)
    assert raster["registered_multiscale_ssim_diagnostic_macro"] == pytest.approx(1.0)


def test_numeric_error_is_exposed_even_when_most_text_matches(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(reference, [(40, 80, "The measured mass equals 12.50 kg", 12)])
    _write_pdf(candidate, [(40, 80, "The measured mass equals 21.50 kg", 12)])

    result = evaluate_pdf_pair(reference, candidate, render_dpi=72)

    numbers = result["axes"]["critical_content"]["metrics"]["numbers"]
    assert numbers["exact_match"] is False
    assert numbers["f1"] == 0.0
    assert numbers["missing"] == ["12.50"]
    assert numbers["extra"] == ["21.50"]
    assert result["axes"]["content"]["metrics"]["strict_nfc_token_inventory"]["f1"] > 0.8


def test_layout_shift_changes_geometry_transport_not_content_transport(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(reference, [(40, 80, "Alpha block", 12), (40, 180, "Beta block", 12)])
    _write_pdf(candidate, [(90, 120, "Alpha block", 12), (90, 220, "Beta block", 12)])

    result = evaluate_pdf_pair(reference, candidate, render_dpi=72)
    transport = result["axes"]["block_transport"]["metrics"]

    assert transport["transported_geometry_cost"] > 0.0
    assert transport["transported_content_cost"] == pytest.approx(0.0)
    assert result["axes"]["geometry"]["metrics"]["center_displacement_q90"] > 0.1
    assert result["axes"]["raster_perceptual"]["metrics"]["registered_ssim_macro"] >= result["axes"]["raster_perceptual"]["metrics"]["unregistered_ssim_macro"]


def test_ssim_abstains_instead_of_resizing_canvas(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    left = fitz.open()
    page = left.new_page(width=300, height=400)
    page.insert_text((40, 80), "same", fontsize=12)
    left.save(reference)
    left.close()
    right = fitz.open()
    page = right.new_page(width=600, height=800)
    page.insert_text((80, 160), "same", fontsize=24)
    right.save(candidate)
    right.close()

    result = evaluate_pdf_pair(reference, candidate, render_dpi=72)

    raster = result["axes"]["raster_perceptual"]
    assert raster["status"] == "abstain"
    assert raster["metrics"]["unregistered_ssim_macro"] is None
    assert raster["evidence"]["pages"][0]["status"] == "abstain_canvas_mismatch"


def test_evidence_serializes_repo_inputs_as_posix_relative_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "checkout"
    reference = root / "data" / "reference.pdf"
    candidate = root / "results" / "candidate.pdf"
    reference.parent.mkdir(parents=True)
    candidate.parent.mkdir(parents=True)
    _write_pdf(reference, [(40, 80, "Reference", 12)])
    _write_pdf(candidate, [(40, 80, "Candidate", 12)])
    monkeypatch.setattr(metric_v2, "ROOT", root)

    result = metric_v2.evaluate_pdf_pair(reference, candidate, render_dpi=72)

    assert result["inputs"]["reference_pdf"] == "data/reference.pdf"
    assert result["inputs"]["candidate_pdf"] == "results/candidate.pdf"


def test_manifest_resolves_absolute_inputs_but_serializes_portable_paths(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reference = ROOT / "data" / "reference.pdf"
    candidate = ROOT / "results" / "candidate.pdf"
    captured: dict[str, Path] = {}

    def fake_evaluate(
        reference_pdf: Path, candidate_pdf: Path, *, render_dpi: int
    ) -> dict[str, object]:
        captured["reference"] = reference_pdf
        captured["candidate"] = candidate_pdf
        assert render_dpi == 72
        return {}

    monkeypatch.setattr(manifest_v2, "evaluate_pdf_pair", fake_evaluate)
    _, output, result = manifest_v2._evaluate(
        (
            0,
            {
                "reference_pdf": reference.as_posix(),
                "candidate_pdf": candidate.as_posix(),
            },
            ROOT.as_posix(),
            72,
        )
    )

    assert result == {}
    assert captured == {"reference": reference, "candidate": candidate}
    assert output["reference_pdf"] == "data/reference.pdf"
    assert output["candidate_pdf"] == "results/candidate.pdf"
    assert output["reference_pdf_resolved"] == "data/reference.pdf"
    assert output["candidate_pdf_resolved"] == "results/candidate.pdf"
