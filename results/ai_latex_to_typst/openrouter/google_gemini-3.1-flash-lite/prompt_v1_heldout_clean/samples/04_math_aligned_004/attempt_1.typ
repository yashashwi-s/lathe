#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures] \
  Source-backed grouped formula sample
])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

$ overline(omega)^m ( (b^(d-1) d^d) / (a^d (d-1)^(d-1)) ) product_(i=0)^(r-1) product_(h=1)^(d-2) (Gamma_p (angle ( (h/(d-1) - m/(q-1)) p^i angle ))) / (Gamma_p (angle ( (h p^i) / (d-1) angle ))) product_((h=1, h != d/2))^(d-1) (Gamma_p (angle ( (h/d + m/(q-1)) p^i angle ))) / (Gamma_p (angle ( (h p^i) / d angle ))) = phi(b). $

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
  &||a||_sharp + ||x^natural - a||_sharp && >= ||x^natural||_sharp \
  & && >= ||x^star||_sharp \
  & && = ||x^natural + (x^star - x^natural)||_sharp \
  & && = ||a + (x^natural - a) + z_1 + z_2||_sharp \
  & && >= ||a + z_1||_sharp - ||(x^natural - a) + z_2||_sharp \
  & && >= ||a + z_1||_sharp - ||x^natural - a||_sharp - ||z_2||_sharp \
  & && = ||a||_sharp + ||z_1||_sharp - ||x^natural - a||_sharp - ||z_2||_sharp.
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
  cases(
    inf_(x_m) F_(tau_m)^(k-1) (x_([n]), x_m, Psi_m) := f_(tau_m) (x_([n]), x_m, Psi_m) + Q_m^(k-1) (x_([n]), x_m),
    g_(tau_m) (x_0, x_([n]), x_m, Psi_m) <= 0,
    "[" A_(0, m), dots, A_(tau_m, m) "]" "[" x_0; x_([n]); x_m "]" = b_m,
    x_m in X_(tau_m).
  )
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$ gamma^0 = mat(sigma^3, 0; 0, -sigma^3), quad gamma^1 = mat(i sigma^2, 0; 0, -i sigma^2), quad gamma^2 = mat(-i sigma^1, 0; 0, i sigma^1), quad gamma^3 = mat(0, I; -I, 0). $

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$ g^dagger = mat(1 + 1/4 eta eta^diamond, 1/2 (b eta^diamond + a^diamond eta), -1/2 (a eta^diamond - b^diamond eta); 1/2 eta^diamond, a^diamond (1 - 1/8 eta eta^diamond), b^diamond (1 - 1/8 eta eta^diamond); 1/2 eta, -b (1 - 1/8 eta eta^diamond), a (1 - 1/8 eta eta^diamond)) $
