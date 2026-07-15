#!/usr/bin/env python3
"""Generate report/dataset_expansion_report.pdf — slide-style deck.

Structure: cover, pipeline, 1-turn difficulty leaderboard, agentic check,
then per-sample case studies with reference-vs-candidate renders showing
what diverges and what the harness fixed over 1-turn.

Rerun: ~/mamba/envs/lathe/bin/python scripts/make_report.py
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

HERE = Path(__file__).resolve().parent.parent  # dataset_expansion/
OUT = HERE / "report" / "dataset_expansion_report.pdf"
VIS = HERE / "visual_review"
PAGE_W, PAGE_H = landscape(A4)

NAVY = colors.HexColor("#14243b")
BLUE = colors.HexColor("#3267a8")
TEAL = colors.HexColor("#168a72")
RED = colors.HexColor("#c74747")
LIGHT = colors.HexColor("#f4f6f8")
MID = colors.HexColor("#d9dfe7")
TEXT = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#5c6773")

ONETURN_ROWS = [
    # set, n, compiled, overall, content, layout, raster, note
    ("lathe_overall", 11, "6/11", 49.7, 89.7, 48.9, 13.2, "current benchmark, 1/category"),
    ("lathe_hard", 8, "6/8", 44.0, 88.4, 38.1, 10.2, "current hard set (core 6+2)"),
    ("i2s_equation", 5, "1/5", 57.7, 64.4, 68.0, 24.7, "image2struct equations"),
    ("i2s_table", 5, "3/5", 68.1, 92.9, 72.8, 27.2, "image2struct tables"),
    ("i2s_algorithm", 5, "5/5", 65.3, 87.4, 73.6, 24.8, "image2struct algorithms"),
    ("i2s_plot", 5, "0/5", None, None, None, None, "TikZ/pgfplots — new category"),
    ("pubmed_table", 5, "2/5", 29.8, 81.1, 28.3, 3.2, "PubMed clinical tables"),
    ("arxiv5t_paper", 5, "1/5", 4.1, 0.9, 23.7, 0.4, "arXiv full papers, real figures"),
    ("neurips_paper", 2, "0/2", None, None, None, None, "NeurIPS full papers"),
]

CASES = [
    ("i2s_plot_001", "TikZ graph drawing (new category)", "nc",
     ["i2s_plot_001_p1_ref_vs_cand.png"],
     ["1-turn: nothing in this set compiles — TikZ has no direct Typst analog.",
      "Harness rebuilds the graph with native Typst curve/circle primitives:",
      "nodes, edges, colors, labels all present (content 98.4).",
      "Residual divergence: figure drawn slightly smaller and shifted, edge-label",
      "fractions collapse, node-label anchors drift, heading typography differs.",
      "Hardness = precise coordinate-space fidelity, not TikZ translation per se."]),
    ("i2s_equation_001", "Dense math derivation (short but tricky)", "nc",
     ["i2s_equation_001_p1_ref_vs_cand.png"],
     ["1-turn fails to compile (emits LaTeX-isms like \\overset as Typst).",
      "Harness compiles and looks close — but content plateaus at 60.7 after",
      "23 turns / 8 score runs. The residual is semantic: subscript stacks like",
      "Var_{P_{s,a,nu0(s)}} flatten or reorder, \\min{} spacing differs, radical",
      "groupings shift token positions.",
      "Hardness = dense-notation translation; the ceiling is semantic, not layout."]),
    ("pubmed_table_004", "Clinical retention-time table (86 rows)", "27.3",
     ["pubmed_table_004_p2_ref_vs_cand.png"],
     ["Reference renders one wide 6-column table; candidate reflows it into",
      "narrower stacked fragments with smaller type and different column breaks.",
      "All cells present (content 77.8) but the table geometry is structurally",
      "different, so layout/raster stay low.",
      "Same reflow failure that dominates the current hard set — at 5x the cell",
      "count, with multi-line cells and paired half-tables."]),
    ("arxiv5t_paper_019", "Real 5-page arXiv paper (REVTeX)", "nc",
     ["arxiv5t_paper_019_p2_ref_vs_cand.png"],
     ["1-turn: no compile. Harness: content 94.5 — it reads like the paper,",
      "but doesn't look like it: REVTeX centered small-caps headings vs Typst",
      "default bold left headings, tighter leading, different display sizing.",
      "Density mismatch compounds page by page: candidate fits in 4 pages",
      "instead of 5 (pages 5/4).",
      "Hardness = document-class-level style emulation, beyond content."]),
    ("neurips_paper_029", "Real 11-page NeurIPS paper", "nc",
     ["neurips_paper_029_p1_ref_vs_cand.png", "neurips_paper_029_p5_ref_vs_cand.png"],
     ["The largest run: $2.16, 12.3 min, 24 turns. Harness holds page count",
      "on an 11-page document (11/11, pagination 96.3) and content 83.8.",
      "Layout stalls at 51.9 — the same class-style drift as the arXiv paper,",
      "compounded across sections, figures and two-column-ish blocks.",
      "Verbose-hard: pagination is winnable, faithful styling is the ceiling."]),
]

AGENTIC_ROWS = []
for run in sorted((HERE / "runs_agentic").glob("*dsx_v3/summary.json")):
    s = json.loads(run.read_text())
    f = s["final"]
    AGENTIC_ROWS.append((s["sample_id"], f, s))


class Deck:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))

    def new_page(self, title: str, subtitle: str = ""):
        c = self.c
        c.setFillColor(LIGHT)
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.rect(0, PAGE_H - 60, PAGE_W, 60, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(36, PAGE_H - 40, title)
        if subtitle:
            c.setFont("Helvetica", 11)
            c.setFillColor(MID)
            c.drawRightString(PAGE_W - 36, PAGE_H - 38, subtitle)

    def text_block(self, x, y, lines, size=11, leading=16, color=TEXT, bold_first=False):
        c = self.c
        for i, line in enumerate(lines):
            c.setFont("Helvetica-Bold" if (bold_first and i == 0) else "Helvetica", size)
            c.setFillColor(color)
            c.drawString(x, y - i * leading, line)
        return y - len(lines) * leading

    def table(self, x, y, headers, rows, widths, size=9):
        c = self.c
        row_h = 17
        c.setFont("Helvetica-Bold", size)
        c.setFillColor(NAVY)
        cx = x
        for h, w in zip(headers, widths):
            c.drawString(cx + 3, y, h)
            cx += w
        y -= 6
        c.setStrokeColor(MID)
        c.line(x, y, x + sum(widths), y)
        for r_i, row in enumerate(rows):
            y -= row_h
            if r_i % 2 == 0:
                c.setFillColor(colors.white)
                c.rect(x, y - 4, sum(widths), row_h, stroke=0, fill=1)
            cx = x
            c.setFont("Helvetica", size)
            for val, w in zip(row, widths):
                c.setFillColor(RED if val in ("nc", "0/5", "0/2") else TEXT)
                c.drawString(cx + 3, y, str(val))
                cx += w
        return y

    def image(self, path: Path, x, y, max_w, max_h):
        img = ImageReader(str(path))
        iw, ih = img.getSize()
        scale = min(max_w / iw, max_h / ih)
        w, h = iw * scale, ih * scale
        self.c.setFillColor(colors.white)
        self.c.rect(x, y - h, w, h, stroke=1, fill=1)
        self.c.drawImage(img, x, y - h, w, h)
        return w, h

    def done(self):
        self.c.showPage()

    def save(self):
        self.c.save()


def main() -> None:
    d = Deck(OUT)

    # ---- cover
    d.new_page("Dataset expansion: benchmarking candidate HF corpora")
    d.text_block(36, PAGE_H - 120, [
        "Question: which HuggingFace datasets raise the difficulty ceiling of the LaTeX->Typst benchmark?",
        "",
        "Probe: 1-turn sonnet-4.6 (low effort) on every set — same prompt & official scoring as harness_baseline —",
        "then an agentic check (opus low, visual, harness v3, $3 cap) on 6 hard picks (short + verbose).",
        "",
        "7 new sets built from: stanford-crfm/image2struct-latex-v1 (equation/table/algorithm/plot),",
        "deepcopy/pubmed-tables-latex-768px, TIGER-Lab/arxiv-latex-5T, Mithilss/neurips-2025-arxiv-latex-sources.",
        "",
        "Caveat: new reference PDFs compiled with tectonic 0.16.9 (XeTeX), not pdfLaTeX — small font-metric drift",
        "vs the lathe canon; acceptable for difficulty ranking.",
    ], size=12, leading=19)
    d.c.setFillColor(MUTED)
    d.c.setFont("Helvetica", 10)
    d.c.drawString(36, 48, f"{date.today().isoformat()} — dataset_expansion/ — scores: pdf_fidelity_v0.1 + raster_v0.2, 0-100")
    d.done()

    # ---- 1-turn leaderboard
    d.new_page("1-turn difficulty probe", "sonnet-4.6, low effort, ~$0.06-0.43/run")
    d.text_block(36, PAGE_H - 90, [
        "Compile rate is the primary signal (a set nobody compiles is past the current ceiling);",
        "component means are over compiled samples only.",
    ], size=11)
    rows = []
    for name, n, comp, ov, ct, ly, ra, note in ONETURN_ROWS:
        rows.append((name, n, comp,
                     f"{ov:.1f}" if ov is not None else "—",
                     f"{ct:.1f}" if ct is not None else "—",
                     f"{ly:.1f}" if ly is not None else "—",
                     f"{ra:.1f}" if ra is not None else "—",
                     note))
    d.table(36, PAGE_H - 140, ["set", "n", "compiled", "overall", "content", "layout", "raster", "note"],
            rows, [110, 30, 60, 55, 55, 55, 55, 240], size=9)
    d.text_block(36, 110, [
        "Ranking: full papers (1/7 compile; the one compile scored 4.1) > i2s_plot (0/5) > pubmed_table (2/5, 29.8)",
        "> i2s_equation (1/5) >> i2s_table / i2s_algorithm (near or easier than the current hard set).",
    ], size=11, bold_first=False)
    d.done()

    # ---- agentic check
    d.new_page("Agentic check: does the harness solve them?", "opus low, visual, harness v3, $3 cap")
    d.text_block(36, PAGE_H - 90, [
        "6 hard picks (short + verbose). 1-turn compiled 1/6; the harness compiled 6/6 — but plateaued at 57.9-67.1,",
        "all below the ~78 the same harness family reaches on the lathe hard set. Every run stopped on plateau, not budget.",
    ], size=11)
    arows = []
    oneturn = {"i2s_plot_001": "nc", "i2s_equation_001": "nc", "pubmed_table_004": "27.3",
               "pubmed_table_005": "nc", "arxiv5t_paper_019": "nc", "neurips_paper_029": "nc"}
    for sid, f, s in AGENTIC_ROWS:
        arows.append((sid, oneturn.get(sid, "?"), f"{100*f['overall']:.1f}",
                      f"{100*f['content']:.1f}", f"{100*f['layout']:.1f}",
                      f"{100*f['raster']:.1f}", f["pages"],
                      f"${s['cost_usd']:.2f}", f"{s['duration_s']/60:.1f}m", s["num_turns"]))
    d.table(36, PAGE_H - 150,
            ["sample", "1-turn", "overall", "content", "layout", "raster", "pages", "cost", "time", "turns"],
            arows, [150, 50, 55, 55, 55, 55, 50, 50, 45, 45], size=9)
    d.text_block(36, 120, [
        "Two hardness flavors emerge:",
        "verbose-hard (papers): content fine, style/pagination breaks;  short-hard (equations): content itself stalls.",
    ], size=11)
    d.done()

    # ---- case studies
    for sid, title, oneturn_score, images, commentary in CASES:
        f = next((f for s, f, _ in AGENTIC_ROWS if s == sid), None)
        sub = (f"1-turn {oneturn_score} -> harness {100*f['overall']:.1f}" if f else "")
        d.new_page(f"Case: {sid} — {title}", sub)
        img_y = PAGE_H - 80
        x = 36
        max_w = (PAGE_W - 72 - 20 * (len(images) - 1)) / len(images)
        for im in images:
            p = VIS / im
            if p.exists():
                w, h = d.image(p, x, img_y, max_w, PAGE_H - 220)
                x += w + 20
        d.c.setFont("Helvetica-Oblique", 9)
        d.c.setFillColor(MUTED)
        d.c.drawString(36, 128, "reference (left) vs harness candidate (right)")
        d.text_block(36, 110, commentary, size=10, leading=14)
        d.done()

    d.save()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
