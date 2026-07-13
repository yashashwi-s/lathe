#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let heavyrule = 0.8pt
#let lightrule = 0.5pt

#table(
  columns: 4,
  stroke: none,
  align: (left, left, right, right),

  table.hline(y: 0, stroke: heavyrule),

  table.cell(colspan: 2, align: center)[Taxonomy],
  table.cell(colspan: 2, align: center)[Metrics],

  table.hline(y: 1, start: 0, end: 2, stroke: lightrule),
  table.hline(y: 1, start: 2, end: 4, stroke: lightrule),

  [Class],
  [Order],
  [Avg. Weight (g)],
  [Avg. Length (cm)],

  table.hline(y: 2, stroke: lightrule),

  [Aves],
  [Passeriformes],
  [45.2],
  [15.4],

  [Mammalia],
  [Rodentia],
  [25.4],
  [10.2],

  table.hline(y: 4, stroke: heavyrule),
)#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let heavyrule = 0.8pt
#let lightrule = 0.5pt

#table(
  columns: 4,
  stroke: none,
  align: (left, left, right, right),

  table.hline(y: 0, stroke: heavyrule),

  table.cell(colspan: 2, align: center)[Taxonomy],
  table.cell(colspan: 2, align: center)[Metrics],

  table.hline(y: 1, start: 0, end: 2, stroke: lightrule),
  table.hline(y: 1, start: 2, end: 4, stroke: lightrule),

  [Class],
  [Order],
  [Avg. Weight (g)],
  [Avg. Length (cm)],

  table.hline(y: 2, stroke: lightrule),

  [Aves],
  [Passeriformes],
  [45.2],
  [15.4],

  [Mammalia],
  [Rodentia],
  [25.4],
  [10.2],

  table.hline(y: 4, stroke: heavyrule),
)