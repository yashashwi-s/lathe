#let margin = sys.inputs.at("margin", default: "1in")
#let fontsize = sys.inputs.at("fontsize", default: "11pt")

#set page(paper: "us-letter", margin: eval(margin), numbering: "1")
#set text(font: "New Computer Modern", size: eval(fontsize))
#set par(justify: true, leading: 0.55em)
#show math.equation: set text(font: "New Computer Modern Math")

#align(center)[
  #v(0.6in)
  #text(size: 17.28pt)[Algorithmic Pseudocode Sample 3]
  #v(0.7em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
]
#v(1.5em)

#heading(numbering: "1", outlined: false)[Algorithm]

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#pagebreak()

#let cmt(x) = h(1fr) + text[▷ #x]
#let kw(x) = text(weight: "bold")[#x]
#let mono(x) = text(font: "DejaVu Sans Mono", size: 0.9em)[#x]

#let indent1 = h(1.5em)
#let indent2 = h(3.0em)
#let indent3 = h(4.5em)
#let indent4 = h(6.0em)

#line(length: 100%, stroke: 0.6pt)
#v(-0.6em)
#line(length: 100%, stroke: 0.6pt)
#v(-0.3em)
*Algorithm 2* Initialization of the control and state variables
#v(-0.3em)
#line(length: 100%, stroke: 0.4pt)

#set par(justify: false, leading: 0.65em)

#indent1 #kw[for] $t in {-1, dots, -T^("traceback")}$ #kw[do] #cmt[Retrieve the values of $P_(u,t)$] \
#indent2 $P_(u,t) <- mono("Power.GetValue")(t)$ \
#indent1 #kw[end for] \
#indent1 #kw[for] $t in {-1, dots, -T^("traceback")}$ #kw[do] #cmt[Initial conditions on the state variables] \
#indent2 #kw[if] $P_(u,t) > mono("MinimumPower.GetValue")(t)$ #kw[then] \
#indent3 $S_(u,t)^("OFF") <- 0$ \
#indent3 $S_(u,t)^("STOP") <- 0$ \
#indent3 $S_(u,t)^("START") <- 0$ \
#indent3 #kw[if] $P_(u,t) < P_(u,t-1)$ #kw[then] #h(1em) ▷ Exact initialization required only if the FLAT state is defined. \
#indent4 $S_(t-1)^("ON_UP") <- 0$ \
#indent4 $S_(t-1)^("ON_DOWN") <- 1$ \
#indent4 $S_(t-1)^("ON_FLAT") <- 0$ \
#indent3 #kw[else if] $P_(u,t) > P_(u,t-1)$ #kw[then] \
#indent4 $S_(t-1)^("ON_UP") <- 1$ \
#indent4 $S_(t-1)^("ON_DOWN") <- 0$ \
#indent4 $S_(t-1)^("ON_FLAT") <- 0$ \
#indent3 #kw[else if] $P_(u,t) = P_(u,t-1)$ #kw[then] \
#indent4 $S_(t-1)^("ON_UP") <- 0$ \
#indent4 $S_(t-1)^("ON_DOWN") <- 0$ \
#indent4 $S_(t-1)^("ON_FLAT") <- 1$ \
#indent3 #kw[end if] \
#indent2 #kw[else if] $P_(u,t) > 0$ #kw[then] #cmt[Reconstruct the startups and shutdowns] \
#indent3 #kw[if] $P_(u,t) < P_(u,t-1)$ #kw[then] \
#indent4 $S_(t)^("STOP") <- 1$ \
#indent4 $S_(t)^("START") <- 0$ \
#indent3 #kw[else] \
#indent4 $S_(t)^("STOP") <- 0$ \
#indent4 $S_(t)^("START") <- 1$ \
#indent3 #kw[end if] \
#indent2 #kw[else] #cmt[Final possibility: the unit is OFF.] \
#indent3 $S_(u,t)^("OFF") <- 1$ \
#indent3 $S_(u,t)^("STOP") <- 0$ \
#indent3 $S_(u,t)^("START") <- 0$ \
#indent3 $S_(t-1)^("ON_UP") <- 0$ \
#indent3 $S_(t-1)^("ON_DOWN") <- 0$ \
#indent3 $S_(t-1)^("ON_FLAT") <- 0$ \
#indent2 #kw[end if] \
#indent1 #kw[end for]

#v(-0.3em)
#line(length: 100%, stroke: 0.4pt)
#v(-0.6em)
#line(length: 100%, stroke: 0.6pt)
