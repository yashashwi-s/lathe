#!/usr/bin/env python3
"""Build the protocol-valid held-out publication scorecard."""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "results" / "publication_v0"
SPLIT = Path("data/latex_benchmark_v0/splits/heldout_clean_127.csv")
PROMPT_DEV = Path("data/latex_benchmark_v0/splits/prompt_dev_33.csv")
GEMINI_RUN = Path(
    "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/"
    "prompt_v1_heldout_clean"
)
ENGINE_MANIFEST = Path("results/latex_benchmark_v0/engine_manifest.csv")
GEMINI_METRICS = Path(
    "results/metric_research_v2/gemini_frozen_156/metric_v2_scores.csv"
)
ENGINE_METRICS = Path(
    "results/metric_research_v2/scorecards/engine_metric_v2/metric_v2_scores.csv"
)
RENDER_DPI = 96

ENGINE_LABELS = {
    "pandoc": "Pandoc",
    "tylax": "Tylax",
    "typetex": "TypeTeX",
}
EXPECTED_COMPILED = {
    "gemini_first_pass": 46,
    "gemini_after_one_repair": 77,
    "pandoc": 124,
    "tylax": 75,
    "typetex": 120,
}
SUMMARY_STAGES = {
    "gemini_first_pass": "attempt_1",
    "gemini_after_one_repair": "cumulative_after_at_most_one_repair",
    "pandoc": "as_tested_output",
    "tylax": "as_tested_output",
    "typetex": "as_tested_output",
}

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

PER_SAMPLE_FIELDS = (
    "sample_id",
    "category",
    "system_id",
    "display_label",
    "protocol_id",
    "protocol_label",
    "candidate_stage",
    "compiled",
    "compile_status",
    "compile_failure_class",
    "attempts_used",
    "repair_attempted",
    "reference_pdf",
    "reference_sha256",
    "candidate_pdf",
    "candidate_sha256",
    "metric_source_csv",
    "metric_source_evidence_json",
    "metric_v2_status",
    *METRIC_FIELDS,
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


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            {field: "" if row.get(field) is None else row.get(field, "") for field in fields}
            for row in rows
        )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _text_sha256(path: Path) -> str:
    """Match the runner's UTF-8 text hash (universal newlines, then UTF-8)."""

    return hashlib.sha256(path.read_text(encoding="utf-8").encode()).hexdigest()


def _repo_path(root: Path, value: str | Path) -> str:
    path = Path(value)
    resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"path escapes repository: {value}") from error


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    lowered = value.strip().lower()
    if lowered not in {"true", "false"}:
        raise ValueError(f"expected boolean text, got {value!r}")
    return lowered == "true"


def _number(row: dict[str, Any], field: str) -> float | None:
    value = row.get(field)
    if value in (None, ""):
        return None
    return float(value)


def _median(rows: list[dict[str, Any]], field: str) -> float | None:
    values = [value for row in rows if (value := _number(row, field)) is not None]
    return round(statistics.median(values), 6) if values else None


def _set_digest(rows: list[dict[str, Any]]) -> str:
    records = [
        {
            "sample_id": row["sample_id"],
            "candidate_pdf": row["candidate_pdf"],
            "candidate_sha256": row["candidate_sha256"],
        }
        for row in rows
        if row["compiled"] is True
    ]
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _artifact(path: Path, root: Path) -> dict[str, str]:
    return {"path": _repo_path(root, path), "sha256_raw_bytes": _sha256(path)}


