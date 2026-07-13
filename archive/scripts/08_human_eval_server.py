import os
import csv
import json
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory, render_template_string

app = Flask(__name__)

# Paths
BASE_DIR = Path(__file__).parent.parent
AI_MODELS_DIR = BASE_DIR / "ai_models"
RATINGS_FILE = AI_MODELS_DIR / "manual_human_ratings.csv"
RETRIES_FILE = AI_MODELS_DIR / "retries.json"
DATA_DIR = BASE_DIR / "data" / "reference_pdfs"

# Initialize ratings CSV if not exists
if not RATINGS_FILE.exists():
    with open(RATINGS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["segment", "gemini_rank", "claude_rank", "gpt_rank", "comment"])

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Models Human Evaluation</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --bg-card: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --border: rgba(255, 255, 255, 0.1);
        }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
            color: var(--text-main);
            margin: 0; padding: 2rem;
            min-height: 100vh;
        }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .card { background: var(--bg-card); border-radius: 12px; border: 1px solid var(--border); padding: 1.5rem; display: flex; flex-direction: column; }
        .img-container { background: #fff; padding: 1rem; border-radius: 8px; flex-grow: 1; display: flex; justify-content: center; overflow: auto; max-height: 60vh; }
        .img-container img { max-width: 100%; height: auto; object-fit: contain; }
        .models-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem; }
        .model-card { background: rgba(0,0,0,0.3); border-radius: 8px; padding: 1rem; text-align: center; border: 1px solid var(--border); }
        .rank-buttons { display: flex; justify-content: center; gap: 0.5rem; margin-top: 1rem; }
        .rank-btn { background: rgba(255,255,255,0.1); border: 1px solid var(--border); color: white; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
        .rank-btn.selected { background: var(--accent); border-color: var(--accent); }
        .retries { color: #f87171; font-size: 0.85rem; margin-top: 0.5rem; }
        .submit-btn { background: var(--accent); color: white; border: none; padding: 1rem 2rem; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 2rem; width: 100%; font-size: 1.1rem; }
        .submit-btn:hover { background: #2563eb; }
        .comment { width: 100%; padding: 1rem; margin-top: 1rem; background: rgba(0,0,0,0.2); border: 1px solid var(--border); color: white; border-radius: 8px; box-sizing: border-box; }
        .engine-ref { margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px; border: 1px solid var(--border); }
        .engine-ref summary { cursor: pointer; font-weight: bold; color: var(--accent); }
        .engine-imgs { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem; }
        .engine-imgs img { width: 100%; background: #fff; border-radius: 4px; }
    </style>
</head>
<body>
    <div id="app"></div>
    <script>
        let currentSample = null;
        let rankings = { gemini: null, gpt: null };

        async function loadNext() {
            const res = await fetch('/api/next');
            const data = await res.json();
            if (data.status === 'done') {
                document.getElementById('app').innerHTML = '<h2>All segments rated!</h2>';
                return;
            }
            currentSample = data;
            rankings = { gemini: null, gpt: null };
            render();
        }

        function setRank(model, rank) {
            // Remove rank from other models if it's 1,2 (exclusive ranking)
            for (let m in rankings) {
                if (rankings[m] === rank) rankings[m] = null;
            }
            rankings[model] = rank;
            render();
        }

        async function copyImage(imgElement) {
            try {
                const response = await fetch(imgElement.src);
                const blob = await response.blob();
                await navigator.clipboard.write([
                    new ClipboardItem({ [blob.type]: blob })
                ]);
                
                // Visual feedback instead of alert
                const originalText = imgElement.nextElementSibling.innerText;
                imgElement.nextElementSibling.innerText = "Copied!";
                setTimeout(() => {
                    imgElement.nextElementSibling.innerText = originalText;
                }, 1000);
            } catch (err) {
                console.error(err.name, err.message);
            }
        }

        async function submit() {
            if (!rankings.gemini || !rankings.gpt) {
                alert("Please rank both models!");
                return;
            }
            const comment = document.getElementById('comment').value;
            await fetch('/api/rate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ segment: currentSample.segment, rankings, comment })
            });
            loadNext();
        }

        function render() {
            if (!currentSample) return;
            
            const renderModel = (model) => `
                <div class="model-card">
                    <h3>${model.toUpperCase()}</h3>
                    <div class="img-container" style="height: 250px; position: relative;">
                        ${currentSample.models[model] ? `<img id="img-${model}" src="/img/${currentSample.segment}/${model}/output.png" />
                        <button style="position:absolute; top: 10px; right: 10px; padding: 0.25rem 0.5rem; font-size: 0.8rem; background: rgba(0,0,0,0.5); color: white;" onclick="copyImage(document.getElementById('img-${model}'))">Copy</button>` : '<span>No output yet</span>'}
                    </div>
                    <div class="retries">Retries: ${currentSample.retries[model] || 0}</div>
                    <div class="rank-buttons">
                        ${[1,2].map(r => `
                            <button class="rank-btn ${rankings[model] === r ? 'selected' : ''}" onclick="setRank('${model}', ${r})">${r}</button>
                        `).join('')}
                    </div>
                </div>
            `;

            const engineImgs = ['pandoc', 'tylax'].map(eng => {
                return `<div><h4>${eng}</h4><img src="/engine_img/${currentSample.segment}/${eng}.png" onerror="this.parentElement.style.display='none'" /></div>`;
            }).join('');

            document.getElementById('app').innerHTML = `
                <div class="header">
                    <h1>Evaluating: ${currentSample.segment}</h1>
                    <span style="color: var(--text-muted)">(${currentSample.remaining} remaining)</span>
                </div>
                <div class="grid">
                    <div class="card">
                        <h2>Reference PDF</h2>
                        <div class="img-container" style="position: relative;">
                            <img id="ref-img" src="/ref_img/${currentSample.ref_path}" />
                            <button style="position:absolute; top: 10px; right: 10px; padding: 0.25rem 0.5rem; font-size: 0.8rem; background: rgba(0,0,0,0.5); color: white;" onclick="copyImage(document.getElementById('ref-img'))">Copy</button>
                        </div>
                    </div>
                    <div class="card">
                        <h2>AI Models</h2>
                        <div class="models-grid" style="grid-template-columns: 1fr 1fr;">
                            ${renderModel('gemini')}
                            ${renderModel('gpt')}
                        </div>
                        <textarea id="comment" class="comment" placeholder="Any comments?"></textarea>
                        <button class="submit-btn" onclick="submit()">Submit Rankings</button>
                        
                        <details class="engine-ref">
                            <summary>View Baseline Engines</summary>
                            <div class="engine-imgs">
                                ${engineImgs}
                            </div>
                        </details>
                    </div>
                </div>
            `;
        }

        loadNext();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/img/<segment>/<model>/<path:filename>')
def serve_img(segment, model, filename):
    return send_from_directory(AI_MODELS_DIR / segment / model, filename)
    
@app.route('/engine_img/<segment>/<path:filename>')
def serve_engine_img(segment, filename):
    return send_from_directory(AI_MODELS_DIR / segment / "engines", filename)
    
@app.route('/ref_img/<path:filename>')
def serve_ref_img(filename):
    return send_from_directory(DATA_DIR, filename)

@app.route('/api/next')
def get_next():
    # Get retries
    retries = {}
    if RETRIES_FILE.exists():
        with open(RETRIES_FILE, "r") as f:
            retries = json.load(f)
            
    # Get rated
    rated = set()
    if RATINGS_FILE.exists():
        with open(RATINGS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rated.add(row["segment"])
                
    # Find all segments
    segments = []
    if AI_MODELS_DIR.exists():
        for d in sorted(AI_MODELS_DIR.iterdir()):
            if d.is_dir() and d.name != "engines" and not d.name.startswith("."):
                segments.append(d.name)
                
    remaining = [s for s in segments if s not in rated]
    
    if not remaining:
        return jsonify({"status": "done"})
        
    target = remaining[0]
    
    # Figure out reference path
    # e.g., prose_easy -> 01_prose/easy.pdf
    # This requires matching the folder name.
    # Let's just find the pdf in data/reference_pdfs that ends with easy.pdf or hard.pdf
    cat_part = target.rsplit("_", 1)[0]
    diff_part = target.rsplit("_", 1)[1]
    
    # Find exact reference path
    ref_path = None
    for d in DATA_DIR.iterdir():
        if d.is_dir() and cat_part in d.name:
            if (d / f"{diff_part}.pdf").exists():
                # We need to serve a PNG of the reference. The old server used reference.png in results.
                # Since we don't have reference.png easily available, wait, we do in results/!
                pass
                
    # Actually, it's much easier to serve the reference PNG from results/
    results_dir = BASE_DIR / "results"
    ref_png_path = None
    for d in results_dir.iterdir():
        if d.is_dir() and cat_part in d.name:
            if (d / diff_part / "reference.png").exists():
                ref_png_path = f"{d.name}/{diff_part}/reference.png"
                break
                
    # Check what models exist
    models_exist = {}
    for m in ["gemini", "gpt"]:
        # We look for ANY png file in the model directory
        pngs = list((AI_MODELS_DIR / target / m).glob("*.png"))
        if pngs:
            # Send just the filename
            models_exist[m] = pngs[0].name
        else:
            models_exist[m] = None
            
    return jsonify({
        "status": "ok",
        "segment": target,
        "remaining": len(remaining),
        "ref_path": ref_png_path,
        "models": models_exist,
        "retries": retries.get(target, {})
    })

# We override the ref_img route to serve from results/ instead
@app.route('/ref_img/<cat>/<diff>/reference.png')
def serve_ref_png(cat, diff):
    return send_from_directory(BASE_DIR / "results" / cat / diff, "reference.png")

@app.route('/api/rate', methods=['POST'])
def rate():
    data = request.json
    segment = data.get("segment")
    r = data.get("rankings", {})
    
    with open(RATINGS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            segment,
            r.get("gemini", ""),
            r.get("claude", ""),
            r.get("gpt", ""),
            data.get("comment", "")
        ])
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
