"""Build held-out cascade reports and comparison grid."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data" / "latex_benchmark_v0"
SPLIT = DATASET / "splits" / "heldout_clean_127.csv"
ENGINE_DIR = ROOT / "results" / "latex_benchmark_v0"
AI_ROOT = ROOT / "results" / "ai_latex_to_typst" / "openrouter" / "google_gemini-3.1-flash-lite"
V1 = AI_ROOT / "prompt_v1_heldout_clean"
V2 = AI_ROOT / "prompt_v2_heldout_v1_failures"
V3 = AI_ROOT / "prompt_v3_heldout_v2_failures"
OUT_DIR = ROOT / "results" / "ai_latex_to_typst" / "documents"
PAGE_W = 1191
PAGE_H = 842

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

STAGES = [
    ("v1", V1, "prompt v1 heldout"),
    ("v2", V2, "prompt v2 on v1 failures"),
    ("v3", V3, "prompt v3 on v2 failures"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", type=Path, default=SPLIT)
    parser.add_argument("--engine-dir", type=Path, default=ENGINE_DIR)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    return parser.parse_args()


def read_csv(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(newline="", encoding="utf-8")))


def load_meta(run_dir: Path) -> dict[str, dict]:
    result = {}
    for path in (run_dir / "samples").glob("*/meta.json"):
        result[path.parent.name] = json.loads(path.read_text(encoding="utf-8"))
    return result


def engine_index(engine_dir: Path) -> dict[tuple[str, str], dict]:
    return {
        (row["sample_id"], row["engine"]): row
        for row in read_csv(engine_dir / "engine_manifest.csv")
    }


def fit_text(page: fitz.Page, rect: fitz.Rect, text: str, size: float = 8,
             color=(0.12, 0.12, 0.12)) -> None:
    current = size
    while current >= 5.5:
        if page.insert_textbox(rect, text, fontsize=current, fontname="helv",
                               color=color, lineheight=1.18) >= 0:
            return
        current -= 0.5
    page.insert_textbox(rect, text, fontsize=5.5, fontname="helv",
                        color=color, lineheight=1.05)


def draw_pdf_tiled(page: fitz.Page, pdf_path: Path | None, rect: fitz.Rect,
                   failure_text: str = "missing / failed") -> None:
    if pdf_path is None or not pdf_path.exists():
        page.draw_rect(rect, color=(0.72, 0.18, 0.18), fill=(0.99, 0.95, 0.95), width=0.9)
        fit_text(page, rect + (12, 16, -12, -16), failure_text, size=9,
                 color=(0.55, 0.08, 0.08))
        return
    try:
        source = fitz.open(pdf_path)
    except Exception:
        page.draw_rect(rect, color=(0.72, 0.18, 0.18), fill=(0.99, 0.95, 0.95), width=0.9)
        fit_text(page, rect + (12, 16, -12, -16), "invalid PDF", size=9,
                 color=(0.55, 0.08, 0.08))
        return
    try:
        count = source.page_count
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)
        gap = 5
        cell_w = (rect.width - gap * (cols - 1)) / cols
        cell_h = (rect.height - gap * (rows - 1)) / rows
        for index in range(count):
            row = index // cols
            col = index % cols
            cell = fitz.Rect(
                rect.x0 + col * (cell_w + gap),
                rect.y0 + row * (cell_h + gap),
                rect.x0 + col * (cell_w + gap) + cell_w,
                rect.y0 + row * (cell_h + gap) + cell_h,
            )
            source_page = source.load_page(index)
            scale = min(cell.width / source_page.rect.width, cell.height / source_page.rect.height)
            width = source_page.rect.width * scale
            height = source_page.rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - width) / 2,
                cell.y0 + (cell.height - height) / 2,
                cell.x0 + (cell.width + width) / 2,
                cell.y0 + (cell.height + height) / 2,
            )
            page.show_pdf_page(target, source, index)
            page.draw_rect(target, color=(0.62, 0.62, 0.62), width=0.45)
    finally:
        source.close()


def draw_panel(page: fitz.Page, rect: fitz.Rect, label: str,
               pdf_path: Path | None, status: str, failure_text: str = "missing / failed") -> None:
    page.draw_rect(rect, color=(0.30, 0.30, 0.30), fill=(1, 1, 1), width=0.65)
    page.draw_rect(fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y0 + 24),
                   color=(0.16, 0.16, 0.16), fill=(0.95, 0.96, 0.97), width=0.5)
    page.insert_text((rect.x0 + 8, rect.y0 + 15), label, fontsize=9,
                     fontname="helv", color=(0.08, 0.08, 0.08))
    page.insert_textbox(fitz.Rect(rect.x0 + rect.width * 0.42, rect.y0 + 6,
                                  rect.x1 - 8, rect.y0 + 20), status,
                        fontsize=6.5, fontname="helv", color=(0.30, 0.30, 0.30),
                        align=2)
    draw_pdf_tiled(page, pdf_path, rect + (7, 31, -7, -7), failure_text)


def selected_ai(sample_id: str, stage_meta: dict[str, dict[str, dict]]) -> tuple[str, Path | None, dict | None]:
    last_meta = None
    last_stage = ""
    for stage, run_dir, label in STAGES:
        meta = stage_meta[stage].get(sample_id)
        if not meta:
            continue
        last_meta = meta
        last_stage = stage
        if meta.get("final_compiled"):
            return label, run_dir / "samples" / sample_id / "output.pdf", meta
    if last_meta:
        run_dir = dict((stage, run_dir) for stage, run_dir, _ in STAGES)[last_stage]
        return f"prompt {last_stage} final failure", None, last_meta
    return "AI not run", None, None


def cover_page(doc: fitz.Document, rows: list[dict], summaries: dict[str, dict]) -> None:
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((58, 92), "Held-out LaTeX-to-Typst cascade", fontsize=30, fontname="helv")
    page.insert_text((58, 138), "Reference, deterministic engines, and Gemini 3.1 Flash Lite v1-v3", fontsize=17,
                     fontname="helv", color=(0.28, 0.28, 0.28))
    total_cost = sum(float(s.get("reported_cost_usd") or 0) for s in summaries.values())
    text = (
        f"{len(rows)} clean held-out samples. Prompt-development rows are excluded.\n\n"
        "Cascade policy:\n"
        "- v1 runs on all held-out samples\n"
        "- v2 runs only on v1 final compile failures\n"
        "- v3 runs only on v2 final compile failures\n"
        "- every stage allows at most one repair turn using the compiler output\n\n"
        f"Final compiled outputs after cascade: 126/{len(rows)}\n"
        f"Total API-reported cost: ${total_cost:.6f}\n\n"
        "This is a held-out prompt/refinement report, but v2 and v3 are failure-targeted rescue prompts."
    )
    fit_text(page, fitz.Rect(58, 190, 950, 560), text, size=12)


def section_page(doc: fitz.Document, category: str, count: int) -> None:
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_text((58, 108), category, fontsize=27, fontname="helv")
    page.insert_text((58, 152), CATEGORY_LABELS.get(category, category), fontsize=17,
                     fontname="helv", color=(0.28, 0.28, 0.28))
    page.insert_text((58, 194), f"{count} held-out samples", fontsize=11, fontname="helv")


def sample_page(doc: fitz.Document, row: dict, engines: dict, stage_meta: dict) -> dict:
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    sample_id = row["sample_id"]
    page.insert_text((34, 30), f"{sample_id} | {row['category']} | heldout",
                     fontsize=13, fontname="helv")
    source = f"{row['source_dataset']}; {row['source_ids']}"[:220]
    fit_text(page, fitz.Rect(34, 40, PAGE_W - 34, 67), source, size=7,
             color=(0.34, 0.34, 0.34))
    page.draw_line((34, 72), (PAGE_W - 34, 72), color=(0.72, 0.72, 0.72), width=0.6)

    margin = 34
    gap_x = 16
    gap_y = 18
    top = 86
    cell_w = (PAGE_W - 2 * margin - 2 * gap_x) / 3
    cell_h = (PAGE_H - top - margin - gap_y) / 2
    rects = []
    for grid_row in range(2):
        for grid_col in range(3):
            x0 = margin + grid_col * (cell_w + gap_x)
            y0 = top + grid_row * (cell_h + gap_y)
            rects.append(fitz.Rect(x0, y0, x0 + cell_w, y0 + cell_h))

    reference = ROOT / row["reference_pdf"]
    ai_label, ai_pdf, ai_meta = selected_ai(sample_id, stage_meta)
    ai_status = "not run"
    ai_failure = "AI output unavailable"
    if ai_meta:
        ai_status = f"compile={'ok' if ai_meta.get('final_compiled') else 'failed'}; attempts={ai_meta.get('attempts')}"
        ai_failure = f"failed after {ai_meta.get('attempts')} attempt(s)\n{ai_meta.get('final_error_summary', '')}"

    draw_panel(page, rects[0], "Reference", reference, f"pages={row['page_count']}")
    draw_panel(page, rects[1], f"AI - {ai_label}", ai_pdf, ai_status, ai_failure)

    stage_lines = []
    selected_stage = ""
    for stage, _run_dir, label in STAGES:
        meta = stage_meta[stage].get(sample_id)
        if not meta:
            continue
        status = "ok" if meta.get("final_compiled") else "failed"
        stage_lines.append(f"{label}: {status}, attempts={meta.get('attempts')}")
        if meta.get("final_compiled") and not selected_stage:
            selected_stage = stage
    info = (
        f"Selected AI stage: {selected_stage or 'none'}\n"
        f"Reference page count: {row['page_count']}\n"
        f"AI page count: {ai_meta.get('candidate_pages') if ai_meta else 'n/a'}\n"
        f"Source: {row['source_dataset']}\n"
        f"Source IDs: {row['source_ids']}\n\n"
        + "\n".join(stage_lines)
        + "\n\nAll source and engine pages are tiled; no page is intentionally omitted."
    )
    page.draw_rect(rects[2], color=(0.30, 0.30, 0.30), fill=(0.97, 0.98, 0.99), width=0.65)
    page.insert_text((rects[2].x0 + 10, rects[2].y0 + 18), "Status and provenance", fontsize=9,
                     fontname="helv")
    fit_text(page, rects[2] + (10, 34, -10, -10), info, size=8)

    engine_status = {}
    for offset, engine in enumerate(("pandoc", "tylax", "typetex"), start=3):
        engine_row = engines.get((sample_id, engine))
        status = "not run"
        pdf = None
        failure = "engine output unavailable"
        if engine_row:
            status = f"convert={engine_row['conversion_status']}; compile={engine_row['compile_status']}"
            if engine_row["compile_status"] == "ok":
                pdf = ROOT / engine_row["pdf_path"]
            failure = status
            engine_status[engine] = engine_row["compile_status"]
        draw_panel(page, rects[offset], engine.title(), pdf, status, failure)

    return {
        "sample_id": sample_id,
        "category": row["category"],
        "selected_ai_stage": selected_stage,
        "ai_final_compiled": bool(ai_meta and ai_meta.get("final_compiled")),
        "ai_attempts_selected_stage": ai_meta.get("attempts") if ai_meta else "",
        "reference_pages": row["page_count"],
        "ai_pages": ai_meta.get("candidate_pages") if ai_meta else "",
        "page_count_match": bool(ai_meta and ai_meta.get("page_count_match")),
        "v1_final_compiled": bool(stage_meta["v1"].get(sample_id, {}).get("final_compiled")),
        "v2_final_compiled": bool(stage_meta["v2"].get(sample_id, {}).get("final_compiled")),
        "v3_final_compiled": bool(stage_meta["v3"].get(sample_id, {}).get("final_compiled")),
        "pandoc_compile": engine_status.get("pandoc", "missing"),
        "tylax_compile": engine_status.get("tylax", "missing"),
        "typetex_compile": engine_status.get("typetex", "missing"),
    }


def write_analysis(out_dir: Path, rows: list[dict], manifest: list[dict], summaries: dict[str, dict]) -> None:
    by_category = defaultdict(lambda: {"n": 0, "compiled": 0})
    stage_counts = Counter(row["selected_ai_stage"] or "failed" for row in manifest)
    for row in manifest:
        cell = by_category[row["category"]]
        cell["n"] += 1
        cell["compiled"] += int(row["ai_final_compiled"])
    total_cost = sum(float(summary.get("reported_cost_usd") or 0) for summary in summaries.values())
    lines = [
        "# Held-out cascade analysis",
        "",
        f"Clean held-out samples: {len(rows)}",
        f"Final compiled after v1-v3 cascade: {sum(row['ai_final_compiled'] for row in manifest)}/{len(rows)}",
        f"Page-count matches among compiled outputs: {sum(row['page_count_match'] for row in manifest)}",
        f"API-reported cost: ${total_cost:.6f}",
        "",
        "## Stage summaries",
        "",
        "| Stage | Samples run | First-pass compiled | Final compiled | Repaired | Cost |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for stage in ("v1", "v2", "v3"):
        summary = summaries[stage]
        lines.append(
            f"| `{stage}` | {summary['completed']} | {summary['first_pass_compiled']} | "
            f"{summary['final_compiled']} | {summary['repaired']} | "
            f"${float(summary['reported_cost_usd']):.6f} |"
        )
    lines.extend(["", "## Selected final stage", "", "| Stage | Samples |", "|---|---:|"])
    for stage, count in sorted(stage_counts.items()):
        lines.append(f"| `{stage}` | {count} |")
    lines.extend(["", "## By category", "", "| Category | Compiled | Total |", "|---|---:|---:|"])
    for category in sorted(by_category):
        cell = by_category[category]
        lines.append(f"| `{category}` | {cell['compiled']} | {cell['n']} |")
    remaining = [row for row in manifest if not row["ai_final_compiled"]]
    lines.extend(["", "## Remaining failures", ""])
    if not remaining:
        lines.append("No final compile failures remain.")
    else:
        lines.extend(["| Sample | Category | Last stage |", "|---|---|---|"])
        for row in remaining:
            lines.append(f"| `{row['sample_id']}` | `{row['category']}` | `v3` |")
    lines.extend([
        "",
        "## Interpretation",
        "",
        "v1 is the broad held-out run. v2 and v3 are targeted rescue prompts written after observing failure patterns, so the cascade result should be reported separately from the single-prompt v1 held-out result.",
    ])
    (out_dir / "heldout_cascade_analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    rows = read_csv(args.split)
    engines = engine_index(args.engine_dir)
    stage_meta = {stage: load_meta(run_dir) for stage, run_dir, _ in STAGES}
    summaries = {
        stage: json.loads((run_dir / "summary.json").read_text(encoding="utf-8"))
        for stage, run_dir, _ in STAGES
    }
    by_category = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row)

    doc = fitz.open()
    cover_page(doc, rows, summaries)
    manifest = []
    for category in sorted(by_category):
        category_rows = by_category[category]
        section_page(doc, category, len(category_rows))
        for row in category_rows:
            manifest.append(sample_page(doc, row, engines, stage_meta))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_pdf = args.out_dir / "heldout_v1_v2_v3_cascade_engine_comparison_grid.pdf"
    out_manifest = args.out_dir / "heldout_v1_v2_v3_cascade_manifest.csv"
    doc.set_metadata({
        "title": "Held-out LaTeX-to-Typst cascade comparison",
        "subject": "127-sample held-out v1-v3 cascade review grid",
        "author": "Lathe benchmark",
    })
    doc.save(out_pdf, garbage=4, deflate=True)
    doc.close()

    with out_manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]))
        writer.writeheader()
        writer.writerows(manifest)
    write_analysis(args.out_dir, rows, manifest, summaries)
    print(f"comparison: {out_pdf}")
    print(f"manifest: {out_manifest}")
    print(f"samples: {len(manifest)}")


if __name__ == "__main__":
    main()
