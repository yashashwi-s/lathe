#!/bin/bash
# Build the three report PDFs from their markdown sources.
# Run from the repo root:  bash scripts/build_reports.sh
set -e

PANDOC_OPTS="--pdf-engine=xelatex -V geometry:margin=2.2cm -V fontsize=10pt -V colorlinks=true"

pandoc reports/benchmark_findings.md -o reports/benchmark_findings.pdf $PANDOC_OPTS
echo "built reports/benchmark_findings.pdf"

pandoc reports/visual_alignment_report.md -o reports/visual_alignment_report.pdf $PANDOC_OPTS
echo "built reports/visual_alignment_report.pdf"

pandoc reports/appendix.md -o reports/appendix.pdf $PANDOC_OPTS
echo "built reports/appendix.pdf"
