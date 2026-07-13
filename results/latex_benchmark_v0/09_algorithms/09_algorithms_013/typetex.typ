#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
Initialize actor network #mi(`\mu_\theta`) and critic networks
#mi(`Q_{\omega_1}`) and #mi(`Q_{\omega_2}`). Initialize corresponding
target networks: #mi(`\theta' \leftarrow \theta`),
#mi(`{\omega'}_1 \leftarrow \omega_1`),
#mi(`{\omega'}_2 \leftarrow \omega_2`) and choose
#mi(`\rho_\text{p} \in (0, 1)`). Initialize replay buffer
#mi(`\mathcal{R}`). Choose a batch size #mi(`K`), a gradient based
optimization algorithm and a corresponding learning rate
#mi(`\lambda_\text{actor}, \lambda_\text{critic} > 0`) for both
optimization procedures, a time step size #mi(`\Delta t`) and a stopping
criterion. Choose standard deviation exploration noise
#mi(`\sigma_\text{expl}`) and lower and upper action bounds
#mi(`a_\text{low}, a_\text{high}`). Select clipped action and step the
environment dynamics forward. $ #mitex(`
a= \text{clip}(\mu_\theta(s) + \epsilon, a_\text{low}, a_\text{high}), \quad \epsilon \sim \mathcal{N}(0, \sigma_\text{expl}).
`) $ Observe next state #mi(`s'`), reward #mi(`r`), and done signal
#mi(`d`) and store the tuple #mi(`(s, a, r, s', d)`) in the replay
buffer. Reset trajectory. Sample batch
#mi(`\mathcal{B} = \{(s^{(k)}, a^{(k)}, r^{(k)}, {s'}^{(k)}, d^{(k)})\}_{k=1}^K`)
from replay buffer. Compute targets (Clipped Double Q-learning and
policy smoothing). $ #mitex(`
y(r, s', d) = r + (1-d) \min\limits_{i=1, 2} \left\{ Q_{{\omega'}_i}(s', \tilde{a}) \right\}, \quad \tilde{a}= \text{clip}(\mu_{\theta'}(s) + \epsilon, a_\text{low}, a_\text{high}), \quad \epsilon \sim \mathcal{N}(0, \sigma_\text{target}).
`) $ Estimate critic gradient
#mi(`\nabla_\omega L(Q_\omega^{\mu_\theta})`) by $ #mitex(`
\nabla_{\omega_i} \Biggl(\frac{1}{K} \sum\limits_{k=1}^K \left(Q_{\omega_i}(s^{(k)}, a^{(k)}) - y(r^{(k)}, {s'}^{(k)}, d^{(k)}) \right)^2 \Biggr), \quad \text{for} \,\, i=1,2.
`) $ Update the critic parameters #mi(`\omega_i`) based on the
optimization algorithm. Estimate actor gradient
#mi(`\nabla_\theta J(\mu_\theta)`) by $ #mitex(`
\nabla_{\theta} \Biggl(\frac{1}{K} \sum\limits_{k=1}^K Q_{\omega_1}(s^{(k)}, \mu_\theta(s^{(k)})) \Biggr).
`) $ Update the actor parameters #mi(`\theta`) based on the optimization
algorithm. Update target networks softly: $ #mitex(`
\theta' \leftarrow \rho_\text{p} \theta' + (1 - \rho_\text{p})\theta, \quad
{\omega'}_i \leftarrow \rho_\text{p} {\omega'}_i + (1 - \rho_\text{p})\omega_i, \quad \text{for} \, \, i=1, 2.
`) $

]
]
