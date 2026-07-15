#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true, leading: 0.65em)
#show math.equation: set text(size: 11pt)

#let clipped = math.sans("clipped")
#let Var = math.sans("Var")
#let pe = math.sans("pe")
#let dstar(args) = $d^(mu^star, nu_0) lr((#args), size: #120%)$

#v(43pt)
#align(center)[
  #text(size: 17.28pt)[Equation Sample 1]
  #v(1.2em)
  #text(size: 12pt)[Dataset-expansion sample]
]
#v(2.5em)

= Derivation

The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#let d0 = $d^(mu^star, nu_0) lr((s, a, nu_0(s); rho), size: #120%)$
#let VarP = $sans("Var")_(P_(s,a,nu_0(s))) lr((V_sans("pe")^-))$
#let Cc = $C_sans("clipped")^star$
#let logNd = $log N/delta$
#let sumSA = $sum_(s in cal(S), a in cal(A))$

$
alpha_3 & attach(<=, t: "(i)") sumSA d0 sqrt( (Cc log N/delta) / (N min{ d0, 1/(S(A+B)) }) VarP ) \
& <= sqrt((Cc log N/delta)/N) sumSA sqrt(d0 VarP) \
& quad + sqrt((Cc S(A+B) log N/delta)/N) sumSA sqrt(d0) dot sqrt(d0 VarP) \
& attach(<=, t: "(ii)") sqrt(Cc/N log N/delta) dot sqrt(S A) dot sqrt(sumSA d0 VarP) \
& quad + sqrt((Cc S(A+B) log N/delta)/N) [sumSA d0] sqrt(sumSA d0 VarP) \
& <= 2 sqrt((Cc S(A+B) log N/delta)/N) sqrt(sumSA d0 VarP) \
& attach(=, t: "(iii)") 2 sqrt((Cc S(A+B))/N log N/delta) sqrt( sum_(s in cal(S)) d^(mu^star, nu_0)(s;rho) EE_(a tilde mu^star (s), b tilde nu_0(s)) [sans("Var")_(P_(s,a,b))(V_sans("pe")^-)] ) \
& attach(<=, t: "(iv)") 2 sqrt((Cc S(A+B))/N log N/delta) sqrt( sum_(s in cal(S)) d^(mu^star, nu_0)(s;rho) sans("Var")_(P_s^(mu^star, nu_0)) (V_sans("pe")^-) ).
$
