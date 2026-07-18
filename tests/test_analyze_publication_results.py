from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.evaluation.analyze_publication_results import (
    AXES,
    METRIC_FIELDS,
    SYSTEM_IDS,
    analyze,
)


FIELDS = (
    "sample_id",
    "category",
    "system_id",
    "display_label",
    "compiled",
    *METRIC_FIELDS,
)


def _rows() -> list[dict[str, str]]:
    labels = {
        "gemini_first_pass": "Gemini first pass",
        "gemini_after_one_repair": "Gemini after one repair",
        "pandoc": "Pandoc",
        "tylax": "Tylax",
        "typetex": "TypeTeX",
    }
    rows = []
    for sample_id, category in (("a", "cat_1"), ("b", "cat_1"), ("c", "cat_2")):
        for system_id in SYSTEM_IDS:
            compiled = not (
                (system_id == "gemini_first_pass" and sample_id in {"b", "c"})
                or (system_id == "gemini_after_one_repair" and sample_id == "c")
                or (system_id == "tylax" and sample_id == "c")
            )
            row = {field: "" for field in FIELDS}
            row.update(
                sample_id=sample_id,
                category=category,
                system_id=system_id,
                display_label=labels[system_id],
                compiled=str(compiled),
            )
            if compiled:
                baseline_value = {"a": 0.8, "b": 0.5, "c": 0.4}[sample_id]
                center_value = {"a": 0.1, "b": 0.3, "c": 0.4}[sample_id]
                if system_id == "gemini_after_one_repair":
                    value = baseline_value
                    center = center_value
                elif system_id in {"pandoc", "tylax", "typetex"}:
                    value = {"a": 0.7, "b": 0.5, "c": 0.6}[sample_id]
                    center = {"a": 0.2, "b": 0.2, "c": 0.5}[sample_id]
                else:
                    value = baseline_value - 0.05
                    center = center_value + 0.05
                for axis, _ in AXES:
                    row[axis] = str(
                        center if axis == "token_center_displacement_q90" else value
                    )
            rows.append(row)
    return rows


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_paired_direction_compile_denominator_and_categories(tmp_path: Path) -> None:
    source = tmp_path / "per_sample_scores.csv"
    _write(source, _rows())
    output = tmp_path / "output"

    document = analyze(
        source,
        output,
        expected_universe_n=3,
        bootstrap_iterations=200,
    )

    assert document["analysis"]["overall_scalar_score"] is None
    compile_by_system = {
        row["system_id"]: row for row in document["compile_rate_results"]
    }
    assert compile_by_system["gemini_after_one_repair"]["compiled_n"] == 2
    assert compile_by_system["gemini_after_one_repair"]["failed_n"] == 1
    assert compile_by_system["gemini_after_one_repair"]["universe_n"] == 3

    paired = _read(output / "paired_axis_results.csv")
    strict = next(
        row
        for row in paired
        if row["comparator_system_id"] == "pandoc"
        and row["axis"] == "strict_word_f1"
    )
    assert strict["paired_n"] == "2"
    assert strict["common_compiled_n"] == "2"
    assert strict["abstention_n"] == "0"
    assert strict["estimate"] == "0.05"
    assert (strict["wins"], strict["ties"], strict["losses"]) == ("1", "1", "0")

    displacement = next(
        row
        for row in paired
        if row["comparator_system_id"] == "pandoc"
        and row["axis"] == "token_center_displacement_q90"
    )
    assert displacement["direction"] == "lower_is_better"
    assert displacement["estimate"] == "0.0"
    assert (displacement["wins"], displacement["ties"], displacement["losses"]) == (
        "1",
        "0",
        "1",
    )

    categories = _read(output / "category_results.csv")
    cat_2_compile = next(
        row
        for row in categories
        if row["system_id"] == "gemini_after_one_repair"
        and row["category"] == "cat_2"
        and row["axis"] == "compile_rate"
    )
    assert cat_2_compile["universe_n"] == "1"
    assert cat_2_compile["compiled_n"] == "0"
    assert cat_2_compile["compile_rate"] == "0.0"
    cat_2_strict = next(
        row
        for row in categories
        if row["system_id"] == "gemini_after_one_repair"
        and row["category"] == "cat_2"
        and row["axis"] == "strict_word_f1"
    )
    assert cat_2_strict["applicable_n"] == "0"
    assert cat_2_strict["median"] == ""


def test_axis_abstention_is_removed_only_from_that_pair(tmp_path: Path) -> None:
    rows = _rows()
    target = next(
        row
        for row in rows
        if row["sample_id"] == "b" and row["system_id"] == "pandoc"
    )
    target["strict_word_f1"] = ""
    source = tmp_path / "scores.csv"
    _write(source, rows)

    analyze(source, tmp_path / "out", expected_universe_n=3, bootstrap_iterations=50)
    paired = _read(tmp_path / "out" / "paired_axis_results.csv")
    strict = next(
        row
        for row in paired
        if row["comparator_system_id"] == "pandoc"
        and row["axis"] == "strict_word_f1"
    )
    compatibility = next(
        row
        for row in paired
        if row["comparator_system_id"] == "pandoc"
        and row["axis"] == "compatibility_word_f1"
    )
    assert (strict["common_compiled_n"], strict["paired_n"], strict["abstention_n"]) == (
        "2",
        "1",
        "1",
    )
    assert compatibility["paired_n"] == "2"


def test_regeneration_is_byte_identical(tmp_path: Path) -> None:
    source = tmp_path / "scores.csv"
    _write(source, _rows())
    output = tmp_path / "out"
    names = (
        "publication_statistics.json",
        "paired_axis_results.csv",
        "category_results.csv",
    )

    analyze(source, output, expected_universe_n=3, bootstrap_iterations=100)
    first = {name: (output / name).read_bytes() for name in names}
    analyze(source, output, expected_universe_n=3, bootstrap_iterations=100)
    second = {name: (output / name).read_bytes() for name in names}

    assert second == first


@pytest.mark.parametrize("failure", ["duplicate", "missing", "nonfinite"])
def test_invalid_primary_matrix_fails_closed(tmp_path: Path, failure: str) -> None:
    rows = _rows()
    if failure == "duplicate":
        rows.append(dict(rows[0]))
        match = "duplicate sample/system row"
    elif failure == "missing":
        rows.pop()
        match = "incomplete sample/system matrix"
    else:
        target = next(row for row in rows if row["compiled"] == "True")
        target["strict_word_f1"] = "nan"
        match = "nonfinite value"
    source = tmp_path / "scores.csv"
    _write(source, rows)
    output = tmp_path / "out"

    with pytest.raises(ValueError, match=match):
        analyze(source, output, expected_universe_n=3, bootstrap_iterations=10)

    assert not output.exists()
