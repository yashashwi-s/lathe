#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Non-Perturbative 2D Quantum Gravity, Again",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Non-Perturbative 2D Quantum Gravity, Again]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   This is a talk given by S.D. at the the workshop on Random Surfaces and 2D Quantum Gravity, Barcelona 10-14 June 1991. It is an updated review of recent work done by the authors on a proposal for non-perturbatively stable 2D quantum gravity coupled to c<1 matter, based on the flows of the (generalised) KdV hierarchy.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<us1>) and #cite(<us2>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `us1`. ] <us1>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `us2`. ] <us2>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `gm`. ] <gm>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `dooglass`. ] <dooglass>

