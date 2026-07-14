#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

#par(hanging-indent: 0pt)[*Expression 1.* The following expression is taken from a source-backed formula corpus.]

$
  &D=1: &&chi_y(E)=0,, \
  &D=2: &&chi_y(E)=2(1+10y+y^2)(1-y)^(r-2),, \
  &D=3: &&chi_y(E)=-chi(E)y(1+y)(1-y)^(r-3),, \
  &D=4: &&chi_y(E)=(2+(2r-8-chi(E))y \
  & &&hskip 2cm +(8r+12-4chi(E))y^2+(2r-8-chi(E))y^3+2y^4)(1-y)^(r-4),, \
  &D=5: &&chi_y(E)=-chi(E)y(1+y)(1+10y+y^2)(1-y)^(r-5),,
$

#par(hanging-indent: 0pt)[*Expression 2.* The following expression is taken from a source-backed formula corpus.]

$
  &cal(I)_("D")(eta_0, delta) - cal(I)_("D")(eta, 0) \
  &quad = cal(I)_("D")(eta_0, delta) - cal(I)_("D")(eta, delta) + cal(I)_("D")(eta, delta) - cal(I)_("D")(eta, 0) \
  &quad <= Psi(eta_0-eta, 0) + Psi(0, delta) = Psi(|eta_0-eta|, 0) + Psi(0, delta).
$

#par(hanging-indent: 0pt)[*Expression 3.* The following expression is taken from a source-backed formula corpus.]

$
  &phi_lambda(v, s') \
  &quad = f(s') - lambda_1 bold(d)_(cal(S)_1)(s_1, s_1')^(p_1) - lambda_2 bold(d)_(cal(S)_2)(s_2, s_2')^(p_2) \
  &quad >= B + (B - lambda_1) bold(d)_(cal(S)_1)(s_1, s_1')^(p_1) + (B - lambda_2) bold(d)_(cal(S)_2)(s_2, s_2')^(p_2) >= B.
$

#par(hanging-indent: 0pt)[*Expression 4.* The following expression is taken from a source-backed formula corpus.]

$
  S_("IIB") &= -T_(M_2) l integral d^2 xi sqrt(|tilde(g)_(i j) - 1/(tilde(k)^2)(partial_i rho + tilde(B)^((1))_i)(partial_j rho + tilde(B)^((1))_j)|) \
  & \
  & - T_(M_2) l / 2 integral d^2 xi epsilon^(i j) [tilde(B)^((2))_(i j) + 2 partial_i rho (tilde(A)^((1))_i + m pi alpha' b_j)] .
$

#par(hanging-indent: 0pt)[*Expression 5.* The following expression is taken from a source-backed formula corpus.]

$
  &angle q_(i 0) - Q_(i 0) angle &&= 0 ,, \
  & && \
  &angle dot(q)_(i 0) angle &&= 0 ,, \
  & && \
  &m omega_i omega_j angle (q_(i 0) - Q_(i 0))(q_(j 0) - Q_(j 0)) angle &&= k_B T delta_(i j) ,, \
  & && \
  &m angle dot(q)_(i 0) dot(q)_(j 0) angle &&= k_B T delta_(i j) ,, \
  & && \
  &angle dot(q)_(i 0)(q_(j 0) - Q_(j 0)) angle &&= 0 .
$
