#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

$ #mitex(`
\begin{aligned}
v_{mn}^{x}
&=\langle m|v^{x}|n\rangle\\
&=\mathrm{d} elta_{mn}\langle v^{x}\rangle (\frac{k_{x}}{\rho})(-\mathrm{d} elta_{m,0}+\mathrm{d} elta_{m,1})
+(1-\mathrm{d} elta_{mn})\langle v^{x}\rangle (\frac{k_{z}}{\rho}\frac{k_{x}}{\sqrt{k_{x}^{2}+k_{y}^{2}}}-i\frac{k_{y}}{\sqrt{k_{x}^{2}+k_{y}^{2}}})\\
&=\mathrm{d} elta_{mn}\langle v^{x}\rangle ({\rm sin}\theta{\rm cos}\phi)(-\mathrm{d} elta_{m,0}+\mathrm{d} elta_{m,1})
+(1-\mathrm{d} elta_{mn})\langle v^{x}\rangle ({\rm cos}\theta{\rm cos}\phi-i{\rm sin}\phi),\\
v_{mn}^{y}
&=\mathrm{d} elta_{mn}\langle v^{y}\rangle ({\rm sin}\theta{\rm sin}\phi)(-\mathrm{d} elta_{m,0}+\mathrm{d} elta_{m,1})
+(1-\mathrm{d} elta_{mn})\langle v^{y}\rangle ({\rm cos}\theta{\rm sin}\phi-i{\rm cos}\phi),\\
v_{mn}^{z}
&=\mathrm{d} elta_{mn}\langle v^{z}\rangle {\rm cos}\theta(-\mathrm{d} elta_{m,0}+\mathrm{d} elta_{m,1})
+(1-\mathrm{d} elta_{mn})\langle v^{z}\rangle \frac{-{\rm sin}\theta}{\rho},\\
\end{aligned}
`) $
