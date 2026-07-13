#!/usr/bin/env python3
"""Build the first simple, source-backed LaTeX benchmark slice.

This starts with the strongest Hugging Face sources:
- OleehyO/latex-formulas for grouped math documents
- piushorn/arxiv-latex-tables-43k for grouped table documents

Run with:
  mamba run -n lathe python scripts/dataset/build_simple_benchmark_v0.py
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import fitz
from datasets import load_dataset


OUT_DIR = Path("data/simple_benchmark_v0")

TABLES_REPO = "piushorn/arxiv-latex-tables-43k"
TABLES_FILE = f"hf://datasets/{TABLES_REPO}/data/train-00000-of-00001.parquet"

FORMULAS_REPO = "OleehyO/latex-formulas"
FORMULAS_FILES = [
    f"hf://datasets/{FORMULAS_REPO}/cleaned_formulas/train-00000-of-00006.parquet"
]


@dataclass
class SampleRecord:
    sample_id: str
    category: str
    source_family: str
    source_dataset: str
    source_ids: str
    status: str
    reason: str
    page_count: int
    compile_seconds: float
    nonblank_lines: int
    source_chars: int
    sha256_source: str
    sha256_pdf: str
    sample_dir: str


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slug(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text[:80] or "sample"


def nonblank_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def run_pdflatex(sample_dir: Path, timeout: int) -> tuple[bool, str, float]:
    start = time.monotonic()
    cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    logs = []
    ok = True
    for _ in range(2):
        try:
            proc = subprocess.run(
                cmd,
                cwd=sample_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            raw = exc.stdout or b""
            if isinstance(raw, str):
                decoded = raw
            else:
                decoded = raw.decode("utf-8", errors="replace")
            return False, decoded + "\nTIMEOUT\n", time.monotonic() - start
        logs.append((proc.stdout or b"").decode("utf-8", errors="replace"))
        if proc.returncode != 0:
            ok = False
            break
    return ok, "\n\n--- pass break ---\n\n".join(logs), time.monotonic() - start


def pdf_page_count(path: Path) -> int:
    doc = fitz.open(path)
    try:
        return doc.page_count
    finally:
        doc.close()


def normalize_formula(formula: str) -> str:
    formula = formula.strip()
    formula = re.sub(r"\\mbox\{([^}]*)\}", r"\\text{\1}", formula)
    formula = re.sub(r"\\textrm\{([^}]*)\}", r"\\mathrm{\1}", formula)
    return formula


def formula_kind(formula: str) -> str:
    if re.search(r"\\begin\{(?:aligned|cases|array|matrix|pmatrix|bmatrix|vmatrix|Vmatrix)", formula):
        return "aligned"
    inner = re.sub(r"\\begin\{align\*\}|\\end\{align\*\}|\\begin\{align\}|\\end\{align\}", "", formula)
    if "\\\\" in inner or "&" in inner:
        return "aligned"
    return "inline_display"


def formula_score(formula: str) -> int:
    score = len(formula)
    score += 80 if formula_kind(formula) == "aligned" else 0
    score -= 300 if len(formula) > 900 else 0
    score -= 500 if any(token in formula for token in ["\\includegraphics", "\\begin{tikzpicture}", "\\input", "\\write18"]) else 0
    return score


def formula_body(formula: str) -> str:
    formula = normalize_formula(formula)
    if re.search(r"\\begin\{(?:equation|equation\*|align|align\*|gather|gather\*|multline|multline\*)\}", formula):
        return formula
    if re.search(r"\\begin\{(?:aligned|cases|matrix|pmatrix|bmatrix|array)\}", formula):
        return "\\[\n" + formula + "\n\\]"
    if formula.startswith("$") or formula.startswith("\\["):
        return formula
    return "\\[\n" + formula + "\n\\]"


def build_formula_tex(category: str, formulas: list[dict]) -> str:
    title = "Inline and Display Mathematics" if category == "03_math_inline_display" else "Aligned Mathematical Structures"
    chunks = []
    for i, item in enumerate(formulas, start=1):
        chunks.append(
            "\\paragraph{Expression %d.} The following expression is taken from a source-backed formula corpus.\n\n%s"
            % (i, formula_body(item["latex_formula"]))
        )
    return r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts,mathtools,bm}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\title{%s}
\author{Source-backed grouped formula sample}
\date{}
\begin{document}
\maketitle
\section{Expressions}
%s
\end{document}
""" % (title, "\n\n".join(chunks))


def table_complexity(tabular: str) -> str:
    if re.search(r"\\multirow|\\multicolumn|\\cline|\\cmidrule|\\toprule|\\midrule|\\bottomrule|\\Xhline|\\makecell", tabular):
        return "moderate"
    return "simple"


