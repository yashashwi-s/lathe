#let ink = rgb("#20272b")
#let muted = rgb("#586368")
#let faint = rgb("#eef0ed")
#let rule = rgb("#d2d7d5")
#let paper = rgb("#fbfaf7")
#let white = rgb("#ffffff")
#let teal = rgb("#147a7e")
#let teal-soft = rgb("#e1eeee")
#let rust = rgb("#a84732")
#let rust-soft = rgb("#f2e5e0")
#let amber = rgb("#a86d09")
#let amber-soft = rgb("#f4ead6")
#let gray-soft = rgb("#eceeed")

#set document(
  title: "PDF Fidelity Evaluation System — current method and evidence",
  author: "Lathe metric research",
)
#set page(
  width: 297mm,
  height: 210mm,
  margin: (x: 14mm, top: 12mm, bottom: 12mm),
  fill: paper,
  footer: context [
    #set text(font: "Avenir Next", size: 8.6pt, fill: muted)
    #grid(columns: (1fr, auto),
      [LATHE / PDF FIDELITY EVALUATION SYSTEM],
      [#counter(page).display("1")],
    )
  ],
)
#set text(font: "Avenir Next", size: 11.4pt, fill: ink, lang: "en")
#set par(justify: false, leading: 0.50em, spacing: 0.62em)
#set list(indent: 1.20em, body-indent: 0.55em, spacing: 0.38em)
#set enum(indent: 1.20em, body-indent: 0.55em, spacing: 0.38em)
#set table(stroke: rule, inset: (x: 6pt, y: 5pt))
#show link: set text(fill: teal)
#show heading.where(level: 1): it => [
  #set text(weight: 650, size: 27pt, fill: ink)
  #block(above: 0pt, below: 7pt)[#it.body]
]
#show heading.where(level: 2): it => [
  #set text(weight: 650, size: 15pt, fill: ink)
  #block(above: 5pt, below: 3pt)[#it.body]
]

