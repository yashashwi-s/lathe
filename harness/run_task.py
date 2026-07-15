#!/usr/bin/env python3
"""Iterative LaTeX->Typst conversion harness around the `claude` CLI.

Per sample: sets up an isolated workdir with the LaTeX source, the reference
PDF, and a `score.sh` feedback tool (compile + pdf_fidelity metrics, plus
visual diff images in --visual mode). Then launches a single non-interactive
`claude -p` session that may iterate freely (edit -> score -> edit) within a
turn/budget cap. Finally scores output.typ officially and writes results.

Usage:
  python3 run_task.py 05_tables_simple_023 --visual
  python3 run_task.py 05_tables_simple_023 --no-visual --model claude-sonnet-4-6
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LATHE = HERE.parent                     # repo root (this file lives in lathe/harness/)
LATHE_PY = Path(os.environ.get("LATHE_PY", sys.executable))
COMPARE = LATHE / "scripts/evaluation/compare_pdfs.py"
SPLIT = LATHE / "data/latex_benchmark_v0/splits/prompt_dev_33.csv"

VISUAL_PROMPT_EXTRA = """
Visual feedback is ENABLED. After each ./score.sh run, the directory
feedback/diagnostics/ contains labeled diff images (reference word boxes,
candidate word boxes, raster diff). READ these images with your Read tool to
see exactly where the candidate diverges (red = missing content, blue = extra
content, yellow/orange = displaced). feedback/reference_pages/ has PNG renders
of the reference PDF pages. Use them to match margins, paper size, spacing,
fonts, and pagination.
"""

NO_VISUAL_PROMPT_EXTRA = """
Visual feedback is DISABLED. You may NOT open, render, or read any image or
PDF content. Your only feedback is: typst compile errors and the numeric
metrics printed by ./score.sh (feedback/metrics.json has component details:
content, layout, typography, raster, pagination, token precision/recall,
review flags). Reason about likely visual causes from those numbers and the
LaTeX source alone.
"""

PROMPT_TEMPLATE = """You are converting a LaTeX document to Typst with maximum visual fidelity.

Files in this directory:
- main.tex        : the LaTeX source (ground truth content)
- reference.pdf   : the pdfLaTeX render you must visually match (do not read the PDF bytes directly{ref_img_note})
- output.typ      : YOUR deliverable. Write/overwrite this Typst file.
- ./score.sh      : run it any time; it compiles output.typ with typst and prints
                    fidelity scores (0-100) vs the reference: overall, visual,
                    content, plus components in feedback/metrics.json.

Scoring (deterministic, same as final grading):
overall = content^0.35 * visual^0.65;
visual = pagination^0.10 * layout^0.40 * typography^0.20 * raster^0.30.
Raster comparison is UNREGISTERED: paper size, margins, font size, and line
spacing must match the reference closely or raster craters. Page count and the
page each word lands on matter (pagination). The one-shot LLM baseline for
this sample scored overall={baseline_overall}, and its weakest components were
raster={baseline_raster} and layout={baseline_layout}.
{mode_extra}
Procedure: write a first output.typ, run ./score.sh, then iterate to maximize
the overall score. Prioritize: (1) compiles, (2) page count matches reference,
(3) token recall/precision >= 0.95, (4) layout and raster as high as possible.
Stop when improvements plateau. Your final output.typ is what gets graded.
"""


def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, **kw)


def load_sample(sample_id: str) -> dict:
    with SPLIT.open() as fh:
        for row in csv.DictReader(fh):
            if row["sample_id"] == sample_id:
                return row
    sys.exit(f"sample {sample_id} not found in {SPLIT}")


def load_baseline(sample_id: str) -> dict:
    path = HERE / "results" / "baseline_oneshot_gemini_flashlite.csv"
    if path.exists():
        with path.open() as fh:
            for row in csv.DictReader(fh):
                if row["sample_id"] == sample_id:
                    return row
    return {}


def write_score_script(workdir: Path, visual: bool) -> None:
    keep_images = "" if visual else (
        'rm -rf feedback/diagnostics 2>/dev/null\n'
    )
    script = f"""#!/bin/bash
