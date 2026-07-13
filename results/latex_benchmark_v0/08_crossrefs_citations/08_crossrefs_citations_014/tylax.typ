#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "On the connection between Quantum Mechanics and the geometry of two-dimensional strings",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[On the connection between Quantum Mechanics and the geometry of two-dimensional strings]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   On the basis of an area-preserving symmetry in the phase space of a one-dimensional matrix model - believed to describe two-dimensional string theory in a black-hole background which also allows for space-time foam - we give a geometric interpretation of the fact that two-dimensional stringy black holes are consistent with conventional quantum mechanics due to the infinite gauged `W-hair' property that characterises them.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<Ell>) and #cite(<Gro>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `Ell`. ] <Ell>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `Gro`. ] <Gro>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `Ant`. ] <Ant>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `Witt`. ] <Witt>

