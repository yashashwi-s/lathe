#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Procedure
<procedure>
The pseudocode below is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

#block[
#mi(`\boldsymbol{\beta}\gets \Call{NewtonOptimization}{\bold{M},\boldsymbol{\beta}, \boldsymbol{\phi}(\bold{u} ;\mathbf{g})}`)
#mi(`\bold{F} \gets \Call{ComputeFluxes}{\boldsymbol{\beta}, \boldsymbol{\phi}(\bold{u} ;\mathbf{g})}`)
#mi(`\bold{M}_{\pm1}, \bold{F}_{\pm1} \gets \Call{SpatialGaugeTransformation}{\bold{M}, \bold{F}, \bold{g}}`)
#mi(`\bold{M} \gets \Call{FiniteVolumeStep}{\bold{M}, \bold{F},\bold{M}_{\pm1}, \bold{F}_{\pm1}, \bold{g}, \Delta t}`)
#strong[return] #mi(`\bold{M}, \boldsymbol{\beta}, \bold{g}`)
#mi(`\bold{M} \gets \Call{SourceTerm}{\bold{M}, \bold{g}, \Delta t}`)
#strong[return] #mi(`\bold{M}, \boldsymbol{\beta}, \bold{g}`)
#mi(`\bold{M}, \boldsymbol{\beta}, \bold{g} \gets \Call{Collision}{\bold{M},\boldsymbol{\beta},\bold{g}, \Delta t/2}`)
#mi(`\bold{M}, \boldsymbol{\beta}, \bold{g} \gets \Call{Transport}{\bold{M},\boldsymbol{\beta},\bold{g}, \Delta t}`)
#mi(`\bold{M}, \boldsymbol{\beta}, \bold{g} \gets \Call{Collision}{\bold{M},\boldsymbol{\beta},\bold{g}, \Delta t/2}`)
#mi(`\bold{g}_H \gets \Call{ComputeGaugeParameters}{\bold{M}, \bold{g}}`)
#mi(`\bold{M}_H,\boldsymbol{\beta}_H \gets \Call{GaugeTransformation}{\bold{M}, \boldsymbol{\beta}, \bold{g}_H, \bold{g}}`)
#strong[return] #mi(`\bold{M}_H, \boldsymbol{\beta}_H, \bold{g}_H`)

]