#let asset(name) = "assets/pdf_fidelity_v3/" + name + ".png"
#let num(x, digits: 3) = if x == none or x == "" { "—" } else { str(calc.round(float(x), digits: digits)) }
#let pct(x, digits: 1) = str(calc.round(float(x) * 100, digits: digits)) + "%"
#let upper-label(body) = text(size: 9pt, weight: 650, fill: muted, tracking: 0.08em)[#upper(body)]
#let page-head(kicker, title, deck: none) = [
  #upper-label(kicker)
  #v(2pt)
  #block(width: 100%)[#heading(level: 1)[#title]]
  #if deck != none [#text(size: 12.2pt, fill: muted)[#deck] #v(4pt)]
  #line(length: 100%, stroke: 0.8pt + rule)
  #v(7pt)
]
#let pill(body, kind: "neutral") = {
  let bg = if kind == "core" { teal-soft } else if kind == "warn" { amber-soft } else if kind == "stop" { rust-soft } else { gray-soft }
  let fg = if kind == "core" { teal } else if kind == "warn" { amber } else if kind == "stop" { rust } else { ink }
  box(fill: bg, radius: 3pt, inset: (x: 7pt, y: 4pt))[
    #text(size: 8.7pt, weight: 700, fill: fg, tracking: 0.04em)[#upper(body)]
  ]
}
#let card(body, fill-color: white, edge: rule, inset: 10pt) = block(
  fill: fill-color,
  stroke: 0.7pt + edge,
  radius: 4pt,
  inset: inset,
  body,
)
#let fact(label, value, note: none, kind: "neutral") = {
  let edge = if kind == "core" { teal } else if kind == "warn" { amber } else if kind == "stop" { rust } else { rule }
  card([
    #upper-label(label)
    #v(3pt)
    #text(size: 22pt, weight: 650, fill: ink)[#value]
    #if note != none [#v(2pt) #text(size: 9.5pt, fill: muted)[#note]]
  ], edge: edge)
}
#let note(title, body, kind: "neutral") = {
  let bg = if kind == "core" { teal-soft } else if kind == "warn" { amber-soft } else if kind == "stop" { rust-soft } else { gray-soft }
  let fg = if kind == "core" { teal } else if kind == "warn" { amber } else if kind == "stop" { rust } else { ink }
  block(fill: bg, radius: 4pt, inset: 10pt)[
    #text(weight: 650, fill: fg)[#title]
    #v(3pt)
    #text(size: 10.5pt, fill: ink)[#body]
  ]
}
#let method-lead(status, kind, stage, question) = grid(
  columns: (auto, 1fr), gutter: 10pt, align: (left, horizon),
  [#pill(status, kind: kind)],
  [#text(size: 10pt, fill: muted)[*Where used:* #stage]],
) + [#v(6pt) #text(size: 15pt, weight: 600)[#question]]
#let image-card(title, path, caption, edge: rule, height: 43mm) = card([
  #upper-label(title)
  #v(4pt)
  #align(center)[#image(path, width: 100%, height: height, fit: "contain")]
  #v(4pt)
  #text(size: 9.5pt, fill: muted)[#caption]
], edge: edge, inset: 8pt)
#let paired-crops(left-title, left-path, left-caption, right-title, right-path, right-caption, height: 42mm) = grid(
  columns: (1fr, 1fr), gutter: 9pt,
  image-card(left-title, left-path, left-caption, edge: teal, height: height),
  image-card(right-title, right-path, right-caption, edge: rust, height: height),
)
#let score-strip(items) = grid(
  columns: (1fr,) * items.len(), gutter: 5pt,
  ..items.map(item => card([
    #upper-label(item.at(0))
    #v(2pt)
    #text(size: 14pt, weight: 650)[#item.at(1)]
    #v(1pt)
    #text(size: 8.8pt, fill: muted)[#item.at(2)]
  ], inset: 7pt)),
)
#let method-footer(direction, input, limitation, source) = grid(
  columns: (1fr, 1fr), gutter: 8pt,
  block(fill: teal-soft, radius: 4pt, inset: 8pt)[
    #text(size: 9.5pt, weight: 650, fill: teal)[Direction + input]
    #v(2pt)
    #text(size: 9.2pt)[*#direction* #input]
  ],
  block(fill: amber-soft, radius: 4pt, inset: 8pt)[
    #text(size: 9.5pt, weight: 650, fill: amber)[Limit / abstention]
    #v(2pt)
    #text(size: 9.2pt)[#limitation]
    #v(2pt)
    #text(size: 8.3pt, fill: muted)[Source: #source]
  ],
)
#let legend() = grid(
  columns: (auto, auto, auto, 1fr), gutter: 10pt, align: (left, horizon),
  [#box(width: 13mm, height: 5mm, stroke: (dash: "dashed", thickness: 1.8pt, paint: teal))],
  [#text(size: 9pt)[reference text]],
  [#box(width: 13mm, height: 5mm, stroke: 1.8pt + rust)],
  [#text(size: 9pt)[candidate text · gray dashed means expected location with no detected text]],
)
#let count-rate-cell(count, total, rate) = [
  #text(size: 9.3pt, weight: 650)[#(str(count) + "/" + str(total))]
  #linebreak()
  #text(size: 7.8pt, fill: muted)[#pct(rate)]
]
#let score-cell(value, eligible: none) = [
  #text(size: 9.3pt, weight: 650)[#num(value)]
  #if eligible != none [
    #linebreak()
    #text(size: 7.8pt, fill: muted)[#(str(eligible) + " eligible")]
  ]
]
#let scorecard-table(rows) = table(
  columns: (29mm, 42mm, 23mm, 23mm, 24mm, 19mm, 19mm, 19mm, 19mm, 19mm, 22mm),
  align: (left, left, center, center, center, center, center, center, center, center, center),
  inset: (x: 3.5pt, y: 5pt),
  table.header(
    table.cell(fill: gray-soft)[#upper-label("SYSTEM")],
    table.cell(fill: gray-soft)[#upper-label("PROTOCOL")],
    table.cell(fill: gray-soft)[#upper-label("COMPILED")],
    table.cell(fill: gray-soft)[#upper-label("PAGE EXACT")],
    table.cell(fill: gray-soft)[#upper-label("CANVAS EXACT")],
    table.cell(fill: gray-soft)[#upper-label("STRICT F1 ↑")],
    table.cell(fill: gray-soft)[#upper-label("NFKC F1 ↑")],
    table.cell(fill: gray-soft)[#upper-label("REF. COV. ↑")],
    table.cell(fill: gray-soft)[#upper-label("CENTER q90 ↓")],
    table.cell(fill: gray-soft)[#upper-label("LTSIM ↑")],
    table.cell(fill: gray-soft)[#upper-label("SSIM ↑")],
  ),
  ..rows.map(row => (
    table.cell(fill: white)[#text(size: 9.2pt, weight: 650)[#row.label]],
    table.cell(fill: white)[#text(size: 8.1pt, fill: muted)[#row.protocol]],
    table.cell(fill: white)[#count-rate-cell(row.compiled, row.total, row.compile_rate)],
    table.cell(fill: white)[#count-rate-cell(row.page_exact, row.total, row.page_exact_rate_all)],
    table.cell(fill: white)[#count-rate-cell(row.canvas_exact, row.compiled, row.canvas_exact_rate_compiled)],
    table.cell(fill: white)[#score-cell(row.strict_word_f1_median)],
    table.cell(fill: white)[#score-cell(row.compatibility_word_f1_median)],
    table.cell(fill: white)[#score-cell(row.reference_coverage_median)],
    table.cell(fill: white)[#score-cell(row.center_q90_median)],
    table.cell(fill: white)[#score-cell(row.text_ltsim_median)],
    table.cell(fill: white)[#score-cell(row.ssim_median, eligible: row.ssim_eligible)],
  )).flatten(),
)

#let ctl = json("../results/metric_research_v2/controlled_retained_628/validation/validation_summary.json")
#let identity = json("../results/metric_research_v2/identity_157_final/identity_validation.json")
#let gemini = json("../results/metric_research_v2/gemini_frozen_156/metric_summary.json").groups.all
#let reaudit = json("../results/metric_research_v2/controlled_retained_628/validation/reaudit/reaudit_agreement.json")
#let overlap-scores = csv("../results/metric_research_v2/claude_overlap/metric_v2/metric_v2_scores.csv", row-type: dictionary)
#let scorecards = json("../results/metric_research_v2/scorecards/scorecards.json")
#let score-for(sample, role) = overlap-scores.find(row => row.sample_id == sample and row.asset_role == role)

// 1 — cover
#set page(footer: none)
#v(18mm)
#upper-label("LATHE / CURRENT RESEARCH SYSTEM / 18 JULY 2026")
#v(7mm)
#text(size: 40pt, weight: 650, fill: ink)[PDF fidelity evaluation]
#v(3mm)
#text(size: 18pt, fill: muted)[Current method, visual evidence, and AI-model comparisons]
#v(14mm)
#grid(columns: (1.25fr, 1fr), gutter: 16mm,
  [
    #block(stroke: (left: 4pt + teal), inset: (left: 12pt, y: 2pt))[
      #text(size: 16pt, weight: 600)[What the system returns]
      #v(5pt)
      #text(size: 13pt)[A non-compensatory evidence vector: exact page facts, content preservation, localized text geometry, conditional layout and raster diagnostics, plus explicit abstentions.]
    ]
    #v(10mm)
    #note("The central rule", [A high score on one axis never erases a failure on another. There is no universal 0–100 grade.], kind: "stop")
  ],
  [
    #fact("OUTPUT 1", "facts", note: "page count · canvas · eligibility", kind: "core")
    #v(6pt)
    #fact("OUTPUT 2", "scores", note: "raw axes with direction and coverage", kind: "core")
    #v(6pt)
    #fact("OUTPUT 3", "evidence", note: "text boxes · missing values · transport flows", kind: "core")
  ],
)
#set page(footer: context [
  #set text(font: "Avenir Next", size: 8.6pt, fill: muted)
  #grid(columns: (1fr, auto), [LATHE / PDF FIDELITY EVALUATION SYSTEM], [#counter(page).display("1")])
])
#pagebreak()

// 2 — pipeline
#page-head("01 / WHAT WE USE NOW", "The current evaluation pipeline", deck: [The pair is gated first; each later module answers a narrower question and keeps its own evidence.])
#grid(columns: (1fr, auto, 1fr, auto, 1fr), gutter: 7pt, align: (center, horizon),
  card([#pill("INPUT") #v(5pt) #text(size: 15pt, weight: 600)[Reference PDF] #linebreak() #text(size: 15pt, weight: 600)[Candidate PDF] #v(5pt) #text(size: 9.5pt, fill: muted)[hashes · producer · protocol]], edge: rule),
  [#text(size: 22pt, fill: muted)[→]],
  card([#pill("GATE", kind: "core") #v(5pt) #text(size: 15pt, weight: 600)[Open + page facts] #v(5pt) #text(size: 9.5pt, fill: muted)[page count · physical canvas · paired-page eligibility]], edge: teal),
  [#text(size: 22pt, fill: muted)[→]],
  card([#pill("CORE", kind: "core") #v(5pt) #text(size: 15pt, weight: 600)[Exact preservation] #v(5pt) #text(size: 9.5pt, fill: muted)[strict NFC · NFKC view · numbers/operators/citations]], edge: teal),
)
#v(9pt)
#align(center)[#text(size: 22pt, fill: muted)[↓]]
#v(5pt)
#grid(columns: (1fr, auto, 1fr, auto, 1fr), gutter: 7pt, align: (center, horizon),
  card([#pill("EVIDENCE", kind: "core") #v(5pt) #text(size: 15pt, weight: 600)[Report packet] #v(5pt) #text(size: 9.5pt, fill: muted)[scores · coverage · text boxes · missing values · abstention reasons]], edge: teal),
  [#text(size: 22pt, fill: muted)[←]],
  card([#pill("CONDITIONAL", kind: "warn") #v(5pt) #text(size: 15pt, weight: 600)[Raster + structures] #v(5pt) #text(size: 9.5pt, fill: muted)[same-canvas SSIM · legacy ink · structure abstentions]], edge: amber),
  [#text(size: 22pt, fill: muted)[←]],
  card([#pill("CONDITIONAL", kind: "warn") #v(5pt) #text(size: 15pt, weight: 600)[Spatial evidence] #v(5pt) #text(size: 9.5pt, fill: muted)[token geometry · Text-LTSim · pagination · order · typography]], edge: amber),
)
#v(10mm)
#grid(columns: (1fr, 1fr, 1fr), gutter: 8pt,
  note("Hard facts", [Page count and physical canvas are never normalized away.], kind: "core"),
  note("No silent substitution", [NFKC does not overwrite strict NFC; block geometry does not substitute for content.], kind: "core"),
  note("Fail closed", [A metric reports “abstain” when its required representation is absent.], kind: "warn"),
)

#pagebreak()

// 3 — reading a result
#page-head("02 / HOW TO READ A RESULT", "One PDF pair, one evidence chain", deck: [The boxes enclose the actual text blocks. The scores describe different properties of the same conversion.])
#method-lead("EXPLAINED EXAMPLE", "core", [after exact-word matching and block extraction], [What survived, and where did it move?])
#v(6pt)
#paired-crops(
  "REFERENCE · PAGE 1", asset("geometry_address_reference"), [Teal dashed box: manually outlined sender-address text region.],
  "GEMINI · PAGE 1", asset("geometry_address_candidate"), [Rust solid box: the same exact words appear near the upper-right.],
  height: 39mm,
)
#v(7pt)
#score-strip((
  ("STRICT WORD F1 ↑", "0.969", "nearly all words retained"),
  ("CENTER q90 ↓", "0.671", "large matched-word movement"),
  ("TEXT-LTSIM ↑", "0.671", "text-block transport only"),
  ("NUMBER F1 ↑", "0.667", "date numerals missing"),
))
#v(7pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("What the scores jointly say", [Content is almost complete, but its placement is not. Exact text protects against calling the pair a content failure; geometry and Text-LTSim identify large spatial change.], kind: "core"),
  note("What they still cannot say", [No calibrated cutoff converts 0.671 into “major.” The visible conclusion comes from the boxed text and the exact metric evidence, not a hidden quality band.], kind: "warn"),
)
#v(5pt)
#legend()

#pagebreak()

// 4 — status map
#page-head("03 / CURRENT STATUS", "What is used, conditional, pending, or rejected", deck: [The status is part of the result. “Not scored” is preferable to a fabricated number.])
#grid(columns: (1fr, 1fr, 1fr), gutter: 9pt,
  card([
    #pill("USED NOW", kind: "core")
    #v(7pt)
    *Hard facts*  
    page count · physical canvas · eligibility
    #v(5pt)
    *Core preservation*  
    strict NFC tokens · character edit · NFKC compatibility · numbers/operators/restricted citations
    #v(5pt)
    *Evidence anchors*  
    exact NFKC word matches · unmatched word boxes
  ], edge: teal),
  card([
    #pill("CONDITIONAL / DIAGNOSTIC", kind: "warn")
    #v(7pt)
    token center displacement · size ratios · Text-LTSim text-only trial · benchmark block OT · page assignment/boundaries · reading-order tau · typography metadata · same-canvas SSIM · four-scale raster adaptation · tolerant ink
    #v(7pt)
    #text(size: 10pt, fill: muted)[Each is reported with coverage, eligibility, or a warning. None is a universal perceptual grade.]
  ], edge: amber),
  card([
    #pill("PENDING / ABSTAIN / REJECTED", kind: "stop")
    #v(7pt)
    *Pending:* official CLEval conformance  
    *Abstain:* semantic LTSim, GriTS, TEDS, formula structure, figure/caption structure  
    *Rejected:* universal scalar; resized-canvas “SSIM”; collapsed token-IoU tail as an AI grade
  ], edge: rust),
)
#v(9mm)
#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 7pt,
  fact("REFERENCES", "157", note: "accepted PDF pairs for identity"),
  fact("GEMINI", "156", note: "frozen compiled outputs"),
  fact("FOUR-WAY SETS", "7", note: "21 candidate PDFs"),
  fact("OVERALL SCORE", "none", note: "deliberately null", kind: "stop"),
)

#pagebreak()

// 5 — canvas and page facts
#page-head("04 / METHOD", "Eligibility, page count, and physical canvas")
#method-lead("HARD GATE", "core", [first, before any spatial or raster comparison], [Are these PDFs open, and are their page sequences physically comparable?])
#v(7pt)
#grid(columns: (1.05fr, 0.95fr), gutter: 12mm,
  [
    #heading(level: 2)[What is measured]
    The evaluator records PDF-open status, page count, and every page width/height in points. It reports page-count delta, exact paired-size rate, and maximum absolute log width/height ratio.

    #heading(level: 2)[Why it comes first]
    Normalizing each page independently can make Letter and A4 layouts look deceptively similar. Canvas mismatch therefore remains an explicit finding and makes same-canvas raster metrics abstain.

    #v(5pt)
    #score-strip((
      ("PAGE COUNT", "129 / 156", "Gemini pairs exact"),
      ("CANVAS", "2 / 156", "all paired pages exact"),
    ))
  ],
  [
    #card([
      #upper-label("PHYSICAL PAGE EXAMPLE")
      #v(8pt)
      #grid(columns: (1fr, 1fr), gutter: 12pt, align: (center, bottom),
        [#align(center)[#box(width: 42mm, height: 54.35mm, stroke: 2pt + teal)[#align(center + horizon)[#text(size: 10pt, weight: 650)[LETTER#linebreak()612 × 792 pt]]]]],
        [#align(center)[#box(width: 39.55mm, height: 55.88mm, stroke: 2pt + rust)[#align(center + horizon)[#text(size: 10pt, weight: 650)[A4#linebreak()595.276 × 841.890 pt]]]]],
      )
      #v(6pt)
      #text(size: 9.5pt, fill: muted)[The outlines use the true aspect ratios. A renderer may make the pages occupy similar screen space, but their physical dimensions differ.]
    ], edge: rule)
  ],
)
#v(7pt)
#method-footer(
  [Exact facts; zero delta and exact size are required for equality.],
  [Input: PDF page dictionaries and point dimensions.],
  [This gate says nothing about content or layout inside a page. It only establishes comparability.],
  [PDF 1.7 page geometry; repository implementation `_canvas_axis`.],
)

#pagebreak()

// 6 — strict text
#page-head("05 / METHOD", "Strict extracted-text preservation")
#method-lead("CORE", "core", [primary content-preservation stage], [Did the candidate preserve the extracted text exactly, without semantic forgiveness?])
#v(6pt)
#paired-crops(
  "REFERENCE TEXT SAMPLE", asset("strict_math_reference"), [Rendered mathematical expression; teal box is a manual text-region locator.],
  "GEMINI TEXT SAMPLE", asset("strict_math_candidate"), [Literal source commands are printed as clipped text; rust box is manual visual evidence.],
  height: 38mm,
)
#v(6pt)
#score-strip((
  ("TOKEN F1 ↑", "0.474", "multiset overlap"),
  ("CHAR EDIT ↑", "0.507", "normalized edit similarity"),
  ("OPERATOR F1 ↑", "0.267", "critical inventory"),
  ("REF COVERAGE ↑", "0.390", "exact NFKC word anchors"),
))
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("Definition", [$P = "TP"/("TP"+"FP")$, $R = "TP"/("TP"+"FN")$, $F_1 = 2 P R/(P+R)$. Text is NFC-normalized, soft hyphens are removed, whitespace is collapsed, and whitespace tokens are counted as a multiset.], kind: "core"),
  note("Box provenance", [Strict token F1 has no intrinsic coordinates. The boxes above merely identify the visible text samples; missing/extra localization comes from the separate NFKC PDF-word layer.], kind: "warn"),
)
#v(5pt)
#method-footer(
  [Higher is better; exact preservation is 1.],
  [Input: extracted page text in stable page order.],
  [PDF text extraction can tokenize visually faithful math differently. Across Gemini, median strict F1 is 0.821; its content-issue AUC against one LLM audit is only 0.550.],
  [Unicode Standard Annex #15; Levenshtein edit distance; repository `_content_axis_v2`.],
)

#pagebreak()

// 7 — NFKC and grounding
#page-head("06 / METHOD", "NFKC compatibility and exact-word grounding")
#method-lead("USED + DIAGNOSTIC", "core", [after strict content, before geometry and typography], [Which compatibility-normalized words match, and which exact text objects are missing?])
#v(6pt)
#paired-crops(
  "REFERENCE · UNMATCHED WORDS", asset("date_reference"), [The reference contains “13. Juli 2026.” Its PDF-word boxes provide coordinates.],
  "CANDIDATE · NO TEXT OBJECT", asset("date_candidate_absent"), [Gray dashed outline is the projected location only. No candidate word box exists.],
  height: 31mm,
)
#v(6pt)
#score-strip((
  ("STRICT F1 ↑", "0.969", "whole document"),
  ("NFKC F1 ↑", "0.969", "compatibility view"),
  ("REF COVERAGE ↑", "0.940", "exact word anchors"),
  ("MISSING", "3 words", "13. · Juli · 2026"),
))
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("How it works", [Words are normalized with NFKC and matched deterministically by exact text plus page/occurrence/center cost. Matched and unmatched PDF words retain their page and rectangle.], kind: "core"),
  note("What it is not", [This is not published CLEval. It gives no partial-character, crop, split, merge, or granularity credit. Repeated words can be assigned ambiguously.], kind: "warn"),
)
#v(5pt)
#method-footer(
  [Higher coverage/F1 is better; the strict NFC view remains authoritative.],
  [Input: PyMuPDF word rectangles and transcription.],
  [NFKC may collapse meaningful glyph distinctions. Never overwrite a strict mismatch with a compatibility match.],
  [Unicode Standard Annex #15; repository `_match_words` and `_text_grounding_axis`.],
)

#pagebreak()

// 8 — numbers/operators
#page-head("07 / METHOD", "Critical inventories: numbers and operators")
#method-lead("USED, PARTIAL", "core", [after general text preservation], [Did the candidate preserve high-risk numeric and mathematical symbols?])
#v(6pt)
#grid(columns: (0.86fr, 1.14fr), gutter: 9pt,
  image-card("MISSING DATE", asset("date_reference"), [Reference text box. Candidate contains no corresponding date text object.], edge: teal, height: 31mm),
  image-card("MALFORMED FORMULA", asset("strict_math_candidate"), [The candidate prints source syntax; the box encloses the exact offending text line.], edge: rust, height: 31mm),
)
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  card([
    #upper-label("NUMBER EXAMPLE")
    #v(3pt)
    #text(size: 18pt, weight: 650)[F1 0.667]
    #v(3pt)
    Precision 1.000 · recall 0.500  
    Missing inventory: *13*, *2026*  
    Whole-document strict F1 remains 0.969.
  ], edge: teal),
  card([
    #upper-label("OPERATOR EXAMPLE")
    #v(3pt)
    #text(size: 18pt, weight: 650)[F1 0.267]
    #v(3pt)
    Missing: $partial$, $nabla$, +, minus, =  
    Added: eight literal carets.  
    The fixed inventory exposes a failure hidden inside prose.
  ], edge: rust),
)
#v(6pt)
#method-footer(
  [Higher F1 is better; exactness requires equal non-empty multisets.],
  [Input: NFKC text; regex numbers and a frozen operator character set.],
  [Units and general punctuation are absent. Regex numbers include page/layout numerals. An empty inventory is “not applicable,” not evidence of fidelity.],
  [Repository `_critical_content_axis`; no published perceptual threshold.],
)

#pagebreak()

// 9 — citations
#page-head("08 / METHOD", "Restricted citation-marker inventory")
#method-lead("USED, GATED", "warn", [critical-content tail, only when citation-bearing text is expected], [Were visible citation markers retained rather than replaced by source keys?])
#v(6pt)
#paired-crops(
  "REFERENCE INLINE CITATIONS", asset("citation_reference"), [The teal box encloses “[1] and [2]”.],
  "GEMINI SOURCE KEYS", asset("citation_candidate"), [The rust box encloses “[teinep] and [STR.55]”.],
  height: 32mm,
)
#v(6pt)
#score-strip((
  ("CITATION F1 ↑", "0.000", "six markers missing"),
  ("STRICT F1 ↑", "0.849", "surrounding prose survives"),
  ("NUMBER F1 ↑", "0.571", "numeric markers lost"),
  ("EXACT", "false", "inventory differs"),
))
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("Why the score is zero", [The six expected numeric markers do not match the six bracketed source-key forms. The paired text boxes show the specific substitution.], kind: "core"),
  note("Regex failure mode", [Bracketed table values can look like citations. In Claude Opus `05_tables_simple_023`, 17 bracketed cells were false citation matches even though the reference had no citations. Applicability must therefore be construct-aware.], kind: "warn"),
)
#v(5pt)
#method-footer(
  [Higher is better; exactness is required when applicable.],
  [Input: a deliberately restricted bracketed-marker regex.],
  [Not a general citation parser. It must be disabled when source/construct evidence does not establish citation applicability.],
  [Repository `_critical_content_axis`; benchmark-defined inventory.],
)

#pagebreak()

// 10 — geometry
#page-head("09 / METHOD", "Matched-word geometry")
#method-lead("CONDITIONAL DIAGNOSTIC", "warn", [after exact NFKC word matching], [When the words survive, how far did their PDF text boxes move or change size?])
#v(6pt)
#paired-crops(
  "REFERENCE ADDRESS BLOCK", asset("geometry_address_reference"), [Exact words occupy the upper-left/mid-page region.],
  "GEMINI ADDRESS BLOCK", asset("geometry_address_candidate"), [The same words move to the extreme upper-right.],
  height: 38mm,
)
#v(6pt)
#score-strip((
  ("MATCH COVERAGE ↑", "0.940", "reference words anchored"),
  ("CENTER q50 ↓", "0.286", "median displacement"),
  ("CENTER q90 ↓", "0.671", "large tail movement"),
  ("CONTENT F1 ↑", "0.969", "movement, not deletion"),
))
#v(6pt)
#note("Definition", [Each matched word center is normalized by its own page width/height. Displacement is Euclidean distance in normalized page coordinates; q50/q90/max summarize the pair. Width and height use absolute log ratios.], kind: "core")
#v(5pt)
#method-footer(
  [Lower displacement and size error are better; higher match coverage is better.],
  [Input: exact NFKC matched PDF words plus page rectangles.],
  [Repeated-token assignment has no runner-up ambiguity margin. Own-canvas normalization can hide physical size differences, so the canvas gate must remain separate.],
  [Repository `_geometry_axis`; no calibrated severity cutoff.],
)

