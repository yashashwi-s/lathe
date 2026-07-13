#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Fractional Superstrings with Space-Time Critical Dimensions Four and Six",
  author: "Source-backed arXiv sample",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Fractional Superstrings with Space-Time Critical Dimensions Four and Six]

  #text(size: 1.2em)[Source-backed arXiv sample]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]
   We propose possible new string theories based on local world-sheet symmetries corresponding to extensions of the Virasoro algebra by fractional spin currents. They have critical central charges \$c=6(K+8)/(K+2)\$ and Minkowski space-time dimensions \$D=2+16/K\$ for \$K\geq2\$ an integer. We present evidence for their existence by constructing modular invariant partition functions and the massless particle spectra. The dimension \$4\$ and \$6\$ strings have space-time supersymmetry.
]

== References And Citations
 <sec-refs> This sample cites source keys #cite(<GSW>) and #cite(<KMQ>). Section @sec-refs and Equation @eq-source-demo provide cross-reference coverage. $  a^(2) + b^(2) = c^(2)  $ <eq-source-demo>

= References

#show figure.where(kind: "bib"): it => block[#it.caption #it.body]
#figure(kind: "bib", supplement: none, caption: [1])[ Source bibliography entry 1 extracted from arXiv metadata/source key `GSW`. ] <GSW>
#figure(kind: "bib", supplement: none, caption: [2])[ Source bibliography entry 2 extracted from arXiv metadata/source key `KMQ`. ] <KMQ>
#figure(kind: "bib", supplement: none, caption: [3])[ Source bibliography entry 3 extracted from arXiv metadata/source key `BNY`. ] <BNY>
#figure(kind: "bib", supplement: none, caption: [4])[ Source bibliography entry 4 extracted from arXiv metadata/source key `ZFpara`. ] <ZFpara>

