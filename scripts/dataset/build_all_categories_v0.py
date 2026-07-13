#!/usr/bin/env python3
"""Build one source-backed, category-balanced LaTeX benchmark directory.

This script assembles already validated HF slices and fills the missing simple
categories from the `scholarweave/arxiv-latex` HF corpus. It keeps the first
benchmark intentionally modest: pdfLaTeX only, 1-3 rendered pages, and no
diagram-heavy stress categories.

Run with:
  mamba run -n lathe python scripts/dataset/build_all_categories_v0.py
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


OUT_DIR = Path("data/latex_benchmark_v0")
SCHOLARWEAVE = "scholarweave/arxiv-latex"

SOURCE_SLICES = [
    Path("archive/dataset_intermediate_corpora_2026-07-13/simple_benchmark_v0_160"),
    Path("archive/dataset_intermediate_corpora_2026-07-13/simple_benchmark_algorithms"),
]

TARGETS = {
    "01_prose_sections": 15,
    "02_lists_formatting": 15,
    "03_math_inline_display": 18,
    "04_math_aligned": 15,
    "05_tables_simple": 18,
    "06_tables_moderate": 18,
    "07_figures_captions": 15,
    "08_crossrefs_citations": 15,
    "09_algorithms": 12,
    "10_compact_papers": 15,
    "11_forms_cv_letters": 10,
}

SCHOLARWEAVE_TARGETS = {
    "01_prose_sections",
    "02_lists_formatting",
    "07_figures_captions",
    "08_crossrefs_citations",
    "10_compact_papers",
}

DEFERRED = {
    "12_diagrams_plots_stress": "Deferred by design; TikZ/PGFPlots/diagram categories should be a later stress set, not the first simple benchmark.",
}

TEXLIVE_FORM_SOURCES = [
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/europecv/templates/cv_template_academic_en.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/europecv/templates/cv_template_en.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-14.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-2.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-3.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-15.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-1.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-0.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-12.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-4.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-5.tex"),
    Path("/usr/local/texlive/2026/texmf-dist/doc/latex/koma-script-examples/Kapitel-4/source/letter-13.tex"),
]


@dataclass
class Record:
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def nonblank_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        line = re.sub(r"(?<!\\)%.*", "", line)
        if line.strip():
            lines.append(line.rstrip())
    return "\n".join(lines)


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def clean_text(text: str, limit: int = 1400) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    text = text.replace("\x00", "")
    if len(text) > limit:
        cut = text[:limit]
        if "." in cut:
            cut = cut[: cut.rfind(".") + 1]
        text = cut
    return latex_escape(text)


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


def tex_preamble(title: str, author: str = "Source-backed arXiv sample") -> str:
    return r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts,mathtools}
\usepackage{array,booktabs,enumitem,graphicx,xcolor,hyperref}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\title{%s}
\author{%s}
\date{}
\begin{document}
\maketitle
""" % (latex_escape(title)[:180], latex_escape(author)[:180])


def tex_end() -> str:
    return "\n\\end{document}\n"


def compile_generated(
    out_dir: Path,
    category: str,
    sample_id: str,
    tex: str,
    source_dataset: str,
    source_ids: str,
    timeout: int,
    max_pages: int,
    source_family: str = "hf_extracted",
) -> Record:
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
        "source_family": source_family,
        "source_dataset": source_dataset,
        "source_ids": source_ids,
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
        source_family=source_family,
        source_dataset=source_dataset,
        source_ids=source_ids,
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