#pagebreak()

// 11 — IoU and size
#page-head("10 / METHOD", "Box overlap and size residuals")
#method-lead("RAW DIAGNOSTIC", "warn", [same matched-word geometry module], [Do the matched word rectangles overlap, and is their scale similar?])
#v(6pt)
#paired-crops(
  "REFERENCE TOKEN · 25.571 pt", asset("typography_reference"), [The dashed box tightly encloses the matched token “(‘have’)”.],
  "GEMINI TOKEN · 11.000 pt", asset("typography_candidate"), [The solid box encloses the same extracted token at much smaller scale.],
  height: 39mm,
)
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("Useful raw residual", [$|log(25.571 / 11.000)| = 0.843565$. The size ratio is directly interpretable for this matched text sample.], kind: "core"),
  note("Rejected collapsed tail", [Token box IoU q10 is *0 for all 156 Gemini outputs*. That tail statistic separates nothing in this corpus and is not used as a model grade.], kind: "stop"),
)
#v(7pt)
#score-strip((
  ("FONT-SIZE q90 ↓", "0.844", "large scale error"),
  ("BASELINE q90 ↓", "0.449", "vertical mismatch"),
  ("WORD COVERAGE ↑", "0.975", "text mostly matched"),
))
#v(5pt)
#method-footer(
  [Higher IoU is better; lower absolute log size ratio is better.],
  [Input: exact matched word rectangles and extracted font size.],
  [IoU is brittle when even a correct word shifts. Report distributions and concrete pairs; do not collapse the all-zero tail into a score.],
  [Standard rectangle IoU; repository `_geometry_axis`.],
)

#pagebreak()

// 12 — Text-LTSim
#page-head("11 / METHOD", "Text-LTSim: text-block transport only")
#method-lead("CONDITIONAL TRIAL", "warn", [after text-block extraction on paired non-empty pages], [How much spatial transport is needed to align the two sets of extracted text blocks?])
#v(6pt)
#paired-crops(
  "AUTOMATED FLOW · REFERENCE", asset("ltsim_flow_reference"), [Amber box is one extracted block in the largest-cost transport contribution.],
  "AUTOMATED FLOW · CANDIDATE", asset("ltsim_flow_candidate"), [Amber box is the block receiving that transported mass.],
  height: 35mm,
)
#v(6pt)
#grid(columns: (1.12fr, 0.88fr), gutter: 8pt,
  note("Current implementation", [Each page uses non-empty extracted text blocks, uniform mass, label similarity 1 because every element is “text,” GIoU-derived spatial cost, optimal transport EMD, and $"Text-LTSim" = exp(-"EMD")$.], kind: "core"),
  card([
    #upper-label("THIS PAGE")
    #v(3pt)
    #text(size: 20pt, weight: 650)[0.671]
    #v(3pt)
    EMD 0.400  
    shown flow: mass 0.200 × cost 0.495
  ], edge: amber),
)
#v(6pt)
#note("What the boxes prove—and expose", [The shown transport contribution is real evaluator evidence. It routes mass from “In Erwartung einer Einladung” to “Petra Mustermann”; because uniform optimal transport is spatial rather than semantic matching, the flow can connect unrelated text. Also, the all-text cost is bounded by 0.5, so $exp(-"EMD")$ cannot fall below $exp(-0.5) approx 0.607$.], kind: "warn")
#v(5pt)
#method-footer(
  [Higher is better within the same extraction policy.],
  [Input: paired pages with non-empty generic text blocks.],
  [Measures text geometry and segmentation—not formula, table, figure, or semantic layout. Uniform mass makes producer-dependent block splitting consequential.],
  [LTSim, 2024; GIoU, 2019; repository `_text_ltsim_axis`.],
)

#pagebreak()

