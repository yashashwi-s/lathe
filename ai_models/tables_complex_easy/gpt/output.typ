#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#table(
  columns: 3,
  align: center,
  stroke: (x, y) => (
    left: if x == 0 { 0.4pt + black } else { none },
    right: 0.4pt + black,
  ),
  table.hline(stroke: 0.4pt + black),
  table.cell(rowspan: 2)[Phase],
  table.cell(colspan: 2)[Duration (hours)],
  [Expected], [Actual],
  table.hline(stroke: 0.4pt + black),
  [Setup], [2.0], [2.5],
  [Execution], [12.0], [11.5],
  [Analysis], [4.0], [5.0],
  table.hline(stroke: 0.4pt + black),
)