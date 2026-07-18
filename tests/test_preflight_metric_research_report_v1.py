from __future__ import annotations

import unittest

from scripts.evaluation.preflight_metric_research_report_v1 import (
    _completed_ai_audit,
    _completed_control_audit,
    _register_rows,
)


class ReportPreflightTest(unittest.TestCase):
    def test_completed_control_audit_accepts_explicit_records(self) -> None:
        responses = [{
            "confidence": "high", "reviewer": "research_audit", "abstain": "false",
            "changed_panel": "A", "visible_defect_axis": "content",
            "region_description": "lower-left paragraph",
        } for _ in range(628)]
        answers = [{
            "candidate_panel_hidden_truth": "A", "candidate_valid": "true",
            "mutation_visible": "true", "target_box_correct": "true",
            "label_correct": "true", "predicted_box_useful": "false",
            "reviewer": "research_audit",
        } for _ in range(628)]
        self.assertEqual(_completed_control_audit(responses, answers), [])

    def test_incomplete_ai_audit_is_rejected(self) -> None:
        responses = [{
            "severity_summary": "major layout drift", "confidence": "high",
            "review_notes": "visible reflow", "reviewer": "research_audit",
        } for _ in range(156)]
        answers = [{
            "top_residual_box_useful_after_unblind": "true",
            "axis_labels_plausible_after_unblind": "true",
            "unblind_notes": "",
            "reviewer": "research_audit",
        } for _ in range(156)]
        errors = _completed_ai_audit(responses, answers)
        self.assertTrue(any("post-unblind audit records incomplete" in error for error in errors))

    def test_register_labels_reference_and_ai_output_roles(self) -> None:
        profile = [{
            "sample_id": "sample_001", "category": "prose", "prompt_split": "heldout",
            "metric_partition": "metric_test", "reference_pages": "1",
            "ai_model_id": "google/gemini-3.1-flash-lite", "ai_selected_stage": "v1",
        }]
        score = {
            "sample_id": "sample_001", "page_count_match": "true", "canvas_match": "false",
        }
        for axis in ("content", "layout", "typography", "appearance", "structure", "pagination"):
            score[f"axis_{axis}"] = "0.5"
            score[f"band_{axis}"] = "abstain"
        rows = _register_rows(profile, [score], [])
        self.assertEqual(rows[0]["ai_output_label"], "AI-produced Typst PDF")
        self.assertEqual(rows[0]["ai_model_id"], "google/gemini-3.1-flash-lite")
        self.assertEqual(rows[0]["ai_quality_band_content"], "abstain")


if __name__ == "__main__":
    unittest.main()
