"""API-driven Gemini LaTeX→Typst conversion runner.

Runs every sample in data/survivors.csv through Gemini with a visual-fidelity
prompt (reference render attached), gives at most ONE retry with the exact
compiler error, and stores everything under ai_api/gemini/<sample_id>/.

Usage (from the repo root, lathe env):

  mamba run -n lathe python scripts/22_run_gemini_api.py                # full run, tough-first
  mamba run -n lathe python scripts/22_run_gemini_api.py --dry-run      # show the plan only
  mamba run -n lathe python scripts/22_run_gemini_api.py --limit 3      # first 3 pending samples
  mamba run -n lathe python scripts/22_run_gemini_api.py --samples cv_complex_hard,beamer_hard
  mamba run -n lathe python scripts/22_run_gemini_api.py --force        # redo finished samples
  mamba run -n lathe python scripts/22_run_gemini_api.py --no-image     # text-only prompting
  mamba run -n lathe python scripts/22_run_gemini_api.py --model gemini-2.5-pro

Outputs per sample (ai_api/gemini/<sample_id>/):
  attempt_1.typ / attempt_1_error.txt     first attempt (+ compiler error if it failed)
  attempt_2.typ / attempt_2_error.txt     retry, only if attempt 1 failed
  output.typ / output.pdf / output.png    final result (only when a compile succeeded)
  meta.json                               full record: model, keys, timings, scores
Plus: ai_api/run_manifest.csv (one row per finished sample) and logs/gemini_api_<ts>.log.
"""
import argparse
import csv
import json
import logging
import os
import re
import subprocess
import sys
import time
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from importlib import import_module
va = import_module("18_visual_alignment")  # reuse the benchmark's alignment scoring

import fitz

MANIFEST = ROOT / "ai_api" / "run_manifest.csv"
OUT_ROOT = None  # set in main(): ai_api/<model>/ so different models never mix
PITFALLS = (ROOT / "scripts" / "prompt_pitfalls.md").read_text()
GRAPHICS = ("tikz", "pgfplots", "posters")

# toughest categories first; within a category: hard, attention_*, medium, easy
CATEGORY_ORDER = ["13_cv_complex", "12_cv_simple", "15_beamer", "14_posters",
                  "10_tikz_complex", "11_pgfplots", "09_tikz_simple", "04_paper_full",
                  "07_tables_complex", "05_paper_small", "03_eq_hard", "08_algorithms",
                  "02_eq_simple", "06_tables_simple", "01_prose"]
DIFFICULTY_ORDER = {"hard": 0, "medium": 2, "easy": 3}  # attention_* → 1

