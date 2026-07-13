#!/usr/bin/env python3
"""Convert the unified benchmark through Pandoc, Tylax, and TypeTeX approx.

Run with:
  mamba run -n lathe python scripts/dataset/convert_all_v0_engines.py
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path


DATASET = Path("data/latex_benchmark_v0")
OUT_DIR = Path("results/latex_benchmark_v0")
FILTER = Path("scripts/dataset/typetex_filter.lua")


@dataclass
class EngineRecord:
    sample_id: str
    category: str
    engine: str
    source_tex: str
    typ_path: str
    pdf_path: str
    conversion_status: str
    compile_status: str
    conversion_seconds: float
    compile_seconds: float
    conversion_returncode: int
    compile_returncode: int
    log_path: str


def run(cmd: list[str], cwd: Path, timeout: int) -> tuple[int, str, float]:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout or "", time.monotonic() - start
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if not isinstance(out, str):
            out = out.decode("utf-8", errors="replace")
        return 124, out + "\nTIMEOUT\n", time.monotonic() - start
    except Exception as exc:
        return 1, f"ERROR: {exc}\n", time.monotonic() - start


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def compile_typst(typ_path: Path, pdf_path: Path, cwd: Path, timeout: int) -> tuple[int, str, float]:
    return run(["typst", "compile", str(typ_path), str(pdf_path)], cwd, timeout)


def patch_typst(content: str, engine: str) -> str:
    """Apply general Typst compile-safety patches.

    These are intentionally broad converter-output repairs, not sample-specific
    rewrites: enable numbering for Pandoc-style references, and degrade
    unresolved citations/refs into visible bracketed text instead of hard Typst
    errors.
    """
    preamble = '#set heading(numbering: "1.")\n#set math.equation(numbering: "1.")\n'
    if engine == "typetex":
        preamble = '#import "@preview/mitex:0.2.4": *\n' + preamble
    labels = set(re.findall(r"<([^>\n]+)>", content))

    def replace_ref(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in labels:
            return "@" + key
        return "[" + key + "]"

    content = re.sub(r"@([A-Za-z0-9:._-]+)", replace_ref, content)
    content = content.replace("\\\\%", "%").replace("\\\\#", "#")
    if not content.startswith(preamble):
        content = preamble + content
    return content


def engine_cmd(engine: str, tex_path: Path, typ_path: Path) -> tuple[list[str], str]:
    if engine == "pandoc":
        return ["pandoc", "-f", "latex", "-t", "typst", str(tex_path), "-o", str(typ_path)], ""
    if engine == "tylax":
        tylax = os.path.expanduser("~/.cargo/bin/t2l")
        return [tylax, "-f", "-o", str(typ_path), str(tex_path)], ""
    if engine == "typetex":
        return [
            "pandoc",
            "-f",
            "latex",
            "-t",
            "typst",
            "--lua-filter",
            str(FILTER.resolve()),
            str(tex_path),
            "-o",
            str(typ_path),
        ], ""
    raise ValueError(engine)


def convert_sample(row: dict, args: argparse.Namespace) -> list[EngineRecord]:
    sample_id = row["sample_id"]
    category = row["category"]
    sample_dir = Path(row["sample_dir"])
    tex_path = sample_dir / "main.tex"
    rel_dir = Path(category) / sample_id
    out_dir = args.out / rel_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for engine in ["pandoc", "tylax", "typetex"]:
        typ_path = out_dir / f"{engine}.typ"
        pdf_path = out_dir / f"{engine}.pdf"
        log_path = out_dir / f"{engine}.log"
        cmd, preamble = engine_cmd(engine, tex_path.resolve(), typ_path.resolve())
        conv_rc, conv_log, conv_seconds = run(cmd, out_dir, args.convert_timeout)
        if preamble and typ_path.exists():
            typ_path.write_text(preamble + typ_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        if typ_path.exists():
            typ_path.write_text(patch_typst(typ_path.read_text(encoding="utf-8", errors="replace"), engine), encoding="utf-8")
        comp_rc = 1
        comp_log = ""
        comp_seconds = 0.0
        if conv_rc == 0 and typ_path.exists() and typ_path.stat().st_size > 0:
            comp_rc, comp_log, comp_seconds = compile_typst(typ_path.resolve(), pdf_path.resolve(), out_dir, args.compile_timeout)
        write(
            log_path,
            "COMMAND:\n"
            + " ".join(cmd)
            + "\n\nCONVERSION LOG:\n"
            + conv_log
            + "\n\nTYPST COMPILE LOG:\n"
            + comp_log,
        )
        records.append(
            EngineRecord(
                sample_id=sample_id,
                category=category,
                engine=engine,
                source_tex=str(tex_path),
                typ_path=str(typ_path),
                pdf_path=str(pdf_path),
                conversion_status="ok" if conv_rc == 0 and typ_path.exists() else "failed",
                compile_status="ok" if comp_rc == 0 and pdf_path.exists() else "failed",
                conversion_seconds=round(conv_seconds, 3),
                compile_seconds=round(comp_seconds, 3),
                conversion_returncode=conv_rc,
                compile_returncode=comp_rc,
                log_path=str(log_path),
            )
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    parser.add_argument("--convert-timeout", type=int, default=45)
    parser.add_argument("--compile-timeout", type=int, default=45)
    args = parser.parse_args()

    accepted = args.dataset / "manifests" / "accepted.csv"
    rows = list(csv.DictReader(accepted.open(encoding="utf-8")))
    args.out.mkdir(parents=True, exist_ok=True)
    all_records: list[EngineRecord] = []
    for idx, row in enumerate(rows, start=1):
        print(f"[{idx}/{len(rows)}] {row['category']}/{row['sample_id']}", flush=True)
        recs = convert_sample(row, args)
        all_records.extend(recs)
        statuses = " ".join(f"{r.engine}:{r.compile_status}" for r in recs)
        print(f"  {statuses}", flush=True)

    manifest = args.out / "engine_manifest.csv"
    fields = list(asdict(all_records[0]).keys()) if all_records else [f.name for f in EngineRecord.__dataclass_fields__.values()]
    with manifest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for record in all_records:
            writer.writerow(asdict(record))

    summary: dict[str, dict[str, int]] = {}
    for record in all_records:
        summary.setdefault(record.engine, {"converted": 0, "compiled": 0, "total": 0})
        summary[record.engine]["total"] += 1
        summary[record.engine]["converted"] += int(record.conversion_status == "ok")
        summary[record.engine]["compiled"] += int(record.compile_status == "ok")
    write(args.out / "summary.json", json.dumps(summary, indent=2) + "\n")
    print(f"manifest: {manifest}", flush=True)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