# Compile output.typ and score it against reference.pdf.
cd "$(dirname "$0")"
mkdir -p feedback
if ! typst compile output.typ candidate.pdf 2> feedback/compile.log; then
  echo "COMPILE FAILED - see feedback/compile.log:"
  cat feedback/compile.log
  exit 1
fi
{LATHE_PY} {COMPARE} reference.pdf candidate.pdf --out-dir feedback/diagnostics > feedback/score.out 2> feedback/score.err
cp feedback/diagnostics/metrics.json feedback/metrics.json 2>/dev/null
{keep_images}cat feedback/score.out
{LATHE_PY} - <<'EOF'
import json
m = json.load(open('feedback/metrics.json'))
s = m['scores']
print('components: ' + ', '.join(f"{{k}}={{100*v:.1f}}" for k, v in s.items()))
print('pages ref/cand:', m['reference_pages'], '/', m['candidate_pages'],
      '| token P/R: %.3f/%.3f' % (m['content_details']['token_precision'], m['content_details']['token_recall']),
      '| flags:', ','.join(m['review_flags']) or 'none')
EOF
"""
    path = workdir / "score.sh"
    path.write_text(script)
    path.chmod(0o755)


V2_FEEDBACK = HERE / "feedback_v2.py"

V2_PROMPT_EXTRA = """
Extra v2 tooling in this directory:
- ./score.sh now prints FINE-GRAINED feedback: every content/layout/typography
  subcomponent, pagination split into page-count vs same-page-word parts, and a
  PER-PAGE line (layout geometry, displaced/missing/extra word counts, raster
  ink/edge/ssim, and a "registered raster" diagnostic = same raster metric
  after best global shift). If registered raster is much higher than raster,
  fix margins/paper size; if not, raster is at its font floor - stop chasing it.
- ./score.sh AUTO-CHECKPOINTS: whenever overall improves, output.typ is copied
  to feedback/best/output.typ. Your best version is never lost; the final
  grade uses the best checkpoint. Feel free to experiment aggressively.
- ./sweep.sh 'margin=1.5cm,2cm,2.5cm' 'fontsize=9pt,10pt,11pt' grid-searches
  typst --input values and prints the ranked results (max 60 combos). To use
  it, write output.typ so tunables read sys.inputs with defaults, e.g.:
    #let margin = sys.inputs.at("margin", default: "2.5cm")
    #set page(margin: eval(margin))
  Then bake the winning values in as the defaults. Use this INSTEAD of
  manually nudging numbers one score-run at a time.
"""


def write_v2_scripts(workdir: Path, visual: bool, raster_v2: bool = False) -> None:
    keep = " --keep-images" if visual else ""
    rv2 = " --raster-v2" if raster_v2 else ""
    (workdir / "score.sh").write_text(
        f"""#!/bin/bash
cd "$(dirname "$0")"
{LATHE_PY} {V2_FEEDBACK} score{keep}{rv2}
""")
    (workdir / "score.sh").chmod(0o755)
    (workdir / "sweep.sh").write_text(
        f"""#!/bin/bash
cd "$(dirname "$0")"
{LATHE_PY} {V2_FEEDBACK} sweep{rv2} "$@"
""")
    (workdir / "sweep.sh").chmod(0o755)


V3_PROMPT_EXTRA = """
v3 metric note: the raster component you are scored on is raster_v0.2 =
0.70*ink_f1(+-4px) + 0.30*exp(-edge_dist/10). It is tolerant to ~4px drift but
still UNREGISTERED: paper size, margins, font size and leading must match.
Each per-page line also shows "registered raster" (same v0.2 metric after the
best global shift). Play strategy:
- registered >> raster  -> a global offset/margin/paper-size problem; fix
  page setup, cheap points.
- registered ~= raster and both low -> the page genuinely renders differently
  (table sized/wrapped differently, wrong leading/font size). Fix the layout;
  do NOT shrink fonts globally just to squeeze pagination - match each
  block's true size from the reference.
