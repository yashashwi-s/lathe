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
$ frac(partial cal(V), partial phi) = inline 2/n frac(1,(cal(M)^(2)))thin cal(M)_(m n) frac(partial cal(V), partial cal(M)_(m n))thin,thin thin thin thin => cal(M)^(m n)cal(M)_(p q) frac(partial cal(V), partial cal(M)_(p q)) -(cal(M)^(2)) frac(partial cal(V), partial cal(M)_(m n)) = 0 thin .  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ integral D V exp(frac(,)integral d^(4)x epsilon.alt^(mu nu tau lambda)zws^(+)W_(mu nu)^(alpha beta)zws^(+)G_(tau lambda)^(sigma rho)zws epsilon_(alpha beta sigma rho)- frac(,)integral d^(4)x epsilon.alt^(mu nu tau lambda)zws^(-)W_(mu nu)^(alpha beta)zws^(-)G_(tau lambda)^(sigma rho)zws epsilon_(alpha beta sigma rho)).  $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ I = integral_(Sigma) d^(3) x sqrt(gamma)(R(gamma)- over(1, 2)((D U)^(2) - e^(- 2 U)(D V)^(2)) - over(1, 2)((D Phi)^(2) - e^(- 2 Phi)(D Psi)^(2)) -(D T)^(2) + e^(-(U + Phi))V(T))  $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ 2 frac(integral_(b = theta_(2))^(b = theta_(1))e^(frac(rho r s cos(b), 1 - rho^(2)))thin d b, 2 pi integral_(0)^(2 pi)e^(frac(rho r s cos a, 1 - rho^(2)))d a)<= 2 frac(integral_(b = 0)^(b = theta_(1)- theta_(2))e^(frac(rho r s cos(b), 1 - rho^(2)))thin d b, 2 pi integral_(0)^(2 pi)e^(frac(rho r s cos a, 1 - rho^(2)))d a)< frac(theta_(1)- theta_(2), 2 pi^(2)).  $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ frac(d, d lambda)S_(omega,upright(bold(c)))(Phi_(0)^(lambda))= -(sqrt(lambda)- 1)(2 L(Phi_(0))+ upright(bold(c)) dot upright(bold(P))(Phi_(0)))(lambda + frac(upright(bold(c)) dot upright(bold(P))(Phi_(0)), 2 L(Phi_(0))+ upright(bold(c)) dot upright(bold(P))(Phi_(0)))sqrt(lambda)+ frac(upright(bold(c)) dot upright(bold(P))(Phi_(0)), 2 L(Phi_(0))+ upright(bold(c)) dot upright(bold(P))(Phi_(0))))  $
]

