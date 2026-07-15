#!/usr/bin/env python3
"""raster_v0.2 — tolerant re-scoring of stored PDF pairs (no reruns needed).

Motivation (measured 2026-07-14, see RESULTS.md bounds note): under
pdf_fidelity_v0.1 the raster component had a practical ceiling of ~25-30 even
for visually faithful conversions. Diagnosis on stored artifacts showed the
ceiling is NOT font mismatch (candidates already embed New Computer Modern,
per-word registered ink F1 ~0.84) but metric harshness:

- foreground SSIM ~0.03 for virtually every real pair (25% of weight dead),
- ink F1 tolerance of +-2 px is smaller than unavoidable sub-line drift
  between two typesetting engines,
- edge-distance decay exp(-d/4) saturates at typical drift distances.

raster_v0.2 keeps the same inputs (144 DPI renders, same ink threshold) and
changes only the combination:

    raster_v2 = 0.70 * ink_f1(tolerance +-4 px) + 0.30 * exp(-edge_dist / 10)

Identity still scores 100. Ordering vs v0.1 is preserved (checked on all
stored runs). Overall/visual are recombined with the stored content/layout/
typography/pagination scores using the unchanged v0.1 weights.

Usage:
    ~/mamba/envs/lathe/bin/python raster_v2.py           # rescore everything
    ~/mamba/envs/lathe/bin/python raster_v2.py --check   # validation suite
Writes runs/<run>/raster_v2.json and baseline_raster_v2.json.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import cv2
import fitz
import numpy as np

HERE = Path(__file__).resolve().parent
LATHE = HERE.parent                     # repo root (this file lives in lathe/harness/)
sys.path.insert(0, str(LATHE / "scripts/evaluation"))
from pdf_fidelity import (EPSILON, INK_THRESHOLD, METRIC_CONFIG, _pad_pair,
                          geometric_mean, render_page)

RASTER_V2_VERSION = "raster_v0.2"
TOLERANCE_PX = 4
EDGE_TAU = 10.0
W_INK, W_EDGE = 0.70, 0.30


def raster_v2_page(ref: np.ndarray, cand: np.ndarray) -> dict:
    ref, cand = _pad_pair(ref, cand)
    ref_gray = cv2.cvtColor(ref, cv2.COLOR_RGB2GRAY)
    cand_gray = cv2.cvtColor(cand, cv2.COLOR_RGB2GRAY)
    ref_ink = ref_gray < INK_THRESHOLD
    cand_ink = cand_gray < INK_THRESHOLD
    kernel = np.ones((2 * TOLERANCE_PX + 1, 2 * TOLERANCE_PX + 1), np.uint8)
    ref_dilated = cv2.dilate(ref_ink.astype(np.uint8), kernel) > 0
    cand_dilated = cv2.dilate(cand_ink.astype(np.uint8), kernel) > 0
    recall = float((ref_ink & cand_dilated).sum() / max(1, ref_ink.sum()))
    precision = float((cand_ink & ref_dilated).sum() / max(1, cand_ink.sum()))
    ink_f1 = 2 * precision * recall / max(EPSILON, precision + recall)

    ref_edge = cv2.Canny(ref_gray, 80, 180) > 0
    cand_edge = cv2.Canny(cand_gray, 80, 180) > 0
    if ref_edge.any() and cand_edge.any():
        ref_dist = cv2.distanceTransform((~ref_edge).astype(np.uint8), cv2.DIST_L2, 3)
        cand_dist = cv2.distanceTransform((~cand_edge).astype(np.uint8), cv2.DIST_L2, 3)
        mean_distance = 0.5 * (float(cand_dist[ref_edge].mean()) + float(ref_dist[cand_edge].mean()))
        edge_score = math.exp(-mean_distance / EDGE_TAU)
    elif not ref_edge.any() and not cand_edge.any():
        mean_distance, edge_score = 0.0, 1.0
    else:
        mean_distance, edge_score = float(max(ref_gray.shape)), 0.0
    return {"ink_f1": ink_f1, "edge_score": edge_score,
            "mean_edge_distance_px": mean_distance,
            "score": W_INK * ink_f1 + W_EDGE * edge_score}


def raster_v2(reference_pdf: Path, candidate_pdf: Path) -> dict:
    ref_pages = fitz.open(reference_pdf).page_count
    cand_pages = fitz.open(candidate_pdf).page_count
    pages = []
    for index in range(max(ref_pages, cand_pages)):
        ref = render_page(reference_pdf, index) if index < ref_pages else None
        cand = render_page(candidate_pdf, index) if index < cand_pages else None
        if ref is None:
            ref = np.full(cand.shape, 255, np.uint8)
        if cand is None:
            cand = np.full(ref.shape, 255, np.uint8)
        metric = raster_v2_page(ref, cand)
        metric["page"] = index + 1
        pages.append(metric)
    return {"raster": float(np.mean([p["score"] for p in pages])), "pages": pages}


def recombine(scores: dict, raster: float) -> dict:
    """Recompute visual/overall with the stored non-raster components."""
    vw = METRIC_CONFIG["visual_geometric_mean"]
    ow = METRIC_CONFIG["overall_geometric_mean"]
    visual = geometric_mean([(scores["pagination"], vw["pagination"]),
                             (scores["layout"], vw["layout"]),
                             (scores["typography"], vw["typography"]),
                             (raster, vw["raster"])])
    overall = geometric_mean([(scores["content"], ow["content"]), (visual, ow["visual"])])
    return {"raster": raster, "visual": visual, "overall": overall}


def dataset_reference(sample_id: str) -> Path:
    split = LATHE / "data/latex_benchmark_v0/splits/prompt_dev_33.csv"
    with split.open() as fh:
        for row in csv.DictReader(fh):
            if row["sample_id"] == sample_id:
                return LATHE / row["reference_pdf"]
    raise FileNotFoundError(sample_id)


STAGE_DIRS = {
    "v0": "prompt_v0",
    "v1_targeted_retry": "prompt_v1_v0_failures",
    "v3_rescue": "prompt_v3_prompt_dev_failures",
}
GEMINI = LATHE / "results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite"


def rescore_runs() -> None:
    for summary_path in sorted((HERE / "runs").glob("*/summary.json")):
        run = summary_path.parent
        data = json.loads(summary_path.read_text())
        final = data.get("final")
        if not final or not final.get("compiled"):
            continue
        candidate = run / "final_candidate.pdf"
        reference = run / "work" / "reference.pdf"
        if not reference.exists():
            reference = dataset_reference(data["sample_id"])
        if not candidate.exists():
            candidate = run / "work" / "candidate.pdf"
        result = raster_v2(reference, candidate)
        combined = recombine(final, result["raster"])
        payload = {"metric_version": RASTER_V2_VERSION, "raster_v1": final["raster"],
                   **combined, "pages": result["pages"]}
        (run / "raster_v2.json").write_text(json.dumps(payload, indent=1))
        print(f"{run.name:60s} raster {100*final['raster']:5.1f} -> {100*combined['raster']:5.1f}"
              f"  overall {100*final['overall']:5.1f} -> {100*combined['overall']:5.1f}")


def rescore_baseline() -> None:
    out = {}
    with (HERE / "results" / "baseline_oneshot_gemini_flashlite.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    for row in rows:
        sample = row["sample_id"]
        stage_dir = STAGE_DIRS.get(row["ai_stage"])
        candidate = GEMINI / stage_dir / "samples" / sample / "output.pdf" if stage_dir else None
        if not candidate or not candidate.exists():
            print(f"{sample:40s} SKIP (no output.pdf for stage {row['ai_stage']})")
            continue
        result = raster_v2(dataset_reference(sample), candidate)
        scores = {k: float(row[k]) for k in ("content", "layout", "typography", "pagination")}
        combined = recombine(scores, result["raster"])
        out[sample] = {"metric_version": RASTER_V2_VERSION,
                       "raster_v1": float(row["raster"]), **combined}
        print(f"{sample:40s} raster {100*float(row['raster']):5.1f} -> {100*combined['raster']:5.1f}"
              f"  overall {100*float(row['overall']):5.1f} -> {100*combined['overall']:5.1f}")
    (HERE / "results" / "baseline_raster_v2.json").write_text(json.dumps(out, indent=1))


def check() -> None:
    work = HERE / "runs/05_tables_simple_005__novisual__opus__core/work"
    reference = work / "reference.pdf"
    if not reference.exists():
        # Rendered run inputs are intentionally gitignored. Keep the validation
        # suite reproducible from a clean clone by using the canonical source.
        reference = dataset_reference("05_tables_simple_005")
    ref = render_page(reference, 0)
    print("identity:", round(raster_v2_page(ref, ref.copy())["score"], 4))
    for shift in (1, 2, 4, 8, 16):
        matrix = np.float32([[1, 0, shift], [0, 1, 0]])
        shifted = cv2.warpAffine(ref, matrix, (ref.shape[1], ref.shape[0]),
                                 borderValue=(255, 255, 255))
        print(f"uniform shift {shift:2d}px:", round(raster_v2_page(ref, shifted)["score"], 3))
    blank = np.full_like(ref, 255)
    print("vs blank page:", round(raster_v2_page(ref, blank)["score"], 4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        rescore_runs()
        rescore_baseline()
