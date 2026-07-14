#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$
  &delta r_+ = delta(M + sqrt(M^2 - a^2 - Q^2)) \
  & = delta M + 1/2 (M^2 - a^2 - Q^2)^(-1/2) dot 2(M delta M - a delta a) \
  & = delta M + (r_+ - M)^(-1) (M delta M - a delta a) ; \
  & a delta a = a delta(J/M) = a/M delta J - a^2/M delta M ;
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
  A circle_X B &= (A X)(X^dagger B) \
  &= (A X^(2/3) X^(1/3))(X^(-1/3) X^(-2/3) B) \
  &= X^(1/3) [(X^(-1/3) A X^(2/3))(X^(-2/3) B)] \
  &= X^(1/3) [(X^(-1/3) A X^(1/3) X^(1/3))(X^(-1/3) X^(-1/3) B)] \
  &= X^(1/3) {[(X^(-1/3) A X^(1/3))(X^(-1/3) B X^(1/3))] X^(-1/3)} \
  &= X^(1/3) [(X^(-1/3) A X^(1/3))(X^(-1/3) B X^(1/3))] X^(-1/3)
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
  F_("p;r")^((L))(q) = q^(-r(r-1)) times cases(
    F_("p-2")^((L)) [ mat(bold(Q)_(r,1); bold(0)) ](bold(e)_r | q) "if" L != r-1 mod 2,
    F_("p-2")^((L)) [ mat(bold(Q)_(p-r,p); bold(0)) ](bold(e)_(p-r) | q) "if" L equiv r-1 mod 2
  )
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$
  u(tau) = e^(sqrt(gamma^2 + m^2/2) tau) [u_0 cosh(gamma tau) - (u_0 sqrt(gamma^2 + m^2/2) - dot(u)_0) 1/gamma sinh(gamma tau)] \
  v(tau) = e^(-sqrt(gamma^2 + m^2/2) tau) [v_0 cosh(gamma tau) + (v_0 sqrt(gamma^2 + m^2/2) + dot(v)_0) 1/gamma sinh(gamma tau)]
$

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$
  "*" f_(mu nu)(x) = - e_0 / (4 pi epsilon_0 c) [partial_mu vec(n)(x) wedge partial_nu vec(n)(x)] vec(n)(x) = mat(
    0, B_x, B_y, B_z;
    -B_x, 0, E_z/c, -E_y/c;
    -B_y, -E_z/c, 0, E_x/c;
    -B_z, E_y/c, -E_x/c, 0
  )
$