def copy_existing_slices(out_dir: Path) -> list[Record]:
    records: list[Record] = []
    copied_counts = {category: 0 for category in TARGETS}
    for source_root in SOURCE_SLICES:
        manifest = source_root / "manifests" / "accepted.csv"
        if not manifest.exists():
            continue
        with manifest.open(newline="", encoding="utf-8") as f:
            rows = sorted(csv.DictReader(f), key=lambda r: (r["category"], r["sample_id"]))
            for row in rows:
                src_dir = Path(row["sample_dir"])
                category = row["category"]
                if category not in TARGETS or copied_counts[category] >= TARGETS[category]:
                    continue
                sample_id = row["sample_id"]
                dst_dir = out_dir / "corpus" / category / sample_id
                if dst_dir.exists():
                    shutil.rmtree(dst_dir)
                dst_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(src_dir, dst_dir)
                source_ids = row.get("source_ids") or row.get("source_id") or ""
                rec = Record(
                    sample_id=sample_id,
                    category=category,
                    source_family=row.get("source_family", "hf_extracted"),
                    source_dataset=row.get("source_dataset", ""),
                    source_ids=source_ids,
                    status="accepted",
                    reason="accepted",
                    page_count=int(row.get("page_count") or 0),
                    compile_seconds=float(row.get("compile_seconds") or 0),
                    nonblank_lines=int(row.get("nonblank_lines") or 0),
                    source_chars=int(row.get("source_chars") or 0),
                    sha256_source=row.get("sha256_source", ""),
                    sha256_pdf=row.get("sha256_pdf", ""),
                    sample_dir=str(dst_dir),
                )
                records.append(rec)
                copied_counts[category] += 1
    return records


def env_blocks(source: str, envs: tuple[str, ...]) -> list[str]:
    found = []
    for env in envs:
        pattern = re.compile(r"\\begin\{%s\}.*?\\end\{%s\}" % (re.escape(env), re.escape(env)), re.S)
        found.extend(m.group(0) for m in pattern.finditer(source))
    return found


def captions(source: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"\\caption(?:\[[^\]]*\])?\{(.{20,700}?)\}", source, re.S)]


def bib_keys(source: str) -> list[str]:
    keys = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", source)
    if not keys:
        for cite in re.findall(r"\\cite\w*\{([^}]+)\}", source):
            keys.extend(k.strip() for k in cite.split(",") if k.strip())
    seen = []
    for key in keys:
        if key not in seen and re.match(r"^[A-Za-z0-9:._-]{2,80}$", key):
            seen.append(key)
    return seen[:6]


def plain_paragraphs_from_source(source: str, limit: int = 3) -> list[str]:
    source = strip_comments(source)
    source = re.sub(r"\\(?:section|subsection|subsubsection)\*?\{[^}]+\}", "\n\n", source)
    source = re.sub(r"\\begin\{[^}]+\}.*?\\end\{[^}]+\}", "\n\n", source, flags=re.S)
    source = re.sub(r"\$[^$]{0,300}\$", " math expression ", source)
    source = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", source)
    source = re.sub(r"[{}]", " ", source)
    paras = []
    for para in re.split(r"\n\s*\n", source):
        para = re.sub(r"\s+", " ", para).strip()
        words = para.split()
        if 35 <= len(words) <= 180:
            paras.append(latex_escape(para))
        if len(paras) >= limit:
            break
    return paras


def build_prose(row: dict) -> str:
    title = row.get("title") or row["id"]
    abstract = clean_text(row.get("abstract", ""), 1800)
    authors = clean_text(row.get("authors", ""), 300)
    paras = plain_paragraphs_from_source(row.get("latex", ""), 2)
    body = [
        "\\begin{abstract}",
        abstract,
        "\\end{abstract}",
        "\\section{Source Metadata}",
        f"This sample is based on arXiv record \\texttt{{{latex_escape(row['id'])}}}. Authors: {authors}.",
    ]
    for idx, para in enumerate(paras, 1):
        body.append(f"\\section{{Extracted Prose {idx}}}\n{para}")
    if not paras:
        body.append("\\section{Abstract Discussion}\n" + abstract)
    return tex_preamble(title) + "\n".join(body) + tex_end()


def build_lists(row: dict, blocks: list[str]) -> str:
    title = row.get("title") or row["id"]
    body = [
        "\\section{Extracted Lists}",
        "The list environments below are extracted from arXiv LaTeX source and wrapped for pdfLaTeX validation.",
    ]
    body.extend(blocks[:2])
    return tex_preamble(title) + "\n\n".join(body) + tex_end()


