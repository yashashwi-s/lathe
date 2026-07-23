#!/usr/bin/env python3
"""Phase A: rescore already-compiled harness/dsx candidate PDFs with the v2
evidence-vector evaluator (pdf_metric_axes_v2), and compare axis-by-axis
against the stored v0.1 scalar scores.

No API spend: only re-reads existing final_candidate.pdf files.

Run with the lathe env python:
  ~/mamba/envs/lathe/bin/python metric_research/rescore_v2.py
"""
from __future__ import annotations

import csv
import importlib
import json
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
LATHE_DSX = WS / "lathe-dsx"
OUT = WS / "metric_research"
RENDER_DPI = 96  # match the report's frozen evidence (code default is 120)

# representative samples: hard lathe (tables/algo/figure/math) + dsx tiers
SAMPLES = [
    "05_tables_simple_023", "06_tables_moderate_010", "09_algorithms_003",
    "07_figures_captions_007", "04_math_aligned_014",
    "i2s_equation_001", "pubmed_table_004", "i2s_plot_001", "arxiv5t_paper_019",
]

RUN_ROOTS = [
    WS / "harness_baseline" / "runs",
    WS / "dataset_expansion" / "runs",
    WS / "dataset_expansion" / "runs_agentic",
]

sys.path.insert(0, str(LATHE_DSX))
v2 = importlib.import_module("scripts.evaluation.pdf_metric_axes_v2")


def lathe_ref(sample_id: str) -> Path | None:
    split = LATHE_DSX / "data/latex_benchmark_v0/splits/prompt_dev_33.csv"
    if not split.exists():
        return None
    with split.open() as fh:
        for row in csv.DictReader(fh):
            if row["sample_id"] == sample_id:
                p = LATHE_DSX / row["reference_pdf"]
                return p if p.exists() else None
    return None


def dsx_ref(sample_id: str, set_name: str | None) -> Path | None:
    corpus = WS / "dataset_expansion" / "corpus"
    if set_name:
        p = corpus / set_name / sample_id / "reference.pdf"
        if p.exists():
            return p
    for p in corpus.glob(f"*/{sample_id}/reference.pdf"):
        return p
    return None


def resolve_reference(run: Path, summary: dict) -> Path | None:
    local = run / "work" / "reference.pdf"
    if local.exists():
        return local
    sid = summary["sample_id"]
    return lathe_ref(sid) or dsx_ref(sid, summary.get("set"))


def g(d: dict, *path, default=None):
    for k in path:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d


def flatten_axes(axes: dict) -> dict:
    """Pull the decision-relevant scalar from each axis into a flat record."""
    def m(ax):
        return axes.get(ax, {}).get("metrics", {}) or {}
    canvas, content, crit = m("canvas"), m("content"), m("critical_content")
    geom, tl, pag = m("geometry"), m("text_ltsim"), m("pagination")
    ro, typo = m("reading_order"), m("typography")
    rink, rper = m("raster_ink"), m("raster_perceptual")
    ssim_eligible = g(rper, "scored_page_count", default=0) or 0
    return {
        # hard facts
        "page_count_delta": canvas.get("page_count_delta"),
        "canvas_exact_rate": round(canvas.get("exact_paired_size_rate", 0), 3),
        "canvas_wlog_max": round(canvas.get("width_abs_log_ratio_max", 0), 3),
        # content
        "strict_f1": round(g(content, "strict_nfc_token_inventory", "f1", default=0), 3),
        "strict_recall": round(g(content, "strict_nfc_token_inventory", "recall", default=0), 3),
        "strict_prec": round(g(content, "strict_nfc_token_inventory", "precision", default=0), 3),
        "nfkc_edit_sim": round(content.get("compatibility_nfkc_document_edit_similarity", 0), 3),
        # critical inventories
        "number_f1": round(g(crit, "numbers", "f1", default=0), 3),
        "operator_f1": round(g(crit, "operators", "f1", default=0), 3),
        "citation_f1": round(g(crit, "citation_markers", "f1", default=0), 3),
        # geometry
        "center_q50": round(geom.get("center_displacement_q50", 0), 3),
        "center_q90": round(geom.get("center_displacement_q90", 0), 3),
        "geom_ref_cov": round(geom.get("reference_match_coverage", 0), 3),
        # layout transport
        "ltsim_elem": round(tl.get("text_ltsim_element_weighted", 0), 3),
        "ltsim_macro": round(tl.get("text_ltsim_page_macro", 0), 3),
        "ltsim_worst": round(tl.get("text_ltsim_worst_page", 0), 3),
        # pagination / order
        "page_break_f1": round(pag.get("page_break_f1", 0), 3),
        "page_assign_acc": round(pag.get("matched_block_page_assignment_accuracy", 0), 3),
        "kendall_tau": round(ro.get("kendall_tau", 0), 3),
        "tau_cov": round(ro.get("reference_block_coverage", 0), 3),
        # typography
        "typo_style_hmean": round(typo.get("style_coverage_hmean", 0), 3),
        "font_size_q90": round(typo.get("font_size_abs_log_ratio_q90", 0), 3),
        # raster
        "ink_f1_reg": round(rink.get("registered_tolerant_ink_f1_macro", 0), 3),
        "ink_f1_unreg": round(rink.get("unregistered_tolerant_ink_f1_macro", 0), 3),
        "ssim_reg": round(rper.get("registered_ssim_macro", 0), 3) if ssim_eligible else None,
        "ssim_eligible_pages": ssim_eligible,
        # structures
        "tables": axes.get("tables", {}).get("status"),
        "formulas": axes.get("formulas", {}).get("status"),
        "figures": axes.get("figures", {}).get("status"),
    }


