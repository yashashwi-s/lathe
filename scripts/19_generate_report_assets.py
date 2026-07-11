"""Generate all report imagery from ai_models/absolute_scores.json and on-disk PDFs.

Outputs (run from the repo root):
  assets/appendix_grids/<sample_id>.png   2x2 grid: Reference / Pandoc / Tylax / TypeTeX
  assets/fair_grids/<sample_id>.png       3x2 grid: Reference / Gemini / GPT / Pandoc / Tylax / TypeTeX
  assets/examples/<name>.png              1x2 Reference-vs-candidate pairs used in the
                                          visual alignment report

Every panel label (Match / Pos) is read from absolute_scores.json at generation time,
so the images can never disagree with the scores table. Candidates whose record has
compiles == 0 get a red FAILED panel regardless of what files exist on disk.
"""
import json
from pathlib import Path

import cv2
import fitz
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SCORES = ROOT / "ai_models" / "absolute_scores.json"
GRAPHICS = ("tikz", "pgfplots", "posters")

FAIR_SAMPLES = [
    "prose_easy", "prose_hard", "eq_simple_hard", "eq_hard_hard",
    "tables_complex_easy", "tables_complex_hard", "algorithms_easy", "algorithms_medium",
]

# Reference-vs-candidate pairs shown in visual_alignment_report.md
EXAMPLE_PAIRS = [
    ("curated_1_prose_easy_gpt", "prose_easy", "gpt"),
    ("curated_2_tables_complex_hard_tylax", "tables_complex_hard", "tylax"),
    ("curated_3_cv_complex_hard_tylax_patched", "cv_complex_hard", "tylax_patched"),
    ("curated_4_eq_simple_hard_pandoc", "eq_simple_hard", "pandoc"),
    ("positive_1_prose_easy_pandoc", "prose_easy", "pandoc"),
    ("positive_2_eq_simple_easy_pandoc", "eq_simple_easy", "pandoc"),
    ("negative_1_paper_full_easy_typetex", "paper_full_easy", "typetex"),
    ("negative_2_tables_complex_attention_table2_typetex", "tables_complex_attention_table2", "typetex"),
]

PANEL = 1000  # px, square panels


def category_map():
    """sample prefix (e.g. 'cv_complex') -> numbered dir name (e.g. '13_cv_complex')"""
    out = {}
    for d in (ROOT / "results").iterdir():
        if d.is_dir() and d.name[0].isdigit():
            out[d.name.split("_", 1)[1]] = d.name
    return out


CATS = category_map()


def split_sample(sample_id):
    """'cv_complex_hard' -> ('13_cv_complex', 'hard')"""
    for prefix in sorted(CATS, key=len, reverse=True):
        if sample_id.startswith(prefix + "_"):
            return CATS[prefix], sample_id[len(prefix) + 1:]
    raise ValueError(f"cannot resolve category for {sample_id}")


def ref_pdf(sample_id):
    cat, diff = split_sample(sample_id)
    return ROOT / "data" / "reference_pdfs" / cat / f"{diff}.pdf"


def cand_pdf(sample_id, candidate):
    if candidate in ("gemini", "gpt", "claude"):
        return ROOT / "ai_models" / sample_id / candidate / "output.pdf"
    name = candidate
    if name == "typetex":
        name = "typetex_approx"
    elif name == "typetex_patched":
        name = "typetex_approx_patched"
    cat, diff = split_sample(sample_id)
    return ROOT / "results" / cat / diff / f"{name}.pdf"


def render_panel(pdf_path, box_color):
    """Render page 1 with text-block bounding boxes, cropped and padded to PANELxPANEL."""
    img = None
    if pdf_path and Path(pdf_path).exists():
        try:
            doc = fitz.open(pdf_path)
            if len(doc):
                page = doc[0]
                pix = page.get_pixmap(dpi=150)
                img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
                if pix.n == 1:
                    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                elif pix.n == 4:
                    img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
                else:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                sx, sy = pix.w / page.rect.width, pix.h / page.rect.height
                for b in page.get_text("dict")["blocks"]:
                    if b["type"] != 0:
                        continue
                    x0, y0, x1, y1 = b["bbox"]
                    cv2.rectangle(img, (int(x0 * sx), int(y0 * sy)),
                                  (int(x1 * sx), int(y1 * sy)), box_color, 2)
        except Exception as e:
            print(f"  render error {pdf_path}: {e}")
            img = None
    if img is None:
        return np.full((PANEL, PANEL, 3), 255, dtype=np.uint8)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    coords = cv2.findNonZero(thresh)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        pad = 20
        x, y = max(0, x - pad), max(0, y - pad)
        w = min(img.shape[1] - x, w + 2 * pad)
        h = min(img.shape[0] - y, h + 2 * pad)
        img = img[y:y + h, x:x + w]

    h, w = img.shape[:2]
    scale = min(PANEL / w, PANEL / h)
    if scale < 1:
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    h, w = img.shape[:2]
    canvas = np.full((PANEL, PANEL, 3), 255, dtype=np.uint8)
    y0, x0 = (PANEL - h) // 2, (PANEL - w) // 2
    canvas[y0:y0 + h, x0:x0 + w] = img
    return canvas


