#set document(title: "Table Conversion")
#set page(
  width: 595pt,
  height: 842pt,
  margin: (left: 1in, right: 1in, top: 1in, bottom: 1in), // Standard article margins
  footer: align(center, [#page-number]),
)

#table(
  columns: (auto, auto, auto, auto), // Equivalent to LaTeX's llrr
  align: (left, left, right, right),
  // booktabs-like styling for borders
  stroke: (
    top: 0.8pt,    // Corresponds to \toprule
    bottom: 0.8pt, // Corresponds to \bottomrule
    x: 0pt,        // No vertical lines
    y: 0pt,        // No default internal horizontal lines
  ),
  // Custom horizontal lines for cmidrule and midrule
  hline: (idx, _) => {
    if idx == 1 { // After the first header row (Taxonomy/Metrics)
      (column: 0..2, stroke: 0.5pt), // Corresponds to \cmidrule(r){1-2}
      (column: 2..4, stroke: 0.5pt), // Corresponds to \cmidrule(l){3-4}
    } else if idx == 2 { // After the second header row (Class/Order/Avg. Weight/Avg. Length)
      0.8pt // Corresponds to \midrule
    } else {
      none // No other internal horizontal lines
    }
  },
  // Table content
  cell(colspan: 2, align: center)[Taxonomy], cell(colspan: 2, align: center)[Metrics],
  [Class], [Order], [Avg. Weight (g)], [Avg. Length (cm)],
  cell(rowspan: 2)[Aves], [Passeriformes], [45.2], [15.4],
  [], [Strigiformes], [1200.5], [45.0],
  [Mammalia], [Rodentia], [25.4], [10.2],
)