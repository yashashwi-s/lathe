#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Plot Sample 1]
  #v(0.5em)
  #text(size: 14pt)[Dataset-expansion sample]
  #v(1.5em)
]

= Visualization

The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  {
    import cetz.draw: *
    cetz.canvas(length: 0.75pt, {
      let blue = rgb(42, 175, 236)
      let lw = 2.8

      // Draw all edges
      line((328.41, 104.55), (514.77, 239.95), stroke: (paint: blue, thickness: lw))
      line((514.77, 239.95), (443.59, 459.02), stroke: (paint: blue, thickness: lw))
      line((142.06, 239.95), (328.41, 104.55), stroke: (paint: blue, thickness: lw))
      line((142.06, 239.95), (213.24, 459.02), stroke: (paint: blue, thickness: lw))
      line((213.24, 459.02), (443.59, 459.02), stroke: (paint: blue, thickness: lw))
      line((328.41, 104.55), (443.59, 459.02), stroke: (paint: blue, thickness: lw))
      line((142.06, 239.95), (443.59, 459.02), stroke: (paint: blue, thickness: lw))
      line((514.77, 239.95), (213.24, 459.02), stroke: (paint: blue, thickness: lw))
      line((142.06, 239.95), (514.77, 239.95), stroke: (paint: blue, thickness: lw))
      line((328.41, 104.55), (213.24, 459.02), stroke: (paint: blue, thickness: lw))

      // Draw circles (nodes)
      let r = 36.11
      circle((328.41, 104.55), radius: r, stroke: (paint: blue, thickness: lw), fill: white)
      circle((514.77, 239.95), radius: r, stroke: (paint: blue, thickness: lw), fill: white)
      circle((443.59, 459.02), radius: r, stroke: (paint: blue, thickness: lw), fill: white)
      circle((213.24, 459.02), radius: r, stroke: (paint: blue, thickness: lw), fill: white)
      circle((142.06, 239.95), radius: r, stroke: (paint: blue, thickness: lw), fill: white)

      // Node labels (inside circles) - font=\huge ~ 25pt, at 0.75pt scale
      content((328.41, 104.55), text(size: 18.75pt)[$9$])
      content((514.77, 239.95), text(size: 18.75pt)[$9$])
      content((443.59, 459.02), text(size: 18.75pt)[$6$])
      content((213.24, 459.02), text(size: 18.75pt)[$4$])
      content((142.06, 239.95), text(size: 18.75pt)[$4$])

      // External labels (\Large ~ 14pt, at 0.75pt scale)
      // Top node label: "6 5/6" at (314.22, 10.06)
      content((341, 10.06), anchor: "north-west", text(size: 10.5pt)[$6 frac(5,6)$])
      // Right node label: "6 5/6" at (559.22, 217.1)
      content((559.22, 230), anchor: "north-west", text(size: 10.5pt)[$6 frac(5,6)$])
      // Bottom-right label: "6 1/3" at (481.22, 463.1)
      content((481.22, 476), anchor: "north-west", text(size: 10.5pt)[$6 frac(1,3)$])
      // Left node external label: "6" at (80.22, 235.1)
      content((80.22, 248), anchor: "north-west", text(size: 10.5pt)[$6$])
      // Bottom-left external label: "6" at (155.22, 481.1)
      content((155.22, 494), anchor: "north-west", text(size: 10.5pt)[$6$])
    })
  },
  caption: [Source-backed plot.]
)