def _metric_values(metric: dict[str, str] | None) -> dict[str, str]:
    if metric is None:
        return {field: "" for field in METRIC_FIELDS}
    return {field: metric.get(field, "") for field in METRIC_FIELDS}


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    first = rows[0]
    compiled = [row for row in rows if row["compiled"] is True]
    page_exact = sum(_number(row, "page_count_delta") == 0 for row in compiled)
    canvas_exact = sum(_number(row, "canvas_exact_size_rate") == 1 for row in compiled)
    ssim = [
        value for row in compiled
        if (value := _number(row, "unregistered_ssim")) is not None
    ]
    universe = len(rows)
    return {
        "system_id": first["system_id"],
        "display_label": first["display_label"],
        "protocol_id": first["protocol_id"],
        "protocol_label": first["protocol_label"],
        "candidate_stage": SUMMARY_STAGES[first["system_id"]],
        "universe_n": universe,
        "compiled_n": len(compiled),
        "compile_rate": round(len(compiled) / universe, 6),
        "page_exact_n": page_exact,
        "page_exact_rate_all": round(page_exact / universe, 6),
        "canvas_exact_n": canvas_exact,
        "canvas_exact_rate_compiled": (
            round(canvas_exact / len(compiled), 6) if compiled else None
        ),
        "strict_word_f1_median": _median(compiled, "strict_word_f1"),
        "compatibility_word_f1_median": _median(compiled, "compatibility_word_f1"),
        "reference_coverage_median": _median(
            compiled, "matched_word_reference_coverage"
        ),
        "center_displacement_q90_median": _median(
            compiled, "token_center_displacement_q90"
        ),
        "text_ltsim_median": _median(compiled, "text_ltsim_page_macro"),
        "ssim_eligible_n": len(ssim),
        "ssim_median": round(statistics.median(ssim), 6) if ssim else None,
        "fidelity_population": "compiled PDFs only (system-specific subset)",
        "candidate_set_sha256": _set_digest(compiled),
    }


def _score_row(
    *,
    sample: dict[str, str],
    system_id: str,
    display_label: str,
    protocol_id: str,
    protocol_label: str,
    candidate_stage: str,
    compiled: bool,
    failure: str,
    attempts_used: str | int,
    repair_attempted: bool | str,
    candidate: str,
    metric_source: Path,
    metric: dict[str, str] | None,
    root: Path,
) -> dict[str, Any]:
    reference = _repo_path(root, sample["reference_pdf"])
    candidate = _repo_path(root, candidate) if candidate else ""
    return {
        "sample_id": sample["sample_id"],
        "category": sample["category"],
        "system_id": system_id,
        "display_label": display_label,
        "protocol_id": protocol_id,
        "protocol_label": protocol_label,
        "candidate_stage": candidate_stage,
        "compiled": compiled,
        "compile_status": "compiled" if compiled else "failed",
        "compile_failure_class": "" if compiled else failure,
        "attempts_used": attempts_used,
        "repair_attempted": repair_attempted,
        "reference_pdf": reference,
        "reference_sha256": _sha256(root / reference),
        "candidate_pdf": candidate,
        "candidate_sha256": _sha256(root / candidate) if candidate else "",
        "metric_source_csv": _repo_path(root, metric_source) if metric else "",
        "metric_source_evidence_json": metric.get("v2_evidence_json", "") if metric else "",
        "metric_v2_status": metric.get("v2_status", "") if metric else "not_scored_uncompiled",
        **_metric_values(metric),
    }


