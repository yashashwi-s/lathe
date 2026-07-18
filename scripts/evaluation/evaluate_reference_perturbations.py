#!/usr/bin/env python3
"""Self-supervised metric calibration using perturbations of real reference PDFs."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import fitz
import numpy as np

from pdf_fidelity import SCORECARD_CONFIG, SCORECARD_VERSION, compare_pdfs, normalize_token


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPLIT = ROOT / "data" / "latex_benchmark_v0" / "splits" / "prompt_dev_33.csv"
DEFAULT_OUT = ROOT / "results" / "metric_calibration" / "reference_perturbations_v0_3"
NUMBER_PATTERN = re.compile(r"^[+\-−]?(?:\d+(?:[.,]\d+)*|\.\d+)(?:%|‰)?$")


@dataclass(frozen=True)
class Variant:
    family: str
    severity: float
    label: str
    expectation: str


BASE_VARIANTS = [
    Variant("identity_clone", 0, "producer_clone", "no_flags"),
    Variant("translation", 1, "translate_1pt", "no_hard_failure"),
    Variant("translation", 4, "translate_4pt", "layout_monotonic"),
    Variant("translation", 12, "translate_12pt", "layout_monotonic"),
    Variant("word_deletion", 0.01, "delete_1pct_words", "token_recall"),
    Variant("word_deletion", 0.05, "delete_5pct_words", "token_recall"),
    Variant("word_deletion", 0.15, "delete_15pct_words", "token_recall"),
    Variant("word_addition", 5, "add_5_words", "token_precision"),
    Variant("word_addition", 20, "add_20_words", "token_precision"),
    Variant("numeric_change", 1, "change_one_number", "numeric_token_mismatch"),
    Variant("obstruction", 0.15, "obstruct_15pct_width", "appearance_monotonic"),
    Variant("obstruction", 0.45, "obstruct_45pct_width", "appearance_monotonic"),
    Variant("nontext_erasure", 1, "erase_largest_vector_region", "nontext_structure"),
    Variant("table_row_erasure", 1, "erase_one_table_row", "table_structure"),
    Variant("formula_glyph_erasure", 1, "erase_one_formula_glyph", "formula_glyph_proxy"),
    Variant("crop", 0.08, "crop_bottom_8pct", "appearance_monotonic"),
    Variant("crop", 0.20, "crop_bottom_20pct", "appearance_monotonic"),
    Variant("extra_page", 1, "append_blank_page", "page_count"),
    Variant("missing_page", 1, "remove_last_page", "page_count"),
    Variant("page_reorder", 1, "swap_first_two_pages", "page_sequence"),
]


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def select_references(rows: list[dict]) -> list[dict]:
    """Choose one median-complexity clean development reference per category."""
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["category"]].append(row)
    selected = []
    priority = {"medium": 0, "low": 1, "high": 2}
    for category, candidates in sorted(grouped.items()):
        selected.append(min(
            candidates,
            key=lambda row: (priority.get(row["complexity_band"], 9),
                             abs(float(row["complexity_score"]) - 0.5), row["sample_id"]),
        ))
    return selected


def _save(document: fitz.Document, path: Path) -> None:
    document.save(path, garbage=4, deflate=True)
    document.close()


def _white_background(page: fitz.Page) -> None:
    """Make transparency deterministic across MuPDF and Poppler renderers."""
    page.draw_rect(page.rect, color=None, fill=(1, 1, 1), overlay=False)


def _clone(source: Path, output: Path, order: list[int] | None = None) -> None:
    with fitz.open(source) as reference:
        document = fitz.open()
        pages = order if order is not None else list(range(reference.page_count))
        for page_index in pages:
            document.insert_pdf(reference, from_page=page_index, to_page=page_index)
        _save(document, output)


def _eligible_words(document: fitz.Document, *, numeric: bool = False) -> list[tuple[int, tuple]]:
    words: list[tuple[int, tuple]] = []
    for page_index, page in enumerate(document):
        for word in page.get_text("words", sort=True):
            norm = normalize_token(str(word[4]))
            if numeric and NUMBER_PATTERN.fullmatch(norm):
                words.append((page_index, word))
            elif not numeric and len(norm) >= 3 and any(character.isalpha() for character in norm):
                words.append((page_index, word))
    return words


def _translation(source: Path, output: Path, shift: float) -> None:
    with fitz.open(source) as reference:
        document = fitz.open()
        for page_index, source_page in enumerate(reference):
            rect = source_page.rect
            page = document.new_page(width=rect.width, height=rect.height)
            _white_background(page)
            target = fitz.Rect(shift, shift, rect.width + shift, rect.height + shift)
            page.show_pdf_page(target, reference, page_index, keep_proportion=False)
        _save(document, output)


def _word_deletion(source: Path, output: Path, fraction: float) -> None:
    document = fitz.open(source)
    for page in document:
        _white_background(page)
    words = _eligible_words(document)
    count = max(1, int(math.ceil(len(words) * fraction)))
    selected = np.linspace(0, len(words) - 1, min(count, len(words)), dtype=int)
    pages = set()
    for index in selected:
        page_index, word = words[int(index)]
        rect = fitz.Rect(*word[:4])
        document[page_index].add_redact_annot(rect, fill=(1, 1, 1), cross_out=False)
        pages.add(page_index)
    for page_index in pages:
        document[page_index].apply_redactions(images=0, graphics=0, text=0)
    _save(document, output)


def _word_addition(source: Path, output: Path, count: int) -> None:
    document = fitz.open(source)
    page = document[0]
    _white_background(page)
    tokens = " ".join(f"extraneous{index:02d}" for index in range(count))
    rect = fitz.Rect(36, page.rect.height - 62, page.rect.width - 36, page.rect.height - 18)
    page.draw_rect(rect, color=None, fill=(1, 1, 1), overlay=True)
    page.insert_textbox(rect + (4, 4, -4, -4), tokens, fontsize=7, fontname="helv",
                        color=(0, 0, 0), overlay=True)
    _save(document, output)


def _numeric_change(source: Path, output: Path) -> bool:
    document = fitz.open(source)
    words = _eligible_words(document, numeric=True)
    if not words:
        document.close()
        return False
    page_index, word = words[len(words) // 2]
    _white_background(document[page_index])
    original = normalize_token(str(word[4]))
    replacement = "987654" if original != "987654" else "123456"
    rect = fitz.Rect(*word[:4])
    fontsize = max(5.0, min(14.0, rect.height * 0.72))
    document[page_index].add_redact_annot(
        rect,
        text=replacement,
        fontname="helv",
        fontsize=fontsize,
        fill=(1, 1, 1),
        text_color=(0, 0, 0),
        cross_out=False,
    )
    document[page_index].apply_redactions(images=0, graphics=0, text=0)
    _save(document, output)
    return True


def _obstruction(source: Path, output: Path, width_fraction: float) -> None:
    document = fitz.open(source)
    target_page = max(range(document.page_count), key=lambda index: len(document[index].get_text("words")))
    page = document[target_page]
    _white_background(page)
    words = page.get_text("words", sort=True)
    if words:
        union = fitz.Rect(*words[0][:4])
        for word in words[1:]:
            union |= fitz.Rect(*word[:4])
    else:
        union = page.rect
    width = max(36.0, union.width * width_fraction)
    height = max(28.0, min(72.0, union.height * 0.12))
    center = fitz.Point((union.x0 + union.x1) / 2, (union.y0 + union.y1) / 2)
    rect = fitz.Rect(center.x - width / 2, center.y - height / 2,
                     center.x + width / 2, center.y + height / 2) & page.rect
    page.draw_rect(rect, color=(0, 0, 0), fill=(0, 0, 0), overlay=True)
    _save(document, output)


def _nontext_erasure(source: Path, output: Path) -> bool:
    document = fitz.open(source)
    candidates = []
    for page_index, page in enumerate(document):
        drawings = page.get_drawings()
        if not drawings:
            continue
        rects = [fitz.Rect(drawing["rect"]) for drawing in drawings]
        rect = fitz.Rect(
            min(item.x0 for item in rects),
            min(item.y0 for item in rects),
            max(item.x1 for item in rects),
            max(item.y1 for item in rects),
        )
        area = rect.width * rect.height
        if area >= 100:
            candidates.append((area, page_index, rect))
    if not candidates:
        document.close()
        return False
    _, page_index, rect = max(candidates)
    page = document[page_index]
    page.add_redact_annot(rect, fill=None, cross_out=False)
    page.apply_redactions(images=0, graphics=2, text=1)
    _save(document, output)
    return True


def _table_row_erasure(source: Path, output: Path) -> bool:
    document = fitz.open(source)
    candidates = [
        (table.row_count * table.col_count, page_index, table)
        for page_index, page in enumerate(document)
        for table in page.find_tables().tables
        if table.row_count >= 2
    ]
    if not candidates:
        document.close()
        return False
    _, page_index, table = max(candidates, key=lambda item: item[0])
    bbox = fitz.Rect(table.bbox)
    row_height = bbox.height / table.row_count
    row = fitz.Rect(bbox.x0 - 1, bbox.y1 - row_height - 1, bbox.x1 + 1, bbox.y1 + 1)
    page = document[page_index]
    _white_background(page)
    page.add_redact_annot(row, fill=(1, 1, 1), cross_out=False)
    page.apply_redactions(images=0, graphics=2, text=0)
    _save(document, output)
    return True


def _formula_glyph_erasure(source: Path, output: Path) -> bool:
    document = fitz.open(source)
    markers = ("math", "cmmi", "cmsy", "cmex", "msam", "msbm", "symbol")
    glyphs = [
        (page_index, character)
        for page_index, page in enumerate(document)
        for block in page.get_text("rawdict").get("blocks", [])
        for line in block.get("lines", [])
        for span in line.get("spans", [])
        if any(marker in str(span.get("font", "")).casefold() for marker in markers)
        for character in span.get("chars", [])
        if str(character.get("c", "")).strip()
    ]
    if not glyphs:
        document.close()
        return False
    page_index, glyph = glyphs[len(glyphs) // 2]
    page = document[page_index]
    _white_background(page)
    page.add_redact_annot(fitz.Rect(glyph["bbox"]), fill=(1, 1, 1), cross_out=False)
    page.apply_redactions(images=0, graphics=0, text=0)
    _save(document, output)
    return True


def _crop(source: Path, output: Path, fraction: float) -> None:
    with fitz.open(source) as reference:
        document = fitz.open()
        for page_index, source_page in enumerate(reference):
            rect = source_page.rect
            visible_height = rect.height * (1.0 - fraction)
            page = document.new_page(width=rect.width, height=visible_height)
            _white_background(page)
            page.show_pdf_page(
                fitz.Rect(0, 0, rect.width, rect.height),
                reference,
                page_index,
                keep_proportion=False,
            )
        _save(document, output)


def _extra_page(source: Path, output: Path) -> None:
    document = fitz.open(source)
    size = document[-1].rect
    _white_background(document.new_page(width=size.width, height=size.height))
    _save(document, output)


def build_variant(source: Path, output: Path, variant: Variant) -> bool:
    with fitz.open(source) as document:
        page_count = document.page_count
    if variant.family == "identity_clone":
        _clone(source, output)
    elif variant.family == "translation":
        _translation(source, output, variant.severity)
    elif variant.family == "word_deletion":
        _word_deletion(source, output, variant.severity)
    elif variant.family == "word_addition":
        _word_addition(source, output, int(variant.severity))
    elif variant.family == "numeric_change":
        return _numeric_change(source, output)
    elif variant.family == "obstruction":
        _obstruction(source, output, variant.severity)
    elif variant.family == "nontext_erasure":
        return _nontext_erasure(source, output)
    elif variant.family == "table_row_erasure":
        return _table_row_erasure(source, output)
    elif variant.family == "formula_glyph_erasure":
        return _formula_glyph_erasure(source, output)
    elif variant.family == "crop":
        _crop(source, output, variant.severity)
    elif variant.family == "extra_page":
        _extra_page(source, output)
    elif variant.family == "missing_page":
        if page_count < 2:
            return False
        _clone(source, output, list(range(page_count - 1)))
    elif variant.family == "page_reorder":
        if page_count < 2:
            return False
        _clone(source, output, [1, 0, *range(2, page_count)])
    else:
        raise ValueError(variant.family)
    return True


def monotonic(values: list[float], tolerance: float = 0.01) -> bool:
    return all(later <= earlier + tolerance for earlier, later in zip(values, values[1:]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--limit-samples", type=int, default=0)
    parser.add_argument("--keep-examples-dir", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected = select_references(read_csv(args.split))
    if args.limit_samples:
        selected = selected[:args.limit_samples]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if args.keep_examples_dir:
        args.keep_examples_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="lathe_reference_perturbations_") as directory:
        work = Path(directory)
        for sample_index, sample in enumerate(selected, start=1):
            sample_id = sample["sample_id"]
            reference = ROOT / sample["reference_pdf"]
            print(f"[{sample_index:02d}/{len(selected):02d}] {sample_id}", flush=True)
            for variant_index, variant in enumerate(BASE_VARIANTS):
                candidate = work / f"{sample_id}_{variant_index:02d}.pdf"
                if not build_variant(reference, candidate, variant):
                    continue
                if args.keep_examples_dir and sample_index == 1:
                    _clone(candidate, args.keep_examples_dir / f"{variant.label}.pdf")
                result, *_ = compare_pdfs(reference, candidate)
                scorecard = result["scorecard"]
                axes = scorecard["axes"]
                tables = scorecard["specialized_diagnostics"]["tables"]
                formula = scorecard["specialized_diagnostics"]["formula_glyph_proxy"]
                nontext = axes["appearance_proxy"]["nontext"]
                rows.append({
                    "sample_id": sample_id,
                    "category": sample["category"],
                    "complexity_band": sample["complexity_band"],
                    "reference_pages": result["reference_pages"],
                    "family": variant.family,
                    "severity": variant.severity,
                    "variant": variant.label,
                    "expectation": variant.expectation,
                    "status": scorecard["status"],
                    "failed_gates": ";".join(scorecard["failed_gates"]),
                    "review_flags": ";".join(scorecard["review_flags"]),
                    "diagnostic_flags": ";".join(scorecard["diagnostic_flags"]),
                    "content": axes["content"]["score"],
                    "token_precision": axes["content"]["token_precision"],
                    "token_recall": axes["content"]["token_recall"],
                    "numeric_exact": axes["content"]["numeric_token_multiset"]["exact"],
                    "layout": axes["layout"]["score"],
                    "layout_coverage_min": axes["layout"]["correspondence_evidence"][
                        "minimum_coverage"
                    ],
                    "typography": axes["typography"]["score"],
                    "appearance_proxy": axes["appearance_proxy"]["score"],
                    "appearance_local_q10": axes["appearance_proxy"]["local_worst_region"],
                    "nontext_applicable": nontext["applicable"],
                    "nontext_score": nontext["score"],
                    "pagination": axes["pagination"]["score"],
                    "table_applicable": tables["applicable"],
                    "table_count_exact": tables.get("count_exact", ""),
                    "table_row_exact_rate": tables.get("row_count_exact_rate", ""),
                    "table_column_exact_rate": tables.get("column_count_exact_rate", ""),
                    "formula_applicable": formula["applicable"],
                    "formula_character_recall": formula.get("character_recall", ""),
                    "formula_character_f1": formula.get("character_f1", ""),
                })

    csv_path = args.out_dir / "reference_perturbation_scores.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest_fields = ["sample_id", "category", "complexity_band", "reference_pdf"]
    with (args.out_dir / "selection_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=manifest_fields)
        writer.writeheader()
        writer.writerows({key: row[key] for key in manifest_fields} for row in selected)
    (args.out_dir / "scorecard_config.json").write_text(
        json.dumps(SCORECARD_CONFIG, indent=2) + "\n", encoding="utf-8"
    )

    by_family: dict[str, list[dict]] = defaultdict(list)
    by_sample_family: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        by_family[row["family"]].append(row)
        by_sample_family[(row["sample_id"], row["family"])].append(row)
    identity = by_family["identity_clone"]
    identity_by_sample = {row["sample_id"]: row for row in identity}
    detection = {
        "identity clone has no flags": [
            not row["failed_gates"] and not row["review_flags"] for row in identity
        ],
        "1pt translation has no hard failure": [
            not row["failed_gates"] for row in by_family["translation"] if float(row["severity"]) == 1
        ],
        "15pct deletion fails token recall": [
            "token_recall" in row["failed_gates"]
            for row in by_family["word_deletion"] if math.isclose(float(row["severity"]), 0.15)
        ],
        "20-word addition lowers precision": [
            float(row["token_precision"]) < 1.0
            for row in by_family["word_addition"] if float(row["severity"]) == 20
        ],
        "numeric change raises diagnostic": [
            "numeric_token_mismatch" in row["diagnostic_flags"] for row in by_family["numeric_change"]
        ],
        "extra page fails page count": [
            "page_count" in row["failed_gates"] for row in by_family["extra_page"]
        ],
        "missing page fails page count": [
            "page_count" in row["failed_gates"] for row in by_family["missing_page"]
        ],
        "reorder lowers page sequence": [
            float(row["pagination"]) < SCORECARD_CONFIG["provisional_review_triggers"]["page_sequence_min"]
            for row in by_family["page_reorder"]
        ],
        "severe obstruction raises structure or appearance signal": [
            "localized_appearance_failure" in row["diagnostic_flags"]
            or "nontext_structure_mismatch" in row["diagnostic_flags"]
            or "table_structure_mismatch" in row["review_flags"]
            for row in by_family["obstruction"] if math.isclose(float(row["severity"]), 0.45)
        ],
        "nontext erasure lowers nontext score": [
            float(row["nontext_score"])
            < float(identity_by_sample[row["sample_id"]]["nontext_score"])
            for row in by_family["nontext_erasure"]
            if row["nontext_score"] not in ("", None)
            and identity_by_sample[row["sample_id"]]["nontext_score"] not in ("", None)
        ],
        "table row erasure changes extracted topology": [
            (str(row["table_count_exact"]).casefold() == "false")
            or (row["table_row_exact_rate"] not in ("", None)
                and float(row["table_row_exact_rate"]) < 1.0)
            for row in by_family["table_row_erasure"]
        ],
        "formula glyph erasure lowers glyph recall": [
            row["formula_character_recall"] not in ("", None)
            and float(row["formula_character_recall"])
            < float(identity_by_sample[row["sample_id"]]["formula_character_recall"])
            for row in by_family["formula_glyph_erasure"]
        ],
    }
    target_axis = {
        "translation": "layout",
        "word_deletion": "token_recall",
        "word_addition": "token_precision",
        "obstruction": "appearance_local_q10",
        "crop": "appearance_proxy",
    }
    monotonic_checks: list[tuple[str, str, bool, list[float]]] = []
    for (sample_id, family), family_rows in sorted(by_sample_family.items()):
        if family not in target_axis:
            continue
        axis = target_axis[family]
        ordered = sorted(family_rows, key=lambda row: float(row["severity"]))
        values = [float(identity_by_sample[sample_id][axis]), *[float(row[axis]) for row in ordered]]
        monotonic_checks.append((sample_id, family, monotonic(values), values))

    lines = [
        f"# Real-reference perturbation study — {SCORECARD_VERSION}",
        "",
        "This self-supervised calibration study applies source-known perturbations to real benchmark "
        "reference PDFs. It validates invariance and detector behavior without human preference labels.",
        "",
        f"References: {len(selected)} (one per benchmark category). Comparisons: {len(rows)}.",
        "",
        "## Detector checks",
        "",
        "| Invariant / expected detector | Hits | Total | Rate |",
        "|---|---:|---:|---:|",
    ]
    for label, outcomes in detection.items():
        hits = sum(outcomes)
        lines.append(f"| {label} | {hits} | {len(outcomes)} | {100 * hits / max(1, len(outcomes)):.1f}% |")
    lines.extend([
        "",
        "## Monotonic response",
        "",
        "| Family | Passing sample series | Total | Rate |",
        "|---|---:|---:|---:|",
    ])
    for family in target_axis:
        checks = [check for check in monotonic_checks if check[1] == family]
        lines.append(
            f"| `{family}` | {sum(check[2] for check in checks)} | {len(checks)} | "
            f"{100 * sum(check[2] for check in checks) / max(1, len(checks)):.1f}% |"
        )
    failures = [check for check in monotonic_checks if not check[2]]
    lines.extend([
        "",
        "## Interpretation boundary",
        "",
        "Known corruptions can validate sensitivity, monotonicity, and exact structural gates. They cannot "
        "define aesthetic preference or an acceptable real conversion threshold. Therefore this study can "
        "justify detector revisions and abstention rules, but not a fitted overall score.",
        "",
        f"Non-monotonic series requiring inspection: {len(failures)}.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "mamba run -n lathe python scripts/evaluation/evaluate_reference_perturbations.py",
        "```",
        "",
        f"Raw results: `{csv_path.relative_to(ROOT) if csv_path.is_relative_to(ROOT) else csv_path}`.",
    ])
    (args.out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"comparisons={len(rows)}")
    print(f"monotonic={sum(check[2] for check in monotonic_checks)}/{len(monotonic_checks)}")
    print(f"summary={args.out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
