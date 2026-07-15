#!/usr/bin/env python3
"""Build a visually labeled grid of every available model and engine family.

The report deliberately separates three evidence regimes:

1. the current canonical hard set (shared reference, Gemini, Claude, engines),
2. the dataset-expansion stress test (Claude-only model coverage so far), and
3. the archived provisional benchmark (legacy GPT/Gemini/Claude results).

Stored Typst-only Claude results are compiled into a temporary directory and
embedded in the final PDF. Missing, failed, and not-run cells remain visible.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import fitz


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "output/pdf/all_models_engines_reference_grid.pdf"
DEFAULT_MANIFEST = ROOT / "output/pdf/all_models_engines_reference_grid_manifest.csv"
DEFAULT_TMP = ROOT / "tmp/pdfs/all_models_engine_grid"

PAGE_W = 17 * 72
PAGE_H = 11 * 72

CANONICAL_SAMPLES = (
    "03_math_inline_display_004",
    "04_math_aligned_014",
    "05_tables_simple_005",
    "05_tables_simple_021",
    "05_tables_simple_023",
    "06_tables_moderate_010",
    "07_figures_captions_007",
    "09_algorithms_003",
)
CORE_AGENTIC = set(CANONICAL_SAMPLES[2:])

EXPANSION_SAMPLES = (
    "arxiv5t_paper_019",
    "i2s_equation_001",
    "i2s_plot_001",
    "neurips_paper_029",
    "pubmed_table_004",
    "pubmed_table_005",
)

LEGACY_SAMPLES = {
    "algorithms_easy": ("08_algorithms", "easy"),
    "algorithms_medium": ("08_algorithms", "medium"),
    "eq_hard_hard": ("03_eq_hard", "hard"),
    "eq_simple_hard": ("02_eq_simple", "hard"),
    "prose_easy": ("01_prose", "easy"),
    "prose_hard": ("01_prose", "hard"),
    "tables_complex_easy": ("07_tables_complex", "easy"),
    "tables_complex_hard": ("07_tables_complex", "hard"),
}


@dataclass
class Panel:
    candidate: str
    label: str
    path: Optional[Path]
    status: str
    state: str = "ok"
    source: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--tmp", type=Path, default=DEFAULT_TMP)
    parser.add_argument("--keep-assets", action="store_true")
    return parser.parse_args()


def read_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fit_text(
    page: fitz.Page,
    rect: fitz.Rect,
    text: str,
    size: float = 9,
    minimum: float = 5.5,
    color: Tuple[float, float, float] = (0.12, 0.14, 0.17),
    align: int = 0,
) -> None:
    current = size
    while current >= minimum:
        remaining = page.insert_textbox(
            rect,
            text,
            fontsize=current,
            fontname="helv",
            color=color,
            lineheight=1.15,
            align=align,
        )
        if remaining >= 0:
            return
        current -= 0.5


def draw_pdf_tiled(page: fitz.Page, path: Path, rect: fitz.Rect) -> int:
    source = fitz.open(path)
    try:
        count = source.page_count
        cols = max(1, math.ceil(math.sqrt(count * rect.width / rect.height)))
        rows = math.ceil(count / cols)
        gap = 3.5
        cell_w = (rect.width - gap * (cols - 1)) / cols
        cell_h = (rect.height - gap * (rows - 1)) / rows
        for index in range(count):
            row, col = divmod(index, cols)
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
            page.draw_rect(target, color=(0.68, 0.70, 0.73), width=0.35)
        return count
    finally:
        source.close()


def draw_panel(page: fitz.Page, rect: fitz.Rect, panel: Panel) -> int:
    colors = {
        "ok": ((0.25, 0.31, 0.39), (0.96, 0.97, 0.98)),
        "failed": ((0.68, 0.18, 0.17), (1.00, 0.95, 0.95)),
        "not_run": ((0.46, 0.48, 0.51), (0.96, 0.96, 0.96)),
        "info": ((0.18, 0.39, 0.54), (0.94, 0.98, 1.00)),
    }
    border, fill = colors.get(panel.state, colors["ok"])
    page.draw_rect(rect, color=border, fill=(1, 1, 1), width=0.8)
    header = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y0 + 32)
    page.draw_rect(header, color=border, fill=fill, width=0.6)
    fit_text(page, header + (8, 6, -8, -5), panel.label, size=8.5, minimum=6.5)

    content = rect + (7, 38, -7, -24)
    pages = 0
    if panel.path and panel.path.exists():
        try:
            pages = draw_pdf_tiled(page, panel.path, content)
        except Exception as exc:
            panel.state = "failed"
            panel.status = "Invalid PDF: " + str(exc)[:120]
            fit_text(page, content + (10, 20, -10, -20), panel.status, size=9,
                     color=(0.58, 0.10, 0.09), align=1)
    else:
        message = panel.status or "Artifact unavailable"
        color = (0.58, 0.10, 0.09) if panel.state == "failed" else (0.38, 0.40, 0.43)
        fit_text(page, content + (12, 24, -12, -24), message, size=9,
                 color=color, align=1)

    footer = fitz.Rect(rect.x0 + 6, rect.y1 - 20, rect.x1 - 6, rect.y1 - 4)
    status = panel.status
    if pages:
        status = (status + " | " if status else "") + f"{pages} page(s) tiled"
    fit_text(page, footer, status, size=6.5, minimum=5.5, color=(0.33, 0.35, 0.38), align=1)
    return pages


def panel_rects() -> List[fitz.Rect]:
    margin_x = 30
    top = 62
    bottom = 25
    gap_x = 12
    gap_y = 13
    width = (PAGE_W - 2 * margin_x - 3 * gap_x) / 4
    height = (PAGE_H - top - bottom - gap_y) / 2
    rects = []
    for row in range(2):
        for col in range(4):
            x0 = margin_x + col * (width + gap_x)
            y0 = top + row * (height + gap_y)
            rects.append(fitz.Rect(x0, y0, x0 + width, y0 + height))
    return rects


def compile_typst(source: Path, output: Path) -> Tuple[Optional[Path], str, str]:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = ["typst", "compile", "--root", str(ROOT), str(source), str(output)]
    run = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    if run.returncode == 0 and output.exists():
        return output, "compiled from stored Typst", "ok"
    error = (run.stderr or run.stdout or "Typst compile failed").strip().replace("\n", " ")
    return None, "recompile failed: " + error[:180], "failed"


def summary_for_typst(source: Path) -> Optional[Path]:
    for directory in (source.parent, source.parent.parent):
        candidate = directory / "summary.json"
        if candidate.exists():
            return candidate
    return None


def model_status(source: Path) -> Tuple[bool, str]:
    summary_path = summary_for_typst(source)
    if not summary_path:
        return True, "stored Typst output"
    summary = read_json(summary_path)
    final = summary.get("final") or {}
    compiled = bool(final.get("compiled"))
    bits = [summary.get("method", "model output")]
    raster_path = summary_path.parent / "raster_v2.json"
    score = None
    if raster_path.exists():
        score = read_json(raster_path).get("overall")
    if score is None:
        score = final.get("overall")
    if score is not None:
        bits.append(f"overall={100 * float(score):.1f}")
    if final.get("pages"):
        bits.append("pages=" + str(final["pages"]))
    return compiled, "; ".join(bits)


def compiled_model_panel(
    tmp: Path,
    section: str,
    sample: str,
    candidate: str,
    label: str,
    source: Path,
) -> Panel:
    if not source.exists():
        return Panel(candidate, label, None, "stored Typst output missing", "failed", str(source))
    stored_compiled, detail = model_status(source)
    if not stored_compiled:
        return Panel(candidate, label, None, detail + "; no compiled artifact", "failed", str(source))
    output = tmp / section / sample / (candidate.replace("_", "-") + ".pdf")
    compile_source = source
    if section == "expansion":
        # Full-document outputs can reference figures shipped with the source
        # corpus, while the PR intentionally stores only the generated .typ in
        # each run directory. Recreate the original compilation context in tmp.
        family = sample.rsplit("_", 1)[0]
        corpus = ROOT / "dataset_expansion/corpus" / family / sample
        staged = output.parent / "source"
        shutil.copytree(corpus, staged, dirs_exist_ok=True)
        compile_source = staged / "output.typ"
        shutil.copy2(source, compile_source)
    pdf, compile_note, state = compile_typst(compile_source, output)
    return Panel(candidate, label, pdf, detail + "; " + compile_note, state, str(source))


def gemini_panel(sample: str) -> Panel:
    root = ROOT / "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite"
    stages = (
        ("prompt_v3_prompt_dev_failures", "prompt v3 rescue"),
        ("prompt_v1_v0_failures", "prompt v1 targeted retry"),
        ("prompt_v0", "prompt v0"),
    )
    for directory, label in stages:
        sample_dir = root / directory / "samples" / sample
        meta_path = sample_dir / "meta.json"
        pdf = sample_dir / "output.pdf"
        if not meta_path.exists():
            continue
        meta = read_json(meta_path)
        if meta.get("final_compiled") and pdf.exists():
            return Panel(
                "gemini_3_1_flash_lite",
                "Gemini 3.1 Flash Lite - one-turn cascade",
                pdf,
                f"{label}; attempts={meta.get('attempts', 'n/a')}",
                "ok",
                str(pdf),
            )
        return Panel(
            "gemini_3_1_flash_lite",
            "Gemini 3.1 Flash Lite - one-turn cascade",
            None,
            f"{label}; compile failed",
            "failed",
            str(meta_path),
        )
    return Panel(
        "gemini_3_1_flash_lite",
        "Gemini 3.1 Flash Lite - one-turn cascade",
        None,
        "not evaluated",
        "not_run",
    )


def engine_index() -> Dict[Tuple[str, str], dict]:
    path = ROOT / "results/latex_benchmark_v0/engine_manifest.csv"
    return {(row["sample_id"], row["engine"]): row for row in read_csv(path)}


def canonical_engine_panel(sample: str, engine: str, index: Dict[Tuple[str, str], dict]) -> Panel:
    category = sample.rsplit("_", 1)[0]
    row = index.get((sample, engine))
    label = {"pandoc": "Pandoc", "tylax": "Tylax", "typetex": "TypeTeX"}[engine]
    path = ROOT / "results/latex_benchmark_v0" / category / sample / f"{engine}.pdf"
    if row and row.get("compile_status") == "ok" and path.exists():
        return Panel(engine, label + " - deterministic engine", path,
                     "conversion=ok; compile=ok", "ok", str(path))
    status = "not evaluated"
    state = "not_run"
    if row:
        status = f"conversion={row.get('conversion_status')}; compile={row.get('compile_status')}"
        state = "failed"
    return Panel(engine, label + " - deterministic engine", None, status, state, str(path))


def canonical_panels(tmp: Path, sample: str, engines: Dict[Tuple[str, str], dict]) -> List[Panel]:
    category = sample.rsplit("_", 1)[0]
    reference = ROOT / "data/latex_benchmark_v0/corpus" / category / sample / "reference.pdf"
    if sample in CORE_AGENTIC:
        sonnet = ROOT / "harness/runs" / f"{sample}__visual__sonnet__qlow/work/output.typ"
        opus = ROOT / "harness/runs" / f"{sample}__visual__opus__v3run_v3/best_checkpoint.typ"
        sonnet_label = "Claude Sonnet 4.6 - agentic v1 visual low"
        opus_label = "Claude Opus 4.7 - agentic v3 visual medium"
    else:
        sonnet = ROOT / "harness/runs" / f"{sample}__1turn__sonnet__base/output.typ"
        opus = ROOT / "harness/runs" / f"{sample}__1turn__opus__base/output.typ"
        sonnet_label = "Claude Sonnet 4.6 - one-turn low"
        opus_label = "Claude Opus 4.7 - one-turn low"
    panels = [
        Panel("reference", "Reference - pdfLaTeX", reference, "canonical reference", "ok", str(reference)),
        gemini_panel(sample),
        compiled_model_panel(tmp, "canonical", sample, "claude_sonnet_4_6", sonnet_label, sonnet),
        compiled_model_panel(tmp, "canonical", sample, "claude_opus_4_7", opus_label, opus),
    ]
    panels.extend(canonical_engine_panel(sample, engine, engines) for engine in ("pandoc", "tylax", "typetex"))
    note = (
        "CURRENT CANONICAL HARD SET\n\n"
        "Same sample and reference across every populated cell. Claude uses agentic outputs "
        "on the six core hard samples and one-turn outputs on the two extra math samples. "
        "Gemini uses the stored prompt cascade. Missing cells are shown, not dropped."
    )
    panels.append(Panel("scope", "Scope and comparability", None, note, "info"))
    return panels


def expansion_panels(tmp: Path, sample: str) -> List[Panel]:
    family = sample.rsplit("_", 1)[0]
    reference = ROOT / "dataset_expansion/corpus" / family / sample / "reference.pdf"
    sonnet = ROOT / "dataset_expansion/runs" / f"{sample}__1turn__sonnet__dsx/work/output.typ"
    opus = ROOT / "dataset_expansion/runs_agentic" / f"{sample}__visual__opus__dsx_v3/work/output.typ"
    panels = [
        Panel("reference", "Reference - Tectonic LaTeX", reference,
              "dataset-expansion reference", "ok", str(reference)),
        Panel("gemini_3_1_flash_lite", "Gemini 3.1 Flash Lite", None,
              "not evaluated on expansion set", "not_run"),
        compiled_model_panel(tmp, "expansion", sample, "claude_sonnet_4_6",
                             "Claude Sonnet 4.6 - one-turn low", sonnet),
        compiled_model_panel(tmp, "expansion", sample, "claude_opus_4_7",
                             "Claude Opus 4.7 - agentic v3 visual low", opus),
    ]
    for engine, label in (("pandoc", "Pandoc"), ("tylax", "Tylax"), ("typetex", "TypeTeX")):
        panels.append(Panel(engine, label + " - deterministic engine", None,
                            "not evaluated on expansion set", "not_run"))
    note = (
        "DATASET-EXPANSION STRESS TEST\n\n"
        "This PR evaluated Claude Sonnet one-turn and Claude Opus agentic v3 only. "
        "The empty Gemini and engine cells are intentional coverage gaps. References were "
        "compiled with Tectonic, so these pages are not pooled with pdfLaTeX benchmark scores."
    )
    panels.append(Panel("scope", "Scope and comparability", None, note, "info"))
    return panels


def legacy_panels(sample: str, mapping: Tuple[str, str]) -> List[Panel]:
    category, difficulty = mapping
    model_root = ROOT / "archive/ai_models" / sample
    reference = ROOT / "archive/data/reference_pdfs" / category / f"{difficulty}.pdf"
    result_root = ROOT / "archive/results" / category / difficulty
    panels = [
        Panel("reference", "Reference - pdfLaTeX", reference,
              "archived provisional reference", "ok", str(reference)),
        Panel("gemini_legacy", "Gemini - legacy manual run; version unrecorded",
              model_root / "gemini/output.pdf", "archived exploratory output", "ok",
              str(model_root / "gemini/output.pdf")),
        Panel("claude_legacy", "Claude - legacy manual run; version unrecorded",
              model_root / "claude/output.pdf", "archived exploratory output", "ok",
              str(model_root / "claude/output.pdf")),
        Panel("gpt_legacy", "OpenAI GPT - legacy manual run; version unrecorded",
              model_root / "gpt/output.pdf", "archived exploratory output",
              "ok" if (model_root / "gpt/output.pdf").exists() else "failed",
              str(model_root / "gpt/output.pdf")),
        Panel("pandoc", "Pandoc - archived deterministic engine",
              result_root / "pandoc.pdf", "archived as-tested output", "ok",
              str(result_root / "pandoc.pdf")),
        Panel("tylax", "Tylax - archived deterministic engine",
              result_root / "tylax.pdf", "archived as-tested output", "ok",
              str(result_root / "tylax.pdf")),
        Panel("typetex", "TypeTeX - archived deterministic engine",
              result_root / "typetex_approx.pdf", "archived as-tested output", "ok",
              str(result_root / "typetex_approx.pdf")),
    ]
    for panel in panels:
        if panel.candidate != "reference" and (not panel.path or not panel.path.exists()):
            panel.path = None
            panel.state = "failed"
            panel.status = "compile failed or artifact missing in archived run"
    note = (
        "ARCHIVED PROVISIONAL BENCHMARK\n\n"
        "These outputs predate latex_benchmark_v0. Model versions and prompting were not "
        "recorded consistently, and the old 15-category corpus is no longer canonical. "
        "This appendix is visual provenance only and must not be compared numerically with "
        "the current benchmark or dataset-expansion sections."
    )
    panels.append(Panel("scope", "Scope and comparability", None, note, "info"))
    return panels


def add_cover(document: fitz.Document) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, fill=(0.975, 0.98, 0.985), color=None)
    page.draw_rect(fitz.Rect(0, 0, 18, PAGE_H), fill=(0.10, 0.33, 0.50), color=None)
    page.insert_text((60, 94), "All models and engines", fontsize=31, fontname="helv",
                     color=(0.08, 0.13, 0.18))
    page.insert_text((60, 136), "Reference-aligned LaTeX-to-Typst visual grid", fontsize=19,
                     fontname="helv", color=(0.20, 0.32, 0.41))
    intro = (
        "A consolidated visual review of every model and deterministic-engine family with "
        "rendered artifacts in this repository. Every populated panel embeds the complete "
        "available PDF; multi-page documents are tiled. Failed and not-evaluated candidates "
        "remain visible as labeled cells.\n\n"
        "The report is partitioned by evidence regime to prevent false comparisons."
    )
    fit_text(page, fitz.Rect(60, 180, 900, 310), intro, size=12, minimum=10)
    rows = (
        ("Part I", "Current canonical hard set", "8 samples", "Gemini, Claude Sonnet, Claude Opus, Pandoc, Tylax, TypeTeX"),
        ("Part II", "Dataset-expansion stress test", "6 samples", "Claude Sonnet and Claude Opus; other candidates explicitly not run"),
        ("Appendix", "Archived provisional benchmark", "8 samples", "Legacy Gemini, Claude, GPT, Pandoc, Tylax, TypeTeX"),
    )
    y = 350
    for part, title, count, detail in rows:
        page.draw_rect(fitz.Rect(60, y, 1145, y + 76), color=(0.76, 0.80, 0.83),
                       fill=(1, 1, 1), width=0.7)
        page.insert_text((78, y + 23), part, fontsize=9, fontname="helv",
                         color=(0.10, 0.33, 0.50))
        page.insert_text((180, y + 25), title, fontsize=15, fontname="helv",
                         color=(0.10, 0.14, 0.18))
        page.insert_text((970, y + 25), count, fontsize=10, fontname="helv",
                         color=(0.35, 0.38, 0.41))
        fit_text(page, fitz.Rect(180, y + 38, 1110, y + 67), detail, size=8,
                 color=(0.34, 0.37, 0.40))
        y += 90
    page.insert_text((60, PAGE_H - 30), "Generated from repository artifacts; no paid model calls.",
                     fontsize=8, fontname="helv", color=(0.42, 0.44, 0.47))


def add_divider(document: fitz.Document, title: str, subtitle: str, body: str) -> None:
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, fill=(0.975, 0.98, 0.985), color=None)
    page.draw_rect(fitz.Rect(0, 0, PAGE_W, 18), fill=(0.10, 0.33, 0.50), color=None)
    page.insert_text((60, 125), title, fontsize=29, fontname="helv", color=(0.08, 0.13, 0.18))
    page.insert_text((60, 168), subtitle, fontsize=17, fontname="helv", color=(0.20, 0.32, 0.41))
    fit_text(page, fitz.Rect(60, 225, 1080, 520), body, size=12, minimum=10)


def add_sample_page(
    document: fitz.Document,
    section: str,
    sample: str,
    panels: List[Panel],
    manifest_rows: List[dict],
) -> None:
    if len(panels) != 8:
        raise ValueError(f"{sample}: expected 8 panels, got {len(panels)}")
    page = document.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, fill=(0.985, 0.988, 0.991), color=None)
    page.insert_text((30, 27), sample, fontsize=15, fontname="helv", color=(0.08, 0.13, 0.18))
    page.insert_text((30, 45), section, fontsize=8, fontname="helv", color=(0.35, 0.39, 0.42))
    page.draw_line((30, 54), (PAGE_W - 30, 54), color=(0.75, 0.78, 0.81), width=0.6)
    report_page = document.page_count
    for rect, panel in zip(panel_rects(), panels):
        page_count = draw_panel(page, rect, panel)
        manifest_rows.append({
            "section": section,
            "sample_id": sample,
            "candidate": panel.candidate,
            "label": panel.label,
            "state": panel.state,
            "status": panel.status,
            "source_artifact": portable_artifact_path(panel.source),
            "embedded_pdf": embedded_artifact_label(panel.path),
            "embedded_pages": page_count,
            "report_page": report_page,
        })
    page.insert_text((PAGE_W - 118, PAGE_H - 9), f"report page {report_page}", fontsize=6,
                     fontname="helv", color=(0.45, 0.47, 0.49))


def write_manifest(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def portable_artifact_path(value: str) -> str:
    if not value:
        return ""
    path = Path(value)
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def embedded_artifact_label(path: Optional[Path]) -> str:
    if not path:
        return ""
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        return str(path)
    if relative.parts[:3] == ("tmp", "pdfs", "all_models_engine_grid"):
        return "temporary Typst compile embedded in report"
    return str(relative)


def main() -> None:
    args = parse_args()
    if args.tmp.exists():
        shutil.rmtree(args.tmp)
    args.tmp.mkdir(parents=True, exist_ok=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)

    document = fitz.open()
    manifest_rows: List[dict] = []
    toc = [[1, "All models and engines", 1]]
    add_cover(document)

    add_divider(
        document,
        "Part I - Current canonical hard set",
        "Direct same-sample visual comparison",
        "Eight difficult latex_benchmark_v0 samples with a shared pdfLaTeX reference. "
        "The six core harness samples include agentic Claude outputs; two extra math samples "
        "have one-turn Claude outputs. Gemini uses the stored prompt cascade, and all three "
        "deterministic engines are shown when they compiled.",
    )
    toc.append([1, "Part I - Current canonical hard set", document.page_count])
    engines = engine_index()
    for sample in CANONICAL_SAMPLES:
        add_sample_page(document, "current canonical hard set", sample,
                        canonical_panels(args.tmp, sample, engines), manifest_rows)
        toc.append([2, sample, document.page_count])

    add_divider(
        document,
        "Part II - Dataset-expansion stress test",
        "Harder source-backed candidates from four external datasets",
        "Six hard picks from the merged dataset-expansion PR. Claude Sonnet one-turn compiled "
        "only one of these six; Claude Opus in the visual v3 harness compiled all six. Gemini "
        "and deterministic engines were not run, so their cells are explicitly marked rather "
        "than inferred. References were compiled with Tectonic.",
    )
    toc.append([1, "Part II - Dataset-expansion stress test", document.page_count])
    for sample in EXPANSION_SAMPLES:
        add_sample_page(document, "dataset-expansion stress test", sample,
                        expansion_panels(args.tmp, sample), manifest_rows)
        toc.append([2, sample, document.page_count])

    add_divider(
        document,
        "Appendix - Archived provisional benchmark",
        "Legacy model coverage, retained as visual provenance",
        "The old exploratory corpus contains the repository's only GPT renders and additional "
        "legacy Gemini and Claude outputs. Model versions were not consistently recorded. "
        "These pages are therefore isolated from the canonical benchmark and must not be used "
        "for cross-section quantitative claims.",
    )
    toc.append([1, "Appendix - Archived provisional benchmark", document.page_count])
    for sample, mapping in LEGACY_SAMPLES.items():
        add_sample_page(document, "archived provisional benchmark", sample,
                        legacy_panels(sample, mapping), manifest_rows)
        toc.append([2, sample, document.page_count])

    document.set_toc(toc)
    document.set_metadata({
        "title": "All models and engines - reference-aligned visual grid",
        "subject": "LaTeX-to-Typst model and deterministic-engine comparison",
        "author": "Lathe benchmark",
    })
    document.save(args.out, garbage=4, deflate=True)
    page_count = document.page_count
    document.close()
    write_manifest(args.manifest, manifest_rows)

    if not args.keep_assets:
        shutil.rmtree(args.tmp)

    print(f"pdf: {args.out}")
    print(f"manifest: {args.manifest}")
    print(f"pages: {page_count}")
    print(f"candidate cells: {len(manifest_rows)}")


if __name__ == "__main__":
    main()
