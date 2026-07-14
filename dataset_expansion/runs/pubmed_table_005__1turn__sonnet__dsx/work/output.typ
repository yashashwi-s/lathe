#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Clinical Table Sample 5]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Patient Data

The table below is a medical-literature table reproduced verbatim from a PubMed-derived dataset.

#set text(size: 7pt)

#let c(content) = align(center)[#content]
#let b(content) = text(weight: "bold")[#content]

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto),
  align: (col, row) => left,
  stroke: 0.5pt,

  // Row 1: header spanning
  [], table.cell(colspan: 17, align: center)[#b[Percent of individual counts of demonstrated patterns (patterns without any counts are not listed)]],

  // Row 2: subject headers
  [#b[Subjects]], [#b[P1]], [#b[P2]], [#b[P3]], [#b[P4]], [#b[P5]], [#b[P6]], [#b[P7]], [#b[P8]], [#b[P9]], [#b[P1]0], [#b[P1]1], [#b[P1]2], [#b[P1]3], [#b[P1]4], [#b[P1]5], [#b[P1]6], [],

  // Row 3: LS header
  [Patterns\*], table.cell(colspan: 16, align: center)[Long swings, summarized all (LS: n = 103)], [% in total],

  // LS data rows
  [1-2-3], [85.7], [92.9], [100], [100], [100], [83.3], [100], [33.3], [33.3], [], [100], [], [43.7], [80], [90], [100], [76.1],
  [2-1-3], [], [7.1], [], [], [], [16.7], [], [], [50], [100], [], [], [25], [], [], [], [13.3],
  [1-3-2], [14.3], [], [], [], [], [], [], [], [], [], [], [], [25], [], [10], [], [3.3],
  [2-3-1], [], [], [], [], [], [], [], [66.7], [16.7], [], [], [], [6.3], [20], [], [], [7.3],
  [Sum], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100],

  // NAS header
  table.cell(colspan: 16, align: center)[Near axis swings, summarized all (NAS: n = 31)], [% in total],

  // NAS data rows
  [1-2-3], [80], [], [33.3], [], [], [], [], [], [100], [], [], [], [33.3], [], [], [], [30.8],
  [2-1-3], [20], [], [66.7], [], [], [50], [100], [100], [], [], [66.7], [], [66.7], [], [], [], [58.8],
  [1-3-2], [], [], [], [], [], [25], [], [], [], [], [33.3], [], [], [], [], [], [7.3],
  [2-3-1], [], [], [], [], [], [25], [], [], [], [], [], [], [], [], [], [], [3.1],
  [Sum], [100], [], [100], [], [], [100], [100], [100], [100], [], [100], [], [100], [], [], [], [100],

  // UAS header
  table.cell(colspan: 16, align: center)[Upper arm swings, summarized all (UAS: n = 15)], [% in total],

  // UAS data rows
  [2–3\*\*], [], [], [], [], [100], [100], [100], [], [100], [], [], [], [], [], [], [], [80],
  [3–2], [100], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [20],
  [Sum], [100], [], [], [], [100], [100], [100], [], [100], [], [], [], [], [], [], [], [100],

  // SupS header
  table.cell(colspan: 16, align: center)[Support swings, summarized all (SupS: n = 138)], [% in total],

  // SupS data rows
  [2–3\*\*], [100], [], [], [], [100], [90.6], [100], [100], [100], [100], [], [], [100], [], [], [], [98.8],
  [3–2], [], [], [], [], [], [9.4], [], [], [], [], [], [], [], [], [], [], [1.2],
  [Sum], [100], [], [], [], [100], [100], [100], [100], [100], [100], [], [], [100], [], [], [], [100],

  // HSS header
  table.cell(colspan: 16, align: center)[Handspring-Salto on Trampoline, summarized all (HSS: n = 15)], [% in total],

  // HSS data rows
  [1-2-3], [], [], [], [], [], [], [], [], [], [], [], [], [], [80], [80], [100], [86.7],
  [1-3-2], [], [], [], [], [], [], [], [], [], [], [], [], [], [20], [20], [], [13.3],
  [Sum], [], [], [], [], [], [], [], [], [], [], [], [], [], [100], [100], [100], [100],

  // Turns header
  table.cell(colspan: 16, align: center)[Pivot movements, summarized all (Turns: n = 9)], [% in total],

  // Turns data rows
  [1-2-3], [], [], [], [], [100], [100], [100], [50], [100], [100], [], [100], [], [], [], [], [81.3],
  [3-1-2], [], [], [], [100], [], [], [], [], [], [], [], [], [], [], [], [], [12.5],
  [2-3-1], [], [], [], [], [], [], [], [50], [], [], [], [], [], [], [], [], [6.2],
  [Sum], [], [], [], [100], [100], [100], [100], [100], [100], [100], [], [100], [], [], [], [], [100],

  // All elements header
  [All elements], table.cell(colspan: 16, align: center)[All elements summarized (patterns in % of counts) without UAS and SupS\*\*], [% in total],

  // All elements data rows
  [1-2-3], [82.9], [92.9], [66.7], [50], [100], [61.2], [66.7], [27.8], [77.8], [50], [50], [100], [38.6], [80], [85], [100], [70.6],
  [2-1-3], [10], [7.1], [33.3], [], [], [22.2], [33.3], [33.3], [16.7], [50], [33.3], [], [45.8], [], [15], [], [18.8],
  [1-3-2], [7.1], [], [], [], [], [8.3], [], [], [], [], [16.7], [], [12.5], [10], [], [], [3.4],
  [3-1-2], [], [], [], [50], [], [], [], [], [], [], [], [], [3.1], [], [], [], [3.3],
  [2-3-1], [], [], [], [], [], [8.3], [], [38.9], [5.5], [], [], [], [], [10], [], [], [3.9],
  [3-2-1], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [0],
  [Sum], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100], [100],

  // UAS SupS summary header
  table.cell(colspan: 16, align: center)[UAS and SupS\*\* summarized (patterns in % of counts)], [% in total],

  // UAS SupS data rows
  [2–3\*\*], [50], [], [], [], [100], [92.7], [100], [100], [100], [100], [], [], [100], [], [], [], [92.8],
  [3–2], [50], [], [], [], [], [7.3], [], [], [], [], [], [], [], [], [], [], [7.2],
  [100], [], [], [], [100], [100], [100], [100], [100], [100], [], [], [100], [], [], [], [100],

  // Footer subject row
  [#b[Subjects]], [#b[P1]], [#b[P2]], [#b[P3]], [#b[P4]], [#b[P5]], [#b[P6]], [#b[P7]], [#b[P8]], [#b[P9]], [#b[P1]0], [#b[P1]1], [#b[P1]2], [#b[P1]3], [#b[P1]4], [#b[P1]5], [#b[P1]6], [],
)
