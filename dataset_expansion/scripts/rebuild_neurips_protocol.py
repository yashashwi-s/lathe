#!/usr/bin/env python3
"""Rebuild the stable PR #2 NeurIPS sources after upstream parquet re-sharding.

The exploratory builder selected papers positionally from the first two
parquet shards. Hugging Face later re-sharded the dataset, so stable source IDs
must be used to reproduce the accepted PR samples without silently replacing
them with different papers.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from pathlib import Path

import fsspec
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CORPUS, finalize_sample, write_manifest  # noqa: E402


NEURIPS = "hf://datasets/Mithilss/neurips-2025-arxiv-latex-sources/data/train-{i:05d}.parquet"
COLUMNS = [
    "arxiv_id", "relative_path", "extension", "file_size", "is_text",
    "text", "content",
]


def load_protocol(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle) if row["status"] == "accepted"]
    if not rows:
        raise SystemExit(f"no accepted rows in protocol manifest: {path}")
    return rows


def locate_sources(source_ids: set[str], shard_count: int) -> dict[str, int]:
    located: dict[str, int] = {}
    for index in range(shard_count):
        print(f"scan arxiv_id column: shard {index + 1}/{shard_count}", flush=True)
        with fsspec.open(NEURIPS.format(i=index)) as handle:
            values = set(
                pq.read_table(handle, columns=["arxiv_id"])
                .column("arxiv_id").to_pylist()
            )
        for source_id in source_ids & values:
            located[source_id] = index
    missing = sorted(source_ids - set(located))
    if missing:
        raise SystemExit(f"stable NeurIPS source IDs not found: {missing}")
    return located


def load_paper(source_id: str, shard: int) -> list[dict]:
    print(f"load {source_id} from shard {shard}", flush=True)
    with fsspec.open(NEURIPS.format(i=shard)) as handle:
        return pq.read_table(
            handle,
            columns=COLUMNS,
            filters=[("arxiv_id", "=", source_id)],
        ).to_pylist()


def main_tex(files: list[dict]) -> dict | None:
    texs = [row for row in files if row["extension"] == ".tex"]
    if len(texs) == 1:
        return texs[0]
    documents = [
        row for row in texs
        if row.get("text") and "\\documentclass" in row["text"][:4000]
    ]
    return documents[0] if len(documents) == 1 else None


def safe_relative(value: str) -> Path:
    relative = Path(re.sub(r"^\./", "", value or ""))
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"unsafe source path: {value!r}")
    return relative


def materialize(sample_dir: Path, files: list[dict], main: dict) -> Path:
    for row in files:
        relative = safe_relative(row["relative_path"])
        if not relative.parts or str(relative).endswith("/"):
            continue
        destination = sample_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if row["is_text"] and row["text"] is not None:
            destination.write_text(row["text"], encoding="utf-8", errors="replace")
        elif row["content"] is not None:
            destination.write_bytes(row["content"])
    source = sample_dir / safe_relative(main["relative_path"])
    if source.name != "main.tex":
        destination = source.parent / "main.tex"
        source.rename(destination)
        source = destination
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=CORPUS)
    parser.add_argument(
        "--protocol-manifest",
        type=Path,
        default=CORPUS / "neurips_paper" / "manifest.csv",
    )
    parser.add_argument("--shards", type=int, default=4)
    parser.add_argument("--max-pages", type=int, default=12)
    parser.add_argument("--max-chars", type=int, default=60_000)
    args = parser.parse_args()

    protocol = load_protocol(args.protocol_manifest.resolve())
    protocol_by_source = {row["source_id"]: row["sample_id"] for row in protocol}
    located = locate_sources(set(protocol_by_source), args.shards)
    set_dir = args.corpus.resolve() / "neurips_paper"
    if set_dir.exists():
        scan_manifest = set_dir / "manifest.csv"
        if scan_manifest.exists():
            shutil.copy2(
                scan_manifest,
                args.corpus.resolve() / "neurips_reshard_scan_manifest.csv",
            )
        shutil.rmtree(set_dir)
    records = []
    for source_id, sample_id in protocol_by_source.items():
        files = load_paper(source_id, located[source_id])
        main = main_tex(files)
        if main is None or not main.get("text"):
            raise SystemExit(f"{source_id}: no unique main TeX source")
        if len(main["text"]) > args.max_chars:
            raise SystemExit(f"{source_id}: main TeX exceeds {args.max_chars} characters")
        sample_dir = set_dir / sample_id
        sample_dir.mkdir(parents=True, exist_ok=True)
        main_path = materialize(sample_dir, files, main)
        if main_path.parent != sample_dir:
            raise SystemExit(f"{source_id}: main.tex is unexpectedly nested at {main_path}")
        record = finalize_sample(
            sample_dir,
            "Mithilss/neurips-2025-arxiv-latex-sources",
            source_id,
            max_pages=args.max_pages,
            timeout=240,
        )
        record["sample_id"] = sample_id
        if record["status"] != "accepted":
            raise SystemExit(f"{sample_id}/{source_id}: {record['reason']}")
        records.append(record)
        print(f"accepted {sample_id} <- {source_id} ({record['page_count']}p)", flush=True)
    write_manifest(records, set_dir / "manifest.csv")


if __name__ == "__main__":
    main()
