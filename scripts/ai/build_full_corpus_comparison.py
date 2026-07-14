"""Assemble the prompt-development and held-out grids into one corpus review PDF."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data" / "latex_benchmark_v0"
DOCUMENTS = ROOT / "results" / "ai_latex_to_typst" / "documents"

ACCEPTED = DATASET / "accepted_manifest.csv"
PROMPT_MANIFEST = DOCUMENTS / "prompt_clean_v0_v1_v3_engine_comparison_manifest.csv"
PROMPT_PDF = DOCUMENTS / "prompt_clean_v0_v1_v3_engine_comparison_grid.pdf"
HELDOUT_MANIFEST = DOCUMENTS / "heldout_v1_v2_v3_cascade_manifest.csv"
HELDOUT_PDF = DOCUMENTS / "heldout_v1_v2_v3_cascade_engine_comparison_grid.pdf"
OUT_PDF = DOCUMENTS / "full_157_ai_engine_comparison_grid.pdf"
OUT_MANIFEST = DOCUMENTS / "full_157_ai_engine_comparison_manifest.csv"

PAGE_W = 1191
PAGE_H = 842
SAMPLE_HEADER = re.compile(r"^(\d{2}_[a-z0-9_]+_\d{3})\s+\|")

CATEGORY_LABELS = {
    "01_prose_sections": "Prose sections",
    "02_lists_formatting": "Lists and formatting",
    "03_math_inline_display": "Inline and display math",
    "04_math_aligned": "Aligned math",
    "05_tables_simple": "Simple tables",
    "06_tables_moderate": "Moderate tables",
    "07_figures_captions": "Figures and captions",
    "08_crossrefs_citations": "Cross-references and citations",
    "09_algorithms": "Algorithms",
    "10_compact_papers": "Compact papers",
    "11_forms_cv_letters": "Forms, CVs, and letters",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accepted", type=Path, default=ACCEPTED)
    parser.add_argument("--prompt-manifest", type=Path, default=PROMPT_MANIFEST)
    parser.add_argument("--prompt-pdf", type=Path, default=PROMPT_PDF)
    parser.add_argument("--heldout-manifest", type=Path, default=HELDOUT_MANIFEST)
    parser.add_argument("--heldout-pdf", type=Path, default=HELDOUT_PDF)
    parser.add_argument("--out", type=Path, default=OUT_PDF)
    parser.add_argument("--manifest", type=Path, default=OUT_MANIFEST)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def index_sample_pages(document: fitz.Document, source: Path) -> dict[str, int]:
    index: dict[str, int] = {}
    for page_number, page in enumerate(document):
        for line in page.get_text("text").splitlines():
            match = SAMPLE_HEADER.match(line.strip())
            if not match:
                continue
            sample_id = match.group(1)
            if sample_id in index:
                raise ValueError(f"duplicate sample page for {sample_id} in {source}")
            index[sample_id] = page_number
            break
    return index


def fit_text(page: fitz.Page, rect: fitz.Rect, text: str, size: float) -> None:
    current = size
    while current >= 7:
        if page.insert_textbox(
            rect, text, fontsize=current, fontname="helv",
            color=(0.18, 0.18, 0.18), lineheight=1.25,
        ) >= 0:
            return
        current -= 0.5
    raise ValueError("cover text did not fit")


def add_cover(document: fitz.Document, accepted_count: int) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((58, 92), "LaTeX-to-Typst full corpus comparison", fontsize=30, fontname="helv")
    page.insert_text(
        (58, 138),
        "pdfLaTeX reference, Gemini 3.1 Flash Lite, and deterministic engines",
        fontsize=17,
        fontname="helv",
        color=(0.28, 0.28, 0.28),
    )
    text = (
        f"{accepted_count} accepted samples, with one complete comparison page per sample. "
        "Every page of each available source PDF is tiled inside its panel.\n\n"
        "AI output selection:\n"
        "- 30 prompt-development samples use the final compiled v0/v1/v3 rescue output\n"
        "- 127 held-out samples use the earliest compiled output from the v1/v2/v3 cascade\n"
        "- the single remaining AI compile failure stays visible as a labeled failure panel\n\n"
        "Each comparison page also includes Pandoc, Tylax, and TypeTeX outputs. Failed or "
        "missing engine conversions remain visible rather than being omitted.\n\n"
        "The prompt-development subset is included for corpus-wide visual review only and "
        "must remain excluded from held-out benchmark claims."
    )
    fit_text(page, fitz.Rect(58, 190, 970, 600), text, 12)


def add_section(document: fitz.Document, category: str, count: int) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((58, 108), category, fontsize=27, fontname="helv")
    page.insert_text(
        (58, 152), CATEGORY_LABELS.get(category, category), fontsize=17,
        fontname="helv", color=(0.28, 0.28, 0.28),
    )
    page.insert_text((58, 194), f"{count} accepted samples", fontsize=11, fontname="helv")


def normalized_manifest_row(
    accepted_row: dict[str, str], source_split: str, source_pdf: Path,
    source_page: int, report_page: int, result_row: dict[str, str],
) -> dict[str, str | int]:
    selected_stage = result_row.get("selected_ai_stage") or result_row.get("ai_prompt_version", "")
    return {
        "sample_id": accepted_row["sample_id"],
        "category": accepted_row["category"],
        "source_split": source_split,
        "selected_ai_stage": selected_stage,
        "ai_final_compiled": result_row.get("ai_final_compiled", ""),
        "reference_pages": result_row.get("reference_pages", accepted_row["page_count"]),
        "ai_pages": result_row.get("ai_pages", ""),
        "page_count_match": result_row.get("page_count_match", ""),
        "pandoc_compile": result_row.get("pandoc_compile", ""),
        "tylax_compile": result_row.get("tylax_compile", ""),
        "typetex_compile": result_row.get("typetex_compile", ""),
        "source_comparison_pdf": str(source_pdf.relative_to(ROOT)),
        "source_pdf_page": source_page + 1,
        "report_page": report_page,
    }


def main() -> None:
    args = parse_args()
    accepted_rows = read_csv(args.accepted)
    accepted_by_id = {row["sample_id"]: row for row in accepted_rows}
    if len(accepted_by_id) != len(accepted_rows):
        raise ValueError("accepted manifest contains duplicate sample IDs")

    prompt_rows = {row["sample_id"]: row for row in read_csv(args.prompt_manifest)}
    heldout_rows = {row["sample_id"]: row for row in read_csv(args.heldout_manifest)}
    overlap = set(prompt_rows) & set(heldout_rows)
    if overlap:
        raise ValueError(f"prompt-development and held-out manifests overlap: {sorted(overlap)}")
    combined_ids = set(prompt_rows) | set(heldout_rows)
    accepted_ids = set(accepted_by_id)
    if combined_ids != accepted_ids:
        missing = sorted(accepted_ids - combined_ids)
        extra = sorted(combined_ids - accepted_ids)
        raise ValueError(f"split manifests do not partition accepted corpus; missing={missing}, extra={extra}")

    prompt_pdf = fitz.open(args.prompt_pdf)
    heldout_pdf = fitz.open(args.heldout_pdf)
    try:
        prompt_pages = index_sample_pages(prompt_pdf, args.prompt_pdf)
        heldout_pages = index_sample_pages(heldout_pdf, args.heldout_pdf)
        if set(prompt_pages) != set(prompt_rows):
            raise ValueError("prompt-development PDF pages do not match its manifest")
        if set(heldout_pages) != set(heldout_rows):
            raise ValueError("held-out PDF pages do not match its manifest")

        by_category: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in accepted_rows:
            by_category[row["category"]].append(row)
        for rows in by_category.values():
            rows.sort(key=lambda row: row["sample_id"])

        output = fitz.open()
        add_cover(output, len(accepted_rows))
        toc = [[1, "Full corpus comparison", 1]]
        manifest: list[dict[str, str | int]] = []

        for category in sorted(by_category):
            category_rows = by_category[category]
            add_section(output, category, len(category_rows))
            toc.append([1, f"{category} - {CATEGORY_LABELS.get(category, category)}", output.page_count])
            for accepted_row in category_rows:
                sample_id = accepted_row["sample_id"]
                if sample_id in prompt_rows:
                    source_split = "prompt_dev"
                    source_doc = prompt_pdf
                    source_path = args.prompt_pdf
                    source_page = prompt_pages[sample_id]
                    result_row = prompt_rows[sample_id]
                else:
                    source_split = "heldout"
                    source_doc = heldout_pdf
                    source_path = args.heldout_pdf
                    source_page = heldout_pages[sample_id]
                    result_row = heldout_rows[sample_id]

                output.insert_pdf(source_doc, from_page=source_page, to_page=source_page)
                report_page = output.page_count
                copied_page = output[-1]
                copied_page.insert_text(
                    (PAGE_W - 150, PAGE_H - 9), f"full corpus page {report_page}",
                    fontsize=6, fontname="helv", color=(0.42, 0.42, 0.42),
                )
                toc.append([2, sample_id, report_page])
                manifest.append(normalized_manifest_row(
                    accepted_row, source_split, source_path, source_page,
                    report_page, result_row,
                ))

        if len(manifest) != len(accepted_rows):
            raise AssertionError("not every accepted sample was added to the report")

        output.set_toc(toc)
        output.set_metadata({
            "title": "LaTeX-to-Typst full 157-sample comparison",
            "subject": "Full accepted corpus visual review grid",
            "author": "Lathe benchmark",
        })
        args.out.parent.mkdir(parents=True, exist_ok=True)
        output.save(args.out, garbage=4, deflate=True)
        output.close()
    finally:
        prompt_pdf.close()
        heldout_pdf.close()

    with args.manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)

    print(f"comparison: {args.out}")
    print(f"manifest: {args.manifest}")
    print(f"samples: {len(manifest)}")
    print(f"pages: {1 + len(by_category) + len(manifest)}")


if __name__ == "__main__":
    main()