// 13 — block OT and relations
#page-head("12 / METHOD", "Benchmark block transport and layout relations")
#method-lead("DIAGNOSTIC ADAPTATIONS", "warn", [beside Text-LTSim, never under its published name], [Can coarse block-level residuals help explain a candidate without claiming semantic layout fidelity?])
#v(7pt)
#grid(columns: (1fr, 1fr), gutter: 9pt,
  card([
    #pill("BLOCK OT", kind: "warn")
    #v(6pt)
    Mass is proportional to normalized character count. Cost is benchmark-defined as *0.65 geometry + 0.35 content* across page-stacked blocks. It reports combined, geometry, and content similarities plus the largest mass × cost flows.
    #v(7pt)
    #score-strip((("GEOMETRY ↑", "0.440", "moved letter"), ("CONTENT ↑", "0.898", "text survives")))
  ], edge: amber),
  card([
    #pill("LAYOUT RELATIONS", kind: "warn")
    #v(6pt)
    Content-matched block centers receive one coarse relation—left, right, above, or below. Agreement and mismatch examples are emitted.
    #v(7pt)
    #note("Status", [No dedicated controlled validation or manual-alignment result exists. Matching uses a low 0.25 content threshold.], kind: "warn")
  ], edge: amber),
)
#v(8pt)
#paired-crops(
  "REFERENCE TEXT BLOCK", asset("geometry_address_reference"), [The block’s words are preserved.],
  "CANDIDATE TEXT BLOCK", asset("geometry_address_candidate"), [Its location changes; geometry falls while content remains high.],
  height: 31mm,
)
#v(6pt)
#method-footer(
  [Higher similarities/relations agreement are better.],
  [Input: extracted PDF blocks and content-based matches.],
  [These are benchmark adaptations, not published LTSim or PaIRS. Page stacking and block segmentation are producer-dependent.],
  [LTSim/GIoU only as primitives; repository `_block_transport_axis` and `_layout_relations_axis`.],
)

#pagebreak()

// 14 — pagination
#page-head("13 / METHOD", "Pagination: exact page count and raw boundaries")
#method-lead("COUNT USED · BOUNDARIES CONDITIONAL", "warn", [independent page-structure module], [Was content omitted, or was it merely moved across a page break?])
#v(6pt)
#paired-crops(
  "REFERENCE · PAGE 2", asset("pagination_reference"), [Expression 5(ii) appears on the second reference page.],
  "GEMINI · PAGE 1", asset("pagination_candidate"), [The same text appears on the only candidate page.],
  height: 34mm,
)
#v(6pt)
#score-strip((
  ("PAGE DELTA", "−1", "2 reference → 1 candidate"),
  ("BOUNDARY F1 ↑", "0.000", "one break missed"),
  ("ASSIGNMENT ↑", "0.868", "matched blocks on same index"),
  ("NUMBER F1 ↑", "0.974", "content mostly retained"),
))
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("Objective finding", [The paired text boxes prove Expression 5 was reflowed rather than deleted. Exact page count is a hard fact and the missed boundary is concrete evidence.], kind: "core"),
  note("Raw-diagnostic warning", [The current code emits page-boundary F1 without the planned confidence gate. It can equal 1 vacuously when neither side exposes a break.], kind: "warn"),
)
#v(5pt)
#method-footer(
  [Page delta 0 is exact; higher assignment/boundary values are better.],
  [Input: page counts and content-matched adjacent blocks.],
  [Boundary evidence inherits block matching and extraction order errors. Report TP/FP/FN and the exact block pair, never F1 alone.],
  [Repository `_pagination_axis`; no calibrated perceptual threshold.],
)

#pagebreak()

// 15 — reading order
#page-head("14 / METHOD", "Reading-order Kendall tau")
#method-lead("RAW CONDITIONAL DIAGNOSTIC", "warn", [after content-based block matching], [Does the extracted candidate block sequence preserve the reference pairwise order?])
#v(7pt)
#grid(columns: (1.05fr, 0.95fr), gutter: 10pt,
  [
    #note("Definition", [For $N$ matched blocks and $I$ inversions, $tau = 1 - 4 I/(N(N-1))$. Higher is better; coverage and inversion examples must accompany the value.], kind: "core")
    #v(7pt)
    #score-strip((
      ("TAU ↑", "0.824", "example pair"),
      ("INVERSIONS ↓", "62", "matched order pairs"),
      ("REF COVERAGE ↑", "0.950", "38 blocks matched"),
    ))
  ],
  [
    #card([
      #upper-label("ACTUAL EXTRACTED BLOCK PAIR")
      #v(6pt)
      #box(width: 100%, stroke: (dash: "dashed", thickness: 1.5pt, paint: teal), inset: 6pt)[“1 Expressions” → “Expression 1. The following expression …”]
      #v(5pt)
      #box(width: 100%, stroke: 1.5pt + rust, inset: 6pt)[“r + s” → “Expressions Expression 1. The following expression …”]
      #v(5pt)
      #text(size: 9.3pt, fill: muted)[This reported inversion also exposes a dubious block correspondence; the text samples are shown exactly rather than hidden behind tau.]
    ], edge: amber)
  ],
)
#v(8pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("Where it helps", [Concrete inversions can flag a column or algorithm block that was extracted in a different sequence.], kind: "core"),
  note("Why it stays raw", [PyMuPDF geometric extraction order is not logical/accessibility order. Current code also lacks the planned match-count, coverage, and ambiguity gates.], kind: "warn"),
)
#v(6pt)
#method-footer(
  [Higher tau is better within a declared order policy.],
  [Input: matched block indices in extracted order.],
  [Never call this authoritative semantic reading order. Low-coverage matches can produce deceptively high tau.],
  [Lapata, 2006, doi:10.1162/coli.2006.32.4.471; PyMuPDF extraction docs.],
)

#pagebreak()

// 16 — typography
#page-head("15 / METHOD", "Typographic metadata diagnostics")
#method-lead("CONDITIONAL DIAGNOSTIC", "warn", [after exact-word grounding], [Did matched text keep similar extracted size, baseline, font metadata, and style flags?])
#v(6pt)
#paired-crops(
  "REFERENCE · 25.571 pt", asset("typography_reference"), [The dashed box encloses the matched PDF word.],
  "GEMINI · 11.000 pt", asset("typography_candidate"), [The candidate’s exact word is less than half the extracted font size.],
  height: 39mm,
)
#v(6pt)
#score-strip((
  ("SIZE q90 ↓", "0.844", "|log size ratio|"),
  ("BASELINE q90 ↓", "0.449", "box-bottom displacement"),
  ("STYLE COVERAGE ↑", "0.779", "grounded words"),
  ("GEMINI AUC", "0.535", "unstable LLM audit link"),
))
#v(6pt)
#note("What is reported", [Font-size error; cleaned font-name and exact color agreement; bold/italic/serif/monospace flag agreement; box-bottom displacement used as a baseline proxy; and paired mismatch boxes.], kind: "core")
#v(5pt)
#method-footer(
  [Lower size/baseline error and higher agreement are better.],
  [Input: exact-word pairs with PyMuPDF span metadata.],
  [Subset font names, aliases, flags, colors, and box bottoms are producer metadata—not guaranteed visual equivalence or true baselines.],
  [PDF Reference 1.7; PyMuPDF extraction docs; benchmark-defined diagnostics.],
)

#pagebreak()

// 17 — SSIM
#page-head("16 / METHOD", "Same-canvas SSIM")
#method-lead("CONDITIONAL RASTER DIAGNOSTIC", "warn", [after an exact physical-canvas and raster-grid gate], [On directly comparable pages, how similar are the grayscale local image statistics?])
#v(6pt)
#paired-crops(
  "REFERENCE · PAGE 2", asset("ssim_collision_reference"), [Manual text-region box: normal lower rows and caption.],
  "GEMINI · PAGE 2", asset("ssim_collision_candidate"), [Manual text-region box: rows and caption collide into an unreadable band.],
  height: 38mm,
)
#v(6pt)
#score-strip((
  ("PAGE 1 SSIM ↑", "0.955", "visually close"),
  ("PAGE 2 SSIM ↑", "0.362", "collision band"),
  ("PAGE 3 SSIM ↑", "0.358", "collision band"),
  ("MACRO SSIM ↑", "0.558", "same canvas"),
))
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("Eligibility", [Identical physical page points, raster dimensions, renderer, grayscale conversion, and DPI; the candidate is never resized for SSIM. Only 2/156 Gemini pairs were eligible.], kind: "core"),
  note("Localization warning", [The boxes above are manual text evidence. The evaluator retains no local SSIM map; its `registered_difference_bbox` comes from tolerant ink and must not be called an SSIM box.], kind: "warn"),
)
#v(5pt)
#method-footer(
  [Higher is better; identity is 1.],
  [Input: same-canvas grayscale rasters under frozen settings.],
  [White background can dominate. Claude Opus `05_tables_simple_005` scored 0.571—nearly the severe example’s 0.558—yet its audit found no clear defect. SSIM is not a severity grade.],
  [Wang et al., 2004, doi:10.1109/TIP.2003.819861.],
)

#pagebreak()

// 18 — four-scale adaptation
#page-head("17 / METHOD", "Four-scale SSIM geometric-mean adaptation")
#method-lead("BENCHMARK-DEFINED DIAGNOSTIC", "warn", [beside same-canvas SSIM on eligible pairs], [Does the raster resemblance persist after fixed downsampling?])
#v(9pt)
#grid(columns: (1.15fr, 0.85fr), gutter: 12mm,
  [
    #heading(level: 2)[Current construction]
    At scale factors 1, 2, 4, and 8, compute SSIM independently. Remap each value as $S'_s = "clip"(("SSIM"_s + 1)/2)$, then report
    $S_("4scale") = exp((1/4) sum_s log S'_s)$.
    #v(8pt)
    #grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 7pt, align: (center, bottom),
      [#box(width: 41mm, height: 30mm, fill: white, stroke: 1.5pt + teal)[#align(center + horizon)[1×]]],
      [#box(width: 31mm, height: 23mm, fill: white, stroke: 1.5pt + teal)[#align(center + horizon)[2×]]],
      [#box(width: 23mm, height: 17mm, fill: white, stroke: 1.5pt + teal)[#align(center + horizon)[4×]]],
      [#box(width: 16mm, height: 12mm, fill: white, stroke: 1.5pt + teal)[#align(center + horizon)[8×]]],
    )
  ],
  [
    #fact("EXAMPLE", "0.755", note: "unregistered four-scale", kind: "warn")
    #v(7pt)
    #fact("TRANSLATED", "0.761", note: "after optional registration", kind: "warn")
    #v(7pt)
    #note("Same gate", [Only 2/156 Gemini pairs were eligible.], kind: "warn")
  ],
)
#v(9pt)
#note("Not canonical MS-SSIM", [Published MS-SSIM combines luminance at the coarsest scale and contrast/structure across scales with fixed weights. Independently averaging four SSIM values is a different metric and is labeled accordingly.], kind: "stop")
#v(6pt)
#method-footer(
  [Higher is better among eligible same-canvas pairs.],
  [Input: the same frozen grayscale rasters at four scales.],
  [No human calibration; not canonical MS-SSIM; inherits every same-canvas SSIM limitation.],
  [Wang, Simoncelli & Bovik, 2003; repository `_multiscale_ssim_diagnostic`.],
)

#pagebreak()

// 19 — tolerant ink
#page-head("18 / METHOD", "Two-pixel tolerant binary-ink overlap")
#method-lead("LEGACY DIAGNOSTIC", "warn", [broad raster difference finder, not a physical-layout score], [How much thresholded ink overlaps after canvas resizing and optional translation?])
#v(6pt)
#paired-crops(
  "REFERENCE TEXT SCALE", asset("typography_reference"), [Matched word at 25.571 pt.],
  "GEMINI TEXT SCALE", asset("typography_candidate"), [Matched word at 11.000 pt; real miniaturization remains after registration.],
  height: 36mm,
)
#v(6pt)
#score-strip((
  ("UNREGISTERED F1 ↑", "0.093", "after forced resize"),
  ("REGISTERED F1 ↑", "0.296", "translation helps"),
  ("CANVAS EXACT", "0.000", "Letter vs A4"),
  ("USEFUL BOXES", "43 / 156", "Gemini audit"),
))
#v(6pt)
#note("Definition", [Threshold grayscale at 245; dilate each binary ink mask by two pixels; compute symmetric precision, recall, and F1. The legacy path first resizes the candidate to the reference raster and can translation-register it.], kind: "core")
#v(5pt)
#method-footer(
  [Higher overlap is better only under the frozen rendering transform.],
  [Input: resized thresholded rasters; optional translation.],
  [Canvas was judged a confound in 145/156 Gemini cases. The one residual enclosure is often broad; it is neither physical layout evidence nor SSIM localization.],
  [Benchmark-defined diagnostic; repository `_raster_axis`.],
)

