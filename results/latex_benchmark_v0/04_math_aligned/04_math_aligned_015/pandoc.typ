#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Expressions
<expressions>
==== Expression 1.
<expression-1.>
The following expression is taken from a source-backed formula corpus.

\$\$\\begin{align\*}
 {\\rm P}\_{j,j+i} =&\\sum^{M-j}\_{m=i+1} {M-j \\choose m} \\mathbb{P}\_{\\rm TX}^m \\left(1- \\mathbb{P}\_{\\rm TX}\\right) ^{M-j-m} \\\\ &\\times \\frac{M-j-i}{M-j}m \\cdots (m-i+1)\\mathbb{P}\_K^{m} \\gamma\_i \\gamma\_{m,i} \\\\ &+{M-j \\choose i} \\mathbb{P}\_{\\rm TX}^i \\left(1- \\mathbb{P}\_{\\rm TX}\\right) ^{M-j-i} \\frac{M-j-i}{M-j}i! \\mathbb{P}\_K^{i}\\gamma\_i ,
\\end{align\*}\$\$

==== Expression 2.
<expression-2.>
The following expression is taken from a source-backed formula corpus.

$ Q\(x\) & = sum_(x\/log x lt.eq p lt.eq x - sqrt(x)) pi\(x - p\)+ O #scale(x: 240%, y: 240%)[\(] sum_(p lt.eq x\/log x) pi\(x\)+ sum_(x - sqrt(x) lt.eq p lt.eq x) x #scale(x: 240%, y: 240%)[\)]\
 & = sum_(x\/log x lt.eq p lt.eq x - sqrt(x)) pi\(x - p\)+ O #scale(x: 240%, y: 240%)[\(] pi\(x\)pi #scale(x: 240%, y: 240%)[\(] frac(x, log x) #scale(x: 240%, y: 240%)[\)] + x sqrt(x) #scale(x: 240%, y: 240%)[\)]\
 & = sum_(x\/log x lt.eq p lt.eq x - sqrt(x)) pi\(x - p\)+ O #scale(x: 240%, y: 240%)[\(] frac(x^2, log^3 x) #scale(x: 240%, y: 240%)[\)] . $

==== Expression 3.
<expression-3.>
The following expression is taken from a source-backed formula corpus.

$ partial_(hat(xi)) u\(hat(xi)\,0\)- partial_(hat(xi)) w\(hat(xi)\,0\) & lt.eq partial_(hat(xi)) u\(hat(xi)\,0\)- partial_(hat(xi)) w\(0\,0\)+\[partial_(hat(xi)) hat(w)\]_(0\,beta)\|hat(xi)\|^beta\
 & = [U_beta \( 1 + beta \) cos \(\(1 + beta\)pi / 2\) + \[ partial_(hat(xi)) hat(w) \]_(0\,beta)]\|hat(xi)\|^beta\, $

==== Expression 4.
<expression-4.>
The following expression is taken from a source-backed formula corpus.

$ I I + I I I & arrow.r 0\;\
I V & = integral_(d\(x\,p\)gt.eq rho)\(frac(rho^2, 4 epsilon.alt) - n\)e^(- frac(rho^2, 4 epsilon.alt) - C) arrow.r 0\;\
I & = e^(- C) integral_(\|y\|lt.eq rho / sqrt(epsilon.alt))\(frac(\|y\|^2, 2) - n\)\(2 pi\)^(- n\/2)e^(-\|y\|^2\/4)\(1 + O\(epsilon.alt\|y\|^2\)d y\
 & arrow.r integral_(bb(R)^n)\(frac(\|y\|^2, 2) - n\)\(2 pi\)^(- n\/2)e^(-\|y\|^2\/4) d y = 0 . $

==== Expression 5.
<expression-5.>
The following expression is taken from a source-backed formula corpus.

$ frac(1, omega\(B\)) parallel\(b - b_B\)f_1 parallel_(L_omega^s)^s & = frac(1, omega\(B\)) integral_(5 B)\|b\(y\)- b_B\|^s\|f\|^sd omega\(y\)\
 & lt.eq #scale(x: 180%, y: 180%)[\(] frac(1, omega\(B\)) integral_(5 B)\|b\(y\)- b_B\|^(s s'_1)d omega\(y\)#scale(x: 180%, y: 180%)[\)]^(1 / s'_1) #scale(x: 180%, y: 180%)[\(] frac(1, omega\(B\)) integral_(5 B)\|f\|^(s s_1)d omega\(y\)#scale(x: 180%, y: 180%)[\)]^(1 / s_1)\
 & lt.tilde ell\(B\)^(beta s)parallel b parallel_(Lambda^beta)^s M_(s s_1)^s\(f\)\(x\) $
