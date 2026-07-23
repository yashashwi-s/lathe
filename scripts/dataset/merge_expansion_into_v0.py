#!/usr/bin/env python3
"""Merge the accepted dataset-expansion PR samples into the canonical corpus.

The expansion builders should first be rerun into a staging corpus. This tool
validates the seven expected sets, copies each complete accepted source tree,
updates the canonical manifests, writes the dedicated expansion split, and
regenerates the one-sample-per-page preview.

Run with:
  mamba run -n lathe python scripts/dataset/merge_expansion_into_v0.py \
    --expansion-corpus /tmp/lathe_dataset_expansion_rerun/corpus
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATASET = ROOT / "data" / "latex_benchmark_v0"
DEFAULT_EXPANSION = ROOT / "dataset_expansion" / "corpus"
EXPECTED_COUNTS = {
    "i2s_equation": 5,
    "i2s_table": 5,
    "i2s_algorithm": 5,
    "i2s_plot": 5,
    "pubmed_table": 5,
    "arxiv5t_paper": 5,
    "neurips_paper": 2,
}
MANIFEST_FIELDS = [
    "sample_id",
    "category",
    "source_family",
    "source_dataset",
    "source_ids",
    "status",
    "reason",
    "page_count",
    "compile_seconds",
    "nonblank_lines",
    "source_chars",
    "sha256_source",
    "sha256_pdf",
    "sample_dir",
]
SPLIT_FIELDS = [
    "sample_id",
    "category",
    "complexity_band",
    "complexity_score",
    "page_count",
    "source_chars",
    "nonblank_lines",
    "structural_constructs",
    "deterministic_engine_failures",
    "source_family",
    "source_dataset",
    "source_ids",
    "source_path",
    "reference_pdf",
    "selection_basis",
]
PROTOCOL_GENERATED_FILES = {"reference.pdf", "provenance.json", "compile.log"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_to_root(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def validate_protocol_source_tree(
    current: Path, protocol: Path, identity: str
) -> None:
    """Require every source artifact frozen in PR #2 to remain byte-identical.

    Fresh builders may retain additional upstream files, and reference PDFs are
    expected to be freshly compiled. Neither condition weakens the stable
    protocol identity of the source tree accepted by the PR.
    """
    for protocol_path in protocol.rglob("*"):
        if not protocol_path.is_file():
            continue
        relative = protocol_path.relative_to(protocol)
        if relative.name in PROTOCOL_GENERATED_FILES:
            continue
        current_path = current / relative
        if not current_path.is_file():
            raise SystemExit(f"{identity}: rerun is missing PR #2 source {relative}")
        if sha256_file(current_path) != sha256_file(protocol_path):
            raise SystemExit(f"{identity}: rerun source differs from PR #2: {relative}")


def load_expansion_rows(corpus: Path) -> list[dict[str, str]]:
    accepted: list[dict[str, str]] = []
    observed: dict[str, int] = {}
    for set_name, expected in EXPECTED_COUNTS.items():
        set_dir = corpus / set_name
        manifest = set_dir / "manifest.csv"
        if not manifest.exists():
            raise SystemExit(f"missing expansion manifest: {manifest}")
        rows = [row for row in read_csv(manifest) if row["status"] == "accepted"]
        observed[set_name] = len(rows)
        if len(rows) != expected:
            raise SystemExit(
                f"{set_name}: expected {expected} accepted samples from PR #2, "
                f"found {len(rows)}"
            )
        for row in rows:
            sample_dir = set_dir / row["sample_id"]
            required = [
                sample_dir / name
                for name in (
                    "main.tex", "reference.pdf", "compile.log", "provenance.json"
                )
            ]
            missing = [str(path) for path in required if not path.exists()]
            if missing:
                raise SystemExit(f"{row['sample_id']}: missing required files: {missing}")
            with fitz.open(sample_dir / "reference.pdf") as document:
                pages = document.page_count
            if pages != int(row["page_count"]):
                raise SystemExit(
                    f"{row['sample_id']}: manifest says {row['page_count']} pages, PDF has {pages}"
                )
            row = dict(row)
            row["source_dir"] = str(sample_dir)
            row["rerun_sample_id"] = row["sample_id"]
            accepted.append(row)
        protocol_manifest = DEFAULT_EXPANSION / set_name / "manifest.csv"
        if corpus.resolve() != DEFAULT_EXPANSION.resolve() and protocol_manifest.exists():
            protocol_rows = [
                row for row in read_csv(protocol_manifest)
                if row["status"] == "accepted"
            ]
            if set_name == "neurips_paper":
                source_ids = {row["source_id"] for row in rows}
                protocol_by_source = {
                    row["source_id"]: row["sample_id"] for row in protocol_rows
                }
                if source_ids != set(protocol_by_source):
                    raise SystemExit(
                        f"{set_name}: rerun source selection differs from PR #2; "
                        f"rerun={sorted(source_ids)}, protocol={sorted(protocol_by_source)}"
                    )
                current_by_source = {row["source_id"]: row for row in rows}
                for source_id, protocol_sample_id in protocol_by_source.items():
                    current_source = set_dir / current_by_source[source_id]["sample_id"]
                    protocol_source = DEFAULT_EXPANSION / set_name / protocol_sample_id
                    validate_protocol_source_tree(
                        current_source, protocol_source, f"{set_name}/{source_id}"
                    )
                # HF row ordering may move as a dataset is updated. Source IDs
                # are the stable identity; restore the PR sample IDs.
                for row in accepted:
                    if row["set"] == set_name:
                        row["sample_id"] = protocol_by_source[row["source_id"]]
            else:
                identity = [(row["sample_id"], row["source_id"]) for row in rows]
                protocol_identity = [
                    (row["sample_id"], row["source_id"]) for row in protocol_rows
                ]
                if identity != protocol_identity:
                    raise SystemExit(
                        f"{set_name}: rerun identity differs from PR #2; "
                        f"rerun={identity}, protocol={protocol_identity}"
                    )
                for row in rows:
                    current_source = set_dir / row["sample_id"]
                    protocol_source = DEFAULT_EXPANSION / set_name / row["sample_id"]
                    validate_protocol_source_tree(
                        current_source,
                        protocol_source,
                        f"{set_name}/{row['sample_id']}",
                    )
    print("validated expansion counts:", json.dumps(observed, sort_keys=True))
    return accepted


def transient_build_file(_directory: str, names: list[str]) -> set[str]:
    ignored = set()
    for name in names:
        if name in {"main.aux", "main.log", "main.out", "main.blg", "main.synctex.gz"}:
            ignored.add(name)
    return ignored


def install_source_trees(dataset: Path, expansion_rows: list[dict[str, str]]) -> None:
    corpus = dataset / "corpus"
    staging = corpus / ".expansion_merge_staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    by_category: dict[str, list[dict[str, str]]] = {}
    for row in expansion_rows:
        by_category.setdefault(row["set"], []).append(row)
    try:
        for category, rows in by_category.items():
            category_stage = staging / category
            category_stage.mkdir()
            for row in rows:
                source = Path(row["source_dir"])
                destination = category_stage / row["sample_id"]
                shutil.copytree(source, destination, ignore=transient_build_file)
                provenance_path = destination / "provenance.json"
                provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
                provenance["sample_id"] = row["sample_id"]
                if row["rerun_sample_id"] != row["sample_id"]:
                    provenance["rerun_selection_id"] = row["rerun_sample_id"]
                    provenance["stable_protocol_id"] = row["sample_id"]
                provenance_path.write_text(
                    json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
                )
        for category in by_category:
            destination = corpus / category
            if destination.exists():
                shutil.rmtree(destination)
            (staging / category).rename(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def validate_base(dataset: Path, expected_base_count: int) -> None:
    rows = read_csv(dataset / "manifests" / "all.csv")
    expansion_categories = set(EXPECTED_COUNTS)
    base_accepted = [
        row for row in rows
        if row["category"] not in expansion_categories and row["status"] == "accepted"
    ]
    if len(base_accepted) != expected_base_count:
        raise SystemExit(
            f"expected {expected_base_count} base accepted samples, found {len(base_accepted)}"
        )


def canonical_record(dataset: Path, row: dict[str, str]) -> dict[str, str | int]:
    sample_dir = dataset / "corpus" / row["set"] / row["sample_id"]
    source = sample_dir / "main.tex"
    reference = sample_dir / "reference.pdf"
    text = source.read_text(encoding="utf-8", errors="replace")
    with fitz.open(reference) as document:
        pages = document.page_count
    return {
        "sample_id": row["sample_id"],
        "category": row["set"],
        "source_family": "hf_dataset_expansion",
        "source_dataset": row["source_dataset"],
        "source_ids": row["source_id"],
        "status": "accepted",
        "reason": "accepted",
        "page_count": pages,
        "compile_seconds": row["compile_seconds"],
        "nonblank_lines": sum(bool(line.strip()) for line in text.splitlines()),
        "source_chars": len(text),
        "sha256_source": sha256_file(source),
        "sha256_pdf": sha256_file(reference),
        "sample_dir": relative_to_root(sample_dir),
    }


def write_manifests(dataset: Path, expansion_rows: list[dict[str, str]],
                    expected_base_count: int) -> list[dict]:
    all_path = dataset / "manifests" / "all.csv"
    old_rows = read_csv(all_path)
    expansion_categories = set(EXPECTED_COUNTS)
    base_rows = [row for row in old_rows if row["category"] not in expansion_categories]
    base_accepted = [row for row in base_rows if row["status"] == "accepted"]
    if len(base_accepted) != expected_base_count:
        raise SystemExit(
            f"expected {expected_base_count} base accepted samples, found {len(base_accepted)}"
        )
    new_rows = [canonical_record(dataset, row) for row in expansion_rows]
    sample_ids = [row["sample_id"] for row in base_rows] + [row["sample_id"] for row in new_rows]
    duplicates = sorted(sample for sample, count in Counter(sample_ids).items() if count > 1)
    if duplicates:
        raise SystemExit(f"sample ID collision(s): {duplicates}")
    combined = base_rows + new_rows
    accepted = [row for row in combined if row["status"] == "accepted"]
    rejected = [row for row in combined if row["status"] != "accepted"]
    write_csv(dataset / "manifests" / "all.csv", combined, MANIFEST_FIELDS)
    write_csv(dataset / "manifests" / "accepted.csv", accepted, MANIFEST_FIELDS)
    write_csv(dataset / "manifests" / "rejected.csv", rejected, MANIFEST_FIELDS)
    write_csv(dataset / "accepted_manifest.csv", accepted, MANIFEST_FIELDS)
    write_csv(dataset / "compile_results.csv", combined, MANIFEST_FIELDS)
    return accepted


def write_expansion_split(dataset: Path, accepted: list[dict]) -> Path:
    rows = []
    for row in accepted:
        if row["category"] not in EXPECTED_COUNTS:
            continue
        sample_dir = Path(row["sample_dir"])
        rows.append({
            "sample_id": row["sample_id"],
            "category": row["category"],
            "complexity_band": "expansion",
            "complexity_score": "",
            "page_count": row["page_count"],
            "source_chars": row["source_chars"],
            "nonblank_lines": row["nonblank_lines"],
            "structural_constructs": "",
            "deterministic_engine_failures": "",
            "source_family": row["source_family"],
            "source_dataset": row["source_dataset"],
            "source_ids": row["source_ids"],
            "source_path": str(sample_dir / "main.tex"),
            "reference_pdf": str(sample_dir / "reference.pdf"),
            "selection_basis": (
                "accepted dataset_expansion PR sample; excluded from the historical "
                "30-document prompt-development and 127-document held-out claims"
            ),
        })
    path = dataset / "splits" / "expansion_32.csv"
    write_csv(path, rows, SPLIT_FIELDS)
    return path


def draw_pdf_tiled(page: fitz.Page, source_path: Path, rect: fitz.Rect) -> None:
    source = fitz.open(source_path)
    try:
        count = source.page_count
        columns = math.ceil(math.sqrt(count))
        rows = math.ceil(count / columns)
        gap = 5
        cell_w = (rect.width - gap * (columns - 1)) / columns
        cell_h = (rect.height - gap * (rows - 1)) / rows
        for index in range(count):
            row, column = divmod(index, columns)
            cell = fitz.Rect(
                rect.x0 + column * (cell_w + gap),
                rect.y0 + row * (cell_h + gap),
                rect.x0 + column * (cell_w + gap) + cell_w,
                rect.y0 + row * (cell_h + gap) + cell_h,
            )
            source_page = source.load_page(index)
            scale = min(cell.width / source_page.rect.width, cell.height / source_page.rect.height)
            width, height = source_page.rect.width * scale, source_page.rect.height * scale
            target = fitz.Rect(
                cell.x0 + (cell.width - width) / 2,
                cell.y0 + (cell.height - height) / 2,
                cell.x0 + (cell.width + width) / 2,
                cell.y0 + (cell.height + height) / 2,
            )
            page.show_pdf_page(target, source, index)
            page.draw_rect(target, color=(0.65, 0.65, 0.65), width=0.4)
    finally:
        source.close()


def build_preview(dataset: Path, accepted: list[dict]) -> Path:
    output = dataset / "previews" / "latex_benchmark_v0_preview.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    document = fitz.open()
    for row in accepted:
        page = document.new_page(width=842, height=595)
        page.insert_text((36, 30), f"{row['sample_id']} | {row['category']}", fontsize=12)
        page.insert_text(
            (36, 48),
            f"{row['source_dataset']} | {row['page_count']} reference page(s)",
            fontsize=7,
        )
        page.draw_line((36, 58), (806, 58), color=(0.7, 0.7, 0.7), width=0.5)
        reference = ROOT / row["sample_dir"] / "reference.pdf"
        draw_pdf_tiled(page, reference, fitz.Rect(36, 70, 806, 570))
    document.save(output, garbage=3, deflate=True)
    document.close()
    optimize_preview(output, len(accepted))
    return output


def optimize_preview(output: Path, expected_pages: int) -> None:
    """Downsample the review-only preview without touching reference PDFs."""
    ghostscript = shutil.which("gs")
    if not ghostscript:
        print("preview optimization skipped: Ghostscript not found")
        return
    optimized = output.with_name(f".{output.stem}.optimized.pdf")
    command = [
        ghostscript,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.7",
        "-dPDFSETTINGS=/ebook",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={optimized}",
        str(output),
    ]
    try:
        completed = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        if completed.returncode != 0 or not optimized.exists():
            print("preview optimization skipped: Ghostscript failed")
            return
        with fitz.open(optimized) as document:
            if document.page_count != expected_pages:
                print("preview optimization skipped: page-count validation failed")
                return
        if optimized.stat().st_size >= output.stat().st_size:
            print("preview optimization skipped: no size reduction")
            return
        optimized.replace(output)
        print(f"optimized preview size: {output.stat().st_size} bytes")
    finally:
        if optimized.exists():
            optimized.unlink()


def write_import_record(dataset: Path, accepted_count: int) -> Path:
    path = dataset / "expansion_import.json"
    path.write_text(json.dumps({
        "imported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_accepted_samples": 157,
        "expansion_accepted_samples": sum(EXPECTED_COUNTS.values()),
        "canonical_accepted_samples": accepted_count,
        "source_experiment": "dataset_expansion",
        "source_pr": 2,
        "reference_protocols": {
            "base_157": "pdfLaTeX",
            "expansion_32": "Tectonic 0.16.9",
        },
        "expansion_builder_parameters": {
            "snippet_samples_per_set": 5,
            "full_document_target_per_set": 5,
            "max_reference_pages": 12,
            "max_main_tex_chars": 60000,
            "arxiv5t_scan": 400,
            "neurips_shards": 2,
        },
        "accepted_by_set": EXPECTED_COUNTS,
        "historical_splits_unchanged": [
            "splits/prompt_dev_33.csv",
            "splits/heldout_clean_127.csv",
        ],
        "new_split": "splits/expansion_32.csv",
    }, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument(
        "--expansion-corpus",
        type=Path,
        required=True,
        help="fresh staging corpus produced by the expansion rebuild commands",
    )
    parser.add_argument("--expected-base-count", type=int, default=157)
    args = parser.parse_args()
    dataset = args.dataset.resolve()
    expansion_corpus = args.expansion_corpus.resolve()
    expansion_rows = load_expansion_rows(expansion_corpus)
    validate_base(dataset, args.expected_base_count)
    install_source_trees(dataset, expansion_rows)
    accepted = write_manifests(dataset, expansion_rows, args.expected_base_count)
    split = write_expansion_split(dataset, accepted)
    preview = build_preview(dataset, accepted)
    import_record = write_import_record(dataset, len(accepted))
    rerun_scan = expansion_corpus / "neurips_reshard_scan_manifest.csv"
    if rerun_scan.exists():
        shutil.copy2(rerun_scan, dataset / "expansion_rerun_neurips_scan.csv")
    print(f"accepted corpus: {len(accepted)}")
    print(f"expansion split: {relative_to_root(split)}")
    print(f"preview: {relative_to_root(preview)}")
    print(f"import record: {relative_to_root(import_record)}")


if __name__ == "__main__":
    main()
