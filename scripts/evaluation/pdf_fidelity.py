"""Source-independent PDF fidelity metrics and visual diagnostics.

The comparator deliberately separates content fidelity from visual fidelity.
It uses PDF words rather than PDF text blocks so different producer chunking
does not create the false mismatches seen in the archived evaluator.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

import cv2
import fitz
import numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import linear_sum_assignment
from scipy.stats import kendalltau
from skimage.metrics import structural_similarity


RENDER_DPI = 144
RENDER_SCALE = RENDER_DPI / 72.0
INK_THRESHOLD = 245
EPSILON = 1e-6
METRIC_VERSION = "pdf_fidelity_v0.1"
METRIC_CONFIG = {
    "metric_version": METRIC_VERSION,
    "render_dpi": RENDER_DPI,
    "ink_threshold": INK_THRESHOLD,
    "foreground_tolerance_pixels": 2,
    "matched_box_thresholds_page_diagonal": {"green_max": 0.015, "yellow_max": 0.05},
    "content": {"token_multiset_f1": 0.75, "character_sequence_similarity": 0.25},
    "layout": {"word_geometry": 0.50, "local_flow": 0.25, "reading_order": 0.15, "page_geometry": 0.10},
    "typography": {
        "font_size": 0.35, "font_family": 0.20, "bold": 0.12, "italic": 0.10,
        "font_class": 0.10, "color": 0.13,
    },
    "raster": {"tolerant_ink_f1": 0.50, "edge_distance": 0.25, "foreground_ssim": 0.25},
    "pagination": {"page_count_ratio": 0.70, "matched_word_page_assignment": 0.30},
    "visual_geometric_mean": {"pagination": 0.10, "layout": 0.40, "typography": 0.20, "raster": 0.30},
    "overall_geometric_mean": {"content": 0.35, "visual": 0.65},
}


@dataclass
class PdfWord:
    index: int
    page: int
    bbox: tuple[float, float, float, float]
    text: str
    norm: str
    font: str = ""
    font_family: str = ""
    size: float = 0.0
    flags: int = 0
    color: int = 0

    @property
    def bold(self) -> bool:
        return bool(self.flags & 16) or "bold" in self.font.lower()

    @property
    def italic(self) -> bool:
        lower = self.font.lower()
        return bool(self.flags & 2) or "italic" in lower or "oblique" in lower

    @property
    def serif(self) -> bool:
        return bool(self.flags & 4)

    @property
    def mono(self) -> bool:
        return bool(self.flags & 8)


@dataclass
class PdfData:
    path: str
    page_sizes: list[tuple[float, float]]
    words: list[PdfWord]
    page_text: list[str]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def geometric_mean(parts: Iterable[tuple[float, float]]) -> float:
    return math.exp(sum(weight * math.log(max(EPSILON, value)) for value, weight in parts))


def normalize_token(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.replace("\u00ad", "")
    text = re.sub(r"^\W+|\W+$", "", text, flags=re.UNICODE)
    return text


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.replace("\u00ad", "")
    text = re.sub(r"-\s+", "", text)
    return re.sub(r"\s+", " ", text).strip()


def canonical_font_family(font: str) -> str:
    value = font.split("+")[-1].casefold()
    value = re.sub(r"(bold|italic|oblique|regular|roman|medium|book|semibold)", "", value)
    value = re.sub(r"[^a-z0-9]", "", value)
    aliases = (
        ("newcomputermodern", "computer-modern"),
        ("latinmodern", "computer-modern"),
        ("lmodern", "computer-modern"),
        ("cmr", "computer-modern"),
        ("cmb", "computer-modern"),
        ("cms", "computer-modern"),
        ("cmmi", "computer-modern-math"),
        ("cmsy", "computer-modern-math"),
        ("cmex", "computer-modern-math"),
        ("libertinus", "libertinus"),
        ("texgyretermes", "times"),
        ("times", "times"),
        ("courier", "courier"),
        ("helvetica", "helvetica"),
    )
    for marker, family in aliases:
        if marker in value:
            return family
    return value


def _intersection_area(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[2], b[2]), min(a[3], b[3])
    return max(0.0, x1 - x0) * max(0.0, y1 - y0)


def _span_for_word(bbox: tuple[float, float, float, float], spans: list[dict]) -> dict | None:
    cx = (bbox[0] + bbox[2]) / 2
    cy = (bbox[1] + bbox[3]) / 2
    containing = [s for s in spans if s["bbox"][0] <= cx <= s["bbox"][2] and s["bbox"][1] <= cy <= s["bbox"][3]]
    if containing:
        return min(containing, key=lambda s: (s["bbox"][2] - s["bbox"][0]) * (s["bbox"][3] - s["bbox"][1]))
    best = max(spans, key=lambda s: _intersection_area(bbox, s["bbox"]), default=None)
    if best and _intersection_area(bbox, best["bbox"]) > 0:
        return best
    return None


def extract_pdf(path: Path) -> PdfData:
    words: list[PdfWord] = []
    sizes: list[tuple[float, float]] = []
    page_text: list[str] = []
    with fitz.open(path) as document:
        for page_index, page in enumerate(document):
            sizes.append((float(page.rect.width), float(page.rect.height)))
            spans: list[dict] = []
            structure = page.get_text("dict", sort=True)
            for block in structure.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if span.get("text", "").strip():
                            spans.append(span)

            page_words = page.get_text("words", sort=True)
            page_text.append(" ".join(item[4] for item in page_words))
            for item in page_words:
                bbox = tuple(float(value) for value in item[:4])
                text = str(item[4])
                norm = normalize_token(text)
                span = _span_for_word(bbox, spans)
                font = str(span.get("font", "")) if span else ""
                words.append(PdfWord(
                    index=len(words),
                    page=page_index,
                    bbox=bbox,
                    text=text,
                    norm=norm,
                    font=font,
                    font_family=canonical_font_family(font),
                    size=float(span.get("size", 0.0)) if span else 0.0,
                    flags=int(span.get("flags", 0)) if span else 0,
                    color=int(span.get("color", 0)) if span else 0,
                ))
    return PdfData(str(path), sizes, words, page_text)


def _normalized_center(word: PdfWord, data: PdfData) -> tuple[float, float]:
    width, height = data.page_sizes[word.page]
    return ((word.bbox[0] + word.bbox[2]) / (2 * width),
            (word.bbox[1] + word.bbox[3]) / (2 * height))


def match_words(reference: PdfData, candidate: PdfData) -> tuple[list[tuple[int, int]], set[int], set[int]]:
    """Match identical normalized token occurrences with minimum geometric cost."""
    ref_groups: dict[str, list[int]] = defaultdict(list)
    cand_groups: dict[str, list[int]] = defaultdict(list)
    for word in reference.words:
        if word.norm:
            ref_groups[word.norm].append(word.index)
    for word in candidate.words:
        if word.norm:
            cand_groups[word.norm].append(word.index)

    pairs: list[tuple[int, int]] = []
    for token in sorted(ref_groups.keys() & cand_groups.keys()):
        ref_ids = ref_groups[token]
        cand_ids = cand_groups[token]
        costs = np.zeros((len(ref_ids), len(cand_ids)), dtype=np.float64)
        for rpos, ref_id in enumerate(ref_ids):
            rw = reference.words[ref_id]
            rx, ry = _normalized_center(rw, reference)
            for cpos, cand_id in enumerate(cand_ids):
                cw = candidate.words[cand_id]
                cx, cy = _normalized_center(cw, candidate)
                page_cost = abs(rw.page - cw.page) * 1.25
                costs[rpos, cpos] = page_cost + math.hypot(rx - cx, ry - cy)
        rsel, csel = linear_sum_assignment(costs)
        pairs.extend((ref_ids[r], cand_ids[c]) for r, c in zip(rsel, csel))

    pairs.sort()
    matched_ref = {pair[0] for pair in pairs}
    matched_cand = {pair[1] for pair in pairs}
    return pairs, set(range(len(reference.words))) - matched_ref, set(range(len(candidate.words))) - matched_cand


def _rgb(color: int) -> tuple[int, int, int]:
    return ((color >> 16) & 255, (color >> 8) & 255, color & 255)


def _color_score(a: int, b: int) -> float:
    av = np.array(_rgb(a), dtype=np.float64)
    bv = np.array(_rgb(b), dtype=np.float64)
    return clamp(1.0 - float(np.linalg.norm(av - bv)) / math.sqrt(3 * 255**2))


def _font_family_score(a: PdfWord, b: PdfWord) -> float:
    if a.font_family and a.font_family == b.font_family:
        return 1.0
    if a.serif == b.serif and a.mono == b.mono:
        return 0.65
    return 0.25


def _size_score(ref: PdfWord, cand: PdfWord) -> float:
    if ref.size <= 0 or cand.size <= 0:
        return 0.5
    return math.exp(-abs(math.log(cand.size / ref.size)) / 0.30)


def _page_geometry(reference: PdfData, candidate: PdfData) -> float:
    count = min(len(reference.page_sizes), len(candidate.page_sizes))
    if count == 0:
        return 0.0
    scores = []
    for index in range(count):
        rw, rh = reference.page_sizes[index]
        cw, ch = candidate.page_sizes[index]
        scores.append(math.exp(-1.5 * (abs(math.log(cw / rw)) + abs(math.log(ch / rh)))))
    return float(np.mean(scores))


def _word_geometry(reference: PdfData, candidate: PdfData,
                   pairs: list[tuple[int, int]]) -> tuple[float, list[dict], float]:
    records: list[dict] = []
    scores: list[float] = []
    same_page = 0
    for ref_id, cand_id in pairs:
        ref = reference.words[ref_id]
        cand = candidate.words[cand_id]
        rx, ry = _normalized_center(ref, reference)
        cx, cy = _normalized_center(cand, candidate)
        if ref.page == cand.page:
            same_page += 1
            distance = math.hypot(rx - cx, ry - cy) / math.sqrt(2)
            position_score = math.exp(-distance / 0.06)
            rw = max(EPSILON, (ref.bbox[2] - ref.bbox[0]) / reference.page_sizes[ref.page][0])
            rh = max(EPSILON, (ref.bbox[3] - ref.bbox[1]) / reference.page_sizes[ref.page][1])
            cw = max(EPSILON, (cand.bbox[2] - cand.bbox[0]) / candidate.page_sizes[cand.page][0])
            ch = max(EPSILON, (cand.bbox[3] - cand.bbox[1]) / candidate.page_sizes[cand.page][1])
            box_size_score = math.exp(-0.5 * abs(math.log(cw / rw)) - 0.8 * abs(math.log(ch / rh)))
            score = 0.75 * position_score + 0.25 * box_size_score
        else:
            distance = 1.0
            position_score = 0.0
            box_size_score = 0.0
            score = 0.0
        scores.append(score)
        records.append({
            "reference_index": ref_id,
            "candidate_index": cand_id,
            "token": ref.norm,
            "reference_page": ref.page + 1,
            "candidate_page": cand.page + 1,
            "reference_bbox": list(ref.bbox),
            "candidate_bbox": list(cand.bbox),
            "position_error": distance,
            "position_score": position_score,
            "box_size_score": box_size_score,
            "geometry_score": score,
        })
    return (float(np.mean(scores)) if scores else 0.0, records,
            same_page / len(pairs) if pairs else 0.0)


def _reading_order_score(pairs: list[tuple[int, int]]) -> float:
    if len(pairs) < 3:
        return 1.0 if pairs else 0.0
    ordered = sorted(pairs, key=lambda pair: pair[0])
    candidate_order = [pair[1] for pair in ordered]
    tau = kendalltau(range(len(candidate_order)), candidate_order).statistic
    if tau is None or math.isnan(tau):
        return 0.0
    return clamp((tau + 1.0) / 2.0)


def _flow_score(reference: PdfData, candidate: PdfData,
                pairs: list[tuple[int, int]]) -> float:
    if len(pairs) < 2:
        return 1.0 if pairs else 0.0
    ordered = sorted(pairs, key=lambda pair: pair[0])
    scores = []
    for first, second in zip(ordered, ordered[1:]):
        ra, ca = reference.words[first[0]], candidate.words[first[1]]
        rb, cb = reference.words[second[0]], candidate.words[second[1]]
        if ra.page != rb.page or ca.page != cb.page or ra.page != ca.page or rb.page != cb.page:
            scores.append(0.0)
            continue
        rax, ray = _normalized_center(ra, reference)
        rbx, rby = _normalized_center(rb, reference)
        cax, cay = _normalized_center(ca, candidate)
        cbx, cby = _normalized_center(cb, candidate)
        delta_error = math.hypot((rbx - rax) - (cbx - cax), (rby - ray) - (cby - cay))
        scores.append(math.exp(-delta_error / 0.05))
    return float(np.mean(scores)) if scores else 0.0


def _typography(reference: PdfData, candidate: PdfData,
                pairs: list[tuple[int, int]]) -> tuple[float, dict]:
    if not pairs:
        return 0.0, {}
    size_scores = []
    family_scores = []
    bold_scores = []
    italic_scores = []
    class_scores = []
    color_scores = []
    exact_family = []
    for ref_id, cand_id in pairs:
        ref, cand = reference.words[ref_id], candidate.words[cand_id]
        size_scores.append(_size_score(ref, cand))
        family_scores.append(_font_family_score(ref, cand))
        exact_family.append(float(bool(ref.font_family) and ref.font_family == cand.font_family))
        bold_scores.append(float(ref.bold == cand.bold))
        italic_scores.append(float(ref.italic == cand.italic))
        class_scores.append(float(ref.serif == cand.serif and ref.mono == cand.mono))
        color_scores.append(_color_score(ref.color, cand.color))
    details = {
        "font_size": float(np.mean(size_scores)),
        "font_family": float(np.mean(family_scores)),
        "font_family_exact_rate": float(np.mean(exact_family)),
        "bold": float(np.mean(bold_scores)),
        "italic": float(np.mean(italic_scores)),
        "font_class": float(np.mean(class_scores)),
        "color": float(np.mean(color_scores)),
    }
    score = (0.35 * details["font_size"] + 0.20 * details["font_family"] +
             0.12 * details["bold"] + 0.10 * details["italic"] +
             0.10 * details["font_class"] + 0.13 * details["color"])
    return score, details


def render_page(path: Path, page_index: int, dpi: int = RENDER_DPI) -> np.ndarray:
    with fitz.open(path) as document:
        page = document.load_page(page_index)
        pixmap = page.get_pixmap(dpi=dpi, colorspace=fitz.csRGB, alpha=False)
        return np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(pixmap.height, pixmap.width, 3).copy()


def _pad_pair(reference: np.ndarray, candidate: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    height = max(reference.shape[0], candidate.shape[0])
    width = max(reference.shape[1], candidate.shape[1])
    ref = np.full((height, width, 3), 255, dtype=np.uint8)
    cand = np.full((height, width, 3), 255, dtype=np.uint8)
    ref[:reference.shape[0], :reference.shape[1]] = reference
    cand[:candidate.shape[0], :candidate.shape[1]] = candidate
    return ref, cand


def raster_page_metrics(reference: np.ndarray, candidate: np.ndarray) -> tuple[dict, np.ndarray]:
    reference, candidate = _pad_pair(reference, candidate)
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_RGB2GRAY)
    cand_gray = cv2.cvtColor(candidate, cv2.COLOR_RGB2GRAY)
    ref_ink = ref_gray < INK_THRESHOLD
    cand_ink = cand_gray < INK_THRESHOLD
    kernel = np.ones((5, 5), dtype=np.uint8)
    ref_dilated = cv2.dilate(ref_ink.astype(np.uint8), kernel) > 0
    cand_dilated = cv2.dilate(cand_ink.astype(np.uint8), kernel) > 0
    recall = float((ref_ink & cand_dilated).sum() / max(1, ref_ink.sum()))
    precision = float((cand_ink & ref_dilated).sum() / max(1, cand_ink.sum()))
    ink_f1 = 2 * precision * recall / max(EPSILON, precision + recall)

    ref_edge = cv2.Canny(ref_gray, 80, 180) > 0
    cand_edge = cv2.Canny(cand_gray, 80, 180) > 0
    if ref_edge.any() and cand_edge.any():
        ref_distance = cv2.distanceTransform((~ref_edge).astype(np.uint8), cv2.DIST_L2, 3)
        cand_distance = cv2.distanceTransform((~cand_edge).astype(np.uint8), cv2.DIST_L2, 3)
        mean_distance = 0.5 * (float(cand_distance[ref_edge].mean()) + float(ref_distance[cand_edge].mean()))
        edge_score = math.exp(-mean_distance / 4.0)
    elif not ref_edge.any() and not cand_edge.any():
        mean_distance, edge_score = 0.0, 1.0
    else:
        mean_distance, edge_score = float(max(ref_gray.shape)), 0.0

    union = ref_ink | cand_ink
    if union.any():
        ys, xs = np.where(union)
        pad = 12
        y0, y1 = max(0, int(ys.min()) - pad), min(ref_gray.shape[0], int(ys.max()) + pad + 1)
        x0, x1 = max(0, int(xs.min()) - pad), min(ref_gray.shape[1], int(xs.max()) + pad + 1)
        _, ssim_map = structural_similarity(ref_gray[y0:y1, x0:x1], cand_gray[y0:y1, x0:x1],
                                            data_range=255, full=True)
        mask = cv2.dilate(union[y0:y1, x0:x1].astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
        foreground_ssim = clamp(float(ssim_map[mask].mean())) if mask.any() else 1.0
    else:
        foreground_ssim = 1.0

    score = 0.50 * ink_f1 + 0.25 * edge_score + 0.25 * foreground_ssim
    diff = np.full_like(reference, 255)
    overlap = ref_ink & cand_ink
    diff[overlap] = (35, 35, 35)
    diff[ref_ink & ~cand_ink] = (220, 45, 45)
    diff[cand_ink & ~ref_ink] = (35, 105, 220)
    return {
        "score": score,
        "ink_precision": precision,
        "ink_recall": recall,
        "ink_f1": ink_f1,
        "edge_score": edge_score,
        "mean_edge_distance_px": mean_distance,
        "foreground_ssim": foreground_ssim,
    }, diff


def compare_pdfs(reference_path: Path, candidate_path: Path) -> tuple[dict, PdfData, PdfData, list[np.ndarray]]:
    reference = extract_pdf(reference_path)
    candidate = extract_pdf(candidate_path)
    pairs, unmatched_ref, unmatched_cand = match_words(reference, candidate)

    ref_norms = [word.norm for word in reference.words if word.norm]
    cand_norms = [word.norm for word in candidate.words if word.norm]
    intersection = sum((Counter(ref_norms) & Counter(cand_norms)).values())
    precision = intersection / max(1, len(cand_norms))
    recall = intersection / max(1, len(ref_norms))
    token_f1 = 2 * precision * recall / max(EPSILON, precision + recall)
    ref_text = normalize_text(" ".join(reference.page_text))
    cand_text = normalize_text(" ".join(candidate.page_text))
    char_similarity = SequenceMatcher(None, ref_text, cand_text, autojunk=False).ratio()
    sequence_similarity = SequenceMatcher(None, ref_norms, cand_norms, autojunk=False).ratio()
    content = 0.75 * token_f1 + 0.25 * char_similarity

    word_geometry, match_records, page_assignment = _word_geometry(reference, candidate, pairs)
    reading_order = _reading_order_score(pairs)
    flow = _flow_score(reference, candidate, pairs)
    page_geometry = _page_geometry(reference, candidate)
    layout = 0.50 * word_geometry + 0.25 * flow + 0.15 * reading_order + 0.10 * page_geometry
    typography, typography_details = _typography(reference, candidate, pairs)

    ref_pages, cand_pages = len(reference.page_sizes), len(candidate.page_sizes)
    page_count_score = min(ref_pages, cand_pages) / max(1, max(ref_pages, cand_pages))
    pagination = 0.70 * page_count_score + 0.30 * page_assignment

    raster_pages: list[dict] = []
    diff_images: list[np.ndarray] = []
    for page_index in range(max(ref_pages, cand_pages)):
        if page_index < ref_pages:
            ref_image = render_page(reference_path, page_index)
        else:
            cand_shape = render_page(candidate_path, page_index).shape
            ref_image = np.full(cand_shape, 255, dtype=np.uint8)
        if page_index < cand_pages:
            cand_image = render_page(candidate_path, page_index)
        else:
            cand_image = np.full(ref_image.shape, 255, dtype=np.uint8)
        page_metric, diff = raster_page_metrics(ref_image, cand_image)
        page_metric["page"] = page_index + 1
        raster_pages.append(page_metric)
        diff_images.append(diff)
    raster = float(np.mean([page["score"] for page in raster_pages])) if raster_pages else 0.0

    visual = geometric_mean(((pagination, 0.10), (layout, 0.40), (typography, 0.20), (raster, 0.30)))
    overall = geometric_mean(((content, 0.35), (visual, 0.65)))

    flags = []
    if ref_pages != cand_pages:
        flags.append("page_count_mismatch")
    if len(pairs) < 10:
        flags.append("low_layout_evidence")
    if abs(content - visual) > 0.25:
        flags.append("content_visual_disagreement")
    if abs(raster - layout) > 0.25:
        flags.append("raster_layout_disagreement")
    if typography < 0.55 and len(pairs) >= 10:
        flags.append("typography_mismatch")

    result = {
        "metric_version": METRIC_VERSION,
        "reference_pdf": str(reference_path),
        "candidate_pdf": str(candidate_path),
        "reference_pages": ref_pages,
        "candidate_pages": cand_pages,
        "reference_words": len(ref_norms),
        "candidate_words": len(cand_norms),
        "matched_words": len(pairs),
        "unmatched_reference_words": len(unmatched_ref),
        "unmatched_candidate_words": len(unmatched_cand),
        "scores": {
            "overall": overall,
            "visual": visual,
            "content": content,
            "pagination": pagination,
            "layout": layout,
            "typography": typography,
            "raster": raster,
        },
        "content_details": {
            "token_precision": precision,
            "token_recall": recall,
            "token_f1": token_f1,
            "character_similarity": char_similarity,
            "reading_sequence_similarity": sequence_similarity,
        },
        "layout_details": {
            "word_geometry": word_geometry,
            "flow": flow,
            "reading_order": reading_order,
            "page_geometry": page_geometry,
            "page_assignment": page_assignment,
        },
        "typography_details": typography_details,
        "raster_pages": raster_pages,
        "review_flags": flags,
        "matches": match_records,
        "unmatched_reference_indices": sorted(unmatched_ref),
        "unmatched_candidate_indices": sorted(unmatched_cand),
    }
    return result, reference, candidate, diff_images


def _box_color(position_error: float, same_page: bool) -> tuple[int, int, int]:
    if not same_page or position_error > 0.05:
        return (238, 135, 35)
    if position_error > 0.015:
        return (235, 190, 25)
    return (25, 165, 88)


def _draw_word_box(draw: ImageDraw.ImageDraw, bbox: tuple[float, ...], color: tuple[int, int, int],
                   width: int = 2) -> None:
    scaled = tuple(int(round(value * RENDER_SCALE)) for value in bbox)
    draw.rectangle(scaled, outline=color, width=width)


def create_diagnostic_images(result: dict, reference: PdfData, candidate: PdfData,
                             diff_images: list[np.ndarray], out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    ref_matches = {record["reference_index"]: record for record in result["matches"]}
    cand_matches = {record["candidate_index"]: record for record in result["matches"]}
    ref_unmatched = set(result["unmatched_reference_indices"])
    cand_unmatched = set(result["unmatched_candidate_indices"])
    assets = {"reference": [], "candidate": [], "diff": []}

    for page_index in range(len(reference.page_sizes)):
        image = Image.fromarray(render_page(Path(reference.path), page_index))
        draw = ImageDraw.Draw(image)
        for word in (word for word in reference.words if word.page == page_index):
            if word.index in ref_unmatched:
                _draw_word_box(draw, word.bbox, (220, 45, 45), 3)
            elif word.index in ref_matches:
                record = ref_matches[word.index]
                color = _box_color(record["position_error"], record["reference_page"] == record["candidate_page"])
                _draw_word_box(draw, word.bbox, color, 2)
        path = out_dir / f"reference_p{page_index + 1}_boxes.png"
        image.save(path)
        assets["reference"].append(path)

    for page_index in range(len(candidate.page_sizes)):
        image = Image.fromarray(render_page(Path(candidate.path), page_index))
        draw = ImageDraw.Draw(image)
        for word in (word for word in candidate.words if word.page == page_index):
            if word.index in cand_unmatched:
                _draw_word_box(draw, word.bbox, (35, 105, 220), 3)
            elif word.index in cand_matches:
                record = cand_matches[word.index]
                color = _box_color(record["position_error"], record["reference_page"] == record["candidate_page"])
                _draw_word_box(draw, word.bbox, color, 2)
        path = out_dir / f"candidate_p{page_index + 1}_boxes.png"
        image.save(path)
        assets["candidate"].append(path)

    for page_index, array in enumerate(diff_images):
        image = Image.fromarray(array)
        draw = ImageDraw.Draw(image)
        for record in result["matches"]:
            if record["reference_page"] == page_index + 1 and record["candidate_page"] == page_index + 1:
                if record["position_error"] > 0.015:
                    _draw_word_box(draw, tuple(record["reference_bbox"]), (238, 135, 35), 2)
        for ref_index in ref_unmatched:
            word = reference.words[ref_index]
            if word.page == page_index:
                _draw_word_box(draw, word.bbox, (220, 45, 45), 3)
        for cand_index in cand_unmatched:
            word = candidate.words[cand_index]
            if word.page == page_index:
                _draw_word_box(draw, word.bbox, (35, 105, 220), 3)
        path = out_dir / f"diff_p{page_index + 1}.png"
        image.save(path)
        assets["diff"].append(path)

    return {key: [str(path) for path in value] for key, value in assets.items()}


def public_result(result: dict) -> dict:
    """Return the JSON payload without the large per-token match list."""
    return {key: value for key, value in result.items()
            if key not in {"matches", "unmatched_reference_indices", "unmatched_candidate_indices"}}
