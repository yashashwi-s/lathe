#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center, text(size: 1.5em, weight: "bold")[Aligned Mathematical Structures])
#align(center, [Source-backed grouped formula sample])

= Expressions

*Expression 1.* The following expression is taken from a source-backed formula corpus.

#text("$\Delta_{(n-1 l+1)}^{(1)}(x_1,\dots,x_m|z_1,\dots,z_{n-1}|z_n,\dots,z_N) = q^{l-n+1}\sum_{k=n}^{N} z_k \frac{\prod_{j=1}^{n-1}(z_k-z_j q^{-2})}{\prod_{i=n, i\neq k}^{N} (z_i-z_k)q^{-1}} \Delta^{(n l)}(x_1,\dots,x_m|z_1,\dots, z_{n-1},z_k|z_{n},\dots,z_N)$")

*Expression 2.* The following expression is taken from a source-backed formula corpus.

#text("$[\alpha_{\mathcal{L}}(a),\alpha_{\mathcal{L}}(b),[x,y,z]_{\mathcal{L}}]_{\mathcal{L}} = [[a,b,x]_{\mathcal{L}}, \alpha_{\mathcal{L}}(y), \alpha_{\mathcal{L}}(z)]_{\mathcal{L}}+ [\alpha_{\mathcal{L}}(x),[a,b,y]_{\mathcal{L}},\alpha_{\mathcal{L}}(z)]_{\mathcal{L}}+[\alpha_{\mathcal{L}}(x),\alpha_{\mathcal{L}}(y),[a,b,z]_{\mathcal{L}}]_{\mathcal{L}}$")

*Expression 3.* The following expression is taken from a source-backed formula corpus.

#text("$(II) \quad \begin{pmatrix} x_1+iy_1 \\ x_2+iy_2 \\ x_3+iy_3 \\ x_4+iy_4 \end{pmatrix} \leftrightarrow \frac{1}{\sqrt{2}} \begin{pmatrix} -(y_2+y_4) +j(y_2-y_4) \\ (y_1 + y_3) -j(y_1-y_3) \\ (x_2 + x_4) -j(x_2 - x_4) \\ -(x_1 + x_3) +j(x_1 - x_3) \end{pmatrix}$")

*Expression 4.* The following expression is taken from a source-backed formula corpus.

#text("$(|\partial_t^{\ell}\mathcal{D}^{\alpha}\phi|^2)_t = -2\sum_{\ell_1+|\alpha_1|>0}\partial_t^{\ell}\mathcal{D}^{\alpha}\phi\partial_t^{\ell_1}\mathcal{D}^{\alpha_1}v\cdot\nabla(\partial_t^{\ell_2}\mathcal{D}^{\alpha_2}\phi)-v\cdot\nabla|\partial_t^{\ell}\mathcal{D}^{\alpha}\phi|^2$")

*Expression 5.* The following expression is taken from a source-backed formula corpus.

#table(
  columns: 3,
  [Tr [$\Gamma_{s}(P^{a})\Gamma_{s}(P_{b})$] = $\delta^{a}{}_{b}$], [$\Rightarrow$], [$\Gamma_{s}(P^{a}) = \frac{-i}{2g}\gamma^{a}$],
  [], [], [],
  [Tr [$\Gamma_{s}(M^{ab})\Gamma_{s}(P_{cd})$] = $\delta^{ab}{}_{cd}$], [$\Rightarrow$], [$\Gamma_{s}(M^{ab}) = -\frac{1}{2}\gamma^{ab}$]
)
