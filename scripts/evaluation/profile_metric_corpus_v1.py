#!/usr/bin/env python3
"""Profile the canonical 157-reference corpus for metric research.

This script does not score PDF fidelity. It records the evidence needed to
design and validate a scorer: reference structure, PDF observables,
augmentation applicability, provenance gaps, the frozen metric-research split,
and coverage/canvas properties of the stored 157-sample Gemini run.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Iterable

import fitz


ROOT = Path(__file__).resolve().parents[2]
ACCEPTED = ROOT / "data" / "latex_benchmark_v0" / "accepted_manifest.csv"
AI_MANIFEST = (
    ROOT / "results" / "ai_latex_to_typst" / "documents"
    / "full_157_ai_engine_comparison_manifest.csv"
)
AI_ROOT = (
    ROOT / "results" / "ai_latex_to_typst" / "openrouter"
    / "google_gemini-3.1-flash-lite"
)
OUT_DIR = ROOT / "results" / "metric_research_v1"
PARTITION_SEED = 20260715
CANONICAL_PARTITION_TARGETS = {
    "metric_dev": 80,
    "metric_validation": 39,
    "metric_test": 38,
}
PARTITION_ORDER = tuple(CANONICAL_PARTITION_TARGETS)

LETTER = (612.0, 792.0)
A4 = (595.276, 841.89)
SIZE_TOLERANCE_PT = 1.0

SEMANTIC_TABLE_CATEGORIES = {"05_tables_simple", "06_tables_moderate"}
SEMANTIC_FIGURE_CATEGORIES = {"07_figures_captions"}

SOURCE_PATTERNS = {
    "has_inline_math": re.compile(r"(?<!\\)\$(?!\$)|\\\(|\\begin\{math\}"),
    "has_display_math": re.compile(
        r"\$\$|\\\[|\\begin\{(?:equation\*?|align\*?|gather\*?|"
        r"multline\*?|displaymath|split|cases)\}"
    ),
    "has_table_like_environment": re.compile(
        r"\\begin\{(?:table\*?|tabular\*?|tabularx|longtable|array)\}"
    ),
    "has_figure_source": re.compile(
        r"\\begin\{figure\*?\}|\\includegraphics|"
        r"\\begin\{(?:tikzpicture|picture|pspicture)\}"
    ),
    "has_list_source": re.compile(r"\\begin\{(?:itemize|enumerate|description)\}"),
    "has_algorithm_source": re.compile(
        r"\\begin\{(?:algorithm\*?|algorithmic|algorithm2e|pseudocode)\}|"
        r"\\(?:KwData|KwResult|SetKw|REQUIRE|ENSURE)\b"
    ),
    "has_crossref_source": re.compile(
        r"\\(?:ref|eqref|pageref|cite|citep|citet|label|bibitem)\b"
    ),
}

EXPLICIT_LICENSE_PATTERN = re.compile(
    r"LaTeX Project Public License|SPDX-License-Identifier|"
    r"Creative Commons|distributed and/or modified under the",
    re.IGNORECASE,
)
EXPECTED_PROVENANCE_FIELDS = {
    "license",
    "source_url",
    "authors",
    "retrieval_timestamp",
    "transformation_record",
}

AI_RUNS = {
    ("prompt_dev", "v0"): AI_ROOT / "prompt_v0",
    ("prompt_dev", "v1_targeted_retry"): AI_ROOT / "prompt_v1_v0_failures",
    ("prompt_dev", "v3_rescue"): AI_ROOT / "prompt_v3_prompt_dev_failures",
    ("heldout", "v1"): AI_ROOT / "prompt_v1_heldout_clean",
    ("heldout", "v2"): AI_ROOT / "prompt_v2_heldout_v1_failures",
    ("heldout", "v3"): AI_ROOT / "prompt_v3_heldout_v2_failures",
}

# One comparison pair is reference versus one seeded candidate variant.
AUGMENTATION_FAMILIES = (
    ("identity_lossless_roundtrip", "all", 1, "invariant"),
    ("canvas_translation", "all", 12, "layout"),
    ("uniform_scale", "all", 6, "layout"),
    ("largest_block_displacement", "all", 12, "layout"),
    ("text_span_deletion", "all", 3, "content"),
    ("lexical_numeric_substitution", "all", 6, "content"),
    ("typography_reflow", "all", 12, "typography"),
    ("edge_crop_local_occlusion", "all", 15, "content+appearance"),
    ("render_only_degradation", "all", 9, "appearance_only"),
    ("fixed_compound_defects", "all", 6, "multiple"),
    ("page_sequence_and_count", "multipage", None, "pagination"),
    ("display_math_structure", "display_math", 12, "content+layout"),
    ("inline_math_structure", "inline_math", 6, "content+typography"),
    ("semantic_table_structure", "semantic_table", 15, "content+layout"),
    ("figure_and_caption", "semantic_figure", 15, "content+layout"),
    ("list_structure", "list", 12, "content+layout"),
    ("cross_reference_semantics", "crossref", 9, "content"),
    ("algorithm_structure", "algorithm", 12, "content+layout"),
    ("form_geometry", "form", 9, "layout"),
    ("prose_hierarchy", "prose", 9, "content+layout"),
    ("compact_paper_flow", "compact", 9, "layout+pagination"),
)
UNIVERSAL_PAIR_COUNT = sum(
    variants for _name, scope, variants, _axis in AUGMENTATION_FAMILIES
    if scope == "all" and variants is not None
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED)
    parser.add_argument("--ai-manifest", type=Path, default=AI_MANIFEST)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--seed", type=int, default=PARTITION_SEED)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _stable_hash(seed: int, *parts: object) -> str:
    payload = "\x1f".join([str(seed), *(str(part) for part in parts)])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def strip_latex_comments(source: str) -> str:
    """Remove comments while preserving escaped percent signs."""
    output = []
    for line in source.splitlines():
        comment_at = None
        for index, character in enumerate(line):
            if character != "%":
                continue
            slash_count = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                slash_count += 1
                cursor -= 1
            if slash_count % 2 == 0:
                comment_at = index
                break
        output.append(line if comment_at is None else line[:comment_at])
    return "\n".join(output)


def parse_source_signals(source: str, category: str) -> dict[str, bool]:
    """Return source-derived semantic applicability signals."""
    visible_source = strip_latex_comments(source)
    signals = {
        name: bool(pattern.search(visible_source))
        for name, pattern in SOURCE_PATTERNS.items()
    }
    signals.update({
        "has_math_any": signals["has_inline_math"] or signals["has_display_math"],
        "has_semantic_table": category in SEMANTIC_TABLE_CATEGORIES,
        "has_semantic_figure": category in SEMANTIC_FIGURE_CATEGORIES,
        "has_form_semantics": category == "11_forms_cv_letters",
        "has_prose_semantics": category == "01_prose_sections",
        "has_compact_paper_semantics": category == "10_compact_papers",
    })
    return signals


def _partition_targets(total: int) -> dict[str, int]:
    if total == sum(CANONICAL_PARTITION_TARGETS.values()):
        return dict(CANONICAL_PARTITION_TARGETS)
    fractions = {"metric_dev": 0.51, "metric_validation": 0.25, "metric_test": 0.24}
    ideals = {name: total * fraction for name, fraction in fractions.items()}
    targets = {name: math.floor(value) for name, value in ideals.items()}
    for name in sorted(
        fractions, key=lambda item: (ideals[item] - targets[item], item), reverse=True
    )[: total - sum(targets.values())]:
        targets[name] += 1
    return targets


def _category_quotas(rows: list[dict[str, str]], targets: dict[str, int],
                     seed: int) -> dict[str, dict[str, int]]:
    by_category = Counter(row["category"] for row in rows)
    total = len(rows)
    quotas: dict[str, dict[str, int]] = {}
    ideals: dict[str, dict[str, float]] = {}
    for category, count in sorted(by_category.items()):
        ideals[category] = {
            partition: count * targets[partition] / total for partition in PARTITION_ORDER
        }
        quota = {partition: math.floor(ideals[category][partition]) for partition in PARTITION_ORDER}
        missing = count - sum(quota.values())
        ranked = sorted(
            PARTITION_ORDER,
            key=lambda partition: (
                ideals[category][partition] - quota[partition],
                _stable_hash(seed, category, partition),
            ),
            reverse=True,
        )
        for partition in ranked[:missing]:
            quota[partition] += 1
        quotas[category] = quota

    totals = Counter()
    for quota in quotas.values():
        totals.update(quota)
    while any(totals[name] != targets[name] for name in PARTITION_ORDER):
        over = [name for name in PARTITION_ORDER if totals[name] > targets[name]]
        under = [name for name in PARTITION_ORDER if totals[name] < targets[name]]
        candidates = []
        for source_partition in over:
            for destination_partition in under:
                for category, quota in quotas.items():
                    if quota[source_partition] <= 0:
                        continue
                    old_cost = (
                        (quota[source_partition] - ideals[category][source_partition]) ** 2
                        + (quota[destination_partition] - ideals[category][destination_partition]) ** 2
                    )
                    new_cost = (
                        (quota[source_partition] - 1 - ideals[category][source_partition]) ** 2
                        + (quota[destination_partition] + 1 - ideals[category][destination_partition]) ** 2
                    )
                    candidates.append((
                        new_cost - old_cost,
                        _stable_hash(seed, "quota-adjust", category,
                                     source_partition, destination_partition),
                        category,
                        source_partition,
                        destination_partition,
                    ))
        if not candidates:
            raise RuntimeError("could not reconcile metric partition quotas")
        _cost, _tie, category, source_partition, destination_partition = min(candidates)
        quotas[category][source_partition] -= 1
        quotas[category][destination_partition] += 1
        totals[source_partition] -= 1
        totals[destination_partition] += 1
    return quotas


def _interleaved_category_rows(rows: list[dict[str, str]], seed: int) -> list[dict[str, str]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (row["page_count"], row["source_family"], row["source_dataset"])
        groups[key].append(row)
    for key, values in groups.items():
        values.sort(key=lambda row: _stable_hash(seed, "row", key, row["sample_id"]))
    keys = sorted(groups, key=lambda key: _stable_hash(seed, "stratum", key))
    ordered = []
    round_index = 0
    while keys:
        offset = round_index % len(keys)
        keys = keys[offset:] + keys[:offset]
        for key in list(keys):
            if groups[key]:
                ordered.append(groups[key].pop(0))
        keys = [key for key in keys if groups[key]]
        round_index += 1
    return ordered


def assign_metric_partitions(rows: list[dict[str, str]],
                             seed: int = PARTITION_SEED) -> dict[str, str]:
    """Assign fixed category quotas and interleave page/source strata."""
    if not rows:
        return {}
    sample_ids = [row["sample_id"] for row in rows]
    if len(sample_ids) != len(set(sample_ids)):
        raise ValueError("sample IDs must be unique for metric partitioning")
    targets = _partition_targets(len(rows))
    quotas = _category_quotas(rows, targets, seed)
    by_category: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row)

    assignments = {}
    for category, values in sorted(by_category.items()):
        ordered = _interleaved_category_rows(values, seed)
        assigned = Counter()
        for position, row in enumerate(ordered):
            available = [
                partition for partition in PARTITION_ORDER
                if assigned[partition] < quotas[category][partition]
            ]
            partition = max(
                available,
                key=lambda item: (
                    quotas[category][item] * (position + 1) / len(ordered) - assigned[item],
                    _stable_hash(seed, "partition", row["sample_id"], item),
                ),
            )
            assignments[row["sample_id"]] = partition
            assigned[partition] += 1

    actual = Counter(assignments.values())
    if any(actual[name] != targets[name] for name in PARTITION_ORDER):
        raise AssertionError(f"partition counts drifted: {dict(actual)} != {targets}")
    return assignments


def _close_size(first: tuple[float, float], second: tuple[float, float]) -> bool:
    return all(abs(left - right) <= SIZE_TOLERANCE_PT for left, right in zip(first, second))


def classify_page_size(size: tuple[float, float]) -> str:
    if _close_size(size, LETTER):
        return "letter"
    if _close_size(size, A4):
        return "a4"
    if _close_size(size, tuple(reversed(LETTER))):
        return "letter_landscape"
    if _close_size(size, tuple(reversed(A4))):
        return "a4_landscape"
    return "other"


def _document_canvas(page_sizes: list[tuple[float, float]]) -> str:
    classes = {classify_page_size(size) for size in page_sizes}
    return next(iter(classes)) if len(classes) == 1 else "mixed"


def _page_sizes_json(page_sizes: list[tuple[float, float]]) -> str:
    return json.dumps([[round(width, 3), round(height, 3)] for width, height in page_sizes],
                      separators=(",", ":"))


def profile_pdf(path: Path) -> dict:
    page_sizes = []
    word_count = 0
    drawing_count = 0
    image_count = 0
    table_count = 0
    with fitz.open(path) as document:
        for page in document:
            page_sizes.append((float(page.rect.width), float(page.rect.height)))
            word_count += len(page.get_text("words"))
            drawing_count += len(page.get_drawings())
            image_count += len(page.get_images(full=True))
            table_count += len(page.find_tables().tables)
    return {
        "page_count": len(page_sizes),
        "page_sizes": page_sizes,
        "page_sizes_json": _page_sizes_json(page_sizes),
        "canvas": _document_canvas(page_sizes),
        "word_count": word_count,
        "drawing_count": drawing_count,
        "image_count": image_count,
        "table_detector_count": table_count,
    }


def _as_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def _display_path(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def selected_ai_path(row: dict[str, str]) -> Path | None:
    run_dir = AI_RUNS.get((row.get("source_split", ""), row.get("selected_ai_stage", "")))
    if run_dir is None:
        return None
    return run_dir / "samples" / row["sample_id"] / "output.pdf"


def _same_size_sequence(first: list[tuple[float, float]],
                        second: list[tuple[float, float]]) -> bool:
    return len(first) == len(second) and all(
        _close_size(left, right) for left, right in zip(first, second)
    )


def _license_fields(provenance: dict) -> list[str]:
    return sorted(key for key in provenance if "licen" in key.casefold())


def build_profiles(accepted_rows: list[dict[str, str]], ai_rows: list[dict[str, str]],
                   seed: int) -> tuple[list[dict], list[dict]]:
    if len(accepted_rows) != 157:
        raise ValueError(f"expected 157 accepted rows, found {len(accepted_rows)}")
    ai_by_id = {row["sample_id"]: row for row in ai_rows}
    if len(ai_by_id) != len(ai_rows):
        raise ValueError("AI manifest contains duplicate sample IDs")
    accepted_ids = {row["sample_id"] for row in accepted_rows}
    if set(ai_by_id) != accepted_ids:
        raise ValueError("AI manifest does not cover the accepted corpus exactly")
    partitions = assign_metric_partitions(accepted_rows, seed)

    profiles = []
    applicability = []
    for accepted in accepted_rows:
        sample_id = accepted["sample_id"]
        sample_dir = ROOT / accepted["sample_dir"]
        source_path = sample_dir / "main.tex"
        reference_path = sample_dir / "reference.pdf"
        provenance_path = sample_dir / "provenance.json"
        source = source_path.read_text(encoding="utf-8", errors="replace")
        signals = parse_source_signals(source, accepted["category"])
        reference = profile_pdf(reference_path)
        provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
        provenance_license_fields = _license_fields(provenance)
        provenance_gaps = sorted(EXPECTED_PROVENANCE_FIELDS - set(provenance))

        ai_row = ai_by_id[sample_id]
        candidate_path = selected_ai_path(ai_row)
        candidate_exists = bool(candidate_path and candidate_path.exists())
        candidate = profile_pdf(candidate_path) if candidate_exists else None
        first_canvas_match = bool(
            candidate and reference["page_sizes"] and candidate["page_sizes"]
            and _close_size(reference["page_sizes"][0], candidate["page_sizes"][0])
        )
        sequence_match = bool(
            candidate and _same_size_sequence(reference["page_sizes"], candidate["page_sizes"])
        )
        page_count_match = bool(
            candidate and reference["page_count"] == candidate["page_count"]
        )

        profile = {
            "sample_id": sample_id,
            "category": accepted["category"],
            "metric_partition": partitions[sample_id],
            "metric_partition_seed": seed,
            "prompt_split": ai_row["source_split"],
            "source_family": accepted["source_family"],
            "source_dataset": accepted["source_dataset"],
            "source_ids": accepted["source_ids"],
            "source_chars": accepted["source_chars"],
            "nonblank_lines": accepted["nonblank_lines"],
            "reference_pdf": _display_path(reference_path),
            "reference_pages": reference["page_count"],
            "reference_page_sizes_pt": reference["page_sizes_json"],
            "reference_canvas": reference["canvas"],
            "reference_word_count": reference["word_count"],
            "reference_drawing_count": reference["drawing_count"],
            "reference_image_count": reference["image_count"],
            "reference_table_detector_count": reference["table_detector_count"],
            **signals,
            "provenance_path": _display_path(provenance_path),
            "provenance_source_id_field": (
                "source_ids" if "source_ids" in provenance else
                "source_id" if "source_id" in provenance else "missing"
            ),
            "provenance_license_fields": ";".join(provenance_license_fields),
            "provenance_has_license_field": bool(provenance_license_fields),
            "source_has_explicit_license_text": bool(EXPLICIT_LICENSE_PATTERN.search(source)),
            "provenance_missing_research_fields": ";".join(provenance_gaps),
            "ai_model_id": "google/gemini-3.1-flash-lite",
            "ai_selected_stage": ai_row["selected_ai_stage"],
            "ai_manifest_final_compiled": _as_bool(ai_row["ai_final_compiled"]),
            "ai_candidate_pdf": _display_path(candidate_path),
            "ai_candidate_exists": candidate_exists,
            "ai_candidate_pages": candidate["page_count"] if candidate else "",
            "ai_candidate_page_sizes_pt": candidate["page_sizes_json"] if candidate else "",
            "ai_candidate_canvas": candidate["canvas"] if candidate else "missing",
            "ai_page_count_match_measured": page_count_match if candidate else "",
            "ai_first_page_canvas_match": first_canvas_match if candidate else "",
            "ai_page_size_sequence_match": sequence_match if candidate else "",
            "ai_canvas_mismatch": (not first_canvas_match) if candidate else "",
        }
        profiles.append(profile)

        page_pairs = 4 + 2 * reference["page_count"] if reference["page_count"] > 1 else 0
        counts = {
            "universal": UNIVERSAL_PAIR_COUNT,
            "multipage": page_pairs,
            "display_math": 12 if signals["has_display_math"] else 0,
            "inline_math": 6 if signals["has_inline_math"] else 0,
            "semantic_table": 15 if signals["has_semantic_table"] else 0,
            "semantic_figure": 15 if signals["has_semantic_figure"] else 0,
            "list": 12 if signals["has_list_source"] else 0,
            "crossref": 9 if signals["has_crossref_source"] else 0,
            "algorithm": 12 if signals["has_algorithm_source"] else 0,
            "form": 9 if signals["has_form_semantics"] else 0,
            "prose": 9 if signals["has_prose_semantics"] else 0,
            "compact": 9 if signals["has_compact_paper_semantics"] else 0,
        }
        applicability.append({
            "sample_id": sample_id,
            "category": accepted["category"],
            "metric_partition": partitions[sample_id],
            "reference_pages": reference["page_count"],
            "apply_universal": True,
            "apply_multipage": reference["page_count"] > 1,
            "apply_display_math": signals["has_display_math"],
            "apply_inline_math": signals["has_inline_math"],
            "apply_semantic_table": signals["has_semantic_table"],
            "apply_semantic_figure": signals["has_semantic_figure"],
            "apply_list": signals["has_list_source"],
            "apply_crossref": signals["has_crossref_source"],
            "apply_algorithm": signals["has_algorithm_source"],
            "apply_form": signals["has_form_semantics"],
            "apply_prose": signals["has_prose_semantics"],
            "apply_compact": signals["has_compact_paper_semantics"],
            "pairs_universal": counts["universal"],
            "pairs_multipage": counts["multipage"],
            "pairs_display_math": counts["display_math"],
            "pairs_inline_math": counts["inline_math"],
            "pairs_semantic_table": counts["semantic_table"],
            "pairs_semantic_figure": counts["semantic_figure"],
            "pairs_list": counts["list"],
            "pairs_crossref": counts["crossref"],
            "pairs_algorithm": counts["algorithm"],
            "pairs_form": counts["form"],
            "pairs_prose": counts["prose"],
            "pairs_compact": counts["compact"],
            "estimated_total_pairs": sum(counts.values()),
            "manual_blind_bundle_pairs": 5,
        })
    return profiles, applicability


def _counts(rows: Iterable[dict], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[field]) for row in rows).items()))


def _partition_crosstab(profiles: list[dict], field: str) -> dict[str, dict[str, int]]:
    values: dict[str, Counter] = defaultdict(Counter)
    for row in profiles:
        values[str(row[field])][row["metric_partition"]] += 1
    return {
        key: {partition: counter.get(partition, 0) for partition in PARTITION_ORDER}
        for key, counter in sorted(values.items())
    }


def build_summary(profiles: list[dict], applicability: list[dict], accepted_fields: list[str],
                  seed: int, accepted_path: Path = ACCEPTED,
                  ai_manifest_path: Path = AI_MANIFEST) -> dict:
    signal_fields = [
        "has_inline_math", "has_display_math", "has_math_any",
        "has_table_like_environment", "has_semantic_table", "has_figure_source",
        "has_semantic_figure", "has_list_source", "has_algorithm_source",
        "has_crossref_source", "has_form_semantics", "has_prose_semantics",
        "has_compact_paper_semantics",
    ]
    pair_fields = [field for field in applicability[0] if field.startswith("pairs_")]
    ai_available = [row for row in profiles if row["ai_candidate_exists"]]
    word_counts = [int(row["reference_word_count"]) for row in profiles]
    augmentation_totals = {
        field.removeprefix("pairs_"): sum(int(row[field]) for row in applicability)
        for field in pair_fields
    }
    family_totals = []
    for name, scope, variants, expected_axis in AUGMENTATION_FAMILIES:
        if scope == "all":
            pairs = len(profiles) * int(variants)
        elif scope == "multipage":
            pairs = augmentation_totals["multipage"]
        else:
            pairs = sum(
                int(row[f"pairs_{scope}"]) for row in applicability
            )
        family_totals.append({
            "family": name,
            "scope": scope,
            "variants_per_applicable_document": variants if variants is not None else "4+2*pages",
            "expected_axis": expected_axis,
            "pairs": pairs,
        })

    source_id_fields = Counter(row["provenance_source_id_field"] for row in profiles)
    return {
        "schema_version": "metric_corpus_profile_v1",
        "inputs": {
            "accepted_manifest": _display_path(accepted_path),
            "ai_manifest": _display_path(ai_manifest_path),
        },
        "corpus": {
            "documents": len(profiles),
            "reference_pages": sum(int(row["reference_pages"]) for row in profiles),
            "categories": _counts(profiles, "category"),
            "page_count_distribution": _counts(profiles, "reference_pages"),
            "reference_canvas_documents": _counts(profiles, "reference_canvas"),
            "source_families": _counts(profiles, "source_family"),
            "source_datasets": _counts(profiles, "source_dataset"),
            "reference_word_count": {
                "min": min(word_counts),
                "median": median(word_counts),
                "max": max(word_counts),
            },
            "source_signal_document_counts": {
                field: sum(bool(row[field]) for row in profiles) for field in signal_fields
            },
            "pdf_table_detector_documents": sum(
                int(row["reference_table_detector_count"]) > 0 for row in profiles
            ),
        },
        "metric_partitions": {
            "seed": seed,
            "method": (
                "exact category quotas with deterministic page-count/source-dataset "
                "interleaving; independent of the prompt-development split"
            ),
            "counts": _counts(profiles, "metric_partition"),
            "by_category": _partition_crosstab(profiles, "category"),
            "by_page_count": _partition_crosstab(profiles, "reference_pages"),
            "by_source_dataset": _partition_crosstab(profiles, "source_dataset"),
            "prompt_split_cross_tab": _partition_crosstab(profiles, "prompt_split"),
        },
        "stored_ai_coverage": {
            "model_id": "google/gemini-3.1-flash-lite",
            "manifest_rows": len(profiles),
            "manifest_final_compiled": sum(bool(row["ai_manifest_final_compiled"]) for row in profiles),
            "physical_candidate_pdfs": len(ai_available),
            "missing_candidates": [row["sample_id"] for row in profiles if not row["ai_candidate_exists"]],
            "page_count_matches": sum(row["ai_page_count_match_measured"] is True for row in ai_available),
            "page_count_mismatches": sum(row["ai_page_count_match_measured"] is False for row in ai_available),
            "candidate_canvas_documents": _counts(ai_available, "ai_candidate_canvas"),
            "first_page_canvas_matches": sum(row["ai_first_page_canvas_match"] is True for row in ai_available),
            "first_page_canvas_mismatches": sum(row["ai_canvas_mismatch"] is True for row in ai_available),
            "page_size_sequence_matches": sum(row["ai_page_size_sequence_match"] is True for row in ai_available),
            "selected_stages": _counts(profiles, "ai_selected_stage"),
        },
        "provenance_and_license": {
            "accepted_manifest_fields": accepted_fields,
            "accepted_manifest_license_fields": [
                field for field in accepted_fields if "licen" in field.casefold()
            ],
            "provenance_license_field_documents": sum(
                bool(row["provenance_has_license_field"]) for row in profiles
            ),
            "source_explicit_license_text_documents": sum(
                bool(row["source_has_explicit_license_text"]) for row in profiles
            ),
            "provenance_source_id_fields": dict(sorted(source_id_fields.items())),
            "expected_missing_research_fields": sorted(EXPECTED_PROVENANCE_FIELDS),
            "redistribution_status": "not established by canonical metadata",
        },
        "augmentation_matrix": {
            "pair_unit": "one reference PDF versus one seeded candidate variant",
            "family_totals": family_totals,
            "estimated_total_pairs": sum(row["estimated_total_pairs"] for row in applicability),
            "render_only_pairs": 9 * len(profiles),
            "manual_blind_bundle_pairs": sum(row["manual_blind_bundle_pairs"] for row in applicability),
            "manual_non_null_pairs": 4 * len(profiles),
        },
        "interpretation_warnings": [
            "The PDF table detector is evidence, not the semantic table applicability label.",
            "Canvas mismatch is reported separately from pagination and within-page layout.",
            "Render-only degradation must not calibrate extraction-based content metrics.",
            "Prompt and metric partitions serve different purposes and must not be conflated.",
            "Canonical metadata does not establish redistribution rights for the corpus.",
        ],
    }


def _markdown_table(headers: list[str], rows: Iterable[Iterable[object]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return lines


def summary_markdown(summary: dict) -> str:
    corpus = summary["corpus"]
    partitions = summary["metric_partitions"]
    ai = summary["stored_ai_coverage"]
    provenance = summary["provenance_and_license"]
    augmentation = summary["augmentation_matrix"]
    lines = [
        "# Metric corpus profile v1",
        "",
        "This is a corpus and evidence profile, not a PDF-fidelity score.",
        "",
        "## Canonical corpus",
        "",
        f"- Documents: {corpus['documents']}",
        f"- Reference pages: {corpus['reference_pages']}",
        f"- Page counts: {corpus['page_count_distribution']}",
        f"- Reference canvases: {corpus['reference_canvas_documents']}",
        f"- Word counts (min / median / max): "
        f"{corpus['reference_word_count']['min']} / {corpus['reference_word_count']['median']} / "
        f"{corpus['reference_word_count']['max']}",
        "",
        *(_markdown_table(
            ["Category", "Documents"],
            corpus["categories"].items(),
        )),
        "",
        "## Source and PDF signals",
        "",
        *(_markdown_table(
            ["Signal", "Documents"],
            corpus["source_signal_document_counts"].items(),
        )),
        "",
        f"PyMuPDF's table detector finds tables in {corpus['pdf_table_detector_documents']} "
        "documents. Semantic table applicability comes from the 36 documents in the two "
        "canonical table categories; detector misses must remain visible.",
        "",
        "## Frozen metric-research partitions",
        "",
        f"Seed: `{partitions['seed']}`. {partitions['method']}.",
        "",
        *(_markdown_table(
            ["Partition", "Documents"],
            ((name, partitions["counts"].get(name, 0)) for name in PARTITION_ORDER),
        )),
        "",
        "These partitions are independent of the 30-row prompt-development and 127-row "
        "held-out prompt split. Metric weights and thresholds may be fit only on "
        "`metric_dev`; `metric_test` stays locked.",
        "",
        "## Stored AI-output coverage",
        "",
        f"- Model: `{ai['model_id']}`",
        f"- Compiled candidates: {ai['physical_candidate_pdfs']}/{ai['manifest_rows']}",
        f"- Page-count matches: {ai['page_count_matches']}; mismatches: {ai['page_count_mismatches']}",
        f"- Candidate canvas documents: {ai['candidate_canvas_documents']}",
        f"- First-page canvas matches: {ai['first_page_canvas_matches']}; "
        f"mismatches: {ai['first_page_canvas_mismatches']}",
        "",
        "Canvas is its own diagnostic. Most references are Letter while most stored Typst "
        "outputs are A4; silently folding that producer default into a general layout score "
        "would make the score hard to explain.",
        "",
        "## Augmentation applicability",
        "",
        f"Estimated controlled pairs: **{augmentation['estimated_total_pairs']:,}**. "
        f"The blinded manual bundle contains {augmentation['manual_blind_bundle_pairs']:,} "
        f"pairs ({augmentation['manual_non_null_pairs']:,} non-null), covering all 157 references.",
        "",
        *(_markdown_table(
            ["Family", "Scope", "Variants", "Expected axis", "Pairs"],
            (
                (row["family"], row["scope"], row["variants_per_applicable_document"],
                 row["expected_axis"], f"{row['pairs']:,}")
                for row in augmentation["family_totals"]
            ),
        )),
        "",
        "The render-only degradation lane is appearance-only. It cannot be used to teach an "
        "extraction-based content metric that rasterized PDFs have missing content.",
        "",
        "## Provenance and licensing",
        "",
        f"- License columns in accepted manifest: {provenance['accepted_manifest_license_fields']}",
        f"- Per-sample provenance records with a license field: "
        f"{provenance['provenance_license_field_documents']}/157",
        f"- Sources containing explicit license text: "
        f"{provenance['source_explicit_license_text_documents']}/157",
        f"- Source-ID field variants: {provenance['provenance_source_id_fields']}",
        f"- Redistribution status: **{provenance['redistribution_status']}**",
        "",
        "Missing research metadata includes license, original URL, authors, retrieval "
        "timestamp, and transformation record. Those gaps must be fixed before a "
        "redistributable benchmark claim.",
        "",
        "## Files",
        "",
        "- `corpus_profile_157.csv`: one measured row per accepted reference and stored AI result.",
        "- `augmentation_applicability_157.csv`: per-reference augmentation lanes and pair counts.",
        "- `corpus_summary.json`: machine-readable counts, partitions, gaps, and warnings.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    accepted_rows = read_csv(args.accepted)
    ai_rows = read_csv(args.ai_manifest)
    profiles, applicability = build_profiles(accepted_rows, ai_rows, args.seed)
    accepted_fields = list(accepted_rows[0]) if accepted_rows else []
    summary = build_summary(
        profiles, applicability, accepted_fields, args.seed, args.accepted, args.ai_manifest
    )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "corpus_profile_157.csv", profiles)
    write_csv(args.out_dir / "augmentation_applicability_157.csv", applicability)
    (args.out_dir / "corpus_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (args.out_dir / "corpus_summary.md").write_text(
        summary_markdown(summary), encoding="utf-8"
    )
    print(f"documents: {len(profiles)}")
    print(f"estimated augmentation pairs: {summary['augmentation_matrix']['estimated_total_pairs']}")
    print(f"output: {args.out_dir}")


if __name__ == "__main__":
    main()
