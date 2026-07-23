#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

$  & E_(p\(tilde(x)\))\[⟨G N N_theta \( tilde(x) \) \, nabla_(tilde(x)) log p \( tilde(x) \)⟩\]\
= & integral_(tilde(x)) p\(tilde(x)\)⟨G N N_theta \( tilde(x) \) \, nabla_(tilde(x)) log p \( tilde(x) \)⟩ upright(d) tilde(x)\
= & integral_(tilde(x)) p\(tilde(x)\)⟨G N N_theta \( tilde(x) \) \, frac(nabla_(tilde(x)) p\(tilde(x)\), p\(tilde(x)\))⟩ upright(d) tilde(x)\
= & integral_(tilde(x)) ⟨G N N_theta \( tilde(x) \) \, nabla_(tilde(x)) p \( tilde(x) \)⟩ upright(d) tilde(x)\
= & integral_(tilde(x)) ⟨G N N_theta \( tilde(x) \) \, nabla_(tilde(x)) (integral_x p \( tilde(x) \| x \) p \( x \) upright(d) x)⟩ upright(d) tilde(x)\
= & integral_(tilde(x)) ⟨G N N_theta \( tilde(x) \) \, integral_x p \( x \) nabla_(tilde(x)) p \( tilde(x) \| x \) upright(d) x⟩ upright(d) tilde(x)\
= & integral_(tilde(x)) ⟨G N N_theta \( tilde(x) \) \, integral_x p \( tilde(x) \| x \) p \( x \) nabla_(tilde(x)) log p \( tilde(x) \| x \) upright(d) x⟩ upright(d) tilde(x)\
= & integral_(tilde(x)) integral_x p\(tilde(x)\|x\)p\(x\)⟨G N N_theta \( tilde(x) \) \, nabla_(tilde(x)) log p \( tilde(x) \| x \)⟩ upright(d) x upright(d) tilde(x)\
= & E_(p\(tilde(x)\,x\))\[⟨G N N_theta \( tilde(x) \) \, nabla_(tilde(x)) log p \( tilde(x) \| x \)⟩\]\
 $
