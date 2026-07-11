import os
import sys
import json
import time
import io
import shutil
import subprocess
from pathlib import Path
from PIL import Image

from dotenv import load_dotenv
load_dotenv()

from google import genai
from google.genai import types
from google.genai.errors import ClientError

sys.path.append(str(Path(__file__).parent.resolve()))
from importlib import import_module
feedback_utils = import_module("12_feedback_utils")

TARGET_CATEGORIES = [
    "tikz", "pgfplots", "algorithms", "cv", "beamer", "posters", "tables_complex"
]

DIFFICULTY_ORDER = {"hard": 0, "medium": 1, "easy": 2}

PROMPT_B = """You are converting a LaTeX document to Typst. Your primary goal is idiomatic, minimal, maintainable Typst code.

Use Typst's semantic constructs wherever the original content maps onto them:
- table() / table.cell() for anything tabular
- grid() or stack() for multi-column or sequential layouts
- align(), heading(), figure() for structural elements

Avoid place() with hardcoded dx/dy point values except where there is genuinely no semantic alternative. Avoid magic numbers.
Output only valid Typst source. Do not add markdown backticks if possible, just the raw source code."""

API_KEYS = []
clients = []
current_client_idx = 0

def init_clients():
    global API_KEYS, clients
    API_KEYS = [os.environ.get(k) for k in ["GEMINI_API_KEY", "API_1", "API_2", "API_3", "API_4", "API_5", "API_6", "API_7"] if os.environ.get(k)]
    if not API_KEYS:
        print("Error: No API keys found.")
        sys.exit(1)
    for key in API_KEYS:
        clients.append(genai.Client(api_key=key))