def build_publication_data(root: Path = ROOT) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    split_path = root / SPLIT
    split_rows = _read_csv(split_path)
    split_ids = [row["sample_id"] for row in split_rows]
    heldout = set(split_ids)
    _require(len(split_ids) == 127, f"held-out split has {len(split_ids)} rows, expected 127")
    _require(len(heldout) == 127, "held-out split contains duplicate IDs")

    dev_ids = {row["sample_id"] for row in _read_csv(root / PROMPT_DEV)}
    leakage = sorted(heldout & dev_ids)
    _require(not leakage, f"prompt-development leakage: {leakage}")

    run_dir = root / GEMINI_RUN
    snapshot_path = run_dir / "split_manifest.csv"
    snapshot_rows = _read_csv(snapshot_path)
    snapshot_ids = {row["sample_id"] for row in snapshot_rows}
    _require(snapshot_ids == heldout, "Gemini split snapshot IDs differ from held-out split")
    _require(split_path.read_bytes() == snapshot_path.read_bytes(), "split snapshot bytes differ")

    run_config_path = run_dir / "run_config.json"
    run_config = json.loads(run_config_path.read_text(encoding="utf-8"))
    _require(run_config["split_path"] == SPLIT.as_posix(), "Gemini run used a different split")
    _require(run_config["split_count"] == 127, "Gemini run config split count is not 127")
    _require(run_config["temperature"] == 0, "Gemini temperature is not zero")
    _require(run_config["max_repairs"] == 1, "Gemini run did not allow exactly one repair")
    _require(run_config["source_only"] is True, "Gemini run was not source-only")
    _require(
        run_config["reference_images_supplied"] is False,
        "Gemini run received reference images",
    )
    _require(run_config["split_sha256"] == _text_sha256(split_path), "split text hash mismatch")
    prompt_path = root / run_config["prompt_path"]
    retry_path = root / run_config["retry_prompt_path"]
    _require(
        run_config["system_prompt_sha256"] == _text_sha256(prompt_path),
        "system prompt hash mismatch",
    )
    _require(
        run_config["retry_prompt_sha256"] == _text_sha256(retry_path),
        "retry prompt hash mismatch",
    )
    _require(
        (run_dir / "system_prompt.txt").read_text(encoding="utf-8")
        == prompt_path.read_text(encoding="utf-8"),
        "run-local system prompt differs from source prompt",
    )
    _require(
        (run_dir / "retry_prompt.txt").read_text(encoding="utf-8")
        == retry_path.read_text(encoding="utf-8"),
        "run-local retry prompt differs from source prompt",
    )

    run_manifest_path = run_dir / "run_manifest.csv"
    run_rows = _read_csv(run_manifest_path)
    _require(len(run_rows) == 127, "Gemini run manifest does not contain 127 rows")
    _require(
        {row["sample_id"] for row in run_rows} == heldout,
        "Gemini run manifest IDs differ from held-out IDs",
    )
    run_by_id = {row["sample_id"]: row for row in run_rows}

    gemini_metric_path = root / GEMINI_METRICS
    gemini_metric_rows = _read_csv(gemini_metric_path)
    clean_prefix = GEMINI_RUN.as_posix() + "/samples/"
    exact_gemini_metrics = [
        row for row in gemini_metric_rows
        if row.get("candidate_pdf", "").startswith(clean_prefix)
    ]
    _require(len(exact_gemini_metrics) == 77, "expected 77 exact clean-run Gemini metrics")
    gemini_metrics_by_id = {row["sample_id"]: row for row in exact_gemini_metrics}
    _require(len(gemini_metrics_by_id) == 77, "duplicate clean-run Gemini metric rows")

    metas: dict[str, dict[str, Any]] = {}
    first_pass_ids: set[str] = set()
    final_ids: set[str] = set()
    repaired_ids: set[str] = set()
    for sample_id in split_ids:
        manifest = run_by_id[sample_id]
        meta_path = run_dir / "samples" / sample_id / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        metas[sample_id] = meta
        first_pass = _bool(manifest["first_pass_compiled"])
        final = _bool(manifest["final_compiled"])
        _require(meta["first_pass_compiled"] is first_pass, f"{sample_id}: first-pass mismatch")
        _require(meta["final_compiled"] is final, f"{sample_id}: final status mismatch")
        _require(meta["requested_model"] == run_config["model"], f"{sample_id}: model mismatch")
        if first_pass:
            first_pass_ids.add(sample_id)
        if final:
            final_ids.add(sample_id)
            expected_candidate = (
                GEMINI_RUN / "samples" / sample_id / "output.pdf"
            ).as_posix()
            metric = gemini_metrics_by_id.get(sample_id)
            _require(metric is not None, f"{sample_id}: missing clean-run metric row")
            _require(metric["candidate_pdf"] == expected_candidate, f"{sample_id}: candidate path mismatch")
            _require(metric["v2_status"] == "scored", f"{sample_id}: metric-v2 was not scored")
            _require(metric.get("ai_selected_stage") == "v1", f"{sample_id}: non-v1 metric row")
            _require(
                metric.get("ai_system_prompt_sha256") == run_config["system_prompt_sha256"],
                f"{sample_id}: score row prompt hash mismatch",
            )
            attempt = 1 if first_pass else 2
            _require(
                _sha256(root / expected_candidate)
                == _sha256(run_dir / "samples" / sample_id / f"attempt_{attempt}.pdf"),
                f"{sample_id}: output PDF is not the recorded successful attempt",
            )
            if attempt == 2:
                repaired_ids.add(sample_id)
        else:
            _require(sample_id not in gemini_metrics_by_id, f"{sample_id}: failed output was scored")

    _require(first_pass_ids <= final_ids, "first-pass successes are not a subset of final successes")
    _require(final_ids == set(gemini_metrics_by_id), "Gemini final/metric ID sets differ")

    engine_manifest_path = root / ENGINE_MANIFEST
    engine_manifest_rows = _read_csv(engine_manifest_path)
    engine_by_key = {
        (row["sample_id"], row["engine"]): row
        for row in engine_manifest_rows
        if row["sample_id"] in heldout and row["engine"] in ENGINE_LABELS
    }
    _require(len(engine_by_key) == 127 * 3, "engine manifest is incomplete on held-out IDs")

    engine_metric_path = root / ENGINE_METRICS
    engine_metric_rows = _read_csv(engine_metric_path)
    engine_metrics_by_key = {
        (row["sample_id"], row["system_id"]): row
        for row in engine_metric_rows
        if row["sample_id"] in heldout and row["system_id"] in ENGINE_LABELS
    }

    per_sample: list[dict[str, Any]] = []
    for sample in split_rows:
        sample_id = sample["sample_id"]
        meta = metas[sample_id]
        first_pass = sample_id in first_pass_ids
        final = sample_id in final_ids
        repair_attempted = int(meta["attempts"]) == 2
        first_failure = ""
        if not first_pass:
            attempts = meta.get("attempt_records") or []
            first_failure = (
                attempts[0].get("error_class", "") if attempts else meta.get("error_class", "")
            )
        gemini_metric = gemini_metrics_by_id.get(sample_id)
        candidate = (
            (GEMINI_RUN / "samples" / sample_id / "output.pdf").as_posix()
            if first_pass else ""
        )
        per_sample.append(_score_row(
            sample=sample,
            system_id="gemini_first_pass",
            display_label="Gemini 3.1 Flash Lite — first pass",
            protocol_id="gemini_prompt_v1_first_pass",
            protocol_label="source-only prompt v1; first compiler attempt; no repair credited",
            candidate_stage="attempt_1",
            compiled=first_pass,
            failure=first_failure,
            attempts_used=1,
            repair_attempted=False,
            candidate=candidate,
            metric_source=GEMINI_METRICS,
            metric=gemini_metric if first_pass else None,
            root=root,
        ))
        candidate = (
            (GEMINI_RUN / "samples" / sample_id / "output.pdf").as_posix()
            if final else ""
        )
        stage = "attempt_1" if first_pass else "attempt_2_repair" if final else "no_compiled_pdf"
        per_sample.append(_score_row(
            sample=sample,
            system_id="gemini_after_one_repair",
            display_label="Gemini 3.1 Flash Lite — after ≤1 repair",
            protocol_id="gemini_prompt_v1_after_one_compiler_repair",
            protocol_label="source-only prompt v1; first attempt plus at most one compiler-error repair",
            candidate_stage=stage,
            compiled=final,
            failure=meta.get("error_class", "") or meta.get("status", "failed"),
            attempts_used=meta["attempts"],
            repair_attempted=repair_attempted,
            candidate=candidate,
            metric_source=GEMINI_METRICS,
            metric=gemini_metric if final else None,
            root=root,
        ))

        for engine, label in ENGINE_LABELS.items():
            manifest = engine_by_key[(sample_id, engine)]
            compiled = manifest["compile_status"] == "ok"
            metric = engine_metrics_by_key.get((sample_id, engine))
            if compiled:
                _require(metric is not None, f"{sample_id}/{engine}: missing metric row")
                _require(metric["v2_status"] == "scored", f"{sample_id}/{engine}: metric failed")
                expected_candidate = _repo_path(root, manifest["pdf_path"])
                _require(
                    metric["candidate_pdf"] == expected_candidate,
                    f"{sample_id}/{engine}: metric candidate path mismatch",
                )
            else:
                _require(metric is None, f"{sample_id}/{engine}: failed engine output was scored")
            per_sample.append(_score_row(
                sample=sample,
                system_id=engine,
                display_label=label,
                protocol_id=f"deterministic_{engine}_as_tested",
                protocol_label="deterministic archived engine output; executable version not recorded",
                candidate_stage="as_tested_output",
                compiled=compiled,
                failure=(
                    f"conversion={manifest['conversion_status']};compile={manifest['compile_status']}"
                ),
                attempts_used="",
                repair_attempted="",
                candidate=manifest["pdf_path"] if compiled else "",
                metric_source=ENGINE_METRICS,
                metric=metric,
                root=root,
            ))

    system_order = (
        "gemini_first_pass",
        "gemini_after_one_repair",
        "pandoc",
        "tylax",
        "typetex",
    )
    scorecard = [
        _summarize([row for row in per_sample if row["system_id"] == system_id])
        for system_id in system_order
    ]
    actual_counts = {row["system_id"]: row["compiled_n"] for row in scorecard}
    _require(actual_counts == EXPECTED_COMPILED, f"compile counts changed: {actual_counts}")
    _require(len(per_sample) == 127 * 5, "per-sample score table is not 127 x 5")

    requested_models = sorted({metas[sample_id]["requested_model"] for sample_id in split_ids})
    resolved_models = sorted({
        attempt.get("resolved_model", "")
        for meta in metas.values()
        for attempt in meta.get("attempt_records", [])
        if attempt.get("resolved_model")
    })
    provenance = {
        "hash_algorithm": "SHA-256",
        "hash_semantics": {
            "sha256_raw_bytes": "digest of exact file bytes",
            "sha256_text_normalized_lf": (
                "UTF-8 text after Python universal-newline normalization; matches run_config"
            ),
            "candidate_set_sha256": (
                "digest of canonical JSON records: sample_id, candidate path, candidate raw hash"
            ),
        },
        "inputs": {
            "heldout_split": {
                **_artifact(split_path, root),
                "sha256_text_normalized_lf": _text_sha256(split_path),
            },
            "gemini_split_snapshot": {
                **_artifact(snapshot_path, root),
                "sha256_text_normalized_lf": _text_sha256(snapshot_path),
            },
            "prompt_dev_split": _artifact(root / PROMPT_DEV, root),
            "gemini_run_config": _artifact(run_config_path, root),
            "gemini_run_manifest": _artifact(run_manifest_path, root),
            "system_prompt": {
                **_artifact(prompt_path, root),
                "sha256_text_normalized_lf": _text_sha256(prompt_path),
            },
            "retry_prompt": {
                **_artifact(retry_path, root),
                "sha256_text_normalized_lf": _text_sha256(retry_path),
            },
            "engine_manifest": _artifact(engine_manifest_path, root),
            "gemini_metric_v2_scores": _artifact(gemini_metric_path, root),
            "engine_metric_v2_scores": _artifact(engine_metric_path, root),
            "metric_v2_implementation": _artifact(
                root / "scripts/evaluation/pdf_metric_axes_v2.py", root
            ),
            "metric_v2_manifest_evaluator": _artifact(
                root / "scripts/evaluation/evaluate_metric_v2_manifest.py", root
            ),
            "engine_conversion_script": _artifact(
                root / "scripts/dataset/convert_all_v0_engines.py", root
            ),
            "typetex_filter": _artifact(root / "scripts/dataset/typetex_filter.lua", root),
        },
        "gemini": {
            "requested_model_routes": requested_models,
            "resolved_model_routes": resolved_models,
            "immutable_provider_checkpoint": None,
            "model_identity_limit": "API route recorded; immutable provider checkpoint not supplied",
            "temperature": run_config["temperature"],
            "max_repairs": run_config["max_repairs"],
            "source_only": run_config["source_only"],
            "reference_images_supplied": run_config["reference_images_supplied"],
            "typst_version": run_config["typst_version"],
        },
        "engines": {
            engine: {
                "protocol_id": f"deterministic_{engine}_as_tested",
                "executable_version": None,
                "version_limit": "not recorded; archived outputs are scored as tested",
            }
            for engine in ENGINE_LABELS
        },
        "metric": {
            "evaluator": "pdf_metric_axes_v2",
            "render_dpi": RENDER_DPI,
            "aggregate_score": None,
        },
    }
    validation = {
        "heldout_ids_n": len(heldout),
        "heldout_ids_unique": True,
        "gemini_run_ids_exactly_match_heldout": True,
        "gemini_split_snapshot_bytes_match_canonical": True,
        "prompt_dev_overlap_n": len(leakage),
        "prompt_dev_overlap_ids": leakage,
        "all_gemini_candidates_under_prompt_v1_heldout_clean": True,
        "all_gemini_metric_rows_prompt_stage_v1": True,
        "adaptive_v0_v2_v3_rows_used": 0,
        "claude_rows_used": 0,
        "first_pass_compiled_n": len(first_pass_ids),
        "repair_attempted_n": sum(int(meta["attempts"]) == 2 for meta in metas.values()),
        "repair_success_n": len(repaired_ids),
        "after_one_repair_compiled_n": len(final_ids),
        "expected_compiled_n": EXPECTED_COMPILED,
        "actual_compiled_n": actual_counts,
        "metric_rows_cover_every_compiled_pdf": True,
        "failed_outputs_have_empty_fidelity_axes": True,
    }
    document = {
        "schema_version": "publication_scorecard_v0.1",
        "benchmark": {
            "name": "LaTeX-to-Typst held-out benchmark v0",
            "universe_n": 127,
            "split": SPLIT.as_posix(),
            "protocol": (
                "Frozen source-only Gemini prompt v1, reported before and after at most one "
                "compiler-error repair; deterministic engines restricted to the same 127 IDs"
            ),
            "compile_denominator": "all 127 held-out references",
            "fidelity_population": "compiled PDFs only, separately for each system",
            "overall_scalar_score": None,
        },
        "provenance": provenance,
        "validation": validation,
        "artifacts": {},
        "scorecard": scorecard,
    }
    return document, per_sample


