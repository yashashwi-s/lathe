#set page(paper: "us-letter", margin: 1in)
#set text(font: ("New Computer Modern", "Latin Modern Roman", "CMU Serif", "Times New Roman"), size: 11pt)
#set par(justify: true, leading: 0.55em, first-line-indent: 1.5em)

// \maketitle equivalent
#align(center)[
  #v(2em)
  #text(size: 17.28pt)[On the Dynamics of Light Wilson Quarks]
  #v(1.5em)
  #text(size: 12pt)[Source-backed arXiv sample]
  #v(1em)
  #text(size: 12pt)[ ]
  #v(1.5em)
]

// \section{Figure Captions}
#block(above: 1.4em, below: 0.8em)[
  #text(size: 14.4pt, weight: "bold")[1#h(1em)Figure Captions]
]

// Figure — intextsep=12pt above; abovecaptionskip=10pt
#v(12pt)
#align(center)[
  #box(stroke: 0.4pt, width: 78%, height: 1.15in)
]
#v(10pt)

// Caption: "Figure 1: ..." — normal weight paragraph, justified, full text width
#par(justify: true, first-line-indent: 0em)[
  #text("Figure 1: Time history of the effective pion mass (distance $8$) for $\\beta=5.30$ and $\\kappa=0.1677$ on a $16^3\\times 32$ lattice. Symbols are: ($\\times$) HMC at $\\delta\\tau=0.0069$, ($+$) HMD at $\\delta\\tau=0.0069$, ($\\bigcirc$) HMD at $\\delta\\tau=0.004$. Also shown is the blocksize$=40$ ($\\Diamond$) HMC acceptance uncorrected for autocorrelations.")
]

#v(12pt)

Figures#h(0.25em)1 through#h(0.25em)1 preserve source-backed captions while replacing external graphics with deterministic placeholders.
