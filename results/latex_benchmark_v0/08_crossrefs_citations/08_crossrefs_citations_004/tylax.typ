#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "String Theory and the Donaldson Polynomial",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[String Theory and the Donaldson Polynomial]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   It is shown that the scattering of spacetime axions with fivebrane solitons of heterotic string theory at zero momentum is proportional to the Donaldson polynomial.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<teinep>) and #cite(<STR.55>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `teinep`. ] <teinep>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `STR.55`. ] <STR.55>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `strb`. ] <strb>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `donref`. ] <donref>

