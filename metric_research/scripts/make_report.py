#!/usr/bin/env python3
"""Generate metric_research/report/metric_harness_report.pdf.

Slide-style deck (mirrors harness_baseline / dataset_expansion make_report.py,
canvas-drawn tables so they always render). Question:

  Does driving the agentic harness loop with the v2 EVIDENCE VECTOR (gate-first,
  non-compensatory) beat the v0.1 SCALAR feedback on hard LaTeX->Typst samples?

Per sample it compares, side by side:
  reference  |  arm A (v0.1 scalar feedback)  |  arm B (v2 evidence-vector feedback)
with per-metric isolation (v2 gates + drivers), cost/duration/turns, and a
commentary on what each feedback regime fixed vs missed.

Rerun: ~/mamba/envs/lathe/bin/python metric_research/make_report.py
"""
from __future__ import annotations

import importlib
import json
import sys
from datetime import date
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

WS = Path(__file__).resolve().parent.parent
HERE = WS / "metric_research"
LATHE_DSX = WS / "lathe-dsx"
OUT = HERE / "report" / "metric_harness_report.pdf"
VIS = HERE / "report" / "assets"
LABEL = "ab2"

sys.path.insert(0, str(LATHE_DSX))
sys.path.insert(0, str(HERE))
v2 = importlib.import_module("scripts.evaluation.pdf_metric_axes_v2")
fb = importlib.import_module("feedback_v4")

PAGE_W, PAGE_H = landscape(A4)
NAVY = colors.HexColor("#14243b")
BLUE = colors.HexColor("#3267a8")
TEAL = colors.HexColor("#168a72")
RED = colors.HexColor("#c74747")
AMBER = colors.HexColor("#b8860b")
LIGHT = colors.HexColor("#f4f6f8")
MID = colors.HexColor("#d9dfe7")
TEXT = colors.HexColor("#1f2933")
MUTED = colors.HexColor("#5c6773")

# sample_id -> (title, page_index_to_show, category_or_set)
SAMPLES = [
    ("06_tables_moderate_010", "Table reflow, 2->3 pages (lathe hard)", 0, "lathe"),
    ("05_tables_simple_023", "Table + invented rows (lathe hard)", 0, "lathe"),
    ("09_algorithms_003", "Algorithm block, math extraction (lathe hard)", 1, "lathe"),
    ("pubmed_table_004", "Clinical retention-time table (dsx)", 1, "pubmed_table"),
    ("arxiv5t_paper_019", "Real 5-page arXiv paper (dsx, verbose)", 1, "arxiv5t_paper"),
    ("i2s_equation_001", "Dense math derivation (dsx, short/tricky)", 0, "i2s_equation"),
]

ARM_A_DIR = WS / "harness_baseline" / "runs"
ARM_B_DIR = HERE / "runs_phaseb"


def lathe_ref(sid: str) -> Path | None:
    import csv
    split = LATHE_DSX / "data/latex_benchmark_v0/splits/prompt_dev_33.csv"
    with split.open() as fh:
        for row in csv.DictReader(fh):
            if row["sample_id"] == sid:
                p = LATHE_DSX / row["reference_pdf"]
                return p if p.exists() else None
    return None


def resolve_ref(sid: str, cat: str) -> Path | None:
    if cat == "lathe":
        return lathe_ref(sid)
    p = WS / "dataset_expansion" / "corpus" / cat / sid / "reference.pdf"
    return p if p.exists() else None


def arm_a_run(sid: str) -> Path | None:
    d = ARM_A_DIR / f"{sid}__visual__opus__{LABEL}_v3"
    return d if (d / "summary.json").exists() else None


def arm_b_run(sid: str) -> Path | None:
    d = ARM_B_DIR / f"{sid}__visual__opus__{LABEL}__v4"
    return d if (d / "summary.json").exists() else None


def baseline_run(sid: str) -> Path | None:
    for pat in [ARM_A_DIR / f"{sid}__1turn__opus__base",
                WS / "dataset_expansion" / "runs" / f"{sid}__1turn__sonnet__dsx"]:
        if (pat / "final_candidate.pdf").exists():
            return pat
    return None


