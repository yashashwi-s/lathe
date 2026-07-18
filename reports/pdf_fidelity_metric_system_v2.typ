#let ink = rgb("#20262b")
#let muted = rgb("#626c72")
#let rule = rgb("#d8dcde")
#let paper = rgb("#fbfaf7")
#let panel = rgb("#f2f3f1")
#let accent = rgb("#96543f")
#let accent-soft = rgb("#efe3dd")
#let blue = rgb("#355f6a")
#let blue-soft = rgb("#dfeaec")

#set document(title: "An evidence-bearing PDF fidelity prototype", author: "Lathe metric research")
#set page(width: 420mm, height: 297mm, margin: (x: 20mm, top: 17mm, bottom: 16mm), fill: paper,
  footer: context [
    #set text(font: "Avenir Next", size: 7.5pt, fill: muted)
    #grid(columns: (1fr, auto), [LATHE / PDF FIDELITY METRIC SYSTEM v2], [#counter(page).display("1")])
  ])
#set text(font: "Avenir Next", size: 10.2pt, fill: ink, lang: "en")
#set par(justify: false, leading: 0.62em, spacing: 0.7em)
#set list(indent: 1.25em, body-indent: 0.55em, spacing: 0.45em)
#set enum(indent: 1.25em, body-indent: 0.55em, spacing: 0.45em)
#set table(stroke: rule, inset: (x: 6pt, y: 5pt))
#show heading.where(level: 1): it => [
  #set text(font: "Avenir Next", weight: 650, size: 24pt, fill: ink)
  #block(above: 0pt, below: 10pt)[#it.body]
]
#show heading.where(level: 2): it => [
  #set text(font: "Avenir Next", weight: 650, size: 13pt, fill: ink)
  #block(above: 8pt, below: 4pt)[#it.body]
]
#show link: set text(fill: blue)

#let pct(x, digits: 1) = str(calc.round(x * 100, digits: digits)) + "%"
#let num(x, digits: 3) = if x == none { "—" } else { str(calc.round(x, digits: digits)) }
#let chip(body, kind: "neutral") = {
  let bg = if kind == "accent" { accent-soft } else if kind == "blue" { blue-soft } else { panel }
  let fg = if kind == "accent" { accent } else if kind == "blue" { blue } else { ink }
  box(fill: bg, inset: (x: 7pt, y: 4pt), radius: 3pt)[#text(size: 8pt, weight: 600, fill: fg)[#body]]
}
#let label(body) = text(size: 7.6pt, weight: 600, fill: muted, tracking: 0.08em)[#upper(body)]
#let page-head(kicker, title, deck: none) = [
  #label(kicker)
  #v(3pt)
  #heading(level: 1)[#title]
  #if deck != none [#text(size: 11pt, fill: muted)[#deck] #v(5pt)]
  #line(length: 100%, stroke: 0.8pt + rule)
  #v(8pt)
]
#let metric-card(title, value, note, kind: "neutral") = {
  let edge = if kind == "accent" { accent } else if kind == "blue" { blue } else { rule }
  block(fill: white, stroke: (left: 3pt + edge, rest: 0.6pt + rule), radius: 3pt, inset: 10pt)[
    #label(title)
    #v(3pt)
    #text(size: 22pt, weight: 650, fill: ink)[#value]
    #v(3pt)
    #text(size: 8.2pt, fill: muted)[#note]
  ]
}
#let callout(title, body, kind: "neutral") = {
  let bg = if kind == "accent" { accent-soft } else if kind == "blue" { blue-soft } else { panel }
  let fg = if kind == "accent" { accent } else if kind == "blue" { blue } else { ink }
  block(fill: bg, radius: 4pt, inset: 12pt)[
    #text(weight: 650, fill: fg)[#title]
    #v(4pt)
    #text(size: 9.2pt, fill: ink)[#body]
  ]
}
#let decision-row(name, status, body, kind: "neutral") = grid(
  columns: (42mm, 28mm, 1fr), gutter: 8pt, align: (left, left, left),
  [#text(weight: 650)[#name]], [#chip(status, kind: kind)], [#text(size: 9pt, fill: muted)[#body]]
)
#let mini-bar(label-text, value, color: blue) = grid(
  columns: (46mm, 1fr, 18mm), gutter: 7pt, align: (left, horizon, right),
  [#text(size: 8.5pt)[#label-text]],
  [#block(height: 5pt, fill: panel, radius: 2.5pt)[#block(width: value * 100%, height: 5pt, fill: color, radius: 2.5pt)]],
  [#text(size: 8.5pt, weight: 600)[#pct(value)]]
)

#let ctl = json("../results/metric_research_v2/controlled_retained_628/validation/validation_summary.json")
#let identity = json("../results/metric_research_v2/identity_157_final/identity_validation.json")
#let fullv1 = json("../results/metric_research_v1/full_157_v1/controlled_validation.json")
#let gemini = json("../results/metric_research_v2/gemini_frozen_156/metric_summary.json").groups.all
#let ai-align = json("../results/metric_research_v2/gemini_frozen_156/analysis/ai_manual_metric_alignment.json")
#let severity-validation = json("../results/metric_research_v2/layout_severity_all157/validation/severity_validation.json")
#let overlap-summary = json("../results/metric_research_v2/claude_overlap/summary.json")
#let overlap-align = json("../results/metric_research_v2/claude_overlap/analysis/manual_metric_alignment.json")
#let reaudit = json("../results/metric_research_v2/controlled_retained_628/validation/reaudit/reaudit_agreement.json")
#let overlap-scores = csv("../results/metric_research_v2/claude_overlap/metric_v2/metric_v2_scores.csv", row-type: dictionary)
#let ai-blind = (
  csv("../results/metric_research_v1/ai_outputs_frozen_v1/visual_audit/manual_ai_blind_part_001_052.csv", row-type: dictionary)
  + csv("../results/metric_research_v1/ai_outputs_frozen_v1/visual_audit/manual_ai_blind_part_053_104.csv", row-type: dictionary)
  + csv("../results/metric_research_v1/ai_outputs_frozen_v1/visual_audit/manual_ai_blind_part_105_156.csv", row-type: dictionary)
)
#let ai-unblind = (
  csv("../results/metric_research_v1/ai_outputs_frozen_v1/visual_audit/manual_ai_unblind_part_001_052.csv", row-type: dictionary)
  + csv("../results/metric_research_v1/ai_outputs_frozen_v1/visual_audit/manual_ai_unblind_part_053_104.csv", row-type: dictionary)
  + csv("../results/metric_research_v1/ai_outputs_frozen_v1/visual_audit/manual_ai_unblind_part_105_156.csv", row-type: dictionary)
)
#let ai-residual-useful = ai-unblind.filter(row => row.top_residual_box_useful_after_unblind == "true").len() / ai-unblind.len()
#let ai-axis-plausible = ai-unblind.filter(row => row.axis_labels_plausible_after_unblind == "true").len() / ai-unblind.len()
#let ai-canvas-confound = ai-unblind.filter(row => row.canvas_confound == "true").len() / ai-unblind.len()
#let ai-major-any = ai-blind.filter(row => (row.content_issue == "major" or row.layout_issue == "major" or row.typography_issue == "major" or row.pagination_issue == "major" or row.specialized_issue == "major")).len() / ai-blind.len()

