#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#show heading: set text(font: "New Computer Modern")
#set par(justify: true, leading: 0.55em)

#align(center)[
  #v(1em)
  #text(size: 17pt)[On the Dynamics of Light Wilson Quarks]

  #v(0.8em)
  #text(size: 12pt)[Source-backed arXiv sample]
  #v(1em)
]

#v(1.5em)

= Figure Captions

#v(0.8em)

#figure(
  block(
    width: 78%,
    height: 1.15in,
    stroke: 0.4pt + black,
  )[],
  caption: [Time history of the effective pion mass (distance \$8\$) for \$\\beta=5.30\$ and \$\\kappa=0.1677\$ on a \$16^3\\times 32\$ lattice. Symbols are: (\$\\times\$) HMC at \$\\delta\\tau=0.0069\$, (\$+\$) HMD at \$\\delta\\tau=0.0069\$, (\$\\bigcirc\$) HMD at \$\\delta\\tau=0.004\$. Also shown is the blocksize\$=40\$ (\$\\Diamond\$) HMC acceptance uncorrected for autocorrelations.],
)
#v(1em)

Figures~1 through~1 preserve source-backed captions while replacing external graphics with deterministic placeholders.
