#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Procedure
<procedure>
The pseudocode below is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

#block[
\$\\boldsymbol{\\beta}\\gets \\Call{NewtonOptimization}{\\bold{M},\\boldsymbol{\\beta}, \\boldsymbol{\\phi}(\\bold{u} ;\\mathbf{g})}\$
\$\\bold{F} \\gets \\Call{ComputeFluxes}{\\boldsymbol{\\beta}, \\boldsymbol{\\phi}(\\bold{u} ;\\mathbf{g})}\$
\$\\bold{M}\_{\\pm1}, \\bold{F}\_{\\pm1} \\gets \\Call{SpatialGaugeTransformation}{\\bold{M}, \\bold{F}, \\bold{g}}\$
\$\\bold{M} \\gets \\Call{FiniteVolumeStep}{\\bold{M}, \\bold{F},\\bold{M}\_{\\pm1}, \\bold{F}\_{\\pm1}, \\bold{g}, \\Delta t}\$
#strong[return] \$\\bold{M}, \\boldsymbol{\\beta}, \\bold{g}\$
\$\\bold{M} \\gets \\Call{SourceTerm}{\\bold{M}, \\bold{g}, \\Delta t}\$
#strong[return] \$\\bold{M}, \\boldsymbol{\\beta}, \\bold{g}\$
\$\\bold{M}, \\boldsymbol{\\beta}, \\bold{g} \\gets \\Call{Collision}{\\bold{M},\\boldsymbol{\\beta},\\bold{g}, \\Delta t/2}\$
\$\\bold{M}, \\boldsymbol{\\beta}, \\bold{g} \\gets \\Call{Transport}{\\bold{M},\\boldsymbol{\\beta},\\bold{g}, \\Delta t}\$
\$\\bold{M}, \\boldsymbol{\\beta}, \\bold{g} \\gets \\Call{Collision}{\\bold{M},\\boldsymbol{\\beta},\\bold{g}, \\Delta t/2}\$
\$\\bold{g}\_H \\gets \\Call{ComputeGaugeParameters}{\\bold{M}, \\bold{g}}\$
\$\\bold{M}\_H,\\boldsymbol{\\beta}\_H \\gets \\Call{GaugeTransformation}{\\bold{M}, \\boldsymbol{\\beta}, \\bold{g}\_H, \\bold{g}}\$
#strong[return] \$\\bold{M}\_H, \\boldsymbol{\\beta}\_H, \\bold{g}\_H\$

]
