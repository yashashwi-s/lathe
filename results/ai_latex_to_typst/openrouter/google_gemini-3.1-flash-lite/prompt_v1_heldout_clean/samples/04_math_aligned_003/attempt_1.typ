#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$
  S_g = integral d^4 x e { R(e, omega) + 6g^2 + 2 e^(-1) epsilon^(mu nu rho sigma) bar(psi)_mu gamma_5 gamma_nu (hat(cal(D))_rho + i g A_rho sigma^2) psi_sigma - cal(F)^2 \
  + cal(J)_((m))^(mu nu) (cal(J)_((e) mu nu) + cal(J)_((m) mu nu)) } ,
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
  V_12 &= 2^2 cos[k_(1 lambda_1) wedge k_(2 lambda_2) + (p_lambda + q_lambda) wedge (k_(1 lambda_1) - k_(2 lambda_2))] cos(p_lambda wedge q_lambda) \
  V_34 &= 2^2 cos[k_(3 lambda_3) wedge k_(4 lambda_4) + (p_lambda + q_lambda) wedge (k_(3 lambda_3) - k_(4 lambda_4))] cos(p_lambda wedge q_lambda)
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
  cal(I)(lambda delta + (1-lambda) delta') &>= lambda sup_(gamma in Sigma(delta)) integral_(cal(S)) f(s) d gamma(s) + (1-lambda) sup_(gamma' in Sigma(delta')) integral_(cal(S)) f(s) d gamma'(s) \
  &>= lambda cal(I)(delta) + (1-lambda) cal(I)(delta')
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$
  [e_i, f_j] &= delta_(i j) (k_i - k_i^(-1)) / (Q_i - Q_i^(-1)) \
  k_i e_j k_i^(-1) &= Q_i^(a_(i j)) e_j, quad k_i f_j k_i^(-1) = Q_i^(-a_(i j)) f_j \
  k_i k_i^(-1) &= k_i^(-1) k_i = 1, quad k_i k_j = k_j k_i \
  [e_i, e_i] &= [f_i, f_i] = 0, "if" quad a_(i i) = 0
$

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$
  cal(R)_(beta_0, beta_1)(z) := & (cal(A)_0 - z I)^(-1) - (I - z cal(A)_0^(-1))^(-1) Pi(overline(beta_0 + beta_1 M(z)))^(-1) beta_1 (Pi^*(I - z cal(A)_0^(-1))^(-1)) \
  = & (cal(A)_0 - z I)^(-1) - S(z) (overline(beta_0 + beta_1 M(z)))^(-1) beta_1 S^*(overline(z))
$
