"""Regenerate human- and machine-readable reports for one AI conversion run."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    return parser.parse_args()


def load_records(run_dir: Path) -> list[dict]:
    records = []
    for path in sorted((run_dir / "samples").glob("*/meta.json")):
        records.append(json.loads(path.read_text()))
    return records


def render_rate(numerator: int, denominator: int) -> str:
    return "n/a" if denominator == 0 else f"{numerator}/{denominator} ({100 * numerator / denominator:.1f}%)"


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def write_manifest(run_dir: Path, records: list[dict]) -> None:
    fields = [
        "sample_id", "category", "complexity_band", "status", "attempts",
        "first_pass_compiled", "final_compiled", "repaired", "error_class",
        "reference_pages", "candidate_pages", "page_count_match", "prompt_tokens",
        "completion_tokens", "total_tokens", "reported_cost_usd", "duration_seconds",
        "estimated_cost_usd", "accounted_cost_usd", "requested_model",
        "resolved_model", "response_id",
    ]
    with (run_dir / "run_manifest.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in fields})


def write_errors(run_dir: Path, records: list[dict]) -> None:
    failed_attempts = []
    warning_counts = Counter()
    warning_rows = []
    for record in records:
        for attempt in record.get("attempt_records") or []:
            log_path = (
                run_dir / "samples" / record["sample_id"]
                / f"attempt_{attempt.get('attempt')}_compile.log"
            )
            log_text = log_path.read_text(errors="replace") if log_path.exists() else ""
            warnings = [line for line in log_text.splitlines() if line.startswith("warning:")]
            for warning in warnings:
                message = warning.removeprefix("warning:").strip()
                warning_counts[message] += 1
                warning_rows.append({
                    "sample_id": record["sample_id"],
                    "category": record["category"],
                    "attempt": attempt.get("attempt"),
                    "warning": message,
                    "compile_ok": attempt.get("compile_ok"),
                    "log_path": str(log_path.relative_to(run_dir)),
                })
            if attempt.get("compile_ok") is False:
                error_lines = [line for line in log_text.splitlines() if line.startswith("error:")]
                summary = error_lines[0] if error_lines else (
                    attempt.get("compiler_summary") or "no compiler output"
                )
                failed_attempts.append({
                    "sample_id": record["sample_id"],
                    "category": record["category"],
                    "complexity_band": record.get("complexity_band", ""),
                    "attempt": attempt.get("attempt"),
                    "error_class": attempt.get("error_class") or "unknown",
                    "summary": summary,
                    "eventual_result": "repaired" if record.get("final_compiled") else "final_failure",
                    "log_path": (
                        f"samples/{record['sample_id']}/"
                        f"attempt_{attempt.get('attempt')}_compile.log"
                    ),
                })
    infrastructure = [record for record in records if record.get("status") != "finished"]
    classes = Counter(item["error_class"] for item in failed_attempts)
    lines = [
        "# Compilation errors",
        "",
        "This report includes every failed Typst compilation attempt, including",
        "attempts later repaired by the model. API and local infrastructure failures",
        "are reported separately and do not count as model compilation failures.",
        "",
        f"- Failed compilation attempts: {len(failed_attempts)}",
        f"- Repaired failed attempts: {sum(item['eventual_result'] == 'repaired' for item in failed_attempts)}",
        f"- Samples with final compilation failure: {sum(not record.get('final_compiled') and record.get('status') == 'finished' for record in records)}",
        f"- Compiler warning occurrences: {len(warning_rows)}",
        f"- Infrastructure failures: {len(infrastructure)}",
        "",
        "## Error classes",
        "",
        "| Error class | Failed attempts |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(classes.items()))
    lines.extend(["", "## Compilation attempts", ""])
    if not failed_attempts:
        lines.append("No failed compilation attempts have been recorded.")
    else:
        lines.extend(["| Sample | Category | Attempt | Error class | Result | Error | Log |",
                      "|---|---|---:|---|---|---|---|"])
        for item in failed_attempts:
            error = str(item["summary"]).replace("|", "\\|")
            lines.append(
                f"| `{item['sample_id']}` | `{item['category']}` | {item['attempt']} | "
                f"`{item['error_class']}` | `{item['eventual_result']}` | {error} | "
                f"[`log`]({item['log_path']}) |"
            )
    lines.extend(["", "## Infrastructure failures", ""])
    if not infrastructure:
        lines.append("No API, provider, or local runner failures have been recorded.")
    else:
        lines.extend(["| Sample | Status | Error class | Error |", "|---|---|---|---|"])
        for record in infrastructure:
            error = str(record.get("final_error_summary") or "").replace("|", "\\|")
            lines.append(
                f"| `{record['sample_id']}` | `{record.get('status', 'unknown')}` | "
                f"`{record.get('error_class', 'unknown')}` | {error} |"
            )
    lines.extend(["", "## Compiler warnings", ""])
    if not warning_counts:
        lines.append("No compiler warnings have been recorded.")
    else:
        lines.extend(["| Warning | Occurrences |", "|---|---:|"])
        for warning, count in warning_counts.most_common():
            escaped_warning = warning.replace("|", "\\|")
            lines.append(f"| {escaped_warning} | {count} |")
    (run_dir / "compilation_errors.md").write_text("\n".join(lines) + "\n")
    fields = ["sample_id", "category", "complexity_band", "attempt", "error_class",
              "eventual_result", "summary", "log_path"]
    with (run_dir / "compilation_errors.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(failed_attempts)
    warning_fields = ["sample_id", "category", "attempt", "warning", "compile_ok", "log_path"]
    with (run_dir / "compilation_warnings.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=warning_fields, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(warning_rows)


def write_summary(run_dir: Path, records: list[dict]) -> None:
    finished = [record for record in records if record.get("status") == "finished"]
    infrastructure_errors = [record for record in records if record.get("status") != "finished"]
    first = sum(bool(record.get("first_pass_compiled")) for record in finished)
    final = sum(bool(record.get("final_compiled")) for record in finished)
    repaired = sum(bool(record.get("repaired")) for record in finished)
    page_matches = sum(bool(record.get("page_count_match")) for record in finished if record.get("final_compiled"))
    retry_opportunities = sum(not bool(record.get("first_pass_compiled")) for record in finished)
    cost = sum(float(record.get("reported_cost_usd") or 0) for record in finished)
    accounted_cost = sum(float(record.get("accounted_cost_usd") or 0) for record in finished)
    prompt_tokens = sum(int(record.get("prompt_tokens") or 0) for record in finished)
    completion_tokens = sum(int(record.get("completion_tokens") or 0) for record in finished)

    by_category = defaultdict(lambda: {"n": 0, "first": 0, "final": 0, "repaired": 0})
    for record in finished:
        cell = by_category[record["category"]]
        cell["n"] += 1
        cell["first"] += int(bool(record.get("first_pass_compiled")))
        cell["final"] += int(bool(record.get("final_compiled")))
        cell["repaired"] += int(bool(record.get("repaired")))

    config = json.loads((run_dir / "run_config.json").read_text()) if (run_dir / "run_config.json").exists() else {}
    expected_samples = int(config.get("split_count") or 33)
    split_path = str(config.get("split_path") or "")
    if "expansion_32.csv" in split_path:
        run_title = "AI LaTeX-to-Typst expansion evaluation"
        sample_scope = (
            f"These {expected_samples} dataset-expansion samples are a targeted "
            "post-freeze evaluation; they are excluded from the historical "
            "30-document prompt-development and 127-document held-out claims."
        )
    else:
        run_title = "AI LaTeX-to-Typst prompt-development run"
        sample_scope = (
            f"The {expected_samples} clean filtered samples are development data; "
            "results here are not held-out benchmark claims."
        )
    lines = [
        f"# {run_title}",
        "",
        "This directory is a self-contained audit record for one prompt/model configuration.",
        sample_scope,
        "",
        "## Configuration",
        "",
        f"- Model: `{config.get('model', 'not recorded')}`",
        f"- Prompt: `{config.get('prompt_path', 'not recorded')}`",
        f"- Typst: `{config.get('typst_version', 'not recorded')}`",
        f"- Maximum repair attempts: {config.get('max_repairs', 1)}",
        f"- Reference images supplied: "
        f"{'yes' if config.get('reference_images_supplied') else 'no'}",
        f"- Source graphics available during compile: "
        f"{'yes' if config.get('source_assets_available_during_compile') else 'no'}",
        f"- OpenRouter app attribution: "
        f"`{(config.get('openrouter_app') or {}).get('title', 'not recorded')}`",
        "",
        "## Results",
        "",
        f"- Recorded samples: {len(records)}/{expected_samples}",
        f"- Samples reaching model-output evaluation: {len(finished)}",
        f"- API/provider/local runner failures: {len(infrastructure_errors)}",
        f"- First-pass compile rate: {render_rate(first, len(finished))}",
        f"- Repair success: {render_rate(repaired, retry_opportunities)}",
        f"- Final compile rate: {render_rate(final, len(finished))}",
        f"- Page-count match among compiled outputs: {render_rate(page_matches, final)}",
        f"- Prompt tokens: {prompt_tokens}",
        f"- Completion tokens: {completion_tokens}",
        f"- API-reported cost: ${cost:.6f}",
        f"- Budget-accounted cost: ${accounted_cost:.6f}",
        "",
        "## By category",
        "",
        "| Category | Completed | First pass | Final | Repaired |",
        "|---|---:|---:|---:|---:|",
    ]
    for category in sorted(by_category):
        cell = by_category[category]
        lines.append(
            f"| `{category}` | {cell['n']} | {cell['first']} | {cell['final']} | {cell['repaired']} |"
        )
    lines.extend([
        "",
        "## Files",
        "",
        "- `run_config.json`: immutable run parameters and prompt hashes.",
        "- `run_manifest.csv`: one compact row per completed sample.",
        "- `compilation_errors.md`: grouped final failure summaries.",
        "- `compilation_errors.csv`: every failed compile attempt in machine-readable form.",
        "- `compilation_warnings.csv`: every compiler warning occurrence.",
        "- `analysis.md`: interpretation of this frozen run and its conditional PDF metrics.",
        "- `metric_v2/gate_ladder.{md,csv,json}`: non-compensating correctness gates and independent drivers.",
        "- `system_prompt.txt`, `retry_prompt.txt`, and `split_manifest.csv`: exact run snapshots.",
        "- `samples/<sample_id>/`: raw responses, normalized Typst, compiler logs, PDFs, and metadata.",
        "",
        "Regenerate this report with:",
        "",
        "```bash",
        f"mamba run -n lathe python scripts/ai/report_openrouter_typst.py {display_path(run_dir)}",
        "```",
    ])
    (run_dir / "README.md").write_text("\n".join(lines) + "\n")
    (run_dir / "summary.json").write_text(json.dumps({
        "completed": len(finished), "first_pass_compiled": first,
        "final_compiled": final, "repaired": repaired,
        "page_count_matches": page_matches,
        "retry_opportunities": retry_opportunities, "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens, "reported_cost_usd": cost,
        "accounted_cost_usd": accounted_cost,
    }, indent=2) + "\n")


def main() -> None:
    args = parse_args()
    args.run_dir.mkdir(parents=True, exist_ok=True)
    records = load_records(args.run_dir)
    write_manifest(args.run_dir, records)
    write_errors(args.run_dir, records)
    write_summary(args.run_dir, records)
    print(f"reported {len(records)} sample record(s) in {args.run_dir}")


if __name__ == "__main__":
    main()
