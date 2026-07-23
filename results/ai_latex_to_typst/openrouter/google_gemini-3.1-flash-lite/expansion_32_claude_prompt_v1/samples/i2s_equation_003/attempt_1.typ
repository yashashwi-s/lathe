#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")

#align(center)[
  #text(size: 2em, weight: "bold")[Equation Sample 3]
  #v(1em)
  #text(size: 1.2em)[Dataset-expansion sample]
  #v(1em)
]

#heading(level: 1)[Derivation]
The following display is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

$
  &E_(p (tilde(x)))[angle.l GNN_theta (tilde(x)), nabla_(tilde(x)) log p (tilde(x)) angle.r] \
  =& integral_(tilde(x)) p (tilde(x)) angle.l GNN_theta (tilde(x)), nabla_(tilde(x)) log p (tilde(x)) angle.r "d"tilde(x) \
  =& integral_(tilde(x)) p (tilde(x)) angle.l GNN_theta (tilde(x)), (nabla_(tilde(x)) p (tilde(x))) / (p (tilde(x))) angle.r "d"tilde(x) \
  =& integral_(tilde(x)) angle.l GNN_theta (tilde(x)), nabla_(tilde(x)) p (tilde(x)) angle.r "d"tilde(x) \
  =& integral_(tilde(x)) angle.l GNN_theta (tilde(x)), nabla_(tilde(x)) (integral_(x) p (tilde(x)|x)p(x) "d"x) angle.r "d"tilde(x) \
  =& integral_(tilde(x)) angle.l GNN_theta (tilde(x)), integral_(x) p(x) nabla_(tilde(x)) p (tilde(x)|x) "d"x angle.r "d"tilde(x) \
  =& integral_(tilde(x)) angle.l GNN_theta (tilde(x)), integral_(x) p (tilde(x)|x) p(x) nabla_(tilde(x)) log p (tilde(x)|x) "d"x angle.r "d"tilde(x) \
  =& integral_(tilde(x)) integral_(x) p (tilde(x)|x) p(x) angle.l GNN_theta (tilde(x)), nabla_(tilde(x)) log p (tilde(x)|x) angle.r "d"x "d"tilde(x) \
  =& E_(p (tilde(x),x)) [ angle.l GNN_theta (tilde(x)), nabla_(tilde(x)) log p (tilde(x)|x) angle.r ]
$
