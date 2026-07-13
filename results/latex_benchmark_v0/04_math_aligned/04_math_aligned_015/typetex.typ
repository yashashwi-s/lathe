#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Expressions
<expressions>
==== Expression 1.
<expression-1.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
 {\rm P}_{j,j+i} =&\sum^{M-j}_{m=i+1} {M-j \choose m} \mathbb{P}_{\rm TX}^m \left(1- \mathbb{P}_{\rm TX}\right) ^{M-j-m} \\ &\times \frac{M-j-i}{M-j}m \cdots (m-i+1)\mathbb{P}_K^{m} \gamma_i \gamma_{m,i} \\ &+{M-j \choose i} \mathbb{P}_{\rm TX}^i \left(1- \mathbb{P}_{\rm TX}\right) ^{M-j-i} \frac{M-j-i}{M-j}i! \mathbb{P}_K^{i}\gamma_i ,
\end{aligned}`) $

==== Expression 2.
<expression-2.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
 Q(x) &= \sum_{x/\log x \le p \le x-\sqrt x} \pi(x-p) + O\bigg( \sum_{p\le x/\log x} \pi(x) + \sum_{x-\sqrt x\le p\le x} x \bigg) \\ &= \sum_{x/\log x \le p \le x-\sqrt x} \pi(x-p) + O\bigg( \pi(x) \pi\bigg( \frac x{\log x} \bigg) + x\sqrt x \bigg) \\ &= \sum_{x/\log x \le p \le x-\sqrt x} \pi(x-p) + O\bigg( \frac{x^2}{\log^3x} \bigg).
\end{aligned}`) $

==== Expression 3.
<expression-3.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
 \partial_{\hat \xi} u(\hat \xi, 0) - \partial_{\hat \xi} w(\hat \xi, 0) & \leq \partial_{\hat \xi} u(\hat \xi, 0) - \partial_{\hat \xi} w(0, 0) + [ \partial_{\hat \xi} \hat w]_{0,\beta} |\hat{\xi}|^\beta \\ & = \left[ U_\beta (1+\beta) \cos{((1+\beta) \frac{\pi}{2})} + [ \partial_{\hat \xi} \hat w]_{0,\beta} \right ] |\hat \xi|^\beta,
\end{aligned}`) $

==== Expression 4.
<expression-4.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
II+III &\rightarrow 0;\\IV&= \int_{d(x,p)\geq \rho}(\frac{\rho^2}{4\epsilon}-n)e^{-\frac{\rho^2}{4\epsilon}-C} \rightarrow 0;\\I&= e^{-C}\int_{|y|\leq \frac{\rho}{\sqrt{\epsilon}}} (\frac{|y|^2}{2}-n) (2\pi)^{-n/2} e^{-|y|^2/4}(1+O(\epsilon |y|^2) dy \\&\rightarrow \int_{\mathbb{R}^n} (\frac{|y|^2}{2}-n) (2\pi)^{-n/2} e^{-|y|^2/4} dy=0.
\end{aligned}`) $

==== Expression 5.
<expression-5.>
The following expression is taken from a source-backed formula corpus.

$ #mitex(`\begin{aligned}
\frac1{\omega(B)}\|(b-b_B)f_1\|^s_{L^s_\omega}&=\frac1{\omega(B)}\int_{5B} |b(y)-b_B|^s|f|^sd\omega(y) \\&\le { \Big(\frac1{\omega(B)}\int_{5B} |b(y)-b_B|^{ss_1'}d\omega(y) \Big)^{\frac1{s_1'}}} \Big(\frac1{\omega(B)}\int_{5B} |f|^{ss_1} d\omega(y)\Big)^{\frac1{s_1}}\\ &\lesssim \ell(B)^{\beta s}\|b\|^s_{\Lambda^\beta} M^s_{ss_1}(f)(x)
\end{aligned}`) $
