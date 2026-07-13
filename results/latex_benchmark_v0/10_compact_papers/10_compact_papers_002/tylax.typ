#set heading(numbering: "1.")
#set math.equation(numbering: "1.")
#set document(
  title: "Spectral Density Study of the SU(3) Deconfining Phase Transition",
  author: "Nelsons A. Alves, Bernd Al. Berg and Sergiu Sanielevici",
)

#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

#align(center)[
  #text(size: 2em, weight: "bold")[Spectral Density Study of the SU(3) Deconfining Phase Transition]

  #text(size: 1.2em)[Nelsons A. Alves, Bernd Al. Berg and Sergiu Sanielevici]

]

          /* \maketitle */
#block(width: 100%, inset: 1em)[
  #align(center)[#text(weight: "bold")[Abstract]]

 We present spectral density reweighting techniques adapted to the analysis of a time series of data with a continuous range of allowed values. In a first application we analyze action and Polyakov line data from a Monte Carlo simulation on \$L\_t L^3 (L\_t=2,4)\$ lattices for the SU(3) deconfining phase transition. We calculate partition function zeros, as well as maxima of the specific heat and of the order parameter susceptibility. Details and warnings are given concerning i) autocorrelations in computer time and ii) a reliable extraction of partition function zeros. The finite size scaling analysis of these data leads to precise results for the critical couplings \$\beta\_c\$, for the critical exponent \$\nu\$ and for the latent heat \$\triangle s\$. In both cases (\$L\_t=2\$ and 4), the first order nature of the transition is substantiated.

]

== Introduction

 We present spectral density reweighting techniques adapted to the analysis of a time series of data with a continuous range of allowed values. In a first application we analyze action and Polyakov line data from a Monte Carlo simulation on math expression lattices for the SU(3) deconfining phase transition. We calculate partition function zeros, as well as maxima of the specific heat and of the order parameter susceptibility. Details and warnings are given concerning i) autocorrelations in computer time and ii) a reliable extraction of partition function zeros. The finite size scaling analysis of these data leads to precise results for the critical couplings math expression , for the critical exponent math expression and for the latent heat math expression . In both cases ( math expression and 4), the first order nature of the transition is substantiated.

== Method

 math expression && 10,000 && 120,000 ~(360) && 5.094 && 5.026 && 5.1550 && 0.4060 && 0.4710 math expression && 10,000 && 120,000 ~(120) && 5.090 && 5.042 && 5.1220&& 0.4080 && 0.4610 math expression && 10,000 && 120,000 ~~(30) && 5.090 && 5.050 && 5.1080 && 0.4090 && 0.4550 math expression && 10,000 && 120,000 ~~(12) && 5.092 && 5.064 && 5.1070 && 0.4110 && 0.4540 math expression && 10,000 && 120,000 ~~(12) && 5.095 && 5.078 && 5.1140 && 0.4130 && 0.4580

 $  L(theta) = sum_(i = 1)^(n) ell(x_(i), theta)  $ <eq-compact>
 Equation @eq-compact is included to keep the sample paper-like while remaining small.

== Conclusion

 math expression && 10,000 && 120,000 (1300) && 5.570 && 5.488 && 5.6710 && 0.4960 && 0.5560 math expression && 10,000 && 120,000 (2080) && 5.610 && 5.533 && 5.7350 && 0.5120 && 0.5640 math expression && 10,000 && 120,000 (3000) && 5.640 && 5.566 && 5.7650 && 0.5220 && 0.5690

