#!/usr/bin/env python3
"""Regenerate RESULTS.md: methods x metrics tables + cost-vs-score plots.

Rows come from (a) the one-shot baseline CSV and (b) every completed harness
run found in runs/*/summary.json (grouped by method = model + mode + effort).
All fidelity metrics share the 0-100 scale, so aggregates are plain means.
Run with the lathe env python for plots: ~/mamba/envs/lathe/bin/python
(falls back to tables-only if matplotlib is missing).
"""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORE = [
    "06_tables_moderate_010", "05_tables_simple_023", "05_tables_simple_005",
    "09_algorithms_003", "05_tables_simple_021", "07_figures_captions_007",
]
EXTENDED = ["04_math_aligned_014", "03_math_inline_display_004"]
METRICS = ["overall", "content", "layout", "typography", "raster", "pagination"]
BASELINE_METHOD = "gemini-3.1-flash-lite (1-turn cascade)"


def load_methods() -> dict[str, dict[str, dict]]:
    """method name -> sample_id -> entry dict (metrics 0-1, cost, time, iters)."""
    methods: dict[str, dict[str, dict]] = {}

    baseline_v2_path = HERE / "results" / "baseline_raster_v2.json"
    baseline_v2 = json.loads(baseline_v2_path.read_text()) if baseline_v2_path.exists() else {}

    baseline: dict[str, dict] = {}
    with (HERE / "results" / "baseline_oneshot_gemini_flashlite.csv").open() as fh:
        for row in csv.DictReader(fh):
            entry = {k: float(row[k]) for k in METRICS}
            entry["pages"] = f"{row['reference_pages']}/{row['candidate_pages']}"
            entry["token_pr"] = (float(row["token_precision"]), float(row["token_recall"]))
            rescored = baseline_v2.get(row["sample_id"])
            if rescored:  # raster_v0.2 rescoring of the stored PDFs
                entry["raster"] = rescored["raster"]
                entry["overall"] = rescored["overall"]
            baseline[row["sample_id"]] = entry
    methods[BASELINE_METHOD] = baseline

    for summary_path in sorted((HERE / "runs").glob("*/summary.json")):
        data = json.loads(summary_path.read_text())
        final = data.get("final")
        method = data.get("method") or f"claude {data['model']} agentic ({data['mode']})"
        bucket = methods.setdefault(method, {})
        meta = {k: data.get(k) for k in ("cost_usd", "duration_s", "score_runs", "num_turns")}
        if not final or not final.get("compiled"):
            bucket[data["sample_id"]] = {"failed_compile": True, **meta}
            continue
        entry = {k: float(final[k]) for k in METRICS}
        raster_v2_path = summary_path.parent / "raster_v2.json"
        if raster_v2_path.exists():  # raster_v0.2 rescoring of the stored PDFs
            rescored = json.loads(raster_v2_path.read_text())
            entry["raster"] = rescored["raster"]
            entry["overall"] = rescored["overall"]
        entry["pages"] = final.get("pages", "?")
        entry.update(meta)
        metrics_json = summary_path.parent / "final_diagnostics" / "metrics.json"
        if metrics_json.exists():
            details = json.loads(metrics_json.read_text())["content_details"]
            entry["token_pr"] = (details["token_precision"], details["token_recall"])
        bucket[data["sample_id"]] = entry
    return methods


def passes_gates(entry: dict) -> str:
    if entry.get("failed_compile"):
        return "FAIL(G1)"
    if "token_pr" not in entry:
        return "?"
    ref, cand = entry["pages"].split("/")
    if ref != cand or entry["pagination"] < 0.999:
        return "FAIL(G2)"
    p, r = entry["token_pr"]
    if p < 0.95 or r < 0.95:
        return "FAIL(G3)"
    if entry["layout"] < 0.75:
        return "FAIL(G4)"
    return "PASS"


def agg(methods: dict, sample_ids: list[str]) -> dict[str, dict]:
    """method -> aggregate row (means over scored samples, plus cost/time/pass)."""
    out = {}
    for method, samples in methods.items():
        entries = [samples.get(s) for s in sample_ids]
        present = [e for e in entries if e is not None]
        scored = [e for e in present if not e.get("failed_compile")]
        if not present:
            continue
        row = {"n_done": len(present), "n_scored": len(scored), "n_total": len(sample_ids),
               "n_pass": sum(1 for e in present if passes_gates(e) == "PASS")}
        for k in METRICS:
            row[k] = statistics.mean(e[k] for e in scored) if scored else None
        costs = [e["cost_usd"] for e in present if e.get("cost_usd")]
        times = [e["duration_s"] for e in present if e.get("duration_s")]
        iters = [e["score_runs"] for e in present if e.get("score_runs")]
        row["cost"] = statistics.mean(costs) if costs else None
        row["time"] = statistics.mean(times) if times else None
        row["iters"] = statistics.mean(iters) if iters else None
        out[method] = row
    return out


