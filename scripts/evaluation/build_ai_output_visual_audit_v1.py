#!/usr/bin/env python3
"""Build blind and evidence-rich visual audit books for every AI output."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path

import fitz
from PIL import Image, ImageDraw

from build_pilot_visual_audit_v1 import _draw_normalized, _fit, _font


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROFILE = ROOT / "results" / "metric_research_v1" / "corpus_profile_157.csv"
DEFAULT_SCORES = ROOT / "results" / "metric_research_v1" / "ai_outputs_frozen_v1" / "ai_output_axis_scores.csv"
DEFAULT_OUTPUT = ROOT / "results" / "metric_research_v1" / "ai_outputs_frozen_v1" / "visual_audit"
SIZE = (2400, 1600)
LEFT = (35, 310, 1170, 1560)
RIGHT = (1230, 310, 2365, 1560)
AXES = ("content", "layout", "typography", "appearance", "pagination", "structure")
AUDIT_SEED = 20260715


def _render_pages(path: Path, dpi: int = 95) -> list[Image.Image]:
    images = []
    with fitz.open(path) as document:
        for page in document:
            pixmap = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
            images.append(Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples))
    return images


def _bbox(value: str) -> tuple[float, float, float, float] | None:
    if not value:
        return None
    parsed = json.loads(value)
    return tuple(float(number) for number in parsed) if len(parsed) == 4 else None


def _page_grid(images: list[Image.Image], box: tuple[int, int, int, int]) -> list[tuple[int, int, int, int]]:
    count = max(1, len(images))
    columns = 1 if count == 1 else 2
    rows = math.ceil(count / columns)
    x0, y0, x1, y1 = box
    gap = 22
    width = (x1 - x0 - gap * (columns - 1)) // columns
    height = (y1 - y0 - gap * (rows - 1)) // rows
    return [
        (x0 + (index % columns) * (width + gap), y0 + (index // columns) * (height + gap),
         x0 + (index % columns) * (width + gap) + width,
         y0 + (index // columns) * (height + gap) + height)
        for index in range(count)
    ]


def _draw_document(canvas: Image.Image, path: Path, box: tuple[int, int, int, int],
                   highlight_page: int | None = None,
                   highlight_bbox: tuple[float, float, float, float] | None = None) -> None:
    draw = ImageDraw.Draw(canvas)
    images = _render_pages(path)
    for index, (image, slot) in enumerate(zip(images, _page_grid(images, box))):
        fitted, placed = _fit(image, slot)
        canvas.paste(fitted, placed[:2])
        draw.rectangle(placed, outline=(132, 142, 153), width=2)
        draw.rectangle((placed[0], placed[1], placed[0] + 82, placed[1] + 25), fill=(22, 31, 43))
        draw.text((placed[0] + 8, placed[1] + 2), f"PAGE {index + 1}", font=_font(15, True), fill="white")
        if index == highlight_page:
            _draw_normalized(draw, placed, highlight_bbox, (0, 158, 197), 5)
        fitted.close()
        image.close()


def _axis_text(row: dict[str, str]) -> str:
    values = []
    for axis in AXES:
        score = row.get(f"axis_{axis}", "")
        raw = "-" if not score else f"{float(score):.3f}"
        values.append(f"{axis.upper()} {raw} | {row.get(f'band_{axis}', 'abstain')}")
    return "    ".join(values)


def _blind_rows(profile: list[dict[str, str]], scores: dict[str, dict[str, str]]) -> list[tuple[dict[str, str], dict[str, str]]]:
    rows = [(row, scores[row["sample_id"]]) for row in profile if row["sample_id"] in scores]
    random.Random(AUDIT_SEED).shuffle(rows)
    return rows


def _canvas(row: dict[str, str], *, blind: bool) -> Image.Image:
    canvas = Image.new("RGB", SIZE, (238, 241, 244))
    draw = ImageDraw.Draw(canvas)
    sample = row["sample_id"]
    if blind:
        draw.text((35, 24), f"BLIND AI-OUTPUT AUDIT | CASE {row['audit_case_id']}",
                  font=_font(35, True), fill=(22, 31, 43))
        draw.text((35, 74), "Record visible content, layout, typography, pagination, and specialized-structure defects.",
                  font=_font(22), fill=(40, 55, 72))
        draw.text((35, 112), "Model, prompt stage, automatic axes, bands, and residual box are hidden.",
                  font=_font(20), fill=(72, 83, 96))
    else:
        draw.text((35, 24), f"AI OUTPUT EVIDENCE | {sample} | {row['category']}",
                  font=_font(35, True), fill=(22, 31, 43))
        draw.text((35, 73), f"MODEL  {row['ai_model_id']}    SELECTED PROMPT STAGE  {row['ai_selected_stage']}",
                  font=_font(23, True), fill=(40, 55, 72))
        draw.text((35, 112), (
            f"PROMPT  {row['ai_prompt_path']}    SHA256  {row['ai_system_prompt_sha256']}    "
            f"FINAL ATTEMPT  {row['ai_final_attempt']}"
        ), font=_font(17), fill=(40, 55, 72))
        draw.text((35, 148), _axis_text(row), font=_font(18), fill=(40, 55, 72))
        draw.text((35, 184), "AI severity labels disabled. Raw diagnostics only. Cyan = registered raster-residual enclosure.",
                  font=_font(18), fill=(72, 83, 96))
        draw.text((35, 218), f"Page count match: {row['page_count_match']}    Canvas sequence match: {row['canvas_match']}",
                  font=_font(18), fill=(72, 83, 96))
        draw.text((35, 250), (
            f"Residual page: {row.get('top_difference_page') or '-'}    "
            f"side: {row.get('top_difference_side') or '-'}    "
            f"frame: {row.get('top_difference_coordinate_frame') or '-'}    "
            f"registration px: {row.get('registration_translation_px') or '-'}"
        ), font=_font(17), fill=(72, 83, 96))
    draw.text((LEFT[0], LEFT[1] - 36), "REFERENCE PDF", font=_font(20, True), fill=(22, 31, 43))
    draw.text((RIGHT[0], RIGHT[1] - 36), "AI-GENERATED TYPST PDF" if not blind else "CANDIDATE PDF",
              font=_font(20, True), fill=(22, 31, 43))
    side = row.get("top_difference_side", "paired_reference_frame")
    page = int(row["top_difference_page"]) if row.get("top_difference_page") else None
    bbox = _bbox(row.get("top_difference_bbox", ""))
    _draw_document(
        canvas, ROOT / row["reference_pdf"], LEFT,
        None if blind or side == "candidate" else page,
        None if blind or side == "candidate" else bbox,
    )
    _draw_document(
        canvas, ROOT / row["candidate_pdf"], RIGHT,
        page if not blind and side == "candidate" else None,
        bbox if not blind and side == "candidate" else None,
    )
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--scores", type=Path, default=DEFAULT_SCORES)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    with args.profile.open(newline="", encoding="utf-8") as handle:
        profile = list(csv.DictReader(handle))
    with args.scores.open(newline="", encoding="utf-8") as handle:
        scores = {row["sample_id"]: row for row in csv.DictReader(handle)}
    blind_dir, evidence_dir = args.out_dir / "blind", args.out_dir / "unblinded"
    blind_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    blind_book, evidence_book = fitz.open(), fitz.open()
    responses = []
    answer_key = []
    for index, (row, score) in enumerate(_blind_rows(profile, scores), 1):
        case_id = f"AI{index:03d}"
        score["audit_case_id"] = case_id
        blind = _canvas(score, blind=True)
        evidence = _canvas(score, blind=False)
        blind_path = blind_dir / f"sample_{index:03d}.jpg"
        evidence_path = evidence_dir / f"sample_{index:03d}_{row['sample_id']}.jpg"
        blind.save(blind_path, quality=92, optimize=True)
        evidence.save(evidence_path, quality=92, optimize=True)
        for book, path in ((blind_book, blind_path), (evidence_book, evidence_path)):
            page = book.new_page(width=1200, height=800)
            page.insert_image(page.rect, filename=str(path))
        blind.close()
        evidence.close()
        responses.append({
            "audit_case_id": case_id,
            "blind_index": index,
            "content_issue": "",
            "layout_issue": "",
            "typography_issue": "",
            "pagination_issue": "",
            "specialized_issue": "",
            "severity_summary": "",
            "confidence": "",
            "review_notes": "",
            "reviewer": "LLM_research_audit",
        })
        answer_key.append({
            "audit_case_id": case_id,
            "audit_index": index,
            "sample_id": row["sample_id"],
            "category": row["category"],
            "model_hidden_truth": score["ai_model_id"],
            "resolved_model_hidden_truth": score["ai_resolved_model"],
            "selected_prompt_stage_hidden_truth": score["ai_selected_stage"],
            "prompt_path_hidden_truth": score["ai_prompt_path"],
            "system_prompt_sha256_hidden_truth": score["ai_system_prompt_sha256"],
            "final_attempt_hidden_truth": score["ai_final_attempt"],
            "candidate_compiled": "true",
            "top_residual_box_useful_after_unblind": "",
            "axis_labels_plausible_after_unblind": "",
            "canvas_confound": score["canvas_match"] == "false",
            "reviewer": "LLM_research_audit",
            "unblind_notes": "",
        })
    blind_path = args.out_dir / "ai_outputs_blind_audit_book.pdf"
    evidence_path = args.out_dir / "ai_outputs_unblinded_evidence_book.pdf"
    blind_book.save(blind_path, deflate=True, garbage=4)
    evidence_book.save(evidence_path, deflate=True, garbage=4)
    blind_book.close()
    evidence_book.close()
    response_path = args.out_dir / "blind_ai_response_manifest.csv"
    with response_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(responses[0]))
        writer.writeheader()
        writer.writerows(responses)
    answer_path = args.out_dir / "ai_audit_answer_key.csv"
    with answer_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(answer_key[0]))
        writer.writeheader()
        writer.writerows(answer_key)
    summary = {
        "artifact_kind": "llm_research_audit_not_human_ratings",
        "blind_order_seed": AUDIT_SEED,
        "compiled_ai_outputs": len(answer_key),
        "missing_ai_outputs": len(profile) - len(answer_key),
        "blind_book": str(blind_path),
        "unblinded_book": str(evidence_path),
        "blind_response_manifest": str(response_path),
        "answer_key": str(answer_path),
    }
    (args.out_dir / "audit_build_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
