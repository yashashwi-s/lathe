#import "@preview/mitex:0.2.4": *
#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
= References And Citations
<sec:refs>
This sample cites source keys [halpkit] and [moretal.] Section~@sec:refs
and Equation~[eq:source-demo] provide cross-reference coverage.
$ #mitex(`

a^2 + b^2 = c^2
`) $

#block[
9 Source bibliography entry 1 extracted from arXiv metadata/source key
'halpkit'. Source bibliography entry 2 extracted from arXiv
metadata/source key 'moretal'. Source bibliography entry 3 extracted
from arXiv metadata/source key 'irrcons'. Source bibliography entry 4
extracted from arXiv metadata/source key 'schratro'.

]
