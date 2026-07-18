#!/usr/bin/env python3
"""Add final strict/compatibility and critical text fields to a pre-freeze v2 table."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

import pdf_metric_axes_v1 as v1  # noqa: E402
import pdf_metric_axes_v2 as v2  # noqa: E402


ADDED_FIELDS = (
    "strict_word_f1",
    "strict_document_edit_similarity",
    "compatibility_word_f1",
    "compatibility_document_edit_similarity",
    "reference_number_count",
    "candidate_number_count",
    "reference_operator_count",
    "candidate_operator_count",
    "reference_citation_count",
    "candidate_citation_count",
)


def _strict_text(extraction: v1.PdfExtraction) -> str:
    value = "\n\f\n".join(page.text for page in extraction.pages).replace("\u00ad", "")
    value = unicodedata.normalize("NFC", value)
    return re.sub(r"\s+", " ", value).strip()


def _enrich(row: dict[str, str]) -> dict[str, str]:
    reference = v1.extract_pdf(row.get("reference_pdf_resolved") or row.get("source_pdf") or row["reference_pdf"])
    candidate = v1.extract_pdf(row.get("candidate_pdf_resolved") or row["candidate_pdf"])
    left = _strict_text(reference)
    right = _strict_text(candidate)
    strict_inventory = v2._inventory(left.split(), right.split())
    critical = v2._critical_content_axis(reference, candidate)["metrics"]
    output = dict(row)
    output["strict_word_f1"] = strict_inventory["f1"]
    output["strict_document_edit_similarity"] = v1._normalized_edit_similarity(left, right)
    output["compatibility_word_f1"] = row.get("word_f1", row.get("compatibility_word_f1", ""))
    output["compatibility_document_edit_similarity"] = row.get(
        "document_edit_similarity", row.get("compatibility_document_edit_similarity", "")
    )
    for name in ("number", "operator", "citation"):
        inventory = critical[f"{name}s" if name != "citation" else "citation_markers"]
        output[f"{name}_f1"] = inventory["f1"]
        output[f"{name}_exact"] = inventory["exact_match"]
        output[f"reference_{name}_count"] = inventory["reference_count"]
        output[f"candidate_{name}_count"] = inventory["candidate_count"]
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    with args.scores.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        enriched = list(executor.map(_enrich, rows, chunksize=1))
    output_fields = [field for field in fields if field not in ADDED_FIELDS]
    insert_at = output_fields.index("number_f1") if "number_f1" in output_fields else len(output_fields)
    for field in reversed(ADDED_FIELDS):
        output_fields.insert(insert_at, field)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(enriched)
    print(f"enriched {len(enriched)} rows -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