# CLI aliases resolved from the run transcripts ("model" field in API events)
MODEL_VERSIONS = {"opus": "opus-4.7", "sonnet": "sonnet-4.6",
                  "claude-sonnet-4-6": "sonnet-4.6"}
EFFORT_EMOJI = {"low": "⚡", "medium": "⚡⚡", "high": "⚡⚡⚡"}


def split_method(method: str) -> tuple[str, str, str, str]:
    """method string -> (model, effort, feedback, harness) columns."""
    import re
    raw_model = method.split(" (")[0].replace("claude ", "").replace(" 1-turn", "").replace(" agentic", "")
    model = MODEL_VERSIONS.get(raw_model, raw_model)
    effort_match = re.search(r"effort (\w+)", method)
    effort = EFFORT_EMOJI.get(effort_match.group(1), effort_match.group(1)) if effort_match else "—"
    if "1-turn" in method or "cascade" in method:
        feedback, harness = "1-turn", "—"
    else:
        feedback = "👁" if "novisual" not in method else "✗"
        hmatch = re.search(r"\[(v\d+)\]", method)
        harness = hmatch.group(1) if hmatch else "v1"
    return model, effort, feedback, harness


def method_table(rows: dict[str, dict]) -> list[str]:
    # bold = fully-covered method whose mean is the best across ALL rows
    # (a partial method can block bolding but never gets bolded itself)
    best = {k: max((r[k] for r in rows.values() if r[k] is not None), default=None)
            for k in METRICS}
    full = {m: r for m, r in rows.items() if r["n_scored"] == r["n_total"]}
    best_cost = min((r["cost"] for r in full.values() if r["cost"]), default=None)

    lines = ["| model | effort | feedback | harness | " + " | ".join(METRICS) +
             " | pass | $/run | min/run | iters |",
             "|---|---|---|---|" + "---:|" * (len(METRICS) + 4)]
    for method, r in sorted(rows.items(), key=lambda kv: -(kv[1]["overall"] or 0)):
        cells = []
        for k in METRICS:
            if r[k] is None:
                cells.append("nc")
                continue
            v = f"{100 * r[k]:.1f}"
            if r["n_scored"] < r["n_total"]:
                v = f"({v})"
            elif best[k] is not None and abs(r[k] - best[k]) < 1e-9:
                v = f"**{v}**"
            cells.append(v)
        cost = "—" if r["cost"] is None else (
            f"**{r['cost']:.2f}**" if best_cost and abs(r["cost"] - best_cost) < 1e-9
            else f"{r['cost']:.2f}")
        time = "—" if r["time"] is None else f"{r['time'] / 60:.1f}"
        iters = "—" if r["iters"] is None else f"{r['iters']:.0f}"
        model, effort, feedback, harness = split_method(method)
        lines.append(f"| {model} | {effort} | {feedback} | {harness} | " + " | ".join(cells) +
                     f" | {r['n_pass']}/{r['n_done']} | {cost} | {time} | {iters} |")
    lines += ["", "Legend: feedback 👁 = visual diffs available, ✗ = blind "
              "(numeric metrics only), 1-turn = single prompt no tools; effort "
              "⚡/⚡⚡/⚡⚡⚡ = low/medium/high reasoning; harness v2 adds "
              "checkpointing + sweep + fine-grained feedback; v3 additionally "
              "feeds raster_v0.2 + registered-raster into the mid-run loop "
              "(same number as final grading). Parenthesized = "
              "partial coverage (mean over samples scored so far); **bold** = "
              "best fully-covered method per column; nc = nothing compiled; "
              "$/run is the CLI's own accounting (— = cost not captured).", ""]
    return lines