SYSTEM_PROMPT = f"""You are an expert LaTeX-to-Typst converter. Your single objective: produce Typst source whose compiled PDF looks AS CLOSE AS POSSIBLE to the compiled output of the given LaTeX document — same page count, same layout, same visual structure, same text.

Rules, in priority order:
1. VISUAL FIDELITY BEATS CODE PURITY. Prefer idiomatic Typst (#table, #grid, #figure, headings, math), but when no semantic construct reproduces the look, patch your way there with explicit spacing (#v, #h), grid, rect, line, or place. A hacky visual match beats an elegant mismatch.
2. Your output must compile standalone with the Typst CLI (version 0.14). COMPILING AT ALL matters more than anything else: a plain but compiling document beats a beautiful one that errors.
3. Reproduce EVERY page of the reference, including title pages. Never silently drop content. The prompt tells you the reference page count and page size — match both with `#set page(...)` and `#pagebreak()`.
4. Never leave a page blank. For pictures you cannot translate directly (TikZ, plots), redraw an approximation with Typst primitives or CeTZ.
5. Output RAW Typst source only — no markdown fences, no commentary, no explanations.

TYPST QUICK RULES — Typst is NOT LaTeX. Every rule below corresponds to a compile error that actually occurred in previous runs. Violating any of these means failure:

1. ALL math lives inside dollar signs: inline `$x^2$`, display `$ x^2 $` (with spaces inside the dollars). The characters `^ _ & \\` are ONLY valid inside `$...$`. Never write math bare in markup or code.
2. Typst math is its own language, not LaTeX math: multi-character sub/superscripts need parentheses `sum_(k=1)^n`; fractions are `frac(a, b)` or `a/b`; `\\times`→`times`, `\\cdot`→`dot`, `\\leq`→`<=`, `\\infty`→`infinity`, Greek letters are bare words (`alpha`, `Sigma`); prose inside math goes in quotes: `$"error rate"$`. NEVER write a backslash command inside math.
3. Aligned multi-line equations are written INSIDE one math block using `&` and line breaks: `$ a &= b \\ c &= d $`. `#align(...)` does NOT align equations — it takes exactly one alignment (e.g. `center`) plus a body and only positions content on the page.
4. Tables: `#table(columns: 3, [A], [B], [C], ...)` — EVERY cell is its own `[bracketed]` argument separated by commas, including numbers: `[110]`, never bare `110`. Never use `&` or `\\` in a table. Column widths: `columns: (auto, 1fr, 3cm)`. Tables have no caption argument — wrap: `#figure(table(...), caption: [...])`.
5. `#set page(paper: "a4", margin: (x: 2.5cm, y: 3cm))` — the paper name is a QUOTED STRING. Font: `#set text(font: "New Computer Modern")` — exactly that name (no "Roman" suffix, never "Latin Modern Roman").
6. Page numbers: `#set page(numbering: "1")`. There is no `page-number()`; reading any counter requires `#context`, e.g. `#context counter(page).display()`.
7. `#` enters code from markup. Inside a `{...}` code block you are ALREADY in code: write `let`, `for`, `if` with NO `#`. Inside `[...]` you are back in markup.
8. Strings are always quoted; lengths always have units (`2pt`, `1.5cm`, `1fr`). Scientific notation like `2e` or `2.2e` is invalid — write the full number.
9. Package imports — this exact allowlist has been verified to exist; use ONLY these, with EXACTLY these versions, and only when needed:
   - `#import "@preview/cetz:0.3.2"` — general drawing (TikZ-like)
   - `#import "@preview/cetz-plot:0.1.1"` — data plots (pgfplots-like)
   - `#import "@preview/lovelace:0.3.0": *` — pseudocode
   - `#import "@preview/algo:0.3.4": algo, i, d, comment` — algorithms
   Anything else (@preview/plot, @preview/draw, @preview/algorithms, @preview/article, ...) DOES NOT EXIST and fails the compile. When unsure, use no imports at all — native Typst is always safest.
10. Bare `@word` is a cross-reference and crashes if the label doesn't exist — this includes emails and domains in text. Write emails with an escaped at (`user\\@navy.mil`) and URLs via `#link("https://x.gov")[x.gov]`. Only use `@label` for labels you created, and number headings before referencing them.
11. Spanning table cells: `table.cell(rowspan: 2)[...]` / `table.cell(colspan: 3)[...]` as the cell itself. NEVER pass `rowspan:`/`colspan:` directly to `#table(...)`, never invent `(rowspan: 2, [...])` tuples, and never repeat any named argument in any function call.
12. Upright words inside math use quotes: `$"MultiHead"(Q, K, V)$` — never `#text(...)` inside math.
13. In math, separate numbers from letters with a space: `2 i`, `10000^(2 i)` — Typst lexes `2i` as a number with an invalid unit suffix.

ACCUMULATED PITFALLS from previous runs — every one of these has actually burned us; avoid them all:

{PITFALLS}"""

RETRY_PROMPT = """Your Typst source failed to compile. This is your final attempt; the exact compiler output is below. Fix the errors and output the FULL corrected raw Typst source (the whole document, not a diff). No markdown fences, no commentary.

--- typst compile output ---
{error}
--- end ---"""

log = logging.getLogger("gemini_api")


# ---------------------------------------------------------------- key pool
class DailyQuotaExhausted(Exception):
    """Every key has hit its per-DAY free-tier quota; only tomorrow helps."""


