#set page(
  margin: (left: 1in, right: 1in, top: 1in, bottom: 1in),
  footer: [
    #h(1fr) #text(10pt, "1") #h(1fr) // Centered page number
  ],
)

// Set default font to match LaTeX's Computer Modern family
#set text(
  font: "New Computer Modern", // A good match for LaTeX's default
  size: 11pt, // Standard article body font size
)

// Custom styling for headings to match LaTeX article class defaults
#show heading: it => {
  if it.level == 1 {
    // \section* equivalent: \Huge, bold, specific spacing
    // LaTeX \section* (with 11pt base) typically uses a font size around 20pt-22pt.
    // It also has specific vertical spacing before and after.
    set text(20pt, weight: "bold")
    // Approximate LaTeX article class \section* spacing
    // The 'spacing' property for 'block' expects a single length or dictionary for 'top' and 'bottom'.
    // To set 'before' and 'after' spacing, we need to use 'block.spacing' directly.
    set block(above: 19pt, below: 12pt)
    it.body
  } else if it.level == 2 {
    // \subsection* equivalent: \Large, bold, specific spacing
    // LaTeX \subsection* (with 11pt base) typically uses a font size around 16pt-17pt.
    // It also has specific vertical spacing before and after.
    set text(16pt, weight: "bold")
    // Approximate LaTeX article class \subsection* spacing
    set block(above: 18pt, below: 8pt)
    it.body
  } else {
    it // Default for other heading levels
  }
}

#heading(level: 1)[Alexander Hamilton]
ahamilton@treasury.gov #h(0.5em) | #h(0.5em) New York, NY // Added #h(0.5em) for spacing around the pipe

#line(length: 100%) // Equivalent to \hrule
#v(3mm) // Equivalent to \vspace{3mm}

#heading(level: 2)[Education]
*King's College (Columbia University)* #h(1fr) 1774 - 1776 \
Studies in Mathematics and Law