#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures]
  #v(0.5em)
  Source-backed grouped formula sample
])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$
mu_1(2 epsilon - epsilon^2) alpha_1^2 &= (1-c)/t (2 epsilon - epsilon^2) 1/2t (sum_(v in V(K)) delta_v)^2 \
&< epsilon t^(-2) (sum_(v in V(K)) delta_v)^2 \
&<= min{ epsilon^(-1) t^(-2) (sum_(v in S) delta_v)^2, 2 epsilon t^(-1) sum_(v in V(K)) delta_v^2 }
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
table(
  columns: (auto, auto, auto, auto),
  align: (right, center, left, left),
  $L_{-1}$, $L_0$, $L_1$, $L_2 dots.c$,
  $J_{-2} J_{-1}$, $J_0$, $J_1$, $J_2 dots.c$,
  $Lambda_{-3} Lambda_{-2} Lambda_{-1}$, $Lambda_0$, $Lambda_1$, $Lambda_2 dots.c$,
  $dots.c dots.c dots.c dots.c dots.c dots.c dots.c$, $dots.c$, $dots.c$, $dots.c dots.c dots.c dots.c dots.c$
)
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
integral_0^t integral_(RR^3) (partial_t phi_1 xi + gamma k_1 v dot (xi nabla phi_1 + phi_1 nabla xi) + gamma k_1 bar(p) v dot nabla phi_1 - k_1 phi_1 v dot nabla xi) "d"x "d"s \
= -integral_(RR^3) xi_0(x, tau) phi_1(dot.c, 0) "d"x
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$
table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (right, center, left, right, center, left),
  $delta k$, $=$, $1/2 theta k ell$, $delta A^{(1)}$, $=$, $-theta A^{(2)}$,
  $$, $$, $$, $$, $$, $$,
  $delta e^phi$, $=$, $-7/4 theta ell e^phi$, $delta A^{(2)}$, $=$, $theta A^{(1)}$,
  $$, $$, $$, $$, $$, $$,
  $delta ell$, $=$, $theta (1 + ell^2 - 2k e^(-2phi))$, $delta B$, $=$, $0$
)
$

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$
P_0 U(vec(a), 1) B_s^n 1 &= P_0 psi^(beta_1, n)(g_1)_(U(vec(a))) psi^(beta_2, n)(g_2)_(U(vec(a))) dots.c psi^(beta_(s-1), n)(g_(s-1))_(U(vec(a))) U(vec(a), 1) psi^(beta_s, n)(g_s) 1 \
&= e^(i[a^0 hat(H) - a^1 hat(P)]) P_0 B_s^(n, vec(a)) 1 = e^(i[a^0 hat(H) - a^1 hat(P)]) [B_s^(n, vec(a)) 1 - angle.l B_s^n 1, 1 angle.r 1]
$
