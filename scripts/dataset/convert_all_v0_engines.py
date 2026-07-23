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
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path


DATASET = Path("data/latex_benchmark_v0")
OUT_DIR = Path("results/latex_benchmark_v0")
FILTER = Path("scripts/dataset/typetex_filter.lua")
ROOT = Path(__file__).resolve().parents[2]


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


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def compile_typst(typ_path: Path, pdf_path: Path, cwd: Path, timeout: int) -> tuple[int, str, float]:
    return run(
        ["typst", "compile", "--root", str(ROOT), str(typ_path), str(pdf_path)],
        cwd,
        timeout,
    )


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


def engine_cmd(engine: str, tex_path: Path, typ_path: Path,
               sample_dir: Path) -> tuple[list[str], str]:
    if engine == "pandoc":
        return [
            "pandoc", "-f", "latex", "-t", "typst",
            "--resource-path", str(sample_dir), str(tex_path), "-o", str(typ_path),
        ], ""
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
            "--resource-path",
            str(sample_dir),
            str(tex_path),
            "-o",
            str(typ_path),
        ], ""
    raise ValueError(engine)


def convert_sample(row: dict, args: argparse.Namespace) -> list[EngineRecord]:
    sample_id = row["sample_id"]
    category = row["category"]
    sample_dir = Path(row["sample_dir"])
    if not sample_dir.is_absolute():
        sample_dir = ROOT / sample_dir
    sample_dir = sample_dir.resolve()
    tex_path = sample_dir / "main.tex"
    rel_dir = Path(category) / sample_id
    out_dir = args.out / rel_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    for asset in sample_dir.rglob("*"):
        if (
            asset.is_file()
            and asset.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".pdf"}
            and asset.name not in {"reference.pdf", "main.pdf"}
        ):
            destination = out_dir / asset.relative_to(sample_dir)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, destination)
    records = []
    for engine in ["pandoc", "tylax", "typetex"]:
        typ_path = out_dir / f"{engine}.typ"
        pdf_path = out_dir / f"{engine}.pdf"
        log_path = out_dir / f"{engine}.log"
        cmd, preamble = engine_cmd(
            engine, tex_path.resolve(), typ_path.resolve(), sample_dir
        )
        # Run converters beside main.tex so real multi-file documents can
        # resolve \input files and graphics using their original source tree.
        conv_rc, conv_log, conv_seconds = run(cmd, sample_dir, args.convert_timeout)
        if preamble and typ_path.exists():
            typ_path.write_text(preamble + typ_path.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        if typ_path.exists():
            typ_path.write_text(patch_typst(typ_path.read_text(encoding="utf-8", errors="replace"), engine), encoding="utf-8")
        comp_rc = 1
        comp_log = ""
        comp_seconds = 0.0
        if conv_rc == 0 and typ_path.exists() and typ_path.stat().st_size > 0:
            comp_rc, comp_log, comp_seconds = compile_typst(
                typ_path.resolve(), pdf_path.resolve(), ROOT, args.compile_timeout
            )
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
                source_tex=relative(tex_path),
                typ_path=relative(typ_path),
                pdf_path=relative(pdf_path),
                conversion_status="ok" if conv_rc == 0 and typ_path.exists() else "failed",
                compile_status="ok" if comp_rc == 0 and pdf_path.exists() else "failed",
                conversion_seconds=round(conv_seconds, 3),
                compile_seconds=round(comp_seconds, 3),
                conversion_returncode=conv_rc,
                compile_returncode=comp_rc,
                log_path=relative(log_path),
            )
        )
    return records


def record_from_csv(row: dict[str, str]) -> EngineRecord:
    values = dict(row)
    for field in ("conversion_seconds", "compile_seconds"):
        values[field] = float(values[field])
    for field in ("conversion_returncode", "compile_returncode"):
        values[field] = int(values[field])
    return EngineRecord(**values)


def summarize(records: list[EngineRecord]) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for record in records:
        summary.setdefault(record.engine, {"converted": 0, "compiled": 0, "total": 0})
        summary[record.engine]["total"] += 1
        summary[record.engine]["converted"] += int(record.conversion_status == "ok")
        summary[record.engine]["compiled"] += int(record.compile_status == "ok")
    return summary


