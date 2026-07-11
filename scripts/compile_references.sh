#!/bin/bash
set -e

# Compile attention_prose1
pdflatex -output-directory=data/reference_pdfs/01_prose data/01_prose/attention_prose1.tex
# Compile attention_eq1
pdflatex -output-directory=data/reference_pdfs/03_eq_hard data/03_eq_hard/attention_eq1.tex
# Compile attention_table1
pdflatex -output-directory=data/reference_pdfs/07_tables_complex data/07_tables_complex/attention_table1.tex
# Compile attention_table2
pdflatex -output-directory=data/reference_pdfs/07_tables_complex data/07_tables_complex/attention_table2.tex

echo "All reference PDFs compiled successfully."
