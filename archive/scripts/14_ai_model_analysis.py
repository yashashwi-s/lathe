import json
import csv
from pathlib import Path

def main():
    ai_models_dir = Path("ai_models")
    ratings_file = ai_models_dir / "manual_human_ratings.csv"
    retries_file = ai_models_dir / "retries.json"
    
    with open(retries_file, "r") as f:
        retries = json.load(f)
        
    ratings = {}
    with open(ratings_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ratings[row["segment"]] = row
            
    models = ["gemini", "gpt"]
    results = []
    
    print("Segment | Gemini Rank | Gemini Retries | Gemini Score | GPT Rank | GPT Retries | GPT Score")
    print("---|---|---|---|---|---|---")
    
    total_gemini = 0
    total_gpt = 0
    count = 0
    
    for seg in sorted(ratings.keys()):
        row = ratings[seg]
        seg_retries = retries.get(seg, {})
        
        scores = {}
        for m in models:
            # Rank score (max 0.5)
            rank = row.get(f"{m}_rank", "")
            rank_score = 0
            if rank == "1": rank_score = 0.5
            elif rank == "2": rank_score = 0.25
            
            # Compile score (max 0.5)
            r = seg_retries.get(m, 0)
            compile_score = max(0, 0.5 - (r * 0.1))
            
            scores[m] = rank_score + compile_score
            
        print(f"{seg} | {row.get('gemini_rank')} | {seg_retries.get('gemini', 0)} | {scores['gemini']:.2f} | {row.get('gpt_rank')} | {seg_retries.get('gpt', 0)} | {scores['gpt']:.2f}")
        
        total_gemini += scores["gemini"]
        total_gpt += scores["gpt"]
        count += 1
        
    print(f"\nOverall Average: Gemini = {total_gemini/count:.2f}, GPT = {total_gpt/count:.2f}")

if __name__ == "__main__":
    main()
