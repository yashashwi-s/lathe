#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "serif")

#align(center, [
  #text(size: 1.44em, weight: "bold")[Algorithm Sample 5] \
  #text(size: 1.2em)[Dataset-expansion sample] \
  #v(1em)
])

= Procedure
The pseudocode below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#let alg-indent = 1.5em
#let comment(c) = h(1fr) + text(fill: rgb(0, 0, 0, 150), size: 0.9em)[// #c]
#let func(name, args) = text(weight: "bold")[Function] + " " + name + "(" + args + ")"
#let state(content) = pad(left: alg-indent, content)

#v(1em)
#block(stroke: (top: 0.5pt, bottom: 0.5pt), inset: (y: 0.5em))[
  #set text(font: "monospace")
  #func("Transport", [$bold(M), bold(beta), bold(g), Delta t$]) #comment("Input moments, natural parameters, and gauge parameters for all cells") \
  #state[$bold(beta) arrow.l "NewtonOptimization"(bold(M), bold(beta), phi(bold(u); bold(g)))$ #comment("Solve the natural parameters by Alg. 1 in the gauge $bold(g)$")] \
  #state[$bold(F) arrow.l "ComputeFluxes"(bold(beta), phi(bold(u); bold(g)))$ #comment("Compute fluxes of the statistics $phi(bold(u); bold(g))$ by eq. (3)")] \
  #state[$bold(M)_(plus.minus 1), bold(F)_(plus.minus 1) arrow.l "SpatialGaugeTransformation"(bold(M), bold(F), bold(g))$ #comment("Perform gauge transformation as in eq. (4)")] \
  #state[$bold(M) arrow.l "FiniteVolumeStep"(bold(M), bold(F), bold(M)_(plus.minus 1), bold(F)_(plus.minus 1), bold(g), Delta t)$ #comment("One step forward in time by eq. (5)")] \
  #state[#text(weight: "bold")[return] $bold(M), bold(beta), bold(g)$] \
  #func("Collision", [$bold(M), bold(beta), bold(g), Delta t$]) #comment("Input moments, natural parameters, and gauge parameters for all cells") \
  #state[$bold(M) arrow.l "SourceTerm"(bold(M), bold(g), Delta t)$ #comment("Compute source term by operator splitting eq. (6)")] \
  #state[#text(weight: "bold")[return] $bold(M), bold(beta), bold(g)$] \
  #func("Step", [$bold(M), bold(beta), bold(g)$]) #comment("Input moments, natural parameters, and gauge parameters for all cells") \
  #state[$bold(M), bold(beta), bold(g) arrow.l "Collision"(bold(M), bold(beta), bold(g), Delta t/2)$ #comment("Compute collision term by operator splitting")] \
  #state[$bold(M), bold(beta), bold(g) arrow.l "Transport"(bold(M), bold(beta), bold(g), Delta t)$ #comment("Compute Transport term by operator splitting")] \
  #state[$bold(M), bold(beta), bold(g) arrow.l "Collision"(bold(M), bold(beta), bold(g), Delta t/2)$ #comment("Compute collision term by operator splitting")] \
  #state[$bold(g)_H arrow.l "ComputeGaugeParameters"(bold(M), bold(g))$ #comment("Compute the Hermite gauge parameters by eq. (7)")] \
  #state[$bold(M)_H, bold(beta)_H arrow.l "GaugeTransformation"(bold(M), bold(beta), bold(g)_H, bold(g))$ #comment("Transform into the Hermite gauge using eq. (8) and eq. (9)")] \
  #state[#text(weight: "bold")[return] $bold(M)_H, bold(beta)_H, bold(g)_H$]
]
