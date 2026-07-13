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
$ cal(L)= 1/4(F_(mu nu)^(a))^(2)+ overline(psi)_(mu)^(i)[ D /^(i j)psi_(mu)^(j)- 1/2gamma_(alpha)D_(mu)^(i j)psi_(alpha)^(j)- 1/2gamma_(mu)D_(alpha)^(i j)psi_(alpha)^(j)+ 3/8gamma_(mu)D /^(i j)gamma_(alpha)psi_(alpha) ] .  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ cal(I)(delta) = inf_(lambda in RR^(2)_(+)) { chevron.l lambda, delta chevron.r + cal(I)^(star)(lambda) } = inf_(lambda in RR^(2)_(+)) { chevron.l lambda, delta chevron.r + sup_(gamma in Pi(mu_(1), mu_(2))) integral_(cal(V)) f_(lambda)(v) thin d gamma(v) }, $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$  phi.alt_(1)(x), choose(phi.alt_(2)(x), phi.alt_(3)(x)),choose(phi.alt_(4)(x), phi.alt_(5)(x)) -> c thin e splambda x phi.alt_(1)(x), U choose(e sp- lambda sp prime x phi.alt_(2)(x), e sp- lambda sp prime x phi.alt_(3)(x)),V choose(e splambda spprime prime x phi.alt_(4)(x), e splambda spprime prime x phi.alt_(5)(x))  $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ frac(partial L, partial w_(i j k l))(g_(i j),g_(i j,k),g_(i j,k l))= frac(partial x^(i), partial tilde(x)^(a))frac(partial x^(j), partial tilde(x)^(b))frac(partial x^(k), partial tilde(x)^(c))frac(partial x^(l), partial tilde(x)^(d))frac(partial L, partial w_(a b c d))(tilde(g)_(i j),tilde(g)_(i j,k),tilde(g)_(i j,k l)).  $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ q^(Q)product_(k = 1)^(Q - 1)frac(q z_(i)- z_(k), z_(i)- q z_(k)) = frac((z_(i)- i tau kappa lambda^(- 1/2)q^(1/2))(z_(i) + i kappa lambda^(1/2)q^(1/2)),(q^(1/2)z_(i)+ i tau kappa lambda^(- 1/2))(q^(1/2)z_(i)- i kappa lambda^(1/2))).  $
]

