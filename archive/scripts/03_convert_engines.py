import csv
import subprocess
import os
import re
from pathlib import Path
import json

def run_conversion(name, cmd, cwd, input_file, output_file, prepend=""):
    try:
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        print(f"    Timeout running {name}")
    except Exception as e:
        print(f"    Error running {name}: {e}")
        
    if prepend and output_file.exists():
        content = output_file.read_text()
        output_file.write_text(prepend + content)
        
    # Try compiling with Typst
    if output_file.exists():
        result = subprocess.run(["typst", "compile", str(output_file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return 1
    return 0

def main():
    survivors_path = Path("data/survivors.csv")
    if not survivors_path.exists():
        print("No survivors found.")
        return

    results = []
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    mitex_preamble = '#import "@preview/mitex:0.2.4": *\n#set heading(numbering: "1.")\n'

    with open(survivors_path, "r") as f:
        samples = list(csv.DictReader(f))

    for sample in samples:
        src_path = Path(sample["path"]).resolve()
        cat = sample["category"]
        fname = sample["filename"]
        base = src_path.stem
        
        print(f"Processing {cat}/{fname}...")
        
        out_dir = results_dir / cat / base
        out_dir.mkdir(parents=True, exist_ok=True)
        
        if not src_path.exists():
            continue
            
        tex_content = src_path.read_text()
        
        scores = {
            "category": cat,
            "filename": fname,
            "difficulty": sample["difficulty"]
        }
        
        # 1. Pandoc
        pandoc_out = out_dir / "pandoc.typ"
        scores["pandoc"] = run_conversion(
            "pandoc",
            ["pandoc", "-f", "latex", "-t", "typst", str(src_path), "-o", str(pandoc_out)],
            out_dir, src_path, pandoc_out
        )
        
        # 2. Tylax
        tylax_bin = os.path.expanduser("~/.cargo/bin/t2l")
        tylax_out = out_dir / "tylax.typ"
        scores["tylax"] = run_conversion(
            "tylax",
            [tylax_bin, "-f", "-o", str(tylax_out), str(src_path)],
            out_dir, src_path, tylax_out
        )
        
        # 3. TypeTeX Approximation (Pandoc + MiTeX)
        typetex_out = out_dir / "typetex_approx.typ"
        filter_path = Path("scripts/typetex_filter.lua").resolve()
        scores["typetex_approx"] = run_conversion(
            "typetex",
            ["pandoc", "-f", "latex", "-t", "typst", "--lua-filter", str(filter_path), str(src_path), "-o", str(typetex_out)],
            out_dir, src_path, typetex_out,
            prepend=mitex_preamble
        )
        
        results.append(scores)
        print(f"  Scores: Pandoc={scores['pandoc']} Tylax={scores['tylax']} TypeTeX={scores['typetex_approx']}")

    with open("results/compile_metrics.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "filename", "difficulty", "pandoc", "tylax", "typetex_approx"])
        writer.writeheader()
        writer.writerows(results)
        
    print("\nConversion complete.")

if __name__ == "__main__":
    main()
