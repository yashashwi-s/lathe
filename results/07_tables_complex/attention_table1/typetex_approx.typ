#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#block[
#block[
#figure(
  align(center)[#table(
    columns: 6,
    align: (left,center,center,center,center,center,),
    table.header([Model], table.cell(align: center, colspan: 2)[BLEU], [], table.cell(align: center, colspan: 2)[Training
      Cost (FLOPs)],),
    table.hline(),
    [2-3], [EN-DE], [EN-FR], [], [EN-DE], [EN-FR],
    [ByteNet], [23.75], [], [], [], [],
    [Deep-Att + PosUnk], [], [39.2], [], [], [#mi(`1.0\cdot10^{20}`)],
    [GNMT +
    RL], [24.6], [39.92], [], [#mi(`2.3\cdot10^{19}`)], [#mi(`1.4\cdot10^{20}`)],
    [ConvS2S], [25.16], [40.46], [], [#mi(`9.6\cdot10^{18}`)], [#mi(`1.5\cdot10^{20}`)],
    [MoE], [26.03], [40.56], [], [#mi(`2.0\cdot10^{19}`)], [#mi(`1.2\cdot10^{20}`)],
    [Deep-Att + PosUnk
    Ensemble], [], [40.4], [], [], [#mi(`8.0\cdot10^{20}`)],
    [GNMT + RL
    Ensemble], [26.30], [41.16], [], [#mi(`1.8\cdot10^{20}`)], [#mi(`1.1\cdot10^{21}`)],
    [ConvS2S
    Ensemble], [26.36], [#strong[41.29]], [], [#mi(`7.7\cdot10^{19}`)], [#mi(`1.2\cdot10^{21}`)],
    [Transformer (base
    model)], [27.3], [38.1], [], table.cell(align: center, colspan: 2)[#mi(`3.3\cdot10^{18}`)],
    [Transformer
    (big)], [#strong[28.4]], [#strong[41.8]], [], table.cell(align: center, colspan: 2)[#mi(`2.3\cdot10^{19}`)],
  )]
  , caption: [The Transformer achieves better BLEU scores than previous
  state-of-the-art models on the English-to-German and English-to-French
  newstest2014 tests at a fraction of the training cost. ]
  , kind: table
  )

] <tab:wmt-results>
]
