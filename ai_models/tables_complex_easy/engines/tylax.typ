#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

   #table(
    columns: (auto, auto, auto),
    align: (center, center, center),
    table.hline(),
    table.cell(rowspan: 2)[Phase], table.cell(colspan: 2)[Duration (hours)],
    [Expected], [Actual],
    table.hline(),
    [Setup], [2.0], [2.5],
    [Execution], [12.0], [11.5],
    [Analysis], [4.0], [5.0],
    table.hline(),
)

