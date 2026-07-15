#!/usr/bin/env python3
"""1-turn LaTeX->Typst baseline over dataset_expansion sample sets.

Mirrors harness_baseline/run_oneturn.py (same prompt, same claude CLI flags,
same official scoring via compare_pdfs.py + raster_v0.2 recombination), but
takes any sample dir containing main.tex + reference.pdf.

Usage:
  python3 run_baseline.py corpus/i2s_equation/i2s_equation_001 --model sonnet
  python3 run_baseline.py --set i2s_equation          # all samples in a set
  python3 run_baseline.py --lathe 01_prose_sections_001  # a lathe corpus sample
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent      # dataset_expansion/
WORKSPACE = HERE.parent
LATHE = WORKSPACE / "lathe"
LATHE_PY = Path.home() / "mamba/envs/lathe/bin/python"
COMPARE = LATHE / "scripts/evaluation/compare_pdfs.py"
RUNS = HERE / "runs"

sys.path.insert(0, str(WORKSPACE / "harness_baseline"))
from raster_v2 import raster_v2, recombine  # noqa: E402

PROMPT = """Convert the following LaTeX document to Typst (v0.15) with maximum \
visual fidelity to its pdfLaTeX render: preserve all content, page size, \
margins, font sizes, spacing, structure, and pagination as closely as possible.
{assets_note}
Reply with ONLY the complete Typst source in a single ```typst code block. \
No commentary.

LaTeX source:

```latex
{latex}
```
"""

ASSETS_NOTE = """
The document references these graphics files, which will be present in the \
compile directory (use #image("<path>", ...) as needed):
{files}
"""


def extract_typst(text: str) -> str | None:
    blocks = re.findall(r"```(?:typst|typ)?\n(.*?)```", text, re.DOTALL)
    if blocks:
        return max(blocks, key=len)
    return text.strip() or None


def lathe_sample_dir(sample_id: str) -> Path:
    split = LATHE / "data/latex_benchmark_v0/splits/prompt_dev_33.csv"
    with split.open() as fh:
        for row in csv.DictReader(fh):
            if row["sample_id"] == sample_id:
                return (LATHE / row["source_path"]).parent
    sys.exit(f"lathe sample {sample_id} not found")


def run_sample(sample_dir: Path, set_name: str, model: str, effort: str,
               label: str) -> dict:
    sample_id = sample_dir.name
    run_dir = RUNS / f"{sample_id}__1turn__{model}__{label}"
    if (run_dir / "summary.json").exists():
        print(f"skip {sample_id} (already run)")
        return json.loads((run_dir / "summary.json").read_text())
    run_dir.mkdir(parents=True, exist_ok=True)

    latex = (sample_dir / "main.tex").read_text(errors="replace")
    assets = [p for p in sample_dir.rglob("*")
              if p.is_file() and p.suffix.lower() in
              (".png", ".jpg", ".jpeg", ".svg", ".pdf")
              and p.name not in ("reference.pdf", "main.pdf")]
    note = ""
    if assets:
        rels = [str(p.relative_to(sample_dir)) for p in assets]
        note = ASSETS_NOTE.format(files="\n".join(f"- {r}" for r in rels))
    prompt = PROMPT.format(latex=latex, assets_note=note)
    (run_dir / "prompt.txt").write_text(prompt)

    proc = subprocess.run(
        ["claude", "-p", prompt, "--model", model, "--effort", effort,
         "--tools", "", "--output-format", "json", "--no-session-persistence"],
        text=True, capture_output=True, cwd=run_dir)
    (run_dir / "claude_stdout.txt").write_text(proc.stdout)
    (run_dir / "claude_stderr.log").write_text(proc.stderr)

    reply, meta = "", {}
    if proc.returncode == 0 and proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            reply = payload.get("result", "")
            meta = {"cost_usd": payload.get("total_cost_usd"),
                    "duration_s": round((payload.get("duration_ms") or 0) / 1000)}
        except json.JSONDecodeError:
            reply = proc.stdout

    summary = {"sample_id": sample_id, "set": set_name, "mode": "1turn",
               "model": model, "effort": effort,
               "method": f"claude {model} 1-turn (effort {effort})",
               "claude_exit": proc.returncode, **meta, "final": None,
               "ts": datetime.now(timezone.utc).isoformat()}

    typst_src = extract_typst(reply) if reply else None
    if typst_src:
        work = run_dir / "work"
        work.mkdir(exist_ok=True)
        for p in assets:
            dst = work / p.relative_to(sample_dir)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(p, dst)
        typ = work / "output.typ"
        typ.write_text(typst_src)
        pdf = run_dir / "final_candidate.pdf"
        comp = subprocess.run(["typst", "compile", "--root", str(work),
                               str(typ), str(pdf)],
                              text=True, capture_output=True)
        (run_dir / "final_compile.log").write_text(comp.stderr)
        if comp.returncode != 0:
            summary["final"] = {"compiled": False}
        else:
            ref = sample_dir / "reference.pdf"
            subprocess.run([str(LATHE_PY), str(COMPARE), str(ref), str(pdf),
                            "--out-dir", str(run_dir / "final_diagnostics")],
                           text=True, capture_output=True)
            mfile = run_dir / "final_diagnostics" / "metrics.json"
            if mfile.exists():
                metrics = json.loads(mfile.read_text())
                scores = metrics["scores"]
                r2 = raster_v2(ref, pdf)
                combined = recombine(scores, r2["raster"])
                summary["final"] = {
                    "compiled": True, **scores,
                    "raster_v1": scores["raster"], **combined,
                    "pages": f"{metrics['reference_pages']}/{metrics['candidate_pages']}",
                    "review_flags": metrics["review_flags"]}
            else:
                summary["final"] = {"compiled": True, "scored": False}
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    f = summary.get("final") or {}
    print(f"{sample_id:28s} overall={100*f.get('overall', 0):5.1f} "
          f"compiled={f.get('compiled')} cost=${summary.get('cost_usd') or 0:.2f}")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sample_dirs", nargs="*")
    ap.add_argument("--set", dest="set_name")
    ap.add_argument("--lathe", nargs="*", default=[])
    ap.add_argument("--lathe-set-name", default="lathe")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--label", default="dsx")
    args = ap.parse_args()

    jobs: list[tuple[Path, str]] = []
    if args.set_name:
        for d in sorted((HERE / "corpus" / args.set_name).iterdir()):
            if d.is_dir() and (d / "reference.pdf").exists():
                jobs.append((d, args.set_name))
    for s in args.sample_dirs:
        d = Path(s).resolve()
        jobs.append((d, d.parent.name))
    for sid in args.lathe:
        jobs.append((lathe_sample_dir(sid), args.lathe_set_name))

    total = 0.0
    for d, set_name in jobs:
        s = run_sample(d, set_name, args.model, args.effort, args.label)
        total += s.get("cost_usd") or 0
    print(f"total cost: ${total:.2f}")


if __name__ == "__main__":
    main()
