#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Aligned Mathematical Structures]
  #v(0.5em)
  #text(size: 12pt)[Source-backed grouped formula sample]
  #v(1.5em)
]

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$ F^dagger H^dagger H F (p,q) = delta(p,q) mat(delim: "(", 3, 0, 2e^(-i p_1 + i p_2), 2e^(-i p_1 - i p_2); 0, 3, -2e^(+i p_1 + i p_2), 2e^(+i p_1 - i p_2); 2e^(+i p_1 - i p_2), -2e^(-i p_1 - i p_2), 3, 0; 2e^(+i p_1 + i p_2), 2e^(-i p_1 + i p_2), 0, 3), $

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$ cal(I)(lambda delta + (1-lambda) delta') &= sup_(nu in Sigma(lambda delta + (1-lambda) delta')) integral_(cal(S)) f(s) d nu(s) \
  &>= integral_(cal(S)) f d gamma'' = lambda integral_(cal(S)) f d gamma + (1-lambda) integral_(cal(S)) f d gamma'. $

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$ 1/2 {mat(delim: "[", Q_alpha; tilde(Q)_alpha), mat(delim: "[", Q_beta, tilde(Q)_beta)} = mat(delim: "[", 1, 0; 0, 1) M delta_(alpha beta) + mat(delim: "[", p, q\/g_s; q\/g_s, -p) (L (Gamma^0 Gamma^1)_(alpha beta)) / (2 pi alpha') . $

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$ &delta Psi_alpha = 1/8 omega^(m n) (Gamma_(m n))_alpha^(space beta) Psi_beta, quad &&Gamma_(m n) equiv Gamma_m tilde(Gamma)_n - Gamma_n tilde(Gamma)_m, \
  &delta chi^alpha = 1/8 omega^(m n) (tilde(Gamma)_(m n))^alpha_(space beta) chi^beta, quad &&tilde(Gamma)_(m n) equiv tilde(Gamma)_m Gamma_n - tilde(Gamma)_n Gamma_m, $

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$ R_(i j)^((ell))(Lambda_1, dots, Lambda_i, dots, Lambda_j, dots, Lambda_N) = cases(
  (Lambda_1, dots, Lambda_i - ell, dots, Lambda_j + ell, dots, Lambda_N) & "if" quad Lambda_i > Lambda_j",",
  (Lambda_1, dots, Lambda_i + ell, dots, Lambda_j - ell, dots, Lambda_N) & "if" quad Lambda_j > Lambda_i".",
) $
