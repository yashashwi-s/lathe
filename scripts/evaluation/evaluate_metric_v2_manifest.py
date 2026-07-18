#!/usr/bin/env python3
"""Evaluate a CSV of reference/candidate PDF pairs with metric axes v2."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from pdf_metric_axes_v2 import evaluate_pdf_pair, serialize_path  # noqa: E402


METRIC_FIELDS = (
    "strict_word_f1",
    "strict_document_edit_similarity",
    "compatibility_word_f1",
    "compatibility_document_edit_similarity",
    "number_f1",
    "reference_number_count",
    "candidate_number_count",
    "number_exact",
    "operator_f1",
    "reference_operator_count",
    "candidate_operator_count",
    "operator_exact",
    "citation_f1",
    "reference_citation_count",
    "candidate_citation_count",
    "citation_exact",
    "matched_word_reference_coverage",
    "token_center_displacement_q50",
    "token_center_displacement_q90",
    "token_bbox_iou_q10",
    "block_transport_combined_similarity",
    "block_transport_geometry_similarity",
    "block_transport_content_similarity",
    "block_transport_cost",
    "text_ltsim_page_macro",
    "text_ltsim_worst_page",
    "reading_order_tau",
    "reading_order_reference_coverage",
    "style_coverage_hmean",
    "font_size_log_error_q90",
    "baseline_displacement_q90",
    "unregistered_ink_f1",
    "registered_ink_f1",
    "unregistered_ssim",
    "registered_ssim",
    "unregistered_multiscale_ssim_diagnostic",
    "registered_multiscale_ssim_diagnostic",
    "reference_page_count",
    "candidate_page_count",
    "page_count_delta",
    "page_break_f1",
    "canvas_exact_size_rate",
    "table_status",
    "formula_status",
    "figure_status",
)


def _get(value: dict[str, Any], path: str) -> Any:
    current: Any = value
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _finite(value: Any) -> Any:
    return value if not isinstance(value, float) or math.isfinite(value) else None


def flatten(result: dict[str, Any]) -> dict[str, Any]:
    paths = {
        "strict_word_f1": "axes.content.metrics.strict_nfc_token_inventory.f1",
        "strict_document_edit_similarity": "axes.content.metrics.strict_nfc_document_edit_similarity",
        "compatibility_word_f1": "axes.content.metrics.compatibility_nfkc_token_inventory.f1",
        "compatibility_document_edit_similarity": "axes.content.metrics.compatibility_nfkc_document_edit_similarity",
        "number_f1": "axes.critical_content.metrics.numbers.f1",
        "reference_number_count": "axes.critical_content.metrics.numbers.reference_count",
        "candidate_number_count": "axes.critical_content.metrics.numbers.candidate_count",
        "number_exact": "axes.critical_content.metrics.numbers.exact_match",
        "operator_f1": "axes.critical_content.metrics.operators.f1",
        "reference_operator_count": "axes.critical_content.metrics.operators.reference_count",
        "candidate_operator_count": "axes.critical_content.metrics.operators.candidate_count",
        "operator_exact": "axes.critical_content.metrics.operators.exact_match",
        "citation_f1": "axes.critical_content.metrics.citation_markers.f1",
        "reference_citation_count": "axes.critical_content.metrics.citation_markers.reference_count",
        "candidate_citation_count": "axes.critical_content.metrics.citation_markers.candidate_count",
        "citation_exact": "axes.critical_content.metrics.citation_markers.exact_match",
        "matched_word_reference_coverage": "axes.geometry.metrics.reference_match_coverage",
        "token_center_displacement_q50": "axes.geometry.metrics.center_displacement_q50",
        "token_center_displacement_q90": "axes.geometry.metrics.center_displacement_q90",
        "token_bbox_iou_q10": "axes.geometry.metrics.bbox_iou_q10",
        "block_transport_combined_similarity": "axes.block_transport.metrics.combined_transport_similarity_exp",
        "block_transport_geometry_similarity": "axes.block_transport.metrics.geometry_transport_similarity_exp",
        "block_transport_content_similarity": "axes.block_transport.metrics.content_transport_similarity_exp",
        "block_transport_cost": "axes.block_transport.metrics.combined_transport_cost",
        "text_ltsim_page_macro": "axes.text_ltsim.metrics.text_ltsim_page_macro",
        "text_ltsim_worst_page": "axes.text_ltsim.metrics.text_ltsim_worst_page",
        "reading_order_tau": "axes.reading_order.metrics.kendall_tau",
        "reading_order_reference_coverage": "axes.reading_order.metrics.reference_block_coverage",
        "style_coverage_hmean": "axes.typography.metrics.style_coverage_hmean",
        "font_size_log_error_q90": "axes.typography.metrics.font_size_abs_log_ratio_q90",
        "baseline_displacement_q90": "axes.typography.metrics.baseline_displacement_q90",
        "unregistered_ink_f1": "axes.raster_ink.metrics.unregistered_tolerant_ink_f1_macro",
        "registered_ink_f1": "axes.raster_ink.metrics.registered_tolerant_ink_f1_macro",
        "unregistered_ssim": "axes.raster_perceptual.metrics.unregistered_ssim_macro",
        "registered_ssim": "axes.raster_perceptual.metrics.registered_ssim_macro",
        "unregistered_multiscale_ssim_diagnostic": "axes.raster_perceptual.metrics.unregistered_multiscale_ssim_diagnostic_macro",
        "registered_multiscale_ssim_diagnostic": "axes.raster_perceptual.metrics.registered_multiscale_ssim_diagnostic_macro",
        "reference_page_count": "inputs.reference_page_count",
        "candidate_page_count": "inputs.candidate_page_count",
        "page_count_delta": "axes.pagination.metrics.page_count_delta",
        "page_break_f1": "axes.pagination.metrics.page_break_f1",
        "canvas_exact_size_rate": "axes.canvas.metrics.exact_paired_size_rate",
        "table_status": "axes.tables.status",
        "formula_status": "axes.formulas.status",
        "figure_status": "axes.figures.status",
    }
    return {name: _finite(_get(result, path)) for name, path in paths.items()}


def _resolve(path: str, base: Path) -> Path:
    value = Path(path).expanduser()
    return value.resolve() if value.is_absolute() else (base / value).resolve()


def _case_id(row: dict[str, str], index: int) -> str:
    for key in ("case_id", "comparison_id", "variant_id", "sample_id"):
        if row.get(key):
            return row[key]
    digest = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()[:12]
    return f"row_{index:05d}_{digest}"


def _asset_rows_to_pairs(
    rows: list[dict[str, str]],
    *,
    group_column: str,
    role_column: str,
    path_column: str,
    reference_role: str,
) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(row[group_column], []).append(row)
    pairs = []
    for group, assets in groups.items():
        references = [row for row in assets if row[role_column] == reference_role]
        if len(references) != 1:
            raise ValueError(f"{group}: expected exactly one {reference_role!r} asset")
        reference = references[0]
        for candidate in assets:
            if candidate is reference:
                continue
            pair = dict(candidate)
            pair["comparison_id"] = f"{group}__{candidate[role_column]}"
            pair["reference_pdf"] = reference[path_column]
            pair["candidate_pdf"] = candidate[path_column]
            pair["reference_display_label"] = reference.get("display_label", reference_role)
            pairs.append(pair)
    return pairs


def _evaluate(payload: tuple[int, dict[str, str], str, int]) -> tuple[int, dict[str, Any], dict[str, Any] | None]:
    index, row, base_text, dpi = payload
    base = Path(base_text)
    output = dict(row)
    output["v2_status"] = "failed"
    output["v2_error"] = ""
    reference = _resolve(row.get("reference_pdf") or row.get("source_pdf") or "", base)
    candidate = _resolve(row.get("candidate_pdf") or "", base)
    if row.get("reference_pdf"):
        output["reference_pdf"] = serialize_path(reference)
    if row.get("source_pdf"):
        output["source_pdf"] = serialize_path(reference)
    if row.get("candidate_pdf"):
        output["candidate_pdf"] = serialize_path(candidate)
    if row.get("sample_dir"):
        output["sample_dir"] = serialize_path(_resolve(row["sample_dir"], base))
    if row.get("pdf_path"):
        output["pdf_path"] = serialize_path(_resolve(row["pdf_path"], base))
    output["reference_pdf_resolved"] = serialize_path(reference)
    output["candidate_pdf_resolved"] = serialize_path(candidate)
    try:
        result = evaluate_pdf_pair(reference, candidate, render_dpi=dpi)
        output.update(flatten(result))
        output["v2_status"] = "scored"
        return index, output, result
    except Exception as error:  # preserved in the result table for fail-closed preflight
        output["v2_error"] = f"{type(error).__name__}: {error}"
        return index, output, None


def _ordered_map(function: Any, values: list[Any], workers: int) -> Iterable[Any]:
    if workers == 1:
        yield from map(function, values)
        return
    with ProcessPoolExecutor(max_workers=workers) as executor:
        yield from executor.map(function, values, chunksize=1)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=max(1, min(4, os.cpu_count() or 1)))
    parser.add_argument("--render-dpi", type=int, default=96)
    parser.add_argument("--asset-role-column")
    parser.add_argument("--asset-group-column", default="comparison_set_id")
    parser.add_argument("--asset-path-column", default="pdf_path")
    parser.add_argument("--reference-role", default="reference")
    parser.add_argument("--sample-id", action="append", default=[])
    parser.add_argument(
        "--self-reference",
        action="store_true",
        help="evaluate sample_dir/reference.pdf against itself for identity validation",
    )
    args = parser.parse_args()
    if args.workers < 1:
        raise SystemExit("--workers must be positive")
    manifest = args.manifest.resolve()
    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("manifest is empty")
    if args.sample_id:
        selected = set(args.sample_id)
        rows = [row for row in rows if row.get("sample_id") in selected]
        if not rows:
            raise SystemExit("no rows matched --sample-id")
    if args.asset_role_column:
        rows = _asset_rows_to_pairs(
            rows,
            group_column=args.asset_group_column,
            role_column=args.asset_role_column,
            path_column=args.asset_path_column,
            reference_role=args.reference_role,
        )
    if args.self_reference:
        for row in rows:
            reference = str(Path(row["sample_dir"]) / "reference.pdf")
            row["reference_pdf"] = reference
            row["candidate_pdf"] = reference
            row["comparison_id"] = f"{row.get('sample_id', 'sample')}__self"

    args.out_dir = args.out_dir.resolve()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = args.out_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    payloads = [(index, row, str(ROOT), args.render_dpi) for index, row in enumerate(rows)]
    evaluated: list[dict[str, Any]] = []
    failed = 0
    for index, row, result in _ordered_map(_evaluate, payloads, args.workers):
        case_id = _case_id(rows[index], index)
        evidence_path = evidence_dir / f"{case_id}.json"
        row["v2_evidence_json"] = serialize_path(evidence_path) if result is not None else ""
        if result is not None:
            evidence_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        else:
            failed += 1
        evaluated.append((index, row))
    evaluated.sort(key=lambda item: item[0])
    output_rows = [row for _, row in evaluated]
    fieldnames = list(rows[0]) + [
        "reference_pdf_resolved",
        "candidate_pdf_resolved",
        "v2_status",
        "v2_error",
        *METRIC_FIELDS,
        "v2_evidence_json",
    ]
    output_csv = args.out_dir / "metric_v2_scores.csv"
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output_rows)
    summary = {
        "evaluator": "pdf_metric_axes_v2",
        "manifest": serialize_path(manifest),
        "rows": len(rows),
        "scored": len(rows) - failed,
        "failed": failed,
        "render_dpi": args.render_dpi,
        "workers": args.workers,
        "aggregate_score": None,
    }
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
