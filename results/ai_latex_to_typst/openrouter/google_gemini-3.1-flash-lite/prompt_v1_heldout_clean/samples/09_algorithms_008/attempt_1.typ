#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Algorithmic Pseudocode Sample 8] \
  Source-backed Image2Struct algorithm sample \
  #v(1em)
])

= Algorithm
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  block(stroke: 0.5pt + black, inset: 10pt)[
    #set enum(numbering: "1.")
    #text(weight: "bold")[Input:] $n$ independent realizations of the $p$-random vector $bold(X)$, $bold(x)^{(1)}, bold(x)^{(2)}, dots.c, bold(x)^{(n)}$; a topological ordering $Ord$, (and a stopping level $m$). \
    #text(weight: "bold")[Output:] An estimated DAG $hat(G)$. \
    1. Form the complete undirected graph $tilde(G)$ on the vertex set $V$. \
    2. Orient edges on $tilde(G)$ respecting the topological ordering to form DAG $G'$. \
    3. $l = -1$; $quad hat(G) = G'$ \
    4. *repeat* \
    5. $quad l = l + 1$ \
    6. $quad$ *for* all vertices $s in V$, *do* \
    7. $quad quad$ let $bold(K)_s = p a(s)$ \
    8. $quad$ *end for* \
    9. $quad$ *repeat* \
    10. $quad quad$ Select a (new) edge $t arrow s$ in $hat(G)$ such that \
    11. $quad quad |bold(K)_s \\ {t}| >= l$. \
    12. $quad quad$ *repeat* \
    13. $quad quad quad$ choose a (new) set $bold(S) subset bold(K)_s \\ {t}$ with $|bold(S)| = l$. \
    14. $quad quad quad$ *if* $H_0: theta_(s t | bold(K)) = 0$ not rejected \
    15. $quad quad quad quad$ delete edge $t arrow s$ from $hat(G)$ \
    16. $quad quad quad$ *end if* \
    17. $quad quad$ *until* edge $t arrow s$ is deleted or all $bold(S) subset bold(K)_s \\ {t}$ with $|bold(S)| = l$ have been considered. \
    18. $quad$ *until* all edge $t arrow s$ in $hat(G)$ such that $|bold(K)_s \\ {t}| >= l$ and $bold(S) subset bold(K)_s \\ {t}$ with $|bold(S)| = l$ have been tested for conditional independence. \
    19. *until* $l = m$ or for each edge $t arrow s$ in $hat(G)$: $|bold(K)_s \\ {t}| < l$.
  ],
  caption: [Source-backed algorithmic procedure]
)
