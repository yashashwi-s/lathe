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
$  mat(delim: #none, "\rm minimize", C dot U hat(X) U^(T) ; "\rm subject to", A_(i) dot U hat(X) U^(T) = b_(i) thick thick forall i in {1,...,m } ;, hat(X) in bb(S)^(d)_(+)) mat(delim: #none, "\rm maximize", b^(T)y ; "\rm subject to", U^(T)(C - sum^(m)_(i = 1) y_(i) A_(i)) U in bb(S)^(d)_(+), ; ;)  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ q dot N_(d)& = sum_(x,y,z in bb(F)_(q))theta(z E_(d)(x,y)) \ & = q^(2)+ sum_(z in bb(F)_(q)^(times))theta(z b)+ sum_(y,z in bb(F)_(q)^(times))theta(b z)theta(- z y^(2))+ sum_(x,z in bb(F)_(q)^(times))theta(z x^(d))theta(z a x)theta(z b) \ & + sum_(x,y,z in bb(F)_(q)^(times))theta(x^(d)z)theta(a x z)theta(b z)theta(- z y^(2)) \ & = q^(2)+ A + B + C + D .  $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ M = frac(1, sqrt(1 + ** dot ** - over(1, 4)(**times **)^(2)))mat(delim: "(", 1 - over(i, 2)(** times **)dot **, - ** dot **;b e g i n a l i g n *2 e x ]** dot **, 1 + over(i, 2)(** times **)dot **)  $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ U(arrow(a),1)(S, f_(alpha) times.circle rho(E^(alpha))) : = & e^(- i[hat(f)_(0)dot hat(H)(arrow(a), rho) + hat(f)_(1)dot hat(P)(arrow(a),rho)])(S + arrow(a), f_(alpha)(dot - arrow(a)) times.circle rho(E^(alpha))) \ = & e^(i[a^(0) hat(H)(rho) - a^(1)hat(P)(rho)])(S + arrow(a), f_(alpha)(dot - arrow(a)) times.circle rho(E^(alpha))) .  $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ I_(1) & =(- infinity, omega_(xi)^(ast) - frac(alpha xi^(alpha), 2(1 - alpha))], \ I_(2) & =[omega_(xi)^(ast) - frac(alpha xi^(alpha), 2(1 - alpha)), omega_(xi)^(ast) + frac(alpha xi^(alpha), 2(1 - alpha))], \ I_(3) & =[omega_(xi)^(ast) + frac(alpha xi^(alpha), 2(1 - alpha)), 0 ], "and" \ I_(4) & =[0, infinity).  $
]

