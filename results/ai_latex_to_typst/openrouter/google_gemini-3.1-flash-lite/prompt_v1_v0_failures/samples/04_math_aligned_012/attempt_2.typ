#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.4em, weight: "bold")[Aligned Mathematical Structures]
  #v(0.5em)
  Source-backed grouped formula sample
])

= Expressions

#par(hanging-indent: 0pt)[*Expression 1.* The following expression is taken from a source-backed formula corpus.]

$ cal(J)_("D")(delta) = inf_(lambda in RR_+^L, psi_ell > - infinity, (psi_ell)_(ell in [L]) in product_(ell in [L]) L^1(mu_ell)) { angle.l lambda, delta angle.r + sum_(ell=1)^L integral psi_ell d mu_ell : sum_(ell=1)^L psi_ell(s_ell) >= g_(lambda, [L])(s), forall s } $

#par(hanging-indent: 0pt)[*Expression 2.* The following expression is taken from a source-backed formula corpus.]

$ C_n(x) = cases(
  K - v x + G_n(x + B) & s_(k-1) < x <= hat(S)_k - B quad k=1, dots, w-1,
  K - v x + G_n(hat(S)_k) & hat(S)_k - B < x <= s_k quad k=1, dots, w-1,
  K - v x + G_n(x + B) & s_(w-1) < x <= S_m - B,
  K - v x + G_n(S_m) & S_m - B < x <= s_m,
  -v x + G_n(x) & x > s_m
) $

#par(hanging-indent: 0pt)[*Expression 3.* The following expression is taken from a source-backed formula corpus.]

$ 1/2 mat(1, 0; 0, 1) \
\
 plus.minus 1/2 mat(1, 0; 0, -1) " or " plus.minus 1/2 mat(0, 1; 1, 0) " or " plus.minus (q_i)/2 mat(0, 1; -1, 0) $

#par(hanging-indent: 0pt)[*Expression 4.* The following expression is taken from a source-backed formula corpus.]

$ & |phi_n(alpha_a(E_psi)) - chi(E_psi)| \
= & |phi_n(alpha_a(E_psi)) - chi(E_(f_n) E_psi)| \
<= & integral_(b in U_n) f_n(b) (integral |Delta(b^(-1) a)^m psi(g_1 b^(-1) a, dots, g_m b^(-1) a) - psi(g_1, g_2, dots, g_m)| d g_1 dots d g_m) d b \
<= & epsilon integral_(b in U_n) f_n(b) \
<= & epsilon $

#par(hanging-indent: 0pt)[*Expression 5.* The following expression is taken from a source-backed formula corpus.]

$ V^((1)) = & 1/(4!) f phi^4 + 1/48 (beta_f - 4 f gamma_phi) phi^4 (log (phi^2)/(mu^2) - 25/6) \
& - 1/2 xi R phi^2 - 1/4 (beta_xi - 2 xi gamma_phi) R phi^2 (log (phi^2)/(mu^2) - 3) $
