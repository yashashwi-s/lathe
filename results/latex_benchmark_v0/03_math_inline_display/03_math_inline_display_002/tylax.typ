#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Inline and Display Mathematics",
  author: "Source-backed grouped formula sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Inline and Display Mathematics]

  #text(size: 1.2em)[Source-backed grouped formula sample]

]

         /* \maketitle */
== Expressions

===== Expression 1.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ cal(I)_(upright(D))(delta) = sup_(pi in Pi(mu_(1), mu_(2))) inf_(lambda in RR_(+)^(2))[ chevron.l lambda, delta chevron.r + integral_(cal(V)) g_(lambda) thin d pi ] = inf_(lambda in RR_(+)^(2)) sup_(pi in Pi(mu_(1), mu_(2)))[ chevron.l lambda, delta chevron.r + integral_(cal(V)) g_(lambda) thin d pi ] .  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ upright(R)_(upright(D))(lambda, delta) = chevron.l lambda, delta chevron.r + sup_(x^(prime) in RR^(d))[ sum_(1 <= ell <= 2) phi_(ell)(x^(prime), lambda_(ell)) ] upright(R)_(upright(D))(lambda, delta) = chevron.l lambda, delta chevron.r + sum_(1 <= ell <= 2) sup_(x^(prime) in RR^(d))phi_(ell)(x^(prime), lambda_(ell)).  $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ (zws^(c)D_(-)^(alpha,alpha ',beta,beta ',gamma)t^(- rho))(x)= frac(Gamma(beta '+ rho + m) Gamma(- alpha - alpha '+ gamma + rho) Gamma(- alpha '- beta + gamma + rho + m), Gamma(rho) Gamma(- alpha '+ beta '+ rho + m) Gamma(- alpha - alpha '- beta + gamma + rho + m))x^(alpha + alpha '- gamma - rho).  $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ cal(I)_(upright(D))(delta_(1), 0) = sup_(pi in Pi(mu_(1), mu_(2))) inf_(lambda_(1) in RR_(+))[ lambda_(1) delta_(1) + integral g_(lambda, 1) thin d pi ] = sup_(pi in Pi(mu_(1), mu_(2))) inf_(lambda in RR^(2)_(+))[ chevron.l lambda,(delta_(1), 0) chevron.r + integral_(cal(V)) g_(lambda) thin d pi ] .  $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ [^(2)^(0)^(1)partial_(theta.alt)+ frac(^(3)^(0)^(1), sin theta.alt)partial_(phi)+^(2)^(0)^(1)S partial_(theta.alt) S^(- 1)+ frac(^(3)^(0)^(1), sin theta.alt)S partial_(phi) S^(- 1) ] = - i kappa  $
]

