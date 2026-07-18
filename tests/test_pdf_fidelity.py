from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from pdf_fidelity import compare_pdfs  # noqa: E402


def make_pdf(path: Path, *, shift: float = 0.0, omit_second_line: bool = False,
             value: str = "42", page_order: tuple[int, ...] = (1,)) -> None:
    document = fitz.open()
    page_phrases = {
        1: "alpha amber atlas autumn cedar delta ember forest",
        2: "binary cobalt circuit data engine flux graph horizon",
        3: "kernel lunar matrix nebula orbit plasma quantum vector",
        4: "willow xenon yellow zenith bridge cloud river stone",
    }
    for page_number in page_order:
        page = document.new_page(width=612, height=792)
        page.insert_text((72 + shift, 100 + shift), f"PDF fidelity page {page_number}", fontsize=18,
                         fontname="helv")
        if not omit_second_line:
            page.insert_text(
                (72 + shift, 140 + shift),
                f"Content and layout must both matter. Recorded value {value}.",
                fontsize=12,
                fontname="hebo",
            )
            page.insert_text(
                (72 + shift, 170 + shift),
                page_phrases.get(page_number, "unique fallback page content"),
                fontsize=10,
                fontname="helv",
            )
    document.save(path)
    document.close()


def make_repetitive_pages(path: Path, order: tuple[int, ...]) -> None:
    document = fitz.open()
    common = "Repeated table report common header metric score standard deviation confidence interval"
    for page_number in order:
        page = document.new_page(width=612, height=792)
        page.insert_text((72, 90), common, fontsize=12, fontname="hebo")
        for row in range(8):
            page.insert_text(
                (72, 130 + row * 24),
                f"common row label result value page {page_number} item {100 * page_number + row}",
                fontsize=10,
                fontname="helv",
            )
    document.save(path)
    document.close()


def make_figure_pdf(path: Path, *, include_figure: bool = True) -> None:
    document = fitz.open()
    page = document.new_page(width=612, height=792)
    page.insert_text((72, 90), "Figure fidelity example", fontsize=16, fontname="helv")
    if include_figure:
        page.draw_rect(fitz.Rect(120, 180, 470, 430), color=(0, 0, 0), width=2)
        page.draw_line((140, 400), (440, 210), color=(0, 0, 0), width=3)
        page.draw_circle((305, 305), 70, color=(0, 0, 0), width=3)
    document.save(path)
    document.close()


def make_table_pdf(path: Path, *, rows: int) -> None:
    document = fitz.open()
    page = document.new_page(width=612, height=792)
    x0, y0, width, row_height = 72, 140, 420, 36
    for row in range(rows + 1):
        y = y0 + row * row_height
        page.draw_line((x0, y), (x0 + width, y), color=(0, 0, 0), width=1)
    for column in range(4):
        x = x0 + column * width / 3
        page.draw_line((x, y0), (x, y0 + rows * row_height), color=(0, 0, 0), width=1)
    for row in range(rows):
        for column in range(3):
            page.insert_text(
                (x0 + column * width / 3 + 8, y0 + row * row_height + 23),
                f"r{row}c{column}", fontsize=10, fontname="helv",
            )
    document.save(path)
    document.close()


def make_formula_pdf(path: Path) -> None:
    document = fitz.open()
    page = document.new_page(width=612, height=792)
    page.insert_text((72, 120), "abcde", fontsize=20, fontname="symb")
    document.save(path)
    document.close()


