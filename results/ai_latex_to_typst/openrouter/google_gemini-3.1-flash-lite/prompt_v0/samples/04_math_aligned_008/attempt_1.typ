#set page(margin: 1in)
#set text(size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

#par(hanging-indent: 0pt)[*Expression 1.* The following expression is taken from a source-backed formula corpus.]

$ F^dagger H^dagger H F (p,q) = delta(p,q) mat(3, 0, 2 e^(-i p_1 + i p_2), 2 e^(-i p_1 - i p_2); 0, 3, -2 e^(+i p_1 + i p_2), 2 e^(+i p_1 - i p_2); 2 e^(+i p_1 - i p_2), -2 e^(-i p_1 - i p_2), 3, 0; 2 e^(+i p_1 + i p_2), 2 e^(-i p_1 + i p_2), 0, 3) $

#par(hanging-indent: 0pt)[*Expression 2.* The following expression is taken from a source-backed formula corpus.]

$
  cal(I)(lambda delta + (1-lambda) delta') &= sup_(nu in Sigma(lambda delta + (1-lambda) delta')) integral_(cal(S)) f(s) d nu(s) \
  &>= integral_(cal(S)) f d gamma'' = lambda integral_(cal(S)) f d gamma + (1-lambda) integral_(cal(S)) f d gamma'
$

#par(hanging-indent: 0pt)[*Expression 3.* The following expression is taken from a source-backed formula corpus.]

$ 1/2 { mat(Q_alpha; tilde(Q)_alpha) , [Q_beta quad tilde(Q)_beta] } = mat(1, 0; 0, 1) M delta_(alpha beta) + mat(p, q/g_s; q/g_s, -p) (L (Gamma^0 Gamma^1)_(alpha beta)) / (2 pi alpha') $

#par(hanging-indent: 0pt)[*Expression 4.* The following expression is taken from a source-backed formula corpus.]

$
  &delta Psi_alpha = 1/8 omega^(m n) (Gamma_(m n))_alpha^beta Psi_beta, &&Gamma_(m n) equiv Gamma_m tilde(Gamma)_n - Gamma_n tilde(Gamma)_m, \
  &delta chi^alpha = 1/8 omega^(m n) (tilde(Gamma)_(m n))^alpha_beta chi^beta, &&tilde(Gamma)_(m n) equiv tilde(Gamma)_m Gamma_n - tilde(Gamma)_n Gamma_m
$

#par(hanging-indent: 0pt)[*Expression 5.* The following expression is taken from a source-backed formula corpus.]

$ R_(i j)^(ell)(Lambda_1, dots.c, Lambda_i, dots.c, Lambda_j, dots.c, Lambda_N) = cases(
  (Lambda_1, dots.c, Lambda_i - ell, dots.c, Lambda_j + ell, dots.c, Lambda_N) quad "if" quad Lambda_i > Lambda_j,
  (Lambda_1, dots.c, Lambda_i + ell, dots.c, Lambda_j - ell, dots.c, Lambda_N) quad "if" quad Lambda_j > Lambda_i
) $
