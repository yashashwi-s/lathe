#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

// TikZ converted to CeTZ
#import "@preview/cetz:0.3.4": canvas, draw

#canvas({
  import draw: *

  content((0, 3), [$y$-axis], anchor: "south")
  line((0, -1), (0, 3), mark: (end: ">"))
  content(({x}, {x * x / 2}), [$f(x) = \frac{x^2}{2}$], anchor: "west")
})

