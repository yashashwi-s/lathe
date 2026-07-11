#set page(numbering: "1")

#import "@preview/draw:0.1.0" as draw

#draw.canvas(
  width: 3pt,
  height: 2pt,
  {
    draw.path(
      points: ((0pt, 2pt), (3pt, 0pt)),
      stroke: (paint: blue, thickness: 0.8pt)
    )
    draw.path(
      points: ((0pt, 0pt), (3pt, 2pt)),
      stroke: (paint: red, thickness: 0.8pt)
    )
  }
)