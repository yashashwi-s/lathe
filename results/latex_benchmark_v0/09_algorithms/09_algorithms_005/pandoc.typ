#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
#smallcaps[LSH] $d\,n in bb(N)_(+)$ $K\,L in bb(N)_(+)$
$p_(upright(n e a r))\,p_(upright(f a r)) in\(0\,1\)$ For $l in L$,
$cal(T)_l :=\[n\]$ $cal(R) :=\[n\]$
$cal(H) := { f in cal(H) : bb(R)^d arrow.r\[M\]}$ For $l in\[L\]$,
$cal(H)_l in cal(H)^K$ For $b in\[M^K\]$, $cal(S)_b :=$AVL tree
#smallcaps[ChooseHashFunc]\($k\,L$)
#smallcaps[ConstructHashTable]\(${ x_i }_(i in\[n\])$)
$cal(R) arrow.l 0$
$cal(R) arrow.l cal(R) union cal(T)_l$.#smallcaps[Retrieve]\($cal(H)_l\(q\)$)
$cal(H)_l\(z\)$.#smallcaps[Insert]\($z$)
$cal(H)_l\(x_i\)$.#smallcaps[Delete]\($x_i$)

]
]
