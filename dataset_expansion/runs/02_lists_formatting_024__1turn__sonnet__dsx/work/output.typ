#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true)

#align(center)[
  #text(size: 17pt, weight: "bold")[Path Integrals and Voronin's Theorem on the Universality of the Riemann Zeta Function]
  #v(0.5em)
  #text(size: 12pt)[Source-backed arXiv sample]
]

#v(1em)

= Extracted Lists

The list environments below are extracted from arXiv LaTeX source and wrapped for pdfLaTeX validation.

#let custom-list(items) = {
  for (label, body) in items {
    grid(
      columns: (2em, 1fr),
      gutter: 0pt,
      align(top)[#label],
      align(top)[#body],
    )
    v(0.4em)
  }
}

#custom-list((
  [(i)],
  [The calculations we have carried out demonstrate the validity of the expressions for the partition function in Euclidean quantum mechanics.  This includes the validity of the factorization conjecture for the density $rho_nu (n)$.],
  [(ii)],
  [The applications of our method could either be for actual numerical calculations or for obtaining formal results.   It may also be used for a complex actions.],
  [(iii)],
  [The continuous form of Voronin's theorem, leads us to contemplate a far reaching conjecture.  This concerns taking the limit $a arrow.r 0$, where $a$ is the lattice spacing.  If in this limit a measure, $rho_infinity (n)$, exists, then essentially any quantum mechanical problem can be reduced to quadratures.],
))

#v(0.6em)

#custom-list((
  [(i)],
  [The calculations we have carried out demonstrate the validity of the expressions for the partition function in Euclidean quantum mechanics.  This includes the validity of the factorization conjecture for the density $rho_nu (n)$.],
  [(ii)],
  [The applications of our method could either be for actual numerical calculations or for obtaining formal results.  On the computational side, it is clear that one has to look for a fast algorithm to pick those integers, $n$, for which the path $gamma_sigma (j;n)$ makes an important contribution to quantum averages.  The hope is to get a variant of the Monte Carlo method that, in some cases, could be more efficient; and that also could be used for a complex action.],
  [(iii)],
  [The continuous form of Voronin's theorem, leads us to contemplate a far reaching conjecture.  This concerns taking the limit $a arrow.r 0$, where $a$ is the lattice spacing.  If in this limit a measure, $rho_infinity (n)$, exists, then essentially any quantum mechanical problem can be reduced to quadratures.],
))
