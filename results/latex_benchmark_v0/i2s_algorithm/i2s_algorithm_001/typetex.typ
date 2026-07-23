#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Procedure
<procedure>
The pseudocode below is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

#block[
For #mi(`\beta\in (1,\frac{3}{2})`) set
#mi(`\varepsilon = \frac{3}{2}-\beta`) and
#mi(`T = L^{2(1-\varepsilon)}`). For #mi(`i=1,\cdots,d`), solve for the
approximate first-order corrector #mi(`\phi_{i,T}^{(L)}`): $ #mitex(`
\mathrm{d} frac{1}{T}\phi_{i,T}^{(L)}-\nabla \cdot a \nabla \phi_{i,T}^{(L)} =\nabla\cdot ae_i \, \mbox{ in }Q_{2L}, \hspace{0.3in} \phi_{i,T}^{(L)}=0 \, \mbox{ on }\partial Q_{2L}.
`) $ Calculate the approximate homogenized coefficients via $ #mitex(`
a_h^{(L)}e_i=\int \omega q_{i,T}^{(L)},
`) $ where $ #mitex(`
q_{i,T}^{(L)}:=a(e_i+\nabla\phi_{i,T}^{(L)})
`) $ and #mi(`\omega(x)=\frac{1}{L^d}\hat{\omega}(\frac{x}{L})`) with
#mi(`\hat{\omega}`) as in Theorem [thm:luottooptimal.] Find
#mi(`\tilde{u}_h^{(L)}`) on #mi(`\partial Q_L`): $ #mitex(`
\tilde{u}_h^{(L)} =\int G_h^{(L)}* (\nabla\cdot g),
`) $where
#mi(`G_h^{(L)}(x) := \frac{1}{4\pi\left|(a_h^{(L)})^{-1/2}x\right|}`) is
the Green function for the constant-coefficient operator
#mi(`-\nabla\cdot a_h^{(L)} \nabla`). Solve for approximate first-order
flux correctors
#mi(`\sigma_{i,T}^{(L)}=\{\sigma_{ijk,T}^{(L)}\}_{j,k}`): $ #mitex(`
\mathrm{d} frac{1}{T}\sigma_{ijk,T}^{(L)}-\Delta \sigma_{ijk,T}^{(L)} =\partial_j q_{ik,T}^{(L)}-\partial_k q_{ij,T}^{(L)} \, \mbox{ in }Q_{\frac{7}{4}L}, \hspace{0.3in} \sigma_{ijk,T}^{(L)}=0 \, \mbox{ on }\partial Q_{\frac{7}{4}L}.
`) $ Solve for approximate second-order correctors
#mi(`\psi_{ij,T}^{(L)}`): $ #mitex(`
\mathrm{d} frac{1}{T}\psi_{ij,T}^{(L)} - \nabla\cdot a \nabla \psi_{ij,T}^{(L)} = \nabla\cdot (\phi_{i,T}^{(L)}a-\sigma_{i,T}^{(L)})e_j \, \mbox{ in }Q_{\frac{3}{2}L}, \hspace{0.3in} \psi_{ij,T}^{(L)}=0 \,\mbox{ on }\partial Q_{\frac{3}{2}L}.
`) $ For the indices $ #mitex(`
(i,j)\in \mathcal{J}=\{(1,2),(1,3),(2,3),(2,2),(3,3)\},
`) $ calculate $ #mitex(`
c_{ij,T}^{(L)}=-\int g\cdot \nabla \Bigl(\sum_{k=1}^3\phi_{k,T}^{(L)}\partial_k v_{h,ij}^{(L)}+(2-\mathrm{d} elta_{ij})(\psi_{ij,T}^{(L)}-\mathrm{d} frac{a_{hij}^{(L)}}{a_{h11}^{(L)}}\psi_{11,T}^{(L)})\Bigr) ,
`) $ where #mi(`v_{h,ij}^{(L)}`) denote the #mi(`a_h^{(L)}`)-harmonic
polynomials $ #mitex(`
v_{h,ij}^{(L)}=(1-\mathrm{d} frac{1}{2}\mathrm{d} elta_{ij})(x_ix_j-\mathrm{d} frac{a_{hij}^{(L)}}{a_{h11}^{(L)}}x_1^2).
`) $ Obtain #mi(`u_h^{(L)}`) as $ #mitex(`
u_h^{(L)}=\tilde{u}_h^{(L)}+ \sum_{i=1}^3(\int g \cdot\nabla \phi_{i,T}^{(L)})\partial_i G_h^{(L)} +\sum_{(i,j)\in\mathcal{J}}c_{ij,T}^{(L)}\partial_{ij} G_h^{(L)}.
`) $ Solve for #mi(`u^{(L)}`) (here and for the rest of the paper we
adopt Einstein's summation convention for repeated indices): $ #mitex(`
-\nabla \cdot a \nabla u^{(L)}=\nabla \cdot g\text{ in }Q_L,\hspace{0.3in} u^{(L)}=(1+\phi_{i,T}^{(L)}\partial_i+\psi_{ij,T}^{(L)}\partial_{ij}) u_h^{(L)}\text{ on }\partial Q_L.
`) $

]
