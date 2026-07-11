import cv2
import numpy as np
import fitz
from pathlib import Path
import json

def draw_bboxes_on_pdf(pdf_path, is_ref, color):
    if not Path(pdf_path).exists():
        return np.full((1000, 1000, 3), 255, dtype=np.uint8)
    try:
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            return np.full((1000, 1000, 3), 255, dtype=np.uint8)
        page = doc[0]
        blocks = [b for b in page.get_text("dict")["blocks"] if b["type"] == 0]
        
        pix = page.get_pixmap(dpi=150)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        if pix.n == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        elif pix.n == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
        scale_x = pix.w / page.rect.width
        scale_y = pix.h / page.rect.height
        
        for b in blocks:
            x0, y0, x1, y1 = b["bbox"]
            cv2.rectangle(img, (int(x0*scale_x), int(y0*scale_y)), (int(x1*scale_x), int(y1*scale_y)), color, 2)
            
        # Crop empty space
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        coords = cv2.findNonZero(thresh)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)
            padding = 20
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(img.shape[1] - x, w + 2*padding)
            h = min(img.shape[0] - y, h + 2*padding)
            img = img[y:y+h, x:x+w]
            
        # Pad to 1000x1000
        target_h, target_w = 1000, 1000
        h, w = img.shape[:2]
        scale = min(target_w/w, target_h/h)
        if scale < 1:
            new_w, new_h = int(w*scale), int(h*scale)
            img = cv2.resize(img, (new_w, new_h))
        else:
            new_w, new_h = w, h
            
        padded = np.full((target_h, target_w, 3), 255, dtype=np.uint8)
        start_y = (target_h - new_h) // 2
        start_x = (target_w - new_w) // 2
        padded[start_y:start_y+new_h, start_x:start_x+new_w] = img
        return padded
    except Exception as e:
        print(f"Error on {pdf_path}: {e}")
        return np.full((1000, 1000, 3), 255, dtype=np.uint8)

def add_label(img, name, score=None):
    h, w = img.shape[:2]
    # Add border
    cv2.rectangle(img, (0, 0), (w-1, h-1), (200, 200, 200), 4)
    
    # Name Bottom Left
    name_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
    name_x = 20
    name_y = h - 20
    cv2.rectangle(img, (name_x - 10, name_y - 35), (name_x + name_size[0] + 10, name_y + 10), (200, 200, 200), -1)
    cv2.putText(img, name, (name_x, name_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
    
    # Score Bottom Right
    if score:
        score_size = cv2.getTextSize(score, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
        score_x = w - score_size[0] - 20
        score_y = h - 20
        cv2.rectangle(img, (score_x - 10, score_y - 35), (score_x + score_size[0] + 10, score_y + 10), (200, 200, 200), -1)
        cv2.putText(img, score, (score_x, score_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        
    return img

def create_grid(sample_id, ref_pdf, pandoc_pdf, tylax_pdf, typetex_pdf, out_path, scores_dict):
    color_ref = (0, 255, 0)
    color_cand = (0, 0, 255)
    
    img_ref = add_label(draw_bboxes_on_pdf(ref_pdf, True, color_ref), "Reference")
    
    def get_score_str(cand):
        s = scores_dict.get(sample_id, {}).get(cand, {})
        # Based on user's statement "Match Rate: 0.00 | Pos Score: 0.000"
        match = s.get("content_match_rate", 0.0)
        pos = s.get("alignment_score", 0.0)
        if match is None: match = 0.0
        if pos is None: pos = 0.0
        return f"Match: {match:.2f}, Pos: {pos:.3f}"
        
    img_pandoc = add_label(draw_bboxes_on_pdf(pandoc_pdf, False, color_cand), "Pandoc", get_score_str("pandoc"))
    img_tylax = add_label(draw_bboxes_on_pdf(tylax_pdf, False, color_cand), "Tylax", get_score_str("tylax"))
    img_typetex = add_label(draw_bboxes_on_pdf(typetex_pdf, False, color_cand), "Typetex", get_score_str("typetex_approx"))
    
    top = np.hstack([img_ref, img_pandoc])
    bottom = np.hstack([img_tylax, img_typetex])
    grid = np.vstack([top, bottom])
    
    cv2.imwrite(out_path, grid)
    print(f"Saved {out_path}")

with open("ai_models/absolute_scores.json", "r") as f:
    records = json.load(f)
    
scores = {}
for r in records:
    sample_id = r["sample_id"]
    cand = r["candidate"]
    if sample_id not in scores:
        scores[sample_id] = {}
    scores[sample_id][cand] = r

out_dir = "/Users/yashashwisinghania/.gemini/antigravity-ide/brain/3d0f5497-5f8e-4a1f-a022-7a5114d70450/scratch/appendix_grids"

create_grid(
    "tables_simple_easy",
    "data/reference_pdfs/06_tables_simple/easy.pdf",
    "results/06_tables_simple/easy/pandoc.pdf",
    "results/06_tables_simple/easy/tylax.pdf",
    "results/06_tables_simple/easy/typetex_approx.pdf",
    f"{out_dir}/tables_simple_easy.png",
    scores
)

create_grid(
    "tables_complex_attention_table1",
    "data/reference_pdfs/07_tables_complex/attention_table1.pdf",
    "results/07_tables_complex/attention_table1/pandoc.pdf",
    "results/07_tables_complex/attention_table1/tylax.pdf",
    "results/07_tables_complex/attention_table1/typetex_approx.pdf",
    f"{out_dir}/tables_complex_attention_table1.png",
    scores
)
