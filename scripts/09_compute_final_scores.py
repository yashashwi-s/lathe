import csv
from collections import defaultdict
from pathlib import Path

def compute_scores():
    # Load compile status
    compile_status = {}
    with open("results/visual_metrics.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample_id = f"{row['category']}/{Path(row['filename']).stem}"
            compile_status[sample_id] = {
                "pandoc": float(row.get("pandoc_compile", 0)) > 0,
                "tylax": float(row.get("tylax_compile", 0)) > 0,
                "typetex_approx": float(row.get("typetex_approx_compile", 0)) > 0,
            }

    # Rank mappings
    rank_scores = {
        "1": 0.5,
        "2": 0.25,
        "3": 0.1,
        "4": 0.0
    }

    engines = ["pandoc", "tylax", "typetex_approx"]
    
    # Store category level aggregates
    cat_scores = defaultdict(lambda: {e: 0.0 for e in engines})
    cat_counts = defaultdict(int)
    overall_scores = {e: 0.0 for e in engines}
    total_samples = 0

    with open("results/human_ratings.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample_id = row["sample"]
            category = sample_id.split("/")[0]
            is_rubbish = row.get("is_rubbish", "false").lower() == "true"
            
            c_status = compile_status.get(sample_id, {e: False for e in engines})
            
            total_samples += 1
            cat_counts[category] += 1
            
            for eng in engines:
                score = 0.0
                
                # 0.5 for compiling successfully
                if c_status[eng]:
                    score += 0.5
                    
                # Visual score based on rank
                if not is_rubbish:
                    rank = row.get(f"{eng}_rank", "").strip()
                    if rank in rank_scores:
                        score += rank_scores[rank]
                        
                cat_scores[category][eng] += score
                overall_scores[eng] += score

    # Print markdown table
    print("## Final Aggregated Scores (Compile: 0.5 + Visual: up to 0.5)")
    print("| Category | Pandoc | Tylax | TypeTeX |")
    print("|----------|--------|-------|---------|")
    
    for cat in sorted(cat_scores.keys()):
        count = cat_counts[cat]
        scores = cat_scores[cat]
        # Normalize by count (average score out of 1.0)
        p = scores['pandoc'] / count
        t = scores['tylax'] / count
        tx = scores['typetex_approx'] / count
        print(f"| {cat} | {p:.2f} | {t:.2f} | {tx:.2f} |")
        
    print("| **OVERALL** | **{:.2f}** | **{:.2f}** | **{:.2f}** |".format(
        overall_scores['pandoc'] / total_samples,
        overall_scores['tylax'] / total_samples,
        overall_scores['typetex_approx'] / total_samples
    ))

if __name__ == "__main__":
    compute_scores()
