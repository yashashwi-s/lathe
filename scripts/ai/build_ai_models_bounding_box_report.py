#!/usr/bin/env python3
"""Build an AI-only reference comparison PDF with labeled word bounding boxes."""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

import fitz


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from pdf_fidelity import compare_pdfs  # noqa: E402
from build_all_models_engine_grid import (  # noqa: E402
    CANONICAL_SAMPLES,
    Panel,
    canonical_panels,
)


DEFAULT_OUT = ROOT / "output" / "pdf" / "ai_models_bounding_box_comparison.pdf"
DEFAULT_MANIFEST = (
    ROOT / "output" / "pdf" / "ai_models_bounding_box_comparison_manifest.csv"
)
DEFAULT_TMP = ROOT / "tmp" / "pdfs" / "ai_models_bounding_box_comparison"

PAGE_W = 17 * 72
PAGE_H = 11 * 72
INK = (0.075, 0.10, 0.13)
MUTED = (0.34, 0.38, 0.42)
RULE = (0.78, 0.81, 0.84)
GREEN = (0.10, 0.62, 0.36)
AMBER = (0.88, 0.60, 0.08)
ORANGE = (0.90, 0.33, 0.08)
RED = (0.82, 0.12, 0.16)
BLUE = (0.08, 0.40, 0.86)
GRAY = (0.45, 0.48, 0.51)

AI_CANDIDATES = (
    "gemini_3_1_flash_lite",
    "claude_sonnet_4_6",
    "claude_opus_4_7",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--tmp", type=Path, default=DEFAULT_TMP)
    parser.add_argument("--keep-assets", action="store_true")
    return parser.parse_args()


def fit_text(page: fitz.Page, rect: fitz.Rect, text: str, *, size: float = 9,
             minimum: float = 5.5, color=INK, align: int = 0,
             font: str = "helv") -> None:
    current = size
    while current >= minimum:
        remaining = page.insert_textbox(
            rect,
            text,
            fontsize=current,
            fontname=font,
            color=color,
            lineheight=1.12,
            align=align,
        )
        if remaining >= 0:
            return
        current -= 0.5


def portable(path: Optional[Path]) -> str:
    if not path:
        return ""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_artifact(source: str) -> str:
    return portable(Path(source)) if source else ""


def candidate_artifact(path: Optional[Path]) -> str:
    if not path:
        return ""
    try:
        path.relative_to(ROOT / "tmp")
        return "temporary compiled PDF embedded in report"
    except ValueError:
        return portable(path)


def tile_targets(path: Path, rect: fitz.Rect) -> list[tuple[int, fitz.Rect, fitz.Rect]]:
    """Return (page index, source rect, report target) placements."""
    with fitz.open(path) as source:
        count = source.page_count
        columns = 1 if count == 1 else 2
        rows = (count + columns - 1) // columns
        gap_x, gap_y = 10.0, 17.0
        cell_w = (rect.width - gap_x * (columns - 1)) / columns
        cell_h = (rect.height - gap_y * (rows - 1)) / rows
        placements = []
        for page_index in range(count):
            row, column = divmod(page_index, columns)
            cell = fitz.Rect(
                rect.x0 + column * (cell_w + gap_x),
                rect.y0 + row * (cell_h + gap_y),
                rect.x0 + column * (cell_w + gap_x) + cell_w,
                rect.y0 + row * (cell_h + gap_y) + cell_h,
            )
            source_rect = source[page_index].rect
            scale = min(cell.width / source_rect.width, cell.height / source_rect.height)
            width, height = source_rect.width * scale, source_rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - width) / 2,
                cell.y0 + (cell.height - height) / 2,
                cell.x0 + (cell.width + width) / 2,
                cell.y0 + (cell.height + height) / 2,
            )
            placements.append((page_index, source_rect, target))
        return placements


def map_bbox(bbox: tuple[float, ...], source: fitz.Rect, target: fitz.Rect) -> fitz.Rect:
    sx, sy = target.width / source.width, target.height / source.height
    return fitz.Rect(
        target.x0 + (bbox[0] - source.x0) * sx,
        target.y0 + (bbox[1] - source.y0) * sy,
        target.x0 + (bbox[2] - source.x0) * sx,
        target.y0 + (bbox[3] - source.y0) * sy,
    )


