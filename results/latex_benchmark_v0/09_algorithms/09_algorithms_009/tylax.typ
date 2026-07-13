#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 9",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 9]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic[1] \State{$ t \gets1; \ \textbf{m}_{1} \gets \mathbf{1}_{\bar{C}}; \ \alpha \gets1 $ \hfill \# Step t = 1}\For{$ e \gets1,...,E $ } \State{FBP() \hfill \# Algorithm~\ref{FBP:alg}} \EndFor \State{$ \bar{\textbf{s}}_{1} \gets \text{mean of} \ \tilde{s} \ \text{across data} $ }\For{$ t \gets2,...,T $} \hfill \# Steps $ t \geq2 $ \State{\hfill \# Phase 1} \State{$ \bar{\textbf{s}}_t \gets \bar{\textbf{s}}_{t-1}; \ \alpha \gets \frac{1}{2}; \ \textbf{m}_{t} \gets \textbf{m}_{t-1} $ } \For{$ e \gets1,...,E_{1} $} \State{FBP()} \EndFor \State{$ \bar{\textbf{s}} \gets \text{mean of} \ \tilde{s} \ \text{on data} $ \hfill \# Phase 2} \State{$ \bar{\textbf{s}}_{t} \gets \frac{1}{2}(\bar{\textbf{s}}_{t} + \bar{\textbf{s}}) $ } \For{$ e \gets E_{1}+1,...,E_{2} $} \State{$ \alpha \gets \max \{\alpha- \frac{1}{2(E_{2}-E_{1})},0 \} $} \State{FBP()} \EndFor \State{\# Indices that sort an array; \hfill Phase 3} \State{$ R = \text{argsort} \{ \bar{\textbf{s}}_{t}[i] : \textbf{m}_{t}[i] = 1 \} $} \State{$ D_{t} \gets \{R[0],...,R[C_{t-1}-C_{t}] \} $} \For{$ e \gets E_{2} + 1,...,E_{3} $} \State{$ \textbf{m}_{t} \gets \max \{\textbf{m}_{t} - \frac{\mathbb{I}[i]_{i \in D_{t}} }{E_{3} - E_{2}}, \textbf{0}_{\bar{C}} \} $} \State{FBP()} \EndFor \For{$ e \gets E_{3}+1,...,E $} \hfill \# Phase 4 \State{FBP()} \EndFor \State{Cache $ \mathcal{T}_{t} $, $ \textbf{m}_{t},\bar{\textbf{s}}_{t} $ for equation~\ref{Outer_Loop:eq}} \EndFor algorithmic 
```
]

