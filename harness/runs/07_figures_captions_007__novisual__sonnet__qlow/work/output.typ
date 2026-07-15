#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)
#set heading(numbering: "1")
#set figure.caption(separator: [: ])
#show figure.caption: set align(left)
#show heading.where(level: 1): it => {
  v(15pt)
  text(size: 14.4pt, weight: "bold")[#counter(heading).display() #h(1em) #it.body]
  v(10pt)
}

#v(2em)
#align(center)[
  #block(text(size: 17.28pt, weight: "bold")[On the Dynamics of Light Wilson Quarks])
  #v(1.5em)
  #block(text(size: 12pt)[Source-backed arXiv sample])
  #v(1em)
  #block(text(size: 12pt)[ ])
]
#v(1.5em)

= Figure Captions

#figure(
  box(stroke: 0.4pt, width: 0.78 * 100%, height: 1.15in),
  caption: [Time history of the effective pion mass (distance $8$) for $beta = 5.30$ and $kappa = 0.1677$ on a $16^3 times 32$ lattice. Symbols are: ($times$) HMC at $delta tau = 0.0069$, ($+$) HMD at $delta tau = 0.0069$, (○) HMD at $delta tau = 0.004$. Also shown is the blocksize$=40$ (◇) HMC acceptance uncorrected for autocorrelations.]
) <fig:source-1>

Figures~#ref(<fig:source-1>, supplement: none) through~#ref(<fig:source-1>, supplement: none) preserve source-backed captions while replacing external graphics with deterministic placeholders.
