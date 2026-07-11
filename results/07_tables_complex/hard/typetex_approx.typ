#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#figure(
  align(center)[#table(
    columns: 4,
    align: (left,left,right,right,),
    table.header(table.cell(align: center, colspan: 2)[Taxonomy], table.cell(align: center, colspan: 2)[Metrics],),
    table.hline(),
    [1-2 (l)3-4 Class], [Order], [Avg. Weight (g)], [Avg. Length (cm)],
    table.cell(rowspan: 2)[Aves], [Passeriformes], [45.2], [15.4],
    [Strigiformes], [1200.5], [45.0],
    [Mammalia], [Rodentia], [25.4], [10.2],
  )]
  , kind: table
  )