def build_figures(row: dict, caps: list[str]) -> str:
    title = row.get("title") or row["id"]
    body = ["\\section{Figure Captions}"]
    for idx, cap in enumerate(caps[:3], 1):
        body.append(
            r"""\begin{figure}[htbp]
\centering
\fbox{\rule{0pt}{1.15in}\rule{0.78\linewidth}{0pt}}
\caption{%s}
\label{fig:source-%d}
\end{figure}
""" % (clean_text(cap, 500), idx)
        )
    body.append("Figures~\\ref{fig:source-1} through~\\ref{fig:source-%d} preserve source-backed captions while replacing external graphics with deterministic placeholders." % min(len(caps[:3]), 3))
    return tex_preamble(title) + "\n\n".join(body) + tex_end()


def build_crossrefs(row: dict, keys: list[str]) -> str:
    title = row.get("title") or row["id"]
    key1 = keys[0]
    key2 = keys[1] if len(keys) > 1 else keys[0]
    abstract = clean_text(row.get("abstract", ""), 900)
    bibitems = []
    for idx, key in enumerate(keys[:4], 1):
        bibitems.append(r"\bibitem{%s} Source bibliography entry %d extracted from arXiv metadata/source key `%s`." % (key, idx, latex_escape(key)))
    body = r"""\begin{abstract}
%s
\end{abstract}
\section{References And Citations}
\label{sec:refs}
This sample cites source keys \cite{%s} and \cite{%s}. Section~\ref{sec:refs} and Equation~\ref{eq:source-demo} provide cross-reference coverage.
\begin{equation}
\label{eq:source-demo}
a^2 + b^2 = c^2
\end{equation}
\begin{thebibliography}{9}
%s
\end{thebibliography}
""" % (abstract, key1, key2, "\n".join(bibitems))
    return tex_preamble(title) + body + tex_end()


def build_compact(row: dict) -> str:
    title = row.get("title") or row["id"]
    abstract = clean_text(row.get("abstract", ""), 1200)
    paras = plain_paragraphs_from_source(row.get("latex", ""), 3)
    if len(paras) < 2:
        paras = [abstract, abstract]
    body = [
        "\\begin{abstract}",
        abstract,
        "\\end{abstract}",
        "\\section{Introduction}",
        paras[0],
        "\\section{Method}",
        paras[1],
        r"""\begin{equation}
\label{eq:compact}
L(\theta) = \sum_{i=1}^{n} \ell(x_i, \theta)
\end{equation}
Equation~\ref{eq:compact} is included to keep the sample paper-like while remaining small.""",
        "\\section{Conclusion}",
        paras[2] if len(paras) > 2 else paras[0],
    ]
    return tex_preamble(title, row.get("authors") or "Source-backed arXiv sample") + "\n\n".join(body) + tex_end()


def category_candidate(row: dict, counts: dict[str, int]) -> tuple[str, str] | None:
    source = row.get("latex") or ""
    if counts["02_lists_formatting"] < TARGETS["02_lists_formatting"]:
        blocks = env_blocks(source, ("itemize", "enumerate", "description"))
        blocks = [b for b in blocks if 80 <= len(b) <= 2500 and "\\input" not in b]
        if blocks:
            return "02_lists_formatting", build_lists(row, blocks)
    if counts["07_figures_captions"] < TARGETS["07_figures_captions"]:
        caps = captions(source)
        caps = [c for c in caps if 40 <= len(c) <= 700 and "\\" not in c[:20]]
        if caps:
            return "07_figures_captions", build_figures(row, caps)
    if counts["08_crossrefs_citations"] < TARGETS["08_crossrefs_citations"]:
        keys = bib_keys(source)
        if keys:
            return "08_crossrefs_citations", build_crossrefs(row, keys)
    if counts["10_compact_papers"] < TARGETS["10_compact_papers"]:
        paras = plain_paragraphs_from_source(source, 2)
        if len(paras) >= 2 and row.get("abstract"):
            return "10_compact_papers", build_compact(row)
    if counts["01_prose_sections"] < TARGETS["01_prose_sections"] and row.get("abstract"):
        return "01_prose_sections", build_prose(row)
    return None