class KeyPool:
    """Round-robin over all available API keys; rotate on 429; cool down when
    a full cycle is RPM-limited; abort cleanly when every key is out of its
    per-day quota (free tier: requests/day/project/model — keys sharing a
    Google Cloud project share this budget)."""

    KEY_NAMES = ["GEMINI_API_KEY", "API_1", "API_2", "API_3",
                 "API_4", "API_5", "API_6", "API_7"]

    def __init__(self):
        self.keys = [os.environ[k].strip() for k in self.KEY_NAMES
                     if os.environ.get(k, "").strip()]
        if not self.keys:
            sys.exit("ERROR: no API keys found in .env "
                     "(expected GEMINI_API_KEY and/or API_1..API_7)")
        self.clients = [genai.Client(api_key=k) for k in self.keys]
        self.idx = 0
        self.daily_dead = set()  # key indices that hit the per-day quota
        log.info(f"loaded {len(self.keys)} API keys")

    def _advance(self):
        for _ in range(len(self.clients)):
            self.idx = (self.idx + 1) % len(self.clients)
            if self.idx not in self.daily_dead:
                return
        raise DailyQuotaExhausted()

    def generate(self, model, contents):
        """Returns (text, key_index_used). Rotates keys on rate limits."""
        cooldowns = 0
        for _ in range(len(self.clients) * 6):
            if len(self.daily_dead) == len(self.clients):
                raise DailyQuotaExhausted()
            i = self.idx
            try:
                resp = self.clients[i].models.generate_content(
                    model=model,
                    contents=contents,
                    config=types.GenerateContentConfig(temperature=0.2),
                )
                self._advance()  # spread load
                text = (resp.text or "").strip()
                if not text:
                    raise RuntimeError("empty response text")
                return text, i
            except ClientError as e:
                if e.code == 429:
                    if "PerDay" in str(e):
                        self.daily_dead.add(i)
                        log.warning(f"  key #{i} DAILY quota exhausted "
                                    f"({len(self.daily_dead)}/{len(self.clients)} keys dead)")
                        self._advance()
                    else:
                        log.warning(f"  key #{i} rate-limited (RPM), rotating")
                        self._advance()
                        if self.idx <= i:  # wrapped a full cycle
                            cooldowns += 1
                            if cooldowns > 5:
                                raise RuntimeError("all keys exhausted repeatedly")
                            log.warning("  all live keys RPM-limited — cooling down 65s")
                            time.sleep(65)
                else:
                    log.error(f"  key #{i} API error {e.code}: {e}")
                    self._advance()
                    time.sleep(5)
            except DailyQuotaExhausted:
                raise
            except Exception as e:
                log.error(f"  key #{i} error: {e}")
                self._advance()
                time.sleep(5)
        raise RuntimeError("generate() failed after exhausting retries")


