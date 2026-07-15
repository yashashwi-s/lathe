#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: false)

#align(center)[
  #text(size: 17pt, weight: "bold")[Inline and Display Mathematics]
  #v(0.5em)
  #text(size: 12pt)[Source-backed grouped formula sample]
  #v(1em)
]

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$ frac(partial cal(V), partial phi) = textstyle frac(2, n) frac(1, "Tr"(cal(M)^2)) cal(M)_(m n) frac(partial cal(V), partial cal(M)_(m n)) , quad => cal(M)^(m n) cal(M)_(p q) frac(partial cal(V), partial cal(M)_(p q)) - "Tr"(cal(M)^2) frac(partial cal(V), partial cal(M)_(m n)) = 0 . $

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$ integral D V exp( frac(1,2) integral d^4 x epsilon^(mu nu tau lambda) {}^(+) W_(mu nu)^(alpha beta) {}^(+) G_(tau lambda)^(sigma rho) epsilon_(alpha beta sigma rho) - frac(1,2) integral d^4 x epsilon^(mu nu tau lambda) {}^(-) W_(mu nu)^(alpha beta) {}^(-) G_(tau lambda)^(sigma rho) epsilon_(alpha beta sigma rho) ) $

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$ I = integral_Sigma d^3 x sqrt(gamma) lr(( R(gamma) - frac(1,2) lr((lr((D U))^2 - e^(-2U) lr((D V))^2)) - frac(1,2) lr((lr((D Phi))^2 - e^(-2 Phi) lr((D Psi))^2)) - lr((D T))^2 + e^(-(U + Phi)) V(T) )) $

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$ 2 frac(integral_(b=theta_2)^(b=theta_1) e^(frac(rho r s cos(b), 1-rho^2)) d b, 2 pi integral_0^(2 pi) e^(frac(rho r s cos a, 1-rho^2)) d a) <= 2 frac(integral_(b=0)^(b=theta_1 - theta_2) e^(frac(rho r s cos(b), 1-rho^2)) d b, 2 pi integral_0^(2 pi) e^(frac(rho r s cos a, 1-rho^2)) d a) < frac(theta_1 - theta_2, 2 pi^2) . $

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$ frac(d, d lambda) S_(omega, bold(c))(Phi_0^lambda) = -(sqrt(lambda)-1)(2L(Phi_0)+bold(c) dot bold(P)(Phi_0)) lr((lambda + frac(bold(c) dot bold(P)(Phi_0), 2L(Phi_0)+bold(c) dot bold(P)(Phi_0)) sqrt(lambda) + frac(bold(c) dot bold(P)(Phi_0), 2L(Phi_0)+bold(c) dot bold(P)(Phi_0)))) $
