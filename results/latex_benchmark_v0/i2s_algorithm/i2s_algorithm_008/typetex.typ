#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Procedure
<procedure>
The pseudocode below is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

#block[
+ Input: data #mi(`y_{1:T}`), level #mi(`l\in\mathbb{N}`), particle
  number #mi(`N\in\mathbb{N}`) and parameter #mi(`\theta\in\Theta`).

+ Initialize: For #mi(`i\in\{1,\mathrm{d} ots,N\}`), independently
  generate #mi(`\overline{W}_{\Delta_l:1}^{i,l}`) from
  #mi(`\mathcal{N}(0,\Delta_l)`). For
  #mi(`(i,k)\in\{1,\mathrm{d} ots,N\}\times\{1,\mathrm{d} ots,\Delta_{l-1}^{-1}\}`)
  set
  #mi(`\overline{W}_{k\Delta_{l-1}}^{i,l-1} = \overline{W}_{2k\Delta_{l}}^{i,l} + \overline{W}_{(2k-1)\Delta_{l}}^{i,l}.`)
  Set #mi(`t=1`), #mi(`\hat{\tilde{p}}^N(y_{1:0})=1`) for convention and
  go to step 3.

+ Iterate: For #mi(`i\in\{1,\mathrm{d} ots,N\}`) compute
  $ #mitex(`\tilde{u}_t^i = \frac{\max\{\kappa_{t,l}(\overline{w}_{\Delta_l:t}^{i,l}),\kappa_{t,l-1}(\overline{w}_{\Delta_{l-1}:t}^{i,l-1})\}}{\sum_{j=1}^N\max\{\kappa_{t,l}(\overline{w}_{\Delta_l:t}^{j,l}),\kappa_{t,l-1}(\overline{w}_{\Delta_{l-1}:t}^{j,l-1})\}}.`) $
  Set
  #mi(`\hat{p}^N(y_{1:t})={\hat{p}^N(y_{1:t-1})}\tfrac{1}{N}\sum_{i=1}^N\max\{\kappa_{t,l}(\overline{w}_{\Delta_l:t}^{i,l}),\kappa_{t,l-1}(\overline{w}_{\Delta_{l-1}:t}^{i,l-1})\}`).
  Then sample
  #mi(`(\overline{w}_{\Delta_l:t}^{1:N,l},\overline{w}_{\Delta_{l-1}:t}^{1:N,l-1})`)
  with replacement from
  #mi(`(\overline{w}_{\Delta_l:t}^{1:N,l},\overline{w}_{\Delta_{l-1}:t}^{1:N,l-1})`)
  using probabilities #mi(`\tilde{u}_t^{1:N}`). For
  #mi(`i\in\{1,\mathrm{d} ots,N\}`), independently generate
  #mi(`\overline{W}_{t+\Delta_l:t+1}^i`) from
  #mi(`\mathcal{N}(0,\Delta_l)`). For
  #mi(`(i,k)\in\{1,\mathrm{d} ots,N\}\times\{1,\mathrm{d} ots,\Delta_{l-1}^{-1}\}`)
  set
  #mi(`\overline{W}_{t+k\Delta_{l-1}}^{i,l-1} = \overline{W}_{t+2k\Delta_{l}}^{i,l} + \overline{W}_{t+(2k-1)\Delta_{l}}^{i,l}.`)
  Set #mi(`t=t+1`) and if #mi(`t=T`) go to step 4, otherwise restart
  step 3.

+ Grand Selection: For #mi(`i\in\{1,\mathrm{d} ots,N\}`) compute
  #mi(`\tilde{u}_T^i = \frac{\max\{\kappa_{T,l}(\overline{w}_{\Delta_l:T}^{i,l}),\kappa_{T,l-1}(\overline{w}_{\Delta_{l-1}:T}^{i,l-1})\}}{\sum_{j=1}^N\max\{\kappa_{T,l}(\overline{w}_{\Delta_l:T}^{j,l}),\kappa_{T,l-1}(\overline{w}_{\Delta_{l-1}:T}^{j,l-1})\}}.`)
  Set
  #mi(`\hat{p}^N(y_{1:T})=\hat{p}^N(y_{1:T-1})\tfrac{1}{N}\sum_{i=1}^N
  \max\{\kappa_{T,l}(\overline{w}_{\Delta_l:T}^{i,l}),\kappa_{T,l-1}(\overline{w}_{\Delta_{l-1}:T}^{i,l-1})\}`).
  Sample one
  #mi(`(\overline{w}_{\Delta_l:T}^l, \overline{w}_{\Delta_{l-1}:T}^{l-1})`)
  from
  #mi(`(\overline{w}_{\Delta_l:T}^{1:N,l},\overline{w}_{\Delta_{l-1}:T}^{1:N,l-1})`)
  using #mi(`\tilde{u}_T^{1:N}`) and go to step 5.

+ Output: trajectories
  #mi(`(\overline{w}_{\Delta_l:T}^l,\overline{w}_{\Delta_{l-1}:T}^{l-1})`)
  and normalizing constant estimate #mi(`\hat{\tilde{p}}^N(y_{1:T})`).

]