def v2_vector(ref: Path, cand: Path) -> dict | None:
    if not (ref and cand and ref.exists() and cand.exists()):
        return None
    res = v2.evaluate_pdf_pair(ref, cand, render_dpi=96)
    s = fb.summarize(res["axes"])
    gates = fb.gate_ladder(s)
    s["gates_passed"] = sum(1 for _, ok, _ in gates if ok)
    s["gates_total"] = len(gates)
    s["gates_detail"] = gates
    s["driver_mean"] = fb.driver_mean(s)
    # critical-content evidence for gate callouts
    num = res["axes"].get("critical_content", {}).get("metrics", {}).get("numbers", {})
    s["num_missing"] = num.get("missing", [])[:4]
    s["num_extra"] = num.get("extra", [])[:4]
    s["_res"] = res
    return s


# annotation colors (RGB) — mapped to the metric each box points at
BOX_RASTER = (206, 71, 71)     # red   -> largest visual/raster diff (ink_f1 / ssim)
BOX_MOVE = (219, 134, 11)      # amber -> most-displaced matched word (center_q90 / ltsim)
LEGEND = [
    (BOX_RASTER, "red = biggest raster/appearance diff (ink_f1, ssim)"),
    (BOX_MOVE, "amber = most-displaced matched word (center_q90)"),
]


def render_page(pdf: Path, page_idx: int, target_w: int = 700):
    if not (pdf and pdf.exists()):
        return None, 1.0
    doc = fitz.open(pdf)
    if len(doc) == 0:
        return None, 1.0
    idx = min(page_idx, len(doc) - 1)
    pix = doc[idx].get_pixmap(dpi=110)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    scale = target_w / img.width
    return img.resize((target_w, int(img.height * scale))), scale


def page_boxes(result: dict | None, page_idx: int, which: str) -> list[tuple]:
    """Pull normalized bboxes + labels from the v2 evidence for one page.
    which = 'candidate' or 'reference'. Returns (nx0,ny0,nx1,ny1,color,label)."""
    if not result:
        return []
    ax = result["axes"]
    boxes = []
    for pg in ax.get("raster_perceptual", {}).get("evidence", {}).get("pages", []):
        if pg.get("page") == page_idx:
            bb = (pg.get("registered_difference_bbox") or {}).get("normalized_bbox")
            if bb:
                boxes.append((*bb, BOX_RASTER, "raster diff"))
    for t in ax.get("geometry", {}).get("evidence", {}).get("worst_token_pairs", [])[:2]:
        if t.get(f"{which}_page") == page_idx:
            bb = t.get(f"{which}_bbox_normalized")
            if bb:
                tok = (t.get("token") or "").strip()[:12]
                boxes.append((*bb, BOX_MOVE, f"moved '{tok}'"))
    return boxes


def annotate(img: Image.Image, boxes: list[tuple]) -> None:
    d = ImageDraw.Draw(img)
    W, H = img.size
    try:
        f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
    except Exception:
        f = ImageFont.load_default()
    for nx0, ny0, nx1, ny1, color, label in boxes:
        x0, y0, x1, y1 = nx0 * W, ny0 * H, nx1 * W, ny1 * H
        d.rectangle([x0, y0, x1, y1], outline=color, width=4)
        ty = max(0, y0 - 18)
        tw = d.textlength(label, font=f)
        d.rectangle([x0, ty, x0 + tw + 6, ty + 17], fill=color)
        d.text((x0 + 3, ty + 1), label, fill="white", font=f)


