#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(justify: true)

#align(center)[
  #text(size: 17pt, weight: "bold")[On the Dynamics of Light Wilson Quarks]

  #v(6pt)
  #text(size: 12pt)[Source-backed arXiv sample]
  #v(12pt)
]

= Figure Captions

#figure(
  rect(width: 0.78 * 100%, height: 1.15in, stroke: 0.4pt),
  caption: [Time history of the effective pion mass (distance $8$) for $beta=5.30$ and $kappa=0.1677$ on a $16^3 times 32$ lattice. Symbols are: ($times$) HMC at $delta tau=0.0069$, ($+$) HMD at $delta tau=0.0069$, ($circle.stroked.big$) HMD at $delta tau=0.004$. Also shown is the blocksize$=40$ ($Diamond$) HMC acceptance uncorrected for autocorrelations.],
) <fig:source-1>

Figures~@fig:source-1 through~@fig:source-1 preserve source-backed captions while replacing external graphics with deterministic placeholders.
