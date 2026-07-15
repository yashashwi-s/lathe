#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true, leading: 0.65em, first-line-indent: 1.5em)
#show math.equation: set text(size: 11pt)

#align(center)[
  #v(1.5em)
  #text(size: 17.28pt)[Algorithmic Pseudocode Sample 3]

  #v(1em)
  #text(size: 12pt)[Source-backed Image2Struct algorithm sample]
  #v(2em)
]

#let sect(n, t) = [#v(0.5em) #text(size: 14pt, weight: "bold")[#n #h(0.5em) #t] #v(0.3em)]

#sect(1)[Algorithm]

This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#v(0.6em)

#let Pu = $P_(u,t)$
#let Pum = $P_(u,t-1)$

#let indent(n, body) = pad(left: n * 1.2em, body)
#let kw(x) = text(weight: "bold")[#x]
#let cmt(x) = text(style: "italic")[▷ #x]

#let alg = [
  #set text(size: 11pt)
  #set par(justify: false, leading: 0.7em)
  #align(left)[#text(weight: "bold")[Algorithm 1] Source-backed algorithmic procedure]
  #v(0.6em)
  #line(length: 100%, stroke: 0.5pt)
  #v(-0.3em)

  #let L(n, body) = block(spacing: 0.6em)[#pad(left: n * 1.4em, body)]

  #L(0)[#kw[for] $t in {-1, dots, -T^("traceback")}$ #kw[do] #h(1fr) #cmt[Retrieve the values of #Pu]]
  #L(1)[#Pu $arrow.l$ #raw("Power.GetValue") $(t)$]
  #L(0)[#kw[end for]]
  #L(0)[#kw[for] $t in {-1, dots, -T^("traceback")}$ #kw[do] #h(1fr) #cmt[Initial conditions on the state variables]]
  #L(1)[#kw[if] #Pu $>$ #raw("MinimumPower.GetValue") $(t)$ #kw[then]]
  #L(2)[$S_(u,t)^("OFF") arrow.l 0$]
  #L(2)[$S_(u,t)^("STOP") arrow.l 0$]
  #L(2)[$S_(u,t)^("START") arrow.l 0$]
  #L(2)[#kw[if] #Pu $<$ #Pum #kw[then] #h(1fr) #cmt[Exact initialization required only if the FLAT state is defined.]]
  #L(3)[$S_(t-1)^("ON"\_"UP") arrow.l 0$]
  #L(3)[$S_(t-1)^("ON"\_"DOWN") arrow.l 1$]
  #L(3)[$S_(t-1)^("ON"\_"FLAT") arrow.l 0$]
  #L(2)[#kw[else if] #Pu $>$ #Pum #kw[then]]
  #L(3)[$S_(t-1)^("ON"\_"UP") arrow.l 1$]
  #L(3)[$S_(t-1)^("ON"\_"DOWN") arrow.l 0$]
  #L(3)[$S_(t-1)^("ON"\_"FLAT") arrow.l 0$]
  #L(2)[#kw[else if] #Pu $=$ #Pum #kw[then]]
  #L(3)[$S_(t-1)^("ON"\_"UP") arrow.l 0$]
  #L(3)[$S_(t-1)^("ON"\_"DOWN") arrow.l 0$]
  #L(3)[$S_(t-1)^("ON"\_"FLAT") arrow.l 1$]
  #L(2)[#kw[end if]]
  #L(1)[#kw[else if] #Pu $> 0$ #kw[then] #h(1fr) #cmt[Reconstruct the startups and shutdowns]]
  #L(2)[#kw[if] #Pu $<$ #Pum #kw[then]]
  #L(3)[$S_t^("STOP") arrow.l 1$]
  #L(3)[$S_t^("START") arrow.l 0$]
  #L(2)[#kw[else]]
  #L(3)[$S_t^("STOP") arrow.l 0$]
  #L(3)[$S_t^("START") arrow.l 1$]
  #L(2)[#kw[end if]]
  #L(1)[#kw[else] #h(1fr) #cmt[Final possibility: the unit is OFF.]]
  #L(2)[$S_(u,t)^("OFF") arrow.l 1$]
  #L(2)[$S_(u,t)^("STOP") arrow.l 0$]
  #L(2)[$S_(u,t)^("START") arrow.l 0$]
  #L(2)[$S_(t-1)^("ON"\_"UP") arrow.l 0$]
  #L(2)[$S_(t-1)^("ON"\_"DOWN") arrow.l 0$]
  #L(2)[$S_(t-1)^("ON"\_"FLAT") arrow.l 0$]
  #L(1)[#kw[end if]]
  #L(0)[#kw[end for]]
  #line(length: 100%, stroke: 0.5pt)
  #align(left)[#text(weight: "bold")[Algorithm 2] Initialization of the control and state variables]
]

#alg
