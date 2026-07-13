#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 16",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 16]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic[1] \Require$n,p\in \mathbbN, \omega \in[0,1], x\in \mathbbR^n, v \in \mathbbR^{n}$. \State Find a sorting permutation $\sigma$ of vector $x$. \State Apply the $\sigma$ to $x$ and $v$, in place. \For{$\tilde\omega= 1,0$} \If{$\tilde\omega= 0$} \Comment{Shift $v$ by one place because of 0s on diagonal of $\mathbfI$}. \For{$i = n,n-1,...,2$} \State$v_{i} \gets v_{i-1}$ \EndFor \State$v_{1} \gets0$ \EndIf \State Identify the set of groups $G$ of elements of $v$ corresponding to equal entries in $x$. \State$\tildev \gets v$ \For{$g$ in $G$} \State Calculate sum $\mathbfs$ of $v$'s elements in group $g$. \State Set $0$ in all $\tildev$'s elements in group $g$. \If{$\tilde\omega= 0$} \State Set the $\tildev$'s first element in group $g$ to $\mathbfs$. \Else \State Set the $\tildev$'s last element in group $g$ to $\mathbfs$. \EndIf \EndFor \State$c_{\tilde\omega} \gets$ cumulative sum of $\tildev$ \EndFor \State$c \gets \omega c_1 + (1-\omega)c_0$ \Comment Multiplication and addition element-wise. \State Find the inverse of $\sigma$. \State Apply the $\sigma^{-1}$ to $c$. \State \Return$c$ algorithmic 
```
]

