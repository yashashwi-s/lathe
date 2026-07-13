#set page(
  numbering: "1",
  // The LaTeX article class typically has margins around 1.5in top/bottom and 1.25in left/right.
  // Typst's default 1in margins are usually sufficient and visually similar for most documents.
)

// Define custom commands for math variables used in the table header
#let dmodel = $d_("model")$
#let dff = $d_("ff")$

// Center the table on the page
#align(center)[
  #table(
    // Table caption and label
    caption: [
      Variations on the Transformer architecture. Unlisted values are identical
      to those of the base model. All metrics are on the English-to-German translation
      development set, newstest2013.
    ],
    label: "tab:variations",
    
    // Define column properties: auto-sizing for all columns, centered content
    columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto),
    align: center,
    
    // Define strokes (lines) for the table
    // x: vertical lines after column 1 and column 9
    // y: horizontal lines before the first row, after header (row 2), after base (row 3),
    //    after (A) (row 7), after (B) (row 9), after (C) (row 16),
    //    after (D) (row 20), after (E) (row 21), and after the last row (row 22).
    stroke: (x: (1, 9), y: (1, 3, 4, 8, 10, 17, 21, 22, 23)),
    
    // Table Header
    // Row 1 of header: Multi-row cells for N through epsilon_ls, single-row for train, PPL, BLEU, params
    [ ], // Empty cell for the first column
    (rowspan: 2, [ $N$ ]),
    (rowspan: 2, [ #dmodel ]),
    (rowspan: 2, [ #dff ]),
    (rowspan: 2, [ $h$ ]),
    (rowspan: 2, [ $d_k$ ]),
    (rowspan: 2, [ $d_v$ ]),
    (rowspan: 2, [ $P_("drop")$ ]),
    (rowspan: 2, [ $\epsilon_("ls")$ ]),
    [ train ],
    [ PPL ],
    [ BLEU ],
    [ params ],
    // Row 2 of header: Empty cell for the first column, then the bottom parts of the non-multirow cells
    [ ], // Empty cell for the first column (covered by the rowspan of the first cell)
    // The next 8 cells are implicitly skipped due to the `rowspan: 2` in the previous row
    [ steps ],
    [ (dev) ],
    [ (dev) ],
    [ $\times 10^6$ ],

    // Base model row
    [ base ], [ 6 ], [ 512 ], [ 2048 ], [ 8 ], [ 64 ], [ 64 ], [ 0.1 ], [ 0.1 ], [ 100K ], [ 4.92 ], [ 25.8 ], [ 65 ],

    // Section (A) - Variations in h, d_k, d_v
    (rowspan: 4, [(A)]), [ ], [ ], [ ], [ 1 ], [ 512 ], [ 512 ], [ ], [ ], [ ], [ 5.29 ], [ 24.9 ], [ ],
    [ ], [ ], [ ], [ ], [ 4 ], [ 128 ], [ 128 ], [ ], [ ], [ ], [ 5.00 ], [ 25.5 ], [ ],
    [ ], [ ], [ ], [ ], [ 16 ], [ 32 ], [ 32 ], [ ], [ ], [ ], [ 4.91 ], [ 25.8 ], [ ],
    [ ], [ ], [ ], [ ], [ 32 ], [ 16 ], [ 16 ], [ ], [ ], [ ], [ 5.01 ], [ 25.4 ], [ ],

    // Section (B) - Variations in d_k
    (rowspan: 2, [(B)]), [ ], [ ], [ ], [ ], [ 16 ], [ ], [ ], [ ], [ ], [ 5.16 ], [ 25.1 ], [ 58 ],
    [ ], [ ], [ ], [ ], [ ], [ 32 ], [ ], [ ], [ ], [ ], [ 5.01 ], [ 25.4 ], [ 60 ],

    // Section (C) - Variations in N, d_model, d_ff
    (rowspan: 7, [(C)]), [ 2 ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 6.11 ], [ 23.7 ], [ 36 ],
    [ ], [ 4 ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 5.19 ], [ 25.3 ], [ 50 ],
    [ ], [ 8 ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 4.88 ], [ 25.5 ], [ 80 ],
    [ ], [ ], [ 256 ], [ ], [ ], [ ], [ 32 ], [ 32 ], [ ], [ ], [ ], [ 5.75 ], [ 24.5 ], [ 28 ],
    [ ], [ ], [ 1024 ], [ ], [ ], [ ], [ 128 ], [ 128 ], [ ], [ ], [ ], [ 4.66 ], [ 26.0 ], [ 168 ],
    [ ], [ ], [ ], [ 1024 ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 5.12 ], [ 25.4 ], [ 53 ],
    [ ], [ ], [ ], [ 4096 ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 4.75 ], [ 26.2 ], [ 90 ],

    // Section (D) - Variations in P_drop, epsilon_ls
    (rowspan: 4, [(D)]), [ ], [ ], [ ], [ ], [ ], [ ], [ 0.0 ], [ ], [ ], [ ], [ 5.77 ], [ 24.6 ], [ ],
    [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 0.2 ], [ ], [ ], [ ], [ 4.95 ], [ 25.5 ], [ ],
    [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 0.0 ], [ ], [ ], [ 4.67 ], [ 25.3 ], [ ],
    [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ ], [ 0.2 ], [ ], [ ], [ 5.47 ], [ 25.7 ], [ ],

    // Section (E) - Positional embedding type
    [(E)], [ ], (colspan: 7, [positional embedding instead of sinusoids]), [ ], [4.92], [25.7], [ ],

    // Big model row
    [ big ], [ 6 ], [ 1024 ], [ 4096 ], [ 16 ], [ ], [ ], [ 0.3 ], [ ], [ 300K ], [*4.33*], [*26.4*], [ 213 ],
  )
]
```