def record_color(record: dict) -> tuple[float, float, float]:
    if record["reference_page"] != record["candidate_page"] or record["position_error"] > 0.05:
        return ORANGE
    if record["position_error"] > 0.015:
        return AMBER
    return GREEN


def draw_box(page: fitz.Page, rect: fitz.Rect, color, *, width: float = 0.55) -> None:
    page.draw_rect(rect, color=color, width=width, stroke_opacity=0.92, overlay=True)


def draw_boxed_pdf(page: fitz.Page, path: Path, rect: fitz.Rect, data,
                   records: dict[int, dict], unmatched: set[int], *, side: str) -> None:
    placements = tile_targets(path, rect)
    with fitz.open(path) as source:
        for page_index, source_rect, target in placements:
            page.show_pdf_page(target, source, page_index)
            page.draw_rect(target, color=(0.62, 0.65, 0.68), width=0.5)
            label_rect = fitz.Rect(target.x0, target.y0 - 12, target.x1, target.y0 - 1)
            fit_text(page, label_rect, f"page {page_index + 1}", size=6.5,
                     minimum=6, color=MUTED, align=1)
            for word in (word for word in data.words if word.page == page_index):
                mapped = map_bbox(word.bbox, source_rect, target)
                if word.index in unmatched:
                    color = RED if side == "reference" else BLUE
                    draw_box(page, mapped, color, width=0.8)
                elif word.index in records:
                    draw_box(page, mapped, record_color(records[word.index]))


def badge(page: fitz.Page, x: float, y: float, width: float, label: str,
          value: str, *, color=INK) -> None:
    rect = fitz.Rect(x, y, x + width, y + 39)
    page.draw_rect(rect, color=RULE, fill=(1, 1, 1), width=0.6)
    page.insert_text((x + 7, y + 12), label.upper(), fontsize=5.8, fontname="helv", color=MUTED)
    page.insert_text((x + 7, y + 30), value, fontsize=11, fontname="hebo", color=color)


def status_color(status: str):
    return {"pass": GREEN, "review": AMBER, "fail": RED}.get(status, GRAY)


def box_counts(result: dict) -> Counter:
    counts = Counter()
    for record in result["matches"]:
        if record["reference_page"] != record["candidate_page"] or record["position_error"] > 0.05:
            counts["far_or_page"] += 1
        elif record["position_error"] > 0.015:
            counts["moved"] += 1
        else:
            counts["near"] += 1
    counts["missing"] = len(result["unmatched_reference_indices"])
    counts["extra"] = len(result["unmatched_candidate_indices"])
    return counts


def draw_legend(page: fitz.Page, y: float) -> None:
    entries = [
        (GREEN, "matched, close"),
        (AMBER, "matched, moved"),
        (ORANGE, "far or different page"),
        (RED, "reference-only / missing"),
        (BLUE, "candidate-only / extra"),
    ]
    x = 32.0
    for color, label in entries:
        page.draw_rect(fitz.Rect(x, y, x + 12, y + 8), color=color, width=1.0)
        page.insert_text((x + 17, y + 7), label, fontsize=6.5, fontname="helv", color=MUTED)
        x += 170 if label != "far or different page" else 192


