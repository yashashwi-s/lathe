# Dataset Research Plan: Human-authored LaTeX Corpus

Date: 2026-07-12

## Goal

Replace the current AI-generated 48-sample corpus with a citable, human-authored LaTeX benchmark corpus for LaTeX-to-Typst conversion. The working target is 300-450 candidate samples fetched from credible sources, with compile validation used as a hard gate. If enough well-distributed samples survive, the final corpus can contain 200-300 validated samples.

For the immediate next build, use the simpler categorical plan in `docs/simple_categorical_dataset_plan.md`. The TeX Live seed corpora are useful diagnostic pools, but they are too mixed and package-heavy to be the first benchmark dataset.

Scope constraints for the next dataset version:

- Use `pdflatex` only for the first benchmark iteration.
- Cap accepted reference PDFs at 2-3 pages. Longer source documents can be used only if reduced to a self-contained, human-authored excerpt that still compiles.
- Build the corpus as curriculum-style slices: simple isolated constructs first, then medium structured samples, then hard mixed-layout samples. Do not let the first dataset be mostly dense package demos.
- Treat full research papers as the hardest category, but not as 10-20 page documents. The hard version should be a compact 2-3 page paper-like sample with title, abstract, sections, equations, figures/tables, references, and cross-references.
- Optimize for single-turn LLM API benchmarking. Avoid harness/repair loops in the headline benchmark because cost scales badly across 200-300 samples.
- The current 15 categories are a starting taxonomy, not a fixed requirement. The real goal is representational coverage of LaTeX constructs and document styles.

The old benchmark categories were:

1. Plain prose / paragraphs
2. Simple equations
3. Dense equations
4. Compact papers / proceedings-style papers
5. Paper sections / excerpts
6. Simple tables
7. Complex tables
8. Algorithms / pseudocode
9. Simple TikZ
10. Complex TikZ
11. PGFPlots
12. Simple CVs
13. Complex CVs
14. Posters
15. Beamer slides

These should not be treated as canonical. The new corpus should use a better structured, many-to-many taxonomy: each sample has one broad document form, one source family, and multiple construct tags. This avoids the fake precision of categories like "simple equation" versus "hard equation" when the real conversion challenge may be a mixture of math, macros, tables, labels, and layout.

## Main Finding

There does not appear to be one credible, redistribution-friendly LaTeX dataset that spans this whole taxonomy. The strongest research design is a hybrid corpus:

- arXiv-backed source documents for compact papers, math, algorithms, prose, tables, and many figures.
- Dedicated table/formula/TikZ datasets for focused structural categories.
- TeX Live / CTAN package documentation examples for high-variety construct coverage.
- Version-pinned human templates from LaTeXTemplates, Overleaf-linked GitHub repos, CTAN, and institutional template repos for CVs, letters/posters, reports, and Beamer.

This is more defensible than a single scrape because every sample can carry explicit provenance, license, source URL, source commit or arXiv ID, compile engine, and validation status.

## Representational Taxonomy

Do not build the dataset around one flat list of 15 categories. Use three axes:

### 1. Source family

- `arxiv_source`: original arXiv source archives, preferably CC-filtered.
- `texlive_ctan_doc`: examples shipped in TeX Live / CTAN package docs.
- `hf_extracted`: focused Hugging Face datasets such as arXiv tables and formulas.
- `template_repo`: version-pinned GitHub/Overleaf/LaTeXTemplates sources.
- `institutional_template`: university or conference templates with clear license/provenance.

### 2. Document form

- `compact_paper`: complete 1-3 page paper-like document.
- `paper_excerpt`: self-contained section/chunk extracted from a longer real paper.
- `standalone_construct`: small file focused on one construct, such as a table, formula, figure, or plot.
- `package_example`: TeX Live/CTAN package demonstration.
- `presentation`: Beamer slides.
- `poster`: poster or large-format layout, capped to a manageable rendered page count.
- `cv_resume`: CV/resume.
- `letter_form`: letter, form, invoice, memo, questionnaire, school document.
- `teaching_assessment`: homework, exam, problem sheet, solution sheet.

