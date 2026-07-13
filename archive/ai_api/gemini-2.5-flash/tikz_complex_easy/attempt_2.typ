#set page(
  width: 612pt,  // US Letter width
  height: 792pt, // US Letter height
  margin: (left: 90pt, right: 90pt, top: 90pt, bottom: 90pt), // Approx. 1.25 inch margins
)
#set text(font: "Latin Modern Roman", size: 10pt) // Match LaTeX's default font and size
#set page(numbering: "1") // Add page number '1' at the bottom center

#v(fill) // Push content vertically to center it
#align(center)[
  #draw(
    // Draw the spring line with coil decoration and arrow
    line(
      (0,0), (4cm,0), // Path from (0,0) to (4cm,0)
      stroke: (paint: black, thickness: 0.5pt), // Line color and thickness
      decorate: coil(radius: 2mm, turns: 3), // Coil decoration: 2mm amplitude, 3 turns over 4cm
      end-arrow: {
        kind: "triangle", // Arrowhead style
        size: 3mm,        // Arrowhead size
        fill: black,      // Arrowhead fill color
      },
    ),
    // Place the text label "Spring Force"
    text(
      "Spring Force",
      fill: black,
      size: 10pt,
      origin: (0.5, 1), // Align text's bottom-center to the specified point
    ).translate(x: 2cm, y: 0.3cm), // Position the text's bottom-center at (2cm, 0.3cm)
  )
]
#v(fill) // Push content vertically to center it