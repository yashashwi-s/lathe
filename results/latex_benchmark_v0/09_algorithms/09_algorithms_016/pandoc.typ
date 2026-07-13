#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
$n\,p in bb(N)\,omega in\[0\,1\]\,x in bb(R)^n\,v in bb(R)^n$. Find a
sorting permutation $sigma$ of vector $x$. Apply the $sigma$ to $x$ and
$v$, in place. . $v_i arrow.l v_(i - 1)$ $v_1 arrow.l 0$ Identify the
set of groups $G$ of elements of $v$ corresponding to equal entries in
$x$. $tilde(v) arrow.l v$ Calculate sum $upright(bold(s))$ of $v$'s
elements in group $g$. Set $0$ in all $tilde(v)$'s elements in group
$g$. Set the $tilde(v)$'s first element in group $g$ to
$upright(bold(s))$. Set the $tilde(v)$'s last element in group $g$ to
$upright(bold(s))$. $c_(tilde(omega)) arrow.l$ cumulative sum of
$tilde(v)$ $c arrow.l omega c_1 +\(1 - omega\)c_0$ Multiplication and
addition element-wise. Find the inverse of $sigma$. Apply the
$sigma^(- 1)$ to $c$. $c$

]
]
