from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from merge_metric_batches_v1 import merge_batches  # noqa: E402


FIELDS = ["sample_id", "category", "family", "variant", "severity", "variant_id",
          "status", "applicable", "candidate_pdf"]


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _row(sample: str, variant_id: str) -> dict[str, str]:
    return {"sample_id": sample, "category": "c", "family": "f", "variant": "v",
            "severity": "1", "variant_id": variant_id, "status": "applied",
            "applicable": "true", "candidate_pdf": ""}


def test_merge_requires_exact_case_and_sample_coverage(tmp_path: Path) -> None:
    first, second = tmp_path / "a.csv", tmp_path / "b.csv"
    _write(first, [_row("a", "1")])
    _write(second, [_row("b", "2")])
    fields, rows, summary = merge_batches([first, second], {"a", "b"}, 2)
    assert fields == FIELDS
    assert [row["sample_id"] for row in rows] == ["a", "b"]
    assert summary["unique_variant_ids"] == 2


def test_merge_rejects_duplicate_variant_ids(tmp_path: Path) -> None:
    first, second = tmp_path / "a.csv", tmp_path / "b.csv"
    _write(first, [_row("a", "1")])
    _write(second, [_row("b", "1")])
    with pytest.raises(ValueError, match="duplicate variant_id"):
        merge_batches([first, second], {"a", "b"}, 2)