#pagebreak()

// 20 — CLEval
#page-head("19 / METHOD", "Official CLEval remains pending")
#method-lead("PENDING CONFORMANCE", "stop", [future replacement/complement to exact-word grounding], [Can character-level recognition, split, merge, miss, and granularity errors be scored correctly?])
#v(6pt)
#paired-crops(
  "REFERENCE TABLE TEXT", asset("corrupt_row_reference"), [Correct rows 8–9; teal box encloses the actual table text sample.],
  "CLAUDE OPUS TABLE TEXT", asset("corrupt_row_candidate"), [Literal Typst fragments and bracketed values appear inside the boxed row.],
  height: 37mm,
)
#v(6pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  card([
    #pill("CURRENT")
    #v(5pt)
    Exact NFKC word equality + Hungarian assignment  
    Partial character credit: *none*  
    Split/merge fields: *null*  
    This Claude example: strict F1 *0.789*
  ], edge: rule),
  card([
    #pill("REQUIRED FOR CLEVAL", kind: "stop")
    #v(5pt)
    Official-format word polygons + transcriptions  
    Pseudo-character accounting  
    One-to-many / many-to-one handling  
    Conformance tests against official code
  ], edge: rust),
)
#v(7pt)
#method-footer(
  [Published CLEval P/R/H-mean are higher-better.],
  [Input: official text polygons and transcriptions.],
  [No CLEval score is released. A PDF-character version would be a separately named adaptation and requires crop/split/merge/insertion/deletion/overlap tests.],
  [Baek et al., 2020, doi:10.1109/CVPRW50498.2020.00290; official `clovaai/CLEval`.],
)

#pagebreak()

// 21 — structures
#page-head("20 / METHOD", "Structure metrics abstain when representation is absent")
#method-lead("ABSTAIN", "stop", [specialized tail after common extraction], [Do both PDFs expose the validated structures required by the published metric?])
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 8pt,
  card([
    #pill("GriTS", kind: "stop")
    #v(6pt)
    *Needs:* table grid, row/column spans, cell boxes, and cell text on both sides.  
    *Current input:* generic PDF words/blocks.  
    *Status:* 0/156 Gemini pairs scored.
    #v(6pt)
    #image(asset("corrupt_row_reference"), width: 100%, height: 27mm, fit: "contain")
    #text(size: 8.8pt, fill: muted)[A boxed row is still not a cell-grid matrix.]
  ], edge: rust),
  card([
    #pill("TEDS", kind: "stop")
    #v(6pt)
    *Needs:* a deterministic normalized HTML table tree with spans and cell content.  
    *Current input:* no common HTML tree.  
    *Status:* 0/156 Gemini pairs scored.
    #v(9pt)
    #box(width: 100%, stroke: (dash: "dashed", thickness: 1.5pt, paint: muted), inset: 9pt)[
      table → thead/tbody → tr → td[rowspan, colspan, text]
    ]
  ], edge: rust),
  card([
    #pill("SEMANTIC LAYOUT / FORMULA / FIGURE", kind: "stop")
    #v(6pt)
    *Needs:* validated common labels, boxes/masks, or compatible tokenized formula representations.  
    *Current input:* all blocks labeled only “text.”  
    *Status:* all three specialized axes abstain.
    #v(6pt)
    #image(asset("strict_math_reference"), width: 100%, height: 27mm, fit: "contain")
  ], edge: rust),
)
#v(8pt)
#note("Abstention is evidence about evidence", [It means the required representation is unavailable—not that the candidate scored zero. Detector or parser failure must not be silently attributed to the conversion.], kind: "core")
#v(5pt)
#text(size: 9pt, fill: muted)[Sources: Smock, Pesala & Abraham, GriTS, 2023 · Zhong, ShafieiBavani & Jimeno Yepes, TEDS, 2020 · Otani et al., LTSim, 2024 · Wang et al., character detection matching for formulas, 2025.]

#pagebreak()

// 22 — no scalar
#page-head("21 / OUTPUT", "The released object is an evidence packet, not a scalar")
#method-lead("NO AGGREGATION", "stop", [final output contract], [How can a result remain comparable without allowing one axis to cancel another?])
#v(9pt)
#grid(columns: (1.1fr, 0.9fr), gutter: 12mm,
  [
    #card([
      #upper-label("PER-PDF-PAIR PACKET")
      #v(7pt)
      #table(columns: (42mm, 1fr),
        [*facts*], [hashes · protocol · page count · page points],
        [*content*], [strict/NFKC scores · missing/extra values],
        [*grounding*], [coverage · matched/unmatched text boxes],
        [*spatial*], [raw quantiles · block flows · inversion examples],
        [*conditional*], [eligibility · score · reason for abstention],
        [*structures*], [representation status; usually abstain],
        [*aggregate*], [`null`],
      )
    ], edge: teal)
  ],
  [
    #fact("UNIVERSAL SCORE", "rejected", note: "current release decision", kind: "stop")
    #v(8pt)
    #note("Why", [Axes answer different questions, have different ranges, and abstain differently. No transformations, weights, or missingness rules have been validated against a human-rating target.], kind: "warn")
    #v(8pt)
    #note("Comparison rule", [Read hard failures first; then compare applicable axes side by side with coverage and visual text evidence.], kind: "core")
  ],
)
#v(8pt)
#text(size: 9pt, fill: muted)[Methodological reference: OECD/JRC, *Handbook on Constructing Composite Indicators*, 2008. The handbook does not prohibit composites; it makes their normalization, weighting, compensability, missing-data, and sensitivity assumptions explicit.]

#pagebreak()

// 23 — validation design
#page-head("22 / VERIFICATION", "Four layers of current verification")
#v(4pt)
#grid(columns: (1fr, 1fr), gutter: 9pt,
  card([
    #pill("1 · IDENTITY", kind: "core")
    #v(6pt)
    *157 reference/self pairs*  
    All nine implemented identity checks passed. This confirms exact optima for those checks—not every field in the evaluator.
  ], edge: teal),
  card([
    #pill("2 · CONTROLLED PANEL", kind: "core")
    #v(6pt)
    *628 retained severity-2 mutations*  
    Four cases per document, rescored with v2 and manually reviewed after unblinding for validity, visibility, target box, and predicted-box usefulness.
  ], edge: teal),
  card([
    #pill("3 · SEVERITY SERIES", kind: "warn")
    #v(6pt)
    *471 block-right cases*  
    Three severities over 157 sources. Text-LTSim decreased monotonically in all documents, but the median severity-1→3 drop was only 0.00183 and many middle cases were not visibly valid.
  ], edge: amber),
  card([
    #pill("4 · REAL MODEL OUTPUTS", kind: "warn")
    #v(6pt)
    *156 Gemini + 21 four-way candidates*  
    Every frozen Gemini PDF received an LLM visual inspection; seven complete Reference/Gemini/Sonnet/Opus sets were audited for metric/defect alignment.
  ], edge: amber),
)
#v(10pt)
#note("Evidence boundary", [There are no human ratings. Controlled mutation truth and repeated researcher LLM audits verify mechanical behavior and explanatory consistency; they do not establish human perceptual utility or a model leaderboard.], kind: "stop")

#pagebreak()

// 24 — augmentation design
#page-head("23 / VERIFICATION", "Controlled augmentation was a smoke test, not ground truth")
#v(5pt)
#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 7pt,
  card([#pill("TEXT DELETION", kind: "core") #v(6pt) #text(size: 20pt, weight: 650)[157] #v(4pt) #text(size: 9.5pt, fill: muted)[content cases; remove selected text]], edge: teal),
  card([#pill("BLOCK RIGHT", kind: "core") #v(6pt) #text(size: 20pt, weight: 650)[157] #v(4pt) #text(size: 9.5pt, fill: muted)[layout cases; shift a selected block]], edge: teal),
  card([#pill("LOCAL OCCLUSION", kind: "core") #v(6pt) #text(size: 20pt, weight: 650)[157] #v(4pt) #text(size: 9.5pt, fill: muted)[content + appearance]], edge: teal),
  card([#pill("CONSTRUCT-AWARE", kind: "warn") #v(6pt) #text(size: 20pt, weight: 650)[157] #v(4pt) #text(size: 9.5pt, fill: muted)[math/table/list/figure/crossref/etc.]], edge: amber),
)
#v(9pt)
#grid(columns: (1fr, 1fr), gutter: 9pt,
  [
    #heading(level: 2)[What succeeded]
    On the 530 mutations later judged valid and visible, the expected module’s diagnostic smoke trigger fired in 100% of cases. Target boxes and labels matched the generating transform by construction.

    #v(6pt)
    #note("Important wording", [These thresholds were change-detector smoke rules, not pass/fail quality bands.], kind: "core")
  ],
  [
    #heading(level: 2)[What failed]
    98 mutations were invalid or visually indistinguishable after unblinding. Yet no-op trigger rates were:
    #v(5pt)
    #table(columns: (1fr, auto),
      [content], [40.8%],
      [layout], [82.7%],
      [raster residual], [99.0%],
      [typography], [16.3%],
    )
  ],
)
#v(8pt)
#note("Conclusion", [Automatic difference sensitivity is not visible-defect severity. The current release keeps raw evidence and removes any claim that the smoke thresholds are quality grades.], kind: "warn")

#pagebreak()

// 25 — box and repeat audit
#page-head("24 / VERIFICATION", "Manual box review and repeat-audit stability")
#v(5pt)
#grid(columns: (1fr, 1fr), gutter: 10pt,
  card([
    #pill("BOX USEFULNESS", kind: "core")
    #v(7pt)
    #score-strip((
      ("FULL", "496", "useful"),
      ("PARTIAL", "23", "some value"),
      ("NONE", "109", "not useful"),
    ))
    #v(7pt)
    The prediction was fully useful in 79.0% of all 628 cases. This is a localization audit, not a statement that every underlying mutation was visible.
  ], edge: teal),
  card([
    #pill("SECOND BLIND AUDIT", kind: "warn")
    #v(7pt)
    #score-strip((
      ("PANEL / ABSTAIN", "83.7%", "agreement"),
      ("KAPPA", "0.734", "decision stability"),
      ("AXIS LABEL", "14.6%", "82 both-commit"),
    ))
    #v(7pt)
    The panel decision was fairly stable; the old defect-axis labels were not. The current report therefore treats text boxes and raw evidence as primary and broad axis labels as provisional.
  ], edge: amber),
)
#v(10pt)
#note("Researcher judgment policy", [Every visual example in this report separates three provenances: evaluator word/block evidence, manual text-region evidence, and projected blank regions. Broad raster enclosures are not reused as if they explained text or SSIM.], kind: "core")

