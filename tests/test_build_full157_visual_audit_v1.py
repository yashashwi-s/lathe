from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from build_full157_visual_audit_v1 import _blind_order, _candidate_panel, _selected  # noqa: E402


def test_audit_selection_has_three_universal_and_one_category_case() -> None:
    universal = [
        {"sample_id": "s", "category": "01_prose_sections", "variant": variant,
         "severity": "2", "candidate_pdf": f"{variant}.pdf"}
        for variant in ("text_deletion", "block_right", "local_occlusion")
    ]
    category = [{
        "sample_id": "s", "category": "01_prose_sections",
        "variant": "paragraph_occlusion", "severity": "2",
        "candidate_pdf": "category.pdf",
    }]
    selected = _selected(universal, category)
    assert [row["variant"] for row in selected["s"]] == [
        "text_deletion", "block_right", "local_occlusion", "paragraph_occlusion",
    ]


def test_blind_sheets_use_four_distinct_sources_and_every_case_once() -> None:
    selected = {
        f"s{sample}": [
            {"sample_id": f"s{sample}", "variant_id": f"{sample:02x}{case:02x}"}
            for case in range(4)
        ]
        for sample in range(8)
    }
    ordered = _blind_order(selected)
    assert len(ordered) == 32
    assert len({row["variant_id"] for row in ordered}) == 32
    assert all(
        len({row["sample_id"] for row in ordered[start:start + 4]}) == 4
        for start in range(0, len(ordered), 4)
    )


def test_candidate_side_is_balanced_and_not_fixed_by_sheet_position() -> None:
    panels = [_candidate_panel(sheet, offset) for sheet in range(1, 158) for offset in range(4)]
    assert panels.count("A") == panels.count("B") == 314
    for offset in range(4):
        position = [_candidate_panel(sheet, offset) for sheet in range(1, 158)]
        assert abs(position.count("A") - position.count("B")) == 1
