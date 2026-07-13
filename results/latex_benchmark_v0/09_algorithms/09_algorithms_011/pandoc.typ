#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
#strong[Input:] $phi.alt$, $theta$, initial episodes
$K_(upright(i n i t))$, total budget of episodes $K_(upright(E))$,
#strong[Init:] $phi.alt' arrow.l phi.alt$, $theta' arrow.l theta$,
$cal(D) arrow.l nothing$ Sample a batch $cal(T)$ of $M$ sequences using
pre-trained policy $pi_theta$ Score each sequence in $cal(T)$ Add
unique, valid sequences to replay memory $cal(D)$ Sample a batch
$cal(T)$ of $M$ sequences using current policy $pi_theta$ Score each
sequence in $cal(T)$ Add unique, valid sequences to replay memory
$cal(D)$
$phi.alt arrow.l phi.alt - lambda_Q hat(nabla)_phi.alt J_Q\(phi.alt\|cal(T)\)$
$theta arrow.l theta - lambda_pi hat(nabla)_theta J_pi\(theta\|cal(T)\)$
$alpha arrow.l alpha - lambda_alpha hat(nabla)_alpha J_alpha\(alpha\|cal(T)\)$
$phi.alt' arrow.l tau phi.alt' +\(1 - tau\)phi.alt$
$theta' arrow.l tau theta' +\(1 - tau\)theta$
$phi.alt arrow.l phi.alt - lambda_Q hat(nabla)_phi.alt J_Q\(phi.alt\|cal(D)\)$
$theta arrow.l theta - lambda_pi hat(nabla)_theta J_pi\(theta\|cal(D)\)$
$alpha arrow.l alpha - lambda_alpha hat(nabla)_alpha J_a\(alpha\|cal(D)\)$
$phi.alt' arrow.l tau phi.alt' +\(1 - tau\)phi.alt$
$theta' arrow.l tau theta' +\(1 - tau\)theta$

]
]