#pagebreak()

// 26 — limitations and next work
#page-head("25 / CURRENT LIMITS", "What can be concluded now—and what comes next")
#grid(columns: (1fr, 1fr), gutter: 10pt,
  [
    #heading(level: 2)[Defensible now]
    - Exact page and canvas facts.
    - Literal extracted-text and partial critical-inventory evidence.
    - Conditional matched-word boxes, displacement, size, and typography metadata.
    - Text-block transport with its compressed range disclosed.
    - Raw page/order/raster diagnostics with gates and abstentions.
    - Side-by-side model examples; no cross-protocol ranking.

    #v(7pt)
    #note("Not defensible now", [A universal grade, human preference prediction, structure score without structure extraction, or “best model” claim from the seven heterogeneous four-way runs.], kind: "stop")
  ],
  [
    #heading(level: 2)[Next research sequence]
    #enum(
      [Add construct applicability labels so citation/table/formula modules gate correctly.],
      [Conformance-test official CLEval on synthetic split/merge/crop/character cases.],
      [Add repeated-token ambiguity margins and enforce coverage gates for order/pagination.],
      [Build validated common table-cell and formula-token representations before enabling GriTS/TEDS/CDM-like work.],
      [Create a same-canvas raster microbenchmark and retain local maps only when their provenance is exact.],
      [Keep the vector; defer any scalar calibration until an external rating target exists.],
    )
  ],
)
#v(9pt)
#note("Immediate operational rule", [For current experiments, a candidate is reviewed as an evidence vector: check hard facts and critical mismatches first, inspect boxed text evidence next, then use conditional diagnostics to explain—not override—the visible comparison.], kind: "core")

#let tiny-metric(label, value) = [
  #upper-label(label)
  #v(1pt)
  #text(size: 11pt, weight: 650)[#value]
]
#let reference-panel(sample, asset-name, target-page, page-count, specimen) = card([
  #grid(columns: (1fr, auto), align: (left, horizon),
    [#text(size: 13pt, weight: 650)[Reference]],
    [#pill("TARGET p" + str(target-page), kind: "core")],
  )
  #v(4pt)
  #align(center)[#image(asset(asset-name), width: 100%, height: 46mm, fit: "contain")]
  #v(4pt)
  #grid(columns: (26mm, 1fr), gutter: 5pt,
    tiny-metric("PAGES", str(page-count)),
    [#upper-label("BOXED TEXT") #v(1pt) #text(size: 9.2pt, fill: muted)[#specimen]],
  )
], edge: teal, inset: 8pt)
#let candidate-panel(sample, role, model, asset-name, target-page) = {
  let row = score-for(sample, role)
  let ssim = if row.unregistered_ssim == "" { "abstain" } else { num(row.unregistered_ssim) }
  card([
    #grid(columns: (1fr, auto), align: (left, horizon),
      [#text(size: 13pt, weight: 650)[#model]],
      [#pill("TARGET p" + str(target-page), kind: "warn")],
    )
    #v(4pt)
    #align(center)[#image(asset(asset-name), width: 100%, height: 46mm, fit: "contain")]
    #v(4pt)
    #grid(columns: (1fr, 1fr, 1fr, 1fr, 1fr), gutter: 4pt,
      tiny-metric("TEXT F1 ↑", num(row.strict_word_f1)),
      tiny-metric("LTSIM ↑", num(row.text_ltsim_page_macro)),
      tiny-metric("CENTER ↓", num(row.token_center_displacement_q90)),
      tiny-metric("PAGES", row.reference_page_count + "→" + row.candidate_page_count),
      tiny-metric("SSIM ↑", ssim),
    )
  ], edge: rust, inset: 8pt)
}
#let detail-card(title, asset-name, provenance, caption, kind: "candidate") = {
  let edge = if kind == "reference" { teal } else if kind == "automatic" { amber } else { rust }
  card([
    #grid(columns: (1fr, auto), align: (left, horizon),
      [#text(size: 12pt, weight: 650)[#title]],
      [#pill(provenance, kind: if kind == "automatic" { "warn" } else { "neutral" })],
    )
    #v(4pt)
    #align(center)[#image(asset(asset-name), width: 100%, height: 30mm, fit: "contain")]
    #v(4pt)
    #text(size: 9.4pt, fill: muted)[#caption]
  ], edge: edge, inset: 8pt)
}

#pagebreak()

// 27 — comparison contract
#page-head("26 / MODEL EVIDENCE", "How to read the seven four-way comparisons", deck: [Every complete Reference/Gemini/Sonnet/Opus set is included. The pages test evaluator evidence—not model capability.])
#grid(columns: (1fr, 1fr), gutter: 11mm,
  [
    #heading(level: 2)[Box grammar]
    #grid(columns: (auto, 1fr), gutter: 8pt, row-gutter: 8pt, align: (left, horizon),
      [#box(width: 17mm, height: 6mm, stroke: (dash: "dashed", thickness: 2pt, paint: teal))], [*Reference text region* — tight PDF word/line/block extent.],
      [#box(width: 17mm, height: 6mm, stroke: 2pt + rust)], [*Candidate text region* — tight corresponding text or localized candidate evidence.],
      [#box(width: 17mm, height: 6mm, stroke: 2pt + amber)], [*Evaluator text evidence* — used only when the box comes directly from NFKC unmatched-word or transport JSON.],
      [#box(width: 17mm, height: 6mm, stroke: (dash: "dashed", thickness: 2pt, paint: muted))], [*Expected blank region* — no candidate text object; never presented as a detected box.],
    )
    #v(8pt)
    #note("Score strip", [Text F1 and Text-LTSim: higher is better. Center q90: lower is better. Pages shows reference→candidate. SSIM says “abstain” unless physical canvas and raster grid match. No continuous cutoff is calibrated.], kind: "core")
  ],
  [
    #heading(level: 2)[Protocol boundary]
    #table(columns: (35mm, 1fr),
      [*Gemini*], [Source-only conversion; no reference page images; selected stored prompt-stage output.],
      [*Claude*], [Heterogeneous one-turn or agentic runs; six of seven table/figure cases used iterative visual feedback; effort and revision policies differ.],
      [*Reference*], [Accepted pdfLaTeX benchmark PDF.],
    )
    #v(8pt)
    #note("Allowed conclusion", [A score is useful when its exact evidence agrees with the visible text comparison and its prerequisites hold.], kind: "core")
    #v(7pt)
    #note("Prohibited conclusion", [Do not rank the models from these seven sets. Protocol differences, no human ratings, and conditional metrics make that claim invalid.], kind: "stop")
  ],
)

#pagebreak()

// 28 — seven-reference scorecard
#page-head("27 / SCORECARD", "Seven-reference exploratory scorecard", deck: [Gemini, two Claude models, and three deterministic engines on the exact same seven references. Counts and metric medians are kept separate.])
#note("Descriptive comparison—not a model leaderboard", [Claude mixes one one-turn run with six agentic visual-feedback runs; Gemini is source-only and adaptively selected; the engines are deterministic. The shared documents make the rows inspectable, but the protocols are not equivalent.], kind: "stop")
#v(8pt)
#scorecard-table(scorecards.overlap_7)
#v(8pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Full denominator", [Compiled and page-exact counts use all *7* references. A failed conversion remains visible instead of disappearing from the scorecard.], kind: "core"),
  note("Conditional medians", [Strict/NFKC F1, reference coverage, center q90, Text-LTSim, and SSIM are document medians over compiled PDFs only.], kind: "core"),
  note("SSIM eligibility", [SSIM is reported only when physical canvas and raster grid match. “— / 0 eligible” is an abstention, not a zero.], kind: "warn"),
)
#v(7pt)
#text(size: 9pt, fill: muted)[Shared references: 04_math_aligned_014 · 05_tables_simple_005 · 05_tables_simple_021 · 05_tables_simple_023 · 06_tables_moderate_010 · 07_figures_captions_007 · 09_algorithms_003. All scores use evaluator v2 at 96 DPI.]

#pagebreak()

// 29 — full-corpus scorecard
#page-head("28 / SCORECARD", "All 157 references · Gemini and engines", deck: [One development snapshot covering the complete accepted corpus. Compile coverage stays in the denominator; continuous fidelity axes are conditional on compilation.])
#scorecard-table(scorecards.full_157)
#v(9pt)
#grid(columns: (1fr, 1fr), gutter: 8pt,
  note("What the table supports", [It directly compares output availability, exact pagination, exact physical canvas, literal text preservation, matched-text movement, and text-layout transport. Arrows show direction; no hidden weights combine them.], kind: "core"),
  note("What the table does not support", [The medians use each system’s compiled subset, so they are not a paired rank. SSIM mostly abstains because engine and reference canvases differ. No universal quality score is inferred.], kind: "warn"),
)
#v(8pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  fact("UNIVERSE", "157", note: "accepted references; failures retained", kind: "core"),
  fact("ENGINE PAIRS", "393", note: "all compiled outputs rescored uniformly", kind: "core"),
  fact("EVALUATOR", "v2 / 96 DPI", note: "same implementation and settings", kind: "core"),
)
#v(8pt)
#note("Publication boundary", [Gemini is an adaptive v0–v3 development cascade, not a frozen held-out run; one selected candidate also originated in a provider-error response and must be rerun. Treat this as the current system scorecard, not the paper leaderboard.], kind: "stop")

#pagebreak()

// 30–31 — math014
#page-head("29 / FOUR-WAY OVERVIEW", "04_math_aligned_014 · two pages compressed into one", deck: [The box follows the same Expression 5 text from reference page 2 into candidate page 1.])
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  reference-panel("04_math_aligned_014", "grid_math014_reference", 2, 2, [Expression 5(ii) on reference page 2.]),
  candidate-panel("04_math_aligned_014", "gemini", "Gemini 3.1 Flash Lite", "grid_math014_gemini", 1),
  candidate-panel("04_math_aligned_014", "claude_sonnet", "Claude Sonnet 4.6", "grid_math014_sonnet", 1),
  candidate-panel("04_math_aligned_014", "claude_opus", "Claude Opus 4.7", "grid_math014_opus", 1),
)
#v(5pt)
#text(size: 9pt, fill: muted)[Box type: MANUAL_TEXT, verified against PDF text. LTSim scores only the one paired page and abstains on the unpaired second reference page.]

