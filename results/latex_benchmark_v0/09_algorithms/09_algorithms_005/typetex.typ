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
#smallcaps[LSH] #mi(`d,n \in \mathbb{N}_+`) #mi(`K,L\in \mathbb{N}_+`)
#mi(`p_{\mathrm{near}},p_{\mathrm{far}}\in (0,1)`) For #mi(`l \in L`),
#mi(`\mathcal{T}_l:=[n]`) #mi(`\mathcal{R}:=[n]`)
#mi(`\mathcal{H}:=\{f\in\mathcal{H}:\mathbb{R}^{d}\rightarrow[M]\}`) For
#mi(`l \in [L]`), #mi(`\mathcal{H}_{l} \in \mathcal{H}^K`) For
#mi(`b \in [M^K]`), #mi(`\mathcal{S}_b:=`)AVL tree
#smallcaps[ChooseHashFunc]\(#mi(`k,L`))
#smallcaps[ConstructHashTable]\(#mi(`\{x_i\}_{i\in[n]}`))
#mi(`\mathcal{R} \leftarrow 0`)
#mi(`\mathcal{R}\leftarrow \mathcal{R} \cup \mathcal{T}_{l}`).#smallcaps[Retrieve]\(#mi(`\mathcal{H}_{l}(q)`))
#mi(`\mathcal{H}_{l}(z)`).#smallcaps[Insert]\(#mi(`z`))
#mi(`\mathcal{H}_{l}(x_i)`).#smallcaps[Delete]\(#mi(`x_i`))

]
]
