#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#show math.equation: set text(font: "New Computer Modern Math")

#align(center)[
  #text(size: 17pt, weight: "bold")[Equation Sample 1]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1.5em)
]

= Derivation

The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#set math.equation(numbering: none)

$
alpha_3 &overset((i))(lt.eq) sum_(s in cal(S), a in cal(A)) d^(mu^star, nu_0)(s, a, nu_0(s); rho) sqrt(frac(C_"clipped"^star log frac(N, delta), N min{d^(mu^star, nu_0)(s, a, nu_0(s); rho), frac(1, S(A+B))}) "Var"_(P_(s,a,nu_0(s)))(V_"pe"^-) ) \
&lt.eq sqrt(frac(C_"clipped"^star log frac(N, delta), N)) sum_(s in cal(S), a in cal(A)) sqrt(d^(mu^star, nu_0)(s, a, nu_0(s); rho) "Var"_(P_(s,a,nu_0(s)))(V_"pe"^-) ) \
&quad + sqrt(frac(C_"clipped"^star S(A+B) log frac(N, delta), N)) sum_(s in cal(S), a in cal(A)) sqrt(d^(mu^star, nu_0)(s, a, nu_0(s); rho)) dot sqrt(d^(mu^star, nu_0)(s, a, nu_0(s); rho) "Var"_(P_(s,a,nu_0(s)))(V_"pe"^-)) \
&overset((i i))(lt.eq) sqrt(frac(C_"clipped"^star, N) log frac(N, delta)) dot sqrt(S A) dot sqrt(sum_(s in cal(S), a in cal(A)) d^(mu^star, nu_0)(s, a, nu_0(s); rho) "Var"_(P_(s,a,nu_0(s)))(V_"pe"^-)) \
&quad + sqrt(frac(C_"clipped"^star S(A+B) log frac(N, delta), N)) [sum_(s in cal(S), a in cal(A)) d^(mu^star, nu_0)(s, a, nu_0(s); rho)] sqrt(sum_(s in cal(S), a in cal(A)) d^(mu^star, nu_0)(s, a, nu_0(s); rho) "Var"_(P_(s,a,nu_0(s)))(V_"pe"^-)) \
&lt.eq 2 sqrt(frac(C_"clipped"^star S(A+B) log frac(N, delta), N)) sqrt(sum_(s in cal(S), a in cal(A)) d^(mu^star, nu_0)(s, a, nu_0(s); rho) "Var"_(P_(s,a,nu_0(s)))(V_"pe"^-)) \
&overset((i i i))(=) 2 sqrt(frac(C_"clipped"^star S(A+B), N) log frac(N, delta)) sqrt(sum_(s in cal(S)) d^(mu^star, nu_0)(s; rho) op(bb(E))_(a tilde.op mu^star (s), b tilde.op nu_0(s)) [#h(0pt) "Var"_(P_(s,a,b))(V_"pe"^-)]) \
&overset((i v))(lt.eq) 2 sqrt(frac(C_"clipped"^star S(A+B), N) log frac(N, delta)) sqrt(sum_(s in cal(S)) d^(mu^star, nu_0)(s; rho) "Var"_(P_s^(mu^star, nu_0))(V_"pe"^-)).
$
