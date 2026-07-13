#set document(lang: "en")
#set text(font: "New Computer Modern", size: 10pt) // Explicitly set font and size to match LaTeX article defaults

// Mimic the algorithm environment's caption and horizontal rule
#block(
  width: 100%,
  stroke: (bottom: 0.5pt, paint: black), // Horizontal line below caption
  inset: (top: 0.5em, bottom: 0.5em), // Padding around caption text
  [
    #text(weight: "bold")[Algorithm 1] Simple Variable Assignment
  ]
)

// Add a small vertical space between the rule and the pseudocode
#v(0.8em) // Adjust as needed to match visual spacing

// Mimic the algorithmic environment's content
// Each \State command creates a new line with indentation.
// We'll use a block with a consistent left indent.
#block(
  indent: 1.5em, // Indent for the pseudocode lines (similar to \State)
  [
    $counter \leftarrow 0$ \
    $total \leftarrow \sum_{i=1}^{10} i$
  ]
)