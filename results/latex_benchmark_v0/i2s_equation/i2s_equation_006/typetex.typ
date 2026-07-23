#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

$ #mitex(`\begin{aligned}
G_{c_p} &(b,c_p)\\
&=
- W^{-1} \Big( \varphi (b) \int_0^b \psi(z,0) \frac{\partial}{\partial c_p} \pi_1(z,c_p)m'(z)dz + \psi(b,0)\int_b^\infty \varphi(z) \frac{\partial}{\partial c_p} \pi_1(z,c_p)m'(z)dz \Big), \\
G_{b c_p} &(b,c_p) \\
&= - W^{-1} \Big( \varphi' (b) \int_0^b \psi(z,0) \frac{\partial}{\partial c_p} \pi_1(z,c_p)m'(z)dz
+ \varphi (b) \psi(b,0) \frac{\partial}{\partial c_p} \pi_1 (b, c_p) m'(b) \\
&\hspace{1cm} + \psi '(b,0)\int_b^\infty \varphi(z) \frac{\partial}{\partial c_p} \pi_1(z,c_p)m'(z)dz - \varphi (b) \psi(b,0) \frac{\partial}{\partial c_p} \pi_1 (b, c_p) m'(b) \Big) \\
&= - W^{-1} \Big( \varphi' (b) \int_0^b \psi(z,0) \frac{\partial}{\partial c_p} \pi_1(z,c_p)m'(z)dz + \psi '(b,0)\int_b^\infty \varphi(z) \frac{\partial}{\partial c_p} \pi_1(z,c_p)m'(z)dz \Big).
\end{aligned}`) $