def add_cover(document: fitz.Document, comparison_count: int) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=None, fill=(0.975, 0.98, 0.985))
    page.draw_rect(fitz.Rect(0, 0, 16, PAGE_H), color=None, fill=(0.08, 0.30, 0.46))
    page.insert_text((58, 104), "AI model output comparison", fontsize=30, fontname="hebo", color=INK)
    page.insert_text((58, 148), "Reference-aligned word bounding boxes", fontsize=18,
                     fontname="helv", color=(0.18, 0.31, 0.40))
    scope = (
        "Scope\n"
        "- Eight canonical hard samples from latex_benchmark_v0\n"
        "- Gemini 3.1 Flash Lite, Claude Sonnet 4.6, and Claude Opus 4.7\n"
        "- One dedicated reference-versus-model page per comparison\n"
        "- Deterministic engines, legacy unversioned runs, and incomparable expansion gaps excluded"
    )
    fit_text(page, fitz.Rect(58, 215, 770, 390), scope, size=12, minimum=10)
    page.draw_rect(fitz.Rect(825, 210, 1145, 385), color=RULE, fill=(1, 1, 1), width=0.7)
    page.insert_text((855, 252), str(comparison_count), fontsize=44, fontname="hebo",
                     color=(0.08, 0.30, 0.46))
    page.insert_text((855, 279), "AI/sample comparisons", fontsize=10, fontname="helv", color=MUTED)
    page.insert_text((855, 324), "Vector PDF panels", fontsize=16, fontname="hebo", color=INK)
    page.insert_text((855, 350), "Boxes remain sharp when zoomed", fontsize=9,
                     fontname="helv", color=MUTED)
    page.draw_line((58, 450), (1145, 450), color=RULE, width=0.8)
    fit_text(
        page,
        fitz.Rect(58, 478, 1145, 610),
        "Reading rule: red boxes exist only on the reference side and mark words absent from the "
        "candidate. Blue boxes exist only on the candidate side and mark added words. Green, amber, "
        "and orange indicate progressively larger positional disagreement for matched words. Scores "
        "are the development scorecard axes; no aggregate ranking percentage is shown.",
        size=11,
        minimum=9,
    )
    page.insert_text((58, PAGE_H - 34), "Generated from stored repository artifacts. No model calls.",
                     fontsize=7.5, fontname="helv", color=MUTED)


def add_method_page(document: fitz.Document) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=None, fill=(0.985, 0.988, 0.991))
    page.insert_text((36, 46), "How to read the comparison pages", fontsize=22,
                     fontname="hebo", color=INK)
    page.draw_line((36, 60), (PAGE_W - 36, 60), color=RULE, width=0.7)
    draw_legend(page, 88)
    sections = [
        ("Word correspondence", "Normalized PDF words are matched by identical token text with minimum geometric cost. Bounding boxes are drawn from the original vector PDFs, not raster approximations."),
        ("Reference side", "Red marks reference words that have no candidate match. Matched reference words use the same green/amber/orange position class as their candidate match."),
        ("Candidate side", "Blue marks candidate words absent from the reference. Multi-page documents are tiled; every tile has a page label."),
        ("Scorecard", "Content reports token precision and recall. Layout measures word geometry, local flow, reading order, and page geometry. Appearance uses tolerant ink and edge distance. Pagination uses exact page count and ordered page alignment."),
        ("Limits", "These are text-word boxes. Figures and vector objects affect appearance but do not yet receive object-region boxes. A failed compile is shown as unavailable, not silently removed."),
    ]
    y = 145.0
    for title, body in sections:
        page.draw_rect(fitz.Rect(36, y, PAGE_W - 36, y + 88), color=RULE,
                       fill=(1, 1, 1), width=0.6)
        page.insert_text((54, y + 28), title, fontsize=12, fontname="hebo", color=INK)
        fit_text(page, fitz.Rect(255, y + 14, PAGE_W - 58, y + 74), body,
                 size=9.5, minimum=8, color=MUTED)
        y += 103
    page.insert_text((36, PAGE_H - 24), "Metric: pdf_fidelity_scorecard_v0.2-dev",
                     fontsize=7, fontname="helv", color=MUTED)


