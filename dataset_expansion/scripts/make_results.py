#!/usr/bin/env python3
"""Aggregate dataset_expansion runs into RESULTS.md (per-set difficulty table).

Reads runs/*/summary.json (written by run_baseline.py) plus the pre-existing
1-turn sonnet rows from harness/runs (the "lathe_hard" reference row).

Run: python3 scripts/make_results.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent.parent
HARNESS = HERE.parent / "harness"

COMPONENTS = ("overall", "content", "layout", "typography", "raster", "pagination")

SET_NOTES = {
    "lathe_overall": "current benchmark, 1/category (lathe prompt_dev)",
    "lathe_hard": "current hard set (harness_baseline core 6+2)",
    "i2s_equation": "image2struct equation snippets",
    "i2s_table": "image2struct table snippets",
    "i2s_algorithm": "image2struct algorithm snippets",
    "i2s_plot": "image2struct TikZ/pgfplots snippets (new category)",
    "pubmed_table": "PubMed clinical tables (messy)",
    "arxiv5t_paper": "arXiv-5T full papers, real figures",
    "neurips_paper": "NeurIPS full papers",
}


def load_runs() -> dict[str, list[dict]]:
    by_set: dict[str, list[dict]] = defaultdict(list)
    for p in sorted((HERE / "runs").glob("*/summary.json")):
        s = json.loads(p.read_text())
        by_set[s.get("set", "?")].append(s)
    # lathe_hard: reuse the merged harness 1-turn sonnet runs
    for p in sorted(HARNESS.glob("runs/*__1turn__sonnet__*/summary.json")):
        s = json.loads(p.read_text())
        # patch in raster_v2 recombination if available
        rv2 = p.parent / "raster_v2.json"
        if rv2.exists() and s.get("final"):
            patch = json.loads(rv2.read_text())
            patch.pop("pages", None)  # raster_v2 page list, not the "2/3" string
            s["final"].update(patch)
        by_set["lathe_hard"].append(s)
    return by_set


def load_agentic_runs() -> list[dict]:
    runs = []
    for path in sorted((HERE / "runs_agentic").glob("*/summary.json")):
        summary = json.loads(path.read_text())
        if summary.get("final"):
            runs.append(summary)
    return runs


def fmt_row(name: str, runs: list[dict]) -> str:
    n = len(runs)
    finals = [r["final"] for r in runs if r.get("final")]
    compiled = [f for f in finals if f.get("compiled") and "overall" in f]
    cost = sum(r.get("cost_usd") or 0 for r in runs)
    if not compiled:
        cells = ["—"] * len(COMPONENTS)
    else:
        cells = [f"{100 * mean(f[c] for f in compiled):.1f}" for c in COMPONENTS]
    pagemis = sum(1 for f in compiled
                  if f.get("pages") and len(set(f["pages"].split("/"))) > 1)
    return (f"| {name} | {n} | {len(compiled)}/{n} | "
            + " | ".join(cells)
            + f" | {pagemis} | {cost:.2f} | {SET_NOTES.get(name, '')} |")


def agentic_check_lines(agentic: list[dict], baseline_runs: dict[str, dict]) -> list[str]:
    if not agentic:
        return []
    compiled = sum(bool((run.get("final") or {}).get("compiled")) for run in agentic)
    scores = [100 * run["final"]["overall"] for run in agentic
              if (run.get("final") or {}).get("compiled")]
    lines = [
        "",
        "## Agentic check — opus low, visual, harness v3 ($3 cap)",
        "",
        f"Six high-difficulty picks (short + verbose). 1-turn sonnet compiled "
        f"{sum(bool((baseline_runs.get(run['sample_id'], {}).get('final') or {}).get('compiled')) for run in agentic)}/{len(agentic)};",
        f"the harness compiled {compiled}/{len(agentic)} but plateaued "
        f"{min(scores):.1f}-{max(scores):.1f} — all below the ~78 the",
        "same harness family reaches on the lathe hard set. All runs stopped on",
        "plateau, not budget. Side-by-side renders: `visual_review/`.",
        "",
        "| sample | 1-turn | harness overall | content | layout | raster | pages | $ | min |",
        "|---|---:|---:|---:|---:|---:|---|---:|---:|",
    ]
    for run in agentic:
        final = run["final"]
        baseline_final = (baseline_runs.get(run["sample_id"], {}).get("final") or {})
        baseline = (f"{100 * baseline_final['overall']:.1f}"
                    if baseline_final.get("compiled") and "overall" in baseline_final else "nc")
        lines.append(
            f"| `{run['sample_id']}` | {baseline} | {100 * final['overall']:.1f} | "
            f"{100 * final['content']:.1f} | {100 * final['layout']:.1f} | "
            f"{100 * final['raster']:.1f} | {final.get('pages', '—')} | "
            f"{(run.get('cost_usd') or 0):.2f} | {(run.get('duration_s') or 0) / 60:.1f} |"
        )
    return lines


def main() -> None:
    by_set = load_runs()
    baseline_runs = {
        run["sample_id"]: run
        for runs in by_set.values()
        for run in runs
        if run.get("sample_id")
    }
    order = ["lathe_overall", "lathe_hard", "i2s_equation", "i2s_table",
             "i2s_algorithm", "i2s_plot", "pubmed_table", "arxiv5t_paper",
             "neurips_paper"]
    lines = [
        "# Dataset expansion — 1-turn sonnet (low effort) difficulty benchmark",
        "",
        "All scores pdf_fidelity_v0.1 with **raster_v0.2**, 0-100, averaged over",
        "*compiled* samples only (compile failures shown in the compile column —",
        "they are the strongest difficulty signal). References for new sets were",
        "compiled with **tectonic** (pdflatex unavailable); lathe rows use the",
        "original pdfLaTeX references.",
        "",
        "| set | n | compiled | overall | content | layout | typography | raster | pagination | page-mismatch | $ | note |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for name in order:
        if name in by_set:
            lines.append(fmt_row(name, by_set[name]))
    for name in sorted(set(by_set) - set(order)):
        lines.append(fmt_row(name, by_set[name]))

    lines += ["", "## Per-sample", ""]
    for name in order:
        for r in by_set.get(name, []):
            f = r.get("final") or {}
            if f.get("compiled") and "overall" in f:
                lines.append(f"- `{r['sample_id']}` ({name}): overall "
                             f"{100*f['overall']:.1f}, pages {f.get('pages')}")
            else:
                lines.append(f"- `{r['sample_id']}` ({name}): **no compile**")
    lines += agentic_check_lines(load_agentic_runs(), baseline_runs)
    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {HERE / 'RESULTS.md'}")


if __name__ == "__main__":
    main()
