#set page(
  width: 612pt, // US Letter width
  height: 792pt, // US Letter height
  margin: 1in, // Default LaTeX article margin
)

// Set the text font to Latin Modern Roman to closely match LaTeX's default font.
#set text(font: "Latin Modern Roman")

// Center the entire drawing horizontally on the page.
#align(center)[
  #draw(
    // Typst's `draw` function uses a coordinate system where (0,0) is the top-left,
    // x increases to the right, and y increases downwards.
    // For this specific TiKz diagram, a direct mapping of coordinates works well
    // to achieve the visual layout. We'll use `cm` as the unit for clarity,
    // assuming 1 unit in TiKz corresponds to 1cm in Typst for scaling.

    // Draw the outer rectangle: `\draw[fill=blue!20] (0,0) rectangle (4,2);`
    // This creates a rectangle with its top-left at (0,0) and bottom-right at (4,2).
    rect(width: 4cm, height: 2cm, fill: mix(white, blue, 20%))
      .move(0cm, 0cm), // Position its top-left corner at (0,0)

    // Draw the inner circle: `\draw[fill=red!20] (2,1) circle (0.8);`
    // This creates a circle centered at (2,1) with a radius of 0.8.
    circle(radius: 0.8cm, fill: mix(white, red, 20%))
      .move(2cm, 1cm), // Position its center at (2,1)

    // Place the text node: `\node at (2,1) {\textbf{Center}};`
    // This places the bold text "Center" with its center at (2,1).
    place(
      align(center, text(weight: "bold", "Center")),
      center: (2cm, 1cm)
    ),
  )
]