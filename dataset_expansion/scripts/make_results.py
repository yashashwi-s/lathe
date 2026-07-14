#!/usr/bin/env python3
"""Aggregate dataset_expansion runs into RESULTS.md (per-set difficulty table).

Reads runs/*/summary.json (written by run_baseline.py) plus the pre-existing
1-turn sonnet rows from harness_baseline/runs (the "lathe_hard" reference row).

Run: python3 scripts/make_results.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent.parent
HARNESS = HERE.parent / "harness_baseline"

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
    # lathe_hard: reuse harness_baseline 1-turn sonnet runs
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


def main() -> None:
    by_set = load_runs()
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
    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {HERE / 'RESULTS.md'}")


if __name__ == "__main__":
    main()
