from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from pdf_fidelity import compare_pdfs  # noqa: E402


def make_pdf(path: Path, *, shift: float = 0.0, omit_second_line: bool = False) -> None:
    document = fitz.open()
    page = document.new_page(width=612, height=792)
    page.insert_text((72 + shift, 100 + shift), "PDF fidelity identity test", fontsize=18,
                     fontname="helv")
    if not omit_second_line:
        page.insert_text((72 + shift, 140 + shift), "Content and layout must both matter.",
                         fontsize=12, fontname="hebo")
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


if __name__ == "__main__":
    unittest.main()
