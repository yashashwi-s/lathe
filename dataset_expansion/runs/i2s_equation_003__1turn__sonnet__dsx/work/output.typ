#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Equation Sample 3]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Derivation

The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#v(0.5em)

$
&E_{p (tilde(x)))[angle.l G N N_(theta) (tilde(x)), nabla_(tilde(x)) log p (tilde(x)) angle.r ]\
=& integral_(tilde(x)) p (tilde(x)) angle.l G N N_(theta) (tilde(x)), nabla_(tilde(x)) log p (tilde(x)) angle.r dif tilde(x) \
=& integral_(tilde(x)) p (tilde(x)) angle.l G N N_(theta) (tilde(x)), frac(nabla_(tilde(x)) p (tilde(x)), p (tilde(x))) angle.r dif tilde(x) \
=& integral_(tilde(x)) angle.l G N N_(theta) (tilde(x)), nabla_(tilde(x)) p (tilde(x)) angle.r dif tilde(x) \
=& integral_(tilde(x)) angle.l G N N_(theta) (tilde(x)), nabla_(tilde(x)) (integral_(x) p (tilde(x)|x) p(x) dif x) angle.r dif tilde(x) \
=& integral_(tilde(x)) angle.l G N N_(theta) (tilde(x)), integral_(x) p(x) nabla_(tilde(x)) p (tilde(x)|x) dif x angle.r dif tilde(x) \
=& integral_(tilde(x)) angle.l G N N_(theta) (tilde(x)), integral_(x) p (tilde(x)|x) p(x) nabla_(tilde(x)) log p (tilde(x)|x) dif x angle.r dif tilde(x) \
=& integral_(tilde(x)) integral_(x) p (tilde(x)|x) p(x) angle.l G N N_(theta) (tilde(x)), nabla_(tilde(x)) log p (tilde(x)|x) angle.r dif x dif tilde(x) \
=& E_{p (tilde(x), x)) [ angle.l G N N_(theta) (tilde(x)), nabla_(tilde(x)) log p (tilde(x)|x) angle.r ]
$
