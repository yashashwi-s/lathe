#set page(width: 595pt, height: 842pt) // Match reference page size

#table(
  columns: (auto, auto, auto),
  align: center,
  stroke: 0.5pt, // Default stroke for all borders
  [Dataset], [Accuracy (%)], [Latency (ms)],
  [MNIST], [99.2], [12],
  [CIFAR-10], [95.8], [45],
  [ImageNet], [88.4], [120],
)