#import "@preview/article:0.3.1"

// Set document properties to closely match LaTeX article class defaults
#show: article.doc.with(
  // Default font is often Computer Modern or Latin Modern in LaTeX.
  // New Computer Modern is a good Typst equivalent.
  font: "New Computer Modern",
  lang: "en",
  // Margins are typically 1 inch (2.54cm) in LaTeX article class.
  // Typst's article template often defaults to this.
  // If specific margin adjustments are needed, they would go here.
  // For example: page-margin: (left: 1in, right: 1in, top: 1in, bottom: 1in),
)

// Table hline function to replicate booktabs and custom rules
#let table-hline(idx, col-idx, col-span) = {
  if idx == 0 { // Toprule
    line(length: 100%, stroke: 0.8pt) // Thicker top rule
  } else if idx == 1 { // Cmidrules (between header row 1 and header row 2)
    if col-idx == 1 and col-span == 2 { // For BLEU (columns 2-3)
      line(length: 100%, stroke: 0.5pt)
    } else if col-idx == 4 and col-span == 2 { // For Training Cost (columns 5-6)
      line(length: 100%, stroke: 0.5pt)
    } else {
      none // No line for other columns in this row
    }
  } else if idx == 7 { // Hline after MoE (row 6, 0-indexed, so before row 7)
    line(length: 100%, stroke: 0.5pt)
  } else if idx == 10 { // Specialrule after ConvS2S Ensemble (row 9, 0-indexed, so before row 10)
    line(length: 100%, stroke: 1pt) // 1pt thick
  } else if idx == -1 { // Bottomrule (after the last row)
    line(length: 100%, stroke: 0.8pt) // Thicker bottom rule
  } else {
    none // No other horizontal lines by default
  }
}

#figure(
  align(center,
    table(
      columns: (auto, auto, auto, auto, auto, auto), // 6 columns
      align: (left, center, center, center, center, center), // Column alignments
      hline: table-hline, // Custom horizontal line function
      // No default stroke for internal lines, as we draw them explicitly via hline.
      // column-gutter: 0.8em, // Adjust as needed for column spacing
      // row-gutter: 0.5em, // Adjust as needed for row spacing

      // Header row 1
      table.cell(rowspan: 2, [Model]), // Model spans 2 rows
      table.cell(colspan: 2, align: center, [BLEU]), // BLEU spans 2 columns
      [], // Empty cell for the gap column
      table.cell(colspan: 2, align: center, [Training Cost (FLOPs)]), // Training Cost spans 2 columns

      // Header row 2 (content for the second row of the header)
      // Model cell is spanned from above
      [EN-DE], [EN-FR],
      [], // Empty cell for the gap column
      [EN-DE], [EN-FR],

      // Data rows
      // ByteNet
      [ByteNet], [23.75], [], [], [], [],
      // Deep-Att + PosUnk
      [Deep-Att + PosUnk], [], [39.2], [], [], [$1.0 dot 10^20$],
      // GNMT + RL
      [GNMT + RL], [24.6], [39.92], [], [$2.3 dot 10^19$], [$1.4 dot 10^20$],
      // ConvS2S
      [ConvS2S], [25.16], [40.46], [], [$9.6 dot 10^18$], [$1.5 dot 10^20$],
      // MoE
      [MoE], [26.03], [40.56], [], [$2.0 dot 10^19$], [$1.2 dot 10^20$],

      // Deep-Att + PosUnk Ensemble (after hline, with vertical padding)
      [#v(2em)Deep-Att + PosUnk Ensemble], [], [40.4], [], [], [$8.0 dot 10^20$],
      // GNMT + RL Ensemble
      [GNMT + RL Ensemble], [26.30], [41.16], [], [$1.8 dot 10^20$], [$1.1 dot 10^21$],
      // ConvS2S Ensemble
      [ConvS2S Ensemble], [26.36], [strong("41.29")], [], [$7.7 dot 10^19$], [$1.2 dot 10^21$],

      // Transformer (base model) (after specialrule, with vertical padding)
      [#v(2.2em)Transformer (base model)], [27.3], [38.1], [], table.cell(colspan: 2, align: center, strong($3.3 dot 10^18$)),
      // Transformer (big)
      [Transformer (big)], [strong("28.4")], [strong("41.8")], [], table.cell(colspan: 2, align: center, [$2.3 dot 10^19$]),
    )
  ),
  caption: [The Transformer achieves better BLEU scores than previous state-of-the-art models on the English-to-German and English-to-French newstest2014 tests at a fraction of the training cost.],
  label: <tab:wmt-results>,
  // Adjust spacing between caption and table body to match LaTeX's \vspace{-2mm}
  spacing: (body: 0mm),
)