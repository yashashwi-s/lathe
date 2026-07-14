#set page(paper: "us-letter", margin: 1in, numbering: "1")
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.55em, first-line-indent: 0pt)
#show heading.where(level: 1): it => {
  set text(size: 14.4pt, weight: "bold")
  block(above: 1.2em, below: 0.6em)[#it.body]
}

#align(center)[
  #v(0.5in)
  #text(size: 17.28pt)[Algorithmic Pseudocode Sample 3]
  #v(0.6em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
]
#v(1.5em)

= #h(0.5em) Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#pagebreak()
#v(0.25in)

#let ind = 1.5em
#let cmt(x) = h(1fr) + text[▷ #x]
#let row(x) = block(above: 0.3em, below: 0.3em, x)

#line(length: 100%, stroke: 0.8pt)
#v(-0.6em)
#line(length: 100%, stroke: 0.4pt)
*Algorithm 2* Initialization of the control and state variables
#line(length: 100%, stroke: 0.4pt)

#set par(justify: false, leading: 0.5em)
#set text(size: 11pt)

#let L(n, body) = block(above: 0.55em, below: 0.55em)[#h((n - 2) * 1em)#body]

#L(2)[*for* $t in {-1, dots, -T^("traceback")}$ *do* #h(1fr) ▷ Retrieve the values of $P_(u,t)$]
#L(4)[$P_(u,t) <- $ #raw("Power.GetValue") $(t)$]
#L(2)[*end for*]
#L(2)[*for* $t in {-1, dots, -T^("traceback")}$ *do* #h(1fr) ▷ Initial conditions on the state variables]
#L(4)[*if* $P_(u,t) > $ #raw("MinimumPower.GetValue") $(t)$ *then*]
#L(6)[$S_(u,t)^("OFF") <- 0$]
#L(6)[$S_(u,t)^("STOP") <- 0$]
#L(6)[$S_(u,t)^("START") <- 0$]
#L(6)[*if* $P_(u,t) < P_(u,t-1)$ *then* #h(1em) ▷ Exact initialization required only if the FLAT state is defined.]
#L(8)[$S_(t-1)^("ON"\_"UP") <- 0$]
#L(8)[$S_(t-1)^("ON"\_"DOWN") <- 1$]
#L(8)[$S_(t-1)^("ON"\_"FLAT") <- 0$]
#L(6)[*else if* $P_(u,t) > P_(u,t-1)$ *then*]
#L(8)[$S_(t-1)^("ON"\_"UP") <- 1$]
#L(8)[$S_(t-1)^("ON"\_"DOWN") <- 0$]
#L(8)[$S_(t-1)^("ON"\_"FLAT") <- 0$]
#L(6)[*else if* $P_(u,t) = P_(u,t-1)$ *then*]
#L(8)[$S_(t-1)^("ON"\_"UP") <- 0$]
#L(8)[$S_(t-1)^("ON"\_"DOWN") <- 0$]
#L(8)[$S_(t-1)^("ON"\_"FLAT") <- 1$]
#L(6)[*end if*]
#L(4)[*else if* $P_(u,t) > 0$ *then* #h(1fr) ▷ Reconstruct the startups and shutdowns]
#L(6)[*if* $P_(u,t) < P_(u,t-1)$ *then*]
#L(8)[$S_t^("STOP") <- 1$]
#L(8)[$S_t^("START") <- 0$]
#L(6)[*else*]
#L(8)[$S_t^("STOP") <- 0$]
#L(8)[$S_t^("START") <- 1$]
#L(6)[*end if*]
#L(4)[*else* #h(1fr) ▷ Final possibility: the unit is OFF.]
#L(6)[$S_(u,t)^("OFF") <- 1$]
#L(6)[$S_(u,t)^("STOP") <- 0$]
#L(6)[$S_(u,t)^("START") <- 0$]
#L(6)[$S_(t-1)^("ON"\_"UP") <- 0$]
#L(6)[$S_(t-1)^("ON"\_"DOWN") <- 0$]
#L(6)[$S_(t-1)^("ON"\_"FLAT") <- 0$]
#L(4)[*end if*]
#L(2)[*end for*]

#v(0.3em)
#line(length: 100%, stroke: 0.4pt)
#v(-0.6em)
#line(length: 100%, stroke: 0.8pt)
