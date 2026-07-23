#!/usr/bin/env python3
"""v2-axis feedback tool for the harness loop (Phase B).

Run from a work dir containing main.tex, reference.pdf, output.typ.
  feedback_v4.py score [--keep-images]

Compiles output.typ, scores it with pdf_metric_axes_v2 (96 DPI), and prints a
GATE-FIRST, non-compensatory report (no single weighted overall) plus the small
set of continuous drivers Phase A found most informative. Checkpoints the
best-so-far output.typ by (gates_passed, driver_mean).
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

# repo root = <repo>/metric_research/scripts/feedback_v4.py -> parents[2]
REPO = Path(__file__).resolve().parents[2]
RENDER_DPI = 96  # match the frozen report evidence (code default is 120)
sys.path.insert(0, str(REPO))
v2 = importlib.import_module("scripts.evaluation.pdf_metric_axes_v2")


def compile_typ(work: Path) -> tuple[bool, str]:
    pdf = work / "candidate.pdf"
    res = subprocess.run(
        ["typst", "compile", "--root", str(work), str(work / "output.typ"), str(pdf)],
        text=True, capture_output=True)
    (work / "feedback").mkdir(exist_ok=True)
    (work / "feedback" / "compile.log").write_text(res.stderr)
    return res.returncode == 0, res.stderr


def summarize(axes: dict) -> dict:
    def m(a):
        return axes.get(a, {}).get("metrics", {}) or {}
    content, crit, geom = m("content"), m("critical_content"), m("geometry")
    tl, pag, rink = m("text_ltsim"), m("pagination"), m("raster_ink")
    rper, typo = m("raster_perceptual"), m("typography")
    ci = content.get("strict_nfc_token_inventory", {})
    numbers = crit.get("numbers", {})
    return {
        "page_count_delta": pag.get("page_count_delta"),
        "token_precision": ci.get("precision", 0.0),
        "token_recall": ci.get("recall", 0.0),
        "strict_f1": ci.get("f1", 0.0),
        "number_f1": numbers.get("f1"),
        "number_applicable": numbers.get("reference_count", 0) > 0,
        "center_q90": geom.get("center_displacement_q90", 1.0),
        "ltsim_macro": tl.get("text_ltsim_page_macro", 0.0),
        "ink_f1_reg": rink.get("registered_tolerant_ink_f1_macro", 0.0),
        "ssim_reg": (rper.get("registered_ssim_macro")
                     if rper.get("scored_page_count") else None),
        "page_break_f1": pag.get("page_break_f1"),
        "page_assign_acc": pag.get("matched_block_page_assignment_accuracy"),
        "typo_style_hmean": typo.get("style_coverage_hmean", 0.0),
    }


def gate_ladder(s: dict) -> list[tuple[str, bool, str]]:
    gates = []
    gates.append(("G1 page-count", s["page_count_delta"] == 0,
                  f"delta={s['page_count_delta']}"))
    gates.append(("G2 token-recall>=.95", s["token_recall"] >= 0.95,
                  f"recall={s['token_recall']:.3f}"))
    gates.append(("G3 token-prec>=.95", s["token_precision"] >= 0.95,
                  f"prec={s['token_precision']:.3f}"))
    if s["number_applicable"]:
        gates.append(("G4 number-f1==1", (s["number_f1"] or 0) >= 0.999,
                      f"number_f1={s['number_f1']:.3f}"))
    return gates


def driver_mean(s: dict) -> float:
    # three highest-|r|, mutually-informative visual drivers (Phase A)
    return (s["ink_f1_reg"] + s["ltsim_macro"] + max(0.0, 1 - s["center_q90"])) / 3


def main() -> None:
    work = Path.cwd()
    if len(sys.argv) < 2 or sys.argv[1] != "score":
        sys.exit("usage: feedback_v4.py score")
    ok, err = compile_typ(work)
    if not ok:
        print("COMPILE FAILED:\n" + err[:1500])
        sys.exit(1)
    result = v2.evaluate_pdf_pair(work / "reference.pdf", work / "candidate.pdf",
                                  render_dpi=RENDER_DPI)
    (work / "feedback" / "metrics_v2.json").write_text(json.dumps(result, indent=1))
    s = summarize(result["axes"])
    gates = gate_ladder(s)
    passed = sum(1 for _, ok_, _ in gates if ok_)
    dm = driver_mean(s)

    print("=== v2 EVIDENCE VECTOR (no single overall by design) ===")
    print("HARD GATES (must all pass; these are the human-objectionable failures):")
    for name, ok_, detail in gates:
        print(f"  [{'PASS' if ok_ else 'FAIL'}] {name:22s} {detail}")
    print(f"  -> {passed}/{len(gates)} gates passed")
    print("CONTINUOUS DRIVERS (hill-climb these once gates pass; higher=better,"
          " center_q90 lower=better):")
    print(f"  ink_f1_reg={s['ink_f1_reg']:.3f}  ltsim_macro={s['ltsim_macro']:.3f}"
          f"  center_q90={s['center_q90']:.3f}  -> driver_mean={dm:.3f}")
    ssim = f"{s['ssim_reg']:.3f}" if s["ssim_reg"] is not None else "abstain"
    print(f"REPORT-ONLY (do not over-optimize): ssim_reg={ssim}"
          f"  page_break_f1={s['page_break_f1']}  strict_f1={s['strict_f1']:.3f}"
          f"  number_f1={s['number_f1']}  typo={s['typo_style_hmean']:.3f}")

    # best-so-far checkpoint by (gates_passed, driver_mean)
    best_dir = work / "feedback" / "best"
    best_dir.mkdir(parents=True, exist_ok=True)
    marker = best_dir / "key.json"
    key = [passed, round(dm, 4)]
    prev = json.loads(marker.read_text()) if marker.exists() else [-1, -1]
    if key > prev:
        marker.write_text(json.dumps(key))
        (best_dir / "output.typ").write_text((work / "output.typ").read_text())
        print(f"[checkpoint] new best (gates={passed}, driver={dm:.3f})")


if __name__ == "__main__":
    main()
