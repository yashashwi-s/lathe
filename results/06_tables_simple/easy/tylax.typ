#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

  #table(
    columns: (auto, auto, auto),
    align: (center, center, center),
    table.hline(),
    [Dataset], [Accuracy (%)], [Latency (ms)],
    table.hline(),
    [MNIST], [99.2], [12],
    [CIFAR-10], [95.8], [45],
    [ImageNet], [88.4], [120],
    table.hline(),
)

