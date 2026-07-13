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
#strong[Inputs:] #mi(`s,i,d,a,r,e,v,h`), daily vaccinations
#strong[Output:]
#mi(`\vec{\beta}_{uu}, \vec{\beta}_{vu}, \vec{\beta}_{vv}`),
#mi(`\vec{\beta}_{uv}`) #strong[Initialization:] #mi(`n=7`) or
#mi(`n= 14`) Select window #mi(`z_{j}=\{j-n+1,...,j\}`) Initialize
parameters #mi(`\beta_{uu}`), #mi(`\beta_{vu}`), #mi(`\beta_{vv}`),
#mi(`\beta_{uv}`) Calculate the initial cost
#mi(`C_{j}(n,i,d,\hat{i}_{j},\hat{d}_{j})`) #mi(`flag=0`) Create the
trial parameters set #mi(`P_{k}`) Calculate a cost using every parameter
from #mi(`P_{k}`) set Find the minimum of all costs
#mi(`C_{j}'(n,i,d,\hat{i}_{j},\hat{d}_{j})`)
#mi(`C_{j}(n,i,d,\hat{i}_{j},\hat{d}_{j}) = C_{j}'(n,i,d,\hat{i}_{j},\hat{d}_{j})`)
Keep the modified infection rate and create new set of trial parameters
#mi(`P_{k}'`) #mi(`flag=1`)

]
]
