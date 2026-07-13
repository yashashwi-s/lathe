#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 17",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 17]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic[1] \Statex \textbf{Input:}\texttt{ Set of sequences(S)} \Statex \textbf{Output:}\texttt{ Distance Matrix(D)} \For{\texttt{ $s_{1}$ in S\hspace{0.2cm}}} \State \texttt{ $Es_{1} \gets encoded \hspace{0.2cm} s_{1}$} \State \texttt{ $Cs_{1} \gets Gzip\hspace{0.2cm} compressed \hspace{0.2cm} Es_{1}$} \State \texttt{ $Ls_{1} \gets length \hspace{0.2cm} of \hspace{0.2cm} Cs_{1}$} \State \texttt{ $D \_ local \gets[\ ]$} \For{\texttt{ $s_{2}$ in S\hspace{0.2cm}}} \State \texttt{ $Es_{2} \gets encoded \hspace{0.2cm} s_{2}$} \State \texttt{ $Cs_{2} \gets Gzip \hspace{0.2cm} compressed \hspace{0.2cm} Es_{2}$} \State \texttt{ $Ls_{2} \gets length \hspace{0.2cm} of \hspace{0.2cm} Cs_{2}$} \State \texttt{ $s_{1}s_{2} \gets Concatenate(s_{1},s_{2})$} \State \texttt{ $Es_{1}s_{2} \gets encoded \hspace{0.2cm} s_{1}s_{2}$} \State \texttt{ $Cs_{1}s_{2} \gets Gzip \hspace{0.2cm} compressed \hspace{0.2cm} Es_{1}s_{2}$} \State \texttt{ $Ls_{1}s_{2} \gets length \hspace{0.2cm} of \hspace{0.2cm} Cs_{1}s_{2}$} \State NCD $\gets$ $\dfrac{L s_1 s_2 - Min (Ls_1, Ls_2)}{Max(Ls_1, Ls_2)}$ \State \texttt{ $D\_local.append(NCD)$} \EndFor \State$D.append(D\_local)$ \EndFor \State return $D$ algorithmic 
```
]

