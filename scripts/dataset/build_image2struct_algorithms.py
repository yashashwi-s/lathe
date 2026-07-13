#!/usr/bin/env python3
"""Build algorithm samples from stanford-crfm/image2struct-latex-v1.

Run with:
  mamba run -n lathe python scripts/dataset/build_image2struct_algorithms.py
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

import fitz
from datasets import load_dataset


OUT_DIR = Path("data/simple_benchmark_algorithms")
DATASET = "stanford-crfm/image2struct-latex-v1"
FILES = [
    f"hf://datasets/{DATASET}/algorithm/validation-00000-of-00001.parquet",
    f"hf://datasets/{DATASET}/algorithm/test-00000-of-00001.parquet",
]


@dataclass
class Record:
    sample_id: str
    category: str
    source_family: str
    source_dataset: str
    source_id: str
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
            if not isinstance(raw, str):
                raw = raw.decode("utf-8", errors="replace")
            return False, raw + "\nTIMEOUT\n", time.monotonic() - start
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


def clean_algorithm(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\\begin\{algorithmic\}\s*\n?\[1\]", r"\\begin{algorithmic}[1]", text)
    text = re.sub(r"\\begin\{algorithmic\}\s+\[1\]", r"\\begin{algorithmic}[1]", text)
    return text


def build_tex(algorithm_text: str, idx: int) -> str:
    algorithm_text = clean_algorithm(algorithm_text)
    if "\\begin{algorithmic}" not in algorithm_text:
        algorithm_text = "\\begin{algorithmic}[1]\n" + algorithm_text + "\n\\end{algorithmic}"
    return r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithm}
\usepackage{algpseudocode}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\title{Algorithmic Pseudocode Sample %d}
\author{Source-backed Image2Struct algorithm sample}
\date{}
\begin{document}
\maketitle
\section{Algorithm}
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

\begin{algorithm}[htbp]
\caption{Source-backed algorithmic procedure}
%s
\end{algorithm}
\end{document}
""" % (idx, algorithm_text)


