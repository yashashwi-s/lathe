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
$ mat(delim: #none, display Delta_(plus.minus), = display frac(c, 2 4)plus.minus(I^(plus.minus)_(H)- 2 I^(plus.minus)_(S)- I^(plus.minus)_(C)- I^(plus.minus)_(W)) + display frac(1, 2 pi)Sigma_(plus.minus);, minus.plus display frac(1, 2 pi)display limits(integral)^(infinity)_(- infinity)display frac(d x, 2 pi)phi^(,)_(plus.minus)(x)cal(Q)_(plus.minus)(x)med,)  $
]

===== Expression 2.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ & floor.l frac(- 2 m p^(i), q - 1)floor.r + floor.l frac(m d p^(i), q - 1)floor.r + floor.l frac(- m(d - 1)p^(i), q - 1)floor.r - floor.l frac(- m p^(i), q - 1)floor.r + 1 \ & = sum_(h = 1)^(d - 2)floor.l chevron.l frac(h p^(i), d - 1)chevron.r - frac(m p^(i), q - 1)floor.r + floor.l chevron.l frac(p^(i), 2)chevron.r - frac(m p^(i), q - 1)floor.r + sum_(h = 1)^(d - 1)floor.l chevron.l frac(- h p^(i), d)chevron.r + frac(m p^(i), q - 1)floor.r .  $
]

===== Expression 3.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ mat(delim: #none, upright(bold(E))(upright(bold(x)),t) = display frac(1, 4 pi)integral rho_(e)(upright(bold(x)) ',t - r)frac(upright(bold(r)), r^(3))thin d^(3)x ';space.nobreak ;+ display frac(1, 4 pi)integral upright(bold(J))_(m)(upright(bold(x)) ',t - r)thin **thin frac(upright(bold(r)), r^(3))thin d^(3)x '- display frac(1, 4 pi)integral 1/rfrac(partial upright(bold(J))_(m)(upright(bold(x)) ',t - r), partial t)thin d^(3)x ',)  $
]

===== Expression 4.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ Gamma^(5)= mat(delim: "(", 0, 1_(2) ; 1_(2), 0) ;quad Gamma^(i)= mat(delim: "(", 0, sigma^(i) ; - sigma^(i), 0) ;quad Gamma^(0)= mat(delim: "(", 1_(2), 0 ; 0, - 1_(2)) ;quad Gamma^(4)= - i Gamma^(5)= mat(delim: "(", 0, i_(2) ; i_(2), 0) .  $
]

===== Expression 5.
 The following expression is taken from a source-backed formula corpus.

 #math.equation(block: true, numbering: none)[
$ overline(omega)^(m)(frac(b^(d - 1)d^(d), a^(d)(d - 1)^(d - 1))) product_(i = 0)^(r - 1)product_(h = 1)^(d - 2)frac(Gamma_(p)(chevron.l(frac(h, d - 1)- frac(m, q - 1))p^(i)chevron.r), Gamma_(p)(chevron.l frac(h p^(i), d - 1)chevron.r))product_(h = 1 \ h != d/2)^(d - 1)frac(Gamma_(p)(chevron.l(h/d+ frac(m, q - 1))p^(i)chevron.r), Gamma_(p)(chevron.l frac(h p^(i), d)chevron.r))= 1 .  $
]

