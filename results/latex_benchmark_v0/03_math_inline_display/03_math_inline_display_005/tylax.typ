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
$ integral_(Omega) frac(partial d_(epsilon)(t), partial x_(i)),frac(partial d_(epsilon)(t), partial x_(j)) frac(partial Y^(i), partial x_(j))- frac(,)| nabla d_(epsilon)(t)|^(2)+ frac(1, 4 epsilon^(2))(1 - | d_(epsilon)(t)|^(2))^(2)upright(div) Y + tau_(epsilon)(t), Y dot nabla d_(epsilon)(t) = 0 .  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ abs(sum_(alpha beta gamma delta)chevron.l Phi_(alpha) Phi_(beta) Phi_(gamma) Phi_(delta) chevron.r_(c)lr(/) sum_(alpha beta gamma delta)chevron.l Phi_(alpha) Phi_(beta) Phi_(gamma) Phi_(delta) chevron.r) = abs(chevron.l Phi^(4)(x) chevron.r_(c) lr(/) chevron.l Phi^(4)(x) chevron.r) thick(n = 4) thick, $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ integral_(0)^(R)r thin[ u_(1 epsilon kappa)(r) u_(1 epsilon 'kappa)(r) + u_(2 epsilon kappa)(r) u_(2 epsilon 'kappa)(r) ] = frac(u_(1 epsilon kappa)(R) u_(2 epsilon 'kappa)(R) - u_(1 epsilon 'kappa)(R) u_(2 epsilon kappa)(R), epsilon - epsilon ')thin .  $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ overline(cal(G))_(())^((rho) a)Gamma^((rho))= Delta_(())^((rho) a)+ O(rho^(2)) thin thin,thick thick thick overline(cal(G))_(())^((rho) a)Gamma^((rho))= Delta_(())^((rho) a)+ O(rho^(2)) thin thin,  $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ Z[ J^(mu),overline(eta),eta ] = integral[ d A_(mu) ] Im(A_(mu)) exp(- lr(chevron.l frac(,)F_(mu nu)F^(mu nu) chevron.r) + lr(chevron.l J^(mu) A_(mu) chevron.r) + lr(chevron.l overline(eta)^(prime)(i gamma^(mu) partial_(mu))^(- 1)eta^(prime) chevron.r)), $
]

