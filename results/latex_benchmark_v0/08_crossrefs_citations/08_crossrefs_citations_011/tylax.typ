#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Is S=1 for c=1?",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Is S=1 for c=1?]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   The \$c=1\$ string in the Liouville field theory approach is shown to possess a nontrivial tree-level \$S\$-matrix which satisfies factorization property implied by unitary, if all the extra massive physical states are included.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<sb>) and #cite(<joe>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `sb`. ] <sb>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `joe`. ] <joe>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `gros`. ] <gros>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `pol`. ] <pol>

