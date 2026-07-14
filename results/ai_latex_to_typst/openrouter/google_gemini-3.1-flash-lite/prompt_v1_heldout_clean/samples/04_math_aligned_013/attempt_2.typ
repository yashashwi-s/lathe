#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$
  mat(delim: #none,
    "minimize", C dot U hat(X) U^T;
    "subject to", A_i dot U hat(X) U^T = b_i "  " forall i in {1, dots.h, m};
    , hat(X) in bb(S)^d_+
  )
  "  "
  mat(delim: #none,
    "maximize", b^T y;
    "subject to", U^T (C - sum^m_(i=1) y_i A_i) U in bb(S)^d_+;
    , ""
  )
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
  q dot N_d &= sum_(x,y,z in bb(F)_q) theta(z E_d(x,y)) \
  &= q^2 + sum_(z in bb(F)_q^times) theta(z b) + sum_(y,z in bb(F)_q^times) theta(b z) theta(-z y^2) + sum_(x,z in bb(F)_q^times) theta(z x^d) theta(z a x) theta(z b) \
  &+ sum_(x,y,z in bb(F)_q^times) theta(x^d z) theta(a x z) theta(b z) theta(-z y^2) \
  &= q^2 + A + B + C + D.
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
  M = 1 / sqrt(1 + bold(bar(w)) dot bold(w) - 1/4 (bold(w) times bold(bar(w)))^2) mat(
    1 - i/2 (bold(w) times bold(bar(w))) dot bold(sigma), -bold(w) dot bold(sigma);
    bold(bar(w)) dot bold(sigma), 1 + i/2 (bold(w) times bold(bar(w))) dot bold(sigma)
  )
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$
  U(vec(a), 1)(S, f_alpha otimes rho(E^alpha)) &:= e^(-i[hat(f)_0 dot hat(H)(vec(a), rho) + hat(f)_1 dot hat(P)(vec(a), rho)]) (S + vec(a), f_alpha(dot.c - vec(a)) otimes rho(E^alpha)) \
  &= e^(i[a^0 hat(H)(rho) - a^1 hat(P)(rho)]) (S + vec(a), f_alpha(dot.c - vec(a)) otimes rho(E^alpha)).
$

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$
  I_1 &= (-infinity, omega_xi^ast - (alpha xi^alpha) / (2(1 - alpha))], \
  I_2 &= [omega_xi^ast - (alpha xi^alpha) / (2(1 - alpha)), omega_xi^ast + (alpha xi^alpha) / (2(1 - alpha))], \
  I_3 &= [omega_xi^ast + (alpha xi^alpha) / (2(1 - alpha)), 0], " and " \
  I_4 &= [0, infinity).
$
