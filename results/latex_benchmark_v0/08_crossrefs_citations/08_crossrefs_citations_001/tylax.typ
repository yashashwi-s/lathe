#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Exact Black String Solutions in Three Dimensions",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Exact Black String Solutions in Three Dimensions]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   A family of exact conformal field theories is constructed which describe charged black strings in three dimensions. Unlike previous charged black hole or extended black hole solutions in string theory, the low energy spacetime metric has a regular inner horizon (in addition to the event horizon) and a timelike singularity. As the charge to mass ratio approaches unity, the event horizon remains but the singularity disappears.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<19>) and #cite(<Horowitz>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `19`. ] <19>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `Horowitz`. ] <Horowitz>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `Witten`. ] <Witten>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `Gawedzki`. ] <Gawedzki>

