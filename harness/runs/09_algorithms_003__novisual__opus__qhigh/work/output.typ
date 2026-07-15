#set page(paper: "us-letter", margin: 1in, numbering: "1")
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.55em, first-line-indent: 0em)
#set heading(numbering: "1")

#align(center)[
  #v(1.5em)
  #text(size: 17.28pt)[Algorithmic Pseudocode Sample 3] \
  #v(1.5em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
  #v(2em)
]

#let algcounter = counter("algorithm")

#let algtop(txt) = {
  algcounter.step()
  block(above: 0.4em, below: 0.4em)[
    #line(length: 100%, stroke: 0.8pt)
    #v(-0.5em)
    *Algorithm #context algcounter.display()* #txt
    #v(-0.5em)
    #line(length: 100%, stroke: 0.4pt)
  ]
}

#let algbottom(txt) = {
  algcounter.step()
  block(above: 0em, below: 0.4em)[
    #line(length: 100%, stroke: 0.4pt)
    #v(-0.3em)
    *Algorithm #context algcounter.display():* #txt
    #v(-0.5em)
    #line(length: 100%, stroke: 0.8pt)
  ]
}

#let innertop() = {
  block(above: 0.4em, below: 0em)[
    #line(length: 100%, stroke: 0.8pt)
    #v(-0.3em)
    #line(length: 100%, stroke: 0.4pt)
  ]
}

#let Comment(body) = [#h(1em)#sym.triangle.stroked.r #body]

= Algorithm

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#pagebreak()

#algcounter.step()
#algtop[Initialization of the control and state variables]

#let ind(n, body) = block(above: 0.7em, below: 0.7em)[#h(n*2em)#body]

#ind(0)[*for* $t in {-1, dots, -T^(t r a c e b a c k)}$ *do*#Comment[Retrieve the values of $P_(u,t)$]]
#ind(1)[$P_(u,t) <- mono("Power.GetValue")(t)$]
#ind(0)[*end for*]
#ind(0)[*for* $t in {-1, dots, -T^(t r a c e b a c k)}$ *do*#Comment[Initial conditions on the state variables]]
#ind(1)[*if* $P_(u,t) > mono("MinimumPower.GetValue")(t)$ *then*]
#ind(2)[$S_(u,t)^(O F F) <- 0$]
#ind(2)[$S_(u,t)^(S T O P) <- 0$]
#ind(2)[$S_(u,t)^(S T A R T) <- 0$]
#ind(2)[*if* $P_(u,t) < P_(u,t-1)$ *then*#Comment[Exact initialization required only if the FLAT state is defined.]]
#ind(3)[$S_(t-1)^(O N \_ U P) <- 0$]
#ind(3)[$S_(t-1)^(O N \_ D O W N) <- 1$]
#ind(3)[$S_(t-1)^(O N \_ F L A T) <- 0$]
#ind(2)[*else if* $P_(u,t) > P_(u,t-1)$ *then*]
#ind(3)[$S_(t-1)^(O N \_ U P) <- 1$]
#ind(3)[$S_(t-1)^(O N \_ D O W N) <- 0$]
#ind(3)[$S_(t-1)^(O N \_ F L A T) <- 0$]
#ind(2)[*else if* $P_(u,t) = P_(u,t-1)$ *then*]
#ind(3)[$S_(t-1)^(O N \_ U P) <- 0$]
#ind(3)[$S_(t-1)^(O N \_ D O W N) <- 0$]
#ind(3)[$S_(t-1)^(O N \_ F L A T) <- 1$]
#ind(2)[*end if*]
#ind(1)[*else if* $P_(u,t) > 0$ *then*#Comment[Reconstruct the startups and shutdowns]]
#ind(2)[*if* $P_(u,t) < P_(u,t-1)$ *then*]
#ind(3)[$S_(t)^(S T O P) <- 1$]
#ind(3)[$S_(t)^(S T A R T) <- 0$]
#ind(2)[*else*]
#ind(3)[$S_(t)^(S T O P) <- 0$]
#ind(3)[$S_(t)^(S T A R T) <- 1$]
#ind(2)[*end if*]
#ind(1)[*else*#Comment[Final possibility: the unit is OFF.]]
#ind(2)[$S_(u,t)^(O F F) <- 1$]
#ind(2)[$S_(u,t)^(S T O P) <- 0$]
#ind(2)[$S_(u,t)^(S T A R T) <- 0$]
#ind(2)[$S_(t-1)^(O N \_ U P) <- 0$]
#ind(2)[$S_(t-1)^(O N \_ D O W N) <- 0$]
#ind(2)[$S_(t-1)^(O N \_ F L A T) <- 0$]
#ind(1)[*end if*]
#ind(0)[*end for*]

#block(above: 0em, below: 0.5em)[
  #line(length: 100%, stroke: 0.8pt)
]
