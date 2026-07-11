#set page(
  width: 612pt, // US Letter width
  height: 792pt, // US Letter height
  margin: 1in, // Default LaTeX article margin
)

// Center the entire drawing horizontally on the page.
#align(center)[
  // Create a box to act as the drawing canvas.
  // The rectangle (0,0) rectangle (4,2) defines the main area of the drawing.
  // We set the box dimensions to match this main rectangle.
  #box(width: 4cm, height: 2cm,
    // Place the outer rectangle: `\draw[fill=blue!20] (0,0) rectangle (4,2);`
    // In Typst, `place(dx: x, dy: y, content)` positions `content` with its top-left
    // corner at `(x, y)` relative to the parent box's top-left.
    place(dx: 0cm, dy: 0cm,
      rect(width: 4cm, height: 2cm, fill: mix(white, blue, 20%))
    ),

    // Place the inner circle: `\draw[fill=red!20] (2,1) circle (0.8);`
    // In Typst, `place(center: (x, y), content)` positions `content` with its center
    // at `(x, y)` relative to the parent box's top-left.
    place(center: (2cm, 1cm),
      circle(radius: 0.8cm, fill: mix(white, red, 20%))
    ),

    // Place the text node: `\node at (2,1) {\textbf{Center}};`
    // The text "Center" is placed with its center at (2,1).
    place(center: (2cm, 1cm),
      text(weight: "bold", "Center")
    ),
  )
]
```