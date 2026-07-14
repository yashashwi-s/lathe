#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Algorithmic Pseudocode Sample 9] \
  Source-backed Image2Struct algorithm sample
])

= Algorithm
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  block(inset: 10pt, stroke: 0.5pt, [
    #set enum(numbering: "1.")
    #let indent = h(2em)
    + $t arrow.l 1; m_1 arrow.l 1_bar(C); alpha arrow.l 1$ #h(1fr) // Step t = 1
    + #for e in range(1, 2) [for $e arrow.l 1, ..., E$]
      #indent FBP() #h(1fr) // Algorithm @FBP:alg
    + $bar(s)_1 arrow.l "mean of" tilde(s) "across data"$
    + #for t in range(2, 3) [for $t arrow.l 2, ..., T$] #h(1fr) // Steps $t >= 2$
      #indent // Phase 1
      #indent $bar(s)_t arrow.l bar(s)_(t-1); alpha arrow.l 1/2; m_t arrow.l m_(t-1)$
      #indent #for e in range(1, 2) [for $e arrow.l 1, ..., E_1$]
        #indent #indent FBP()
      #indent $bar(s) arrow.l "mean of" tilde(s) "on data"$ #h(1fr) // Phase 2
      #indent $bar(s)_t arrow.l 1/2(bar(s)_t + bar(s))$
      #indent #for e in range(1, 2) [for $e arrow.l E_1 + 1, ..., E_2$]
        #indent #indent $alpha arrow.l max {alpha - 1/(2(E_2 - E_1)), 0}$
        #indent #indent FBP()
      #indent // Indices that sort an array; Phase 3
      #indent $R = "argsort" { bar(s)_t[i] : m_t[i] = 1 }$
      #indent $D_t arrow.l {R[0], ..., R[C_(t-1) - C_t]}$
      #indent #for e in range(1, 2) [for $e arrow.l E_2 + 1, ..., E_3$]
        #indent #indent $m_t arrow.l max {m_t - (I[i]_(i in D_t)) / (E_3 - E_2), 0_bar(C)}$
        #indent #indent FBP()
      #indent #for e in range(1, 2) [for $e arrow.l E_3 + 1, ..., E$] #h(1fr) // Phase 4
        #indent #indent FBP()
      #indent Cache $cal(T)_t, m_t, bar(s)_t$ for equation @Outer_Loop:eq
  ]),
  caption: [Source-backed algorithmic procedure]
)
