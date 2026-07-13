#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 5",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 5]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic[1] \State{\bf data structure} \textsc{LSH} \State{\bf members} \State \hspace{4mm} $d,n \in \mathbb{N}_+$ \Comment{$d$ is dimension, $n$ is number of data points} \State \hspace{4mm} $K,L\in \mathbb{N}_+$ \Comment{$K$ is amplification factor, $L$ is number of repetition for hashing} \State \hspace{4mm} $p_{\mathrm{near}},p_{\mathrm{far}}\in(0,1)$ \Comment{Collision probability} \State \hspace{4mm} For $l \in L$, $\mathcal{T}_l:=[n]$ \Comment{Hashtable recording data points hashed by $\mathcal{H}_l$} \State \hspace{4mm} $\mathcal{R}:=[n]$ \Comment{retrieved points} \State \hspace{4mm} $\mathcal{H}:=\{f\in \mathcal{H}:\mathbb{R}^{d}\rightarrow[M]\}$ \Comment{$M$ is number of buckets for hashing family $\mathcal{H}$} \State \hspace{4mm} For $l \in[L]$, $\mathcal{H}_{l} \in \mathcal{H}^K$ \Comment{Family of amplified hash functions with at most $M^K$ non-empty buckets} \State \hspace{4mm} For $b \in[M^K]$, $\mathcal{S}_b:=$AVL tree \Comment{Use AVL tree to store points in bucket} \State{\bf end members} \State \State{\bf public} \Procedure{\textsc{Initialize}}{$\{x_i\}_{i\in[n]}\subset \mathbb{R}^d, k,L\in \mathbb{N}_+$} \State \textsc{ChooseHashFunc}($k,L$) \State \textsc{ConstructHashTable}($\{x_i\}_{i\in[n]}$)\EndProcedure \State \Procedure{\textsc{Recover}}{$q\in \mathbb{R}^d$} \State$\mathcal{R} \leftarrow0$ \For{$l\in[L]$} \State$\mathcal{R}\leftarrow \mathcal{R} \cup \mathcal{T}_{l}$.\textsc{Retrieve}($\mathcal{H}_{l}(q)$) \Comment{Find the bucket $\mathcal{H}_{l}(q)$ in $\mathcal{T}_l$ and retrieve all points} \EndFor \EndProcedure \State \Procedure{\textsc{UpdateHashTable}}{$z\in \mathbb{R}^d, i\in[n]$} \For{$l\in[L]$} \State$\mathcal{H}_{l}(z)$.\textsc{Insert}($z$)\Comment{$\mathcal{H}_{l}(z)$ denotes the bucket that $z$ is mapped to} \State$\mathcal{H}_{l}(x_i)$.\textsc{Delete}($x_i$) \EndFor \EndProcedure \State{\bf end data structure} algorithmic 
```
]

