#import "@preview/algorithms:0.1.0" as alg

// Set document language for proper hyphenation and text processing
#set document(lang: "en")

// The algorithms package automatically handles the numbering and formatting
// similar to LaTeX's algorithm and algpseudocode environments.
#alg.algorithm(
  caption: "Simple Variable Assignment",
  body: alg.pseudocode(
    alg.state[
      $counter <- 0$
    ],
    alg.state[
      $total <- sum_(i=1)^10 i$
    ],
  )
)