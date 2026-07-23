# Expansion-32 reference visual audit

This audit covers only the 32 newly added references named in
`data/latex_benchmark_v0/splits/expansion_32.csv` and every one of
their rendered pages. The original 157 references are not included.
Automatic flags are triage signals; acceptance requires recording the
manual contact-sheet decision separately.

- Documents: 32
- Pages: 104
- Render DPI: 110
- Auto-clear: 24
- Needs review: 8
- Automatic failures: 0
- Documents with TeX overfull warnings: 8
- Largest reported overfull amount: 57.214 pt
- Manually reviewed: 32/32
- Manual passes: 32
- Manual failures: 0

## By category

| Category | Documents | Clear | Review | Fail |
|---|---:|---:|---:|---:|
| `arxiv5t_paper` | 5 | 1 | 4 | 0 |
| `i2s_algorithm` | 5 | 5 | 0 | 0 |
| `i2s_equation` | 5 | 4 | 1 | 0 |
| `i2s_plot` | 5 | 4 | 1 | 0 |
| `i2s_table` | 5 | 3 | 2 | 0 |
| `neurips_paper` | 2 | 2 | 0 | 0 |
| `pubmed_table` | 5 | 5 | 0 | 0 |

## Flagged documents

| Sample | Category | Status | Max overfull | Flags |
|---|---|---|---:|---|
| `i2s_equation_001` | `i2s_equation` | `review` | 53.226 pt | compile_overfull |
| `i2s_table_004` | `i2s_table` | `review` | 57.214 pt | compile_overfull |
| `i2s_table_006` | `i2s_table` | `review` | 14.819 pt | compile_overfull |
| `i2s_plot_004` | `i2s_plot` | `review` | 1.280 pt | compile_overfull |
| `arxiv5t_paper_002` | `arxiv5t_paper` | `review` | 24.999 pt | compile_overfull |
| `arxiv5t_paper_006` | `arxiv5t_paper` | `review` | 15.447 pt | compile_overfull |
| `arxiv5t_paper_019` | `arxiv5t_paper` | `review` | 50.938 pt | compile_overfull |
| `arxiv5t_paper_020` | `arxiv5t_paper` | `review` | 42.556 pt | compile_overfull |

## Artifacts

- `document_audit.csv`: one automatic QA record per expansion document.
- `page_audit.csv`: one automatic QA record per rendered reference page.
- `contact_sheets/`: every reference page, labeled and rendered for review.
- `manual_review.csv`: reviewer disposition; created after contact-sheet review.
