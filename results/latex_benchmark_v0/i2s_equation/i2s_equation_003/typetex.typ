#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

$ #mitex(`
\begin{aligned}
&E_{p (\tilde{x})}[\left <GNN_{\theta} (\tilde{x}),\nabla _{\tilde{x}} \log p (\tilde{x})\right > ]\\
=& \int_{\tilde{x}} p (\tilde{x}) \left <GNN_{\theta} (\tilde{x}),\nabla _{\tilde{x}} \log p (\tilde{x})\right > \mathrm{d}\tilde{x} \\
=& \int_{\tilde{x}} p (\tilde{x}) \left <GNN_{\theta} (\tilde{x}),\frac{\nabla _{\tilde{x}} p (\tilde{x})}{p (\tilde{x})}\right > \mathrm{d}\tilde{x} \\
=& \int_{\tilde{x}} \left <GNN_{\theta} (\tilde{x}),\nabla _{\tilde{x}} p (\tilde{x})\right > \mathrm{d}\tilde{x} \\
=& \int_{\tilde{x}} \left<GNN_{\theta} (\tilde{x}),\nabla _{\tilde{x}} \left (\int_{x} p (\tilde{x}|x)p(x) \mathrm{d}x\right ) \right > \mathrm{d}\tilde{x} \\
=& \int_{\tilde{x}} \left <GNN_{\theta} (\tilde{x}), \int_{x} p(x) \nabla _{\tilde{x}} p (\tilde{x}|x) \mathrm{d}x \right > \mathrm{d}\tilde{x} \\
=& \int_{\tilde{x}} \left <GNN_{\theta} (\tilde{x}), \int_{x} p (\tilde{x}|x) p(x) \nabla _{\tilde{x}}\log p (\tilde{x}|x) \mathrm{d}x \right > \mathrm{d}\tilde{x} \\
=& \int_{\tilde{x}} \int_{x} p (\tilde{x}|x) p(x) \left <GNN_{\theta} (\tilde{x}), \nabla _{\tilde{x}}\log p (\tilde{x}|x) \right > \mathrm{d}x \mathrm{d}\tilde{x} \\
=& E_{p (\tilde{x},x)} [ \left <GNN_{\theta} (\tilde{x}), \nabla _{\tilde{x}}\log p (\tilde{x}|x) \right > ]\\
\end{aligned}
`) $
