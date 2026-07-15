#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true, leading: 0.55em)
#show heading.where(level: 1): it => [
  #v(0.5em)
  #text(size: 14pt, weight: "bold")[#it.body]
  #v(0.3em)
]

#align(center)[
  #v(1em)
  #text(size: 17pt)[Algorithmic Pseudocode Sample 3]
  #v(0.8em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
  #v(2em)
]

= 1. Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#v(1em)

#figure(
  kind: "algorithm",
  supplement: [Algorithm],
  caption: [Initialization of the control and state variables],
  block(width: 100%, stroke: (top: 1pt, bottom: 1pt), inset: (top: 6pt, bottom: 6pt))[
    #set align(left)
    #set text(size: 10pt)
    #let ind(n, body) = pad(left: n * 1.2em, body)
    #ind(0)[*for* $t in {-1, dots, -T^("traceback")}$ *do* #h(1fr) $triangle.small.r$ Retrieve the values of $P_(u,t)$] \
    #ind(1)[$P_(u,t) <- mono("Power.GetValue")(t)$] \
    #ind(0)[*end for*] \
    #ind(0)[*for* $t in {-1, dots, -T^("traceback")}$ *do* #h(1fr) $triangle.small.r$ Initial conditions on the state variables] \
    #ind(1)[*if* $P_(u,t) > mono("MinimumPower.GetValue")(t)$ *then*] \
    #ind(2)[$S_(u,t)^("OFF") <- 0$] \
    #ind(2)[$S_(u,t)^("STOP") <- 0$] \
    #ind(2)[$S_(u,t)^("START") <- 0$] \
    #ind(2)[*if* $P_(u,t) < P_(u,t-1)$ *then* #h(1fr) $triangle.small.r$ Exact initialization required only if the FLAT state is defined.] \
    #ind(3)[$S_(t-1)^("ON_UP") <- 0$] \
    #ind(3)[$S_(t-1)^("ON_DOWN") <- 1$] \
    #ind(3)[$S_(t-1)^("ON_FLAT") <- 0$] \
    #ind(2)[*else if* $P_(u,t) > P_(u,t-1)$ *then*] \
    #ind(3)[$S_(t-1)^("ON_UP") <- 1$] \
    #ind(3)[$S_(t-1)^("ON_DOWN") <- 0$] \
    #ind(3)[$S_(t-1)^("ON_FLAT") <- 0$] \
    #ind(2)[*else if* $P_(u,t) = P_(u,t-1)$ *then*] \
    #ind(3)[$S_(t-1)^("ON_UP") <- 0$] \
    #ind(3)[$S_(t-1)^("ON_DOWN") <- 0$] \
    #ind(3)[$S_(t-1)^("ON_FLAT") <- 1$] \
    #ind(2)[*end if*] \
    #ind(1)[*else if* $P_(u,t) > 0$ *then* #h(1fr) $triangle.small.r$ Reconstruct the startups and shutdowns] \
    #ind(2)[*if* $P_(u,t) < P_(u,t-1)$ *then*] \
    #ind(3)[$S_(t)^("STOP") <- 1$] \
    #ind(3)[$S_(t)^("START") <- 0$] \
    #ind(2)[*else*] \
    #ind(3)[$S_(t)^("STOP") <- 0$] \
    #ind(3)[$S_(t)^("START") <- 1$] \
    #ind(2)[*end if*] \
    #ind(1)[*else* #h(1fr) $triangle.small.r$ Final possibility: the unit is OFF.] \
    #ind(2)[$S_(u,t)^("OFF") <- 1$] \
    #ind(2)[$S_(u,t)^("STOP") <- 0$] \
    #ind(2)[$S_(u,t)^("START") <- 0$] \
    #ind(2)[$S_(t-1)^("ON_UP") <- 0$] \
    #ind(2)[$S_(t-1)^("ON_DOWN") <- 0$] \
    #ind(2)[$S_(t-1)^("ON_FLAT") <- 0$] \
    #ind(1)[*end if*] \
    #ind(0)[*end for*]
  ]
)
