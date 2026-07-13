#import "@preview/mitex:0.2.4": *

#mitex(`\begin{pmatrix}
A & B \\
C & D
\end{pmatrix}`)

#mitex(`\begin{pmatrix}
A^{-1} + A^{-1}B(D - CA^{-1}B)^{-1}CA^{-1} & -A^{-1}B(D - CA^{-1}B)^{-1} \\
-(D - CA^{-1}B)^{-1}CA^{-1} & (D - CA^{-1}B)^{-1}
\end{pmatrix}`)

#mitex(`\[
\begin{pmatrix}
A & B \\
C & D
\end{pmatrix}^{-1}
=
\begin{pmatrix}
A^{-1} + A^{-1}B(D - CA^{-1}B)^{-1}CA^{-1} & -A^{-1}B(D - CA^{-1}B)^{-1} \\
-(D - CA^{-1}B)^{-1}CA^{-1} & (D - CA^{-1}B)^{-1}
\end{pmatrix}
\]`)

