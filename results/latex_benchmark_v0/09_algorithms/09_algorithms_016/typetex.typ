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
#mi(`n,p\in\mathbb N, \omega \in [0,1], x\in\mathbb R^n, v \in\mathbb R^{n}`).
Find a sorting permutation #mi(`\sigma`) of vector #mi(`x`). Apply the
#mi(`\sigma`) to #mi(`x`) and #mi(`v`), in place. .
#mi(`v_{i} \gets v_{i-1}`) #mi(`v_{1} \gets 0`) Identify the set of
groups #mi(`G`) of elements of #mi(`v`) corresponding to equal entries
in #mi(`x`). #mi(`\tilde v \gets v`) Calculate sum #mi(`\mathbf s`) of
#mi(`v`)'s elements in group #mi(`g`). Set #mi(`0`) in all
#mi(`\tilde v`)'s elements in group #mi(`g`). Set the #mi(`\tilde v`)'s
first element in group #mi(`g`) to #mi(`\mathbf s`). Set the
#mi(`\tilde v`)'s last element in group #mi(`g`) to #mi(`\mathbf s`).
#mi(`c_{\tilde \omega} \gets`) cumulative sum of #mi(`\tilde v`)
#mi(`c \gets \omega c_1 + (1-\omega)c_0`) Multiplication and addition
element-wise. Find the inverse of #mi(`\sigma`). Apply the
#mi(`\sigma^{-1}`) to #mi(`c`). #mi(`c`)

]
]