// Cover
#set page(footer: none)
#v(27mm)
#label("LATHE / RESEARCH REPORT / 18 JULY 2026")
#v(8mm)
#text(size: 42pt, weight: 650, fill: ink)[An evidence-bearing PDF fidelity prototype]
#v(5mm)
#text(size: 17pt, fill: muted)[LaTeX reference PDFs vs AI-generated Typst PDFs]
#v(14mm)
#grid(columns: (1.45fr, 1fr), gutter: 18mm,
  block(stroke: (left: 5pt + accent), inset: (left: 12pt, y: 3pt))[
    #text(size: 15pt, weight: 600)[The conclusion]
    #v(5pt)
    #text(size: 12pt, fill: ink)[Use a non-compensatory scorecard with exact evidence. Do not release a universal scalar.]
    #v(8pt)
    #text(size: 10pt, fill: muted)[The report keeps strict text and partial critical-symbol preservation, Text-LTSim on the defensible text-only subset, raw token geometry, exact page count, and conditional diagnostics. It rejects collapsed IoU grades, resized-canvas SSIM, and unsupported structure scores.]
  ],
  grid(columns: (1fr, 1fr), gutter: 8pt,
    metric-card("DATASET", "157", "reference documents", kind: "blue"),
    metric-card("V1 AUGMENTATIONS", "16,167", "planned controlled variants", kind: "blue"),
    metric-card("LLM AUDIT PANEL", "628", "four retained cases per document", kind: "accent"),
    metric-card("UNIQUE AI PDFs", "170", "156 Gemini + 14 Claude outputs", kind: "accent"),
  ),
)
#v(17mm)
#callout("Evidence boundary", [No human ratings were used. Controlled mutation truth, exact source-backed evidence, and blinded LLM forensic review validate mechanical behavior; they do not establish human perceptual utility.], kind: "blue")

#set page(footer: context [
  #set text(font: "Avenir Next", size: 7.5pt, fill: muted)
  #grid(columns: (1fr, auto), [LATHE / PDF FIDELITY METRIC SYSTEM v2], [#counter(page).display("1")])
])
#pagebreak()

#page-head("01 / DECISION", "What survives", deck: [A score vector with hard gates and abstentions—not a number that lets one success cancel another failure.])
#grid(columns: (1.15fr, 1fr), gutter: 16mm,
  [
    #decision-row("Eligibility", "RETAIN", [PDF opens; hashes, page count, page size, renderer and protocol are frozen. Canvas mismatch is a finding.], kind: "blue")
    #v(7pt)
    #decision-row("Exact content", "RETAIN", [Strict NFC token P/R/F1 and edit similarity. NFKC is a compatibility view, not a replacement.], kind: "blue")
    #v(7pt)
    #decision-row("Partial critical inventory", "RETAIN", [Numbers, a fixed operator set and restricted citation markers are exact NFKC multisets with concrete missing/added items.], kind: "blue")
    #v(7pt)
    #decision-row("Text layout", "RETAIN", [Published LTSim equations on extracted text blocks only, plus raw token displacement and coverage.], kind: "blue")
    #v(7pt)
    #decision-row("Pagination", "MIXED", [Exact page count is retained. Page assignment and boundary F1 remain conditional diagnostics pending document-form gates.], kind: "blue")
    #v(7pt)
    #decision-row("Raster", "DIAGNOSTIC", [SSIM fails closed on canvas/grid mismatch. Current tolerant-ink F1 resizes canvases and its residual box is translation-registered; neither is fidelity truth.])
    #v(7pt)
    #decision-row("Tables / math / figures", "ABSTAIN", [No GriTS, TEDS or full semantic LTSim until both PDFs expose validated common structures.], kind: "accent")
  ],
  [
    #callout("Comparison rule", [Compare candidates axis by axis. A critical-token, page-count, or eligibility failure cannot be averaged away by a visually similar background.], kind: "accent")
    #v(10pt)
    #metric-card("UNIVERSAL SCORE", "REJECTED", "No defensible calibration without validated structure evidence and human preference data.", kind: "accent")
    #v(10pt)
    #callout("Per-output explanation", [Every row carries applicable matched entities, strict missing/extra token lists, separate boxed NFKC-word evidence, transport flows, diagnostic residual enclosure, applicability state, and reason for abstention.], kind: "blue")
  ],
)

