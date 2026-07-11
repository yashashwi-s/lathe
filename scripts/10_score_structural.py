import re
import sys
from pathlib import Path
from collections import Counter

def score_structural_quality(typ_content):
    score = 1.0
    
    # 1. Penalize imports of absolute-place or drafting
    bad_packages = re.findall(r'#import.*\"@preview/(absolute-place|drafting)', typ_content)
    if bad_packages:
        score -= 0.3 * len(bad_packages)
        
    # 2. Penalize place() with literal dx/dy
    # Matches: place(dx: 10pt, dy: 20pt) or similar.
    # Look for place( ... dx: <number><unit> ... )
    place_literals = re.findall(r'place\([^)]*d[xy]:\s*-?\d+\.?\d*[a-zA-Z%]+', typ_content)
    if place_literals:
        # Penalize a bit for each occurrence, cap at 0.4 penalty
        penalty = min(0.4, 0.05 * len(place_literals))
        score -= penalty
        
    # 3. Penalize fake tables (repeated rect/line) vs real tables (table/grid)
    num_tables = len(re.findall(r'\b(table|grid)\s*\(', typ_content))
    num_rects = len(re.findall(r'\brect\s*\(', typ_content))
    num_lines = len(re.findall(r'\bline\s*\(', typ_content))
    
    # If there are many rects/lines and no tables, big penalty.
    if num_rects + num_lines > 5:
        if num_tables == 0:
            # Likely faking a table entirely
            score -= 0.3
        else:
            # Mixed
            score -= 0.1
            
    # Reward for using tables properly
    if num_tables > 0:
        score += min(0.2, 0.05 * num_tables)

    # 4. Penalize repeated magic numbers (lengths)
    # Match standard Typst lengths: pt, mm, cm, in, em, fr
    lengths = re.findall(r'\b\d+\.?\d*(pt|mm|cm|in|em)\b', typ_content)
    # We want to capture the actual string, not just the unit group
    length_strings = re.findall(r'\b(\d+\.?\d*(?:pt|mm|cm|in|em))\b', typ_content)
    
    counts = Counter(length_strings)
    magic_number_penalty = 0.0
    for length_str, count in counts.items():
        if count >= 3:
            magic_number_penalty += 0.05
    # Cap magic number penalty
    score -= min(0.3, magic_number_penalty)
    
    # 5. Reward set/show rules
    num_set_show = len(re.findall(r'#(set|show)\b', typ_content))
    if num_set_show > 0:
        score += min(0.3, 0.05 * num_set_show)
        
    return max(0.0, min(1.0, score))

def main():
    if len(sys.argv) < 2:
        print("Usage: python 10_score_structural.py <file.typ>")
        sys.exit(1)
        
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)
        
    content = file_path.read_text()
    score = score_structural_quality(content)
    print(f"{score:.2f}")

if __name__ == "__main__":
    main()
