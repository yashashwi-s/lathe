#import "@preview/mitex:0.2.4": *
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

#mi(`n`) independent realizations of the #mi(`p`)-random vector
#mi(`\bold{X}`),
#mi(`\bold{x}^{(1)},\bold{x}^{(2)},\ldots,\bold{x}^{(n)}`)\; a
topological ordering #mi(`Ord`), (and a stopping level #mi(`m`)). An
estimated DAG #mi(`\hat{G}`). Form the complete undirected graph
#mi(`\tilde{G}`) on the vertex set #mi(`V`). Orient edges on
#mi(`\tilde{G}`) respecting the topological ordering to form DAG
#mi(`G'`). #mi(`l=-1`)\; #mi(`\quad \hat{G}=G'`) #strong[repeat]
#mi(`l=l+1`) #strong[for] all vertices #mi(`s\in V`), #strong[do] let
#mi(`\bold{K}_s = pa(s)`) #strong[end for] #strong[repeat] Select a
(new) edge #mi(`t\rightarrow s`) in #mi(`\hat{G}`) such that
#mi(`|\bold{K}_s\backslash\{t\}|\ge l`). #strong[repeat] choose a (new)
set #mi(`\bold{S}\subset \bold{K}_s\backslash\{t\}`) with
#mi(`|\bold{S}|=l`). #strong[if] #mi(`H_0: {\theta}_{st|\bold{K}}=0`)
not rejected delete edge #mi(`t\rightarrow s`) from #mi(`\hat{G}`)
#strong[end if] #strong[until] edge #mi(`t\rightarrow s`) is deleted or
all #mi(`\bold{S}\subset \bold{K}_s\backslash\{t\}`) with
#mi(`|\bold{S}|=l`) have been considered. #strong[until] all edge
#mi(`t\rightarrow s`) in #mi(`\hat{G}`) such that
#mi(`|\bold{K}_s\backslash\{t\}|\ge l`) and
#mi(`\bold{S}\subset \bold{K}_s\backslash\{t\}`) with
#mi(`|\bold{S}|=l`) have been tested for conditional independence.
#strong[until] #mi(`l=m`) or for each edge #mi(`t\rightarrow s`) in
#mi(`\hat{G}`): #mi(`|\bold{K}_s\backslash\{t\}|< l`).

]
]