#pagebreak()
#page-head("02 / SCOPE", "What was actually evaluated", deck: [The report distinguishes generated model PDFs, controlled mutations, and development-only evidence.])
#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 9pt,
  metric-card("REFERENCE SET", "157 / 157", "accepted pdfLaTeX references; 11 document forms"),
  metric-card("CONTROLLED v1", "16,142", "applied of 16,167 planned; 25 not applicable; 0 failed"),
  metric-card("FROZEN GEMINI", "156 / 157", "compiled stored outputs; one missing tables case"),
  metric-card("FOUR-WAY SET", "7", "reference + Gemini + Sonnet + Opus; 21 candidates"),
)
#v(10mm)
#table(
  columns: (36mm, 43mm, 1fr, 54mm),
  table.header([#label("artifact")], [#label("granularity")], [#label("allowed claim")], [#label("prohibited claim")]),
  [Controlled v1 variants], [16,167 planned / 157 sources], [v1 harness mechanics; candidate generation and broad invariants], [v2-wide validation or model quality],
  [Retained v2 panel], [628 rescored + LLM audited], [v2 mechanics on four retained cases per document], [Human perceptual validity],
  [v2 layout severity], [471 rows / 157 sources], [Text-LTSim sensitivity for one block-right family], [General perceptual monotonicity],
  [Frozen Gemini], [156 stored outputs], [Axis distributions, failure evidence, audit consistency], [A universal fidelity leaderboard],
  [Claude overlap], [7 complete four-way sets], [Visual examples and metric/defect alignment], [Model ranking: protocols differ],
  [Prompt-development split], [33 documents], [Method development only], [Held-out benchmark performance],
)
#v(9mm)
#callout("Protocol confound in the four-way grids", [Gemini is source-only with no reference images and at most one repair. Six of seven Claude cases used iterative visual feedback; Sonnet and Opus also used different harness/effort settings. The grids test metric behavior against visible defects, not model capability.], kind: "accent")

#pagebreak()
#page-head("03 / FAILURE ANALYSIS", "Why the first evaluator was rejected", deck: [A useful research result is knowing which plausible-looking numbers are invalid.])
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Collapsed token IoU]
    The q10 token-box IoU projection was *0.000 for every one of the 156 Gemini candidates*. It separated nothing and was removed as an AI grade.

    #heading(level: 2)[Canvas-normalized false comfort]
    Normalizing boxes by each page hid Letter-vs-A4 differences. Canvas is now a separate hard fact; geometry never repairs it.

    #heading(level: 2)[Resized SSIM]
    Resizing an A4 candidate onto a Letter reference makes a mathematically convenient image pair while erasing a real document failure. v2 abstains instead.
  ],
  [
    #heading(level: 2)[Perceptual no-ops]
    The post-unblind audit rejected *#ctl.manual_post_unblind.invalid_or_invisible_rows / #ctl.rows* retained perturbations as not visibly distinguishable. Yet the raster trigger fired on #pct(ctl.invalid_or_invisible_trigger_rate.raster_residual.trigger_rate) of them.

    #heading(level: 2)[Unsupported structure]
    Text boxes are not table cells, formula trees, or figure/caption relations. Returning a structure score would measure an unvalidated detector as much as the candidate.

    #heading(level: 2)[Single-number compensation]
    A page-count or wrong-digit failure must not disappear because typography or whitespace scores well. v2 has no compensatory aggregate.
  ],
)
#v(8mm)
#callout("Scientific consequence", [Automatic difference detection and visible defect severity are different questions. The report gives each a separate evidence contract.], kind: "blue")

