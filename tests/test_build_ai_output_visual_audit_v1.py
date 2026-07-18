from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from build_ai_output_visual_audit_v1 import _axis_text, _blind_rows  # noqa: E402


def test_blind_order_is_deterministic_exhaustive_and_not_source_sorted() -> None:
    profile = [{"sample_id": f"sample_{index:03d}"} for index in range(20)]
    scores = {row["sample_id"]: {"sample_id": row["sample_id"]} for row in profile}

    first = [row[0]["sample_id"] for row in _blind_rows(profile, scores)]
    second = [row[0]["sample_id"] for row in _blind_rows(profile, scores)]

    assert first == second
    assert set(first) == set(scores)
    assert first != sorted(first)


def test_axis_text_shows_zero_and_abstention_explicitly() -> None:
    row = {}
    for axis in ("content", "layout", "typography", "appearance", "pagination", "structure"):
        row[f"axis_{axis}"] = "0.0" if axis == "layout" else ""
        row[f"band_{axis}"] = "abstain"

    text = _axis_text(row)

    assert "LAYOUT 0.000 | abstain" in text
    assert "STRUCTURE - | abstain" in text