def table_score(tabular: str) -> int:
    rows = tabular.count("\\\\")
    cols = max((len(line.split("&")) for line in tabular.splitlines() if "&" in line), default=1)
    score = rows * 20 + cols * 15 + len(tabular) // 20
    if len(tabular) > 6000:
        score -= 600
    if "\\begin{longtable}" in tabular:
        score -= 200
    return score


def sanitize_table(tabular: str) -> str:
    tabular = tabular.strip()
    # Keep original source as much as possible. These packages cover most table macros.
    return tabular


def build_table_tex(category: str, tables: list[dict]) -> str:
    title = "Simple Tables" if category == "05_tables_simple" else "Moderate Tables"
    chunks = []
    for i, item in enumerate(tables, start=1):
        tabular = sanitize_table(item["tabular"])
        chunks.append(
            r"""\begin{table}[htbp]
\centering
\caption{Source table %d: %s}
\resizebox{\linewidth}{!}{%%
%s
}
\end{table}
""" % (i, item["table_id"].replace("_", "\\_"), tabular)
        )
    return r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{array,booktabs,makecell,multirow,tabularx,longtable,colortbl,xcolor,graphicx}
\usepackage{arydshln}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\title{%s}
\author{Source-backed grouped table sample}
\date{}
\begin{document}
\maketitle
\section{Tables}
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

