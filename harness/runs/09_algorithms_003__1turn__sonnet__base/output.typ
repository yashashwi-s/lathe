#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: false)

#align(center)[
  #text(size: 17pt, weight: "bold")[Algorithmic Pseudocode Sample 3]
  #v(0.5em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
  #v(1em)
]

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#v(0.5em)

#block(
  stroke: 0.5pt,
  width: 100%,
  inset: 0pt,
)[
  #block(
    width: 100%,
    fill: rgb("e8e8e8"),
    inset: (x: 8pt, y: 4pt),
  )[
    *Algorithm 1* Source-backed algorithmic procedure
  ]
  #block(
    width: 100%,
    inset: (x: 8pt, y: 6pt),
  )[
    #block(
      stroke: 0.5pt,
      width: 100%,
      inset: 0pt,
    )[
      #block(
        width: 100%,
        fill: rgb("e8e8e8"),
        inset: (x: 8pt, y: 4pt),
      )[
        *Algorithm 2* Initialization of the control and state variables
      ]
      #block(
        width: 100%,
        inset: (x: 8pt, y: 6pt),
      )[
        #set text(size: 10pt)
        #let ind(n) = h(n * 1.5em)

        *for* $t in {-1, dots, -T^"traceback"}$ *do* #h(1fr) $triangle.r$ Retrieve the values of $P_(u,t)$ \
        #ind(1) $P_(u,t) <- sans("Power.GetValue")(t)$ \
        *end for* \
        *for* $t in {-1, dots, -T^"traceback"}$ *do* #h(1fr) $triangle.r$ Initial conditions on the state variables \
        #ind(1) *if* $P_(u,t) > sans("MinimumPower.GetValue")(t)$ *then* \
        #ind(2) $S_(u,t)^"OFF" <- 0$ \
        #ind(2) $S_(u,t)^"STOP" <- 0$ \
        #ind(2) $S_(u,t)^"START" <- 0$ \
        #ind(2) *if* $P_(u,t) < P_(u,t-1)$ *then* #h(1fr) $triangle.r$ Exact initialization required only if the FLAT state is defined. \
        #ind(3) $S_(t-1)^"ON\_UP" <- 0$ \
        #ind(3) $S_(t-1)^"ON\_DOWN" <- 1$ \
        #ind(3) $S_(t-1)^"ON\_FLAT" <- 0$ \
        #ind(2) *else if* $P_(u,t) > P_(u,t-1)$ *then* \
        #ind(3) $S_(t-1)^"ON\_UP" <- 1$ \
        #ind(3) $S_(t-1)^"ON\_DOWN" <- 0$ \
        #ind(3) $S_(t-1)^"ON\_FLAT" <- 0$ \
        #ind(2) *else if* $P_(u,t) = P_(u,t-1)$ *then* \
        #ind(3) $S_(t-1)^"ON\_UP" <- 0$ \
        #ind(3) $S_(t-1)^"ON\_DOWN" <- 0$ \
        #ind(3) $S_(t-1)^"ON\_FLAT" <- 1$ \
        #ind(2) *end if* \
        #ind(1) *else if* $P_(u,t) > 0$ *then* #h(1fr) $triangle.r$ Reconstruct the startups and shutdowns \
        #ind(2) *if* $P_(u,t) < P_(u,t-1)$ *then* \
        #ind(3) $S_(t)^"STOP" <- 1$ \
        #ind(3) $S_(t)^"START" <- 0$ \
        #ind(2) *else* \
        #ind(3) $S_(t)^"STOP" <- 0$ \
        #ind(3) $S_(t)^"START" <- 1$ \
        #ind(2) *end if* \
        #ind(1) *else* #h(1fr) $triangle.r$ Final possibility: the unit is OFF. \
        #ind(2) $S_(u,t)^"OFF" <- 1$ \
        #ind(2) $S_(u,t)^"STOP" <- 0$ \
        #ind(2) $S_(u,t)^"START" <- 0$ \
        #ind(2) $S_(t-1)^"ON\_UP" <- 0$ \
        #ind(2) $S_(t-1)^"ON\_DOWN" <- 0$ \
        #ind(2) $S_(t-1)^"ON\_FLAT" <- 0$ \
        #ind(1) *end if* \
        *end for*
      ]
    ]
  ]
]
