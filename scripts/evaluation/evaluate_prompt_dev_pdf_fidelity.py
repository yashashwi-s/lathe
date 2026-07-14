"""Evaluate and visually report PDF fidelity for the 30 clean prompt-dev samples."""

from __future__ import annotations

import argparse
import csv
import json
import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from pdf_fidelity import METRIC_CONFIG, METRIC_VERSION, compare_pdfs, create_diagnostic_images, public_result


ROOT = Path(__file__).resolve().parents[2]
SPLIT = ROOT / "data" / "latex_benchmark_v0" / "splits" / "prompt_dev_33.csv"
SELECTION_MANIFEST = (ROOT / "results" / "ai_latex_to_typst" / "documents" /
                      "prompt_clean_v0_v1_v3_engine_comparison_manifest.csv")
AI_ROOT = (ROOT / "results" / "ai_latex_to_typst" / "openrouter" /
           "google_gemini-3.1-flash-lite")
RESULT_DIR = ROOT / "results" / "ai_latex_to_typst" / "metrics" / "prompt_dev_30"
REPORT = ROOT / "output" / "pdf" / "prompt_dev_30_pdf_fidelity_report.pdf"

STAGE_DIRS = {
    "v0": "prompt_v0",
    "v1_targeted_retry": "prompt_v1_v0_failures",
    "v3_rescue": "prompt_v3_prompt_dev_failures",
}

PAGE_SIZE = landscape(A3)
PAGE_W, PAGE_H = PAGE_SIZE
NAVY = colors.HexColor("#14243b")
BLUE = colors.HexColor("#3267a8")
TEAL = colors.HexColor("#168a72")
AMBER = colors.HexColor("#d38a22")
RED = colors.HexColor("#c74747")
LIGHT = colors.HexColor("#f4f6f8")
MID = colors.HexColor("#d9dfe7")
TEXT = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#5c6773")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", type=Path, default=SPLIT)
    parser.add_argument("--selection-manifest", type=Path, default=SELECTION_MANIFEST)
    parser.add_argument("--result-dir", type=Path, default=RESULT_DIR)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--limit", type=int, default=0,
                        help="Optional smoke-test limit; zero evaluates all 30 samples.")
    return parser.parse_args()


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def selected_candidate(sample_id: str, stage: str) -> Path:
    run_dir = STAGE_DIRS.get(stage)
    if not run_dir:
        raise ValueError(f"unknown AI selection stage {stage!r} for {sample_id}")
    path = AI_ROOT / run_dir / "samples" / sample_id / "output.pdf"
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def font(size: int = 18) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def make_collage(paths: list[str], output: Path, title: str) -> Path:
    images = [Image.open(path).convert("RGB") for path in paths]
    if not images:
        image = Image.new("RGB", (900, 1200), "white")
        draw = ImageDraw.Draw(image)
        draw.text((40, 40), "No page available", fill=(170, 40, 40), font=font(28))
        image.save(output)
        return output
    columns = 1 if len(images) == 1 else 2
    rows = math.ceil(len(images) / columns)
    cell_w, cell_h = 920, 1240
    header = 42
    collage = Image.new("RGB", (columns * cell_w, rows * (cell_h + header)), (228, 232, 237))
    draw = ImageDraw.Draw(collage)
    label_font = font(22)
    for index, image in enumerate(images):
        row, column = divmod(index, columns)
        x0, y0 = column * cell_w, row * (cell_h + header)
        draw.rectangle((x0, y0, x0 + cell_w - 1, y0 + header - 1), fill=(30, 45, 65))
        draw.text((x0 + 14, y0 + 9), f"{title} - page {index + 1}", fill="white", font=label_font)
        copy = image.copy()
        copy.thumbnail((cell_w - 22, cell_h - 22), Image.Resampling.LANCZOS)
        px = x0 + (cell_w - copy.width) // 2
        py = y0 + header + (cell_h - copy.height) // 2
        collage.paste(copy, (px, py))
    output.parent.mkdir(parents=True, exist_ok=True)
    collage.save(output, quality=94)
    return output


def score_color(value: float) -> colors.Color:
    if value >= 0.80:
        return TEAL
    if value >= 0.60:
        return AMBER
    return RED


