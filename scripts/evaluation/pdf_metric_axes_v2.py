#!/usr/bin/env python3
"""Layered, evidence-first PDF comparison used by the metric v2 research pass.

The evaluator intentionally has no universal score.  It adds three components
to the v1 raw measurements:

* exact inventories for numbers, operators, and citation-like markers;
* a text-block optimal-transport diagnostic with every material flow exposed;
* registered and unregistered single/multi-scale SSIM diagnostics.

The transport and multi-scale diagnostics are transparent adaptations, not
claims of reproducing LTSim or canonical MS-SSIM.  Structure-specific table,
formula, and figure axes continue to abstain until common semantic extraction
exists for both PDFs.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

import cv2
import fitz
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from skimage.metrics import structural_similarity

try:
    from . import pdf_metric_axes_v1 as v1
except ImportError:  # pragma: no cover - direct script execution
    import pdf_metric_axes_v1 as v1


ROOT = Path(__file__).resolve().parents[2]
EVALUATOR_VERSION = "pdf_metric_axes_v2"
MAX_EVIDENCE_ITEMS = 24
_NUMBER_RE = re.compile(r"(?<![\w.])[+-]?(?:\d+(?:[.,]\d+)*|\.\d+)(?:[eE][+-]?\d+)?%?")
_CITATION_RE = re.compile(
    r"\[(?:\d+[a-z]?(?:\s*[-,;]\s*\d+[a-z]?){0,12})\]|"
    r"\((?:18|19|20)\d{2}[a-z]?\)"
)
_OPERATOR_CHARS = frozenset("=<>±×÷−+*/^∑∏∫√≈≠≤≥→←↔∞∂∇∈∉⊂⊆∪∩")


def serialize_path(path: str | Path) -> str:
    """Use a portable repo-relative path when the input is inside this checkout."""

    resolved = Path(path).expanduser().resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def _inventory(reference: Sequence[str], candidate: Sequence[str]) -> dict[str, Any]:
    metrics = dict(v1._inventory_metrics(reference, candidate))
    left = Counter(reference)
    right = Counter(candidate)
    missing = list((left - right).elements())
    extra = list((right - left).elements())
    metrics.update(
        exact_match=left == right,
        missing=missing[:MAX_EVIDENCE_ITEMS],
        extra=extra[:MAX_EVIDENCE_ITEMS],
        missing_count=len(missing),
        extra_count=len(extra),
    )
    return metrics


def _critical_content_axis(reference: v1.PdfExtraction, candidate: v1.PdfExtraction) -> dict[str, Any]:
    reference_text = "\n\f\n".join(page.text for page in reference.pages)
    candidate_text = "\n\f\n".join(page.text for page in candidate.pages)

    def numbers(text: str) -> list[str]:
        return _NUMBER_RE.findall(v1.normalize_text(text))

    def citations(text: str) -> list[str]:
        return _CITATION_RE.findall(v1.normalize_text(text))

    def operators(extraction: v1.PdfExtraction) -> list[str]:
        return [char.normalized for char in extraction.chars if char.normalized in _OPERATOR_CHARS]

    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "numbers": _inventory(numbers(reference_text), numbers(candidate_text)),
            "operators": _inventory(operators(reference), operators(candidate)),
            "citation_markers": _inventory(citations(reference_text), citations(candidate_text)),
        },
        "evidence": {
            "normalization": "Unicode NFKC; case preserved; multiset comparison",
            "number_pattern": _NUMBER_RE.pattern,
            "operator_inventory": "".join(sorted(_OPERATOR_CHARS)),
            "citation_pattern": _CITATION_RE.pattern,
        },
        "interpretation": (
            "Exact critical-symbol inventories prevent visually small numeric or operator errors "
            "from disappearing inside a document-level text average. Empty inventories are "
            "reported as exact but do not establish construct applicability."
        ),
    }


def _content_axis_v2(
    reference: v1.PdfExtraction,
    candidate: v1.PdfExtraction,
    word_pairs: Sequence[tuple[v1.PdfWord, v1.PdfWord]],
    block_pairs: Sequence[tuple[v1.PdfBlock, v1.PdfBlock, float]],
) -> dict[str, Any]:
    result = v1._content_axis(reference, candidate, word_pairs, block_pairs)

    def strict_text(extraction: v1.PdfExtraction) -> str:
        value = "\n\f\n".join(page.text for page in extraction.pages).replace("\u00ad", "")
        value = unicodedata.normalize("NFC", value)
        return re.sub(r"\s+", " ", value).strip()

    left_text = strict_text(reference)
    right_text = strict_text(candidate)
    strict_inventory = _inventory(left_text.split(), right_text.split())
    result["metrics"]["strict_nfc_token_inventory"] = strict_inventory
    result["metrics"]["strict_nfc_document_edit_similarity"] = v1._normalized_edit_similarity(
        left_text, right_text
    )
    result["metrics"]["compatibility_nfkc_token_inventory"] = result["metrics"].pop(
        "token_inventory"
    )
    result["metrics"]["compatibility_nfkc_document_edit_similarity"] = result["metrics"].pop(
        "document_normalized_edit_similarity"
    )
    result["interpretation"] = (
        "Strict NFC preservation is the primary text view. NFKC is reported separately as a "
        "compatibility view for ligature/encoding equivalence; it never hides the strict mismatch."
    )
    return result


def _stacked_bbox(extraction: v1.PdfExtraction, block: v1.PdfBlock, page_denominator: int) -> tuple[float, float, float, float]:
    box = v1._normalized_bbox(block.bbox, v1._page_for(extraction, block.page))
    return (
        box[0],
        (block.page + box[1]) / page_denominator,
        box[2],
        (block.page + box[3]) / page_denominator,
    )


def _area(box: Sequence[float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def _generalized_iou(left: Sequence[float], right: Sequence[float]) -> float:
    intersection = v1._intersection_area(tuple(left), tuple(right))
    union = _area(left) + _area(right) - intersection
    if union <= 0.0:
        return 1.0
    enclosing = (
        min(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        max(left[3], right[3]),
    )
    enclosing_area = _area(enclosing)
    iou = intersection / union
    return iou - ((enclosing_area - union) / enclosing_area if enclosing_area else 0.0)


def _transport_plan(costs: np.ndarray, left_mass: np.ndarray, right_mass: np.ndarray) -> np.ndarray:
    """Solve the finite optimal-transport linear program deterministically."""

    rows, columns = costs.shape
    variable_count = rows * columns
    constraint_rows: list[int] = []
    constraint_columns: list[int] = []
    values: list[float] = []
    rhs: list[float] = []
    constraint = 0
    for row in range(rows):
        for column in range(columns):
            constraint_rows.append(constraint)
            constraint_columns.append(row * columns + column)
            values.append(1.0)
        rhs.append(float(left_mass[row]))
        constraint += 1
    # The last destination constraint is redundant once all source constraints
    # and the other destination constraints are satisfied.
    for column in range(max(0, columns - 1)):
        for row in range(rows):
            constraint_rows.append(constraint)
            constraint_columns.append(row * columns + column)
            values.append(1.0)
        rhs.append(float(right_mass[column]))
        constraint += 1
    matrix = coo_matrix(
        (values, (constraint_rows, constraint_columns)),
        shape=(constraint, variable_count),
    ).tocsr()
    result = linprog(
        costs.reshape(-1),
        A_eq=matrix,
        b_eq=np.asarray(rhs, dtype=np.float64),
        bounds=(0.0, None),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"block transport optimization failed: {result.message}")
    plan = np.asarray(result.x, dtype=np.float64).reshape(rows, columns)
    plan[plan < 1e-12] = 0.0
    return plan


def _text_ltsim_axis(reference: v1.PdfExtraction, candidate: v1.PdfExtraction) -> dict[str, Any]:
    """Published LTSim equations on the supported all-text, per-page subset."""

    pages: list[dict[str, Any]] = []
    paired_page_count = min(len(reference.pages), len(candidate.pages))
    for page_index in range(paired_page_count):
        left_blocks = [block for block in reference.blocks if block.page == page_index]
        right_blocks = [block for block in candidate.blocks if block.page == page_index]
        if not left_blocks or not right_blocks:
            pages.append(
                {
                    "page": page_index,
                    "status": "abstain_empty_layout",
                    "reference_block_count": len(left_blocks),
                    "candidate_block_count": len(right_blocks),
                    "reason": "Published LTSim transport assumes two non-empty layouts.",
                }
            )
            continue
        costs = np.zeros((len(left_blocks), len(right_blocks)), dtype=np.float64)
        left_boxes = [
            v1._normalized_bbox(block.bbox, reference.pages[page_index]) for block in left_blocks
        ]
        right_boxes = [
            v1._normalized_bbox(block.bbox, candidate.pages[page_index]) for block in right_blocks
        ]
        for row, left_box in enumerate(left_boxes):
            for column, right_box in enumerate(right_boxes):
                delta_bbox = (1.0 + _generalized_iou(left_box, right_box)) / 2.0
                delta_label = 1.0  # every element in this supported subset is text
                costs[row, column] = 1.0 - (delta_bbox + delta_label) / 2.0
        left_mass = np.full(len(left_blocks), 1.0 / len(left_blocks), dtype=np.float64)
        right_mass = np.full(len(right_blocks), 1.0 / len(right_blocks), dtype=np.float64)
        plan = _transport_plan(costs, left_mass, right_mass)
        emd = float(np.sum(plan * costs))
        flows = []
        for row, column in zip(*np.nonzero(plan)):
            flows.append(
                {
                    "reference_block_index": left_blocks[int(row)].index,
                    "candidate_block_index": right_blocks[int(column)].index,
                    "mass": float(plan[row, column]),
                    "cost": float(costs[row, column]),
                    "reference_bbox_normalized": list(left_boxes[int(row)]),
                    "candidate_bbox_normalized": list(right_boxes[int(column)]),
                }
            )
        flows.sort(key=lambda item: (-(item["mass"] * item["cost"]), item["reference_block_index"], item["candidate_block_index"]))
        pages.append(
            {
                "page": page_index,
                "status": "scored",
                "reference_block_count": len(left_blocks),
                "candidate_block_count": len(right_blocks),
                "emd": emd,
                "text_ltsim": math.exp(-emd),
                "largest_cost_contributions": flows[:MAX_EVIDENCE_ITEMS],
            }
        )
    for page_index in range(paired_page_count, max(len(reference.pages), len(candidate.pages))):
        pages.append(
            {
                "page": page_index,
                "status": "abstain_unpaired_page",
                "reason": "Text-LTSim is undefined without a paired non-empty layout; pagination reports this failure.",
            }
        )
    scored = [page for page in pages if page["status"] == "scored"]
    values = [float(page["text_ltsim"]) for page in scored]
    weights = [max(page["reference_block_count"], page["candidate_block_count"]) for page in scored]
    return {
        "status": "scored" if scored else "abstain",
        "applicable": True if scored else None,
        "metrics": {
            "paired_page_count": paired_page_count,
            "scored_page_count": len(scored),
            "abstained_page_count": len(pages) - len(scored),
            "text_ltsim_page_macro": sum(values) / len(values) if values else None,
            "text_ltsim_element_weighted": (
                sum(value * weight for value, weight in zip(values, weights)) / sum(weights)
                if weights and sum(weights)
                else None
            ),
            "text_ltsim_worst_page": min(values) if values else None,
        },
        "evidence": {
            "pages": pages,
            "equations": (
                "uniform mass; delta_bbox=(1+GIoU)/2; delta_label=1 for text; "
                "mu=1-(delta_bbox+delta_label)/2; Text-LTSim=exp(-EMD), sigma=1"
            ),
        },
        "interpretation": (
            "Faithful published LTSim equations on extracted text blocks only. It measures "
            "text-layout geometry/segmentation, not full semantic layout; non-text classes abstain."
        ),
    }


def _block_transport_axis(reference: v1.PdfExtraction, candidate: v1.PdfExtraction) -> dict[str, Any]:
    if not reference.blocks or not candidate.blocks:
        return {
            "status": "abstain",
            "applicable": None,
            "metrics": {"reference_block_count": len(reference.blocks), "candidate_block_count": len(candidate.blocks)},
            "evidence": {},
            "reason": "Both PDFs must expose text blocks for block transport.",
        }

    page_denominator = max(len(reference.pages), len(candidate.pages), 1)
    reference_boxes = [_stacked_bbox(reference, block, page_denominator) for block in reference.blocks]
    candidate_boxes = [_stacked_bbox(candidate, block, page_denominator) for block in candidate.blocks]
    geometry_cost = np.zeros((len(reference.blocks), len(candidate.blocks)), dtype=np.float64)
    content_cost = np.zeros_like(geometry_cost)
    combined_cost = np.zeros_like(geometry_cost)
    for row, reference_block in enumerate(reference.blocks):
        for column, candidate_block in enumerate(candidate.blocks):
            giou = _generalized_iou(reference_boxes[row], candidate_boxes[column])
            geometry_similarity = min(1.0, max(0.0, (giou + 1.0) / 2.0))
            text_similarity = v1._normalized_edit_similarity(
                reference_block.normalized, candidate_block.normalized
            )
            geometry_cost[row, column] = 1.0 - geometry_similarity
            content_cost[row, column] = 1.0 - text_similarity
            combined_cost[row, column] = 0.65 * geometry_cost[row, column] + 0.35 * content_cost[row, column]

    reference_mass = np.asarray(
        [max(1, len(block.normalized)) for block in reference.blocks], dtype=np.float64
    )
    candidate_mass = np.asarray(
        [max(1, len(block.normalized)) for block in candidate.blocks], dtype=np.float64
    )
    reference_mass /= reference_mass.sum()
    candidate_mass /= candidate_mass.sum()
    plan = _transport_plan(combined_cost, reference_mass, candidate_mass)
    total_cost = float(np.sum(plan * combined_cost))
    transported_geometry_cost = float(np.sum(plan * geometry_cost))
    transported_content_cost = float(np.sum(plan * content_cost))

    flows = []
    for row, column in zip(*np.nonzero(plan)):
        mass = float(plan[row, column])
        flows.append(
            {
                "reference_block_index": reference.blocks[int(row)].index,
                "candidate_block_index": candidate.blocks[int(column)].index,
                "mass": mass,
                "combined_cost": float(combined_cost[row, column]),
                "geometry_cost": float(geometry_cost[row, column]),
                "content_cost": float(content_cost[row, column]),
                "reference_page": reference.blocks[int(row)].page,
                "candidate_page": candidate.blocks[int(column)].page,
                "reference_bbox_stacked_normalized": list(reference_boxes[int(row)]),
                "candidate_bbox_stacked_normalized": list(candidate_boxes[int(column)]),
                "reference_text": reference.blocks[int(row)].text[:180],
                "candidate_text": candidate.blocks[int(column)].text[:180],
            }
        )
    flows.sort(key=lambda item: (-(item["mass"] * item["combined_cost"]), item["reference_block_index"], item["candidate_block_index"]))
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "reference_block_count": len(reference.blocks),
            "candidate_block_count": len(candidate.blocks),
            "transported_mass": float(plan.sum()),
            "combined_transport_cost": total_cost,
            "combined_transport_similarity_exp": math.exp(-total_cost),
            "transported_geometry_cost": transported_geometry_cost,
            "geometry_transport_similarity_exp": math.exp(-transported_geometry_cost),
            "transported_content_cost": transported_content_cost,
            "content_transport_similarity_exp": math.exp(-transported_content_cost),
            "nonzero_flow_count": int(np.count_nonzero(plan)),
        },
        "evidence": {
            "largest_cost_contributions": flows[:MAX_EVIDENCE_ITEMS],
            "mass_policy": "block normalized-character count; minimum mass unit 1",
            "cost_policy": "0.65 * (1 - rescaled GIoU) + 0.35 * normalized Levenshtein distance",
            "page_geometry": "page boxes stacked vertically and normalized by max page count",
        },
        "interpretation": (
            "Exact optimal transport over extracted text blocks. This is an LTSim-inspired, "
            "fully specified adaptation—not the published LTSim implementation or a semantic "
            "table/formula metric. Report geometry and content costs separately with the flows."
        ),
    }


def _ssim(gray_left: np.ndarray, gray_right: np.ndarray) -> float:
    minimum = min(gray_left.shape)
    if minimum < 3:
        return float(np.array_equal(gray_left, gray_right))
    win_size = min(11, minimum if minimum % 2 else minimum - 1)
    return float(
        structural_similarity(
            gray_left,
            gray_right,
            data_range=255,
            win_size=win_size,
            gaussian_weights=True,
            sigma=1.5,
            use_sample_covariance=False,
        )
    )


def _multiscale_ssim_diagnostic(left: np.ndarray, right: np.ndarray) -> tuple[float, list[dict[str, Any]]]:
    values = []
    scale = 1
    current_left = left
    current_right = right
    while scale <= 8 and min(current_left.shape) >= 16:
        score = _ssim(current_left, current_right)
        values.append({"downsample_factor": scale, "ssim": score})
        if scale == 8:
            break
        current_left = cv2.resize(current_left, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        current_right = cv2.resize(current_right, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        scale *= 2
    if not values:
        return _ssim(left, right), [{"downsample_factor": 1, "ssim": _ssim(left, right)}]
    # A geometric mean prevents a strong coarse scale from compensating for a
    # destroyed fine scale. This is not the canonical MS-SSIM decomposition.
    clipped = [max(1e-12, min(1.0, (item["ssim"] + 1.0) / 2.0)) for item in values]
    diagnostic = math.exp(sum(math.log(value) for value in clipped) / len(clipped))
    return diagnostic, values


def _perceptual_raster_axis(reference_path: str, candidate_path: str, *, dpi: int, tolerance_px: int) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    with fitz.open(reference_path) as left_document, fitz.open(candidate_path) as right_document:
        paired = min(len(left_document), len(right_document))
        for page_index in range(paired):
            left_rect = left_document[page_index].rect
            right_rect = right_document[page_index].rect
            if abs(left_rect.width - right_rect.width) > 1e-6 or abs(left_rect.height - right_rect.height) > 1e-6:
                pages.append(
                    {
                        "page": page_index,
                        "status": "abstain_canvas_mismatch",
                        "reference_size_points": [left_rect.width, left_rect.height],
                        "candidate_size_points": [right_rect.width, right_rect.height],
                        "reason": "Ordinary same-grid SSIM is invalid when physical page canvases differ.",
                    }
                )
                continue
            left = v1._render_page(left_document, page_index, dpi)
            right_original = v1._render_page(right_document, page_index, dpi)
            if right_original.shape != left.shape:
                pages.append(
                    {
                        "page": page_index,
                        "status": "abstain_raster_grid_mismatch",
                        "reference_raster_size": [left.shape[1], left.shape[0]],
                        "candidate_raster_size": [right_original.shape[1], right_original.shape[0]],
                        "reason": "Fixed-DPI raster grids differ despite nominally equal page points.",
                    }
                )
                continue
            right = right_original
            registered, shift, _, _ = v1._registered_candidate(left, right, tolerance_px)
            unregistered_multiscale, unregistered_scales = _multiscale_ssim_diagnostic(left, right)
            registered_multiscale, registered_scales = _multiscale_ssim_diagnostic(left, registered)
            _, unmatched = v1._tolerant_ink_metrics(left, registered, tolerance_px)
            pages.append(
                {
                    "page": page_index,
                    "status": "scored",
                    "unregistered_ssim": _ssim(left, right),
                    "registered_ssim": _ssim(left, registered),
                    "unregistered_multiscale_ssim_diagnostic": unregistered_multiscale,
                    "registered_multiscale_ssim_diagnostic": registered_multiscale,
                    "unregistered_scale_scores": unregistered_scales,
                    "registered_scale_scores": registered_scales,
                    "registration_translation_px": list(shift),
                    "candidate_resized_to_reference_canvas": False,
                    "reference_raster_size": [left.shape[1], left.shape[0]],
                    "candidate_raster_size_before_resize": [right_original.shape[1], right_original.shape[0]],
                    "registered_difference_bbox": v1._difference_bbox(unmatched),
                }
            )
        unpaired = abs(len(left_document) - len(right_document))

    scored_pages = [page for page in pages if page.get("status") == "scored"]

    def macro(name: str) -> float | None:
        values = [float(page[name]) for page in scored_pages]
        return sum(values) / len(values) if values else None

    return {
        "status": "scored" if scored_pages else "abstain",
        "applicable": True if scored_pages else None,
        "metrics": {
            "paired_page_count": len(pages),
            "scored_page_count": len(scored_pages),
            "abstained_page_count": len(pages) - len(scored_pages),
            "unpaired_page_count": unpaired,
            "unregistered_ssim_macro": macro("unregistered_ssim"),
            "registered_ssim_macro": macro("registered_ssim"),
            "unregistered_multiscale_ssim_diagnostic_macro": macro("unregistered_multiscale_ssim_diagnostic"),
            "registered_multiscale_ssim_diagnostic_macro": macro("registered_multiscale_ssim_diagnostic"),
        },
        "evidence": {"pages": pages},
        "interpretation": (
            "SSIM is reported before and after translation-only registration. The multiscale value "
            "is the documented geometric mean of four SSIM scales, not canonical MS-SSIM. "
            "No candidate resizing is performed; SSIM abstains when physical canvases/grids differ."
        ),
    }


def evaluate_pdf_pair(
    reference_pdf: str | Path,
    candidate_pdf: str | Path,
    *,
    applicability: Mapping[str, Any] | None = None,
    render_dpi: int = v1.DEFAULT_RENDER_DPI,
    ink_tolerance_px: int = v1.INK_TOLERANCE_PX,
) -> dict[str, Any]:
    if render_dpi <= 0:
        raise ValueError("render_dpi must be positive")
    if ink_tolerance_px < 0:
        raise ValueError("ink_tolerance_px must be non-negative")
    reference = v1.extract_pdf(reference_pdf)
    candidate = v1.extract_pdf(candidate_pdf)
    word_pairs = v1._match_words(reference, candidate)
    block_pairs = v1._match_blocks(reference, candidate)
    applicability = applicability or {}

    axes = {
        "canvas": v1._canvas_axis(reference, candidate),
        "content": _content_axis_v2(reference, candidate, word_pairs, block_pairs),
        "critical_content": _critical_content_axis(reference, candidate),
        "text_grounding": v1._text_grounding_axis(reference, candidate, word_pairs),
        "geometry": v1._geometry_axis(reference, candidate, word_pairs),
        "text_ltsim": _text_ltsim_axis(reference, candidate),
        "block_transport": _block_transport_axis(reference, candidate),
        "layout_relations": v1._layout_relations_axis(reference, candidate, block_pairs),
        "reading_order": v1._reading_order_axis(reference, candidate, block_pairs),
        "pagination": v1._pagination_axis(reference, candidate, block_pairs),
        "typography": v1._typography_axis(reference, candidate, word_pairs),
        "raster_ink": v1._raster_axis(reference.path, candidate.path, dpi=render_dpi, tolerance_px=ink_tolerance_px),
        "raster_perceptual": _perceptual_raster_axis(reference.path, candidate.path, dpi=render_dpi, tolerance_px=ink_tolerance_px),
        "tables": v1._specialized_axis("tables", applicability.get("tables")),
        "formulas": v1._specialized_axis("formulas", applicability.get("formulas")),
        "figures": v1._specialized_axis("figures", applicability.get("figures")),
    }
    return {
        "evaluator": {
            "name": EVALUATOR_VERSION,
            "version": 2,
            "aggregate_score": None,
            "policy": "No compensatory scalar. Report raw axes, coverage, abstentions, and localized evidence.",
        },
        "inputs": {
            "reference_pdf": serialize_path(reference.path),
            "candidate_pdf": serialize_path(candidate.path),
            "reference_page_count": len(reference.pages),
            "candidate_page_count": len(candidate.pages),
        },
        "configuration": {
            "render_dpi": render_dpi,
            "ink_threshold": v1.INK_THRESHOLD,
            "ink_tolerance_px": ink_tolerance_px,
            "normalization": "Unicode NFKC, soft-hyphen removal, collapsed whitespace; case preserved",
        },
        "applicability": {key: applicability.get(key) for key in ("tables", "formulas", "figures")},
        "axes": axes,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference_pdf", type=Path)
    parser.add_argument("candidate_pdf", type=Path)
    parser.add_argument("--applicability-json")
    parser.add_argument("--render-dpi", type=int, default=v1.DEFAULT_RENDER_DPI)
    parser.add_argument("--ink-tolerance-px", type=int, default=v1.INK_TOLERANCE_PX)
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    applicability = json.loads(args.applicability_json) if args.applicability_json else None
    result = evaluate_pdf_pair(
        args.reference_pdf,
        args.candidate_pdf,
        applicability=applicability,
        render_dpi=args.render_dpi,
        ink_tolerance_px=args.ink_tolerance_px,
    )
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
