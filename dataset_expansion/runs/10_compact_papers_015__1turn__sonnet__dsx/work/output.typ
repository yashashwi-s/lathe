#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true)

#let title = "Loop Equations and the Topological Phase of Multi-Cut Matrix Models"
#let authors = "C. Crnkovic, M. Douglas, G. Moore"

#align(center)[
  #v(1em)
  #text(size: 14pt, weight: "bold")[#title]
  #v(0.8em)
  #text(size: 11pt)[#authors]
  #v(1.2em)
]

#block(inset: (left: 0.5in, right: 0.5in))[
  #text(size: 10pt)[
    *Abstract*

    We study the double scaling limit of mKdV type, realized in the two-cut Hermitian matrix model. Building on the work of Periwal and Shevitz and of Nappi, we find an exact solution including all odd scaling operators, in terms of a hierarchy of flows of $2 times 2$ matrices. We derive from it loop equations which can be expressed as Virasoro constraints on the partition function. We discover a "pure topological" phase of the theory in which all correlation functions are determined by recursion relations. We also examine macroscopic loop amplitudes, which suggest a relation to 2D gravity coupled to dense polymers.
  ]
]

#v(1em)

= Introduction

We study the double scaling limit of mKdV type, realized in the two-cut Hermitian matrix model. Building on the work of Periwal and Shevitz and of Nappi, we find an exact solution including all odd scaling operators, in terms of a hierarchy of flows of math expression matrices. We derive from it loop equations which can be expressed as Virasoro constraints on the partition function. We discover a "pure topological" phase of the theory in which all correlation functions are determined by recursion relations. We also examine macroscopic loop amplitudes, which suggest a relation to 2D gravity coupled to dense polymers. math expression (crnkovic\@yalphy.hepnet, or \ \@yalehep.bitnet), Address after Sept. 1991: CERN, Theory Division, CH-1211, Geneva 23, Switzerland. On leave of absence from Institute "Ruder Bo skovi\'c ," Zagreb, Yugoslavia. math expression (mrd\@ruhets.rutgers.edu) math expression (moore\@yalphy.hepnet, or \ \@yalehep.bitnet)

= Method

where math expression , math expression , and math expression are matrices satisfying math expression . Finally, redefining math expression we obtain (dropping tilde from math expression ) math expression = 4(D+q) \_3 A . math expression We will need the resolvent math expression R 1 (D+q) \_3 - 4 . math expression In their work on the resolvents of matrix differential operators \ Gelfand and Dikii show that math expression satisfies

$ L(theta) = sum_(i=1)^(n) ell(x_i, theta) $ <eq:compact>

Equation~@eq:compact is included to keep the sample paper-like while remaining small.

= Conclusion

and that it has an asymptotic expansion math expression R(x, ) = \_ k=0 ^ R\_k ^ -k . math expression From \ it is clear that, up to constants, the most general expansion of math expression is \_3 R = \_ k=0 ^ \_ k-1 ^ -k , where math expression . Plugging \ into \ results in the recursion relations determining math expression , math expression , math expression . Setting math expression , math expression , we obtain
