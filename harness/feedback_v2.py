#!/usr/bin/env python3
"""v2 feedback tool for the conversion harness. Run with the lathe env python.

Subcommands (run from the sample workdir):
  score  - compile output.typ, score vs reference.pdf, print a fine-grained
           per-component and per-page report, checkpoint best output.typ.
  sweep  - grid-search `typst --input key=value` combos over output.typ,
           score each, report ranked results (requires output.typ to read
           sys.inputs).

Everything printed is either an existing pdf_fidelity_v0.1 number that was
previously hidden (content/layout/typography details, per-page raster
components, pagination subcomponents) or a per-page regrouping of the
existing per-word match scores. The only additional diagnostic is
"registered raster": the same raster metric recomputed after the best global
per-page translation, reported alongside (NOT part of) the official score,
so the agent can tell alignment problems from the font-induced floor.
"""

from __future__ import annotations

import argparse
import itertools
import json
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

LATHE_EVAL = Path(__file__).resolve().parents[1] / "scripts" / "evaluation"
sys.path.insert(0, str(LATHE_EVAL))
from pdf_fidelity import compare_pdfs, create_diagnostic_images, raster_page_metrics, render_page  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from raster_v2 import raster_v2, raster_v2_page, recombine  # noqa: E402


def _ink(img: np.ndarray) -> np.ndarray:
    return (cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) < 245).astype(np.float32)


def registered_raster(reference_pdf: Path, candidate_pdf: Path, pages: int,
                      use_raster_v2: bool = False) -> list[dict]:
    """Official raster metric per page after best global translation (diagnostic).

    With use_raster_v2 the registered score is computed with raster_v0.2 so it
    is directly comparable to the v3 headline raster.
    """
    out = []
    import fitz
    n_ref = fitz.open(reference_pdf).page_count
    n_cand = fitz.open(candidate_pdf).page_count
    for i in range(min(pages, n_ref, n_cand)):
        ref = render_page(reference_pdf, i)
        cand = render_page(candidate_pdf, i)
        h = max(ref.shape[0], cand.shape[0])
        w = max(ref.shape[1], cand.shape[1])
        pad = lambda a: np.pad(a, ((0, h - a.shape[0]), (0, w - a.shape[1]), (0, 0)),
                               constant_values=255)
        ref, cand = pad(ref), pad(cand)
        (dx, dy), _ = cv2.phaseCorrelate(_ink(ref), _ink(cand))
        matrix = np.float32([[1, 0, -dx], [0, 1, -dy]])
        shifted = cv2.warpAffine(cand, matrix, (w, h), borderValue=(255, 255, 255))
        if use_raster_v2:
            metrics = raster_v2_page(ref, shifted)
        else:
            metrics, _ = raster_page_metrics(ref, shifted)
        out.append({"page": i + 1, "shift_px": [round(float(dx), 1), round(float(dy), 1)],
                    "registered_score": metrics["score"], "registered_ink_f1": metrics["ink_f1"]})
    return out


def per_page_layout(result: dict) -> dict[int, dict]:
    """Regroup the existing per-word match scores by reference page."""
    pages: dict[int, dict] = defaultdict(lambda: {"geom": [], "moved_page": 0, "displaced": 0})
    for m in result["matches"]:
        p = pages[m["reference_page"]]
        p["geom"].append(m["geometry_score"])
        if m["reference_page"] != m["candidate_page"]:
            p["moved_page"] += 1
        elif m["position_error"] > 0.05:
            p["displaced"] += 1
    return pages


