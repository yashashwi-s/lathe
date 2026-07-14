"""Shared helpers for dataset_expansion builders.

All new reference PDFs are compiled with **tectonic** (XeTeX-based) because
pdflatex is not installed locally. This differs from the lathe canon
(pdfLaTeX); font metrics drift slightly, which is acceptable for a
dataset-fit/difficulty benchmark but should be noted in any writeup.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent  # dataset_expansion/
CORPUS = ROOT / "corpus"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compile_tectonic(sample_dir: Path, tex_name: str = "main.tex",
                     timeout: int = 120) -> tuple[bool, str, float]:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            ["tectonic", "--keep-logs", tex_name],
            cwd=sample_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raw = exc.stdout or b""
        if not isinstance(raw, str):
            raw = raw.decode("utf-8", errors="replace")
        return False, raw + "\nTIMEOUT\n", time.monotonic() - start
    log = (proc.stdout or b"").decode("utf-8", errors="replace")
    return proc.returncode == 0, log, time.monotonic() - start


def pdf_page_count(path: Path) -> int:
    doc = fitz.open(path)
    try:
        return doc.page_count
    finally:
        doc.close()


def finalize_sample(sample_dir: Path, dataset: str, source_id: str,
                    max_pages: int = 6, timeout: int = 120,
                    tex_name: str = "main.tex") -> dict:
    """Compile main.tex -> reference.pdf, write provenance, return record."""
    ok, log, seconds = compile_tectonic(sample_dir, tex_name, timeout)
    (sample_dir / "compile.log").write_text(log, encoding="utf-8")
    pdf = sample_dir / tex_name.replace(".tex", ".pdf")
    rec = {"sample_id": sample_dir.name, "set": sample_dir.parent.name,
           "source_dataset": dataset, "source_id": source_id,
           "status": "accepted", "reason": "accepted", "page_count": 0,
           "compile_seconds": round(seconds, 2),
           "source_chars": len((sample_dir / tex_name).read_text(errors="replace")),
           "sample_dir": str(sample_dir)}
    if not ok or not pdf.exists() or pdf.stat().st_size == 0:
        rec.update(status="rejected", reason="compile_failed")
        return rec
    try:
        pages = pdf_page_count(pdf)
    except Exception:
        rec.update(status="rejected", reason="invalid_pdf")
        return rec
    if pages < 1 or pages > max_pages:
        rec.update(status="rejected", reason=f"page_count_{pages}", page_count=pages)
        return rec
    ref = sample_dir / "reference.pdf"
    pdf.rename(ref)
    rec["page_count"] = pages
    (sample_dir / "provenance.json").write_text(json.dumps({
        **{k: rec[k] for k in ("sample_id", "source_dataset", "source_id",
                               "page_count", "compile_seconds")},
        "compile_engine": "tectonic 0.16.9",
        "sha256_source": sha256_file(sample_dir / tex_name),
        "sha256_pdf": sha256_file(ref),
    }, indent=2) + "\n")
    return rec


def write_manifest(records: list[dict], out_csv: Path) -> None:
    import csv
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        return
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)
