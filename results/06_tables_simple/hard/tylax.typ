#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#figure(
  caption: [Inference performance metrics across model scales.],
)[
#table(
    columns: (auto, auto, auto),
    align: (center, center, center),
    [*Model Architecture*], [*Parameters (M)*], [*Throughput (seq/s)*],
    [Transformer-Base], [110], [2450],
    [Transformer-Large], [340], [890],
)

]

