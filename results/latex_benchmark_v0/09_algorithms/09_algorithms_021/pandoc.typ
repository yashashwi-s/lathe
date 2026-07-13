#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Algorithm
<algorithm>
This sample contains algorithmic pseudocode extracted from a
source-backed LaTeX benchmark dataset. It is wrapped in a minimal
article document for pdfLaTeX validation.

#block[
#block[
$tau$: Scale of coordinate noise $G N N_theta$: Graph Neural Network
with parameter $theta$ \${\\rm NoiseHead}\_{\\theta\_{n}}\$: Network
module with parameter $theta_n$ for prediction of node-level noise of
each atom \${\\rm LabelHead}\_{\\theta\_{l}}\$: Network module with
parameter $theta_l$ for prediction of graph-level label of $x_i$ $X$:
Training dataset $x_i$: Input conformation $y_i$: Label of $x_i$ $T$:
Training steps $cal(N)$: Gaussian distribution $lambda_p$: Loss weight
of property prediction loss $lambda_n$: Loss weight of Noisy Nodes loss
$x_i\,y_i$ = dataloader($X$) $tilde(x) = x_i + Delta x_i$ , where
$Delta x_i tilde.op cal(N)\(0\,tau^2 I_(3 N)\)$, $N$ is atom number of
$x_i$
\$y\_{i}^{pred}={\\rm LabelHead}\_{\\theta\_{l}}(GNN\_{\\theta}(\\tilde{x}))\$
\$\\Delta{x\_i}^{pred}={\\rm NoiseHead}\_{\\theta\_{n}}(GNN\_{\\theta}(\\tilde{x}))\$
Loss =
$lambda_p$PropertyPredictionLoss$\(y_i^(p r e d)\,y_i\)$+$lambda_n\|\|Delta x_i^(p r e d) - Delta x_i\|\|_2^2$
Optimise(Loss) $T = T - 1$

]
]
