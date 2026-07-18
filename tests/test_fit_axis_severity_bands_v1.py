from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from fit_axis_severity_bands_v1 import fit_bands  # noqa: E402


def _row(sample: str, severity: int, score: float, variant: str = "balanced") -> dict[str, str]:
    return {
        "sample_id": sample, "status": "applied", "applicable": "true",
        "severity": str(severity), "expected_axis": "content", "axis_content": str(score),
        "variant": variant,
    }


def test_bands_fit_only_development_and_evaluate_held_partitions() -> None:
    rows = []
    partitions = {}
    for partition, sample in (("metric_dev", "d"), ("metric_validation", "v"), ("metric_test", "t")):
        partitions[sample] = partition
        rows.extend(_row(sample, severity, 1.0 - severity * 0.2) for severity in range(4))
    result = fit_bands(rows, partitions, ["axis_content"])
    content = result["axes"]["axis_content"]
    assert content["status"] == "synthetic_internal_pass"
    assert content["thresholds"] == {
        "reference_like_min": 0.9, "mild_min": 0.7,
        "moderate_min": 0.5, "severe_below": 0.5,
    }
    assert content["evaluation"]["metric_validation"]["exact_accuracy"] == 1.0
    assert content["evaluation"]["metric_test"]["within_one_accuracy"] == 1.0


def test_collapsed_development_anchors_remain_trial() -> None:
    rows = [_row("d", severity, 1.0) for severity in range(4)]
    result = fit_bands(rows, {"d": "metric_dev"}, ["axis_content"])
    assert result["axes"]["axis_content"]["status"] == "trial"


def test_frozen_thresholds_are_not_deployed_after_held_gate_failure() -> None:
    rows = [_row("d", severity, 1.0 - severity * 0.2) for severity in range(4)]
    rows += [_row("v", severity, 1.0) for severity in range(4)]
    rows += [_row("t", severity, 1.0) for severity in range(4)]
    result = fit_bands(
        rows, {"d": "metric_dev", "v": "metric_validation", "t": "metric_test"},
        ["axis_content"],
    )
    content = result["axes"]["axis_content"]
    assert content["thresholds"]["reference_like_min"] == 0.9
    assert content["status"] == "trial"
    assert content["held_gate"]["metric_validation_pass"] is False


def test_incomplete_variant_is_excluded_from_balanced_anchors() -> None:
    rows = []
    partitions = {}
    for partition, sample in (("metric_dev", "d"), ("metric_validation", "v"), ("metric_test", "t")):
        partitions[sample] = partition
        rows.extend(_row(sample, severity, 1.0 - severity * 0.2) for severity in range(4))
    rows.append(_row("d", 2, -100.0, variant="severity_two_only"))
    content = fit_bands(rows, partitions, ["axis_content"])["axes"]["axis_content"]
    assert content["development_anchor_medians"]["moderate"] == 0.6


def test_complete_variants_receive_equal_weight_after_duplicate_averaging() -> None:
    rows = []
    partitions = {}
    for partition, sample in (("metric_dev", "d"), ("metric_validation", "v"), ("metric_test", "t")):
        partitions[sample] = partition
        rows.append(_row(sample, 0, 1.0))
        for severity, first, second in ((1, 0.9, 0.5), (2, 0.8, 0.4), (3, 0.7, 0.3)):
            rows.append(_row(sample, severity, first, variant="a"))
            rows.append(_row(sample, severity, second, variant="b"))
        rows.extend(_row(sample, 1, 0.9, variant="a") for _ in range(4))
    content = fit_bands(rows, partitions, ["axis_content"])["axes"]["axis_content"]
    assert abs(content["development_anchor_medians"]["mild"] - 0.7) < 1e-12
