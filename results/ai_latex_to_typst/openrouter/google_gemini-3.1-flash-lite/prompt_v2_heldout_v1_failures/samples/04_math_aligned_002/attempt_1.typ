#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

= Aligned Mathematical Structures

#text("Source-backed grouped formula sample")

== Expressions

#par[Expression 1. The following expression is taken from a source-backed formula corpus.]

#table(columns: 3, align: center,
  [#text("$\\psi^{\\dagger} \\psi$")], [#text("$\\Rightarrow$")], [#text("$\\beta\\int_{\\alpha_-}^{\\alpha_+}{dp \\over 2\\pi}={\\beta\\over 2\\pi}(\\alpha_+-\\alpha_-)$")],
  [#text("${1\\over \\beta^2}{\\partial \\psi^{\\dagger} \\over \\partial \\lambda}{\\partial \\psi \\over \\partial \\lambda}$")], [#text("$\\Rightarrow$")], [#text("${\\beta\\over 2\\pi}\\int dp \\, p^2={\\beta \\over 6\\pi}(\\alpha_+^3 +-\\alpha_-^3)$")],
  [#text("$\\cdots$")], [#text("$\\cdots$")], [#text("$\\cdots$")]
)

#par[Expression 2. The following expression is taken from a source-backed formula corpus.]

$ x = "text"("epsilon"^-1 (R_n R_{n+1}) log^(2N-3)(( (R_n R_{n+1}) / "epsilon" )^((R_n R_{n+1})/2) (N-1) / "eta" )) $

$ y = "text"("log"^4(( (R_n R_{n+1}) / "epsilon" )^(1/2) "log"^(N-1)( ( (R_n R_{n+1}) / "epsilon" )^((R_n R_{n+1})/2) (N-1) / "eta" )) "log" product_{j != n} I_j) $

#par[Expression 3. The following expression is taken from a source-backed formula corpus.]

#text("$C_n(x)=\\min\\{L_n(x)+\\int_0^\\infty C_{n-1}(x-\\xi)f_n(\\xi) \\mathrm{d}\\xi, \\min_{x< y \\leq x+B} \\{K+v(y-x)+L_n(y)+\\int_0^\\infty C_{n-1}(y-\\xi)f_n(\\xi) \\mathrm{d}\\xi\\}\\}$")

#text("$G_n(x)=vx + L_n(x)+\\int_0^\\infty C_{n-1}(x-\\xi)f_n(\\xi) \\mathrm{d}\\xi$")

#text("$C_n(x)=-vx + \\min\\{G_n(x),K + \\min_{x\\leq y \\leq x+B} G_n(y)\\}$")

#par[Expression 4. The following expression is taken from a source-backed formula corpus.]

#text("$\\left \\{ j^{\\mu}(x) = \\lim_{y\\rightarrow x}\\frac{1}{2}(\\bar{\\psi}(x)\\gamma^{\\mu}\\psi(y) + \\bar{\\psi}(y)\\gamma^\\mu\\psi(x)) = -\\frac{\\beta}{2\\pi}\\epsilon^{\\mu\\nu}\\partial_{\\nu}\\phi(x) \\right.$")

#text("$\\frac{4\\pi}{\\beta^2} = 1 + g/\\pi$")

#text("$\\frac{m_0^2}{\\beta^2}\\cos \\beta\\phi = Z M \\bar{\\psi}\\psi$")

#par[Expression 5. The following expression is taken from a source-backed formula corpus.]

#table(columns: 3, align: center,
  [#text("$\\{ U^1_{\\alpha} \\}$")], [#text("$\\stackrel{ \\rho_{V, \\{ U^1_{\\alpha} \\}} }{ \\longleftarrow }$")], [#text("$\\{ U^1_{\\alpha} |_V \\}$")],
  [#text("$\\scriptstyle{ \\rho_{12} } \\uparrow$")], [], [#text("$\\uparrow \\scriptstyle{ \\rho_{V, 12} }$")],
  [#text("$\\{ U^2_{\\alpha} \\}$")], [#text("$\\stackrel{ \\rho_{V, \\{ U^2_{\\alpha} \\} } }{ \\longleftarrow }$")], [#text("$\\{ U^2_{\\alpha} |_V \\}$")]
)