def write_wrapped(pdf: canvas.Canvas, text: str, x: float, y: float, width: float,
                  size: float = 10, leading: float = 14, color=TEXT,
                  font_name: str = "Helvetica") -> float:
    max_chars = max(18, int(width / (size * 0.53)))
    pdf.setFont(font_name, size)
    pdf.setFillColor(color)
    for paragraph in text.split("\n"):
        lines = textwrap.wrap(paragraph, width=max_chars, break_long_words=False) or [""]
        for line in lines:
            pdf.drawString(x, y, line)
            y -= leading
        y -= leading * 0.25
    return y


def page_header(pdf: canvas.Canvas, title: str, subtitle: str = "") -> None:
    pdf.setFillColor(NAVY)
    pdf.rect(0, PAGE_H - 54, PAGE_W, 54, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(34, PAGE_H - 34, title)
    if subtitle:
        pdf.setFont("Helvetica", 9)
        pdf.setFillColor(colors.HexColor("#d6e0eb"))
        pdf.drawRightString(PAGE_W - 34, PAGE_H - 33, subtitle)


def footer(pdf: canvas.Canvas, page_number: int) -> None:
    pdf.setStrokeColor(MID)
    pdf.line(34, 25, PAGE_W - 34, 25)
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(34, 12, "Lathe prompt-development PDF fidelity calibration - development data only")
    pdf.drawRightString(PAGE_W - 34, 12, str(page_number))


def score_card(pdf: canvas.Canvas, x: float, y: float, width: float,
               label: str, value: float, detail: str = "") -> None:
    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(MID)
    pdf.roundRect(x, y, width, 58, 6, stroke=1, fill=1)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.setFillColor(MUTED)
    pdf.drawString(x + 10, y + 41, label.upper())
    pdf.setFont("Helvetica-Bold", 23)
    pdf.setFillColor(score_color(value))
    pdf.drawString(x + 10, y + 15, f"{100 * value:.1f}")
    if detail:
        pdf.setFont("Helvetica", 7.5)
        pdf.setFillColor(MUTED)
        pdf.drawRightString(x + width - 9, y + 18, detail)


def cover_page(pdf: canvas.Canvas, count: int) -> None:
    pdf.setFillColor(NAVY)
    pdf.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawString(62, PAGE_H - 120, "PDF fidelity calibration")
    pdf.setFont("Helvetica", 20)
    pdf.setFillColor(colors.HexColor("#b9cbe0"))
    pdf.drawString(62, PAGE_H - 158, "Content, layout, typography, and raster comparison")
    pdf.setFillColor(colors.HexColor("#1c3554"))
    pdf.roundRect(62, PAGE_H - 350, PAGE_W - 124, 132, 12, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 17)
    pdf.drawString(86, PAGE_H - 258, f"{count} clean prompt-development conversions")
    body = (
        "Each sample is compared against its pdfLaTeX reference using word-level content matching, "
        "absolute and relative geometry, reading order, font and style attributes, tolerant foreground "
        "overlap, edge distance, and foreground-masked structural similarity. Every result page includes "
        "reference boxes, candidate boxes, raster differences, component scores, and review flags."
    )
    write_wrapped(pdf, body, 86, PAGE_H - 290, PAGE_W - 172, 11, 15,
                  colors.HexColor("#d6e0eb"))
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.HexColor("#91a8c2"))
    pdf.drawString(62, 58, "Calibration artifact - not a held-out benchmark claim")
    pdf.showPage()