def print_report(result: dict, ref_data, cand_data, reg: list[dict],
                 rv2: dict | None = None) -> None:
    s = result["scores"]
    if rv2 is not None:
        s = {**s, **{k: rv2[k] for k in ("raster", "visual", "overall")}}
        print("== scores (raster_v0.2; same numbers as final grading) ==")
        print("  " + "  ".join(f"{k}={100 * v:.1f}" for k, v in s.items()))
        print(f"  (raster under old v0.1 would be {100 * result['scores']['raster']:.1f}; "
              "ignore v0.1, you are graded on the numbers above)")
    else:
        print("== scores ==")
        print("  " + "  ".join(f"{k}={100 * v:.1f}" for k, v in s.items()))
    cd = result["content_details"]
    print(f"== content ==  token P/R/F1 {cd['token_precision']:.3f}/{cd['token_recall']:.3f}/"
          f"{cd['token_f1']:.3f}  char_sim {cd['character_similarity']:.3f}  "
          f"order_sim {cd['reading_sequence_similarity']:.3f}")
    ld = result["layout_details"]
    print(f"== layout ==  word_geometry {100 * ld['word_geometry']:.1f}  flow {100 * ld['flow']:.1f}  "
          f"reading_order {100 * ld['reading_order']:.1f}  page_geometry {100 * ld['page_geometry']:.1f}")
    td = result["typography_details"]
    print("== typography ==  " + "  ".join(f"{k} {100 * v:.1f}" for k, v in td.items()))
    ref_pages, cand_pages = result["reference_pages"], result["candidate_pages"]
    count_score = min(ref_pages, cand_pages) / max(1, max(ref_pages, cand_pages))
    print(f"== pagination ==  page_count {ref_pages}/{cand_pages} (score {100 * count_score:.1f})  "
          f"same_page_words {100 * ld['page_assignment']:.1f}")

    ref_unmatched_pages = defaultdict(int)
    for i in result["unmatched_reference_indices"]:
        ref_unmatched_pages[ref_data.words[i].page + 1] += 1
    cand_unmatched_pages = defaultdict(int)
    for i in result["unmatched_candidate_indices"]:
        cand_unmatched_pages[cand_data.words[i].page + 1] += 1

    pages = per_page_layout(result)
    reg_by_page = {r["page"]: r for r in reg}
    raster_pages = rv2["pages"] if rv2 is not None else result["raster_pages"]
    print("== per page ==")
    for rp in raster_pages:
        page = rp["page"]
        lay = pages.get(page)
        geom = 100 * float(np.mean(lay["geom"])) if lay and lay["geom"] else 0.0
        r = reg_by_page.get(page)
        reg_txt = (f"registered_raster {100 * r['registered_score']:.1f} "
                   f"(shift {r['shift_px']} px)") if r else "registered_raster n/a"
        if rv2 is not None:
            raster_txt = (f"raster {100 * rp['score']:.1f} (ink_f1 {100 * rp['ink_f1']:.1f}, "
                          f"edge {100 * rp['edge_score']:.1f}, "
                          f"edge_dist {rp['mean_edge_distance_px']:.1f}px)")
        else:
            raster_txt = (f"raster {100 * rp['score']:.1f} (ink_f1 {100 * rp['ink_f1']:.1f}, "
                          f"edge {100 * rp['edge_score']:.1f}, ssim {100 * rp['foreground_ssim']:.1f})")
        print(f"  p{page}: layout_geom {geom:.1f}  displaced {lay['displaced'] if lay else 0}  "
              f"moved_page {lay['moved_page'] if lay else 0}  "
              f"missing_words {ref_unmatched_pages.get(page, 0)}  "
              f"extra_words {cand_unmatched_pages.get(page, 0)}  |  "
              f"{raster_txt}  {reg_txt}")
    if reg:
        gap = np.mean([r["registered_score"] for r in reg]) - s["raster"]
        if gap > 0.10:
            print(f"  HINT: registered raster is {100 * gap:.0f} pts higher -> global shift/margin "
                  "misalignment; fix margins/paper size.")
        else:
            print("  HINT: registration barely helps -> raster is near its font-rendering floor; "
                  "stop chasing raster, optimize layout/content instead.")
    print(f"flags: {', '.join(result['review_flags']) or 'none'}")


def compile_typ(typ: Path, pdf: Path, inputs: dict[str, str] | None = None) -> tuple[bool, str]:
    cmd = ["typst", "compile"]
    for k, v in (inputs or {}).items():
        cmd += ["--input", f"{k}={v}"]
    cmd += [str(typ), str(pdf)]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return proc.returncode == 0, proc.stderr


