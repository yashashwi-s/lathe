#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= Derivation
<derivation>
The following display is drawn from a source-backed image-to-LaTeX
benchmark and reproduced verbatim.

\$\$\\begin{equation\*}
\\renewcommand{\\arraystretch}{1.5}
\\begin{array}
{\@{}l\@{\\:}l\@{}}
||f||\_{1\_{\\mu}}+||g||\_{1\_{\\mu}}
& =\\int \\limits\_{x\\in \\mathcal{D}} |f(x)|+|g(x)| d \\mu(x) \\\\
& = + \\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\\ge 0,g(x)\\ge 0, }} f(x)+g(x) d\\mu(x)
- \\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\<0,g(x)\< 0, }}
f(x)+g(x) d\\mu(x) \\\\
& \\quad +\\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\\ge 0,g(x)\< 0, }} f(x)-g(x) d\\mu(x)
+ \\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\<0,g(x)\\ge 0, }} g(x)-f(x) d\\mu(x) \\\\
& = + \\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\\ge 0,g(x)\\ge 0,
}} \\max(f(x),g(x))+\\min(f(x),g(x)) d\\mu(x) \\\\
& \\quad - \\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\<0,g(x)\< 0, }}
\\max(f(x),g(x))+\\min(f(x),g(x)) d\\mu(x) \\\\
& \\quad +\\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\\ge 0,g(x)\<
0, }} \\max(f(x),g(x))-\\min(f(x),g(x)) d\\mu(x) \\\\
& \\quad + \\int \\limits\_{\\substack{x \\in \\mathcal{D} \\\\f(x)\<0,g(x)\\ge
0, }} \\max(f(x),g(x))-\\min(f(x),g(x)) d\\mu(x). \\\\
\\end{array}
\\renewcommand{\\arraystretch}{1}
\\end{equation\*}\$\$
