#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Equation Sample 6",
  author: "Dataset-expansion sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Equation Sample 6]

  #text(size: 1.2em)[Dataset-expansion sample]

]

         /* \maketitle */
== Derivation
 The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

 #math.equation(block: true, numbering: none)[
$  G_(c_(p)) &(b,c_(p)) \ & = - W^(- 1) phi(b) integral_(0)^(b) psi(z,0) frac(partial, partial c_(p)) pi_(1)(z,c_(p))m '(z)d z + psi(b,0)integral_(b)^(infinity) phi(z) frac(partial, partial c_(p)) pi_(1)(z,c_(p))m '(z)d z, \ G_(b c_(p)) &(b,c_(p)) \ & = - W^(- 1) phi '(b) integral_(0)^(b) psi(z,0) frac(partial, partial c_(p)) pi_(1)(z,c_(p))m '(z)d z + phi(b) psi(b,0) frac(partial, partial c_(p)) pi_(1)(b, c_(p)) m '(b) \ & #h()1 c m + psi '(b,0)integral_(b)^(infinity) phi(z) frac(partial, partial c_(p)) pi_(1)(z,c_(p))m '(z)d z - phi(b) psi(b,0) frac(partial, partial c_(p)) pi_(1)(b, c_(p)) m '(b) \ & = - W^(- 1) phi '(b) integral_(0)^(b) psi(z,0) frac(partial, partial c_(p)) pi_(1)(z,c_(p))m '(z)d z + psi '(b,0)integral_(b)^(infinity) phi(z) frac(partial, partial c_(p)) pi_(1)(z,c_(p))m '(z)d z .  $
]

