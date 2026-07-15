#set page(paper: "us-letter", margin: 1in, numbering: "1", number-align: center)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1")
#show heading.where(level: 1): it => block(above: 1.5em, below: 0.8em)[
  #text(size: 12pt, weight: "bold")[#counter(heading).display()#h(1em)#it.body]
]

#align(center)[
  #v(3.2em)
  #text(size: 17pt)[Algorithmic Pseudocode Sample 3]
  #v(1em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
]

#v(1.7em)

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#pagebreak()

#block(
  width: 100%,
  stroke: (top: 0.8pt, bottom: 0.8pt),
  inset: (top: 3pt, bottom: 3pt, left: 0pt, right: 0pt),
)[
  #set text(size: 10pt)
  #set par(justify: false, leading: 0.45em)

  *Algorithm 2* #h(0.5em) Initialization of the control and state variables\
  #line(length: 100%, stroke: 0.4pt)

  #let i1 = h(1.5em)
  #let i2 = h(3em)
  #let i3 = h(4.5em)
  #let cmt(c) = h(1fr) + [#sym.triangle.r #c]

  *for* $t in {-1, dots.h, -T^italic("traceback")}$ *do* #cmt[Retrieve the values of $P_(u,t)$]\
  #i1 $P_(u,t) <- $ `Power.GetValue`$(t)$\
  *end for*\
  *for* $t in {-1, dots.h, -T^italic("traceback")}$ *do* #cmt[Initial conditions on the state variables]\
  #i1 *if* $P_(u,t) >$ `MinimumPower.GetValue`$(t)$ *then*\
  #i2 $S_(u,t)^"OFF" <- 0$\
  #i2 $S_(u,t)^"STOP" <- 0$\
  #i2 $S_(u,t)^"START" <- 0$\
  #i2 *if* $P_(u,t) < P_(u,t-1)$ *then* #cmt[Exact initialization required only if the FLAT state is defined.]\
  #i3 $S_(t-1)^"ON_UP" <- 0$\
  #i3 $S_(t-1)^"ON_DOWN" <- 1$\
  #i3 $S_(t-1)^"ON_FLAT" <- 0$\
  #i2 *else if* $P_(u,t) > P_(u,t-1)$ *then*\
  #i3 $S_(t-1)^"ON_UP" <- 1$\
  #i3 $S_(t-1)^"ON_DOWN" <- 0$\
  #i3 $S_(t-1)^"ON_FLAT" <- 0$\
  #i2 *else if* $P_(u,t) = P_(u,t-1)$ *then*\
  #i3 $S_(t-1)^"ON_UP" <- 0$\
  #i3 $S_(t-1)^"ON_DOWN" <- 0$\
  #i3 $S_(t-1)^"ON_FLAT" <- 1$\
  #i2 *end if*\
  #i1 *else if* $P_(u,t) > 0$ *then* #cmt[Reconstruct the startups and shutdowns]\
  #i2 *if* $P_(u,t) < P_(u,t-1)$ *then*\
  #i3 $S_t^"STOP" <- 1$\
  #i3 $S_t^"START" <- 0$\
  #i2 *else*\
  #i3 $S_t^"STOP" <- 0$\
  #i3 $S_t^"START" <- 1$\
  #i2 *end if*\
  #i1 *else* #cmt[Final possibility: the unit is OFF.]\
  #i2 $S_(u,t)^"OFF" <- 1$\
  #i2 $S_(u,t)^"STOP" <- 0$\
  #i2 $S_(u,t)^"START" <- 0$\
  #i2 $S_(t-1)^"ON_UP" <- 0$\
  #i2 $S_(t-1)^"ON_DOWN" <- 0$\
  #i2 $S_(t-1)^"ON_FLAT" <- 0$\
  #i1 *end if*\
  *end for*
]