def cmd_score(work: Path, keep_images: bool, use_raster_v2: bool = False) -> int:
    fb = work / "feedback"
    fb.mkdir(exist_ok=True)
    ok, err = compile_typ(work / "output.typ", work / "candidate.pdf")
    (fb / "compile.log").write_text(err)
    if not ok:
        print("COMPILE FAILED - see feedback/compile.log:")
        print(err[:3000])
        return 1
    result, ref_data, cand_data, diffs = compare_pdfs(work / "reference.pdf", work / "candidate.pdf")
    if keep_images:
        create_diagnostic_images(result, ref_data, cand_data, diffs, fb / "diagnostics")
    reg = registered_raster(work / "reference.pdf", work / "candidate.pdf",
                            max(result["reference_pages"], result["candidate_pages"]),
                            use_raster_v2=use_raster_v2)
    rv2 = None
    if use_raster_v2:
        rr = raster_v2(work / "reference.pdf", work / "candidate.pdf")
        rv2 = {**recombine(result["scores"], rr["raster"]), "pages": rr["pages"]}
    payload = {k: v for k, v in result.items()
               if k not in {"matches", "unmatched_reference_indices", "unmatched_candidate_indices"}}
    payload["registered_raster_pages"] = reg
    if rv2 is not None:
        payload["raster_v2"] = rv2
        payload["scores_v2"] = {**result["scores"],
                                **{k: rv2[k] for k in ("raster", "visual", "overall")}}
    (fb / "metrics.json").write_text(json.dumps(payload, indent=2) + "\n")
    print_report(result, ref_data, cand_data, reg, rv2=rv2)

    # checkpoint best-so-far (on the same scale the agent sees)
    best_dir = fb / "best"
    best_dir.mkdir(exist_ok=True)
    best_file = best_dir / "score.json"
    overall = rv2["overall"] if rv2 is not None else result["scores"]["overall"]
    prev = json.loads(best_file.read_text())["overall"] if best_file.exists() else -1
    if overall > prev:
        shutil.copy(work / "output.typ", best_dir / "output.typ")
        best_file.write_text(json.dumps({"overall": overall}) + "\n")
        print(f"checkpoint: NEW BEST {100 * overall:.1f} saved to feedback/best/output.typ"
              + (f" (previous {100 * prev:.1f})" if prev >= 0 else ""))
    else:
        print(f"checkpoint: below best {100 * prev:.1f} (current {100 * overall:.1f}); "
              "best kept at feedback/best/output.typ")
    return 0


def cmd_sweep(work: Path, specs: list[str], use_raster_v2: bool = False) -> int:
    grid: dict[str, list[str]] = {}
    for spec in specs:
        key, _, values = spec.partition("=")
        grid[key] = values.split(",")
    combos = [dict(zip(grid, values)) for values in itertools.product(*grid.values())]
    if len(combos) > 60:
        print(f"refusing to sweep {len(combos)} combos (max 60); coarsen the grid")
        return 1
    print(f"sweeping {len(combos)} combos of {list(grid)} "
          "(output.typ must read them via sys.inputs)")
    rows = []
    for combo in combos:
        pdf = work / "feedback" / "sweep_candidate.pdf"
        ok, err = compile_typ(work / "output.typ", pdf, combo)
        if not ok:
            rows.append((None, combo, "compile error: " + err.strip().splitlines()[0][:80] if err.strip() else "compile error"))
            continue
        result, *_ = compare_pdfs(work / "reference.pdf", pdf)
        s = result["scores"]
        if use_raster_v2:
            rr = raster_v2(work / "reference.pdf", pdf)
            s = {**s, **recombine(s, rr["raster"])}
        rows.append((s["overall"], combo,
                     f"overall={100 * s['overall']:.1f} layout={100 * s['layout']:.1f} "
                     f"raster={100 * s['raster']:.1f} pagination={100 * s['pagination']:.1f} "
                     f"pages={result['reference_pages']}/{result['candidate_pages']}"))
    rows.sort(key=lambda r: -(r[0] or -1))
    for overall, combo, desc in rows[:15]:
        print(f"  {json.dumps(combo)}  ->  {desc}")
    if rows and rows[0][0] is not None:
        print(f"BEST: --input " + " --input ".join(f"{k}={v}" for k, v in rows[0][1].items()))
        print("Bake the best values into output.typ as the sys.inputs defaults, then ./score.sh.")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["score", "sweep"])
    ap.add_argument("specs", nargs="*", help="sweep: key=v1,v2 key2=v3,v4")
    ap.add_argument("--workdir", type=Path, default=Path.cwd())
    ap.add_argument("--keep-images", action="store_true")
    ap.add_argument("--raster-v2", action="store_true",
                    help="v3 harness: score/sweep/checkpoint with raster_v0.2")
    args = ap.parse_args()
    if args.command == "score":
        sys.exit(cmd_score(args.workdir, args.keep_images, use_raster_v2=args.raster_v2))
    sys.exit(cmd_sweep(args.workdir, args.specs, use_raster_v2=args.raster_v2))


if __name__ == "__main__":
    main()
