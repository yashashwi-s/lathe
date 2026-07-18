#!/usr/bin/env python3
"""Record the frozen manual visual audit of all 157 reference preview panels."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "latex_benchmark_v0" / "accepted_manifest.csv"
OUTPUT = ROOT / "results" / "metric_research_v1" / "reference_visual_audit_157.csv"
SUMMARY = ROOT / "results" / "metric_research_v1" / "reference_visual_audit_157.md"


CATEGORY_NOTES = {
    "01_prose_sections": (
        "Clean scholarly prose scaffold; substantial template reuse limits independent visual variety."
    ),
    "02_lists_formatting": (
        "List structure is visible, but item density varies from a few short items to long extracted prose."
    ),
    "03_math_inline_display": (
        "Clean one-page five-expression scaffold; useful formula variety but repeated page structure."
    ),
    "04_math_aligned": (
        "Aligned formulas are visible; several references flow to a second page and exercise pagination."
    ),
    "05_tables_simple": (
        "Wide variation in table density and page count; some references reserve an introductory page."
    ),
    "06_tables_moderate": (
        "Dense, wide, or grouped tables across one to three pages; several begin with a sparse scaffold page."
    ),
    "07_figures_captions": (
        "Scope limit: panels contain blank placeholder rectangles and captions, not image-semantic content."
    ),
    "08_crossrefs_citations": (
        "Clean equation/reference scaffold with heavy structural reuse; useful for exact labels and citations."
    ),
    "09_algorithms": (
        "Pseudocode rules, indentation, line numbers, and comments are visible across one or two pages."
    ),
    "10_compact_papers": (
        "Dense one- or two-page article layouts provide compact prose, equations, references, and page flow."
    ),
    "11_forms_cv_letters": (
        "CV/form examples are structurally rich; letter examples are close template variants."
    ),
}


SPECIAL_NOTES = {
    "05_tables_simple_020": (
        "Content outlier: the table material includes large stacked natural-language response labels; retain "
        "for robustness but report it separately in sensitivity checks."
    ),
    "11_forms_cv_letters_001": "Three-page CV/form template with table-like fields and signatures.",
    "11_forms_cv_letters_002": "Two-page CV/form template; distinct from the repeated letter subgroup.",
}


def main() -> None:
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 157:
        raise RuntimeError(f"expected 157 accepted references, found {len(rows)}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "sample_id", "category", "preview_page", "reference_pages",
        "manual_render_check", "visual_scope", "manual_note",
    ]
    output_rows = []
    for index, row in enumerate(rows, start=2):
        category = row["category"]
        scope = "presence_geometry_caption_only" if category == "07_figures_captions" else "full_reference_panel"
        note = SPECIAL_NOTES.get(row["sample_id"], CATEGORY_NOTES[category])
        output_rows.append({
            "sample_id": row["sample_id"],
            "category": category,
            "preview_page": index,
            "reference_pages": row["page_count"],
            "manual_render_check": "pass",
            "visual_scope": scope,
            "manual_note": note,
        })

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    figure_limited = sum(row["visual_scope"] != "full_reference_panel" for row in output_rows)
    SUMMARY.write_text(
        "# Reference visual audit v1\n\n"
        "The complete 158-page benchmark preview was rendered and inspected in 40 two-by-two "
        "contact sheets. Preview page 1 is the cover; pages 2-158 contain all 157 accepted "
        "references. Multipage references are tiled inside their panel.\n\n"
        f"- References checked: **{len(output_rows)} / 157**\n"
        "- Missing, blank, clipped, or unreadable preview panels: **0**\n"
        f"- Figure references restricted to presence/geometry/caption validation: **{figure_limited}**\n"
        "- Material corpus limitation: repeated category scaffolds reduce independent visual variety.\n"
        "- Content outlier retained for sensitivity analysis: `05_tables_simple_020`.\n\n"
        "This pass verifies reference rendering and visible scope. It does not validate the correctness "
        "of every source fact or create human perceptual ratings.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
