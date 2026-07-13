import csv
import subprocess
from pathlib import Path
import shutil

def main():
    manifest_path = Path("data/manifest.csv")
    pdf_dir = Path("data/reference_pdfs")
    pdf_dir.mkdir(parents=True, exist_ok=True)
    failures_dir = Path("failures")
    failures_dir.mkdir(exist_ok=True)

    with open(manifest_path, "r") as f:
        reader = csv.DictReader(f)
        samples = list(reader)

    survivors = []

    for sample in samples:
        src_path = Path(sample["path"])
        if not src_path.exists():
            continue
            
        print(f"Compiling {src_path}...")
        
        # Compile in the pdf_dir to avoid clutter
        out_dir = pdf_dir / sample["category"]
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", str(out_dir), str(src_path)]
        
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            survivors.append(sample)
            print(f"  Success: {src_path}")
        else:
            print(f"  FAILED: {src_path}")
            # Move failed tex file to failures/
            dest = failures_dir / f"{sample['category']}_{sample['filename']}"
            shutil.move(src_path, dest)

    # Write surviving manifest
    with open("data/survivors.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=samples[0].keys())
        writer.writeheader()
        writer.writerows(survivors)
        
    print(f"\nCompile gate complete. {len(survivors)} / {len(samples)} survived.")

if __name__ == "__main__":
    main()