### 3. Construct tags

Use many tags per sample:

- `text_sectioning`
- `lists`
- `footnotes`
- `inline_math`
- `display_math`
- `aligned_math`
- `theorems_proofs`
- `simple_table`
- `complex_table`
- `long_table`
- `figures_images`
- `captions`
- `crossrefs`
- `citations_bibliography`
- `algorithm_pseudocode`
- `tikz`
- `pgfplots`
- `diagram_nodes_edges`
- `multi_column`
- `minipage_boxes`
- `custom_macros`
- `custom_environments`
- `beamer_frames`
- `poster_blocks`
- `fonts_symbols`
- `color`

The manifest should expose all three axes. Reporting can still group samples into readable categories later, but the underlying corpus should be coverage-tagged.

## Local Source-pool Evidence

Initial scan of local TeX Live 2026 documentation under `/usr/local/texlive/2026/texmf-dist/doc`:

| Query | Approx. matching files |
|---|---:|
| `.tex` / `.ltx` files | 14,566 |
| Files with `\documentclass` | 10,031 |
| TikZ pictures | 973 |
| TikZ/PGFPlots-related | 1,037 |
| Tables / tabular-like environments | 2,431 |
| Algorithm-related | 73 |
| Beamer/frame/theme-related | 301 |
| Equation/math display-related | 2,629 |
| Figures/images | 1,684 |
| Bibliography/citation-related | 2,098 |
| Letter/form-related | 174 |
| CV/resume-related | 387 |

These are not accepted samples yet; they are discovery-pool counts. The point is that TeX Live/CTAN documentation can realistically support broad construct coverage with human-authored source, especially for diagrams, package examples, layouts, tables, and Beamer.

## Source Notes

### arXiv source archives

Use arXiv as the backbone for real scientific LaTeX, especially compact paper-like documents and extractable 2-3 page sections. arXiv documents that most submissions use the default arXiv license, which permits arXiv distribution but does not grant third parties redistribution rights. Therefore, only samples with explicit redistributable licenses should be stored directly in the benchmark repo. For the rest, store source IDs plus a reproducible fetch script, not the source files.

Practical use:

- Fetch source archives via `https://arxiv.org/e-print/<arxiv_id>` for selected IDs.
- Prefer IDs whose metadata reports CC BY, CC BY-SA, or CC0.
- Compile locally and reject anything that does not produce a valid PDF.
- Reject or excerpt sources whose compiled reference exceeds 3 pages.
- Store `source_url`, `arxiv_id`, `license`, `authors`, `title`, `version`, `primary_category`, and `source_sha256`.

References:

- arXiv bulk source access notes: https://info.arxiv.org/help/bulk_data_s3.html
- arXiv API docs: https://info.arxiv.org/help/api/index.html

### `common-pile/arxiv_papers`

This is useful, but not as a direct LaTeX source corpus. The dataset card says the pipeline downloaded LaTeX source, converted it through LaTeXML into HTML, then converted HTML to plaintext. Its value for this project is as a citable, license-filtered arXiv ID and metadata list, not as the actual `.tex` content.

Why use it:

- About 317k arXiv paper rows.
- Includes papers uploaded under CC BY, CC BY-SA, and CC0.
- Has citation metadata through the Common Pile paper.
- Good for sampling redistributable arXiv IDs before fetching source from arXiv.

Reference: https://huggingface.co/datasets/common-pile/arxiv_papers

### `KiteFishAI/arxiv-tex-corpus-full`

This has actual LaTeX in JSONL and is useful as a large fallback pool, especially for math, CS, physics, and statistics. The dataset card states no compilation validation was enforced, no semantic cleaning was applied, and no LaTeX normalization was performed. It should therefore be treated as candidate discovery only, with local compile validation and license verification before inclusion.

Why use it:

