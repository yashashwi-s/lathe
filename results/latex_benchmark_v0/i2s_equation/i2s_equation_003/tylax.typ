#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Equation Sample 3",
  author: "Dataset-expansion sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Equation Sample 3]

  #text(size: 1.2em)[Dataset-expansion sample]

]

         /* \maketitle */
== Derivation
 The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

 #math.equation(block: true, numbering: none)[
$  & E_(p(tilde(x)))[lr(< G N N_(theta)(tilde(x)),nabla_(tilde(x)) log p(tilde(x)) >) ] \ = & integral_(tilde(x)) p(tilde(x)) lr(< G N N_(theta)(tilde(x)),nabla_(tilde(x)) log p(tilde(x)) >) dif tilde(x) \ = & integral_(tilde(x)) p(tilde(x)) lr(< G N N_(theta)(tilde(x)),frac(nabla_(tilde(x)) p(tilde(x)), p(tilde(x))) >) dif tilde(x) \ = & integral_(tilde(x)) lr(< G N N_(theta)(tilde(x)),nabla_(tilde(x)) p(tilde(x)) >) dif tilde(x) \ = & integral_(tilde(x)) lr(< G N N_(theta)(tilde(x)),nabla_(tilde(x))(integral_(x) p(tilde(x) | x)p(x) dif x) >) dif tilde(x) \ = & integral_(tilde(x)) lr(< G N N_(theta)(tilde(x)), integral_(x) p(x) nabla_(tilde(x)) p(tilde(x) | x) dif x >) dif tilde(x) \ = & integral_(tilde(x)) lr(< G N N_(theta)(tilde(x)), integral_(x) p(tilde(x) | x) p(x) nabla_(tilde(x))log p(tilde(x) | x) dif x >) dif tilde(x) \ = & integral_(tilde(x)) integral_(x) p(tilde(x) | x) p(x) lr(< G N N_(theta)(tilde(x)), nabla_(tilde(x))log p(tilde(x) | x) >) dif x dif tilde(x) \ = & E_(p(tilde(x),x))[ lr(< G N N_(theta)(tilde(x)), nabla_(tilde(x))log p(tilde(x) | x) >) ] \  $
]