def add_failed_comparison(document: fitz.Document, sample: str, panel: Panel,
                          reference: Path, manifest_rows: list[dict]) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=None, fill=(0.985, 0.988, 0.991))
    page.insert_text((30, 32), sample, fontsize=17, fontname="hebo", color=INK)
    fit_text(page, fitz.Rect(220, 18, PAGE_W - 30, 46), panel.label,
             size=11, minimum=8, color=MUTED, align=2)
    page.draw_line((30, 57), (PAGE_W - 30, 57), color=RULE, width=0.7)
    page.draw_rect(fitz.Rect(170, 170, PAGE_W - 170, 560), color=(0.88, 0.55, 0.55),
                   fill=(1.0, 0.97, 0.97), width=0.8)
    page.insert_text((205, 230), "NO COMPILED PDF", fontsize=24, fontname="hebo", color=RED)
    fit_text(page, fitz.Rect(205, 270, PAGE_W - 205, 455), panel.status,
             size=11, minimum=8, color=INK)
    fit_text(page, fitz.Rect(205, 465, PAGE_W - 205, 520),
             "No bounding-box comparison is possible. The failed model output remains in scope and is not dropped from the report.",
             size=9, minimum=8, color=MUTED)
    manifest_rows.append({
        "sample_id": sample,
        "candidate": panel.candidate,
        "label": panel.label,
        "state": panel.state,
        "scorecard_status": "unavailable",
        "reference_pdf": portable(reference),
        "candidate_pdf": "",
        "source_artifact": source_artifact(panel.source),
        "reference_pages": "",
        "candidate_pages": "",
        "token_precision": "",
        "token_recall": "",
        "layout": "",
        "typography": "",
        "appearance_proxy": "",
        "pagination": "",
        "near_boxes": "",
        "moved_boxes": "",
        "far_or_page_boxes": "",
        "missing_boxes": "",
        "extra_boxes": "",
        "failed_gates": "compile",
        "review_flags": "",
        "report_page": document.page_count,
    })


def add_comparison(document: fitz.Document, sample: str, panel: Panel,
                   reference: Path, manifest_rows: list[dict]) -> None:
    result, reference_data, candidate_data, _ = compare_pdfs(reference, panel.path)
    scorecard = result["scorecard"]
    axes = scorecard["axes"]
    counts = box_counts(result)
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=None, fill=(0.985, 0.988, 0.991))
    page.insert_text((30, 30), sample, fontsize=16, fontname="hebo", color=INK)
    fit_text(page, fitz.Rect(235, 16, PAGE_W - 30, 44), panel.label,
             size=10.5, minimum=8, color=MUTED, align=2)
    page.draw_line((30, 56), (PAGE_W - 30, 56), color=RULE, width=0.7)

    badges = [
        ("status", scorecard["status"], status_color(scorecard["status"])),
        ("pages", f"{result['reference_pages']} / {result['candidate_pages']}", INK),
        ("token P/R", f"{100 * axes['content']['token_precision']:.1f} / {100 * axes['content']['token_recall']:.1f}", INK),
        ("layout", f"{100 * axes['layout']['score']:.1f}", INK),
        ("typography", f"{100 * axes['typography']['score']:.1f}", INK),
        ("appearance", f"{100 * axes['appearance_proxy']['score']:.1f}", INK),
        ("page sequence", f"{100 * axes['pagination']['score']:.1f}", INK),
    ]
    badge_w, gap = 154.0, 10.0
    x = 30.0
    for label, value, color in badges:
        badge(page, x, 69, badge_w, label, value, color=color)
        x += badge_w + gap
    flags = "failed gates: " + (", ".join(scorecard["failed_gates"]) or "none")
    flags += " | review: " + (", ".join(scorecard["review_flags"]) or "none")
    fit_text(page, fitz.Rect(30, 116, PAGE_W - 30, 137), flags,
             size=7.2, minimum=6, color=MUTED)
    draw_legend(page, 146)

    left = fitz.Rect(30, 187, PAGE_W / 2 - 10, PAGE_H - 33)
    right = fitz.Rect(PAGE_W / 2 + 10, 187, PAGE_W - 30, PAGE_H - 33)
    page.draw_rect(fitz.Rect(left.x0, left.y0 - 25, left.x1, left.y0 - 3),
                   color=(0.22, 0.34, 0.43), fill=(0.94, 0.97, 0.98), width=0.6)
    page.draw_rect(fitz.Rect(right.x0, right.y0 - 25, right.x1, right.y0 - 3),
                   color=(0.22, 0.34, 0.43), fill=(0.94, 0.97, 0.98), width=0.6)
    page.insert_text((left.x0 + 8, left.y0 - 10), "REFERENCE - candidate-specific correspondence",
                     fontsize=7.5, fontname="hebo", color=INK)
    page.insert_text((right.x0 + 8, right.y0 - 10), "AI CANDIDATE - matched and extra words",
                     fontsize=7.5, fontname="hebo", color=INK)

    reference_records = {record["reference_index"]: record for record in result["matches"]}
    candidate_records = {record["candidate_index"]: record for record in result["matches"]}
    draw_boxed_pdf(
        page,
        reference,
        left,
        reference_data,
        reference_records,
        set(result["unmatched_reference_indices"]),
        side="reference",
    )
    draw_boxed_pdf(
        page,
        panel.path,
        right,
        candidate_data,
        candidate_records,
        set(result["unmatched_candidate_indices"]),
        side="candidate",
    )
    page.insert_text((30, PAGE_H - 13),
                     f"boxes: near {counts['near']} | moved {counts['moved']} | far/page {counts['far_or_page']} | missing {counts['missing']} | extra {counts['extra']}",
                     fontsize=6.5, fontname="helv", color=MUTED)
    page.insert_text((PAGE_W - 112, PAGE_H - 13), f"report page {document.page_count}",
                     fontsize=6.5, fontname="helv", color=MUTED)

    manifest_rows.append({
        "sample_id": sample,
        "candidate": panel.candidate,
        "label": panel.label,
        "state": panel.state,
        "scorecard_status": scorecard["status"],
        "reference_pdf": portable(reference),
        "candidate_pdf": candidate_artifact(panel.path),
        "source_artifact": source_artifact(panel.source),
        "reference_pages": result["reference_pages"],
        "candidate_pages": result["candidate_pages"],
        "token_precision": axes["content"]["token_precision"],
        "token_recall": axes["content"]["token_recall"],
        "layout": axes["layout"]["score"],
        "typography": axes["typography"]["score"],
        "appearance_proxy": axes["appearance_proxy"]["score"],
        "pagination": axes["pagination"]["score"],
        "near_boxes": counts["near"],
        "moved_boxes": counts["moved"],
        "far_or_page_boxes": counts["far_or_page"],
        "missing_boxes": counts["missing"],
        "extra_boxes": counts["extra"],
        "failed_gates": ";".join(scorecard["failed_gates"]),
        "review_flags": ";".join(scorecard["review_flags"]),
        "report_page": document.page_count,
    })


