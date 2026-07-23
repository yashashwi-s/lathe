#!/usr/bin/env python3
"""Build snippet-wrapped sample sets from HF datasets.

Sets produced (corpus/<set>/<sample_id>/):
  i2s_equation   stanford-crfm/image2struct-latex-v1 equation (hard/medium first)
  i2s_table      ... table
  i2s_algorithm  ... algorithm
  i2s_plot       ... plot (TikZ/pgfplots stress cases)
  pubmed_table   deepcopy/pubmed-tables-latex-768px (messy medical tables)

Each snippet is wrapped in the same minimal-article template family the lathe
builders use, then compiled with tectonic; rejects are dropped.

Run: ~/mamba/envs/lathe/bin/python scripts/build_snippet_sets.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import fsspec
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CORPUS, finalize_sample, write_manifest

I2S = "hf://datasets/stanford-crfm/image2struct-latex-v1/{cfg}/validation-00000-of-00001.parquet"
PUBMED = "hf://datasets/deepcopy/pubmed-tables-latex-768px/data/train-00000-of-00024.parquet"

PREAMBLE_BASE = r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts,mathtools}
\usepackage{booktabs,multirow,array,tabularx}
\usepackage{graphicx}
"""

PREAMBLE_ALGO = PREAMBLE_BASE + "\\usepackage{algorithm}\n\\usepackage{algpseudocode}\n"
PREAMBLE_PLOT = PREAMBLE_BASE + "\\usepackage{tikz}\n\\usepackage{pgfplots}\n\\pgfplotsset{compat=1.17}\n"

BODY = r"""\title{%(title)s}
\author{Dataset-expansion sample}
\date{}
\begin{document}
\maketitle
\section{%(section)s}
%(intro)s

%(payload)s

\end{document}
"""


def wrap(preamble: str, title: str, section: str, intro: str, payload: str) -> str:
    return preamble + BODY % {"title": title, "section": section,
                              "intro": intro, "payload": payload}


def fit_tabular(
    payload: str, width: str, height: str, *, total_height: bool = False
) -> str:
    """Scale one source table as a unit so no source-backed cells are clipped."""
    begin = payload.find("\\begin{tabular}")
    end_marker = "\\end{tabular}"
    end = payload.rfind(end_marker)
    if begin < 0 or end < begin:
        raise ValueError("table-fit repair requires one tabular environment")
    end += len(end_marker)
    command = "\\resizebox*" if total_height else "\\resizebox"
    fitted = (
        f"{command}{{{width}}}{{{height}}}{{%\n"
        + payload[begin:end]
        + "}%\n"
    )
    return payload[:begin] + fitted + payload[end:]


I2S_HEIGHT_REPAIRS = {"2402.14942.tar.gz"}
PUBMED_WIDTH_REPAIRS = {
    "PMC2936360_table_3",
    "PMC4469303_table_6",
    "PMC3395126_table_0",
    "PMC4378895_table_2",
}


def load_i2s(cfg: str, columns=("text", "difficulty", "length", "instance_name")) -> list[dict]:
    with fsspec.open(I2S.format(cfg=cfg)) as f:
        return pq.read_table(f, columns=list(columns)).to_pylist()


BAD = ("\\includegraphics", "\\input{", "\\write18", "\\href", "\\cite")


def pick(rows: list[dict], n: int, min_len: int, max_len: int,
         extra_bad: tuple = ()) -> list[dict]:
    order = {"hard": 0, "medium": 1, "easy": 2}
    rows = [r for r in rows if r.get("text")]
    rows.sort(key=lambda r: (order.get(r.get("difficulty", ""), 3), -len(r["text"])))
    out, seen = [], set()
    for r in rows:
        t = r["text"].strip()
        if not (min_len <= len(t) <= max_len) or t in seen:
            continue
        if any(b in t for b in BAD + extra_bad):
            continue
        seen.add(t)
        out.append(r)
        if len(out) >= n * 3:  # keep spares for compile rejects
            break
    return out


