#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$
  mat(delim: none,
    psi^dagger psi, arrow.r, beta integral_(alpha_-)^(alpha_+) (d p) / (2 pi) = (beta) / (2 pi) (alpha_+ - alpha_-);
    1 / beta^2 (partial psi^dagger) / (partial lambda) (partial psi) / (partial lambda), arrow.r, (beta) / (2 pi) integral d p p^2 = (beta) / (6 pi) (alpha_+^3 - alpha_-^3);
    dots.c, dots.c, dots.c
  )
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
  x &= epsilon^(-1) (R_n R_(n+1)) log^(2N-3) (( (R_n R_(n+1)) / epsilon )^((R_n R_(n+1)) / 2) (N-1) / eta), \
  y &= log^4 (( (R_n R_(n+1)) / epsilon )^(1/2) log^(N-1) (( (R_n R_(n+1)) / epsilon )^((R_n R_(n+1)) / 2) (N-1) / eta)) log product_(j != n) I_j
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
  mat(delim: none, align: left,
    C_n(x) = min { L_n(x) + integral_0^infinity C_(n-1)(x - xi) f_n(xi) "d"xi, min_(x < y <= x+B) {K + v(y-x) + L_n(y) + integral_0^infinity C_(n-1)(y - xi) f_n(xi) "d"xi} };
    G_n(x) = v x + L_n(x) + integral_0^infinity C_(n-1)(x - xi) f_n(xi) "d"xi;
    C_n(x) = -v x + min {G_n(x), K + min_(x <= y <= x+B) G_n(y)}
  )
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$
  lr(brace.l, size: #150%,
    mat(delim: none, align: left,
      j^mu(x) = lim_(y -> x) 1/2 (bar(psi)(x) gamma^mu psi(y) + bar(psi)(y) gamma^mu psi(x)) = - (beta) / (2 pi) epsilon^(mu nu) partial_nu phi(x);
      (4 pi) / beta^2 = 1 + g / pi;
      (m_0^2) / beta^2 cos(beta phi) = Z M bar(psi) psi
    )
  )
$

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$
  mat(delim: none,
    { U^1_alpha }, arrow.l.long^((rho_(V, { U^1_alpha }))) , { U^1_alpha |_V };
    script(rho_12) arrow.t, , arrow.t script(rho_(V, 12));
    { U^2_alpha }, arrow.l.long^((rho_(V, { U^2_alpha }))) , { U^2_alpha |_V }
  )
$
