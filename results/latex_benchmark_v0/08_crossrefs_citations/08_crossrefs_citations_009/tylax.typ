#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Effective Superstrings",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Effective Superstrings]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We generalize the method of quantizing effective strings proposed by Polchinski and Strominger to superstrings. The Ramond-Neveu-Schwarz string is different from the Green-Schwarz string in non-critical dimensions. Both are anomaly-free and Poincare invariant. Some implications of the results are discussed. The formal analogy with 4D (super)gravity is pointed out.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<pol>) and #cite(<div>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `pol`. ] <pol>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `div`. ] <div>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `hughes`. ] <hughes>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `gs`. ] <gs>

