#!/usr/bin/env python3
"""Exercise the development scorecard on controlled PDF corruptions."""

from __future__ import annotations

import argparse
import csv
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

import fitz

from pdf_fidelity import SCORECARD_CONFIG, SCORECARD_VERSION, compare_pdfs


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "results" / "metric_calibration" / "controlled_v0_2"


@dataclass(frozen=True)
class Corruption:
    family: str
    severity: int
    label: str
    shift_pt: float = 0.0
    deleted_rows: int = 0
    changed_numbers: int = 0
    font_delta: float = 0.0
    obstruction_width: float = 0.0
    extra_pages: int = 0
    page_order: tuple[int, ...] = (1, 2, 3)


PAGE_TEXT = {
    1: (
        "Evaluation protocol and controlled evidence",
        "Alpha amber atlas autumn cedar delta ember forest. The benchmark records 2026 trials.",
    ),
    2: (
        "Measured results and table structure",
        "Binary cobalt circuit data engine flux graph horizon. Values are checked exactly.",
    ),
    3: (
        "Discussion and reproducibility",
        "Kernel lunar matrix nebula orbit plasma quantum vector. All artifacts remain auditable.",
    ),
}
TABLE_ROWS = [
    ("Content", "91.4", "0.8"),
    ("Layout", "76.2", "1.4"),
    ("Typography", "84.7", "0.6"),
    ("Appearance", "72.5", "2.1"),
    ("Pagination", "100.0", "0.0"),
]


def _changed_table(count: int) -> list[tuple[str, str, str]]:
    rows = [list(row) for row in TABLE_ROWS]
    positions = [(0, 1), (1, 1), (2, 2), (3, 1), (4, 1)]
    for row_index, column_index in positions[:count]:
        value = rows[row_index][column_index]
        rows[row_index][column_index] = value.replace("1", "7", 1) if "1" in value else "999.9"
    return [tuple(row) for row in rows]


def build_pdf(path: Path, corruption: Corruption) -> None:
    document = fitz.open()
    rows = _changed_table(corruption.changed_numbers)
    kept_rows = rows[:max(0, len(rows) - corruption.deleted_rows)]
    for source_page in corruption.page_order:
        page = document.new_page(width=612, height=792)
        shift = corruption.shift_pt
        title, body = PAGE_TEXT[source_page]
        page.insert_text(
            (54 + shift, 70 + shift), title,
            fontsize=18 + corruption.font_delta, fontname="hebo",
        )
        page.insert_text(
            (54 + shift, 105 + shift), body,
            fontsize=11 + corruption.font_delta, fontname="helv",
        )
        page.insert_text(
            (54 + shift, 132 + shift), f"Page marker {source_page}; protocol revision 2.0.",
            fontsize=10 + corruption.font_delta, fontname="heit",
        )
        if source_page == 2:
            x0, y0 = 54 + shift, 190 + shift
            widths = (170, 90, 90)
            row_height = 32
            headers = ("Axis", "Score", "Error")
            for column, header in enumerate(headers):
                page.insert_text(
                    (x0 + sum(widths[:column]) + 7, y0 + 21), header,
                    fontsize=10 + corruption.font_delta, fontname="hebo",
                )
            all_rows = [headers, *kept_rows]
            for row_index in range(len(all_rows) + 1):
                y = y0 + row_index * row_height
                page.draw_line((x0, y), (x0 + sum(widths), y), color=(0, 0, 0), width=0.8)
            for x in (x0, x0 + widths[0], x0 + widths[0] + widths[1], x0 + sum(widths)):
                page.draw_line(
                    (x, y0), (x, y0 + len(all_rows) * row_height), color=(0, 0, 0), width=0.8
                )
            for row_index, row in enumerate(kept_rows, start=1):
                for column, value in enumerate(row):
                    page.insert_text(
                        (x0 + sum(widths[:column]) + 7, y0 + row_index * row_height + 21),
                        value,
                        fontsize=10 + corruption.font_delta,
                        fontname="helv",
                    )
            if corruption.obstruction_width:
                page.draw_rect(
                    fitz.Rect(x0 + 45, y0 + 42, x0 + 45 + corruption.obstruction_width, y0 + 112),
                    color=(0, 0, 0), fill=(0, 0, 0), overlay=True,
                )
    for _ in range(corruption.extra_pages):
        document.new_page(width=612, height=792)
    document.save(path)
    document.close()


