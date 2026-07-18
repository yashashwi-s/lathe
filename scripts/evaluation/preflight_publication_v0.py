#!/usr/bin/env python3
"""Fail-closed release gate for the publication-v0 benchmark scorecard.

The gate deliberately writes nothing unless the canonical corpus, frozen
protocol, candidates, metric evidence, publication table, and recorded hashes
agree.  Development/adaptive/model-overlap results may remain in the repository
as research evidence, but cannot enter the primary 127-document table.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_ACCEPTED = 157
EXPECTED_PROMPT_DEV = 30
EXPECTED_HELDOUT = 127
EXPECTED_MODEL = "google/gemini-3.1-flash-lite"
EXPECTED_STATISTICS_SCHEMA = "publication_statistics_v0.1"
EXPECTED_STATISTICS_SEED = 20260718
EXPECTED_STATISTICS_ITERATIONS = 10_000
EXPECTED_STATISTICS_TIE_TOLERANCE = 1e-6
EXPECTED_SYSTEMS = (
    "gemini_first_pass",
    "gemini_after_one_repair",
    "pandoc",
    "tylax",
    "typetex",
)
ENGINE_SYSTEMS = frozenset({"pandoc", "tylax", "typetex"})
EXPECTED_STATISTICS_BASELINE = "gemini_after_one_repair"
EXPECTED_STATISTICS_COMPARATORS = ("pandoc", "tylax", "typetex")
EXPECTED_STATISTICS_AXES = (
    ("strict_word_f1", "higher_is_better"),
    ("compatibility_word_f1", "higher_is_better"),
    ("matched_word_reference_coverage", "higher_is_better"),
    ("token_center_displacement_q90", "lower_is_better"),
    ("text_ltsim_page_macro", "higher_is_better"),
)
PAIRED_AXIS_FIELDS = (
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
CATEGORY_RESULT_FIELDS = (
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
EXPECTED_PRIMARY_PROTOCOLS = {
    "gemini_first_pass": "gemini_prompt_v1_first_pass",
    "gemini_after_one_repair": "gemini_prompt_v1_after_one_compiler_repair",
    "pandoc": "deterministic_pandoc_as_tested",
    "tylax": "deterministic_tylax_as_tested",
    "typetex": "deterministic_typetex_as_tested",
}
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
SCORECARD_NUMERIC_FIELDS = SCORECARD_FIELDS[5:-2]
PER_SAMPLE_METRIC_FIELDS = (
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
CLAIM_BOUNDARIES = {
    "scope": (
        "The primary table uses the frozen 127-document held-out split. The 30 prompt-development "
        "documents, adaptive v2/v3 retries, and Claude overlap runs are excluded."
    ),
    "protocol": (
        "Gemini is reported at first pass and after at most one compiler-error repair under the "
        "same frozen v1 source-only protocol. Engines are deterministic baselines."
    ),
    "aggregation": (
        "Compilation and exact-page rates retain all 127 held-out documents in the denominator. "
        "Fidelity medians are conditional on compiled PDFs; SSIM has its own eligibility count."
    ),
    "interpretation": (
        "The benchmark reports an evidence vector, not one universal grade or human-preference score."
    ),
    "uncertainty": (
        "Compilation intervals use all 127 held-out IDs. Fidelity effects are paired by document "
        "on common compiled, non-abstained rows and use a fixed document-level bootstrap."
    ),
    "identity": (
        "The AI identity is the recorded API route, not an immutable provider checkpoint hash."
    ),
}


@dataclass(frozen=True)
class PublicationPaths:
    root: Path
    accepted: Path
    prompt_dev: Path
    heldout: Path
    engine_manifest: Path
    run_dir: Path
    per_sample_csv: Path
    scorecard_csv: Path
    scorecard_json: Path
    scorecard_summary: Path
    publication_statistics: Path
    paired_axis_results: Path
    category_results: Path
    statistics_analyzer: Path
    report_source: Path
    pdf_source: Path
    report_pdf: Path
    output_dir: Path

    @classmethod
    def from_root(cls, root: Path) -> "PublicationPaths":
        root = root.resolve()
        output_dir = root / "results" / "publication_v0"
        run_dir = (
            root
            / "results"
            / "ai_latex_to_typst"
            / "openrouter"
            / "google_gemini-3.1-flash-lite"
            / "prompt_v1_heldout_clean"
        )
        return cls(
            root=root,
            accepted=root / "data" / "latex_benchmark_v0" / "accepted_manifest.csv",
            prompt_dev=root / "data" / "latex_benchmark_v0" / "splits" / "prompt_dev_33.csv",
            heldout=root / "data" / "latex_benchmark_v0" / "splits" / "heldout_clean_127.csv",
            engine_manifest=root / "results" / "latex_benchmark_v0" / "engine_manifest.csv",
            run_dir=run_dir,
            per_sample_csv=output_dir / "per_sample_scores.csv",
            scorecard_csv=output_dir / "scorecard.csv",
            scorecard_json=output_dir / "scorecard.json",
            scorecard_summary=output_dir / "summary.md",
            publication_statistics=output_dir / "publication_statistics.json",
            paired_axis_results=output_dir / "paired_axis_results.csv",
            category_results=output_dir / "category_results.csv",
            statistics_analyzer=root / "scripts" / "evaluation" / "analyze_publication_results.py",
            report_source=root / "reports" / "benchmark_paper_blog.md",
            pdf_source=root / "reports" / "pdf_fidelity_metric_system_v3.typ",
            report_pdf=root / "output" / "pdf" / "pdf_fidelity_metric_system_v3.pdf",
            output_dir=output_dir,
        )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_sha256(path: Path) -> str:
    """Match the API runner's UTF-8, universal-newline hash semantics."""

    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def repo_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def resolve_repo_path(value: str, root: Path) -> Path:
    candidate = Path(value)
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"path escapes repository: {value}") from error
    return resolved


def parse_bool(value: object) -> bool | None:
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    return None


def finite_number(value: object) -> float | None:
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _ids(
    rows: Sequence[Mapping[str, str]],
    *,
    label: str,
    expected_count: int,
) -> tuple[set[str], list[str]]:
    values = [row.get("sample_id", "").strip() for row in rows]
    counts = Counter(values)
    errors: list[str] = []
    blank = counts.pop("", 0)
    duplicates = sorted(sample_id for sample_id, count in counts.items() if count != 1)
    if len(rows) != expected_count:
        errors.append(f"{label}: expected {expected_count} rows, found {len(rows)}")
    if blank:
        errors.append(f"{label}: {blank} rows have blank sample_id")
    if duplicates:
        errors.append(f"{label}: duplicate sample_id values: {', '.join(duplicates[:8])}")
    return set(counts), errors


def validate_split_contract(
    accepted: Sequence[Mapping[str, str]],
    prompt_dev: Sequence[Mapping[str, str]],
    heldout: Sequence[Mapping[str, str]],
    *,
    expected_accepted: int = EXPECTED_ACCEPTED,
    expected_prompt_dev: int = EXPECTED_PROMPT_DEV,
    expected_heldout: int = EXPECTED_HELDOUT,
) -> list[str]:
    accepted_ids, errors = _ids(
        accepted, label="accepted manifest", expected_count=expected_accepted
    )
    dev_ids, dev_errors = _ids(
        prompt_dev, label="prompt-development split", expected_count=expected_prompt_dev
    )
    heldout_ids, heldout_errors = _ids(
        heldout, label="held-out split", expected_count=expected_heldout
    )
    errors.extend(dev_errors)
    errors.extend(heldout_errors)
    overlap = sorted(dev_ids & heldout_ids)
    if overlap:
        errors.append(f"split leakage: {len(overlap)} IDs occur in both splits: {', '.join(overlap[:8])}")
    union = dev_ids | heldout_ids
    if union != accepted_ids:
        missing = sorted(accepted_ids - union)
        extra = sorted(union - accepted_ids)
        errors.append(
            "split union does not equal canonical accepted IDs"
            f" (missing={missing[:8]}, extra={extra[:8]})"
        )
    if any(row.get("status") != "accepted" for row in accepted):
        errors.append("accepted manifest contains a row whose status is not 'accepted'")
    return errors


def validate_canonical_artifacts(
    rows: Sequence[Mapping[str, str]], *, root: Path
) -> tuple[list[str], list[Path], list[Path]]:
    errors: list[str] = []
    sources: list[Path] = []
    references: list[Path] = []
    for row in rows:
        sample_id = row.get("sample_id", "<blank>")
        try:
            sample_dir = resolve_repo_path(row.get("sample_dir", ""), root)
        except ValueError as error:
            errors.append(f"{sample_id}: {error}")
            continue
        source = sample_dir / "main.tex"
        reference = sample_dir / "reference.pdf"
        sources.append(source)
        references.append(reference)
        for label, path, recorded_hash in (
            ("source", source, row.get("sha256_source", "")),
            ("reference", reference, row.get("sha256_pdf", "")),
        ):
            if not path.is_file():
                errors.append(f"{sample_id}: canonical {label} artifact is missing")
            elif sha256(path) != recorded_hash:
                errors.append(f"{sample_id}: canonical {label} SHA-256 is stale")
    return errors, sources, references


