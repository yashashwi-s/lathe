#!/usr/bin/env python3
"""Audit the development scorecard on the clean prompt-development cascade."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from pdf_fidelity import SCORECARD_CONFIG, SCORECARD_VERSION, compare_pdfs


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPLIT = ROOT / "data" / "latex_benchmark_v0" / "splits" / "prompt_dev_33.csv"
DEFAULT_SELECTION = (
    ROOT / "results" / "ai_latex_to_typst" / "documents"
    / "prompt_clean_v0_v1_v3_engine_comparison_manifest.csv"
)
DEFAULT_OUT = ROOT / "results" / "metric_calibration" / "prompt_dev_scorecard_v0_3"
AI_ROOT = (
    ROOT / "results" / "ai_latex_to_typst" / "openrouter"
    / "google_gemini-3.1-flash-lite"
)
STAGE_DIRS = {
    "v0": "prompt_v0",
    "v1_targeted_retry": "prompt_v1_v0_failures",
    "v3_rescue": "prompt_v3_prompt_dev_failures",
}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", type=Path, default=DEFAULT_SPLIT)
    parser.add_argument("--selection-manifest", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    split = read_csv(args.split)
    if args.limit:
        split = split[:args.limit]
    selection = {row["sample_id"]: row for row in read_csv(args.selection_manifest)}
    rows: list[dict] = []
    for index, sample in enumerate(split, start=1):
        sample_id = sample["sample_id"]
        stage = selection[sample_id]["ai_prompt_version"]
        reference = ROOT / sample["reference_pdf"]
        candidate = AI_ROOT / STAGE_DIRS[stage] / "samples" / sample_id / "output.pdf"
        print(f"[{index:02d}/{len(split):02d}] {sample_id} ({stage})", flush=True)
        result, *_ = compare_pdfs(reference, candidate)
        scorecard = result["scorecard"]
        axes = scorecard["axes"]
        evidence = axes["layout"]["correspondence_evidence"]
        nontext = axes["appearance_proxy"]["nontext"]
        tables = scorecard["specialized_diagnostics"]["tables"]
        formula = scorecard["specialized_diagnostics"]["formula_glyph_proxy"]
        rows.append({
            "sample_id": sample_id,
            "category": sample["category"],
            "complexity_band": sample["complexity_band"],
            "ai_stage": stage,
            "status": scorecard["status"],
            "failed_gates": ";".join(scorecard["failed_gates"]),
            "review_flags": ";".join(scorecard["review_flags"]),
            "diagnostic_flags": ";".join(scorecard["diagnostic_flags"]),
            "reference_pages": result["reference_pages"],
            "candidate_pages": result["candidate_pages"],
            "content": axes["content"]["score"],
            "token_precision": axes["content"]["token_precision"],
            "token_recall": axes["content"]["token_recall"],
            "numeric_exact": axes["content"]["numeric_token_multiset"]["exact"],
            "layout": axes["layout"]["score"],
            "layout_coverage_min": evidence["minimum_coverage"],
            "layout_reliability": evidence["reliability"],
            "typography": axes["typography"]["score"],
            "appearance_proxy": axes["appearance_proxy"]["score"],
            "appearance_local_q10": axes["appearance_proxy"]["local_worst_region"],
            "nontext_applicable": nontext["applicable"],
            "nontext_score": nontext["score"],
            "pagination": axes["pagination"]["score"],
            "table_applicable": tables["applicable"],
            "table_reference_count": tables["reference_count"],
            "table_candidate_count": tables["candidate_count"],
            "formula_applicable": formula["applicable"],
            "formula_character_recall": formula.get("character_recall", ""),
            "legacy_overall": result["scores"]["overall"],
        })

    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / "prompt_dev_scorecard.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.out_dir / "scorecard_config.json").write_text(
        json.dumps(SCORECARD_CONFIG, indent=2) + "\n", encoding="utf-8"
    )

    status_counts = Counter(row["status"] for row in rows)
    gate_counts: Counter[str] = Counter()
    review_counts: Counter[str] = Counter()
    diagnostic_counts: Counter[str] = Counter()
    category_status: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        category_status[row["category"]][row["status"]] += 1
        gate_counts.update(filter(None, row["failed_gates"].split(";")))
        review_counts.update(filter(None, row["review_flags"].split(";")))
        diagnostic_counts.update(filter(None, row["diagnostic_flags"].split(";")))
    lines = [
        f"# Prompt-development audit — {SCORECARD_VERSION}",
        "",
        "This is development data used to find gate disagreements for automated stress testing. "
        "It is not a held-out benchmark result.",
        "",
        "## Status distribution",
        "",
        "| Status | Samples |",
        "|---|---:|",
    ]
    for status in ("pass", "review", "fail"):
        lines.append(f"| `{status}` | {status_counts[status]} |")
    lines.extend([
        "",
        "## Failed critical gates",
        "",
        "| Gate | Samples |",
        "|---|---:|",
    ])
    for name, count in gate_counts.most_common():
        lines.append(f"| `{name}` | {count} |")
    lines.extend([
        "",
        "## Review triggers",
        "",
        "| Trigger | Samples |",
        "|---|---:|",
    ])
    for name, count in review_counts.most_common():
        lines.append(f"| `{name}` | {count} |")
    lines.extend([
        "",
        "## Diagnostic-only signals",
        "",
        "These signals are logged but cannot change status because blind validation found them weak or producer-sensitive.",
        "",
        "| Signal | Samples |",
        "|---|---:|",
    ])
    for name, count in diagnostic_counts.most_common():
        lines.append(f"| `{name}` | {count} |")
    lines.extend([
        "",
        "## Status by document form",
        "",
        "| Category | Pass | Review | Fail |",
        "|---|---:|---:|---:|",
    ])
    for category, counts in sorted(category_status.items()):
        lines.append(
            f"| `{category}` | {counts['pass']} | {counts['review']} | {counts['fail']} |"
        )
    lines.extend([
        "",
        "## Calibration use",
        "",
        "Prioritize automated perturbation checks for: (1) samples where a critical gate fails despite strong smooth axes, "
        "(2) samples with appearance/layout disagreement, and (3) category-specific clusters. The exact "
        "numeric mismatch diagnostic must be replaced by context-aware math comparison before it can become a gate.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "mamba run -n lathe python scripts/evaluation/audit_prompt_dev_scorecard.py",
        "```",
    ])
    (args.out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"status={dict(status_counts)}")
    print(f"summary={args.out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
