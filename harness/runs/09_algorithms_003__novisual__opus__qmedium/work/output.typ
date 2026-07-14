#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true, leading: 0.55em)

#align(center)[
  #text(size: 17.28pt)[Algorithmic Pseudocode Sample 3]

  #v(0.6em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
]

#v(1em)

#text(size: 14.4pt, weight: "bold")[1#h(0.75em)Algorithm]

#v(0.6em)

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#v(0.5em)

#let kw(x) = text(weight: "bold")[#x]
#let cmt(x) = text[$triangle.stroked.small$ #x]
#let ind(n, body) = pad(left: n * 1em, body)

#figure(
  kind: "algorithm",
  supplement: [Algorithm],
  caption: [Initialization of the control and state variables],
)[
  #set align(left)
  #set text(size: 10pt)
  #show: block.with(stroke: (top: 0.5pt, bottom: 0.5pt), inset: (y: 6pt), width: 100%)

  #let line(body) = block(spacing: 0.4em, body)
  #let pt = $P_(u,t)$
  #let ptm = $P_(u,t-1)$

  #line[#kw[for] $t in {-1, dots, -T^("traceback")}$ #kw[do] #h(1fr) #cmt[Retrieve the values of $P_(u,t)$]]
  #ind(1)[#line[$P_(u,t) <- upright("Power.GetValue")(t)$]]
  #line[#kw[end for]]
  #line[#kw[for] $t in {-1, dots, -T^("traceback")}$ #kw[do] #h(1fr) #cmt[Initial conditions on the state variables]]
  #ind(1)[#line[#kw[if] $P_(u,t) > upright("MinimumPower.GetValue")(t)$ #kw[then]]]
  #ind(2)[#line[$S_(u,t)^("OFF") <- 0$]]
  #ind(2)[#line[$S_(u,t)^("STOP") <- 0$]]
  #ind(2)[#line[$S_(u,t)^("START") <- 0$]]
  #ind(2)[#line[#kw[if] $P_(u,t) < P_(u,t-1)$ #kw[then] #h(1fr) #cmt[Exact initialization required only if the FLAT state is defined.]]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"UP") <- 0$]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"DOWN") <- 1$]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"FLAT") <- 0$]]
  #ind(2)[#line[#kw[else if] $P_(u,t) > P_(u,t-1)$ #kw[then]]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"UP") <- 1$]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"DOWN") <- 0$]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"FLAT") <- 0$]]
  #ind(2)[#line[#kw[else if] $P_(u,t) = P_(u,t-1)$ #kw[then]]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"UP") <- 0$]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"DOWN") <- 0$]]
  #ind(3)[#line[$S_(t-1)^("ON"\_"FLAT") <- 1$]]
  #ind(2)[#line[#kw[end if]]]
  #ind(1)[#line[#kw[else if] $P_(u,t) > 0$ #kw[then] #h(1fr) #cmt[Reconstruct the startups and shutdowns]]]
  #ind(2)[#line[#kw[if] $P_(u,t) < P_(u,t-1)$ #kw[then]]]
  #ind(3)[#line[$S_(t)^("STOP") <- 1$]]
  #ind(3)[#line[$S_(t)^("START") <- 0$]]
  #ind(2)[#line[#kw[else]]]
  #ind(3)[#line[$S_(t)^("STOP") <- 0$]]
  #ind(3)[#line[$S_(t)^("START") <- 1$]]
  #ind(2)[#line[#kw[end if]]]
  #ind(1)[#line[#kw[else] #h(1fr) #cmt[Final possibility: the unit is OFF.]]]
  #ind(2)[#line[$S_(u,t)^("OFF") <- 1$]]
  #ind(2)[#line[$S_(u,t)^("STOP") <- 0$]]
  #ind(2)[#line[$S_(u,t)^("START") <- 0$]]
  #ind(2)[#line[$S_(t-1)^("ON"\_"UP") <- 0$]]
  #ind(2)[#line[$S_(t-1)^("ON"\_"DOWN") <- 0$]]
  #ind(2)[#line[$S_(t-1)^("ON"\_"FLAT") <- 0$]]
  #ind(1)[#line[#kw[end if]]]
  #line[#kw[end for]]
]
