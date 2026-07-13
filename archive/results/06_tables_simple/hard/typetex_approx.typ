#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#figure(
  align(center)[#table(
    columns: 3,
    align: (center,center,center,),
    [#strong[Model Architecture]], [#strong[Parameters
    (M)]], [#strong[Throughput (seq/s)]],
    [Transformer-Base], [110], [2450],
    [Transformer-Large], [340], [890],
  )]
  , caption: [Inference performance metrics across model scales.]
  , kind: table
  )