#pagebreak()
#page-head("30 / BOXED EVIDENCE", "04_math_aligned_014 · the same text crosses the page boundary")
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  detail-card("Reference · page 2", "detail_math014_reference", "MANUAL_TEXT", [Expression 5(ii) is present on the second reference page.], kind: "reference"),
  detail-card("Gemini · page 1", "detail_math014_gemini", "MANUAL_TEXT", [The same line appears much earlier on the only candidate page.]),
  detail-card("Sonnet · page 1", "detail_math014_sonnet", "MANUAL_TEXT", [Same content; two pages are compressed into one.]),
  detail-card("Opus · page 1", "detail_math014_opus", "MANUAL_TEXT", [Same page-count failure despite preserving the section number.]),
)
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Gemini", [Page delta *−1* · boundary F1 *0* · center q90 *0.546*. Strict F1 *0.431* rises to NFKC *0.618*, so extraction representation contributes to the low content value.], kind: "warn"),
  note("Sonnet", [Page delta *−1* · boundary F1 *0* · center q90 *0.700*. The visually evident claim is pagination, not a model-quality rank from LTSim *0.705*.], kind: "warn"),
  note("Opus", [Page delta *−1* · boundary F1 *0* · center q90 *0.630*. It preserves “1 Expressions,” but still compresses the complete document.], kind: "warn"),
)

#pagebreak()

// 32–33 — table005
#page-head("31 / FOUR-WAY OVERVIEW", "05_tables_simple_005 · clean final row versus bottom collision", deck: [The box encloses row 47 in each table-1 page; Gemini’s row shares the bottom band with other rows and the caption.])
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  reference-panel("05_tables_simple_005", "grid_table005_reference", 1, 2, [Clean final table row on page 1.]),
  candidate-panel("05_tables_simple_005", "gemini", "Gemini 3.1 Flash Lite", "grid_table005_gemini", 2),
  candidate-panel("05_tables_simple_005", "claude_sonnet", "Claude Sonnet 4.6", "grid_table005_sonnet", 1),
  candidate-panel("05_tables_simple_005", "claude_opus", "Claude Opus 4.7", "grid_table005_opus", 1),
)

#pagebreak()
#page-head("32 / BOXED EVIDENCE", "05_tables_simple_005 · high text F1 does not prevent a collision")
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  detail-card("Reference · row 47", "detail_table005_reference", "MANUAL_TEXT", [The row is isolated and readable.], kind: "reference"),
  detail-card("Gemini · row 47", "detail_table005_gemini", "MANUAL_TEXT", [Rows, values, and “Table 1” overprint in the same lower-page band.]),
  detail-card("Sonnet · row 47", "detail_table005_sonnet", "MANUAL_TEXT", [The row remains readable on page 1.]),
  detail-card("Opus · row 47", "detail_table005_opus", "MANUAL_TEXT", [The row remains readable; the audit found no clear defect at this resolution.]),
)
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Gemini", [Strict F1 *0.948* preserves most words, but page delta *+1*, boundary F1 *0*, center q90 *0.326*, and the boxed collision show a severe layout/pagination failure. SSIM abstains on canvas mismatch.], kind: "warn"),
  note("Sonnet", [Strict F1 *0.998* · page delta *0* · center q90 *0.137*. Its Text-LTSim *0.679* is lower than Gemini’s *0.712* despite the cleaner visible row—evidence that LTSim is not a severity rank.], kind: "warn"),
  note("Opus", [Strict F1 *0.998* · page delta *0* · center q90 *0.056*. SSIM *0.571* is close to the separate severe-collision example’s macro *0.558*, again showing that SSIM is diagnostic.], kind: "warn"),
)

#pagebreak()

// 34–35 — table021
#page-head("33 / FOUR-WAY OVERVIEW", "05_tables_simple_021 · where Table 1 begins", deck: [The boxed caption appears on reference page 2; Gemini moves it onto page 1, while both Claude candidates keep it on page 2.])
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  reference-panel("05_tables_simple_021", "grid_table021_reference", 2, 3, [“Table 1: Source table 1 …” on page 2.]),
  candidate-panel("05_tables_simple_021", "gemini", "Gemini 3.1 Flash Lite", "grid_table021_gemini", 1),
  candidate-panel("05_tables_simple_021", "claude_sonnet", "Claude Sonnet 4.6", "grid_table021_sonnet", 2),
  candidate-panel("05_tables_simple_021", "claude_opus", "Claude Opus 4.7", "grid_table021_opus", 2),
)

#pagebreak()
#page-head("34 / BOXED EVIDENCE", "05_tables_simple_021 · page assignment is clearer than a global score")
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  detail-card("Reference · page 2", "detail_table021_reference", "MANUAL_TEXT", [Table 1 starts on its own page.], kind: "reference"),
  detail-card("Gemini · page 1", "detail_table021_gemini", "MANUAL_TEXT", [The introduction and Table 1 share the first candidate page.]),
  detail-card("Sonnet · page 2", "detail_table021_sonnet", "MANUAL_TEXT", [The three-page table sequence is retained.]),
  detail-card("Opus · page 2", "detail_table021_opus", "MANUAL_TEXT", [The caption remains on the reference page index.]),
)
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Gemini", [Pages *3→2* · boundary F1 *0.400* · center q90 *0.327*. Strict F1 *0.471* versus NFKC *0.847* also shows that much of the low strict value is compatibility/extraction behavior.], kind: "warn"),
  note("Sonnet", [Pages *3→3*, visibly preserved; raw boundary F1 is only *0.286*. This conflict is why boundary scoring remains ungated and conditional.], kind: "warn"),
  note("Opus", [Pages *3→3* · boundary F1 *1.000* · center q90 *0.166*. The box supplies the concrete page-assignment witness missing from an aggregate score.], kind: "warn"),
)

#pagebreak()

// 36–37 — table023
#page-head("35 / FOUR-WAY OVERVIEW", "05_tables_simple_023 · invented rows and leaked Typst syntax", deck: [The boxes mark each candidate’s decisive text evidence. They are intentionally not presented as one common metric region.])
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  reference-panel("05_tables_simple_023", "grid_table023_reference", 3, 3, [The reference visibly ends at rows 20–21.]),
  candidate-panel("05_tables_simple_023", "gemini", "Gemini 3.1 Flash Lite", "grid_table023_gemini", 2),
  candidate-panel("05_tables_simple_023", "claude_sonnet", "Claude Sonnet 4.6", "grid_table023_sonnet", 3),
  candidate-panel("05_tables_simple_023", "claude_opus", "Claude Opus 4.7", "grid_table023_opus", 3),
)

#pagebreak()
#page-head("36 / BOXED EVIDENCE", "05_tables_simple_023 · three distinct content failures")
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  detail-card("Reference · final rows", "detail_table023_reference", "MANUAL_TEXT", [Rows 20–21 are the last visible entries.], kind: "reference"),
  detail-card("Gemini · extra rows", "detail_table023_gemini", "MANUAL_TEXT", [Rows 22–24 exist despite being absent after reference row 21.]),
  detail-card("Sonnet · extra rows", "detail_table023_sonnet", "MANUAL_TEXT", [Rows 22–24 are also invented even though page count remains three.]),
  detail-card("Opus · raw source", "detail_table023_opus", "MANUAL + NFKC", [The rust box encloses the row; amber encloses evaluator unmatched `#sc` syntax.], kind: "automatic"),
)
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Gemini", [Strict F1 *0.826* · number F1 *0.828* · pages *3→2* · tau *−0.333*. Extra rows and pagination both fail. SSIM abstains.], kind: "warn"),
  note("Sonnet", [Strict F1 *0.909* · number F1 *0.952* · pages *3→3*. Exact page count misses the invented rows; the text box supplies the missing content evidence.], kind: "warn"),
  note("Opus", [Strict F1 *0.789* · center q90 *0.135*. Geometry stays modest because corrupted text remains in the table region. Citation F1 *0* is a false-positive alarm from bracketed leaked syntax.], kind: "warn"),
)
#v(6pt)
#note("Structure gap", [The failures are visibly structural, yet GriTS and TEDS correctly abstain because generic PDF words are not validated cell grids or normalized HTML trees.], kind: "core")

#pagebreak()

// 38–39 — table010
#page-head("37 / FOUR-WAY OVERVIEW", "06_tables_moderate_010 · the final FireSentry row", deck: [The same table row is boxed in all four PDFs. Gemini pushes it into a clipped lower-page collision band.])
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  reference-panel("06_tables_moderate_010", "grid_table010_reference", 1, 2, [Clean FireSentry row near the end of Table 1.]),
  candidate-panel("06_tables_moderate_010", "gemini", "Gemini 3.1 Flash Lite", "grid_table010_gemini", 2),
  candidate-panel("06_tables_moderate_010", "claude_sonnet", "Claude Sonnet 4.6", "grid_table010_sonnet", 1),
  candidate-panel("06_tables_moderate_010", "claude_opus", "Claude Opus 4.7", "grid_table010_opus", 1),
)

#pagebreak()
#page-head("38 / BOXED EVIDENCE", "06_tables_moderate_010 · bottom overprint versus clean rows")
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  detail-card("Reference · FireSentry", "detail_table010_reference", "MANUAL_TEXT", [The final row is readable with separated columns.], kind: "reference"),
  detail-card("Gemini · FireSentry", "detail_table010_gemini", "MANUAL_TEXT", [The row, neighboring rows, and caption collapse into the page edge.]),
  detail-card("Sonnet · FireSentry", "detail_table010_sonnet", "MANUAL_TEXT", [The row remains readable on page 1.]),
  detail-card("Opus · FireSentry", "detail_table010_opus", "MANUAL_TEXT", [Text placement is close; heavier rules are a separate manual appearance finding.]),
)
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Gemini", [Strict F1 *0.891* · number F1 *0.816* · pages *2→3* · center q90 *0.327*. Concatenated bottom text explains merged numeric tokens such as `20,000,0002013`.], kind: "warn"),
  note("Sonnet", [Strict F1 *0.986* · pages *2→2* · center q90 *0.122*. Raw page-break F1 is *0* despite the preserved sequence, so it cannot be treated as ground truth.], kind: "warn"),
  note("Opus", [Strict F1 *0.984* · pages *2→2* · center q90 *0.029*. Raw page-break F1 is also *0*; the boxed row and exact page facts are more reliable here.], kind: "warn"),
)

#pagebreak()

// 40–41 — figure007
#page-head("39 / FOUR-WAY OVERVIEW", "07_figures_captions_007 · literal math text versus rendered symbols", deck: [The boxed caption specimen is expected literally as `$16^3\\times 32$` in the reference PDF.])
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  reference-panel("07_figures_captions_007", "grid_figure007_reference", 1, 1, [Literal escaped math text in the caption.]),
  candidate-panel("07_figures_captions_007", "gemini", "Gemini 3.1 Flash Lite", "grid_figure007_gemini", 1),
  candidate-panel("07_figures_captions_007", "claude_sonnet", "Claude Sonnet 4.6", "grid_figure007_sonnet", 1),
  candidate-panel("07_figures_captions_007", "claude_opus", "Claude Opus 4.7", "grid_figure007_opus", 1),
)

