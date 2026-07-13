#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
Initialize actor network $mu_theta$ and critic networks $Q_(omega_1)$
and $Q_(omega_2)$. Initialize corresponding target networks:
$theta' arrow.l theta$, $omega'_1 arrow.l omega_1$,
$omega'_2 arrow.l omega_2$ and choose $rho_(upright("p")) in\(0\,1\)$.
Initialize replay buffer $cal(R)$. Choose a batch size $K$, a gradient
based optimization algorithm and a corresponding learning rate
$lambda_(upright("actor"))\,lambda_(upright("critic")) > 0$ for both
optimization procedures, a time step size $Delta t$ and a stopping
criterion. Choose standard deviation exploration noise
$sigma_(upright("expl"))$ and lower and upper action bounds
$a_(upright("low"))\,a_(upright("high"))$. Select clipped action and
step the environment dynamics forward.
$ a = upright("clip")\(mu_theta\(s\)+ epsilon.alt\,a_(upright("low"))\,a_(upright("high"))\)\,quad epsilon.alt tilde.op cal(N)\(0\,sigma_(upright("expl"))\). $
Observe next state $s'$, reward $r$, and done signal $d$ and store the
tuple $\(s\,a\,r\,s'\,d\)$ in the replay buffer. Reset trajectory.
Sample batch
$cal(B) = {\(s^(\(k\))\,a^(\(k\))\,r^(\(k\))\,s'^(\(k\))\,d^(\(k\))\)}_(k = 1)^K$
from replay buffer. Compute targets (Clipped Double Q-learning and
policy smoothing).
$ y\(r\,s'\,d\)= r +\(1 - d\)min_(i = 1\,2) {Q_(omega'_i) \( s' \, tilde(a) \)}\,quad tilde(a) = upright("clip")\(mu_(theta')\(s\)+ epsilon.alt\,a_(upright("low"))\,a_(upright("high"))\)\,quad epsilon.alt tilde.op cal(N)\(0\,sigma_(upright("target"))\). $
Estimate critic gradient $nabla_omega L\(Q_omega^(mu_theta)\)$ by
$ nabla_(omega_i) #scale(x: 300%, y: 300%)[\(] 1 / K sum_(k = 1)^K (Q_(omega_i) \( s^(\(k\)) \, a^(\(k\)) \) - y \( r^(\(k\)) \, s'^(\(k\)) \, d^(\(k\)) \))^2 #scale(x: 300%, y: 300%)[\)]\,quad upright("for") thin thin i = 1\,2 . $
Update the critic parameters $omega_i$ based on the optimization
algorithm. Estimate actor gradient $nabla_theta J\(mu_theta\)$ by
$ nabla_theta #scale(x: 300%, y: 300%)[\(] 1 / K sum_(k = 1)^K Q_(omega_1)\(s^(\(k\))\,mu_theta\(s^(\(k\))\)\)#scale(x: 300%, y: 300%)[\)] . $
Update the actor parameters $theta$ based on the optimization algorithm.
Update target networks softly:
$ theta' arrow.l rho_(upright("p")) theta' +\(1 - rho_(upright("p"))\)theta\,quad omega'_i arrow.l rho_(upright("p")) omega'_i +\(1 - rho_(upright("p"))\)omega_i\,quad upright("for") thin thin i = 1\,2 . $

]
]
