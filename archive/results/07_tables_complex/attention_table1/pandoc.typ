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
    [Deep-Att + PosUnk], [], [39.2], [], [], [$1.0 dot.op 10^20$],
    [GNMT +
    RL], [24.6], [39.92], [], [$2.3 dot.op 10^19$], [$1.4 dot.op 10^20$],
    [ConvS2S], [25.16], [40.46], [], [$9.6 dot.op 10^18$], [$1.5 dot.op 10^20$],
    [MoE], [26.03], [40.56], [], [$2.0 dot.op 10^19$], [$1.2 dot.op 10^20$],
    [Deep-Att + PosUnk
    Ensemble], [], [40.4], [], [], [$8.0 dot.op 10^20$],
    [GNMT + RL
    Ensemble], [26.30], [41.16], [], [$1.8 dot.op 10^20$], [$1.1 dot.op 10^21$],
    [ConvS2S
    Ensemble], [26.36], [#strong[41.29]], [], [$7.7 dot.op 10^19$], [$1.2 dot.op 10^21$],
    [Transformer (base
    model)], [27.3], [38.1], [], table.cell(align: center, colspan: 2)[$3.3 dot.op 10^18$],
    [Transformer
    (big)], [#strong[28.4]], [#strong[41.8]], [], table.cell(align: center, colspan: 2)[$2.3 dot.op 10^19$],
  )]
  , caption: [The Transformer achieves better BLEU scores than previous
  state-of-the-art models on the English-to-German and English-to-French
  newstest2014 tests at a fraction of the training cost. ]
  , kind: table
  )

] <tab:wmt-results>
]