def validate_primary_rows(rows: Sequence[Mapping[str, str]], *, universe_n: int = EXPECTED_HELDOUT) -> list[str]:
    errors: list[str] = []
    if not rows:
        return ["primary scorecard has no rows"]
    fields = set(rows[0])
    missing_fields = [field for field in SCORECARD_FIELDS if field not in fields]
    if missing_fields:
        errors.append(f"primary scorecard missing fields: {', '.join(missing_fields)}")
        return errors
    systems = [row.get("system_id", "") for row in rows]
    if systems != list(EXPECTED_SYSTEMS):
        errors.append(
            "primary scorecard systems/order must be exactly "
            f"{list(EXPECTED_SYSTEMS)}, found {systems}"
        )
    expected_stages = {
        "gemini_first_pass": "attempt_1",
        "gemini_after_one_repair": "cumulative_after_at_most_one_repair",
        "pandoc": "as_tested_output",
        "tylax": "as_tested_output",
        "typetex": "as_tested_output",
    }
    for row in rows:
        system = row.get("system_id", "")
        searchable = " ".join(str(value) for value in row.values()).lower()
        if any(token in searchable for token in ("claude", "prompt_dev", "adaptive", "v2", "v3")):
            errors.append(f"{system or '<blank>'}: development/adaptive/Claude data entered primary table")
        if row.get("protocol_id") != EXPECTED_PRIMARY_PROTOCOLS.get(system):
            errors.append(
                f"{system}: wrong protocol_id {row.get('protocol_id')!r}; "
                f"expected {EXPECTED_PRIMARY_PROTOCOLS.get(system)!r}"
            )
        if row.get("candidate_stage") != expected_stages.get(system):
            errors.append(
                f"{system}: wrong candidate_stage {row.get('candidate_stage')!r}; "
                f"expected {expected_stages.get(system)!r}"
            )
        if finite_number(row.get("universe_n")) != universe_n:
            errors.append(f"{system}: universe_n must be {universe_n}")
        compiled = finite_number(row.get("compiled_n"))
        if compiled is None or compiled < 0 or compiled > universe_n or int(compiled) != compiled:
            errors.append(f"{system}: compiled_n is not an integer in [0, {universe_n}]")
        for field in SCORECARD_NUMERIC_FIELDS:
            text = str(row.get(field, "")).strip()
            if not text:
                if field != "ssim_median" or finite_number(row.get("ssim_eligible_n")) != 0:
                    errors.append(f"{system}: blank {field} lacks an explicit zero-eligibility abstention")
            elif finite_number(text) is None:
                errors.append(f"{system}: {field} is not finite: {text!r}")
        candidate_set_hash = row.get("candidate_set_sha256", "")
        if len(candidate_set_hash) != 64 or any(char not in "0123456789abcdef" for char in candidate_set_hash):
            errors.append(f"{system}: candidate_set_sha256 is malformed")
    return errors


def _abstention_is_explicit(axis: Mapping[str, Any]) -> bool:
    if axis.get("status") != "abstain":
        return False
    if str(axis.get("reason", "")).strip():
        return True
    evidence = axis.get("evidence")
    if not isinstance(evidence, Mapping):
        return False
    pages = evidence.get("pages")
    return isinstance(pages, list) and bool(pages) and all(
        isinstance(page, Mapping) and str(page.get("reason", "")).strip() for page in pages
    )


def _metric_value_matches(actual: str, expected: Any) -> bool:
    if expected is None:
        return not actual.strip()
    if isinstance(expected, bool):
        return parse_bool(actual) is expected
    if isinstance(expected, (int, float)):
        value = finite_number(actual)
        return value is not None and math.isclose(value, float(expected), rel_tol=1e-12, abs_tol=1e-12)
    return actual.strip() == str(expected)


def validate_metric_rows(
    rows: Sequence[Mapping[str, str]],
    *,
    expected_candidates: Mapping[tuple[str, str], Path],
    expected_references: Mapping[str, Path] | None = None,
    root: Path,
    flatten_evidence: Any,
) -> list[str]:
    """Validate one metric row and evidence JSON per expected compiled candidate."""

    errors: list[str] = []
    keyed: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in rows:
        key = (row.get("system_id", ""), row.get("sample_id", ""))
        if key in keyed:
            errors.append(f"metric rows: duplicate system/sample pair {key}")
        keyed[key] = row
    expected_keys = set(expected_candidates)
    actual_keys = set(keyed)
    if actual_keys != expected_keys:
        errors.append(
            "metric row coverage mismatch"
            f" (missing={sorted(expected_keys - actual_keys)[:8]}, extra={sorted(actual_keys - expected_keys)[:8]})"
        )
    for key in sorted(expected_keys & actual_keys):
        row = keyed[key]
        label = f"{key[0]}/{key[1]}"
        if row.get("v2_status") != "scored" or row.get("v2_error", "").strip():
            errors.append(f"{label}: metric row is not cleanly scored")
            continue
        candidate_text = row.get("candidate_pdf_resolved") or row.get("candidate_pdf", "")
        try:
            candidate = resolve_repo_path(candidate_text, root)
        except ValueError as error:
            errors.append(f"{label}: {error}")
            continue
        if candidate != expected_candidates[key].resolve():
            errors.append(f"{label}: candidate artifact does not match frozen protocol")
        if not candidate.is_file():
            errors.append(f"{label}: candidate artifact is missing: {candidate_text}")
        evidence_text = row.get("v2_evidence_json", "").strip()
        if not evidence_text:
            errors.append(f"{label}: metric evidence path is missing")
            continue
        try:
            evidence_path = resolve_repo_path(evidence_text, root)
        except ValueError as error:
            errors.append(f"{label}: {error}")
            continue
        if not evidence_path.is_file():
            errors.append(f"{label}: metric evidence artifact is missing: {evidence_text}")
            continue
        try:
            evidence = read_json(evidence_path)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            errors.append(f"{label}: invalid metric evidence JSON: {error}")
            continue
        inputs = evidence.get("inputs", {})
        if not isinstance(inputs, Mapping):
            errors.append(f"{label}: evidence has no inputs object")
        else:
            try:
                evidence_candidate = resolve_repo_path(str(inputs.get("candidate_pdf", "")), root)
                if evidence_candidate != candidate:
                    errors.append(f"{label}: evidence points to a different candidate artifact")
            except ValueError as error:
                errors.append(f"{label}: evidence candidate {error}")
            if expected_references is not None:
                try:
                    evidence_reference = resolve_repo_path(str(inputs.get("reference_pdf", "")), root)
                    if evidence_reference != expected_references[key[1]].resolve():
                        errors.append(f"{label}: evidence points to a different reference artifact")
                except (KeyError, ValueError) as error:
                    errors.append(f"{label}: evidence reference {error}")
        flattened = flatten_evidence(evidence)
        for field, expected in flattened.items():
            if field in row and not _metric_value_matches(str(row.get(field, "")), expected):
                errors.append(f"{label}: stale metric value for {field}")
        axes = evidence.get("axes", {})
        if not isinstance(axes, Mapping):
            axes = {}
        axis_by_field = {
            "strict_word_f1": "content",
            "compatibility_word_f1": "content",
            "number_f1": "critical_content",
            "operator_f1": "critical_content",
            "citation_f1": "critical_content",
            "matched_word_reference_coverage": "geometry",
            "token_center_displacement_q90": "geometry",
            "block_transport_combined_similarity": "block_transport",
            "text_ltsim_page_macro": "text_ltsim",
            "reading_order_tau": "reading_order",
            "style_coverage_hmean": "typography",
            "unregistered_ink_f1": "raster_ink",
            "page_count_delta": "pagination",
            "page_break_f1": "pagination",
            "canvas_exact_size_rate": "canvas",
            "unregistered_ssim": "raster_perceptual",
        }
        for field in PER_SAMPLE_METRIC_FIELDS:
            value = str(row.get(field, "")).strip()
            if value and finite_number(value) is None:
                errors.append(f"{label}: nonfinite metric {field}={value!r}")
            if not value:
                axis = axes.get(axis_by_field[field], {})
                if not isinstance(axis, Mapping) or not _abstention_is_explicit(axis):
                    errors.append(f"{label}: blank {field} lacks explicit evaluator abstention")
    return errors


def validate_recorded_hashes(document: Mapping[str, Any], *, root: Path) -> tuple[list[str], set[Path]]:
    """Validate every JSON path/SHA-256 pair, including nested artifact records."""

    errors: list[str] = []
    recorded: set[Path] = set()

    def check(path_value: object, hash_value: object, label: str) -> None:
        if not isinstance(path_value, str) or not path_value.strip():
            errors.append(f"{label}: recorded path is blank")
            return
        if not isinstance(hash_value, str) or len(hash_value) != 64:
            errors.append(f"{label}: recorded SHA-256 is malformed")
            return
        try:
            path = resolve_repo_path(path_value, root)
        except ValueError as error:
            errors.append(f"{label}: {error}")
            return
        recorded.add(path)
        if not path.is_file():
            errors.append(f"{label}: hashed artifact is missing: {path_value}")
        elif sha256(path) != hash_value:
            errors.append(f"{label}: stale SHA-256 for {path_value}")

    def walk(value: Any, label: str) -> None:
        if isinstance(value, Mapping):
            if "path" in value and "sha256" in value:
                check(value["path"], value["sha256"], label)
            elif "path" in value and "sha256_raw_bytes" in value:
                check(value["path"], value["sha256_raw_bytes"], label)
            for key, child in value.items():
                if key.endswith("_path"):
                    stem = key[:-5]
                    hash_key = f"{stem}_sha256"
                    if hash_key in value:
                        check(child, value[hash_key], f"{label}.{stem}")
                walk(child, f"{label}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{label}[{index}]")

    walk(document, "scorecard")
    return errors, recorded


