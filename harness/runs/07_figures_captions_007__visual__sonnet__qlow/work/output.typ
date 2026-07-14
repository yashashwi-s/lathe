#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 1.5em)
#set figure(gap: 10pt, numbering: "1")
#show figure: it => {
  v(12pt)
  it
  v(12pt)
}
#set figure.caption(separator: [: ])
#show heading.where(level: 1): it => {
  v(1.5em, weak: true)
  text(size: 12pt, weight: "bold")[1#h(1em)#it.body]
  v(0.8em, weak: true)
}

#let bs = sym.backslash

#align(center)[
  #v(0.57in)
  #text(size: 17.28pt)[On the Dynamics of Light Wilson Quarks]
  #linebreak()
  #v(0.5em)
  Source-backed arXiv sample
]
#v(0.2em)

= Figure Captions

#figure(
  rect(width: 0.78 * 100%, height: 1.15in, stroke: 0.4pt),
  caption: [Time history of the effective pion mass (distance \$8\$) for \$\u{005C}beta=5.30\$ and \$\u{005C}kappa=0.1677\$ on a \$16^3\u{005C}times 32\$ lattice. Symbols are: (\$\u{005C}times\$) HMC at \$\u{005C}delta\u{005C}tau=0.0069\$, (\$+\$) HMD at \$\u{005C}delta\u{005C}tau=0.0069\$, (\$\u{005C}bigcirc\$) HMD at \$\u{005C}delta\u{005C}tau=0.004\$. Also shown is the blocksize\$=40\$ (\$\u{005C}Diamond\$) HMC acceptance uncorrected for autocorrelations.],
  kind: image,
) <fig:source-1>

Figures 1 through 1 preserve source-backed captions while replacing external graphics with deterministic placeholders.
