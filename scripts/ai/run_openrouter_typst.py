"""Run the source-only OpenRouter LaTeX-to-Typst prompt-development experiment.

Dry-run is the default. Paid requests require both `--execute` and the literal
`--confirm-paid-run YES`. Each sample receives one initial request and at most
one compiler-error repair request.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPLIT = ROOT / "data" / "latex_benchmark_v0" / "splits" / "prompt_dev_33.csv"
DEFAULT_SYSTEM = ROOT / "prompts" / "latex_to_typst" / "system_v0.txt"
DEFAULT_RETRY = ROOT / "prompts" / "latex_to_typst" / "retry_v0.txt"
DEFAULT_RUN_DIR = (
    ROOT / "results" / "ai_latex_to_typst" / "openrouter"
    / "google_gemini-3.1-flash-lite" / "prompt_v0"
)
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


class BudgetExhausted(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    parser.add_argument("--system-prompt", type=Path, default=DEFAULT_SYSTEM)
    parser.add_argument("--retry-prompt", type=Path, default=DEFAULT_RETRY)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--model", default="google/gemini-3.1-flash-lite")
    parser.add_argument("--samples", help="comma-separated sample IDs")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--max-completion-tokens", type=int, default=10_000)
    parser.add_argument("--max-cost-usd", type=float, default=1.00)
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--compile-timeout-seconds", type=int, default=90)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--recover-existing", action="store_true",
                        help="recover compiled attempts without loading the API key")
    parser.add_argument("--execute", action="store_true",
                        help="permit paid network requests")
    parser.add_argument("--confirm-paid-run", default="",
                        help="must be exactly YES when --execute is used")
    return parser.parse_args()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def strip_fences(text: str) -> str:
    """Apply the only allowed response normalization: remove outer code fences."""
    value = text.strip()
    match = re.fullmatch(r"```(?:typst|typ)?\s*\n(.*?)\n?```", value, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip() + "\n"
    lines = value.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip() + "\n"


def sanitize(text: str, secret: str = "") -> str:
    value = text.replace(str(ROOT), ".")
    if secret:
        value = value.replace(secret, "[REDACTED]")
    value = re.sub(r"sk-or-v1-[A-Za-z0-9_-]+", "[REDACTED]", value)
    return value


def compile_typst(source: Path, pdf: Path, timeout: int) -> tuple[bool, str, float]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            ["typst", "compile", str(source), str(pdf)],
            cwd=ROOT, capture_output=True, text=True, timeout=timeout,
        )
        output = (result.stderr or result.stdout or "").strip()
        return result.returncode == 0, sanitize(output), time.monotonic() - started
    except subprocess.TimeoutExpired:
        return False, f"typst compile timed out after {timeout} seconds", time.monotonic() - started


def pdf_pages(path: Path) -> int | None:
    if not path.exists():
        return None
    try:
        import fitz

        with fitz.open(path) as document:
            return len(document)
    except Exception:
        pass
    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo:
        result = subprocess.run([pdfinfo, str(path)], capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
            if match:
                return int(match.group(1))
    return None


def classify_failure(error: str, status: str = "") -> str:
    lower = error.lower()
    if status == "api_error":
        return "api_or_provider"
    if "timed out" in lower:
        return "compile_timeout"
    if "unknown variable" in lower or "unknown function" in lower:
        return "unknown_symbol_or_function"
    if "package" in lower or "failed to load" in lower or "module" in lower:
        return "package_or_import"
    if "label" in lower or "reference" in lower:
        return "reference_or_label"
    if "context is known" in lower or "context" in lower and "error:" in lower:
        return "context_required"
    if any(token in lower for token in ("math", "superscript", "subscript", "number suffix")):
        return "math_syntax"
    if any(token in lower for token in ("expected", "unexpected", "unclosed", "not valid in code")):
        return "general_syntax"
    return "other_compile_error"


def request_openrouter(payload: dict, key: str, timeout: int) -> dict:
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "X-OpenRouter-Title": "lathe-latex-to-typst-prompt-development",
            "X-OpenRouter-Metadata": "enabled",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {sanitize(body, key)[:2000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenRouter connection error: {sanitize(str(exc), key)}") from exc


def extract_response(response: dict) -> tuple[str, dict]:
    try:
        text = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("OpenRouter response did not contain assistant text") from exc
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("OpenRouter returned empty assistant text")
    return text, response.get("usage") or {}


def build_payload(model: str, messages: list[dict], max_tokens: int, session_id: str) -> dict:
    return {
        "model": model,
        "messages": messages,
        "temperature": 0,
        "max_completion_tokens": max_tokens,
        "session_id": session_id,
        "provider": {
            "sort": "price",
            "data_collection": "deny",
            "zdr": True,
            "max_price": {"prompt": 0.25, "completion": 1.50},
        },
    }


def safe_request_snapshot(payload: dict) -> dict:
    return payload  # Authorization is an HTTP header and is never placed in this object.


def load_rows(path: Path, sample_filter: set[str] | None, limit: int | None) -> list[dict]:
    rows = list(csv.DictReader(path.open(newline="")))
    if sample_filter is not None:
        found = {row["sample_id"] for row in rows}
        missing = sample_filter - found
        if missing:
            raise SystemExit(f"unknown sample IDs: {sorted(missing)}")
        rows = [row for row in rows if row["sample_id"] in sample_filter]
    return rows[:limit] if limit else rows


def current_cost(run_dir: Path) -> float:
    total = 0.0
    for path in (run_dir / "samples").glob("*/meta.json"):
        total += float(json.loads(path.read_text()).get("accounted_cost_usd") or 0)
    return total


def update_usage(meta: dict, usage: dict) -> str:
    prompt_tokens = int(usage.get("prompt_tokens") or 0)
    completion_tokens = int(usage.get("completion_tokens") or 0)
    meta["prompt_tokens"] += prompt_tokens
    meta["completion_tokens"] += completion_tokens
    meta["total_tokens"] += int(usage.get("total_tokens") or prompt_tokens + completion_tokens)
    estimated = prompt_tokens * 0.25 / 1_000_000 + completion_tokens * 1.50 / 1_000_000
    meta["estimated_cost_usd"] += estimated
    if usage.get("cost") is not None:
        reported = float(usage["cost"])
        meta["reported_cost_usd"] += reported
        meta["accounted_cost_usd"] += reported
        return "api_reported"
    meta["accounted_cost_usd"] += estimated
    return "token_estimate_at_max_price"


def recover_compiled_sample(args: argparse.Namespace, row: dict) -> dict | None:
    """Recover a compiled attempt if post-processing crashed before meta was saved."""
    sample_dir = args.run_dir / "samples" / row["sample_id"]
    attempts = [attempt for attempt in (1, 2)
                if (sample_dir / f"attempt_{attempt}.typ").exists()
                and (sample_dir / f"attempt_{attempt}.pdf").exists()
                and (sample_dir / f"response_{attempt}.json").exists()]
    if not attempts:
        return None
    attempt = max(attempts)
    typ_path = sample_dir / f"attempt_{attempt}.typ"
    pdf_path = sample_dir / f"attempt_{attempt}.pdf"
    compiled, compiler_output, compile_seconds = compile_typst(
        typ_path, pdf_path, args.compile_timeout_seconds
    )
    (sample_dir / f"attempt_{attempt}_compile.log").write_text(compiler_output + "\n")
    if not compiled:
        return None

    response = json.loads((sample_dir / f"response_{attempt}.json").read_text())
    usage = response.get("usage") or {}
    meta = {
        "sample_id": row["sample_id"],
        "category": row["category"],
        "complexity_band": row["complexity_band"],
        "status": "finished",
        "started_at": datetime.fromtimestamp(
            (sample_dir / f"request_{attempt}.json").stat().st_mtime, timezone.utc
        ).isoformat(timespec="seconds"),
        "attempts": attempt,
        "first_pass_compiled": attempt == 1,
        "final_compiled": True,
        "repaired": attempt == 2,
        "error_class": "",
        "final_error_summary": "",
        "reference_pages": int(row["page_count"]),
        "candidate_pages": pdf_pages(pdf_path),
        "page_count_match": False,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "reported_cost_usd": 0.0,
        "estimated_cost_usd": 0.0,
        "accounted_cost_usd": 0.0,
        "requested_model": args.model,
        "resolved_model": response.get("model") or "",
        "response_id": response.get("id") or "",
        "source_path": row["source_path"],
        "reference_pdf": row["reference_pdf"],
        "attempt_records": [{
            "attempt": attempt,
            "response_id": response.get("id"),
            "resolved_model": response.get("model"),
            "finish_reason": (response.get("choices") or [{}])[0].get("finish_reason"),
            "call_seconds": None,
            "compile_seconds": round(compile_seconds, 3),
            "compile_ok": True,
            "usage": usage,
            "cost_basis": "",
            "compiler_summary": "",
            "recovered_after_postprocessing_crash": True,
        }],
        "duration_seconds": None,
        "finished_at": utc_now(),
        "recovered_after_postprocessing_crash": True,
    }
    meta["page_count_match"] = meta["candidate_pages"] == meta["reference_pages"]
    cost_basis = update_usage(meta, usage)
    meta["attempt_records"][0]["cost_basis"] = cost_basis
    shutil.copy2(typ_path, sample_dir / "output.typ")
    shutil.copy2(pdf_path, sample_dir / "output.pdf")
    (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def run_sample(args: argparse.Namespace, row: dict, key: str,
               system_prompt: str, retry_prompt: str) -> dict:
    sample_id = row["sample_id"]
    sample_dir = args.run_dir / "samples" / sample_id
    sample_dir.mkdir(parents=True, exist_ok=True)
    source_path = ROOT / row["source_path"]
    reference_pdf = ROOT / row["reference_pdf"]
    latex = source_path.read_text(errors="replace")
    user_prompt = "Convert this complete LaTeX document to Typst:\n\n" + latex
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    started = time.monotonic()
    meta = {
        "sample_id": sample_id,
        "category": row["category"],
        "complexity_band": row["complexity_band"],
        "status": "running",
        "started_at": utc_now(),
        "attempts": 0,
        "first_pass_compiled": False,
        "final_compiled": False,
        "repaired": False,
        "error_class": "",
        "reference_pages": int(row["page_count"]),
        "candidate_pages": None,
        "page_count_match": False,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "reported_cost_usd": 0.0,
        "estimated_cost_usd": 0.0,
        "accounted_cost_usd": 0.0,
        "requested_model": args.model,
        "resolved_model": "",
        "response_id": "",
        "source_path": row["source_path"],
        "reference_pdf": row["reference_pdf"],
        "attempt_records": [],
    }

    final_error = ""
    for attempt in (1, 2):
        if current_cost(args.run_dir) + meta["accounted_cost_usd"] >= args.max_cost_usd:
            raise BudgetExhausted(f"reported run cost reached ${args.max_cost_usd:.2f}")
        payload = build_payload(args.model, messages, args.max_completion_tokens, sample_id)
        (sample_dir / f"request_{attempt}.json").write_text(
            json.dumps(safe_request_snapshot(payload), indent=2) + "\n"
        )
        call_started = time.monotonic()
        try:
            response = request_openrouter(payload, key, args.timeout_seconds)
            raw, usage = extract_response(response)
        except Exception as exc:
            error = sanitize(str(exc), key)
            meta["attempts"] = attempt
            meta["status"] = "api_error"
            meta["error_class"] = "api_or_provider"
            meta["final_error_summary"] = error[:300]
            meta["duration_seconds"] = round(time.monotonic() - started, 3)
            meta["finished_at"] = utc_now()
            (sample_dir / f"attempt_{attempt}_api_error.log").write_text(error + "\n")
            (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
            return meta
        call_seconds = time.monotonic() - call_started
        (sample_dir / f"response_{attempt}.json").write_text(json.dumps(response, indent=2) + "\n")
        cost_basis = update_usage(meta, usage)
        meta["resolved_model"] = response.get("model") or meta["resolved_model"]
        meta["response_id"] = response.get("id") or meta["response_id"]
        meta["attempts"] = attempt

        (sample_dir / f"attempt_{attempt}.raw.txt").write_text(raw)
        code = strip_fences(raw)
        typ_path = sample_dir / f"attempt_{attempt}.typ"
        pdf_path = sample_dir / f"attempt_{attempt}.pdf"
        typ_path.write_text(code)
        compiled, compiler_output, compile_seconds = compile_typst(
            typ_path, pdf_path, args.compile_timeout_seconds
        )
        (sample_dir / f"attempt_{attempt}_compile.log").write_text(compiler_output + "\n")
        meta["attempt_records"].append({
            "attempt": attempt,
            "response_id": response.get("id"),
            "resolved_model": response.get("model"),
            "finish_reason": (response.get("choices") or [{}])[0].get("finish_reason"),
            "call_seconds": round(call_seconds, 3),
            "compile_seconds": round(compile_seconds, 3),
            "compile_ok": compiled,
            "error_class": "" if compiled else classify_failure(compiler_output),
            "usage": usage,
            "cost_basis": cost_basis,
            "compiler_summary": "" if compiled else compiler_output.splitlines()[0][:300],
        })
        if attempt == 1:
            meta["first_pass_compiled"] = compiled
        if compiled:
            meta["final_compiled"] = True
            meta["repaired"] = attempt == 2
            shutil.copy2(typ_path, sample_dir / "output.typ")
            shutil.copy2(pdf_path, sample_dir / "output.pdf")
            meta["candidate_pages"] = pdf_pages(pdf_path)
            meta["page_count_match"] = meta["candidate_pages"] == meta["reference_pages"]
            break

        final_error = compiler_output
        if attempt == 1:
            messages.extend([
                {"role": "assistant", "content": raw},
                {"role": "user", "content": retry_prompt.format(
                    compiler_output=compiler_output[:6000]
                )},
            ])

    meta["status"] = "finished"
    meta["error_class"] = "" if meta["final_compiled"] else classify_failure(final_error)
    meta["final_error_summary"] = "" if meta["final_compiled"] else (
        final_error.splitlines()[0][:300] if final_error else "no compiler output"
    )
    meta["duration_seconds"] = round(time.monotonic() - started, 3)
    meta["finished_at"] = utc_now()
    (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def write_config(args: argparse.Namespace, system_prompt: str, retry_prompt: str) -> None:
    args.run_dir.mkdir(parents=True, exist_ok=True)
    config_path = args.run_dir / "run_config.json"
    config = {
        "created_at": utc_now(),
        "model": args.model,
        "split_path": relative(args.split),
        "split_sha256": sha256_text(args.split.read_text()),
        "split_count": sum(1 for _ in csv.DictReader(args.split.open(newline=""))),
        "split_snapshot": "split_manifest.csv",
        "prompt_path": relative(args.system_prompt),
        "retry_prompt_path": relative(args.retry_prompt),
        "system_prompt_sha256": sha256_text(system_prompt),
        "retry_prompt_sha256": sha256_text(retry_prompt),
        "temperature": 0,
        "max_completion_tokens": args.max_completion_tokens,
        "max_repairs": 1,
        "max_cost_usd": args.max_cost_usd,
        "source_only": True,
        "reference_images_supplied": False,
        "normalization": "remove outer Markdown code fences only",
        "provider": {"sort": "price", "data_collection": "deny", "zdr": True,
                     "max_price": {"prompt": 0.25, "completion": 1.50}},
        "typst_version": subprocess.run(
            ["typst", "--version"], capture_output=True, text=True, check=True
        ).stdout.strip(),
    }
    if config_path.exists():
        existing = json.loads(config_path.read_text())
        comparable = {key: value for key, value in existing.items() if key != "created_at"}
        expected = {key: value for key, value in config.items() if key != "created_at"}
        if comparable != expected:
            raise SystemExit("run_config.json exists with different parameters; use a new run directory")
    else:
        config_path.write_text(json.dumps(config, indent=2) + "\n")
    (args.run_dir / "system_prompt.txt").write_text(system_prompt)
    (args.run_dir / "retry_prompt.txt").write_text(retry_prompt)
    shutil.copy2(args.split, args.run_dir / "split_manifest.csv")


def regenerate_reports(run_dir: Path) -> None:
    script = ROOT / "scripts" / "ai" / "report_openrouter_typst.py"
    subprocess.run([sys.executable, str(script), str(run_dir)], cwd=ROOT, check=True)


def record_runner_error(args: argparse.Namespace, row: dict, exc: Exception, key: str) -> dict:
    """Persist an unexpected per-sample failure so the run can continue."""
    sample_dir = args.run_dir / "samples" / row["sample_id"]
    sample_dir.mkdir(parents=True, exist_ok=True)
    details = sanitize(traceback.format_exc(), key)
    (sample_dir / "runner_error.log").write_text(details + "\n")
    meta = {
        "sample_id": row["sample_id"],
        "category": row["category"],
        "complexity_band": row["complexity_band"],
        "status": "runner_error",
        "started_at": utc_now(),
        "finished_at": utc_now(),
        "attempts": 0,
        "first_pass_compiled": False,
        "final_compiled": False,
        "repaired": False,
        "error_class": "runner_or_local_infrastructure",
        "final_error_summary": sanitize(str(exc), key)[:300],
        "reference_pages": int(row["page_count"]),
        "candidate_pages": None,
        "page_count_match": False,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
        "reported_cost_usd": 0.0,
        "estimated_cost_usd": 0.0,
        "accounted_cost_usd": 0.0,
        "duration_seconds": None,
        "requested_model": args.model,
        "resolved_model": "",
        "response_id": "",
        "source_path": row["source_path"],
        "reference_pdf": row["reference_pdf"],
        "attempt_records": [],
    }
    (sample_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def main() -> None:
    args = parse_args()
    args.split = args.split.resolve()
    args.system_prompt = args.system_prompt.resolve()
    args.retry_prompt = args.retry_prompt.resolve()
    args.run_dir = args.run_dir.resolve()
    system_prompt = args.system_prompt.read_text()
    retry_prompt = args.retry_prompt.read_text()
    wanted = set(args.samples.split(",")) if args.samples else None
    rows = load_rows(args.split, wanted, args.limit)

    print(f"model: {args.model}")
    print(f"split: {relative(args.split)}")
    print(f"run directory: {relative(args.run_dir)}")
    print(f"planned samples: {len(rows)}")
    for row in rows:
        print(f"  {row['sample_id']} ({row['complexity_band']})")

    write_config(args, system_prompt, retry_prompt)
    regenerate_reports(args.run_dir)
    if args.recover_existing:
        recovered_count = 0
        for row in rows:
            meta_path = args.run_dir / "samples" / row["sample_id"] / "meta.json"
            previous = json.loads(meta_path.read_text()) if meta_path.exists() else {}
            if previous.get("status") == "finished":
                continue
            recovered = recover_compiled_sample(args, row)
            if recovered:
                recovered_count += 1
                print(f"recover {row['sample_id']}: compiled attempt {recovered['attempts']} already exists")
        regenerate_reports(args.run_dir)
        print(f"recovered {recovered_count} sample(s) without an API request")
    if not args.execute:
        print("dry run only: report scaffold written; no key loaded and no network request made")
        return
    if args.confirm_paid_run != "YES":
        raise SystemExit("paid execution requires --confirm-paid-run YES")

    load_dotenv(ROOT / ".env")
    key = os.environ.get("OPENROUTER", "").strip()
    if not key:
        raise SystemExit("OPENROUTER is not set")
    completed = 0
    try:
        for row in rows:
            meta_path = args.run_dir / "samples" / row["sample_id"] / "meta.json"
            if meta_path.exists() and not args.force:
                previous = json.loads(meta_path.read_text())
                if previous.get("status") == "finished":
                    print(f"skip {row['sample_id']}: already completed")
                    continue
                recovered = recover_compiled_sample(args, row)
                if recovered:
                    print(f"recover {row['sample_id']}: compiled attempt {recovered['attempts']} already exists")
                    regenerate_reports(args.run_dir)
                    continue
                print(f"retry {row['sample_id']}: previous status={previous.get('status', 'unknown')}")
            print(f"run {row['sample_id']}")
            try:
                meta = run_sample(args, row, key, system_prompt, retry_prompt)
            except Exception as exc:
                meta = record_runner_error(args, row, exc, key)
                print(f"  isolated runner error: {meta['final_error_summary']}")
            completed += 1
            print(f"  status={meta['status']} compiled={meta['final_compiled']} attempts={meta['attempts']}")
            regenerate_reports(args.run_dir)
    except BudgetExhausted as exc:
        print(f"stopped: {exc}")
    finally:
        regenerate_reports(args.run_dir)
    print(f"completed {completed} new sample(s)")


if __name__ == "__main__":
    main()