- About 80GB of structured JSONL LaTeX.
- Fields include `paper_id`, `category`, and `latex`.
- Categories include math, CS, HEP theory, HEP phenomenology, quantum physics, and statistics.

Risk:

- License metadata is weaker for redistribution than the Common Pile route.
- It is large, so sample by streaming rather than downloading fully.

Reference: https://huggingface.co/datasets/KiteFishAI/arxiv-tex-corpus-full

### `piushorn/arxiv-latex-tables-43k`

This is the best dedicated source for table categories. The dataset card says it contains 43,651 LaTeX tables extracted from arXiv papers published in December 2025, classified as simple, moderate, or complex; all tables compile with `pdflatex`; and it uses a redistributable CC license filter.

Use for:

- `06_tables_simple`
- `07_tables_complex`

Sampling:

- Pull 40 simple, 40 moderate, and 40 complex candidates.
- Wrap each `tabular` in a standard minimal document for validation.
- Keep a balanced final set across the three complexity classes.

Reference: https://huggingface.co/datasets/piushorn/arxiv-latex-tables-43k

### `OleehyO/latex-formulas`

This is useful for focused equation stress tests, but it is less ideal for document-level conversion because the samples are formulas rather than full papers. The dataset card describes raw and cleaned formula-image pairs scraped from arXiv, with the cleaned set containing about 550k formula-image pairs.

Use for:

- `02_eq_simple`
- `03_eq_hard`

Sampling:

- Prefer raw formulas for environmental diversity (`equation`, `align`, `gather`).
- Avoid only-cleaned data if the benchmark wants messy real-world LaTeX; the cleaned set removes complex/custom cases.
- Wrap formulas into tiny documents and compile gate.

Reference: https://huggingface.co/datasets/OleehyO/latex-formulas

### TeX Live / CTAN documentation examples

This should be a first-class source pool. A local TeX Live 2026 install contains many human-authored `.tex` examples under:

```text
/usr/local/texlive/2026/texmf-dist/doc
```

Initial local discovery found examples for:

- Beamer themes and Beamer demos.
- `beamerposter`.
- PGF/TikZ and package-specific TikZ demos such as `pgf-umlsd`, `pgf-go`, `pgf-pie`, and ornament/poster examples.
- `pgfplots`.
- CV examples such as `curriculum-vitae`.
- Letter examples such as `onlinebrief24`.
- Tables/charts/data-driven examples such as `datatool` and `xltabular`.
- Journal/class samples such as `aastex` and `llncsconf`.

Why this is valuable:

- It is already installed, diverse, and usually small.
- Examples are authored to demonstrate real LaTeX package capabilities, which is exactly what converter benchmarks need.
- Package examples often stress unusual constructs that arXiv sampling may underrepresent.

Rules:

- Only include examples that compile with `pdflatex`.
- Only include examples whose license is clear from the package metadata or source tree.
- Record TeX Live version, package name, package version if available, original path, and source hash.
- Prefer small standalone examples; avoid full manuals unless extracting clearly marked example files.
- Reject examples that require shell escape, network access, proprietary fonts, LuaLaTeX/XeLaTeX, or nonlocal assets.

This pool is especially good for underrepresented construct categories:

- Beamer / presentation structure.
- Posters.
- Diagrams.
- Plots.
- Tables.
- Lists, indexing, glossaries, bibliographies.
- Letters/CVs/forms.

### TikZ and PGFPlots sources

Use a mixed strategy:

- arXiv source archives containing `tikzpicture`, `pgfplots`, `axis`, or `tikzcd`.
- DaTikZ-style corpora only after checking license and human-authored provenance.
- TeXample.net / PGF manual / CTAN package examples for curated, human-authored examples.

Use for:

- `09_tikz_simple`
- `10_tikz_complex`
- `11_pgfplots`

Compile rule:

- Use `pdflatex` only for the first dataset version.
- Reject sources that require `lualatex` or `xelatex`; record them as possible future-version candidates.
- Reject examples that need missing external assets unless the asset license is clear and the asset can be stored or reproducibly fetched.

