#!/usr/bin/env python3
"""Build the frozen rendered-PDF fidelity research report."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

import fitz
from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "results" / "metric_research_v1"
FULL = BASE / "full_157_v1"
AI = BASE / "ai_outputs_frozen_v1"
TRIAL = BASE / "ai_outputs_center_q90_trial_v1"
FREEZE = BASE / "final_report_inputs_v1"
DEFAULT_OUT = ROOT / "output" / "pdf" / "rendered_pdf_fidelity_research_report_v1.pdf"

PAGE_W, PAGE_H = landscape(A3)
MARGIN = 44
NAVY = colors.HexColor("#123047")
INK = colors.HexColor("#18242D")
MUTED = colors.HexColor("#53636E")
TEAL = colors.HexColor("#137A78")
ORANGE = colors.HexColor("#D8672A")
GREEN = colors.HexColor("#2D7A4B")
OCHRE = colors.HexColor("#A36D13")
RED = colors.HexColor("#D13C3C")
CYAN = colors.HexColor("#00A7C4")
RULE = colors.HexColor("#CBD3D8")
PALE = colors.HexColor("#F4F7F8")
WHITE = colors.white


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def _float(value: object) -> float | None:
    try:
        number = float(str(value))
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _pct(value: float | None, digits: int = 1) -> str:
    return "ABSTAIN" if value is None else f"{100 * value:.{digits}f}%"


def _num(value: float | None, digits: int = 3) -> str:
    return "ABSTAIN" if value is None else f"{value:.{digits}f}"


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty quantile")
    position = (len(ordered) - 1) * q
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


class Report:
    def __init__(self, output: Path) -> None:
        output.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(output), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
        self.page_no = 0

    def cover(self, title: str, subtitle: str, conclusion: str) -> None:
        self.page_no += 1
        c = self.c
        c.setFillColor(PALE)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.rect(0, 0, 28, PAGE_H, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 31)
        c.drawString(82, PAGE_H - 120, title)
        c.setFillColor(TEAL)
        c.setFont("Helvetica", 17)
        c.drawString(84, PAGE_H - 160, subtitle)
        self.paragraph(conclusion, 84, PAGE_H - 365, 680, 150, 15, INK)
        c.setStrokeColor(RULE)
        c.setFillColor(WHITE)
        c.roundRect(820, PAGE_H - 410, 310, 235, 8, fill=1, stroke=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(844, PAGE_H - 215, "BOTTOM LINE")
        self.paragraph(
            "The present system is reproducible and explainable, but it is not yet a real universal PDF grade. "
            "Content, pagination, and localized raster evidence are useful diagnostics. The strict controlled-response "
            "gate fails, structure abstains, and the original layout scalar collapses on every AI output.",
            844, PAGE_H - 380, 260, 145, 11, INK,
        )
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(84, 54, "Research artifact - one recorded AI route - no human ratings - no universal score")
        c.showPage()

    def page(self, title: str, subtitle: str = "", section: str = "") -> None:
        self.page_no += 1
        c = self.c
        c.setFillColor(WHITE)
        c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.rect(0, PAGE_H - 9, PAGE_W, 9, fill=1, stroke=0)
        if section:
            c.setFillColor(TEAL)
            c.setFont("Helvetica-Bold", 7)
            c.drawString(MARGIN, PAGE_H - 29, section.upper())
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(MARGIN, PAGE_H - 58, title)
        if subtitle:
            c.setFillColor(MUTED)
            c.setFont("Helvetica", 9.5)
            c.drawString(MARGIN, PAGE_H - 78, subtitle[:190])
        c.setStrokeColor(RULE)
        c.line(MARGIN, PAGE_H - 92, PAGE_W - MARGIN, PAGE_H - 92)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7)
        c.drawRightString(PAGE_W - MARGIN, 23, str(self.page_no))

    def end(self) -> None:
        self.c.showPage()

    def save(self) -> None:
        self.c.save()

    def paragraph(
        self, text: str, x: float, y: float, width: float, height: float,
        size: float = 10, color=INK, bold: bool = False,
    ) -> None:
        style = ParagraphStyle(
            "body", fontName="Helvetica-Bold" if bold else "Helvetica",
            fontSize=size, leading=size * 1.32, textColor=color, alignment=TA_LEFT,
            spaceAfter=0,
        )
        paragraph = Paragraph(text, style)
        _w, used = paragraph.wrap(width, height)
        if used > height + 0.1:
            raise ValueError(f"paragraph overflow: {text[:80]}")
        paragraph.drawOn(self.c, x, y + height - used)

    def card(
        self, x: float, y: float, width: float, height: float,
        title: str, body: str, accent=TEAL,
    ) -> None:
        c = self.c
        c.setFillColor(WHITE)
        c.setStrokeColor(RULE)
        c.roundRect(x, y, width, height, 5, fill=1, stroke=1)
        c.setFillColor(accent)
        c.rect(x, y, 6, height, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 18, y + height - 27, title)
        self.paragraph(
            body.replace("\n", "<br/>"), x + 18, y + 13,
            width - 34, height - 50, 9.5, MUTED,
        )

    def table(
        self, rows: list[list[str]], x: float, y_top: float, widths: list[float],
        row_height: float = 30, font_size: float = 8,
    ) -> float:
        header_style = ParagraphStyle(
            "table_header", fontName="Helvetica-Bold", fontSize=font_size,
            leading=font_size * 1.12, textColor=WHITE,
        )
        body_style = ParagraphStyle(
            "table_body", fontName="Helvetica", fontSize=font_size,
            leading=font_size * 1.12, textColor=INK,
        )
        rendered_rows = [
            [
                Paragraph(str(value).replace("\n", "<br/>"), header_style if index == 0 else body_style)
                for value in row
            ]
            for index, row in enumerate(rows)
        ]
        table = Table(rendered_rows, colWidths=widths, rowHeights=[row_height] * len(rows))
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), font_size),
            ("LEADING", (0, 0), (-1, -1), font_size * 1.15),
            ("GRID", (0, 0), (-1, -1), 0.4, RULE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("BACKGROUND", (0, 1), (-1, -1), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
        ]))
        width = sum(widths)
        height = row_height * len(rows)
        table.wrapOn(self.c, width, height)
        table.drawOn(self.c, x, y_top - height)
        return y_top - height


def _status_chip(c: canvas.Canvas, x: float, y: float, label: str) -> None:
    palette = {
        "VERIFIED": GREEN, "TRIAL": OCHRE, "ABSTAINING": MUTED,
        "NOT IMPLEMENTED": NAVY, "FAILED GATE": RED,
    }
    width = max(70, 7.1 * len(label) + 18)
    c.setFillColor(palette[label])
    c.roundRect(x, y, width, 20, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x + width / 2, y + 6.5, label)


def _bar(c: canvas.Canvas, x: float, y: float, width: float, value: float, label: str,
         note: str = "", color=TEAL) -> None:
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y + 17, label)
    c.setFillColor(PALE)
    c.roundRect(x, y, width, 10, 3, fill=1, stroke=0)
    c.setFillColor(color)
    c.roundRect(x, y, max(1, width * min(1, max(0, value))), 10, 3, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7)
    c.drawRightString(x + width, y + 17, note or f"{value:.3f}")


def _render_page(pdf: Path, page_index: int, dpi: int = 120) -> Image.Image:
    with fitz.open(pdf) as document:
        pix = document[page_index].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")


def _draw_document(
    c: canvas.Canvas, pdf: Path, x: float, y: float, width: float, height: float,
    label: str, overlays: list[tuple[int, list[float], str]] | None = None,
) -> None:
    overlays = overlays or []
    with fitz.open(pdf) as document:
        count = min(3, document.page_count)
    cols = 1 if count == 1 else 2
    rows = math.ceil(count / cols)
    gap = 10
    label_h = 22
    cell_w = (width - gap * (cols - 1)) / cols
    cell_h = (height - label_h - gap * (rows - 1)) / rows
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x, y + height - 10, label)
    for index in range(count):
        image = _render_page(pdf, index)
        draw = ImageDraw.Draw(image)
        for page_index, bbox, color_name in overlays:
            if page_index != index:
                continue
            color = "#D13C3C" if color_name == "red" else "#00A7C4"
            px = [
                int(bbox[0] * image.width), int(bbox[1] * image.height),
                int(bbox[2] * image.width), int(bbox[3] * image.height),
            ]
            draw.rectangle(px, outline=color, width=max(4, image.width // 250))
        row, col = divmod(index, cols)
        target_x = x + col * (cell_w + gap)
        target_y = y + height - label_h - (row + 1) * cell_h - row * gap
        scale = min(cell_w / image.width, cell_h / image.height)
        draw_w, draw_h = image.width * scale, image.height * scale
        left = target_x + (cell_w - draw_w) / 2
        bottom = target_y + (cell_h - draw_h) / 2
        c.drawImage(ImageReader(image), left, bottom, draw_w, draw_h, preserveAspectRatio=True)
        c.setStrokeColor(RULE)
        c.rect(left, bottom, draw_w, draw_h, fill=0, stroke=1)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 6.5)
        c.drawString(left, bottom - 9, f"PAGE {index + 1}")
        image.close()
    if count < 1:
        raise ValueError(f"empty PDF: {pdf}")


def _axis_values(rows: list[dict[str, str]], axis: str) -> list[float]:
    return [value for row in rows if (value := _float(row.get(f"axis_{axis}"))) is not None]


def _select_controlled_examples(
    answers: list[dict[str, str]], all_results: list[dict[str, str]],
) -> list[dict[str, str]]:
    results = {
        (row["sample_id"], row["variant"], row["severity"]): row for row in all_results
    }
    selected = []
    for variant in ("text_deletion", "block_right", "local_occlusion", "table_row_occlusion"):
        candidates = [
            answer for answer in answers
            if answer["variant"] == variant and answer["candidate_valid"] == "true"
            and answer["mutation_visible"] == "true" and answer["label_correct"] == "true"
            and (answer["sample_id"], answer["variant"], answer["severity"]) in results
        ]
        if not candidates:
            continue
        axis = candidates[0]["expected_axis"].split("+")[0].replace("_only", "")
        values = [
            _float(results[(row["sample_id"], row["variant"], row["severity"])].get(f"axis_{axis}"))
            for row in candidates
        ]
        numeric = [value for value in values if value is not None]
        target = median(numeric) if numeric else 0
        selected.append(min(
            candidates,
            key=lambda row: abs((
                _float(results[(row["sample_id"], row["variant"], row["severity"])].get(f"axis_{axis}"))
                or 0
            ) - target),
        ))
    return selected


def _select_ai_examples(
    scores: list[dict[str, str]], trial_scores: list[dict[str, str]],
) -> list[tuple[str, dict[str, str]]]:
    trial = {row["sample_id"]: row for row in trial_scores}
    eligible = [
        row for row in scores
        if row["analysis_role"] == "prompt_heldout_metric_test_adaptive_pipeline"
    ] or scores
    content = [float(row["axis_content"]) for row in eligible]
    layout = [float(trial[row["sample_id"]]["axis_layout"]) for row in eligible]
    content_median = median(content)
    content_p10 = _quantile(content, 0.10)
    layout_p10 = _quantile(layout, 0.10)
    representative = min(
        [row for row in eligible if row["page_count_match"] == "true"] or eligible,
        key=lambda row: abs(float(row["axis_content"]) - content_median),
    )
    content_tail = min(eligible, key=lambda row: abs(float(row["axis_content"]) - content_p10))
    layout_tail = min(
        eligible, key=lambda row: abs(float(trial[row["sample_id"]]["axis_layout"]) - layout_p10)
    )
    pagination = min(
        [row for row in scores if row["page_count_match"] == "false"] or scores,
        key=lambda row: float(row["axis_pagination"]),
    )
    return [
        ("Representative held metric-test output", representative),
        ("Content-axis lower-tail case", content_tail),
        ("Center-layout trial lower-tail case", layout_tail),
        ("Pagination mismatch case", pagination),
    ]


def _comparison_page(
    report: Report, title: str, subtitle: str, reference: Path, candidate: Path,
    notes: list[str], reference_overlays=None, candidate_overlays=None, ai: bool = False,
) -> None:
    report.page(title, subtitle, "Visual evidence")
    _draw_document(
        report.c, reference, MARGIN, 112, (PAGE_W - 3 * MARGIN) / 2, PAGE_H - 245,
        "REFERENCE PDF", reference_overlays,
    )
    _draw_document(
        report.c, candidate, (PAGE_W + MARGIN) / 2, 112,
        (PAGE_W - 3 * MARGIN) / 2, PAGE_H - 245,
        "AI-PRODUCED TYPST PDF" if ai else "CONTROLLED CANDIDATE PDF", candidate_overlays,
    )
    y = 91
    for note in notes[:3]:
        report.c.setFillColor(INK)
        report.c.circle(MARGIN + 3, y + 4, 2, fill=1, stroke=0)
        report.paragraph(note, MARGIN + 12, y - 6, PAGE_W - 2 * MARGIN - 12, 22, 8.5, MUTED)
        y -= 22
    report.end()


def build(output: Path, freeze_dir: Path) -> int:
    frozen_path = freeze_dir / "frozen_report_inputs.json"
    register_path = freeze_dir / "final_report_register_157.csv"
    if not frozen_path.exists() or not register_path.exists():
        raise ValueError("report inputs are not frozen; run preflight with --freeze-dir first")
    frozen = _read_json(frozen_path)
    register = _read_csv(register_path)
    if len(register) != 157 or len({row["sample_id"] for row in register}) != 157:
        raise ValueError("frozen register must contain 157 unique samples")

    profile = _read_csv(BASE / "corpus_profile_157.csv")
    validation = _read_json(FULL / "controlled_validation.json")
    validation_layout = _read_json(FULL / "controlled_validation_layout_iou.json")
    pilot_layout = _read_json(BASE / "layout_center_pilot_11_v1" / "validation_layout.json")
    determinism = _read_json(FULL / "determinism_validation.json")
    bands = _read_json(FULL / "axis_severity_bands.json")
    merge = _read_json(FULL / "merged_run_summary.json")
    ai_summary = _read_json(AI / "summary.json")
    trial_summary = _read_json(TRIAL / "summary.json")
    audit_analysis = _read_json(BASE / "llm_visual_audit_analysis_v1.json")
    ai_scores = _read_csv(AI / "ai_output_axis_scores.csv")
    trial_scores = _read_csv(TRIAL / "ai_output_axis_scores.csv")
    control_answers = _read_csv(FULL / "visual_audit" / "audit_answer_key.csv")
    all_results = _read_csv(FULL / "augmentation_results.csv") + _read_csv(
        BASE / "category_audit_repeat_v1" / "augmentation_results.csv"
    )
    controlled_examples = _select_controlled_examples(control_answers, all_results)
    ai_examples = _select_ai_examples(ai_scores, trial_scores)
    trial_by_sample = {row["sample_id"]: row for row in trial_scores}

    report = Report(output)
    report.cover(
        "Rendered PDF fidelity",
        "A 157-reference study of explainable metrics for AI-produced Typst PDFs",
        "A deterministic harness can expose content loss, pagination changes, and localized raster residuals. "
        "It cannot yet support a universal grade: the strict controlled-response gate fails, specialized "
        "structure abstains, and the first layout scalar has no variance on the AI corpus.",
    )

    report.page("Executive result", "The negative findings are part of the result, not hidden caveats.", "Decision")
    report.card(44, 470, 345, 200, "What is established",
                "All 157 references were exercised by 16,167 deterministic cases. The 471-case repeat is byte, render, score, and localization identical. Content inventory, pagination, and raster localization remain useful raw diagnostics.", GREEN)
    report.card(410, 470, 345, 200, "What failed",
                "The strict adjacent-severity gate is 0.843 against a 0.950 requirement. The exact-box layout projection is 0.0 for all 156 AI outputs. Category and variant failures are retained rather than averaged away.", RED)
    report.card(776, 470, 370, 200, "What the report does",
                "Reports independent axes, evidence, applicability, and abstention. It evaluates one recorded Gemini route, not multiple models. It does not estimate human preference and does not create an overall score.", TEAL)
    report.paragraph(
        "This report evaluates one AI conversion corpus against 157 accepted LaTeX reference PDFs. "
        "It does not compare multiple AI models and does not estimate human preference.<br/><br/>"
        "The primary result is an axis vector with evidence and abstention. There is no universal quality score.",
        54, 170, PAGE_W - 108, 220, 15, INK, True,
    )
    report.end()

    report.page("How to read the evidence", "Status is method maturity; scored/abstain is pair-level evidence state.", "Guide")
    statuses = [
        ("VERIFIED", "Passed the stated project check. This is not human-quality validation."),
        ("TRIAL", "Implemented but below a gate, incomplete, or transfer-limited."),
        ("ABSTAINING", "Applicable concept, insufficient validated extraction or scoring."),
        ("NOT IMPLEMENTED", "Literature method discussed but not present in this evaluator."),
    ]
    for index, (label, body) in enumerate(statuses):
        y = 590 - index * 92
        _status_chip(report.c, 64, y + 26, label)
        report.paragraph(body, 245, y, 770, 60, 11, INK)
    report.card(64, 125, 1050, 120, "Bounding-box legend",
                "RED: generator-recorded controlled edit region. CYAN: registered raster-residual enclosure in the stated coordinate frame. Cyan is a localization diagnostic only; it does not identify semantic cause, axis attribution, or human importance.", CYAN)
    report.end()

    report.page("Claim boundary", "What the executed study measures and what it explicitly does not.", "Scope")
    report.table([
        ["Area", "Executed evidence", "Claim limit"],
        ["Controlled study", "16,167 cases; 157 sources; three severities; 628 retained audit cases", "Known synthetic edits are not AI-output realism or training data"],
        ["AI transfer", "156 compiled PDFs from one recorded API route", "No cross-model rank; adaptive prompt cascade is descriptive"],
        ["Ratings", "Blind LLM research audit", "No human ratings; judge is not ground truth"],
        ["Aggregation", "Five raw projections plus structure abstention", "No compensatory scalar and no AI severity labels"],
        ["Specialized content", "Applicability and visible audit notes", "No GriTS, TEDS, CDM, or validated figure grade"],
    ], 64, 650, [150, 420, 510], 64, 9)
    report.end()

    counts = Counter(row["category"] for row in profile)
    report.page("Corpus", "157 accepted references, 239 pages, 11 document forms.", "Data")
    report.table(
        [["Document form", "Sources"]] + [[key, str(value)] for key, value in sorted(counts.items())],
        64, 650, [620, 150], 39, 9,
    )
    page_counts = Counter(int(row["reference_pages"]) for row in profile)
    report.card(875, 470, 250, 180, "Reference pages",
                f"1 page: {page_counts[1]}\n2 pages: {page_counts[2]}\n3 pages: {page_counts[3]}\n\nEvery accepted reference is 1-3 pages.", TEAL)
    report.card(875, 260, 250, 180, "Metric split", "metric_dev: 80\nmetric_validation: 39\nmetric_test: 38\n\nSource PDF is the inference cluster.", ORANGE)
    report.end()

    report.page("Evaluated AI route", "Exact recorded identity and denominator before any metric.", "AI corpus")
    report.table([
        ["Field", "Frozen value"],
        ["API route", "google/gemini-3.1-flash-lite"],
        ["Compiled candidates", "156 / 157"],
        ["Missing candidate", "06_tables_moderate_030"],
        ["Selected stages", ", ".join(f"{key}: {value}" for key, value in ai_summary["selected_prompt_stages"].items())],
        ["Final attempts", ", ".join(f"attempt {key}: {value}" for key, value in ai_summary["final_attempts"].items())],
        ["Identity limitation", "API route recorded; immutable provider checkpoint hash not returned"],
        ["Protocol limitation", "Adaptive v1-v3 rescue cascade; not one frozen-prompt benchmark"],
    ], 64, 650, [235, 830], 53, 9)
    report.end()

    report.page("Measurement architecture", "Eligibility first, then raw evidence, projections, and abstention.", "Method")
    steps = [
        ("1  ELIGIBILITY", "Compilation, pages, canvases, source and model provenance"),
        ("2  EXTRACTION", "Tokens, blocks, boxes, style, raster, page boundaries"),
        ("3  RAW EVIDENCE", "Matches, misses, displacement, size errors, residual regions"),
        ("4  PROJECTIONS", "Independent high-is-better diagnostics; no overall score"),
        ("5  EXPLANATION", "Page, region, coordinate frame, axis state, versions"),
    ]
    for index, (title, body) in enumerate(steps):
        x = 55 + index * 225
        report.card(x, 360, 205, 220, title, body, TEAL if index < 3 else ORANGE)
        if index < len(steps) - 1:
            report.c.setStrokeColor(NAVY)
            report.c.line(x + 205, 470, x + 224, 470)
    report.paragraph(
        "A missing output is not scored. An extraction failure is evaluator abstention, not candidate zero. "
        "Every AI severity band is disabled and recorded as abstain.",
        64, 155, 1050, 90, 13, INK, True,
    )
    report.end()

    report.page("Five executed projections", "Transparent harness projections, not published-method substitutes.", "Method")
    report.table([
        ["Axis", "Executed projection", "Primary limitation", "Status"],
        ["Content", "Token multiset precision/recall/F1", "Ignores order and repeated-token identity", "TRIAL"],
        ["Layout v1", "q10 exact-token matched box IoU", "Sensitive on controls; 0.0 on all AI outputs", "FAILED GATE"],
        ["Typography", "min(style coverage, exp(-size max), exp(-20 baseline q90))", "Mixed diagnostic; no domain calibration", "TRIAL"],
        ["Appearance", "Unregistered tolerant ink F1", "Canvas and renderer confounds; not semantic", "TRIAL"],
        ["Pagination", "Page-count ratio x page-break F1", "Depends on block matching; coarse", "TRIAL"],
        ["Structure", "No scalar", "Validated common table/formula/figure representation absent", "ABSTAINING"],
    ], 44, 650, [120, 360, 490, 120], 58, 8.3)
    report.paragraph(
        "The center-displacement trial uses 1 - min(1, q90 center distance / sqrt(2)). It transfers without collapse but misses its 0.95 pilot gate and is not promoted.",
        55, 120, 1080, 70, 10.5, INK,
    )
    report.end()

    report.page("Published methods: exact implementation status", "Design targets are not mislabeled as implemented metrics.", "Literature")
    report.table([
        ["Method", "Use in this study", "Status", "Primary source"],
        ["CLEval", "Design target for recognition/localization", "NOT IMPLEMENTED", "Baek et al., CVPRW 2020"],
        ["LTSim", "Next layout experiment", "NOT IMPLEMENTED", "arXiv:2407.12356"],
        ["GriTS", "Table topology/content/location target", "NOT IMPLEMENTED", "arXiv:2203.12555"],
        ["TEDS", "Common-HTML table cross-check", "NOT IMPLEMENTED", "PubTabNet, arXiv:1911.10683"],
        ["CDM", "Formula token/position target", "NOT IMPLEMENTED", "arXiv:2409.03643"],
        ["SSIM / MS-SSIM", "Raster diagnostic literature only", "NOT IMPLEMENTED", "Wang et al., 2004"],
        ["Kendall order tau", "Design target; current extractor lacks validated order", "NOT IMPLEMENTED", "Lapata, 2006"],
        ["LLM judge", "Blind research audit only", "TRIAL", "Position-bias literature, 2024"],
    ], 44, 650, [165, 385, 160, 390], 55, 8.2)
    report.end()

    report.page("Controlled augmentation program", "Known edit type, severity, and location across every accepted source.", "Validation")
    report.card(64, 485, 250, 170, "Planned", "16,167 deterministic cases\n157 unique sources\n11 forms\n3 severity levels", TEAL)
    report.card(335, 485, 250, 170, "Executed", f"{merge['status_counts']['applied']:,} applied\n{merge['status_counts']['not_applicable']} not applicable\n0 failed", GREEN)
    report.card(606, 485, 250, 170, "Visual audit", "628 retained severity-2 candidates\n4 cases per source\n314 A / 314 B", ORANGE)
    report.card(877, 485, 250, 170, "Reality limit", "Synthetic controls test response. They do not reproduce the frequency or importance of real AI errors.", RED)
    report.paragraph(
        "Families cover content edits, local and global geometry, typography and reflow, raster corruption, pagination, tables, figures, formulas, lists, algorithms, cross-references, forms, and fixed compounds. Unsupported structure modules still abstain.",
        64, 190, 1060, 170, 13, INK,
    )
    report.end()

    report.page("Splits and leakage controls", "Prompt development and metric development are different axes.", "Validation")
    report.table([
        ["Role", "Count", "Allowed use"],
        ["metric_dev", "80", "Internal projection/profile development"],
        ["metric_validation", "39", "Frozen held gate"],
        ["metric_test", "38", "One-time confirmation; 8 rows are prompt development"],
        ["prompt_dev", "30", "Prompt development only; descriptive AI results"],
        ["prompt_heldout + metric_test", "30 compiled", "Strongest joint reference subset; still adaptive-pipeline descriptive"],
    ], 64, 650, [260, 130, 670], 67, 9)
    report.card(64, 180, 1060, 120, "Leakage conclusion",
                "The AI corpus cannot support a frozen one-prompt benchmark claim. The adaptive rescue pipeline is reported as a pipeline, and prompt-development samples are excluded from held benchmark summaries.", RED)
    report.end()

    dm = validation["document_macro"]
    gates = validation["gate_assessment"]["overall"]
    report.page("Corrected validation gates", "Source-clustered analysis with 2,000 bootstrap replicates.", "Results")
    gate_rows = [
        ["Gate", "Observed", "Requirement", "Result"],
        ["Adjacent severity ordering", f"{dm['adjacent_monotonic_accuracy']:.3f}", ">= 0.950", "FAIL"],
        ["Kendall tau-b lower 95% CI", f"{validation['bootstrap_95_ci']['document_macro']['kendall_tau_b']['low']:.3f}", "> 0.700", "PASS"],
        ["Lossless invariant false positives", f"{dm['invariant_false_positive_rate']:.3f}", "< 0.010", "PASS"],
        ["Raster residual localization", f"{dm['localization_hit_rate']:.3f}", ">= 0.900", "PASS"],
        ["Overall controlled status", "fails_or_incomplete", "all mandatory + no hidden scope flags", "FAIL"],
    ]
    report.table(gate_rows, 64, 650, [360, 180, 270, 160], 62, 9)
    report.paragraph(
        "A strong global tau does not rescue local ties or reversals. Family, variant, and category failures are preserved; they are not averaged away.",
        64, 180, 1040, 90, 12, INK, True,
    )
    report.end()

    report.page("Where the controlled system fails", "The failure map is the basis for next experiments.", "Results")
    flags = validation["gate_assessment"]
    rows = [
        ["Scope", "Flagged", "Examples"],
        ["Families", str(len(flags["family_flags"])), ", ".join(list(flags["family_flags"])[:6])],
        ["Variants", str(len(flags["variant_flags"])), ", ".join(list(flags["variant_flags"])[:8])],
        ["Categories", str(len(flags["category_flags"])), "all 11 forms have at least one adjacent-order or compound flag"],
        ["Compounds", f"dominance {dm['compound_dominance_accuracy']:.3f}", "some compound scores exceed a named component"],
        ["Structure", "no scalar", "tables, formulas, and figures abstain rather than use heuristic counts"],
    ]
    report.table(rows, 64, 650, [200, 220, 640], 72, 8.8)
    report.end()

    old_layout = validation_layout["document_macro"]
    new_layout = pilot_layout["document_macro"]
    report.page("Layout transfer: sensitivity versus robustness", "A stopped trial, not a post-hoc replacement.", "Results")
    report.table([
        ["Property", "Exact-box IoU q10", "Center q90 trial"],
        ["AI range", "0.000 - 0.000", "0.417 - 0.949"],
        ["AI median", "0.000", "0.791"],
        ["Controlled sources", "157", "11-form pilot"],
        ["Adjacent ordering", f"{old_layout['adjacent_monotonic_accuracy']:.3f}", f"{new_layout['adjacent_monotonic_accuracy']:.3f}"],
        ["Target-axis drop", f"{old_layout['target_axis_drop']:.3f}", f"{new_layout['target_axis_drop']:.4f}"],
        ["Decision", "reject as AI grade", "trial; pilot gate failed"],
    ], 64, 650, [300, 360, 360], 63, 9)
    report.card(64, 135, 1020, 105, "Stopping rule applied",
                "The center trial fixes non-discrimination but remains weak and scores 0.914 against the 0.950 adjacent-order gate. A second 16,167-case run was not justified after pilot failure.", ORANGE)
    report.end()

    report.page("Internal synthetic profiles", "Coarse defect-equivalence bands are disabled on AI outputs.", "Results")
    rows = [["Axis", "Internal status", "Validation", "Test", "AI labels"]]
    for axis, definition in bands["axes"].items():
        held = definition.get("held_gate") or {}
        rows.append([
            axis.removeprefix("axis_"), definition["status"],
            str(held.get("metric_validation_pass", "NA")),
            str(held.get("metric_test_confirmation_pass", "NA")), "ABSTAIN",
        ])
    report.table(rows, 64, 650, [220, 300, 190, 190, 170], 58, 8.5)
    report.paragraph(
        "A coarse four-band classification can pass while stricter adjacent severity ordering fails. These labels mean similarity to controlled defect levels, not acceptable or unacceptable quality.",
        64, 165, 1030, 90, 11, INK,
    )
    report.end()

    report.page("Independent determinism", "The same 471 cases were regenerated from references and seed.", "Reproducibility")
    for index, (label, value) in enumerate([
        ("Score + localization", determinism["score_and_localization_agreement"]),
        ("PDF bytes", determinism["pdf_byte_agreement"]),
        ("Rendered pixels", determinism["render_pixel_agreement"]),
    ]):
        _bar(report.c, 80, 560 - index * 110, 720, value, label, f"{value:.3f}", GREEN)
    report.card(850, 350, 275, 260, "Repeat accounting",
                f"471 shared cases\n157 retained PDF pairs\n{determinism['reference_only_cases']:,} expected non-repeat rows\n0 repeat-only rows\nTolerance 1e-12", TEAL)
    report.end()

    controlled_audit = audit_analysis["controlled"]
    report.page("Blind controlled audit", "Four shuffled A/B cases per source; truth revealed only after freeze.", "Manual audit")
    report.card(64, 470, 250, 170, "Coverage", f"{controlled_audit['judged']} judged\n{controlled_audit['abstained']} abstained\n{_pct(controlled_audit['coverage'])} coverage", TEAL)
    report.card(335, 470, 250, 170, "Panel detection", _pct(controlled_audit["changed_panel_accuracy"]) + "\nnon-abstained cases", GREEN)
    report.card(606, 470, 250, 170, "Axis label", _pct(controlled_audit["axis_label_accuracy"]) + "\nnon-abstained cases", ORANGE)
    post = controlled_audit["post_unblind"]
    report.card(877, 470, 250, 170, "Post-unblind", f"valid {_pct(post['candidate_valid']['rate'])}\nvisible {_pct(post['mutation_visible']['rate'])}\ncyan useful {_pct(post['predicted_box_useful']['rate'])}", CYAN)
    report.paragraph(
        "The audit measures mutation visibility, blind identification, and localization usefulness. It does not convert controlled edits into a human utility scale.",
        64, 205, 1050, 110, 13, INK, True,
    )
    report.end()

    for answer in controlled_examples:
        target = json.loads(answer["known_target_bbox"])
        predicted = json.loads(answer["predicted_bbox"]) if answer["predicted_bbox"] else None
        ref_overlays = []
        if predicted:
            ref_overlays.append((int(answer["predicted_page"]), predicted, "cyan"))
        candidate_overlays = [(int(answer["target_page"]), target, "red")]
        _comparison_page(
            report,
            f"Controlled example: {answer['variant'].replace('_', ' ')}",
            f"CONTROLLED PERTURBATION | {answer['sample_id']} | severity {answer['severity']} | expected {answer['expected_axis']}",
            _resolve(answer["source_pdf"]), _resolve(answer["candidate_pdf"]),
            [
                "Red is the generator-recorded edit region on the candidate.",
                "Cyan is the registered raster-residual enclosure on the reference frame.",
                f"Post-unblind: visible={answer['mutation_visible']}; target box={answer['target_box_correct']}; cyan useful={answer['predicted_box_useful']}.",
            ],
            ref_overlays, candidate_overlays, False,
        )

    ai_audit = audit_analysis["ai_outputs"]
    report.page("Blind AI-output audit", "156 complete document pairs; model, prompt, axes, and residual hidden.", "Manual audit")
    issue_rows = [["Axis", "None", "Minor", "Moderate", "Major", "Unclear", "Score vs severity rho"]]
    for axis, result in ai_audit["axes"].items():
        counts_axis = result["issue_counts"]
        issue_rows.append([
            axis, str(counts_axis.get("none", 0)), str(counts_axis.get("minor", 0)),
            str(counts_axis.get("moderate", 0)), str(counts_axis.get("major", 0)),
            str(counts_axis.get("unclear", 0)), _num(result["spearman_score_vs_issue_severity"]),
        ])
    report.table(issue_rows, 64, 650, [190, 120, 120, 130, 120, 120, 250], 62, 8.4)
    report.paragraph(
        "Negative rho is the expected direction because higher automatic fidelity should coincide with lower visible issue severity. Association with this LLM audit can falsify a metric; it cannot establish human validity.",
        64, 135, 1040, 85, 10.5, INK,
    )
    report.end()

    report.page("AI raw-axis distributions", "156 scored outputs; structure abstains; bands are disabled.", "AI results")
    axes = ("content", "layout", "typography", "appearance", "pagination")
    for index, axis in enumerate(axes):
        summary = trial_summary["axes"][axis] if axis == "layout" else ai_summary["axes"][axis]
        y = 610 - index * 102
        minimum, med, maximum = summary["raw_min"], summary["raw_median"], summary["raw_max"]
        _bar(report.c, 100, y, 760, med, axis.upper(), f"min {minimum:.3f} | median {med:.3f} | max {maximum:.3f}", TEAL if axis != "layout" else ORANGE)
    report.card(890, 350, 250, 255, "Interpretation",
                "Content is exact-token retention. Layout shown here is the non-promoted center trial because v1 is constant zero. Typography and appearance are strongly renderer/canvas sensitive. Pagination is coarse. Structure abstains.", ORANGE)
    report.end()

    report.page("Prompt stages and analysis roles", "The evaluated corpus is an adaptive conversion pipeline.", "AI results")
    stage_rows = [["Selected stage", "Outputs"]] + [
        [key, str(value)] for key, value in ai_summary["selected_prompt_stages"].items()
    ]
    report.table(stage_rows, 64, 650, [400, 170], 46, 9)
    role_rows = [["Analysis role", "Outputs"]] + [
        [key.replace("_", " "), str(value)] for key, value in ai_summary["analysis_roles"].items()
    ]
    report.table(role_rows, 680, 650, [380, 150], 58, 8.5)
    report.end()

    report.page("Page and canvas confounds", "These are causes to report, not errors to silently fold into appearance.", "AI results")
    report.card(64, 455, 310, 190, "Page count", f"{156 - ai_summary['page_count_mismatches']} match\n{ai_summary['page_count_mismatches']} mismatch", TEAL)
    report.card(400, 455, 310, 190, "Canvas sequence", f"{156 - ai_summary['canvas_mismatches']} match\n{ai_summary['canvas_mismatches']} mismatch", RED)
    report.card(736, 455, 390, 190, "Dominant transfer confound", "144 references use Letter while their candidates use A4. Appearance and typography values therefore mix conversion differences with canvas and renderer behavior.", ORANGE)
    report.paragraph(
        "Canvas mismatch is kept as explicit evidence. It is not registered away, because changing Letter to A4 can itself be a fidelity defect. At the same time, it prevents a clean interpretation of low page-raster similarity as an AI semantic failure.",
        64, 180, 1060, 150, 13, INK,
    )
    report.end()

    report.page("AI category profile", "Medians are comparable within an axis column only.", "AI results")
    category_values: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for row in ai_scores:
        for axis in ("content", "typography", "appearance", "pagination"):
            category_values[row["category"]][axis].append(float(row[f"axis_{axis}"]))
        category_values[row["category"]]["layout_trial"].append(
            float(trial_by_sample[row["sample_id"]]["axis_layout"])
        )
    category_rows = [["Document form", "Content", "Layout trial", "Typography", "Appearance", "Pagination"]]
    for category, values in sorted(category_values.items()):
        category_rows.append([
            category, *[_num(median(values[key])) for key in (
                "content", "layout_trial", "typography", "appearance", "pagination"
            )],
        ])
    report.table(category_rows, 44, 650, [310, 145, 145, 145, 145, 145], 42, 7.8)
    report.end()

    for title, row in ai_examples:
        trial_row = trial_by_sample[row["sample_id"]]
        residual = json.loads(row["top_difference_bbox"]) if row["top_difference_bbox"] else None
        ref_overlays = []
        cand_overlays = []
        if residual:
            target = ref_overlays if row["top_difference_side"] == "paired_reference_frame" else cand_overlays
            target.append((int(row["top_difference_page"]), residual, "cyan"))
        _comparison_page(
            report, title,
            f"AI OUTPUT | google/gemini-3.1-flash-lite | prompt {row['ai_selected_stage']} | {row['sample_id']}",
            ROOT / row["reference_pdf"], ROOT / row["candidate_pdf"],
            [
                f"Raw axes: content {float(row['axis_content']):.3f}; center-layout trial {float(trial_row['axis_layout']):.3f}; typography {float(row['axis_typography']):.3f}; appearance {float(row['axis_appearance']):.3f}; pagination {float(row['axis_pagination']):.3f}.",
                f"Page-count match={row['page_count_match']}; canvas match={row['canvas_match']}; analysis role={row['analysis_role']}.",
                "Cyan, when present, is a registered raster-residual enclosure, not a source-known AI defect box.",
            ],
            ref_overlays, cand_overlays, True,
        )

    report.page("Negative results", "A useful benchmark report says what not to use.", "Conclusion")
    report.table([
        ["Rejected interpretation", "Evidence"],
        ["One overall PDF score", "No validated common utility scale; axes compensate incorrectly"],
        ["Exact-box IoU as AI layout grade", "0.0 for all 156 outputs"],
        ["Synthetic bands as AI quality", "All 936 AI band cells explicitly abstain"],
        ["Raster similarity as semantic correctness", "145 canvas mismatches and renderer sensitivity"],
        ["Structure from page-level heuristics", "No validated GriTS/TEDS/CDM/common object representation"],
        ["Cross-model leaderboard", "Only one near-complete recorded AI route"],
        ["Human preference claim", "No human ratings"],
    ], 64, 650, [390, 670], 62, 9)
    report.end()

    report.page("Method status at freeze", "Status does not change because a chart looks favorable.", "Conclusion")
    status_rows = [
        ["Component", "Status", "Reason"],
        ["Deterministic generation and rerun", "VERIFIED", "471/471 scores and 157/157 byte/render artifacts agree"],
        ["Content token inventory", "TRIAL", "Useful diagnostic; order and repeated-token ambiguity remain"],
        ["Layout IoU q10", "FAILED GATE", "Sensitive on controls; no variance on AI corpus"],
        ["Center q90 layout", "TRIAL", "Non-collapsing transfer; 0.914 pilot ordering below 0.950"],
        ["Typography scalar", "TRIAL", "Mixed transform and canvas/renderer sensitivity"],
        ["Raster residual", "TRIAL", "Strong controlled localization; not semantic"],
        ["Pagination", "TRIAL", "Page and boundary evidence; block matching dependency"],
        ["Specialized structure", "ABSTAINING", "No validated common extraction"],
        ["CLEval/LTSim/GriTS/TEDS/CDM/SSIM", "NOT IMPLEMENTED", "Literature targets only"],
    ]
    report.table(status_rows, 44, 650, [330, 180, 590], 51, 8.2)
    report.end()

    report.page("Next experiments", "Ordered by scientific dependency with explicit stopping rules.", "Conclusion")
    next_rows = [
        ["Priority", "Experiment", "Promotion rule"],
        ["1", "Implement published LTSim and strict-label variant over source-backed blocks", "Held adjacent ordering >=0.95; no AI collapse; defect evidence retained"],
        ["2", "Adapt CLEval to reliable PDF character quads with extraction coverage", "Recognition/localization gates pass by form; abstain below coverage threshold"],
        ["3", "Create common table HTML/grid representation; implement GriTS and TEDS", "Row/column/span perturbations ordered on validation and test"],
        ["4", "Create cross-language formula token representation; trial CDM", "Digit/operator/subscript defects localized without syntax bias"],
        ["5", "Add a second frozen AI route and one fixed prompt", "Only then attempt paired cross-model comparison"],
        ["6", "Collect independent expert human ratings when available", "Only then calibrate acceptability or utility; keep axes visible"],
    ]
    report.table(next_rows, 44, 650, [90, 490, 540], 68, 8.4)
    report.end()

    report.page("Primary references and artifact map", "Readable links and exact local evidence paths.", "References")
    references = [
        "Lapata (2006), Automatic Evaluation of Information Ordering - https://aclanthology.org/J06-4002/",
        "Baek et al. (2020), CLEval - https://openaccess.thecvf.com/content_CVPRW_2020/",
        "Smock et al. (2022), GriTS - https://arxiv.org/abs/2203.12555",
        "Zhong et al. (2020), PubTabNet/TEDS - https://arxiv.org/abs/1911.10683",
        "CDM (2024) - https://arxiv.org/abs/2409.03643",
        "LTSim (2024) - https://arxiv.org/abs/2407.12356",
        "Wang et al. (2004), SSIM - https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf",
        "Position bias study (2024) - https://arxiv.org/abs/2406.07791",
    ]
    report.paragraph("<br/>".join(references), 64, 345, 1050, 300, 10.5, INK)
    report.paragraph(
        "Frozen inputs: results/metric_research_v1/final_report_inputs_v1/frozen_report_inputs.json<br/>"
        "Controlled validation: results/metric_research_v1/full_157_v1/controlled_validation.json<br/>"
        "AI scores: results/metric_research_v1/ai_outputs_frozen_v1/ai_output_axis_scores.csv<br/>"
        "LLM audit analysis: results/metric_research_v1/llm_visual_audit_analysis_v1.json",
        64, 115, 1050, 160, 9.5, MUTED,
    )
    report.end()

    register_trial = {row["sample_id"]: row for row in trial_scores}
    rows_per_page = 12
    for start in range(0, len(register), rows_per_page):
        chunk = register[start:start + rows_per_page]
        report.page(
            f"Complete 157-source register {start + 1}-{start + len(chunk)}",
            "Exact AI route: google/gemini-3.1-flash-lite | compare values within an axis only | structure: ABSTAIN",
            "Appendix",
        )
        table_rows = [[
            "Sample", "Form", "Prompt / metric", "Ref / AI pages", "Stage", "Content",
            "Layout v1", "Center trial", "Typography", "Appearance", "Pagination", "State",
        ]]
        for row in chunk:
            trial_row = register_trial.get(row["sample_id"], {})
            table_rows.append([
                row["sample_id"], row["document_form"].replace("_", " "),
                f"{row['prompt_split']}\n{row['metric_partition']}",
                f"{row['reference_pages']} / {trial_row.get('candidate_pages', '-')}",
                row["selected_prompt_stage"] or "-",
                _num(_float(row["raw_axis_content"])),
                _num(_float(row["raw_axis_layout"])),
                _num(_float(trial_row.get("axis_layout"))),
                _num(_float(row["raw_axis_typography"])),
                _num(_float(row["raw_axis_appearance"])),
                _num(_float(row["raw_axis_pagination"])),
                row["ai_output_state"] if row["ai_output_state"] == "compiled" else row["missing_reason"],
            ])
        report.table(
            table_rows, 28, 650,
            [155, 145, 120, 80, 75, 72, 72, 78, 78, 78, 78, 110],
            42, 6.6,
        )
        report.end()

    report.save()
    return report.page_no


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--freeze-dir", type=Path, default=FREEZE)
    args = parser.parse_args()
    pages = build(args.out, args.freeze_dir)
    print(json.dumps({"output": str(args.out), "pages": pages}, indent=2))


if __name__ == "__main__":
    main()
