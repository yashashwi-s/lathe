#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 11",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 11]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic[1] \Statex \textbf{Input:} $\phi$, $\theta$, initial episodes $K_{\mathrm{init}}$, total budget of episodes $K_{\mathrm{E}}$, \Statex \textbf{Init:} $\phi' \gets \phi$, $\theta' \gets \theta$, $\mathcal{D} \gets \emptyset$ \For{each initial episode $1,\dots,K_{\mathrm{init}}$} \State Sample a batch $\mathcal{T}$ of $M$ sequences using pre-trained policy $\pi_\theta$ \State Score each sequence in $\mathcal{T}$ \State Add unique, valid sequences to replay memory $\mathcal{D}$ \EndFor \For{each episode $K_{\mathrm{init}}+1,\dots,K_{\mathrm{E}}$} \State Sample a batch $\mathcal{T}$ of $M$ sequences using current policy $\pi_\theta$ \State Score each sequence in $\mathcal{T}$ \State Add unique, valid sequences to replay memory $\mathcal{D}$ \State$\phi \gets \phi- \lambda_Q \hat{\nabla}_\phi J_Q (\phi \vert \mathcal{T})$ \Comment{On-policy update of Q-function parameters} \State$\theta \gets \theta- \lambda_\pi \hat{\nabla}_\theta J_\pi(\theta \vert \mathcal{T})$ \Comment{On-policy update of policy parameters} \State$\alpha \gets \alpha- \lambda_\alpha \hat{\nabla}_\alpha J_\alpha(\alpha \vert \mathcal{T})$ \Comment{On-policy update of temperature} \State$\phi' \gets \tau \phi' + (1-\tau) \phi$ \Comment{Update target parameters} \State$\theta' \gets \tau \theta' + (1-\tau) \theta$ \Comment{Update average policy parameters} \For{each off-policy update} \State$\phi \gets \phi- \lambda_Q \hat{\nabla}_\phi J_Q (\phi \vert \mathcal{D})$ \State$\theta \gets \theta- \lambda_\pi \hat{\nabla}_\theta J_\pi(\theta \vert \mathcal{D})$ \State$\alpha \gets \alpha- \lambda_\alpha \hat{\nabla}_\alpha J_a (\alpha \vert \mathcal{D})$ \State$\phi' \gets \tau \phi' + (1-\tau) \phi$ \State$\theta' \gets \tau \theta' + (1-\tau) \theta$ \EndFor \EndFor algorithmic 
```
]

