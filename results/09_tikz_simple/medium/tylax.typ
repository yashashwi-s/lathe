#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

// TikZ converted to CeTZ
#import "@preview/cetz:0.3.4": canvas, draw

#canvas({
  import draw: *

  circle((2, 1), radius: 0.8, fill: red.lighten(80%))
  content((2, 1), [\textbf{Center}])
})

