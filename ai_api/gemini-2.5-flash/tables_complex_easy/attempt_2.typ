#set document(paper: "a4")

#table(
  columns: (auto, auto, auto), // Define 3 columns with automatic width
  stroke: 0.5pt, // Apply a 0.5pt stroke to all cell borders and outer table borders
  align: center, // Center align content in all cells

  // Header Row 1
  // The "Phase" cell spans 2 rows
  cell(rowspan: 2, [Phase]),
  // The "Duration (hours)" cell spans 2 columns
  cell(colspan: 2, [Duration (hours)]),

  // Header Row 2
  // The first column is occupied by the "Phase" cell from the row above.
  // Define content for the remaining columns.
  [Expected],
  [Actual],

  // Data rows
  [Setup], [2.0], [2.5],
  [Execution], [12.0], [11.5],
  [Analysis], [4.0], [5.0],
)