class PdfFidelityTest(unittest.TestCase):
    def test_identity_scores_one(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "identity.pdf"
            make_pdf(path)
            result, *_ = compare_pdfs(path, path)
            for name, score in result["scores"].items():
                self.assertAlmostEqual(score, 1.0, places=6, msg=name)
            self.assertEqual(result["scorecard"]["status"], "pass")
            self.assertIsNone(result["scorecard"]["aggregate_score"])
            for axis in result["scorecard"]["axes"].values():
                self.assertAlmostEqual(axis["score"], 1.0, places=6)

    def test_shift_reduces_visual_not_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            shifted = Path(directory) / "shifted.pdf"
            make_pdf(reference)
            make_pdf(shifted, shift=36)
            result, *_ = compare_pdfs(reference, shifted)
            self.assertGreater(result["scores"]["content"], 0.99)
            self.assertLess(result["scores"]["visual"], 0.75)
            # Relative flow and reading order remain correct under a rigid shift,
            # so layout falls moderately while the unregistered raster term
            # supplies the stronger visible penalty.
            self.assertLess(result["scores"]["layout"], 0.85)

    def test_omission_reduces_content_and_overall(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            omitted = Path(directory) / "omitted.pdf"
            make_pdf(reference)
            make_pdf(omitted, omit_second_line=True)
            result, *_ = compare_pdfs(reference, omitted)
            self.assertLess(result["scores"]["content"], 0.80)
            self.assertLess(result["scores"]["overall"], 0.85)
            self.assertGreater(result["unmatched_reference_words"], 0)
            self.assertEqual(result["scorecard"]["status"], "fail")
            self.assertIn("token_recall", result["scorecard"]["failed_gates"])

    def test_numeric_change_is_diagnostic_without_unvalidated_hard_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            changed = Path(directory) / "changed.pdf"
            make_pdf(reference, value="42")
            make_pdf(changed, value="43")
            result, *_ = compare_pdfs(reference, changed)
            self.assertNotIn("numeric_token_multiset", result["scorecard"]["failed_gates"])
            self.assertNotIn("numeric_token_mismatch", result["scorecard"]["review_flags"])
            self.assertIn("numeric_token_mismatch", result["scorecard"]["diagnostic_flags"])

    def test_page_sequence_detects_reordering_and_extra_page(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            reordered = Path(directory) / "reordered.pdf"
            extra = Path(directory) / "extra.pdf"
            make_pdf(reference, page_order=(1, 2, 3))
            make_pdf(reordered, page_order=(1, 3, 2))
            make_pdf(extra, page_order=(1, 2, 3, 4))
            reordered_result, *_ = compare_pdfs(reference, reordered)
            extra_result, *_ = compare_pdfs(reference, extra)
            self.assertLess(
                reordered_result["scorecard"]["axes"]["pagination"]["score"], 0.85
            )
            self.assertIn(
                "low_page_sequence_alignment", reordered_result["scorecard"]["review_flags"]
            )
            self.assertIn("page_count", extra_result["scorecard"]["failed_gates"])

    def test_page_sequence_uses_rare_tokens_for_repetitive_pages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            reordered = Path(directory) / "reordered.pdf"
            make_repetitive_pages(reference, (1, 2))
            make_repetitive_pages(reordered, (2, 1))
            result, *_ = compare_pdfs(reference, reordered)
            self.assertLess(result["scorecard"]["axes"]["pagination"]["score"], 0.90)
            self.assertIn("low_page_sequence_alignment", result["scorecard"]["review_flags"])

    def test_correspondence_coverage_exposes_survivor_bias(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            omitted = Path(directory) / "omitted.pdf"
            make_pdf(reference)
            make_pdf(omitted, omit_second_line=True)
            result, *_ = compare_pdfs(reference, omitted)
            evidence = result["scorecard"]["axes"]["layout"]["correspondence_evidence"]
            self.assertLess(evidence["minimum_coverage"], 0.80)
            self.assertIn(
                "low_layout_correspondence_coverage", result["scorecard"]["review_flags"]
            )

    def test_nontext_and_local_metrics_detect_missing_figure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            missing = Path(directory) / "missing.pdf"
            make_figure_pdf(reference, include_figure=True)
            make_figure_pdf(missing, include_figure=False)
            result, *_ = compare_pdfs(reference, missing)
            appearance = result["scorecard"]["axes"]["appearance_proxy"]
            self.assertTrue(appearance["nontext"]["applicable"])
            self.assertLess(appearance["nontext"]["score"], 0.65)
            self.assertLess(appearance["local_worst_region"], 0.70)
            self.assertIn("nontext_structure_mismatch", result["scorecard"]["diagnostic_flags"])
            self.assertIn("localized_appearance_failure", result["scorecard"]["diagnostic_flags"])

    def test_table_topology_reports_row_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.pdf"
            candidate = Path(directory) / "candidate.pdf"
            make_table_pdf(reference, rows=4)
            make_table_pdf(candidate, rows=3)
            result, *_ = compare_pdfs(reference, candidate)
            tables = result["scorecard"]["specialized_diagnostics"]["tables"]
            self.assertTrue(tables["applicable"])
            self.assertLess(tables["row_count_exact_rate"], 1.0)
            self.assertIn("table_structure_mismatch", result["scorecard"]["review_flags"])

    def test_formula_glyph_proxy_is_exact_on_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "formula.pdf"
            make_formula_pdf(path)
            result, *_ = compare_pdfs(path, path)
            formula = result["scorecard"]["specialized_diagnostics"]["formula_glyph_proxy"]
            self.assertTrue(formula["applicable"])
            self.assertAlmostEqual(formula["character_f1"], 1.0)


if __name__ == "__main__":
    unittest.main()