def methodology_page_one(pdf: canvas.Canvas, page_number: int) -> None:
    page_header(pdf, "Methodology 1/3 - What the score means")
    x, y = 48, PAGE_H - 92
    pdf.setFont("Helvetica-Bold", 18)
    pdf.setFillColor(TEXT)
    pdf.drawString(x, y, "Two headline scores, one auditable overall score")
    y -= 34
    columns = [
        ("CONTENT FIDELITY", "Order-independent normalized token precision/recall/F1 plus a lower-weight full-text character sequence similarity. This reduces producer reading-order bias while still detecting omissions, additions, and substitutions."),
        ("VISUAL FIDELITY", "A weighted geometric mean of pagination, word and flow layout, typography, and raster appearance. The primary comparison does not translate or resize the candidate to improve alignment."),
        ("OVERALL FIDELITY", "Content^0.35 x Visual^0.65. The geometric combination prevents a high score on one axis from fully hiding a serious failure on another axis."),
    ]
    col_w = (PAGE_W - 2 * x - 28) / 3
    for index, (heading, body) in enumerate(columns):
        cx = x + index * (col_w + 14)
        pdf.setFillColor(LIGHT)
        pdf.roundRect(cx, y - 190, col_w, 190, 8, stroke=0, fill=1)
        pdf.setFillColor(BLUE if index < 2 else TEAL)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(cx + 16, y - 28, heading)
        write_wrapped(pdf, body, cx + 16, y - 56, col_w - 32, 10, 14, TEXT)
    y -= 238
    pdf.setFont("Helvetica-Bold", 15)
    pdf.setFillColor(TEXT)
    pdf.drawString(x, y, "Visual fidelity composition")
    y -= 28
    pdf.setFillColor(colors.white)
    pdf.setStrokeColor(MID)
    pdf.roundRect(x, y - 116, PAGE_W - 2 * x, 116, 8, stroke=1, fill=1)
    formula = "Visual = Pagination^0.10 x Layout^0.40 x Typography^0.20 x Raster^0.30"
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColor(NAVY)
    pdf.drawString(x + 22, y - 32, formula)
    details = (
        "The current weights are reasoned calibration weights, not learned constants. They make visual behavior dominant, "
        "include fonts and emphasis explicitly, and retain a smaller pagination term. Human review should update them only "
        "after the 30 pages in this report are annotated."
    )
    write_wrapped(pdf, details, x + 22, y - 58, PAGE_W - 2 * x - 44, 10, 14, TEXT)
    footer(pdf, page_number)
    pdf.showPage()


def methodology_page_two(pdf: canvas.Canvas, page_number: int) -> None:
    page_header(pdf, "Methodology 2/3 - Component definitions")
    x, y = 48, PAGE_H - 88
    rows = [
        ("Pagination", "70% page-count ratio + 30% fraction of matched words remaining on the same page."),
        ("Layout", "50% absolute matched-word geometry + 25% local reading-flow displacement + 15% reading order + 10% physical page geometry."),
        ("Typography", "Font size 35%, canonicalized family 20%, bold 12%, italic 10%, serif/monospace class 10%, color 13%."),
        ("Raster", "50% two-pixel-tolerant ink F1 + 25% symmetric edge-distance score + 25% foreground-masked SSIM at 144 DPI."),
        ("Content", "75% multiset token F1 + 25% normalized full-text character sequence similarity."),
    ]
    for heading, body in rows:
        pdf.setFillColor(LIGHT)
        pdf.roundRect(x, y - 82, PAGE_W - 2 * x, 72, 6, stroke=0, fill=1)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColor(NAVY)
        pdf.drawString(x + 16, y - 34, heading)
        write_wrapped(pdf, body, x + 150, y - 27, PAGE_W - 2 * x - 170, 10, 13, TEXT)
        y -= 86
    y -= 2
    pdf.setFont("Helvetica-Bold", 14)
    pdf.setFillColor(TEXT)
    pdf.drawString(x, y, "Why word boxes instead of PDF blocks?")
    y -= 23
    explanation = (
        "PDF producers split and merge blocks differently. Matching normalized word occurrences with a minimum-cost "
        "assignment avoids the old table failure in which identical text was rejected because one PDF emitted a whole "
        "table as one block and another emitted one block per row. Unmatched reference words are still explicit omissions; "
        "unmatched candidate words are explicit additions."
    )
    write_wrapped(pdf, explanation, x, y, PAGE_W - 2 * x, 10, 14, TEXT)
    footer(pdf, page_number)
    pdf.showPage()


