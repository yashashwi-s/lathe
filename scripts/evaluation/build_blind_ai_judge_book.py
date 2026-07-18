#!/usr/bin/env python3
"""Build an anonymous reference/candidate book for manual visual scoring."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "results" / "metric_calibration" / "canonical_ai_v0_3" / "canonical_ai_scorecard.csv"
DEFAULT_OUT = ROOT / "results" / "metric_calibration" / "canonical_ai_v0_3" / "manual_audit"
PAGE_W, PAGE_H = 1224.0, 792.0
INK = (0.10, 0.12, 0.15)
MUTED = (0.34, 0.38, 0.43)
RULE = (0.72, 0.76, 0.80)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def case_id(row: dict) -> str:
    digest = hashlib.sha256(
        f"{row['sample_id']}|{row['candidate_key']}".encode("utf-8")
    ).hexdigest()[:5].upper()
    return f"B-{digest}"


def tile_pdf(report_page: fitz.Page, source_path: Path, panel: fitz.Rect) -> None:
    with fitz.open(source_path) as source:
        columns = 1 if source.page_count == 1 else 2
        rows = (source.page_count + columns - 1) // columns
        gap_x, gap_y = 10.0, 18.0
        cell_w = (panel.width - gap_x * (columns - 1)) / columns
        cell_h = (panel.height - gap_y * (rows - 1)) / rows
        for page_index, source_page in enumerate(source):
            row, column = divmod(page_index, columns)
            cell = fitz.Rect(
                panel.x0 + column * (cell_w + gap_x),
                panel.y0 + row * (cell_h + gap_y),
                panel.x0 + column * (cell_w + gap_x) + cell_w,
                panel.y0 + row * (cell_h + gap_y) + cell_h,
            )
            scale = min(cell.width / source_page.rect.width, cell.height / source_page.rect.height)
            width, height = source_page.rect.width * scale, source_page.rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - width) / 2,
                cell.y0 + (cell.height - height) / 2,
                cell.x0 + (cell.width + width) / 2,
                cell.y0 + (cell.height + height) / 2,
            )
            report_page.draw_rect(target, color=RULE, width=0.6)
            report_page.show_pdf_page(target, source, page_index, keep_proportion=True)
            report_page.insert_text(
                (target.x0, target.y0 - 7), f"page {page_index + 1}",
                fontsize=6.5, fontname="helv", color=MUTED,
            )


def add_rubric(document: fitz.Document) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((42, 58), "Blinded visual audit", fontsize=27, fontname="hebo", color=INK)
    page.insert_text(
        (42, 88),
        "Reference is always left. Candidate identity and automated scores are hidden.",
        fontsize=12, fontname="helv", color=MUTED,
    )
    rows = [
        ("Content", "Visible text, numbers, formulae, captions, and rows are present and correct."),
        ("Layout", "Page count, placement, spacing, alignment, reading flow, and scale match."),
        ("Typography", "Font class, size hierarchy, emphasis, color, and density match."),
        ("Structure", "Tables, rules, figures, formula structure, and other non-text objects match."),
        ("Overall", "Holistic reference fidelity after considering all four dimensions."),
    ]
    y = 150.0
    for name, description in rows:
        page.draw_rect(fitz.Rect(42, y, PAGE_W - 42, y + 72), color=RULE, width=0.7)
        page.insert_text((62, y + 29), name, fontsize=14, fontname="hebo", color=INK)
        page.insert_text((230, y + 28), description, fontsize=10, fontname="helv", color=MUTED)
        y += 84
    page.insert_text((42, 596), "Ordinal scale", fontsize=14, fontname="hebo", color=INK)
    scale = (
        "0 unusable / fundamentally wrong    1 major defects    2 recognizable but materially wrong    "
        "3 minor-to-moderate defects    4 visually faithful"
    )
    page.insert_text((42, 626), scale, fontsize=10, fontname="helv", color=MUTED)
    page.insert_text(
        (42, 683),
        "Protocol: score each case independently; log confidence and concrete evidence; rank cases only "
        "within the same sample; unblind after all judgments are frozen.",
        fontsize=10, fontname="helv", color=INK,
    )


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows = read_csv(args.input)
    rows.sort(key=lambda row: (row["sample_id"], case_id(row)))
    document = fitz.open()
    add_rubric(document)
    mapping = []
    rubric = []
    for row in rows:
        blind_id = case_id(row)
        category = row["category"]
        reference = ROOT / "data" / "latex_benchmark_v0" / "corpus" / category / row["sample_id"] / "reference.pdf"
        candidate = ROOT / row["candidate_pdf"] if row["candidate_pdf"] else None
        page = document.new_page(width=PAGE_W, height=PAGE_H)
        page.insert_text((32, 38), row["sample_id"], fontsize=17, fontname="hebo", color=INK)
        page.insert_text((PAGE_W - 150, 38), blind_id, fontsize=15, fontname="hebo", color=INK)
        page.draw_line((32, 57), (PAGE_W - 32, 57), color=RULE, width=0.7)
        left = fitz.Rect(32, 105, PAGE_W / 2 - 10, PAGE_H - 34)
        right = fitz.Rect(PAGE_W / 2 + 10, 105, PAGE_W - 32, PAGE_H - 34)
        page.insert_text((left.x0, 87), "REFERENCE", fontsize=10, fontname="hebo", color=INK)
        page.insert_text((right.x0, 87), f"CANDIDATE {blind_id}", fontsize=10, fontname="hebo", color=INK)
        tile_pdf(page, reference, left)
        if candidate and candidate.exists():
            tile_pdf(page, candidate, right)
        else:
            page.draw_rect(right, color=(0.82, 0.25, 0.25), fill=(1, 0.97, 0.97), width=0.8)
            page.insert_text((right.x0 + 36, right.y0 + 72), "COMPILE UNAVAILABLE",
                             fontsize=20, fontname="hebo", color=(0.75, 0.08, 0.10))
        page.insert_text((PAGE_W - 93, PAGE_H - 14), f"page {document.page_count}",
                         fontsize=6.5, fontname="helv", color=MUTED)
        mapping.append({
            "blind_id": blind_id,
            "sample_id": row["sample_id"],
            "candidate_key": row["candidate_key"],
            "display_label": row["display_label"],
            "model_id": row["model_id"],
            "protocol_id": row["protocol_id"],
            "candidate_pdf": row["candidate_pdf"],
        })
        rubric.append({
            "blind_id": blind_id,
            "sample_id": row["sample_id"],
            "content_0_4": "",
            "layout_0_4": "",
            "typography_0_4": "",
            "structure_0_4": "",
            "overall_0_4": "",
            "confidence_low_medium_high": "",
            "within_sample_rank": "",
            "notes": "",
        })

    document.set_metadata({
        "title": "Blinded visual audit book",
        "subject": "Anonymous reference-candidate comparisons for manual scoring",
        "author": "Lathe benchmark",
    })
    pdf_path = args.out_dir / "blind_review_book.pdf"
    document.save(pdf_path, garbage=4, deflate=True)
    document.close()
    for name, records in (("blind_case_map.csv", mapping), ("manual_rubric.csv", rubric)):
        with (args.out_dir / name).open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    print(f"pdf={pdf_path}")
    print(f"cases={len(rows)}")


if __name__ == "__main__":
    main()
