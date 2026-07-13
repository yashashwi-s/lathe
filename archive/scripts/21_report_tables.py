"""Print every aggregate table used in reports/benchmark_findings.md and
reports/visual_alignment_report.md, computed from ai_models/absolute_scores.json.

Run from the repo root:  python scripts/21_report_tables.py

Aggregation rules (documented in the reports):
- Rubric average: Option B — total earned / total possible across all records,
  scaled to 6.0. Compile failures earn 0 across the board and stay in the
  denominator. See scoring_utils.py.
- Patched ceiling: for each engine, substitute the patched record where one
  exists, otherwise use the base record (exactly 48 records per engine).
- Text Content Match (full corpus): mean content_match_rate over all 48 samples;
  graphics samples count 1.0 when compiled (SSIM implies full-structure match)
  and 0.0 when failed; None counts 0.0.
- Text Position (Mean IoU): mean alignment_score over the 36 text samples,
  None/failures as 0.0.
- Graphics Alignment (Mean SSIM): mean alignment_score over the 12 graphics
  samples, None/failures as 0.0.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scoring_utils import compute_average, get_pass_rate, get_patched_ceiling_records

ROOT = Path(__file__).resolve().parent.parent
GRAPHICS = ("tikz", "pgfplots", "posters")
FAIR = ["prose_easy", "prose_hard", "eq_simple_hard", "eq_hard_hard",
        "tables_complex_easy", "tables_complex_hard", "algorithms_easy", "algorithms_medium"]
METRICS = ["compiles", "no_leaked_source", "text_completeness",
           "structural_elements", "numbering_correctness", "typography_correctness"]
ENGINES = ["pandoc", "tylax", "typetex"]


def z(v):
    return 0.0 if v is None else v


def visual_aggregates(recs, cand, samples=None):
    rs = [r for r in recs if r["candidate"] == cand
          and (samples is None or r["sample_id"] in samples)]
    text = [r for r in rs if not any(g in r["sample_id"] for g in GRAPHICS)]
    gfx = [r for r in rs if any(g in r["sample_id"] for g in GRAPHICS)]
    match_vals = [z(r.get("content_match_rate")) for r in rs]
    tm = sum(match_vals) / len(rs) if rs else None
    iou = sum(z(r.get("alignment_score")) for r in text) / len(text) if text else None
    ss = sum(z(r.get("alignment_score")) for r in gfx) / len(gfx) if gfx else None
    return tm, iou, ss


def main():
    recs = json.load(open(ROOT / "ai_models" / "absolute_scores.json"))
    print(f"records: {len(recs)}\n")

    print("## Fair-Subset rubric averages (8 categories, / 6.0)")
    for c in ["gemini", "gpt"]:
        rs = [r for r in recs if r["candidate"] == c and r["sample_id"] in FAIR]
        print(f"  {c:18s} {compute_average(rs):.2f}")
    for e in ENGINES:
        rs = [r for r in get_patched_ceiling_records(recs, e) if r["sample_id"] in FAIR]
        print(f"  {e+' (patched)':18s} {compute_average(rs):.2f}")

    print("\n## Full-corpus rubric averages (48 samples, engines)")
    for e in ENGINES:
        base = [r for r in recs if r["candidate"] == e]
        ceil = get_patched_ceiling_records(recs, e)
        print(f"  {e:8s} as-tested {compute_average(base):.2f}   patched ceiling {compute_average(ceil):.2f}")

    print("\n## Metric pass rates, Fair-Subset (%)")
    print("  candidate          " + "  ".join(f"{m[:9]:>9s}" for m in METRICS))
    for c in ["gemini", "gpt"]:
        rs = [r for r in recs if r["candidate"] == c and r["sample_id"] in FAIR]
        print(f"  {c:18s} " + "  ".join(f"{get_pass_rate(rs, m):9.1f}" for m in METRICS))
    for e in ENGINES:
        rs = [r for r in get_patched_ceiling_records(recs, e) if r["sample_id"] in FAIR]
        print(f"  {e+' (patched)':18s} " + "  ".join(f"{get_pass_rate(rs, m):9.1f}" for m in METRICS))

    print("\n## Metric pass rates, Full Corpus patched ceiling (%)")
    for e in ENGINES:
        rs = get_patched_ceiling_records(recs, e)
        print(f"  {e+' (patched)':18s} " + "  ".join(f"{get_pass_rate(rs, m):9.1f}" for m in METRICS))

    print("\n## Visual alignment, Fair-Subset (match / IoU)")
    for c in ["gemini", "gpt"] + ENGINES:
        tm, iou, _ = visual_aggregates(recs, c, FAIR)
        print(f"  {c:8s} match {tm:.3f}   iou {iou:.3f}")

    print("\n## Visual alignment, Full Corpus (match / IoU / SSIM)")
    for c in ENGINES:
        tm, iou, ss = visual_aggregates(recs, c)
        print(f"  {c:8s} match {tm:.3f}   iou {iou:.3f}   ssim {ss:.3f}")


if __name__ == "__main__":
    main()
