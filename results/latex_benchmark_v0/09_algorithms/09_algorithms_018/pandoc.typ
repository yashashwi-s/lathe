#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
#strong[Inputs:] $s\,i\,d\,a\,r\,e\,v\,h$, daily vaccinations
#strong[Output:]
$arrow(beta)_(u u)\,arrow(beta)_(v u)\,arrow(beta)_(v v)$,
$arrow(beta)_(u v)$ #strong[Initialization:] $n = 7$ or $n = 14$ Select
window $z_j = { j - n + 1\,. . .\,j }$ Initialize parameters
$beta_(u u)$, $beta_(v u)$, $beta_(v v)$, $beta_(u v)$ Calculate the
initial cost $C_j\(n\,i\,d\,hat(i)_j\,hat(d)_j\)$ $f l a g = 0$ Create
the trial parameters set $P_k$ Calculate a cost using every parameter
from $P_k$ set Find the minimum of all costs
$C'_j\(n\,i\,d\,hat(i)_j\,hat(d)_j\)$
$C_j\(n\,i\,d\,hat(i)_j\,hat(d)_j\)= C'_j\(n\,i\,d\,hat(i)_j\,hat(d)_j\)$
Keep the modified infection rate and create new set of trial parameters
$P'_k$ $f l a g = 1$

]
]
