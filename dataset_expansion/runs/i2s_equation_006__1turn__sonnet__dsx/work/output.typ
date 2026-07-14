#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Equation Sample 6]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Derivation

The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#set math.equation(numbering: none)

$
G_(c_p) &(b, c_p) \
&= - W^(-1) lr(( phi(b) integral_0^b psi(z,0) frac(diff, diff c_p) pi_1(z,c_p) m'(z) dif z + psi(b,0) integral_b^infinity phi(z) frac(diff, diff c_p) pi_1(z,c_p) m'(z) dif z ),size:#130%), \
G_(b c_p) &(b,c_p) \
&= - W^(-1) lr(( phi'(b) integral_0^b psi(z,0) frac(diff, diff c_p) pi_1(z,c_p) m'(z) dif z + phi(b) psi(b,0) frac(diff, diff c_p) pi_1(b,c_p) m'(b) \
&hspace(1cm) + psi'(b,0) integral_b^infinity phi(z) frac(diff, diff c_p) pi_1(z,c_p) m'(z) dif z - phi(b) psi(b,0) frac(diff, diff c_p) pi_1(b,c_p) m'(b) ),size:#130%) \
&= - W^(-1) lr(( phi'(b) integral_0^b psi(z,0) frac(diff, diff c_p) pi_1(z,c_p) m'(z) dif z + psi'(b,0) integral_b^infinity phi(z) frac(diff, diff c_p) pi_1(z,c_p) m'(z) dif z ),size:#130%).
$
