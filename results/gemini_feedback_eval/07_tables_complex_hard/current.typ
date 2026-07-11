#table(
  columns: ("left", "left", "right", "right"), // Corresponds to llrr in LaTeX
  stroke: (top: 1pt, bottom: 1pt), // For \toprule and \bottomrule
  header: 2, // The first two rows are header rows

  // Header Row 1: Taxonomy and Metrics with \multicolumn and \cmidrule
  // \cmidrule(r){1-2} \cmidrule(l){3-4} are approximated by bottom strokes on the cells.
  [
    #table.cell(colspan: 2, align: center, stroke: (bottom: 1pt))[Taxonomy],
    #table.cell(colspan: 2, align: center, stroke: (bottom: 1pt))[Metrics],
  ],

  // Header Row 2: Class, Order, Avg. Weight, Avg. Length with \midrule below
  // \midrule is approximated by applying a bottom stroke to each cell in this row.
  [
    #table.cell(stroke: (bottom: 1pt))[Class],
    #table.cell(stroke: (bottom: 1pt))[Order],
    #table.cell(stroke: (bottom: 1pt))[Avg. Weight (g)],
    #table.cell(stroke: (bottom: 1pt))[Avg. Length (cm)],
  ],

  // Data Row 1: Aves (Passeriformes) with \multirow
  [
    #table.cell(rowspan: 2)[Aves], // Corresponds to \multirow{2}{*}{Aves}
    [Passeriformes],
    [45.2],
    [15.4],
  ],
  // Data Row 2: Aves (Strigiformes) - continues rowspan from previous row
  [
    [Strigiformes],
    [1200.5],
    [45.0],
  ],
  // Data Row 3: Mammalia (Rodentia)
  [
    [Mammalia],
    [Rodentia],
    [25.4],
    [10.2],
  ],
)