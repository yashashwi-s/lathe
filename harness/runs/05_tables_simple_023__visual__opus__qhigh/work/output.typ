#set page(paper: "us-letter", margin: 1in, numbering: "1")
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true, leading: 0.55em)

// Title block
#align(center)[
  #v(48pt)
  #text(size: 17.28pt)[Simple Tables]
  #v(12pt)
  #text(size: 12pt)[Source-backed grouped table sample]
]

#v(24pt)

#text(size: 14.4pt, weight: "bold")[1#h(1em)Tables]
#v(6pt)

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#pagebreak()

// ----- Table 1 (Page 2) -----
#align(center)[
  Table 1: Source table 1: 2512.03307\_table\_5
]
#v(4pt)

#let t1 = table(
  columns: (auto,) * 11,
  stroke: (x, y) => {
    let s = 0.5pt + black
    (
      left: if x == 0 or x == 1 { s } else { none },
      right: if x == 10 { s } else { none },
      top: if y == 0 or y == 1 { s } else { none },
      bottom: if y == 29 { s } else { none },
    )
  },
  align: center + horizon,
  inset: (x: 5pt, y: 4pt),
  table.header[max-min iter.][$mu_l$][$mu_h$][$mu_(x_(i n))$][$mu_(z_x)$][$mu_(r_s)$][$mu_c$][$mu_a$][$mu_(r_(c a t))$][$mu_m$][$mu_d$],
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

#align(center)[
  #context {
    let m = measure(t1)
    let s = 6.5in / m.width
    scale(x: s * 100%, y: s * 100%, reflow: true, t1)
  }
]

#pagebreak()

// ----- Table 2 (Page 3) - only rows 1..21 visible in reference -----
#align(center)[
  Table 2: Source table 2: 2512.02195\_table\_6
]
#v(4pt)

#let sc(t) = text(features: ("smcp",), size: 0.9em)[#lower(t)]

#let t2 = table(
  columns: 3,
  stroke: (x, y) => (
    top: if y == 0 or y == 1 { 0.5pt } else { none },
    bottom: if y == 21 { 0.5pt } else { none },
  ),
  align: (right, left, right),
  inset: (x: 6pt, y: 2pt),
  [\#], [Word type], [$f$],
  [1.], [_te_ (‘at’, ‘to’, #sc[COMP])], [1018],
  [2.], [_dat_ (‘that’)], [658],
  [3.], [_niet_ (‘not’)], [650],
  [4.], [_om_ (‘to’)], [446],
  [5.], [_de_ (‘the’, #sc[MASC/FEM/PL])], [291],
  [6.], [_er_ (‘there’)], [271],
  [7.], [_geen_ (‘no’)], [270],
  [8.], [_elk_ (‘every’, #sc[NEUT])], [251],
  [9.], [_iedere_ (‘every’, #sc[MASC/FEM])], [247],
  [10.], [_of_ (‘or’, ‘whether’)], [244],
  [11.], [_elke_ (‘every’, #sc[MASC/FEM])], [229],
  [12.], [_ieder_ (‘every’, #sc[NEUT])], [223],
  [13.], [_alle_ (‘all’)], [215],
  [14.], [_een_ (‘a’, ‘one’)], [212],
  [15.], [_ik_ (‘I’)], [194],
  [16.], [_massa’s_ (‘masses’)], [186],
  [17.], [_het_ (‘the’, #sc[NEUT:SG])], [180],
  [18.], [_op_ (‘on’)], [178],
  [19.], [_deze_ (‘this’, #sc[MASC/FEM])], [172],
  [20.], [_weinig_ (‘a few’)], [171],
  [21.], [_daar_ (‘there’)], [163],
)

#align(center)[
  #context {
    let m = measure(t2)
    let s = calc.max(6.5in / m.width, 8in / m.height)
    scale(x: s * 100%, y: s * 100%, reflow: true, t2)
  }
]
