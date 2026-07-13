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
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in fields})


def write_errors(run_dir: Path, records: list[dict]) -> None:
    failures = [record for record in records if not record.get("final_compiled")]
    classes = Counter(record.get("error_class") or "unknown" for record in failures)
    lines = [
        "# Compilation errors",
        "",
        "This report is generated from per-sample `meta.json` records. API and",
        "infrastructure failures are kept separate from model-generated Typst errors.",
        "",
        "## Error classes",
        "",
        "| Error class | Final failures |",
        "|---|---:|",
    ]
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(classes.items()))
    lines.extend(["", "## Failed samples", ""])
    if not failures:
        lines.append("No final compilation failures have been recorded.")
    else:
        lines.extend(["| Sample | Category | Attempts | Error class | Final error |",
                      "|---|---|---:|---|---|"])
        for record in failures:
            error = str(record.get("final_error_summary") or "").replace("|", "\\|")
            lines.append(
                f"| `{record['sample_id']}` | `{record['category']}` | "
                f"{record.get('attempts', 0)} | `{record.get('error_class', 'unknown')}` | {error} |"
            )
    (run_dir / "compilation_errors.md").write_text("\n".join(lines) + "\n")


def write_summary(run_dir: Path, records: list[dict]) -> None:
    finished = [record for record in records if record.get("status") == "finished"]
    api_errors = [record for record in records if record.get("status") == "api_error"]
    first = sum(bool(record.get("first_pass_compiled")) for record in finished)
    final = sum(bool(record.get("final_compiled")) for record in finished)
    repaired = sum(bool(record.get("repaired")) for record in finished)
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
    lines = [
        "# AI LaTeX-to-Typst prompt-development run",
        "",
        "This directory is a self-contained audit record for one prompt/model configuration.",
        "The 33 samples are development data; results here are not held-out benchmark claims.",
        "",
        "## Configuration",
        "",
        f"- Model: `{config.get('model', 'not recorded')}`",
        f"- Prompt: `{config.get('prompt_path', 'not recorded')}`",
        f"- Typst: `{config.get('typst_version', 'not recorded')}`",
        f"- Maximum repair attempts: {config.get('max_repairs', 1)}",
        f"- Reference images supplied: no",
        "",
        "## Results",
        "",
        f"- Recorded samples: {len(records)}/33",
        f"- Samples reaching model-output evaluation: {len(finished)}",
        f"- API/provider failures: {len(api_errors)}",
        f"- First-pass compile rate: {render_rate(first, len(finished))}",
        f"- Repair success: {render_rate(repaired, retry_opportunities)}",
        f"- Final compile rate: {render_rate(final, len(finished))}",
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
        "- `system_prompt.txt`, `retry_prompt.txt`, and `prompt_dev_33.csv`: exact run snapshots.",
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
