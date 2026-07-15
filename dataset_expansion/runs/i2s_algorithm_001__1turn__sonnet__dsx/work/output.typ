#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: false)

#show math.equation: set text(font: "New Computer Modern Math")

#align(center)[
  #v(0.5em)
  #text(size: 17pt, weight: "bold")[Algorithm Sample 1]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Procedure

The pseudocode below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#set enum(numbering: "1.", indent: 0pt)

#block(inset: (left: 0pt))[
#enum(
  [For $beta in (1, 3/2)$ set $epsilon = 3/2 - beta$ and $T = L^(2(1-epsilon))$. For $i=1,dots,d$, solve for the approximate first-order corrector $phi_(i,T)^((L))$:
  $ 1/T phi_(i,T)^((L)) - nabla dot.op a nabla phi_(i,T)^((L)) = nabla dot.op a e_i quad "in " Q_(2L), #h(0.3in) phi_(i,T)^((L)) = 0 quad "on " partial Q_(2L). $
  ],
  [Calculate the approximate homogenized coefficients via
  $ a_h^((L)) e_i = integral omega q_(i,T)^((L)), $
  where
  $ q_(i,T)^((L)) := a(e_i + nabla phi_(i,T)^((L))) $
  and $omega(x) = 1/L^d hat(omega)(x/L)$ with $hat(omega)$ as in Theorem~1.
  ],
  [Find $tilde(u)_h^((L))$ on $partial Q_L$:
  $ tilde(u)_h^((L)) = integral G_h^((L)) * (nabla dot.op g), $
  where $G_h^((L))(x) := 1/(4pi |(a_h^((L)))^(-1\/2) x|)$ is the Green function for the constant-coefficient operator $-nabla dot.op a_h^((L)) nabla$.
  ],
  [Solve for approximate first-order flux correctors $sigma_(i,T)^((L)) = {sigma_(i j k,T)^((L))}_(j,k)$:
  $ 1/T sigma_(i j k,T)^((L)) - Delta sigma_(i j k,T)^((L)) = partial_j q_(i k,T)^((L)) - partial_k q_(i j,T)^((L)) quad "in " Q_(7/4 L), #h(0.3in) sigma_(i j k,T)^((L)) = 0 quad "on " partial Q_(7/4 L). $
  ],
  [Solve for approximate second-order correctors $psi_(i j,T)^((L))$:
  $ 1/T psi_(i j,T)^((L)) - nabla dot.op a nabla psi_(i j,T)^((L)) = nabla dot.op (phi_(i,T)^((L)) a - sigma_(i,T)^((L))) e_j quad "in " Q_(3/2 L), #h(0.3in) psi_(i j,T)^((L)) = 0 quad "on " partial Q_(3/2 L). $
  ],
  [For the indices
  $ (i,j) in cal(J) = {(1,2),(1,3),(2,3),(2,2),(3,3)}, $
  calculate
  $ c_(i j,T)^((L)) = -integral g dot.op nabla lr((sum_(k=1)^3 phi_(k,T)^((L)) partial_k v_(h,i j)^((L)) + (2-delta_(i j))(psi_(i j,T)^((L)) - a_(h i j)^((L))/a_(h 1 1)^((L)) psi_(1 1,T)^((L)))), ) $
  where $v_(h,i j)^((L))$ denote the $a_h^((L))$-harmonic polynomials
  $ v_(h,i j)^((L)) = (1 - 1/2 delta_(i j))(x_i x_j - a_(h i j)^((L))/a_(h 1 1)^((L)) x_1^2). $
  ],
  [Obtain $u_h^((L))$ as
  $ u_h^((L)) = tilde(u)_h^((L)) + sum_(i=1)^3 (integral g dot.op nabla phi_(i,T)^((L))) partial_i G_h^((L)) + sum_((i,j) in cal(J)) c_(i j,T)^((L)) partial_(i j) G_h^((L)). $
  ],
  [Solve for $u^((L))$ (here and for the rest of the paper we adopt Einstein's summation convention for repeated indices):
  $ -nabla dot.op a nabla u^((L)) = nabla dot.op g quad "in " Q_L, #h(0.3in) u^((L)) = (1 + phi_(i,T)^((L)) partial_i + psi_(i j,T)^((L)) partial_(i j)) u_h^((L)) quad "on " partial Q_L. $
  ],
)
]
