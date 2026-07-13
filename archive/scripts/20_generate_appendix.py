"""Generate reports/appendix.md directly from ai_models/absolute_scores.json.

The scores table and the grid figure list are both derived from the same JSON at
generation time, so they cannot contradict each other. Run from the repo root, then
build the PDF with:

  pandoc reports/appendix.md -o reports/appendix.pdf --pdf-engine=xelatex \
      -V geometry:margin=2cm
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPHICS = ("tikz", "pgfplots", "posters")

CANDIDATE_ORDER = ["gemini", "gpt", "pandoc", "pandoc_patched", "tylax",
                   "tylax_patched", "typetex", "typetex_patched"]


def fmt(rec):
    status = "Success" if rec.get("compiles", 0) == 1 else "Failed"
    align_type = "SSIM" if any(g in rec["sample_id"] for g in GRAPHICS) else "IoU"
    m = rec.get("content_match_rate")
    p = rec.get("alignment_score")
    m = 0.0 if m is None else m
    p = 0.0 if p is None else p
    tier = rec.get("alignment_deviation", "n/a").replace("_", " ")
    return status, align_type, f"{m:.2f}", f"{p:.3f}", tier


def main():
    records = json.load(open(ROOT / "ai_models" / "absolute_scores.json"))
    by_sample = {}
    for r in records:
        by_sample.setdefault(r["sample_id"], []).append(r)

    lines = [
        "# Appendix: Complete Dataset Visual Alignment",
        "",
        "This appendix contains the compilation status and visual-alignment scores for "
        "every candidate on every sample, followed by side-by-side 2x2 grids comparing "
        "the structural rendering of the three deterministic engines (Pandoc, Tylax, "
        "TypeTeX) against the reference PDF for all 48 samples. Both the table and the "
        "grid labels are generated programmatically from `ai_models/absolute_scores.json` "
        "by `scripts/20_generate_appendix.py` and `scripts/19_generate_report_assets.py`.",
        "",
        "Tier definitions (text IoU): exact >= 0.70, minor 0.40-0.70, major < 0.40. "
        "`content mismatch` means the candidate compiled but no text block could be "
        "matched to the reference at the Jaccard threshold (0.3); `not applicable` "
        "means the candidate did not produce a PDF to align.",
        "",
        "## Full Dataset Scores Table",
        "",
        "| Sample | Candidate | Status | Type | Match | Pos | Tier |",
        "|:--------------------------------|:----------------|:------|:---|:----|:----|:----------|",
    ]

    for sid in sorted(by_sample):
        recs = sorted(by_sample[sid],
                      key=lambda r: CANDIDATE_ORDER.index(r["candidate"]))
        for r in recs:
            status, at, m, p, tier = fmt(r)
            lines.append(f"| {sid} | {r['candidate']} | {status} | {at} | {m} | {p} | {tier} |")

    lines.append("")
    lines.append("\\newpage")
    lines.append("")

    for sid in sorted(by_sample):
        grid = ROOT / "assets" / "appendix_grids" / f"{sid}.png"
        if not grid.exists():
            raise SystemExit(f"missing grid image for {sid}; run 19_generate_report_assets.py first")
        lines.append(f"## {sid}")
        lines.append("")
        lines.append(f"![{sid}](assets/appendix_grids/{sid}.png){{width=100%}}")
        lines.append("")
        lines.append("\\newpage")
        lines.append("")

    out = ROOT / "reports" / "appendix.md"
    out.write_text("\n".join(lines[:-2]) + "\n")  # drop trailing newpage
    print(f"wrote {out} ({len(by_sample)} samples, {len(records)} records)")


if __name__ == "__main__":
    main()