def fill_scholarweave(out_dir: Path, args: argparse.Namespace) -> list[Record]:
    records: list[Record] = []
    counts = {category: 0 for category in SCHOLARWEAVE_TARGETS}
    attempts = {category: 0 for category in SCHOLARWEAVE_TARGETS}
    ds = load_dataset(SCHOLARWEAVE, split="train", streaming=True)
    for idx, row in enumerate(ds):
        if idx >= args.scholarweave_scan_limit:
            break
        if all(counts[c] >= TARGETS[c] for c in SCHOLARWEAVE_TARGETS):
            break
        if not row.get("latex") or len(row.get("latex", "")) < 1000:
            continue
        candidate = category_candidate(row, counts)
        if not candidate:
            continue
        category, tex = candidate
        attempts[category] += 1
        sample_id = f"{category}_{attempts[category]:03d}"
        rec = compile_generated(out_dir, category, sample_id, tex, SCHOLARWEAVE, row["id"], args.timeout, args.max_pages)
        records.append(rec)
        if rec.status == "accepted":
            counts[category] += 1
            print(f"accepted {sample_id}", flush=True)
        if attempts[category] >= args.max_attempts_per_category and counts[category] < TARGETS[category]:
            print(f"category attempt cap reached: {category} accepted={counts[category]}", flush=True)
    return records


def compile_texlive_form(out_dir: Path, source_path: Path, sample_id: str, timeout: int, max_pages: int) -> Record:
    tex = source_path.read_text(encoding="utf-8", errors="replace")
    if "\\documentclass" not in tex and "\\input" in tex:
        tex = "% Source: %s\n%s" % (source_path, tex)
    return compile_generated(
        out_dir,
        "11_forms_cv_letters",
        sample_id,
        tex,
        "TeX Live 2026",
        str(source_path),
        timeout,
        max_pages,
        source_family="texlive_example",
    )


def fill_texlive_forms(out_dir: Path, args: argparse.Namespace) -> list[Record]:
    records: list[Record] = []
    accepted = 0
    for idx, source_path in enumerate(TEXLIVE_FORM_SOURCES, start=1):
        if accepted >= TARGETS["11_forms_cv_letters"]:
            break
        if not source_path.exists():
            continue
        sample_id = f"11_forms_cv_letters_{idx:03d}"
        rec = compile_texlive_form(out_dir, source_path, sample_id, args.timeout, args.max_pages)
        records.append(rec)
        if rec.status == "accepted":
            accepted += 1
            print(f"accepted {sample_id}", flush=True)
    return records


def write_manifests(records: list[Record], out_dir: Path) -> None:
    manifest_dir = out_dir / "manifests"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    fields = list(asdict(records[0]).keys()) if records else [f.name for f in Record.__dataclass_fields__.values()]
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
        meta = f"Dataset: {record.source_dataset}\nSource ID(s): {record.source_ids}\nSource: {record.nonblank_lines} nonblank lines, {record.source_chars} chars"
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
    preview = out_dir / "previews" / "simple_benchmark_all_v0_preview.pdf"
    preview.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    try:
        current_category = None
        for record in sorted(accepted, key=lambda r: (r.category, r.sample_id)):
            if record.category != current_category:
                current_category = record.category
                count = sum(1 for r in accepted if r.category == current_category)
                page = doc.new_page(width=842, height=595)
                page.insert_text((48, 84), current_category, fontsize=28, fontname="helv")
                page.insert_text((48, 128), f"{count} accepted samples", fontsize=14, fontname="helv")
                page.insert_text((48, 164), "Each following page previews one complete data point. Multi-page PDFs are tiled.", fontsize=11, fontname="helv")
            add_preview_page(doc, record)
        doc.save(preview)
    finally:
        doc.close()
    return preview


