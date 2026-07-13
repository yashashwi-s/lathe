#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Extracted Lists
<extracted-lists>
The list environments below are extracted from arXiv LaTeX source and
wrapped for pdfLaTeX validation.

+ If we analytically continue along a simple loop around $z = 0$ in the
  counterclockwise direction, $t$ becomes $t + 1$. (It will be
  convenient to also introduce $q = e^(2 pi i t)$, which remains
  single-valued near $z = 0$\.)

+ There are cycles $gamma_0$ and $gamma_1$ such that
  $integral_(gamma_0) omega\(z\)$ is single valued near $z = 0$, and
  $ t = frac(integral_(gamma_1) omega\(z\), integral_(gamma_0) omega\(z\)) $
  in an angular sector near $z = 0$.

+ There is a period function for $omega\(z\)$,
  $ f_0\(z\):= integral_(gamma_0) omega\(z\) $ which is single-valued
  near $z = 0$. This period function is unique up to multiplication by a
  constant. (This implies that the cycle $gamma_0$ is also unique up to
  a constant multiple.)

  In particular, the family of meromorphic $n$-forms
  $ tilde(omega)\(z\):= frac(omega\(z\), integral_(gamma_0) omega\(z\)) $
  will have the property that
  $ integral_gamma tilde(omega)\(z\)equiv 1 $ for some $gamma$, and it
  is the unique such family up to constant multiple.

+ Fixing a choice of period function $f_0\(z\)$ as in part (1), there is
  a period function $ f_1\(z\):= integral_(gamma_1) omega\(z\) $ such
  that $phi\(z\):= f_1\(z\)\/f_0\(z\)$ transforms as
  $ phi\(z\)mapsto phi\(z\)+ 1 $ upon transport around $z = 0$ in the
  counterclockwise direction. The ratio $phi\(z\)$ is unique up to the
  addition of a constant.
