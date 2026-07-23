#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Equation Sample 1",
  author: "Dataset-expansion sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Equation Sample 1]

  #text(size: 1.2em)[Dataset-expansion sample]

]

         /* \maketitle */
== Derivation
 The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

 #math.equation(block: true, numbering: none)[
$  alpha_(3) & limits(<=)^("(i)") sum_(s in cal(S),a in cal(A))d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho sqrt(frac(C_(sans(c l i p p e d))^(star)log N/delta, N min { d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho,frac(1, S(A + B)) })sans(V a r)_(P_(s,a,nu_(0)(s)))(V_(sans(p e))^(-)))nonumber \ & <= sqrt(frac(C_(sans(c l i p p e d))^(star)log N/delta, N))sum_(s in cal(S),a in cal(A))sqrt({d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho sans(V a r)_(P_(s,a,nu_(0)(s)))(V_(sans(p e))^(-))})nonumber \ & quad + sqrt(frac(C_(sans(c l i p p e d))^(star)S(A + B) log N/delta, N))sum_(s in cal(S),a in cal(A))sqrt({d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho})dot sqrt({d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho sans(V a r)_(P_(s,a,nu_(0)(s)))(V_(sans(p e))^(-))})nonumber \ & limits(<=)^("(ii)") sqrt(frac(C_(sans(c l i p p e d))^(star), N)log N/delta)dot sqrt(S A)dot sqrt({sum_(s in cal(S),a in cal(A))d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho sans(V a r)_(P_(s,a,nu_(0)(s)))(V_(sans(p e))^(-))})nonumber \ & quad + sqrt(frac(C_(sans(c l i p p e d))^(star)S(A + B) log N/delta, N))[ sum_(s in cal(S),a in cal(A))d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho ] sqrt({sum_(s in cal(S),a in cal(A))d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho sans(V a r)_(P_(s,a,nu_(0)(s)))(V_(sans(p e))^(-))})nonumber \ & <= 2 sqrt(frac(C_(sans(c l i p p e d))^(star)S(A + B) log N/delta, N))sqrt({sum_(s in cal(S),a in cal(A))d^(mu^(star),nu_(0))s,a,nu_(0)(s);rho sans(V a r)_(P_(s,a,nu_(0)(s)))(V_(sans(p e))^(-))})nonumber \ & limits(=)^("(iii)") 2 sqrt(frac(C_(sans(c l i p p e d))^(star)S(A + B), N)log N/delta)sqrt(sum_(s in cal(S))d^(mu^(star),nu_(0))(s ;rho) limits(class("large", bb(E)))_(a tilde mu^(star)(s),b tilde nu_(0)(s))[ sans(V a r)_(P_(s,a,b))(V_(sans(p e))^(-)) ])nonumber \ & limits(<=)^("(iv)") 2 sqrt(frac(C_(sans(c l i p p e d))^(star)S(A + B), N)log N/delta)sqrt(sum_(s in cal(S))d^(mu^(star),nu_(0))(s ;rho) sans(V a r)_(P_(s)^(mu^(star),nu_(0)))(V_(sans(p e))^(-))).  $
]

