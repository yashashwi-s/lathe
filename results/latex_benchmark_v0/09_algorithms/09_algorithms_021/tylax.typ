#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Algorithmic Pseudocode Sample 21",
  author: "Source-backed Image2Struct algorithm sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Algorithmic Pseudocode Sample 21]

  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample]

]

           /* \maketitle */
== Algorithm
 This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

 #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
[htbp] \caption{Source-backed algorithmic procedure} algorithmic[1] \Require \Statex$\tau$: Scale of coordinate noise \Statex$GNN_{\theta}$: Graph Neural Network with parameter $\theta$ \Statex${\rm NoiseHead}_{\theta_{n}}$: Network module with parameter $\theta_{n}$ for prediction of node-level noise of each atom \Statex${\rm LabelHead}_{\theta_{l}}$: Network module with parameter $\theta_{l}$ for prediction of graph-level label of $x_{i}$ \Statex$X$: Training dataset \Statex$x_i$: Input conformation \Statex$y_i$: Label of $x_i$ \Statex$T$: Training steps \Statex$\mathcalN$: Gaussian distribution \Statex$\lambda_{p}$: Loss weight of property prediction loss \Statex$\lambda_{n}$: Loss weight of Noisy Nodes loss \While{$T \neq0$} \State$x_i, y_i$ = dataloader($X$) \Comment{random sample $x_i$ and corresponding label $y_i$ from $X$} \State$\tilde{x} = x_{i} + \Delta{x_i}$ , where $\Delta{x_i} \sim \mathcal{N}(0, {\tau}^2I_{3N})$, $N$ is atom number of $x_i$ \State$y_{i}^{pred}={\rm LabelHead}_{\theta_{l}}(GNN_{\theta}(\tilde{x}))$ \State$\Delta{x_i}^{pred}={\rm NoiseHead}_{\theta_{n}}(GNN_{\theta}(\tilde{x}))$ \State Loss = $\lambda_{p}$PropertyPredictionLoss$(y_{i}^{pred}, y_i)$+$\lambda_{n}||\Delta{x_i}^{pred} - \Delta{x_i}||_{2}^{2}$ \State Optimise(Loss) \State$T = T - 1$ \EndWhile algorithmic 
```
]

