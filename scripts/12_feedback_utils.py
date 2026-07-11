import subprocess
import difflib
from pathlib import Path
import numpy as np
try:
    from PIL import Image
    from skimage.metrics import structural_similarity as ssim
except ImportError:
    pass

def get_compile_feedback(typ_file: Path):
    """
    Compiles the Typst file. Returns (success, error_string_if_any).
    """
    try:
        res = subprocess.run(
            ["typst", "compile", str(typ_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15
        )
        if res.returncode == 0:
            return True, ""
        else:
            # Typst errors are verbose. We keep the last few lines or the first error block.
            err = res.stderr.strip()
            # Truncate if it's crazy long
            if len(err) > 1500:
                err = err[:1500] + "\n...[truncated]"
            return False, err
    except subprocess.TimeoutExpired:
        return False, "Error: Compilation timed out."
    except Exception as e:
        return False, f"Error: {str(e)}"

def generate_text_feedback(ref_txt_path: Path, current_txt_path: Path):
    """
    Returns a unified diff of the raw text to highlight missing or extra content.
    """
    if not ref_txt_path.exists() or not current_txt_path.exists():
        return ""
        
    ref_lines = ref_txt_path.read_text().splitlines()
    curr_lines = current_txt_path.read_text().splitlines()
    
    diff = list(difflib.unified_diff(
        curr_lines, ref_lines,
        fromfile='Your Output Text',
        tofile='Reference Text',
        lineterm=''
    ))
    
    if not diff:
        return "Content exactly matches reference."
        
    diff_str = "\n".join(diff[:50]) # Truncate diff to 50 lines
    if len(diff) > 50:
        diff_str += "\n...[diff truncated]"
        
    return "The text content differs from the reference:\n\n" + diff_str

def create_side_by_side_image(img1_path: Path, img2_path: Path, out_path: Path):
    """
    Creates a side-by-side comparison image for the multi-modal prompt.
    """
    if not img1_path.exists() or not img2_path.exists():
        return None
        
    try:
        im1 = Image.open(img1_path)
        im2 = Image.open(img2_path)
        
        # Ensure same height for side-by-side
        max_h = max(im1.height, im2.height)
        total_w = im1.width + im2.width
        
        new_im = Image.new('RGB', (total_w, max_h), (255, 255, 255))
        new_im.paste(im1, (0, 0))
        new_im.paste(im2, (im1.width, 0))
        
        new_im.save(out_path)
        return out_path
    except Exception as e:
        print(f"Error creating composite image: {e}")
        return None

def compute_visual_diff(ref_path: Path, gen_path: Path, diff_out_path: Path):
    """
    Computes SSIM between reference and generated images.
    Saves a difference mask to diff_out_path.
    Returns the SSIM score.
    """
    if not ref_path.exists() or not gen_path.exists():
        return 1.0 # Assume perfect if missing
        
    try:
        ref = Image.open(ref_path).convert('L')
        gen = Image.open(gen_path).convert('L')
        
        # Ensure exact same size for SSIM
        if ref.size != gen.size:
            gen = gen.resize(ref.size)
            
        ref_arr = np.array(ref)
        gen_arr = np.array(gen)
        
        score, diff = ssim(ref_arr, gen_arr, full=True)
        
        # Generate absolute difference mask for visual feedback
        # Dark where different, light where same, or just pure abs diff
        abs_diff = np.abs(ref_arr.astype(int) - gen_arr.astype(int)).astype(np.uint8)
        # Invert so differences are black, background is white
        diff_mask = 255 - abs_diff
        
        Image.fromarray(diff_mask).save(diff_out_path)
        return score
    except Exception as e:
        print(f"Error computing CV diff: {e}")
        return 1.0