def failed_panel():
    img = np.full((PANEL, PANEL, 3), 255, dtype=np.uint8)
    cv2.rectangle(img, (0, 0), (PANEL - 1, PANEL - 1), (0, 0, 180), 12)
    text = "FAILED TO COMPILE"
    size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.6, 3)[0]
    cv2.putText(img, text, ((PANEL - size[0]) // 2, PANEL // 2),
                cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 180), 3)
    return img


def add_label(img, name, score_text=None):
    h, w = img.shape[:2]
    cv2.rectangle(img, (0, 0), (w - 1, h - 1), (120, 120, 120), 4)
    label = name if score_text is None else f"{name} | {score_text}"
    size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
    x, y = 20, h - 20
    cv2.rectangle(img, (x - 10, y - 35), (x + size[0] + 10, y + 10), (210, 210, 210), -1)
    cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    return img


def score_text(rec):
    if rec is None:
        return "no record"
    if rec.get("compiles", 0) == 0:
        return "Failed"
    m = rec.get("content_match_rate")
    p = rec.get("alignment_score")
    m = 0.0 if m is None else m
    p = 0.0 if p is None else p
    return f"Match: {m:.2f} | Pos: {p:.3f}"


def candidate_panel(sample_id, candidate, rec, color=(0, 0, 255)):
    if rec is not None and rec.get("compiles", 0) == 0:
        return add_label(failed_panel(), pretty(candidate), "Failed")
    return add_label(render_panel(cand_pdf(sample_id, candidate), color),
                     pretty(candidate), score_text(rec))


def pretty(candidate):
    return {"gpt": "GPT", "gemini": "Gemini", "pandoc": "Pandoc", "tylax": "Tylax",
            "typetex": "TypeTeX", "tylax_patched": "Tylax (patched)",
            "pandoc_patched": "Pandoc (patched)",
            "typetex_patched": "TypeTeX (patched)"}.get(candidate, candidate)


def main():
    scores = {}
    for r in json.load(open(SCORES)):
        scores.setdefault(r["sample_id"], {})[r["candidate"]] = r

    grids_dir = ROOT / "assets" / "appendix_grids"
    fair_dir = ROOT / "assets" / "fair_grids"
    ex_dir = ROOT / "assets" / "examples"
    for d in (grids_dir, fair_dir, ex_dir):
        d.mkdir(parents=True, exist_ok=True)

    samples = sorted(scores)

    # 2x2 appendix grids (base engines)
    for sid in samples:
        ref = add_label(render_panel(ref_pdf(sid), (0, 180, 0)), "Reference")
        panels = [candidate_panel(sid, c, scores[sid].get(c)) for c in ("pandoc", "tylax", "typetex")]
        grid = np.vstack([np.hstack([ref, panels[0]]), np.hstack([panels[1], panels[2]])])
        cv2.imwrite(str(grids_dir / f"{sid}.png"), grid)
        print(f"appendix grid: {sid}")

    # 3x2 fair-subset grids (AI models + engines)
    for sid in FAIR_SAMPLES:
        ref = add_label(render_panel(ref_pdf(sid), (0, 180, 0)), "Reference")
        cands = ["gemini", "gpt", "pandoc", "tylax", "typetex"]
        panels = [candidate_panel(sid, c, scores[sid].get(c)) for c in cands]
        top = np.hstack([ref, panels[0], panels[1]])
        bottom = np.hstack(panels[2:])
        cv2.imwrite(str(fair_dir / f"{sid}.png"), np.vstack([top, bottom]))
        print(f"fair grid: {sid}")

    # 1x2 example pairs
    for name, sid, cand in EXAMPLE_PAIRS:
        ref = add_label(render_panel(ref_pdf(sid), (0, 180, 0)), "Reference")
        panel = candidate_panel(sid, cand, scores[sid].get(cand))
        cv2.imwrite(str(ex_dir / f"{name}.png"), np.hstack([ref, panel]))
        print(f"example: {name}")


if __name__ == "__main__":
    main()
