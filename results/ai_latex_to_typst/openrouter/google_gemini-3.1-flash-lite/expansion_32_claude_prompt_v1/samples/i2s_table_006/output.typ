#set page(paper: "us-letter", margin: 1in)
#set text(font: "serif", size: 11pt)

#align(center)[
  #text(size: 1.44em, weight: "bold")[Table Sample 6] \
  #text(size: 1.2em)[Dataset-expansion sample] \
  #v(1em)
]

#heading(level: 1)[Results]
The table below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#figure(
  caption: [The optimal hyperparameters for each downstream model type trained on Peptide-ESM embeddings for the low-N, med-N, and high-N conditions.],
  table(
    columns: (auto, auto, auto),
    stroke: 0.5pt,
    align: left,
    table.header([Embedding], [Downstream Model], [Hyperparameters]),
    [LazBF Peptide-ESM low-N], [SVC], [C=0.1, kernel='linear'],
    [LazBF Peptide-ESM low-N], [MLP], [hidden_layer_sizes=750, activation='relu'],
    [LazBF Peptide-ESM low-N], [LR], [C=1, penalty=None],
    [LazBF Peptide-ESM low-N], [RF], [n_estimators=50, criterion='entropy'],
    [LazBF Peptide-ESM low-N], [AB], [learning_rate=1, n_estimators=50],
    [LazBF Peptide-ESM low-N], [KNN], [n_neighbors=10, weights='uniform'],
    [LazDEF Peptide-ESM low-N], [SVC], [C=1, kernel='linear'],
    [LazDEF Peptide-ESM low-N], [MLP], [hidden_layer_sizes=500, activation='relu'],
    [LazDEF Peptide-ESM low-N], [LR], [C=1, penalty='None'],
    [LazDEF Peptide-ESM low-N], [RF], [n_estimators=200, criterion='gini'],
    [LazDEF Peptide-ESM low-N], [AB], [learning_rate=1, n_estimators=200],
    [LazDEF Peptide-ESM low-N], [KNN], [n_neighbors=25, weights='uniform'],
    [LazBF Peptide-ESM med-N], [SVC], [C=1, kernel='linear'],
    [LazBF Peptide-ESM med-N], [MLP], [hidden_layer_sizes=500, activation='tanh'],
    [LazBF Peptide-ESM med-N], [LR], [C=1, penalty=None],
    [LazBF Peptide-ESM med-N], [RF], [n_estimators=500, criterion='entropy'],
    [LazBF Peptide-ESM med-N], [AB], [learning_rate=0.1, n_estimators=200],
    [LazBF Peptide-ESM med-N], [KNN], [n_neighbors=10, weights='uniform'],
    [LazDEF Peptide-ESM med-N], [SVC], [C=0.1, kernel='linear'],
    [LazDEF Peptide-ESM med-N], [MLP], [hidden_layer_sizes=1000, activation='relu'],
    [LazDEF Peptide-ESM med-N], [LR], [C=0.1, penalty='None'],
    [LazDEF Peptide-ESM med-N], [RF], [n_estimators=200, criterion='entropy'],
    [LazDEF Peptide-ESM med-N], [AB], [learning_rate=1, n_estimators=500],
    [LazDEF Peptide-ESM med-N], [KNN], [n_neighbors=25, weights='distance'],
    [LazBF Peptide-ESM high-N], [SVC], [C=0.1, kernel='linear'],
    [LazBF Peptide-ESM high-N], [MLP], [hidden_layer_sizes=750, activation='tanh'],
    [LazBF Peptide-ESM high-N], [LR], [C=5, penalty=None],
    [LazBF Peptide-ESM high-N], [RF], [n_estimators=500, criterion='entropy'],
    [LazBF Peptide-ESM high-N], [AB], [learning_rate=1, n_estimators=500],
    [LazBF Peptide-ESM high-N], [KNN], [n_neighbors=50, weights='uniform'],
    [LazDEF Peptide-ESM high-N], [SVC], [C=5, kernel='linear'],
    [LazDEF Peptide-ESM high-N], [MLP], [hidden_layer_sizes=50, activation='relu'],
    [LazDEF Peptide-ESM high-N], [LR], [C=1, penalty='None'],
    [LazDEF Peptide-ESM high-N], [RF], [n_estimators=500, criterion='log loss'],
    [LazDEF Peptide-ESM high-N], [AB], [learning_rate=1, n_estimators=500],
    [LazDEF Peptide-ESM high-N], [KNN], [n_neighbors=50, weights='uniform'],
  )
)
