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
#strong[Input:]` Set of sequences(S)`
#strong[Output:]` Distance Matrix(D)`
` `#mi(`Es_{1} \gets encoded \hspace{0.2cm} s_{1}`)
` `#mi(`Cs_{1} \gets Gzip\hspace{0.2cm} compressed \hspace{0.2cm} Es_{1}`)
` `#mi(`Ls_{1} \gets length \hspace{0.2cm} of \hspace{0.2cm} Cs_{1}`)
` `#mi(`D \_ local \gets [\ ]`)
` `#mi(`Es_{2} \gets encoded \hspace{0.2cm} s_{2}`)
` `#mi(`Cs_{2} \gets Gzip \hspace{0.2cm} compressed \hspace{0.2cm} Es_{2}`)
` `#mi(`Ls_{2} \gets length \hspace{0.2cm} of \hspace{0.2cm} Cs_{2}`)
` `#mi(`s_{1}s_{2} \gets Concatenate(s_{1},s_{2})`)
` `#mi(`Es_{1}s_{2} \gets encoded \hspace{0.2cm} s_{1}s_{2}`)
` `#mi(`Cs_{1}s_{2} \gets Gzip \hspace{0.2cm} compressed \hspace{0.2cm} Es_{1}s_{2}`)
` `#mi(`Ls_{1}s_{2} \gets length \hspace{0.2cm} of \hspace{0.2cm} Cs_{1}s_{2}`)
NCD #mi(`\gets`)
#mi(`\mathrm{d} frac{L s_1 s_2 - Min (Ls_1, Ls_2)}{Max(Ls_1, Ls_2)}`)
` `#mi(`D\_local.append(NCD)`) #mi(`D.append(D\_local)`) return #mi(`D`)

]
]
