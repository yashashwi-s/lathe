#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "(2+1)-Dimensional Chern-Simons Gravity as a Dirac Square Root",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[(2+1)-Dimensional Chern-Simons Gravity as a Dirac Square Root]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   For (2+1)-dimensional spacetimes with the spatial topology of a torus, the transformation between the Chern-Simons and ADM versions of quantum gravity is constructed explicitly, and the wave functions are compared. It is shown that Chern-Simons wave functions correspond to modular forms of weight 1/2, that is, spinors on the ADM moduli space, and that their evolution (in York's ``extrinsic time'' variable) is described by a Dirac equation. (This version replaces paper 9109006, which was garbled by my mailer.)
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<Mart>) and #cite(<HosNak>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `Mart`. ] <Mart>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `HosNak`. ] <HosNak>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `Visser`. ] <Visser>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `HosNak2`. ] <HosNak2>