def call_gemini(contents, system_prompt=""):
    global current_client_idx
    config_args = {"temperature": 0.2}
    if system_prompt:
        config_args["system_instruction"] = system_prompt
        
    for attempt in range(len(clients) * 10): 
        try:
            client = clients[current_client_idx]
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(**config_args)
            )
            text = response.text.strip()
            if text.startswith("```typst"):
                text = text[8:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            # Smooth out the 120 RPM limit across 8 keys (2 requests per second)
            time.sleep(0.5)
            
            return text.strip()
            
        except ClientError as e:
            if e.code == 429:
                print(f"    Rate limited on key {current_client_idx}. Rotating...")
                current_client_idx = (current_client_idx + 1) % len(clients)
                if current_client_idx == 0:
                    print("    All keys rate limited. Sleeping for 65 seconds to reset RPM...")
                    time.sleep(65)
            else:
                raise e
        except Exception as e:
            print(f"    Unknown error: {e}. Rotating...")
            current_client_idx = (current_client_idx + 1) % len(clients)
            time.sleep(5)
            
    raise Exception("All API keys exhausted and retry loop failed.")

def compile_to_png(typ_file, png_out):
    try:
        res = subprocess.run(["typst", "compile", "--ppi", "144", str(typ_file), str(png_out)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
        return res.returncode == 0
    except Exception:
        return False

def main():
    init_clients()
    
    data_dir = Path("data")
    results_dir = Path("results/gemini_feedback_eval")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    samples = list(data_dir.rglob("*.tex"))
    
    # Filter for target categories
    filtered_samples = []
    for s in samples:
        if s.parent.name == "data": continue
        cat_name = s.parent.name
        if any(c in cat_name for c in TARGET_CATEGORIES):
            filtered_samples.append(s)
            
    # Sort by difficulty: hard -> medium -> easy
    filtered_samples.sort(key=lambda s: DIFFICULTY_ORDER.get(s.stem.lower(), 99))
    
    if "--fast" in sys.argv:
        filtered_samples = filtered_samples[:3]
        
    for tex_file in filtered_samples:
        cat_name = tex_file.parent.name
        diff_name = tex_file.stem
        sample_name = f"{cat_name}_{diff_name}"
        print(f"\nProcessing {sample_name}...")
        
        sample_dir = results_dir / sample_name
        sample_dir.mkdir(exist_ok=True)
        
        metadata = {"compilation_tries": 0, "logs": []}
        
        # Round 0: Zero-shot
        print("  [Phase A] Running Zero-shot...")
        history = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=f"Convert the following LaTeX to Typst:\n\n```latex\n{tex_file.read_text()}\n```")]
            )
        ]
        
        out_code = call_gemini(contents=history, system_prompt=PROMPT_B)
        history.append(types.Content(role="model", parts=[types.Part.from_text(text=out_code)]))
        
        current_typ = sample_dir / "current.typ"
        current_typ.write_text(out_code)
        
        # Compilation Loop (max 2 error fixes = 3 total checks)
        compiled = False
        for attempt in range(3):
            metadata["compilation_tries"] += 1
            success, err = feedback_utils.get_compile_feedback(current_typ)
            if success:
                compiled = True
                print("    Compile succeeded!")
                break
            
            if attempt == 2:
                print(f"    Compile failed on final attempt ({attempt+1}).")
                metadata["logs"].append(err)
                break
            
            print(f"    Compile failed (attempt {attempt+1}). Sending error feedback.")
            metadata["logs"].append(err)
            
            feedback_prompt = f"Your previous code failed to compile with the following error:\n{err}\n\nPlease fix the syntax errors and output the corrected valid Typst source."
            history.append(types.Content(role="user", parts=[types.Part.from_text(text=feedback_prompt)]))
            out_code = call_gemini(contents=history, system_prompt=PROMPT_B)
            history.append(types.Content(role="model", parts=[types.Part.from_text(text=out_code)]))
            current_typ.write_text(out_code)
            
        if not compiled:
            print("  [Phase A] Failed to compile after max attempts. Skipping.")
            with open(sample_dir / "metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
            continue
            
        # Phase B: Visual CV Evaluation (One-Time Correction)
        print("  [Phase B] Evaluating visual layout with SSIM...")
        png_out = sample_dir / "current.png"
        render_success = compile_to_png(current_typ, png_out)
        
        if render_success:
            ref_png = Path(f"results/{cat_name}/{diff_name}/reference.png")
            if ref_png.exists():
                diff_mask_path = sample_dir / "diff_mask.png"
                ssim_score = feedback_utils.compute_visual_diff(ref_png, png_out, diff_mask_path)
                print(f"    SSIM Score: {ssim_score:.4f}")
                
                metadata["initial_ssim"] = float(ssim_score)
                
                if ssim_score < 0.90:
                    print("    Layout differs (SSIM < 0.90). Generating one-time visual correction round...")
                    composite_path = sample_dir / "composite.png"
                    comp = feedback_utils.create_side_by_side_image(ref_png, png_out, composite_path)
                    
                    if comp and diff_mask_path.exists():
                        feedback_prompt = (
                            f"Your layout compiled but differs from the reference (SSIM similarity score: {ssim_score:.4f}). "
                            "I have attached two images: \n"
                            "1) A composite image showing the reference layout on the left, and your rendered output on the right.\n"
                            "2) A difference mask image showing the exact pixel differences (black indicates deviations).\n\n"
                            "Please analyze these images to see where your layout is wrong, and provide the corrected Typst code."
                        )
                        img_comp = Image.open(comp)
                        img_diff = Image.open(diff_mask_path)
                        
                        b_comp = io.BytesIO()
                        img_comp.save(b_comp, format="PNG")
                        part_comp = types.Part.from_bytes(data=b_comp.getvalue(), mime_type="image/png")
                        
                        b_diff = io.BytesIO()
                        img_diff.save(b_diff, format="PNG")
                        part_diff = types.Part.from_bytes(data=b_diff.getvalue(), mime_type="image/png")
                        
                        history.append(types.Content(
                            role="user", 
                            parts=[part_comp, part_diff, types.Part.from_text(text=feedback_prompt)]
                        ))
                        
                        out_code = call_gemini(contents=history, system_prompt=PROMPT_B)
                        current_typ.write_text(out_code)
                        
                        # Fix any new compilation errors introduced by visual feedback (up to 2 tries)
                        for attempt in range(2):
                            success, err = feedback_utils.get_compile_feedback(current_typ)
                            if success:
                                compile_to_png(current_typ, png_out)
                                print("    Visual correction compiled successfully.")
                                break
                            print(f"    Visual correction failed compile (attempt {attempt+1}). Fixing...")
                            history.append(types.Content(role="model", parts=[types.Part.from_text(text=out_code)]))
                            history.append(types.Content(role="user", parts=[types.Part.from_text(text=f"Compile error:\n{err}\nFix it.")]))
                            out_code = call_gemini(contents=history, system_prompt=PROMPT_B)
                            current_typ.write_text(out_code)
                else:
                    print("    Layout is good (SSIM >= 0.90). Skipping visual correction.")
            else:
                print("    No reference PNG found. Skipping visual eval.")
        else:
            print("    Render to PNG failed.")
            
        with open(sample_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
            
        # Output final gemini image to main results tree for human eval
        final_png = sample_dir / "current.png"
        if final_png.exists():
            final_dest = Path(f"results/{cat_name}/{diff_name}/gemini.png")
            final_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(final_png, final_dest)
            print(f"    Copied final output to {final_dest}")

if __name__ == "__main__":
    main()
