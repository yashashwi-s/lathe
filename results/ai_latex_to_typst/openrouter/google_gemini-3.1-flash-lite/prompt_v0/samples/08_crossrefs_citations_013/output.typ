#set page(margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center, [
  #text(size: 1.5em, weight: "bold")[On quantum group symmetries of conformal field theories]
  #v(1em)
  Source-backed arXiv sample
  #v(1em)
])

#block(inset: (x: 2em))[
  *Abstract*\
  The appearance of quantum groups in conformal field theories is traced back to the Poisson-Lie symmetries of the classical chiral theory. A geometric quantization of the classical theory deforms the Poisson-Lie symmetries to the quantum group ones. This elucidates the fundamental role of chiral symmetries that quantum groups play in conformal models. As a byproduct, one obtains a more geometric approach to the representation theory of quantum groups.
]

= References And Citations
<sec:refs>

This sample cites source keys [1] and [2]. Section @sec:refs and Equation @eq:source-demo provide cross-reference coverage.

$ a^2 + b^2 = c^2 $ <eq:source-demo>

#v(2em)
#text(weight: "bold")[References]
#v(1em)

#let bib(key, content) = [#box(width: 2em)[#key] #content #parbreak()]

#bib("[1]", [Source bibliography entry 1 extracted from arXiv metadata/source key `10`.])
#bib("[2]", [Source bibliography entry 2 extracted from arXiv metadata/source key `11`.])
#bib("[3]", [Source bibliography entry 3 extracted from arXiv metadata/source key `12`.])
#bib("[4]", [Source bibliography entry 4 extracted from arXiv metadata/source key `13`.])
