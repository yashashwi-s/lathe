#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 1",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 1]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic \For{$t\in \{-1,\dots,-T^{traceback}\}$}\Comment{Initialization of $\delta_t^{turned\_on}$ and $\delta_t^{turned\_off}$} \State$\delta_t^{turned\_on}\leftarrow0$ \State$\delta_t^{turned\_off}\leftarrow0$ \If{$S_{u,t}^{STOP} - S_{t-1}^{STOP} = 1$}\Comment{Replace by $S_{u,t}^{OFF} - S_{t-1}^{OFF} = 1$ if STOP is not defined.} \State$\delta_t^{turned\_off}\leftarrow1$ \ElsIf{$S_{u,t}^{START} - S_{t-1}^{START} = 1$}\Comment{Replace by $S_{u,t}^{OFF} - S_{t-1}^{OFF} = -1$ if START is not defined.} \State$\delta_t^{turned\_on}\leftarrow1$ \EndIf \EndFor \For{$t\in \{-1,\dots,-T^{traceback}\}$}\Comment{Initialization of $\delta_t^{stable}$, $\delta_t^{entered\_up}$ and $\delta_t^{entered\_down}$} \State$\delta_t^{stable}\leftarrow0$ \State$\delta_t^{entered\_up}\leftarrow0$ \State$\delta_t^{entered\_down}\leftarrow0$ \If{$S_{u,t}^{STOP} - S_{t-1}^{STOP} = 1$} \State$\delta_t^{stable}\leftarrow1$ \ElsIf{$S_{u,t}^{ON\_{UP}} - S_{t-1}^{ON\_UP} = 1$} \State$\delta_t^{entered\_up}\leftarrow1$ \ElsIf{$S_{u,t}^{ON\_{UP}} - S_{t-1}^{ON\_UP} = 1$} \State$\delta_t^{entered\_down}\leftarrow1$ \EndIf \EndFor \For{$t\in \{-1,\dots,-T^{traceback}\}$}\Comment{Initialization of $\delta_t^{stable}$, $\delta_t^{entered\_up}$ and $\delta_t^{entered\_down}$} \State$\delta_t^{stable}\leftarrow0$ \State$\delta_t^{entered\_up}\leftarrow0$ \State$\delta_t^{entered\_down}\leftarrow0$ \If{$S_{u,t}^{ON\_{FLAT}} - S_{t-1}^{ON\_FLAT} = 1$} \State$\delta_t^{stable}\leftarrow1$ \ElsIf{$S_{u,t}^{ON\_{UP}} - S_{t-1}^{ON\_UP} = 1$} \State$\delta_t^{entered\_up}\leftarrow1$ \ElsIf{$S_{u,t}^{ON\_{DOWN}} - S_{t-1}^{ON\_DOWN} = 1$} \State$\delta_t^{entered\_down}\leftarrow1$ \EndIf \EndFor \For{$t\in \{-1,\dots,-T^{traceback}\}$}\Comment{Initialization of $\delta_t^{flat,down,stop}$ or $\delta_t^{down\_to\_stop}$} \State$\delta_t^{flat,down,stop}\leftarrow \displaystyle{\left \lfloor \frac{S_{u,t}^{STOP} + S_{t-1}^{ON\_DOWN} + S_{t-2}^{ON\_FLAT}}{3}\right \rfloor}$ \State$\delta_t^{down\_to\_stop}\leftarrow0$ \If{$S_{u,t}^{STOP} - S_{t-1}^{ON\_DOWN} = 0$} \State$\delta_t^{down\_to\_stop}\leftarrow1$ \EndIf \EndFor \State$U_{-1} = S_{-1}^{ON\_UP}\times S_{-2}^{ON\_UP}\times \left(P_{u,t_{-1}} - P_{u,t_{-2}}\right)$\Comment{Initial condition on $U_t$} \State$D_{-1} = S_{-1}^{ON\_DOWN}\times S_{-2}^{ON\_DOWN}\times \left(P_{u,t_{-1}} - P_{u,t_{-2}}\right)$\Comment{Initial condition on $D_t$} algorithmic 
```
]

