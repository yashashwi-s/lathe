```typst
#set page(
  width: 363pt,
  height: 272pt,
  margin: (left: 10%, right: 10%, top: 10%, bottom: 10%),
)

// Set default font for the document to a sans-serif font, similar to Beamer's default.
#set text(font: "New Computer Modern Sans", weight: "regular")

// Frame title
#align(left)[
  #text(size: 2.5em, fill: rgb("#4169E1"))[Project Kickoff] // RoyalBlue for title
]

#v(1.5em) // Vertical space between title and body

// Body text
#align(left)[
  #text(size: 1.3em)[Welcome to the initial presentation for the Q3 development cycle. We will outline milestones and deliverables.]
]

// Optional: Replicate Beamer's default navigation symbols at the bottom.
// This is a manual approximation and not automatically generated like in Beamer.
#set text(size: 0.7em, fill: gray)
#place(bottom + center)[
  #h(1fr)
  #box(width: 0.5em, height: 0.5em, stroke: gray, fill: white) // Square
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.right.triangle // Left/Right arrows
  #h(0.5em)
  #sym.arrow.up #sym.arrow.down // Up/Down arrows
  #h(0.5em)
  #sym.arrow.left.triangle #sym.arrow.