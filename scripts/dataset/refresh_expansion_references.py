#!/usr/bin/env python3
"""Recompile selected expansion references and refresh canonical metadata.

This is intentionally limited to sample IDs already frozen in
``splits/expansion_32.csv``. It compiles the maintained source under
``dataset_expansion/corpus``, mirrors the generated reference artifacts into
the canonical corpus, and regenerates manifests, the expansion split, and the
canonical preview without touching any source in the original 157 samples.

Run with:
  mamba run -n lathe python scripts/dataset/refresh_expansion_references.py \
    --sample-id i2s_table_002 --sample-id pubmed_table_002
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "data" / "latex_benchmark_v0"
EXPANSION = ROOT / "dataset_expansion" / "corpus"
EXPANSION_SCRIPTS = ROOT / "dataset_expansion" / "scripts"

sys.path.insert(0, str(EXPANSION_SCRIPTS))
from common import finalize_sample, write_manifest  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_merge_module():
    path = Path(__file__).with_name("merge_expansion_into_v0.py")
    spec = importlib.util.spec_from_file_location("merge_expansion_into_v0", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sample-id",
        action="append",
        required=True,
        help="expansion sample to refresh; repeat for multiple samples",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requested = list(dict.fromkeys(args.sample_id))
    split_rows = read_csv(DATASET / "splits" / "expansion_32.csv")
    split_by_id = {row["sample_id"]: row for row in split_rows}
    outside = [sample_id for sample_id in requested if sample_id not in split_by_id]
    if outside:
        raise SystemExit(f"not in expansion_32.csv: {outside}")

    refreshed: dict[str, dict] = {}
    manifests: dict[str, list[dict[str, str]]] = {}
    for sample_id in requested:
        split_row = split_by_id[sample_id]
        category = split_row["category"]
        manifest_path = EXPANSION / category / "manifest.csv"
        rows = manifests.setdefault(category, read_csv(manifest_path))
        matches = [row for row in rows if row["sample_id"] == sample_id]
        if len(matches) != 1:
            raise SystemExit(
                f"{sample_id}: expected one expansion manifest row, found {len(matches)}"
            )
        manifest_row = matches[0]
        expansion_dir = EXPANSION / category / sample_id
        canonical_dir = DATASET / "corpus" / category / sample_id
        if (expansion_dir / "main.tex").read_bytes() != (
            canonical_dir / "main.tex"
        ).read_bytes():
            raise SystemExit(f"{sample_id}: expansion and canonical sources differ")

        record = finalize_sample(
            expansion_dir,
            manifest_row["source_dataset"],
            manifest_row["source_id"],
            max_pages=12,
        )
        if record["status"] != "accepted":
            raise SystemExit(f"{sample_id}: refresh failed: {record['reason']}")
        for name in ("reference.pdf", "compile.log", "provenance.json"):
            shutil.copy2(expansion_dir / name, canonical_dir / name)
        for field in (
            "status", "reason", "page_count", "compile_seconds", "source_chars"
        ):
            manifest_row[field] = record[field]
        refreshed[sample_id] = record

    for category, rows in manifests.items():
        write_manifest(rows, EXPANSION / category / "manifest.csv")

    merge = load_merge_module()
    current_accepted = read_csv(DATASET / "manifests" / "accepted.csv")
    expansion_rows = []
    for row in current_accepted:
        if row["category"] not in merge.EXPECTED_COUNTS:
            continue
        refreshed_row = refreshed.get(row["sample_id"])
        expansion_rows.append(
            {
                "set": row["category"],
                "sample_id": row["sample_id"],
                "source_dataset": row["source_dataset"],
                "source_id": row["source_ids"],
                "compile_seconds": (
                    refreshed_row["compile_seconds"]
                    if refreshed_row is not None
                    else row["compile_seconds"]
                ),
            }
        )
    if len(expansion_rows) != 32:
        raise SystemExit(f"expected 32 canonical expansion rows, found {len(expansion_rows)}")
    accepted = merge.write_manifests(DATASET, expansion_rows, expected_base_count=157)
    split = merge.write_expansion_split(DATASET, accepted)
    preview = merge.build_preview(DATASET, accepted)
    print(
        json.dumps(
            {
                "refreshed": requested,
                "canonical_accepted": len(accepted),
                "expansion_split": merge.relative_to_root(split),
                "preview": merge.relative_to_root(preview),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