def labeled(img, label, boxes=None, w=700, h=760) -> Image.Image:
    canvas_img = Image.new("RGB", (w, h + 34), "white")
    d = ImageDraw.Draw(canvas_img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except Exception:
        font = ImageFont.load_default()
    d.rectangle([0, 0, w, 30], fill=(20, 36, 59))
    d.text((8, 5), label, fill="white", font=font)
    if img is None:
        d.text((10, 60), "(no compile / missing)", fill=(180, 60, 60), font=font)
    else:
        if boxes:
            annotate(img, boxes)
        ph = min(img.height, h)
        canvas_img.paste(img.crop((0, 0, img.width, ph)), (0, 34))
    return canvas_img


def build_comparison(sid: str, cat: str, page_idx: int, va_res=None, vb_res=None) -> Path | None:
    ref = resolve_ref(sid, cat)
    a = arm_a_run(sid)
    b = arm_b_run(sid)
    cand_a = (a / "final_candidate.pdf") if a else None
    cand_b = (b / "final_candidate.pdf") if b else None
    ref_img, _ = render_page(ref, page_idx)
    a_img, _ = render_page(cand_a, page_idx)
    b_img, _ = render_page(cand_b, page_idx)
    imgs = [
        labeled(ref_img, "REFERENCE (pdfLaTeX)"),
        labeled(a_img, "ARM A: v0.1 scalar feedback", page_boxes(va_res, page_idx, "candidate")),
        labeled(b_img, "ARM B: v2 evidence-vector feedback", page_boxes(vb_res, page_idx, "candidate")),
    ]
    h = max(i.height for i in imgs)
    total = Image.new("RGB", (sum(i.width for i in imgs) + 40, h), "white")
    x = 0
    for i in imgs:
        total.paste(i, (x, 0))
        x += i.width + 20
    VIS.mkdir(parents=True, exist_ok=True)
    out = VIS / f"{sid}_cmp.png"
    total.save(out)
    return out


class Deck:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))

    def page(self, title: str, subtitle: str = ""):
        c = self.c
        c.setFillColor(LIGHT); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setFillColor(NAVY); c.rect(0, PAGE_H - 58, PAGE_W, 58, stroke=0, fill=1)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold", 19)
        c.drawString(34, PAGE_H - 38, title)
        if subtitle:
            c.setFont("Helvetica", 10); c.setFillColor(MID)
            c.drawRightString(PAGE_W - 34, PAGE_H - 37, subtitle)

    def lines(self, x, y, lines, size=11, lead=15, color=TEXT, bold_first=False):
        for i, ln in enumerate(lines):
            self.c.setFont("Helvetica-Bold" if (bold_first and i == 0) else "Helvetica", size)
            self.c.setFillColor(color)
            self.c.drawString(x, y - i * lead, ln)
        return y - len(lines) * lead

    def table(self, x, y, headers, rows, widths, size=10, rh=24, bold_cells=None,
              band_rows=None):
        """band_rows: set of row indices to shade darker (e.g. AVG rows).
        bold_cells: set of (row_index, col_index) to render bold+navy."""
        c = self.c
        bold_cells = bold_cells or set()
        band_rows = band_rows or set()
        c.setFont("Helvetica-Bold", size + 1); c.setFillColor(NAVY)
        cx = x
        for h, w in zip(headers, widths):
            c.drawString(cx + 2, y, h); cx += w
        y -= 7
        c.setStrokeColor(NAVY); c.setLineWidth(1.2); c.line(x, y, x + sum(widths), y)
        c.setLineWidth(1)
        for ri, row in enumerate(rows):
            y -= rh
            if ri in band_rows:
                c.setFillColor(MID); c.rect(x, y - 4, sum(widths), rh, stroke=0, fill=1)
            elif ri % 2 == 0:
                c.setFillColor(colors.white); c.rect(x, y - 4, sum(widths), rh, stroke=0, fill=1)
            cx = x
            for ci, (val, w) in enumerate(zip(row, widths)):
                sval = str(val)
                is_bold = ci == 0 or ri in band_rows or (ri, ci) in bold_cells
                c.setFont("Helvetica-Bold" if is_bold else "Helvetica", size)
                col = TEXT
                if sval in ("FAIL", "nc") or sval.endswith("FAIL"):
                    col = RED
                elif sval == "PASS" or sval.endswith("PASS"):
                    col = TEAL
                elif (ri, ci) in bold_cells:
                    col = TEAL
                c.setFillColor(col)
                c.drawString(cx + 2, y, sval); cx += w
        return y

    def image(self, path: Path, x, y, max_w, max_h):
        img = ImageReader(str(path)); iw, ih = img.getSize()
        s = min(max_w / iw, max_h / ih); w, h = iw * s, ih * s
        self.c.drawImage(img, x, y - h, w, h)
        return w, h

    def done(self):
        self.c.showPage()

    def save(self):
        self.c.save()


