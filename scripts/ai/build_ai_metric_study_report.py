#!/usr/bin/env python3
"""Build the final AI-only PDF fidelity metric study and case book."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from pdf_fidelity import SCORECARD_VERSION, compare_pdfs  # noqa: E402
from build_ai_models_bounding_box_report import (  # noqa: E402
    AMBER,
    BLUE,
    GREEN,
    INK,
    MUTED,
    ORANGE,
    PAGE_H,
    PAGE_W,
    RED,
    RULE,
    box_counts,
    draw_boxed_pdf,
    draw_legend,
    fit_text,
)


RESULT_DIR = ROOT / "results" / "metric_calibration" / "canonical_ai_v0_3"
DEFAULT_OUT = ROOT / "output" / "pdf" / "ai_model_fidelity_metric_study_v0_3.pdf"
DEFAULT_MANIFEST = ROOT / "output" / "pdf" / "ai_model_fidelity_metric_study_v0_3_manifest.csv"
DEFAULT_TMP = ROOT / "tmp" / "pdfs" / "ai_model_fidelity_metric_study_v0_3"

NAVY = (0.055, 0.18, 0.27)
TEAL = (0.04, 0.46, 0.46)
PALE = (0.965, 0.975, 0.98)
PALE_BLUE = (0.925, 0.955, 0.97)
PALE_RED = (1.0, 0.955, 0.955)
WHITE = (1.0, 1.0, 1.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--tmp", type=Path, default=DEFAULT_TMP)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def portable(path: Path | str) -> str:
    value = Path(path)
    try:
        return str(value.relative_to(ROOT))
    except ValueError:
        return str(value)


def pct(value: str | float | None, digits: int = 1) -> str:
    if value in (None, ""):
        return "NA"
    return f"{100 * float(value):.{digits}f}"


def score(value: str | float | None, digits: int = 2) -> str:
    if value in (None, ""):
        return "NA"
    return f"{float(value):.{digits}f}"


def page_base(document: fitz.Document, title: str, subtitle: str = "", *, section: str = "") -> fitz.Page:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=None, fill=PALE)
    page.draw_rect(fitz.Rect(0, 0, PAGE_W, 10), color=None, fill=NAVY)
    if section:
        page.insert_text((36, 31), section.upper(), fontsize=6.5, fontname="hebo", color=TEAL)
    page.insert_text((36, 58), title, fontsize=21, fontname="hebo", color=INK)
    if subtitle:
        fit_text(page, fitz.Rect(36, 66, PAGE_W - 36, 95), subtitle, size=9.5, minimum=8, color=MUTED)
    page.draw_line((36, 101), (PAGE_W - 36, 101), color=RULE, width=0.7)
    page.insert_text((PAGE_W - 84, PAGE_H - 16), str(document.page_count), fontsize=6.5, fontname="helv", color=MUTED)
    return page


def card(page: fitz.Page, rect: fitz.Rect, title: str, body: str, *, accent=TEAL,
         body_size: float = 9.2) -> None:
    page.draw_rect(rect, color=RULE, fill=WHITE, width=0.6)
    page.draw_rect(fitz.Rect(rect.x0, rect.y0, rect.x0 + 6, rect.y1), color=None, fill=accent)
    page.insert_text((rect.x0 + 18, rect.y0 + 25), title, fontsize=11, fontname="hebo", color=INK)
    fit_text(page, fitz.Rect(rect.x0 + 18, rect.y0 + 38, rect.x1 - 16, rect.y1 - 13), body,
             size=body_size, minimum=7.2, color=MUTED)


def metric_badge(page: fitz.Page, rect: fitz.Rect, label: str, value: str, *, color=INK,
                 note: str = "") -> None:
    page.draw_rect(rect, color=RULE, fill=WHITE, width=0.6)
    page.insert_text((rect.x0 + 8, rect.y0 + 12), label.upper(), fontsize=5.4, fontname="hebo", color=MUTED)
    page.insert_text((rect.x0 + 8, rect.y0 + 31), value, fontsize=11.5, fontname="hebo", color=color)
    if note:
        fit_text(page, fitz.Rect(rect.x0 + 8, rect.y0 + 35, rect.x1 - 6, rect.y1 - 4), note,
                 size=5.5, minimum=5.0, color=MUTED)


def draw_table(page: fitz.Page, rect: fitz.Rect, headers: list[str], rows: list[list[str]],
               widths: list[float], *, font_size: float = 7.2, row_height: float = 29.0) -> None:
    x_positions = [rect.x0]
    for fraction in widths:
        x_positions.append(x_positions[-1] + rect.width * fraction)
    y = rect.y0
    page.draw_rect(fitz.Rect(rect.x0, y, rect.x1, y + row_height), color=NAVY, fill=NAVY, width=0.4)
    for index, header in enumerate(headers):
        fit_text(page, fitz.Rect(x_positions[index] + 6, y + 7, x_positions[index + 1] - 4, y + row_height - 4),
                 header, size=font_size, minimum=5.5, color=WHITE, font="hebo")
    y += row_height
    for row_index, row in enumerate(rows):
        fill = WHITE if row_index % 2 == 0 else (0.975, 0.98, 0.983)
        page.draw_rect(fitz.Rect(rect.x0, y, rect.x1, y + row_height), color=RULE, fill=fill, width=0.35)
        for index, value in enumerate(row):
            fit_text(page, fitz.Rect(x_positions[index] + 6, y + 6, x_positions[index + 1] - 4, y + row_height - 4),
                     value, size=font_size, minimum=5.2, color=INK)
        y += row_height


def add_cover(document: fitz.Document) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=None, fill=(0.972, 0.98, 0.983))
    page.draw_rect(fitz.Rect(0, 0, 26, PAGE_H), color=None, fill=NAVY)
    page.insert_text((70, 82), "AI model output fidelity", fontsize=33, fontname="hebo", color=INK)
    page.insert_text((70, 124), "A calibrated metric system for LaTeX-to-Typst PDFs", fontsize=19, fontname="helv", color=NAVY)
    fit_text(
        page,
        fitz.Rect(70, 175, 760, 315),
        "Deterministic axes, source-known data augmentation, a frozen blind LLM judge, "
        "leave-one-reference-out grade calibration, and a fully labeled bounding-box case book. "
        "This report contains AI outputs only.",
        size=13,
        minimum=11,
        color=MUTED,
    )
    stats = [
        ("24", "stored AI outputs"),
        ("23", "compiled and blind-rated"),
        ("186", "controlled perturbation pairs"),
        ("55/55", "monotonic severity series"),
        ("0.260", "leave-one-reference-out grade MAE"),
        ("100%", "within one blind grade"),
    ]
    x0, y0, w, h, gap = 70.0, 385.0, 215.0, 82.0, 15.0
    for index, (value, label) in enumerate(stats):
        row, column = divmod(index, 3)
        rect = fitz.Rect(x0 + column * (w + gap), y0 + row * (h + gap), x0 + column * (w + gap) + w, y0 + row * (h + gap) + h)
        page.draw_rect(rect, color=RULE, fill=WHITE, width=0.7)
        page.insert_text((rect.x0 + 14, rect.y0 + 34), value, fontsize=22, fontname="hebo", color=TEAL)
        fit_text(page, fitz.Rect(rect.x0 + 14, rect.y0 + 43, rect.x1 - 10, rect.y1 - 8), label, size=7.5, minimum=6.5, color=MUTED)
    page.draw_rect(fitz.Rect(825, 170, 1165, 580), color=RULE, fill=WHITE, width=0.7)
    page.insert_text((855, 210), "Decision", fontsize=13, fontname="hebo", color=NAVY)
    fit_text(
        page,
        fitz.Rect(855, 235, 1138, 515),
        "Use a profile, not a cosmetic similarity percentage.\n\n"
        "Grade from the worst of content, layout, typography, and pagination after monotonic calibration. "
        "Show appearance and structure beside it.\n\n"
        "Keep strict exact-reproduction gates separate from the 0-4 quality grade.\n\n"
        "Abstain or request judge review when evidence coverage is low.\n\n"
        "The grade is calibrated to one blind LLM judge, not human ratings, and remains a development result.",
        size=10.5,
        minimum=9,
        color=INK,
    )
    page.insert_text((70, PAGE_H - 35), "Study version v0.3 | 15 July 2026 | repository artifacts only | no paid model calls", fontsize=7.5, fontname="helv", color=MUTED)


def add_decision_page(document: fitz.Document) -> None:
    page = page_base(document, "The answer: a gated profile plus a calibrated ordinal grade",
                     "The system separates fidelity dimensions first, then uses a conservative grade only where blind validation supports it.", section="decision")
    card(page, fitz.Rect(36, 125, 386, 320), "1. Deterministic profile",
         "Content, layout, typography, appearance, pagination, table topology, formula glyph diagnostics, and evidence coverage are reported independently. No strong axis can erase a failed axis.")
    card(page, fitz.Rect(402, 125, 752, 320), "2. Strict status",
         "Fail means the provisional exact-reproduction gates detect low token precision, low token recall, or wrong page count. Review means evidence or a validated disagreement trigger remains. Status is not a preference rank.", accent=AMBER)
    card(page, fitz.Rect(768, 125, 1118, 320), "3. Quality grade",
         "The development 0-4 grade maps min(content, layout, typography, pagination) through a monotonic calibration. The minimum is deliberate: catastrophic reflow cannot be averaged away.", accent=NAVY)
    card(page, fitz.Rect(36, 345, 566, 585), "Grade semantics",
         "4 - Close reproduction: all major content and document structure are preserved; residual differences are limited.\n\n"
         "3 - Useful reproduction: complete enough to use, with visible but bounded layout or style differences.\n\n"
         "2 - Partial reproduction: core material survives, but at least one major visual or structural defect remains.\n\n"
         "1 - Unusable fidelity: severe overlap, page collapse, table failure, or equivalent structural damage.\n\n"
         "0 - Catastrophic or unassessable output. Compile failures are reported as unavailable, not silently graded.", accent=TEAL)
    card(page, fitz.Rect(582, 345, 1118, 585), "What is and is not verified",
         "Verified here: controlled sensitivity, monotonicity, detector behavior, blind within-sample ranking, correlation with one frozen judge, and leave-one-reference-out calibration.\n\n"
         "Not verified: agreement with humans, population-level model quality, generalization to held-out benchmark claims, aesthetic preference, or a reliable formula-equivalence metric.\n\n"
         "The grade is therefore an operational development grade. The raw axes and evidence flags remain the primary scientific record.", accent=RED)


def add_protocol_page(document: fitz.Document, canonical: list[dict[str, str]]) -> None:
    page = page_base(document, "Exact AI protocol registry",
                     "Model family is not enough. Prompt path, visual feedback, effort, and revision policy define the evaluated system.", section="scope")
    seen = {}
    for row in canonical:
        seen.setdefault(row["protocol_id"], row)
    order = [
        "gemini_prompt_stage_cascade", "sonnet_one_turn_low", "opus_one_turn_low",
        "sonnet_agentic_v1_visual_low", "opus_agentic_v3_visual_medium",
    ]
    rows = []
    for protocol_id in order:
        row = seen[protocol_id]
        revision = "stored selected stage; see case" if protocol_id == "gemini_prompt_stage_cascade" else row["revision_policy"]
        rows.append([
            row["display_label"], row["model_id"], row["generation_method"],
            row["visual_feedback"], row["effort"], revision,
        ])
    draw_table(page, fitz.Rect(36, 130, PAGE_W - 36, 370),
               ["Exact report label", "Model ID", "Generation method", "Visual feedback", "Effort", "Revision"],
               rows, [0.22, 0.15, 0.22, 0.18, 0.08, 0.15], font_size=6.6, row_height=43)
    card(page, fitz.Rect(36, 410, 575, 610), "Comparison rule",
         "Never pool one-turn and agentic outputs under a model name. The canonical set contains two one-turn math cases and six agentic hard cases. Means across protocols cover different references and are descriptive only. Shared-reference head-to-head counts are the defensible comparison.")
    card(page, fitz.Rect(591, 410, 1118, 610), "Output provenance",
         "Gemini rows point to stored OpenRouter output PDFs. Claude rows are recompiled from stored Typst harness artifacts. One Sonnet one-turn source does not compile and remains explicitly unavailable. No model was called while producing this report.", accent=NAVY)


def add_sample_page(document: fitz.Document, canonical: list[dict[str, str]]) -> None:
    page = page_base(document, "Evaluation material",
                     "Eight canonical hard references were used for the blind AI comparison; one real reference per category was used in the broader perturbation study.", section="scope")
    by_sample = {}
    for row in canonical:
        by_sample.setdefault(row["sample_id"], row)
    rows = []
    for sample_id, row in by_sample.items():
        rows.append([sample_id, row["category"], row["reference_pages"], "3 stored protocols"])
    draw_table(page, fitz.Rect(36, 130, 760, 505), ["Sample ID", "Document form", "Reference pages", "AI outputs"], rows,
               [0.32, 0.34, 0.16, 0.18], font_size=7.1, row_height=40)
    card(page, fitz.Rect(785, 130, 1118, 335), "Development use only",
         "These references come from the frozen prompt-development split. They are suitable for metric development and blind disagreement analysis, but cannot support final held-out benchmark claims.", accent=RED)
    card(page, fitz.Rect(785, 355, 1118, 560), "Coverage represented",
         "Inline and displayed math; aligned math; simple and moderate tables; figure placeholders and captions; and algorithm pseudocode. The set is deliberately hard and is not a balanced estimate of general document prevalence.")


def add_architecture_page(document: fitz.Document) -> None:
    page = page_base(document, "Metric architecture",
                     "Each axis has a target failure, an evidence requirement, and an explicit abstention or limitation path.", section="method")
    rows = [
        ["Content", "Token multiset F1 + character sequence", "Omission, addition, substitution", "PDF text extraction; math encoding"],
        ["Layout", "Matched-word geometry + local flow + order", "Displacement, reflow, order", "Requires enough matched words"],
        ["Typography", "Size, family/class, emphasis, color", "Font and emphasis drift", "Producer font metadata"],
        ["Appearance", "Tolerant ink F1 + edge distance", "Visible global drift and obstruction", "Not an object metric"],
        ["Pagination", "Page count + rare-token ordered alignment", "Missing, extra, reordered pages", "Repeated pages can be ambiguous"],
        ["Tables", "Extracted count, rows, columns, cells", "Topology damage", "Heuristic; not GriTS or TEDS"],
        ["Formula diagnostic", "Math-font glyph multiset and sequence", "Source-known glyph loss", "Producer-sensitive; no grade role"],
        ["Evidence", "Matched-token coverage and applicability", "Survivor bias and false confidence", "Routes to review/abstention"],
    ]
    draw_table(page, fitz.Rect(36, 128, PAGE_W - 36, 505), ["Axis", "Current implementation", "Target failure", "Boundary"], rows,
               [0.14, 0.31, 0.27, 0.28], font_size=7.0, row_height=43)
    card(page, fitz.Rect(36, 540, 1118, 650), "Design rule",
         "The raw profile is primary. The 0-4 grade is secondary and uses only content, layout, typography, and pagination. Appearance stays visible because it ranks well in this sample, but it is excluded from the conservative floor until its object/text decomposition is stronger.", accent=NAVY)


def add_boxes_page(document: fitz.Document) -> None:
    page = page_base(document, "Bounding boxes are evidence, not decoration",
                     "Every compiled AI case later in this report shows the reference and candidate with candidate-specific token correspondence.", section="method")
    draw_legend(page, 135)
    explanations = [
        (GREEN, "Green", "Matched token; normalized displacement is at most 1.5% of the page diagonal."),
        (AMBER, "Amber", "Matched token; displacement is between 1.5% and 5% of the page diagonal."),
        (ORANGE, "Orange", "Matched token; displacement exceeds 5% or the token lands on a different page."),
        (RED, "Red on reference", "Reference-only token. This is direct evidence of missing textual content."),
        (BLUE, "Blue on candidate", "Candidate-only token. This is direct evidence of added or rewritten textual content."),
    ]
    y = 190.0
    for color, label, body in explanations:
        page.draw_rect(fitz.Rect(55, y + 9, 73, y + 27), color=color, width=1.5)
        page.insert_text((95, y + 23), label, fontsize=10.5, fontname="hebo", color=INK)
        fit_text(page, fitz.Rect(240, y + 6, 1085, y + 35), body, size=9.0, minimum=8, color=MUTED)
        y += 58
    card(page, fitz.Rect(55, 505, 1085, 645), "Interpretation boundary",
         "A dense green page can still be wrong if formulas share extractable tokens but differ semantically, or if a table is scaled to illegibility. That is why boxes are read alongside page count, layout, appearance, table topology, and the blind case note. Vector figures do not receive word boxes.", accent=RED)


def add_augmentation_page(document: fitz.Document) -> None:
    page = page_base(document, "Source-known data augmentation",
                     "Controlled corruptions provide labels without human ratings: the evaluator knows exactly what was changed and how severity should order.", section="validation")
    families = [
        ["Translation", "1, 4, 12 pt", "Layout decreases; 1 pt has no hard fail"],
        ["Word deletion", "increasing fractions", "Recall decreases; severe deletion fails"],
        ["Word addition", "increasing token count", "Precision decreases"],
        ["Numeric replacement", "known digit changes", "Diagnostic fires; no grade role"],
        ["Obstruction", "two area levels", "Appearance/structure signal increases"],
        ["Crop", "increasing crop", "Visual and content axes decrease"],
        ["Page edits", "add, remove, reorder", "Page gate and ordered alignment respond"],
        ["Object erasure", "non-text, table row, formula glyph", "Specialized detector response or abstention"],
    ]
    draw_table(page, fitz.Rect(36, 130, 800, 505), ["Augmentation family", "Severity", "Expected response"], families,
               [0.26, 0.25, 0.49], font_size=7.4, row_height=43)
    card(page, fitz.Rect(825, 130, 1118, 320), "Run size",
         "11 real reference PDFs\n186 comparisons\n55 ordered severity series\n0 non-monotonic series", accent=NAVY, body_size=11)
    card(page, fitz.Rect(825, 340, 1118, 530), "Why this matters",
         "The augmentation harness can prove sensitivity, invariance, monotonicity, and detector recall. It cannot define aesthetic preference or acceptable real-output thresholds by itself.", accent=TEAL)


def add_detector_page(document: fitz.Document) -> None:
    page = page_base(document, "Augmentation outcomes and signal policy",
                     "Every registered expected detector fired on every applicable controlled case in the v0.3 rerun.", section="validation")
    rows = [
        ["Identity clone has no flags", "11/11", "Status invariant"],
        ["1 pt translation has no hard failure", "11/11", "Nuisance invariant"],
        ["15% deletion fails token recall", "11/11", "Critical gate"],
        ["20-word addition lowers precision", "11/11", "Continuous axis"],
        ["Numeric change raises diagnostic", "11/11", "Diagnostic only"],
        ["Extra/missing/reordered page detected", "17/17", "Gate/review"],
        ["Severe obstruction raises signal", "11/11", "Diagnostic/review evidence"],
        ["Applicable non-text erasure lowers proxy", "6/6", "Diagnostic only"],
        ["Table row erasure changes topology", "1/1", "Review"],
        ["Formula glyph erasure lowers recall", "7/7", "Diagnostic only"],
    ]
    draw_table(page, fitz.Rect(36, 130, 750, 590), ["Expected behavior", "Hits", "Role"], rows,
               [0.56, 0.17, 0.27], font_size=7.1, row_height=41)
    card(page, fitz.Rect(775, 130, 1118, 330), "Demoted after real-output audit",
         "Numeric-token mismatch fired on 30/30 prompt-development outputs. Local worst-cell appearance also fired on 30/30 and tied on 15/22 blind ranking pairs. The non-text proxy had weak blind structure correlation. All three remain logged but cannot change status or grade.", accent=RED)
    card(page, fitz.Rect(775, 350, 1118, 550), "Retained",
         "Global content and layout, typography, pagination, correspondence coverage, page-sequence disagreement, and extracted table topology retain operational roles. Formula glyph comparison is explicitly producer-sensitive and diagnostic only.", accent=TEAL)


def add_judge_page(document: fitz.Document) -> None:
    page = page_base(document, "Blind LLM judge protocol",
                     "The judge saw anonymous candidate IDs and reference/candidate page images. Model identity and automated metrics were hidden until the CSV was frozen.", section="validation")
    steps = [
        ("1", "Blind", "Random anonymous IDs within each reference. No model, provider, effort, prompt, or score was visible."),
        ("2", "Rate", "0-4 content, layout, typography, structural-object fidelity, and overall fidelity; confidence recorded."),
        ("3", "Rank", "A strict within-reference rank was assigned to compiled candidates so shared-reference comparisons are explicit."),
        ("4", "Freeze", "The rubric CSV was written before opening the blind map. One compile failure stayed unscored and in scope."),
        ("5", "Validate", "Automated axes were correlated with frozen judgments; grade candidates were tested leave-one-reference-out."),
    ]
    y = 135.0
    for number, title, body in steps:
        page.draw_circle((70, y + 27), 20, color=TEAL, fill=TEAL)
        page.insert_text((64, y + 33), number, fontsize=12, fontname="hebo", color=WHITE)
        page.insert_text((110, y + 22), title, fontsize=11, fontname="hebo", color=INK)
        fit_text(page, fitz.Rect(220, y + 5, 1080, y + 52), body, size=9.2, minimum=8, color=MUTED)
        y += 87
    card(page, fitz.Rect(55, 590, 1085, 680), "Bias boundary",
         "This is one LLM judge, not a human panel. Blinding controls model-label and metric anchoring, but not judge subjectivity. Results are a development calibration and must be revalidated with independent judges or humans before benchmark publication.", accent=RED, body_size=8.5)


def bar(page: fitz.Page, x: float, y: float, width: float, value: float, label: str, note: str,
        *, maximum: float = 1.0, color=TEAL) -> None:
    page.insert_text((x, y + 10), label, fontsize=7.6, fontname="helv", color=INK)
    page.draw_rect(fitz.Rect(x + 230, y, x + 230 + width, y + 14), color=RULE, fill=(0.91, 0.93, 0.94), width=0.4)
    page.draw_rect(fitz.Rect(x + 230, y, x + 230 + width * max(0.0, min(1.0, value / maximum)), y + 14), color=None, fill=color)
    page.insert_text((x + 240 + width, y + 10), note, fontsize=7.2, fontname="hebo", color=INK)


def add_correlation_page(document: fitz.Document, validation: dict) -> None:
    page = page_base(document, "Does the deterministic profile track the blind judge?",
                     "Spearman rank correlations on 23 compiled cases. These are diagnostic estimates on a small, non-independent sample.", section="validation")
    items = [
        ("Manual content vs automated content", validation["correlations"]["content"]["auto_content"]),
        ("Manual layout vs automated layout", validation["correlations"]["layout"]["auto_layout"]),
        ("Manual layout vs pagination", validation["correlations"]["layout"]["auto_pagination"]),
        ("Manual typography vs typography", validation["correlations"]["typography"]["auto_typography"]),
        ("Manual overall vs layout", validation["correlations"]["overall"]["auto_layout"]),
        ("Manual overall vs appearance", validation["correlations"]["overall"]["appearance_proxy"]),
        ("Manual overall vs conservative floor", validation["correlations"]["overall"]["fidelity_core_floor"]),
        ("Manual formula content vs glyph proxy", validation["correlations"]["content"]["formula_character_f1"]),
    ]
    y = 140.0
    for label, values in items:
        rho = values["rho"]
        color = RED if rho < 0.2 else AMBER if rho < 0.6 else TEAL
        bar(page, 55, y, 510, max(0.0, rho), label, f"rho {rho:.3f} | n={values['n']}", color=color)
        y += 48
    card(page, fitz.Rect(55, 555, 1085, 680), "Reading the result",
         "Layout and pagination explain most visible success and failure in this hard set. The conservative floor reaches rho=0.937 with blind overall judgment. Formula glyph similarity does not track judged formula fidelity and is excluded from the grade. Typography is directionally useful but remains metadata-sensitive.", accent=NAVY)


def add_calibration_page(document: fitz.Document, validation: dict) -> None:
    page = page_base(document, "Leave-one-reference-out grade calibration",
                     "For each held-out reference, the monotonic mapping was fitted using candidates from the other seven references only.", section="validation")
    values = validation["leave_one_sample_out_isotonic_calibration"]
    rows = []
    for name in ["auto_layout", "appearance_proxy", "auto_pagination", "visual_core_mean", "fidelity_core_floor", "all_axis_mean"]:
        result = values[name]
        rows.append([name, f"{result['mae']:.3f}", f"{result['rho']:.3f}", f"{100 * result['rounded_exact']:.1f}%", f"{100 * result['rounded_within_one']:.1f}%"])
    draw_table(page, fitz.Rect(36, 132, 760, 410), ["Calibration input", "MAE 0-4", "rho", "Exact", "Within one"], rows,
               [0.37, 0.15, 0.14, 0.17, 0.17], font_size=7.5, row_height=38)
    card(page, fitz.Rect(785, 132, 1118, 330), "Selected grade input",
         "fidelity_core_floor = min(content, layout, typography, pagination)\n\nLOO MAE: 0.260\nExact integer grade: 73.9%\nWithin one grade: 100%", accent=NAVY, body_size=10)
    card(page, fitz.Rect(36, 450, 560, 635), "Why the floor",
         "It is the most conservative interpretable candidate and has the lowest held-out MAE. A page collapse, missing content, or severe typography failure cannot be canceled by a strong score elsewhere. Content did not become the minimum on this small set, but remains in the definition for new cases.")
    card(page, fitz.Rect(576, 450, 1118, 635), "Deployment boundary",
         "Canonical case grades in this report use cross-validated predictions, not a mapping trained on the same reference. The full-fit monotonic knots are development calibration for new samples. Model claims still require a held-out evaluation split.", accent=RED)


def add_protocol_results_page(document: fitz.Document, validation: dict) -> None:
    page = page_base(document, "AI protocol results",
                     "Blind overall means and cross-validated grade means. Protocols cover different references, so the shared-reference page is the comparison result.", section="results")
    rows = []
    for values in validation["protocol_summary"].values():
        counts = values["manual_grade_counts"]
        distribution = " / ".join(f"{grade}:{counts[str(grade)]}" for grade in range(1, 5))
        rows.append([values["display_label"], str(values["n"]), f"{values['manual_overall_mean']:.2f}", f"{values['cross_validated_grade_mean']:.2f}", distribution])
    draw_table(page, fitz.Rect(36, 135, PAGE_W - 36, 405), ["Exact protocol", "n", "Blind mean", "CV grade mean", "Manual grade counts 1/2/3/4"], rows,
               [0.43, 0.07, 0.14, 0.16, 0.20], font_size=7.1, row_height=45)
    card(page, fitz.Rect(36, 445, 560, 620), "Observed pattern",
         "The agentic visual protocols dominate their one-turn and Gemini comparisons on the shared hard references. Claude Opus 4.7 agentic v3 visual medium has the strongest blind mean in its six-case set. This is a protocol result, not a model-family-only result.", accent=TEAL)
    card(page, fitz.Rect(576, 445, 1118, 620), "Do not overread the means",
         "Gemini covers eight cases, each agentic protocol covers six, one-turn Opus covers two, and one-turn Sonnet has one compiled case. Different case mixes make unpaired mean comparisons invalid. Use head-to-head wins and the case sheets.", accent=RED)


def add_head_to_head_page(document: fitz.Document, validation: dict) -> None:
    page = page_base(document, "Blind head-to-head on shared references",
                     "A win means the frozen within-reference rank preferred one compiled output over the other.", section="results")
    rows = []
    for item in validation["blind_head_to_head"]:
        rows.append([item["left_label"], item["right_label"], str(item["shared_samples"]), str(item["left_wins"]), str(item["right_wins"]), str(item["ties"])])
    draw_table(page, fitz.Rect(36, 132, PAGE_W - 36, 455), ["Left protocol", "Right protocol", "Shared", "Left wins", "Right wins", "Ties"], rows,
               [0.34, 0.34, 0.08, 0.09, 0.09, 0.06], font_size=6.8, row_height=46)
    card(page, fitz.Rect(36, 500, 1118, 650), "Defensible comparison",
         "On the six shared agentic references, Claude Opus 4.7 - agentic v3 visual medium wins 5 and Claude Sonnet 4.6 - agentic v1 visual low wins 1. Both agentic protocols win all six shared comparisons against Gemini 3.1 Flash Lite - one-turn cascade. The one-turn comparisons contain only one or two shared compiled cases and are too small for a general claim.", accent=NAVY)


def grade_fill(value: float | None):
    if value is None:
        return (0.92, 0.92, 0.92)
    return {
        0: (0.78, 0.78, 0.78),
        1: (0.96, 0.78, 0.78),
        2: (0.98, 0.89, 0.66),
        3: (0.78, 0.91, 0.86),
        4: (0.55, 0.82, 0.72),
    }[int(round(value))]


def add_grade_matrix_page(document: fitz.Document, judgments: list[dict[str, str]], blind_map: list[dict[str, str]]) -> None:
    page = page_base(document, "Blind grade matrix",
                     "Cells show manual overall grade 0-4. Blank means that exact protocol has no stored case; X means stored source did not compile.", section="results")
    map_by_blind = {row["blind_id"]: row for row in blind_map}
    protocols = [
        ("gemini_prompt_stage_cascade", "Gemini\ncascade"),
        ("sonnet_one_turn_low", "Sonnet\none-turn"),
        ("opus_one_turn_low", "Opus\none-turn"),
        ("sonnet_agentic_v1_visual_low", "Sonnet\nagentic v1"),
        ("opus_agentic_v3_visual_medium", "Opus\nagentic v3"),
    ]
    samples = []
    cells = {}
    for judgment in judgments:
        mapping = map_by_blind[judgment["blind_id"]]
        if mapping["sample_id"] not in samples:
            samples.append(mapping["sample_id"])
        value = judgment["overall_0_4"]
        cells[(mapping["sample_id"], mapping["protocol_id"])] = None if value == "" else float(value)
    x0, y0 = 300.0, 145.0
    cell_w, cell_h = 145.0, 54.0
    for column, (_, label) in enumerate(protocols):
        fit_text(page, fitz.Rect(x0 + column * cell_w, y0 - 42, x0 + (column + 1) * cell_w - 5, y0 - 4), label, size=7.0, minimum=6, color=INK, align=1, font="hebo")
    for row_index, sample_id in enumerate(samples):
        y = y0 + row_index * cell_h
        fit_text(page, fitz.Rect(36, y + 12, x0 - 16, y + cell_h - 4), sample_id, size=7.6, minimum=6.5, color=INK)
        for column, (protocol_id, _) in enumerate(protocols):
            key = (sample_id, protocol_id)
            rect = fitz.Rect(x0 + column * cell_w, y, x0 + (column + 1) * cell_w - 6, y + cell_h - 6)
            if key not in cells:
                page.draw_rect(rect, color=RULE, fill=(0.965, 0.965, 0.965), width=0.5)
                continue
            value = cells[key]
            page.draw_rect(rect, color=RULE, fill=grade_fill(value), width=0.5)
            text = "X" if value is None else str(int(value))
            page.insert_text((rect.x0 + rect.width / 2 - 4, rect.y0 + 30), text, fontsize=12, fontname="hebo", color=INK)
    draw_legend_y = y0 + len(samples) * cell_h + 18
    labels = [(1, "unusable"), (2, "major defect"), (3, "useful"), (4, "close")]
    x = 300.0
    for value, label in labels:
        page.draw_rect(fitz.Rect(x, draw_legend_y, x + 26, draw_legend_y + 18), color=RULE, fill=grade_fill(value), width=0.5)
        page.insert_text((x + 34, draw_legend_y + 14), f"{value} {label}", fontsize=7.0, fontname="helv", color=MUTED)
        x += 175
    card(page, fitz.Rect(36, 620, 1118, 700), "Pattern",
         "The matrix makes the protocol interaction visible: one-turn math outputs remain compressed; Gemini fails most table/page structure cases; agentic visual loops recover many layouts; Opus v3 is strongest on five of the six shared agentic cases.", accent=TEAL, body_size=8)


def add_limits_page(document: fitz.Document) -> None:
    page = page_base(document, "Known limitations and next research steps",
                     "The method is useful now because its boundaries are explicit. The next work should reduce those boundaries, not add more unvalidated scores.", section="decision")
    rows = [
        ["No human ratings", "One blind LLM judge anchors the grade", "Add independent judges or humans; measure inter-rater reliability"],
        ["Development split", "Canonical cases are prompt-development data", "Freeze the system; run a held-out benchmark separately"],
        ["Formula semantics", "Glyph proxy is producer-sensitive and uncorrelated", "Normalize formula regions or compare rendered math subimages"],
        ["Non-text objects", "Masked-ink proxy is weak", "Detect image/vector regions; score presence, box, and appearance"],
        ["Tables", "Count/row/column heuristic only", "Implement GriTS or TEDS(IoU) when structure extraction is stable"],
        ["Typography", "Font metadata differs across producers", "Add raster line-height, x-height, weight, and spacing measurements"],
        ["Sample size", "23 compiled cases across 8 references", "Expand blind calibration by document form and difficulty"],
    ]
    draw_table(page, fitz.Rect(36, 130, PAGE_W - 36, 520), ["Boundary", "Current consequence", "Next verifiable step"], rows,
               [0.20, 0.34, 0.46], font_size=7.2, row_height=47)
    card(page, fitz.Rect(36, 565, 1118, 675), "Freeze rule",
         "Version the renderer, extraction logic, axis definitions, evidence thresholds, and calibration knots before held-out use. Do not change them after inspecting held-out model results. Report exact protocol, compiled denominator, confidence, raw axes, status, and grade together.", accent=RED)


def add_case_page(document: fitz.Document, mapping: dict[str, str], automated: dict[str, str],
                  judgment: dict[str, str], joined: dict[str, str] | None,
                  manifest_rows: list[dict]) -> None:
    sample_id = mapping["sample_id"]
    category = sample_id.rsplit("_", 1)[0]
    reference = ROOT / "data" / "latex_benchmark_v0" / "corpus" / category / sample_id / "reference.pdf"
    page = page_base(document, sample_id, mapping["display_label"], section="case book")
    page.insert_text((36, 119), f"MODEL ID  {mapping['model_id']}", fontsize=6.3, fontname="hebo", color=MUTED)
    fit_text(page, fitz.Rect(330, 108, 1118, 128),
             f"PROTOCOL  {mapping['protocol_id']}  |  VISUAL {automated['visual_feedback']}  |  EFFORT {automated['effort']}",
             size=6.3, minimum=5.3, color=MUTED, align=2, font="hebo")
    if automated["candidate_state"] != "ok" or not mapping["candidate_pdf"]:
        page.draw_rect(fitz.Rect(160, 205, PAGE_W - 160, 555), color=(0.85, 0.55, 0.55), fill=PALE_RED, width=0.8)
        page.insert_text((205, 270), "COMPILE UNAVAILABLE", fontsize=24, fontname="hebo", color=RED)
        fit_text(page, fitz.Rect(205, 310, PAGE_W - 205, 450), automated["candidate_status"], size=11, minimum=8, color=INK)
        fit_text(page, fitz.Rect(205, 465, PAGE_W - 205, 525), judgment["notes"], size=9, minimum=8, color=MUTED)
        manifest_rows.append({
            "report_page": document.page_count, "blind_id": mapping["blind_id"], "sample_id": sample_id,
            "display_label": mapping["display_label"], "protocol_id": mapping["protocol_id"],
            "state": "unavailable", "manual_overall": "", "cv_grade": "", "reference_pdf": portable(reference),
            "candidate_pdf": "", "box_missing": "", "box_extra": "",
        })
        return

    candidate = ROOT / mapping["candidate_pdf"]
    result, reference_data, candidate_data, _ = compare_pdfs(reference, candidate)
    axes = result["scorecard"]["axes"]
    counts = box_counts(result)
    status = result["scorecard"]["status"]
    status_color = {"pass": GREEN, "review": AMBER, "fail": RED}.get(status, MUTED)
    manual_grade = judgment["overall_0_4"]
    cv_grade = joined["cv_grade_continuous_0_4"] if joined else ""
    badges = [
        ("STRICT STATUS", status.upper(), status_color, "exact gates"),
        ("BLIND GRADE", manual_grade, NAVY, "0-4 frozen judge"),
        ("CV AUTO GRADE", score(cv_grade), TEAL, "leave-one-ref-out"),
        ("PAGES R/C", f"{result['reference_pages']} / {result['candidate_pages']}", INK, "reference/candidate"),
        ("CONTENT", pct(axes["content"]["score"]), INK, "0-100"),
        ("LAYOUT", pct(axes["layout"]["score"]), INK, axes["layout"]["correspondence_evidence"]["reliability"]),
        ("TYPOGRAPHY", pct(axes["typography"]["score"]), INK, "0-100; metadata"),
        ("APPEARANCE", pct(axes["appearance_proxy"]["score"]), INK, "0-100; global"),
        ("PAGINATION", pct(axes["pagination"]["score"]), INK, "0-100; order"),
    ]
    x0, y0, gap, w, h = 36.0, 137.0, 8.0, 116.0, 49.0
    for index, (label, value, color, note) in enumerate(badges):
        metric_badge(page, fitz.Rect(x0 + index * (w + gap), y0, x0 + index * (w + gap) + w, y0 + h), label, value, color=color, note=note)
    flags = f"failed: {', '.join(result['scorecard']['failed_gates']) or 'none'} | review: {', '.join(result['scorecard']['review_flags']) or 'none'} | diagnostic: {', '.join(result['scorecard']['diagnostic_flags']) or 'none'}"
    fit_text(page, fitz.Rect(36, 192, 1118, 212), flags, size=6.1, minimum=5.3, color=MUTED)
    draw_legend(page, 220)

    left = fitz.Rect(36, 255, PAGE_W / 2 - 14, 610)
    right = fitz.Rect(PAGE_W / 2 + 14, 255, PAGE_W - 36, 610)
    for rect, label in ((left, "REFERENCE - missing words are red"), (right, "AI OUTPUT - added words are blue")):
        page.draw_rect(fitz.Rect(rect.x0, rect.y0 - 21, rect.x1, rect.y0 - 3), color=RULE, fill=PALE_BLUE, width=0.5)
        page.insert_text((rect.x0 + 7, rect.y0 - 9), label, fontsize=6.5, fontname="hebo", color=INK)
    reference_records = {record["reference_index"]: record for record in result["matches"]}
    candidate_records = {record["candidate_index"]: record for record in result["matches"]}
    draw_boxed_pdf(page, reference, left, reference_data, reference_records, set(result["unmatched_reference_indices"]), side="reference")
    draw_boxed_pdf(page, candidate, right, candidate_data, candidate_records, set(result["unmatched_candidate_indices"]), side="candidate")

    page.draw_rect(fitz.Rect(36, 625, 1118, 704), color=RULE, fill=WHITE, width=0.5)
    page.insert_text((48, 644), "BLIND NOTE", fontsize=6.0, fontname="hebo", color=TEAL)
    fit_text(page, fitz.Rect(132, 632, 900, 670), judgment["notes"], size=7.2, minimum=6.3, color=INK)
    page.insert_text((920, 644), f"rank {judgment['within_sample_rank']} | confidence {judgment['confidence_low_medium_high']}", fontsize=6.5, fontname="hebo", color=MUTED)
    fit_text(page, fitz.Rect(48, 675, 1110, 699),
             f"boxes close {counts['near']} | moved {counts['moved']} | far/page {counts['far_or_page']} | missing {counts['missing']} | extra {counts['extra']} | source {automated['source_artifact']}",
             size=5.7, minimum=5.0, color=MUTED)
    manifest_rows.append({
        "report_page": document.page_count, "blind_id": mapping["blind_id"], "sample_id": sample_id,
        "display_label": mapping["display_label"], "protocol_id": mapping["protocol_id"], "state": "ok",
        "manual_overall": manual_grade, "cv_grade": cv_grade, "reference_pdf": portable(reference),
        "candidate_pdf": mapping["candidate_pdf"], "box_missing": counts["missing"], "box_extra": counts["extra"],
    })


def add_references_page(document: fitz.Document) -> None:
    page = page_base(document, "Metric literature and adoption decisions",
                     "Primary sources examined for document, table, formula, perceptual, and judge methodology.", section="references")
    refs = [
        ("OmniDocBench", "Modular text, formula, table, and reading-order evaluation; adopted as the architectural precedent.", "https://arxiv.org/abs/2412.07626"),
        ("GriTS", "Grid-table similarity for topology, content, and location; recommended next table metric after reliable structure extraction.", "https://arxiv.org/abs/2203.12555"),
        ("TEDS(IoU)", "Tree-edit table structure with geometric cell similarity; reviewed, not implemented in v0.3.", "https://arxiv.org/abs/2208.00385"),
        ("CDM", "Formula evaluation designed for visually equivalent expressions; motivates replacing the producer-sensitive glyph proxy.", "https://arxiv.org/abs/2409.03643"),
        ("SSIM", "Classical structural image similarity; foreground use was tested but removed from the active appearance proxy after poor discrimination.", "https://doi.org/10.1109/TIP.2003.819861"),
        ("LPIPS", "Learned perceptual image similarity for natural images; reviewed but not adopted without typeset-domain calibration.", "https://openaccess.thecvf.com/content_cvpr_2018/html/Zhang_The_Unreasonable_Effectiveness_CVPR_2018_paper.html"),
        ("DISTS", "Structure and texture perceptual similarity; reviewed but not adopted without document-domain validation.", "https://arxiv.org/abs/2004.07728"),
        ("LLM judge position bias", "Evidence that order can bias pairwise judgments; motivates anonymization, fixed layout, and freezing before unblinding.", "https://arxiv.org/abs/2406.07791"),
    ]
    y = 125.0
    for index, (name, decision, url) in enumerate(refs, start=1):
        page.insert_text((45, y + 14), f"{index:02d}", fontsize=9, fontname="hebo", color=TEAL)
        page.insert_text((85, y + 14), name, fontsize=9, fontname="hebo", color=INK)
        fit_text(page, fitz.Rect(260, y + 2, 850, y + 37), decision, size=7.1, minimum=6.2, color=MUTED)
        fit_text(page, fitz.Rect(865, y + 2, 1120, y + 37), url, size=5.8, minimum=5.1, color=NAVY)
        page.draw_line((45, y + 43), (1120, y + 43), color=RULE, width=0.35)
        y += 65
    card(page, fitz.Rect(45, 660, 1120, 730), "Citation rule",
         "The report adopts modular evaluation and bias controls. It does not claim to implement GriTS, TEDS(IoU), CDM, LPIPS, or DISTS. Those methods are labeled as precedents or next steps, not hidden behind generic names.", accent=NAVY, body_size=7.5)


def add_reproduction_page(document: fitz.Document) -> None:
    page = page_base(document, "Reproduction and artifact map",
                     "All commands use the repository's lathe mamba environment. No API calls are required.", section="reproduce")
    commands = [
        "mamba run -n lathe python -m unittest tests/test_pdf_fidelity.py",
        "mamba run -n lathe python scripts/evaluation/evaluate_reference_perturbations.py",
        "mamba run -n lathe python scripts/evaluation/audit_prompt_dev_scorecard.py",
        "mamba run -n lathe python scripts/evaluation/audit_canonical_ai_models.py",
        "mamba run -n lathe python scripts/evaluation/analyze_manual_validation.py",
        "mamba run -n lathe python scripts/ai/build_ai_metric_study_report.py",
    ]
    y = 135.0
    for index, command in enumerate(commands, start=1):
        page.draw_rect(fitz.Rect(55, y, 1110, y + 49), color=RULE, fill=WHITE, width=0.5)
        page.insert_text((70, y + 19), f"{index}.", fontsize=7.5, fontname="hebo", color=TEAL)
        fit_text(page, fitz.Rect(100, y + 8, 1090, y + 42), command, size=7.5, minimum=6.3, color=INK, font="cour")
        y += 62
    artifacts = (
        "Core metric: scripts/evaluation/pdf_fidelity.py\n"
        "Augmentations: results/metric_calibration/reference_perturbations_v0_3/\n"
        "Prompt audit: results/metric_calibration/prompt_dev_scorecard_v0_3/\n"
        "Canonical AI audit: results/metric_calibration/canonical_ai_v0_3/\n"
        "Frozen blind rubric: results/metric_calibration/canonical_ai_v0_3/manual_audit/manual_rubric.csv\n"
        "Unblinded validation: results/metric_calibration/canonical_ai_v0_3/manual_audit/manual_validation.md\n"
        "Case manifest: output/pdf/ai_model_fidelity_metric_study_v0_3_manifest.csv"
    )
    card(page, fitz.Rect(55, 530, 1110, 710), "Artifact locations", artifacts, accent=NAVY, body_size=8.2)


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

    canonical = read_csv(RESULT_DIR / "canonical_ai_scorecard.csv")
    audit_dir = RESULT_DIR / "manual_audit"
    blind_map = read_csv(audit_dir / "blind_case_map.csv")
    judgments = read_csv(audit_dir / "manual_rubric.csv")
    joined = read_csv(audit_dir / "manual_judgments_unblinded.csv")
    validation = json.loads((audit_dir / "manual_validation.json").read_text())
    canonical_by_key = {(row["sample_id"], row["protocol_id"]): row for row in canonical}
    judgment_by_blind = {row["blind_id"]: row for row in judgments}
    joined_by_blind = {row["blind_id"]: row for row in joined}

    document = fitz.open()
    add_cover(document)
    add_decision_page(document)
    add_protocol_page(document, canonical)
    add_sample_page(document, canonical)
    add_architecture_page(document)
    add_boxes_page(document)
    add_augmentation_page(document)
    add_detector_page(document)
    add_judge_page(document)
    add_correlation_page(document, validation)
    add_calibration_page(document, validation)
    add_protocol_results_page(document, validation)
    add_head_to_head_page(document, validation)
    add_grade_matrix_page(document, judgments, blind_map)
    add_limits_page(document)

    manifest_rows: list[dict] = []
    toc = [[1, "Decision and scope", 1], [1, "Method and validation", 5], [1, "AI protocol results", 12], [1, "Case book", document.page_count + 1]]
    for mapping in blind_map:
        automated = canonical_by_key[(mapping["sample_id"], mapping["protocol_id"])]
        add_case_page(document, mapping, automated, judgment_by_blind[mapping["blind_id"]], joined_by_blind.get(mapping["blind_id"]), manifest_rows)
        toc.append([2, f"{mapping['sample_id']} - {mapping['display_label']}", document.page_count])
    add_references_page(document)
    add_reproduction_page(document)
    toc.extend([[1, "References", document.page_count - 1], [1, "Reproduction", document.page_count]])

    document.set_toc(toc)
    document.set_metadata({
        "title": "AI model output fidelity - calibrated metric study v0.3",
        "subject": "AI-only LaTeX-to-Typst PDF evaluation with blind validation and bounding boxes",
        "author": "Lathe benchmark",
        "keywords": "PDF fidelity, LaTeX, Typst, LLM judge, evaluation metrics, bounding boxes",
    })
    document.save(args.out, garbage=4, deflate=True)
    pages = document.page_count
    document.close()
    write_manifest(args.manifest, manifest_rows)
    shutil.rmtree(args.tmp)
    print(f"pdf={args.out}")
    print(f"manifest={args.manifest}")
    print(f"pages={pages}")
    print(f"scorecard={SCORECARD_VERSION}")


if __name__ == "__main__":
    main()
