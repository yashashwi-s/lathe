#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Classical Gravity Coupled to Liouville Theory",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Classical Gravity Coupled to Liouville Theory]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We consider the two dimensional Jackiw-Teitelboim model of gravity. We first couple the model to the Liouville action and \$c\$ scalar fields and show, treating the combined system as a non linear sigma model, that the resulting theory can be interpreted as a critical string moving in a target space of dimension \$D=c+2\$. We then analyse perturbatively a generalised model containing a kinetic term and an arbitrary potential for the auxiliary field. We use the background field method and work with covariant gauges. We show that the renormalisability of the theory depends on the form of the potential. For a general potential, the theory can be renormalised as a non linear sigma model. In the particular case of a Liouville-like potential, the theory is renormalisable in the usual sense.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<any>) and #cite(<any>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `any`. ] <any>

