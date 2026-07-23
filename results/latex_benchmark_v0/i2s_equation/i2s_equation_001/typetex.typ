#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

$ #mitex(`\begin{aligned}
\alpha_{3} & \overset{\text{(i)}}{\leq}\sum_{s\in\mathcal{S},a\in\mathcal{A}}d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)\sqrt{\frac{C_{\mathsf{clipped}}^{\star}\log\frac{N}{\mathrm{d} elta}}{N\min\left\{ d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big),\frac{1}{S\left(A+B\right)}\right\} }\mathsf{Var}_{P_{s,a,\nu_{0}(s)}}\left(V_{\mathsf{pe}}^{-}\right)}\nonumber \\
& \leq\sqrt{\frac{C_{\mathsf{clipped}}^{\star}\log\frac{N}{\mathrm{d} elta}}{N}}\sum_{s\in\mathcal{S},a\in\mathcal{A}}\sqrt{d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)\mathsf{Var}_{P_{s,a,\nu_{0}(s)}}\left(V_{\mathsf{pe}}^{-}\right)}\nonumber \\
& \quad+\sqrt{\frac{C_{\mathsf{clipped}}^{\star}S\left(A+B\right)\log\frac{N}{\mathrm{d} elta}}{N}}\sum_{s\in\mathcal{S},a\in\mathcal{A}}\sqrt{d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)}\cdot\sqrt{d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)\mathsf{Var}_{P_{s,a,\nu_{0}(s)}}\left(V_{\mathsf{pe}}^{-}\right)}\nonumber \\
& \overset{\text{(ii)}}{\leq}\sqrt{\frac{C_{\mathsf{clipped}}^{\star}}{N}\log\frac{N}{\mathrm{d} elta}}\cdot\sqrt{SA}\cdot\sqrt{\sum_{s\in\mathcal{S},a\in\mathcal{A}}d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)\mathsf{Var}_{P_{s,a,\nu_{0}(s)}}\left(V_{\mathsf{pe}}^{-}\right)}\nonumber \\
& \quad+\sqrt{\frac{C_{\mathsf{clipped}}^{\star}S\left(A+B\right)\log\frac{N}{\mathrm{d} elta}}{N}}\left[\sum_{s\in\mathcal{S},a\in\mathcal{A}}d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)\right]\sqrt{\sum_{s\in\mathcal{S},a\in\mathcal{A}}d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)\mathsf{Var}_{P_{s,a,\nu_{0}(s)}}\left(V_{\mathsf{pe}}^{-}\right)}\nonumber \\
& \leq2\sqrt{\frac{C_{\mathsf{clipped}}^{\star}S\left(A+B\right)\log\frac{N}{\mathrm{d} elta}}{N}}\sqrt{\sum_{s\in\mathcal{S},a\in\mathcal{A}}d^{\mu^{\star},\nu_{0}}\big(s,a,\nu_{0}(s);\rho\big)\mathsf{Var}_{P_{s,a,\nu_{0}(s)}}\left(V_{\mathsf{pe}}^{-}\right)}\nonumber \\
& \overset{\text{(iii)}}{=}2\sqrt{\frac{C_{\mathsf{clipped}}^{\star}S\left(A+B\right)}{N}\log\frac{N}{\mathrm{d} elta}}\sqrt{\sum_{s\in\mathcal{S}}d^{\mu^{\star},\nu_{0}}\left(s;\rho\right)\mathop{\mathbb{E}}\limits _{a\sim\mu^{\star}(s),b\sim\nu_{0}(s)}\left[\mathsf{Var}_{P_{s,a,b}}\left(V_{\mathsf{pe}}^{-}\right)\right]}\nonumber \\
& \overset{\text{(iv)}}{\leq}2\sqrt{\frac{C_{\mathsf{clipped}}^{\star}S\left(A+B\right)}{N}\log\frac{N}{\mathrm{d} elta}}\sqrt{\sum_{s\in\mathcal{S}}d^{\mu^{\star},\nu_{0}}\left(s;\rho\right)\mathsf{Var}_{P_{s}^{\mu^{\star},\nu_{0}}}\left(V_{\mathsf{pe}}^{-}\right)}.
\end{aligned}`) $
