#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Expressions
<expressions>
==== Expression 1.
<expression-1.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
 \begin{array}{lll}\text{\rm minimize} & C \cdot U \hat{X}U^T \\ \text{\rm subject to} & A_i \cdot U \hat{X}U^T = b_i \;\; \forall i \in \{1,\ldots,m\} \\& \hat{X} \in \mathbb{S}^d_{+}\end{array} \begin{array}{lll}\text{\rm maximize} & b^Ty \\ \text{\rm subject to} & U^T (C - \sum^{m}_{i=1} y_i A_i) U \in \mathbb{S}^d_{+}, \\ \\\end{array}
\end{aligned}`) $

==== Expression 2.
<expression-2.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
q\cdot N_d&=\sum_{x,y,z\in\mathbb{F}_q}\theta(zE_d(x,y))\\&=q^2+\sum_{z\in\mathbb{F}_{q}^{\times}}\theta(zb)+\sum_{y,z\in\mathbb{F}_{q}^{\times}}\theta(bz)\theta(-zy^2)+\sum_{x,z\in\mathbb{F}_{q}^{\times}}\theta(zx^d)\theta(zax)\theta(zb)\\&+\sum_{x,y,z\in\mathbb{F}_{q}^{\times}}\theta(x^dz)\theta(axz)\theta(bz)\theta(-zy^2)\\&=q^2+A+B+C+D.
\end{aligned}`) $

==== Expression 3.
<expression-3.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
M = \frac{1}{\sqrt{1+{\bf \bar{w}} \cdot {\bf w} - {1\over 4}({\bf w}\times{\bf {\bar w}})^2 }}\left(\begin{array}{cc}1- {i\over 2}({\bf w} \times {\bf \bar{w}})\cdot {\bf \sigma} & -{\bf w} \cdot {\bf \sigma}\\begin{aligned}2ex]{\bf \bar{w}} \cdot {\bf \sigma} & 1+ {i\over 2}({\bf w} \times {\bf\bar{w}})\cdot {\bf \sigma}\end{array}\right)
\end{aligned}`) $

==== Expression 4.
<expression-4.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
U(\vec{a},1)\left(S, f_\alpha \otimes \rho(E^\alpha)\right) :=& e^{-i[\hat{f}_0\cdot\hat{H}(\vec{a}, \rho) + \hat{f}_1\cdot \hat{P}(\vec{a},\rho)]}\left(S+\vec{a}, f_\alpha(\cdot - \vec{a}) \otimes \rho(E^\alpha)\right) \\=& e^{i[a^0 \hat{H}(\rho) - a^1\hat{P}(\rho)]}\left(S+\vec{a}, f_\alpha(\cdot - \vec{a}) \otimes \rho(E^\alpha)\right).
\end{aligned}`) $

==== Expression 5.
<expression-5.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
I_1 & = (-\infty, \omega_{\xi}^{\ast} - \frac{\alpha \xi^{\alpha}}{2(1 - \alpha)}], \\I_2 & = [\omega_{\xi}^{\ast} - \frac{\alpha \xi^{\alpha}}{2(1 - \alpha)}, \omega_{\xi}^{\ast} + \frac{\alpha \xi^{\alpha}}{2(1 - \alpha)}],\\I_3 & = [\omega_{\xi}^{\ast} + \frac{\alpha \xi^{\alpha}}{2(1 - \alpha)}, 0], \text{ and } \\I_4 & = [0, \infty).
\end{aligned}`) $
