#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Plot Sample 3]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Visualization

The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  {
    import cetz.draw: *
    cetz.canvas(length: 0.75pt, {
      // Scale factor: x=0.75pt, y=0.75pt, yscale=-1 means y increases downward
      // We'll work in the original coordinate system

      set-style(stroke: (thickness: 1.5pt))

      // Left diagram
      // Horizontal lines
      line((52.05, 101.79), (72.55, 101.79))
      line((112.9, 101.79), (134.4, 101.79))
      // Diagonal up-right from junction
      line((72.55, 101.79), (92.38, 72.25))
      line((92.38, 72.25), (112.9, 101.79))
      // Vertical lines
      line((92.38, 52.84), (92.38, 72.25))
      line((92.38, 131.54), (92.38, 150.45))
      // Bottom splits
      line((104.28, 162.26), (92.38, 150.45))
      line((81.28, 163.26), (92.38, 150.45))
      // Left input splits
      line((40.24, 113.69), (52.05, 101.79))
      line((39.24, 90.69), (52.05, 101.79))

      // Red lines with arrows (left diagram)
      set-style(stroke: (paint: rgb(182, 5, 60), thickness: 1.5pt))
      line((72.55, 101.79), (92.38, 131.54))
      line((112.9, 101.79), (92.38, 131.54))
      // Arrow at (92.38, 131.54) pointing down
      // Approximate arrowhead
      line((92.38, 131.54), (92.38 - 4, 131.54 - 8))
      line((92.38, 131.54), (92.38 + 4, 131.54 - 8))

      // Right diagram - black lines
      set-style(stroke: (paint: black, thickness: 1.5pt))
      line((216.85, 101.79), (237.35, 101.79))
      line((237.35, 101.79), (257.18, 72.25))
      line((257.18, 72.25), (277.7, 101.79))
      line((277.7, 101.79), (299.2, 101.79))
      line((257.18, 52.84), (257.18, 72.25))
      line((257.18, 131.54), (257.18, 150.45))
      line((269.08, 162.26), (257.18, 150.45))
      line((246.08, 163.26), (257.18, 150.45))
      line((245.37, 40.94), (257.18, 52.84))
      line((268.38, 40.11), (257.18, 52.84))

      // Red lines (right diagram)
      set-style(stroke: (paint: rgb(182, 5, 60), thickness: 1.5pt))
      line((237.35, 101.79), (257.18, 131.54))
      line((277.7, 101.79), (257.18, 131.54))
      line((257.18, 131.54), (257.18 - 4, 131.54 - 8))
      line((257.18, 131.54), (257.18 + 4, 131.54 - 8))

      // Labels - using content
      set-style(stroke: none)

      // Right label d (teal)
      content((306, 94.01), text(fill: rgb(6, 79, 97), size: 11pt)[$d$])
      // Left label b (teal)
      content((201.04, 94.61), text(fill: rgb(6, 79, 97), size: 11pt)[$b$])
      // Right gamma (red)
      content((244.74, 104.01), text(fill: rgb(182, 5, 60), size: 9pt)[$gamma$])
      // Left ell_2
      content((55.05, 86.24), text(size: 9pt)[$ell_2$])
      // x_1 right diagram
      content((229.79, 77.79), text(size: 9pt)[$x_1$])
      // x_2 right diagram
      content((268.79, 77.79), text(size: 9pt)[$x_2$])
      // c_1 (teal)
      content((232.83, 24.4), text(fill: rgb(6, 79, 97), size: 11pt)[$c_1$])
      // c_2 (teal)
      content((264.5, 24.4), text(fill: rgb(6, 79, 97), size: 11pt)[$c_2$])
      // d left (teal)
      content((136.63, 94.31), text(fill: rgb(6, 79, 97), size: 11pt)[$d$])
      // a_1 left bottom (teal)
      content((69.38, 163.46), text(fill: rgb(6, 79, 97), size: 11pt)[$a_1$])
      // c top left (teal)
      content((88.18, 35.6), text(fill: rgb(6, 79, 97), size: 11pt)[$c$])
      // gamma left (red)
      content((79.5, 104.01), text(fill: rgb(182, 5, 60), size: 9pt)[$gamma$])
      // h_1 left (dark red)
      content((64.45, 110.51), text(fill: rgb(108, 4, 35), size: 9pt)[$h_1$])
      // ell_1 left
      content((94.38, 134.94), text(size: 9pt)[$ell_1$])
      // x_1 left
      content((68.05, 75.79), text(size: 9pt)[$x_1$])
      // a_2 left bottom (teal)
      content((102.98, 163.46), text(fill: rgb(6, 79, 97), size: 11pt)[$a_2$])
      // x_2 left
      content((101.38, 75.79), text(size: 9pt)[$x_2$])
      // h_2 left (dark red)
      content((106.05, 110.51), text(fill: rgb(108, 4, 35), size: 9pt)[$h_2$])
      // a_1 right bottom (teal)
      content((232.38, 163.46), text(fill: rgb(6, 79, 97), size: 11pt)[$a_1$])
      // a_2 right bottom (teal)
      content((265.98, 163.46), text(fill: rgb(6, 79, 97), size: 11pt)[$a_2$])
      // b_2 far left (teal)
      content((21.29, 78), text(fill: rgb(6, 79, 97), size: 11pt)[$b_2$])
      // b_1 far left (teal)
      content((21.29, 105.61), text(fill: rgb(6, 79, 97), size: 11pt)[$b_1$])
      // h_1 right (dark red)
      content((229.45, 110.51), text(fill: rgb(108, 4, 35), size: 9pt)[$h_1$])
      // h_2 right (dark red)
      content((272.05, 110.51), text(fill: rgb(108, 4, 35), size: 9pt)[$h_2$])
      // ell_1 right
      content((259.18, 134.94), text(size: 9pt)[$ell_1$])
      // ell_2 right
      content((259.18, 56.24), text(size: 9pt)[$ell_2$])
    })
  },
  caption: [Source-backed plot.]
)
