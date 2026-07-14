#set page(
  paper: "us-letter",
  margin: 1in,
  numbering: "1",
  number-align: center,
)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.55em)

#set heading(numbering: "1")
#show heading.where(level: 1): it => {
  set text(size: 14pt, weight: "bold")
  block(above: 1.4em, below: 0.9em)[#it]
}

// Title
#align(center)[
  #v(0.55in)
  #text(size: 17.28pt)[Algorithmic Pseudocode Sample 3]

  #v(1.2em)
  #text(size: 11pt)[Source-backed Image2Struct algorithm sample]
]

#v(1.8em)

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#pagebreak()

#v(0.05in)

// Algorithm float
#let indent = h(1.5em)
#let indent2 = h(3em)
#let indent3 = h(4.5em)
#let indent4 = h(6em)
#let comment(body) = h(1fr) + [#sym.triangle.stroked.r #body]
#let tt(s) = text(font: "DejaVu Sans Mono", size: 0.92em, s)

#block(width: 100%, spacing: 0pt)[
  #line(length: 100%, stroke: 0.8pt)
  #v(-0.6em)
  #line(length: 100%, stroke: 0.4pt)
  #v(0.1em)
  *Algorithm 2* Initialization of the control and state variables
  #v(-0.5em)
  #line(length: 100%, stroke: 0.4pt)

  #set par(justify: false, leading: 0.62em, first-line-indent: 0pt)
  #set text(size: 11pt)
  #v(-0.2em)

  #indent *for* $t in {-1, dots, -T^("traceback")}$ *do* #comment[Retrieve the values of $P_(u,t)$] \
  #indent2 $P_(u,t) <- #tt("Power.GetValue") (t)$ \
  #indent *end for* \
  #indent *for* $t in {-1, dots, -T^("traceback")}$ *do* #comment[Initial conditions on the state variables] \
  #indent2 *if* $P_(u,t) > #tt("MinimumPower.GetValue") (t)$ *then* \
  #indent3 $S_(u,t)^("OFF") <- 0$ \
  #indent3 $S_(u,t)^("STOP") <- 0$ \
  #indent3 $S_(u,t)^("START") <- 0$ \
  #indent3 *if* $P_(u,t) < P_(u,t-1)$ *then* #h(0.7em) #sym.triangle.stroked.r Exact initialization required only if the FLAT state is defined. \
  #indent4 $S_(t-1)^("ON"\_"UP") <- 0$ \
  #indent4 $S_(t-1)^("ON"\_"DOWN") <- 1$ \
  #indent4 $S_(t-1)^("ON"\_"FLAT") <- 0$ \
  #indent3 *else if* $P_(u,t) > P_(u,t-1)$ *then* \
  #indent4 $S_(t-1)^("ON"\_"UP") <- 1$ \
  #indent4 $S_(t-1)^("ON"\_"DOWN") <- 0$ \
  #indent4 $S_(t-1)^("ON"\_"FLAT") <- 0$ \
  #indent3 *else if* $P_(u,t) = P_(u,t-1)$ *then* \
  #indent4 $S_(t-1)^("ON"\_"UP") <- 0$ \
  #indent4 $S_(t-1)^("ON"\_"DOWN") <- 0$ \
  #indent4 $S_(t-1)^("ON"\_"FLAT") <- 1$ \
  #indent3 *end if* \
  #indent2 *else if* $P_(u,t) > 0$ *then* #comment[Reconstruct the startups and shutdowns] \
  #indent3 *if* $P_(u,t) < P_(u,t-1)$ *then* \
  #indent4 $S_(t)^("STOP") <- 1$ \
  #indent4 $S_(t)^("START") <- 0$ \
  #indent3 *else* \
  #indent4 $S_(t)^("STOP") <- 0$ \
  #indent4 $S_(t)^("START") <- 1$ \
  #indent3 *end if* \
  #indent2 *else* #comment[Final possibility: the unit is OFF.] \
  #indent3 $S_(u,t)^("OFF") <- 1$ \
  #indent3 $S_(u,t)^("STOP") <- 0$ \
  #indent3 $S_(u,t)^("START") <- 0$ \
  #indent3 $S_(t-1)^("ON"\_"UP") <- 0$ \
  #indent3 $S_(t-1)^("ON"\_"DOWN") <- 0$ \
  #indent3 $S_(t-1)^("ON"\_"FLAT") <- 0$ \
  #indent2 *end if* \
  #indent *end for*

  #v(0.4em)
  #line(length: 100%, stroke: 0.4pt)
  #v(-0.4em)
  #line(length: 100%, stroke: 0.8pt)
]
