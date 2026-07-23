#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithm Sample 3",
  author: "Dataset-expansion sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithm Sample 3]

  #text(size: 1.2em)[Dataset-expansion sample]

]

           /* \maketitle */
== Procedure
 The pseudocode below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
 [1] \State Initialize actor network $\mu_\theta$ and critic networks $Q_{\omega_1}$ and $Q_{\omega_2}$. \State Initialize corresponding target networks: $\theta' \leftarrow \theta$, ${\omega'}_1 \leftarrow \omega_1$, ${\omega'}_2 \leftarrow \omega_2$ and choose $\rho_\text{p} \in(0, 1)$. \State Initialize replay buffer $\mathcal{R}$. \State Choose a batch size $K$, a gradient based optimization algorithm and a corresponding learning rate $\lambda_\text{actor}, \lambda_\text{critic} > 0$ for both optimization procedures, a time step size $\Delta t$ and a stopping criterion. \State Choose standard deviation exploration noise $\sigma_\text{expl}$ and lower and upper action bounds $a_\text{low}, a_\text{high}$. \Repeat \State Select clipped action and step the environment dynamics forward. equation* a= \text{clip}(\mu_\theta(s) + \epsilon, a_\text{low}, a_\text{high}), \quad \epsilon \sim \mathcal{N}(0, \sigma_\text{expl}). equation* \State Observe next state $s'$, reward $r$, and done signal $d$ and store the tuple $(s, a, r, s', d)$ in the replay buffer. \If{$s'$ is terminal} \State Reset trajectory. \EndIf \For{$j$ in range(\textit{update frequency})} \State Sample batch $\mathcal{B} = \{(s^{(k)}, a^{(k)}, r^{(k)}, {s'}^{(k)}, d^{(k)})\}_{k=1}^K$ from replay buffer. \State Compute targets (Clipped Double Q-learning and policy smoothing). equation* y(r, s', d) = r + (1-d) \min \limits_{i=1, 2} \left \{ Q_{{\omega'}_i}(s', \tilde{a}) \right \}, \quad \tilde{a}= \text{clip}(\mu_{\theta'}(s) + \epsilon, a_\text{low}, a_\text{high}), \quad \epsilon \sim \mathcal{N}(0, \sigma_\text{target}). equation* \State Estimate critic gradient $\nabla_\omega L(Q_\omega^{\mu_\theta})$ by equation* \nabla_{\omega_i} \Biggl(\frac{1}{K} \sum \limits_{k=1}^K \left(Q_{\omega_i}(s^{(k)}, a^{(k)}) - y(r^{(k)}, {s'}^{(k)}, d^{(k)}) \right)^2 \Biggr), \quad \text{for} \,\, i=1,2. equation* \State Update the critic parameters $\omega_i$ based on the optimization algorithm. \If{$j \text{ mod } \textit{policy delay frequency} = 0$} \State Estimate actor gradient $\nabla_\theta J(\mu_\theta)$ by equation* \nabla_{\theta} \Biggl(\frac{1}{K} \sum \limits_{k=1}^K Q_{\omega_1}(s^{(k)}, \mu_\theta(s^{(k)})) \Biggr). equation* \State Update the actor parameters $\theta$ based on the optimization algorithm. \State Update target networks softly: equation* \theta' \leftarrow \rho_\text{p} \theta' + (1 - \rho_\text{p})\theta, \quad{\omega'}_i \leftarrow \rho_\text{p} {\omega'}_i + (1 - \rho_\text{p})\omega_i, \quad \text{for} \, \, i=1, 2. equation* \EndIf \EndFor \Until{stopping criterion is fulfilled.} 
```
]

