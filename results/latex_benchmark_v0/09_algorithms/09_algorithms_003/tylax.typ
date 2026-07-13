#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 3",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 3]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithm [H] algorithmic \For{$t\in \{-1,\dots,-T^{traceback}\}$}\Comment{Retrieve the values of $P_{u,t}$} \State$P_{u,t}\leftarrow \textrm{{\tt Power.GetValue}}(t)$ \EndFor \For{$t\in \{-1,\dots,-T^{traceback}\}$}\Comment{Initial conditions on the state variables} \If{$P_{u,t} > \textrm{{\tt MinimumPower.GetValue}}(t)$} \State$S_{u,t}^{OFF} \leftarrow0$ \State$S_{u,t}^{STOP} \leftarrow0$ \State$S_{u,t}^{START} \leftarrow0$ \If{$P_{u,t} < P_{u,t-1}$}\Comment{Exact initialization required only if the FLAT state is defined.} \State$S_{t-1}^{ON\_UP} \leftarrow0$ \State$S_{t-1}^{ON\_DOWN} \leftarrow1$ \State$S_{t-1}^{ON\_FLAT} \leftarrow0$ \ElsIf{$P_{u,t} > P_{u,t-1}$} \State$S_{t-1}^{ON\_UP} \leftarrow1$ \State$S_{t-1}^{ON\_DOWN} \leftarrow0$ \State$S_{t-1}^{ON\_FLAT} \leftarrow0$ \ElsIf{$P_{u,t} = P_{u,t-1}$} \State$S_{t-1}^{ON\_UP} \leftarrow0$ \State$S_{t-1}^{ON\_DOWN} \leftarrow0$ \State$S_{t-1}^{ON\_FLAT} \leftarrow1$ \EndIf \ElsIf{$P_{u,t} > 0$}\Comment{Reconstruct the startups and shutdowns} \If{$P_{u,t} < P_{u,t-1}$} \State$S_{t}^{STOP} \leftarrow1$ \State$S_{t}^{START} \leftarrow0$ \Else \State$S_{t}^{STOP} \leftarrow0$ \State$S_{t}^{START} \leftarrow1$ \EndIf \Else \Comment{Final possibility: the unit is OFF.} \State$S_{u,t}^{OFF} \leftarrow1$ \State$S_{u,t}^{STOP} \leftarrow0$ \State$S_{u,t}^{START} \leftarrow0$ \State$S_{t-1}^{ON\_UP} \leftarrow0$ \State$S_{t-1}^{ON\_DOWN} \leftarrow0$ \State$S_{t-1}^{ON\_FLAT} \leftarrow0$ \EndIf \EndFor algorithmic \caption{Initialization of the control and state variables}algorithm 
```
]

