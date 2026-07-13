#!/usr/bin/env python3
"""Build a small, reviewable TeX Live seed corpus.

The script is intentionally conservative:
- pdfLaTeX only
- accepted PDFs must be 1-3 pages
- candidates are stratified by document form, source package, size bucket, and
  construct tags
- the preview PDF shows one complete data point per page, tiling multi-page
  samples into a grid
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import textwrap
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import fitz


TEXLIVE_DOC = Path("/usr/local/texlive/2026/texmf-dist/doc")
DEFAULT_OUT = Path("data/texlive_seed")

TEXT_EXTENSIONS = {
    ".tex",
    ".ltx",
    ".sty",
    ".cls",
    ".bib",
    ".bst",
    ".def",
    ".cfg",
    ".dat",
    ".csv",
    ".txt",
}
ASSET_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".eps",
    ".mps",
}
COPY_EXTENSIONS = TEXT_EXTENSIONS | ASSET_EXTENSIONS

SKIP_DIR_PARTS = {
    ".git",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}

PDFLATEX_UNLIKELY_TOPLEVEL = {
    "context",
    "lualatex",
    "luatex",
    "metapost",
    "platex",
    "uplatex",
    "uptex",
    "xelatex",
    "xetex",
}

SKIP_FILE_EXTENSIONS = {
    ".aux",
    ".bbl",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".idx",
    ".ilg",
    ".ind",
    ".log",
    ".out",
    ".synctex.gz",
    ".toc",
}

FORM_QUOTAS_240 = {
    "compact_paper": 40,
    "paper_excerpt": 30,
    "math_short": 30,
    "table": 30,
    "figure_diagram_plot": 40,
    "algorithm": 12,
    "presentation": 18,
    "poster_layout": 12,
    "cv_resume": 12,
    "letter_form_teaching": 16,
    "package_example": 20,
}

SIMPLE_FORM_QUOTAS_120 = {
    "math_short": 24,
    "table": 24,
    "figure_diagram_plot": 18,
    "package_example": 18,
    "compact_paper": 14,
    "letter_form_teaching": 10,
    "algorithm": 6,
    "paper_excerpt": 4,
    "cv_resume": 2,
}

HARD_FORM_QUOTAS_120 = {
    "compact_paper": 24,
    "paper_excerpt": 18,
    "figure_diagram_plot": 18,
    "presentation": 14,
    "poster_layout": 12,
    "table": 12,
    "math_short": 10,
    "algorithm": 6,
    "cv_resume": 4,
    "letter_form_teaching": 2,
}

TAG_MINIMUMS_240 = {
    "display_math": 50,
    "aligned_math": 25,
    "simple_table": 25,
    "complex_table": 25,
    "figures_images": 30,
    "tikz": 25,
    "pgfplots": 15,
    "citations_bibliography": 30,
    "crossrefs": 40,
    "custom_macros": 40,
    "algorithm_pseudocode": 10,
    "multi_column": 25,
    "minipage_boxes": 25,
    "beamer_frames": 15,
    "poster_blocks": 8,
}

PROFILE_QUOTAS = {
    "balanced": FORM_QUOTAS_240,
    "simple": SIMPLE_FORM_QUOTAS_120,
    "hard": HARD_FORM_QUOTAS_120,
}

COMPLEX_TAGS = {
    "aligned_math",
    "beamer_frames",
    "citations_bibliography",
    "complex_table",
    "custom_environments",
    "custom_macros",
    "long_table",
    "minipage_boxes",
    "multi_column",
    "pgfplots",
    "poster_blocks",
    "theorems_proofs",
}


@dataclass
class Candidate:
    path: str
    package: str
    source_family: str
    document_form: str
    construct_tags: str
    size_bucket: str
    nonblank_lines: int
    source_chars: int
    score: int
    sha256_source: str


@dataclass
class CompileResult:
    sample_id: str
    status: str
    reason: str
    page_count: int
    compile_seconds: float
    source_path: str
    package: str
    source_family: str
    document_form: str
    construct_tags: str
    size_bucket: str
    nonblank_lines: int
    source_chars: int
    sha256_source: str
    sha256_pdf: str
    corpus_dir: str


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except UnicodeDecodeError:
            return None
    except OSError:
        return None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_sample_id(path: Path, package: str) -> str:
    stem = re.sub(r"[^a-zA-Z0-9]+", "_", path.stem).strip("_").lower()
    pkg = re.sub(r"[^a-zA-Z0-9]+", "_", package).strip("_").lower()
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:8]
    base = f"{pkg}_{stem}_{digest}".strip("_")
    return base[:90]


def package_name(path: Path, texlive_doc: Path) -> str:
    rel = path.relative_to(texlive_doc)
    parts = rel.parts
    if len(parts) >= 3 and parts[0] in {"latex", "plain", "generic", "context"}:
        return parts[1]
    if len(parts) >= 2:
        return parts[1] if parts[0] in {"metapost", "fonts"} else parts[0]
    return "unknown"


def nonblank_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def size_bucket(nonblank: int, chars: int) -> str:
    if nonblank <= 8 or chars < 450:
        return "tiny"
    if nonblank <= 25 or chars < 1500:
        return "short"
    if nonblank <= 100 or chars < 8000:
        return "medium"
    return "large"


def has_documentclass(text: str) -> bool:
    return bool(re.search(r"\\documentclass(?:\[[^\]]*\])?\{[^}]+\}", text))


def document_form(text: str, path: Path, package: str) -> str:
    lower = (text[:12000] + " " + str(path) + " " + package).lower()
    cls_match = re.search(r"\\documentclass(?:\[[^\]]*\])?\{([^}]+)\}", text)
    cls = cls_match.group(1).lower() if cls_match else ""

    if "beamerposter" in lower or "poster" in lower and "\\begin{frame}" not in text:
        return "poster_layout"
    if cls == "beamer" or "\\begin{frame}" in text or "\\usetheme" in text:
        return "presentation"
    if any(term in lower for term in ["curriculum", "vitae", "resume", "moderncv", "europecv"]):
        return "cv_resume"
    if any(term in lower for term in ["\\begin{letter}", "\\opening", "\\closing", "onlinebrief", "scrlttr2"]):
        return "letter_form_teaching"
    if any(term in lower for term in ["exam", "homework", "worksheet", "school", "questionnaire"]):
        return "letter_form_teaching"
    if re.search(r"\\begin\{algorithm\}|\\begin\{algorithmic\}|algorithm2e", text):
        return "algorithm"
    if re.search(r"\\begin\{tikzpicture\}|\\begin\{axis\}|pgfplots|tikz-cd", text):
        return "figure_diagram_plot"
    if re.search(r"\\begin\{tabular\}|\\begin\{longtable\}|\\begin\{tabularx\}", text):
        return "table"
    if re.search(r"\\begin\{abstract\}", text) and re.search(r"\\section", text):
        return "compact_paper"
    if re.search(r"\\section|\\subsection", text) and re.search(r"\\cite|\\bibliography|\\begin\{thebibliography\}", text):
        return "paper_excerpt"
    if re.search(r"\\begin\{equation\}|\\begin\{align\}|\\\[", text):
        return "math_short"
    if cls in {"article", "report", "proc", "llncs", "amsart", "revtex4-2", "aastex631", "aastex701"}:
        return "compact_paper"
    return "package_example"


def construct_tags(text: str) -> list[str]:
    tags = set()
    checks = [
        ("text_sectioning", r"\\(?:part|chapter|section|subsection|paragraph)\b"),
        ("lists", r"\\begin\{(?:itemize|enumerate|description)\}"),
        ("footnotes", r"\\footnote\b"),
        ("inline_math", r"(?<!\\)\$[^$]+\$|\\\([^)]*\\\)"),
        ("display_math", r"\\begin\{(?:equation|displaymath|gather|multline)\}|\\\["),
        ("aligned_math", r"\\begin\{(?:align|alignat|aligned|split|eqnarray)\}"),
        ("theorems_proofs", r"\\begin\{(?:theorem|lemma|proof|proposition|corollary)\}|\\newtheorem"),
        ("simple_table", r"\\begin\{tabular\}"),
        ("complex_table", r"\\(?:multicolumn|multirow)|\\begin\{(?:tabularx|longtable|xltabular|supertabular)\}"),
        ("long_table", r"\\begin\{(?:longtable|xltabular|supertabular)\}"),
        ("figures_images", r"\\includegraphics|\\begin\{figure\}"),
        ("captions", r"\\caption\b"),
        ("crossrefs", r"\\label\b|\\ref\b|\\pageref\b|\\autoref\b|\\cref\b"),
        ("citations_bibliography", r"\\cite\b|\\bibliography\b|\\addbibresource|\\begin\{thebibliography\}"),
        ("algorithm_pseudocode", r"\\begin\{algorithm\}|\\begin\{algorithmic\}|algorithm2e"),
        ("tikz", r"\\begin\{tikzpicture\}|tikz-cd|\\usetikzlibrary"),
        ("pgfplots", r"\\begin\{axis\}|pgfplots|\\usepackage\{pgfplots\}"),
        ("diagram_nodes_edges", r"\\node\b|\\draw\b|\\path\b|\\graph\b"),
        ("multi_column", r"\\twocolumn|\\begin\{multicols\}|\\multicolumn"),
        ("minipage_boxes", r"\\begin\{minipage\}|\\parbox|\\fbox|\\framebox|\\begin\{tcolorbox\}"),
        ("custom_macros", r"\\newcommand|\\renewcommand|\\def\\|\\DeclareMathOperator"),
        ("custom_environments", r"\\newenvironment|\\renewenvironment"),
        ("beamer_frames", r"\\begin\{frame\}|\\frametitle|\\usetheme"),
        ("poster_blocks", r"\\begin\{block\}|beamerposter|poster"),
        ("fonts_symbols", r"\\usepackage\{[^}]*font|\\mathbb|\\mathcal|\\ding|\\symbol"),
        ("color", r"\\usepackage\{xcolor\}|\\color\b|\\textcolor|\\definecolor"),
    ]
    for tag, pattern in checks:
        if re.search(pattern, text):
            tags.add(tag)
    return sorted(tags)


def candidate_score(form: str, tags: list[str], bucket: str, nonblank: int, chars: int, path: Path) -> int:
    score = len(tags) * 8
    if bucket == "medium":
        score += 35
    elif bucket == "large":
        score += 8
    elif bucket == "short":
        score += 18
    else:
        score += 4
    if form in {"compact_paper", "figure_diagram_plot", "table", "presentation"}:
        score += 14
    path_text = str(path).lower()
    name = path.name.lower()
    if any(part in path_text for part in ["/example", "/examples", "/demo", "/samples", "/sample", "/test"]):
        score += 38
    if any(term in name for term in ["example", "demo", "sample", "test"]):
        score += 24
    if any(term in name for term in ["manual", "guide", "doc", "documentation", "lshort", "thesis"]):
        score -= 45
    if any(term in path_text for term in ["/manual", "/guide", "/doc/", "/src/"]):
        score -= 18
    if chars > 120000 or nonblank > 1600:
        score -= 80
    return score


def profile_score(candidate: Candidate, profile: str) -> int:
    tags = set(filter(None, candidate.construct_tags.split(";")))
    tag_count = len(tags)
    score = candidate.score

    if profile == "simple":
        if candidate.size_bucket == "short":
            score += 42
        elif candidate.size_bucket == "medium":
            score += 30
        elif candidate.size_bucket == "tiny":
            score += 12
        else:
            score -= 45
        if tag_count <= 3:
            score += 36
        elif tag_count <= 6:
            score += 18
        else:
            score -= 10 * (tag_count - 6)
        score -= 16 * len(tags & COMPLEX_TAGS)
        if tags & {"simple_table", "inline_math", "display_math", "figures_images", "lists"}:
            score += 18
        if candidate.document_form in {"presentation", "poster_layout", "paper_excerpt"}:
            score -= 28
        return score

    if profile == "hard":
        score += 10 * tag_count
        score += 18 * len(tags & COMPLEX_TAGS)
        if candidate.size_bucket == "large":
            score += 28
        elif candidate.size_bucket == "medium":
            score += 18
        if candidate.document_form in {"compact_paper", "paper_excerpt", "presentation", "poster_layout"}:
            score += 24
        return score

    return score


def profile_allows_candidate(candidate: Candidate, profile: str) -> bool:
    if profile != "simple":
        return True
    tags = set(filter(None, candidate.construct_tags.split(";")))
    tag_count = len(tags)
    if candidate.size_bucket == "large":
        return False
    if tag_count > 9:
        return False
    if len(tags & COMPLEX_TAGS) > 3:
        return False
    return True


def discover(texlive_doc: Path, max_file_bytes: int) -> list[Candidate]:
    candidates: list[Candidate] = []
    for path in texlive_doc.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".tex", ".ltx"}:
            continue
        if any(part in SKIP_DIR_PARTS for part in path.parts):
            continue
        try:
            top = path.relative_to(texlive_doc).parts[0]
        except ValueError:
            top = ""
        if top in PDFLATEX_UNLIKELY_TOPLEVEL:
            continue
        try:
            if path.stat().st_size > max_file_bytes:
                continue
        except OSError:
            continue
        text = read_text(path)
        if not text or not has_documentclass(text):
            continue
        nonblank = nonblank_line_count(text)
        chars = len(text)
        package = package_name(path, texlive_doc)
        form = document_form(text, path, package)
        tags = construct_tags(text)
        bucket = size_bucket(nonblank, chars)
        score = candidate_score(form, tags, bucket, nonblank, chars, path)
        candidates.append(
            Candidate(
                path=str(path),
                package=package,
                source_family="texlive_ctan_doc",
                document_form=form,
                construct_tags=";".join(tags),
                size_bucket=bucket,
                nonblank_lines=nonblank,
                source_chars=chars,
                score=score,
                sha256_source=sha256_file(path),
            )
        )
    return candidates


def write_candidates_csv(candidates: list[Candidate], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(candidates[0]).keys()) if candidates else [])
        if candidates:
            writer.writeheader()
            for candidate in candidates:
                writer.writerow(asdict(candidate))


def read_candidates_csv(path: Path) -> list[Candidate]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    candidates = []
    for row in rows:
        candidates.append(
            Candidate(
                path=row["path"],
                package=row["package"],
                source_family=row["source_family"],
                document_form=row["document_form"],
                construct_tags=row["construct_tags"],
                size_bucket=row["size_bucket"],
                nonblank_lines=int(row["nonblank_lines"]),
                source_chars=int(row["source_chars"]),
                score=int(row["score"]),
                sha256_source=row["sha256_source"],
            )
        )
    return candidates


def stratified_candidates(
    candidates: list[Candidate],
    target: int,
    seed: int,
    tiny_fraction: float,
    profile: str,
) -> list[Candidate]:
    random.seed(seed)
    by_form: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        if not profile_allows_candidate(candidate, profile):
            continue
        by_form.setdefault(candidate.document_form, []).append(candidate)

    quota_template = PROFILE_QUOTAS[profile]
    base_total = sum(quota_template.values())
    quotas = {
        form: max(1, round(quota * target / base_total))
        for form, quota in quota_template.items()
    }
    tiny_cap = max(2, round(target * tiny_fraction))
    package_cap = max(2, round(target * 0.10))

    selected_by_form: dict[str, list[Candidate]] = {}
    selected_paths: set[str] = set()
    package_counts: dict[str, int] = {}
    tiny_count = 0

    def accept(candidate: Candidate) -> bool:
        nonlocal tiny_count
        if candidate.path in selected_paths:
            return False
        if package_counts.get(candidate.package, 0) >= package_cap:
            return False
        if candidate.size_bucket == "tiny" and tiny_count >= tiny_cap:
            return False
        package_counts[candidate.package] = package_counts.get(candidate.package, 0) + 1
        if candidate.size_bucket == "tiny":
            tiny_count += 1
        selected_by_form.setdefault(candidate.document_form, []).append(candidate)
        selected_paths.add(candidate.path)
        return True

    for form, quota in quotas.items():
        pool = by_form.get(form, [])
        random.shuffle(pool)
        pool.sort(key=lambda c: (profile_score(c, profile), c.nonblank_lines), reverse=True)
        form_count = 0
        for candidate in pool:
            if form_count >= quota:
                break
            if accept(candidate):
                form_count += 1

    current_count = sum(len(items) for items in selected_by_form.values())
    if current_count < target:
        rest = [
            c for c in candidates
            if c.path not in selected_paths and profile_allows_candidate(c, profile)
        ]
        random.shuffle(rest)
        rest.sort(key=lambda c: (profile_score(c, profile), c.nonblank_lines), reverse=True)
        for candidate in rest:
            current_count = sum(len(items) for items in selected_by_form.values())
            if current_count >= target:
                break
            accept(candidate)

    ordered: list[Candidate] = []
    form_order = sorted(selected_by_form, key=lambda f: quotas.get(f, 0), reverse=True)
    while len(ordered) < target:
        progressed = False
        for form in form_order:
            items = selected_by_form.get(form, [])
            if items:
                ordered.append(items.pop(0))
                progressed = True
                if len(ordered) >= target:
                    break
        if not progressed:
            break
    return ordered


def should_copy(path: Path) -> bool:
    if path.is_dir():
        return path.name not in SKIP_DIR_PARTS
    suffix = path.suffix.lower()
    if suffix in SKIP_FILE_EXTENSIONS:
        return False
    return suffix in COPY_EXTENSIONS


def copy_source_tree(src: Path, dst: Path, max_tree_bytes: int) -> bool:
    root = src.parent
    total = 0
    for path in root.rglob("*"):
        if not path.is_file() or not should_copy(path):
            continue
        try:
            total += path.stat().st_size
        except OSError:
            continue
        if total > max_tree_bytes:
            return False

    dst.mkdir(parents=True, exist_ok=True)
    for path in root.rglob("*"):
        if not path.is_file() or not should_copy(path):
            continue
        rel = path.relative_to(root)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    return True


def run_pdflatex(workdir: Path, tex_name: str, timeout: int) -> tuple[bool, str, float]:
    start = time.monotonic()
    cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_name]
    combined = []
    ok = True
    for _ in range(2):
        try:
            proc = subprocess.run(
                cmd,
                cwd=workdir,
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
        combined.append((proc.stdout or b"").decode("utf-8", errors="replace"))
        if proc.returncode != 0:
            ok = False
            break
    return ok, "\n\n--- pass break ---\n\n".join(combined), time.monotonic() - start


def pdf_page_count(path: Path) -> int:
    doc = fitz.open(path)
    try:
        return doc.page_count
    finally:
        doc.close()


def compile_candidates(
    candidates: list[Candidate],
    out_dir: Path,
    max_accept: int,
    timeout: int,
    max_pages: int,
    max_tree_bytes: int,
) -> list[CompileResult]:
    corpus_dir = out_dir / "corpus"
    rejected_dir = out_dir / "rejected_logs"
    corpus_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)

    results: list[CompileResult] = []
    accepted = 0
    seen_ids: set[str] = set()
    accepted_package_counts: dict[str, int] = {}
    accepted_form_counts: dict[str, int] = {}
    accepted_package_cap = max(2, round(max_accept * 0.10))
    base_total = sum(FORM_QUOTAS_240.values())
    accepted_form_caps = {
        form: max(3, math.ceil(quota * max_accept / base_total * 1.45))
        for form, quota in FORM_QUOTAS_240.items()
    }

    for candidate in candidates:
        if accepted >= max_accept:
            break
        src = Path(candidate.path)
        sample_id = safe_sample_id(src, candidate.package)
        while sample_id in seen_ids:
            sample_id += "_x"
        seen_ids.add(sample_id)

        sample_dir = corpus_dir / candidate.document_form / sample_id
        build_dir = out_dir / "build" / sample_id
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if sample_dir.exists():
            shutil.rmtree(sample_dir)
        build_dir.mkdir(parents=True, exist_ok=True)

        if accepted_package_counts.get(candidate.package, 0) >= accepted_package_cap:
            results.append(rejected_result(candidate, sample_id, "distribution_cap_package"))
            continue
        if accepted_form_counts.get(candidate.document_form, 0) >= accepted_form_caps.get(candidate.document_form, 3):
            results.append(rejected_result(candidate, sample_id, "distribution_cap_form"))
            continue

        source_tree = build_dir / "source_tree"
        if not copy_source_tree(src, source_tree, max_tree_bytes=max_tree_bytes):
            result = rejected_result(candidate, sample_id, "source_tree_too_large")
            results.append(result)
            continue

        rel_tex = src.relative_to(src.parent)
        ok, log, seconds = run_pdflatex(source_tree, rel_tex.name, timeout=timeout)
        pdf = source_tree / f"{src.stem}.pdf"
        if not ok or not pdf.exists() or pdf.stat().st_size == 0:
            (rejected_dir / f"{sample_id}.log").write_text(log, encoding="utf-8", errors="replace")
            result = rejected_result(candidate, sample_id, "pdflatex_failed", seconds=seconds)
            results.append(result)
            continue

        try:
            pages = pdf_page_count(pdf)
        except Exception:
            (rejected_dir / f"{sample_id}.log").write_text(log, encoding="utf-8", errors="replace")
            result = rejected_result(candidate, sample_id, "invalid_pdf", seconds=seconds)
            results.append(result)
            continue
        if pages < 1 or pages > max_pages:
            (rejected_dir / f"{sample_id}.log").write_text(log, encoding="utf-8", errors="replace")
            result = rejected_result(candidate, sample_id, f"page_count_{pages}", seconds=seconds, pages=pages)
            results.append(result)
            continue

        sample_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_tree, sample_dir / "source_tree")
        shutil.copy2(source_tree / rel_tex.name, sample_dir / "main.tex")
        shutil.copy2(pdf, sample_dir / "reference.pdf")
        (sample_dir / "compile.log").write_text(log, encoding="utf-8", errors="replace")

        pdf_hash = sha256_file(sample_dir / "reference.pdf")
        provenance = {
            "sample_id": sample_id,
            "source_family": candidate.source_family,
            "document_form": candidate.document_form,
            "construct_tags": candidate.construct_tags.split(";") if candidate.construct_tags else [],
            "size_bucket": candidate.size_bucket,
            "package": candidate.package,
            "texlive_version": "2026",
            "original_path": candidate.path,
            "source_tree_root": str(src.parent),
            "compile_engine": "pdflatex",
            "compile_command": "pdflatex -interaction=nonstopmode -halt-on-error main.tex",
            "compile_seconds": round(seconds, 3),
            "page_count": pages,
            "nonblank_lines": candidate.nonblank_lines,
            "source_chars": candidate.source_chars,
            "sha256_source": candidate.sha256_source,
            "sha256_pdf": pdf_hash,
            "license_status": "package-level license must be confirmed before final freeze",
        }
        (sample_dir / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")

        result = CompileResult(
            sample_id=sample_id,
            status="accepted",
            reason="accepted",
            page_count=pages,
            compile_seconds=seconds,
            source_path=candidate.path,
            package=candidate.package,
            source_family=candidate.source_family,
            document_form=candidate.document_form,
            construct_tags=candidate.construct_tags,
            size_bucket=candidate.size_bucket,
            nonblank_lines=candidate.nonblank_lines,
            source_chars=candidate.source_chars,
            sha256_source=candidate.sha256_source,
            sha256_pdf=pdf_hash,
            corpus_dir=str(sample_dir),
        )
        results.append(result)
        accepted += 1
        accepted_package_counts[candidate.package] = accepted_package_counts.get(candidate.package, 0) + 1
        accepted_form_counts[candidate.document_form] = accepted_form_counts.get(candidate.document_form, 0) + 1
        print(f"accepted {accepted:03d}: {sample_id} ({pages}p, {candidate.document_form})", flush=True)

    return results


def rejected_result(
    candidate: Candidate,
    sample_id: str,
    reason: str,
    seconds: float = 0.0,
    pages: int = 0,
) -> CompileResult:
    return CompileResult(
        sample_id=sample_id,
        status="rejected",
        reason=reason,
        page_count=pages,
        compile_seconds=seconds,
        source_path=candidate.path,
        package=candidate.package,
        source_family=candidate.source_family,
        document_form=candidate.document_form,
        construct_tags=candidate.construct_tags,
        size_bucket=candidate.size_bucket,
        nonblank_lines=candidate.nonblank_lines,
        source_chars=candidate.source_chars,
        sha256_source=candidate.sha256_source,
        sha256_pdf="",
        corpus_dir="",
    )


def write_results_csv(results: list[CompileResult], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(asdict(results[0]).keys()) if results else [field.name for field in CompileResult.__dataclass_fields__.values()]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for result in results:
            writer.writerow(asdict(result))


def write_accepted_manifest(results: list[CompileResult], path: Path) -> None:
    accepted = [result for result in results if result.status == "accepted"]
    fields = list(asdict(accepted[0]).keys()) if accepted else [field.name for field in CompileResult.__dataclass_fields__.values()]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for result in accepted:
            writer.writerow(asdict(result))


def read_results_csv(path: Path) -> list[CompileResult]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    results = []
    for row in rows:
        results.append(
            CompileResult(
                sample_id=row["sample_id"],
                status=row["status"],
                reason=row["reason"],
                page_count=int(row["page_count"]),
                compile_seconds=float(row["compile_seconds"]),
                source_path=row["source_path"],
                package=row["package"],
                source_family=row["source_family"],
                document_form=row["document_form"],
                construct_tags=row["construct_tags"],
                size_bucket=row["size_bucket"],
                nonblank_lines=int(row["nonblank_lines"]),
                source_chars=int(row["source_chars"]),
                sha256_source=row["sha256_source"],
                sha256_pdf=row["sha256_pdf"],
                corpus_dir=row["corpus_dir"],
            )
        )
    return results


def draw_wrapped_text(page: fitz.Page, rect: fitz.Rect, text: str, fontsize: int = 8) -> None:
    page.insert_textbox(
        rect,
        text,
        fontsize=fontsize,
        fontname="helv",
        color=(0.10, 0.10, 0.10),
        align=fitz.TEXT_ALIGN_LEFT,
    )


def add_preview_page(out: fitz.Document, result: CompileResult, sample_dir: Path) -> None:
    pdf_path = sample_dir / "reference.pdf"
    src_doc = fitz.open(pdf_path)
    try:
        page = out.new_page(width=842, height=595)  # A4 landscape in points
        margin = 24
        header_h = 82
        title = f"{result.sample_id}  |  {result.document_form}  |  {result.page_count} page(s)"
        tags = result.construct_tags.replace(";", ", ")
        meta = (
            f"Package: {result.package}\n"
            f"Size: {result.size_bucket}, {result.nonblank_lines} nonblank lines, {result.source_chars} chars\n"
            f"Tags: {tags or 'none'}\n"
            f"Source: {result.source_path}"
        )
        page.insert_text((margin, 24), title, fontsize=13, fontname="helv", color=(0, 0, 0))
        draw_wrapped_text(page, fitz.Rect(margin, 38, 818, margin + header_h), meta, fontsize=7)
        page.draw_line((margin, margin + header_h), (818, margin + header_h), color=(0.75, 0.75, 0.75))

        n = src_doc.page_count
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
            src_page = src_doc.load_page(idx)
            src_rect = src_page.rect
            scale = min(cell.width / src_rect.width, cell.height / src_rect.height)
            w = src_rect.width * scale
            h = src_rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - w) / 2,
                cell.y0 + (cell.height - h) / 2,
                cell.x0 + (cell.width + w) / 2,
                cell.y0 + (cell.height + h) / 2,
            )
            page.show_pdf_page(target, src_doc, idx)
            page.draw_rect(target, color=(0.55, 0.55, 0.55), width=0.6)
            page.insert_text((target.x0, max(target.y0 - 3, grid.y0 - 2)), f"p{idx + 1}", fontsize=6, color=(0.25, 0.25, 0.25))
    finally:
        src_doc.close()


def build_preview(results: list[CompileResult], out_dir: Path, limit: int | None = None) -> Path:
    accepted = [r for r in results if r.status == "accepted" and r.corpus_dir]
    accepted.sort(key=lambda r: (r.document_form, r.package, r.sample_id))
    if limit:
        accepted = accepted[:limit]

    preview_dir = out_dir / "previews"
    preview_dir.mkdir(parents=True, exist_ok=True)
    preview_pdf = preview_dir / "texlive_seed_preview.pdf"
    out = fitz.open()
    try:
        for result in accepted:
            add_preview_page(out, result, Path(result.corpus_dir))
        out.save(preview_pdf)
    finally:
        out.close()
    return preview_pdf


def summarize(results: list[CompileResult], out_dir: Path) -> None:
    accepted = [r for r in results if r.status == "accepted"]
    by_form: dict[str, int] = {}
    by_bucket: dict[str, int] = {}
    by_package: dict[str, int] = {}
    by_tag: dict[str, int] = {}
    for result in accepted:
        by_form[result.document_form] = by_form.get(result.document_form, 0) + 1
        by_bucket[result.size_bucket] = by_bucket.get(result.size_bucket, 0) + 1
        by_package[result.package] = by_package.get(result.package, 0) + 1
        for tag in filter(None, result.construct_tags.split(";")):
            by_tag[tag] = by_tag.get(tag, 0) + 1

    lines = [
        "# TeX Live Seed Corpus Summary",
        "",
        f"Accepted samples: {len(accepted)}",
        f"Rejected candidates: {len([r for r in results if r.status == 'rejected'])}",
        "",
        "## By Document Form",
        "",
    ]
    for key, value in sorted(by_form.items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## By Size Bucket", ""])
    for key, value in sorted(by_bucket.items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Top Packages", ""])
    for key, value in sorted(by_package.items(), key=lambda kv: (-kv[1], kv[0]))[:30]:
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Top Construct Tags", ""])
    for key, value in sorted(by_tag.items(), key=lambda kv: (-kv[1], kv[0]))[:40]:
        lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- This is a seed corpus, not the final frozen benchmark.",
            "- Package-level licenses still need confirmation before redistribution.",
            "- Samples are pdfLaTeX-only and capped at 3 reference-PDF pages.",
        ]
    )
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--texlive-doc", type=Path, default=TEXLIVE_DOC)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--discover-only", action="store_true")
    parser.add_argument("--compile-only", action="store_true")
    parser.add_argument("--preview-only", action="store_true")
    parser.add_argument("--profile", choices=sorted(PROFILE_QUOTAS), default="balanced")
    parser.add_argument("--candidate-target", type=int, default=360)
    parser.add_argument("--max-accept", type=int, default=240)
    parser.add_argument("--max-pages", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260712)
    parser.add_argument("--tiny-fraction", type=float, default=0.08)
    parser.add_argument("--max-file-bytes", type=int, default=350_000)
    parser.add_argument("--max-tree-bytes", type=int, default=8_000_000)
    parser.add_argument("--preview-limit", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    candidates_csv = args.out / "candidates.csv"
    selected_csv = args.out / "selected_candidates.csv"
    results_csv = args.out / "compile_results.csv"
    accepted_csv = args.out / "accepted_manifest.csv"

    if args.preview_only:
        results = read_results_csv(results_csv)
        write_accepted_manifest(results, accepted_csv)
        summarize(results, args.out)
        preview = build_preview(results, args.out, limit=args.preview_limit or None)
        print(f"preview: {preview}")
        return

    if args.compile_only:
        selected = read_candidates_csv(selected_csv)
    else:
        print(f"discovering TeX Live candidates under {args.texlive_doc}")
        candidates = discover(args.texlive_doc, max_file_bytes=args.max_file_bytes)
        candidates.sort(key=lambda c: (profile_score(c, args.profile), c.nonblank_lines), reverse=True)
        write_candidates_csv(candidates, candidates_csv)
        print(f"discovered {len(candidates)} candidates: {candidates_csv}")
        selected = stratified_candidates(
            candidates,
            target=args.candidate_target,
            seed=args.seed,
            tiny_fraction=args.tiny_fraction,
            profile=args.profile,
        )
        write_candidates_csv(selected, selected_csv)
        print(f"selected {len(selected)} candidates: {selected_csv}")
        if args.discover_only:
            return

    results = compile_candidates(
        selected,
        args.out,
        max_accept=args.max_accept,
        timeout=args.timeout,
        max_pages=args.max_pages,
        max_tree_bytes=args.max_tree_bytes,
    )
    write_results_csv(results, results_csv)
    write_accepted_manifest(results, accepted_csv)
    summarize(results, args.out)
    preview = build_preview(results, args.out, limit=args.preview_limit or None)
    print(f"results: {results_csv}")
    print(f"summary: {args.out / 'summary.md'}")
    print(f"preview: {preview}")


if __name__ == "__main__":
    main()