def validate_per_sample_rows(
    rows: Sequence[Mapping[str, str]],
    *,
    heldout: Sequence[Mapping[str, str]],
    expected_candidates: Mapping[tuple[str, str], Path],
    recorded_metric_tables: set[Path],
    root: Path,
) -> tuple[list[str], list[dict[str, str]], dict[str, Path]]:
    """Validate the full 127 x 5 accounting table and return compiled metric rows."""

    errors: list[str] = []
    heldout_by_id = {row["sample_id"]: row for row in heldout}
    expected_keys = {
        (system, sample_id) for system in EXPECTED_SYSTEMS for sample_id in heldout_by_id
    }
    keyed: dict[tuple[str, str], Mapping[str, str]] = {}
    for row in rows:
        key = (row.get("system_id", ""), row.get("sample_id", ""))
        if key in keyed:
            errors.append(f"per-sample table has duplicate system/sample pair {key}")
        keyed[key] = row
    if set(keyed) != expected_keys or len(rows) != len(expected_keys):
        errors.append(
            "per-sample table must contain exactly 127 x 5 rows"
            f" (missing={sorted(expected_keys - set(keyed))[:8]}, extra={sorted(set(keyed) - expected_keys)[:8]})"
        )
    compiled_by_key: dict[tuple[str, str], dict[str, str]] = {}
    expected_references: dict[str, Path] = {}
    for sample_id, sample in heldout_by_id.items():
        try:
            expected_references[sample_id] = resolve_repo_path(sample["reference_pdf"], root)
        except ValueError as error:
            errors.append(f"{sample_id}: {error}")
    for key in sorted(expected_keys & set(keyed)):
        system, sample_id = key
        row = keyed[key]
        label = f"{system}/{sample_id}"
        if row.get("protocol_id") != EXPECTED_PRIMARY_PROTOCOLS[system]:
            errors.append(f"{label}: wrong primary protocol")
        if system == "gemini_first_pass":
            expected_stage = "attempt_1"
        elif system == "gemini_after_one_repair":
            expected_stage = (
                "attempt_1"
                if ("gemini_first_pass", sample_id) in expected_candidates
                else "attempt_2_repair"
                if key in expected_candidates
                else "no_compiled_pdf"
            )
        else:
            expected_stage = "as_tested_output"
        if row.get("candidate_stage") != expected_stage:
            errors.append(
                f"{label}: candidate_stage {row.get('candidate_stage')!r} does not match {expected_stage!r}"
            )
        searchable = " ".join(
            str(row.get(field, ""))
            for field in ("system_id", "display_label", "protocol_id", "protocol_label", "candidate_stage")
        ).lower()
        if any(token in searchable for token in ("claude", "prompt_dev", "adaptive", "v2", "v3")):
            errors.append(f"{label}: development/adaptive/Claude stage in primary per-sample table")
        compiled = parse_bool(row.get("compiled"))
        expected_compiled = key in expected_candidates
        if compiled is not expected_compiled:
            errors.append(f"{label}: compiled state disagrees with source artifact manifest")
        expected_reference = expected_references.get(sample_id)
        reference_text = row.get("reference_pdf", "")
        try:
            reference = resolve_repo_path(reference_text, root)
        except ValueError as error:
            errors.append(f"{label}: reference {error}")
            reference = None
        if reference is not None:
            if reference != expected_reference:
                errors.append(f"{label}: reference path differs from held-out split")
            if not reference.is_file():
                errors.append(f"{label}: reference PDF is missing")
            elif row.get("reference_sha256") != sha256(reference):
                errors.append(f"{label}: stale reference PDF hash")
        metric_values = [str(row.get(field, "")).strip() for field in PER_SAMPLE_METRIC_FIELDS]
        if expected_compiled:
            candidate_text = row.get("candidate_pdf", "")
            try:
                candidate = resolve_repo_path(candidate_text, root)
            except ValueError as error:
                errors.append(f"{label}: candidate {error}")
                candidate = None
            if candidate is not None:
                if candidate != expected_candidates[key].resolve():
                    errors.append(f"{label}: candidate path differs from frozen artifact")
                if not candidate.is_file():
                    errors.append(f"{label}: compiled candidate PDF is missing")
                elif row.get("candidate_sha256") != sha256(candidate):
                    errors.append(f"{label}: stale candidate PDF hash")
            if row.get("compile_status") != "compiled" or row.get("metric_v2_status") != "scored":
                errors.append(f"{label}: compiled row is not explicitly marked compiled/scored")
            source_text = row.get("metric_source_csv", "")
            try:
                source = resolve_repo_path(source_text, root)
                if source not in recorded_metric_tables:
                    errors.append(f"{label}: metric source is not a hashed scorecard input")
            except ValueError as error:
                errors.append(f"{label}: metric source {error}")
            normalized = dict(row)
            normalized["v2_status"] = row.get("metric_v2_status", "")
            normalized["v2_error"] = ""
            normalized["v2_evidence_json"] = row.get("metric_source_evidence_json", "")
            compiled_by_key[key] = normalized
        else:
            if row.get("compile_status") != "failed":
                errors.append(f"{label}: uncompiled row must be explicitly marked failed")
            if row.get("metric_v2_status") != "not_scored_uncompiled":
                errors.append(f"{label}: uncompiled row lacks explicit metric abstention status")
            if row.get("candidate_pdf", "").strip() or row.get("candidate_sha256", "").strip():
                errors.append(f"{label}: uncompiled row contains a candidate artifact")
            if row.get("metric_source_csv", "").strip() or row.get("metric_source_evidence_json", "").strip():
                errors.append(f"{label}: uncompiled row contains metric evidence")
            if any(metric_values):
                errors.append(f"{label}: uncompiled row contains fidelity values")
            if not row.get("compile_failure_class", "").strip():
                errors.append(f"{label}: failed row lacks an explicit failure class")
    compiled_metric_rows = [
        compiled_by_key[(row.get("system_id", ""), row.get("sample_id", ""))]
        for row in rows
        if (row.get("system_id", ""), row.get("sample_id", "")) in compiled_by_key
    ]
    return errors, compiled_metric_rows, expected_references


