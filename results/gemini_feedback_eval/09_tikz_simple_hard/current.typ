#let unit = 1pt // Corresponds to TikZ's default unit (1pt) for coordinates
#let scale_factor = 1.5
#let stroke_thickness = 1.5pt // Desired visual thickness for "thick" lines

#box(scale: scale_factor, {
  // X-axis
  #line(
    (-1 * unit, 0 * unit),
    (3 * unit, 0 * unit),
    stroke: (paint: black, thickness: stroke_thickness / scale_factor, arrow: "end")
  )
  #place(
    right + center, // Align right of the point, centered vertically
    (3 * unit, 0 * unit),
    $x$-axis
  )

  // Y-axis
  #line(
    (0 * unit, -1 * unit),
    (0 * unit, 3 * unit),
    stroke: (paint: black, thickness: stroke_thickness / scale_factor, arrow: "end")
  )
  #place(
    top + center, // Align above the point, centered horizontally
    (0 * unit, 3 * unit),
    $y$-axis
  )

  // Parabola: f(x) = x^2 / 2
  #let points = ()
  #let x_start = 0
  #let x_end = 2.5
  #let step_size = 0.05 // Smaller step for a smoother curve

  // Generate points for the path
  #for x in range(x_start, x_end + step_size / 2, step_size) {
    let y = x * x / 2
    points.push((x * unit, y * unit))
  }

  #path(
    points,
    stroke: (paint: red, thickness: stroke_thickness / scale_factor),
  )

  // Label for the parabola
  #let last_x = x_end
  #let last_y = last_x * last_x / 2 // Calculate y for the last x
  #place(
    right + center,
    (last_x * unit, last_y * unit),
    $f(x) = frac(x^2, 2)$
  )
})