#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "On quantum group symmetries of conformal field theories",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[On quantum group symmetries of conformal field theories]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   The appearance of quantum groups in conformal field theories is traced back to the Poisson-Lie symmetries of the classical chiral theory. A geometric quantization of the classical theory deforms the Poisson-Lie symmetries to the quantum group ones. This elucidates the fundamental role of chiral symmetries that quantum groups play in conformal models. As a byproduct, one obtains a more geometric approach to the representation theory of quantum groups.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<10>) and #cite(<11>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `10`. ] <10>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `11`. ] <11>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `12`. ] <12>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `13`. ] <13>