def _format_metric(value: Any) -> str:
    return "—" if value is None else f"{float(value):.3f}"


def _markdown(document: dict[str, Any]) -> str:
    rows = document["scorecard"]
    lines = [
        "# Publication benchmark scorecard v0",
        "",
        "This is the primary frozen 127-reference held-out comparison. Gemini uses only the "
        "source-only `prompt_v1_heldout_clean` run. Its first pass and cumulative result after "
        "at most one compiler-error repair are reported separately. Claude and the adaptive "
        "v0/v2/v3 cascade are excluded.",
        "",
        "## Compile and exact-document outcomes",
        "",
        "| System | Compiled / 127 | Page count exact / 127 | Canvas exact / compiled |",
        "|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['display_label']} | {row['compiled_n']}/127 "
            f"({100 * row['compile_rate']:.1f}%) | {row['page_exact_n']}/127 "
            f"| {row['canvas_exact_n']}/{row['compiled_n']} |"
        )
    lines.extend([
        "",
        "## Fidelity medians on compiled PDFs",
        "",
        "| System | Strict text F1 ↑ | NFKC text F1 ↑ | Reference coverage ↑ | Center q90 ↓ | Text-LTSim ↑ | SSIM ↑ (eligible n) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ])
    for row in rows:
        lines.append(
            f"| {row['display_label']} | {_format_metric(row['strict_word_f1_median'])} "
            f"| {_format_metric(row['compatibility_word_f1_median'])} "
            f"| {_format_metric(row['reference_coverage_median'])} "
            f"| {_format_metric(row['center_displacement_q90_median'])} "
            f"| {_format_metric(row['text_ltsim_median'])} "
            f"| {_format_metric(row['ssim_median'])} ({row['ssim_eligible_n']}) |"
        )
    split_hash = document["provenance"]["inputs"]["heldout_split"][
        "sha256_text_normalized_lf"
    ]
    prompt_hash = document["provenance"]["inputs"]["system_prompt"][
        "sha256_text_normalized_lf"
    ]
    lines.extend([
        "",
        "## Reading the table",
        "",
        "Compilation and exact-page counts always retain all 127 references. Fidelity medians "
        "are conditional on that system producing a compiled PDF, so they are not a paired "
        "ranking and are never collapsed into one overall score. SSIM abstains when page canvas "
        "sizes are incompatible.",
        "",
        f"Split text SHA-256: `{split_hash}`  ",
        f"System prompt SHA-256: `{prompt_hash}`  ",
        f"Metric: `pdf_metric_axes_v2` at {RENDER_DPI} DPI.",
        "",
        "Exact per-reference statuses, hashes, metrics, and evidence paths are in "
        "`per_sample_scores.csv`; complete protocol hashes and validation gates are in "
        "`scorecard.json`.",
        "",
    ])
    return "\n".join(lines)


def write_publication_outputs(root: Path = ROOT, out_dir: Path | None = None) -> dict[str, Any]:
    out_dir = out_dir or root / "results" / "publication_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    document, per_sample = build_publication_data(root)
    scorecard_csv = out_dir / "scorecard.csv"
    per_sample_csv = out_dir / "per_sample_scores.csv"
    summary_md = out_dir / "summary.md"
    _write_csv(per_sample_csv, per_sample, PER_SAMPLE_FIELDS)
    _write_csv(scorecard_csv, document["scorecard"], SCORECARD_FIELDS)
    summary_md.write_text(_markdown(document), encoding="utf-8")
    document["artifacts"] = {
        "per_sample_scores": _artifact(per_sample_csv, root),
        "scorecard_csv": _artifact(scorecard_csv, root),
        "summary_markdown": _artifact(summary_md, root),
    }
    json_path = out_dir / "scorecard.json"
    json_path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return document


def main() -> int:
    document = write_publication_outputs()
    print(json.dumps({
        "output_dir": _repo_path(ROOT, OUT_DIR),
        "compiled": document["validation"]["actual_compiled_n"],
        "prompt_dev_overlap_n": document["validation"]["prompt_dev_overlap_n"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
