import os
import shutil
from pathlib import Path

SEGMENTS = [
    ("01_prose", "easy"),
    ("01_prose", "hard"),
    ("02_eq_simple", "hard"),
    ("03_eq_hard", "hard"),
    ("07_tables_complex", "easy"),
    ("07_tables_complex", "hard"),
    ("08_algorithms", "easy"),
    ("08_algorithms", "medium")
]

PROMPT_TEMPLATE = """You are converting a LaTeX document to Typst. Your primary goal is idiomatic, minimal, maintainable Typst code.
Use Typst's semantic constructs wherever the original content maps onto them:

table() / table.cell() for anything tabular
grid() or stack() for multi-column or sequential layouts
align(), heading(), figure() for structural elements
Avoid place() with hardcoded dx/dy point values except where there is genuinely no semantic alternative. Avoid magic numbers.
Output only valid Typst source. Do not add markdown backticks if possible, just the raw source code.

{latex_code}

i want the exact same visual output. with good code quality. read the typs docs dont guess"""

def main():
    ai_models_dir = Path("ai_models")
    ai_models_dir.mkdir(exist_ok=True)
    
    for cat, diff in SEGMENTS:
        # Create segment folder name (e.g., prose_easy)
        cat_name = cat.split("_", 1)[1] if "_" in cat else cat
        segment_name = f"{cat_name}_{diff}"
        segment_dir = ai_models_dir / segment_name
        
        segment_dir.mkdir(exist_ok=True)
        
        # Create ai model folders and engines folder
        for folder in ["gemini", "claude", "gpt", "engines"]:
            (segment_dir / folder).mkdir(exist_ok=True)
            
        # 1. Generate prompt.txt
        tex_path = Path(f"data/{cat}/{diff}.tex")
        if tex_path.exists():
            latex_code = tex_path.read_text()
            prompt = PROMPT_TEMPLATE.replace("{latex_code}", latex_code)
            (segment_dir / "prompt.txt").write_text(prompt)
        else:
            print(f"Warning: {tex_path} not found!")
            
        # 2. Copy engine results if they exist (Removed typetex)
        engines = ["pandoc.typ", "tylax.typ"]
        for eng in engines:
            src_eng = Path(f"results/{cat}/{diff}/{eng}")
            dst_eng = segment_dir / "engines" / eng
            if src_eng.exists():
                shutil.copy2(src_eng, dst_eng)
            else:
                print(f"Warning: Engine result {src_eng} not found!")
                
        # Also clean up typetex_approx if it exists
        typetex_typ = segment_dir / "engines" / "typetex_approx.typ"
        typetex_png = segment_dir / "engines" / "typetex_approx.png"
        if typetex_typ.exists():
            typetex_typ.unlink()
        if typetex_png.exists():
            typetex_png.unlink()
                
    print("AI Models setup complete!")

if __name__ == "__main__":
    main()
