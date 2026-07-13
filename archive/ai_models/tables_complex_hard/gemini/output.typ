#table(
columns: 4,
stroke: none,
align: (col, row) => (left, left, right, right).at(col),
table.hline(stroke: 1pt),
table.cell(colspan: 2, align: center)[Taxonomy],
table.cell(colspan: 2, align: center)[Metrics],
table.hline(start: 0, end: 2, stroke: 0.5pt),
table.hline(start: 2, end: 4, stroke: 0.5pt),
[Class], [Order], [Avg. Weight (g)], [Avg. Length (cm)],
table.hline(stroke: 0.5pt),
table.cell(rowspan: 2)[Aves], [Passeriformes], [45.2], [15.4],
[Strigiformes], [1200.5], [45.0],
[Mammalia], [Rodentia], [25.4], [10.2],
table.hline(stroke: 1pt)
)