%s
\end{document}
""" % (title, "\n\n".join(chunks))


def compile_sample(
    out_dir: Path,
    category: str,
    sample_id: str,
    tex: str,
    source_family: str,
    source_dataset: str,
    source_ids: list[str],
    timeout: int,
    max_pages: int,
) -> SampleRecord:
    sample_dir = out_dir / "corpus" / category / sample_id
    if sample_dir.exists():
        shutil.rmtree(sample_dir)
    sample_dir.mkdir(parents=True, exist_ok=True)
    write_text(sample_dir / "main.tex", tex)
    ok, log, seconds = run_pdflatex(sample_dir, timeout=timeout)
    write_text(sample_dir / "compile.log", log)

    pdf = sample_dir / "main.pdf"
    reference = sample_dir / "reference.pdf"
    reason = "accepted"
    status = "accepted"
    page_count = 0
    sha_pdf = ""
    if not ok or not pdf.exists() or pdf.stat().st_size == 0:
        status = "rejected"
        reason = "pdflatex_failed"
    else:
        try:
            page_count = pdf_page_count(pdf)
        except Exception:
            status = "rejected"
            reason = "invalid_pdf"
        if status == "accepted" and (page_count < 1 or page_count > max_pages):
            status = "rejected"
            reason = f"page_count_{page_count}"
        if status == "accepted":
            shutil.move(str(pdf), str(reference))
            sha_pdf = sha256_file(reference)

    sha_src = sha256_file(sample_dir / "main.tex")
    provenance = {
        "sample_id": sample_id,
        "category": category,
        "source_family": source_family,
        "source_dataset": source_dataset,
        "source_ids": source_ids,
        "compile_engine": "pdflatex",
        "compile_command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex",
        "compile_seconds": round(seconds, 3),
        "page_count": page_count,
        "sha256_source": sha_src,
        "sha256_pdf": sha_pdf,
    }
    write_text(sample_dir / "provenance.json", json.dumps(provenance, indent=2))

    if status != "accepted":
        rejected_dir = out_dir / "rejected" / category / sample_id
        if rejected_dir.exists():
            shutil.rmtree(rejected_dir)
        rejected_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(sample_dir), str(rejected_dir))
        sample_dir = rejected_dir

    return SampleRecord(
        sample_id=sample_id,
        category=category,
        source_family=source_family,
        source_dataset=source_dataset,
        source_ids=";".join(source_ids),
        status=status,
        reason=reason,
        page_count=page_count,
        compile_seconds=seconds,
        nonblank_lines=nonblank_lines(tex),
        source_chars=len(tex),
        sha256_source=sha_src,
        sha256_pdf=sha_pdf,
        sample_dir=str(sample_dir),
    )


def batched(items: list[dict], size: int) -> Iterable[list[dict]]:
    for i in range(0, len(items), size):
        yield items[i:i + size]


def collect_formulas(limit: int) -> tuple[list[dict], list[dict]]:
    ds = load_dataset("parquet", data_files=FORMULAS_FILES, split="train", streaming=True)
    ds = ds.select_columns(["latex_formula"])
    inline: list[dict] = []
    aligned: list[dict] = []
    seen = set()
    max_rows = max(5000, limit * 100)
    for idx, row in enumerate(ds):
        if idx >= max_rows:
            break
        formula = normalize_formula(row.get("latex_formula", ""))
        if not formula or formula in seen:
            continue
        seen.add(formula)
        if len(formula) < 25 or len(formula) > 800:
            continue
        if any(bad in formula for bad in ["\\includegraphics", "\\begin{tikzpicture}", "\\input", "\\href", "\\url"]):
            continue
        item = {"id": f"latex-formulas-{idx}", "latex_formula": formula, "score": formula_score(formula)}
        if formula_kind(formula) == "aligned":
            aligned.append(item)
        else:
            inline.append(item)
        if len(inline) >= limit and len(aligned) >= limit:
            break
        if idx and idx % 1000 == 0:
            print(f"scanned formulas: {idx} inline={len(inline)} aligned={len(aligned)}", flush=True)
    inline.sort(key=lambda x: x["score"], reverse=True)
    aligned.sort(key=lambda x: x["score"], reverse=True)
    return inline[:limit], aligned[:limit]


def collect_tables(limit: int) -> tuple[list[dict], list[dict]]:
    ds = load_dataset("parquet", data_files=TABLES_FILE, split="train", streaming=True)
    ds = ds.select_columns(["table_id", "tabular", "complexity"])
    simple: list[dict] = []
    moderate: list[dict] = []
    seen = set()
    max_rows = max(5000, limit * 100)
    for idx, row in enumerate(ds):
        if idx >= max_rows:
            break
        tabular = row.get("tabular", "")
        table_id = row.get("table_id", "")
        if not tabular or tabular in seen:
            continue
        seen.add(tabular)
        if len(tabular) < 150 or len(tabular) > 5000:
            continue
        if any(bad in tabular for bad in ["\\input", "\\includegraphics", "\\begin{tikzpicture}"]):
            continue
        item = {
            "table_id": str(table_id),
            "tabular": tabular,
            "complexity": row.get("complexity", ""),
            "score": table_score(tabular),
        }
        comp = table_complexity(tabular)
        if comp == "simple":
            simple.append(item)
        elif comp == "moderate":
            moderate.append(item)
        if len(simple) >= limit and len(moderate) >= limit:
            break
    simple.sort(key=lambda x: x["score"], reverse=True)
    moderate.sort(key=lambda x: x["score"], reverse=True)
    return simple[:limit], moderate[:limit]


def write_manifest(records: list[SampleRecord], out_dir: Path) -> None:
    manifest_dir = out_dir / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    fields = list(asdict(records[0]).keys()) if records else [field.name for field in SampleRecord.__dataclass_fields__.values()]
    for name, subset in {
        "all.csv": records,
        "accepted.csv": [r for r in records if r.status == "accepted"],
        "rejected.csv": [r for r in records if r.status != "accepted"],
    }.items():
        with (manifest_dir / name).open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for record in subset:
                writer.writerow(asdict(record))


def add_preview_page(out: fitz.Document, record: SampleRecord) -> None:
    pdf_path = Path(record.sample_dir) / "reference.pdf"
    src = fitz.open(pdf_path)
    try:
        page = out.new_page(width=842, height=595)
        margin = 24
        header_h = 78
        title = f"{record.sample_id}  |  {record.category}  |  {record.page_count} page(s)"
        meta = (
            f"Dataset: {record.source_dataset}\n"
            f"Source IDs: {record.source_ids[:180]}\n"
            f"Source: {record.nonblank_lines} nonblank lines, {record.source_chars} chars"
        )
        page.insert_text((margin, 24), title, fontsize=13, fontname="helv")
        page.insert_textbox(fitz.Rect(margin, 38, 818, margin + header_h), meta, fontsize=7, fontname="helv")
        page.draw_line((margin, margin + header_h), (818, margin + header_h), color=(0.75, 0.75, 0.75))

        n = src.page_count
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)
        grid = fitz.Rect(margin, margin + header_h + 14, 818, 571)
        gap = 12
        cell_w = (grid.width - gap * (cols - 1)) / cols
        cell_h = (grid.height - gap * (rows - 1)) / rows
        for idx in range(n):
            row = idx // cols
            col = idx % cols
            cell = fitz.Rect(
                grid.x0 + col * (cell_w + gap),
                grid.y0 + row * (cell_h + gap),
                grid.x0 + col * (cell_w + gap) + cell_w,
                grid.y0 + row * (cell_h + gap) + cell_h,
            )
            sp = src.load_page(idx)
            scale = min(cell.width / sp.rect.width, cell.height / sp.rect.height)
            w = sp.rect.width * scale
            h = sp.rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - w) / 2,
                cell.y0 + (cell.height - h) / 2,
                cell.x0 + (cell.width + w) / 2,
                cell.y0 + (cell.height + h) / 2,
            )
            page.show_pdf_page(target, src, idx)
            page.draw_rect(target, color=(0.55, 0.55, 0.55), width=0.6)
            page.insert_text((target.x0, max(target.y0 - 3, grid.y0 - 2)), f"p{idx + 1}", fontsize=6)
    finally:
        src.close()


def build_preview(records: list[SampleRecord], out_dir: Path) -> Path:
    accepted = [r for r in records if r.status == "accepted"]
    accepted.sort(key=lambda r: (r.category, r.sample_id))
    preview = out_dir / "previews" / "simple_benchmark_v0_preview.pdf"
    preview.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    try:
        for record in accepted:
            add_preview_page(doc, record)
        doc.save(preview)
    finally:
        doc.close()
    return preview


def write_summary(records: list[SampleRecord], out_dir: Path) -> None:
    accepted = [r for r in records if r.status == "accepted"]
    rejected = [r for r in records if r.status != "accepted"]
    by_cat: dict[str, int] = {}
    for record in accepted:
        by_cat[record.category] = by_cat.get(record.category, 0) + 1
    lines = [
        "# Simple Benchmark v0 Summary",
        "",
        f"Accepted samples: {len(accepted)}",
        f"Rejected samples: {len(rejected)}",
        "",
        "## Accepted By Category",
        "",
    ]
    for cat, count in sorted(by_cat.items()):
        lines.append(f"- `{cat}`: {count}")
    lines.extend([
        "",
        "## Sources",
        "",
        f"- Tables: `{TABLES_REPO}`",
        f"- Formulas: `{FORMULAS_REPO}`",
        "",
        "## Notes",
        "",
        "- This is an initial HF-backed slice, not the full final dataset.",
        "- Formula/table rows are grouped into 1-3 page documents so samples are not one-liners.",
        "- All accepted samples compiled with `pdflatex` locally.",
    ])
    write_text(out_dir / "summary.md", "\n".join(lines) + "\n")


def build(args: argparse.Namespace) -> None:
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    records: list[SampleRecord] = []

    print("collecting formulas", flush=True)
    inline, aligned = collect_formulas(args.formula_scan_limit)
    print(f"formula pools: inline={len(inline)} aligned={len(aligned)}", flush=True)
    formula_specs = [
        ("03_math_inline_display", inline, args.math_samples, args.formulas_per_sample),
        ("04_math_aligned", aligned, args.math_samples, args.formulas_per_sample),
    ]
    for category, pool, target_samples, group_size in formula_specs:
        accepted = 0
        for idx, group in enumerate(batched(pool, group_size), start=1):
            if accepted >= target_samples:
                break
            if len(group) < group_size:
                continue
            sample_id = f"{category}_{idx:03d}"
            tex = build_formula_tex(category, group)
            record = compile_sample(
                out_dir, category, sample_id, tex,
                "hf_extracted", FORMULAS_REPO,
                [item["id"] for item in group],
                args.timeout, args.max_pages,
            )
            records.append(record)
            if record.status == "accepted":
                accepted += 1
                print(f"accepted {sample_id}", flush=True)

    print("collecting tables", flush=True)
    simple, moderate = collect_tables(args.table_scan_limit)
    print(f"table pools: simple={len(simple)} moderate={len(moderate)}", flush=True)
    table_specs = [
        ("05_tables_simple", simple, args.table_samples, args.tables_per_sample),
        ("06_tables_moderate", moderate, args.table_samples, args.tables_per_sample),
    ]
    for category, pool, target_samples, group_size in table_specs:
        accepted = 0
        for idx, group in enumerate(batched(pool, group_size), start=1):
            if accepted >= target_samples:
                break
            if len(group) < group_size:
                continue
            sample_id = f"{category}_{idx:03d}"
            tex = build_table_tex(category, group)
            record = compile_sample(
                out_dir, category, sample_id, tex,
                "hf_extracted", TABLES_REPO,
                [item["table_id"] for item in group],
                args.timeout, args.max_pages,
            )
            records.append(record)
            if record.status == "accepted":
                accepted += 1
                print(f"accepted {sample_id}", flush=True)

    write_manifest(records, out_dir)
    write_summary(records, out_dir)
    preview = build_preview(records, out_dir)
    print(f"summary: {out_dir / 'summary.md'}", flush=True)
    print(f"preview: {preview}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    parser.add_argument("--math-samples", type=int, default=10)
    parser.add_argument("--table-samples", type=int, default=10)
    parser.add_argument("--formulas-per-sample", type=int, default=5)
    parser.add_argument("--tables-per-sample", type=int, default=2)
    parser.add_argument("--formula-scan-limit", type=int, default=500)
    parser.add_argument("--table-scan-limit", type=int, default=500)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-pages", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    build(parse_args())


if __name__ == "__main__":
    main()
