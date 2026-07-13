#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
\$P\_{u,t}\\leftarrow\\textrm{{\\tt Power.GetValue}}(t)\$
$S_(u\,t)^(O F F) arrow.l 0$ $S_(u\,t)^(S T O P) arrow.l 0$
$S_(u\,t)^(S T A R T) arrow.l 0$ $S_(t - 1)^(O N\_U P) arrow.l 0$
$S_(t - 1)^(O N\_D O W N) arrow.l 1$
$S_(t - 1)^(O N\_F L A T) arrow.l 0$ $S_(t - 1)^(O N\_U P) arrow.l 1$
$S_(t - 1)^(O N\_D O W N) arrow.l 0$
$S_(t - 1)^(O N\_F L A T) arrow.l 0$ $S_(t - 1)^(O N\_U P) arrow.l 0$
$S_(t - 1)^(O N\_D O W N) arrow.l 0$
$S_(t - 1)^(O N\_F L A T) arrow.l 1$ $S_t^(S T O P) arrow.l 1$
$S_t^(S T A R T) arrow.l 0$ $S_t^(S T O P) arrow.l 0$
$S_t^(S T A R T) arrow.l 1$ $S_(u\,t)^(O F F) arrow.l 1$
$S_(u\,t)^(S T O P) arrow.l 0$ $S_(u\,t)^(S T A R T) arrow.l 0$
$S_(t - 1)^(O N\_U P) arrow.l 0$ $S_(t - 1)^(O N\_D O W N) arrow.l 0$
$S_(t - 1)^(O N\_F L A T) arrow.l 0$

]
]