def sample_tables(methods: dict, sample_ids: list[str]) -> list[str]:
    lines: list[str] = []
    for sample in sample_ids:
        rows = {m: s[sample] for m, s in methods.items() if sample in s}
        if not rows:
            continue
        best = max((e["overall"] for e in rows.values() if not e.get("failed_compile")),
                   default=None)
        lines += [f"### `{sample}`", "",
                  "| method | " + " | ".join(METRICS) + " | pages | token P/R | gates | $ |",
                  "|---|" + "---:|" * len(METRICS) + "---|---|---|---:|"]
        for method, e in sorted(rows.items(),
                                key=lambda kv: -(kv[1].get("overall") or 0)):
            cost = f"{e['cost_usd']:.2f}" if e.get("cost_usd") else "—"
            if e.get("failed_compile"):
                lines.append(f"| {method} | " + " | ".join(["nc"] * len(METRICS)) +
                             f" | — | — | FAIL(G1) | {cost} |")
                continue
            pr = e.get("token_pr")
            pr_txt = f"{pr[0]:.3f}/{pr[1]:.3f}" if pr else "?"
            cells = []
            for k in METRICS:
                v = f"{100 * e[k]:.1f}"
                if k == "overall" and best is not None and abs(e[k] - best) < 1e-9:
                    v = f"**{v}**"
                cells.append(v)
            lines.append(f"| {method} | " + " | ".join(cells) +
                         f" | {e['pages']} | {pr_txt} | {passes_gates(e)} | {cost} |")
        lines.append("")
    return lines


def scatter_plot(methods: dict, sample_ids: list[str], out: Path) -> bool:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    fig, ax = plt.subplots(figsize=(9, 6))
    cmap = plt.get_cmap("tab10")
    for i, (method, samples) in enumerate(methods.items()):
        xs, ys = [], []
        for s in sample_ids:
            e = samples.get(s)
            if e and not e.get("failed_compile") and e.get("cost_usd"):
                xs.append(e["cost_usd"])
                ys.append(100 * e["overall"])
        if method == BASELINE_METHOD:
            vals = [100 * samples[s]["overall"] for s in sample_ids if s in samples]
            if vals:
                ax.axhline(statistics.mean(vals), color="gray", ls="--", lw=1,
                           label=f"{method} (mean, cost n/a)")
            continue
        if xs:
            ax.scatter(xs, ys, s=55, alpha=0.85, color=cmap(i % 10), label=method)
    ax.set_xlabel("cost per run (USD)")
    ax.set_ylabel("overall fidelity (0–100)")
    ax.set_title("Cost vs overall score — one point per (sample, run)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return True


def main() -> None:
    methods = load_methods()
    total_cost = sum(e.get("cost_usd") or 0 for s in methods.values() for e in s.values())
    lines = [
        "# Results — methods × metrics on the hardest samples",
        "",
        "All fidelity metrics are 0–100. Content/layout/typography/pagination are",
        "pdf_fidelity_v0.1; **raster is raster_v0.2** (see `raster_v2.py`) — a",
        "rescoring of the *same stored PDFs* (no reruns) with ±4 px ink tolerance,",
        "softer edge decay, and the dead foreground-SSIM term dropped. Overall is",
        "recombined with the unchanged v0.1 weights. Gates = frozen pass criteria",
        "from README (G1 compile, G2 pagination, G3 token P/R ≥ .95, G4 layout ≥ 75;",
        "gates don't depend on raster, so pass/fail is unchanged).",
        "",
        "Metric bounds to read scores against:",
        "",
        "- **Theoretical range** 0–100 for every component; 100 = identical PDF.",
        "- **raster_v0.2 calibration:** identity = 100; a uniform 8 px whole-page",
        "  shift ≈ 96; vs a blank page = 0. The old v0.1 ceiling (~25–30 for",
        "  faithful conversions) was diagnosed as metric harshness, not fonts:",
        "  candidates already embed New Computer Modern (per-word registered ink",
        "  F1 ≈ 0.84 vs the pdfLaTeX reference), while v0.1's foreground SSIM sat",
        "  at ≈ 0.03 for every real pair and its ±2 px ink tolerance was below",
        "  unavoidable cross-engine drift. Best observed raster_v0.2 so far: 78.9.",
        "- **Lower anchor:** the one-shot gemini flash-lite baseline row.",
        "",
        f"Total tracked spend so far: **${total_cost:.2f}**",
        "(agentic + 1-turn runs with cost capture).",
        "",
        "## Aggregate — core 6 hard samples",
        "",
    ]
    lines += method_table(agg(methods, CORE))
    lines += ["## Aggregate — extended set (core 6 + 2 math)",
              "",
              "Only 1-turn methods cover the 2 extra math samples so far.",
              ""]
    lines += method_table(agg(methods, CORE + EXTENDED))
    if scatter_plot(methods, CORE + EXTENDED, HERE / "plots" / "cost_vs_overall.png"):
        lines += ["## Cost vs score", "",
                  "![cost vs overall](plots/cost_vs_overall.png)", ""]
    lines += ["## Per-sample breakdown", ""]
    lines += sample_tables(methods, CORE + EXTENDED)
    (HERE / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {HERE / 'RESULTS.md'} (methods: {len(methods)}, spend ${total_cost:.2f})")


if __name__ == "__main__":
    main()