#pagebreak()
#page-head("04 / LITERATURE", "Metric decisions from primary sources", deck: [Published names are used only where their required inputs and equations are actually present.])
#table(
  columns: (33mm, 54mm, 1fr, 35mm),
  table.header([#label("method")], [#label("required representation")], [#label("decision here")], [#label("status")]),
  [CLEval], [word polygons, transcriptions, split/merge accounting], [Exact-word grounding retained; published CLEval stays pending an official-code conformance oracle.], [#chip("PENDING")],
  [LTSim], [boxes + semantic labels + optimal transport], [Published equations implemented per page on the all-text subset; full semantic LTSim abstains.], [#chip("TEXT-ONLY", kind: "blue")],
  [GriTS], [table grid cells, spans, boxes and text], [No score from generic PDF words/blocks.], [#chip("ABSTAIN", kind: "accent")],
  [TEDS], [normalized HTML table trees], [No score until both PDFs share validated normalized trees.], [#chip("ABSTAIN", kind: "accent")],
  [Kendall tau], [confident matched order with a valid total-order policy], [Conditional diagnostic with coverage and inversion examples.], [#chip("CONDITIONAL")],
  [SSIM / multiscale adaptation], [same physical canvas, renderer and raster grid], [Fail closed; no resizing. The multiscale value is an adaptation, not canonical MS-SSIM.], [#chip("DIAGNOSTIC")],
)
#v(7mm)
#text(size: 8.5pt, fill: muted)[Primary references: #link("https://openaccess.thecvf.com/content_CVPRW_2020/papers/w34/Baek_CLEval_Character-Level_Evaluation_for_Text_Detection_and_Recognition_Tasks_CVPRW_2020_paper.pdf")[CLEval] · #link("https://arxiv.org/pdf/2407.12356")[LTSim] · #link("https://arxiv.org/pdf/2203.12555")[GriTS] · #link("https://arxiv.org/pdf/1911.10683")[TEDS] · #link("https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf")[SSIM] · #link("https://ece.uwaterloo.ca/~z70wang/publications/msssim.pdf")[MS-SSIM] · #link("https://aclanthology.org/J06-4002.pdf")[reading-order tau].]

#pagebreak()
#page-head("05 / SCORECARD", "The research-prototype vector", deck: [Every component has a direction, coverage, evidence and abstention state.])
#table(
  columns: (34mm, 61mm, 48mm, 1fr),
  table.header([#label("component")], [#label("raw observables")], [#label("failure evidence")], [#label("reporting rule")]),
  [Eligibility], [open/hash/protocol, page count, page points], [exact file/page facts], [Gate before scoring; never normalized away.],
  [Content], [strict NFC whitespace-token P/R/F1; character edit similarity], [strict missing/added token lists], [NFKC shown separately as compatibility.],
  [Partial critical inventory], [number/fixed-operator/restricted-citation P/R/F1 + exactness], [concrete missing and extra values], [Units and general punctuation are not yet inventoried.],
  [Text geometry], [coverage, center q50/q90, IoU q10/q50, size ratios], [worst NFKC-matched PDF-word boxes], [Separate boxed evidence; not the strict token multiset.],
  [Text-LTSim], [per-page EMD and exp(-EMD)], [largest transport-cost flows], [Published equations, all elements labeled text.],
  [Reading order], [tau, inversion count, matched coverage], [concrete inverted blocks], [Conditional pending coverage, ambiguity and document-form gates.],
  [Pagination], [count delta, page assignment, boundary P/R/F1], [mismatched boundaries], [Count accepted; assignment/boundaries conditional.],
  [Typography], [font-size/baseline/style residuals], [worst styled word pairs], [Diagnostic metadata; not perceptual truth.],
  [Raster], [resized-canvas ink P/R/F1; fail-closed SSIM; registered residual boxes], [translation-registered enclosure], [SSIM only same canvas; other raster outputs are diagnostics.],
  [Structures], [GriTS/TEDS/full semantic LTSim], [applicability + reason], [Abstain until common validated extraction.],
)

#pagebreak()
#page-head("06 / CONTENT", "Exact preservation with a partial critical inventory", deck: [Semantic similarity is insufficient when the task is faithful typesetting conversion.])
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Strict view]
    Unicode NFC, soft-hyphen removal and collapsed whitespace; case is preserved. Report whitespace-token multiset precision, recall and F1, plus normalized character edit similarity. These strict missing/added lists do not carry boxes.

    #heading(level: 2)[Compatibility view]
    Unicode NFKC is shown separately to reveal ligature or encoding equivalence. It never replaces or conceals strict mismatches.

    #heading(level: 2)[Critical classes]
    Regex numbers, a fixed mathematical-operator character set and restricted citation-like markers have separate exact NFKC inventories. Units and general punctuation are not implemented. Empty inventories are not evidence that a construct was preserved.
  ],
  [
    #metric-card("GEMINI / STRICT TOKEN F1", num(gemini.metrics.strict_word_f1.median), "NFC whitespace-token median across 156; q10 " + num(gemini.metrics.strict_word_f1.q10) + ", q90 " + num(gemini.metrics.strict_word_f1.q90), kind: "blue")
    #v(8pt)
    #metric-card("NUMBER INVENTORY", pct(gemini.critical_inventories.number.exact_rate), "exact among " + str(gemini.critical_inventories.number.applicable_pairs) + " pairs; includes page numerals", kind: "accent")
    #v(8pt)
    #callout("Interpretation", [A low document text score does not identify whether the error is a page number, table cell or formula syntax. The partial inventory names critical mismatches; separate NFKC PDF-word matching provides localized boxes.])
  ],
)

#pagebreak()
#page-head("07 / LAYOUT", "Text-LTSim plus raw geometry—not a collapsed box score", deck: [The published transport equations are faithful only on the subset the extractor actually supports.])
#grid(columns: (1.05fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Per-page Text-LTSim]
    For text blocks with normalized boxes, each page uses uniform mass, $delta_("bbox")=(1+"GIoU")/2$, $delta_("label")=1$, $mu=1-(delta_("bbox")+delta_("label"))/2$, and $"Text-LTSim"=exp(-"EMD")$ with $sigma=1$.

    #heading(level: 2)[What it does not claim]
    All elements are labeled *text*. The result measures text-block geometry and segmentation, not semantic table/formula/figure layout.

    #heading(level: 2)[Raw residuals stay visible]
    Exact-token center displacement, box IoU and coverage accompany the transport value. Block inversion and page-assignment outputs remain conditional diagnostics pending their gates.
  ],
  [
    #grid(columns: (1fr, 1fr), gutter: 8pt,
      metric-card("IDENTITY", if identity.status == "pass" { "157 / 157" } else { "FAILED" }, "all nine implemented checks passed", kind: "blue"),
      metric-card("SEVERITY ORDER", pct(severity-validation.all_documents.adjacent_nonincreasing_rate), "471 comparisons; mechanical monotonicity", kind: "blue"),
      metric-card("VISIBLE AT s2", str(severity-validation.manual_severity2_valid_visible_documents.documents) + " / 157", "60 mutations were invalid or invisible to the LLM pass", kind: "accent"),
      metric-card("MEDIAN s1 → s3 DROP", num(severity-validation.all_documents.score_drop_s1_to_s3.median, digits: 4), "not a perceptual grade interval"),
    )
    #v(8pt)
    #callout("Sensitivity is not salience", [Text-LTSim decreased monotonically even for the 60 severity-2 mutations rejected as invalid or visually indistinguishable. It is a reliable mechanical detector here, not a calibrated perception model.], kind: "accent")
  ],
)

#pagebreak()
#page-head("08 / RASTER", "Canvas first; pixels second", deck: [Raster metrics expose residuals but are not allowed to repair geometry or assert semantics.])
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Fail-closed SSIM]
    Ordinary SSIM requires equal physical page points and equal fixed-DPI raster grids. If either differs, the value is an abstention—not a resized comparison.

    #heading(level: 2)[Current raster boundary]
    SSIM and the multiscale adaptation abstain unless physical canvas and raster grid match. The existing tolerant-ink F1 instead resizes the candidate canvas, and its residual enclosure is computed after translation registration. Both remain diagnostics, not unregistered fidelity evidence.

    #heading(level: 2)[Why page means are weak]
    White background dominates typeset pages. Tolerant active-ink precision/recall/F1 and its registered enclosure can reveal gross disagreement, but cannot establish physical fidelity across different canvases.
  ],
  [
    #metric-card("GEMINI SSIM ELIGIBLE", str(gemini.ssim_scored_pairs) + " / 156", "154 abstentions are caused by canvas/grid mismatch, not zero scores", kind: "accent")
    #v(8pt)
    #metric-card("OVERLAP / GEMINI", "0 / 7", "all seven are A4 while references are Letter", kind: "accent")
    #v(8pt)
    #metric-card("OVERLAP / CLAUDE", "14 / 14", "Sonnet and Opus use the same Letter canvas as the references", kind: "blue")
  ],
)