# ---------------------------------------------------------------- helpers
def strip_fences(text):
    """Remove markdown code fences even when malformed (missing/misplaced
    closing fence caused real 'unclosed raw text' compile failures)."""
    text = text.strip()
    m = re.match(r"^```(?:typst|typ)?\s*\n(.*?)\n?```\s*$", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    lines = [l for l in lines if l.strip() != "```"]
    return "\n".join(lines).strip()


def compile_typst(typ_file, pdf_file):
    """Returns (ok, stderr)."""
    try:
        res = subprocess.run(["typst", "compile", str(typ_file), str(pdf_file)],
                             capture_output=True, text=True, timeout=90)
        return res.returncode == 0, (res.stderr or res.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return False, "typst compile timed out after 90s"


def first_error_line(err):
    """First 'error:' line of compiler output (warnings may precede it)."""
    for line in err.splitlines():
        if line.startswith("error"):
            return line[:160]
    return err.splitlines()[0][:160] if err else "no output"


def render_png(pdf_file, png_file, dpi=150):
    doc = fitz.open(pdf_file)
    doc[0].get_pixmap(dpi=dpi).save(png_file)
    doc.close()


def ref_page_parts(ref_pdf, max_pages=3, dpi=110):
    """Reference pages as image Parts for the prompt."""
    doc = fitz.open(ref_pdf)
    parts = []
    for i in range(min(len(doc), max_pages)):
        parts.append(types.Part.from_bytes(
            data=doc[i].get_pixmap(dpi=dpi).tobytes("png"), mime_type="image/png"))
    n_pages = len(doc)
    w, h = doc[0].rect.width, doc[0].rect.height
    doc.close()
    return parts, n_pages, w, h


def load_samples():
    """survivors.csv rows → ordered list of dicts, toughest first."""
    rows = list(csv.DictReader(open(ROOT / "data" / "survivors.csv")))
    samples = []
    for r in rows:
        stem = Path(r["filename"]).stem
        sid = f"{r['category'].split('_', 1)[1]}_{stem}"
        diff_rank = 1 if stem.startswith("attention") else DIFFICULTY_ORDER.get(stem, 2)
        samples.append({
            "sample_id": sid,
            "category": r["category"],
            "stem": stem,
            "tex": ROOT / r["path"],
            "ref_pdf": ROOT / "data" / "reference_pdfs" / r["category"] / f"{stem}.pdf",
            "order": (CATEGORY_ORDER.index(r["category"]), diff_rank),
        })
    samples.sort(key=lambda s: s["order"])
    return samples


def score_alignment(sample_id, ref_pdf, cand_pdf):
    """Same scoring the benchmark uses (18_visual_alignment)."""
    try:
        if any(g in sample_id for g in GRAPHICS):
            res = va.evaluate_ssim(str(ref_pdf), str(cand_pdf))
        else:
            res = va.evaluate_iou(str(ref_pdf), str(cand_pdf))
        return {"alignment_score": res["alignment_score"],
                "content_match_rate": res["content_match_rate"],
                "reference_pages": res["reference_pages"],
                "candidate_pages": res["candidate_pages"],
                "page_count_mismatch": res["page_count_mismatch"]}
    except Exception as e:
        log.warning(f"  alignment scoring failed: {e}")
        return {"alignment_score": None, "content_match_rate": None,
                "scoring_error": str(e)}


def append_manifest(row):
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    new = not MANIFEST.exists()
    with open(MANIFEST, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["timestamp", "sample_id", "model",
                                          "with_image", "attempts", "compiled",
                                          "alignment_score", "content_match_rate",
                                          "ref_pages", "cand_pages", "duration_s"])
        if new:
            w.writeheader()
        w.writerow(row)


# ---------------------------------------------------------------- per-sample
def run_sample(pool, model, sample, with_image):
    sid = sample["sample_id"]
    out_dir = OUT_ROOT / sid
    out_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    tex = sample["tex"].read_text()
    parts = []
    if with_image and sample["ref_pdf"].exists():
        img_parts, n_pages, w, h = ref_page_parts(sample["ref_pdf"])
        parts += img_parts
        geometry = (f"The reference LaTeX output renders to {n_pages} page(s) of "
                    f"{w:.0f}x{h:.0f} pt. The attached image(s) show the reference "
                    f"render — match it as closely as you can.")
    else:
        n_pages = None
        geometry = "No reference render is attached; infer the layout from the LaTeX source."

    parts.append(types.Part.from_text(text=(
        f"{geometry}\n\nConvert this LaTeX document to Typst:\n\n"
        f"```latex\n{tex}\n```")))
    history = [types.Content(role="user", parts=parts)]

    meta = {"sample_id": sid, "model": model, "with_image": with_image,
            "started": datetime.now().isoformat(timespec="seconds"),
            "attempts": [], "compiled": False}

    code, compiled, error = None, False, None
    for attempt in (1, 2):
        log.info(f"  attempt {attempt}: calling {model} …")
        t_call = time.time()
        raw, key_idx = pool.generate(model, history)
        code = strip_fences(raw)
        typ = out_dir / f"attempt_{attempt}.typ"
        typ.write_text(code)

        ok, error = compile_typst(typ, out_dir / "output.pdf")
        meta["attempts"].append({
            "n": attempt, "key_index": key_idx,
            "gen_seconds": round(time.time() - t_call, 1),
            "code_chars": len(code), "compile_ok": ok,
            "error_snippet": None if ok else first_error_line(error),
        })
        if ok:
            compiled = True
            log.info(f"  attempt {attempt}: COMPILED  ({len(code)} chars, "
                     f"key #{key_idx}, {meta['attempts'][-1]['gen_seconds']}s)")
            break

        (out_dir / f"attempt_{attempt}_error.txt").write_text(error)
        log.info(f"  attempt {attempt}: compile FAILED — {first_error_line(error)}")
        if attempt == 1:
            history.append(types.Content(role="model",
                                         parts=[types.Part.from_text(text=raw)]))
            history.append(types.Content(role="user", parts=[types.Part.from_text(
                text=RETRY_PROMPT.format(error=error[:3000]))]))

    meta["compiled"] = compiled
    scores = {}
    if compiled:
        (out_dir / "output.typ").write_text(code)
        render_png(out_dir / "output.pdf", out_dir / "output.png")
        scores = score_alignment(sid, sample["ref_pdf"], out_dir / "output.pdf")
        meta["alignment"] = scores
        a = scores.get("alignment_score")
        m = scores.get("content_match_rate")
        log.info(f"  alignment: pos={a if a is None else round(a, 3)}  "
                 f"match={m if m is None else round(m, 3)}  "
                 f"pages ref/cand={scores.get('reference_pages')}/{scores.get('candidate_pages')}")
    else:
        (out_dir / "output.pdf").unlink(missing_ok=True)
        log.info("  FINAL: failed to compile after 2 attempts")

    meta["duration_s"] = round(time.time() - t0, 1)
    meta["finished"] = datetime.now().isoformat(timespec="seconds")
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    append_manifest({
        "timestamp": meta["finished"], "sample_id": sid, "model": model,
        "with_image": with_image, "attempts": len(meta["attempts"]),
        "compiled": compiled,
        "alignment_score": scores.get("alignment_score"),
        "content_match_rate": scores.get("content_match_rate"),
        "ref_pages": scores.get("reference_pages"),
        "cand_pages": scores.get("candidate_pages"),
        "duration_s": meta["duration_s"],
    })
    return meta


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--samples", help="comma-separated sample_ids to run")
    ap.add_argument("--limit", type=int, help="run at most N pending samples")
    ap.add_argument("--force", action="store_true", help="redo finished samples")
    ap.add_argument("--redo-failed", action="store_true",
                    help="also redo samples that previously failed to compile")
    ap.add_argument("--no-image", action="store_true", help="text-only prompting")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and exit")
    args = ap.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    (ROOT / "logs").mkdir(exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                        datefmt="%H:%M:%S", force=True,
                        handlers=[logging.FileHandler(ROOT / "logs" / f"gemini_api_{ts}.log"),
                                  logging.StreamHandler()])
    for noisy in ("google_genai", "google_genai.models", "httpx", "httpcore"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    global OUT_ROOT
    OUT_ROOT = ROOT / "ai_api" / args.model

    samples = load_samples()
    if args.samples:
        want = set(args.samples.split(","))
        samples = [s for s in samples if s["sample_id"] in want]
        missing = want - {s["sample_id"] for s in samples}
        if missing:
            sys.exit(f"ERROR: unknown sample_ids: {sorted(missing)}")

    pending = []
    for s in samples:
        meta_path = OUT_ROOT / s["sample_id"] / "meta.json"
        if meta_path.exists() and not args.force:
            if args.redo_failed:
                if json.loads(meta_path.read_text()).get("compiled"):
                    continue  # keep successes, redo failures
            else:
                continue
        pending.append(s)
    if args.limit:
        pending = pending[:args.limit]

    log.info(f"plan: {len(pending)} sample(s), model={args.model}, "
             f"image={'off' if args.no_image else 'on'} "
             f"({len(samples) - len(pending)} already done, use --force to redo)")
    for s in pending:
        log.info(f"  - {s['sample_id']}")
    if args.dry_run or not pending:
        return

    pool = KeyPool()
    done, compiled_n = 0, 0
    for s in pending:
        done += 1
        log.info(f"[{done}/{len(pending)}] ===== {s['sample_id']} =====")
        try:
            meta = run_sample(pool, args.model, s, with_image=not args.no_image)
            compiled_n += int(meta["compiled"])
        except DailyQuotaExhausted:
            done -= 1
            log.warning(f"DAILY QUOTA EXHAUSTED on every key for model {args.model}. "
                        f"Stopping cleanly — unfinished samples stay pending. "
                        f"Re-run the same command after the quota resets (midnight "
                        f"Pacific), or retry now with a different --model "
                        f"(per-day quotas are per model).")
            break
        except Exception as e:
            log.exception(f"  sample crashed: {e}")

    log.info(f"DONE: {compiled_n}/{done} compiled this session. "
             f"Manifest: {MANIFEST.relative_to(ROOT)}  Outputs: {OUT_ROOT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