References:

- PGF/TikZ package information and gallery pointers: https://www.ctan.org/pkg/pgf
- TeXample TikZ gallery: https://www.texample.net/tikz/examples/
- AutomaTikZ / DaTikZ paper: https://arxiv.org/abs/2310.00367

### LaTeXTemplates.com

This is useful for non-paper document classes and layouts: CVs, resumes, cover letters, formal letters, books, posters, presentations, assignments, theses, newsletters, and reports. The site itself says most templates are licensed under CC BY-NC-SA 4.0, so each selected template still needs per-template license confirmation.

Use for:

- `12_cv_simple`
- `13_cv_complex`
- `14_posters`
- `15_beamer`
- possible future categories: letters, books, assignments, newsletters, theses

Reference: https://www.latextemplates.com/

### Overleaf Gallery and linked GitHub repos

Overleaf is a strong discovery layer, especially when entries link to GitHub repositories or state a clear license. Prefer GitHub-backed templates because they can be pinned by commit hash and cited reproducibly.

Observed useful categories:

- CVs and resumes
- Presentations / Beamer
- Posters
- Assignments
- Letters
- Theses
- Reports
- Books

Selection rule:

- Do not cite "Overleaf gallery page only" as the canonical source if a GitHub repo exists.
- Pin `owner/repo@commit`.
- Store license file, source URL, and exact compile command.

References:

- CV gallery: https://www.overleaf.com/gallery/tagged/cv
- Presentation gallery: https://www.overleaf.com/gallery/tagged/presentation
- Poster gallery: https://www.overleaf.com/gallery/tagged/poster

### Semantic Scholar / S2ORC

Semantic Scholar is useful for metadata and paper discovery, but it is not a primary LaTeX source for this benchmark. S2ORC provides structured academic full text and rich metadata, not original `.tex` source suitable for LaTeX-to-Typst conversion. The Semantic Scholar API/Datasets can still help identify papers, fields, citations, venues, and open-access metadata, but final source retrieval should come from arXiv, CTAN, TeX Live docs, or versioned repositories.

Use for:

- Candidate discovery and diversity checks across fields/venues.
- Citation metadata in the paper.
- Linking selected arXiv papers to broader scholarly metadata.

Do not use for:

- Direct benchmark samples unless original LaTeX source is available elsewhere.

References:

- Semantic Scholar API overview: https://www.semanticscholar.org/product/api
- S2ORC paper: https://arxiv.org/abs/1911.02782

## Recommended Corpus Shape

Aim for 300-450 candidates and keep 200-300 validated samples after compile filtering. More than 200 final samples is fine as long as distribution remains controlled. Avoid letting arXiv papers or TeX Live examples dominate just because they are easiest to harvest.

### Source-family balance

Target final proportions:

| Source family | Final target |
|---|---:|
| arXiv source archives | 30-40% |
| TeX Live / CTAN docs | 30-40% |
| Focused HF extracted datasets | 10-20% |
| Template repos / institutional templates | 10-20% |

Hard caps:

- No single source family should exceed 45%.
- No single package, repo, arXiv subject, or template site should exceed 10% of the final corpus.
- No exact source document should contribute more than 3 accepted samples unless explicitly marked as an ablation/stress source.

### Document-form balance

Suggested final shape for a 240-sample corpus:

| Document form | Final target | Primary sources |
|---|---:|---|
| Compact papers | 35-45 | CC-filtered arXiv source archives, class samples |
| Paper excerpts | 25-35 | arXiv sections extracted from compiling papers |
| Math-heavy standalone/short docs | 25-35 | formula datasets, math/physics arXiv, TeX Live math docs |
| Tables | 25-35 | arXiv LaTeX Tables 43k, TeX Live table packages |
| Figures, TikZ, diagrams, plots | 35-45 | TeX Live docs, CTAN, TeXample, arXiv |
| Algorithms / pseudocode | 10-15 | CS arXiv, TeX Live algorithm packages |
| Beamer presentations | 15-20 | TeX Live docs, template repos, institutional templates |
| Posters / layout-rich pages | 10-15 | TeX Live docs, template repos |
| CVs / resumes | 10-15 | TeX Live docs, template repos, LaTeXTemplates |
| Letters / forms / teaching docs | 20-25 | TeX Live docs, templates |

