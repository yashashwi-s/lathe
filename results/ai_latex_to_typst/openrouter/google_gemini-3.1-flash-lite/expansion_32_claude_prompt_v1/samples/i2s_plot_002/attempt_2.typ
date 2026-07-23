#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt)

#align(center)[
  #text(size: 2em, weight: "bold")[Plot Sample 2] \
  #text(size: 1.2em)[Dataset-expansion sample] \
  #v(1em)
]

= Visualization
The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  align(center)[
    #let dot = circle(radius: 3pt, fill: black)
    #let node(x, y, label) = place(dx: x * 30pt, dy: y * 30pt, align(center + horizon, [#label]))
    #let draw_dot(x, y) = place(dx: x * 30pt, dy: y * 30pt, dot)
    
    #set text(size: 8pt)
    #box(width: 400pt, height: 450pt, {
      place(top + left, {
        // SU(n)
        place(dy: 30pt, {
          line(start: (-60pt, 0pt), end: (15pt, 0pt), stroke: 1pt)
          line(start: (45pt, 0pt), end: (60pt, 0pt), stroke: 1pt)
          draw_dot(-2, 0); draw_dot(-1, 0); draw_dot(0, 0); draw_dot(2, 0)
          node(-2, -0.5, "1"); node(-1, -0.5, "2"); node(0, -0.5, "3"); node(2, -0.5, "$n-1$")
          node(1, 0, "$\cdots$")
          place(dx: -90pt, dy: 0pt, text(fill: blue, "$SU(n)$:"))
        })

        // Spin(2n+1)
        place(dy: 80pt, {
          line(start: (-60pt, 0pt), end: (-15pt, 0pt), stroke: 1pt)
          line(start: (15pt, 0pt), end: (60pt, 0pt), stroke: 1pt)
          line(start: (30pt, 2pt), end: (60pt, 2pt), stroke: 1pt)
          line(start: (30pt, -2pt), end: (60pt, -2pt), stroke: 1pt)
          place(dx: 45pt, dy: -4pt, text(size: 12pt, "▶"))
          draw_dot(-2, 0); draw_dot(-1, 0); draw_dot(1, 0); draw_dot(2, 0)
          node(-2, -0.5, "0"); node(-1, -0.5, "0"); node(1, -0.5, "0"); node(2, -0.5, "1")
          node(0, 0, "$\cdots$")
          place(dx: -105pt, dy: 0pt, text(fill: blue, "$Spin(2n+1)$:"))
        })
      })
    })
  ],
  caption: [Source-backed plot.]
)
