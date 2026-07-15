#!/usr/bin/env python3
"""Build real full-document sample sets (the structural-difficulty jump).

Sets produced (corpus/<set>/<sample_id>/):
  arxiv5t_paper   TIGER-Lab/arxiv-latex-5T — whole paper directories
                  (main.tex + real figure assets), month 2401.
  neurips_paper   Mithilss/neurips-2025-arxiv-latex-sources — papers whose
                  source is dominated by a single .tex file, small enough to
                  fit a 1-turn prompt; assets downloaded alongside.

Selection: prefer papers whose reference render is <= --max-pages (default 8)
and whose main .tex is <= --max-chars (default 60k, ~15k tokens) so a 1-turn
run is feasible. Compiled with tectonic; rejects dropped.

Run: ~/mamba/envs/lathe/bin/python scripts/build_fulldoc_sets.py
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

import fsspec
import pyarrow.parquet as pq
from huggingface_hub import HfApi, hf_hub_download

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CORPUS, finalize_sample, write_manifest

ARXIV5T = "TIGER-Lab/arxiv-latex-5T"
NEURIPS = "hf://datasets/Mithilss/neurips-2025-arxiv-latex-sources/data/train-{i:05d}.parquet"

ASSET_EXT = {".png", ".jpg", ".jpeg", ".pdf", ".eps", ".bst", ".cls", ".sty",
             ".bib", ".bbl", ".tex", ".txt"}


def find_main_tex(sdir: Path) -> Path | None:
    texs = sorted(sdir.rglob("*.tex"))
    docs = [t for t in texs
            if "\\documentclass" in t.read_text(errors="replace")[:6000]]
    if len(docs) == 1:
        return docs[0]
    named = [t for t in docs if t.name.lower() in ("main.tex", "paper.tex", "ms.tex")]
    return named[0] if named else None


def build_arxiv5t(n: int, max_pages: int, max_chars: int, scan: int) -> list[dict]:
    """Papers in 2401/ are stored as <id>.gz — gzipped tar (or single tex)."""
    import gzip
    import tarfile

    api = HfApi()
    set_dir = CORPUS / "arxiv5t_paper"
    if set_dir.exists():
        shutil.rmtree(set_dir)
    entries = api.list_repo_tree(ARXIV5T, repo_type="dataset",
                                 path_in_repo="2401", recursive=False)
    blobs = [e.path for e in entries if e.path.endswith(".gz")][:scan]
    records, accepted, idx = [], 0, 0
    for blob in blobs:
        if accepted >= n:
            break
        idx += 1
        sid = f"arxiv5t_paper_{idx:03d}"
        sdir = set_dir / sid
        sdir.mkdir(parents=True, exist_ok=True)
        try:
            local = Path(hf_hub_download(ARXIV5T, blob, repo_type="dataset"))
        except Exception as exc:
            print(f"skip {blob}: download failed ({exc})")
            shutil.rmtree(sdir, ignore_errors=True)
            continue
        try:
            with tarfile.open(local, "r:gz") as tar:
                tar.extractall(sdir, filter="data")
        except tarfile.ReadError:
            # single gzipped .tex file
            try:
                (sdir / "main.tex").write_bytes(gzip.decompress(local.read_bytes()))
            except Exception:
                shutil.rmtree(sdir, ignore_errors=True)
                print(f"skip {blob}: not tar.gz or gz-tex")
                continue
        main = find_main_tex(sdir)
        if main is None:
            shutil.rmtree(sdir, ignore_errors=True)
            print(f"skip {blob}: no main tex")
            continue
        tex = main.read_text(errors="replace")
        if len(tex) > max_chars:
            shutil.rmtree(sdir, ignore_errors=True)
            print(f"skip {blob}: main tex {len(tex)} chars > {max_chars}")
            continue
        if main.name != "main.tex":
            main = main.rename(main.parent / "main.tex")
        rec = finalize_sample(main.parent, ARXIV5T, blob,
                              max_pages=max_pages, timeout=240)
        rec["sample_id"] = sid
        records.append(rec)
        if rec["status"] == "accepted":
            accepted += 1
            print(f"accepted {sid} <- {blob} ({rec['page_count']}p)")
        else:
            shutil.rmtree(sdir, ignore_errors=True)
            print(f"rejected {sid} <- {blob}: {rec['reason']}")
    write_manifest(records, set_dir / "manifest.csv")
    return records


def build_neurips(n: int, max_pages: int, max_chars: int, shards: int) -> list[dict]:
    set_dir = CORPUS / "neurips_paper"
    if set_dir.exists():
        shutil.rmtree(set_dir)
    papers: dict[str, list[dict]] = defaultdict(list)
    for i in range(shards):
        with fsspec.open(NEURIPS.format(i=i)) as f:
            rows = pq.read_table(f, columns=["arxiv_id", "relative_path", "extension",
                                             "file_size", "is_text", "text", "content"]).to_pylist()
        for r in rows:
            papers[r["arxiv_id"]].append(r)
    records, accepted, idx = [], 0, 0
    # Prefer papers with exactly one .tex and modest total size.
    def main_tex(files):
        texs = [f for f in files if f["extension"] == ".tex"]
        if len(texs) != 1:
            docs = [f for f in texs if f["text"] and "\\documentclass" in f["text"][:4000]]
            return docs[0] if len(docs) == 1 else None
        return texs[0]

    cands = []
    for aid, files in papers.items():
        mt = main_tex(files)
        if mt is None or not mt["text"]:
            continue
        if not (5000 < len(mt["text"]) <= max_chars):
            continue
        if sum(f["file_size"] or 0 for f in files) > 20_000_000 or len(files) > 40:
            continue
        cands.append((aid, files, mt))
    cands.sort(key=lambda c: len(c[2]["text"]))
    for aid, files, mt in cands:
        if accepted >= n:
            break
        idx += 1
        sid = f"neurips_paper_{idx:03d}"
        sdir = set_dir / sid
        sdir.mkdir(parents=True, exist_ok=True)
        for f in files:
            rel = re.sub(r"^\./", "", f["relative_path"] or "")
            if not rel or rel.endswith("/"):
                continue
            dst = sdir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if f["is_text"] and f["text"] is not None:
                dst.write_text(f["text"], encoding="utf-8", errors="replace")
            elif f["content"] is not None:
                dst.write_bytes(f["content"])
        main = sdir / re.sub(r"^\./", "", mt["relative_path"])
        if main.name != "main.tex":
            main.rename(main.parent / "main.tex")
            main = main.parent / "main.tex"
        # compile from the dir containing main.tex
        rec = finalize_sample(main.parent, "Mithilss/neurips-2025-arxiv-latex-sources",
                              aid, max_pages=max_pages, timeout=240)
        rec["sample_id"] = sid
        records.append(rec)
        if rec["status"] == "accepted":
            accepted += 1
            print(f"accepted {sid} <- {aid} ({rec['page_count']}p)")
        else:
            shutil.rmtree(sdir, ignore_errors=True)
            print(f"rejected {sid} <- {aid}: {rec['reason']}")
    write_manifest(records, set_dir / "manifest.csv")
    return records


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--max-pages", type=int, default=8)
    ap.add_argument("--max-chars", type=int, default=60_000)
    ap.add_argument("--scan", type=int, default=400)
    ap.add_argument("--neurips-shards", type=int, default=2)
    ap.add_argument("--only", choices=["arxiv5t", "neurips"])
    args = ap.parse_args()
    if args.only in (None, "arxiv5t"):
        build_arxiv5t(args.n, args.max_pages, args.max_chars, args.scan)
    if args.only in (None, "neurips"):
        build_neurips(args.n, args.max_pages, args.max_chars, args.neurips_shards)


if __name__ == "__main__":
    main()
