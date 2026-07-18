#!/usr/bin/env python3
"""Build the readable benchmark manuscript from frozen publication artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "results" / "publication_v0"
DEFAULT_OUTPUT = ROOT / "reports" / "benchmark_paper_blog.md"

PRIMARY_FILES = ("scorecard.json", "scorecard.csv", "per_sample_scores.csv")
STATISTICS_FILES = (
    "publication_statistics.json",
    "paired_axis_results.csv",
    "category_results.csv",
)
SYSTEM_IDS = (
    "gemini_first_pass",
    "gemini_after_one_repair",
    "pandoc",
    "tylax",
    "typetex",
)
SCORECARD_FIELDS = (
    "system_id",
    "display_label",
    "protocol_id",
    "protocol_label",
    "candidate_stage",
    "universe_n",
    "compiled_n",
    "compile_rate",
    "page_exact_n",
    "page_exact_rate_all",
    "canvas_exact_n",
    "canvas_exact_rate_compiled",
    "strict_word_f1_median",
    "compatibility_word_f1_median",
    "reference_coverage_median",
    "center_displacement_q90_median",
    "text_ltsim_median",
    "ssim_eligible_n",
    "ssim_median",
    "fidelity_population",
    "candidate_set_sha256",
)
PER_SAMPLE_FIELDS = (
    "sample_id",
    "category",
    "system_id",
    "display_label",
    "protocol_id",
    "candidate_stage",
    "compiled",
    "compile_status",
    "compile_failure_class",
    "reference_pdf",
    "reference_sha256",
    "candidate_pdf",
    "candidate_sha256",
    "metric_source_csv",
    "metric_source_evidence_json",
    "metric_v2_status",
    "strict_word_f1",
    "compatibility_word_f1",
    "matched_word_reference_coverage",
    "token_center_displacement_q90",
    "text_ltsim_page_macro",
    "unregistered_ssim",
    "page_count_delta",
    "canvas_exact_size_rate",
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"{path.name}: expected at least one data row")
    return rows


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name}: expected a JSON object")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _finite(value: Any, *, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field}: expected a number, found {value!r}") from error
    if not math.isfinite(number):
        raise ValueError(f"{field}: non-finite value {value!r}")
    return number


def _optional_number(value: Any, *, field: str) -> float | None:
    return None if value in (None, "") else _finite(value, field=field)


def _bool(value: Any, *, field: str) -> bool:
    normalized = str(value).strip().lower()
    if normalized not in {"true", "false"}:
        raise ValueError(f"{field}: expected true or false, found {value!r}")
    return normalized == "true"


def _same_value(left: Any, right: Any, *, field: str) -> bool:
    if left in (None, "") and right in (None, ""):
        return True
    if field.endswith(("_n", "_rate", "_median")):
        return math.isclose(
            _finite(left, field=field), _finite(right, field=field), rel_tol=1e-12, abs_tol=1e-12
        )
    return str(left).strip() == str(right).strip()


def _validate_artifact_hash(document: Mapping[str, Any], key: str, path: Path) -> None:
    record = document.get("artifacts", {}).get(key)
    _require(isinstance(record, Mapping), f"scorecard.json: missing artifacts.{key}")
    _require(Path(str(record.get("path", ""))).name == path.name, f"artifacts.{key}: wrong path")
    _require(
        record.get("sha256_raw_bytes") == _sha256(path),
        f"artifacts.{key}: stale SHA-256 for {path.name}",
    )


def _median(rows: Sequence[Mapping[str, str]], field: str) -> float | None:
    values = [
        value
        for row in rows
        if (value := _optional_number(row.get(field), field=field)) is not None
    ]
    return round(statistics.median(values), 6) if values else None


def _validate_primary(
    document: dict[str, Any],
    scorecard_csv: list[dict[str, str]],
    per_sample: list[dict[str, str]],
    input_dir: Path,
) -> None:
    required_keys = {"schema_version", "benchmark", "provenance", "validation", "artifacts", "scorecard"}
    _require(required_keys <= set(document), "scorecard.json: missing required top-level keys")
    _require(document["schema_version"] == "publication_scorecard_v0.1", "unsupported scorecard schema")
    benchmark = document["benchmark"]
    validation = document["validation"]
    provenance = document["provenance"]
    _require(isinstance(benchmark, Mapping), "scorecard.json: benchmark must be an object")
    _require(isinstance(validation, Mapping), "scorecard.json: validation must be an object")
    _require(isinstance(provenance, Mapping), "scorecard.json: provenance must be an object")
    _require(benchmark.get("overall_scalar_score") is None, "publication must not define an overall scalar")
    _require(provenance.get("metric", {}).get("aggregate_score") is None, "metric aggregate must be null")
    gemini = provenance.get("gemini", {})
    _require(gemini.get("temperature") == 0, "primary model temperature is not frozen at zero")
    _require(gemini.get("max_repairs") == 1, "primary protocol must allow exactly one repair")
    _require(gemini.get("source_only") is True, "primary model protocol is not source-only")
    _require(gemini.get("reference_images_supplied") is False, "reference images entered the primary protocol")
    _require(validation.get("prompt_dev_overlap_n") == 0, "prompt-development leakage is nonzero")
    _require(validation.get("adaptive_v0_v2_v3_rows_used") == 0, "adaptive rows entered primary data")
    _require(validation.get("claude_rows_used") == 0, "Claude rows entered primary data")
    _require(validation.get("metric_rows_cover_every_compiled_pdf") is True, "metric coverage gate failed")
    _require(validation.get("failed_outputs_have_empty_fidelity_axes") is True, "failure abstention gate failed")

    json_rows = document["scorecard"]
    _require(isinstance(json_rows, list), "scorecard.json: scorecard must be a list")
    _require([row.get("system_id") for row in json_rows] == list(SYSTEM_IDS), "unexpected primary systems/order")
    _require([row.get("system_id") for row in scorecard_csv] == list(SYSTEM_IDS), "scorecard.csv systems/order differ")
    _require(len(json_rows) == len(scorecard_csv), "scorecard CSV/JSON row counts differ")
    for index, (json_row, csv_row) in enumerate(zip(json_rows, scorecard_csv)):
        missing = [field for field in SCORECARD_FIELDS if field not in json_row or field not in csv_row]
        _require(not missing, f"scorecard row {index}: missing fields {missing}")
        for field in SCORECARD_FIELDS:
            _require(
                _same_value(json_row.get(field), csv_row.get(field), field=field),
                f"scorecard CSV/JSON mismatch at row {index}, field {field}",
            )

    missing_per_sample = [field for field in PER_SAMPLE_FIELDS if field not in per_sample[0]]
    _require(not missing_per_sample, f"per_sample_scores.csv: missing fields {missing_per_sample}")
    universe_n = int(_finite(benchmark.get("universe_n"), field="benchmark.universe_n"))
    _require(len(per_sample) == universe_n * len(json_rows), "per-sample table does not cover every system/reference")

    for summary in json_rows:
        system = summary["system_id"]
        rows = [row for row in per_sample if row["system_id"] == system]
        _require(len(rows) == universe_n, f"{system}: wrong per-sample row count")
        _require(len({row["sample_id"] for row in rows}) == universe_n, f"{system}: duplicate sample IDs")
        _require(all(row["display_label"] == summary["display_label"] for row in rows), f"{system}: label drift")
        _require(all(row["protocol_id"] == summary["protocol_id"] for row in rows), f"{system}: protocol drift")
        compiled = [row for row in rows if _bool(row["compiled"], field=f"{system}.compiled")]
        uncompiled = [row for row in rows if row not in compiled]
        _require(int(summary["universe_n"]) == universe_n, f"{system}: universe count mismatch")
        _require(len(compiled) == int(summary["compiled_n"]), f"{system}: compiled count mismatch")
        _require(
            math.isclose(float(summary["compile_rate"]), len(compiled) / universe_n, abs_tol=1e-6),
            f"{system}: stale compile rate",
        )
        _require(all(row["candidate_pdf"] and row["candidate_sha256"] for row in compiled), f"{system}: compiled artifact missing")
        _require(
            all(not row["candidate_pdf"] and row["metric_v2_status"] == "not_scored_uncompiled" for row in uncompiled),
            f"{system}: failed output has a candidate or metric score",
        )
        expected = {
            "page_exact_n": sum(_optional_number(row["page_count_delta"], field="page_count_delta") == 0 for row in compiled),
            "canvas_exact_n": sum(_optional_number(row["canvas_exact_size_rate"], field="canvas_exact_size_rate") == 1 for row in compiled),
            "strict_word_f1_median": _median(compiled, "strict_word_f1"),
            "compatibility_word_f1_median": _median(compiled, "compatibility_word_f1"),
            "reference_coverage_median": _median(compiled, "matched_word_reference_coverage"),
            "center_displacement_q90_median": _median(compiled, "token_center_displacement_q90"),
            "text_ltsim_median": _median(compiled, "text_ltsim_page_macro"),
            "ssim_eligible_n": sum(bool(row["unregistered_ssim"]) for row in compiled),
            "ssim_median": _median(compiled, "unregistered_ssim"),
        }
        for field, value in expected.items():
            _require(_same_value(summary.get(field), value, field=field), f"{system}: stale aggregate {field}")
        _require(
            math.isclose(float(summary["page_exact_rate_all"]), expected["page_exact_n"] / universe_n, abs_tol=1e-6),
            f"{system}: stale exact-page rate",
        )
        expected_canvas_rate = round(expected["canvas_exact_n"] / len(compiled), 6) if compiled else None
        _require(
            _same_value(summary["canvas_exact_rate_compiled"], expected_canvas_rate, field="canvas_exact_rate_compiled"),
            f"{system}: stale exact-canvas rate",
        )

    actual_counts = {row["system_id"]: int(row["compiled_n"]) for row in json_rows}
    _require(validation.get("actual_compiled_n") == actual_counts, "validation compile counts are stale")
    _require(
        validation.get("first_pass_compiled_n") == actual_counts["gemini_first_pass"],
        "first-pass validation count is stale",
    )
    _require(
        validation.get("after_one_repair_compiled_n") == actual_counts["gemini_after_one_repair"],
        "post-repair validation count is stale",
    )
    _require(
        validation.get("repair_success_n")
        == actual_counts["gemini_after_one_repair"] - actual_counts["gemini_first_pass"],
        "repair-success validation count is stale",
    )
    _validate_artifact_hash(document, "per_sample_scores", input_dir / "per_sample_scores.csv")
    _validate_artifact_hash(document, "scorecard_csv", input_dir / "scorecard.csv")


def load_publication(input_dir: Path) -> tuple[dict[str, Any], list[dict[str, str]], dict[str, Any] | None]:
    missing = [name for name in PRIMARY_FILES if not (input_dir / name).is_file()]
    _require(not missing, f"missing required publication files: {', '.join(missing)}")
    present_statistics = [name for name in STATISTICS_FILES if (input_dir / name).is_file()]
    _require(
        not present_statistics or len(present_statistics) == len(STATISTICS_FILES),
        "publication statistics are partial; require JSON, paired-axis CSV, and category CSV together",
    )
    document = _read_json(input_dir / "scorecard.json")
    scorecard_csv = _read_csv(input_dir / "scorecard.csv")
    per_sample = _read_csv(input_dir / "per_sample_scores.csv")
    _validate_primary(document, scorecard_csv, per_sample, input_dir)
    statistics_document = _read_json(input_dir / "publication_statistics.json") if present_statistics else None
    if statistics_document is not None:
        statistics_document = {
            **statistics_document,
            "paired_axis_rows": _read_csv(input_dir / "paired_axis_results.csv"),
            "category_rows": _read_csv(input_dir / "category_results.csv"),
        }
    return document, per_sample, statistics_document


def _percent(value: Any) -> str:
    return f"{100 * _finite(value, field='rate'):.1f}%"


def _metric(value: Any) -> str:
    return "abstain" if value in (None, "") else f"{_finite(value, field='metric'):.3f}"


def _escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def _failure_summary(rows: Sequence[Mapping[str, str]]) -> str:
    failures = Counter(
        (_escape(row.get("compile_failure_class")) or "unclassified failure")
        for row in rows
        if str(row.get("compiled", "")).lower() == "false"
    )
    return "; ".join(f"{label}: {count}" for label, count in failures.most_common()) or "none"


def _render_statistics(statistics_document: dict[str, Any] | None) -> list[str]:
    if statistics_document is None:
        return [
            "## Paired uncertainty",
            "",
            "No paired interval is emitted in this release because the complete publication-statistics artifact set is absent.",
        ]
    schema = statistics_document.get("schema_version")
    rows = statistics_document["paired_axis_rows"]
    required = {"comparison", "axis", "paired_n", "estimate", "ci_low", "ci_high", "method"}
    _require(schema is not None, "publication_statistics.json: missing schema_version")
    _require(required <= set(rows[0]), "paired_axis_results.csv: unsupported schema")
    lines = [
        "## Paired uncertainty",
        "",
        "These comparisons use only reference IDs eligible for both systems on the named axis. Intervals are paired; they do not repair missing outputs or turn the vector into a rank.",
        "",
        "| Comparison | Axis | Paired n | Estimate | Interval | Method |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {_escape(row['comparison'])} | {_escape(row['axis'])} | {int(_finite(row['paired_n'], field='paired_n'))} "
            f"| {_metric(row['estimate'])} | [{_metric(row['ci_low'])}, {_metric(row['ci_high'])}] | {_escape(row['method'])} |"
        )
    return lines


def render_manuscript(
    document: dict[str, Any],
    per_sample: list[dict[str, str]],
    statistics_document: dict[str, Any] | None,
) -> str:
    benchmark = document["benchmark"]
    provenance = document["provenance"]
    validation = document["validation"]
    scorecard = document["scorecard"]
    universe = int(benchmark["universe_n"])
    gemini = provenance["gemini"]
    metric = provenance["metric"]
    model_routes = ", ".join(gemini["resolved_model_routes"] or gemini["requested_model_routes"])
    lines = [
        "<!-- Generated by scripts/evaluation/build_publication_manuscript.py. Do not hand-edit numeric claims. -->",
        "# Measuring source-only LaTeX-to-Typst conversion",
        "",
        "Lathe evaluates a conversion as an auditable chain: assigned source, conversion and compile outcome, rendered PDF, metric evidence, and abstention reason. It deliberately does not publish a universal grade.",
        "",
        "## Task and data",
        "",
        f"The primary study is **{_escape(benchmark['name'])}**. It assigns **{universe}** held-out LaTeX references from `{_escape(benchmark['split'])}` to every primary system. The task is source-only conversion: a system receives LaTeX and must return Typst; the reference rendering is evaluation evidence, not model input.",
        "",
        f"Prompt-development overlap is **{validation['prompt_dev_overlap_n']}** references. Compilation uses {_escape(benchmark['compile_denominator'])}; fidelity uses {_escape(benchmark['fidelity_population'])}.",
        "",
        "## Frozen primary protocol",
        "",
        f"The recorded model route is `{_escape(model_routes)}`. The run uses temperature **{gemini['temperature']}**, Typst **{_escape(gemini['typst_version'])}**, and at most **{gemini['max_repairs']}** compiler-error repair. Reference images supplied: **{str(gemini['reference_images_supplied']).lower()}**. First-pass and post-repair results are separate rows so repair credit is visible.",
        "",
        f"The model identity limit is explicit: {_escape(gemini['model_identity_limit'])}. Deterministic engines are scored from their archived as-tested outputs; their executable versions were not recorded.",
        "",
        "## Metric vector and abstentions",
        "",
        f"The evaluator is `{_escape(metric['evaluator'])}` at **{metric['render_dpi']} DPI**. It reports transport, content, geometry, Text-LTSim, reading order, pagination, canvas, typography/ink, and eligible raster evidence independently.",
        "",
        "Strict text F1 preserves exact Unicode distinctions; compatibility text F1 exposes normalization-only differences. Exact number, operator, and citation inventories make critical token changes inspectable. Reference coverage and token-center displacement describe retained text and its movement. Text-LTSim is computed only on eligible page text. SSIM abstains when physical canvases or raster grids are incompatible. Empty fidelity cells for uncompiled outputs are abstentions, never zero-valued visual judgments.",
        "",
        "## Primary scorecard",
        "",
        "Full-denominator outcomes and compiled-only fidelity are kept in separate columns. Higher is better except center displacement.",
        "",
        f"| System | Compiled / {universe} | Exact pages / {universe} | Exact canvas / compiled | Strict F1 | Compat. F1 | Ref. coverage | Center q90 ↓ | Text-LTSim | SSIM (eligible n) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in scorecard:
        lines.append(
            f"| {_escape(row['display_label'])} | {row['compiled_n']}/{row['universe_n']} ({_percent(row['compile_rate'])}) "
            f"| {row['page_exact_n']}/{row['universe_n']} | {row['canvas_exact_n']}/{row['compiled_n']} "
            f"| {_metric(row['strict_word_f1_median'])} | {_metric(row['compatibility_word_f1_median'])} "
            f"| {_metric(row['reference_coverage_median'])} | {_metric(row['center_displacement_q90_median'])} "
            f"| {_metric(row['text_ltsim_median'])} | {_metric(row['ssim_median'])} ({row['ssim_eligible_n']}) |"
        )
    lines.extend([
        "",
        "Conditional medians answer, ‘when this system produced a PDF, what evidence did that PDF show?’ They are not a fair paired ranking because each system can compile a different subset. Compile rate remains the non-negotiable coverage result.",
        "",
        "## Repair and compilation failures",
        "",
        f"The frozen model run compiled **{validation['first_pass_compiled_n']}** references on its first pass. A repair was attempted for **{validation['repair_attempted_n']}** references and succeeded for **{validation['repair_success_n']}**; cumulative compiled coverage after the allowed repair is **{validation['after_one_repair_compiled_n']}**.",
        "",
        "| System | Failed | Recorded failure classes |",
        "|---|---:|---|",
    ])
    for row in scorecard:
        rows = [item for item in per_sample if item["system_id"] == row["system_id"]]
        lines.append(
            f"| {_escape(row['display_label'])} | {int(row['universe_n']) - int(row['compiled_n'])} | {_failure_summary(rows)} |"
        )
    lines.extend(["", *_render_statistics(statistics_document), ""])
    lines.extend([
        "## Exploratory evidence kept outside the primary table",
        "",
        f"Adaptive prompt-cascade rows used in the primary table: **{validation['adaptive_v0_v2_v3_rows_used']}**. Claude-overlap rows used: **{validation['claude_rows_used']}**. This exclusion is methodological, not cosmetic.",
        "",
        "The adaptive cascade changes prompts after failure patterns are observed, so it measures recoverability and prompt debugging rather than one frozen protocol. The available Claude overlap was collected under heterogeneous protocols and is suitable for labeled visual case studies only; it cannot support a fair model leaderboard.",
        "",
        "## Controlled metric evidence",
        "",
        "Source-known mutations test metric mechanics: identity, deletion, wrong critical tokens, translation, typography changes, obstruction, page insertion/removal, and page reordering should affect the corresponding axes while unrelated axes remain stable. These tests support directionality, sensitivity, invariance, and abstention behavior. They do not supply human preference labels or calibrate a universal score.",
        "",
        "Every published pair retains its reference and candidate hashes, source CSV, evidence JSON, metric status, and axis values in `per_sample_scores.csv`. This is the explanation layer: a table cell can be traced back to tokens, boxes, page pairing, and the evaluator's explicit abstention reason.",
        "",
        "## Limitations and licensing",
        "",
        "- Conditional fidelity distributions are system-specific because compilation coverage differs.",
        "- The model record identifies an API route, not an immutable provider checkpoint.",
        "- Deterministic-engine executable versions were not recorded; archived artifacts define the as-tested candidates.",
        "- PDF text extraction and font metadata are imperfect. Structure-dependent table, formula, figure, and semantic measures abstain without validated common structures.",
        "- Controlled corruption and blinded LLM evidence audits are engineering validation, not human perceptual ratings.",
        "- Per-sample provenance is recorded, but TeX Live/CTAN-derived material still needs package-level license review before redistribution.",
        "",
        "## Reproduce and audit",
        "",
        "```bash",
        "mamba run -n lathe python scripts/evaluation/build_publication_scorecard_v0.py",
        "mamba run -n lathe python scripts/evaluation/analyze_publication_results.py",
        "mamba run -n lathe python scripts/evaluation/build_publication_manuscript.py",
        "mamba run -n lathe python scripts/evaluation/preflight_publication_v0.py --check-only",
        "```",
        "",
        f"Held-out split: `{_escape(provenance['inputs']['heldout_split']['path'])}`  ",
        f"Held-out split SHA-256: `{_escape(provenance['inputs']['heldout_split']['sha256_raw_bytes'])}`  ",
        f"System prompt: `{_escape(provenance['inputs']['system_prompt']['path'])}`  ",
        f"System prompt SHA-256: `{_escape(provenance['inputs']['system_prompt']['sha256_raw_bytes'])}`  ",
        f"Metric implementation: `{_escape(provenance['inputs']['metric_v2_implementation']['path'])}`",
        "",
        "The manuscript is replaced only after all required publication files, hashes, per-system coverage, and recomputed aggregates agree.",
        "",
    ])
    return "\n".join(lines)


def build(input_dir: Path = DEFAULT_INPUT, output: Path = DEFAULT_OUTPUT) -> str:
    document, per_sample, statistics_document = load_publication(input_dir)
    manuscript = render_manuscript(document, per_sample, statistics_document)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(manuscript, encoding="utf-8")
    return manuscript


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    manuscript = build(args.input_dir, args.output)
    print(json.dumps({"output": str(args.output), "bytes": len(manuscript.encode())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