def build_set(corpus: Path, set_name: str, candidates: list[dict], make_tex,
              n: int, dataset: str, max_pages: int = 4) -> list[dict]:
    set_dir = corpus / set_name
    if set_dir.exists():
        shutil.rmtree(set_dir)
    records, accepted = [], 0
    for i, row in enumerate(candidates, 1):
        if accepted >= n:
            break
        sid = f"{set_name}_{i:03d}"
        sdir = set_dir / sid
        sdir.mkdir(parents=True, exist_ok=True)
        (sdir / "main.tex").write_text(make_tex(row, i), encoding="utf-8")
        rec = finalize_sample(sdir, dataset, row.get("instance_name") or row.get("filename", f"row{i}"),
                              max_pages=max_pages)
        rec["difficulty"] = row.get("difficulty", "")
        records.append(rec)
        if rec["status"] == "accepted":
            accepted += 1
            print(f"accepted {sid} ({rec['page_count']}p, {rec['source_chars']} chars)")
        else:
            shutil.rmtree(sdir, ignore_errors=True)
            print(f"rejected {sid}: {rec['reason']}")
    write_manifest(records, set_dir / "manifest.csv")
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n", nargs="?", type=int, default=5)
    parser.add_argument(
        "--corpus",
        type=Path,
        default=CORPUS,
        help="output corpus root (use a staging directory for safe reruns)",
    )
    parser.add_argument(
        "--only",
        action="append",
        choices=["i2s_equation", "i2s_table", "i2s_algorithm", "i2s_plot", "pubmed_table"],
        help="build only this set; repeat to select multiple sets",
    )
    args = parser.parse_args()
    n = args.n
    corpus = args.corpus.resolve()
    wanted = set(args.only or [
        "i2s_equation", "i2s_table", "i2s_algorithm", "i2s_plot", "pubmed_table"
    ])
    all_records = {}

    if "i2s_equation" in wanted:
        eq = pick(load_i2s("equation"), n, 300, 2500)
        all_records["i2s_equation"] = build_set(
            corpus, "i2s_equation", eq,
            lambda r, i: wrap(PREAMBLE_BASE, f"Equation Sample {i}", "Derivation",
                              "The following display is drawn from a source-backed "
                              "image-to-LaTeX benchmark and reproduced verbatim.",
                              r["text"]),
            n, "stanford-crfm/image2struct-latex-v1:equation")

    if "i2s_table" in wanted:
        tb = pick(load_i2s("table"), n, 400, 4000)
        all_records["i2s_table"] = build_set(
            corpus, "i2s_table", tb,
            lambda r, i: wrap(PREAMBLE_BASE, f"Table Sample {i}", "Results",
                              "The table below is drawn from a source-backed "
                              "image-to-LaTeX benchmark and reproduced verbatim.",
                              fit_tabular(
                                  r["text"], "!", "0.76\\textheight",
                                  total_height=True,
                              )
                              if r.get("instance_name") in I2S_HEIGHT_REPAIRS
                              else r["text"]),
            n, "stanford-crfm/image2struct-latex-v1:table")

    if "i2s_algorithm" in wanted:
        al = pick(load_i2s("algorithm"), n, 300, 3000)
        all_records["i2s_algorithm"] = build_set(
            corpus, "i2s_algorithm", al,
            lambda r, i: wrap(PREAMBLE_ALGO, f"Algorithm Sample {i}", "Procedure",
                              "The pseudocode below is drawn from a source-backed "
                              "image-to-LaTeX benchmark and reproduced verbatim.",
                              r["text"] if "\\begin{algorithm" in r["text"]
                              else "\\begin{algorithm}[htbp]\n\\caption{Procedure}\n"
                                   + r["text"] + "\n\\end{algorithm}"),
            n, "stanford-crfm/image2struct-latex-v1:algorithm")

    if "i2s_plot" in wanted:
        pl = pick(load_i2s("plot"), n, 500, 8000)
        all_records["i2s_plot"] = build_set(
            corpus, "i2s_plot", pl,
            lambda r, i: wrap(PREAMBLE_PLOT, f"Plot Sample {i}", "Visualization",
                              "The figure below is a TikZ/pgfplots drawing drawn from "
                              "a source-backed image-to-LaTeX benchmark.",
                              "\\begin{figure}[htbp]\n\\centering\n" + r["text"]
                              + "\n\\caption{Source-backed plot.}\n\\end{figure}"),
            n, "stanford-crfm/image2struct-latex-v1:plot", max_pages=4)

    if "pubmed_table" in wanted:
        with fsspec.open(PUBMED) as f:
            pm = pq.read_table(f, columns=["latex", "filename"]).slice(0, 2000).to_pylist()
        for r in pm:
            r["text"] = r.pop("latex")
        pm = pick(pm, n, 600, 6000)
        all_records["pubmed_table"] = build_set(
            corpus, "pubmed_table", pm,
            lambda r, i: wrap(PREAMBLE_BASE + "\\usepackage{makecell,longtable,threeparttable,siunitx}\n",
                              f"Clinical Table Sample {i}", "Patient Data",
                              "The table below is a medical-literature table "
                              "reproduced verbatim from a PubMed-derived dataset.",
                              fit_tabular(r["text"], "\\textwidth", "!")
                              if r.get("filename") in PUBMED_WIDTH_REPAIRS
                              else r["text"]),
            n, "deepcopy/pubmed-tables-latex-768px")

    summary = {k: sum(1 for r in v if r["status"] == "accepted") for k, v in all_records.items()}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