def write_engine_manifest(path: Path, records: list[EngineRecord]) -> None:
    fields = list(EngineRecord.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET)
    parser.add_argument("--out", type=Path, default=OUT_DIR)
    parser.add_argument("--convert-timeout", type=int, default=45)
    parser.add_argument("--compile-timeout", type=int, default=45)
    parser.add_argument(
        "--split",
        type=Path,
        help="convert only sample IDs listed in this CSV",
    )
    parser.add_argument(
        "--sample-id",
        action="append",
        help="convert only this sample ID; repeat for multiple samples",
    )
    args = parser.parse_args()
    args.dataset = args.dataset.resolve()
    args.out = args.out.resolve()

    accepted = args.dataset / "manifests" / "accepted.csv"
    all_rows = list(csv.DictReader(accepted.open(encoding="utf-8")))
    all_ids = {row["sample_id"] for row in all_rows}
    selected_ids = set(all_ids)
    if args.split:
        split_ids = {
            row["sample_id"]
            for row in csv.DictReader(args.split.resolve().open(encoding="utf-8"))
        }
        unknown = sorted(split_ids - all_ids)
        if unknown:
            raise SystemExit(f"split contains unknown accepted sample IDs: {unknown}")
        selected_ids &= split_ids
    if args.sample_id:
        requested = set(args.sample_id)
        unknown = sorted(requested - all_ids)
        if unknown:
            raise SystemExit(f"unknown accepted sample IDs: {unknown}")
        selected_ids &= requested
    rows = [row for row in all_rows if row["sample_id"] in selected_ids]
    if not rows:
        raise SystemExit("selection contains no accepted samples")
    args.out.mkdir(parents=True, exist_ok=True)
    selected_records: list[EngineRecord] = []
    for idx, row in enumerate(rows, start=1):
        print(f"[{idx}/{len(rows)}] {row['category']}/{row['sample_id']}", flush=True)
        recs = convert_sample(row, args)
        selected_records.extend(recs)
        statuses = " ".join(f"{r.engine}:{r.compile_status}" for r in recs)
        print(f"  {statuses}", flush=True)

    manifest = args.out / "engine_manifest.csv"
    updated = {(row.sample_id, row.engine): row for row in selected_records}
    if manifest.exists() and selected_ids != all_ids:
        with manifest.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                key = (row["sample_id"], row["engine"])
                if key not in updated:
                    updated[key] = record_from_csv(row)
    engine_order = {engine: index for index, engine in enumerate(("pandoc", "tylax", "typetex"))}
    row_order = {row["sample_id"]: index for index, row in enumerate(all_rows)}
    all_records = sorted(
        updated.values(),
        key=lambda row: (row_order.get(row.sample_id, len(row_order)), engine_order[row.engine]),
    )
    write_engine_manifest(manifest, all_records)
    write_engine_manifest(args.out / "last_run_manifest.csv", selected_records)

    summary = summarize(all_records)
    last_run_summary = summarize(selected_records)
    write(args.out / "summary.json", json.dumps(summary, indent=2) + "\n")
    write(
        args.out / "last_run_summary.json",
        json.dumps(last_run_summary, indent=2) + "\n",
    )

    failures = [
        {
            "sample_id": record.sample_id,
            "category": record.category,
            "engine": record.engine,
            "conversion_status": record.conversion_status,
            "compile_status": record.compile_status,
            "log_path": record.log_path,
        }
        for record in all_records
        if record.conversion_status != "ok" or record.compile_status != "ok"
    ]
    failure_csv = args.out / "compilation_errors.csv"
    failure_fields = [
        "sample_id", "category", "engine", "conversion_status",
        "compile_status", "log_path",
    ]
    with failure_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=failure_fields, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(failures)
    lines = [
        "# Deterministic engine compilation errors",
        "",
        f"Failures: {len(failures)} of {len(all_records)} engine/sample pairs.",
        "",
        "| Sample | Category | Engine | Conversion | Compile | Log |",
        "|---|---|---|---|---|---|",
    ]
    for failure in failures:
        lines.append(
            "| {sample_id} | {category} | {engine} | {conversion_status} | "
            "{compile_status} | `{log_path}` |".format(**failure)
        )
    write(args.out / "compilation_errors.md", "\n".join(lines) + "\n")
    print(f"manifest: {manifest}", flush=True)
    print("last run:", json.dumps(last_run_summary, indent=2), flush=True)
    print("combined:", json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
