from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from build_publication_scorecard_v0 import (  # noqa: E402
    EXPECTED_COMPILED,
    build_publication_data,
)


def test_publication_scorecard_is_exact_frozen_heldout_protocol() -> None:
    document, per_sample = build_publication_data(ROOT)

    assert len(per_sample) == 127 * 5
    assert document["validation"]["actual_compiled_n"] == EXPECTED_COMPILED
    assert document["validation"]["prompt_dev_overlap_n"] == 0
    assert document["validation"]["adaptive_v0_v2_v3_rows_used"] == 0
    assert document["validation"]["claude_rows_used"] == 0
    assert document["validation"]["first_pass_compiled_n"] == 46
    assert document["validation"]["after_one_repair_compiled_n"] == 77

    gemini = [row for row in per_sample if row["system_id"].startswith("gemini_")]
    assert all(
        not row["candidate_pdf"]
        or "/prompt_v1_heldout_clean/samples/" in row["candidate_pdf"]
        for row in gemini
    )
    assert all(
        row["metric_v2_status"] == "scored"
        if row["compiled"] else row["metric_v2_status"] == "not_scored_uncompiled"
        for row in per_sample
    )


def test_fidelity_medians_are_conditioned_on_compiled_rows() -> None:
    document, per_sample = build_publication_data(ROOT)
    by_system = {row["system_id"]: row for row in document["scorecard"]}

    for system_id, expected in EXPECTED_COMPILED.items():
        summary = by_system[system_id]
        rows = [row for row in per_sample if row["system_id"] == system_id]
        assert summary["universe_n"] == 127
        assert summary["compiled_n"] == expected
        assert sum(row["compiled"] is True for row in rows) == expected
        assert all(
            row["strict_word_f1"] == "" and row["candidate_pdf"] == ""
            for row in rows
            if row["compiled"] is False
        )
        assert summary["fidelity_population"] == "compiled PDFs only (system-specific subset)"
