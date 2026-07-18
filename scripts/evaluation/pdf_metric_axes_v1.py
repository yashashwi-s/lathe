#!/usr/bin/env python3
"""Explainable, axis-wise comparison of a reference PDF and a candidate PDF.

This evaluator deliberately does not produce a universal scalar.  Each axis
reports its own raw measurements, applicability state, and localized evidence.
Raster registration is a diagnostic for rendering noise; unregistered geometry
is retained as the layout evidence.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

import cv2
import fitz
import numpy as np
from rapidfuzz.distance import Levenshtein
from scipy.optimize import linear_sum_assignment


EVALUATOR_VERSION = "pdf_metric_axes_v1"
DEFAULT_RENDER_DPI = 120
INK_THRESHOLD = 245
INK_TOLERANCE_PX = 2
MAX_EVIDENCE_ITEMS = 24

BBox = tuple[float, float, float, float]


@dataclass(frozen=True)
class PdfPage:
    index: int
    width: float
    height: float
    text: str


@dataclass(frozen=True)
class PdfChar:
    index: int
    page: int
    bbox: BBox
    text: str
    normalized: str
    font: str
    size: float
    flags: int
    color: int


@dataclass(frozen=True)
class PdfWord:
    index: int
    page: int
    bbox: BBox
    text: str
    normalized: str
    block_index: int
    line_index: int
    word_index: int
    font: str
    size: float
    flags: int
    color: int


@dataclass(frozen=True)
class PdfBlock:
    index: int
    page: int
    bbox: BBox
    text: str
    normalized: str
    word_indices: tuple[int, ...]


@dataclass(frozen=True)
class PdfExtraction:
    path: str
    pages: tuple[PdfPage, ...]
    chars: tuple[PdfChar, ...]
    words: tuple[PdfWord, ...]
    blocks: tuple[PdfBlock, ...]


@dataclass(frozen=True)
class _SpanStyle:
    bbox: BBox
    font: str
    size: float
    flags: int
    color: int


def normalize_text(text: str) -> str:
    """Normalize Unicode and whitespace without deleting meaningful symbols."""

    value = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    return re.sub(r"\s+", " ", value).strip()


def _bbox_union(boxes: Sequence[BBox]) -> BBox:
    return (
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    )


def _intersection_area(left: BBox, right: BBox) -> float:
    width = max(0.0, min(left[2], right[2]) - max(left[0], right[0]))
    height = max(0.0, min(left[3], right[3]) - max(left[1], right[1]))
    return width * height


def _style_for_word(bbox: BBox, spans: Sequence[_SpanStyle]) -> _SpanStyle:
    if not spans:
        return _SpanStyle(bbox=bbox, font="", size=0.0, flags=0, color=0)
    return max(
        spans,
        key=lambda span: (
            _intersection_area(bbox, span.bbox),
            -abs(span.bbox[1] - bbox[1]),
            span.font,
        ),
    )


def _clean_font_name(font: str) -> str:
    name = font.split("+", 1)[-1] if "+" in font else font
    return normalize_text(name).casefold()


def extract_pdf(path: str | Path) -> PdfExtraction:
    """Extract and cache pages, characters, words, blocks, and style metadata."""

    resolved = Path(path).expanduser().resolve()
    stat = resolved.stat()
    return _extract_pdf_cached(str(resolved), stat.st_size, stat.st_mtime_ns)


@lru_cache(maxsize=128)
def _extract_pdf_cached(path: str, _size: int, _mtime_ns: int) -> PdfExtraction:
    pages: list[PdfPage] = []
    chars: list[PdfChar] = []
    words: list[PdfWord] = []
    blocks: list[PdfBlock] = []

    with fitz.open(path) as document:
        for page_index, page in enumerate(document):
            raw = page.get_text("rawdict", sort=True)
            page_spans: list[_SpanStyle] = []
            for raw_block in raw.get("blocks", []):
                if raw_block.get("type", 0) != 0:
                    continue
                for line in raw_block.get("lines", []):
                    for span in line.get("spans", []):
                        span_bbox = tuple(float(value) for value in span["bbox"])
                        style = _SpanStyle(
                            bbox=span_bbox,
                            font=str(span.get("font", "")),
                            size=float(span.get("size", 0.0)),
                            flags=int(span.get("flags", 0)),
                            color=int(span.get("color", 0)),
                        )
                        page_spans.append(style)
                        for raw_char in span.get("chars", []):
                            text = str(raw_char.get("c", ""))
                            chars.append(
                                PdfChar(
                                    index=len(chars),
                                    page=page_index,
                                    bbox=tuple(float(value) for value in raw_char["bbox"]),
                                    text=text,
                                    normalized=normalize_text(text),
                                    font=style.font,
                                    size=style.size,
                                    flags=style.flags,
                                    color=style.color,
                                )
                            )

            raw_words = page.get_text("words", sort=True)
            block_rows: dict[int, list[tuple[Any, ...]]] = defaultdict(list)
            for row in raw_words:
                block_rows[int(row[5])].append(tuple(row))

            ordered_block_numbers = sorted(
                block_rows,
                key=lambda number: (
                    min(row[1] for row in block_rows[number]),
                    min(row[0] for row in block_rows[number]),
                    number,
                ),
            )
            page_word_text: list[str] = []
            for native_block_number in ordered_block_numbers:
                block_index = len(blocks)
                block_word_indices: list[int] = []
                block_boxes: list[BBox] = []
                block_text: list[str] = []
                for row in sorted(
                    block_rows[native_block_number],
                    key=lambda value: (int(value[6]), int(value[7]), value[1], value[0]),
                ):
                    bbox = tuple(float(value) for value in row[:4])
                    text = str(row[4])
                    style = _style_for_word(bbox, page_spans)
                    global_word_index = len(words)
                    words.append(
                        PdfWord(
                            index=global_word_index,
                            page=page_index,
                            bbox=bbox,
                            text=text,
                            normalized=normalize_text(text),
                            block_index=block_index,
                            line_index=int(row[6]),
                            word_index=int(row[7]),
                            font=style.font,
                            size=style.size,
                            flags=style.flags,
                            color=style.color,
                        )
                    )
                    block_word_indices.append(global_word_index)
                    block_boxes.append(bbox)
                    block_text.append(text)
                    page_word_text.append(text)
                if block_boxes:
                    joined = " ".join(block_text)
                    blocks.append(
                        PdfBlock(
                            index=block_index,
                            page=page_index,
                            bbox=_bbox_union(block_boxes),
                            text=joined,
                            normalized=normalize_text(joined),
                            word_indices=tuple(block_word_indices),
                        )
                    )

            pages.append(
                PdfPage(
                    index=page_index,
                    width=float(page.rect.width),
                    height=float(page.rect.height),
                    text=" ".join(page_word_text),
                )
            )

    return PdfExtraction(
        path=path,
        pages=tuple(pages),
        chars=tuple(chars),
        words=tuple(words),
        blocks=tuple(blocks),
    )


def clear_extraction_cache() -> None:
    _extract_pdf_cached.cache_clear()


def extraction_cache_info() -> Any:
    return _extract_pdf_cached.cache_info()


def _page_for(extraction: PdfExtraction, page: int) -> PdfPage:
    return extraction.pages[page]


def _normalized_bbox(bbox: BBox, page: PdfPage) -> BBox:
    width = max(page.width, 1e-9)
    height = max(page.height, 1e-9)
    return (bbox[0] / width, bbox[1] / height, bbox[2] / width, bbox[3] / height)


def _bbox_center(bbox: BBox) -> tuple[float, float]:
    return ((bbox[0] + bbox[2]) / 2.0, (bbox[1] + bbox[3]) / 2.0)


def _bbox_iou(left: BBox, right: BBox) -> float:
    intersection = _intersection_area(left, right)
    left_area = max(0.0, left[2] - left[0]) * max(0.0, left[3] - left[1])
    right_area = max(0.0, right[2] - right[0]) * max(0.0, right[3] - right[1])
    union = left_area + right_area - intersection
    return intersection / union if union else 1.0


def _center_distance(left: BBox, right: BBox) -> float:
    left_center = _bbox_center(left)
    right_center = _bbox_center(right)
    return math.hypot(left_center[0] - right_center[0], left_center[1] - right_center[1])


def _safe_log_ratio(left: float, right: float) -> float:
    if left <= 0.0 or right <= 0.0:
        return 0.0 if left == right else float("inf")
    return abs(math.log(right / left))


def _quantile(values: Sequence[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.quantile(np.asarray(values, dtype=np.float64), q))


def _normalized_edit_similarity(reference: str, candidate: str) -> float:
    denominator = max(len(reference), len(candidate))
    if denominator == 0:
        return 1.0
    return 1.0 - (Levenshtein.distance(reference, candidate) / denominator)


def _inventory_metrics(reference: Sequence[str], candidate: Sequence[str]) -> dict[str, float | int]:
    reference_counter = Counter(token for token in reference if token)
    candidate_counter = Counter(token for token in candidate if token)
    overlap = sum((reference_counter & candidate_counter).values())
    reference_count = sum(reference_counter.values())
    candidate_count = sum(candidate_counter.values())
    precision = overlap / candidate_count if candidate_count else float(reference_count == 0)
    recall = overlap / reference_count if reference_count else float(candidate_count == 0)
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "reference_count": reference_count,
        "candidate_count": candidate_count,
        "matched_count": overlap,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def _match_words(
    reference: PdfExtraction,
    candidate: PdfExtraction,
) -> list[tuple[PdfWord, PdfWord]]:
    reference_groups: dict[str, list[PdfWord]] = defaultdict(list)
    candidate_groups: dict[str, list[PdfWord]] = defaultdict(list)
    for word in reference.words:
        if word.normalized:
            reference_groups[word.normalized].append(word)
    for word in candidate.words:
        if word.normalized:
            candidate_groups[word.normalized].append(word)

    pairs: list[tuple[PdfWord, PdfWord]] = []
    page_denominator = max(len(reference.pages), len(candidate.pages), 2) - 1
    for token in sorted(reference_groups.keys() & candidate_groups.keys()):
        reference_words = reference_groups[token]
        candidate_words = candidate_groups[token]
        costs = np.zeros((len(reference_words), len(candidate_words)), dtype=np.float64)
        reference_rank_denominator = max(len(reference_words) - 1, 1)
        candidate_rank_denominator = max(len(candidate_words) - 1, 1)
        for row_index, reference_word in enumerate(reference_words):
            reference_bbox = _normalized_bbox(
                reference_word.bbox, _page_for(reference, reference_word.page)
            )
            for column_index, candidate_word in enumerate(candidate_words):
                candidate_bbox = _normalized_bbox(
                    candidate_word.bbox, _page_for(candidate, candidate_word.page)
                )
                page_cost = abs(reference_word.page - candidate_word.page) / page_denominator
                occurrence_rank_cost = abs(
                    row_index / reference_rank_denominator
                    - column_index / candidate_rank_denominator
                )
                costs[row_index, column_index] = (
                    0.75 * page_cost
                    + _center_distance(reference_bbox, candidate_bbox)
                    + 0.75 * occurrence_rank_cost
                    + 1e-9 * (row_index * len(candidate_words) + column_index)
                )
        rows, columns = linear_sum_assignment(costs)
        pairs.extend(
            (reference_words[int(row)], candidate_words[int(column)])
            for row, column in zip(rows, columns)
        )
    return sorted(pairs, key=lambda pair: (pair[0].index, pair[1].index))


def _match_blocks(
    reference: PdfExtraction,
    candidate: PdfExtraction,
) -> list[tuple[PdfBlock, PdfBlock, float]]:
    if not reference.blocks or not candidate.blocks:
        return []
    costs = np.ones((len(reference.blocks), len(candidate.blocks)), dtype=np.float64)
    similarities = np.zeros_like(costs)
    page_denominator = max(len(reference.pages), len(candidate.pages), 2) - 1
    for row_index, reference_block in enumerate(reference.blocks):
        reference_bbox = _normalized_bbox(
            reference_block.bbox, _page_for(reference, reference_block.page)
        )
        for column_index, candidate_block in enumerate(candidate.blocks):
            candidate_bbox = _normalized_bbox(
                candidate_block.bbox, _page_for(candidate, candidate_block.page)
            )
            content_similarity = SequenceMatcher(
                None, reference_block.normalized, candidate_block.normalized, autojunk=False
            ).ratio()
            similarities[row_index, column_index] = content_similarity
            page_cost = abs(reference_block.page - candidate_block.page) / page_denominator
            costs[row_index, column_index] = (
                1.0
                - content_similarity
                + 0.05 * page_cost
                + 0.02 * _center_distance(reference_bbox, candidate_bbox)
                + 1e-9 * (row_index * len(candidate.blocks) + column_index)
            )
    rows, columns = linear_sum_assignment(costs)
    pairs = []
    for row, column in zip(rows, columns):
        similarity = float(similarities[row, column])
        if similarity >= 0.25:
            pairs.append((reference.blocks[int(row)], candidate.blocks[int(column)], similarity))
    return sorted(pairs, key=lambda pair: (pair[0].index, pair[1].index))


def _word_evidence(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    pair: tuple[PdfWord, PdfWord],
) -> dict[str, Any]:
    reference_word, candidate_word = pair
    reference_bbox = _normalized_bbox(
        reference_word.bbox, _page_for(reference, reference_word.page)
    )
    candidate_bbox = _normalized_bbox(
        candidate_word.bbox, _page_for(candidate, candidate_word.page)
    )
    reference_width = reference_bbox[2] - reference_bbox[0]
    candidate_width = candidate_bbox[2] - candidate_bbox[0]
    reference_height = reference_bbox[3] - reference_bbox[1]
    candidate_height = candidate_bbox[3] - candidate_bbox[1]
    return {
        "token": reference_word.normalized,
        "reference_word_index": reference_word.index,
        "candidate_word_index": candidate_word.index,
        "reference_page": reference_word.page,
        "candidate_page": candidate_word.page,
        "reference_bbox": list(reference_word.bbox),
        "candidate_bbox": list(candidate_word.bbox),
        "reference_bbox_normalized": list(reference_bbox),
        "candidate_bbox_normalized": list(candidate_bbox),
        "center_displacement": _center_distance(reference_bbox, candidate_bbox),
        "bbox_iou": _bbox_iou(reference_bbox, candidate_bbox),
        "width_abs_log_ratio": _safe_log_ratio(reference_width, candidate_width),
        "height_abs_log_ratio": _safe_log_ratio(reference_height, candidate_height),
    }


def _canvas_axis(reference: PdfExtraction, candidate: PdfExtraction) -> dict[str, Any]:
    page_pairs = []
    for page_index in range(min(len(reference.pages), len(candidate.pages))):
        reference_page = reference.pages[page_index]
        candidate_page = candidate.pages[page_index]
        width_abs_log_ratio = _safe_log_ratio(reference_page.width, candidate_page.width)
        height_abs_log_ratio = _safe_log_ratio(reference_page.height, candidate_page.height)
        page_pairs.append(
            {
                "page": page_index,
                "reference_size_points": [reference_page.width, reference_page.height],
                "candidate_size_points": [candidate_page.width, candidate_page.height],
                "width_abs_log_ratio": width_abs_log_ratio,
                "height_abs_log_ratio": height_abs_log_ratio,
                "exact_size_match": width_abs_log_ratio < 1e-9 and height_abs_log_ratio < 1e-9,
            }
        )
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "reference_page_count": len(reference.pages),
            "candidate_page_count": len(candidate.pages),
            "page_count_delta": len(candidate.pages) - len(reference.pages),
            "paired_page_count": len(page_pairs),
            "exact_paired_size_rate": (
                sum(item["exact_size_match"] for item in page_pairs) / len(page_pairs)
                if page_pairs
                else None
            ),
            "width_abs_log_ratio_max": max(
                (item["width_abs_log_ratio"] for item in page_pairs), default=None
            ),
            "height_abs_log_ratio_max": max(
                (item["height_abs_log_ratio"] for item in page_pairs), default=None
            ),
        },
        "evidence": {"page_pairs": page_pairs},
        "interpretation": "Canvas/page-size mismatch only; no token layout residual is folded into this axis.",
    }


def _content_axis(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    word_pairs: Sequence[tuple[PdfWord, PdfWord]],
    block_pairs: Sequence[tuple[PdfBlock, PdfBlock, float]],
) -> dict[str, Any]:
    reference_tokens = [word.normalized for word in reference.words if word.normalized]
    candidate_tokens = [word.normalized for word in candidate.words if word.normalized]
    inventory = _inventory_metrics(reference_tokens, candidate_tokens)
    reference_text = normalize_text("\n\f\n".join(page.text for page in reference.pages))
    candidate_text = normalize_text("\n\f\n".join(page.text for page in candidate.pages))

    matched_reference = {pair[0].index for pair in word_pairs}
    matched_candidate = {pair[1].index for pair in word_pairs}
    unmatched_reference = [
        {
            "word_index": word.index,
            "page": word.page,
            "bbox": list(word.bbox),
            "text": word.text,
            "normalized": word.normalized,
        }
        for word in reference.words
        if word.normalized and word.index not in matched_reference
    ][:MAX_EVIDENCE_ITEMS]
    unmatched_candidate = [
        {
            "word_index": word.index,
            "page": word.page,
            "bbox": list(word.bbox),
            "text": word.text,
            "normalized": word.normalized,
        }
        for word in candidate.words
        if word.normalized and word.index not in matched_candidate
    ][:MAX_EVIDENCE_ITEMS]

    block_edit_values = [
        _normalized_edit_similarity(reference_block.normalized, candidate_block.normalized)
        for reference_block, candidate_block, _ in block_pairs
    ]
    block_evidence = [
        {
            "reference_block_index": reference_block.index,
            "candidate_block_index": candidate_block.index,
            "reference_page": reference_block.page,
            "candidate_page": candidate_block.page,
            "reference_text": reference_block.text[:240],
            "candidate_text": candidate_block.text[:240],
            "normalized_edit_similarity": _normalized_edit_similarity(
                reference_block.normalized, candidate_block.normalized
            ),
        }
        for reference_block, candidate_block, _ in block_pairs
    ]
    block_evidence.sort(key=lambda item: item["normalized_edit_similarity"])

    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "token_inventory": inventory,
            "document_normalized_edit_similarity": _normalized_edit_similarity(
                reference_text, candidate_text
            ),
            "matched_block_normalized_edit_similarity_macro": (
                sum(block_edit_values) / len(block_edit_values) if block_edit_values else None
            ),
            "matched_block_count": len(block_pairs),
        },
        "evidence": {
            "unmatched_reference_words": unmatched_reference,
            "unmatched_candidate_words": unmatched_candidate,
            "lowest_similarity_block_pairs": block_evidence[:MAX_EVIDENCE_ITEMS],
        },
        "interpretation": "Token multiset retention and normalized Levenshtein similarity; ordering is reported separately.",
    }


def _geometry_axis(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    word_pairs: Sequence[tuple[PdfWord, PdfWord]],
) -> dict[str, Any]:
    if not word_pairs:
        return {
            "status": "abstain",
            "applicable": None,
            "metrics": {"matched_token_count": 0},
            "evidence": {},
            "reason": "No identical normalized tokens were available for geometry matching.",
        }

    evidence = [_word_evidence(reference, candidate, pair) for pair in word_pairs]
    center_displacements = [item["center_displacement"] for item in evidence]
    ious = [item["bbox_iou"] for item in evidence]
    width_errors = [item["width_abs_log_ratio"] for item in evidence]
    height_errors = [item["height_abs_log_ratio"] for item in evidence]
    worst = sorted(
        evidence,
        key=lambda item: (-item["center_displacement"], item["reference_word_index"]),
    )[:MAX_EVIDENCE_ITEMS]
    reference_count = sum(bool(word.normalized) for word in reference.words)
    candidate_count = sum(bool(word.normalized) for word in candidate.words)
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "matched_token_count": len(word_pairs),
            "reference_match_coverage": len(word_pairs) / reference_count if reference_count else 1.0,
            "candidate_match_coverage": len(word_pairs) / candidate_count if candidate_count else 1.0,
            "center_displacement_q50": _quantile(center_displacements, 0.50),
            "center_displacement_q90": _quantile(center_displacements, 0.90),
            "center_displacement_max": max(center_displacements),
            "bbox_iou_q10": _quantile(ious, 0.10),
            "bbox_iou_q50": _quantile(ious, 0.50),
            "width_abs_log_ratio_q90": _quantile(width_errors, 0.90),
            "height_abs_log_ratio_q90": _quantile(height_errors, 0.90),
        },
        "evidence": {"worst_token_pairs": worst},
        "interpretation": "Token boxes are normalized by each page's own canvas; canvas mismatch remains a separate axis.",
    }


def _text_grounding_axis(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    word_pairs: Sequence[tuple[PdfWord, PdfWord]],
) -> dict[str, Any]:
    """Report exact-word recognition/localization coverage without claiming CLEval."""

    reference_count = sum(bool(word.normalized) for word in reference.words)
    candidate_count = sum(bool(word.normalized) for word in candidate.words)
    matched_count = len(word_pairs)
    precision = matched_count / candidate_count if candidate_count else float(reference_count == 0)
    recall = matched_count / reference_count if reference_count else float(candidate_count == 0)
    hmean = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    if reference_count == 0 and candidate_count == 0:
        status = "abstain"
        reason = "Neither PDF exposed normalized words; word-grounding evidence is unavailable."
    else:
        status = "scored"
        reason = None
    result = {
        "status": status,
        "applicable": None if status == "abstain" else True,
        "metrics": {
            "reference_word_count": reference_count,
            "candidate_word_count": candidate_count,
            "exact_matched_word_count": matched_count,
            "word_precision": precision,
            "word_recall": recall,
            "word_hmean": hmean,
            "split_count": None,
            "merge_count": None,
        },
        "evidence": {
            "match_policy": (
                "exact Unicode-NFKC word text with deterministic page/position assignment for repeats"
            ),
        },
        "interpretation": (
            "Digital-PDF exact-word grounding adaptation; it is not the published CLEval algorithm. "
            "Split/merge values remain null until a validated implementation exists."
        ),
    }
    if reason:
        result["reason"] = reason
    return result


def _spatial_relation(first: BBox, second: BBox) -> str:
    first_center = _bbox_center(first)
    second_center = _bbox_center(second)
    dx = second_center[0] - first_center[0]
    dy = second_center[1] - first_center[1]
    if abs(dx) > abs(dy):
        return "right_of" if dx > 0 else "left_of"
    return "below" if dy > 0 else "above"


def _layout_relations_axis(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    block_pairs: Sequence[tuple[PdfBlock, PdfBlock, float]],
) -> dict[str, Any]:
    """Compare matched block geometry and pairwise relations as a transparent trial."""

    if not block_pairs:
        return {
            "status": "abstain",
            "applicable": None,
            "metrics": {"matched_block_count": 0, "pairwise_relation_count": 0},
            "evidence": {},
            "reason": "No content-matched text blocks were available for layout comparison.",
        }
    matched = []
    for reference_block, candidate_block, content_similarity in block_pairs:
        reference_bbox = _normalized_bbox(
            reference_block.bbox, _page_for(reference, reference_block.page)
        )
        candidate_bbox = _normalized_bbox(
            candidate_block.bbox, _page_for(candidate, candidate_block.page)
        )
        matched.append({
            "reference": reference_block,
            "candidate": candidate_block,
            "reference_bbox": reference_bbox,
            "candidate_bbox": candidate_bbox,
            "content_similarity": content_similarity,
            "bbox_iou": _bbox_iou(reference_bbox, candidate_bbox),
            "center_displacement": _center_distance(reference_bbox, candidate_bbox),
        })

    relation_count = 0
    relation_agreements = 0
    mismatches = []
    for left_index in range(len(matched)):
        for right_index in range(left_index + 1, len(matched)):
            left = matched[left_index]
            right = matched[right_index]
            reference_relation = _spatial_relation(left["reference_bbox"], right["reference_bbox"])
            candidate_relation = _spatial_relation(left["candidate_bbox"], right["candidate_bbox"])
            relation_count += 1
            relation_agreements += int(reference_relation == candidate_relation)
            if reference_relation != candidate_relation:
                mismatches.append({
                    "reference_block_pair": [
                        left["reference"].index, right["reference"].index,
                    ],
                    "candidate_block_pair": [
                        left["candidate"].index, right["candidate"].index,
                    ],
                    "reference_relation": reference_relation,
                    "candidate_relation": candidate_relation,
                    "reference_text": [
                        left["reference"].text[:120], right["reference"].text[:120],
                    ],
                })
    ious = [item["bbox_iou"] for item in matched]
    displacements = [item["center_displacement"] for item in matched]
    worst_blocks = sorted(
        matched, key=lambda item: (-item["center_displacement"], item["reference"].index)
    )[:MAX_EVIDENCE_ITEMS]
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "matched_block_count": len(matched),
            "reference_block_coverage": len(matched) / len(reference.blocks),
            "candidate_block_coverage": len(matched) / len(candidate.blocks),
            "matched_block_iou_q10": _quantile(ious, 0.10),
            "matched_block_iou_q50": _quantile(ious, 0.50),
            "matched_block_center_displacement_q90": _quantile(displacements, 0.90),
            "pairwise_relation_count": relation_count,
            "pairwise_relation_agreement": (
                relation_agreements / relation_count if relation_count else None
            ),
        },
        "evidence": {
            "relation_mismatches": mismatches[:MAX_EVIDENCE_ITEMS],
            "worst_block_pairs": [
                {
                    "reference_block_index": item["reference"].index,
                    "candidate_block_index": item["candidate"].index,
                    "reference_page": item["reference"].page,
                    "candidate_page": item["candidate"].page,
                    "reference_bbox_normalized": list(item["reference_bbox"]),
                    "candidate_bbox_normalized": list(item["candidate_bbox"]),
                    "center_displacement": item["center_displacement"],
                    "bbox_iou": item["bbox_iou"],
                    "reference_text": item["reference"].text[:160],
                }
                for item in worst_blocks
            ],
        },
        "interpretation": (
            "Transparent matched-block relation trial inspired by pairwise-layout work; "
            "this is not the published PaIRS or LTSim metric."
        ),
    }


def _reading_order_axis(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    block_pairs: Sequence[tuple[PdfBlock, PdfBlock, float]],
) -> dict[str, Any]:
    pair_by_reference = sorted(block_pairs, key=lambda pair: pair[0].index)
    pair_count = len(pair_by_reference)
    coverage = {
        "reference_block_coverage": pair_count / len(reference.blocks) if reference.blocks else 1.0,
        "candidate_block_coverage": pair_count / len(candidate.blocks) if candidate.blocks else 1.0,
    }
    if pair_count < 2:
        return {
            "status": "abstain",
            "applicable": None,
            "metrics": {"matched_block_count": pair_count, **coverage, "kendall_tau": None},
            "evidence": {},
            "reason": "At least two matched text blocks are required for reading-order comparison.",
        }

    candidate_sequence = [pair[1].index for pair in pair_by_reference]
    inversions = []
    for left_index in range(pair_count):
        for right_index in range(left_index + 1, pair_count):
            if candidate_sequence[left_index] > candidate_sequence[right_index]:
                left_pair = pair_by_reference[left_index]
                right_pair = pair_by_reference[right_index]
                inversions.append(
                    {
                        "reference_block_pair": [left_pair[0].index, right_pair[0].index],
                        "candidate_block_pair": [left_pair[1].index, right_pair[1].index],
                        "reference_text": [left_pair[0].text[:120], right_pair[0].text[:120]],
                        "candidate_text": [left_pair[1].text[:120], right_pair[1].text[:120]],
                    }
                )
    denominator = pair_count * (pair_count - 1)
    tau = 1.0 - (4.0 * len(inversions) / denominator)
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "matched_block_count": pair_count,
            **coverage,
            "inversion_count": len(inversions),
            "kendall_tau": tau,
        },
        "evidence": {"inverted_block_pairs": inversions[:MAX_EVIDENCE_ITEMS]},
        "interpretation": "Kendall tau is computed only on content-matched blocks; coverage must accompany it.",
    }


def _pagination_axis(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    block_pairs: Sequence[tuple[PdfBlock, PdfBlock, float]],
) -> dict[str, Any]:
    ordered_pairs = sorted(block_pairs, key=lambda pair: pair[0].index)
    page_assignment_accuracy = (
        sum(reference_block.page == candidate_block.page for reference_block, candidate_block, _ in ordered_pairs)
        / len(ordered_pairs)
        if ordered_pairs
        else None
    )
    boundaries = []
    true_positive = false_positive = false_negative = 0
    for left_pair, right_pair in zip(ordered_pairs, ordered_pairs[1:]):
        reference_break = left_pair[0].page != right_pair[0].page
        candidate_break = left_pair[1].page != right_pair[1].page
        true_positive += int(reference_break and candidate_break)
        false_positive += int(not reference_break and candidate_break)
        false_negative += int(reference_break and not candidate_break)
        if reference_break != candidate_break:
            boundaries.append(
                {
                    "reference_block_pair": [left_pair[0].index, right_pair[0].index],
                    "candidate_block_pair": [left_pair[1].index, right_pair[1].index],
                    "reference_page_break": reference_break,
                    "candidate_page_break": candidate_break,
                    "reference_pages": [left_pair[0].page, right_pair[0].page],
                    "candidate_pages": [left_pair[1].page, right_pair[1].page],
                }
            )
    reference_positive = true_positive + false_negative
    candidate_positive = true_positive + false_positive
    if reference_positive == 0 and candidate_positive == 0:
        precision = recall = f1 = 1.0
    else:
        precision = true_positive / candidate_positive if candidate_positive else 0.0
        recall = true_positive / reference_positive if reference_positive else 0.0
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "reference_page_count": len(reference.pages),
            "candidate_page_count": len(candidate.pages),
            "page_count_delta": len(candidate.pages) - len(reference.pages),
            "matched_block_count": len(ordered_pairs),
            "matched_block_page_assignment_accuracy": page_assignment_accuracy,
            "page_break_precision": precision,
            "page_break_recall": recall,
            "page_break_f1": f1,
            "page_break_true_positive": true_positive,
            "page_break_false_positive": false_positive,
            "page_break_false_negative": false_negative,
        },
        "evidence": {"mismatched_page_breaks": boundaries[:MAX_EVIDENCE_ITEMS]},
        "interpretation": "Page count, matched-block page assignment, and page-break boundaries are reported independently.",
    }


def _style_bits(flags: int) -> dict[str, bool]:
    return {
        "italic": bool(flags & 2),
        "serif": bool(flags & 4),
        "monospace": bool(flags & 8),
        "bold": bool(flags & 16),
    }


def _typography_axis(
    reference: PdfExtraction,
    candidate: PdfExtraction,
    word_pairs: Sequence[tuple[PdfWord, PdfWord]],
) -> dict[str, Any]:
    styled_pairs = [pair for pair in word_pairs if pair[0].size > 0.0 and pair[1].size > 0.0]
    if not styled_pairs:
        return {
            "status": "abstain",
            "applicable": None,
            "metrics": {"styled_matched_token_count": 0},
            "evidence": {},
            "reason": "No matched tokens with extractable font metadata were available.",
        }

    size_errors = [_safe_log_ratio(left.size, right.size) for left, right in styled_pairs]
    font_agreement = [
        _clean_font_name(left.font) == _clean_font_name(right.font) for left, right in styled_pairs
    ]
    color_agreement = [left.color == right.color for left, right in styled_pairs]
    bit_agreement: dict[str, list[bool]] = defaultdict(list)
    baseline_residuals = []
    mismatch_evidence = []
    for left, right in styled_pairs:
        left_bits = _style_bits(left.flags)
        right_bits = _style_bits(right.flags)
        for name in left_bits:
            bit_agreement[name].append(left_bits[name] == right_bits[name])
        left_bbox = _normalized_bbox(left.bbox, _page_for(reference, left.page))
        right_bbox = _normalized_bbox(right.bbox, _page_for(candidate, right.page))
        baseline_residual = abs(left_bbox[3] - right_bbox[3])
        baseline_residuals.append(baseline_residual)
        if (
            _clean_font_name(left.font) != _clean_font_name(right.font)
            or left_bits != right_bits
            or left.color != right.color
            or _safe_log_ratio(left.size, right.size) > 0.03
        ):
            mismatch_evidence.append(
                {
                    "token": left.normalized,
                    "reference_page": left.page,
                    "candidate_page": right.page,
                    "reference_bbox": list(left.bbox),
                    "candidate_bbox": list(right.bbox),
                    "reference_font": left.font,
                    "candidate_font": right.font,
                    "reference_size": left.size,
                    "candidate_size": right.size,
                    "font_size_abs_log_ratio": _safe_log_ratio(left.size, right.size),
                    "reference_style_bits": left_bits,
                    "candidate_style_bits": right_bits,
                    "reference_color": left.color,
                    "candidate_color": right.color,
                }
            )
    mismatch_evidence.sort(
        key=lambda item: (-item["font_size_abs_log_ratio"], item["token"])
    )
    reference_styled_count = sum(word.size > 0.0 for word in reference.words)
    candidate_styled_count = sum(word.size > 0.0 for word in candidate.words)
    reference_coverage = len(styled_pairs) / reference_styled_count if reference_styled_count else 0.0
    candidate_coverage = len(styled_pairs) / candidate_styled_count if candidate_styled_count else 0.0
    coverage_hmean = (
        2.0 * reference_coverage * candidate_coverage / (reference_coverage + candidate_coverage)
        if reference_coverage + candidate_coverage else 0.0
    )
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "styled_matched_token_count": len(styled_pairs),
            "reference_styled_token_count": reference_styled_count,
            "candidate_styled_token_count": candidate_styled_count,
            "reference_style_coverage": reference_coverage,
            "candidate_style_coverage": candidate_coverage,
            "style_coverage_hmean": coverage_hmean,
            "font_size_abs_log_ratio_q50": _quantile(size_errors, 0.50),
            "font_size_abs_log_ratio_q90": _quantile(size_errors, 0.90),
            "font_size_abs_log_ratio_max": max(size_errors),
            "font_name_exact_agreement_rate": sum(font_agreement) / len(font_agreement),
            "color_exact_agreement_rate": sum(color_agreement) / len(color_agreement),
            "bold_agreement_rate": sum(bit_agreement["bold"]) / len(styled_pairs),
            "italic_agreement_rate": sum(bit_agreement["italic"]) / len(styled_pairs),
            "serif_agreement_rate": sum(bit_agreement["serif"]) / len(styled_pairs),
            "monospace_agreement_rate": sum(bit_agreement["monospace"]) / len(styled_pairs),
            "baseline_displacement_q90": _quantile(baseline_residuals, 0.90),
        },
        "evidence": {"style_mismatches": mismatch_evidence[:MAX_EVIDENCE_ITEMS]},
        "interpretation": "Raw PDF font observables are diagnostic; font names and flags are renderer metadata, not perceptual truth.",
    }


def _render_page(document: fitz.Document, page_index: int, dpi: int) -> np.ndarray:
    scale = dpi / 72.0
    pixmap = document[page_index].get_pixmap(
        matrix=fitz.Matrix(scale, scale), colorspace=fitz.csGRAY, alpha=False
    )
    return np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(pixmap.height, pixmap.width)


def _ink_mask(gray: np.ndarray) -> np.ndarray:
    return gray < INK_THRESHOLD


def _dilate(mask: np.ndarray, tolerance_px: int) -> np.ndarray:
    if tolerance_px <= 0:
        return mask
    size = 2 * tolerance_px + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    return cv2.dilate(mask.astype(np.uint8), kernel).astype(bool)


def _tolerant_ink_metrics(
    reference_gray: np.ndarray,
    candidate_gray: np.ndarray,
    tolerance_px: int,
) -> tuple[dict[str, float | int], np.ndarray]:
    reference_ink = _ink_mask(reference_gray)
    candidate_ink = _ink_mask(candidate_gray)
    reference_count = int(reference_ink.sum())
    candidate_count = int(candidate_ink.sum())
    candidate_near = _dilate(candidate_ink, tolerance_px)
    reference_near = _dilate(reference_ink, tolerance_px)
    matched_reference = int((reference_ink & candidate_near).sum())
    matched_candidate = int((candidate_ink & reference_near).sum())
    recall = matched_reference / reference_count if reference_count else float(candidate_count == 0)
    precision = matched_candidate / candidate_count if candidate_count else float(reference_count == 0)
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    unmatched = (reference_ink & ~candidate_near) | (candidate_ink & ~reference_near)
    union_count = int((reference_ink | candidate_ink).sum())
    return (
        {
            "reference_ink_pixels": reference_count,
            "candidate_ink_pixels": candidate_count,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "unmatched_ink_pixels": int(unmatched.sum()),
            "unmatched_ink_fraction_of_union": int(unmatched.sum()) / union_count if union_count else 0.0,
        },
        unmatched,
    )


def _warp_translation(gray: np.ndarray, dx: int, dy: int) -> np.ndarray:
    matrix = np.asarray([[1.0, 0.0, float(dx)], [0.0, 1.0, float(dy)]], dtype=np.float32)
    return cv2.warpAffine(
        gray,
        matrix,
        (gray.shape[1], gray.shape[0]),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=255,
    )


def _registered_candidate(
    reference_gray: np.ndarray,
    candidate_gray: np.ndarray,
    tolerance_px: int,
) -> tuple[np.ndarray, tuple[int, int], float, float]:
    unregistered_metrics, _ = _tolerant_ink_metrics(
        reference_gray, candidate_gray, tolerance_px
    )
    best_gray = candidate_gray
    best_shift = (0, 0)
    best_f1 = float(unregistered_metrics["f1"])
    reference_signal = _ink_mask(reference_gray).astype(np.float32)
    candidate_signal = _ink_mask(candidate_gray).astype(np.float32)
    proposed: list[tuple[int, int]] = [(0, 0)]
    if reference_signal.any() and candidate_signal.any():
        (shift_x, shift_y), _ = cv2.phaseCorrelate(reference_signal, candidate_signal)
        rounded = (int(round(shift_x)), int(round(shift_y)))
        limit_x = max(4, int(reference_gray.shape[1] * 0.15))
        limit_y = max(4, int(reference_gray.shape[0] * 0.15))
        if abs(rounded[0]) <= limit_x and abs(rounded[1]) <= limit_y:
            proposed.extend([rounded, (-rounded[0], -rounded[1])])
    for dx, dy in dict.fromkeys(proposed):
        registered = _warp_translation(candidate_gray, dx, dy)
        metrics, _ = _tolerant_ink_metrics(reference_gray, registered, tolerance_px)
        f1 = float(metrics["f1"])
        if f1 > best_f1 + 1e-12:
            best_gray = registered
            best_shift = (dx, dy)
            best_f1 = f1
    return best_gray, best_shift, float(unregistered_metrics["f1"]), best_f1


def _difference_bbox(mask: np.ndarray) -> dict[str, Any] | None:
    rows, columns = np.nonzero(mask)
    if not len(rows):
        return None
    x0 = int(columns.min())
    y0 = int(rows.min())
    x1 = int(columns.max()) + 1
    y1 = int(rows.max()) + 1
    height, width = mask.shape
    return {
        "pixel_bbox": [x0, y0, x1, y1],
        "normalized_bbox": [x0 / width, y0 / height, x1 / width, y1 / height],
    }


def _raster_axis(
    reference_path: str,
    candidate_path: str,
    *,
    dpi: int,
    tolerance_px: int,
) -> dict[str, Any]:
    page_evidence = []
    with fitz.open(reference_path) as reference_document, fitz.open(candidate_path) as candidate_document:
        paired_page_count = min(len(reference_document), len(candidate_document))
        for page_index in range(paired_page_count):
            reference_gray = _render_page(reference_document, page_index, dpi)
            candidate_gray_original = _render_page(candidate_document, page_index, dpi)
            candidate_gray = cv2.resize(
                candidate_gray_original,
                (reference_gray.shape[1], reference_gray.shape[0]),
                interpolation=cv2.INTER_AREA,
            )
            unregistered_metrics, _ = _tolerant_ink_metrics(
                reference_gray, candidate_gray, tolerance_px
            )
            registered_gray, shift, _, _ = _registered_candidate(
                reference_gray, candidate_gray, tolerance_px
            )
            registered_metrics, unmatched = _tolerant_ink_metrics(
                reference_gray, registered_gray, tolerance_px
            )
            page_evidence.append(
                {
                    "page": page_index,
                    "reference_raster_size": [reference_gray.shape[1], reference_gray.shape[0]],
                    "candidate_raster_size_before_resize": [
                        candidate_gray_original.shape[1],
                        candidate_gray_original.shape[0],
                    ],
                    "candidate_resized_to_reference_canvas": True,
                    "coordinate_frame": "registered_reference_raster",
                    "registration_translation_px": [shift[0], shift[1]],
                    "unregistered": unregistered_metrics,
                    "registered": registered_metrics,
                    "registered_mean_absolute_gray_difference": float(
                        np.mean(
                            np.abs(
                                reference_gray.astype(np.int16)
                                - registered_gray.astype(np.int16)
                            )
                        )
                        / 255.0
                    ),
                    "top_difference_bbox": _difference_bbox(unmatched),
                }
            )

        for page_index in range(paired_page_count, len(reference_document)):
            gray = _render_page(reference_document, page_index, dpi)
            page_evidence.append(
                {
                    "page": page_index,
                    "unpaired_side": "reference",
                    "coordinate_frame": "reference",
                    "top_difference_bbox": {
                        "pixel_bbox": [0, 0, gray.shape[1], gray.shape[0]],
                        "normalized_bbox": [0.0, 0.0, 1.0, 1.0],
                    },
                }
            )
        for page_index in range(paired_page_count, len(candidate_document)):
            gray = _render_page(candidate_document, page_index, dpi)
            page_evidence.append(
                {
                    "page": page_index,
                    "unpaired_side": "candidate",
                    "coordinate_frame": "candidate",
                    "top_difference_bbox": {
                        "pixel_bbox": [0, 0, gray.shape[1], gray.shape[0]],
                        "normalized_bbox": [0.0, 0.0, 1.0, 1.0],
                    },
                }
            )

    paired = [item for item in page_evidence if "registered" in item]
    unpaired_count = len(page_evidence) - len(paired)
    unregistered_values = [float(item["unregistered"]["f1"]) for item in paired]
    registered_values = [float(item["registered"]["f1"]) for item in paired]
    if unpaired_count:
        unregistered_values.extend([0.0] * unpaired_count)
        registered_values.extend([0.0] * unpaired_count)
    top_difference = None
    candidates_with_difference = [
        item
        for item in page_evidence
        if item.get("top_difference_bbox") is not None
    ]
    if candidates_with_difference:
        top_item = max(
            candidates_with_difference,
            key=lambda item: (
                item.get("registered", {}).get("unmatched_ink_fraction_of_union", 1.0),
                -item["page"],
            ),
        )
        top_difference = {
            "page": top_item["page"],
            "unpaired_side": top_item.get("unpaired_side"),
            "coordinate_frame": (
                top_item.get("unpaired_side") or "registered_reference_raster"
            ),
            "registration_translation_px": top_item.get("registration_translation_px"),
            **top_item["top_difference_bbox"],
        }
    return {
        "status": "scored",
        "applicable": True,
        "metrics": {
            "paired_page_count": len(paired),
            "unpaired_page_count": unpaired_count,
            "unregistered_tolerant_ink_f1_macro": (
                sum(unregistered_values) / len(unregistered_values)
                if unregistered_values
                else 1.0
            ),
            "registered_tolerant_ink_f1_macro": (
                sum(registered_values) / len(registered_values) if registered_values else 1.0
            ),
            "registration_gain": (
                (sum(registered_values) - sum(unregistered_values)) / len(registered_values)
                if registered_values
                else 0.0
            ),
        },
        "evidence": {
            "pages": page_evidence,
            "top_difference_bbox": top_difference,
        },
        "interpretation": "Candidate pages are resized to the reference canvas, then optionally translation-registered. Use canvas and geometry axes for layout claims.",
    }


def _specialized_axis(name: str, source_flag: Any) -> dict[str, Any]:
    if isinstance(source_flag, Mapping):
        reference_flag = source_flag.get("reference")
        candidate_flag = source_flag.get("candidate")
    else:
        reference_flag = source_flag
        candidate_flag = source_flag
    supplied = source_flag is not None
    flags = {"reference": reference_flag, "candidate": candidate_flag}
    if supplied and reference_flag is False and candidate_flag is False:
        return {
            "status": "not_applicable",
            "applicable": False,
            "metrics": {},
            "evidence": {"source_flags": flags},
            "reason": f"Source flags state that {name} are absent from both PDFs.",
        }
    if reference_flag is True or candidate_flag is True:
        return {
            "status": "abstain",
            "applicable": True,
            "metrics": {},
            "evidence": {"source_flags": flags},
            "reason": f"{name.title()} are present, but this evaluator has no validated structure-aware {name} metric.",
        }
    return {
        "status": "abstain",
        "applicable": None,
        "metrics": {},
        "evidence": {"source_flags": flags},
        "reason": f"Applicability for {name} was not established by source metadata.",
    }


def evaluate_pdf_pair(
    reference_pdf: str | Path,
    candidate_pdf: str | Path,
    *,
    applicability: Mapping[str, Any] | None = None,
    render_dpi: int = DEFAULT_RENDER_DPI,
    ink_tolerance_px: int = INK_TOLERANCE_PX,
) -> dict[str, Any]:
    """Evaluate a PDF pair and return deterministic JSON-compatible axes."""

    if render_dpi <= 0:
        raise ValueError("render_dpi must be positive")
    if ink_tolerance_px < 0:
        raise ValueError("ink_tolerance_px must be non-negative")
    reference = extract_pdf(reference_pdf)
    candidate = extract_pdf(candidate_pdf)
    word_pairs = _match_words(reference, candidate)
    block_pairs = _match_blocks(reference, candidate)
    applicability = applicability or {}

    axes = {
        "canvas": _canvas_axis(reference, candidate),
        "content": _content_axis(reference, candidate, word_pairs, block_pairs),
        "text_grounding": _text_grounding_axis(reference, candidate, word_pairs),
        "geometry": _geometry_axis(reference, candidate, word_pairs),
        "layout_relations": _layout_relations_axis(reference, candidate, block_pairs),
        "reading_order": _reading_order_axis(reference, candidate, block_pairs),
        "pagination": _pagination_axis(reference, candidate, block_pairs),
        "typography": _typography_axis(reference, candidate, word_pairs),
        "raster_diagnostic": _raster_axis(
            reference.path,
            candidate.path,
            dpi=render_dpi,
            tolerance_px=ink_tolerance_px,
        ),
        "tables": _specialized_axis("tables", applicability.get("tables")),
        "formulas": _specialized_axis("formulas", applicability.get("formulas")),
        "figures": _specialized_axis("figures", applicability.get("figures")),
    }
    return {
        "evaluator": {
            "name": EVALUATOR_VERSION,
            "version": 1,
            "aggregate_score": None,
            "policy": "No universal scalar; inspect axis values, applicability, coverage, and evidence together.",
        },
        "inputs": {
            "reference_pdf": reference.path,
            "candidate_pdf": candidate.path,
            "reference_page_count": len(reference.pages),
            "candidate_page_count": len(candidate.pages),
        },
        "configuration": {
            "render_dpi": render_dpi,
            "ink_threshold": INK_THRESHOLD,
            "ink_tolerance_px": ink_tolerance_px,
            "normalization": "Unicode NFKC, soft-hyphen removal, collapsed whitespace; case preserved",
        },
        "applicability": {
            key: applicability.get(key) for key in ("tables", "formulas", "figures")
        },
        "axes": axes,
    }


def _parse_applicability(value: str | None) -> Mapping[str, Any] | None:
    if value is None:
        return None
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("--applicability-json must decode to an object")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report explainable PDF-pair metric axes without an aggregate score."
    )
    parser.add_argument("reference_pdf", type=Path)
    parser.add_argument("candidate_pdf", type=Path)
    parser.add_argument(
        "--applicability-json",
        help='Source flags, e.g. \'{"tables": false, "formulas": true}\'.',
    )
    parser.add_argument("--render-dpi", type=int, default=DEFAULT_RENDER_DPI)
    parser.add_argument("--ink-tolerance-px", type=int, default=INK_TOLERANCE_PX)
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = evaluate_pdf_pair(
        args.reference_pdf,
        args.candidate_pdf,
        applicability=_parse_applicability(args.applicability_json),
        render_dpi=args.render_dpi,
        ink_tolerance_px=args.ink_tolerance_px,
    )
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            indent=2 if args.pretty else None,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
