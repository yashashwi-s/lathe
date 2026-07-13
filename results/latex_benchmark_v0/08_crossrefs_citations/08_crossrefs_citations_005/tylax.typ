#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Correlation functions in super Liouville theory",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Correlation functions in super Liouville theory]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We calculate three- and four-point functions in super Liouville theory coupled to super Coulomb gas on world sheets with spherical topology. We first integrate over the zero mode and assume that a parameter takes an integer value. After calculating the amplitudes, we formally continue the parameter to an arbitrary real number. Remarkably the result is completely parallel to the bosonic case, the amplitudes being of the same form as those of the bosonic case.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<11>) and #cite(<12>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `11`. ] <11>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `12`. ] <12>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `13`. ] <13>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `10`. ] <10>

