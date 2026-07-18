#!/usr/bin/env python3
"""Generate and evaluate deterministic, source-known PDF perturbations.

These artifacts are controlled mutations of benchmark references. They are not
AI conversions and must not be reported as model outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import io
import json
import math
import re
import shutil
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import fitz
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = ROOT / "data" / "latex_benchmark_v0" / "accepted_manifest.csv"
DEFAULT_APPLICABILITY = ROOT / "results" / "metric_research_v1" / "augmentation_applicability_157.csv"
DEFAULT_OUTPUT = ROOT / "results" / "metric_research_v1" / "augmentations_v1"
SEVERITIES = (1, 2, 3)
AXIS_COLUMNS = (
    "axis_content", "axis_layout", "axis_typography", "axis_appearance",
    "axis_structure", "axis_pagination",
)
OUTPUT_FIELDS = (
    "sample_id", "category", "family", "variant", "severity", "seed", "applicable",
    "status", "reason", "expected_axis", "expected_page", "expected_bbox",
    "target_page", "target_bbox", "localization_applicable",
    "predicted_page", "predicted_bbox", "components", "variant_id",
    "artifact_kind", "is_ai_output", "source_pdf", "candidate_pdf",
    "metric_adapter", *AXIS_COLUMNS,
)


class NotApplicable(Exception):
    """The source lacks the construct required by one planned perturbation."""


@dataclass(frozen=True)
class FamilySpec:
    name: str
    operation: str
    expected_axis: str
    severities: tuple[int, ...] = SEVERITIES
    components: tuple[str, ...] = ()
    group: str = ""
    parameter: str = ""

    @property
    def family_name(self) -> str:
        return self.group or self.name


@dataclass(frozen=True)
class PlanCase:
    sample_id: str
    category: str
    source_pdf: Path
    family: FamilySpec
    severity: int
    seed: int

    @property
    def variant_id(self) -> str:
        value = f"{self.seed}|{self.sample_id}|{self.family.name}|{self.severity}"
        return hashlib.sha256(value.encode()).hexdigest()[:16]


@dataclass
class Target:
    page: int
    bbox: tuple[float, float, float, float]
    payload: dict = field(default_factory=dict)


@dataclass
class ReferenceInfo:
    page_sizes: list[tuple[float, float]]
    words: list[tuple[int, tuple[float, float, float, float], str]]
    blocks: list[tuple[int, tuple[float, float, float, float], str]]
    tables: list[tuple[int, tuple[float, float, float, float]]]
    figures: list[tuple[int, tuple[float, float, float, float]]]
    source_text: str


CONTROL_SPECS = (
    FamilySpec("lossless_roundtrip", "lossless", "invariant", (0,),
               group="identity_lossless_roundtrip"),
)
UNIVERSAL_SPECS = (
    FamilySpec("translate_left", "global_translation", "layout", group="canvas_translation", parameter="left"),
    FamilySpec("translate_right", "global_translation", "layout", group="canvas_translation", parameter="right"),
    FamilySpec("translate_up", "global_translation", "layout", group="canvas_translation", parameter="up"),
    FamilySpec("translate_down", "global_translation", "layout", group="canvas_translation", parameter="down"),
    FamilySpec("scale_shrink", "global_scale", "layout", group="uniform_scale", parameter="shrink"),
    FamilySpec("scale_grow", "global_scale", "layout", group="uniform_scale", parameter="grow"),
    FamilySpec("block_left", "block_displacement", "layout", group="largest_block_displacement", parameter="left"),
    FamilySpec("block_right", "block_displacement", "layout", group="largest_block_displacement", parameter="right"),
    FamilySpec("block_up", "block_displacement", "layout", group="largest_block_displacement", parameter="up"),
    FamilySpec("block_down", "block_displacement", "layout", group="largest_block_displacement", parameter="down"),
    FamilySpec("text_deletion", "text_deletion", "content", group="text_span_deletion"),
    FamilySpec("lexical_corruption", "lexical_corruption", "content", group="lexical_numeric_substitution"),
    FamilySpec("numeric_corruption", "numeric_corruption", "content", group="lexical_numeric_substitution"),
    FamilySpec("font_smaller", "font_size", "typography", group="typography_reflow", parameter="smaller"),
    FamilySpec("font_larger", "font_size", "typography", group="typography_reflow", parameter="larger"),
    FamilySpec("line_spacing_tighter", "line_spacing", "typography", group="typography_reflow", parameter="tighter"),
    FamilySpec("line_spacing_wider", "line_spacing", "typography", group="typography_reflow", parameter="wider"),
    FamilySpec("crop_left", "page_crop", "appearance", group="edge_crop_local_occlusion", parameter="left"),
    FamilySpec("crop_right", "page_crop", "appearance", group="edge_crop_local_occlusion", parameter="right"),
    FamilySpec("crop_top", "page_crop", "appearance", group="edge_crop_local_occlusion", parameter="top"),
    FamilySpec("crop_bottom", "page_crop", "appearance", group="edge_crop_local_occlusion", parameter="bottom"),
    FamilySpec("local_occlusion", "local_occlusion", "content+appearance", group="edge_crop_local_occlusion"),
    FamilySpec("appearance_blur", "appearance_blur", "appearance", group="render_only_degradation"),
    FamilySpec("appearance_downsample", "appearance_downsample", "appearance", group="render_only_degradation"),
    FamilySpec("appearance_jpeg", "appearance_jpeg", "appearance", group="render_only_degradation"),
)
COMPOUND_SPECS = (
    FamilySpec(
        "compound_delete_translate", "compound", "content", (2,),
        components=("text_deletion", "translate_right"), group="fixed_compound_defects",
    ),
    FamilySpec(
        "compound_font_occlusion", "compound", "appearance", (2,),
        components=("font_larger", "local_occlusion"), group="fixed_compound_defects",
    ),
    FamilySpec(
        "compound_lexical_block", "compound", "layout", (2,),
        components=("lexical_corruption", "block_down"), group="fixed_compound_defects",
    ),
    FamilySpec("compound_numeric_crop", "compound", "content+appearance", (2,),
               components=("numeric_corruption", "crop_bottom"), group="fixed_compound_defects"),
    FamilySpec("compound_blur_occlusion", "compound", "appearance", (2,),
               components=("appearance_blur", "local_occlusion"), group="fixed_compound_defects"),
    FamilySpec("compound_spacing_block", "compound", "typography+layout", (2,),
               components=("line_spacing_wider", "block_left"), group="fixed_compound_defects"),
)
MULTIPAGE_SPECS = (
    FamilySpec("page_reverse", "page_reverse", "pagination", (1,), group="page_sequence_and_count"),
    FamilySpec("page_swap_first", "page_swap_first", "pagination", (1,), group="page_sequence_and_count"),
    FamilySpec("blank_page_before", "blank_page_before", "pagination", (1,), group="page_sequence_and_count"),
    FamilySpec("blank_page_after", "blank_page_after", "pagination", (1,), group="page_sequence_and_count"),
)
SCOPE_SPECS = {
    "display_math": (
        FamilySpec("display_math_delete", "math_symbol_deletion", "content", group="display_math_structure"),
        FamilySpec("display_math_corrupt", "math_symbol_corruption", "content", group="display_math_structure"),
        FamilySpec("display_math_displace", "block_displacement", "layout", group="display_math_structure", parameter="right"),
        FamilySpec("display_math_occlude", "local_occlusion", "content+appearance", group="display_math_structure"),
    ),
    "inline_math": (
        FamilySpec("inline_math_corrupt", "math_symbol_corruption", "content", group="inline_math_structure"),
        FamilySpec("inline_math_resize", "math_font_size", "typography", group="inline_math_structure", parameter="larger"),
    ),
    "semantic_table": (
        FamilySpec("table_row_occlusion", "table_row_occlusion", "content+appearance", group="semantic_table_structure"),
        FamilySpec("table_column_occlusion", "table_column_occlusion", "content+appearance", group="semantic_table_structure"),
        FamilySpec("table_displacement", "table_displacement", "layout", group="semantic_table_structure", parameter="right"),
        FamilySpec("table_text_corruption", "table_text_corruption", "content", group="semantic_table_structure"),
        FamilySpec("table_rule_occlusion", "table_rule_occlusion", "appearance", group="semantic_table_structure"),
    ),
    "semantic_figure": (
        FamilySpec("figure_occlusion", "figure_occlusion", "content+appearance", group="figure_and_caption"),
        FamilySpec("figure_displacement", "figure_displacement", "layout", group="figure_and_caption", parameter="right"),
        FamilySpec("figure_resize", "figure_resize", "layout", group="figure_and_caption", parameter="shrink"),
        FamilySpec("figure_substitution", "figure_substitution", "content+appearance", group="figure_and_caption"),
        FamilySpec("caption_corruption", "caption_corruption", "content", group="figure_and_caption"),
    ),
    "list": (
        FamilySpec("list_marker_deletion", "list_marker_deletion", "content", group="list_structure"),
        FamilySpec("list_item_right", "block_displacement", "layout", group="list_structure", parameter="right"),
        FamilySpec("list_item_left", "block_displacement", "layout", group="list_structure", parameter="left"),
        FamilySpec("list_item_occlusion", "local_occlusion", "content+appearance", group="list_structure"),
    ),
    "crossref": (
        FamilySpec("crossref_token_corruption", "crossref_corruption", "content", group="cross_reference_semantics"),
        FamilySpec("citation_token_deletion", "citation_deletion", "content", group="cross_reference_semantics"),
        FamilySpec("crossref_region_displacement", "block_displacement", "layout", group="cross_reference_semantics", parameter="right"),
    ),
    "algorithm": (
        FamilySpec("algorithm_line_deletion", "algorithm_line_deletion", "content", group="algorithm_structure"),
        FamilySpec("algorithm_line_right", "block_displacement", "layout", group="algorithm_structure", parameter="right"),
        FamilySpec("algorithm_line_left", "block_displacement", "layout", group="algorithm_structure", parameter="left"),
        FamilySpec("algorithm_rule_occlusion", "algorithm_rule_occlusion", "appearance", group="algorithm_structure"),
    ),
    "form": (
        FamilySpec("form_field_occlusion", "form_field_occlusion", "appearance", group="form_geometry"),
        FamilySpec("form_field_right", "block_displacement", "layout", group="form_geometry", parameter="right"),
        FamilySpec("form_block_font_smaller", "font_size", "typography", group="form_geometry", parameter="smaller"),
    ),
    "prose": (
        FamilySpec("paragraph_displacement", "block_displacement", "layout", group="prose_hierarchy", parameter="down"),
        FamilySpec("prose_block_font_larger", "font_size", "typography", group="prose_hierarchy", parameter="larger"),
        FamilySpec("paragraph_occlusion", "local_occlusion", "content+appearance", group="prose_hierarchy"),
    ),
    "compact": (
        FamilySpec("compact_block_displacement", "block_displacement", "layout", group="compact_paper_flow", parameter="right"),
        FamilySpec("compact_scale", "global_scale", "layout", group="compact_paper_flow", parameter="shrink"),
        FamilySpec("compact_blank_page_stress", "append_blank_pages", "pagination", group="compact_paper_flow"),
    ),
}
SPEC_BY_NAME = {
    spec.name: spec
    for spec in (
        *CONTROL_SPECS, *UNIVERSAL_SPECS, *COMPOUND_SPECS, *MULTIPAGE_SPECS,
        *(spec for specs in SCOPE_SPECS.values() for spec in specs),
    )
}


def category_key(category: str) -> str:
    for key in ("prose", "list", "math", "table", "figure", "crossref", "algorithm", "compact", "form"):
        if key in category:
            return key
    raise ValueError(f"no specialized family mapping for category {category!r}")


def stable_index(length: int, *parts: object) -> int:
    digest = hashlib.sha256("|".join(map(str, parts)).encode()).digest()
    return int.from_bytes(digest[:8], "big") % length


def _rect_tuple(rect: fitz.Rect | tuple) -> tuple[float, float, float, float]:
    value = fitz.Rect(rect)
    return (float(value.x0), float(value.y0), float(value.x1), float(value.y1))


def _union(rectangles: list[tuple[float, float, float, float]]) -> tuple[float, float, float, float]:
    return (
        min(rect[0] for rect in rectangles), min(rect[1] for rect in rectangles),
        max(rect[2] for rect in rectangles), max(rect[3] for rect in rectangles),
    )


class ReferenceCache:
    def __init__(self) -> None:
        self.bytes: dict[Path, bytes] = {}
        self.info: dict[Path, ReferenceInfo] = {}

    def load_bytes(self, path: Path) -> bytes:
        if path not in self.bytes:
            self.bytes[path] = path.read_bytes()
        return self.bytes[path]

    def inspect(self, path: Path) -> ReferenceInfo:
        if path in self.info:
            return self.info[path]
        data = self.load_bytes(path)
        document = fitz.open(stream=data, filetype="pdf")
        words = []
        blocks = []
        tables = []
        figures = []
        page_sizes = []
        for page_index, page in enumerate(document):
            page_sizes.append((float(page.rect.width), float(page.rect.height)))
            for word in page.get_text("words", sort=True):
                words.append((page_index, _rect_tuple(word[:4]), str(word[4])))
            for block in page.get_text("blocks", sort=True):
                if len(block) >= 7 and int(block[6]) == 0 and str(block[4]).strip():
                    blocks.append((page_index, _rect_tuple(block[:4]), str(block[4]).strip()))
            try:
                tables.extend((page_index, _rect_tuple(table.bbox)) for table in page.find_tables().tables)
            except Exception:
                pass
            for image in page.get_image_info():
                if image.get("bbox"):
                    bbox = fitz.Rect(image["bbox"])
                    if bbox.width * bbox.height > 100:
                        figures.append((page_index, _rect_tuple(bbox)))
            drawing_rectangles = []
            for drawing in page.get_drawings():
                bbox = fitz.Rect(drawing["rect"])
                drawing_rectangles.append(bbox)
                if 400 < bbox.width * bbox.height < page.rect.width * page.rect.height * 0.8:
                    figures.append((page_index, _rect_tuple(bbox)))
            # Figure placeholders and ruled objects are often encoded as
            # separate zero-area line drawings. Their union is the meaningful
            # source-known region, not any individual line.
            if drawing_rectangles:
                union = fitz.Rect(
                    min(bbox.x0 for bbox in drawing_rectangles),
                    min(bbox.y0 for bbox in drawing_rectangles),
                    max(bbox.x1 for bbox in drawing_rectangles),
                    max(bbox.y1 for bbox in drawing_rectangles),
                )
                area = union.width * union.height
                if 400 < area < page.rect.width * page.rect.height * 0.8:
                    figures.append((page_index, _rect_tuple(union)))
        document.close()
        source_path = path.with_name("main.tex")
        source_text = source_path.read_text(encoding="utf-8", errors="replace") if source_path.exists() else ""
        result = ReferenceInfo(page_sizes, words, blocks, tables, figures, source_text)
        self.info[path] = result
        return result


def read_manifest(path: Path, sample_ids: set[str] | None = None,
                  categories: set[str] | None = None) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get("status", "accepted") == "accepted"]
    if sample_ids:
        rows = [row for row in rows if row["sample_id"] in sample_ids]
    if categories:
        rows = [row for row in rows if row["category"] in categories]
    return sorted(rows, key=lambda row: row["sample_id"])


def add_applicability(rows: list[dict[str, str]], path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return rows
    with path.open(newline="", encoding="utf-8") as handle:
        by_sample = {row["sample_id"]: row for row in csv.DictReader(handle)}
    return [{**row, **by_sample.get(row["sample_id"], {})} for row in rows]


def resolve_source_pdf(row: dict[str, str]) -> Path:
    if row.get("reference_pdf"):
        path = Path(row["reference_pdf"])
    else:
        path = Path(row["sample_dir"]) / "reference.pdf"
    return path if path.is_absolute() else ROOT / path


def _row_bool(row: dict[str, str], field: str, fallback: bool = False) -> bool:
    value = str(row.get(field, "")).strip().casefold()
    if not value:
        return fallback
    return value in {"1", "true", "yes", "y"}


def _scope_fallback(category: str, scope: str) -> bool:
    key = category_key(category)
    return {
        "display_math": key == "math",
        "inline_math": key == "math",
        "semantic_table": key == "table",
        "semantic_figure": key == "figure",
        "list": key == "list",
        "crossref": key == "crossref",
        "algorithm": key == "algorithm",
        "form": key == "form",
        "prose": key == "prose",
        "compact": key == "compact",
    }[scope]


def _multipage_specs(page_count: int) -> tuple[FamilySpec, ...]:
    fixed = MULTIPAGE_SPECS
    indexed = tuple(
        FamilySpec(
            f"page_{operation}_{page_index}", f"page_{operation}_index", "pagination",
            (1,), group="page_sequence_and_count", parameter=str(page_index),
        )
        for operation in ("delete", "duplicate")
        for page_index in range(page_count)
    )
    return (*fixed, *indexed)


def plan_cases(rows: list[dict[str, str]], seed: int) -> list[PlanCase]:
    cases = []
    for row in rows:
        page_count = int(row.get("reference_pages") or 0)
        if not page_count:
            with fitz.open(resolve_source_pdf(row)) as document:
                page_count = document.page_count
        specialized = tuple(
            spec
            for scope, scope_specs in SCOPE_SPECS.items()
            if _row_bool(row, f"apply_{scope}", _scope_fallback(row["category"], scope))
            for spec in scope_specs
        )
        multipage = _multipage_specs(page_count) if page_count > 1 else ()
        specs = (*CONTROL_SPECS, *UNIVERSAL_SPECS, *COMPOUND_SPECS, *multipage, *specialized)
        for spec in specs:
            for severity in spec.severities:
                cases.append(PlanCase(
                    row["sample_id"], row["category"], resolve_source_pdf(row),
                    spec, severity, seed,
                ))
    return cases


def _best_local_group(info: ReferenceInfo, candidates: list[tuple[int, tuple, str]]) -> list[tuple[int, tuple, str]]:
    groups = []
    for page, bbox, _text in info.blocks:
        block = fitz.Rect(bbox)
        group = [
            word for word in candidates if word[0] == page
            and block.contains(fitz.Point(
                (word[1][0] + word[1][2]) / 2,
                (word[1][1] + word[1][3]) / 2,
            ))
        ]
        if group:
            groups.append(group)
    if groups:
        return max(groups, key=lambda group: (len(group), -group[0][0], -group[0][1][1]))
    by_page: dict[int, list[tuple[int, tuple, str]]] = defaultdict(list)
    for word in candidates:
        by_page[word[0]].append(word)
    return max(by_page.values(), key=len)


def _selected_words(info: ReferenceInfo, case: PlanCase, numeric: bool = False,
                    pattern: re.Pattern | None = None) -> list[tuple[int, tuple, str]]:
    candidates = info.words
    if numeric:
        candidates = [word for word in candidates if re.search(r"\d", word[2])]
    if pattern:
        candidates = [word for word in candidates if pattern.search(word[2])]
    if not candidates:
        raise NotApplicable("no matching text tokens")
    candidates = _best_local_group(info, candidates)
    fractions = {1: 0.01, 2: 0.05, 3: 0.15}
    count = max(case.severity, round(len(candidates) * fractions.get(case.severity, 0.05)))
    count = min(count, len(candidates))
    anchor = stable_index(len(candidates), case.seed, case.sample_id, case.family.name)
    start = min(anchor, len(candidates) - count)
    return candidates[start:start + count]


def _words_in_region(info: ReferenceInfo, page: int, bbox: tuple) -> list[tuple[int, tuple, str]]:
    region = fitz.Rect(bbox)
    return [
        word for word in info.words
        if word[0] == page and region.intersects(fitz.Rect(word[1]))
    ]


def target_for(case: PlanCase, info: ReferenceInfo) -> Target:
    operation = case.family.operation
    if not info.page_sizes:
        raise NotApplicable("empty PDF")
    full_page = (0.0, 0.0, *info.page_sizes[0])
    if operation in {
        "identity", "lossless", "global_translation", "global_scale", "page_crop",
        "appearance_blur", "appearance_downsample", "appearance_jpeg",
    }:
        return Target(0, full_page)
    if operation in {
        "page_reverse", "page_swap_first", "blank_page_before", "blank_page_after",
        "page_delete_index", "page_duplicate_index",
    }:
        if len(info.page_sizes) < 2:
            raise NotApplicable("requires at least two pages")
        page = int(case.family.parameter) if operation in {"page_delete_index", "page_duplicate_index"} else 0
        return Target(page, (0.0, 0.0, *info.page_sizes[page]))
    if operation == "append_blank_pages":
        page = len(info.page_sizes) - 1
        return Target(page, (0.0, 0.0, *info.page_sizes[page]))
    if operation == "compound":
        targets = [target_for(PlanCase(
            case.sample_id, case.category, case.source_pdf, SPEC_BY_NAME[name], case.severity, case.seed
        ), info) for name in case.family.components]
        same_page = all(target.page == targets[0].page for target in targets)
        return Target(targets[0].page, _union([target.bbox for target in targets]) if same_page else targets[0].bbox)
    if operation in {"text_deletion", "lexical_corruption", "numeric_corruption"}:
        words = _selected_words(info, case, numeric=operation == "numeric_corruption")
        return Target(words[0][0], _union([word[1] for word in words]), {"words": words})
    if operation in {"math_symbol_deletion", "math_symbol_corruption", "math_font_size"}:
        symbolic = [
            word for word in info.words
            if len(word[2]) <= 4 or re.search(r"[=+\-*/^_<>≤≥∑∫√()]", word[2])
        ]
        candidates = _best_local_group(info, symbolic) if symbolic else _selected_words(info, case)
        page = candidates[0][0]
        count = min(case.severity, len(candidates))
        anchor = stable_index(len(candidates), case.seed, case.sample_id, case.family.name)
        start = min(anchor, len(candidates) - count)
        selected = candidates[start:start + count]
        return Target(page, _union([word[1] for word in selected]),
                      {"words": selected, "text": " ".join(word[2] for word in selected)})
    if operation in {"list_marker_deletion", "crossref_corruption", "citation_deletion"}:
        patterns = {
            "list_marker_deletion": re.compile(r"^(?:[•·*-]|\(?\d+[.)])$"),
            "crossref_corruption": re.compile(r"^(?:fig(?:ure)?|table|section|eq(?:uation)?)", re.I),
            "citation_deletion": re.compile(r"^(?:\[?\d+[\],;]?|cite|ref)", re.I),
        }
        words = _selected_words(info, case, pattern=patterns[operation])
        return Target(words[0][0], _union([word[1] for word in words]), {"words": words})
    if operation in {
        "table_row_occlusion", "table_column_occlusion", "table_displacement",
        "table_text_corruption", "table_rule_occlusion",
    }:
        candidates = list(info.tables)
        if not candidates and "tables" in case.category:
            # Borderless source tables are extracted as dense multiline text
            # blocks. Restrict this fallback to table-category documents.
            candidates = [
                (page, bbox) for page, bbox, text in info.blocks
                if len([line for line in text.splitlines() if line.strip()]) >= 4
            ]
        if not candidates:
            raise NotApplicable("no table or dense table-text region detected")
        page, bbox = max(candidates, key=lambda item: (item[1][2] - item[1][0]) * (item[1][3] - item[1][1]))
        if operation == "table_text_corruption":
            words = _words_in_region(info, page, bbox)
            if not words:
                raise NotApplicable("table region has no extracted text token")
            count = min(case.severity, len(words))
            anchor = stable_index(len(words), case.seed, case.sample_id, case.family.name)
            start = min(anchor, len(words) - count)
            selected = words[start:start + count]
            return Target(page, _union([word[1] for word in selected]), {"words": selected})
        return Target(page, bbox)
    if operation in {"caption_corruption"}:
        labels = [word for word in info.words if re.match(r"^(?:fig(?:ure)?)[.:]?", word[2], re.I)]
        if not labels:
            raise NotApplicable("no extracted figure caption label")
        label = labels[stable_index(len(labels), case.seed, case.sample_id, case.family.name)]
        same_line = [
            word for word in info.words if word[0] == label[0]
            and abs((word[1][1] + word[1][3]) / 2 - (label[1][1] + label[1][3]) / 2) < 4
        ]
        start = same_line.index(label) if label in same_line else 0
        selected = same_line[start:start + case.severity] or [label]
        return Target(label[0], _union([word[1] for word in selected]), {"words": selected})
    if operation in {
        "figure_occlusion", "figure_displacement", "figure_resize", "figure_substitution",
    }:
        if not info.figures:
            raise NotApplicable("no figure region detected")
        page, bbox = max(info.figures, key=lambda item: (item[1][2] - item[1][0]) * (item[1][3] - item[1][1]))
        return Target(page, bbox)
    if not info.blocks:
        raise NotApplicable("no text block detected")
    page, bbox, text = max(
        info.blocks, key=lambda item: (item[1][2] - item[1][0]) * (item[1][3] - item[1][1])
    )
    if operation == "line_spacing" and len([line for line in text.splitlines() if line.strip()]) < 2:
        raise NotApplicable("no multi-line text block")
    if operation == "algorithm_line_deletion":
        x0, y0, x1, y1 = bbox
        height = max(6.0, (y1 - y0) * {1: 0.08, 2: 0.16, 3: 0.28}[case.severity])
        bbox = (x0, (y0 + y1 - height) / 2, x1, (y0 + y1 + height) / 2)
    if operation == "form_field_occlusion":
        x0, y0, x1, y1 = bbox
        bbox = (x0 + (x1 - x0) * 0.45, y0, x1, y0 + (y1 - y0) * 0.35)
    return Target(page, bbox, {"text": text, "words": _words_in_region(info, page, bbox)})


def affected_target(case: PlanCase, info: ReferenceInfo, target: Target | None = None) -> Target:
    """Return the exact source-coordinate region changed by a planned mutation."""
    if case.family.operation == "compound":
        targets = []
        for name in case.family.components:
            component = PlanCase(
                case.sample_id, case.category, case.source_pdf, SPEC_BY_NAME[name],
                case.severity, case.seed,
            )
            targets.append(affected_target(component, info))
        if all(item.page == targets[0].page for item in targets):
            return Target(targets[0].page, _union([item.bbox for item in targets]))
        return targets[0]
    target = target or target_for(case, info)
    operation = case.family.operation
    rect = fitz.Rect(target.bbox)
    if operation == "page_crop":
        fraction = {1: 0.02, 2: 0.08, 3: 0.18}[case.severity]
        width, height = info.page_sizes[0]
        regions = {
            "left": (0.0, 0.0, width * fraction, height),
            "right": (width * (1 - fraction), 0.0, width, height),
            "top": (0.0, 0.0, width, height * fraction),
            "bottom": (0.0, height * (1 - fraction), width, height),
        }
        return Target(0, regions[case.family.parameter])
    if operation in {"block_displacement", "figure_displacement", "table_displacement"}:
        shift = {1: 3.0, 2: 10.0, 3: 24.0}[case.severity]
        dx, dy = {
            "left": (-shift, 0.0), "right": (shift, 0.0),
            "up": (0.0, -shift), "down": (0.0, shift),
        }.get(case.family.parameter, (shift, shift))
        moved = fitz.Rect(rect) + (dx, dy, dx, dy)
        moved &= fitz.Rect(0, 0, *info.page_sizes[target.page])
        return Target(target.page, _union([_rect_tuple(rect), _rect_tuple(moved)]))
    if operation in {"local_occlusion", "figure_occlusion", "form_field_occlusion"}:
        fraction = {1: 0.06, 2: 0.16, 3: 0.35}[case.severity]
        inset_x = rect.width * (1 - fraction) / 2
        inset_y = rect.height * (1 - fraction) / 2
        rect += (inset_x, inset_y, -inset_x, -inset_y)
        return Target(target.page, _rect_tuple(rect))
    if operation == "figure_substitution":
        fraction = {1: 0.30, 2: 0.60, 3: 1.0}[case.severity]
        inset_x = rect.width * (1 - fraction) / 2
        inset_y = rect.height * (1 - fraction) / 2
        rect += (inset_x, inset_y, -inset_x, -inset_y)
        return Target(target.page, _rect_tuple(rect))
    if operation == "table_row_occlusion":
        fraction = {1: 0.06, 2: 0.16, 3: 0.35}[case.severity]
        height = max(2.0, rect.height * fraction)
        rect = fitz.Rect(
            rect.x0, rect.y0 + rect.height * 0.5 - height / 2,
            rect.x1, rect.y0 + rect.height * 0.5 + height / 2,
        )
        return Target(target.page, _rect_tuple(rect))
    if operation == "table_column_occlusion":
        fraction = {1: 0.06, 2: 0.16, 3: 0.35}[case.severity]
        width = max(2.0, rect.width * fraction)
        rect = fitz.Rect(
            rect.x0 + rect.width * 0.5 - width / 2, rect.y0,
            rect.x0 + rect.width * 0.5 + width / 2, rect.y1,
        )
        return Target(target.page, _rect_tuple(rect))
    if operation in {"table_rule_occlusion", "algorithm_rule_occlusion"}:
        height = max(2.0, rect.height * {1: 0.01, 2: 0.025, 3: 0.05}[case.severity])
        rule = fitz.Rect(rect.x0, rect.y0 + rect.height * 0.5 - height / 2,
                         rect.x1, rect.y0 + rect.height * 0.5 + height / 2)
        return Target(target.page, _rect_tuple(rule))
    return Target(target.page, target.bbox, target.payload)


def _save(document: fitz.Document, path: Path) -> None:
    document.save(path, garbage=4, deflate=True, no_new_id=True)
    document.close()


def _redact(document: fitz.Document, target: Target, boxes: list[tuple] | None = None,
            fill: tuple[float, float, float] = (1, 1, 1)) -> None:
    page = document[target.page]
    for bbox in boxes or [target.bbox]:
        page.add_redact_annot(fitz.Rect(bbox), fill=fill, cross_out=False)
    page.apply_redactions(images=0, graphics=0, text=0)


def _displace(data: bytes, output: Path, target: Target, severity: int, direction: str) -> None:
    source = fitz.open(stream=data, filetype="pdf")
    document = fitz.open(stream=data, filetype="pdf")
    _redact(document, target)
    page = document[target.page]
    clip = fitz.Rect(target.bbox)
    shift = {1: 3.0, 2: 10.0, 3: 24.0}[severity]
    dx, dy = {
        "left": (-shift, 0.0), "right": (shift, 0.0),
        "up": (0.0, -shift), "down": (0.0, shift),
    }.get(direction, (shift, shift))
    destination = clip + (dx, dy, dx, dy)
    destination &= page.rect
    if destination.width < 2 or destination.height < 2:
        source.close()
        document.close()
        raise NotApplicable("displaced region falls outside page")
    page.show_pdf_page(destination, source, target.page, clip=clip, keep_proportion=False, overlay=True)
    source.close()
    _save(document, output)


def _appearance_overlay(data: bytes, output: Path, operation: str, severity: int) -> None:
    source = fitz.open(stream=data, filetype="pdf")
    document = fitz.open()
    for page_index, source_page in enumerate(source):
        page = document.new_page(width=source_page.rect.width, height=source_page.rect.height)
        page.show_pdf_page(page.rect, source, page_index)
        pixmap = source_page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        image_format, save_args = "PNG", {}
        if operation == "appearance_blur":
            image = image.filter(ImageFilter.GaussianBlur({1: 0.6, 2: 1.4, 3: 2.8}[severity]))
        elif operation == "appearance_downsample":
            ratio = {1: 0.75, 2: 0.45, 3: 0.25}[severity]
            reduced = image.resize((max(1, round(image.width * ratio)), max(1, round(image.height * ratio))))
            image = reduced.resize(image.size)
        else:
            image_format, save_args = "JPEG", {"quality": {1: 82, 2: 50, 3: 22}[severity]}
        stream = io.BytesIO()
        image.save(stream, format=image_format, **save_args)
        page.insert_image(page.rect, stream=stream.getvalue(), overlay=True)
    source.close()
    _save(document, output)


def mutate_single(data: bytes, output: Path, case: PlanCase, target: Target) -> None:
    operation = case.family.operation
    severity = case.severity
    if operation == "identity":
        source = fitz.open(stream=data, filetype="pdf")
        document = fitz.open()
        document.insert_pdf(source)
        source.close()
        _save(document, output)
        return
    if operation == "lossless":
        document = fitz.open(stream=data, filetype="pdf")
        _save(document, output)
        return
    if operation in {"global_translation", "global_scale"}:
        source = fitz.open(stream=data, filetype="pdf")
        document = fitz.open()
        for page_index, source_page in enumerate(source):
            page = document.new_page(width=source_page.rect.width, height=source_page.rect.height)
            rect = fitz.Rect(source_page.rect)
            if operation == "global_translation":
                shift = {1: 1.0, 2: 4.0, 3: 12.0}[severity]
                dx, dy = {
                    "left": (-shift, 0.0), "right": (shift, 0.0),
                    "up": (0.0, -shift), "down": (0.0, shift),
                }[case.family.parameter]
                rect += (dx, dy, dx, dy)
            else:
                inset = min(rect.width, rect.height) * {1: 0.005, 2: 0.02, 3: 0.05}[severity]
                if case.family.parameter == "grow":
                    inset = -inset
                rect += (inset, inset, -inset, -inset)
            page.show_pdf_page(rect, source, page_index, keep_proportion=False)
        source.close()
        _save(document, output)
        return
    if operation in {"block_displacement", "figure_displacement", "table_displacement"}:
        _displace(data, output, target, severity, case.family.parameter)
        return
    if operation == "figure_resize":
        source = fitz.open(stream=data, filetype="pdf")
        document = fitz.open(stream=data, filetype="pdf")
        _redact(document, target)
        clip = fitz.Rect(target.bbox)
        factor = {1: 0.92, 2: 0.75, 3: 0.55}[severity]
        destination = fitz.Rect(clip)
        destination += (
            clip.width * (1 - factor) / 2, clip.height * (1 - factor) / 2,
            -clip.width * (1 - factor) / 2, -clip.height * (1 - factor) / 2,
        )
        document[target.page].show_pdf_page(
            destination, source, target.page, clip=clip, keep_proportion=False, overlay=True,
        )
        source.close()
        _save(document, output)
        return
    if operation in {"appearance_blur", "appearance_downsample", "appearance_jpeg"}:
        _appearance_overlay(data, output, operation, severity)
        return
    if operation in {
        "page_reverse", "page_swap_first", "blank_page_before", "blank_page_after",
        "page_delete_index", "page_duplicate_index", "append_blank_pages",
    }:
        source = fitz.open(stream=data, filetype="pdf")
        order = list(range(source.page_count))
        if operation == "page_reverse":
            order.reverse()
        elif operation == "page_swap_first":
            order[0], order[1] = order[1], order[0]
        elif operation == "page_delete_index":
            del order[int(case.family.parameter)]
        elif operation == "page_duplicate_index":
            index = int(case.family.parameter)
            order.insert(index + 1, index)
        document = fitz.open()
        if operation == "blank_page_before":
            document.new_page(width=source[0].rect.width, height=source[0].rect.height)
        for page_index in order:
            document.insert_pdf(source, from_page=page_index, to_page=page_index)
        if operation == "blank_page_after":
            document.new_page(width=source[-1].rect.width, height=source[-1].rect.height)
        elif operation == "append_blank_pages":
            for _ in range(severity):
                document.new_page(width=source[-1].rect.width, height=source[-1].rect.height)
        source.close()
        _save(document, output)
        return
    document = fitz.open(stream=data, filetype="pdf")
    if operation == "page_crop":
        fraction = {1: 0.02, 2: 0.08, 3: 0.18}[severity]
        for page in document:
            width, height = page.rect.width, page.rect.height
            clipped = {
                "left": fitz.Rect(0, 0, width * fraction, height),
                "right": fitz.Rect(width * (1 - fraction), 0, width, height),
                "top": fitz.Rect(0, 0, width, height * fraction),
                "bottom": fitz.Rect(0, height * (1 - fraction), width, height),
            }[case.family.parameter]
            page.add_redact_annot(clipped, fill=(1, 1, 1), cross_out=False)
            page.apply_redactions(images=0, graphics=0, text=0)
    elif operation in {"text_deletion", "math_symbol_deletion", "list_marker_deletion",
                       "citation_deletion", "algorithm_line_deletion"}:
        boxes = [word[1] for word in target.payload.get("words", [])] or [target.bbox]
        _redact(document, target, boxes)
    elif operation in {
        "lexical_corruption", "numeric_corruption", "crossref_corruption",
        "math_symbol_corruption", "table_text_corruption", "caption_corruption",
    }:
        words = target.payload.get("words", [])
        _redact(document, target, [word[1] for word in words])
        page = document[target.page]
        for _, bbox, original in words:
            replacement = "987654" if operation == "numeric_corruption" else "mismatch"
            if operation == "math_symbol_corruption":
                replacement = "≠"
            elif operation == "caption_corruption":
                replacement = "Table"
            if replacement == original:
                replacement = "altered"
            page.insert_textbox(fitz.Rect(bbox), replacement, fontsize=max(4, min(10, fitz.Rect(bbox).height * 0.7)))
    elif operation in {"font_size", "math_font_size", "line_spacing"}:
        words = target.payload.get("words", [])
        if not words:
            document.close()
            raise NotApplicable("typography target has no extracted words")
        _redact(document, target, [word[1] for word in words])
        page = document[target.page]
        if operation in {"font_size", "math_font_size"}:
            factor = (
                {1: 0.9, 2: 0.75, 3: 0.55}
                if case.family.parameter == "smaller"
                else {1: 1.1, 2: 1.3, 3: 1.6}
            )[severity]
            for _, bbox, text in words:
                rect = fitz.Rect(bbox)
                fontsize = max(3.0, rect.height * factor)
                page.insert_text((rect.x0, rect.y1 - rect.height * 0.12), text,
                                 fontsize=fontsize, fontname="helv")
        else:
            target_rect = fitz.Rect(target.bbox)
            factor = (
                {1: 0.92, 2: 0.75, 3: 0.55}
                if case.family.parameter == "tighter"
                else {1: 1.1, 2: 1.35, 3: 1.7}
            )[severity]
            for _, bbox, text in words:
                rect = fitz.Rect(bbox)
                moved_center = target_rect.y0 + (
                    (rect.y0 + rect.y1) / 2 - target_rect.y0
                ) * factor
                fontsize = max(3.0, rect.height)
                page.insert_text((rect.x0, moved_center + rect.height * 0.38), text,
                                 fontsize=fontsize, fontname="helv")
    elif operation in {"local_occlusion", "figure_occlusion", "form_field_occlusion",
                       "table_row_occlusion", "table_column_occlusion", "figure_substitution",
                       "table_rule_occlusion", "algorithm_rule_occlusion"}:
        rect = fitz.Rect(target.bbox)
        fraction = {1: 0.06, 2: 0.16, 3: 0.35}[severity]
        if operation == "table_row_occlusion":
            height = max(2.0, rect.height * fraction)
            rect = fitz.Rect(rect.x0, rect.y0 + rect.height * 0.5 - height / 2, rect.x1,
                             rect.y0 + rect.height * 0.5 + height / 2)
        elif operation == "table_column_occlusion":
            width = max(2.0, rect.width * fraction)
            rect = fitz.Rect(rect.x0 + rect.width * 0.5 - width / 2, rect.y0,
                             rect.x0 + rect.width * 0.5 + width / 2, rect.y1)
        elif operation in {"table_rule_occlusion", "algorithm_rule_occlusion"}:
            height = max(2.0, rect.height * {1: 0.01, 2: 0.025, 3: 0.05}[severity])
            rect = fitz.Rect(rect.x0, rect.y0 + rect.height * 0.5 - height / 2,
                             rect.x1, rect.y0 + rect.height * 0.5 + height / 2)
        elif operation == "figure_substitution":
            fraction = {1: 0.30, 2: 0.60, 3: 1.0}[severity]
            inset_x = rect.width * (1 - fraction) / 2
            inset_y = rect.height * (1 - fraction) / 2
            rect += (inset_x, inset_y, -inset_x, -inset_y)
        else:
            inset_x = rect.width * (1 - fraction) / 2
            inset_y = rect.height * (1 - fraction) / 2
            rect += (inset_x, inset_y, -inset_x, -inset_y)
        local = Target(target.page, _rect_tuple(rect))
        _redact(document, local, fill=(0, 0, 0))
    else:
        document.close()
        raise ValueError(f"unsupported operation: {operation}")
    _save(document, output)


def generate_variant(cache: ReferenceCache, case: PlanCase, output: Path) -> Target:
    info = cache.inspect(case.source_pdf)
    target = target_for(case, info)
    output.parent.mkdir(parents=True, exist_ok=True)
    if case.family.operation != "compound":
        mutate_single(cache.load_bytes(case.source_pdf), output, case, target)
        return affected_target(case, info, target)
    data = cache.load_bytes(case.source_pdf)
    with tempfile.TemporaryDirectory(prefix="lathe-augment-") as directory:
        for index, name in enumerate(case.family.components):
            spec = SPEC_BY_NAME[name]
            component = PlanCase(
                case.sample_id, case.category, case.source_pdf, spec, case.severity, case.seed
            )
            component_target = target_for(component, info)
            path = output if index == len(case.family.components) - 1 else Path(directory) / f"{index}.pdf"
            mutate_single(data, path, component, component_target)
            if path != output:
                data = path.read_bytes()
    return affected_target(case, info, target)


def _flatten_metric(
    result: object, layout_projection: str = "bbox_iou_q10"
) -> tuple[dict[str, float], int | None, tuple | None]:
    if isinstance(result, tuple):
        result = result[0]
    if not isinstance(result, dict):
        raise TypeError("metric evaluator must return a dict or tuple whose first item is a dict")
    axes = result.get("axes") or result.get("scorecard", {}).get("axes", {})
    flattened = {}
    # The metric modules intentionally expose observables, not axis scalars.
    # These high-is-better projections are limited to augmentation response
    # analysis; they are not validated perceptual grades.
    content_metrics = axes.get("content", {}).get("metrics", {})
    content_inventory = (
        content_metrics.get("strict_nfc_token_inventory")
        or content_metrics.get("token_inventory")
        or content_metrics.get("compatibility_nfkc_token_inventory")
        or {}
    )
    content = content_inventory.get("f1")
    geometry = axes.get("geometry", {}).get("metrics", {})
    if layout_projection == "bbox_iou_q10":
        layout = geometry.get("bbox_iou_q10")
    elif layout_projection == "center_displacement_q90":
        displacement = geometry.get("center_displacement_q90")
        layout = (
            1.0 - min(1.0, max(0.0, float(displacement)) / math.sqrt(2.0))
            if isinstance(displacement, (int, float)) and math.isfinite(displacement)
            else None
        )
    elif layout_projection == "text_ltsim_page_macro":
        layout = axes.get("text_ltsim", {}).get("metrics", {}).get(
            "text_ltsim_page_macro"
        )
    else:
        raise ValueError(f"unsupported layout projection: {layout_projection}")
    typography_metrics = axes.get("typography", {}).get("metrics", {})
    typography_error = typography_metrics.get("font_size_abs_log_ratio_max")
    typography_baseline_error = typography_metrics.get("baseline_displacement_q90")
    typography_coverage = typography_metrics.get("style_coverage_hmean")
    raster_axis = axes.get("raster_ink") or axes.get("raster_diagnostic") or {}
    appearance = raster_axis.get("metrics", {}).get("unregistered_tolerant_ink_f1_macro")
    pagination_metrics = axes.get("pagination", {}).get("metrics", {})
    page_break_f1 = pagination_metrics.get("page_break_f1")
    reference_pages = result.get("inputs", {}).get("reference_page_count")
    candidate_pages = result.get("inputs", {}).get("candidate_page_count")
    pagination = None
    if isinstance(reference_pages, int) and isinstance(candidate_pages, int):
        page_count_ratio = min(reference_pages, candidate_pages) / max(1, reference_pages, candidate_pages)
        pagination = page_count_ratio * page_break_f1 if isinstance(page_break_f1, (int, float)) else page_count_ratio
    projections = {
        "axis_content": content,
        "axis_layout": layout,
        "axis_typography": (
            min(
                float(typography_coverage),
                math.exp(-float(typography_error)),
                math.exp(-20.0 * float(typography_baseline_error)),
            )
            if all(
                isinstance(value, (int, float)) and math.isfinite(value)
                for value in (typography_error, typography_baseline_error, typography_coverage)
            )
            else None
        ),
        "axis_appearance": appearance,
        # No structure scalar: v1 explicitly abstains for tables, formulas,
        # and figures until a validated structure-aware metric exists.
        "axis_structure": None,
        "axis_pagination": pagination,
    }
    for name, value in projections.items():
        if isinstance(value, (int, float)) and math.isfinite(value):
            flattened[name] = float(value)

    localization = result.get("localization") or result.get("primary_defect", {})
    if not localization:
        raster_evidence_axis = axes.get("raster_ink") or axes.get("raster_diagnostic")
        if isinstance(raster_evidence_axis, dict):
            localization = raster_evidence_axis.get("evidence", {}).get(
                "top_difference_bbox", {}
            )
    page = localization.get("page") if isinstance(localization, dict) else None
    bbox = None
    if isinstance(localization, dict):
        bbox = localization.get("normalized_bbox") or localization.get("bbox")
    return flattened, page, tuple(bbox) if isinstance(bbox, (list, tuple)) and len(bbox) == 4 else None


def _normalized_expected(target: Target, info: ReferenceInfo) -> tuple[int, list[float]]:
    width, height = info.page_sizes[target.page]
    x0, y0, x1, y1 = target.bbox
    return target.page, [x0 / width, y0 / height, x1 / width, y1 / height]


def _localization_applicable(case: PlanCase) -> bool:
    operation = case.family.operation
    if operation == "compound":
        return all(_localization_applicable(PlanCase(
            case.sample_id, case.category, case.source_pdf, SPEC_BY_NAME[name],
            case.severity, case.seed,
        )) for name in case.family.components)
    return operation not in {
        "identity", "lossless", "global_translation", "global_scale", "page_crop",
        "appearance_blur", "appearance_downsample", "appearance_jpeg",
        "page_reverse", "page_swap_first", "blank_page_before", "blank_page_after",
        "page_delete_index", "page_duplicate_index", "append_blank_pages",
    }


def load_metric_adapter(
    layout_projection: str = "bbox_iou_q10",
    metric_version: str = "v1",
) -> tuple[str, Callable[[Path, Path], tuple[dict, int | None, tuple | None]]]:
    try:
        module_name = f"pdf_metric_axes_{metric_version}"
        module = importlib.import_module(module_name)
        for name in ("evaluate_pdf_pair", "evaluate_pair", "compare_pdfs"):
            function = getattr(module, name, None)
            if callable(function):
                return (
                    f"{module_name}.{name}#layout={layout_projection}",
                    lambda ref, cand, fn=function: _flatten_metric(
                        fn(ref, cand), layout_projection=layout_projection
                    ),
                )
        raise AttributeError(f"{module_name} has no supported pair evaluator")
    except ModuleNotFoundError:
        module = importlib.import_module("pdf_fidelity")
        return (
            f"pdf_fidelity.compare_pdfs#layout={layout_projection}",
            lambda ref, cand: _flatten_metric(
                module.compare_pdfs(ref, cand), layout_projection=layout_projection
            ),
        )


def _base_result(case: PlanCase) -> dict[str, object]:
    return {
        "sample_id": case.sample_id,
        "category": case.category,
        "family": case.family.family_name,
        "variant": case.family.name,
        "severity": case.severity,
        "seed": case.seed,
        "applicable": "false",
        "status": "failed",
        "reason": "",
        "expected_axis": case.family.expected_axis,
        "expected_page": "",
        "expected_bbox": "",
        "target_page": "",
        "target_bbox": "",
        "localization_applicable": "false",
        "predicted_page": "",
        "predicted_bbox": "",
        "components": "+".join(case.family.components),
        "variant_id": case.variant_id,
        "artifact_kind": "controlled_reference_perturbation",
        "is_ai_output": "false",
        "source_pdf": str(case.source_pdf),
        "candidate_pdf": "",
        "metric_adapter": "",
        **{column: "" for column in AXIS_COLUMNS},
    }


def inspect_case(cache: ReferenceCache, case: PlanCase) -> tuple[str, str, Target | None]:
    try:
        info = cache.inspect(case.source_pdf)
        target = affected_target(case, info, target_for(case, info))
        return "planned", "", target
    except NotApplicable as error:
        return "not_applicable", str(error), None
    except Exception as error:
        return "failed", f"inspection failed: {error}", None


def execute_case(cache: ReferenceCache, case: PlanCase, candidate: Path,
                 adapter_name: str, evaluator: Callable) -> dict[str, object]:
    result = _base_result(case)
    status, reason, _ = inspect_case(cache, case)
    if status != "planned":
        result.update(status=status, reason=reason)
        return result
    try:
        target = generate_variant(cache, case, candidate)
        axes, predicted_page, predicted_bbox = evaluator(case.source_pdf, candidate)
        target_page, target_bbox = _normalized_expected(target, cache.inspect(case.source_pdf))
        localizable = _localization_applicable(case)
        expected_page, expected_bbox = target_page, target_bbox
        if case.family.expected_axis == "invariant" or not localizable:
            expected_page, expected_bbox = "", None
        result.update(
            applicable="true", status="applied", reason="", expected_page=expected_page,
            expected_bbox=(
                json.dumps([round(value, 6) for value in expected_bbox])
                if expected_bbox is not None else ""
            ),
            target_page=target_page,
            target_bbox=json.dumps([round(value, 6) for value in target_bbox]),
            localization_applicable=str(localizable).lower(),
            predicted_page=predicted_page if predicted_page is not None else "",
            predicted_bbox=json.dumps(predicted_bbox) if predicted_bbox else "",
            metric_adapter=adapter_name, **axes,
        )
    except NotApplicable as error:
        result.update(status="not_applicable", reason=str(error))
    except Exception as error:
        result.update(status="failed", reason=f"generation/evaluation failed: {error}")
    return result


def summarize_plan(cache: ReferenceCache, cases: list[PlanCase]) -> tuple[list[dict], dict]:
    rows = []
    counts = Counter()
    family_counts: dict[str, Counter] = defaultdict(Counter)
    for case in cases:
        status, reason, target = inspect_case(cache, case)
        counts[status] += 1
        family_counts[case.family.family_name][status] += 1
        rows.append({
            "sample_id": case.sample_id, "category": case.category,
            "family": case.family.family_name, "variant": case.family.name,
            "severity": case.severity, "seed": case.seed,
            "plan_status": status, "reason": reason,
            "expected_axis": case.family.expected_axis,
            "expected_page": (
                target.page if target and case.family.expected_axis != "invariant"
                and _localization_applicable(case) else ""
            ),
            "target_page": target.page if target else "",
            "target_bbox": (
                json.dumps([
                    round(target.bbox[0] / cache.inspect(case.source_pdf).page_sizes[target.page][0], 6),
                    round(target.bbox[1] / cache.inspect(case.source_pdf).page_sizes[target.page][1], 6),
                    round(target.bbox[2] / cache.inspect(case.source_pdf).page_sizes[target.page][0], 6),
                    round(target.bbox[3] / cache.inspect(case.source_pdf).page_sizes[target.page][1], 6),
                ]) if target else ""
            ),
            "localization_applicable": str(_localization_applicable(case) and target is not None).lower(),
            "expected_bbox": (
                json.dumps([
                    round(target.bbox[0] / cache.inspect(case.source_pdf).page_sizes[target.page][0], 6),
                    round(target.bbox[1] / cache.inspect(case.source_pdf).page_sizes[target.page][1], 6),
                    round(target.bbox[2] / cache.inspect(case.source_pdf).page_sizes[target.page][0], 6),
                    round(target.bbox[3] / cache.inspect(case.source_pdf).page_sizes[target.page][1], 6),
                ]) if target and case.family.expected_axis != "invariant"
                and _localization_applicable(case) else ""
            ),
            "components": "+".join(case.family.components), "variant_id": case.variant_id,
            "source_pdf": str(case.source_pdf),
        })
    summary = {
        "artifact_kind": "controlled_reference_perturbation_plan_not_ai_outputs",
        "cases": len(cases), "source_documents": len({case.sample_id for case in cases}),
        "status_counts": dict(sorted(counts.items())),
        "family_counts": {family: dict(sorted(values.items())) for family, values in sorted(family_counts.items())},
    }
    return rows, summary


def write_csv(path: Path, rows: list[dict], fieldnames: tuple | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--applicability", type=Path, default=DEFAULT_APPLICABILITY)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=20260715)
    parser.add_argument("--sample-id", action="append", default=[])
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--variant", action="append", default=[], help="run only these exact variant names")
    parser.add_argument("--dry-run", action="store_true", help="inspect and count the exact matrix only")
    parser.add_argument("--audit-sample", action="append", default=[], help="preserve variants for this sample")
    parser.add_argument(
        "--audit-case", action="append", default=[], metavar="VARIANT:SEVERITY",
        help="preserve this exact variant/severity for every matched source",
    )
    parser.add_argument("--keep-audit-per-family", type=int, default=0)
    parser.add_argument(
        "--layout-projection",
        choices=("bbox_iou_q10", "center_displacement_q90", "text_ltsim_page_macro"),
        default="bbox_iou_q10",
    )
    parser.add_argument("--metric-version", choices=("v1", "v2"), default="v1")
    parser.add_argument("--resume", action="store_true", help="resume from augmentation_results.csv")
    args = parser.parse_args()

    manifest = add_applicability(read_manifest(
        args.manifest, set(args.sample_id) or None, set(args.category) or None,
    ), args.applicability)
    if not manifest:
        raise SystemExit("no accepted samples matched the filters")
    cases = plan_cases(manifest, args.seed)
    if args.variant:
        selected_variants = set(args.variant)
        cases = [case for case in cases if case.family.name in selected_variants]
        if not cases:
            raise SystemExit("no planned cases matched --variant")
    cache = ReferenceCache()
    if args.dry_run:
        rows, summary = summarize_plan(cache, cases)
        write_csv(args.out_dir / "plan.csv", rows, list(rows[0]))
        (args.out_dir / "plan_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=2))
        return

    adapter_name, evaluator = load_metric_adapter(args.layout_projection, args.metric_version)
    candidate_dir = args.out_dir / "candidates"
    audit_dir = args.out_dir / "audit"
    candidates_kept = Counter()
    audit_samples = set(args.audit_sample)
    audit_cases = set()
    for value in args.audit_case:
        try:
            variant, severity = value.rsplit(":", 1)
            audit_cases.add((variant, int(severity)))
        except ValueError as error:
            raise SystemExit(f"invalid --audit-case {value!r}; expected VARIANT:SEVERITY") from error
    results_path = args.out_dir / "augmentation_results.csv"
    if results_path.exists() and not args.resume:
        raise SystemExit(f"results already exist; use --resume or a new --out-dir: {results_path}")
    results = []
    if args.resume and results_path.exists():
        with results_path.open(newline="", encoding="utf-8") as handle:
            results = list(csv.DictReader(handle))
        for row in results:
            if row.get("candidate_pdf"):
                candidates_kept[row["family"]] += 1
    completed = {row["variant_id"] for row in results}
    results_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if results else "w"
    with results_path.open(mode, newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        if not results:
            writer.writeheader()
            handle.flush()
        for case in cases:
            if case.variant_id in completed:
                continue
            filename = f"{case.sample_id}__{case.family.name.replace(':', '_').replace('+', '_')}__s{case.severity}.pdf"
            candidate = candidate_dir / filename
            result = execute_case(cache, case, candidate, adapter_name, evaluator)
            keep = result["status"] == "applied" and (
                case.sample_id in audit_samples
                or (case.family.name, case.severity) in audit_cases
                or candidates_kept[case.family.family_name] < args.keep_audit_per_family
            )
            if candidate.exists() and keep:
                audit_dir.mkdir(parents=True, exist_ok=True)
                audit_path = audit_dir / filename
                shutil.move(candidate, audit_path)
                result["candidate_pdf"] = str(audit_path)
                candidates_kept[case.family.family_name] += 1
            elif candidate.exists():
                candidate.unlink()
            writer.writerow(result)
            handle.flush()
            results.append(result)
            completed.add(case.variant_id)
            if len(results) % 100 == 0:
                print(f"progress {len(results)}/{len(cases)}", flush=True)
    if candidate_dir.exists() and not any(candidate_dir.iterdir()):
        candidate_dir.rmdir()
    summary = {
        "artifact_kind": "controlled_reference_perturbations_not_ai_outputs",
        "source_documents": len(manifest), "planned_cases": len(cases), "cases": len(results),
        "status_counts": dict(Counter(row["status"] for row in results)),
        "audit_variants": sum(1 for row in results if row["candidate_pdf"]),
        "metric_adapter": adapter_name,
        "coordinate_contract": "expected and predicted localization are zero-based pages plus normalized bboxes",
        "score_boundary": (
            "axis columns are transparent high-is-better projections of evaluator observables for "
            "perturbation-response analysis, not validated perceptual grades; structure remains blank"
        ),
    }
    (args.out_dir / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
