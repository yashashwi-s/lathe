#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.4em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

#par(hanging-indent: 0pt)[*Expression 1.* The following expression is taken from a source-backed formula corpus.]

$
  B &:= A^* union (A^* + c) \
  C &:= (A^* + 7c - d) union (A^* + 8c - d) \
  D &:= (A^* + 10c - d) union (A^* + 11c - d) \
  E &:= (A^* + 17c - 2d) union (A^* + 18c - 2d) \
  F &:= (A^* + 30c - 3d) union (A^* + 31c - 3d) \
  G &:= (A^* + 37c - 4d) union (A^* + 38c - 4d) \
  H &:= (A^* + 40c - 4d) union (A^* + 41c - 4d) \
  I &:= (A^* + 47c - 5d) union (A^* + 48c - 5d) \
  J &:= B union C union D union E union F union G union H union I
$

#par(hanging-indent: 0pt)[*Expression 2.* The following expression is taken from a source-backed formula corpus.]

$
  &Delta_((n+1 l-1))^((0))(x_1, dots.c, x_m | z_1, dots.c, z_(n+1) | z_(n+2), dots.c, z_N) \
  =& sum_(k=1)^(n+1) (product_(i=n+2)^(N) (z_i - z_k q^(-2))) / (product_(j=1, j != k)^(n+1) (z_k - z_j)q^(-1)) Delta^((n l))(x_1, dots.c, x_m | z_1, hat(dots.c)^k, z_(n+1) | z_k, z_(n+2), dots.c, z_N)
$

#par(hanging-indent: 0pt)[*Expression 3.* The following expression is taken from a source-backed formula corpus.]

$
  &| ||phi_(n,t)(b)||^2 - ||b||^2 | = | ||phi_(n,t)(b)^* phi_(n,t)(b)|| - ||b^* b|| | \
  &<= | ||phi_(n,t^(-1))(b^*) phi_(n,t)(b)|| - ||phi_(n,e)(b^* b)|| | + | ||phi_(n,e)(b^* b)|| - ||b^* b|| | \
  &<= | ||phi_(n,t^(-1))(b^*) phi_(n,t)(b) - phi_(n,e)(b^* b)|| | + | ||phi_(n,e)(b^* b)|| - ||b^* b|| |
$

#par(hanging-indent: 0pt)[*Expression 4.* The following expression is taken from a source-backed formula corpus.]

$
  [ M_i , p_j ] &= i epsilon_(ijk) p_k , quad [ M_i , p_0 ] = 0 , \
  [ N_i , p_0 ] &= i p_i , quad [ p_mu , p_nu ] = 0 , \
  [ N_i , p_j ] &= i delta_(ij) [ kappa c sinh(p_0 / (kappa c)) e^(-p_0 / (kappa c)) + 1/2 (1 / (kappa c)) (vec(p))^2 ] - i / (kappa c) p_i p_j
$

#par(hanging-indent: 0pt)[*Expression 5.* The following expression is taken from a source-backed formula corpus.]

$
  X_1 &:= { w in W_("per")^(1,r)(cal(S)) : w = 0 "on" { zeta = -1 } } \
  X_2 &:= L^infinity([-1,0]) \
  Y &:= { u in (W_("per")^(1,r')(cal(S)))^* : u = cal(A) + partial_xi cal(B)_1 + partial_zeta cal(B)_2, "for" cal(A) , cal(B)_1, cal(B)_2 in L^r(cal(S)) }
$