def compile_sample(out_dir: Path, sample_id: str, tex: str, source_id: str, timeout: int, max_pages: int) -> Record:
    category = "09_algorithms"
    sample_dir = out_dir / "corpus" / category / sample_id
    if sample_dir.exists():
        shutil.rmtree(sample_dir)
    sample_dir.mkdir(parents=True, exist_ok=True)
    write_text(sample_dir / "main.tex", tex)
    ok, log, seconds = run_pdflatex(sample_dir, timeout)
    write_text(sample_dir / "compile.log", log)
    pdf = sample_dir / "main.pdf"
    ref = sample_dir / "reference.pdf"
    status = "accepted"
    reason = "accepted"
    pages = 0
    sha_pdf = ""
    if not ok or not pdf.exists() or pdf.stat().st_size == 0:
        status = "rejected"
        reason = "pdflatex_failed"
    else:
        try:
            pages = pdf_page_count(pdf)
        except Exception:
            status = "rejected"
            reason = "invalid_pdf"
        if status == "accepted" and (pages < 1 or pages > max_pages):
            status = "rejected"
            reason = f"page_count_{pages}"
        if status == "accepted":
            shutil.move(str(pdf), str(ref))
            sha_pdf = sha256_file(ref)

    sha_src = sha256_file(sample_dir / "main.tex")
    provenance = {
        "sample_id": sample_id,
        "category": category,
        "source_family": "hf_extracted",
        "source_dataset": DATASET,
        "source_id": source_id,
        "compile_engine": "pdflatex",
        "compile_command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex",
        "compile_seconds": round(seconds, 3),
        "page_count": pages,
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

    return Record(
        sample_id=sample_id,
        category=category,
        source_family="hf_extracted",
        source_dataset=DATASET,
        source_id=source_id,
        status=status,
        reason=reason,
        page_count=pages,
        compile_seconds=seconds,
        nonblank_lines=nonblank_lines(tex),
        source_chars=len(tex),
        sha256_source=sha_src,
        sha256_pdf=sha_pdf,
        sample_dir=str(sample_dir),
    )


def load_algorithm_rows(scan_limit: int) -> list[dict]:
    rows = []
    seen = set()
    idx_global = 0
    for file in FILES:
        ds = load_dataset("parquet", data_files=file, split="train", streaming=True)
        ds = ds.select_columns(["text"])
        for idx, row in enumerate(ds):
            if idx_global >= scan_limit:
                break
            idx_global += 1
            text = clean_algorithm(row.get("text", ""))
            if not text or text in seen:
                continue
            seen.add(text)
            if len(text) < 180 or len(text) > 3000:
                continue
            if any(bad in text for bad in ["\\includegraphics", "\\input", "\\write18", "\\begin{tikzpicture}"]):
                continue
            score = text.count("\\State") * 20 + text.count("\\For") * 15 + text.count("\\If") * 15 + len(text) // 20
            rows.append({"id": f"image2struct-algorithm-{idx_global}", "text": text, "score": score})
        if idx_global >= scan_limit:
            break
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows


def write_manifests(records: list[Record], out_dir: Path) -> None:
    manifest_dir = out_dir / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    fields = list(asdict(records[0]).keys()) if records else [field.name for field in Record.__dataclass_fields__.values()]
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


def add_preview_page(out: fitz.Document, record: Record) -> None:
    src = fitz.open(Path(record.sample_dir) / "reference.pdf")
    try:
        page = out.new_page(width=842, height=595)
        margin = 24
        header_h = 74
        title = f"{record.sample_id} | {record.category} | {record.page_count} page(s)"
        meta = f"Dataset: {record.source_dataset}\nSource ID: {record.source_id}\nSource: {record.nonblank_lines} nonblank lines, {record.source_chars} chars"
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
    finally:
        src.close()


def build_preview(records: list[Record], out_dir: Path) -> Path:
    accepted = [r for r in records if r.status == "accepted"]
    preview = out_dir / "previews" / "algorithms_preview.pdf"
    preview.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    try:
        for record in accepted:
            add_preview_page(doc, record)
        doc.save(preview)
    finally:
        doc.close()
    return preview


def write_summary(records: list[Record], out_dir: Path) -> None:
    accepted = [r for r in records if r.status == "accepted"]
    rejected = [r for r in records if r.status != "accepted"]
    lines = [
        "# Algorithm Category Slice",
        "",
        f"Accepted samples: {len(accepted)}",
        f"Rejected samples: {len(rejected)}",
        "",
        "Source: `stanford-crfm/image2struct-latex-v1`",
        "",
        "Rows are wrapped into minimal article documents with `algorithm` and `algpseudocode` packages.",
    ]
    write_text(out_dir / "summary.md", "\n".join(lines) + "\n")


def build(args: argparse.Namespace) -> None:
    args.out.mkdir(parents=True, exist_ok=True)
    print("collecting algorithm rows", flush=True)
    rows = load_algorithm_rows(args.scan_limit)
    print(f"candidate rows: {len(rows)}", flush=True)
    records: list[Record] = []
    accepted = 0
    for idx, row in enumerate(rows, start=1):
        if accepted >= args.samples:
            break
        sample_id = f"09_algorithms_{idx:03d}"
        tex = build_tex(row["text"], idx)
        rec = compile_sample(args.out, sample_id, tex, row["id"], args.timeout, args.max_pages)
        records.append(rec)
        if rec.status == "accepted":
            accepted += 1
            print(f"accepted {sample_id}", flush=True)
    write_manifests(records, args.out)
    write_summary(records, args.out)
    preview = build_preview(records, args.out)
    print(f"summary: {args.out / 'summary.md'}", flush=True)
    print(f"preview: {preview}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    parser.add_argument("--samples", type=int, default=30)
    parser.add_argument("--scan-limit", type=int, default=500)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-pages", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    build(parse_args())


if __name__ == "__main__":
    main()
