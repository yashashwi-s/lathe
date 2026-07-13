#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
#strong[Input:]` Set of sequences(S)`
#strong[Output:]` Distance Matrix(D)`
` `$E s_1 arrow.l e n c o d e d #h(0em) s_1$
` `$C s_1 arrow.l G z i p #h(0em) c o m p r e s s e d #h(0em) E s_1$
` `$L s_1 arrow.l l e n g t h #h(0em) o f #h(0em) C s_1$
` `$D\_l o c a l arrow.l\[med\]$
` `$E s_2 arrow.l e n c o d e d #h(0em) s_2$
` `$C s_2 arrow.l G z i p #h(0em) c o m p r e s s e d #h(0em) E s_2$
` `$L s_2 arrow.l l e n g t h #h(0em) o f #h(0em) C s_2$
` `$s_1 s_2 arrow.l C o n c a t e n a t e\(s_1\,s_2\)$
` `$E s_1 s_2 arrow.l e n c o d e d #h(0em) s_1 s_2$
` `$C s_1 s_2 arrow.l G z i p #h(0em) c o m p r e s s e d #h(0em) E s_1 s_2$
` `$L s_1 s_2 arrow.l l e n g t h #h(0em) o f #h(0em) C s_1 s_2$ NCD
$arrow.l$
$frac(L s_1 s_2 - M i n\(L s_1\,L s_2\), M a x\(L s_1\,L s_2\))$
` `$D\_l o c a l . a p p e n d\(N C D\)$
$D . a p p e n d\(D\_l o c a l\)$ return $D$

]
]
