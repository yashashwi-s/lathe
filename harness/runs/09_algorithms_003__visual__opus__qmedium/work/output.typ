#set page(paper: "us-letter", margin: 1in, numbering: "1")
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.55em, first-line-indent: 0pt)
#show heading.where(level: 1): it => {
  set text(size: 14.4pt, weight: "bold")
  block(above: 1.2em, below: 0.8em)[1#h(1em)#it.body]
}

#align(center)[
  #v(1.5cm)
  #text(size: 17.28pt)[Algorithmic Pseudocode Sample 3]
  #v(0.6em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
]

#v(0.8cm)

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#pagebreak()

// Algorithm 2 box
#let cmt(x) = h(1fr) + text[#sym.triangle.stroked.r #x]
#let ind(n, body) = pad(left: n * 1.2em, body)

#line(length: 100%, stroke: 0.8pt)
#v(-0.4em)
#line(length: 100%, stroke: 0.4pt)
#v(-0.2em)

*Algorithm 2* Initialization of the control and state variables

#line(length: 100%, stroke: 0.4pt)
#v(-0.3em)

#set par(justify: false, leading: 0.55em, spacing: 0.7em)
#show math.equation: set text(size: 10.5pt)

#ind(1)[*for* $t in {-1, dots, -T^("traceback")}$ *do* #cmt[Retrieve the values of $P_(u,t)$]]

#ind(2)[$P_(u,t) <- #text(font: "DejaVu Sans Mono", size: 10pt)[Power.GetValue] (t)$]

#ind(1)[*end for*]

#ind(1)[*for* $t in {-1, dots, -T^("traceback")}$ *do* #cmt[Initial conditions on the state variables]]

#ind(2)[*if* $P_(u,t) > #text(font: "DejaVu Sans Mono", size: 10pt)[MinimumPower.GetValue] (t)$ *then*]

#ind(3)[$S_(u,t)^(O F F) <- 0$]

#ind(3)[$S_(u,t)^(S T O P) <- 0$]

#ind(3)[$S_(u,t)^(S T A R T) <- 0$]

#ind(3)[*if* $P_(u,t) < P_(u,t-1)$ *then* #h(0.8em) #text[#sym.triangle.stroked.r Exact initialization required only if the FLAT state is defined.]]

#ind(4)[$S_(t-1)^(O N \_ U P) <- 0$]

#ind(4)[$S_(t-1)^(O N \_ D O W N) <- 1$]

#ind(4)[$S_(t-1)^(O N \_ F L A T) <- 0$]

#ind(3)[*else if* $P_(u,t) > P_(u,t-1)$ *then*]

#ind(4)[$S_(t-1)^(O N \_ U P) <- 1$]

#ind(4)[$S_(t-1)^(O N \_ D O W N) <- 0$]

#ind(4)[$S_(t-1)^(O N \_ F L A T) <- 0$]

#ind(3)[*else if* $P_(u,t) = P_(u,t-1)$ *then*]

#ind(4)[$S_(t-1)^(O N \_ U P) <- 0$]

#ind(4)[$S_(t-1)^(O N \_ D O W N) <- 0$]

#ind(4)[$S_(t-1)^(O N \_ F L A T) <- 1$]

#ind(3)[*end if*]

#ind(2)[*else if* $P_(u,t) > 0$ *then* #cmt[Reconstruct the startups and shutdowns]]

#ind(3)[*if* $P_(u,t) < P_(u,t-1)$ *then*]

#ind(4)[$S_(t)^(S T O P) <- 1$]

#ind(4)[$S_(t)^(S T A R T) <- 0$]

#ind(3)[*else*]

#ind(4)[$S_(t)^(S T O P) <- 0$]

#ind(4)[$S_(t)^(S T A R T) <- 1$]

#ind(3)[*end if*]

#ind(2)[*else* #cmt[Final possibility: the unit is OFF.]]

#ind(3)[$S_(u,t)^(O F F) <- 1$]

#ind(3)[$S_(u,t)^(S T O P) <- 0$]

#ind(3)[$S_(u,t)^(S T A R T) <- 0$]

#ind(3)[$S_(t-1)^(O N \_ U P) <- 0$]

#ind(3)[$S_(t-1)^(O N \_ D O W N) <- 0$]

#ind(3)[$S_(t-1)^(O N \_ F L A T) <- 0$]

#ind(2)[*end if*]

#ind(1)[*end for*]

#v(-0.3em)
#line(length: 100%, stroke: 0.4pt)
#v(-0.4em)
#line(length: 100%, stroke: 0.8pt)