def write_manifest(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.tmp.exists():
        shutil.rmtree(args.tmp)
    args.tmp.mkdir(parents=True, exist_ok=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    panel_sets: list[tuple[str, Path, list[Panel]]] = []
    for sample in CANONICAL_SAMPLES:
        category = sample.rsplit("_", 1)[0]
        reference = ROOT / "data" / "latex_benchmark_v0" / "corpus" / category / sample / "reference.pdf"
        panels = canonical_panels(args.tmp, sample, {})
        ai_panels = [panel for panel in panels if panel.candidate in AI_CANDIDATES]
        panel_sets.append((sample, reference, ai_panels))

    comparison_count = sum(len(panels) for _, _, panels in panel_sets)
    document = fitz.open()
    manifest_rows: list[dict] = []
    toc = [[1, "AI model output comparison", 1], [1, "Legend and method", 2]]
    add_cover(document, comparison_count)
    add_method_page(document)

    for sample, reference, panels in panel_sets:
        for panel in panels:
            if panel.state == "ok" and panel.path and panel.path.exists():
                add_comparison(document, sample, panel, reference, manifest_rows)
            else:
                add_failed_comparison(document, sample, panel, reference, manifest_rows)
            toc.append([2, f"{sample} - {panel.label}", document.page_count])

    document.set_toc(toc)
    document.set_metadata({
        "title": "AI model output comparison - reference-aligned word bounding boxes",
        "subject": "Current AI LaTeX-to-Typst outputs on the canonical hard set",
        "author": "Lathe benchmark",
    })
    document.save(args.out, garbage=4, deflate=True)
    pages = document.page_count
    document.close()
    write_manifest(args.manifest, manifest_rows)

    if not args.keep_assets:
        shutil.rmtree(args.tmp)

    print(f"pdf: {args.out}")
    print(f"manifest: {args.manifest}")
    print(f"pages: {pages}")
    print(f"comparisons: {len(manifest_rows)}")


if __name__ == "__main__":
    main()
