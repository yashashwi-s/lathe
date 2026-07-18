#!/usr/bin/env python3
"""Compute reproducible uncertainty summaries for the held-out publication table.

Compilation is analyzed on all assigned documents. Fidelity comparisons are paired
by sample ID and conditional on both systems compiling and the named axis being
available for both. The script intentionally does not compute an overall score.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import statistics
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "results" / "publication_v0" / "per_sample_scores.csv"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "publication_v0"

EXPECTED_UNIVERSE_N = 127
BASE_SEED = 20260718
BOOTSTRAP_ITERATIONS = 10_000
CONFIDENCE_LEVEL = 0.95
TIE_TOLERANCE = 1e-6

SYSTEM_IDS = (
    "gemini_first_pass",
    "gemini_after_one_repair",
    "pandoc",
    "tylax",
    "typetex",
)
BASELINE_SYSTEM_ID = "gemini_after_one_repair"
COMPARATOR_SYSTEM_IDS = ("pandoc", "tylax", "typetex")

AXES = (
    ("strict_word_f1", "higher_is_better"),
    ("compatibility_word_f1", "higher_is_better"),
    ("matched_word_reference_coverage", "higher_is_better"),
    ("token_center_displacement_q90", "lower_is_better"),
    ("text_ltsim_page_macro", "higher_is_better"),
)

METRIC_FIELDS = (
    "strict_word_f1",
    "compatibility_word_f1",
    "number_f1",
    "operator_f1",
    "citation_f1",
    "matched_word_reference_coverage",
    "token_center_displacement_q90",
    "block_transport_combined_similarity",
    "text_ltsim_page_macro",
    "reading_order_tau",
    "style_coverage_hmean",
    "unregistered_ink_f1",
    "unregistered_ssim",
    "page_count_delta",
    "page_break_f1",
    "canvas_exact_size_rate",
)

PAIRED_FIELDS = (
    "comparison",
    "baseline_system_id",
    "comparator_system_id",
    "axis",
    "direction",
    "paired_n",
    "baseline_median",
    "comparator_median",
    "estimate",
    "ci_low",
    "ci_high",
    "wins",
    "ties",
    "losses",
    "baseline_compiled_n",
    "comparator_compiled_n",
    "common_compiled_n",
    "abstention_n",
    "tie_tolerance",
    "method",
    "seed",
    "stream_seed",
    "bootstrap_iterations",
)

CATEGORY_FIELDS = (
    "system_id",
    "display_label",
    "category",
    "universe_n",
    "compiled_n",
    "compile_rate",
    "axis",
    "direction",
    "applicable_n",
    "median",
    "population",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _reported_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _parse_bool(value: str, *, row_number: int) -> bool:
    lowered = value.strip().lower()
    if lowered not in {"true", "false"}:
        raise ValueError(
            f"row {row_number}: compiled must be True or False, got {value!r}"
        )
    return lowered == "true"


def _parse_metric(value: str, *, field: str, row_number: int) -> float | None:
    stripped = value.strip()
    if not stripped:
        return None
    try:
        number = float(stripped)
    except ValueError as error:
        raise ValueError(
            f"row {row_number}: invalid numeric value for {field}: {value!r}"
        ) from error
    if not math.isfinite(number):
        raise ValueError(
            f"row {row_number}: nonfinite value for {field}: {value!r}"
        )
    return number


def _read_and_validate(
    input_csv: Path,
    *,
    expected_universe_n: int,
) -> tuple[
    list[dict[str, Any]],
    dict[tuple[str, str], dict[str, Any]],
    list[str],
    dict[str, str],
]:
    _require(input_csv.is_file(), f"missing input table: {input_csv}")
    with input_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        _require(
            len(fieldnames) == len(set(fieldnames)),
            "input table has duplicate column names",
        )
        required = {
            "sample_id",
            "category",
            "system_id",
            "display_label",
            "compiled",
            *METRIC_FIELDS,
        }
        missing_fields = sorted(required - set(fieldnames))
        _require(
            not missing_fields,
            f"input table is missing required fields: {', '.join(missing_fields)}",
        )
        raw_rows = list(reader)

    rows: list[dict[str, Any]] = []
    index: dict[tuple[str, str], dict[str, Any]] = {}
    labels: dict[str, str] = {}
    categories_by_sample: dict[str, set[str]] = {}
    samples_by_system = {system_id: set() for system_id in SYSTEM_IDS}

    for row_number, raw in enumerate(raw_rows, start=2):
        sample_id = raw["sample_id"].strip()
        category = raw["category"].strip()
        system_id = raw["system_id"].strip()
        display_label = raw["display_label"].strip()
        _require(sample_id != "", f"row {row_number}: empty sample_id")
        _require(category != "", f"row {row_number}: empty category")
        _require(system_id in SYSTEM_IDS, f"row {row_number}: unknown system_id {system_id!r}")
        _require(display_label != "", f"row {row_number}: empty display_label")

        key = (sample_id, system_id)
        _require(key not in index, f"duplicate sample/system row: {sample_id}/{system_id}")
        compiled = _parse_bool(raw["compiled"], row_number=row_number)
        metrics = {
            field: _parse_metric(raw[field], field=field, row_number=row_number)
            for field in METRIC_FIELDS
        }
        if not compiled:
            populated = [field for field, value in metrics.items() if value is not None]
            _require(
                not populated,
                f"row {row_number}: uncompiled output has metric values: {', '.join(populated)}",
            )

        row: dict[str, Any] = {
            "sample_id": sample_id,
            "category": category,
            "system_id": system_id,
            "display_label": display_label,
            "compiled": compiled,
            **metrics,
        }
        rows.append(row)
        index[key] = row
        samples_by_system[system_id].add(sample_id)
        categories_by_sample.setdefault(sample_id, set()).add(category)
        if system_id in labels:
            _require(
                labels[system_id] == display_label,
                f"inconsistent display_label for {system_id}",
            )
        else:
            labels[system_id] = display_label

    all_samples = sorted({row["sample_id"] for row in rows})
    _require(
        len(all_samples) == expected_universe_n,
        f"expected {expected_universe_n} unique samples, found {len(all_samples)}",
    )
    expected_sample_set = set(all_samples)
    for system_id in SYSTEM_IDS:
        system_samples = samples_by_system[system_id]
        missing = sorted(expected_sample_set - system_samples)
        extra = sorted(system_samples - expected_sample_set)
        _require(
            not missing and not extra,
            f"incomplete sample/system matrix for {system_id}: "
            f"missing={missing[:5]}, extra={extra[:5]}",
        )
    expected_rows = expected_universe_n * len(SYSTEM_IDS)
    _require(
        len(rows) == expected_rows,
        f"expected {expected_rows} sample/system rows, found {len(rows)}",
    )
    for sample_id, categories in categories_by_sample.items():
        _require(
            len(categories) == 1,
            f"inconsistent category for sample {sample_id}: {sorted(categories)}",
        )

    return rows, index, all_samples, labels


def _round(value: float | None) -> float | None:
    return None if value is None else round(value, 6)


def _percentile(sorted_values: Sequence[float], probability: float) -> float:
    _require(bool(sorted_values), "cannot compute a percentile of an empty series")
    position = (len(sorted_values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    weight = position - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def _stream_seed(label: str, base_seed: int) -> int:
    digest = hashlib.sha256(f"{base_seed}:{label}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def _bootstrap_interval(
    values: Sequence[float],
    statistic: Callable[[Iterable[float]], float],
    *,
    label: str,
    base_seed: int,
    iterations: int,
) -> tuple[float, float, int]:
    _require(bool(values), f"cannot bootstrap an empty series: {label}")
    _require(iterations > 0, "bootstrap_iterations must be positive")
    stream_seed = _stream_seed(label, base_seed)
    rng = random.Random(stream_seed)
    count = len(values)
    estimates = [
        statistic(values[rng.randrange(count)] for _ in range(count))
        for _ in range(iterations)
    ]
    estimates.sort()
    alpha = (1 - CONFIDENCE_LEVEL) / 2
    return (
        _percentile(estimates, alpha),
        _percentile(estimates, 1 - alpha),
        stream_seed,
    )


def _mean(values: Iterable[float]) -> float:
    materialized = list(values)
    return sum(materialized) / len(materialized)


def _median(values: Iterable[float]) -> float:
    return statistics.median(values)


def _compile_rate_results(
    index: dict[tuple[str, str], dict[str, Any]],
    sample_ids: Sequence[str],
    labels: dict[str, str],
    *,
    seed: int,
    iterations: int,
) -> list[dict[str, Any]]:
    results = []
    for system_id in SYSTEM_IDS:
        values = [
            float(index[(sample_id, system_id)]["compiled"])
            for sample_id in sample_ids
        ]
        low, high, stream_seed = _bootstrap_interval(
            values,
            _mean,
            label=f"compile_rate:{system_id}",
            base_seed=seed,
            iterations=iterations,
        )
        compiled_n = int(sum(values))
        results.append(
            {
                "system_id": system_id,
                "display_label": labels[system_id],
                "universe_n": len(values),
                "compiled_n": compiled_n,
                "failed_n": len(values) - compiled_n,
                "estimate": _round(compiled_n / len(values)),
                "ci_low": _round(low),
                "ci_high": _round(high),
                "confidence_level": CONFIDENCE_LEVEL,
                "method": "document bootstrap of compile-rate mean; percentile 95% CI",
                "seed": seed,
                "stream_seed": stream_seed,
                "bootstrap_iterations": iterations,
            }
        )
    return results


def _paired_axis_results(
    index: dict[tuple[str, str], dict[str, Any]],
    sample_ids: Sequence[str],
    labels: dict[str, str],
    *,
    seed: int,
    iterations: int,
    tie_tolerance: float,
) -> list[dict[str, Any]]:
    results = []
    baseline_compiled_n = sum(
        index[(sample_id, BASELINE_SYSTEM_ID)]["compiled"] for sample_id in sample_ids
    )
    for comparator_id in COMPARATOR_SYSTEM_IDS:
        comparator_compiled_n = sum(
            index[(sample_id, comparator_id)]["compiled"] for sample_id in sample_ids
        )
        common_sample_ids = [
            sample_id
            for sample_id in sample_ids
            if index[(sample_id, BASELINE_SYSTEM_ID)]["compiled"]
            and index[(sample_id, comparator_id)]["compiled"]
        ]
        comparison = f"{labels[BASELINE_SYSTEM_ID]} vs {labels[comparator_id]}"
        for axis, direction in AXES:
            pairs = [
                (
                    index[(sample_id, BASELINE_SYSTEM_ID)][axis],
                    index[(sample_id, comparator_id)][axis],
                )
                for sample_id in common_sample_ids
                if index[(sample_id, BASELINE_SYSTEM_ID)][axis] is not None
                and index[(sample_id, comparator_id)][axis] is not None
            ]
            differences = [
                baseline - comparator
                if direction == "higher_is_better"
                else comparator - baseline
                for baseline, comparator in pairs
            ]
            _require(
                bool(differences),
                f"no paired non-abstained observations for {comparator_id}/{axis}",
            )
            low, high, stream_seed = _bootstrap_interval(
                differences,
                _median,
                label=f"paired_median:{BASELINE_SYSTEM_ID}:{comparator_id}:{axis}",
                base_seed=seed,
                iterations=iterations,
            )
            wins = sum(value > tie_tolerance for value in differences)
            losses = sum(value < -tie_tolerance for value in differences)
            ties = len(differences) - wins - losses
            results.append(
                {
                    "comparison": comparison,
                    "baseline_system_id": BASELINE_SYSTEM_ID,
                    "comparator_system_id": comparator_id,
                    "axis": axis,
                    "direction": direction,
                    "paired_n": len(pairs),
                    "baseline_median": _round(_median(pair[0] for pair in pairs)),
                    "comparator_median": _round(_median(pair[1] for pair in pairs)),
                    "estimate": _round(_median(differences)),
                    "ci_low": _round(low),
                    "ci_high": _round(high),
                    "wins": wins,
                    "ties": ties,
                    "losses": losses,
                    "baseline_compiled_n": baseline_compiled_n,
                    "comparator_compiled_n": comparator_compiled_n,
                    "common_compiled_n": len(common_sample_ids),
                    "abstention_n": len(common_sample_ids) - len(pairs),
                    "tie_tolerance": tie_tolerance,
                    "method": "paired document bootstrap of median oriented differences; percentile 95% CI",
                    "seed": seed,
                    "stream_seed": stream_seed,
                    "bootstrap_iterations": iterations,
                }
            )
    return results


def _category_results(
    rows: Sequence[dict[str, Any]], labels: dict[str, str]
) -> list[dict[str, Any]]:
    categories = sorted({row["category"] for row in rows})
    results = []
    for system_id in SYSTEM_IDS:
        for category in categories:
            subset = [
                row
                for row in rows
                if row["system_id"] == system_id and row["category"] == category
            ]
            compiled = [row for row in subset if row["compiled"]]
            common = {
                "system_id": system_id,
                "display_label": labels[system_id],
                "category": category,
                "universe_n": len(subset),
                "compiled_n": len(compiled),
                "compile_rate": _round(len(compiled) / len(subset)),
            }
            results.append(
                {
                    **common,
                    "axis": "compile_rate",
                    "direction": "higher_is_better",
                    "applicable_n": len(subset),
                    "median": None,
                    "population": "all assigned documents",
                }
            )
            for axis, direction in AXES:
                values = [row[axis] for row in compiled if row[axis] is not None]
                results.append(
                    {
                        **common,
                        "axis": axis,
                        "direction": direction,
                        "applicable_n": len(values),
                        "median": _round(_median(values)) if values else None,
                        "population": "compiled PDFs with non-abstained axis",
                    }
                )
    return results


def _write_csv(
    path: Path,
    rows: Sequence[dict[str, Any]],
    fields: Sequence[str],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            {
                field: "" if row.get(field) is None else row.get(field, "")
                for field in fields
            }
            for row in rows
        )


def analyze(
    input_csv: Path = DEFAULT_INPUT,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    *,
    expected_universe_n: int = EXPECTED_UNIVERSE_N,
    seed: int = BASE_SEED,
    bootstrap_iterations: int = BOOTSTRAP_ITERATIONS,
    tie_tolerance: float = TIE_TOLERANCE,
) -> dict[str, Any]:
    """Validate the primary matrix, write statistics artifacts, and return the JSON."""

    _require(expected_universe_n > 0, "expected_universe_n must be positive")
    _require(tie_tolerance >= 0, "tie_tolerance must be nonnegative")
    rows, index, sample_ids, labels = _read_and_validate(
        input_csv, expected_universe_n=expected_universe_n
    )
    compile_results = _compile_rate_results(
        index,
        sample_ids,
        labels,
        seed=seed,
        iterations=bootstrap_iterations,
    )
    paired_results = _paired_axis_results(
        index,
        sample_ids,
        labels,
        seed=seed,
        iterations=bootstrap_iterations,
        tie_tolerance=tie_tolerance,
    )
    category_results = _category_results(rows, labels)

    output_dir.mkdir(parents=True, exist_ok=True)
    paired_path = output_dir / "paired_axis_results.csv"
    category_path = output_dir / "category_results.csv"
    json_path = output_dir / "publication_statistics.json"
    _write_csv(paired_path, paired_results, PAIRED_FIELDS)
    _write_csv(category_path, category_results, CATEGORY_FIELDS)

    sample_digest = hashlib.sha256(
        json.dumps(sample_ids, separators=(",", ":")).encode()
    ).hexdigest()
    document = {
        "schema_version": "publication_statistics_v0.1",
        "analysis": {
            "source": _reported_path(input_csv),
            "source_sha256_raw_bytes": _sha256(input_csv),
            "universe_n": len(sample_ids),
            "sample_id_set_sha256": sample_digest,
            "system_order": list(SYSTEM_IDS),
            "baseline_system_id": BASELINE_SYSTEM_ID,
            "comparator_system_ids": list(COMPARATOR_SYSTEM_IDS),
            "axes": [
                {"axis": axis, "direction": direction}
                for axis, direction in AXES
            ],
            "overall_scalar_score": None,
        },
        "bootstrap": {
            "unit": "document/sample ID",
            "confidence_level": CONFIDENCE_LEVEL,
            "interval": "percentile",
            "seed": seed,
            "iterations": bootstrap_iterations,
            "tie_tolerance": tie_tolerance,
            "stream_seeds": "SHA-256-derived from base seed and analysis-series label",
        },
        "compile_rate_results": compile_results,
        "paired_axis_results": paired_results,
        "category_results": category_results,
        "guardrails": [
            "No overall scalar score or cross-axis rank is computed.",
            "Compile-rate denominators contain all assigned held-out documents, including failures.",
            "Fidelity effects use the same sample IDs for both systems and exclude only compile failures or named-axis abstentions.",
            "A positive paired estimate always favors the Gemini post-repair baseline; lower-is-better axes are sign-oriented accordingly.",
            "Category rows are descriptive coverage and medians, not multiplicity-adjusted inferential claims.",
        ],
        "artifacts": {
            "paired_axis_results": {
                "path": _reported_path(paired_path),
                "sha256_raw_bytes": _sha256(paired_path),
            },
            "category_results": {
                "path": _reported_path(category_path),
                "sha256_raw_bytes": _sha256(category_path),
            },
        },
    }
    json_path.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return document


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    document = analyze(args.input, args.output_dir)
    summary = {
        "status": "ok",
        "universe_n": document["analysis"]["universe_n"],
        "compile_rate_rows": len(document["compile_rate_results"]),
        "paired_axis_rows": len(document["paired_axis_results"]),
        "category_rows": len(document["category_results"]),
        "overall_scalar_score": None,
    }
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
