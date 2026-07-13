#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Aligned Mathematical Structures",
  author: "Source-backed grouped formula sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Aligned Mathematical Structures]

  #text(size: 1.2em)[Source-backed grouped formula sample]

]

         /* \maketitle */
== Expressions

===== Expression 1.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ _(j,j + i) = & sum^(M - j)_(m = i + 1) choose(M - j, m) bb(P)_()^(m)(1 - bb(P)_())^(M - j - m) \ & times frac(M - j - i, M - j)m ...(m - i + 1)bb(P)_(K)^(m) gamma_(i) gamma_(m,i) \ & + choose(M - j, i) bb(P)_()^(i)(1 - bb(P)_())^(M - j - i) frac(M - j - i, M - j)i ! bb(P)_(K)^(i)gamma_(i),  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$  Q(x) & = sum_(x /log x <= p <= x - sqrt()) pi(x - p) + O sum_(p <= x /log x) pi(x) + sum_(x - sqrt()<= p <= x) x \ & = sum_(x /log x <= p <= x - sqrt()) pi(x - p) + O pi(x) pi frac(log x,) + x sqrt() \ & = sum_(x /log x <= p <= x - sqrt()) pi(x - p) + O frac(x^(2), log^(3)x) .  $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$  partial_() u(, 0) - partial_() w(, 0) & <= partial_() u(, 0) - partial_() w(0, 0) +[ partial_() ]_(0,beta) | hat(xi) |^(beta) \ & =[ U_(beta)(1 + beta) cos((1 + beta) pi/2) +[ partial_() ]_(0,beta) ] | |^(beta),  $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ I I + I I I & -> 0 ; \ I V & = integral_(d(x,p)>= rho)(frac(rho^(2), 4 epsilon)- n)e^(- frac(rho^(2), 4 epsilon)- C) -> 0 ; \ I & = e^(- C)integral_(| y | <= frac(rho, sqrt(epsilon)))(frac(| y |^(2), 2)- n)(2 pi)^(- n /2) e^(- | y |^(2)/4)(1 + O(epsilon | y |^(2)) d y \ & -> integral_(RR^(n))(frac(| y |^(2), 2)- n)(2 pi)^(- n /2) e^(- | y |^(2)/4) d y = 0 .  $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ frac(omega(B),)bar.v.double(b - b_(B))f_(1)bar.v.double^(s)_(L^(s)_(omega))& = frac(omega(B),)integral_(5 B) | b(y)- b_(B)|^(s)| f |^(s)d omega(y) \ & <= frac(omega(B),)integral_(5 B) | b(y)- b_(B)|^(s s_(1)')d omega(y)^(frac(s_(1)',)) frac(omega(B),)integral_(5 B) | f |^(s s_(1)) d omega(y)^(frac(s_(1),)) \ & lt.tilde ell(B)^(beta s)bar.v.double b bar.v.double^(s)_(Lambda^(beta)) M^(s)_(s s_(1))(f)(x)  $
]

