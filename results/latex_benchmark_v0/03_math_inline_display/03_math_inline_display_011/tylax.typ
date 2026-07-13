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
$ cal(I)_(upright(D))^(star)(lambda) = sup_(gamma in cal(P)_(upright(D))) I_(upright(D), lambda)[gamma ] = sup_(pi in Gamma(Pi, phi_(lambda))) integral_(cal(V) times cal(V)) phi_(lambda) thin d pi = sup_(pi in Pi(mu_(1), ..., mu_(L))) integral_(cal(V)) thin g_(lambda) d pi .  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ G_(mu nu)^((p)) = eta_(mu nu) + partial_(mu) phi.alt^(i)partial_(nu) phi.alt^(i) -(Gamma_(mu)+ Gamma_(i) partial_(mu) phi.alt^(i))partial_(nu) lambda -(Gamma_(nu)+ Gamma_(i) partial_(nu) phi.alt^(i))partial_(mu) lambda + Gamma^(m) partial_(mu) lambda Gamma_(m) partial_(nu) lambda, $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ (frac((Delta_(v)),(Delta^((0))_(v))))^(- 1/2)(frac((Delta_(A)),(Delta^((0))_(A))))^(- 1)(frac((Delta_(c)),(Delta^((0))_(c))))^(+ 1) =(frac((Delta_(-)),(Delta^((0)))))^(- 1) $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ lr(chevron.l alpha_(1),alpha_(2),. . .,alpha_(2 N),t bar.v) U_(L)lr(bar.v alpha_(1)',alpha_(2)',. . .,alpha_(2 N)',t chevron.r) = R^(alpha_(2)'alpha_(3)')_(alpha_(1)alpha_(2))med R^(alpha_(4)'alpha_(5)')_(alpha_(3)alpha_(4))med . . . med R^(alpha_(2 N)'alpha_(1)')_(alpha_(2 N - 1)alpha_(2 N)) $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ P^(-)= 1/2integral d x^(-)d^(2)x^(perp):[ - phi.alt partial^(perp 2)phi.alt + sum_(i = 1)^(2)(_(m)^((i))frac(- partial^(perp 2)+ m^(2), i partial^(+))gamma^(+)psi_(m)^((i))+ 2 g phi.alt_(m)^((i)) psi_(m)^((i)) + g^(2)_(m)^((i))phi.alt frac(gamma^(+), i partial^(+))phi.alt psi_(m)^((i))) ] : thick .  $
]

