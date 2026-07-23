#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Equation Sample 4",
  author: "Dataset-expansion sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Equation Sample 4]

  #text(size: 1.2em)[Dataset-expansion sample]

]

         /* \maketitle */
== Derivation
 The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

 #math.equation(block: true, numbering: none)[
$  mat(delim: #none, | | f | |_(1_(mu))+ | | g | |_(1_(mu)), = limits(integral)_(x in cal(D)) | f(x)| + | g(x)| d mu(x) ;, = + limits(integral)_(x in cal(D) ;f(x)>= 0,g(x)>= 0,) f(x)+ g(x) d mu(x) - limits(integral)_(x in cal(D) ;f(x)< 0,g(x)< 0,) f(x)+ g(x) d mu(x) ;, quad + limits(integral)_(x in cal(D) ;f(x)>= 0,g(x)< 0,) f(x)- g(x) d mu(x) + limits(integral)_(x in cal(D) ;f(x)< 0,g(x)>= 0,) g(x)- f(x) d mu(x) ;, = + limits(integral)_(x in cal(D) ;f(x)>= 0,g(x)>= 0,) max(f(x),g(x))+ min(f(x),g(x)) d mu(x) ;, quad - limits(integral)_(x in cal(D) ;f(x)< 0,g(x)< 0,) max(f(x),g(x))+ min(f(x),g(x)) d mu(x) ;, quad + limits(integral)_(x in cal(D) ;f(x)>= 0,g(x)< 0,) max(f(x),g(x))- min(f(x),g(x)) d mu(x) ;, quad + limits(integral)_(x in cal(D) ;f(x)< 0,g(x)>= 0,) max(f(x),g(x))- min(f(x),g(x)) d mu(x). ;)  $
]