#pagebreak()
#page-head("09 / AUGMENTATION", "16,167 v1 plans; 628 cases rescored in v2", deck: [Synthetic truth is only useful when the mutation itself is real and visible.])
#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 9pt,
  metric-card("PLANNED", "16,167", "103 cases per source on average"),
  metric-card("APPLIED", "16,142", "25 construct-specific not applicable"),
  metric-card("FAILED", "0", "generation/evaluation failures"),
  metric-card("AUDITED", "628", "four cases per each of 157 sources"),
)
#v(8mm)
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Families]
    Global translation/scale; local block displacement; deletion, lexical and numeric corruption; font size and line spacing; crop/occlusion; blur/downsample/JPEG; page reorder/count; tables, figures, formulas, algorithms, forms and fixed compounds.

    #heading(level: 2)[Automated v1 checks]
    Invariant false-positive rate *#pct(fullv1.document_macro.invariant_false_positive_rate)*; raster localization hit *#pct(fullv1.document_macro.localization_hit_rate)*; mean localization IoU *#num(fullv1.document_macro.localization_mean_iou)*; compound dominance *#pct(fullv1.document_macro.compound_dominance_accuracy)*.
  ],
  [
    #mini-bar("valid + visible", ctl.manual_post_unblind.valid_and_visible_rows / ctl.rows, color: blue)
    #v(8pt)
    #mini-bar("invalid / invisible", ctl.manual_post_unblind.invalid_or_invisible_rows / ctl.rows, color: accent)
    #v(12pt)
    #callout("Do not train on the 98 rejected cases", [They are preserved as harness failure evidence. Low-level metrics frequently detect object/raster changes that were not visually distinguishable; using them as perceptual truth would teach the wrong threshold.], kind: "accent")
  ],
)

#pagebreak()
#page-head("10 / BLINDED LLM AUDIT", "What the 628-case forensic pass changed", deck: [No human ratings were used. Blind A/B judgments were frozen before labels, targets and scores were revealed.])
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Post-unblind findings]
    - *#ctl.manual_post_unblind.valid_and_visible_rows* candidates were valid and visibly changed.
    - *#ctl.manual_post_unblind.invalid_or_invisible_rows* were rejected as no-ops or not assessable.
    - The LLM audit marked generator labels and known targets correct in all *#ctl.manual_post_unblind.valid_and_visible_rows* assessable cases.
    - Predicted boxes were fully useful in *496 / 628*, partial in *23 / 628*, and not useful in *109 / 628* cases.
  ],
  [
    #heading(level: 2)[Second blinded LLM pass]
    The 208-case slice was reviewed again with no access to the first judgments, labels, answer key or automatic scores.
    #v(7pt)
    #metric-card("PANEL / ABSTAIN AGREEMENT", pct(reaudit.panel_or_abstain_exact_agreement), "two blinded LLM passes; kappa " + num(reaudit.panel_or_abstain_cohen_kappa), kind: "blue")
    #v(7pt)
    #metric-card("AXIS AGREEMENT", pct(reaudit.axis_agreement_when_both_nonabstain), "only " + str(reaudit.both_nonabstain_cases) + " cases were visible to both passes", kind: "accent")
    #v(7pt)
    #callout("Negative result", [Changed-panel agreement was #pct(reaudit.changed_panel_agreement_when_both_nonabstain) when both passes committed, but the defect-axis taxonomy was unstable. The first pass abstained on #str(reaudit.first_abstain_count) cases and the second on #str(reaudit.second_abstain_count). This is repeatability evidence, not human ground truth.], kind: "accent")
  ],
)

#pagebreak()
#page-head("11 / FROZEN GEMINI", "All 156 available outputs", deck: [The scorecard reports distributions and exact failure facts; no overall grade is assigned.])
#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 9pt,
  metric-card("STRICT TOKEN F1", num(gemini.metrics.strict_word_f1.median), "NFC whitespace-token median; q10 " + num(gemini.metrics.strict_word_f1.q10)),
  metric-card("TEXT-LTSIM", num(gemini.metrics.text_ltsim_page_macro.median), "median; text-only subset"),
  metric-card("CENTER q90", num(gemini.metrics.token_center_displacement_q90.median), "median normalized page diagonal error"),
  metric-card("PAGE COUNT EXACT", pct(gemini.page_count_exact_rate), "129 / 156 outputs"),
)
#v(9mm)
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Critical exactness]
    #mini-bar("operators exact", gemini.critical_inventories.operator.exact_rate, color: blue)
    #v(7pt)
    #mini-bar("citations exact", gemini.critical_inventories.citation.exact_rate, color: blue)
    #v(7pt)
    #mini-bar("numbers exact", gemini.critical_inventories.number.exact_rate, color: accent)
  ],
  [
    #heading(level: 2)[Abstentions are data]
    SSIM is scored on only *#gemini.ssim_scored_pairs / 156* same-canvas pairs. Table, formula and figure structure axes abstain on all 156 because the common semantic representations do not exist.
    #v(7pt)
    #callout("Do not read the medians as a universal model score", [Axes have different meanings, directions, applicability and failure costs. The row-level evidence is the unit of explanation.], kind: "accent")
  ],
)

#pagebreak()
#page-head("12 / AI VISUAL AUDIT", "Every frozen Gemini output was inspected", deck: [Blinded LLM forensic review, not human ratings. The 156-page book hid model identity, prompt stage and automatic scores during first pass.])
#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 9pt,
  metric-card("REVIEWED", str(ai-blind.len()) + " / 156", "all blind cases have five axis labels and evidence"),
  metric-card("MAJOR ON ≥1 AXIS", pct(ai-major-any), "v1 LLM label; no perceptual calibration"),
  metric-card("v1 AXES PLAUSIBLE", pct(ai-axis-plausible), "post-unblind directionality judgment", kind: "blue"),
  metric-card("v1 BOX USEFUL", pct(ai-residual-useful), "registered cyan boxes often failed to localize", kind: "accent"),
)
#v(9mm)
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Canvas confound]
    Post-unblind LLM review marked *#pct(ai-canvas-confound)* of outputs as canvas-confounded. The v2 SSIM gate is stricter: only 2 / 156 pairs share both physical canvas and raster grid.
  ],
  [
    #heading(level: 2)[What manual review adds]
    It distinguishes broad reflow from localized corruption, catches raw command text and table collisions, and can reject a full-page residual enclosure that does not explain the defect.
  ],
)
#v(8mm)
#callout("v2 alignment with the same blinded LLM labels", [Pagination was the only strong discriminator: page-count AUC #num(ai-align.axis_alignment.pagination_page_count.issue_auc) and boundary AUC #num(ai-align.axis_alignment.pagination_boundary.issue_auc). Strict-token AUC was #num(ai-align.axis_alignment.content.issue_auc) and typography AUC #num(ai-align.axis_alignment.typography.issue_auc), both close to chance. Layout AUC is undefined because all 156 outputs were labeled with some layout issue. These are reviewer-consistency diagnostics, not perceptual validation.], kind: "blue")

