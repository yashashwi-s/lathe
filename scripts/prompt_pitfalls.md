# Known LaTeX→Typst conversion pitfalls

This file is injected verbatim into the system prompt of `22_run_gemini_api.py`.
Append every new failure mode we discover — one bullet, imperative, concrete.

- Escape `@` in plain text (emails, twitter handles): bare `@word` is a label
  reference in Typst and crashes or mislinks. Write `\@` or wrap in quotes.
- `\hrule` / `\rule{...}` have no `#horizontalrule` equivalent — that function
  does not exist. Use `#line(length: 100%)` or a filled `#box(...)`.
- Beamer: every `\begin{frame}` is its own page. `\titlepage` must be
  reproduced as a real first page (title, author, date, centered). Frames are
  128mm x 96mm landscape: `#set page(width: 128mm, height: 96mm)`. Separate
  frames with `#pagebreak()`. `block`/`alertblock` → rounded `#rect` with a
  colored title bar. Never drop the title page.
- `moderncv` and other CV classes: do not try to import anything LaTeX —
  recreate the layout manually with `grid(columns: (...))`, `#line`, and bold
  headers, matching the reference's column proportions.
- LaTeX doubled quotes (``...'') must become plain "..." — Typst applies smart
  quotes automatically. Never emit literal `` or '' sequences.
- TikZ / pgfplots: never output a blank page. Redraw the figure with Typst
  primitives (`#line`, `#rect`, `#circle`, `#polygon`, `#path`) or CeTZ
  (`#import "@preview/cetz:0.3.1"`), estimating coordinates from the picture.
- Tables: prefer `#table(columns: (...))` with explicit column widths chosen to
  match the reference geometry; booktabs `\toprule`/`\midrule` → `table.hline()`.
- Algorithms (`algorithm`/`algorithmic`): recreate the numbered "Algorithm 1"
  caption bar and ruled box (a `#figure` with `#line`s and numbered lines);
  do not flatten the pseudocode into prose.
- Section numbering: if the LaTeX numbers sections, `#set heading(numbering: "1.")`.
- Default LaTeX body font is Computer Modern: `#set text(font: "New Computer Modern")`.
  Math in `$...$` uses matching math fonts automatically.
- LaTeX `article` on A4 has generous margins; if unsure use
  `#set page(paper: "a4", margin: (x: 3.1cm, y: 3.5cm))` and adjust to match
  the reference render.
- Only `@preview` package imports compile; no local files, no `#include`.
- Inside a code block you are ALREADY in code mode: never write `#let`, `#for`,
  `#if` inside `{...}` braces (e.g. inside a `#for` body or a CeTZ
  `canvas({...})`) — write `let`, `for`, `if` bare. The `#` prefix is only for
  entering code from markup. (`error: the character '#' is not valid in code`)
- There is no `page-number()` function. Page numbers come from
  `#set page(numbering: "1")` or `#context counter(page).display()`.
- (2026-07-09 run, 38/45 compile failures) The single dominant killer: writing
  math WITHOUT `$...$` delimiters, directly in markup or inside `#align(...)`.
  `^`, `_`, `&`, `\` are only legal inside dollars. `#align` is for page
  alignment of content, not equation alignment — aligned equations use `&`/`\`
  INSIDE one `$ ... $` block.
- LaTeX table syntax (`&` separators, `\\` row ends, `l|c|r` specs) inside
  `#table(...)` — Typst cells are comma-separated `[content]` arguments and
  column specs are `(auto, 1fr, 2cm)`. `l`, `c`, `r` are not variables.
- Hallucinated packages: @preview/plot, @preview/draw, @preview/algorithms,
  @preview/article do not exist (each cost us a sample). Verified available:
  cetz:0.3.2, cetz-plot:0.1.1.
- `#set page(paper: a4)` — paper names must be quoted strings ("a4").
- Fonts: "Latin Modern Roman" and "New Computer Modern Roman" are not
  installed font family names; the correct name is "New Computer Modern".
- Emails/domains in running text become crashing label references
  (`@treasury.gov`): escape the `@` or use #link.
- `2e` / `2.2e` are invalid number literals (scientific notation isn't one).
- `table(caption: ...)` doesn't exist — wrap the table in
  `#figure(..., caption: [...])`.
- (2026-07-10 log mining) `rowspan:`/`colspan:` passed as direct `#table(...)`
  arguments or as `(rowspan: 2, [...])` tuples — spans are cells:
  `table.cell(rowspan: 2)[...]`. Repeating a named argument in any call is a
  hard error ("duplicate argument").
- `#text("word")` inside math — upright text in math is just quotes:
  `$"MultiHead"(Q,K,V)$`.
- `2i` in math ("invalid number suffix: i") — Typst lexes number+letter as a
  unit literal; write `2 i` with a space.
- Verified package allowlist (typst 0.14.2, 2026-07-10): cetz:0.3.2,
  cetz-plot:0.1.1, lovelace:0.3.0, algo:0.3.4. Also resolvable but not
  whitelisted in the prompt: tablem:0.2.0, wrap-it:0.1.1.