def _json_scorecard_rows(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    candidates: list[list[dict[str, Any]]] = []

    def walk(value: Any) -> None:
        if isinstance(value, list) and value and all(isinstance(row, dict) for row in value):
            if all("system_id" in row for row in value):
                candidates.append(value)
        elif isinstance(value, Mapping):
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(document)
    exact = [rows for rows in candidates if [row.get("system_id") for row in rows] == list(EXPECTED_SYSTEMS)]
    if len(exact) != 1:
        raise ValueError(f"scorecard JSON must contain exactly one primary {list(EXPECTED_SYSTEMS)} table")
    return exact[0]


def compare_scorecard_serializations(
    csv_rows: Sequence[Mapping[str, str]], json_rows: Sequence[Mapping[str, Any]]
) -> list[str]:
    errors: list[str] = []
    if len(csv_rows) != len(json_rows):
        return [f"scorecard CSV/JSON row count mismatch: {len(csv_rows)} != {len(json_rows)}"]
    for index, (csv_row, json_row) in enumerate(zip(csv_rows, json_rows)):
        for field in SCORECARD_FIELDS:
            left = str(csv_row.get(field, "")).strip()
            right = "" if json_row.get(field) is None else str(json_row.get(field)).strip()
            if field in SCORECARD_NUMERIC_FIELDS and left and right:
                left_number = finite_number(left)
                right_number = finite_number(right)
                equal = (
                    left_number is not None
                    and right_number is not None
                    and math.isclose(left_number, right_number, rel_tol=1e-12, abs_tol=1e-12)
                )
            else:
                equal = left == right
            if not equal:
                errors.append(f"scorecard CSV/JSON stale value at row {index + 1}, field {field}")
    return errors


def _exact_int(value: object) -> int | None:
    number = finite_number(value)
    if number is None or int(number) != number:
        return None
    return int(number)


def _statistics_stream_seed(label: str) -> int:
    payload = f"{EXPECTED_STATISTICS_SEED}:{label}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def _statistics_percentile(values: Sequence[float], probability: float) -> float:
    position = (len(values) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[lower]
    weight = position - lower
    return values[lower] * (1 - weight) + values[upper] * weight


def _statistics_bootstrap_interval(
    values: Sequence[float], *, label: str, statistic: str
) -> tuple[float, float]:
    if not values:
        raise ValueError(f"cannot bootstrap empty series: {label}")
    rng = random.Random(_statistics_stream_seed(label))
    count = len(values)
    estimates: list[float] = []
    for _ in range(EXPECTED_STATISTICS_ITERATIONS):
        sample = [values[rng.randrange(count)] for _ in range(count)]
        estimate = (
            sum(sample) / count
            if statistic == "mean"
            else float(_median(sample))
        )
        estimates.append(estimate)
    estimates.sort()
    return (
        _statistics_percentile(estimates, 0.025),
        _statistics_percentile(estimates, 0.975),
    )


def _serialized_rows_match(
    csv_rows: Sequence[Mapping[str, str]],
    json_rows: object,
    *,
    fields: Sequence[str],
    label: str,
) -> list[str]:
    if not isinstance(json_rows, list) or not all(isinstance(row, Mapping) for row in json_rows):
        return [f"{label}: JSON rows must be a list of objects"]
    errors: list[str] = []
    if len(csv_rows) != len(json_rows):
        errors.append(f"{label}: CSV/JSON row count mismatch: {len(csv_rows)} != {len(json_rows)}")
    if csv_rows and tuple(csv_rows[0]) != tuple(fields):
        errors.append(f"{label}: CSV fields/order do not match the frozen schema")
    for index, (csv_row, json_row) in enumerate(zip(csv_rows, json_rows), start=1):
        for field in fields:
            left = str(csv_row.get(field, "")).strip()
            value = json_row.get(field)
            right = "" if value is None else str(value).strip()
            if left != right:
                errors.append(f"{label}: CSV/JSON stale value at row {index}, field {field}")
    return errors


def _expect_number(
    errors: list[str],
    value: object,
    expected: float,
    label: str,
    *,
    tolerance: float = 1e-6,
) -> None:
    actual = finite_number(value)
    if actual is None or not math.isclose(actual, expected, rel_tol=0, abs_tol=tolerance):
        errors.append(f"{label}: expected {expected}, found {value!r}")


def validate_statistics_artifacts(
    document: Mapping[str, Any],
    paired_rows: Sequence[Mapping[str, str]],
    category_rows: Sequence[Mapping[str, str]],
    *,
    per_sample_rows: Sequence[Mapping[str, str]],
    root: Path,
    per_sample_path: Path,
    paired_path: Path,
    category_path: Path,
    expected_universe_n: int = EXPECTED_HELDOUT,
) -> list[str]:
    """Independently gate the frozen document-level uncertainty artifacts."""

    errors: list[str] = []
    if document.get("schema_version") != EXPECTED_STATISTICS_SCHEMA:
        errors.append(
            "publication statistics: schema_version must be "
            f"{EXPECTED_STATISTICS_SCHEMA!r}"
        )

    analysis_value = document.get("analysis")
    analysis = analysis_value if isinstance(analysis_value, Mapping) else {}
    if not analysis:
        errors.append("publication statistics: missing analysis object")
    if "overall_scalar_score" not in analysis or analysis.get("overall_scalar_score") is not None:
        errors.append("publication statistics: overall_scalar_score must be explicitly null")
    if _exact_int(analysis.get("universe_n")) != expected_universe_n:
        errors.append(f"publication statistics: universe_n must be {expected_universe_n}")
    if analysis.get("system_order") != list(EXPECTED_SYSTEMS):
        errors.append("publication statistics: system_order does not match the five primary systems")
    if analysis.get("baseline_system_id") != EXPECTED_STATISTICS_BASELINE:
        errors.append("publication statistics: wrong paired-comparison baseline")
    if analysis.get("comparator_system_ids") != list(EXPECTED_STATISTICS_COMPARATORS):
        errors.append("publication statistics: comparator systems must be the three engines")
    expected_axes_document = [
        {"axis": axis, "direction": direction}
        for axis, direction in EXPECTED_STATISTICS_AXES
    ]
    if analysis.get("axes") != expected_axes_document:
        errors.append("publication statistics: axes/directions do not match the frozen five-axis set")

    try:
        source = resolve_repo_path(str(analysis.get("source", "")), root)
    except ValueError as error:
        errors.append(f"publication statistics source: {error}")
        source = None
    if source is not None and source != per_sample_path.resolve():
        errors.append("publication statistics: source is not the frozen per-sample table")
    if analysis.get("source_sha256_raw_bytes") != sha256(per_sample_path):
        errors.append("publication statistics: source SHA-256 is stale")

    bootstrap_value = document.get("bootstrap")
    bootstrap = bootstrap_value if isinstance(bootstrap_value, Mapping) else {}
    if not bootstrap:
        errors.append("publication statistics: missing bootstrap object")
    if bootstrap.get("unit") != "document/sample ID":
        errors.append("publication statistics: bootstrap unit must be document/sample ID")
    if bootstrap.get("interval") != "percentile":
        errors.append("publication statistics: bootstrap interval must be percentile")
    _expect_number(errors, bootstrap.get("confidence_level"), 0.95, "publication statistics confidence")
    if _exact_int(bootstrap.get("seed")) != EXPECTED_STATISTICS_SEED:
        errors.append(f"publication statistics: seed must be {EXPECTED_STATISTICS_SEED}")
    if _exact_int(bootstrap.get("iterations")) != EXPECTED_STATISTICS_ITERATIONS:
        errors.append(
            f"publication statistics: iterations must be {EXPECTED_STATISTICS_ITERATIONS}"
        )
    _expect_number(
        errors,
        bootstrap.get("tie_tolerance"),
        EXPECTED_STATISTICS_TIE_TOLERANCE,
        "publication statistics tie_tolerance",
        tolerance=1e-12,
    )

    index: dict[tuple[str, str], Mapping[str, str]] = {}
    labels: dict[str, str] = {}
    sample_categories: dict[str, str] = {}
    for row in per_sample_rows:
        sample_id = row.get("sample_id", "").strip()
        system_id = row.get("system_id", "").strip()
        key = (sample_id, system_id)
        if key in index:
            errors.append(f"publication statistics input: duplicate system/sample pair {key}")
        index[key] = row
        display_label = row.get("display_label", "").strip()
        if system_id in labels and labels[system_id] != display_label:
            errors.append(f"publication statistics input: inconsistent label for {system_id}")
        elif system_id in EXPECTED_SYSTEMS:
            labels[system_id] = display_label
        category = row.get("category", "").strip()
        if sample_id in sample_categories and sample_categories[sample_id] != category:
            errors.append(f"publication statistics input: inconsistent category for {sample_id}")
        else:
            sample_categories[sample_id] = category

    sample_ids = sorted(sample_categories)
    expected_matrix = {
        (sample_id, system_id)
        for sample_id in sample_ids
        for system_id in EXPECTED_SYSTEMS
    }
    matrix_complete = (
        len(sample_ids) == expected_universe_n
        and set(index) == expected_matrix
        and len(index) == expected_universe_n * len(EXPECTED_SYSTEMS)
    )
    if not matrix_complete:
        errors.append("publication statistics input: expected a complete 127 x 5 primary matrix")
    sample_digest = hashlib.sha256(
        json.dumps(sample_ids, separators=(",", ":")).encode()
    ).hexdigest()
    if analysis.get("sample_id_set_sha256") != sample_digest:
        errors.append("publication statistics: sample-ID set SHA-256 is stale")

    compiled: dict[tuple[str, str], bool] = {}
    for key, row in index.items():
        value = parse_bool(row.get("compiled"))
        if value is None:
            errors.append(f"publication statistics input: invalid compiled value for {key}")
        else:
            compiled[key] = value

    compile_value = document.get("compile_rate_results")
    compile_rows = compile_value if isinstance(compile_value, list) else []
    if not isinstance(compile_value, list) or not all(isinstance(row, Mapping) for row in compile_rows):
        errors.append("publication statistics: compile_rate_results must be a list of objects")
        compile_rows = []
    compile_systems = [str(row.get("system_id", "")) for row in compile_rows]
    if compile_systems != list(EXPECTED_SYSTEMS):
        errors.append("publication statistics: compile-rate rows must cover all five systems exactly once")
    if matrix_complete and len(compiled) == len(index):
        for row in compile_rows:
            system_id = str(row.get("system_id", ""))
            if system_id not in EXPECTED_SYSTEMS:
                continue
            compiled_n = sum(compiled[(sample_id, system_id)] for sample_id in sample_ids)
            label = f"compile-rate {system_id}"
            if _exact_int(row.get("universe_n")) != expected_universe_n:
                errors.append(f"{label}: universe_n must be {expected_universe_n}")
            if _exact_int(row.get("compiled_n")) != compiled_n:
                errors.append(f"{label}: compiled_n disagrees with the primary table")
            if _exact_int(row.get("failed_n")) != expected_universe_n - compiled_n:
                errors.append(f"{label}: failed_n disagrees with the primary table")
            _expect_number(errors, row.get("estimate"), round(compiled_n / expected_universe_n, 6), f"{label} estimate")
            low = finite_number(row.get("ci_low"))
            high = finite_number(row.get("ci_high"))
            if low is None or high is None or not (0 <= low <= high <= 1):
                errors.append(f"{label}: confidence interval is invalid")
            else:
                expected_low, expected_high = _statistics_bootstrap_interval(
                    [float(compiled[(sample_id, system_id)]) for sample_id in sample_ids],
                    label=f"compile_rate:{system_id}",
                    statistic="mean",
                )
                _expect_number(errors, low, round(expected_low, 6), f"{label} ci_low")
                _expect_number(errors, high, round(expected_high, 6), f"{label} ci_high")
            _expect_number(errors, row.get("confidence_level"), 0.95, f"{label} confidence")
            if _exact_int(row.get("seed")) != EXPECTED_STATISTICS_SEED:
                errors.append(f"{label}: wrong seed")
            if _exact_int(row.get("bootstrap_iterations")) != EXPECTED_STATISTICS_ITERATIONS:
                errors.append(f"{label}: wrong bootstrap iteration count")
            expected_stream = _statistics_stream_seed(f"compile_rate:{system_id}")
            if _exact_int(row.get("stream_seed")) != expected_stream:
                errors.append(f"{label}: wrong deterministic stream seed")
            if row.get("method") != "document bootstrap of compile-rate mean; percentile 95% CI":
                errors.append(f"{label}: wrong bootstrap method")

    paired_json = document.get("paired_axis_results")
    errors.extend(
        _serialized_rows_match(
            paired_rows,
            paired_json,
            fields=PAIRED_AXIS_FIELDS,
            label="paired-axis results",
        )
    )
    expected_paired_keys = [
        (comparator, axis)
        for comparator in EXPECTED_STATISTICS_COMPARATORS
        for axis, _ in EXPECTED_STATISTICS_AXES
    ]
    actual_paired_keys = [
        (row.get("comparator_system_id", ""), row.get("axis", ""))
        for row in paired_rows
    ]
    if len(paired_rows) != 15 or actual_paired_keys != expected_paired_keys:
        errors.append("paired-axis results: expected exactly 3 engines x 5 axes in frozen order")

    axis_directions = dict(EXPECTED_STATISTICS_AXES)
    if matrix_complete and len(compiled) == len(index):
        baseline_compiled_n = sum(
            compiled[(sample_id, EXPECTED_STATISTICS_BASELINE)] for sample_id in sample_ids
        )
        for row in paired_rows:
            comparator = row.get("comparator_system_id", "")
            axis = row.get("axis", "")
            if comparator not in EXPECTED_STATISTICS_COMPARATORS or axis not in axis_directions:
                continue
            label = f"paired-axis {comparator}/{axis}"
            direction = axis_directions[axis]
            if row.get("baseline_system_id") != EXPECTED_STATISTICS_BASELINE:
                errors.append(f"{label}: wrong baseline")
            if row.get("direction") != direction:
                errors.append(f"{label}: wrong direction")
            expected_comparison = f"{labels[EXPECTED_STATISTICS_BASELINE]} vs {labels[comparator]}"
            if row.get("comparison") != expected_comparison:
                errors.append(f"{label}: wrong display comparison")
            common_ids = [
                sample_id
                for sample_id in sample_ids
                if compiled[(sample_id, EXPECTED_STATISTICS_BASELINE)]
                and compiled[(sample_id, comparator)]
            ]
            pairs = [
                (
                    finite_number(index[(sample_id, EXPECTED_STATISTICS_BASELINE)].get(axis)),
                    finite_number(index[(sample_id, comparator)].get(axis)),
                )
                for sample_id in common_ids
            ]
            pairs = [(left, right) for left, right in pairs if left is not None and right is not None]
            differences = [
                left - right if direction == "higher_is_better" else right - left
                for left, right in pairs
            ]
            comparator_compiled_n = sum(compiled[(sample_id, comparator)] for sample_id in sample_ids)
            expected_counts = {
                "paired_n": len(pairs),
                "baseline_compiled_n": baseline_compiled_n,
                "comparator_compiled_n": comparator_compiled_n,
                "common_compiled_n": len(common_ids),
                "abstention_n": len(common_ids) - len(pairs),
                "wins": sum(value > EXPECTED_STATISTICS_TIE_TOLERANCE for value in differences),
                "losses": sum(value < -EXPECTED_STATISTICS_TIE_TOLERANCE for value in differences),
            }
            expected_counts["ties"] = len(differences) - expected_counts["wins"] - expected_counts["losses"]
            for field, expected in expected_counts.items():
                if _exact_int(row.get(field)) != expected:
                    errors.append(f"{label}: {field} disagrees with paired primary rows")
            if differences:
                _expect_number(errors, row.get("baseline_median"), round(float(_median(left for left, _ in pairs)), 6), f"{label} baseline median")
                _expect_number(errors, row.get("comparator_median"), round(float(_median(right for _, right in pairs)), 6), f"{label} comparator median")
                _expect_number(errors, row.get("estimate"), round(float(_median(differences)), 6), f"{label} oriented estimate")
            low = finite_number(row.get("ci_low"))
            high = finite_number(row.get("ci_high"))
            if low is None or high is None or low > high:
                errors.append(f"{label}: confidence interval is invalid")
            elif differences:
                expected_low, expected_high = _statistics_bootstrap_interval(
                    differences,
                    label=(
                        f"paired_median:{EXPECTED_STATISTICS_BASELINE}:"
                        f"{comparator}:{axis}"
                    ),
                    statistic="median",
                )
                _expect_number(errors, low, round(expected_low, 6), f"{label} ci_low")
                _expect_number(errors, high, round(expected_high, 6), f"{label} ci_high")
            _expect_number(errors, row.get("tie_tolerance"), EXPECTED_STATISTICS_TIE_TOLERANCE, f"{label} tie tolerance", tolerance=1e-12)
            if _exact_int(row.get("seed")) != EXPECTED_STATISTICS_SEED:
                errors.append(f"{label}: wrong seed")
            if _exact_int(row.get("bootstrap_iterations")) != EXPECTED_STATISTICS_ITERATIONS:
                errors.append(f"{label}: wrong bootstrap iteration count")
            stream_label = f"paired_median:{EXPECTED_STATISTICS_BASELINE}:{comparator}:{axis}"
            if _exact_int(row.get("stream_seed")) != _statistics_stream_seed(stream_label):
                errors.append(f"{label}: wrong deterministic stream seed")
            expected_method = "paired document bootstrap of median oriented differences; percentile 95% CI"
            if row.get("method") != expected_method:
                errors.append(f"{label}: wrong bootstrap method")

    category_json = document.get("category_results")
    errors.extend(
        _serialized_rows_match(
            category_rows,
            category_json,
            fields=CATEGORY_RESULT_FIELDS,
            label="category results",
        )
    )
    categories = sorted(set(sample_categories.values()))
    category_axes = (("compile_rate", "higher_is_better"), *EXPECTED_STATISTICS_AXES)
    expected_category_keys = [
        (system_id, category, axis)
        for system_id in EXPECTED_SYSTEMS
        for category in categories
        for axis, _ in category_axes
    ]
    actual_category_keys = [
        (row.get("system_id", ""), row.get("category", ""), row.get("axis", ""))
        for row in category_rows
    ]
    if actual_category_keys != expected_category_keys:
        errors.append("category results: incomplete or reordered system/category/axis matrix")
    if matrix_complete and len(compiled) == len(index):
        for row in category_rows:
            system_id = row.get("system_id", "")
            category = row.get("category", "")
            axis = row.get("axis", "")
            if system_id not in EXPECTED_SYSTEMS or category not in categories or axis not in dict(category_axes):
                continue
            label = f"category {system_id}/{category}/{axis}"
            category_ids = [
                sample_id for sample_id in sample_ids if sample_categories[sample_id] == category
            ]
            compiled_ids = [sample_id for sample_id in category_ids if compiled[(sample_id, system_id)]]
            if row.get("display_label") != labels[system_id]:
                errors.append(f"{label}: inconsistent display label")
            if _exact_int(row.get("universe_n")) != len(category_ids):
                errors.append(f"{label}: universe_n disagrees with primary rows")
            if _exact_int(row.get("compiled_n")) != len(compiled_ids):
                errors.append(f"{label}: compiled_n disagrees with primary rows")
            _expect_number(errors, row.get("compile_rate"), round(len(compiled_ids) / len(category_ids), 6), f"{label} compile rate")
            expected_direction = dict(category_axes)[axis]
            if row.get("direction") != expected_direction:
                errors.append(f"{label}: wrong direction")
            if axis == "compile_rate":
                applicable_n = len(category_ids)
                expected_median = None
                population = "all assigned documents"
            else:
                values = [
                    value
                    for sample_id in compiled_ids
                    if (value := finite_number(index[(sample_id, system_id)].get(axis))) is not None
                ]
                applicable_n = len(values)
                expected_median = round(float(_median(values)), 6) if values else None
                population = "compiled PDFs with non-abstained axis"
            if _exact_int(row.get("applicable_n")) != applicable_n:
                errors.append(f"{label}: applicable_n disagrees with primary rows")
            median = str(row.get("median", "")).strip()
            if expected_median is None:
                if median:
                    errors.append(f"{label}: median must be an explicit blank abstention")
            else:
                _expect_number(errors, median, expected_median, f"{label} median")
            if row.get("population") != population:
                errors.append(f"{label}: wrong population label")

    hash_errors, recorded = validate_recorded_hashes(document, root=root)
    errors.extend(f"publication statistics: {error}" for error in hash_errors)
    expected_recorded = {paired_path.resolve(), category_path.resolve()}
    if not expected_recorded.issubset(recorded):
        errors.append("publication statistics: CSV artifact paths/hashes are incomplete")
    guardrails = document.get("guardrails")
    if not isinstance(guardrails, list) or not any(
        "no overall scalar" in str(value).lower() for value in guardrails
    ):
        errors.append("publication statistics: missing no-scalar guardrail")
    return errors


def _artifact(path: Path, root: Path) -> dict[str, Any]:
    return {"path": repo_path(path, root), "sha256": sha256(path), "bytes": path.stat().st_size}


def _tree_digest(paths: Iterable[Path], root: Path) -> dict[str, Any]:
    entries = [
        {"path": repo_path(path, root), "sha256": sha256(path), "bytes": path.stat().st_size}
        for path in sorted({path.resolve() for path in paths}, key=lambda value: repo_path(value, root))
    ]
    encoded = json.dumps(entries, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {"files": len(entries), "sha256": hashlib.sha256(encoded).hexdigest(), "entries": entries}


def _expected_candidate_maps(
    heldout_ids: set[str], run_manifest: Sequence[Mapping[str, str]], engine_manifest: Sequence[Mapping[str, str]], paths: PublicationPaths
) -> tuple[dict[tuple[str, str], Path], list[str]]:
    errors: list[str] = []
    expected: dict[tuple[str, str], Path] = {}
    run_by_id = {row.get("sample_id", ""): row for row in run_manifest}
    for sample_id in sorted(heldout_ids):
        row = run_by_id.get(sample_id)
        if row is None:
            continue
        sample_dir = paths.run_dir / "samples" / sample_id
        first = parse_bool(row.get("first_pass_compiled"))
        final = parse_bool(row.get("final_compiled"))
        if first is None or final is None:
            errors.append(f"{sample_id}: run manifest lacks explicit compile booleans")
            continue
        if first:
            # The publication table reuses the metric row for output.pdf.  The
            # run audit below proves it is byte-identical to attempt_1.pdf when
            # the first pass compiled, so no second evaluation can drift.
            expected[("gemini_first_pass", sample_id)] = sample_dir / "output.pdf"
        if final:
            expected[("gemini_after_one_repair", sample_id)] = sample_dir / "output.pdf"
    seen_engines: set[tuple[str, str]] = set()
    for row in engine_manifest:
        sample_id = row.get("sample_id", "")
        engine = row.get("engine", "")
        if sample_id not in heldout_ids or engine not in ENGINE_SYSTEMS:
            continue
        key = (engine, sample_id)
        if key in seen_engines:
            errors.append(f"engine manifest duplicate system/sample pair {key}")
            continue
        seen_engines.add(key)
        if row.get("compile_status") == "ok":
            try:
                expected[key] = resolve_repo_path(row.get("pdf_path", ""), paths.root)
            except ValueError as error:
                errors.append(f"{engine}/{sample_id}: {error}")
    expected_engine_keys = {(engine, sample_id) for engine in ENGINE_SYSTEMS for sample_id in heldout_ids}
    if seen_engines != expected_engine_keys:
        errors.append(
            "engine manifest does not cover each held-out ID for all three engines"
            f" (missing={sorted(expected_engine_keys - seen_engines)[:8]})"
        )
    return expected, errors


def _validate_run(
    paths: PublicationPaths, heldout_ids: set[str]
) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    config_path = paths.run_dir / "run_config.json"
    manifest_path = paths.run_dir / "run_manifest.csv"
    snapshot_path = paths.run_dir / "split_manifest.csv"
    config = read_json(config_path)
    manifest = read_csv(manifest_path)
    snapshot = read_csv(snapshot_path)
    manifest_ids, manifest_errors = _ids(
        manifest, label="frozen v1 run manifest", expected_count=EXPECTED_HELDOUT
    )
    snapshot_ids, snapshot_errors = _ids(
        snapshot, label="frozen v1 split snapshot", expected_count=EXPECTED_HELDOUT
    )
    errors.extend(manifest_errors)
    errors.extend(snapshot_errors)
    if manifest_ids != heldout_ids or snapshot_ids != heldout_ids:
        errors.append("frozen v1 run/snapshot IDs do not exactly match the canonical held-out split")
    exact_config = {
        "model": EXPECTED_MODEL,
        "split_path": repo_path(paths.heldout, paths.root),
        "split_count": EXPECTED_HELDOUT,
        "split_snapshot": "split_manifest.csv",
        "prompt_path": "prompts/latex_to_typst/system_v1.txt",
        "retry_prompt_path": "prompts/latex_to_typst/retry_v1.txt",
        "temperature": 0,
        "max_repairs": 1,
        "source_only": True,
        "reference_images_supplied": False,
    }
    for field, expected in exact_config.items():
        if config.get(field) != expected:
            errors.append(f"frozen v1 run_config {field}={config.get(field)!r}; expected {expected!r}")
    prompt = resolve_repo_path(str(config.get("prompt_path", "")), paths.root)
    retry_prompt = resolve_repo_path(str(config.get("retry_prompt_path", "")), paths.root)
    if text_sha256(paths.heldout) != config.get("split_sha256"):
        errors.append("frozen v1 run_config has stale held-out split hash")
    if text_sha256(prompt) != config.get("system_prompt_sha256"):
        errors.append("frozen v1 run_config has stale system prompt hash")
    if text_sha256(retry_prompt) != config.get("retry_prompt_sha256"):
        errors.append("frozen v1 run_config has stale retry prompt hash")
    if (paths.run_dir / "system_prompt.txt").read_text(encoding="utf-8") != prompt.read_text(encoding="utf-8"):
        errors.append("frozen v1 run-local system prompt differs from source prompt")
    if (paths.run_dir / "retry_prompt.txt").read_text(encoding="utf-8") != retry_prompt.read_text(encoding="utf-8"):
        errors.append("frozen v1 run-local retry prompt differs from source prompt")
    if paths.heldout.read_bytes() != snapshot_path.read_bytes():
        errors.append("frozen v1 split snapshot is not byte-identical to canonical held-out split")
    by_id = {row.get("sample_id", ""): row for row in manifest}
    for sample_id in sorted(heldout_ids & manifest_ids):
        row = by_id[sample_id]
        if row.get("status") != "finished":
            errors.append(f"{sample_id}: frozen v1 run is not finished")
        if row.get("requested_model") != EXPECTED_MODEL or row.get("resolved_model") != EXPECTED_MODEL:
            errors.append(f"{sample_id}: model identity differs from the frozen Gemini route")
        attempts = finite_number(row.get("attempts"))
        if attempts not in {1.0, 2.0}:
            errors.append(f"{sample_id}: attempts must be 1 or 2")
        sample_dir = paths.run_dir / "samples" / sample_id
        meta_path = sample_dir / "meta.json"
        if not meta_path.is_file():
            errors.append(f"{sample_id}: missing frozen run meta.json")
            continue
        meta = read_json(meta_path)
        for field in ("sample_id", "requested_model", "resolved_model", "attempts", "first_pass_compiled", "final_compiled"):
            manifest_value: Any = row.get(field)
            if field in {"attempts"}:
                manifest_value = int(float(str(manifest_value))) if finite_number(manifest_value) is not None else manifest_value
            elif field in {"first_pass_compiled", "final_compiled"}:
                manifest_value = parse_bool(manifest_value)
            if meta.get(field) != manifest_value:
                errors.append(f"{sample_id}: meta/run_manifest mismatch for {field}")
        records = meta.get("attempt_records")
        if not isinstance(records, list) or len(records) != attempts:
            errors.append(f"{sample_id}: attempt_records do not match attempts")
            continue
        if any(record.get("resolved_model") != EXPECTED_MODEL for record in records):
            errors.append(f"{sample_id}: an attempt resolved to a different model route")
        first_compile = bool(records[0].get("compile_ok"))
        if first_compile != bool(meta.get("first_pass_compiled")):
            errors.append(f"{sample_id}: first-pass compile state disagrees with attempt 1")
        successful = [record for record in records if record.get("compile_ok") is True]
        final_compile = bool(successful)
        if final_compile != bool(meta.get("final_compiled")):
            errors.append(f"{sample_id}: final compile state disagrees with attempts")
        if first_compile and not (sample_dir / "attempt_1.pdf").is_file():
            errors.append(f"{sample_id}: missing compiled first-pass PDF")
        output_pdf = sample_dir / "output.pdf"
        output_typ = sample_dir / "output.typ"
        if final_compile and (not output_pdf.is_file() or not output_typ.is_file()):
            errors.append(f"{sample_id}: final-compiled row lacks output.pdf/output.typ")
        if not final_compile and (output_pdf.exists() or output_typ.exists()):
            errors.append(f"{sample_id}: failed row has stale final output artifact")
        if final_compile:
            final_attempt = int(successful[-1]["attempt"])
            attempt_pdf = sample_dir / f"attempt_{final_attempt}.pdf"
            attempt_typ = sample_dir / f"attempt_{final_attempt}.typ"
            if not attempt_pdf.is_file() or not attempt_typ.is_file():
                errors.append(f"{sample_id}: successful final attempt artifacts are missing")
            else:
                if sha256(output_pdf) != sha256(attempt_pdf) or sha256(output_typ) != sha256(attempt_typ):
                    errors.append(f"{sample_id}: final output is not the successful frozen attempt")
    return manifest, errors


def _discover_metric_tables(scorecard: Mapping[str, Any], paths: PublicationPaths) -> list[Path]:
    _, recorded = validate_recorded_hashes(scorecard, root=paths.root)
    tables: list[Path] = []
    for path in recorded:
        if path.suffix.lower() != ".csv" or not path.is_file():
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                fields = set(next(csv.reader(handle)))
        except StopIteration:
            continue
        if {"sample_id", "v2_status", "v2_evidence_json"}.issubset(fields):
            tables.append(path)
    return sorted(set(tables))


def _median(values: Iterable[float]) -> float | None:
    ordered = sorted(values)
    if not ordered:
        return None
    middle = len(ordered) // 2
    return ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2


def _candidate_set_sha256(rows: Sequence[Mapping[str, str]]) -> str:
    records = [
        {
            "sample_id": row["sample_id"],
            "candidate_pdf": row["candidate_pdf"],
            "candidate_sha256": row["candidate_sha256"],
        }
        for row in rows
    ]
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def recompute_scorecard_rows(
    published_rows: Sequence[Mapping[str, str]],
    *,
    metric_rows: Sequence[Mapping[str, str]],
    expected_candidates: Mapping[tuple[str, str], Path],
    universe_n: int = EXPECTED_HELDOUT,
) -> list[dict[str, str]]:
    """Independently recompute every numeric publication cell from frozen rows."""

    template = {row["system_id"]: row for row in published_rows}
    output: list[dict[str, str]] = []
    for system in EXPECTED_SYSTEMS:
        rows = [row for row in metric_rows if row.get("system_id") == system]
        compiled_n = sum(key[0] == system for key in expected_candidates)
        page_exact = sum(finite_number(row.get("page_count_delta")) == 0 for row in rows)
        canvas_exact = sum(finite_number(row.get("canvas_exact_size_rate")) == 1 for row in rows)
        ssim = [
            value
            for row in rows
            if (value := finite_number(row.get("unregistered_ssim"))) is not None
        ]
        def values(field: str) -> list[float]:
            return [value for row in rows if (value := finite_number(row.get(field))) is not None]

        base = template[system]
        calculated: dict[str, Any] = {
            "system_id": system,
            "display_label": base["display_label"],
            "protocol_id": EXPECTED_PRIMARY_PROTOCOLS[system],
            "protocol_label": base["protocol_label"],
            "candidate_stage": base["candidate_stage"],
            "universe_n": universe_n,
            "compiled_n": compiled_n,
            "compile_rate": round(compiled_n / universe_n, 6),
            "page_exact_n": page_exact,
            "page_exact_rate_all": round(page_exact / universe_n, 6),
            "canvas_exact_n": canvas_exact,
            "canvas_exact_rate_compiled": round(canvas_exact / compiled_n, 6) if compiled_n else None,
            "strict_word_f1_median": round(value, 6) if (value := _median(values("strict_word_f1"))) is not None else None,
            "compatibility_word_f1_median": round(value, 6) if (value := _median(values("compatibility_word_f1"))) is not None else None,
            "reference_coverage_median": round(value, 6) if (value := _median(values("matched_word_reference_coverage"))) is not None else None,
            "center_displacement_q90_median": round(value, 6) if (value := _median(values("token_center_displacement_q90"))) is not None else None,
            "text_ltsim_median": round(value, 6) if (value := _median(values("text_ltsim_page_macro"))) is not None else None,
            "ssim_eligible_n": len(ssim),
            "ssim_median": round(value, 6) if (value := _median(ssim)) is not None else None,
            "fidelity_population": base["fidelity_population"],
            "candidate_set_sha256": _candidate_set_sha256(rows),
        }
        output.append({key: "" if value is None else str(value) for key, value in calculated.items()})
    return output


def _compare_recomputed(
    published: Sequence[Mapping[str, str]], recomputed: Sequence[Mapping[str, str]]
) -> list[str]:
    errors: list[str] = []
    for left, right in zip(published, recomputed):
        system = left.get("system_id", "")
        for field in SCORECARD_FIELDS:
            left_value = str(left.get(field, "")).strip()
            right_value = str(right.get(field, "")).strip()
            if field in SCORECARD_NUMERIC_FIELDS and left_value and right_value:
                left_number = finite_number(left_value)
                right_number = finite_number(right_value)
                equal = (
                    left_number is not None
                    and right_number is not None
                    and math.isclose(left_number, right_number, rel_tol=1e-12, abs_tol=1e-12)
                )
            else:
                equal = left_value == right_value
            if not equal:
                errors.append(
                    f"{system}: stale publication value {field}={left_value!r}; recomputed {right_value!r}"
                )
    return errors


def inspect(paths: PublicationPaths, *, require_publication_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    required = [
        paths.accepted,
        paths.prompt_dev,
        paths.heldout,
        paths.engine_manifest,
        paths.run_dir / "run_config.json",
        paths.run_dir / "run_manifest.csv",
        paths.run_dir / "split_manifest.csv",
        paths.run_dir / "system_prompt.txt",
        paths.run_dir / "retry_prompt.txt",
        paths.root / "prompts" / "latex_to_typst" / "system_v1.txt",
        paths.root / "prompts" / "latex_to_typst" / "retry_v1.txt",
        paths.root / "scripts" / "evaluation" / "pdf_metric_axes_v1.py",
        paths.root / "scripts" / "evaluation" / "pdf_metric_axes_v2.py",
        paths.root / "scripts" / "evaluation" / "evaluate_metric_v2_manifest.py",
        paths.root / "scripts" / "evaluation" / "build_publication_scorecard_v0.py",
        paths.statistics_analyzer,
        paths.root / "scripts" / "evaluation" / "build_publication_manuscript.py",
        paths.root / "scripts" / "evaluation" / "preflight_publication_v0.py",
        paths.report_source,
        paths.pdf_source,
        paths.report_pdf,
    ]
    publication_outputs = [
        paths.per_sample_csv,
        paths.scorecard_csv,
        paths.scorecard_json,
        paths.scorecard_summary,
        paths.publication_statistics,
        paths.paired_axis_results,
        paths.category_results,
    ]
    if require_publication_outputs:
        required.extend(publication_outputs)
    errors = [f"missing required artifact: {repo_path(path, paths.root)}" for path in required if not path.is_file()]
    report: dict[str, Any] = {
        "schema_version": "publication_v0_preflight_v1",
        "ready": False,
        "claim_boundaries": CLAIM_BOUNDARIES,
        "errors": errors,
    }
    if errors:
        return report, None, None

    accepted = read_csv(paths.accepted)
    prompt_dev = read_csv(paths.prompt_dev)
    heldout = read_csv(paths.heldout)
    errors.extend(validate_split_contract(accepted, prompt_dev, heldout))
    canonical_errors, canonical_sources, canonical_references = validate_canonical_artifacts(
        accepted, root=paths.root
    )
    errors.extend(canonical_errors)
    heldout_ids = {row["sample_id"] for row in heldout}
    run_manifest, run_errors = _validate_run(paths, heldout_ids)
    errors.extend(run_errors)
    engine_manifest = read_csv(paths.engine_manifest)
    expected_candidates, candidate_errors = _expected_candidate_maps(
        heldout_ids, run_manifest, engine_manifest, paths
    )
    errors.extend(candidate_errors)
    for (system, sample_id), path in expected_candidates.items():
        if not path.is_file():
            errors.append(f"{system}/{sample_id}: expected compiled candidate is missing")

    if not require_publication_outputs and not all(path.is_file() for path in publication_outputs):
        report["errors"] = errors
        report["fixture_outputs_skipped"] = True
        report["ready"] = not errors
        return report, None, None

    scorecard_rows = read_csv(paths.scorecard_csv)
    scorecard_json = read_json(paths.scorecard_json)
    per_sample_rows = read_csv(paths.per_sample_csv)
    statistics_json = read_json(paths.publication_statistics)
    paired_axis_rows = read_csv(paths.paired_axis_results)
    category_rows = read_csv(paths.category_results)
    errors.extend(validate_primary_rows(scorecard_rows))
    errors.extend(
        validate_statistics_artifacts(
            statistics_json,
            paired_axis_rows,
            category_rows,
            per_sample_rows=per_sample_rows,
            root=paths.root,
            per_sample_path=paths.per_sample_csv,
            paired_path=paths.paired_axis_results,
            category_path=paths.category_results,
        )
    )
    try:
        json_rows = _json_scorecard_rows(scorecard_json)
    except ValueError as error:
        errors.append(str(error))
        json_rows = []
    if json_rows:
        errors.extend(compare_scorecard_serializations(scorecard_rows, json_rows))
    try:
        from build_publication_manuscript import load_publication, render_manuscript
    except ImportError:
        from scripts.evaluation.build_publication_manuscript import load_publication, render_manuscript
    try:
        manuscript_document, manuscript_rows, statistics_document = load_publication(paths.output_dir)
        expected_manuscript = render_manuscript(
            manuscript_document, manuscript_rows, statistics_document
        )
        if paths.report_source.read_text(encoding="utf-8") != expected_manuscript:
            errors.append("publication report is stale relative to frozen scorecard artifacts")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors.append(f"publication report cannot be recomputed: {error}")
    hash_errors, recorded_artifacts = validate_recorded_hashes(scorecard_json, root=paths.root)
    errors.extend(hash_errors)
    mandatory_recorded = {
        paths.heldout.resolve(),
        (paths.run_dir / "split_manifest.csv").resolve(),
        (paths.run_dir / "run_config.json").resolve(),
        (paths.run_dir / "run_manifest.csv").resolve(),
        (paths.root / "prompts" / "latex_to_typst" / "system_v1.txt").resolve(),
        (paths.root / "prompts" / "latex_to_typst" / "retry_v1.txt").resolve(),
        paths.engine_manifest.resolve(),
        (paths.root / "scripts" / "evaluation" / "pdf_metric_axes_v2.py").resolve(),
    }
    if not mandatory_recorded.issubset(recorded_artifacts):
        missing = sorted(repo_path(path, paths.root) for path in mandatory_recorded - recorded_artifacts)
        errors.append(f"scorecard provenance omits mandatory frozen artifacts: {missing}")

    metric_tables = _discover_metric_tables(scorecard_json, paths)
    if not metric_tables:
        errors.append("scorecard provenance does not identify any metric-v2 score table")
        metric_rows: list[dict[str, str]] = []
        expected_references: dict[str, Path] = {}
    else:
        per_sample_errors, metric_rows, expected_references = validate_per_sample_rows(
            per_sample_rows,
            heldout=heldout,
            expected_candidates=expected_candidates,
            recorded_metric_tables=set(metric_tables),
            root=paths.root,
        )
        errors.extend(per_sample_errors)
    try:
        from evaluate_metric_v2_manifest import flatten as flatten_evidence
    except ImportError:
        from scripts.evaluation.evaluate_metric_v2_manifest import flatten as flatten_evidence
    if metric_rows:
        errors.extend(
            validate_metric_rows(
                metric_rows,
                expected_candidates=expected_candidates,
                expected_references=expected_references,
                root=paths.root,
                flatten_evidence=flatten_evidence,
            )
        )
        if not validate_primary_rows(scorecard_rows):
            recomputed = recompute_scorecard_rows(
                scorecard_rows,
                metric_rows=metric_rows,
                expected_candidates=expected_candidates,
            )
            errors.extend(_compare_recomputed(scorecard_rows, recomputed))

    report["errors"] = errors
    report["checks"] = {
        "canonical_ids": len(accepted),
        "prompt_dev_ids": len(prompt_dev),
        "heldout_ids": len(heldout),
        "primary_systems": list(EXPECTED_SYSTEMS),
        "expected_compiled_candidates": len(expected_candidates),
        "metric_rows": len(metric_rows),
        "metric_tables": [repo_path(path, paths.root) for path in metric_tables],
        "compile_rate_interval_rows": len(statistics_json.get("compile_rate_results", [])),
        "paired_axis_rows": len(paired_axis_rows),
        "category_rows": len(category_rows),
    }
    if errors:
        return report, None, None

    evidence_paths = [resolve_repo_path(row["v2_evidence_json"], paths.root) for row in metric_rows]
    release_manifest = {
        "schema_version": "publication_v0_release_manifest_v1",
        "status": "passed",
        "benchmark": {
            "accepted_n": EXPECTED_ACCEPTED,
            "prompt_dev_n": EXPECTED_PROMPT_DEV,
            "heldout_n": EXPECTED_HELDOUT,
            "prompt_dev_heldout_overlap_n": 0,
        },
        "primary_systems": list(EXPECTED_SYSTEMS),
        "protocol": {
            "model_route": EXPECTED_MODEL,
            "temperature": 0,
            "source_only": True,
            "reference_images_supplied": False,
            "maximum_compiler_error_repairs": 1,
            "adaptive_retry_stages": False,
        },
        "artifacts": {
            "accepted_manifest": _artifact(paths.accepted, paths.root),
            "prompt_dev_split": _artifact(paths.prompt_dev, paths.root),
            "heldout_split": _artifact(paths.heldout, paths.root),
            "run_config": _artifact(paths.run_dir / "run_config.json", paths.root),
            "run_manifest": _artifact(paths.run_dir / "run_manifest.csv", paths.root),
            "system_prompt": _artifact(paths.root / "prompts/latex_to_typst/system_v1.txt", paths.root),
            "retry_prompt": _artifact(paths.root / "prompts/latex_to_typst/retry_v1.txt", paths.root),
            "engine_manifest": _artifact(paths.engine_manifest, paths.root),
            "evaluator_v1": _artifact(paths.root / "scripts/evaluation/pdf_metric_axes_v1.py", paths.root),
            "evaluator_v2": _artifact(paths.root / "scripts/evaluation/pdf_metric_axes_v2.py", paths.root),
            "metric_runner": _artifact(paths.root / "scripts/evaluation/evaluate_metric_v2_manifest.py", paths.root),
            "scorecard_builder": _artifact(paths.root / "scripts/evaluation/build_publication_scorecard_v0.py", paths.root),
            "statistics_analyzer": _artifact(paths.statistics_analyzer, paths.root),
            "manuscript_builder": _artifact(paths.root / "scripts/evaluation/build_publication_manuscript.py", paths.root),
            "publication_preflight": _artifact(paths.root / "scripts/evaluation/preflight_publication_v0.py", paths.root),
            "scorecard_csv": _artifact(paths.scorecard_csv, paths.root),
            "per_sample_scores": _artifact(paths.per_sample_csv, paths.root),
            "scorecard_json": _artifact(paths.scorecard_json, paths.root),
            "scorecard_summary": _artifact(paths.scorecard_summary, paths.root),
            "publication_statistics": _artifact(paths.publication_statistics, paths.root),
            "paired_axis_results": _artifact(paths.paired_axis_results, paths.root),
            "category_results": _artifact(paths.category_results, paths.root),
            "report_source": _artifact(paths.report_source, paths.root),
            "pdf_source": _artifact(paths.pdf_source, paths.root),
            "report_pdf": _artifact(paths.report_pdf, paths.root),
        },
        "metric_inputs": _tree_digest(metric_tables, paths.root),
        "metric_evidence": _tree_digest(evidence_paths, paths.root),
        "canonical_sources": _tree_digest(canonical_sources, paths.root),
        "canonical_reference_pdfs": _tree_digest(canonical_references, paths.root),
        "compiled_candidate_pdfs": _tree_digest(expected_candidates.values(), paths.root),
    }
    scorecard_by_system = {row["system_id"]: row for row in scorecard_rows}
    claim_registry = {
        "schema_version": "publication_v0_claim_registry_v1",
        "claim_boundaries": CLAIM_BOUNDARIES,
        "claims": [
            {
                "claim_id": "canonical_corpus_and_split",
                "statement": "The canonical corpus contains 157 unique references split into 30 development and 127 held-out IDs with zero overlap.",
                "status": "verified",
                "evidence": [
                    release_manifest["artifacts"]["accepted_manifest"],
                    release_manifest["artifacts"]["prompt_dev_split"],
                    release_manifest["artifacts"]["heldout_split"],
                ],
            },
            {
                "claim_id": "frozen_v1_protocol",
                "statement": "The primary Gemini rows use the source-only frozen v1 run at temperature zero, shown at first pass and after at most one compiler-error repair.",
                "status": "verified",
                "evidence": [
                    release_manifest["artifacts"]["run_config"],
                    release_manifest["artifacts"]["run_manifest"],
                    release_manifest["artifacts"]["system_prompt"],
                    release_manifest["artifacts"]["retry_prompt"],
                ],
            },
            {
                "claim_id": "primary_table_scope",
                "statement": "The primary table contains only two frozen Gemini stages and three deterministic engines; development, adaptive v2/v3, and Claude rows are excluded.",
                "status": "verified",
                "systems": list(EXPECTED_SYSTEMS),
                "evidence": [release_manifest["artifacts"]["scorecard_csv"]],
            },
            {
                "claim_id": "paired_uncertainty",
                "statement": (
                    "Compile-rate intervals use all 127 held-out documents; paired fidelity "
                    "intervals compare the same eligible document IDs with a fixed 10,000-draw "
                    "document bootstrap and no overall scalar."
                ),
                "status": "verified",
                "evidence": [
                    release_manifest["artifacts"]["statistics_analyzer"],
                    release_manifest["artifacts"]["publication_statistics"],
                    release_manifest["artifacts"]["paired_axis_results"],
                    release_manifest["artifacts"]["category_results"],
                ],
            },
            *[
                {
                    "claim_id": f"scorecard_{system}",
                    "statement": (
                        f"{row['display_label']} compiled {row['compiled_n']}/127 held-out documents; "
                        "the accompanying fidelity statistics are medians over its compiled PDFs."
                    ),
                    "status": "verified",
                    "values": {field: row[field] for field in SCORECARD_FIELDS[5:]},
                    "evidence": [
                        release_manifest["artifacts"]["scorecard_csv"],
                        release_manifest["artifacts"]["scorecard_json"],
                    ],
                }
                for system in EXPECTED_SYSTEMS
                for row in [scorecard_by_system[system]]
            ],
        ],
    }
    report["ready"] = True
    return report, release_manifest, claim_registry


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    paths = PublicationPaths.from_root(args.root)
    report, release_manifest, claim_registry = inspect(paths)
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["ready"]:
        return 1
    if not args.check_only:
        assert release_manifest is not None and claim_registry is not None
        write_json(paths.output_dir / "release_manifest.json", release_manifest)
        write_json(paths.output_dir / "claim_registry.json", claim_registry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
