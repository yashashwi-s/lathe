#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Plot Sample 2]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Visualization

The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  {
    import cetz.draw: *
    cetz.canvas(length: 0.85cm, {
      // Helper to draw filled circle
      let dot(pos) = {
        circle(pos, radius: 0.1, fill: black, stroke: black)
      }

      // === SU(n) row at y=0 ===
      line((-2,0), (0.5,0), stroke: 1.5pt)
      dot((-2,0))
      dot((-1,0))
      dot((0,0))
      content((1,0), $dots.h.c$)
      line((1.5,0),(2,0), stroke: 1.5pt)
      dot((2,0))
      content((-2,-0.5), [1])
      content((-1,-0.5), [2])
      content((0,-0.5), [3])
      content((2,-0.5), $n-1$)
      content((-3,0), text(fill: blue)[$S U(n)$:])

      // === Spin(2n+1) row at y=0, shifted x+8.5 ===
      let s1 = (8.5, 0)
      let dx(x) = (s1.at(0) + x, s1.at(1))
      let dxy(x,y) = (s1.at(0)+x, s1.at(1)+y)
      // double line segment
      line(dx(1), dx(2), stroke: (paint: black, thickness: 1.5pt, dash: none))
      line(dx(1), dx(2), stroke: (paint: black, thickness: 1.5pt, dash: none))
      // draw double line as two close lines
      line((s1.at(0)+1, s1.at(1)+0.05), (s1.at(0)+2, s1.at(1)+0.05), stroke: 1.5pt)
      line((s1.at(0)+1, s1.at(1)-0.05), (s1.at(0)+2, s1.at(1)-0.05), stroke: 1.5pt)
      // arrow
      line((s1.at(0)+1.5, s1.at(1)), (s1.at(0)+1.65, s1.at(1)), stroke: (paint: black, thickness: 3pt), mark: (end: ">", fill: black))
      line((s1.at(0)-2, s1.at(1)), (s1.at(0)-0.5, s1.at(1)), stroke: 1.5pt)
      dot(dx(-2))
      dot(dx(-1))
      dot(dx(1))
      content(dx(0), $dots.h.c$)
      line(dx(0.5), dx(1), stroke: 1.5pt)
      dot(dx(2))
      content((s1.at(0)-2, s1.at(1)-0.5), [0])
      content((s1.at(0)-1, s1.at(1)-0.5), [0])
      content((s1.at(0)+1, s1.at(1)-0.5), [0])
      content((s1.at(0)+2, s1.at(1)-0.5), [1])
      content((s1.at(0)-3.5, s1.at(1)), text(fill: blue)[$S p i n(2n+1)$:])

      // === Sp(2n+1) row shifted (3,-1.5) ===
      let s2x = 3.0
      let s2y = -1.5
      let d2(x,y) = (s2x+x, s2y+y)
      // double line
      line(d2(4,0.05), d2(5,0.05), stroke: 1.5pt)
      line(d2(4,-0.05), d2(5,-0.05), stroke: 1.5pt)
      // arrow pointing left
      line(d2(4.55,0), d2(4.4,0), stroke: (paint: black, thickness: 3pt), mark: (end: ">", fill: black))
      line(d2(-2,0), d2(1.5,0), stroke: 1.5pt)
      dot(d2(-2,0))
      dot(d2(-1,0))
      dot(d2(0,0))
      dot(d2(1,0))
      dot(d2(3,0))
      dot(d2(4,0))
      content(d2(2,0), $dots.h.c$)
      line(d2(2.5,0), d2(4,0), stroke: 1.5pt)
      dot(d2(5,0))
      content(d2(-2,-0.5), [1])
      content(d2(-1,-0.5), [0])
      content(d2(0,-0.5), [1])
      content(d2(1,-0.5), [0])
      content(d2(3,-0.5), [1])
      content(d2(4,-0.5), [0])
      content(d2(5,-0.5), [1])
      content(d2(-4,0), text(fill: blue)[$S p(2n+1)$:])

      // === Sp(2n) row shifted (2.5,-3) ===
      let s3x = 2.5
      let s3y = -3.0
      let d3(x,y) = (s3x+x, s3y+y)
      line(d3(5,0.05), d3(6,0.05), stroke: 1.5pt)
      line(d3(5,-0.05), d3(6,-0.05), stroke: 1.5pt)
      line(d3(5.55,0), d3(5.4,0), stroke: (paint: black, thickness: 3pt), mark: (end: ">", fill: black))
      line(d3(-2,0), d3(1.5,0), stroke: 1.5pt)
      dot(d3(-2,0))
      dot(d3(-1,0))
      dot(d3(0,0))
      dot(d3(1,0))
      dot(d3(3,0))
      dot(d3(4,0))
      dot(d3(5,0))
      content(d3(2,0), $dots.h.c$)
      line(d3(2.5,0), d3(5,0), stroke: 1.5pt)
      dot(d3(6,0))
      content(d3(-2,-0.5), [1])
      content(d3(-1,-0.5), [0])
      content(d3(0,-0.5), [1])
      content(d3(1,-0.5), [0])
      content(d3(3,-0.5), [1])
      content(d3(4,-0.5), [0])
      content(d3(5,-0.5), [1])
      content(d3(6,-0.5), [0])
      content(d3(-3.5,0), text(fill: blue)[$S p(2n)$:])

      // === Spin(4n+2) row shifted (2.5,-5.5) ===
      let s4x = 2.5
      let s4y = -5.5
      let d4(x,y) = (s4x+x, s4y+y)
      line(d4(5,1), d4(5,0), stroke: 1.5pt)
      line(d4(5,0), d4(6,0), stroke: 1.5pt)
      line(d4(-2,0), d4(1.5,0), stroke: 1.5pt)
      dot(d4(-2,0))
      dot(d4(-1,0))
      dot(d4(0,0))
      dot(d4(1,0))
      dot(d4(3,0))
      dot(d4(4,0))
      dot(d4(5,0))
      content(d4(2,0), $dots.h.c$)
      line(d4(2.5,0), d4(5,0), stroke: 1.5pt)
      dot(d4(6,0))
      dot(d4(5,1))
      content(d4(-2,-0.5), [2])
      content(d4(-1,-0.5), [0])
      content(d4(0,-0.5), [2])
      content(d4(1,-0.5), [0])
      content(d4(3,-0.5), [2])
      content(d4(4,-0.5), [0])
      content(d4(5,-0.5), [2])
      content(d4(6,-0.5), [1])
      content(d4(5.5,1), [3])
      content(d4(-3.5,0.5), text(fill: blue)[$S p i n(4n+2)$:])

      // === Spin(4n); n_s row shifted (3,-8) ===
      let s5x = 3.0
      let s5y = -8.0
      let d5(x,y) = (s5x+x, s5y+y)
      line(d5(4,1), d5(4,0), stroke: 1.5pt)
      line(d5(4,0), d5(5,0), stroke: 1.5pt)
      line(d5(-2,0), d5(1.5,0), stroke: 1.5pt)
      dot(d5(-2,0))
      dot(d5(-1,0))
      dot(d5(0,0))
      dot(d5(1,0))
      dot(d5(3,0))
      dot(d5(4,0))
      content(d5(2,0), $dots.h.c$)
      line(d5(2.5,0), d5(4,0), stroke: 1.5pt)
      dot(d5(5,0))
      dot(d5(4,1))
      content(d5(-2,-0.5), [1])
      content(d5(-1,-0.5), [0])
      content(d5(0,-0.5), [1])
      content(d5(1,-0.5), [0])
      content(d5(3,-0.5), [1])
      content(d5(4,-0.5), [0])
      content(d5(5,-0.5), [1])
      content(d5(4.5,1), [0])
      content(d5(-4,0.5), text(fill: blue)[$S p i n(4n);~n_s$:])

      // === Spin(4n); n_c row shifted (3,-10.5) ===
      let s6x = 3.0
      let s6y = -10.5
      let d6(x,y) = (s6x+x, s6y+y)
      line(d6(4,1), d6(4,0), stroke: 1.5pt)
      line(d6(4,0), d6(5,0), stroke: 1.5pt)
      line(d6(-2,0), d6(1.5,0), stroke: 1.5pt)
      dot(d6(-2,0))
      dot(d6(-1,0))
      dot(d6(0,0))
      dot(d6(1,0))
      dot(d6(3,0))
      dot(d6(4,0))
      content(d6(2,0), $dots.h.c$)
      line(d6(2.5,0), d6(4,0), stroke: 1.5pt)
      dot(d6(5,0))
      dot(d6(4,1))
      content(d6(-2,-0.5), [1])
      content(d6(-1,-0.5), [0])
      content(d6(0,-0.5), [1])
      content(d6(1,-0.5), [0])
      content(d6(3,-0.5), [1])
      content(d6(4,-0.5), [0])
      content(d6(5,-0.5), [0])
      content(d6(4.5,1), [1])
      content(d6(-4,0.5), text(fill: blue)[$S p i n(4n);~n_c$:])

      // === E6 row shifted (0,-13) ===
      let s7x = 0.0
      let s7y = -13.0
      let d7(x,y) = (s7x+x, s7y+y)
      line(d7(0,1), d7(0,0), stroke: 1.5pt)
      line(d7(-2,0), d7(2,0), stroke: 1.5pt)
      dot(d7(-2,0))
      dot(d7(-1,0))
      dot(d7(0,0))
      dot(d7(1,0))
      dot(d7(2,0))
      dot(d7(0,1))
      content(d7(-2,-0.5), [1])
      content(d7(-1,-0.5), [2])
      content(d7(0,-0.5), [0])
      content(d7(1,-0.5), [1])
      content(d7(2,-0.5), [2])
      content(d7(0.5,1), [0])
      content(d7(-3,0.5), text(fill: blue)[$E_6$:])

      // === E7 row shifted (7.5,-13) ===
      let s8x = 7.5
      let s8y = -13.0
      let d8(x,y) = (s8x+x, s8y+y)
      line(d8(1,1), d8(1,0), stroke: 1.5pt)
      line(d8(-2,0), d8(3,0), stroke: 1.5pt)
      dot(d8(-2,0))
      dot(d8(-1,0))
      dot(d8(0,0))
      dot(d8(1,0))
      dot(d8(2,0))
      dot(d8(3,0))
      dot(d8(1,1))
      content(d8(-2,-0.5), [1])
      content(d8(-1,-0.5), [0])
      content(d8(0,-0.5), [1])
      content(d8(1,-0.5), [0])
      content(d8(2,-0.5), [0])
      content(d8(3,-0.5), [0])
      content(d8(1.5,1), [1])
      content(d8(-3,0.5), text(fill: blue)[$E_7$:])
    })
  },
  caption: [Source-backed plot.]
)
