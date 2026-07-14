#set page(margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")

#align(center, [
  #text(size: 1.44em, weight: "bold")[Inline and Display Mathematics] \
  #text(size: 1.2em)[Source-backed grouped formula sample] \
  #text(size: 1em)[]
])

= Expressions

#par(hanging-indent: 0pt)[*Expression 1.* The following expression is taken from a source-backed formula corpus.]

$ (partial cal(V)) / (partial phi) = (2/n) 1 / (op("Tr")(cal(M)^2)) cal(M)_(m n) (partial cal(V)) / (partial cal(M)_(m n)) , arrow.r.double.long cal(M)^(m n) cal(M)_(p q) (partial cal(V)) / (partial cal(M)_(p q)) - op("Tr")(cal(M)^2) (partial cal(V)) / (partial cal(M)_(m n)) = 0 . $

#par(hanging-indent: 0pt)[*Expression 2.* The following expression is taken from a source-backed formula corpus.]

$ integral D V exp(1/2 integral d^4 x epsilon^(mu nu tau lambda) ""^+ W_(mu nu)^(alpha beta) ""^+ G_(tau lambda)^(sigma rho) epsilon_(alpha beta sigma rho) - 1/2 integral d^4 x epsilon^(mu nu tau lambda) ""^- W_(mu nu)^(alpha beta) ""^- G_(tau lambda)^(sigma rho) epsilon_(alpha beta sigma rho)) . $

#par(hanging-indent: 0pt)[*Expression 3.* The following expression is taken from a source-backed formula corpus.]

$ I = integral_Sigma d^3 x sqrt(gamma) (R(gamma) - 1/2 ((D U)^2 - e^(-2 U) (D V)^2) - 1/2 ((D Phi)^2 - e^(-2 Phi) (D Psi)^2) - (D T)^2 + e^(-(U + Phi)) V(T)) $

#par(hanging-indent: 0pt)[*Expression 4.* The following expression is taken from a source-backed formula corpus.]

$ 2 (integral_(b=theta_2)^(b=theta_1) e^((rho r s cos(b)) / (1 - rho^2)) d b) / (2 pi integral_0^(2 pi) e^((rho r s cos a) / (1 - rho^2)) d a) <= 2 (integral_(b=0)^(b=theta_1 - theta_2) e^((rho r s cos(b)) / (1 - rho^2)) d b) / (2 pi integral_0^(2 pi) e^((rho r s cos a) / (1 - rho^2)) d a) < (theta_1 - theta_2) / (2 pi^2) . $

#par(hanging-indent: 0pt)[*Expression 5.* The following expression is taken from a source-backed formula corpus.]

$ (d / d lambda) S_(omega, bold(c))(Phi_0^lambda) = -(sqrt(lambda) - 1) (2 L(Phi_0) + bold(c) dot bold(P)(Phi_0)) (lambda + (bold(c) dot bold(P)(Phi_0)) / (2 L(Phi_0) + bold(c) dot bold(P)(Phi_0)) sqrt(lambda) + (bold(c) dot bold(P)(Phi_0)) / (2 L(Phi_0) + bold(c) dot bold(P)(Phi_0))) $
