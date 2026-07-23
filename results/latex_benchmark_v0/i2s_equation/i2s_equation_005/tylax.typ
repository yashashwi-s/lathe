#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Equation Sample 5",
  author: "Dataset-expansion sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Equation Sample 5]

  #text(size: 1.2em)[Dataset-expansion sample]

]

         /* \maketitle */
== Derivation
 The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

 #math.equation(block: true, numbering: none)[
$  v_(m n)^(x) & = chevron.l m | v^(x)| n chevron.r \ & = delta_(m n)chevron.l v^(x)chevron.r(frac(k_(x), rho))(- delta_(m,0)+ delta_(m,1)) +(1 - delta_(m n))chevron.l v^(x)chevron.r(frac(k_(z), rho)frac(k_(x), sqrt(k_(x)^(2)+ k_(y)^(2)))- i frac(k_(y), sqrt(k_(x)^(2)+ k_(y)^(2)))) \ & = delta_(m n)chevron.l v^(x)chevron.r(theta phi.alt)(- delta_(m,0)+ delta_(m,1)) +(1 - delta_(m n))chevron.l v^(x)chevron.r(theta phi.alt - i phi.alt), \ v_(m n)^(y) & = delta_(m n)chevron.l v^(y)chevron.r(theta phi.alt)(- delta_(m,0)+ delta_(m,1)) +(1 - delta_(m n))chevron.l v^(y)chevron.r(theta phi.alt - i phi.alt), \ v_(m n)^(z) & = delta_(m n)chevron.l v^(z)chevron.r theta(- delta_(m,0)+ delta_(m,1)) +(1 - delta_(m n))chevron.l v^(z)chevron.r frac(- theta, rho), \  $
]