def fmt(v, p=3):
    return f"{v:.{p}f}" if isinstance(v, (int, float)) else "—"


def main() -> None:
    # collect
    data = []
    for sid, title, pidx, cat in SAMPLES:
        ref = resolve_ref(sid, cat)
        a, b, base = arm_a_run(sid), arm_b_run(sid), baseline_run(sid)
        sa = json.loads((a / "summary.json").read_text()) if a else None
        sb = json.loads((b / "summary.json").read_text()) if b else None
        va = v2_vector(ref, a / "final_candidate.pdf") if a else None
        vb = v2_vector(ref, b / "final_candidate.pdf") if b else None
        vbase = v2_vector(ref, base / "final_candidate.pdf") if base else None
        cmp_png = build_comparison(sid, cat, pidx,
                                   va_res=va.get("_res") if va else None,
                                   vb_res=vb.get("_res") if vb else None)
        data.append(dict(sid=sid, title=title, cat=cat, sa=sa, sb=sb,
                         va=va, vb=vb, vbase=vbase, cmp=cmp_png))

    d = Deck(OUT)

    # cover
    d.page("v0.1 scalar vs v2 evidence-vector feedback in the agentic harness")
    d.lines(34, PAGE_H - 130, [
        "Question: the v2 metric (pdf_fidelity research system) deliberately emits NO single score — a gate-first",
        "evidence vector. The harness needs feedback to hill-climb. Does feeding the agent the v2 vector (gates +",
        "independent drivers) produce better conversions than the v0.1 blended scalar it currently optimizes?",
        "",
        "Design: same model (opus), effort (medium), visual on, $2 cap, same samples. Two arms differ ONLY in the",
        "mid-loop feedback the agent sees:",
        "  ARM A  v0.1  ->  one blended overall = content^.35 * visual^.65  (compensatory: one axis hides another)",
        "  ARM B  v2    ->  HARD GATES (page-count, token P/R, number-F1) then drivers (ink_f1, ltsim, center)",
        "",
        "Grading is identical for both: the v2 evidence vector at 96 DPI (neither arm can game its own feedback).",
    ], size=13, lead=26)
    d.c.setFillColor(MUTED); d.c.setFont("Helvetica", 9)
    d.c.drawString(34, 40, f"{date.today().isoformat()} — metric_research/ — grading: pdf_metric_axes_v2 @96DPI — "
                           f"drivers/gates leave v2 untouched")
    d.done()

    # how to read
    d.page("How to read this — columns & method")
    d.lines(34, PAGE_H - 120, [
        "HARD GATES (non-compensatory; a human reviewer objects if any fails). PASS/FAIL, not blended:",
        "  G1 page-count delta = 0   G2 token recall >= .95   G3 token precision >= .95   G4 number-F1 = 1 (when numbers present)",
        "",
        "CONTINUOUS DRIVERS (hill-climb once gated; Phase A found these the most informative, mutually complementary):",
        "  ink_f1_reg  registered tolerant-ink overlap (raster)   ltsim_macro  text-block transport   center_q90  word displacement (lower=better)",
        "  driver_mean = mean(ink_f1, ltsim, 1-center_q90) — a convenience summary, NOT part of the v2 metric.",
        "",
        "REPORT-ONLY (diagnostic, not optimized): strict_f1 (drops on math the PDF tokenizes oddly — not real loss),",
        "  number_f1, ssim_reg (abstains unless canvas matches), page_break_f1 (noisy — use page-count delta instead).",
        "",
        "Baseline = 1-turn (no loop). Arm A / Arm B = agentic opus, medium, visual, harness — identical except feedback.",
    ], size=12, lead=25)
    d.done()

    # scoreboard (fills the slide: per-sample block of 3 arms, bold better of A vs B per column)
    d.page("Scoreboard (all arms scored by v2)",
           "bold = better of Arm A vs B per column, per sample; AVERAGE = mean over compiled runs")
    headers = ["sample", "arm", "gates", "ink_f1", "ltsim", "cq90", "drv", "numF1", "pagD", "cost", "turns"]
    widths = [150, 76, 50, 54, 52, 50, 50, 58, 46, 54, 46]
    rows = []
    bold = set()
    band = set()
    # accumulate per-arm sums for averages
    acc = {"baseline": [], "A v0.1": [], "B v2": []}
    ri = 0
    for e in data:
        block = {}
        for arm, sm, v in (("baseline", None, e["vbase"]), ("A v0.1", e["sa"], e["va"]),
                           ("B v2", e["sb"], e["vb"])):
            if v is None:
                rows.append((e["sid"] if arm == "baseline" else "", arm, "nc",
                             "—", "—", "—", "—", "—", "—", "—", "—"))
            else:
                cost = f"${sm['cost_usd']:.2f}" if sm and sm.get("cost_usd") else "—"
                turns = sm.get("num_turns", "—") if sm else "—"
                rows.append((e["sid"] if arm == "baseline" else "", arm,
                             f"{v['gates_passed']}/{v['gates_total']}",
                             fmt(v["ink_f1_reg"], 2), fmt(v["ltsim_macro"], 2), fmt(v["center_q90"], 2),
                             fmt(v["driver_mean"], 2), fmt(v.get("number_f1"), 3),
                             str(v["page_count_delta"]), cost, str(turns)))
                acc[arm].append(v)
                block[arm] = (ri, v)
            ri += 1
        # bold the better of A vs B per numeric column within this sample block
        if "A v0.1" in block and "B v2" in block:
            (ra, va), (rb, vb) = block["A v0.1"], block["B v2"]
            better = {  # col_index: (key, higher_is_better)
                2: ("gates_passed", True), 3: ("ink_f1_reg", True), 4: ("ltsim_macro", True),
                5: ("center_q90", False), 6: ("driver_mean", True), 7: ("number_f1", True)}
            for ci, (k, hib) in better.items():
                av, bv = va.get(k) or 0, vb.get(k) or 0
                if av == bv:
                    continue
                win = ra if (av > bv) == hib else rb
                bold.add((win, ci))
    # averages block
    def avg(vs, k):
        xs = [v.get(k) for v in vs if v.get(k) is not None]
        return sum(xs) / len(xs) if xs else None
    for arm in ("baseline", "A v0.1", "B v2"):
        vs = acc[arm]
        band.add(ri)
        if not vs:
            rows.append(("AVERAGE" if arm == "baseline" else "", arm, "—", "—", "—", "—", "—", "—", "—", "—", "—"))
        else:
            gp = avg(vs, "gates_passed")
            rows.append(("AVERAGE" if arm == "baseline" else "", arm,
                         f"{gp:.1f}/4", fmt(avg(vs, "ink_f1_reg"), 2), fmt(avg(vs, "ltsim_macro"), 2),
                         fmt(avg(vs, "center_q90"), 2), fmt(avg(vs, "driver_mean"), 2),
                         fmt(avg(vs, "number_f1"), 3), "", "", ""))
        ri += 1
    d.table(34, PAGE_H - 82, headers, rows, widths, size=10, rh=22, bold_cells=bold, band_rows=band)
    d.done()

    # case studies
    for e in data:
        va, vb = e["va"], e["vb"]
        sub = ""
        if va and vb:
            sub = f"gates A {va['gates_passed']}/{va['gates_total']} vs B {vb['gates_passed']}/{vb['gates_total']}"
        d.page(f"Case: {e['sid']} — {e['title']}", sub)
        # renders occupy from under the header down to the legend/callout band
        if e["cmp"] and e["cmp"].exists():
            d.image(e["cmp"], 34, PAGE_H - 70, PAGE_W - 68, PAGE_H - 208)
        # legend: which box color points at which metric
        lx = 34
        d.c.setFont("Helvetica-Oblique", 9); d.c.setFillColor(MUTED)
        d.c.drawString(lx, 120, "boxes drawn from v2 evidence coords:")
        lx += 205
        for rgb, txt in LEGEND:
            d.c.setFillColor(colors.Color(*[v / 255 for v in rgb]))
            d.c.rect(lx, 117, 12, 9, stroke=0, fill=1)
            d.c.setFillColor(TEXT); d.c.setFont("Helvetica", 9)
            d.c.drawString(lx + 16, 118, txt); lx += d.c.stringWidth(txt, "Helvetica", 9) + 40

        def strip(v, tag, xx, other):
            if not v:
                d.c.setFont("Helvetica-Bold", 12); d.c.setFillColor(RED)
                d.c.drawString(xx, 92, f"{tag}: no compile"); return
            win = v["gates_passed"] > (other["gates_passed"] if other else -1)
            gl = "  ".join(f"{n.split()[0]}={'P' if ok else 'F'}" for n, ok, _ in v["gates_detail"])
            d.c.setFont("Helvetica-Bold", 13); d.c.setFillColor(TEAL if win else NAVY)
            d.c.drawString(xx, 96, f"{tag}   gates {v['gates_passed']}/{v['gates_total']}")
            d.c.setFont("Helvetica", 9.5); d.c.setFillColor(TEXT)
            d.c.drawString(xx, 80, f"{gl}   ink={fmt(v['ink_f1_reg'],2)} ltsim={fmt(v['ltsim_macro'],2)} "
                                   f"cq90={fmt(v['center_q90'],2)} numF1={fmt(v.get('number_f1'),3)}")
            # plain-language: what the failing gate / worst driver points at
            msgs = []
            fails = [n.split()[0] for n, ok, _ in v["gates_detail"] if not ok]
            if "G1" in fails:
                msgs.append(f"page count off ({v['page_count_delta']:+d}) -> wrong pagination")
            if "G4" in fails and (v["num_missing"] or v["num_extra"]):
                bits = []
                if v["num_missing"]:
                    bits.append("missing " + ",".join(v["num_missing"]))
                if v["num_extra"]:
                    bits.append("extra " + ",".join(v["num_extra"]))
                msgs.append("numbers wrong: " + "; ".join(bits))
            if ("G2" in fails or "G3" in fails):
                msgs.append("text not fully preserved (token recall/precision < .95)")
            if not fails:
                msgs.append("all gates pass; residual is visual polish (amber/red boxes)")
            d.c.setFillColor(RED if fails else TEAL); d.c.setFont("Helvetica-Oblique", 9)
            yy = 64
            for m in msgs[:3]:
                d.c.drawString(xx, yy, "\u2192 " + m); yy -= 12
        strip(e["va"], "ARM A v0.1", 34, e["vb"])
        strip(e["vb"], "ARM B v2", PAGE_W / 2 + 20, e["va"])
        d.done()

    # takeaways
    d.page("Takeaways", "avg gates passed: baseline 1.2/4  ->  Arm A (v0.1) 2.0/4  ->  Arm B (v2) 3.2/4")
    d.lines(34, PAGE_H - 130, [
        "1. Non-compensatory feedback helps, consistently: across 6 hard samples Arm B (v2) matched or beat Arm A on the",
        "   HARD GATES a human objects to, winning outright in 5/6 (avg 3.2/4 vs 2.0/4). It closed exact-number-F1 to",
        "   1.000 in 5/6, where Arm A stalled at 0.989-0.998 — the gate ladder names the miss, so the agent fixes it.",
        "2. Arm A (v0.1 scalar) tends to buy visual polish (edges Arm B on the drivers in 4/6, by ~0.02-0.08) while letting a",
        "   single wrong number or off-by-one page slip inside the weighted average — the compensatory failure v2 warned of.",
        "3. Content vs visual are near-independent axes (Phase A: r(strict_f1, overall)=+0.20); one blended number cannot",
        "   represent both, which is exactly why the v2 vector is more actionable feedback.",
        "4. Strict token gates are HARDER, not impossible, on math/algorithm PDFs: on 09_algorithms_003, gate-first feedback",
        "   pushed Arm B from 1/4 to 4/4 (token recall/precision cleared .95) where Arm A stayed at 1/4. Kept strict per request.",
        "5. The verbose full paper (arxiv5t_paper_019) is the shared ceiling (both 1/4) — real multi-page content divergence",
        "   neither feedback resolves at $2 / medium effort.",
        "",
        "Caveat: n=6, one seed per cell (06_tables repeated across 2 seeds agreed: A 3/4, B 4/4). Mechanism evidence, not a",
        "leaderboard; no human ratings exist. All arms graded by pdf_metric_axes_v2 @96 DPI; v2/gates/driver-reward untouched.",
    ], size=12, lead=24)
    d.done()

    d.save()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
