import fitz
import skimage.metrics
import numpy as np
import json
import logging
import os
import unicodedata
import re
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def setup_logging():
    """File+console logging for pipeline runs. Called from main() only, so that
    importing this module (e.g. to reuse evaluate_iou/evaluate_ssim) has no
    side effects."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f"visual_alignment_{timestamp}.log"),
            logging.StreamHandler()
        ]
    )

GRAPHICS_CATEGORIES = ["tikz", "pgfplots", "posters"]

def get_iou(bb1, bb2):
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    x_right = min(bb1[2], bb2[2])
    y_bottom = min(bb1[3], bb2[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    bb1_area = (bb1[2] - bb1[0]) * (bb1[3] - bb1[1])
    bb2_area = (bb2[2] - bb2[0]) * (bb2[3] - bb2[1])
    
    if bb1_area + bb2_area - intersection_area == 0:
        return 0.0
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou

def jaccard_similarity(text1, text2):
    """Calculate word-level Jaccard similarity between two text blocks"""
    t1_norm = unicodedata.normalize('NFKD', text1).lower()
    t2_norm = unicodedata.normalize('NFKD', text2).lower()
    t1 = re.findall(r'[a-z0-9]+', t1_norm)
    t2 = re.findall(r'[a-z0-9]+', t2_norm)
    set1 = set(t1)
    set2 = set(t2)
    if not set1 or not set2:
        return 0.0
    return len(set1.intersection(set2)) / len(set1.union(set2))

def evaluate_ssim(ref_pdf, cand_pdf):
    ref_doc = fitz.open(ref_pdf)
    cand_doc = fitz.open(cand_pdf)
    
    min_pages = min(len(ref_doc), len(cand_doc))
    
    ssims = []
    
    for page_idx in range(min_pages):
        ref_pix = ref_doc[page_idx].get_pixmap(dpi=150, colorspace=fitz.csGRAY)
        cand_pix = cand_doc[page_idx].get_pixmap(dpi=150, colorspace=fitz.csGRAY)
        
        ref_img = np.frombuffer(ref_pix.samples, dtype=np.uint8).reshape(ref_pix.h, ref_pix.w)
        cand_img = np.frombuffer(cand_pix.samples, dtype=np.uint8).reshape(cand_pix.h, cand_pix.w)
        
        target_h = max(ref_img.shape[0], cand_img.shape[0])
        target_w = max(ref_img.shape[1], cand_img.shape[1])
        
        ref_padded = np.full((target_h, target_w), 255, dtype=np.uint8)
        ref_padded[:ref_img.shape[0], :ref_img.shape[1]] = ref_img
        
        cand_padded = np.full((target_h, target_w), 255, dtype=np.uint8)
        cand_padded[:cand_img.shape[0], :cand_img.shape[1]] = cand_img
        
        # Calculate SSIM with full=True to get the diff image
        score, diff_img = skimage.metrics.structural_similarity(ref_padded, cand_padded, data_range=255, full=True)
        
        # Check if candidate page is completely blank
        if not np.any(cand_padded < 250):
            masked_score = 0.0
        else:
            # Mask out pixels that are white in BOTH images
            mask = (ref_padded < 250) | (cand_padded < 250)
            if np.any(mask):
                masked_score = max(0.0, diff_img[mask].mean())
            else:
                masked_score = 1.0
                
        ssims.append(masked_score)
        
    return {
        "alignment_score": sum(ssims) / len(ssims) if ssims else 0.0,
        "content_match_rate": 1.0,  # Full image matching implies 100% of structure exists
        "page_count_mismatch": len(ref_doc) != len(cand_doc),
        "reference_pages": len(ref_doc),
        "candidate_pages": len(cand_doc),
        "unmatched_reference_blocks": 0,
        "unmatched_candidate_blocks": 0,
        "matching_strategy": "ssim"
    }

def evaluate_iou(ref_pdf, cand_pdf):
    ref_doc = fitz.open(ref_pdf)
    cand_doc = fitz.open(cand_pdf)
    
    min_pages = min(len(ref_doc), len(cand_doc))
    
    all_ious = []
    unmatched_ref = 0
    unmatched_cand = 0
    total_ref_blocks = 0
    matched_ref_blocks = 0
    strategy_used = "reading_order"
    
    threshold = 0.3
    
    for page_idx in range(min_pages):
        ref_page = ref_doc[page_idx]
        cand_page = cand_doc[page_idx]
        
        ref_w, ref_h = ref_page.rect.width, ref_page.rect.height
        cand_w, cand_h = cand_page.rect.width, cand_page.rect.height
        
        def filter_page_numbers(blocks, page_height):
            filtered = []
            for b in blocks:
                if b["type"] != 0: continue
                # Check if bottom 20% and only digits
                if b["bbox"][1] > page_height * 0.80:
                    text = ""
                    for l in b.get("lines", []):
                        for s in l.get("spans", []):
                            text += s.get("text", "").strip()
                    if text.isdigit():
                        continue
                filtered.append(b)
            return filtered

        ref_blocks = filter_page_numbers(ref_page.get_text("dict")["blocks"], ref_page.rect.height)
        cand_blocks = filter_page_numbers(cand_page.get_text("dict")["blocks"], cand_page.rect.height)
        
        total_ref_blocks += len(ref_blocks)
        
        if not ref_blocks and not cand_blocks:
            # both empty, perfect match
            all_ious.append(1.0)
            continue
        elif not ref_blocks or not cand_blocks:
            # one empty, one not
            unmatched_ref += len(ref_blocks)
            unmatched_cand += len(cand_blocks)
            continue
            
        ref_off_x = min(b["bbox"][0] for b in ref_blocks)
        ref_off_y = min(b["bbox"][1] for b in ref_blocks)
        cand_off_x = min(b["bbox"][0] for b in cand_blocks)
        cand_off_y = min(b["bbox"][1] for b in cand_blocks)
        
        def normalize(b, w, h, off_x, off_y):
            x0, y0, x1, y1 = b["bbox"]
            return ((x0 - off_x)/w, (y0 - off_y)/h, (x1 - off_x)/w, (y1 - off_y)/h)
            
        def get_text(b):
            text = ""
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    text += span.get("text", "") + " "
            return text.strip()
            
        ref_data = [{"bbox": normalize(b, ref_w, ref_h, ref_off_x, ref_off_y), "text": get_text(b)} for b in ref_blocks]
        cand_data = [{"bbox": normalize(b, cand_w, cand_h, cand_off_x, cand_off_y), "text": get_text(b)} for b in cand_blocks]
        
        if abs(len(ref_data) - len(cand_data)) > 3 or (len(ref_data) > 0 and abs(len(ref_data) - len(cand_data)) / len(ref_data) > 0.2):
            strategy_used = "text_content_fallback"
            matched_cands = set()
            for rb in ref_data:
                best_cand = -1
                best_sim = -1
                for i, cb in enumerate(cand_data):
                    if i in matched_cands:
                        continue
                    sim = jaccard_similarity(rb["text"], cb["text"])
                    if sim > best_sim:
                        best_sim = sim
                        best_cand = i
                
                if best_sim >= threshold:
                    matched_cands.add(best_cand)
                    all_ious.append(get_iou(rb["bbox"], cand_data[best_cand]["bbox"]))
                    matched_ref_blocks += 1
                else:
                    unmatched_ref += 1
            
            unmatched_cand += len(cand_data) - len(matched_cands)
        else:
            ref_data.sort(key=lambda x: (x["bbox"][1], x["bbox"][0]))
            cand_data.sort(key=lambda x: (x["bbox"][1], x["bbox"][0]))
            
            min_blocks = min(len(ref_data), len(cand_data))
            for i in range(min_blocks):
                sim = jaccard_similarity(ref_data[i]["text"], cand_data[i]["text"])
                if sim >= threshold:
                    all_ious.append(get_iou(ref_data[i]["bbox"], cand_data[i]["bbox"]))
                    matched_ref_blocks += 1
                else:
                    unmatched_ref += 1
                    unmatched_cand += 1
            
            unmatched_ref += len(ref_data) - min_blocks
            unmatched_cand += len(cand_data) - min_blocks
            
    content_match_rate = matched_ref_blocks / total_ref_blocks if total_ref_blocks > 0 else 1.0
    if len(all_ious) == 0 and total_ref_blocks > 0:
        position_score = None
    else:
        position_score = sum(all_ious) / len(all_ious) if all_ious else 1.0
        
    return {
        "alignment_score": position_score,
        "content_match_rate": content_match_rate,
        "page_count_mismatch": len(ref_doc) != len(cand_doc),
        "reference_pages": len(ref_doc),
        "candidate_pages": len(cand_doc),
        "unmatched_reference_blocks": unmatched_ref,
        "unmatched_candidate_blocks": unmatched_cand,
        "matching_strategy": strategy_used
    }

def map_score_to_deviation(score, is_graphics, content_match_rate=1.0):
    if content_match_rate == 0.0:
        return "content_mismatch"
    if score is None:
        return "extraction_failed"
    
    if is_graphics:
        if score >= 0.95:
            return "exact"
        elif score >= 0.75:
            return "minor"
        else:
            return "major"
    else:
        # Recalibrated text IoU thresholds
        if score >= 0.70:
            return "exact"
        elif score >= 0.40:
            return "minor"
        else:
            return "major"

def get_ref_path(sample_id):
    # Sample ID format: {category_name}_{difficulty}, e.g. algorithms_easy -> 08_algorithms/easy.pdf
    # But wait, sample_id might not have the numeric prefix.
    # We can search through data/reference_pdfs
    ref_dir = Path("data/reference_pdfs")
    for subdir in ref_dir.iterdir():
        if subdir.is_dir() and sample_id.startswith(subdir.name.split('_', 1)[1]):
            # found category
            difficulty = sample_id[len(subdir.name.split('_', 1)[1])+1:]
            return subdir / f"{difficulty}.pdf"
    return None

def get_cand_path(sample_id, candidate):
    if candidate in ["gemini", "gpt", "claude"]:
        return Path("ai_models") / sample_id / candidate / "output.pdf"
    else:
        results_dir = Path("results")
        file_cand = candidate
        if file_cand == "typetex":
            file_cand = "typetex_approx"
        elif file_cand == "typetex_patched":
            file_cand = "typetex_approx_patched"
        
        for subdir in results_dir.iterdir():
            if subdir.is_dir() and sample_id.startswith(subdir.name.split('_', 1)[1]):
                difficulty = sample_id[len(subdir.name.split('_', 1)[1])+1:]
                cand_pdf = subdir / difficulty / f"{file_cand}.pdf"
                if cand_pdf.exists():
                    return cand_pdf
                # In heuristic evaluator, it uses the same logic. Let's see if it's there.
                return cand_pdf
    return None

def main():
    setup_logging()
    logger.info("Starting Visual Alignment Scoring")
    
    with open("ai_models/absolute_scores.json", "r") as f:
        records = json.load(f)
        
    outcomes = {"exact": 0, "minor": 0, "major": 0, "extraction_failed": 0, "not_applicable": 0}
    
    for r in records:
        sample_id = r["sample_id"]
        candidate = r["candidate"]
        
        if r.get("pipeline_status", "ran") != "ran" or r["compiles"] == 0:
            r["alignment_score"] = None
            r["content_match_rate"] = None
            r["alignment_deviation"] = "not_applicable"
            r["unmatched_reference_blocks"] = 0
            r["unmatched_candidate_blocks"] = 0
            r["page_count_mismatch"] = False
            r["reference_pages"] = 0
            r["candidate_pages"] = 0
            r["matching_strategy"] = "none"
            outcomes["not_applicable"] += 1
            continue
            
        is_graphics = any(g in sample_id for g in GRAPHICS_CATEGORIES)
        
        ref_pdf = get_ref_path(sample_id)
        cand_pdf = get_cand_path(sample_id, candidate)
        
        if not ref_pdf or not ref_pdf.exists():
            logger.error(f"[{sample_id} - {candidate}] Missing reference PDF at {ref_pdf}")
            r["alignment_score"] = None
            r["alignment_deviation"] = "extraction_failed"
            outcomes["extraction_failed"] += 1
            continue
            
        if not cand_pdf or not cand_pdf.exists():
            logger.error(f"[{sample_id} - {candidate}] Missing candidate PDF at {cand_pdf}")
            r["alignment_score"] = None
            r["alignment_deviation"] = "extraction_failed"
            outcomes["extraction_failed"] += 1
            continue
            
        try:
            if is_graphics:
                res = evaluate_ssim(ref_pdf, cand_pdf)
            else:
                res = evaluate_iou(ref_pdf, cand_pdf)
                
            score = res["alignment_score"]
            content_match_rate = res["content_match_rate"]
            tier = map_score_to_deviation(score, is_graphics, content_match_rate)
            
            r.update(res)
            r["alignment_deviation"] = tier
            outcomes.setdefault(tier, 0)
            outcomes[tier] += 1
            
            logger.info(f"[{sample_id} - {candidate}] Strategy: {res['matching_strategy']} | Match Rate: {content_match_rate:.3f} | Score: {score if score is not None else 0.0:.3f} -> {tier}")
            
        except Exception as e:
            logger.exception(f"[{sample_id} - {candidate}] Extraction failed: {e}")
            r["alignment_score"] = None
            r["alignment_deviation"] = "extraction_failed"
            outcomes["extraction_failed"] += 1
            
    with open("ai_models/absolute_scores.json", "w") as f:
        json.dump(records, f, indent=2)
        
    logger.info("Visual Alignment Scoring Complete")
    logger.info(f"Total Outcomes: {outcomes}")

if __name__ == "__main__":
    main()
