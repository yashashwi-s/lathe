#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "The renormalization group flow in 2D N=2 SUSY Landau-Ginsburg models",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[The renormalization group flow in 2D N=2 SUSY Landau-Ginsburg models]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We investigate the renormalization of N=2 SUSY L-G models with central charge \$c=3p/(2+p)\$ perturbed by an almost marginal chiral operator. We calculate the renormalization of the chiral fields up to \$gg{^\*}\$ order and of nonchiral fields up to \$g(g^{\*})\$ order. We propose a formulation of the nonrenormalization theorem and show that it holds in the lowest nontrivial order. It turns out that, in this approximation, the chiral fields can not get renormalized \$\Phi^{k}=\Phi^{k}\_{0}\$. The \$\beta\$ function then remains unchanged \$\beta=\epsilon gr\$.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<rg:fl1>) and #cite(<rg:fl2>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `rg:fl1`. ] <rg-fl1>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `rg:fl2`. ] <rg-fl2>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `rg:fl3`. ] <rg-fl3>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `rg:fl4`. ] <rg-fl4>

