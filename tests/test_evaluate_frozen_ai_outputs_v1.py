from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from evaluate_frozen_ai_outputs_v1 import _ai_provenance, _band, _summary  # noqa: E402


DEFINITION = {
    "status": "synthetic_internal_pass",
    "deploy_to_ai_outputs": True,
    "thresholds": {"reference_like_min": 0.9, "mild_min": 0.7, "moderate_min": 0.5},
}


def test_validated_band_mapping_is_axis_specific() -> None:
    assert [_band(value, DEFINITION) for value in (0.95, 0.8, 0.6, 0.4)] == [
        "reference_like", "mild", "moderate", "severe",
    ]


def test_failed_held_gate_abstains_instead_of_labeling_ai_output() -> None:
    assert _band(0.95, {**DEFINITION, "deploy_to_ai_outputs": False}) == "abstain"


def test_ai_provenance_preserves_prompt_hash_and_successful_attempt(tmp_path: Path) -> None:
    run_dir = tmp_path / "run"
    sample_dir = run_dir / "samples" / "sample"
    sample_dir.mkdir(parents=True)
    candidate = sample_dir / "output.pdf"
    candidate.touch()
    (run_dir / "run_config.json").write_text(json.dumps({
        "model": "provider/model-route",
        "prompt_path": "prompts/system_v2.txt",
        "system_prompt_sha256": "system-sha",
        "retry_prompt_path": "prompts/retry_v2.txt",
        "retry_prompt_sha256": "retry-sha",
        "temperature": 0,
        "typst_version": "typst 0.14.2 (unknown hash)",
    }))
    (sample_dir / "meta.json").write_text(json.dumps({
        "requested_model": "provider/model-route",
        "resolved_model": "provider/model-route",
        "attempts": 2,
        "repaired": True,
        "response_id": "response-2",
        "attempt_records": [
            {"attempt": 1, "compile_ok": False},
            {"attempt": 2, "compile_ok": True},
        ],
    }))

    provenance = _ai_provenance(candidate)

    assert provenance["ai_system_prompt_sha256"] == "system-sha"
    assert provenance["ai_retry_prompt_sha256"] == "retry-sha"
    assert provenance["ai_final_attempt"] == 2
    assert provenance["ai_model_checkpoint"] == "not_recorded_api_route_only"


def test_summary_counts_zero_as_a_scored_axis_value() -> None:
    row = {
        "category": "category",
        "ai_model_id": "model",
        "ai_resolved_model": "model",
        "ai_system_prompt_sha256": "prompt-sha",
        "ai_selected_stage": "v1",
        "ai_final_attempt": "1",
        "analysis_role": "descriptive",
        "page_count_match": "true",
        "canvas_match": "true",
    }
    for axis in ("content", "layout", "typography", "appearance", "structure", "pagination"):
        row[f"axis_{axis}"] = 0.0
        row[f"band_{axis}"] = "abstain"

    summary = _summary([row], {})

    assert summary["axes"]["layout"]["scored_outputs"] == 1
    assert summary["axes"]["layout"]["raw_median"] == 0.0
