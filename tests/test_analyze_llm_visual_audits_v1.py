from scripts.evaluation.analyze_llm_visual_audits_v1 import _rate, _spearman


def test_spearman_handles_ties_and_direction() -> None:
    assert _spearman([1, 2, 2, 4], [4, 3, 3, 1]) == -1.0
    assert _spearman([1, 1, 1], [1, 2, 3]) is None


def test_rate_preserves_missing_records() -> None:
    assert _rate([True, False, None]) == {
        "true": 1, "false": 1, "missing": 1, "rate": 0.5,
    }
