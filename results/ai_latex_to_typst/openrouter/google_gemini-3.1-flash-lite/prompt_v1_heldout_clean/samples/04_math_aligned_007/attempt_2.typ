#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$
  &Delta_((n-1 l+1))^((1))(x_1, dots.c, x_m | z_1, dots.c, z_(n-1) | z_n, dots.c, z_N) \
  =& q^(l-n+1) sum_(k=n)^N z_k (product_(j=1)^(n-1) (z_k - z_j q^(-2))) / (product_(i=n, i != k)^N (z_i - z_k) q^(-1)) Delta^((n l))(x_1, dots.c, x_m | z_1, dots.c, z_(n-1), z_k | z_n, hat(dots.c), z_N)
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
  &[alpha_cal(L)(a), alpha_cal(L)(b), [x, y, z]_cal(L)]_cal(L) \
  =& [[a, b, x]_cal(L), alpha_cal(L)(y), alpha_cal(L)(z)]_cal(L) + [alpha_cal(L)(x), [a, b, y]_cal(L), alpha_cal(L)(z)]_cal(L) + [alpha_cal(L)(x), alpha_cal(L)(y), [a, b, z]_cal(L)]_cal(L)
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
  (II) quad mat(x_1 + "i" y_1; x_2 + "i" y_2; x_3 + "i" y_3; x_4 + "i" y_4) quad <-> quad 1/sqrt(2) mat(-(y_2 + y_4) + "j"(y_2 - y_4); (y_1 + y_3) - "j"(y_1 - y_3); (x_2 + x_4) - "j"(x_2 - x_4); -(x_1 + x_3) + "j"(x_1 - x_3))
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$
  (|partial_t^ell cal(D)^alpha phi|^2)_t = -2 sum_(ell_1 + |alpha_1| > 0) partial_t^ell cal(D)^alpha phi partial_t^ell_1 cal(D)^alpha_1 v dot nabla(partial_t^ell_2 cal(D)^alpha_2 phi) - v dot nabla |partial_t^ell cal(D)^alpha phi|^2
$

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$
  table(
    columns: (auto, auto, auto),
    align: (right, center, left),
    column-gap: 1em,
    "Tr" [Gamma]_s(P^a) [Gamma]_s(P_b) = delta^a_b, "=>", [Gamma]_s(P^a) = (-i)/(2g) gamma^a,
    "", "", "",
    "Tr" [Gamma]_s(M^(ab)) [Gamma]_s(P_(cd)) = delta^(ab)_(cd), "=>", [Gamma]_s(M^(ab)) = -1/2 gamma^(ab)
  )
$
