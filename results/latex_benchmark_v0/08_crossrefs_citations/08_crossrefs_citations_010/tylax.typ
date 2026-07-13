#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "W3 Constructions on Affine Lie Algebras",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[W3 Constructions on Affine Lie Algebras]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We use an argument of Romans showing that every Virasoro construction leads to realizations of \$W\_3\$, to construct \$W\_3\$ realizations on arbitrary affine Lie algebras. Solutions are presented for generic values of the level as well as for specific values of the level but with arbitrary parameters. We give a detailed discussion of the \$\aff{su}(2)\_\ell\$-case. Finally, we discuss possible applications of these realizations to the construction of \$W\$-strings.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<halpkit>) and #cite(<moretal>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `halpkit`. ] <halpkit>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `moretal`. ] <moretal>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `irrcons`. ] <irrcons>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `schratro`. ] <schratro>

