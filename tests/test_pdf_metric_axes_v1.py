from __future__ import annotations

import json
import sys
from pathlib import Path

import fitz
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.evaluation.pdf_metric_axes_v1 import (  # noqa: E402
    clear_extraction_cache,
    evaluate_pdf_pair,
    extract_pdf,
    main,
)


TextSpec = tuple[float, float, str, float]


def _write_pdf(
    path: Path,
    pages: list[list[TextSpec]],
    *,
    page_sizes: list[tuple[float, float]] | None = None,
) -> None:
    document = fitz.open()
    for page_index, text_specs in enumerate(pages):
        width, height = page_sizes[page_index] if page_sizes else (300.0, 400.0)
        page = document.new_page(width=width, height=height)
        for x, y, text, size in text_specs:
            page.insert_text((x, y), text, fontsize=size, fontname="helv")
    document.save(path)
    document.close()


def _two_block_pdf(path: Path) -> None:
    _write_pdf(
        path,
        [[(40, 70, "Alpha token", 12), (40, 170, "Beta token", 12)]],
    )


def test_identity_reports_axes_without_an_aggregate(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _two_block_pdf(reference)
    _two_block_pdf(candidate)

    result = evaluate_pdf_pair(
        reference,
        candidate,
        applicability={"tables": False, "formulas": False, "figures": False},
        render_dpi=96,
    )

    assert result["evaluator"]["aggregate_score"] is None
    assert "score" not in result
    assert result["axes"]["content"]["metrics"]["token_inventory"]["f1"] == 1.0
    assert result["axes"]["text_grounding"]["metrics"]["word_hmean"] == 1.0
    assert result["axes"]["layout_relations"]["metrics"]["pairwise_relation_agreement"] == 1.0
    assert result["axes"]["content"]["metrics"]["document_normalized_edit_similarity"] == 1.0
    assert result["axes"]["geometry"]["metrics"]["center_displacement_q90"] == pytest.approx(0.0)
    assert result["axes"]["reading_order"]["metrics"]["kendall_tau"] == 1.0
    assert result["axes"]["pagination"]["metrics"]["page_break_f1"] == 1.0
    assert result["axes"]["typography"]["metrics"]["font_size_abs_log_ratio_q90"] == pytest.approx(0.0)
    assert result["axes"]["typography"]["metrics"]["style_coverage_hmean"] == pytest.approx(1.0)
    assert result["axes"]["raster_diagnostic"]["metrics"]["registered_tolerant_ink_f1_macro"] == 1.0
    assert result["axes"]["tables"]["status"] == "not_applicable"


def test_canvas_mismatch_is_separate_from_normalized_geometry(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(
        reference,
        [[(30, 80, "Scale invariant", 12)]],
        page_sizes=[(300, 400)],
    )
    _write_pdf(
        candidate,
        [[(60, 160, "Scale invariant", 24)]],
        page_sizes=[(600, 800)],
    )

    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)

    canvas = result["axes"]["canvas"]["metrics"]
    geometry = result["axes"]["geometry"]["metrics"]
    assert canvas["exact_paired_size_rate"] == 0.0
    assert canvas["width_abs_log_ratio_max"] == pytest.approx(0.693147, rel=1e-5)
    assert geometry["center_displacement_q90"] < 0.005


def test_layout_shift_remains_visible_while_registration_is_diagnostic(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(
        reference,
        [[(40, 80, "Alpha distinct", 12), (40, 180, "Beta different", 12)]],
    )
    _write_pdf(
        candidate,
        [[(70, 100, "Alpha distinct", 12), (70, 200, "Beta different", 12)]],
    )

    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)

    assert result["axes"]["canvas"]["metrics"]["exact_paired_size_rate"] == 1.0
    assert result["axes"]["content"]["metrics"]["token_inventory"]["f1"] == 1.0
    assert result["axes"]["geometry"]["metrics"]["center_displacement_q90"] > 0.05
    raster = result["axes"]["raster_diagnostic"]
    assert raster["metrics"]["registered_tolerant_ink_f1_macro"] > raster["metrics"]["unregistered_tolerant_ink_f1_macro"]
    page = raster["evidence"]["pages"][0]
    assert page["coordinate_frame"] == "registered_reference_raster"
    assert page["registration_translation_px"] != [0, 0]
    assert raster["evidence"]["top_difference_bbox"] is None


@pytest.mark.parametrize("extra_side", ["reference", "candidate"])
def test_unpaired_raster_residual_records_its_drawing_side(tmp_path: Path, extra_side: str) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    one_page = [[(40, 80, "shared", 12)]]
    two_pages = one_page + [[(40, 80, "extra", 12)]]
    _write_pdf(reference, two_pages if extra_side == "reference" else one_page)
    _write_pdf(candidate, two_pages if extra_side == "candidate" else one_page)
    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)
    top = result["axes"]["raster_diagnostic"]["evidence"]["top_difference_bbox"]
    assert top["unpaired_side"] == extra_side
    assert top["coordinate_frame"] == extra_side
    assert top["normalized_bbox"] == [0.0, 0.0, 1.0, 1.0]