def methodology_page_three(pdf: canvas.Canvas, page_number: int) -> None:
    page_header(pdf, "Methodology 3/3 - Reading the visual diffs")
    x, y = 48, PAGE_H - 92
    legend = [
        ((25, 165, 88), "Green box", "matched token within 1.5% of the page diagonal"),
        ((235, 190, 25), "Yellow box", "matched token displaced by 1.5% to 5%"),
        ((238, 135, 35), "Orange box", "matched token displaced by more than 5% or moved page"),
        ((220, 45, 45), "Red box / pixels", "reference content missing from the candidate"),
        ((35, 105, 220), "Blue box / pixels", "candidate content absent from the reference"),
        ((35, 35, 35), "Dark pixels", "exact raster foreground overlap"),
    ]
    for rgb, label, meaning in legend:
        pdf.setFillColor(colors.Color(*(value / 255 for value in rgb)))
        pdf.roundRect(x, y - 20, 28, 18, 3, stroke=0, fill=1)
        pdf.setFillColor(TEXT)
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(x + 42, y - 16, label)
        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(MUTED)
        pdf.drawString(x + 160, y - 16, meaning)
        y -= 34
    y -= 12
    pdf.setFillColor(LIGHT)
    pdf.roundRect(x, y - 205, PAGE_W - 2 * x, 205, 8, stroke=0, fill=1)
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x + 18, y - 28, "Interpretation and current limitations")
    caveats = [
        "A low content score with a high raster score is flagged: math glyph encoding can disagree even when rendering is close.",
        "Raster comparison is deliberately unregistered. Global shifts, wrong paper size, and margin changes reduce the score.",
        "Typography is measured only where words match; low matched-word counts produce a low-layout-evidence flag.",
        "Tables and equations are not yet parsed into semantic cell or expression trees. Their visible structure is measured through word geometry and raster evidence.",
        "This report is the calibration set. Score bands and weights should be frozen only after human annotations are compared with these rankings.",
    ]
    yy = y - 56
    for item in caveats:
        pdf.setFillColor(TEAL)
        pdf.circle(x + 24, yy + 3, 2.5, stroke=0, fill=1)
        yy = write_wrapped(pdf, item, x + 36, yy + 7, PAGE_W - 2 * x - 54, 9.5, 13, TEXT)
    y -= 236
    pdf.setFont("Helvetica-Bold", 11)
    pdf.setFillColor(TEXT)
    pdf.drawString(x, y, "Method references")
    refs = (
        "Wang et al., Structural Similarity (2004); Wang et al., Multi-scale SSIM (2003); "
        "PyMuPDF word and span extraction documentation; PaIRS token spatial-relation fidelity (WACV 2026)."
    )
    write_wrapped(pdf, refs, x, y - 20, PAGE_W - 2 * x, 9, 12, MUTED)
    footer(pdf, page_number)
    pdf.showPage()


def summary_pages(pdf: canvas.Canvas, records: list[dict], start_page: int) -> int:
    ordered = sorted(records, key=lambda row: row["scores"]["overall"])
    chunks = [ordered[index:index + 15] for index in range(0, len(ordered), 15)]
    page_number = start_page
    for chunk_index, chunk in enumerate(chunks, start=1):
        page_header(pdf, f"Review priority - lowest overall scores ({chunk_index}/{len(chunks)})")
        x, y = 34, PAGE_H - 82
        widths = [270, 76, 58, 64, 64, 64, 64, 64, 64, 250]
        headers = ["Sample", "Pages", "Overall", "Visual", "Content", "Layout", "Type", "Raster", "Page", "Flags"]
        pdf.setFillColor(NAVY)
        pdf.rect(x, y - 24, sum(widths), 24, stroke=0, fill=1)
        cursor = x
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 8)
        for header, width in zip(headers, widths):
            pdf.drawString(cursor + 5, y - 16, header)
            cursor += width
        y -= 24
        for row_index, row in enumerate(chunk):
            pdf.setFillColor(colors.white if row_index % 2 == 0 else LIGHT)
            pdf.rect(x, y - 38, sum(widths), 38, stroke=0, fill=1)
            values = [
                row["sample_id"], f"{row['reference_pages']}/{row['candidate_pages']}",
                f"{100 * row['scores']['overall']:.1f}", f"{100 * row['scores']['visual']:.1f}",
                f"{100 * row['scores']['content']:.1f}", f"{100 * row['scores']['layout']:.1f}",
                f"{100 * row['scores']['typography']:.1f}", f"{100 * row['scores']['raster']:.1f}",
                f"{100 * row['scores']['pagination']:.1f}", ", ".join(row["review_flags"]) or "none",
            ]
            cursor = x
            for col, (value, width) in enumerate(zip(values, widths)):
                pdf.setFont("Helvetica-Bold" if col in {0, 2} else "Helvetica", 7.5)
                pdf.setFillColor(score_color(row["scores"]["overall"]) if col == 2 else TEXT)
                clipped = value
                while stringWidth(clipped, "Helvetica", 7.5) > width - 10 and len(clipped) > 4:
                    clipped = clipped[:-2]
                if clipped != value:
                    clipped += "..."
                pdf.drawString(cursor + 5, y - 24, clipped)
                cursor += width
            y -= 38
        footer(pdf, page_number)
        pdf.showPage()
        page_number += 1
    return page_number


