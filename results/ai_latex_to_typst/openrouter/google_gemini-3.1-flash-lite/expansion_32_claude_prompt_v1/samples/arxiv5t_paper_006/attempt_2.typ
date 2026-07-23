#set page(paper: "us-letter", margin: (left: 0.75in, right: 0.75in, top: 1in, bottom: 1in))
#set text(font: "Libertinus Serif", size: 10pt)

#align(center)[
  #text(size: 18pt, weight: "bold")[Professional Network Matters: Connections Empower Person-Job Fit]
  #v(1em)
  #text(size: 12pt)[Hao Chen, et al.]
]

#v(1em)

#heading(level: 1, numbering: none)[Abstract]
#include "src/0-abstract.tex"

#text(weight: "bold")[Keywords:] Person-Job Fit, Heterogeneous Information Network, Graph Neural Network

#v(1em)

#include "src/1-introduction.tex"
#include "src/2-relatedwork.tex"
#include "src/3-method.tex"
#include "src/4-experiment.tex"
#include "src/5-conclusion.tex"

#pagebreak()
#heading(level: 1, numbering: none)[Appendix]

#bibliography("ref.bib", style: "ieee")