def main() -> None:
    rows = []
    runs = []
    for root in RUN_ROOTS:
        if not root.exists():
            continue
        for run in sorted(root.iterdir()):
            sfile = run / "summary.json"
            cand = run / "final_candidate.pdf"
            if not (sfile.exists() and cand.exists()):
                continue
            summary = json.loads(sfile.read_text())
            if summary["sample_id"] not in SAMPLES:
                continue
            runs.append((run, summary, cand))

    print(f"rescoring {len(runs)} candidate PDFs at {RENDER_DPI} DPI\n")
    for i, (run, summary, cand) in enumerate(runs, 1):
        ref = resolve_reference(run, summary)
        sid = summary["sample_id"]
        if ref is None:
            print(f"[{i}/{len(runs)}] {sid:26s} SKIP (no reference.pdf)")
            continue
        try:
            result = v2.evaluate_pdf_pair(ref, cand, render_dpi=RENDER_DPI)
        except Exception as exc:  # noqa: BLE001
            print(f"[{i}/{len(runs)}] {sid:26s} ERROR {exc}")
            continue
        (run / "metric_v2.json").write_text(json.dumps(result, indent=1))
        flat = flatten_axes(result["axes"])
        old = summary.get("final") or {}
        rec = {
            "sample_id": sid,
            "set": summary.get("set") or "lathe_hard",
            "method": summary.get("method", run.name),
            "run": run.name,
            "v01_overall": round(old.get("overall", 0) * 100, 1) if old.get("compiled") else None,
            "v01_layout": round(old.get("layout", 0) * 100, 1) if old.get("compiled") else None,
            "v01_raster": round(old.get("raster", 0) * 100, 1) if old.get("compiled") else None,
            "v01_pagination": round(old.get("pagination", 0) * 100, 1) if old.get("compiled") else None,
            **flat,
        }
        rows.append(rec)
        print(f"[{i}/{len(runs)}] {sid:26s} {rec['method'][:38]:38s} "
              f"v01_ov={rec['v01_overall']} strictF1={flat['strict_f1']} "
              f"pagΔ={flat['page_count_delta']} ltsim={flat['ltsim_macro']} "
              f"inkF1={flat['ink_f1_reg']} ssim={flat['ssim_reg']}")

    if not rows:
        print("no rows produced")
        return
    OUT.mkdir(exist_ok=True)
    fields = list(rows[0].keys())
    with (OUT / "phase_a_v2_scores.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {OUT / 'phase_a_v2_scores.csv'} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
