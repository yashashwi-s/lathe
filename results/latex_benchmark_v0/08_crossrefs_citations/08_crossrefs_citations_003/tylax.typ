#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "A New Solution to the Star--Triangle Equation Based on U$_q$(sl(2)) at Roots of Unit",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[A New Solution to the Star--Triangle Equation Based on U$_q$(sl(2)) at Roots of Unit]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We find new solutions to the Yang--Baxter equation in terms of the intertwiner matrix for semi-cyclic representations of the quantum group \$U\_q(s\ell(2))\$ with \$q= e^{2\pi i/N}\$. These intertwiners serve to define the Boltzmann weights of a lattice model, which shares some similarities with the chiral Potts model. An alternative interpretation of these Boltzmann weights is as scattering matrices of solitonic structures whose kinematics is entirely governed by the quantum group. Finally, we consider the limit \$N\to\infty\$ where we find an infinite--dimensional representation of the braid group, which may give rise to an invariant of knots and links.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<19>) and #cite(<19>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `19`. ] <19>

