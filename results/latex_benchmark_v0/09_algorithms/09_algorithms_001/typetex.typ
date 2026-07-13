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
#mi(`\mathrm{d} elta_t^{turned\_on}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{turned\_off}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{turned\_off}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{turned\_on}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{stable}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{entered\_up}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{entered\_down}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{stable}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{entered\_up}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{entered\_down}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{stable}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{entered\_up}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{entered\_down}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{stable}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{entered\_up}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{entered\_down}\leftarrow 1`)
#mi(`\mathrm{d} elta_t^{flat,down,stop}\leftarrow \mathrm{d} isplaystyle{\left\lfloor \frac{S_{u,t}^{STOP} + S_{t-1}^{ON\_DOWN} + S_{t-2}^{ON\_FLAT}}{3}\right\rfloor}`)
#mi(`\mathrm{d} elta_t^{down\_to\_stop}\leftarrow 0`)
#mi(`\mathrm{d} elta_t^{down\_to\_stop}\leftarrow 1`)
#mi(`U_{-1} = S_{-1}^{ON\_UP}\times S_{-2}^{ON\_UP}\times\left(P_{u,t_{-1}} - P_{u,t_{-2}}\right)`)
#mi(`D_{-1} = S_{-1}^{ON\_DOWN}\times S_{-2}^{ON\_DOWN}\times\left(P_{u,t_{-1}} - P_{u,t_{-2}}\right)`)

]
]