#pagebreak()
#page-head("13 / FOUR-WAY OVERLAP", "Diagnostic alignment, not a leaderboard", deck: [Seven complete samples; 21 LLM-reviewed candidate PDFs.])
#grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: 9pt,
  metric-card("MAJOR", str(overlap-align.severity_counts.major), "visible document-level failures", kind: "accent"),
  metric-card("MODERATE", str(overlap-align.severity_counts.moderate), "clear flow/layout changes"),
  metric-card("MINOR", str(overlap-align.severity_counts.minor), "localized visible differences"),
  metric-card("NONE", str(overlap-align.severity_counts.none), "no clear defect at audit resolution", kind: "blue"),
)
#v(8mm)
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Exploratory pooled Spearman rho]
    #mini-bar("tolerant ink diagnostic", overlap-align.global_descriptive_spearman.ink_residual_loss.spearman_rho, color: blue)
    #v(5pt)
    #mini-bar("critical numbers", overlap-align.global_descriptive_spearman.critical_number_loss.spearman_rho, color: blue)
    #v(5pt)
    #mini-bar("page-count delta", overlap-align.global_descriptive_spearman.page_count_abs_delta.spearman_rho, color: blue)
    #v(5pt)
    #mini-bar("Text-LTSim loss", overlap-align.global_descriptive_spearman.text_ltsim_loss.spearman_rho, color: blue)
    #v(5pt)
    #mini-bar("strict text loss", overlap-align.global_descriptive_spearman.strict_content_loss.spearman_rho, color: accent)
  ],
  [
    #callout("Exploratory association", [The resized-canvas tolerant-ink diagnostic, critical-number mismatch, page-count error and Text-LTSim had the largest pooled rank associations with one LLM reviewer's severity ordering. This is not metric validation.], kind: "blue")
    #v(8pt)
    #callout("SSIM did not validate", [Among the 14 Claude pairs where SSIM was eligible, rho was #num(overlap-align.global_descriptive_spearman.ssim_loss.spearman_rho). It stays a localized diagnostic, not a grade.], kind: "accent")
    #v(8pt)
    #text(size: 8.3pt, fill: muted)[n=21 rows clustered in seven documents; one non-human reviewer; heterogeneous protocols. Pooled descriptive correlations are neither independent observations nor inferential benchmark claims.]
  ],
)

// Seven full 2 x 2 sheets.
#let grid-paths = (
  "../results/metric_research_v2/claude_overlap/visual_audit/sheet_01_04_math_aligned_014.png",
  "../results/metric_research_v2/claude_overlap/visual_audit/sheet_02_05_tables_simple_005.png",
  "../results/metric_research_v2/claude_overlap/visual_audit/sheet_03_05_tables_simple_021.png",
  "../results/metric_research_v2/claude_overlap/visual_audit/sheet_04_05_tables_simple_023.png",
  "../results/metric_research_v2/claude_overlap/visual_audit/sheet_05_06_tables_moderate_010.png",
  "../results/metric_research_v2/claude_overlap/visual_audit/sheet_06_07_figures_captions_007.png",
  "../results/metric_research_v2/claude_overlap/visual_audit/sheet_07_09_algorithms_003.png",
)
#for (index, path) in grid-paths.enumerate() [
  #pagebreak()
  #page-head("14–20 / COMPLETE VISUAL GRIDS", "Reference · Gemini · Claude Sonnet · Claude Opus", deck: [Sheet #str(index + 1) of 7. Full pages are tiled; exact protocol and canvas labels are printed inside each quadrant.])
  #align(center)[#image(path, width: 320mm)]
]

