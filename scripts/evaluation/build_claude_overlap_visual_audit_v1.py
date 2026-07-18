#!/usr/bin/env python3
"""Build neutral 2 x 2 evidence sheets for the frozen four-PDF overlap."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "results/metric_research_v2/claude_overlap/overlap_manifest.csv"
DEFAULT_OUTPUT = ROOT / "results/metric_research_v2/claude_overlap/visual_audit"

ROLE_ORDER = ("reference", "gemini", "claude_sonnet", "claude_opus")
ROLE_LABEL = {
    "reference": "Reference - LaTeX benchmark",
    "gemini": "Gemini 3.1 Flash Lite",
    "claude_sonnet": "Claude Sonnet 4.6",
    "claude_opus": "Claude Opus 4.7",
}

# A2 landscape in points. The PDF remains vector; PNG audit sheets are 300 dpi.
PAGE_W = 1683.78
PAGE_H = 1190.55
RENDER_DPI = 300

BLACK = (0.08, 0.08, 0.08)
DARK_GRAY = (0.25, 0.25, 0.25)
MID_GRAY = (0.57, 0.57, 0.57)
LIGHT_GRAY = (0.90, 0.90, 0.90)
PAPER_GRAY = (0.965, 0.965, 0.965)
WHITE = (1.0, 1.0, 1.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["sample_id"]].append(row)
    if len(grouped) != 7 or len(rows) != 28:
        raise ValueError(f"Expected 7 complete sets / 28 rows, got {len(grouped)} / {len(rows)}")
    for sample_id, sample_rows in grouped.items():
        roles = [row["asset_role"] for row in sample_rows]
        if len(sample_rows) != 4 or set(roles) != set(ROLE_ORDER):
            raise ValueError(f"Incomplete role set for {sample_id}: {roles}")
        for row in sample_rows:
            pdf_path = ROOT / row["pdf_path"]
            if not pdf_path.is_file() or row["pdf_open_status"] != "ok":
                raise ValueError(f"Invalid frozen PDF for {sample_id}: {pdf_path}")
    return rows


def insert_textbox_checked(
    page: fitz.Page,
    rect: fitz.Rect,
    text: str,
    *,
    fontsize: float,
    color: tuple[float, float, float],
    fontname: str = "helv",
    align: int = fitz.TEXT_ALIGN_LEFT,
) -> None:
    remaining = page.insert_textbox(
        rect,
        text,
        fontsize=fontsize,
        fontname=fontname,
        color=color,
        align=align,
        lineheight=1.12,
    )
    if remaining < 0:
        raise ValueError(f"Text overflow ({remaining:.2f} pt): {text}")


def draw_document_tiles(
    page: fitz.Page,
    source: fitz.Document,
    body: fitz.Rect,
) -> None:
    count = len(source)
    gap = 12.0
    page_label_h = 15.0
    tile_w = (body.width - gap * (count - 1)) / count
    usable_h = body.height - page_label_h
    for page_index in range(count):
        slot = fitz.Rect(
            body.x0 + page_index * (tile_w + gap),
            body.y0,
            body.x0 + page_index * (tile_w + gap) + tile_w,
            body.y1 - page_label_h,
        )
        source_rect = source[page_index].rect
        scale = min(slot.width / source_rect.width, slot.height / source_rect.height)
        fitted_w = source_rect.width * scale
        fitted_h = source_rect.height * scale
        target = fitz.Rect(
            slot.x0 + (slot.width - fitted_w) / 2,
            slot.y0 + (slot.height - fitted_h) / 2,
            slot.x0 + (slot.width + fitted_w) / 2,
            slot.y0 + (slot.height + fitted_h) / 2,
        )
        page.draw_rect(target, color=MID_GRAY, fill=WHITE, width=0.75, overlay=False)
        page.show_pdf_page(target, source, page_index, keep_proportion=True, overlay=True)
        insert_textbox_checked(
            page,
            fitz.Rect(slot.x0, body.y1 - page_label_h + 1, slot.x1, body.y1),
            f"Page {page_index + 1} of {count}",
            fontsize=7.6,
            color=DARK_GRAY,
            align=fitz.TEXT_ALIGN_CENTER,
        )


def draw_quadrant(page: fitz.Page, area: fitz.Rect, row: dict[str, str]) -> None:
    header_h = 58.0
    pad = 14.0
    page.draw_rect(area, color=MID_GRAY, fill=PAPER_GRAY, width=1.1)
    page.draw_line(
        fitz.Point(area.x0, area.y0 + header_h),
        fitz.Point(area.x1, area.y0 + header_h),
        color=LIGHT_GRAY,
        width=1.0,
    )
    role = row["asset_role"]
    insert_textbox_checked(
        page,
        fitz.Rect(area.x0 + pad, area.y0 + 9, area.x1 - pad, area.y0 + 31),
        ROLE_LABEL[role],
        fontsize=14.0,
        color=BLACK,
        fontname="hebo",
    )
    detail = f"Protocol: {row['protocol_id']} | Pages: {row['page_count']} | Canvas: {row['page_canvas_sizes_pt'].split('|')[0]} pt"
    insert_textbox_checked(
        page,
        fitz.Rect(area.x0 + pad, area.y0 + 34, area.x1 - pad, area.y0 + 52),
        detail,
        fontsize=8.2,
        color=DARK_GRAY,
    )
    body = fitz.Rect(area.x0 + pad, area.y0 + header_h + 12, area.x1 - pad, area.y1 - 10)
    with fitz.open(ROOT / row["pdf_path"]) as source:
        if len(source) != int(row["page_count"]):
            raise ValueError(f"Page-count drift for {row['pdf_path']}")
        draw_document_tiles(page, source, body)


def build_pdf(rows: list[dict[str, str]], output_path: Path) -> None:
    grouped: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    for row in rows:
        grouped[row["sample_id"]][row["asset_role"]] = row

    document = fitz.open()
    margin_x = 34.0
    title_top = 29.0
    grid_top = 105.0
    footer_top = PAGE_H - 31.0
    gap_x = 18.0
    gap_y = 18.0
    quad_w = (PAGE_W - 2 * margin_x - gap_x) / 2
    quad_h = (footer_top - grid_top - gap_y) / 2

    for sheet_number, sample_id in enumerate(sorted(grouped), start=1):
        sample_rows = grouped[sample_id]
        page = document.new_page(width=PAGE_W, height=PAGE_H)
        page.draw_rect(page.rect, color=WHITE, fill=WHITE, overlay=False)
        category = sample_rows["reference"]["category"]
        insert_textbox_checked(
            page,
            fitz.Rect(margin_x, title_top, PAGE_W - margin_x, title_top + 37),
            sample_id,
            fontsize=22.0,
            color=BLACK,
            fontname="hebo",
        )
        insert_textbox_checked(
            page,
            fitz.Rect(margin_x, title_top + 40, PAGE_W - margin_x, title_top + 65),
            f"{category} | Complete stored PDFs | Visual audit evidence - no rank",
            fontsize=10.5,
            color=DARK_GRAY,
        )
        page.draw_line(
            fitz.Point(margin_x, grid_top - 12),
            fitz.Point(PAGE_W - margin_x, grid_top - 12),
            color=LIGHT_GRAY,
            width=1.0,
        )

        areas = (
            fitz.Rect(margin_x, grid_top, margin_x + quad_w, grid_top + quad_h),
            fitz.Rect(margin_x + quad_w + gap_x, grid_top, PAGE_W - margin_x, grid_top + quad_h),
            fitz.Rect(margin_x, grid_top + quad_h + gap_y, margin_x + quad_w, footer_top),
            fitz.Rect(margin_x + quad_w + gap_x, grid_top + quad_h + gap_y, PAGE_W - margin_x, footer_top),
        )
        for area, role in zip(areas, ROLE_ORDER):
            draw_quadrant(page, area, sample_rows[role])

        footer = (
            "Evidence sheet only. Generation conditions differ: Gemini is source-only; most Claude cases used "
            "iterative visual feedback. Do not interpret this page as a controlled model leaderboard."
        )
        insert_textbox_checked(
            page,
            fitz.Rect(margin_x, footer_top + 7, PAGE_W - margin_x - 100, PAGE_H - 7),
            footer,
            fontsize=8.0,
            color=DARK_GRAY,
        )
        insert_textbox_checked(
            page,
            fitz.Rect(PAGE_W - margin_x - 92, footer_top + 7, PAGE_W - margin_x, PAGE_H - 7),
            f"Sheet {sheet_number} / 7",
            fontsize=8.0,
            color=DARK_GRAY,
            align=fitz.TEXT_ALIGN_RIGHT,
        )

    metadata = {
        "title": "Claude overlap visual audit evidence",
        "author": "Lathe metric research",
        "subject": "Seven complete Reference-Gemini-Sonnet-Opus comparison sets",
        "keywords": "PDF fidelity, visual audit, evidence, no leaderboard",
    }
    document.set_metadata(metadata)
    document.save(output_path, garbage=4, deflate=True, clean=True)
    document.close()


def render_sheets(pdf_path: Path, output_dir: Path) -> None:
    with fitz.open(pdf_path) as document:
        if len(document) != 7:
            raise ValueError(f"Expected seven PDF sheets, found {len(document)}")
        matrix = fitz.Matrix(RENDER_DPI / 72.0, RENDER_DPI / 72.0)
        for page_index, page in enumerate(document):
            sample_id = page.get_text("text").splitlines()[0]
            pixmap = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB, alpha=False)
            output_path = output_dir / f"sheet_{page_index + 1:02d}_{sample_id}.png"
            pixmap.save(output_path)


def main() -> None:
    args = parse_args()
    manifest = args.manifest.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = read_manifest(manifest)
    pdf_path = output_dir / "overlap_visual_comparison.pdf"
    build_pdf(rows, pdf_path)
    render_sheets(pdf_path, output_dir)
    print(f"Wrote {pdf_path}")
    print(f"Wrote seven {RENDER_DPI} dpi PNG sheets to {output_dir}")


if __name__ == "__main__":
    main()
