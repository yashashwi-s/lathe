#!/usr/bin/env python3
"""Build provenance and engine-comparison review PDFs for the unified dataset."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import fitz


DATASET = Path("data/latex_benchmark_v0")
ENGINE_DIR = Path("results/latex_benchmark_v0")

CATEGORY_LABELS = {
    "01_prose_sections": "Prose Sections",
    "02_lists_formatting": "Lists And Formatting",
    "03_math_inline_display": "Inline And Display Math",
    "04_math_aligned": "Aligned Math",
    "05_tables_simple": "Simple Tables",
    "06_tables_moderate": "Moderate Tables",
    "07_figures_captions": "Figures And Captions",
    "08_crossrefs_citations": "Crossrefs And Citations",
    "09_algorithms": "Algorithms",
    "10_compact_papers": "Compact Papers",
    "11_forms_cv_letters": "Forms, CVs, And Letters",
}


def load_rows(dataset: Path) -> list[dict]:
    return list(csv.DictReader((dataset / "manifests" / "accepted.csv").open(encoding="utf-8")))


def load_engine_manifest(engine_dir: Path) -> dict[tuple[str, str], dict]:
    path = engine_dir / "engine_manifest.csv"
    if not path.exists():
        return {}
    rows = csv.DictReader(path.open(encoding="utf-8"))
    return {(r["sample_id"], r["engine"]): r for r in rows}


def source_summary(row: dict) -> str:
    dataset = row["source_dataset"]
    ids = row.get("source_ids", "")
    if dataset == "scholarweave/arxiv-latex":
        return f"HF scholarweave/arxiv-latex; arXiv id/excerpt source: {ids}"
    if dataset == "OleehyO/latex-formulas":
        return f"HF OleehyO/latex-formulas; grouped formula row ids: {ids}"
    if dataset == "piushorn/arxiv-latex-tables-43k":
        return f"HF piushorn/arxiv-latex-tables-43k; grouped table ids: {ids}"
    if dataset == "stanford-crfm/image2struct-latex-v1":
        return f"HF stanford-crfm/image2struct-latex-v1; algorithm row id: {ids}"
    if dataset == "TeX Live 2026":
        return f"Local TeX Live 2026 example source: {ids}"
    return f"{dataset}; source ids: {ids}"


def draw_header(page: fitz.Page, title: str, subtitle: str = "") -> None:
    page.insert_text((36, 32), title, fontsize=13, fontname="helv")
    if subtitle:
        page.insert_textbox(fitz.Rect(36, 48, 806, 76), subtitle, fontsize=7, fontname="helv")
    page.draw_line((36, 80), (806, 80), color=(0.72, 0.72, 0.72), width=0.6)


def section_page(doc: fitz.Document, category: str, count: int) -> None:
    page = doc.new_page(width=842, height=595)
    page.insert_text((48, 90), category, fontsize=28, fontname="helv")
    page.insert_text((48, 132), CATEGORY_LABELS.get(category, category), fontsize=16, fontname="helv")
    page.insert_text((48, 166), f"{count} accepted samples", fontsize=12, fontname="helv")


def draw_pdf_tiled(page: fitz.Page, pdf_path: Path, rect: fitz.Rect, max_pages: int | None = None) -> None:
    if not pdf_path.exists():
        page.draw_rect(rect, color=(0.85, 0.25, 0.25), width=0.8)
        page.insert_textbox(rect + (6, 8, -6, -8), "missing / failed", fontsize=8, fontname="helv", align=1)
        return
    try:
        src = fitz.open(pdf_path)
    except Exception:
        page.draw_rect(rect, color=(0.85, 0.25, 0.25), width=0.8)
        page.insert_textbox(rect + (6, 8, -6, -8), "invalid PDF", fontsize=8, fontname="helv", align=1)
        return
    try:
        shown = src.page_count if max_pages is None else min(src.page_count, max_pages)
        cols = math.ceil(math.sqrt(shown))
        rows = math.ceil(shown / cols)
        gap = 5
        cell_w = (rect.width - gap * (cols - 1)) / cols
        cell_h = (rect.height - gap * (rows - 1)) / rows
        for idx in range(shown):
            r = idx // cols
            c = idx % cols
            cell = fitz.Rect(
                rect.x0 + c * (cell_w + gap),
                rect.y0 + r * (cell_h + gap),
                rect.x0 + c * (cell_w + gap) + cell_w,
                rect.y0 + r * (cell_h + gap) + cell_h,
            )
            src_page = src.load_page(idx)
            scale = min(cell.width / src_page.rect.width, cell.height / src_page.rect.height)
            w = src_page.rect.width * scale
            h = src_page.rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - w) / 2,
                cell.y0 + (cell.height - h) / 2,
                cell.x0 + (cell.width + w) / 2,
                cell.y0 + (cell.height + h) / 2,
            )
            page.show_pdf_page(target, src, idx)
            page.draw_rect(target, color=(0.62, 0.62, 0.62), width=0.45)
        if src.page_count > shown:
            page.insert_text((rect.x0 + 6, rect.y1 - 8), f"showing {shown}/{src.page_count} pages", fontsize=6, fontname="helv")
    finally:
        src.close()


def add_provenance_sample(doc: fitz.Document, row: dict) -> None:
    page = doc.new_page(width=842, height=595)
    subtitle = (
        f"Source: {source_summary(row)}\n"
        f"Pages: {row['page_count']} | Nonblank lines: {row['nonblank_lines']} | Source chars: {row['source_chars']} | SHA256 PDF: {row['sha256_pdf'][:16]}..."
    )
    draw_header(page, f"{row['sample_id']} | {row['category']}", subtitle)
    sample_dir = Path(row["sample_dir"])
    draw_pdf_tiled(page, sample_dir / "reference.pdf", fitz.Rect(36, 96, 806, 568), max_pages=None)


def build_provenance(dataset: Path, rows: list[dict], out_path: Path) -> None:
    doc = fitz.open()
    by_cat = {}
    for row in rows:
        by_cat.setdefault(row["category"], []).append(row)
    cover = doc.new_page(width=842, height=595)
    cover.insert_text((48, 70), "Simple Benchmark All v0", fontsize=28, fontname="helv")
    cover.insert_text((48, 112), "Dataset provenance review", fontsize=16, fontname="helv")
    cover.insert_textbox(
        fitz.Rect(48, 150, 794, 520),
        "One section per category. Each sample page shows the rendered reference PDF and exact source origin metadata from the accepted manifest.",
        fontsize=11,
        fontname="helv",
    )
    for category in sorted(by_cat):
        section_page(doc, category, len(by_cat[category]))
        for row in sorted(by_cat[category], key=lambda r: r["sample_id"]):
            add_provenance_sample(doc, row)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    doc.close()


def engine_pdf(engine_dir: Path, row: dict, engine: str) -> Path:
    return engine_dir / row["category"] / row["sample_id"] / f"{engine}.pdf"


def add_comparison_sample(doc: fitz.Document, row: dict, engine_rows: dict[tuple[str, str], dict], engine_dir: Path) -> None:
    page = doc.new_page(width=842, height=595)
    subtitle = f"Origin: {source_summary(row)}"
    draw_header(page, f"{row['sample_id']} | {row['category']}", subtitle)
    cells = [
        ("Reference", Path(row["sample_dir"]) / "reference.pdf", None),
        ("Pandoc", engine_pdf(engine_dir, row, "pandoc"), engine_rows.get((row["sample_id"], "pandoc"))),
        ("Tylax", engine_pdf(engine_dir, row, "tylax"), engine_rows.get((row["sample_id"], "tylax"))),
        ("TypeTeX", engine_pdf(engine_dir, row, "typetex"), engine_rows.get((row["sample_id"], "typetex"))),
    ]
    x0, y0 = 36, 96
    w, h = 372, 218
    gap_x, gap_y = 26, 30
    for idx, (label, pdf, erow) in enumerate(cells):
        r = idx // 2
        c = idx % 2
        label_y = y0 + r * (h + gap_y) - 13
        rect = fitz.Rect(x0 + c * (w + gap_x), y0 + r * (h + gap_y), x0 + c * (w + gap_x) + w, y0 + r * (h + gap_y) + h)
        status = ""
        if erow:
            status = f" convert={erow['conversion_status']} compile={erow['compile_status']}"
        page.insert_text((rect.x0, label_y), label + status, fontsize=9, fontname="helv")
        page.draw_rect(rect, color=(0.2, 0.2, 0.2), width=0.6)
        draw_pdf_tiled(page, pdf, rect + (5, 5, -5, -5), max_pages=None)


def build_comparison(dataset: Path, rows: list[dict], engine_dir: Path, out_path: Path) -> None:
    doc = fitz.open()
    engine_rows = load_engine_manifest(engine_dir)
    by_cat = {}
    for row in rows:
        by_cat.setdefault(row["category"], []).append(row)
    cover = doc.new_page(width=842, height=595)
    cover.insert_text((48, 70), "Simple Benchmark All v0", fontsize=28, fontname="helv")
    cover.insert_text((48, 112), "Reference vs Pandoc vs Tylax vs TypeTeX", fontsize=16, fontname="helv")
    cover.insert_textbox(
        fitz.Rect(48, 150, 794, 520),
        "Each sample page uses a 2x2 grid. Missing cells indicate conversion or Typst compilation failure; status labels are shown above each engine cell.",
        fontsize=11,
        fontname="helv",
    )
    for category in sorted(by_cat):
        section_page(doc, category, len(by_cat[category]))
        for row in sorted(by_cat[category], key=lambda r: r["sample_id"]):
            add_comparison_sample(doc, row, engine_rows, engine_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)
    doc.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--engine-dir", type=Path, default=ENGINE_DIR)
    args = parser.parse_args()

    rows = load_rows(args.dataset)
    docs_dir = args.engine_dir / "documents"
    provenance = docs_dir / "dataset_provenance.pdf"
    comparison = docs_dir / "engine_comparison_grid.pdf"
    build_provenance(args.dataset, rows, provenance)
    build_comparison(args.dataset, rows, args.engine_dir, comparison)
    print(f"provenance: {provenance}")
    print(f"comparison: {comparison}")


if __name__ == "__main__":
    main()
