#set page(margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")

#align(center, [
  #text(size: 1.4em, weight: "bold")[How to Put a Heavier Higgs on the Lattice] \
  Source-backed arXiv sample \
  #v(1em)
])

= Figure Captions

#figure(
  box(stroke: 0.5pt, rect(width: 78%, height: 1.15in, fill: none, stroke: none)),
  caption: [Phase diagram from large $N$ calculation],
) <fig:source-1>

#figure(
  box(stroke: 0.5pt, rect(width: 78%, height: 1.15in, fill: none, stroke: none)),
  caption: [Phase diagram from large $N$ calculation],
) <fig:source-2>

Figures @fig:source-1 through @fig:source-2 preserve source-backed captions while replacing external graphics with deterministic placeholders.
