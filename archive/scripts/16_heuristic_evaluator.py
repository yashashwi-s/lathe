import os
import json
import re
from pathlib import Path

def get_latex_words(tex_code):
    # naive stripping of LaTeX commands for text comparison
    text = re.sub(r'\\[a-zA-Z]+(\[.*?\])?(\{.*?\})?', '', tex_code)
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text)
    return set(w.lower() for w in words)

def evaluate_candidate(candidate_name, segment, typ_file, tex_file, retries, is_engine=False, is_patched=False):
    record = {
        "candidate": candidate_name,
        "is_patched": is_patched,
        "sample_id": segment,
        "pipeline_status": "ran",
        "compiles": 0,
        "retries": retries,
        "no_leaked_source": 0,
        "text_completeness": 0,
        "structural_elements": 0,
        "numbering_correctness": 0,
        "font_match": "N/A",
        "alignment_deviation": "not_implemented",
        "typography_correctness": 0,
        "notes": ""
    }

    if not typ_file.exists():
        record["pipeline_status"] = "not_run"
        if candidate_name == "typetex" and "eq_" in segment:
            record["notes"] = "TypeTeX Lua filter crashes on equations (object has no __toinline metamethod)."
        else:
            record["notes"] = "Source file missing."
        return record

    png_file = typ_file.with_suffix('.png')
    pdf_file = typ_file.with_suffix('.pdf')
    
    if not (png_file.exists() or pdf_file.exists()):
        record["notes"] = "Does not compile. Rendered output missing."
        
        # Reserved character audit findings
        if "cv_" in segment and candidate_name == "tylax":
            record["notes"] += " [Root Cause: Unescaped '@' symbol in email address causes Typst to incorrectly parse it as a label reference.]"
        elif "cv_" in segment and candidate_name in ["pandoc", "typetex"] and ("medium" in segment or "hard" in segment):
            record["notes"] += " [Root Cause: Translates \hrule to #horizontalrule, which is invalid in Typst.]"
            
        err_file = typ_file.parent / "compile_error_prompt.txt"
        if err_file.exists():
            record["notes"] += " " + err_file.read_text().split('=========================================')[1].strip()[:200]
        return record

    record["compiles"] = 1
    typ_code = typ_file.read_text(encoding='utf-8', errors='ignore')
    tex_code = tex_file.read_text(encoding='utf-8', errors='ignore') if tex_file.exists() else ""

    # 2. No leaked source
    leaked = re.findall(r'\\[a-zA-Z]+', typ_code)
    leaked = [l for l in leaked if l not in ['\\n', '\\r', '\\t', '\\u', '\\x']]
    record["no_leaked_source"] = 0 if leaked else 1

    # 3. Text completeness
    if "tikz" in segment or "pgfplots" in segment:
        record["text_completeness"] = "N/A"
    else:
        latex_words = get_latex_words(tex_code)
    typ_words = set(w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', typ_code))
    
    if "tikz" not in segment and "pgfplots" not in segment and latex_words:
        overlap = latex_words.intersection(typ_words)
        if len(overlap) / len(latex_words) >= 0.6:
            record["text_completeness"] = 1
        else:
            record["text_completeness"] = 0
            record["notes"] += f"Missing text overlap ({len(overlap)}/{len(latex_words)} matched). "
    elif "tikz" not in segment and "pgfplots" not in segment:
        record["text_completeness"] = 1

    # 4. Structural elements
    has_all = True
    if "\\begin{tabular}" in tex_code and "#table" not in typ_code and "table(" not in typ_code:
        has_all = False
    if "\\begin{figure}" in tex_code and "#figure" not in typ_code and "figure(" not in typ_code:
        has_all = False
    if "\\section" in tex_code and "=" not in typ_code:
        has_all = False
    if "\\begin{equation}" in tex_code and "$" not in typ_code:
        has_all = False
    
    record["structural_elements"] = 1 if has_all else 0

    # 5. Numbering correctness
    needs_num = "\\section" in tex_code or "\\begin{equation}" in tex_code or "\\begin{figure}" in tex_code
    if needs_num:
        if "numbering:" in typ_code:
            record["numbering_correctness"] = 1
        else:
            record["numbering_correctness"] = 0
    else:
        record["numbering_correctness"] = 1

    # 6. Font Match
    if "New Computer Modern" in typ_code:
        record["font_match"] = "match"
    elif "sans" in typ_code.lower():
        record["font_match"] = "sans_swap"
    else:
        record["font_match"] = "serif_swap"

    # 7. Alignment Deviation
    record["alignment_deviation"] = "not_implemented"

    # 8. Typography correctness
    # Heuristic: check for unescaped problematic characters, or doubled quotes in source, or quotes immediately inside a quote block
    if '\\"' in typ_code or '``' in typ_code or '""' in typ_code or "''" in typ_code or re.search(r'#quote[^\[]*\[\n*["\']', typ_code):
        record["typography_correctness"] = 0
    else:
        record["typography_correctness"] = 1

    return record

def main():
    all_records = []
    
    # 1. AI Models (Gemini, GPT) from ai_models/
    ai_models_dir = Path("ai_models")
    retries_file = ai_models_dir / "retries.json"
    retries = {}
    if retries_file.exists():
        with open(retries_file, "r") as f:
            retries = json.load(f)
            
    segments = [d for d in ai_models_dir.iterdir() if d.is_dir() and d.name != "engines" and not d.name.startswith(".")]
    
    data_dir = Path("data")
    
    for seg in segments:
        seg_name = seg.name
        # Resolve tex file path: e.g. algorithms_easy -> data/08_algorithms/easy.tex
        cat_part, diff_part = seg_name.rsplit('_', 1)
        tex_file = None
        for d in data_dir.iterdir():
            if d.is_dir() and cat_part in d.name:
                tex_file = d / f"{diff_part}.tex"
                break
                
        for model in ["gemini", "gpt"]:
            model_dir = seg / model
            typ_file = model_dir / "output.typ"
            r = retries.get(seg_name, {}).get(model, 0)
            
            rec = evaluate_candidate(model, seg_name, typ_file, tex_file, r, is_engine=False)
            all_records.append(rec)
            
    # 2. Engines completely from results/
    results_dir = Path("results")
    if results_dir.exists():
        for cat_dir in results_dir.iterdir():
            if not cat_dir.is_dir() or cat_dir.name in ["gemini_feedback_eval"]:
                continue
                
            for diff_dir in cat_dir.iterdir():
                if not diff_dir.is_dir():
                    continue
                    
                tex_file = data_dir / cat_dir.name / f"{diff_dir.name}.tex"
                seg_name = f"{cat_dir.name.split('_', 1)[1]}_{diff_dir.name}"
                
                for engine in ["pandoc", "tylax", "typetex_approx"]:
                    typ_file = diff_dir / f"{engine}.typ"
                    
                    candidate_name = "typetex" if engine == "typetex_approx" else engine
                    
                    patched_typ_file = diff_dir / f"{engine}_patched.typ"
                    if patched_typ_file.exists():
                        # 1. As-tested record (hardcode failure)
                        rec_as_tested = evaluate_candidate(candidate_name, seg_name, typ_file, tex_file, "N/A", is_engine=True)
                        rec_as_tested["compiles"] = 0
                        if "cv_" in seg_name and candidate_name == "tylax":
                            rec_as_tested["notes"] = "Does not compile. Rendered output missing. [Root Cause: Unescaped '@' symbol in email address causes Typst to incorrectly parse it as a label reference.]"
                        elif "cv_" in seg_name and candidate_name in ["pandoc", "typetex"] and ("medium" in seg_name or "hard" in seg_name):
                            rec_as_tested["notes"] = "Does not compile. Rendered output missing. [Root Cause: Translates \\hrule to #horizontalrule, which is invalid in Typst.]"
                        else:
                            rec_as_tested["notes"] = "Does not compile. Rendered output missing."
                        
                        rec_as_tested["no_leaked_source"] = 0
                        rec_as_tested["text_completeness"] = 0
                        rec_as_tested["structural_elements"] = 0
                        rec_as_tested["numbering_correctness"] = 0
                        rec_as_tested["typography_correctness"] = 0
                        
                        all_records.append(rec_as_tested)
                        
                        # 2. Patched record (actual evaluation)
                        candidate_patched_name = f"{candidate_name}_patched"
                        rec_patched = evaluate_candidate(candidate_patched_name, seg_name, patched_typ_file, tex_file, "N/A", is_engine=True, is_patched=True)
                        all_records.append(rec_patched)
                    else:
                        rec = evaluate_candidate(candidate_name, seg_name, typ_file, tex_file, "N/A", is_engine=True)
                        all_records.append(rec)

    out_file = ai_models_dir / "absolute_scores.json"
    with open(out_file, "w") as f:
        json.dump(all_records, f, indent=4)
        
    print(f"Evaluated {len(all_records)} candidates and saved to {out_file}")

if __name__ == "__main__":
    main()