#pagebreak()
#page-head("40 / BOXED EVIDENCE", "07_figures_captions_007 · critical inventories name the change")
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  detail-card("Reference caption", "detail_figure007_reference", "NFKC_AUTO", [Evaluator unmatched-word evidence encloses the literal `$16^3\\times 32$`.], kind: "automatic"),
  detail-card("Gemini caption", "detail_figure007_gemini", "NFKC_AUTO", [The candidate renders the specimen as `163 × 32`, changing numeral/operator tokens.], kind: "automatic"),
  detail-card("Sonnet caption", "detail_figure007_sonnet", "MANUAL_TEXT", [The literal specimen is preserved in the caption.]),
  detail-card("Opus caption", "detail_figure007_opus", "MANUAL_TEXT", [The literal specimen is preserved in the caption.]),
)
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Gemini", [Strict F1 *0.740* · number F1 *0.815* · operator F1 *0.824* · center q90 *0.528*. An additional unmatched word `Figure` appears in “Figures Figure 1 …”.], kind: "warn"),
  note("Sonnet", [Strict F1 *0.932* · operator exact *true* · center q90 *0.052* · SSIM *0.869*. Its number mismatch is a missing footer numeral, not caption corruption.], kind: "warn"),
  note("Opus", [Strict F1 *0.932* · operator exact *true* · center q90 *0.046* · SSIM *0.895*. Figure-structure scoring still abstains.], kind: "warn"),
)

#pagebreak()

// 42–43 — algorithm003
#page-head("41 / FOUR-WAY OVERVIEW", "09_algorithms_003 · Algorithm 2 becomes Figure 1", deck: [The full caption line is boxed. Amber sub-boxes mark direct NFKC unmatched-word evidence for the changed label.])
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  reference-panel("09_algorithms_003", "grid_algorithm003_reference", 2, 2, [“Algorithm 2: Initialization …” on page 2.]),
  candidate-panel("09_algorithms_003", "gemini", "Gemini 3.1 Flash Lite", "grid_algorithm003_gemini", 1),
  candidate-panel("09_algorithms_003", "claude_sonnet", "Claude Sonnet 4.6", "grid_algorithm003_sonnet", 2),
  candidate-panel("09_algorithms_003", "claude_opus", "Claude Opus 4.7", "grid_algorithm003_opus", 2),
)

#pagebreak()
#page-head("42 / BOXED EVIDENCE", "09_algorithms_003 · page, label, and extraction evidence agree")
#grid(columns: (1fr, 1fr), gutter: 8pt, row-gutter: 8pt,
  detail-card("Reference · page 2", "detail_algorithm003_reference", "MANUAL + NFKC", [Full line: “Algorithm 2 …”; amber sub-box is direct unmatched text evidence.], kind: "automatic"),
  detail-card("Gemini · page 1", "detail_algorithm003_gemini", "MANUAL + NFKC", [Full line becomes “Figure 1 …” on the only page.], kind: "automatic"),
  detail-card("Sonnet · page 2", "detail_algorithm003_sonnet", "MANUAL_TEXT", [The algorithm label and page sequence are preserved.]),
  detail-card("Opus · page 2", "detail_algorithm003_opus", "MANUAL_TEXT", [The label and page sequence are preserved.]),
)
#v(7pt)
#grid(columns: (1fr, 1fr, 1fr), gutter: 7pt,
  note("Gemini", [Strict F1 *0.475* · NFKC *0.749* · pages *2→1* · boundary F1 *0* · center q90 *0.569*. The label substitution and page compression are both objective.], kind: "warn"),
  note("Sonnet", [Strict F1 *0.609* but NFKC *0.855* · pages *2→2* · SSIM *0.885*. The visual audit found no clear defect, so strict extraction alone must not grade this candidate.], kind: "warn"),
  note("Opus", [Strict F1 *0.611* · NFKC *0.857* · pages *2→2* · center q90 *0.018*. Raw page-break F1 *0.500* conflicts with the preserved sequence and remains conditional.], kind: "warn"),
)

#pagebreak()

// 44 — references
#page-head("43 / REFERENCES", "Primary methods and technical sources")
#grid(columns: (1fr, 1fr), gutter: 11mm,
  [
    #heading(level: 2)[Text, assignment, and layout]
    #text(size: 9.7pt)[
      *Unicode Consortium.* “Unicode Normalization Forms,” UAX #15. #link("https://www.unicode.org/reports/tr15/")[unicode.org/reports/tr15].

      *V. I. Levenshtein.* “Binary Codes Capable of Correcting Deletions, Insertions, and Reversals,” 1965/66. #link("https://www.mathnet.ru/eng/dan31411")[Primary record].

      *H. W. Kuhn.* “The Hungarian Method for the Assignment Problem,” 1955. #link("https://doi.org/10.1002/nav.3800020109")[doi:10.1002/nav.3800020109].

      *H. Rezatofighi et al.* “Generalized Intersection over Union,” CVPR 2019. #link("https://doi.org/10.1109/CVPR.2019.00075")[doi:10.1109/CVPR.2019.00075].

      *Y. Baek et al.* “CLEval: Character-Level Evaluation for Text Detection and Recognition Tasks,” CVPRW 2020. #link("https://doi.org/10.1109/CVPRW50498.2020.00290")[doi:10.1109/CVPRW50498.2020.00290] · #link("https://github.com/clovaai/CLEval")[official code].

      *M. Otani et al.* “LTSim: Layout Transportation-based Similarity Measure for Evaluating Layout Generation,” 2024. #link("https://doi.org/10.48550/arXiv.2407.12356")[doi:10.48550/arXiv.2407.12356].

      *M. Lapata.* “Automatic Evaluation of Information Ordering: Kendall’s Tau,” *Computational Linguistics* 32(4), 2006. #link("https://doi.org/10.1162/coli.2006.32.4.471")[doi:10.1162/coli.2006.32.4.471].
    ]
  ],
  [
    #heading(level: 2)[Raster, tables, and structures]
    #text(size: 9.7pt)[
      *Z. Wang et al.* “Image Quality Assessment: From Error Visibility to Structural Similarity,” *IEEE TIP* 13(4), 2004. #link("https://doi.org/10.1109/TIP.2003.819861")[doi:10.1109/TIP.2003.819861].

      *Z. Wang, E. P. Simoncelli & A. C. Bovik.* “Multiscale Structural Similarity for Image Quality Assessment,” 2003. #link("https://doi.org/10.1109/ACSSC.2003.1292216")[doi:10.1109/ACSSC.2003.1292216].

      *B. Smock, R. Pesala & R. Abraham.* “GriTS: Grid Table Similarity Metric for Table Structure Recognition,” ICDAR 2023. #link("https://doi.org/10.1007/978-3-031-41734-4_33")[doi:10.1007/978-3-031-41734-4_33] · #link("https://github.com/microsoft/table-transformer")[official code].

      *X. Zhong, E. ShafieiBavani & A. Jimeno Yepes.* “Image-Based Table Recognition: Data, Model, and Evaluation,” ECCV 2020. #link("https://doi.org/10.1007/978-3-030-58589-1_34")[doi:10.1007/978-3-030-58589-1_34] · #link("https://github.com/ibm-aur-nlp/PubTabNet")[official code].

      *B. Wang et al.* “Image Over Text: Transforming Formula Recognition Evaluation with Character Detection Matching,” CVPR 2025. #link("https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_Image_Over_Text_Transforming_Formula_Recognition_Evaluation_with_Character_Detection_CVPR_2025_paper.pdf")[paper].

      *Adobe Systems.* *PDF Reference 1.7*, 6th ed., 2006. #link("https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf")[official PDF].

      *OECD/JRC.* *Handbook on Constructing Composite Indicators*, 2008. #link("https://doi.org/10.1787/9789264043466-en")[doi:10.1787/9789264043466-en].
    ]
  ],
)
#v(8pt)
#note("Citation rule used in this report", [Published names are used only for their actual required representation and equations. Repository-defined combinations are labeled adaptations or diagnostics; unavailable representations abstain.], kind: "core")

#pagebreak()

// 45 — reproducibility
#page-head("44 / REPRODUCIBILITY", "Exact artifacts, settings, and rebuild path")
#grid(columns: (1fr, 1fr), gutter: 11mm,
  [
    #heading(level: 2)[Frozen evidence used]
    #text(size: 9.8pt)[
      *Identity:*  
      `results/metric_research_v2/identity_157_final/identity_validation.json`

      *Controlled 628:*  
      `results/metric_research_v2/controlled_retained_628/metric_v2_scores_final.csv`  
      `…/validation/validation_summary.json`  
      `…/validation/reaudit/reaudit_agreement.json`

      *Gemini 156:*  
      `results/metric_research_v2/gemini_frozen_156/metric_v2_scores.csv`  
      `…/analysis/ai_manual_metric_alignment.json`

      *Four-way 21:*  
      `results/metric_research_v2/claude_overlap/metric_v2/metric_v2_scores.csv`  
      `…/visual_audit/manual_visual_findings.csv`

      *Scorecards:*  
      `results/metric_research_v2/scorecards/scorecards.json`  
      `…/engine_metric_v2/metric_v2_scores.csv`

      *Evaluator:*  
      `scripts/evaluation/pdf_metric_axes_v2.py`
    ]
  ],
  [
    #heading(level: 2)[Frozen raster configuration]
    #table(columns: (44mm, 1fr),
      [render DPI], [96 in the scored evidence],
      [ink threshold], [245 grayscale],
      [ink tolerance], [2 pixels],
      [SSIM window], [11 where image size permits],
      [SSIM Gaussian], [weights true; sigma 1.5],
      [covariance], [population (`use_sample_covariance=false`)],
      [multiscale factors], [1, 2, 4, 8],
    )
    #v(7pt)
    #note("Version warning", [The code default is currently 120 DPI, while the frozen evidence in this report records 96 DPI. Exact score reproduction must pass the recorded configuration; do not mix runs.], kind: "warn")
  ],
)
#v(8pt)
#heading(level: 2)[Rebuild the report]
#card([
  #text(font: "Menlo", size: 8.8pt)[
    mamba run -n lathe python scripts/evaluation/build_model_engine_scorecards.py#linebreak()
    mamba run -n lathe python scripts/evaluation/build_pdf_fidelity_report_assets.py#linebreak()
    /opt/homebrew/bin/typst compile --root . reports/pdf_fidelity_metric_system_v3.typ output/pdf/pdf_fidelity_metric_system_v3.pdf#linebreak()
    mkdir -p /tmp/pdf_fidelity_metric_system_v3#linebreak()
    pdftoppm -png -r 144 output/pdf/pdf_fidelity_metric_system_v3.pdf /tmp/pdf_fidelity_metric_system_v3/page
  ]
], edge: rule)
#v(7pt)
#note("Final interpretation", [This system can explain literal preservation, page facts, and localized text/layout evidence today. It cannot yet supply a validated universal perceptual grade; that limitation is part of the result, not omitted uncertainty.], kind: "core")
