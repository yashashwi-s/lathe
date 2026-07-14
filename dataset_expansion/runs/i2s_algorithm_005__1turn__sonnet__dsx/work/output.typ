#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Algorithm Sample 5]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Procedure

The pseudocode below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#v(0.5em)

#set par(leading: 0.8em)

#let kw(t) = text(weight: "bold", t)
#let cm(t) = text(fill: rgb("#555555"), style: "italic", sym.triangle.r + " " + t)
#let ind(n) = h(n * 1.5em)

#block(
  stroke: none,
  width: 100%,
  inset: (x: 0pt, y: 4pt),
)[
  #set text(size: 10.5pt)
  #let line(content) = block(above: 2pt, below: 2pt, content)

  #line[#kw[function] #smallcaps[Transport]$(bold(M), bold(beta), bold(g), Delta t)$ #h(1fr) #cm[Input moments, natural parameters, and gauge parameters for all cells]]
  #line[#ind(1)$bold(beta) <- $ #smallcaps[NewtonOptimization]$(bold(M), bold(beta), bold(phi)(bold(u); bold(g)))$ #h(1fr) #cm[Solve the natural parameters by Alg. 1 in the gauge $bold(g)$]]
  #line[#ind(1)$bold(F) <- $ #smallcaps[ComputeFluxes]$(bold(beta), bold(phi)(bold(u); bold(g)))$ #h(1fr) #cm[Compute fluxes of the statistics $bold(phi)(bold(u); bold(g))$ by (3)]]
  #line[#ind(1)$bold(M)_(plus.minus 1), bold(F)_(plus.minus 1) <- $ #smallcaps[SpatialGaugeTransformation]$(bold(M), bold(F), bold(g))$ #h(1fr) #cm[Perform gauge transformation as in (4)]]
  #line[#ind(1)$bold(M) <- $ #smallcaps[FiniteVolumeStep]$(bold(M), bold(F), bold(M)_(plus.minus 1), bold(F)_(plus.minus 1), bold(g), Delta t)$ #h(1fr) #cm[One step forward in time by (5)]]
  #line[#ind(1)#kw[return] $bold(M), bold(beta), bold(g)$]
  #line[#kw[end function]]

  #v(0.3em)

  #line[#kw[function] #smallcaps[Collision]$(bold(M), bold(beta), bold(g), Delta t)$ #h(1fr) #cm[Input moments, natural parameters, and gauge parameters for all cells]]
  #line[#ind(1)$bold(M) <- $ #smallcaps[SourceTerm]$(bold(M), bold(g), Delta t)$ #h(1fr) #cm[Compute source term by operator splitting (6)]]
  #line[#ind(1)#kw[return] $bold(M), bold(beta), bold(g)$]
  #line[#kw[end function]]

  #v(0.3em)

  #line[#kw[function] #smallcaps[Step]$(bold(M), bold(beta), bold(g))$ #h(1fr) #cm[Input moments, natural parameters, and gauge parameters for all cells]]
  #line[#ind(1)$bold(M), bold(beta), bold(g) <- $ #smallcaps[Collision]$(bold(M), bold(beta), bold(g), Delta t\/2)$ #h(1fr) #cm[Compute collision term by operator splitting]]
  #line[#ind(1)$bold(M), bold(beta), bold(g) <- $ #smallcaps[Transport]$(bold(M), bold(beta), bold(g), Delta t)$ #h(1fr) #cm[Compute Transport term by operator splitting]]
  #line[#ind(1)$bold(M), bold(beta), bold(g) <- $ #smallcaps[Collision]$(bold(M), bold(beta), bold(g), Delta t\/2)$ #h(1fr) #cm[Compute collision term by operator splitting]]
  #line[#ind(1)$bold(g)_H <- $ #smallcaps[ComputeGaugeParameters]$(bold(M), bold(g))$ #h(1fr) #cm[Compute the Hermite gauge parameters by (7)]]
  #line[#ind(1)$bold(M)_H, bold(beta)_H <- $ #smallcaps[GaugeTransformation]$(bold(M), bold(beta), bold(g)_H, bold(g))$ #h(1fr) #cm[Transform into the Hermite gauge using (8) and (9)]]
  #line[#ind(1)#kw[return] $bold(M)_H, bold(beta)_H, bold(g)_H$]
  #line[#kw[end function]]
]