For 300 final samples, scale the same proportions rather than adding a new dominant category.

### Construct coverage minimums

For the final frozen corpus, aim for at least:

| Construct tag | Minimum accepted samples |
|---|---:|
| `display_math` | 50 |
| `aligned_math` | 25 |
| `simple_table` | 25 |
| `complex_table` | 25 |
| `figures_images` | 30 |
| `tikz` | 25 |
| `pgfplots` | 15 |
| `citations_bibliography` | 30 |
| `crossrefs` | 40 |
| `custom_macros` | 40 |
| `algorithm_pseudocode` | 10 |
| `multi_column` / `minipage_boxes` | 25 |
| `beamer_frames` | 15 |
| `poster_blocks` | 8 |

These minimums matter more than preserving the old category list.

## Proposed Repository Structure

Archive the existing generated corpus and create a provenance-first dataset layout:

```text
archive/
  data/
  results/
  ai_models/
  scripts/

data/
  raw/
    arxiv/
    tables/
    formulas/
    texlive/
    templates/
  candidates/
    <sample_id>/
      source.tex
      source_assets/
      provenance.json
  corpus/
    <category>/<sample_id>/
      main.tex
      assets/
      reference.pdf
      compile.log
      provenance.json
  manifests/
    candidates.csv
    corpus.csv
    rejected.csv
    licenses.csv
docs/
  dataset_research_plan.md
  dataset_methodology.md
```

## Manifest Fields

Every candidate and accepted sample should have:

- `sample_id`
- `category`
- `difficulty`
- `source_family`
- `source_name`
- `source_url`
- `canonical_citation`
- `license`
- `license_url`
- `authors`
- `title`
- `source_version`
- `source_commit`
- `arxiv_id`
- `arxiv_version`
- `downloaded_at`
- `sha256_source`
- `sha256_pdf`
- `compile_engine`
- `compile_command`
- `compile_status`
- `compile_seconds`
- `page_count`
- `requires_shell_escape`
- `requires_network`
- `has_external_assets`
- `asset_license_status`
- `rejection_reason`

## Compile Gate

The compile gate should be strict and boring:

1. Create an isolated temp build directory per sample.
2. Copy source and local assets only.
3. Run `pdflatex` with nonstop interaction and halt-on-error.
4. Run twice for references/citations when needed.
5. Accept only if a non-empty valid PDF exists and PyMuPDF can open it.
6. Reject if the accepted reference PDF exceeds 3 pages.
7. Record page count and SHA-256 hashes.
8. Reject samples requiring unavailable assets, network access, shell escape, non-pdfLaTeX engines, or unclear licensed assets.

Compiler command:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Do not patch sources to make them compile except for mechanical wrapper insertion around extracted snippets. If a complete source archive fails as authored, reject it.

## Difficulty Definition

Difficulty should be based on observable LaTeX and layout complexity, not on original document category names.

Suggested features:

- Page count: 1 page, 2 pages, 3 pages.
- Macro/package count.
- Custom command/environment count.
- Number of floats, captions, labels, references, citations.
- Math density and display math count.
- Table complexity: rows, columns, `multicolumn`, `multirow`, `tabularx`, long tables.
- Graphics complexity: TikZ/PGFPlots environments, paths, nodes, axes, legends.
- Structural complexity: sections, lists, footnotes, bibliography, theorem-like environments.
- Layout complexity: columns, minipages, poster blocks, Beamer frames, sidebars.

Use these features to label `easy`, `medium`, and `hard`. A hard sample can still be only 2-3 pages if it combines several constructs.

## Metrics Plan (Deferred)

