#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.55em, first-line-indent: 1.5em)
#set heading(numbering: "1.")
#show heading: set text(weight: "bold")
#show heading.where(level: 1): it => {
  set text(size: 14.4pt)
  block(above: 1.5em, below: 1em)[
    #counter(heading).display("1")#h(1em)#it.body
  ]
}

#align(center)[
  #v(0.38in)
  #text(size: 17.28pt)[On the Dynamics of Light Wilson Quarks]
  #v(1.4em)
  #text(size: 11pt)[Source-backed arXiv sample]
]

#v(2em)

= Figure Captions

#v(0.6em)

#align(center)[
  #box(
    stroke: 0.4pt + black,
    width: 78% * (100% + 0pt),
    height: 1.15in,
  )[]
]

#v(0.6em)

#[
  #set par(first-line-indent: 0pt, justify: true)
  *Figure 1:* Time history of the effective pion mass (distance \$8\$) for \$\\beta=5.30\$ and \$\\kappa=0.1677\$ on a \$16^3\\times 32\$ lattice. Symbols are: (\$\\times\$) HMC at \$\\delta\\tau=0.0069\$, (\$+\$) HMD at \$\\delta\\tau=0.0069\$, (\$\\bigcirc\$) HMD at \$\\delta\\tau=0.004\$. Also shown is the blocksize\$=40\$ (\$\\Diamond\$) HMC acceptance uncorrected for autocorrelations.
]

Figures 1 through 1 preserve source-backed captions while replacing external graphics with deterministic placeholders.
