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
  Delta_(plus.minus) = c/24 plus.minus (I_H^(plus.minus) - 2 I_S^(plus.minus) - I_C^(plus.minus) - I_W^(plus.minus)) + 1/(2 pi) Sigma_(plus.minus) \
  minus.plus 1/(2 pi) integral_(-infinity)^(infinity) (d x)/(2 pi) phi_(plus.minus)^', (x) cal(Q)_(plus.minus) (x)
$

*Expression 2.* The following expression is taken from a source-backed formula corpus.

$
  floor((-2 m p^i)/(q - 1)) + floor((m d p^i)/(q - 1)) + floor((-m (d - 1) p^i)/(q - 1)) - floor((-m p^i)/(q - 1)) + 1 \
  = sum_(h=1)^(d-2) floor(chevron.l (h p^i)/(d - 1) chevron.r - (m p^i)/(q - 1)) + floor(chevron.l (p^i)/2 chevron.r - (m p^i)/(q - 1)) + sum_(h=1)^(d-1) floor(chevron.l (-h p^i)/d chevron.r + (m p^i)/(q - 1))
$

*Expression 3.* The following expression is taken from a source-backed formula corpus.

$
  bold(E)(bold(x), t) = 1/(4 pi) integral rho_e(bold(x)', t - r) (bold(r))/(r^3) d^3 x' \
  + 1/(4 pi) integral bold(J)_m(bold(x)', t - r) times (bold(r))/(r^3) d^3 x' - 1/(4 pi) integral 1/r (partial bold(J)_m(bold(x)', t - r))/(partial t) d^3 x'
$

*Expression 4.* The following expression is taken from a source-backed formula corpus.

$
  Gamma^5 = mat(0, 1_2; 1_2, 0); quad Gamma^i = mat(0, sigma^i; -sigma^i, 0); quad Gamma^0 = mat(1_2, 0; 0, -1_2); quad Gamma^4 = -i Gamma^5 = mat(0, i_2; i_2, 0)
$

*Expression 5.* The following expression is taken from a source-backed formula corpus.

$
  overline(omega)^m ((b^(d-1) d^d)/(a^d (d - 1)^(d-1))) product_(i=0)^(r-1) product_(h=1)^(d-2) (Gamma_p(chevron.l (h/(d - 1) - m/(q - 1)) p^i chevron.r))/(Gamma_p(chevron.l (h p^i)/(d - 1) chevron.r)) product_(h=1, h != d/2)^(d-1) (Gamma_p(chevron.l (h/d + m/(q - 1)) p^i chevron.r))/(Gamma_p(chevron.l (h p^i)/d chevron.r)) = 1
$
