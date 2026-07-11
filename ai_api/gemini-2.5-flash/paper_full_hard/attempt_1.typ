#set page(
  width: 612pt, // Letter paper width (8.5in)
  height: 792pt, // Letter paper height (11in)
  margin: (
    left: 111pt, // Corresponds to LaTeX article class default for letter paper
    right: 111pt,
    top: 108pt, // Corresponds to LaTeX article class default for letter paper (simplified)
    bottom: 108pt,
  ),
  footer: [
    #h(1fr) #text(10pt, counter(page).display()) #h(1fr)
  ]
)

#set text(font: "New Computer Modern", lang: "en", size: 10pt)
#set heading(
  level: 1,
  outlined: false,
  numbering: "1.",
  supplement: none,
  font: "New Computer Modern",
  size: 14.4pt, // Corresponds to LaTeX \Large for section headings
  weight: "bold",
)

= Introduction
The resolution of the black hole information paradox remains a profound challenge in theoretical physics [?]. Recent developments in AdS/CFT correspondence suggest unitary evolution is preserved.

= Holographic Entanglement Entropy
The Ryu-Takayanagi formula relates the entanglement entropy $S_A$ to the area of a minimal surface $\gamma_A$:
#block(
  $ S_A = frac(text("Area")(\gamma_A), 4 G_N) $
)

#bibliography(
  title: none, // LaTeX's thebibliography environment does not print a title by default.
  style: "ieee", // IEEE style provides numeric citations like [1] for the bibliography list.
  entry("hawking1976",
    authors: (
      "Hawking, S. W.",
    ),
    year: 1976,
    title: "Breakdown of predictability in gravitational collapse",
    journal: "_Physical Review D_",
    volume: "14",
    issue: "10",
    pages: "2460",
  ),
)