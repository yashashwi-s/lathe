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
#mi(`\tau`): Scale of coordinate noise #mi(`GNN_{\theta}`): Graph Neural
Network with parameter #mi(`\theta`)
#mi(`{\rm NoiseHead}_{\theta_{n}}`): Network module with parameter
#mi(`\theta_{n}`) for prediction of node-level noise of each atom
#mi(`{\rm LabelHead}_{\theta_{l}}`): Network module with parameter
#mi(`\theta_{l}`) for prediction of graph-level label of #mi(`x_{i}`)
#mi(`X`): Training dataset #mi(`x_i`): Input conformation #mi(`y_i`):
Label of #mi(`x_i`) #mi(`T`): Training steps #mi(`\mathcal N`): Gaussian
distribution #mi(`\lambda_{p}`): Loss weight of property prediction loss
#mi(`\lambda_{n}`): Loss weight of Noisy Nodes loss #mi(`x_i, y_i`) =
dataloader(#mi(`X`)) #mi(`\tilde{x} = x_{i} + \Delta{x_i}`) , where
#mi(`\Delta{x_i} \sim \mathcal{N}(0, {\tau}^2I_{3N})`), #mi(`N`) is atom
number of #mi(`x_i`)
#mi(`y_{i}^{pred}={\rm LabelHead}_{\theta_{l}}(GNN_{\theta}(\tilde{x}))`)
#mi(`\Delta{x_i}^{pred}={\rm NoiseHead}_{\theta_{n}}(GNN_{\theta}(\tilde{x}))`)
Loss =
#mi(`\lambda_{p}`)PropertyPredictionLoss#mi(`(y_{i}^{pred}, y_i)`)+#mi(`\lambda_{n}||\Delta{x_i}^{pred} - \Delta{x_i}||_{2}^{2}`)
Optimise(Loss) #mi(`T = T - 1`)

]
]