def test_content_omission_has_inventory_and_localized_evidence(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(reference, [[(40, 80, "alpha beta gamma", 12)]])
    _write_pdf(candidate, [[(40, 80, "alpha beta", 12)]])

    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)
    content = result["axes"]["content"]

    assert content["metrics"]["token_inventory"]["precision"] == 1.0
    assert content["metrics"]["token_inventory"]["recall"] == pytest.approx(2 / 3)
    assert content["metrics"]["document_normalized_edit_similarity"] < 1.0
    assert content["evidence"]["unmatched_reference_words"][0]["normalized"] == "gamma"
    assert result["axes"]["raster_diagnostic"]["evidence"]["top_difference_bbox"] is not None


def test_content_normalization_preserves_case(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(reference, [[(40, 80, "Mass M", 12)]])
    _write_pdf(candidate, [[(40, 80, "mass m", 12)]])

    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)

    assert result["axes"]["content"]["metrics"]["token_inventory"]["f1"] == 0.0
    assert result["axes"]["text_grounding"]["metrics"]["word_hmean"] == 0.0


def test_reading_order_uses_matched_blocks_and_reports_inversion(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(reference, [[(40, 70, "First alpha", 12), (40, 170, "Second beta", 12)]])
    _write_pdf(candidate, [[(40, 70, "Second beta", 12), (40, 170, "First alpha", 12)]])

    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)
    order = result["axes"]["reading_order"]

    assert order["status"] == "scored"
    assert order["metrics"]["matched_block_count"] == 2
    assert order["metrics"]["inversion_count"] == 1
    assert order["metrics"]["kendall_tau"] == -1.0
    assert len(order["evidence"]["inverted_block_pairs"]) == 1


def test_repeated_word_matching_respects_occurrence_order(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(reference, [[(40, 70, "token", 12), (40, 170, "token", 12)]])
    _write_pdf(candidate, [[(45, 75, "token", 12), (45, 175, "token", 12)]])

    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)
    evidence = result["axes"]["geometry"]["evidence"]["worst_token_pairs"]

    assert [item["reference_word_index"] for item in evidence] == [0, 1]
    assert [item["candidate_word_index"] for item in evidence] == [0, 1]


def test_pagination_reports_page_assignment_and_break_error(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _write_pdf(
        reference,
        [[(40, 80, "Page one alpha", 12)], [(40, 80, "Page two beta", 12)]],
    )
    _write_pdf(
        candidate,
        [[(40, 80, "Page one alpha", 12), (40, 180, "Page two beta", 12)], []],
    )

    result = evaluate_pdf_pair(reference, candidate, render_dpi=96)
    pagination = result["axes"]["pagination"]

    assert pagination["metrics"]["page_count_delta"] == 0
    assert pagination["metrics"]["matched_block_page_assignment_accuracy"] == 0.5
    assert pagination["metrics"]["page_break_recall"] == 0.0
    assert pagination["metrics"]["page_break_f1"] == 0.0
    assert len(pagination["evidence"]["mismatched_page_breaks"]) == 1


def test_specialized_axes_abstain_honestly_from_source_flags(tmp_path: Path) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _two_block_pdf(reference)
    _two_block_pdf(candidate)

    result = evaluate_pdf_pair(
        reference,
        candidate,
        applicability={
            "tables": {"reference": True, "candidate": True},
            "formulas": False,
        },
        render_dpi=96,
    )

    assert result["axes"]["tables"]["status"] == "abstain"
    assert result["axes"]["tables"]["applicable"] is True
    assert result["axes"]["tables"]["metrics"] == {}
    assert result["axes"]["formulas"]["status"] == "not_applicable"
    assert result["axes"]["figures"]["status"] == "abstain"
    assert result["axes"]["figures"]["applicable"] is None


def test_extraction_cache_uses_file_fingerprint(tmp_path: Path) -> None:
    path = tmp_path / "cached.pdf"
    _write_pdf(path, [[(40, 80, "alpha", 12)]])
    clear_extraction_cache()

    first = extract_pdf(path)
    second = extract_pdf(path)
    assert first is second

    replacement = tmp_path / "replacement.pdf"
    _write_pdf(replacement, [[(40, 80, "alpha beta", 12)]])
    path.write_bytes(replacement.read_bytes())
    third = extract_pdf(path)
    assert third is not first
    assert len(third.words) == 2


def test_cli_emits_deterministic_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    reference = tmp_path / "reference.pdf"
    candidate = tmp_path / "candidate.pdf"
    _two_block_pdf(reference)
    _two_block_pdf(candidate)

    exit_code = main(
        [
            str(reference),
            str(candidate),
            "--render-dpi",
            "96",
            "--applicability-json",
            '{"tables": false}',
        ]
    )
    first = capsys.readouterr().out
    exit_code_again = main(
        [
            str(reference),
            str(candidate),
            "--render-dpi",
            "96",
            "--applicability-json",
            '{"tables": false}',
        ]
    )
    second = capsys.readouterr().out

    assert exit_code == exit_code_again == 0
    assert first == second
    parsed = json.loads(first)
    assert parsed["axes"]["tables"]["status"] == "not_applicable"
