#set document(title: "Black Hole Information Paradox")
#set text(lang: "en")

// Define bibliography entries directly within the Typst file
#let bib_data = (
  entry(
    id: "hawking1976",
    authors: (
      (given: "S. W.", family: "Hawking"),
    ),
    title: "Breakdown of predictability in gravitational collapse",
    journal: "Physical Review D",
    volume: "14",
    number: "10",
    pages: "2460",
    year: 1976,
  ),
)

= Introduction
The resolution of the black hole information paradox remains a profound challenge in theoretical physics @hawking1976. Recent developments in AdS/CFT correspondence suggest unitary evolution is preserved.

= Holographic Entanglement Entropy
The Ryu-Takayanagi formula relates the entanglement entropy $S_A$ to the area of a minimal surface $\gamma_A$:

$ S_A = frac(text("Area")(\gamma_A), 4 G_N) <eq:ryu-takayanagi> $

= References
#bibliography(bib_data)