#!/usr/bin/env python3
"""Render every retained pilot mutation for a manual, box-aware visual audit."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS = ROOT / "results" / "metric_research_v1" / "pilot_11_v2" / "augmentation_results.csv"
DEFAULT_OUTPUT = ROOT / "results" / "metric_research_v1" / "pilot_11_v2" / "visual_audit"
COMPOSITE_SIZE = (1500, 900)
PANEL_BOXES = ((24, 180, 730, 870), (770, 180, 1476, 870))


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}", size)


def _render_page(path: Path, page_index: int, dpi: int = 110) -> Image.Image:
    with fitz.open(path) as document:
        page_index = min(max(0, page_index), document.page_count - 1)
        pixmap = document[page_index].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
    return Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)


def _fit(image: Image.Image, box: tuple[int, int, int, int]) -> tuple[Image.Image, tuple[int, int, int, int]]:
    x0, y0, x1, y1 = box
    scale = min((x1 - x0) / image.width, (y1 - y0) / image.height)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    resized = image.resize(size, Image.Resampling.LANCZOS)
    left = x0 + (x1 - x0 - size[0]) // 2
    top = y0 + (y1 - y0 - size[1]) // 2
    return resized, (left, top, left + size[0], top + size[1])


def _bbox(value: str) -> tuple[float, float, float, float] | None:
    if not value:
        return None
    parsed = json.loads(value)
    return tuple(float(number) for number in parsed) if len(parsed) == 4 else None


def _draw_normalized(draw: ImageDraw.ImageDraw, image_box: tuple[int, int, int, int],
                     bbox: tuple[float, float, float, float] | None,
                     color: tuple[int, int, int], width: int) -> None:
    if bbox is None:
        return
    x0, y0, x1, y1 = image_box
    rect = (
        x0 + bbox[0] * (x1 - x0), y0 + bbox[1] * (y1 - y0),
        x0 + bbox[2] * (x1 - x0), y0 + bbox[3] * (y1 - y0),
    )
    draw.rectangle(rect, outline=color, width=width)


def _score_text(row: dict[str, str]) -> str:
    names = [name for name in row["expected_axis"].split("+") if name]
    values = []
    for name in names:
        value = row.get(f"axis_{name}", "")
        if value:
            values.append(f"{name}={float(value):.3f}")
    return "  ".join(values) or "invariant control"


def build_composite(row: dict[str, str], index: int) -> Image.Image:
    target_page = int(row["target_page"] or 0)
    reference = _render_page(Path(row["source_pdf"]), target_page)
    candidate = _render_page(Path(row["candidate_pdf"]), target_page)
    canvas = Image.new("RGB", COMPOSITE_SIZE, "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((24, 18), f"{index:03d}  {row['sample_id']}", font=_font(30, True), fill=(22, 31, 43))
    draw.text((24, 58), f"{row['family']}  /  {row['variant']}  /  severity {row['severity']}",
              font=_font(23), fill=(40, 55, 72))
    draw.text((24, 92), f"Expected: {row['expected_axis']}   {_score_text(row)}",
              font=_font(21), fill=(40, 55, 72))
    draw.text((24, 124), "Red = known synthetic edit region   Cyan = registered raster-residual enclosure",
              font=_font(18), fill=(72, 83, 96))
    target_bbox = _bbox(row["target_bbox"])
    same_page = str(row.get("predicted_page", "")) == str(target_page)
    local_same_page = row.get("localization_applicable", "").lower() == "true" and same_page
    predicted_bbox = _bbox(row["predicted_bbox"]) if local_same_page else None
    for label, image, box, predicted in (
        ("REFERENCE FRAME", reference, PANEL_BOXES[0], predicted_bbox),
        ("CONTROLLED CANDIDATE", candidate, PANEL_BOXES[1], None),
    ):
        fitted, placed = _fit(image, box)
        canvas.paste(fitted, placed[:2])
        draw.rectangle(placed, outline=(132, 142, 153), width=2)
        draw.text((placed[0], placed[1] - 26), label, font=_font(17, True), fill=(22, 31, 43))
        _draw_normalized(draw, placed, target_bbox, (220, 44, 52), 5)
        _draw_normalized(draw, placed, predicted, (0, 158, 197), 4)
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    with args.results.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get("candidate_pdf")]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    composites = []
    manifest = []
    for index, row in enumerate(rows, 1):
        composite = build_composite(row, index)
        path = args.out_dir / f"case_{index:03d}.jpg"
        composite.save(path, quality=92)
        composites.append(composite)
        manifest.append({
            "audit_index": index, "sample_id": row["sample_id"], "category": row["category"],
            "family": row["family"], "variant": row["variant"], "severity": row["severity"],
            "expected_axis": row["expected_axis"], "candidate_pdf": row["candidate_pdf"],
            "target_box_correct": "", "mutation_visible": "", "candidate_valid": "",
            "label_correct": "", "predicted_box_useful": "", "review_notes": "",
        })
    contact_paths = []
    for start in range(0, len(composites), 4):
        sheet = Image.new("RGB", (COMPOSITE_SIZE[0] * 2, COMPOSITE_SIZE[1] * 2), (238, 241, 244))
        for offset, composite in enumerate(composites[start:start + 4]):
            sheet.paste(composite, ((offset % 2) * COMPOSITE_SIZE[0], (offset // 2) * COMPOSITE_SIZE[1]))
        path = args.out_dir / f"contact_{start // 4 + 1:02d}.jpg"
        sheet.save(path, quality=90)
        contact_paths.append(path)
    if contact_paths:
        pages = [Image.open(path).convert("RGB") for path in contact_paths]
        pages[0].save(args.out_dir / "pilot_visual_audit_book.pdf", save_all=True, append_images=pages[1:], resolution=150)
        for page in pages:
            page.close()
    with (args.out_dir / "manual_audit_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    print(json.dumps({"cases": len(rows), "contact_sheets": len(contact_paths)}, indent=2))


if __name__ == "__main__":
    main()
