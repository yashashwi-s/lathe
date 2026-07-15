#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.55em, first-line-indent: 1.5em)
#set heading(numbering: "1")
#show heading: set block(above: 1.4em, below: 1em)
#show heading.where(level: 1): set text(size: 14pt, weight: "bold")

#align(center)[
  #v(0.57in)
  #text(size: 17.28pt)[On the Dynamics of Light Wilson Quarks]

  #v(0.8em)
  #text(size: 11pt)[Source-backed arXiv sample]
]

#v(2em)

= Figure Captions

#v(0.5em)

#align(center)[
  #box(width: 0.78 * (100% - 0pt), height: 1.15in, stroke: 0.4pt)
]

#v(0.8em)

#block(above: 0.6em)[
  #set par(justify: true, first-line-indent: 0em)
  #let bs = "\u{5C}"
  Figure 1: #h(0.6em) Time history of the effective pion mass (distance \$8\$) for \$#bs;beta=5.30\$ and \$#bs;kappa=0.1677\$ on a \$16^3#bs;times 32\$ lattice. Symbols are: (\$#bs;times\$) HMC at \$#bs;delta#bs;tau=0.0069\$, (\$+\$) HMD at \$#bs;delta#bs;tau=0.0069\$, (\$#bs;bigcirc\$) HMD at \$#bs;delta#bs;tau=0.004\$. Also shown is the blocksize\$=40\$ (\$#bs;Diamond\$) HMC acceptance uncorrected for autocorrelations.
]

Figures~1 through~1 preserve source-backed captions while replacing external graphics with deterministic placeholders.
