#!/usr/bin/env python3
"""Evaluate the current canonical AI outputs with exact run-protocol labels."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "ai"))

from build_all_models_engine_grid import (  # noqa: E402
    CANONICAL_SAMPLES,
    canonical_panels,
)
from pdf_fidelity import SCORECARD_CONFIG, SCORECARD_VERSION, compare_pdfs  # noqa: E402


DEFAULT_OUT = ROOT / "results" / "metric_calibration" / "canonical_ai_v0_3"
AI_CANDIDATES = {
    "gemini_3_1_flash_lite",
    "claude_sonnet_4_6",
    "claude_opus_4_7",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def portable(value: str | Path | None) -> str:
    if not value:
        return ""
    path = Path(value)
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def protocol(panel) -> dict[str, str]:
    if panel.candidate == "gemini_3_1_flash_lite":
        return {
            "provider": "OpenRouter",
            "model_id": "google/gemini-3.1-flash-lite",
            "protocol_id": "gemini_prompt_stage_cascade",
            "generation_method": "stored prompt-stage cascade; selected compiled stage",
            "visual_feedback": "none",
            "effort": "not exposed",
            "revision_policy": panel.status,
        }
    one_turn = "one-turn" in panel.label
    opus = panel.candidate == "claude_opus_4_7"
    if one_turn:
        protocol_id = "opus_one_turn_low" if opus else "sonnet_one_turn_low"
        method = "one-turn conversion; compile result only"
        visual, effort, revision = "none", "low", "none"
    elif opus:
        protocol_id = "opus_agentic_v3_visual_medium"
        method = "agentic v3 compile-score-revise loop"
        visual, effort, revision = "reference and candidate page images", "medium", "v3 loop"
    else:
        protocol_id = "sonnet_agentic_v1_visual_low"
        method = "agentic v1 compile-score-revise loop"
        visual, effort, revision = "reference and candidate page images", "low", "v1 loop"
    return {
        "provider": "Anthropic via Claude Code harness",
        "model_id": "claude-opus-4-7" if opus else "claude-sonnet-4-6",
        "protocol_id": protocol_id,
        "generation_method": method,
        "visual_feedback": visual,
        "effort": effort,
        "revision_policy": revision,
    }


def main() -> None:
    args = parse_args()
    compiled = args.out_dir / "compiled"
    if compiled.exists():
        shutil.rmtree(compiled)
    compiled.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    for sample_index, sample_id in enumerate(CANONICAL_SAMPLES, start=1):
        category = sample_id.rsplit("_", 1)[0]
        reference = ROOT / "data" / "latex_benchmark_v0" / "corpus" / category / sample_id / "reference.pdf"
        panels = [
            panel for panel in canonical_panels(compiled, sample_id, {})
            if panel.candidate in AI_CANDIDATES
        ]
        for panel_index, panel in enumerate(panels, start=1):
            print(
                f"[{sample_index:02d}/{len(CANONICAL_SAMPLES):02d}] "
                f"[{panel_index}/3] {sample_id} - {panel.label}",
                flush=True,
            )
            metadata = protocol(panel)
            base = {
                "sample_id": sample_id,
                "category": category,
                "candidate_key": panel.candidate,
                "display_label": panel.label,
                **metadata,
                "source_artifact": portable(panel.source),
                "candidate_pdf": portable(panel.path),
                "candidate_state": panel.state,
                "candidate_status": panel.status,
            }
            if panel.state != "ok" or not panel.path or not panel.path.exists():
                rows.append({
                    **base,
                    "scorecard_status": "unavailable",
                    "failed_gates": "compile",
                    "review_flags": "",
                    "diagnostic_flags": "",
                })
                continue
            result, *_ = compare_pdfs(reference, panel.path)
            scorecard = result["scorecard"]
            axes = scorecard["axes"]
            evidence = axes["layout"]["correspondence_evidence"]
            nontext = axes["appearance_proxy"]["nontext"]
            table = scorecard["specialized_diagnostics"]["tables"]
            formula = scorecard["specialized_diagnostics"]["formula_glyph_proxy"]
            rows.append({
                **base,
                "scorecard_status": scorecard["status"],
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
                "table_applicable": table["applicable"],
                "table_reference_count": table["reference_count"],
                "table_candidate_count": table["candidate_count"],
                "table_row_exact_rate": table.get("row_count_exact_rate", ""),
                "table_column_exact_rate": table.get("column_count_exact_rate", ""),
                "table_cell_count_ratio": table.get("cell_count_ratio", ""),
                "formula_applicable": formula["applicable"],
                "formula_character_precision": formula.get("character_precision", ""),
                "formula_character_recall": formula.get("character_recall", ""),
                "formula_character_f1": formula.get("character_f1", ""),
            })

    args.out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.out_dir / "canonical_ai_scorecard.csv"
    fieldnames = list(dict.fromkeys(key for row in rows for key in row))
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    (args.out_dir / "scorecard_config.json").write_text(
        json.dumps(SCORECARD_CONFIG, indent=2) + "\n", encoding="utf-8"
    )

    by_protocol: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_protocol[row["protocol_id"]].append(row)
    lines = [
        f"# Canonical AI audit - {SCORECARD_VERSION}",
        "",
        "Each row is one exact model/run protocol on one canonical hard sample. "
        "Agentic and one-turn protocols are not pooled. No aggregate fidelity score is computed.",
        "",
        "## Protocol results",
        "",
        "| Protocol | Available | Pass | Review | Fail | Mean token P/R | Mean layout | Mean appearance |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for protocol_id, protocol_rows in sorted(by_protocol.items()):
        available = [row for row in protocol_rows if row["scorecard_status"] != "unavailable"]
        statuses = Counter(row["scorecard_status"] for row in protocol_rows)
        mean = lambda key: sum(float(row[key]) for row in available) / max(1, len(available))
        lines.append(
            f"| `{protocol_id}` | {len(available)}/{len(protocol_rows)} | {statuses['pass']} | "
            f"{statuses['review']} | {statuses['fail']} | "
            f"{100 * mean('token_precision'):.1f}/{100 * mean('token_recall'):.1f} | "
            f"{100 * mean('layout'):.1f} | {100 * mean('appearance_proxy'):.1f} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "Status is a gate-and-review outcome, not a preference ranking. Axis means are descriptive "
        "within one protocol only. Formula and table diagnostics are extraction-dependent proxies. "
        "Manual visual audit is required for disagreements and low-evidence cases.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "mamba run -n lathe python scripts/evaluation/audit_canonical_ai_models.py",
        "```",
    ])
    (args.out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"rows={len(rows)}")
    print(f"summary={args.out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