#let score-for(sample, role) = overlap-scores.find(row => row.sample_id == sample and row.asset_role == role)
#let pdf-box(path, page-no, bbox, ratio) = {
  let w = 52mm
  let h = w / ratio
  box(width: w, height: h, clip: true, stroke: 0.6pt + rule)[
    #image(path, page: page-no, width: w, height: h)
    #place(top + left, dx: bbox.at(0) * w, dy: bbox.at(1) * h)[
      #rect(width: (bbox.at(2) - bbox.at(0)) * w, height: (bbox.at(3) - bbox.at(1)) * h, stroke: 1.6pt + accent)
    ]
  ]
}
#let evidence-card(example) = {
  let score = score-for(example.sample, example.role)
  let ref-path = "../data/latex_benchmark_v0/corpus/" + example.category + "/" + example.sample + "/reference.pdf"
  block(fill: white, stroke: 0.7pt + rule, radius: 4pt, inset: 10pt)[
    #grid(columns: (56mm, 56mm, 1fr), gutter: 10pt, align: (center, center, left),
      [#label("REFERENCE") #v(3pt) #image(ref-path, page: example.ref-page, width: 52mm)],
      [#label(example.model) #v(3pt) #pdf-box(example.path, example.page, example.bbox, example.ratio)],
      [
        #text(weight: 650, size: 12pt)[#example.sample]
        #v(4pt)
        #text(size: 8.8pt)[#example.evidence]
        #v(6pt)
        #table(columns: (1fr, auto), inset: (x: 4pt, y: 2.5pt),
          [Strict token F1], [#num(float(score.strict_word_f1))],
          [Text-LTSim], [#num(float(score.text_ltsim_page_macro))],
          [Center q90], [#num(float(score.token_center_displacement_q90))],
          [Page delta], [#score.page_count_delta],
          [Number exact], [#score.number_exact],
          [SSIM], [#if score.unregistered_ssim == "" { "ABSTAIN" } else { num(float(score.unregistered_ssim)) }],
        )
        #v(4pt)
        #text(size: 7.6pt, fill: muted)[Box: candidate page #str(example.page), normalized [#example.bbox.map(value => str(value)).join(", ")].]
      ]
    )
  ]
}
#let examples = (
  (sample: "05_tables_simple_005", category: "05_tables_simple", role: "gemini", model: "GEMINI 3.1 FLASH LITE", path: "../results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/05_tables_simple_005/output.pdf", page: 2, ref-page: 1, bbox: (0.07, 0.82, 0.95, 0.99), ratio: 595.276/841.89, evidence: [Three pages replace two; the bottom of the table collapses into a dense, unreadable row/caption band.]),
  (sample: "05_tables_simple_023", category: "05_tables_simple", role: "gemini", model: "GEMINI 3.1 FLASH LITE", path: "../results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v0/samples/05_tables_simple_023/output.pdf", page: 2, ref-page: 3, bbox: (0.34, 0.51, 0.66, 0.80), ratio: 595.276/841.89, evidence: [Candidate renders rows 22–35 although the reference table visibly ends at row 21.]),
  (sample: "05_tables_simple_023", category: "05_tables_simple", role: "claude_sonnet", model: "CLAUDE SONNET 4.6", path: "../results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_023/claude-sonnet-4-6.pdf", page: 3, ref-page: 3, bbox: (0.12, 0.31, 0.46, 0.50), ratio: 612/792, evidence: [Page count is preserved, but table 2 contains 35 visible rows instead of the reference’s 21.]),
  (sample: "05_tables_simple_023", category: "05_tables_simple", role: "claude_opus", model: "CLAUDE OPUS 4.7", path: "../results/metric_calibration/canonical_ai_v0_3/compiled/canonical/05_tables_simple_023/claude-opus-4-7.pdf", page: 3, ref-page: 3, bbox: (0.29, 0.08, 0.74, 0.78), ratio: 612/792, evidence: [Literal Typst fragments such as #raw("#it") and #raw("#sc") are exposed inside cells; values are displaced from labels.]),
  (sample: "06_tables_moderate_010", category: "06_tables_moderate", role: "gemini", model: "GEMINI 3.1 FLASH LITE", path: "../results/ai_latex_to_typst/openrouter/google_gemini-3.1-flash-lite/prompt_v1_v0_failures/samples/06_tables_moderate_010/output.pdf", page: 2, ref-page: 1, bbox: (0.08, 0.84, 0.96, 1.00), ratio: 595.276/841.89, evidence: [Table 1 overflows the page; rows and caption are superimposed into one unreadable band.]),
  (sample: "06_tables_moderate_010", category: "06_tables_moderate", role: "claude_opus", model: "CLAUDE OPUS 4.7", path: "../results/metric_calibration/canonical_ai_v0_3/compiled/canonical/06_tables_moderate_010/claude-opus-4-7.pdf", page: 1, ref-page: 1, bbox: (0.11, 0.29, 0.90, 0.82), ratio: 612/792, evidence: [Structure and pagination are preserved; horizontal rules are visibly much heavier throughout the table body.]),
)
#for page-index in range(0, 3) [
  #pagebreak()
  #page-head("21–23 / LOCALIZED EVIDENCE", "Bounding boxes with objective score explanations", deck: [Only defects that can be localized defensibly receive boxes. Document-wide page-flow and absent-element failures intentionally do not.])
  #evidence-card(examples.at(page-index * 2))
  #v(8pt)
  #evidence-card(examples.at(page-index * 2 + 1))
]

#pagebreak()
#page-head("24 / INTERPRETATION", "What the metrics explain—and what they cannot", deck: [A high-quality evaluation system says “unknown” when the evidence is absent.])
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [
    #heading(level: 2)[Explains objectively]
    - exact missing/added words, numbers, operators and citations;
    - page-count and canvas differences;
    - matched token and block displacement;
    - transport flows that dominate Text-LTSim loss;
    - inverted block order and boundary errors;
    - translation-registered tolerant-ink enclosures, explicitly diagnostic;
    - extraction coverage and every abstention reason.
  ],
  [
    #heading(level: 2)[Does not establish]
    - human preference or acceptable visual tolerance;
    - semantic correctness of a table from text blocks alone;
    - formula-tree equality without common math parsing;
    - figure/caption relation fidelity without common regions;
    - fair model rank across different prompting and visual-feedback protocols;
    - a defensible universal scalar.
  ],
)
#v(8mm)
#callout("Operational use", [Use the vector to filter hard failures, compare candidates within the same axis and evidence regime, and inspect localized explanations. Do not average abstentions or let a strong axis compensate for a failed one.], kind: "blue")

#pagebreak()
#page-head("25 / PROTOTYPE DECISION", "Retained, diagnostic, pending, rejected", deck: [This is the smallest defensible research surface supported by the current data.])
#decision-row("Eligibility + provenance", "RETAIN", [Required before any comparison; exact hashes and generation protocol.], kind: "blue")
#v(7pt)
#decision-row("Strict content + partial critical inventory", "RETAIN", [Exact preservation with concrete mismatch evidence and explicit coverage limits.], kind: "blue")
#v(7pt)
#decision-row("Text-LTSim + token geometry", "RETAIN", [Text-only subset with raw coverage and localized flows.], kind: "blue")
#v(7pt)
#decision-row("Exact page count", "RETAIN", [Non-compensatory file-level fact.], kind: "blue")
#v(7pt)
#decision-row("Reading order / page assignment / boundaries", "CONDITIONAL", [Pending coverage, ambiguity and document-form gates.])
#v(7pt)
#decision-row("Typography metadata", "DIAGNOSTIC", [Raw residuals; producer metadata is not perceptual truth.])
#v(7pt)
#decision-row("Raster diagnostics", "DIAGNOSTIC", [SSIM fails closed; current tolerant-ink output is resized-canvas and translation-registered.])
#v(7pt)
#decision-row("Official CLEval", "PENDING", [Feedable from current words, but release waits for official implementation conformance.])
#v(7pt)
#decision-row("GriTS / TEDS / semantic LTSim", "ABSTAIN", [Required table/tree/semantic labels are absent.], kind: "accent")
#v(7pt)
#decision-row("Universal 0–100 score", "REJECT", [Not identifiable from current non-human evidence without arbitrary compensation.], kind: "accent")

#pagebreak()
#page-head("26 / NEXT STEPS", "The shortest path to a benchmark-grade release", deck: [No speculative platform work; each step closes a measured evidence gap.])
#enum(
  [*Freeze v2.* Hash evaluator, renderer, tokenizer and this exact 157-document corpus; rerun determinism after the final text-view split.],
  [*Repair the augmentation generator.* Exclude the 98 no-op/invisible cases and add a visibility preflight before accepting new perturbations.],
  [*Correct the raster axis.* Make tolerant-ink comparison and residual localization fail closed on physical canvas/grid mismatch; preserve any registered view as a separately named renderer diagnostic.],
  [*Implement official CLEval conformance.* Compare repository inputs against the official code on split/merge/crop/insert/delete property tests.],
  [*Build source-backed structure truth.* Export table cell grids/HTML, formula trees and figure/caption regions from both reference and candidate before enabling GriTS, TEDS or full semantic LTSim.],
  [*Run a controlled model experiment.* Same prompt, source access, reference-image access, repair budget, canvas and renderer for every model. The current Claude overlap cannot rank models.],
  [*Later, add human ratings if permitted.* Use paired, counterbalanced judgments to calibrate tolerances and any operational band. Until then, keep raw vectors and abstentions.],
)
#v(9mm)
#callout("Current best answer", [The real metric system is an evidence-bearing, non-compensatory vector. It is less convenient than a single score and substantially more honest—and on the present data it explains failures better.], kind: "accent")

#pagebreak()
#page-head("27 / REPRODUCIBILITY", "Configuration and evidence register", deck: [Paths are repository-relative; generated outputs are stored, hashed and fail-closed.])
#table(
  columns: (55mm, 1fr),
  [Evaluator], [`scripts/evaluation/pdf_metric_axes_v2.py`],
  [Batch scorer], [`scripts/evaluation/evaluate_metric_v2_manifest.py`],
  [Controlled scores], [`results/metric_research_v2/controlled_retained_628/metric_v2_scores_final.csv`],
  [All-157 identity], [`results/metric_research_v2/identity_157_final/`],
  [All-157 layout severity], [`results/metric_research_v2/layout_severity_all157/`],
  [Frozen Gemini scores + audit alignment], [`results/metric_research_v2/gemini_frozen_156/`],
  [Claude overlap], [`results/metric_research_v2/claude_overlap/`],
  [Manual controlled audit], [`results/metric_research_v1/full_157_v1/visual_audit/`],
  [Manual AI audit], [`results/metric_research_v1/ai_outputs_frozen_v1/visual_audit/`],
  [Research note], [`reports/pdf_metric_v2_research_note.md`],
)
#v(8mm)
#grid(columns: (1fr, 1fr), gutter: 14mm,
  [#heading(level: 2)[Frozen raster protocol] 96 dpi in v2 batch runs; grayscale; physical canvas equality required for SSIM. Current tolerant-ink F1 resizes the candidate canvas; its residual box is translation-registered and diagnostic only.],
  [#heading(level: 2)[Extraction boundary] PyMuPDF pages, characters, words, native text blocks and font metadata. No validated table cells, formula trees, semantic classes or authoritative reading order.],
)

#pagebreak()
#page-head("28 / REFERENCES", "Primary methods and implementation sources")
#set text(size: 9pt)
#enum(
  [Baek et al. *CLEval: Character-Level Evaluation for Text Detection and Recognition Tasks.* CVPRW 2020. #link("https://openaccess.thecvf.com/content_CVPRW_2020/papers/w34/Baek_CLEval_Character-Level_Evaluation_for_Text_Detection_and_Recognition_Tasks_CVPRW_2020_paper.pdf")[Paper] · #link("https://github.com/clovaai/CLEval")[official code].],
  [Kikuchi et al. *LTSim: Layout Transportation-based Similarity Measure.* 2024. #link("https://arxiv.org/pdf/2407.12356")[Paper].],
  [Smock et al. *GriTS: Grid Table Similarity Metric for Table Structure Recognition.* 2022. #link("https://arxiv.org/pdf/2203.12555")[Paper] · #link("https://github.com/microsoft/table-transformer")[official code].],
  [Zhong et al. *Image-based Table Recognition: Data, Model, and Evaluation.* PubTabNet / TEDS, 2019. #link("https://arxiv.org/pdf/1911.10683")[Paper] · #link("https://github.com/ibm-aur-nlp/PubTabNet")[official code].],
  [Wang et al. *Image Quality Assessment: From Error Visibility to Structural Similarity.* IEEE TIP 2004. #link("https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf")[Paper].],
  [Wang, Simoncelli and Bovik. *Multi-Scale Structural Similarity for Image Quality Assessment.* 2003. #link("https://ece.uwaterloo.ca/~z70wang/publications/msssim.pdf")[Paper].],
  [Lapata. *Automatic Evaluation of Information Ordering: Kendall's Tau.* Computational Linguistics 2006. #link("https://aclanthology.org/J06-4002.pdf")[Paper].],
  [Nilsson and Akenine-Möller. *Understanding SSIM.* 2020. #link("https://arxiv.org/pdf/2006.13846")[Paper].],
)
#v(10mm)
#callout("Report status", [Research prototype with inspectable raw diagnostics. Benchmark release remains pending the raster correction, conditional-axis gates, structure truth and—if later permitted—human perceptual calibration.], kind: "blue")
