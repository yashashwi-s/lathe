#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

  /* \usetikzlibrary */
// TikZ converted to CeTZ
#import "@preview/cetz:0.3.4": canvas, draw

#canvas({
  import draw: *

  content(calc.add("A", (1.00, 0.00)), [Feature Extraction], name: "B")
  content(calc.add("B", (1.00, 0.00)), [Classification], name: "C")
  line("A", "B", stroke: (thickness: 0.8pt), mark: (end: ">"))
  line("B", "C", stroke: (thickness: 0.8pt), mark: (end: ">"))
})

