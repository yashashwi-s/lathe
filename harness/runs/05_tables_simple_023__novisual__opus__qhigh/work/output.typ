#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.55em, first-line-indent: 1.5em, justify: false)
#show heading: set block(above: 1.2em, below: 0.7em)
#show heading.where(level: 1): it => {
  set text(size: 14.4pt, weight: "bold")
  block(above: 3.5em, below: 2.3em)[#counter(heading).display() #h(1em) #it.body]
}
#set heading(numbering: "1")

// Title block matching \maketitle
#v(2em)
#align(center)[
  #text(size: 17.28pt)[Simple Tables]
  #v(1.5em, weak: true)
  #text(size: 12pt)[Source-backed grouped table sample]
  #v(1em, weak: true)
]
#v(1.5em)

= Tables

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

// Helper: resizebox-like scaling to text width, with optional height cap
#let fit-width(body, max-h: 8.5in) = context {
  let m = measure(body)
  let w = page.width - 2in
  let s-w = w / m.width
  let s-h = max-h / m.height
  let s = calc.min(s-w, s-h)
  scale(x: s * 100%, y: s * 100%, origin: top + left, reflow: true, body)
}

// ============ Table 1 ============
#pagebreak(weak: true)

#let t1 = table(
  columns: 11,
  stroke: none,
  align: center,
  inset: (x: 6pt, y: 3pt),
  table.hline(stroke: 0.5pt),
  table.vline(x: 0, stroke: 0.5pt),
  table.vline(x: 1, stroke: 0.5pt),
  table.vline(x: 11, stroke: 0.5pt),
  [max-min iter.], $mu_l$, $mu_h$, $mu_(x_(i n))$, $mu_(z_x)$, $mu_(r_s)$, $mu_c$, $mu_a$, $mu_(r_(c a t))$, $mu_m$, $mu_d$,
  table.hline(stroke: 0.5pt),
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
  table.hline(stroke: 0.5pt),
)

#align(center)[
  Table 1: Source table 1: 2512.03307_table_5
  #v(0.5em)
  #fit-width(t1)
]

// ============ Table 2 ============
#pagebreak(weak: true)

#let t2 = table(
  columns: 4,
  stroke: none,
  align: (left, left, left, left),
  inset: (x: 6pt, y: 3pt),
  table.hline(stroke: 0.5pt),
  [\#], [Word type], [$f$], [],
  table.hline(stroke: 0.5pt),
  [1.], [#emph[te] (‘at’, ‘to’, #smallcaps[comp])], [1018], [],
  [2.], [#emph[dat] (‘that’)], [658], [],
  [3.], [#emph[niet] (‘not’)], [650], [],
  [4.], [#emph[om] (‘to’)], [446], [],
  [5.], [#emph[de] (‘the’, #smallcaps[masc/fem/pl])], [291], [],
  [6.], [#emph[er] (‘there’)], [271], [],
  [7.], [#emph[geen] (‘no’)], [270], [],
  [8.], [#emph[elk] (‘every’, #smallcaps[neut])], [251], [],
  [9.], [#emph[iedere] (‘every’, #smallcaps[masc/fem])], [247], [],
  [10.], [#emph[of] (‘or’, ‘whether’)], [244], [],
  [11.], [#emph[elke] (‘every’, #smallcaps[masc/fem])], [229], [],
  [12.], [#emph[ieder] (‘every’, #smallcaps[neut])], [223], [],
  [13.], [#emph[alle] (‘all’)], [215], [],
  [14.], [#emph[een] (‘a’, ‘one’)], [212], [],
  [15.], [#emph[ik] (‘I’)], [194], [],
  [16.], [#emph[massa's] (‘masses’)], [186], [],
  [17.], [#emph[het] (‘the’, #smallcaps[neut:sg])], [180], [],
  [18.], [#emph[op] (‘on’)], [178], [],
  [19.], [#emph[deze] (‘this’, #smallcaps[masc/fem])], [172], [],
  [20.], [#emph[weinig] (‘a few’)], [171], [],
  [21.], [#emph[daar] (‘there’)], [163], [],
  [22.], [#emph[aan] (‘to’, #smallcaps[prep])], [161], [],
  [23.], [#emph[veel] (‘a lot of’)], [155], [],
  [24.], [#emph[hier] (‘here’)], [146], [],
  [25.], [#emph[voor] (‘for’)], [144], [],
  [26.], [#emph[dit] (‘this’, #smallcaps[neut])], [140], [],
  [27.], [#emph[zijn] (‘are’, ‘be’, ‘his’)], [130], [],
  [28.], [#emph[door] (‘by’)], [122], [],
  [29.], [#emph[in] (‘in’)], [120], [],
  [30.], [#emph[menig] (‘many’, #smallcaps[sg])], [118], [],
  [31.], [#emph[menige] (‘many’, #smallcaps[pl])], [111], [],
  [32.], [#emph[je] (‘you’, #smallcaps[inform])], [110], [],
  [33.], [#emph[die] (‘that’, #smallcaps[masc/fem])], [103], [],
  [34.], [#emph[waar] (‘where’)], [97], [],
  [35.], [#emph[sommige] (‘some’, #smallcaps[pl])], [90], [],
  table.hline(stroke: 0.5pt),
)

#align(center)[
  Table 2: Source table 2: 2512.02195_table_6
  #v(0.5em)
  #fit-width(t2)
]
