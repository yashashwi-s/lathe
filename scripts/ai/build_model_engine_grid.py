"""Build a reference/engine/AI comparison review PDF for a prompt split."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data" / "latex_benchmark_v0"
DEV_SPLIT = DATASET / "splits" / "prompt_dev_33.csv"
ENGINE_DIR = ROOT / "results" / "latex_benchmark_v0"
AI_ROOT = ROOT / "results" / "ai_latex_to_typst" / "openrouter" / "google_gemini-3.1-flash-lite"
V0_DIR = AI_ROOT / "prompt_v0"
V1_DIR = AI_ROOT / "prompt_v1_v0_failures"
V3_DIR = AI_ROOT / "prompt_v3_prompt_dev_failures"
OUT_DIR = ROOT / "results" / "ai_latex_to_typst" / "documents"

PAGE_W = 1191
PAGE_H = 842

CATEGORY_LABELS = {
    "01_prose_sections": "Prose sections",
    "02_lists_formatting": "Lists and formatting",
    "03_math_inline_display": "Inline and display math",
    "04_math_aligned": "Aligned math",
    "05_tables_simple": "Simple tables",
    "06_tables_moderate": "Moderate tables",
    "07_figures_captions": "Figures and captions",
    "08_crossrefs_citations": "Cross-references and citations",
    "09_algorithms": "Algorithms",
    "10_compact_papers": "Compact papers",
    "11_forms_cv_letters": "Forms, CVs, and letters",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", type=Path, default=DEV_SPLIT)
    parser.add_argument("--engine-dir", type=Path, default=ENGINE_DIR)
    parser.add_argument("--v0-dir", type=Path, default=V0_DIR)
    parser.add_argument("--v1-dir", type=Path, default=V1_DIR)
    parser.add_argument("--v3-dir", type=Path, default=V3_DIR)
    parser.add_argument("--out", type=Path,
                        default=OUT_DIR / "prompt_clean_v0_v1_v3_engine_comparison_grid.pdf")
    parser.add_argument("--manifest", type=Path,
                        default=OUT_DIR / "prompt_clean_v0_v1_v3_engine_comparison_manifest.csv")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict]:
    return list(csv.DictReader(path.open(newline="", encoding="utf-8")))


def load_meta(run_dir: Path) -> dict[str, dict]:
    result = {}
    for path in (run_dir / "samples").glob("*/meta.json"):
        result[path.parent.name] = json.loads(path.read_text())
    return result


def source_summary(row: dict) -> str:
    source = row.get("source_dataset", "unknown")
    ids = row.get("source_ids", "")
    return f"{source}; {ids}"[:220]


def engine_index(engine_dir: Path) -> dict[tuple[str, str], dict]:
    return {
        (row["sample_id"], row["engine"]): row
        for row in read_csv(engine_dir / "engine_manifest.csv")
    }


def fit_text(page: fitz.Page, rect: fitz.Rect, text: str, size: float = 8,
             font: str = "helv", color=(0.12, 0.12, 0.12)) -> None:
    current = size
    while current >= 5.5:
        if page.insert_textbox(rect, text, fontsize=current, fontname=font,
                               color=color, lineheight=1.18) >= 0:
            return
        current -= 0.5
    page.insert_textbox(rect, text, fontsize=5.5, fontname=font, color=color,
                        lineheight=1.05)


def draw_pdf_tiled(page: fitz.Page, pdf_path: Path | None, rect: fitz.Rect,
                   failure_text: str = "missing / failed") -> None:
    if pdf_path is None or not pdf_path.exists():
        page.draw_rect(rect, color=(0.72, 0.18, 0.18), fill=(0.99, 0.95, 0.95), width=0.9)
        fit_text(page, rect + (12, 16, -12, -16), failure_text, size=9,
                 color=(0.55, 0.08, 0.08))
        return
    try:
        source = fitz.open(pdf_path)
    except Exception:
        page.draw_rect(rect, color=(0.72, 0.18, 0.18), fill=(0.99, 0.95, 0.95), width=0.9)
        fit_text(page, rect + (12, 16, -12, -16), "invalid PDF", size=9,
                 color=(0.55, 0.08, 0.08))
        return
    try:
        count = source.page_count
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)
        gap = 5
        cell_w = (rect.width - gap * (cols - 1)) / cols
        cell_h = (rect.height - gap * (rows - 1)) / rows
        for index in range(count):
            row = index // cols
            col = index % cols
            cell = fitz.Rect(
                rect.x0 + col * (cell_w + gap),
                rect.y0 + row * (cell_h + gap),
                rect.x0 + col * (cell_w + gap) + cell_w,
                rect.y0 + row * (cell_h + gap) + cell_h,
            )
            source_page = source.load_page(index)
            scale = min(cell.width / source_page.rect.width, cell.height / source_page.rect.height)
            width = source_page.rect.width * scale
            height = source_page.rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - width) / 2,
                cell.y0 + (cell.height - height) / 2,
                cell.x0 + (cell.width + width) / 2,
                cell.y0 + (cell.height + height) / 2,
            )
            page.show_pdf_page(target, source, index)
            page.draw_rect(target, color=(0.62, 0.62, 0.62), width=0.45)
    finally:
        source.close()


def draw_panel(page: fitz.Page, rect: fitz.Rect, label: str,
               pdf_path: Path | None, status: str, failure_text: str = "missing / failed") -> None:
    page.draw_rect(rect, color=(0.30, 0.30, 0.30), fill=(1, 1, 1), width=0.65)
    page.draw_rect(fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y0 + 24),
                   color=(0.16, 0.16, 0.16), fill=(0.95, 0.96, 0.97), width=0.5)
    page.insert_text((rect.x0 + 8, rect.y0 + 15), label, fontsize=9,
                     fontname="helv", color=(0.08, 0.08, 0.08))
    page.insert_textbox(fitz.Rect(rect.x0 + rect.width * 0.42, rect.y0 + 6,
                                  rect.x1 - 8, rect.y0 + 20), status,
                        fontsize=6.5, fontname="helv", color=(0.30, 0.30, 0.30),
                        align=2)
    draw_pdf_tiled(page, pdf_path, rect + (7, 31, -7, -7), failure_text)


def select_ai(sample_id: str, v0: dict[str, dict], v1: dict[str, dict],
              v3: dict[str, dict], v0_dir: Path, v1_dir: Path,
              v3_dir: Path) -> tuple[str, Path | None, dict | None, str]:
    if sample_id in v3:
        meta = v3[sample_id]
        path = v3_dir / "samples" / sample_id / "output.pdf"
        return "AI - prompt v3 rescue", path if meta.get("final_compiled") else None, meta, "v3_rescue"
    if sample_id in v1:
        meta = v1[sample_id]
        path = v1_dir / "samples" / sample_id / "output.pdf"
        return "AI - prompt v1 targeted retry", path if meta.get("final_compiled") else None, meta, "v1_targeted_retry"
    meta = v0.get(sample_id)
    path = v0_dir / "samples" / sample_id / "output.pdf"
    return "AI - prompt v0", path if meta and meta.get("final_compiled") else None, meta, "v0"


def cover_page(document: fitz.Document, sample_count: int, retry_count: int, rescue_count: int) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((58, 92), "LaTeX-to-Typst comparison", fontsize=30, fontname="helv")
    page.insert_text((58, 138), "Reference, deterministic engines, and Gemini 3.1 Flash Lite", fontsize=17,
                     fontname="helv", color=(0.28, 0.28, 0.28))
    text = (
        f"{sample_count} clean prompt-development samples. Each sample page contains every page of the available PDFs.\n\n"
        "AI selection policy:\n"
        "- prompt-v0 successes use their v0 output\n"
        f"- {retry_count} filtered v0 failures use the prompt-v1 targeted retry output\n"
        f"- {rescue_count} remaining prompt-v1 failures use the prompt-v3 rescue output\n"
        "- failed AI and engine conversions remain visible as labeled failure cells\n\n"
        "This is a review artifact for prompt development, not a held-out benchmark result."
    )
    fit_text(page, fitz.Rect(58, 190, 900, 500), text, size=12)


def section_page(document: fitz.Document, category: str, count: int) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((58, 108), category, fontsize=27, fontname="helv")
    page.insert_text((58, 152), CATEGORY_LABELS.get(category, category), fontsize=17,
                     fontname="helv", color=(0.28, 0.28, 0.28))
    page.insert_text((58, 194), f"{count} review samples", fontsize=11, fontname="helv")


def sample_page(document: fitz.Document, row: dict, engines: dict[tuple[str, str], dict],
                engine_dir: Path, v0: dict[str, dict], v1: dict[str, dict],
                v3: dict[str, dict], v0_dir: Path, v1_dir: Path,
                v3_dir: Path) -> dict:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    sample_id = row["sample_id"]
    page.insert_text((34, 30), f"{sample_id} | {row['category']} | {row['complexity_band']}",
                     fontsize=13, fontname="helv")
    fit_text(page, fitz.Rect(34, 40, PAGE_W - 34, 67), source_summary(row), size=7,
             color=(0.34, 0.34, 0.34))
    page.draw_line((34, 72), (PAGE_W - 34, 72), color=(0.72, 0.72, 0.72), width=0.6)

    margin = 34
    gap_x = 16
    gap_y = 18
    top = 86
    cell_w = (PAGE_W - 2 * margin - 2 * gap_x) / 3
    cell_h = (PAGE_H - top - margin - gap_y) / 2
    rects = []
    for grid_row in range(2):
        for grid_col in range(3):
            x0 = margin + grid_col * (cell_w + gap_x)
            y0 = top + grid_row * (cell_h + gap_y)
            rects.append(fitz.Rect(x0, y0, x0 + cell_w, y0 + cell_h))

    reference = ROOT / row["reference_pdf"]
    ai_label, ai_pdf, ai_meta, ai_stage = select_ai(sample_id, v0, v1, v3, v0_dir, v1_dir, v3_dir)
    ai_status = "not run"
    ai_failure = "AI output unavailable"
    if ai_meta:
        ai_status = f"compile={'ok' if ai_meta.get('final_compiled') else 'failed'}; attempts={ai_meta.get('attempts')}"
        ai_failure = f"failed after {ai_meta.get('attempts')} attempt(s)\n{ai_meta.get('final_error_summary', '')}"

    draw_panel(page, rects[0], "Reference", reference, f"pages={row['page_count']}")
    draw_panel(page, rects[1], ai_label, ai_pdf, ai_status, ai_failure)

    info = (
        f"AI source: {ai_stage}\n"
        f"AI page count: {ai_meta.get('candidate_pages') if ai_meta else 'n/a'}\n"
        f"Reference page count: {row['page_count']}\n"
        f"Source: {row['source_dataset']}\n"
        f"Source IDs: {row['source_ids']}\n\n"
        "All source and engine pages are tiled; no page is intentionally omitted."
    )
    page.draw_rect(rects[2], color=(0.30, 0.30, 0.30), fill=(0.97, 0.98, 0.99), width=0.65)
    page.insert_text((rects[2].x0 + 10, rects[2].y0 + 18), "Status and provenance", fontsize=9,
                     fontname="helv")
    fit_text(page, rects[2] + (10, 34, -10, -10), info, size=8)

    for offset, engine in enumerate(("pandoc", "tylax", "typetex"), start=3):
        engine_row = engines.get((sample_id, engine))
        status = "not run"
        pdf = None
        failure = "engine output unavailable"
        if engine_row:
            status = f"convert={engine_row['conversion_status']}; compile={engine_row['compile_status']}"
            if engine_row["compile_status"] == "ok":
                pdf = engine_dir / row["category"] / sample_id / f"{engine}.pdf"
            failure = status
        draw_panel(page, rects[offset], engine.title(), pdf, status, failure)

    return {
        "sample_id": sample_id,
        "category": row["category"],
        "complexity_band": row["complexity_band"],
        "ai_prompt_version": ai_stage,
        "ai_final_compiled": bool(ai_meta and ai_meta.get("final_compiled")),
        "ai_attempts": ai_meta.get("attempts") if ai_meta else "",
        "reference_pages": row["page_count"],
        "ai_pages": ai_meta.get("candidate_pages") if ai_meta else "",
        "pandoc_compile": engines.get((sample_id, "pandoc"), {}).get("compile_status", "missing"),
        "tylax_compile": engines.get((sample_id, "tylax"), {}).get("compile_status", "missing"),
        "typetex_compile": engines.get((sample_id, "typetex"), {}).get("compile_status", "missing"),
    }


def main() -> None:
    args = parse_args()
    rows = read_csv(args.split)
    engines = engine_index(args.engine_dir)
    v0 = load_meta(args.v0_dir)
    v1 = load_meta(args.v1_dir)
    v3 = load_meta(args.v3_dir)
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row)

    document = fitz.open()
    retry_count = sum(1 for row in rows if row["sample_id"] in v1)
    rescue_count = sum(1 for row in rows if row["sample_id"] in v3)
    cover_page(document, len(rows), retry_count, rescue_count)
    manifest = []
    for category in sorted(by_category):
        category_rows = by_category[category]
        section_page(document, category, len(category_rows))
        for row in category_rows:
            manifest.append(sample_page(
                document, row, engines, args.engine_dir, v0, v1, v3,
                args.v0_dir, args.v1_dir, args.v3_dir
            ))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    document.set_metadata({
        "title": "LaTeX-to-Typst model and engine comparison",
        "subject": f"{len(rows)}-sample prompt-development review grid",
        "author": "Lathe benchmark",
    })
    document.save(args.out, garbage=4, deflate=True)
    document.close()

    with args.manifest.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    print(f"comparison: {args.out}")
    print(f"manifest: {args.manifest}")
    print(f"samples: {len(manifest)}")


if __name__ == "__main__":
    main()