Metrics are not the active focus while building the dataset. Keep this as a placeholder for later benchmark work.

For the next benchmark, keep the single-turn setup and score three layers:

### 1. Reliability

- Typst compile success.
- Retry-free success only for the headline number.
- Runtime and API cost per sample.
- Output completeness: non-empty PDF, expected page count tolerance, no missing first page.

### 2. Source and structural fidelity

- No leaked LaTeX commands in Typst.
- Text retention against reference PDF text, not raw source only.
- Structural element recovery: headings, lists, equations, tables, figures, captions, labels, references, bibliography, Beamer frames.
- Counter/reference correctness where the reference PDF exposes numbering.
- Package/construct-specific checks for tables, math, TikZ-like graphics, plots, and presentations.

### 3. Visual fidelity

- Page-count match.
- Text block matching with token Jaccard plus normalized bounding-box IoU.
- Image/page SSIM for graphics-heavy samples.
- Table geometry metrics: cell grid recovery, row/column alignment, caption placement.
- Equation region match: detect display math blocks and compare bounding boxes.
- Plot/diagram raster similarity for PGF/TikZ/PGFPlots samples.

Headline reporting should separate:

- `Compile rate`
- `Source/structure score`
- `Text match`
- `Layout IoU`
- `Graphics score`
- `Overall score`

Avoid a single opaque aggregate as the only result. The paper will be stronger if it shows which systems fail by compilation, text loss, structure loss, or layout drift.

## Implementation Plan

1. Add a `scripts/dataset/` pipeline:
   - `discover_arxiv.py`
   - `fetch_arxiv_sources.py`
   - `discover_texlive_examples.py`
   - `fetch_hf_tables.py`
   - `fetch_hf_formulas.py`
   - `fetch_template_repos.py`
   - `compile_gate.py`
   - `build_manifest.py`

2. Build the source-specific candidate pools:
   - Use `common-pile/arxiv_papers` for CC-filtered arXiv ID discovery.
   - Fetch actual `.tex` archives from arXiv.
   - Scan local TeX Live docs for standalone pdfLaTeX examples.
   - Stream table/formula datasets by columns; do not download full datasets.
   - Clone only selected template repos at pinned commits.

3. Normalize candidates into the same shape:
   - one `main.tex`
   - local assets
   - `provenance.json`
   - no generated or AI-authored samples

4. Run compile validation:
   - target 300-450 candidates
   - keep compile-valid PDFs only
   - keep only references of 3 pages or fewer
   - log rejected candidates with reason

5. Freeze the final corpus:
   - choose 200-300 validated samples if enough well-distributed samples survive
   - balance document form, construct tags, difficulty, source family, and document length
   - write `data/manifests/corpus.csv`
   - generate `docs/dataset_methodology.md`

6. Re-run the existing conversion/evaluation pipeline on the new corpus.

## Paper Methodology Language

The dataset can be described as a human-authored, provenance-tracked hybrid corpus built from openly licensed arXiv source archives, dedicated LaTeX table/formula corpora, TeX Live/CTAN documentation examples, and version-pinned community or institutional LaTeX templates. Samples were included only if the original LaTeX compiled with `pdflatex` to a valid 1-3 page reference PDF in an isolated build environment. Each retained sample includes source provenance, license metadata, source and PDF hashes, compile command, and rejection logs for excluded candidates.

## Open Questions

- Decide whether non-commercial licenses such as CC BY-NC-SA 4.0 are acceptable for the benchmark repo and paper artifact.
- Decide whether to store redistributable source files directly or store fetch scripts plus IDs for all arXiv-derived papers.
- Decide whether snippets extracted from full papers should be part of the main corpus or only a stress-test subset.
- Decide whether to allow XeLaTeX/LuaLaTeX-only templates in a later benchmark version. For the first pass, exclude them.
- Decide whether TeX Live documentation examples can be redistributed directly package-by-package, or whether the benchmark should record package paths plus a TeX Live version for reconstruction.
