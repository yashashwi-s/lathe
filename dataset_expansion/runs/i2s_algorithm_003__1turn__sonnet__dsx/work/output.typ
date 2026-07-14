#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: false)

#align(center)[
  #text(size: 17pt, weight: "bold")[Algorithm Sample 3]
  #v(6pt)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(4pt)
]

#v(4pt)

= Procedure

The pseudocode below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#v(6pt)

#set par(leading: 0.75em)

#let ind = h(1.5em)
#let ind2 = h(3em)
#let ind3 = h(4.5em)
#let ind4 = h(6em)

#block(stroke: (top: 0.5pt, bottom: 0.5pt), inset: (top: 4pt, bottom: 4pt), width: 100%)[
#set text(size: 10.5pt)
#set par(leading: 0.65em)

#v(2pt)
*1* #ind *Initialize* actor network $mu_theta$ and critic networks $Q_(omega_1)$ and $Q_(omega_2)$.

*2* #ind *Initialize* corresponding target networks: $theta' <- theta$, ${omega'}_1 <- omega_1$, ${omega'}_2 <- omega_2$ and choose $rho_"p" in (0, 1)$.

*3* #ind *Initialize* replay buffer $cal(R)$.

*4* #ind *Choose* a batch size $K$, a gradient based optimization algorithm and a corresponding learning rate $lambda_"actor", lambda_"critic" > 0$ for both optimization procedures, a time step size $Delta t$ and a stopping criterion.

*5* #ind *Choose* standard deviation exploration noise $sigma_"expl"$ and lower and upper action bounds $a_"low", a_"high"$.

*6* #ind **Repeat**

*7* #ind2 *Select* clipped action and step the environment dynamics forward.
#v(2pt)
#align(center)[$a = "clip"(mu_theta (s) + epsilon, a_"low", a_"high"), quad epsilon tilde cal(N)(0, sigma_"expl").$]
#v(2pt)

*8* #ind2 *Observe* next state $s'$, reward $r$, and done signal $d$ and store the tuple $(s, a, r, s', d)$ in the replay buffer.

*9* #ind2 **If** $s'$ *is terminal* **then**

*10* #ind3 *Reset* trajectory.

*11* #ind2 **End If**

*12* #ind2 **For** $j$ *in range*(_update frequency_) **do**

*13* #ind3 *Sample* batch $cal(B) = {(s^((k)), a^((k)), r^((k)), {s'}^((k)), d^((k)})}_(k=1)^K$ from replay buffer.

*14* #ind3 *Compute* targets (Clipped Double Q-learning and policy smoothing).
#v(2pt)
#align(center)[$y(r, s', d) = r + (1-d) min_(i=1, 2) { Q_({omega'}_i)(s', tilde(a)) }, quad tilde(a) = "clip"(mu_(theta')(s) + epsilon, a_"low", a_"high"), quad epsilon tilde cal(N)(0, sigma_"target").$]
#v(2pt)

*15* #ind3 *Estimate* critic gradient $nabla_omega L(Q_omega^(mu_theta))$ by
#v(2pt)
#align(center)[$nabla_(omega_i) (1/K sum_(k=1)^K (Q_(omega_i)(s^((k)), a^((k))) - y(r^((k)), {s'}^((k)), d^((k))) )^2 ), quad "for" space i=1,2.$]
#v(2pt)

*16* #ind3 *Update* the critic parameters $omega_i$ based on the optimization algorithm.

*17* #ind3 **If** $j mod$ _policy delay frequency_ $= 0$ **then**

*18* #ind4 *Estimate* actor gradient $nabla_theta J(mu_theta)$ by
#v(2pt)
#align(center)[$nabla_(theta) (1/K sum_(k=1)^K Q_(omega_1)(s^((k)), mu_theta(s^((k)))) ).$]
#v(2pt)

*19* #ind4 *Update* the actor parameters $theta$ based on the optimization algorithm.

*20* #ind4 *Update* target networks softly:
#v(2pt)
#align(center)[$theta' <- rho_"p" theta' + (1 - rho_"p") theta, quad {omega'}_i <- rho_"p" {omega'}_i + (1 - rho_"p") omega_i, quad "for" space i=1, 2.$]
#v(2pt)

*21* #ind3 **End If**

*22* #ind2 **End For**

*23* #ind **Until** stopping criterion is fulfilled.

#v(2pt)
]