def draw_image_fit(pdf: canvas.Canvas, path: str, rect: tuple[float, float, float, float]) -> None:
    x, y, width, height = rect
    with Image.open(path) as image:
        ratio = min(width / image.width, height / image.height)
        draw_w, draw_h = image.width * ratio, image.height * ratio
    pdf.drawImage(ImageReader(path), x + (width - draw_w) / 2, y + (height - draw_h) / 2,
                  draw_w, draw_h, preserveAspectRatio=True, mask="auto")
    pdf.setStrokeColor(MID)
    pdf.rect(x, y, width, height, stroke=1, fill=0)


def result_page(pdf: canvas.Canvas, row: dict, page_number: int) -> None:
    scores = row["scores"]
    page_header(pdf, row["sample_id"],
                f"{row['category']} | {row['complexity_band']} | AI {row['ai_stage']}")
    margin = 34
    card_gap = 8
    card_w = (PAGE_W - 2 * margin - 6 * card_gap) / 7
    card_y = PAGE_H - 127
    cards = [
        ("Overall", scores["overall"], "headline"),
        ("Visual", scores["visual"], "65% overall"),
        ("Content", scores["content"], "35% overall"),
        ("Layout", scores["layout"], "40% visual"),
        ("Typography", scores["typography"], "20% visual"),
        ("Raster", scores["raster"], "30% visual"),
        ("Pagination", scores["pagination"], "10% visual"),
    ]
    for index, (label, value, detail) in enumerate(cards):
        score_card(pdf, margin + index * (card_w + card_gap), card_y, card_w, label, value, detail)

    info_y = card_y - 18
    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(MUTED)
    pdf.drawString(margin, info_y,
                   f"pages ref/candidate {row['reference_pages']}/{row['candidate_pages']} | "
                   f"words ref/candidate/matched {row['reference_words']}/{row['candidate_words']}/{row['matched_words']} | "
                   f"token P/R {100 * row['content_details']['token_precision']:.1f}/{100 * row['content_details']['token_recall']:.1f}")
    flags = ", ".join(row["review_flags"]) or "none"
    pdf.drawRightString(PAGE_W - margin, info_y, f"review flags: {flags}")

    panel_y = 48
    panel_h = info_y - panel_y - 34
    panel_gap = 12
    panel_w = (PAGE_W - 2 * margin - 2 * panel_gap) / 3
    panels = [
        ("Reference word boxes", row["collages"]["reference"]),
        ("Candidate word boxes", row["collages"]["candidate"]),
        ("Raster diff and error boxes", row["collages"]["diff"]),
    ]
    for index, (label, path) in enumerate(panels):
        x = margin + index * (panel_w + panel_gap)
        pdf.setFillColor(NAVY)
        pdf.roundRect(x, panel_y + panel_h + 4, panel_w, 22, 4, stroke=0, fill=1)
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(x + 8, panel_y + panel_h + 11, label)
        draw_image_fit(pdf, path, (x, panel_y, panel_w, panel_h))
    footer(pdf, page_number)
    pdf.showPage()


def build_report(records: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=PAGE_SIZE, pageCompression=1)
    pdf.setTitle("Lathe prompt-development PDF fidelity calibration")
    pdf.setAuthor("Lathe benchmark")
    cover_page(pdf, len(records))
    methodology_page_one(pdf, 2)
    methodology_page_two(pdf, 3)
    methodology_page_three(pdf, 4)
    next_page = summary_pages(pdf, records, 5)
    for record in records:
        result_page(pdf, record, next_page)
        next_page += 1
    pdf.save()


