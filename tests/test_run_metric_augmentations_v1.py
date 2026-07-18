from __future__ import annotations

import hashlib
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from run_metric_augmentations_v1 import (  # noqa: E402
    COMPOUND_SPECS,
    CONTROL_SPECS,
    UNIVERSAL_SPECS,
    FamilySpec,
    PlanCase,
    ReferenceCache,
    _flatten_metric,
    execute_case,
    generate_variant,
    plan_cases,
    summarize_plan,
)


def make_pdf(path: Path, *, pages: int = 1, numeric: bool = True) -> None:
    document = fitz.open()
    for page_index in range(pages):
        page = document.new_page(width=400, height=500)
        page.insert_text((40, 70), "Research methods", fontsize=16)
        suffix = " value 42" if numeric else ""
        page.insert_textbox(
            fitz.Rect(40, 100, 350, 220),
            "A substantial paragraph spans multiple lines for deterministic mutation.\n"
            f"Second line carries source evidence{suffix}.",
            fontsize=10,
        )
    document.save(path)
    document.close()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class RunMetricAugmentationsTest(unittest.TestCase):
    def test_variant_generation_is_deterministic_and_has_bbox(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "reference.pdf"
            make_pdf(source)
            spec = next(spec for spec in UNIVERSAL_SPECS if spec.name == "text_deletion")
            case = PlanCase("sample", "01_prose_sections", source, spec, 2, 17)
            first, second = root / "first.pdf", root / "second.pdf"
            cache = ReferenceCache()
            first_target = generate_variant(cache, case, first)
            second_target = generate_variant(cache, case, second)
            self.assertEqual(digest(first), digest(second))
            self.assertEqual(first_target.page, 0)
            self.assertGreater(first_target.bbox[2] - first_target.bbox[0], 0)
            self.assertGreater(first_target.bbox[3] - first_target.bbox[1], 0)
            result = execute_case(
                cache, case, root / "evaluated.pdf", "stub",
                lambda _reference, _candidate: ({"axis_content": 0.8}, 0, (0.1, 0.2, 0.3, 0.4)),
            )
            expected_bbox = json.loads(result["expected_bbox"])
            self.assertEqual(result["expected_page"], 0)
            self.assertEqual(result["predicted_page"], 0)
            self.assertTrue(all(0.0 <= value <= 1.0 for value in expected_bbox))

    def test_not_applicable_is_logged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "reference.pdf"
            make_pdf(source, numeric=False)
            spec = next(spec for spec in UNIVERSAL_SPECS if spec.name == "numeric_corruption")
            case = PlanCase("sample", "01_prose_sections", source, spec, 1, 17)
            result = execute_case(
                ReferenceCache(), case, root / "candidate.pdf", "stub",
                lambda _reference, _candidate: ({"axis_content": 1.0}, None, None),
            )
            self.assertEqual(result["status"], "not_applicable")
            self.assertEqual(result["applicable"], "false")
            self.assertIn("no matching text", result["reason"])

    def test_matrix_counts_are_exact_and_scope_applicability_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample_dir = root / "sample"
            sample_dir.mkdir()
            make_pdf(sample_dir / "reference.pdf", pages=1)
            rows = [{
                "sample_id": "sample", "category": "01_prose_sections", "status": "accepted",
                "sample_dir": str(sample_dir),
            }]
            cases = plan_cases(rows, seed=17)
            expected = (
                sum(len(spec.severities) for spec in CONTROL_SPECS)
                + sum(len(spec.severities) for spec in UNIVERSAL_SPECS)
                + sum(len(spec.severities) for spec in COMPOUND_SPECS)
                + 9  # three prose-specialized variants at three severities
            )
            self.assertEqual(len(cases), expected)
            self.assertEqual(expected, 91)  # 82 universal/control + 9 prose
            plan, summary = summarize_plan(ReferenceCache(), cases)
            page_cases = [row for row in plan if row["family"] == "page_sequence_and_count"]
            self.assertEqual(page_cases, [])
            self.assertEqual(summary["cases"], expected)
            self.assertEqual(sum(summary["status_counts"].values()), expected)

    def test_raw_v1_metrics_are_projected_without_structure_claim(self) -> None:
        axes, page, bbox = _flatten_metric({
            "inputs": {"reference_page_count": 2, "candidate_page_count": 3},
            "axes": {
                "content": {"metrics": {"token_inventory": {"f1": 0.8}}},
                "geometry": {"metrics": {"bbox_iou_q10": 0.7}},
                "typography": {"metrics": {
                    "font_size_abs_log_ratio_max": math.log(2),
                    "baseline_displacement_q90": 0.0,
                    "style_coverage_hmean": 1.0,
                }},
                "pagination": {"metrics": {"page_break_f1": 0.9}},
                "raster_diagnostic": {
                    "metrics": {"unregistered_tolerant_ink_f1_macro": 0.6},
                    "evidence": {"top_difference_bbox": {
                        "page": 0, "normalized_bbox": [0.1, 0.2, 0.3, 0.4],
                    }},
                },
                "tables": {"status": "abstain", "metrics": {}},
            },
        })
        self.assertAlmostEqual(axes["axis_content"], 0.8)
        self.assertAlmostEqual(axes["axis_layout"], 0.7)
        self.assertAlmostEqual(axes["axis_typography"], 0.5)
        self.assertAlmostEqual(axes["axis_appearance"], 0.6)
        self.assertAlmostEqual(axes["axis_pagination"], 0.6)
        self.assertNotIn("axis_structure", axes)
        self.assertEqual(page, 0)
        self.assertEqual(bbox, (0.1, 0.2, 0.3, 0.4))

    def test_center_displacement_layout_projection_has_defined_scale(self) -> None:
        axes, _page, _bbox = _flatten_metric({
            "inputs": {"reference_page_count": 1, "candidate_page_count": 1},
            "axes": {
                "geometry": {"metrics": {"center_displacement_q90": math.sqrt(2) / 10}},
                "pagination": {"metrics": {"page_break_f1": 1.0}},
            },
        }, layout_projection="center_displacement_q90")
        self.assertAlmostEqual(axes["axis_layout"], 0.9)


if __name__ == "__main__":
    unittest.main()
