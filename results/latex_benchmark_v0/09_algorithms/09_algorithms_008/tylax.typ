#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 8",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 8]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic[1] \hrule \vskip2pt \State{\textbf{Input}:} $n$ independent realizations of the $p$-random vector $\bold{X}$, $\bold{x}^{(1)},\bold{x}^{(2)},\ldots,\bold{x}^{(n)}$; a topological ordering $Ord$, (and a stopping level $m$). \State{\textbf{Output}:} An estimated DAG $\hat{G}$. \State{} Form the complete undirected graph $\tilde{G}$ on the vertex set $V$. \State{} Orient edges on $\tilde{G}$ respecting the topological ordering to form DAG $G'$. \State{} $l=-1$; $\quad \hat{G}=G'$ \State{} \textbf{repeat} \State{} \quad$l=l+1$ \State{} \quad \textbf{for} all vertices $s\in V$, \textbf{do} \State{} \quad \quad let $\bold{K}_s = pa(s)$ \State{} \quad \textbf{end for} \State{} \quad \textbf{repeat} \State{} \quad \quad Select a (new) edge $t\rightarrow s$ in $\hat{G}$ such that \State{} \quad \quad$|\bold{K}_s\backslash \{t\}|\ge l$. \State{} \quad \quad \textbf{repeat} \State{} \quad \quad \quad choose a (new) set $\bold{S}\subset \bold{K}_s\backslash \{t\}$ with $|\bold{S}|=l$. \State{} \quad \quad \quad \textbf{if} $H_0: {\theta}_{st|\bold{K}}=0$ not rejected%$s$ and $t$ are conditionally independent given $\bold{K}$ then
\State{} \quad \quad \quad \quad delete edge $t\rightarrow s$ from $\hat{G}$ \State{} \quad \quad \quad \textbf{end if} \State{} \quad \quad \textbf{until} edge $t\rightarrow s$ is deleted or all $\bold{S}\subset \bold{K}_s\backslash \{t\}$ with $|\bold{S}|=l$ have been considered. \State{} \quad \textbf{until} all edge $t\rightarrow s$ in $\hat{G}$ such that $|\bold{K}_s\backslash \{t\}|\ge l$ and $\bold{S}\subset \bold{K}_s\backslash \{t\}$ with $|\bold{S}|=l$ have been tested for conditional independence. \State{} \textbf{until} $l=m$ or for each edge $t\rightarrow s$ in $\hat{G}$: $|\bold{K}_s\backslash \{t\}|< l$. algorithmic 
```
]