def write_outputs(records: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "pair_metrics.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    (out_dir / "metric_config.json").write_text(json.dumps(METRIC_CONFIG, indent=2) + "\n", encoding="utf-8")
    fields = [
        "sample_id", "category", "complexity_band", "ai_stage", "reference_pages", "candidate_pages",
        "reference_words", "candidate_words", "matched_words", "overall", "visual", "content",
        "pagination", "layout", "typography", "raster", "token_precision", "token_recall",
        "character_similarity", "word_geometry", "flow", "reading_order", "page_geometry",
        "font_size", "font_family", "bold", "italic", "review_flags",
    ]
    with (out_dir / "pair_metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in records:
            writer.writerow({
                "sample_id": row["sample_id"], "category": row["category"],
                "complexity_band": row["complexity_band"], "ai_stage": row["ai_stage"],
                "reference_pages": row["reference_pages"], "candidate_pages": row["candidate_pages"],
                "reference_words": row["reference_words"], "candidate_words": row["candidate_words"],
                "matched_words": row["matched_words"],
                **{key: row["scores"][key] for key in ["overall", "visual", "content", "pagination", "layout", "typography", "raster"]},
                "token_precision": row["content_details"]["token_precision"],
                "token_recall": row["content_details"]["token_recall"],
                "character_similarity": row["content_details"]["character_similarity"],
                "word_geometry": row["layout_details"]["word_geometry"],
                "flow": row["layout_details"]["flow"],
                "reading_order": row["layout_details"]["reading_order"],
                "page_geometry": row["layout_details"]["page_geometry"],
                "font_size": row["typography_details"].get("font_size", 0),
                "font_family": row["typography_details"].get("font_family", 0),
                "bold": row["typography_details"].get("bold", 0),
                "italic": row["typography_details"].get("italic", 0),
                "review_flags": ";".join(row["review_flags"]),
            })

    ordered = sorted(records, key=lambda row: row["scores"]["overall"])
    means = {name: sum(row["scores"][name] for row in records) / len(records)
             for name in ["overall", "visual", "content", "pagination", "layout", "typography", "raster"]}
    lines = [
        "# Prompt-development PDF fidelity metrics",
        "",
        f"Metric version: `{METRIC_VERSION}`",
        "",
        f"Samples: {len(records)} clean prompt-development conversions.",
        "",
        "These are development/calibration results, not held-out benchmark claims.",
        "",
        "## Aggregate scores",
        "",
        "| Component | Mean / 100 |",
        "|---|---:|",
    ]
    for name, value in means.items():
        lines.append(f"| {name.title()} | {100 * value:.1f} |")
    lines.extend([
        "",
        "## Review order",
        "",
        "| Sample | Overall | Visual | Content | Pages | Review flags |",
        "|---|---:|---:|---:|---:|---|",
    ])
    for row in ordered:
        lines.append(
            f"| `{row['sample_id']}` | {100 * row['scores']['overall']:.1f} | "
            f"{100 * row['scores']['visual']:.1f} | {100 * row['scores']['content']:.1f} | "
            f"{row['reference_pages']}/{row['candidate_pages']} | "
            f"{', '.join(row['review_flags']) or 'none'} |"
        )
    lines.extend([
        "",
        "## Reproduce",
        "",
        "```bash",
        "mamba run -n lathe python scripts/evaluation/evaluate_prompt_dev_pdf_fidelity.py",
        "```",
        "",
        "The exact weights, thresholds, renderer DPI, and normalization settings are frozen in `metric_config.json`.",
    ])
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    split = read_csv(args.split)
    if args.limit:
        split = split[:args.limit]
    selection = {row["sample_id"]: row for row in read_csv(args.selection_manifest)}
    args.result_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for index, split_row in enumerate(split, start=1):
        sample_id = split_row["sample_id"]
        selected = selection[sample_id]
        stage = selected["ai_prompt_version"]
        reference = ROOT / split_row["reference_pdf"]
        candidate = selected_candidate(sample_id, stage)
        print(f"[{index:02d}/{len(split):02d}] {sample_id} ({stage})", flush=True)
        result, ref_data, cand_data, diffs = compare_pdfs(reference, candidate)
        sample_dir = args.result_dir / "diagnostics" / sample_id
        assets = create_diagnostic_images(result, ref_data, cand_data, diffs, sample_dir)
        token_payload = {
            "matches": result["matches"],
            "unmatched_reference_indices": result["unmatched_reference_indices"],
            "unmatched_candidate_indices": result["unmatched_candidate_indices"],
        }
        (sample_dir / "token_matches.json").write_text(json.dumps(token_payload, indent=2) + "\n", encoding="utf-8")
        collages = {}
        for key, label in [("reference", "Reference"), ("candidate", "Candidate"), ("diff", "Diff")]:
            collage = make_collage(assets[key], sample_dir / f"{key}_collage.jpg", label)
            collages[key] = str(collage)
        record = public_result(result)
        record.update({
            "sample_id": sample_id,
            "category": split_row["category"],
            "complexity_band": split_row["complexity_band"],
            "ai_stage": stage,
            "diagnostic_assets": assets,
            "collages": collages,
        })
        records.append(record)

    write_outputs(records, args.result_dir)
    build_report(records, args.report)
    print(f"metrics: {args.result_dir / 'pair_metrics.csv'}")
    print(f"report: {args.report}")


if __name__ == "__main__":
    main()
