import csv
from pathlib import Path
import fitz  # PyMuPDF
from skimage.metrics import structural_similarity as ssim
import numpy as np
from PIL import Image

def get_page_pixmap(pdf_path, dpi=72):
    try:
        doc = fitz.open(pdf_path)
        if len(doc) == 0:
            return None
        page = doc[0]
        pix = page.get_pixmap(dpi=dpi)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return np.array(img.convert("L"))
    except Exception:
        return None

def compute_ssim(img1, img2):
    if img1.shape != img2.shape:
        img2_pil = Image.fromarray(img2).resize((img1.shape[1], img1.shape[0]))
        img2 = np.array(img2_pil)
    
    score, _ = ssim(img1, img2, full=True, data_range=255)
    return score

def compute_bbox_iou(pdf_path1, pdf_path2):
    try:
        doc1 = fitz.open(pdf_path1)
        doc2 = fitz.open(pdf_path2)
        if len(doc1) == 0 or len(doc2) == 0:
            return 0.0
            
        def filter_page_numbers(blocks, page_height):
            filtered = []
            for b in blocks:
                if b[6] != 0: continue
                if b[1] > page_height * 0.80 and b[4].strip().isdigit():
                    continue
                filtered.append(b)
            return filtered
            
        b1 = filter_page_numbers(doc1[0].get_text("blocks"), doc1[0].rect.height)
        b2 = filter_page_numbers(doc2[0].get_text("blocks"), doc2[0].rect.height)
        
        if not b1 or not b2:
            return 0.0
            
        def get_union_rect(blocks):
            rects = [fitz.Rect(b[:4]) for b in blocks if b[6] == 0]
            if not rects:
                return fitz.Rect()
            r = rects[0]
            for rect in rects[1:]:
                r |= rect
            return r
            
        r1 = get_union_rect(b1)
        r2 = get_union_rect(b2)
        
        if r1.is_empty or r2.is_empty:
            return 0.0
            
        intersect = r1 & r2
        if intersect.is_empty:
            return 0.0
            
        def get_area(r):
            return r.width * r.height
            
        iou = get_area(intersect) / (get_area(r1) + get_area(r2) - get_area(intersect))
        return max(0.0, min(1.0, iou))
    except Exception:
        return 0.0

def main():
    results = []
    
    with open("results/compile_metrics.csv", "r") as f:
        compile_metrics = list(csv.DictReader(f))
        
    engine_names = ["pandoc", "tylax", "typetex_approx"]
        
    for row in compile_metrics:
        cat = row["category"]
        fname = row["filename"]
        base = Path(fname).stem
        
        ref_pdf = Path(f"data/reference_pdfs/{cat}/{base}.pdf")
        if not ref_pdf.exists():
            continue
            
        ref_img = get_page_pixmap(ref_pdf)
        if ref_img is None:
            continue
            
        metrics = {
            "category": cat,
            "filename": fname,
            "difficulty": row["difficulty"]
        }
        
        ssim_scores = {}
        
        for eng in engine_names:
            metrics[f"{eng}_compile"] = row[eng]
            metrics[f"{eng}_iou"] = "0.00"
            metrics[f"{eng}_ssim"] = "0.00"
            metrics[f"{eng}_score"] = "0.0"
            
            if row[eng] == "1":
                eng_pdf = Path(f"results/{cat}/{base}/{eng}.pdf")
                if eng_pdf.exists():
                    iou = compute_bbox_iou(ref_pdf, eng_pdf)
                    eng_img = get_page_pixmap(eng_pdf)
                    if eng_img is not None:
                        s_score = compute_ssim(ref_img, eng_img)
                    else:
                        s_score = 0.0
                        
                    metrics[f"{eng}_iou"] = f"{iou:.2f}"
                    metrics[f"{eng}_ssim"] = f"{s_score:.2f}"
                    ssim_scores[eng] = s_score
                    metrics[f"{eng}_score"] = "0.5" # Compilation successful
            elif row[eng] == "-1":
                metrics[f"{eng}_compile"] = "-1"
                metrics[f"{eng}_score"] = "-"
        
        # Give +0.5 to the best engine(s)
        if ssim_scores:
            best_ssim = max(ssim_scores.values())
            for eng, score in ssim_scores.items():
                if score == best_ssim:
                    metrics[f"{eng}_score"] = "1.0"
                    
        results.append(metrics)
        
    fieldnames = ["category", "filename", "difficulty"]
    for eng in engine_names:
        fieldnames.extend([f"{eng}_compile", f"{eng}_iou", f"{eng}_ssim", f"{eng}_score"])
        
    with open("results/visual_metrics.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    print("Metrics computation complete. Saved to results/visual_metrics.csv.")

if __name__ == "__main__":
    main()
