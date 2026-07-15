#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Plot Sample 5]
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
      set-style(stroke: (thickness: 1.5pt))

      let teal = rgb(6, 79, 97)
      let red1 = rgb(182, 5, 60)
      let red2 = rgb(108, 4, 35)

      // Scale transform: xscale=0.9, yscale=-0.9 (y inverted)
      // We apply manually by scaling coordinates: x*0.9, y*0.9 with y flipped
      // Origin shift to make y positive: find max y ~ 165 pts * 0.9 = 148.5
      // We'll use a group with transform

      // Helper: transform point (px, py) with xscale=0.9, yscale=-0.9
      // Since yscale is negative, y is flipped. We add offset to shift into view.
      // max raw y ~ 165 => scaled y = -0.9*165 = -148.5 => offset +148.5
      let yoff = 148.5
      let T(px, py) = (px * 0.9, -py * 0.9 + yoff)

      // --- Graph 1 (leftmost) ---
      line(..T(46,49.17), ..T(71,47.17))
      line(..T(71,47.17), ..T(96.5,71.67))
      line(..T(81.72,127.45), ..T(95,106.17))
      line(..T(96.5,71.67), ..T(125,58.67))
      line(..T(108.72,126.95), ..T(95,106.17))
      line(..T(96.5,71.67), ..T(95,106.17))
      line(..T(58,24.67), ..T(71,47.17))

      // Labels graph 1
      content(T(30.33,44.93), anchor: "north-west", text(fill: teal, size: 10pt)[$b_1$])
      content(T(69.74,129.69), anchor: "north-west", text(fill: teal, size: 10pt)[$a_1$])
      content(T(128.24,49.69), anchor: "north-west", text(fill: teal, size: 10pt)[$c$])
      content(T(105.24,129.19), anchor: "north-west", text(fill: teal, size: 10pt)[$a_2$])
      content(T(99.8,83.3), anchor: "north-west", text(size: 9pt)[$ell_1$])
      content(T(41.33,7.93), anchor: "north-west", text(fill: teal, size: 10pt)[$b_2$])
      content(T(82.8,43.8), anchor: "north-west", text(size: 9pt)[$ell_2$])

      // --- Graph 2 (middle) ---
      line(..T(219.57,50.17), ..T(239.06,62.77))
      line(..T(239.06,62.77), ..T(286.44,62.77))
      // Red arrow from 239.06,62.77 to 263.58,109.26
      line(..T(239.06,62.77), ..T(263.58,109.26), stroke: (paint: red1, thickness: 1.5pt), mark: (end: "straight"))
      // Red arrow from 286.44,62.77 to 263.58,109.26
      line(..T(286.44,62.77), ..T(263.58,109.26), stroke: (paint: red1, thickness: 1.5pt), mark: (end: "straight"))
      line(..T(286.44,62.77), ..T(307.3,51.04))
      line(..T(263.58,109.26), ..T(264,131.96))
      line(..T(307.3,51.04), ..T(318,33.67))
      line(..T(307.3,51.04), ..T(325,59.67))
      line(..T(219.57,50.17), ..T(207,33.17))
      line(..T(200.5,55.17), ..T(219.57,50.17))

      // Labels graph 2
      content(T(319.83,20.22), anchor: "north-west", text(fill: teal, size: 10pt)[$b_1$])
      content(T(184.24,48.98), anchor: "north-west", text(fill: teal, size: 10pt)[$a_1$])
      content(T(259.24,133.98), anchor: "north-west", text(fill: teal, size: 10pt)[$c$])
      content(T(327,53.07), anchor: "north-west", text(fill: teal, size: 10pt)[$b_2$])
      content(T(252.2,74.99), anchor: "north-west", text(fill: red1, size: 9pt)[$gamma$])
      content(T(226.1,41.29), anchor: "north-west", text(size: 9pt)[$ell_1$])
      content(T(293.8,59.59), anchor: "north-west", text(size: 9pt)[$ell_2$])
      content(T(258.2,49.99), anchor: "north-west", text(size: 9pt)[$x$])
      content(T(188.24,22.48), anchor: "north-west", text(fill: teal, size: 10pt)[$a_2$])

      // --- Graph 3 (rightmost) ---
      line(..T(420.57,50.17), ..T(440.06,62.77))
      line(..T(440.06,62.77), ..T(487.44,62.77))
      // Red arrow from 440.06,62.77 to 464.58,109.26
      line(..T(440.06,62.77), ..T(464.58,109.26), stroke: (paint: red1, thickness: 1.5pt), mark: (end: "straight"))
      // Red arrow from 487.44,62.77 to 464.58,109.26
      line(..T(487.44,62.77), ..T(464.58,109.26), stroke: (paint: red1, thickness: 1.5pt), mark: (end: "straight"))
      line(..T(487.44,62.77), ..T(508.3,51.04))
      line(..T(464.58,109.26), ..T(465,131.96))
      line(..T(420.57,50.17), ..T(408,33.17))
      line(..T(401.5,55.17), ..T(420.57,50.17))
      line(..T(465,131.96), ..T(448.5,147.67))
      line(..T(465,131.96), ..T(480.5,148.17))

      // Labels graph 3
      content(T(384.33,45.72), anchor: "north-west", text(fill: teal, size: 10pt)[$b_1$])
      content(T(437.74,150.48), anchor: "north-west", text(fill: teal, size: 10pt)[$a_1$])
      content(T(392,16.57), anchor: "north-west", text(fill: teal, size: 10pt)[$b_2$])
      content(T(455.2,74.99), anchor: "north-west", text(fill: red1, size: 9pt)[$gamma$])
      content(T(466.6,114.29), anchor: "north-west", text(size: 9pt)[$ell_1$])
      content(T(428.3,39.09), anchor: "north-west", text(size: 9pt)[$ell_2$])
      content(T(459.2,47.99), anchor: "north-west", text(size: 9pt)[$x$])
      content(T(476.24,150.48), anchor: "north-west", text(fill: teal, size: 10pt)[$a_2$])
      content(T(511.24,41.98), anchor: "north-west", text(fill: teal, size: 10pt)[$c$])
      content(T(481.8,77.59), anchor: "north-west", text(fill: red2, size: 9pt)[$h_2$])
      content(T(433.3,78.09), anchor: "north-west", text(fill: red2, size: 9pt)[$h_1$])
    })
  },
  caption: [Source-backed plot.]
)
