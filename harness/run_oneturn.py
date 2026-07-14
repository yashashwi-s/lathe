#!/usr/bin/env python3
"""1-turn (non-agentic) LaTeX->Typst baseline via the `claude` CLI.

Single prompt containing the LaTeX source; no tools, no feedback, no retry.
The reply is parsed for a Typst code block, compiled, and officially scored.
Writes runs/<sample>__1turn__<model>__<label>/summary.json in the same format
as run_task.py so make_results.py picks it up.

Usage: python3 run_oneturn.py 05_tables_simple_023 --model opus --effort low
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LATHE = HERE.parent                     # repo root (this file lives in lathe/harness/)
LATHE_PY = Path(os.environ.get("LATHE_PY", sys.executable))
COMPARE = LATHE / "scripts/evaluation/compare_pdfs.py"
SPLIT = LATHE / "data/latex_benchmark_v0/splits/prompt_dev_33.csv"

PROMPT = """Convert the following LaTeX document to Typst (v0.15) with maximum \
visual fidelity to its pdfLaTeX render: preserve all content, page size, \
margins, font sizes, spacing, structure, and pagination as closely as possible.

Reply with ONLY the complete Typst source in a single ```typst code block. \
No commentary.

LaTeX source:

```latex
{latex}
```
"""


def load_sample(sample_id: str) -> dict:
    with SPLIT.open() as fh:
        for row in csv.DictReader(fh):
            if row["sample_id"] == sample_id:
                return row
    sys.exit(f"sample {sample_id} not found")


def extract_typst(text: str) -> str | None:
    blocks = re.findall(r"```(?:typst|typ)?\n(.*?)```", text, re.DOTALL)
    if blocks:
        return max(blocks, key=len)
    return text.strip() or None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sample_id")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    sample = load_sample(args.sample_id)
    label = args.label or datetime.now(timezone.utc).strftime("%m%d_%H%M")
    run_dir = HERE / "runs" / f"{args.sample_id}__1turn__{args.model}__{label}"
    run_dir.mkdir(parents=True, exist_ok=True)

    latex = (LATHE / sample["source_path"]).read_text()
    prompt = PROMPT.format(latex=latex)
    (run_dir / "prompt.txt").write_text(prompt)

    proc = subprocess.run(
        ["claude", "-p", prompt, "--model", args.model, "--effort", args.effort,
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

    summary = {
        "sample_id": args.sample_id,
        "mode": "1turn",
        "model": args.model,
        "method": f"claude {args.model} 1-turn (effort {args.effort})",
        "claude_exit": proc.returncode,
        **meta,
        "final": None,
    }
    typst_src = extract_typst(reply) if reply else None
    if typst_src:
        typ = run_dir / "output.typ"
        typ.write_text(typst_src)
        pdf = run_dir / "final_candidate.pdf"
        comp = subprocess.run(["typst", "compile", str(typ), str(pdf)],
                              text=True, capture_output=True)
        (run_dir / "final_compile.log").write_text(comp.stderr)
        if comp.returncode != 0:
            summary["final"] = {"compiled": False}
        else:
            subprocess.run([str(LATHE_PY), str(COMPARE),
                            str(LATHE / sample["reference_pdf"]), str(pdf),
                            "--out-dir", str(run_dir / "final_diagnostics")],
                           text=True, capture_output=True)
            metrics = json.loads((run_dir / "final_diagnostics" / "metrics.json").read_text())
            summary["final"] = {
                "compiled": True, **metrics["scores"],
                "pages": f"{metrics['reference_pages']}/{metrics['candidate_pages']}",
                "review_flags": metrics["review_flags"],
            }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
