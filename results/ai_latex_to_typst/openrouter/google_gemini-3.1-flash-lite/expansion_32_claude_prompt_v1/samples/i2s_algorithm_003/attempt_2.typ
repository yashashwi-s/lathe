#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.4em, weight: "bold")[Algorithm Sample 3] \
  #text(size: 1.2em)[Dataset-expansion sample]
])

= Procedure
The pseudocode below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#let indent = h(2em)

#block(inset: (left: 1em))[
  1. Initialize actor network $mu_theta$ and critic networks $Q_(omega_1)$ and $Q_(omega_2)$. \
  2. Initialize corresponding target networks: $theta' arrow.l theta$, $omega'_1 arrow.l omega_1$, $omega'_2 arrow.l omega_2$ and choose $rho_"p" in (0, 1)$. \
  3. Initialize replay buffer $cal(R)$. \
  4. Choose a batch size $K$, a gradient based optimization algorithm and a corresponding learning rate $lambda_"actor", lambda_"critic" > 0$ for both optimization procedures, a time step size $Delta t$ and a stopping criterion. \
  5. Choose standard deviation exploration noise $sigma_"expl"$ and lower and upper action bounds $a_"low", a_"high"$. \
  *Repeat* \
  #indent Select clipped action and step the environment dynamics forward. \
  #indent $a = "clip"(mu_theta(s) + epsilon, a_"low", a_"high"), quad epsilon tilde cal(N)(0, sigma_"expl")$. \
  #indent Observe next state $s'$, reward $r$, and done signal $d$ and store the tuple $(s, a, r, s', d)$ in the replay buffer. \
  #indent *If* $s'$ is terminal \
  #indent #indent Reset trajectory. \
  #indent *EndIf* \
  #indent *For* $j$ in range(italic("update frequency")) \
  #indent #indent Sample batch $cal(B) = {(s^((k)), a^((k)), r^((k)), s'^((k)), d^((k)))}_(k=1)^K$ from replay buffer. \
  #indent #indent Compute targets (Clipped Double Q-learning and policy smoothing). \
  #indent #indent $y(r, s', d) = r + (1-d) min_(i=1, 2) { Q_(omega'_i)(s', tilde(a)) }, quad tilde(a) = "clip"(mu_(theta')(s) + epsilon, a_"low", a_"high"), quad epsilon tilde cal(N)(0, sigma_"target")$. \
  #indent #indent Estimate critic gradient $nabla_omega L(Q_omega^(mu_theta))$ by \
  #indent #indent $nabla_(omega_i) (1/K sum_(k=1)^K (Q_(omega_i)(s^((k)), a^((k))) - y(r^((k)), s'^((k)), d^((k))))^2), quad "for" quad i=1, 2$. \
  #indent #indent Update the critic parameters $omega_i$ based on the optimization algorithm. \
  #indent #indent *If* $j "mod" italic("policy delay frequency") = 0$ \
  #indent #indent #indent Estimate actor gradient $nabla_theta J(mu_theta)$ by \
  #indent #indent #indent $nabla_theta (1/K sum_(k=1)^K Q_(omega_1)(s^((k)), mu_theta(s^((k))))) $. \
  #indent #indent #indent Update the actor parameters $theta$ based on the optimization algorithm. \
  #indent #indent #indent Update target networks softly: \
  #indent #indent #indent $theta' arrow.l rho_"p" theta' + (1 - rho_"p")theta, quad omega'_i arrow.l rho_"p" omega'_i + (1 - rho_"p")omega_i, quad "for" quad i=1, 2$. \
  #indent #indent *EndIf* \
  #indent *EndFor* \
  *Until* stopping criterion is fulfilled.
]