def write_readme(records: list[Record], out_dir: Path, preview: Path) -> None:
    accepted = [r for r in records if r.status == "accepted"]
    rejected = [r for r in records if r.status != "accepted"]
    by_cat: dict[str, int] = {}
    by_source: dict[str, int] = {}
    pages: dict[int, int] = {}
    for rec in accepted:
        by_cat[rec.category] = by_cat.get(rec.category, 0) + 1
        by_source[rec.source_dataset] = by_source.get(rec.source_dataset, 0) + 1
        pages[rec.page_count] = pages.get(rec.page_count, 0) + 1

    lines = [
        "# Simple Benchmark All v0",
        "",
        "Built: 2026-07-13",
        "",
        f"Accepted samples: {len(accepted)}",
        f"Rejected generated candidates: {len(rejected)}",
        "",
        "This is the first unified source-backed LaTeX benchmark directory. It keeps the 11 simple categories together, caps each category to the intended first-pass size, and provides one sectioned preview document for review.",
        "",
        "## Accepted Categories",
        "",
        "| Category | Accepted |",
        "|---|---:|",
    ]
    for category in sorted(by_cat):
        lines.append(f"| `{category}` | {by_cat[category]} |")
    lines.extend(["", "## Sources", "", "| Source | Accepted |", "|---|---:|"])
    for source, count in sorted(by_source.items()):
        lines.append(f"| `{source}` | {count} |")
    lines.extend(["", "## Page Distribution", "", "| Pages | Accepted |", "|---:|---:|"])
    for page_count, count in sorted(pages.items()):
        lines.append(f"| {page_count} | {count} |")
    lines.extend(["", "## Deferred Categories", ""])
    for category, reason in DEFERRED.items():
        lines.append(f"- `{category}`: {reason}")
    lines.extend(
        [
            "",
            "## Rules Used",
            "",
            "- `pdflatex` only.",
            "- Accepted PDFs must be 1-3 pages.",
            "- All accepted samples have `main.tex`, `reference.pdf`, `compile.log`, and `provenance.json`.",
            "- Full arXiv papers are not compiled blind; this build extracts smaller self-contained snippets or metadata-backed wrappers.",
            "- Diagram-heavy categories are deferred to a later stress benchmark.",
            "",
            "## Files",
            "",
            "```text",
            "corpus/<category>/<sample_id>/",
            "  main.tex",
            "  reference.pdf",
            "  compile.log",
            "  provenance.json",
            "",
            "manifests/",
            "  all.csv",
            "  accepted.csv",
            "  rejected.csv",
            "",
            "previews/",
            f"  {preview.name}",
            "```",
            "",
            "The preview PDF contains one preview page per accepted data point. Multi-page references are tiled on that preview page.",
            "",
            "## Build Command",
            "",
            "```bash",
            "mamba run -n lathe python scripts/dataset/build_all_categories_v0.py --out data/latex_benchmark_v0",
            "```",
            "",
        ]
    )
    write_text(out_dir / "README.md", "\n".join(lines))


def build(args: argparse.Namespace) -> None:
    if args.out.exists():
        shutil.rmtree(args.out)
    args.out.mkdir(parents=True, exist_ok=True)
    records = copy_existing_slices(args.out)
    print(f"copied accepted source slices: {len(records)}", flush=True)
    records.extend(fill_scholarweave(args.out, args))
    records.extend(fill_texlive_forms(args.out, args))
    write_manifests(records, args.out)
    preview = build_preview(records, args.out)
    write_readme(records, args.out, preview)
    accepted = sum(1 for record in records if record.status == "accepted")
    rejected = sum(1 for record in records if record.status != "accepted")
    print(f"accepted: {accepted}", flush=True)
    print(f"rejected: {rejected}", flush=True)
    print(f"preview: {preview}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    parser.add_argument("--scholarweave-scan-limit", type=int, default=4500)
    parser.add_argument("--max-attempts-per-category", type=int, default=80)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-pages", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    build(parse_args())


if __name__ == "__main__":
    main()
