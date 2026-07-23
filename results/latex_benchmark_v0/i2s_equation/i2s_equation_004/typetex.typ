#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

$ #mitex(`
\renewcommand{\arraystretch}{1.5}
\begin{array}
{@{}l@{\:}l@{}}
||f||_{1_{\mu}}+||g||_{1_{\mu}}
& =\int \limits_{x\in \mathcal{D}} |f(x)|+|g(x)| d \mu(x) \\
& = + \int \limits_{\substack{x \in \mathcal{D} \\f(x)\ge 0,g(x)\ge 0, }} f(x)+g(x) d\mu(x)
- \int \limits_{\substack{x \in \mathcal{D} \\f(x)<0,g(x)< 0, }}
f(x)+g(x) d\mu(x) \\
& \quad +\int \limits_{\substack{x \in \mathcal{D} \\f(x)\ge 0,g(x)< 0, }} f(x)-g(x) d\mu(x)
+ \int \limits_{\substack{x \in \mathcal{D} \\f(x)<0,g(x)\ge 0, }} g(x)-f(x) d\mu(x) \\
& = + \int \limits_{\substack{x \in \mathcal{D} \\f(x)\ge 0,g(x)\ge 0,
}} \max(f(x),g(x))+\min(f(x),g(x)) d\mu(x) \\
& \quad - \int \limits_{\substack{x \in \mathcal{D} \\f(x)<0,g(x)< 0, }}
\max(f(x),g(x))+\min(f(x),g(x)) d\mu(x) \\
& \quad +\int \limits_{\substack{x \in \mathcal{D} \\f(x)\ge 0,g(x)<
0, }} \max(f(x),g(x))-\min(f(x),g(x)) d\mu(x) \\
& \quad + \int \limits_{\substack{x \in \mathcal{D} \\f(x)<0,g(x)\ge
0, }} \max(f(x),g(x))-\min(f(x),g(x)) d\mu(x). \\
\end{array}
\renewcommand{\arraystretch}{1}
`) $
