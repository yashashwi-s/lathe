#!/usr/bin/env python3
"""Build auditable model/engine scorecards for the PDF fidelity report."""

from __future__ import annotations

import csv
import json
import statistics
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "results" / "metric_research_v2" / "scorecards"
ENGINE_METRIC_DIR = OUT_DIR / "engine_metric_v2"
ENGINE_LABELS = {
    "pandoc": "Pandoc",
    "tylax": "Tylax",
    "typetex": "TypeTeX",
}
OVERLAP_SAMPLE_IDS = {
    "04_math_aligned_014",
    "05_tables_simple_005",
    "05_tables_simple_021",
    "05_tables_simple_023",
    "06_tables_moderate_010",
    "07_figures_captions_007",
    "09_algorithms_003",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def number(row: dict[str, str], field: str) -> float | None:
    value = row.get(field, "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def median(rows: list[dict[str, str]], field: str) -> float | None:
    values = [value for row in rows if (value := number(row, field)) is not None]
    return statistics.median(values) if values else None


def summarize(
    rows: list[dict[str, str]],
    *,
    system_id: str,
    label: str,
    protocol: str,
    total: int,
) -> dict[str, object]:
    scored = [row for row in rows if row.get("v2_status") == "scored"]
    page_exact = sum(number(row, "page_count_delta") == 0 for row in scored)
    canvas_exact = sum(number(row, "canvas_exact_size_rate") == 1 for row in scored)
    ssim_values = [
        value for row in scored
        if (value := number(row, "unregistered_ssim")) is not None
    ]
    return {
        "system_id": system_id,
        "label": label,
        "protocol": protocol,
        "total": total,
        "compiled": len(scored),
        "compile_rate": len(scored) / total,
        "page_exact": page_exact,
        "page_exact_rate_all": page_exact / total,
        "canvas_exact": canvas_exact,
        "canvas_exact_rate_compiled": canvas_exact / len(scored) if scored else None,
        "strict_word_f1_median": median(scored, "strict_word_f1"),
        "compatibility_word_f1_median": median(scored, "compatibility_word_f1"),
        "reference_coverage_median": median(scored, "matched_word_reference_coverage"),
        "center_q90_median": median(scored, "token_center_displacement_q90"),
        "text_ltsim_median": median(scored, "text_ltsim_page_macro"),
        "ssim_eligible": len(ssim_values),
        "ssim_median": statistics.median(ssim_values) if ssim_values else None,
    }


def build_engine_metrics() -> list[dict[str, str]]:
    accepted = read_csv(ROOT / "data" / "latex_benchmark_v0" / "accepted_manifest.csv")
    sample_dirs = {row["sample_id"]: row["sample_dir"] for row in accepted}
    engine_rows = read_csv(ROOT / "results" / "latex_benchmark_v0" / "engine_manifest.csv")
    pairs: list[dict[str, object]] = []
    for row in engine_rows:
        if row["compile_status"] != "ok":
            continue
        candidate = ROOT / row["pdf_path"]
        reference = ROOT / sample_dirs[row["sample_id"]] / "reference.pdf"
        if not candidate.is_file() or not reference.is_file():
            raise FileNotFoundError(f"missing scored PDF for {row['sample_id']} / {row['engine']}")
        pairs.append({
            "comparison_id": f"{row['sample_id']}__{row['engine']}",
            "sample_id": row["sample_id"],
            "category": row["category"],
            "system_id": row["engine"],
            "display_label": ENGINE_LABELS[row["engine"]],
            "protocol_id": "deterministic_engine",
            "reference_pdf": str(reference.relative_to(ROOT)),
            "candidate_pdf": row["pdf_path"],
        })
    manifest = OUT_DIR / "engine_pairs.csv"
    write_csv(manifest, pairs, list(pairs[0]))
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "evaluation" / "evaluate_metric_v2_manifest.py"),
            str(manifest),
            "--out-dir",
            str(ENGINE_METRIC_DIR),
            "--workers",
            "4",
            "--render-dpi",
            "96",
        ],
        cwd=ROOT,
        check=True,
    )
    return read_csv(ENGINE_METRIC_DIR / "metric_v2_scores.csv")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    engine_scores = build_engine_metrics()
    gemini_scores = read_csv(
        ROOT / "results" / "metric_research_v2" / "gemini_frozen_156" / "metric_v2_scores.csv"
    )
    overlap_scores = read_csv(
        ROOT / "results" / "metric_research_v2" / "claude_overlap" / "metric_v2" / "metric_v2_scores.csv"
    )

    overlap_systems = [
        ("gemini", "Gemini 3.1 Flash Lite", "source-only adaptive cascade"),
        ("claude_sonnet", "Claude Sonnet 4.6", "1 one-turn + 6 agentic visual"),
        ("claude_opus", "Claude Opus 4.7", "1 one-turn + 6 agentic visual"),
    ]
    overlap = [
        summarize(
            [row for row in overlap_scores if row["asset_role"] == system_id],
            system_id=system_id,
            label=label,
            protocol=protocol,
            total=7,
        )
        for system_id, label, protocol in overlap_systems
    ]
    overlap.extend(
        summarize(
            [
                row for row in engine_scores
                if row["system_id"] == engine and row["sample_id"] in OVERLAP_SAMPLE_IDS
            ],
            system_id=engine,
            label=label,
            protocol="deterministic engine",
            total=7,
        )
        for engine, label in ENGINE_LABELS.items()
    )

    full = [
        summarize(
            gemini_scores,
            system_id="gemini",
            label="Gemini 3.1 Flash Lite",
            protocol="adaptive v0-v3 cascade",
            total=157,
        )
    ]
    full.extend(
        summarize(
            [row for row in engine_scores if row["system_id"] == engine],
            system_id=engine,
            label=label,
            protocol="deterministic engine",
            total=157,
        )
        for engine, label in ENGINE_LABELS.items()
    )

    output = {
        "metric_version": "pdf_metric_axes_v2",
        "render_dpi": 96,
        "aggregation": "document median on compiled PDFs; counts retain the full universe",
        "overlap_7": overlap,
        "full_157": full,
    }
    output_path = OUT_DIR / "scorecards.json"
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
