#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Results
<results>
The table below is drawn from a source-backed image-to-LaTeX benchmark
and reproduced verbatim.

#figure(
  align(center)[#table(
    columns: 3,
    align: (left,left,left,),
    table.header([Embedding], [Downstream Model], [Hyperparameters],),
    table.hline(),
    [LazBF Peptide-ESM low-N], [SVC], [C#mi(`=`)0.1, kernel='linear'],
    [LazBF Peptide-ESM low-N], [MLP], [hidden\_layer\_sizes#mi(`=`)750,
    activation#mi(`=`)'relu'],
    [LazBF Peptide-ESM low-N], [LR], [C#mi(`=`)1, penalty#mi(`=`)None],
    [LazBF Peptide-ESM low-N], [RF], [n\_estimators#mi(`=`)50,
    criterion#mi(`=`)'entropy'],
    [LazBF Peptide-ESM low-N], [AB], [learning\_rate#mi(`=`)1,
    n\_estimators#mi(`=`)50],
    [LazBF Peptide-ESM low-N], [KNN], [n\_neighbors#mi(`=`)10,
    weights#mi(`=`)'uniform'],
    [LazDEF Peptide-ESM low-N], [SVC], [C#mi(`=`)1, kernel='linear'],
    [LazDEF Peptide-ESM low-N], [MLP], [hidden\_layer\_sizes#mi(`=`)500,
    activation#mi(`=`)'relu'],
    [LazDEF Peptide-ESM low-N], [LR], [C#mi(`=`)1,
    penalty#mi(`=`)'None'],
    [LazDEF Peptide-ESM low-N], [RF], [n\_estimators#mi(`=`)200,
    criterion#mi(`=`)'gini'],
    [LazDEF Peptide-ESM low-N], [AB], [learning\_rate#mi(`=`)1,
    n\_estimators#mi(`=`)200],
    [LazDEF Peptide-ESM low-N], [KNN], [n\_neighbors#mi(`=`)25,
    weights#mi(`=`)'uniform'],
    [LazBF Peptide-ESM med-N], [SVC], [C#mi(`=`)1, kernel='linear'],
    [LazBF Peptide-ESM med-N], [MLP], [hidden\_layer\_sizes#mi(`=`)500,
    activation#mi(`=`)'tanh'],
    [LazBF Peptide-ESM med-N], [LR], [C#mi(`=`)1, penalty#mi(`=`)None],
    [LazBF Peptide-ESM med-N], [RF], [n\_estimators#mi(`=`)500,
    criterion#mi(`=`)'entropy'],
    [LazBF Peptide-ESM med-N], [AB], [learning\_rate#mi(`=`)0.1,
    n\_estimators#mi(`=`)200],
    [LazBF Peptide-ESM med-N], [KNN], [n\_neighbors#mi(`=`)10,
    weights#mi(`=`)'uniform'],
    [LazDEF Peptide-ESM med-N], [SVC], [C#mi(`=`)0.1, kernel='linear'],
    [LazDEF Peptide-ESM
    med-N], [MLP], [hidden\_layer\_sizes#mi(`=`)1000,
    activation#mi(`=`)'relu'],
    [LazDEF Peptide-ESM med-N], [LR], [C#mi(`=`)0.1,
    penalty#mi(`=`)'None'],
    [LazDEF Peptide-ESM med-N], [RF], [n\_estimators#mi(`=`)200,
    criterion#mi(`=`)'entropy'],
    [LazDEF Peptide-ESM med-N], [AB], [learning\_rate#mi(`=`)1,
    n\_estimators#mi(`=`)500],
    [LazDEF Peptide-ESM med-N], [KNN], [n\_neighbors#mi(`=`)25,
    weights#mi(`=`)'distance'],
    [LazBF Peptide-ESM high-N], [SVC], [C#mi(`=`)0.1, kernel='linear'],
    [LazBF Peptide-ESM high-N], [MLP], [hidden\_layer\_sizes#mi(`=`)750,
    activation#mi(`=`)'tanh'],
    [LazBF Peptide-ESM high-N], [LR], [C#mi(`=`)5, penalty#mi(`=`)None],
    [LazBF Peptide-ESM high-N], [RF], [n\_estimators#mi(`=`)500,
    criterion#mi(`=`)'entropy'],
    [LazBF Peptide-ESM high-N], [AB], [learning\_rate#mi(`=`)1,
    n\_estimators#mi(`=`)500],
    [LazBF Peptide-ESM high-N], [KNN], [n\_neighbors#mi(`=`)50,
    weights#mi(`=`)'uniform'],
    [LazDEF Peptide-ESM high-N], [SVC], [C#mi(`=`)5, kernel='linear'],
    [LazDEF Peptide-ESM high-N], [MLP], [hidden\_layer\_sizes#mi(`=`)50,
    activation#mi(`=`)'relu'],
    [LazDEF Peptide-ESM high-N], [LR], [C#mi(`=`)1,
    penalty#mi(`=`)'None'],
    [LazDEF Peptide-ESM high-N], [RF], [n\_estimators#mi(`=`)500,
    criterion#mi(`=`)'log loss'],
    [LazDEF Peptide-ESM high-N], [AB], [learning\_rate#mi(`=`)1,
    n\_estimators#mi(`=`)500],
    [LazDEF Peptide-ESM high-N], [KNN], [n\_neighbors#mi(`=`)50,
    weights#mi(`=`)'uniform'],
  )]
  , caption: [The optimal hyperparameters for each downstream model type
  trained on Peptide-ESM embeddings for the low-N, med-N, and high-N
  conditions.]
  , kind: table
  )
