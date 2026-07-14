#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt)
#set par(justify: true)

#align(center)[
  #text(size: 17pt)[Simple Tables]

  #v(0.5em)
  Source-backed grouped table sample
]

#v(1em)

= Tables

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.03307_table_5],
  kind: table,
)[
#set text(size: 6pt)
#table(
  columns: 11,
  align: center,
  stroke: 0.5pt,
  table.header([max-min iter.], [$mu_l$], [$mu_h$], [$mu_(x_(i n))$], [$mu_(z_x)$], [$mu_(r_s)$], [$mu_c$], [$mu_a$], [$mu_(r_(c a t))$], [$mu_m$], [$mu_d$]),
  [1], [5], [10], [3], [5], [1.0], [8], [tanh], [0.9], [0.4], [uniform],
  [2], [3], [5], [2], [5], [0.1], [2], [identity], [1.0], [0.4], [uniform],
  [3], [12], [128], [13], [200], [0.0], [2], [identity], [0.4], [0.0], [uniform],
  [4], [3], [5], [2], [6], [0.6], [2], [tanh], [1.0], [0.0], [exponential],
  [5], [10], [64], [8], [32], [0.4], [2], [tanh], [1.0], [0.0], [uniform],
  [6], [8], [32], [5], [13], [0.8], [10], [identity], [0.0], [0.2], [normal],
  [7], [10], [64], [8], [162], [0.9], [6], [elu], [0.6], [0.0], [normal],
  [8], [5], [10], [3], [13], [0.0], [10], [tanh], [0.8], [0.0], [uniform],
  [9], [5], [10], [3], [5], [0.3], [6], [identity], [0.6], [0.0], [exponential],
  [10], [5], [10], [3], [5], [0.1], [10], [tanh], [0.5], [0.0], [normal],
  [11], [3], [5], [2], [5], [0.0], [8], [relu], [1.0], [0.0], [normal],
  [12], [3], [5], [2], [5], [0.6], [4], [relu], [0.6], [0.0], [exponential],
  [13], [3], [5], [2], [5], [0.4], [6], [tanh], [0.6], [0.0], [normal],
  [14], [5], [10], [3], [5], [0.8], [8], [identity], [0.8], [0.0], [exponential],
  [15], [3], [5], [2], [5], [1.0], [8], [elu], [0.6], [0.0], [uniform],
  [16], [3], [5], [2], [6], [0.7], [6], [identity], [0.3], [0.0], [uniform],
  [17], [8], [32], [5], [91], [0.0], [2], [tanh], [1.0], [0.0], [exponential],
  [18], [3], [5], [2], [5], [0.0], [8], [tanh], [1.0], [0.0], [exponential],
  [19], [3], [5], [2], [6], [0.2], [6], [tanh], [0.2], [0.0], [exponential],
  [20], [12], [128], [13], [200], [0.2], [2], [identity], [0.1], [0.0], [exponential],
  [21], [3], [5], [2], [6], [0.9], [8], [relu], [0.6], [0.0], [exponential],
  [22], [3], [5], [2], [5], [0.3], [8], [identity], [0.2], [0.0], [uniform],
  [23], [5], [10], [3], [5], [0.2], [4], [tanh], [0.3], [0.0], [normal],
  [24], [3], [5], [2], [5], [0.8], [8], [identity], [0.1], [0.0], [uniform],
  [25], [3], [5], [2], [5], [0.2], [4], [relu], [1.0], [0.0], [exponential],
  [26], [3], [5], [2], [5], [0.5], [8], [tanh], [0.8], [0.0], [normal],
  [27], [8], [32], [5], [13], [0.1], [4], [identity], [0.0], [0.0], [exponential],
  [28], [3], [5], [2], [6], [0.4], [4], [tanh], [0.1], [0.0], [exponential],
  [29], [3], [5], [2], [5], [0.1], [8], [identity], [0.2], [0.0], [exponential],
)
]

#v(1em)

#figure(
  caption: [Source table 2: 2512.02195_table_6],
  kind: table,
)[
#table(
  columns: 3,
  align: (left, left, left),
  stroke: none,
  table.hline(),
  [\#], [Word type], [$f$],
  table.hline(),
  [1.], [_te_ ('at', 'to', #smallcaps[comp])], [1018],
  [2.], [_dat_ ('that')], [658],
  [3.], [_niet_ ('not')], [650],
  [4.], [_om_ ('to')], [446],
  [5.], [_de_ ('the', #smallcaps[masc/fem/pl])], [291],
  [6.], [_er_ ('there')], [271],
  [7.], [_geen_ ('no')], [270],
  [8.], [_elk_ ('every', #smallcaps[neut])], [251],
  [9.], [_iedere_ ('every', #smallcaps[masc/fem])], [247],
  [10.], [_of_ ('or', 'whether')], [244],
  [11.], [_elke_ ('every', #smallcaps[masc/fem])], [229],
  [12.], [_ieder_ ('every', #smallcaps[neut])], [223],
  [13.], [_alle_ ('all')], [215],
  [14.], [_een_ ('a', 'one')], [212],
  [15.], [_ik_ ('I')], [194],
  [16.], [_massa's_ ('masses')], [186],
  [17.], [_het_ ('the', #smallcaps[neut:sg])], [180],
  [18.], [_op_ ('on')], [178],
  [19.], [_deze_ ('this', #smallcaps[masc/fem])], [172],
  [20.], [_weinig_ ('a few')], [171],
  [21.], [_daar_ ('there')], [163],
  [22.], [_aan_ ('to', #smallcaps[prep])], [161],
  [23.], [_veel_ ('a lot of')], [155],
  [24.], [_hier_ ('here')], [146],
  [25.], [_voor_ ('for')], [144],
  [26.], [_dit_ ('this', #smallcaps[neut])], [140],
  [27.], [_zijn_ ('are', 'be', 'his')], [130],
  [28.], [_door_ ('by')], [122],
  [29.], [_in_ ('in')], [120],
  [30.], [_menig_ ('many', #smallcaps[sg])], [118],
  [31.], [_menige_ ('many', #smallcaps[pl])], [111],
  [32.], [_je_ ('you', #smallcaps[inform])], [110],
  [33.], [_die_ ('that', #smallcaps[masc/fem])], [103],
  [34.], [_waar_ ('where')], [97],
  [35.], [_sommige_ ('some', #smallcaps[pl])], [90],
  table.hline(),
)
]
