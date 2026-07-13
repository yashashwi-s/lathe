#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#figure(
  align(center)[#table(
    columns: 3,
    align: (left,center,right,),
    [#strong[Hyperparameter]], [#strong[Value]], [#strong[Impact]],
    [Learning Rate], [#mi(`3 \times 10^{-4}`)], [High],
    [Batch Size], [256], [Moderate],
    [Weight Decay], [#mi(`0.01`)], [Low],
  )]
  , kind: table
  )
