#set document(
  title: "Quantum Entanglement in Bipartite Systems",
  author: ("Dr. Alice", "Dr. Bob"),
)

// Set global page and text styles
#set page(margin: (left: 1in, right: 1in, top: 1in, bottom: 1in))
#set text(font: "New Computer Modern", lang: "en") // A common LaTeX-like font

// Manual title page layout, equivalent to \maketitle
#align(center)[
  #v(2em) // Vertical space
  #text(2em, weight: "bold", document.title) // Title
  #v(1em)
  #text(1.2em, document.author.join(" and ")) // Authors
  #v(1em)
  #text(0.9em, datetime.today().display("[month] [day], [year]")) // Date
]
#pagebreak() // End of title page, start new page for content

// Abstract
#heading(level: 0, "Abstract") // Level 0 for abstract, typically unnumbered
We explore the fundamental properties of quantum entanglement in simplified bipartite systems, focusing on Bell state inequalities and information-theoretic interpretations.

// Sections
#heading(level: 1, "Introduction")
Quantum entanglement describes a physical phenomenon where pairs or groups of particles interact in ways such that the quantum state of each particle cannot be described independently.

#heading(level: 1, "Theoretical Framework")
Let $cal(H)_A$ and $cal(H)_B$ be Hilbert spaces. The composite system is $cal(H)_A \otimes cal(H)_B$.