- registered ~= raster and both high -> at the engine floor; move on to
  layout/content.
"""


def setup_workdir(sample: dict, run_dir: Path, visual: bool, harness: str) -> Path:
    workdir = run_dir / "work"
    workdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(LATHE / sample["source_path"], workdir / "main.tex")
    shutil.copy(LATHE / sample["reference_pdf"], workdir / "reference.pdf")
    if harness in ("v2", "v3"):
        write_v2_scripts(workdir, visual, raster_v2=harness == "v3")
    else:
        write_score_script(workdir, visual)
    if visual:
        pages_dir = workdir / "feedback" / "reference_pages"
        pages_dir.mkdir(parents=True, exist_ok=True)
        code = (
            "import fitz, sys; doc = fitz.open('reference.pdf')\n"
            "[page.get_pixmap(dpi=144).save(f'feedback/reference_pages/page_{i+1}.png')"
            " for i, page in enumerate(doc)]"
        )
        sh([str(LATHE_PY), "-c", code], cwd=workdir)
    return workdir


def raster_v2_overall(reference: Path, candidate: Path, scores: dict) -> float:
    """Recombined overall under raster_v0.2 (computed in the lathe env)."""
    code = (
        "import json, sys\n"
        f"sys.path.insert(0, {str(HERE)!r})\n"
        "from raster_v2 import raster_v2, recombine\n"
        "r = raster_v2(sys.argv[1], sys.argv[2])\n"
        "print(json.dumps(recombine(json.loads(sys.argv[3]), r['raster'])))\n"
    )
    proc = sh([str(LATHE_PY), "-c", code, str(reference), str(candidate), json.dumps(scores)])
    return json.loads(proc.stdout.strip())["overall"]


def final_score(workdir: Path, out_dir: Path, use_raster_v2: bool = False) -> dict | None:
    """Grade the last edit and (v2/v3) the best checkpoint; keep whichever wins.

    For v3 the winner is chosen by the raster_v0.2-recombined overall (the
    same number the agent optimized); stored metrics stay v0.1 so
    make_results.py rescoring works unchanged.
    """
    candidates = [workdir / "output.typ", workdir / "feedback" / "best" / "output.typ"]
    best_metrics = None
    best_key = -1.0
    for i, typ in enumerate(c for c in candidates if c.exists()):
        pdf = out_dir / f"final_candidate_{i}.pdf"
        diag = out_dir / f"final_diagnostics_{i}"
        compile_res = sh(["typst", "compile", str(typ), str(pdf)])
        (out_dir / f"final_compile_{i}.log").write_text(compile_res.stderr)
        if compile_res.returncode != 0:
            best_metrics = best_metrics or {"compiled": False}
            continue
        sh([str(LATHE_PY), str(COMPARE), str(workdir / "reference.pdf"), str(pdf),
            "--out-dir", str(diag)])
        metrics = json.loads((diag / "metrics.json").read_text())
        metrics["compiled"] = True
        metrics["graded_file"] = str(typ)
        key = (raster_v2_overall(workdir / "reference.pdf", pdf, metrics["scores"])
               if use_raster_v2 else metrics["scores"]["overall"])
        if not best_metrics or not best_metrics.get("compiled") or key > best_key:
            best_metrics = metrics
            best_key = key
    if best_metrics and best_metrics.get("compiled"):
        # keep the canonical names pointing at the winning version
        idx = 1 if "best/output.typ" in best_metrics["graded_file"] else 0
        shutil.copy(out_dir / f"final_candidate_{idx}.pdf", out_dir / "final_candidate.pdf")
        diag_dir = out_dir / "final_diagnostics"
        if diag_dir.exists():
            shutil.rmtree(diag_dir)
        shutil.copytree(out_dir / f"final_diagnostics_{idx}", diag_dir)
    return best_metrics


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sample_id")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--visual", action="store_true")
    mode.add_argument("--no-visual", action="store_true")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--effort", default="low")
    ap.add_argument("--harness", choices=["v1", "v2", "v3"], default="v1")
    ap.add_argument("--max-budget-usd", type=float, default=3.0)
    ap.add_argument("--runs-dir", type=Path, default=HERE / "runs")
    ap.add_argument("--label", default="")
    ap.add_argument("--setup-only", action="store_true",
                    help="Prepare the workdir and prompt without launching claude.")
    args = ap.parse_args()

    visual = args.visual
    sample = load_sample(args.sample_id)
    baseline = load_baseline(args.sample_id)
    mode_name = "visual" if visual else "novisual"
    label = args.label or datetime.now(timezone.utc).strftime("%m%d_%H%M")
    hsuffix = "" if args.harness == "v1" else f"_{args.harness}"
    run_dir = args.runs_dir / f"{args.sample_id}__{mode_name}__{args.model}__{label}{hsuffix}"
    run_dir.mkdir(parents=True, exist_ok=True)
    workdir = setup_workdir(sample, run_dir, visual, args.harness)

    def pct(key: str) -> str:
        return f"{100 * float(baseline[key]):.1f}" if baseline else "n/a"

    mode_extra = VISUAL_PROMPT_EXTRA if visual else NO_VISUAL_PROMPT_EXTRA
    if args.harness in ("v2", "v3"):
        mode_extra += V2_PROMPT_EXTRA
    if args.harness == "v3":
        mode_extra += V3_PROMPT_EXTRA
    prompt = PROMPT_TEMPLATE.format(
        ref_img_note="; use feedback/reference_pages/*.png instead" if visual else "",
        baseline_overall=pct("overall"), baseline_raster=pct("raster"),
        baseline_layout=pct("layout"),
        mode_extra=mode_extra,
    )
    (run_dir / "prompt.txt").write_text(prompt)
    if args.setup_only:
        print(f"setup complete: {workdir}")
        return

    disallowed = [] if visual else ["Read(**/*.png)", "Read(**/*.jpg)", "Read(**/*.pdf)"]
    cmd = [
        "claude", "-p", prompt,
        "--model", args.model,
        "--effort", args.effort,
        "--max-budget-usd", str(args.max_budget_usd),
        "--output-format", "stream-json", "--verbose",
        "--dangerously-skip-permissions",
        "--no-session-persistence",
    ]
    if disallowed:
        cmd += ["--disallowed-tools", *disallowed]

    print(f"[{args.sample_id}] launching claude ({mode_name}, {args.model}, "
          f"effort {args.effort}, budget ${args.max_budget_usd}) in {workdir}")
    proc = subprocess.run(cmd, cwd=workdir, text=True, capture_output=True)
    (run_dir / "claude_transcript.jsonl").write_text(proc.stdout)
    (run_dir / "claude_stderr.log").write_text(proc.stderr)

    result_meta = {}
    tool_calls = 0
    score_runs = 0
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    tool_calls += 1
                    if "score.sh" in json.dumps(block.get("input", {})):
                        score_runs += 1
        elif event.get("type") == "result":
            result_meta = {
                "cost_usd": event.get("total_cost_usd"),
                "num_turns": event.get("num_turns"),
                "duration_s": round((event.get("duration_ms") or 0) / 1000),
                "is_error": event.get("is_error"),
            }

    metrics = final_score(workdir, run_dir, use_raster_v2=args.harness == "v3")
    summary = {
        "sample_id": args.sample_id,
        "mode": mode_name,
        "model": args.model,
        "method": (f"claude {args.model} agentic ({mode_name}, effort {args.effort})"
                   + ("" if args.harness == "v1" else f" [{args.harness}]")),
        "claude_exit": proc.returncode,
        **result_meta,
        "tool_calls": tool_calls,
        "score_runs": score_runs,
        "baseline_overall": float(baseline["overall"]) if baseline else None,
        "final": (
            None if metrics is None
            else {"compiled": False} if not metrics.get("compiled")
            else {"compiled": True, **metrics["scores"],
                  "pages": f"{metrics['reference_pages']}/{metrics['candidate_pages']}",
                  "review_flags": metrics["review_flags"]}
        ),
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
