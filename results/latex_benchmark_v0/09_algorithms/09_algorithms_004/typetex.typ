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
#mi(`P_{u,t}\leftarrow\textrm{{\tt Power.GetValue}}(t)`)
#mi(`S_{u,t}^{OFF} \leftarrow 0`) #mi(`S_{u,t}^{STOP} \leftarrow 0`)
#mi(`S_{u,t}^{START} \leftarrow 0`) #mi(`S_{t-1}^{ON\_UP} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_DOWN} \leftarrow 1`)
#mi(`S_{t-1}^{ON\_FLAT} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_UP} \leftarrow 1`)
#mi(`S_{t-1}^{ON\_DOWN} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_FLAT} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_UP} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_DOWN} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_FLAT} \leftarrow 1`) #mi(`S_{t}^{STOP} \leftarrow 1`)
#mi(`S_{t}^{START} \leftarrow 0`) #mi(`S_{t}^{STOP} \leftarrow 0`)
#mi(`S_{t}^{START} \leftarrow 1`) #mi(`S_{u,t}^{OFF} \leftarrow 1`)
#mi(`S_{u,t}^{STOP} \leftarrow 0`) #mi(`S_{u,t}^{START} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_UP} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_DOWN} \leftarrow 0`)
#mi(`S_{t-1}^{ON\_FLAT} \leftarrow 0`)

]
]
