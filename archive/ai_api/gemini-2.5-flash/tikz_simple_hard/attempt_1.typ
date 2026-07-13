#set page(
  width: 612pt,
  height: 792pt,
  margin: (left: 1in, right: 1in, top: 1in, bottom: 1in),
)
#set text(font: "New Computer Modern", lang: "en")

// Center the graph on the page
#align(center)[
  #draw(
    scale(1.5), // Apply the scale factor to all coordinates and strokes
    // Default stroke for axes. TikZ 'thick' is 0.8pt.
    stroke: (paint: black, thickness: 0.8pt),

    // X-axis
    line(start: (-1, 0), end: (3, 0), arrow: "classic"),
    // Label "x-axis" to the right of (3,0)
    locate((3, 0)) {
      // TikZ 'node[right]' places the left edge of the text at (3,0), vertically centered.
      // Typst's `text` by default centers horizontally and aligns baseline vertically.
      // `dx: 0.2em` shifts it right.
      // `dy: -0.5em` shifts it up by half its height to center it vertically.
      text(dx: 0.2em, dy: -0.5em, $x$-axis),
    },

    // Y-axis
    line(start: (0, -1), end: (0, 3), arrow: "classic"),
    // Label "y-axis" above (0,3)
    locate((0, 3)) {
      // TikZ 'node[above]' places the bottom edge of the text at (0,3), horizontally centered.
      // `dx: 0.5em` shifts it right to center it horizontally.
      // `dy: -0.2em` shifts it up.
      text(dx: 0.5em, dy: -0.2em, $y$-axis),
    },

    // Function plot
    path(
      stroke: (paint: red, thickness: 0.8pt), // Red color for the curve
      // Generate points for the curve y = x^2/2 from x=0 to x=2.5
      // Using a step of 0.05 for smoothness.
      ..for x in range(0, 2.5, 0.05) { (x, x*x/2) }
    ),

    // Function label
    // The label is placed at the end of the curve, (2.5, 2.5*2.5/2) = (2.5, 3.125)
    // TikZ 'node[right]' means the left edge of the text is at (2.5, 3.125), vertically centered.
    // Visually, in the original image, the label is slightly below the actual end point.
    // Let's adjust the y-coordinate slightly for a better visual match.
    locate((2.5, 2.9)) { // Adjusted y-coordinate for visual match
      text(dx: 0.2em, dy: -0.5em, $f(x) = frac(x^2, 2)$),
    },
  )
]

// Page number at the bottom right
#set align(bottom + right)
#v(1fr) // Push content to the top
#h(1fr) // Push content to the left
#counter(page).display()