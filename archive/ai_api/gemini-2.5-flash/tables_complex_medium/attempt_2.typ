#set page(
  // Set standard A4 page size and margins, similar to LaTeX's article class defaults.
  // The reference image shows a page of 595x842 pt, which is A4.
  // Margins are estimated to match the visual placement of the table.
  margin: (top: 72pt, bottom: 72pt, left: 90pt, right: 90pt),
)

// The original LaTeX document does not explicitly center the table,
// but the reference render shows it horizontally centered on the page.
// We use #align(center) to achieve this.
#align(center)[
  #table(
    // Define column alignments: two left-aligned, two right-aligned.
    // In Typst, column alignments are specified as strings "left", "right", "center".
    columns: (2, "left", "right", "right"), // The first argument is the number of columns, then their alignments.
                                           // Or, more explicitly: (auto, auto, auto, auto) and then specify align for each cell.
                                           // For direct column alignment, it should be like this:
    // columns: (auto, auto, auto, auto), // This defines 4 columns of automatic width
    // align: (left, left, right, right), // This sets the alignment for all cells in each column.
    // Let's try the more direct way for column alignment.
    columns: (auto, auto, auto, auto),
    align: (left, left, right, right),

    // Configure table strokes to mimic booktabs styling:
    // - `stroke`: Applies to the outer frame of the table.
    //   - `top: 2pt`: A thick top rule (like \toprule).
    //   - `bottom: 2pt`: A thick bottom rule (like \bottomrule).
    //   - `left: none, right: none`: No vertical rules on the sides.
    // - `header-stroke`: Applies to the rule directly below the header row.
    //   - `bottom: 1pt`: A thinner rule below the header (like \midrule).
    // - `row-stroke: none`: No horizontal rules between data rows.
    // - `column-stroke: none`: No vertical rules between columns.
    stroke: (top: 2pt, bottom: 2pt, left: none, right: none),
    header-stroke: (bottom: 1pt),
    row-stroke: none,
    column-stroke: none,

    // Define the header row content.
    header: (
      [Family],
      [Species],
      [Mass (kg)],
      [Lifespan (yrs)],
    ),

    // Define the data rows.
    [Felidae], [Panthera leo], [190.0], [14],
    [Canidae], [Canis lupus], [40.0], [8],
    [Ursidae], [Ursus arctos], [300.0], [25],
  )
]