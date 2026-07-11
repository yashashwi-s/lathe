#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

    #table(
    columns: (auto, auto, auto, auto),
    align: (left, left, right, right),
    table.hline(),
    table.cell(colspan: 2)[Taxonomy], table.cell(colspan: 2)[Metrics],
    table.hline(),
    [Class], [Order], [Avg. Weight (g)], [Avg. Length (cm)],
    table.hline(),
    table.cell(rowspan: 2)[Aves], [Passeriformes], [45.2], [15.4],
    [Strigiformes], [1200.5], [45.0],
    [Mammalia], [Rodentia], [25.4], [10.2],
    table.hline(),
)

