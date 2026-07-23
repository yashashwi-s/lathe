#set page(paper: "us-letter", margin: 1in)
#set text(font: "Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.44em, weight: "bold")[Plot Sample 1] \
  Dataset-expansion sample \
  #v(1em)
])

#section("Visualization")
The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  align(center, canvas(length: 0.75pt, {
    import draw: *
    let blue_color = rgb(42, 175, 236)
    let stroke_style = (stroke: (paint: blue_color, thickness: 3.75pt))
    let circle_style = (fill: white, stroke: (paint: blue_color, thickness: 3.75pt))

    line(stroke_style, (328.41, 104.55), (514.77, 239.95))
    line(stroke_style, (514.77, 239.95), (443.59, 459.02))
    line(stroke_style, (142.06, 239.95), (328.41, 104.55))
    line(stroke_style, (142.06, 239.95), (213.24, 459.02))
    line(stroke_style, (213.24, 459.02), (443.59, 459.02))
    line(stroke_style, (328.41, 104.55), (443.59, 459.02))
    line(stroke_style, (142.06, 239.95), (443.59, 459.02))
    line(stroke_style, (514.77, 239.95), (213.24, 459.02))
    line(stroke_style, (142.06, 239.95), (514.77, 239.95))
    line(stroke_style, (328.41, 104.55), (213.24, 459.02))

    circle((328.41, 104.55), radius: 36.12, ..circle_style)
    circle((514.77, 239.95), radius: 36.12, ..circle_style)
    circle((443.59, 459.02), radius: 36.12, ..circle_style)
    circle((213.24, 459.02), radius: 36.12, ..circle_style)
    circle((142.06, 239.95), radius: 36.12, ..circle_style)

    content((318.22, 94.06), text(size: 24.88pt, $9$))
    content((314.22, 10.06), text(size: 17.28pt, $6 5/6$))
    content((559.22, 217.1), text(size: 17.28pt, $6 5/6$))
    content((481.22, 463.1), text(size: 17.28pt, $6 1/3$))
    content((505.22, 229.06), text(size: 24.88pt, $9$))
    content((433.22, 448.06), text(size: 24.88pt, $6$))
    content((202.22, 448.06), text(size: 24.88pt, $4$))
    content((130.22, 229.06), text(size: 24.88pt, $4$))
    content((80.22, 235.1), text(size: 17.28pt, $6$))
    content((155.22, 481.1), text(size: 17.28pt, $6$))
  })),
  caption: [Source-backed plot.]
)
