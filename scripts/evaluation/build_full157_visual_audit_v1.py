#!/usr/bin/env python3
"""Build one four-case visual-audit sheet for every benchmark source PDF."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

from build_pilot_visual_audit_v1 import (
    COMPOSITE_SIZE, PANEL_BOXES, _fit, _font, _render_page, build_composite,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "augmentation_results.csv"
DEFAULT_CATEGORY_RESULTS = ROOT / "results" / "metric_research_v1" / "category_audit_repeat_v1" / "augmentation_results.csv"
DEFAULT_OUTPUT = ROOT / "results" / "metric_research_v1" / "full_157_v1" / "visual_audit"
AUDIT_CASES = (
    ("text_deletion", "2"),
    ("block_right", "2"),
    ("local_occlusion", "2"),
)
CATEGORY_VARIANT = {
    "01_prose_sections": "paragraph_occlusion",
    "02_lists_formatting": "list_item_occlusion",
    "03_math_inline_display": "display_math_occlude",
    "04_math_aligned": "display_math_occlude",
    "05_tables_simple": "table_row_occlusion",
    "06_tables_moderate": "table_column_occlusion",
    "07_figures_captions": "figure_occlusion",
    "08_crossrefs_citations": "crossref_token_corruption",
    "09_algorithms": "algorithm_rule_occlusion",
    "10_compact_papers": "compact_block_displacement",
    "11_forms_cv_letters": "form_field_occlusion",
}
SHEET_SIZE = (COMPOSITE_SIZE[0] * 2, COMPOSITE_SIZE[1] * 2 + 70)


def _blind_composite(row: dict[str, str], case_id: str, candidate_panel: str) -> Image.Image:
    page = int(row["target_page"] or 0)
    reference = _render_page(Path(row["source_pdf"]), page)
    candidate = _render_page(Path(row["candidate_pdf"]), page)
    images = (candidate, reference) if candidate_panel == "A" else (reference, candidate)
    canvas = Image.new("RGB", COMPOSITE_SIZE, "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 18), f"CASE {case_id}", font=_font(30, True), fill=(22, 31, 43))
    draw.text((24, 60), "Which panel changed? Name the visible defect and its page region.",
              font=_font(22), fill=(40, 55, 72))
    draw.text((24, 96), "Mutation identity, expected axis, boxes, and scores are hidden.",
              font=_font(19), fill=(72, 83, 96))
    for label, image, box in zip(("PANEL A", "PANEL B"), images, PANEL_BOXES):
        fitted, placed = _fit(image, box)
        canvas.paste(fitted, placed[:2])
        draw.rectangle(placed, outline=(132, 142, 153), width=2)
        draw.text((placed[0], placed[1] - 26), label, font=_font(17, True), fill=(22, 31, 43))
        fitted.close()
    reference.close()
    candidate.close()
    return canvas


def _blind_order(selected: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    sample_ids = sorted(
        selected,
        key=lambda sample: hashlib.sha256(f"blind-v1:{sample}".encode()).hexdigest(),
    )
    rows_by_sample = {
        sample: sorted(
            selected[sample],
            key=lambda row: hashlib.sha256(f"blind-v1:{row['variant_id']}".encode()).hexdigest(),
        )
        for sample in sample_ids
    }
    if any(len(rows) != 4 for rows in rows_by_sample.values()):
        raise ValueError("blind ordering requires exactly four cases per source")
    step = max(1, len(sample_ids) // 4)
    ordered = []
    for sheet_index in range(len(sample_ids)):
        for case_index in range(4):
            sample = sample_ids[(sheet_index + case_index * step) % len(sample_ids)]
            ordered.append(rows_by_sample[sample][case_index])
    return ordered


def _candidate_panel(sheet_index: int, offset: int) -> str:
    return "A" if (sheet_index + offset) % 2 else "B"


def _selected(rows: list[dict[str, str]], category_rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_sample: dict[str, dict[tuple[str, str], dict[str, str]]] = defaultdict(dict)
    for row in rows:
        key = (row.get("variant", ""), row.get("severity", ""))
        if key in AUDIT_CASES:
            if not row.get("candidate_pdf"):
                raise ValueError(f"missing retained audit PDF for {row['sample_id']} {key}")
            by_sample[row["sample_id"]][key] = row
    missing = {
        sample: [key for key in AUDIT_CASES if key not in found]
        for sample, found in by_sample.items() if len(found) != len(AUDIT_CASES)
    }
    if missing:
        raise ValueError(f"incomplete audit cases: {missing}")
    category_by_sample = {}
    for row in category_rows:
        if row.get("severity") == "2" and row.get("variant") == CATEGORY_VARIANT.get(row.get("category")):
            if not row.get("candidate_pdf"):
                raise ValueError(f"missing retained category audit PDF for {row['sample_id']}")
            category_by_sample[row["sample_id"]] = row
    missing_category = sorted(set(by_sample) - set(category_by_sample))
    if missing_category:
        raise ValueError(f"missing category-aware audit cases: {missing_category}")
    return {
        sample: [found[key] for key in AUDIT_CASES] + [category_by_sample[sample]]
        for sample, found in by_sample.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--category-results", type=Path, default=DEFAULT_CATEGORY_RESULTS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--expected-samples", type=int, default=157)
    args = parser.parse_args()
    with args.results.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    with args.category_results.open(newline="", encoding="utf-8") as handle:
        category_rows = list(csv.DictReader(handle))
    selected = _selected(rows, category_rows)
    if len(selected) != args.expected_samples:
        raise ValueError(f"expected {args.expected_samples} samples, found {len(selected)}")

    blind_dir = args.out_dir / "blind"
    unblinded_dir = args.out_dir / "unblinded"
    blind_dir.mkdir(parents=True, exist_ok=True)
    unblinded_dir.mkdir(parents=True, exist_ok=True)
    answer_key = []
    unblinded_book = fitz.open()
    sample_count = len(selected)
    for sheet_index, (sample_id, sample_rows) in enumerate(sorted(selected.items()), 1):
        unblinded_sheet = Image.new("RGB", SHEET_SIZE, (238, 241, 244))
        unblinded_draw = ImageDraw.Draw(unblinded_sheet)
        unblinded_draw.text((24, 17), f"UNBLINDED EVIDENCE {sheet_index:03d}/{sample_count}  ·  {sample_id}",
                  font=_font(28, True), fill=(22, 31, 43))
        unblinded_path = unblinded_dir / f"sample_{sheet_index:03d}_{sample_id}.jpg"
        for case_index, row in enumerate(sample_rows, 1):
            case_id = row["variant_id"][:12].upper()
            unblinded_composite = build_composite(row, case_index)
            x = (case_index - 1) % 2 * COMPOSITE_SIZE[0]
            y = 70 + (case_index - 1) // 2 * COMPOSITE_SIZE[1]
            unblinded_sheet.paste(unblinded_composite, (x, y))
            unblinded_composite.close()
            answer_key.append({
                "case_id": case_id,
                "candidate_panel_hidden_truth": "",
                "sample_id": sample_id,
                "category": row["category"],
                "variant": row["variant"],
                "severity": row["severity"],
                "expected_axis": row["expected_axis"],
                "source_pdf": row["source_pdf"],
                "candidate_pdf": row["candidate_pdf"],
                "target_page": row["target_page"],
                "known_target_bbox": row["target_bbox"],
                "expected_page": row["expected_page"],
                "expected_bbox": row["expected_bbox"],
                "predicted_page": row["predicted_page"],
                "predicted_bbox": row["predicted_bbox"],
                "unblinded_sheet": sheet_index,
                "unblinded_image": str(unblinded_path),
                "candidate_valid": "",
                "mutation_visible": "",
                "target_box_correct": "",
                "label_correct": "",
                "predicted_box_useful": "",
                "reviewer": "LLM_research_audit",
                "review_notes": "",
            })
        unblinded_sheet.save(unblinded_path, quality=92, optimize=True)
        page = unblinded_book.new_page(width=1200, height=748)
        page.insert_image(page.rect, filename=str(unblinded_path))
        unblinded_sheet.close()

    case_ids = [row["case_id"] for row in answer_key]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("blind case IDs are not unique")
    answer_by_case = {row["case_id"]: row for row in answer_key}
    blind_rows = _blind_order(selected)
    blind_sheet_count = math.ceil(len(blind_rows) / 4)
    blind_responses = []
    blind_book = fitz.open()
    for start in range(0, len(blind_rows), 4):
        sheet_index = start // 4 + 1
        blind_sheet = Image.new("RGB", SHEET_SIZE, (238, 241, 244))
        blind_draw = ImageDraw.Draw(blind_sheet)
        blind_draw.text(
            (24, 17),
            f"BLINDED AUDIT SHEET {sheet_index:03d}/{blind_sheet_count}  ·  FOUR SHUFFLED A/B CASES",
            font=_font(28, True), fill=(22, 31, 43),
        )
        for offset, row in enumerate(blind_rows[start:start + 4]):
            blind_index = start + offset + 1
            case_id = row["variant_id"][:12].upper()
            candidate_panel = _candidate_panel(sheet_index, offset)
            composite = _blind_composite(row, case_id, candidate_panel)
            x = offset % 2 * COMPOSITE_SIZE[0]
            y = 70 + offset // 2 * COMPOSITE_SIZE[1]
            blind_sheet.paste(composite, (x, y))
            composite.close()
            answer_by_case[case_id]["candidate_panel_hidden_truth"] = candidate_panel
            blind_responses.append({
                "blind_index": blind_index,
                "blind_sheet": sheet_index,
                "sheet_position": offset + 1,
                "case_id": case_id,
                "changed_panel": "",
                "visible_defect_axis": "",
                "region_description": "",
                "confidence": "",
                "abstain": "",
                "review_notes": "",
                "reviewer": "LLM_research_audit",
            })
        blind_path = blind_dir / f"sheet_{sheet_index:03d}.jpg"
        blind_sheet.save(blind_path, quality=92, optimize=True)
        page = blind_book.new_page(width=1200, height=748)
        page.insert_image(page.rect, filename=str(blind_path))
        blind_sheet.close()
    blind_book_path = args.out_dir / "full157_blind_audit_book.pdf"
    unblinded_book_path = args.out_dir / "full157_unblinded_evidence_book.pdf"
    blind_book.save(blind_book_path, deflate=True, garbage=4)
    unblinded_book.save(unblinded_book_path, deflate=True, garbage=4)
    blind_book.close()
    unblinded_book.close()

    response_path = args.out_dir / "blind_response_manifest.csv"
    with response_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(blind_responses[0]))
        writer.writeheader()
        writer.writerows(blind_responses)
    answer_path = args.out_dir / "audit_answer_key.csv"
    with answer_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(answer_key[0]))
        writer.writeheader()
        writer.writerows(answer_key)
    summary = {
        "artifact_kind": "manual_audit_of_controlled_reference_perturbations_not_ai_outputs",
        "source_sheets": len(selected),
        "cases": len(answer_key),
        "universal_audit_cases": [f"{variant}:severity_{severity}" for variant, severity in AUDIT_CASES],
        "category_audit_variants": CATEGORY_VARIANT,
        "blind_book": str(blind_book_path),
        "unblinded_book": str(unblinded_book_path),
        "blind_response_manifest": str(response_path),
        "answer_key": str(answer_path),
        "candidate_panel_counts": {"A": len(answer_key) // 2, "B": len(answer_key) // 2},
    }
    (args.out_dir / "audit_build_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
