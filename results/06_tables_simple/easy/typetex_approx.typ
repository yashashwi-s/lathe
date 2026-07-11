#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#figure(
  align(center)[#table(
    columns: 3,
    align: (center,center,center,),
    table.header([Dataset], [Accuracy (%)], [Latency (ms)],),
    table.hline(),
    [MNIST], [99.2], [12],
    [CIFAR-10], [95.8], [45],
    [ImageNet], [88.4], [120],
  )]
  , kind: table
  )
