import os
import csv
from pathlib import Path
from importlib import import_module

structural_scorer = import_module("10_score_structural")

BASE_DIR = Path(__file__).parent.parent
RESULTS_DIR = BASE_DIR / "results" / "gemini_feedback_eval"

def main():
    if not RESULTS_DIR.exists():
        print("No Gemini results found.")
        return

    print("| Sample | Zero-shot | Round 1 | Round 2 |")
    print("|---|---|---|---|")
    
    for sample_dir in sorted(RESULTS_DIR.iterdir()):
        if not sample_dir.is_dir():
            continue
            
        sample = sample_dir.name
        scores = []
        for round_idx in range(3):
            round_file = sample_dir / f"round_{round_idx}.typ"
            if round_file.exists():
                code = round_file.read_text()
                score = structural_scorer.score_structural_quality(code)
                scores.append(f"{score:.2f}")
            else:
                scores.append("-")
                
        print(f"| {sample} | {scores[0]} | {scores[1]} | {scores[2]} |")

if __name__ == "__main__":
    main()
