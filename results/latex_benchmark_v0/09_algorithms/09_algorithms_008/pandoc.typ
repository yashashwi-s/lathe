#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[

#horizontalrule

$n$ independent realizations of the $p$-random vector \$\\bold{X}\$,
\$\\bold{x}^{(1)},\\bold{x}^{(2)},\\ldots,\\bold{x}^{(n)}\$\; a
topological ordering $O r d$, (and a stopping level $m$). An estimated
DAG $hat(G)$. Form the complete undirected graph $tilde(G)$ on the
vertex set $V$. Orient edges on $tilde(G)$ respecting the topological
ordering to form DAG $G'$. $l = - 1$\; $quad hat(G) = G'$
#strong[repeat] $l = l + 1$ #strong[for] all vertices $s in V$,
#strong[do] let \$\\bold{K}\_s = pa(s)\$ #strong[end for]
#strong[repeat] Select a (new) edge $t arrow.r s$ in $hat(G)$ such that
\$|\\bold{K}\_s\\backslash\\{t\\}|\\ge l\$. #strong[repeat] choose a
(new) set \$\\bold{S}\\subset \\bold{K}\_s\\backslash\\{t\\}\$ with
\$|\\bold{S}|=l\$. #strong[if] \$H\_0: {\\theta}\_{st|\\bold{K}}=0\$ not
rejected delete edge $t arrow.r s$ from $hat(G)$ #strong[end if]
#strong[until] edge $t arrow.r s$ is deleted or all
\$\\bold{S}\\subset \\bold{K}\_s\\backslash\\{t\\}\$ with
\$|\\bold{S}|=l\$ have been considered. #strong[until] all edge
$t arrow.r s$ in $hat(G)$ such that
\$|\\bold{K}\_s\\backslash\\{t\\}|\\ge l\$ and
\$\\bold{S}\\subset \\bold{K}\_s\\backslash\\{t\\}\$ with
\$|\\bold{S}|=l\$ have been tested for conditional independence.
#strong[until] $l = m$ or for each edge $t arrow.r s$ in $hat(G)$:
\$|\\bold{K}\_s\\backslash\\{t\\}|\< l\$.

]
]