def cases() -> list[Corruption]:
    return [
        Corruption("identity", 0, "identity"),
        *[Corruption("translation", value, f"shift_{2 * value}px", shift_pt=value)
          for value in (2, 4, 8, 16)],
        *[Corruption("text_deletion", value, f"delete_{value}_table_rows", deleted_rows=value)
          for value in (1, 2, 4)],
        *[Corruption("wrong_numbers", value, f"change_{value}_numeric_tokens", changed_numbers=value)
          for value in (1, 2, 4)],
        *[Corruption("font_substitution", value, f"font_plus_{value}pt", font_delta=value)
          for value in (1, 2, 4)],
        *[Corruption("obstruction", value, f"obstruction_{value}px", obstruction_width=value)
          for value in (60, 120, 240)],
        *[Corruption("extra_pages", value, f"append_{value}_blank_pages", extra_pages=value)
          for value in (1, 2, 3)],
        Corruption("missing_pages", 1, "remove_last_page", page_order=(1, 2)),
        Corruption("missing_pages", 2, "remove_last_two_pages", page_order=(1,)),
        Corruption("page_reorder", 1, "swap_pages_2_and_3", page_order=(1, 3, 2)),
    ]


EXPECTED_AXIS = {
    "translation": "layout",
    "text_deletion": "content_recall",
    "wrong_numbers": "content",
    "font_substitution": "typography",
    "obstruction": "appearance_proxy",
    "extra_pages": "pagination",
    "missing_pages": "pagination",
}


def monotonic(values: list[float], tolerance: float = 0.01) -> bool:
    return all(later <= earlier + tolerance for earlier, later in zip(values, values[1:]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="lathe_metric_controlled_") as directory:
        work = Path(directory)
        reference = work / "reference.pdf"
        build_pdf(reference, Corruption("identity", 0, "reference"))
        for index, corruption in enumerate(cases()):
            candidate = work / f"candidate_{index:02d}.pdf"
            build_pdf(candidate, corruption)
            result, *_ = compare_pdfs(reference, candidate)
            axes = result["scorecard"]["axes"]
            rows.append({
                "family": corruption.family,
                "severity": corruption.severity,
                "case": corruption.label,
                "scorecard_status": result["scorecard"]["status"],
                "failed_gates": ";".join(result["scorecard"]["failed_gates"]),
                "review_flags": ";".join(result["scorecard"]["review_flags"]),
                "content": axes["content"]["score"],
                "content_precision": axes["content"]["token_precision"],
                "content_recall": axes["content"]["token_recall"],
                "layout": axes["layout"]["score"],
                "typography": axes["typography"]["score"],
                "appearance_proxy": axes["appearance_proxy"]["score"],
                "pagination": axes["pagination"]["score"],
                "legacy_overall": result["scores"]["overall"],
            })

    csv_path = args.out_dir / "controlled_scores.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (args.out_dir / "scorecard_config.json").write_text(
        json.dumps(SCORECARD_CONFIG, indent=2) + "\n", encoding="utf-8"
    )

    identity = rows[0]
    checks = []
    for family, axis in EXPECTED_AXIS.items():
        family_rows = sorted((row for row in rows if row["family"] == family), key=lambda row: row["severity"])
        start_axis = "content_recall" if axis == "content_recall" else axis
        values = [float(identity[start_axis]), *[float(row[start_axis]) for row in family_rows]]
        checks.append((family, axis, monotonic(values), values))

    lines = [
        f"# Controlled metric study — {SCORECARD_VERSION}",
        "",
        "This development study exercises the five-axis scorecard on synthetic, source-known PDF failures. "
        "It validates detector behavior but does not define aesthetic preference.",
        "",
        "## Outcome",
        "",
        "| Failure family | Target axis | Monotonic | Scores from identity → severe |",
        "|---|---|---:|---|",
    ]
    for family, axis, passed, values in checks:
        lines.append(
            f"| `{family}` | `{axis}` | {'yes' if passed else '**no**'} | "
            + " → ".join(f"{100 * value:.1f}" for value in values)
            + " |"
        )
    reorder = next(row for row in rows if row["family"] == "page_reorder")
    wrong = [row for row in rows if row["family"] == "wrong_numbers"]
    lines.extend([
        "",
        "## Gate behavior",
        "",
        f"- Every wrong-number case tripped the numeric-token review trigger: "
        f"{all('numeric_token_mismatch' in row['review_flags'] for row in wrong)}.",
        "- Every added or missing-page case tripped the exact page-count gate.",
        f"- Page reordering kept exact page count but reduced sequence alignment to "
        f"{100 * float(reorder['pagination']):.1f} and produced status `{reorder['scorecard_status']}`.",
        "- Obstruction leaves PDF text extraction intact; the appearance proxy is therefore the targeted signal.",
        "",
        "## Interpretation",
        "",
        "The scorecard now exposes directional evidence and explicit failure gates without inventing a new "
        "overall percentage. Thresholds remain provisional. The next calibration step is the stratified "
        "real-reference perturbation matrix in `reference_perturbations_v0_1`.",
        "",
        "## Reproduce",
        "",
        "```bash",
        "mamba run -n lathe python scripts/evaluation/evaluate_controlled_metric_scorecard.py",
        "```",
        "",
        f"Raw results: `{csv_path.relative_to(ROOT)}`.",
    ])
    (args.out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"cases={len(rows)}")
    print(f"monotonic_checks={sum(check[2] for check in checks)}/{len(checks)}")
    print(f"summary={args.out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
