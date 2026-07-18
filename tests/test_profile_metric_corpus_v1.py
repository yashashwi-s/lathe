from __future__ import annotations

import csv
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "evaluation"))

from profile_metric_corpus_v1 import (  # noqa: E402
    PARTITION_SEED,
    assign_metric_partitions,
    parse_source_signals,
)


class ProfileMetricCorpusTest(unittest.TestCase):
    def test_source_signals_ignore_comments_and_preserve_semantics(self) -> None:
        source = r"""
        % \begin{figure}\includegraphics{comment-only}\end{figure}
        Visible inline $x + 1$ and Figure~\ref{fig:one}.
        \begin{align*} y &= 2x \end{align*}
        \begin{table}\begin{tabular}{cc}a&b\\c&d\end{tabular}\end{table}
        \begin{enumerate}\item first\end{enumerate}
        \begin{algorithm}\begin{algorithmic}\State work\end{algorithmic}\end{algorithm}
        """
        signals = parse_source_signals(source, "05_tables_simple")
        self.assertTrue(signals["has_inline_math"])
        self.assertTrue(signals["has_display_math"])
        self.assertTrue(signals["has_math_any"])
        self.assertTrue(signals["has_table_like_environment"])
        self.assertTrue(signals["has_semantic_table"])
        self.assertFalse(signals["has_figure_source"])
        self.assertFalse(signals["has_semantic_figure"])
        self.assertTrue(signals["has_list_source"])
        self.assertTrue(signals["has_algorithm_source"])
        self.assertTrue(signals["has_crossref_source"])

    def test_canonical_partition_counts_are_exact_and_deterministic(self) -> None:
        manifest = ROOT / "data" / "latex_benchmark_v0" / "accepted_manifest.csv"
        with manifest.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        first = assign_metric_partitions(rows, PARTITION_SEED)
        second = assign_metric_partitions(rows, PARTITION_SEED)
        self.assertEqual(first, second)
        self.assertEqual(
            Counter(first.values()),
            Counter({"metric_dev": 80, "metric_validation": 39, "metric_test": 38}),
        )
        by_category = {}
        for row in rows:
            by_category.setdefault(row["category"], set()).add(first[row["sample_id"]])
        self.assertTrue(all(partitions == set(Counter(first.values())) for partitions in by_category.values()))


if __name__ == "__main__":
    unittest.main()
