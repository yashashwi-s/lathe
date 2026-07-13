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
#strong[Input:] #mi(`\phi`), #mi(`\theta`), initial episodes
#mi(`K_{\mathrm{init}}`), total budget of episodes
#mi(`K_{\mathrm{E}}`), #strong[Init:] #mi(`\phi' \gets \phi`),
#mi(`\theta' \gets \theta`), #mi(`\mathcal{D} \gets \emptyset`) Sample a
batch #mi(`\mathcal{T}`) of #mi(`M`) sequences using pre-trained policy
#mi(`\pi_\theta`) Score each sequence in #mi(`\mathcal{T}`) Add unique,
valid sequences to replay memory #mi(`\mathcal{D}`) Sample a batch
#mi(`\mathcal{T}`) of #mi(`M`) sequences using current policy
#mi(`\pi_\theta`) Score each sequence in #mi(`\mathcal{T}`) Add unique,
valid sequences to replay memory #mi(`\mathcal{D}`)
#mi(`\phi \gets \phi - \lambda_Q \hat{\nabla}_\phi J_Q (\phi \vert \mathcal{T})`)
#mi(`\theta \gets \theta - \lambda_\pi \hat{\nabla}_\theta J_\pi (\theta\vert \mathcal{T})`)
#mi(`\alpha \gets \alpha - \lambda_\alpha \hat{\nabla}_\alpha J_\alpha (\alpha \vert \mathcal{T})`)
#mi(`\phi' \gets \tau \phi' + (1-\tau) \phi`)
#mi(`\theta' \gets \tau \theta' + (1-\tau) \theta`)
#mi(`\phi \gets \phi - \lambda_Q \hat{\nabla}_\phi J_Q (\phi \vert \mathcal{D})`)
#mi(`\theta \gets \theta - \lambda_\pi \hat{\nabla}_\theta J_\pi (\theta\vert \mathcal{D})`)
#mi(`\alpha \gets \alpha - \lambda_\alpha \hat{\nabla}_\alpha J_a (\alpha \vert \mathcal{D})`)
#mi(`\phi' \gets \tau \phi' + (1-\tau) \phi`)
#mi(`\theta' \gets \tau \theta' + (1-\tau) \theta`)

]
]
