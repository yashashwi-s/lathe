#set page(margin: 1in)

// First table: Grace Hopper's name and contact info
#grid(
  columns: (1fr, auto), // First column expands, second column is auto-width
  column-gutter: 1.2em, // Corresponds to 2 * \tabcolsep (default LaTeX inter-column space)
  align: (left, right), // Align content in first column left, second column right
  text(1.44em, weight: "bold", "Grace Hopper"), // \LARGE is approx 1.44 times normal font size
  "ghopper@navy.mil",
  "Rear Admiral, US Navy",
  "Arlington, VA",
)

#v(3mm) // Vertical space
#line(length: 100%) // Horizontal rule spanning the full width
#v(3mm) // Vertical space

// Second table: Achievements
#grid(
  columns: (auto, 1fr), // First column is auto-width, second column expands
  column-gutter: 1.2em, // Corresponds to 2 * \tabcolsep
  align: (left, left), // Align content in both columns left
  strong("1952"),
  "Invented the first operational compiler (A-0 System).",
  strong("1959"),
  "Served as technical consultant on the CODASYL committee, leading to the creation of COBOL.",
)