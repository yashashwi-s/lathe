#!/usr/bin/env python3
"""Phase B v2-feedback arm: agentic LaTeX->Typst loop where the mid-run feedback
is the v2 evidence vector (feedback_v4.py) instead of the v0.1 scalar.

Usage:
  run_phaseb.py <sample_dir_or_lathe_id> --model opus --effort medium [--visual]

Pairs with the existing v0.1 arm (harness_baseline/run_task.py --harness v3) on
the same sample/model/effort/budget for a head-to-head A/B.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
HERE = WS / "metric_research"
LATHE_DSX = WS / "lathe-dsx"
LATHE_PY = Path.home() / "mamba/envs/lathe/bin/python"
FEEDBACK = HERE / "feedback_v4.py"
SPLIT = LATHE_DSX / "data/latex_benchmark_v0/splits/prompt_dev_33.csv"
RUNS = HERE / "runs_phaseb"

PROMPT = """You are converting a LaTeX document to Typst (v0.15) with maximum visual fidelity.

Files here:
- main.tex       : LaTeX source (ground-truth content)
- reference.pdf  : the pdfLaTeX render to match (do NOT read the PDF bytes{img})
- output.typ     : YOUR deliverable; write/overwrite this Typst file
- ./score.sh     : compiles output.typ and prints a v2 EVIDENCE VECTOR

This evaluator is NON-COMPENSATORY: there is no single overall score. You are
judged on a GATE LADDER first, then continuous drivers. Your job:
1. Pass every HARD GATE (these are the failures a human reviewer objects to):
   page-count delta = 0, token recall & precision >= 0.95, and number_f1 = 1
   when numbers are present. A high driver score NEVER excuses a failed gate.
2. Once gates pass, hill-climb the CONTINUOUS DRIVERS (ink_f1_reg, ltsim_macro
   up; center_q90 down). The REPORT-ONLY fields (ssim, page_break_f1, strict_f1)
   are diagnostic context, not targets — strict_f1 can be low for math that the
   PDF tokenizes differently even when content is correct, so trust the gates.
{mode}
Procedure: write output.typ, run ./score.sh, iterate. ./score.sh auto-checkpoints
your best version by (gates passed, driver mean); that best version is graded.
Stop when gates pass and drivers plateau.
"""

VIS = ("\nVisual feedback ON: feedback/reference_pages/*.png are the reference"
       " page renders; read them to match margins, paper size, pagination.\n")
NOVIS = ("\nVisual feedback OFF: reason from compile logs, the v2 vector, and the"
         " LaTeX source only. Do not open images or PDFs.\n")


def load_sample(arg: str) -> dict:
    d = Path(arg).expanduser()
    if d.is_dir() and (d / "main.tex").exists():
        return {"sample_id": d.name, "sample_dir": str(d.resolve()),
                "src": d / "main.tex", "ref": d / "reference.pdf"}
    with SPLIT.open() as fh:
        for row in csv.DictReader(fh):
            if row["sample_id"] == arg:
                base = LATHE_DSX
                return {"sample_id": arg, "sample_dir": None,
                        "src": base / row["source_path"],
                        "ref": base / row["reference_pdf"]}
    raise SystemExit(f"sample {arg} not found")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sample")
    ap.add_argument("--model", default="opus")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--visual", action="store_true")
    ap.add_argument("--max-budget-usd", type=float, default=3.0)
    ap.add_argument("--label", default="")
    ap.add_argument("--setup-only", action="store_true")
    args = ap.parse_args()

    s = load_sample(args.sample)
    sid = s["sample_id"]
    label = args.label or datetime.now(timezone.utc).strftime("%m%d_%H%M")
    mode = "visual" if args.visual else "novisual"
    run = RUNS / f"{sid}__{mode}__{args.model}__{label}__v4"
    work = run / "work"
    work.mkdir(parents=True, exist_ok=True)
    shutil.copy(s["src"], work / "main.tex")
    shutil.copy(s["ref"], work / "reference.pdf")
    if s["sample_dir"]:
        sd = Path(s["sample_dir"])
        for p in sd.rglob("*"):
            if (p.is_file() and p.suffix.lower() in
                    (".png", ".jpg", ".jpeg", ".svg", ".pdf", ".sty", ".cls", ".bst", ".bbl")
                    and p.name not in ("reference.pdf", "main.pdf")):
                dst = work / p.relative_to(sd)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(p, dst)
    (work / "score.sh").write_text(
        f'#!/bin/bash\ncd "$(dirname "$0")"\n{LATHE_PY} {FEEDBACK} score\n')
    (work / "score.sh").chmod(0o755)
    if args.visual:
        pd = work / "feedback" / "reference_pages"
        pd.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(LATHE_PY), "-c",
                        "import fitz;d=fitz.open('reference.pdf');"
                        "[p.get_pixmap(dpi=144).save(f'feedback/reference_pages/page_{i+1}.png')"
                        " for i,p in enumerate(d)]"], cwd=work)

    prompt = PROMPT.format(img="; use feedback/reference_pages/*.png" if args.visual else "",
                           mode=VIS if args.visual else NOVIS)
    (run / "prompt.txt").write_text(prompt)
    if args.setup_only:
        print(f"setup complete: {work}")
        return

    cmd = ["claude", "-p", prompt, "--model", args.model, "--effort", args.effort,
           "--max-budget-usd", str(args.max_budget_usd),
           "--output-format", "stream-json", "--verbose",
           "--dangerously-skip-permissions", "--no-session-persistence"]
    if not args.visual:
        cmd += ["--disallowed-tools", "Read(**/*.png)", "Read(**/*.jpg)", "Read(**/*.pdf)"]
    print(f"[{sid}] launching claude v4 ({mode}, {args.model}, {args.effort}, "
          f"${args.max_budget_usd})")
    proc = subprocess.run(cmd, cwd=work, text=True, capture_output=True)
    (run / "claude_transcript.jsonl").write_text(proc.stdout)
    (run / "claude_stderr.log").write_text(proc.stderr)

    # final grade: best checkpoint if present else last edit
    best = work / "feedback" / "best" / "output.typ"
    graded = best if best.exists() else (work / "output.typ")
    final = {"compiled": False}
    if graded.exists():
        pdf = run / "final_candidate.pdf"
        comp = subprocess.run(["typst", "compile", "--root", str(work), str(graded), str(pdf)],
                              text=True, capture_output=True)
        (run / "final_compile.log").write_text(comp.stderr)
        if comp.returncode == 0:
            import importlib, sys as _sys
            _sys.path.insert(0, str(LATHE_DSX))
            v2 = importlib.import_module("scripts.evaluation.pdf_metric_axes_v2")
            res = v2.evaluate_pdf_pair(work / "reference.pdf", pdf, render_dpi=96)
            (run / "final_metrics_v2.json").write_text(json.dumps(res, indent=1))
            final = {"compiled": True, "graded_file": str(graded)}
    meta = {}
    for line in proc.stdout.splitlines():
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("type") == "result":
            meta = {"cost_usd": e.get("total_cost_usd"), "num_turns": e.get("num_turns"),
                    "duration_s": round((e.get("duration_ms") or 0) / 1000)}
    summary = {"sample_id": sid, "arm": "v4_v2feedback", "mode": mode,
               "model": args.model, "effort": args.effort, **meta, "final": final}
    (run / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
