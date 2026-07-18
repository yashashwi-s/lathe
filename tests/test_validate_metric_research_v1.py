from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from validate_metric_research_v1 import analyze_rows, read_csv  # noqa: E402


FIELDS = [
    "sample_id", "category", "family", "severity", "seed", "applicable",
    "expected_axis", "expected_page", "expected_bbox", "predicted_page",
    "predicted_bbox", "components", "axis_content", "axis_layout",
]


def row(sample: str, category: str, family: str, severity: float, expected_axis: str,
        content: object, layout: object, *, seed: str = "a", expected_page: object = "",
        expected_bbox: object = "", predicted_page: object = "",
        predicted_bbox: object = "", components: str = "") -> dict[str, object]:
    return {
        "sample_id": sample, "category": category, "family": family,
        "severity": severity, "seed": seed, "applicable": "true",
        "expected_axis": expected_axis, "expected_page": expected_page,
        "expected_bbox": expected_bbox, "predicted_page": predicted_page,
        "predicted_bbox": predicted_bbox, "components": components,
        "axis_content": content, "axis_layout": layout,
    }


class ValidateMetricResearchTest(unittest.TestCase):
    def test_synthetic_csv_relations_and_clustered_summary(self) -> None:
        rows = [
            row("s1", "text", "identity", 0, "none", 1.0, 1.0),
            row("s1", "text", "rewrite", 0, "invariant", 0.999, 1.0),
            row("s1", "text", "deletion", 1, "content", 0.9, 0.99,
                expected_page=1, expected_bbox="[0,0,10,10]", predicted_page=1,
                predicted_bbox="[0,0,10,10]"),
            row("s1", "text", "deletion", 1, "content", 0.9, 0.99,
                expected_page=1, expected_bbox="[0,0,10,10]", predicted_page=1,
                predicted_bbox="[0,0,10,10]"),  # deterministic rerun
            row("s1", "text", "deletion", 2, "content", 0.7, 0.98),
            row("s1", "text", "movement", 1, "layout", 0.99, 0.8),
            row("s1", "text", "compound:deletion+movement", 1, "layout", 0.8, 0.7,
                components="deletion+movement"),
            row("s2", "table", "identity", 0, "none", 1.0, 1.0),
            row("s2", "table", "rewrite", 0, "invariant", 0.8, 1.0),
            row("s2", "table", "deletion", 1, "content", 0.85, 0.99,
                expected_page=1, expected_bbox="0,0,10,10", predicted_page=2,
                predicted_bbox="20,20,30,30"),
            row("s2", "table", "deletion", 2, "content", 0.9, 0.98),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tiny.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            result = analyze_rows(read_csv(path), bootstrap_replicates=100, seed=7)

        deletion = result["per_family"]["deletion"]["document_macro"]
        self.assertEqual(result["source_documents"], 2)
        self.assertAlmostEqual(deletion["adjacent_monotonic_accuracy"], 0.75)
        self.assertAlmostEqual(deletion["kendall_tau_b"], 2 / 3)
        self.assertAlmostEqual(deletion["localization_hit_rate"], 0.5)
        self.assertAlmostEqual(deletion["localization_mean_iou"], 0.5)
        self.assertAlmostEqual(result["document_macro"]["invariant_false_positive_rate"], 0.5)
        self.assertAlmostEqual(
            result["per_family"]["compound:deletion+movement"]["document_macro"]
            ["compound_dominance_accuracy"], 1.0,
        )
        self.assertAlmostEqual(
            result["document_macro"]["projection_repeat_agreement"], 1.0
        )
        self.assertEqual(result["bootstrap_95_ci"]["replicates"], 100)
        self.assertIn("adjacent_monotonic_accuracy", result["bootstrap_95_ci"]["document_macro"])

    def test_missing_expected_axis_score_is_an_abstention(self) -> None:
        rows = [
            row("s1", "text", "identity", 0, "none", 1.0, 1.0),
            row("s1", "text", "deletion", 1, "content", "", 0.9),
        ]
        result = analyze_rows(rows, bootstrap_replicates=0)
        self.assertEqual(result["per_family"]["deletion"]["document_macro"]["abstention_rate"], 1.0)

    def test_multi_axis_target_validates_every_named_axis(self) -> None:
        rows = [
            row("s1", "mixed", "identity", 0, "none", 1.0, 1.0),
            row("s1", "mixed", "crop", 1, "content+layout", 0.9, 0.8),
            row("s1", "mixed", "crop", 2, "content+layout", 0.7, 0.6),
            row("s1", "mixed", "crop", 3, "content+layout", 0.5, 0.4),
        ]
        result = analyze_rows(rows, bootstrap_replicates=0)
        metrics = result["per_family"]["crop"]["document_macro"]
        self.assertAlmostEqual(metrics["adjacent_monotonic_accuracy"], 1.0)
        self.assertAlmostEqual(metrics["kendall_tau_b"], 1.0)
        self.assertIsNone(result["gate_assessment"]["overall"]["projection_repeat_confirmed"])
        self.assertNotIn(
            "projection_repeat_confirmed",
            result["gate_assessment"]["mandatory_controlled_response_gates"],
        )


if __name__ == "__main__":
    unittest.main()
