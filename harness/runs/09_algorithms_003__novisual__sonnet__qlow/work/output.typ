#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em, spacing: 1.2em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Algorithmic Pseudocode Sample 3]

  #v(0.5em)
  Source-backed Image2Struct algorithm sample
]

#v(1em)

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#let ind = h(1.5em)
#let comment(c) = h(1fr) + $triangle.r$ + h(0.3em) + text(style: "italic")[#c]

#figure(
  block(
    width: 100%,
    stroke: 0.5pt,
    inset: 8pt,
    align(left)[
      #set par(leading: 0.55em, spacing: 0.55em)
      *Algorithm 1* Source-backed algorithmic procedure

      #line(length: 100%, stroke: 0.5pt)

      *for* $t in {-1, dots, -T^"traceback"}$ *do* #comment[Retrieve the values of $P_(u,t)$] \
      #ind $P_(u,t) <- "Power.GetValue"(t)$ \
      *end for* \
      *for* $t in {-1, dots, -T^"traceback"}$ *do* #comment[Initial conditions on the state variables] \
      #ind *if* $P_(u,t) > "MinimumPower.GetValue"(t)$ *then* \
      #ind#ind $S_(u,t)^"OFF" <- 0$ \
      #ind#ind $S_(u,t)^"STOP" <- 0$ \
      #ind#ind $S_(u,t)^"START" <- 0$ \
      #ind#ind *if* $P_(u,t) < P_(u,t-1)$ *then* #comment[Exact initialization required only if the FLAT state is defined.] \
      #ind#ind#ind $S_(t-1)^"ON_UP" <- 0$ \
      #ind#ind#ind $S_(t-1)^"ON_DOWN" <- 1$ \
      #ind#ind#ind $S_(t-1)^"ON_FLAT" <- 0$ \
      #ind#ind *else if* $P_(u,t) > P_(u,t-1)$ *then* \
      #ind#ind#ind $S_(t-1)^"ON_UP" <- 1$ \
      #ind#ind#ind $S_(t-1)^"ON_DOWN" <- 0$ \
      #ind#ind#ind $S_(t-1)^"ON_FLAT" <- 0$ \
      #ind#ind *else if* $P_(u,t) = P_(u,t-1)$ *then* \
      #ind#ind#ind $S_(t-1)^"ON_UP" <- 0$ \
      #ind#ind#ind $S_(t-1)^"ON_DOWN" <- 0$ \
      #ind#ind#ind $S_(t-1)^"ON_FLAT" <- 1$ \
      #ind#ind *end if* \
      #ind *else if* $P_(u,t) > 0$ *then* #comment[Reconstruct the startups and shutdowns] \
      #ind#ind *if* $P_(u,t) < P_(u,t-1)$ *then* \
      #ind#ind#ind $S_t^"STOP" <- 1$ \
      #ind#ind#ind $S_t^"START" <- 0$ \
      #ind#ind *else* \
      #ind#ind#ind $S_t^"STOP" <- 0$ \
      #ind#ind#ind $S_t^"START" <- 1$ \
      #ind#ind *end if* \
      #ind *else* #comment[Final possibility: the unit is OFF.] \
      #ind#ind $S_(u,t)^"OFF" <- 1$ \
      #ind#ind $S_(u,t)^"STOP" <- 0$ \
      #ind#ind $S_(u,t)^"START" <- 0$ \
      #ind#ind $S_(t-1)^"ON_UP" <- 0$ \
      #ind#ind $S_(t-1)^"ON_DOWN" <- 0$ \
      #ind#ind $S_(t-1)^"ON_FLAT" <- 0$ \
      #ind *end if* \
      *end for*

      #line(length: 100%, stroke: 0.5pt)

      *Algorithm 2* Initialization of the control and state variables
    ]
  ),
  caption: none
)
