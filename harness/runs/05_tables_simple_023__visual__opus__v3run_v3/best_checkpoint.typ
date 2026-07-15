#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.55em, justify: true)
#show math.equation: set text(font: "New Computer Modern Math")

// Title block
#align(center)[
  #v(30pt)
  #text(size: 17.28pt)[Simple Tables]
  #v(8pt)
  #text(size: 12pt)[Source-backed grouped table sample]
]
#v(18pt)

#text(size: 14.4pt, weight: "bold")[1#h(1em)Tables]
#v(6pt)

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#pagebreak()

// Table 1
#align(center)[
  Table 1: Source table 1: 2512.03307_table_5
  #v(4pt)
]

#let hdr(x) = align(center)[#x]
#align(center)[
  #block(width: 100%)[
    #set text(size: 8.5pt)
    #table(
      columns: (auto,) * 11,
      align: center,
      stroke: 0.5pt,
      table.header(
        [max-min iter.], $mu_l$, $mu_h$, $mu_(x_"in")$, $mu_(z_x)$, $mu_(r_s)$, $mu_c$, $mu_a$, $mu_(r_"cat")$, $mu_m$, $mu_d$,
      ),
      [1],  [5],[10],[3],[5],[1.0],[8],[tanh],[0.9],[0.4],[uniform],
      [2],  [3],[5],[2],[5],[0.1],[2],[identity],[1.0],[0.4],[uniform],
      [3],  [12],[128],[13],[200],[0.0],[2],[identity],[0.4],[0.0],[uniform],
      [4],  [3],[5],[2],[6],[0.6],[2],[tanh],[1.0],[0.0],[exponential],
      [5],  [10],[64],[8],[32],[0.4],[2],[tanh],[1.0],[0.0],[uniform],
      [6],  [8],[32],[5],[13],[0.8],[10],[identity],[0.0],[0.2],[normal],
      [7],  [10],[64],[8],[162],[0.9],[6],[elu],[0.6],[0.0],[normal],
      [8],  [5],[10],[3],[13],[0.0],[10],[tanh],[0.8],[0.0],[uniform],
      [9],  [5],[10],[3],[5],[0.3],[6],[identity],[0.6],[0.0],[exponential],
      [10], [5],[10],[3],[5],[0.1],[10],[tanh],[0.5],[0.0],[normal],
      [11], [3],[5],[2],[5],[0.0],[8],[relu],[1.0],[0.0],[normal],
      [12], [3],[5],[2],[5],[0.6],[4],[relu],[0.6],[0.0],[exponential],
      [13], [3],[5],[2],[5],[0.4],[6],[tanh],[0.6],[0.0],[normal],
      [14], [5],[10],[3],[5],[0.8],[8],[identity],[0.8],[0.0],[exponential],
      [15], [3],[5],[2],[5],[1.0],[8],[elu],[0.6],[0.0],[uniform],
      [16], [3],[5],[2],[6],[0.7],[6],[identity],[0.3],[0.0],[uniform],
      [17], [8],[32],[5],[91],[0.0],[2],[tanh],[1.0],[0.0],[exponential],
      [18], [3],[5],[2],[5],[0.0],[8],[tanh],[1.0],[0.0],[exponential],
      [19], [3],[5],[2],[6],[0.2],[6],[tanh],[0.2],[0.0],[exponential],
      [20], [12],[128],[13],[200],[0.2],[2],[identity],[0.1],[0.0],[exponential],
      [21], [3],[5],[2],[6],[0.9],[8],[relu],[0.6],[0.0],[exponential],
      [22], [3],[5],[2],[5],[0.3],[8],[identity],[0.2],[0.0],[uniform],
      [23], [5],[10],[3],[5],[0.2],[4],[tanh],[0.3],[0.0],[normal],
      [24], [3],[5],[2],[5],[0.8],[8],[identity],[0.1],[0.0],[uniform],
      [25], [3],[5],[2],[5],[0.2],[4],[relu],[1.0],[0.0],[exponential],
      [26], [3],[5],[2],[5],[0.5],[8],[tanh],[0.8],[0.0],[normal],
      [27], [8],[32],[5],[13],[0.1],[4],[identity],[0.0],[0.0],[exponential],
      [28], [3],[5],[2],[6],[0.4],[4],[tanh],[0.1],[0.0],[exponential],
      [29], [3],[5],[2],[5],[0.1],[8],[identity],[0.2],[0.0],[exponential],
    )
  ]
]

#pagebreak()

// Table 2
#align(center)[
  Table 2: Source table 2: 2512.02195_table_6
  #v(4pt)
]

#let it(x) = text(style: "italic")[#x]
#let sc(x) = smallcaps(lower(x))

#align(center)[
  #block(width: 55%)[
    #set text(size: 11pt)
    #table(
      columns: (auto, 1fr, auto),
      align: (left, left, right),
      stroke: none,
      inset: (x: 4pt, y: 2pt),
      table.hline(),
      [\#], [Word type], [#it("f")],
      table.hline(),
      [1.], [#it("te") (`at', `to', #sc("comp"))], [1018],
      [2.], [#it("dat") (`that')], [658],
      [3.], [#it("niet") (`not')], [650],
      [4.], [#it("om") (`to')], [446],
      [5.], [#it("de") (`the', #sc("masc/fem/pl"))], [291],
      [6.], [#it("er") (`there')], [271],
      [7.], [#it("geen") (`no')], [270],
      [8.], [#it("elk") (`every', #sc("neut"))], [251],
      [9.], [#it("iedere") (`every', #sc("masc/fem"))], [247],
      [10.], [#it("of") (`or', `whether')], [244],
      [11.], [#it("elke") (`every', #sc("masc/fem"))], [229],
      [12.], [#it("ieder") (`every', #sc("neut"))], [223],
      [13.], [#it("alle") (`all')], [215],
      [14.], [#it("een") (`a', `one')], [212],
      [15.], [#it("ik") (`I')], [194],
      [16.], [#it("massa's") (`masses')], [186],
      [17.], [#it("het") (`the', #sc("neut:sg"))], [180],
      [18.], [#it("op") (`on')], [178],
      [19.], [#it("deze") (`this', #sc("masc/fem"))], [172],
      [20.], [#it("weinig") (`a few')], [171],
      [21.], [#it("daar") (`there')], [163],
      [22.], [#it("aan") (`to', #sc("prep"))], [161],
      [23.], [#it("veel") (`a lot of')], [155],
      [24.], [#it("hier") (`here')], [146],
      [25.], [#it("voor") (`for')], [144],
      [26.], [#it("dit") (`this', #sc("neut"))], [140],
      [27.], [#it("zijn") (`are', `be', `his')], [130],
      [28.], [#it("door") (`by')], [122],
      [29.], [#it("in") (`in')], [120],
      [30.], [#it("menig") (`many', #sc("sg"))], [118],
      [31.], [#it("menige") (`many', #sc("pl"))], [111],
      [32.], [#it("je") (`you', #sc("inform"))], [110],
      [33.], [#it("die") (`that', #sc("masc/fem"))], [103],
      [34.], [#it("waar") (`where')], [97],
      [35.], [#it("sommige") (`some', #sc("pl"))], [90],
      table.hline(),
    )
  ]
]
