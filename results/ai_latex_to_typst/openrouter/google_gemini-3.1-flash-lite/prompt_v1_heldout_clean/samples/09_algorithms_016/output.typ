#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center, [
  #text(size: 1.44em, weight: "bold")[Algorithmic Pseudocode Sample 16] \
  #text(size: 1.2em)[Source-backed Image2Struct algorithm sample] \
  #text(size: 1em)[]
])

= Algorithm
This sample contains algorithmic pseudocode extracted from a source-backed LaTeX benchmark dataset. It is wrapped in a minimal article document for pdfLaTeX validation.

#figure(
  block[
    #set enum(numbering: "1.")
    #line(length: 100%, stroke: 0.5pt)
    *Require:* $n, p in NN, omega in [0, 1], x in RR^n, v in RR^n$.
    + Find a sorting permutation $sigma$ of vector $x$.
    + Apply the $sigma$ to $x$ and $v$, in place.
    + For $tilde omega = 1, 0$
      + If $tilde omega = 0$ // Shift $v$ by one place because of 0s on diagonal of $bold(I)$.
        + For $i = n, n - 1, ..., 2$
          + $v_i <- v_(i - 1)$
        + $v_1 <- 0$
      + Identify the set of groups $G$ of elements of $v$ corresponding to equal entries in $x$.
      + $tilde v <- v$
      + For $g$ in $G$
        + Calculate sum $bold(s)$ of $v$'s elements in group $g$.
        + Set $0$ in all $tilde v$'s elements in group $g$.
        + If $tilde omega = 0$
          + Set the $tilde v$'s first element in group $g$ to $bold(s)$.
        + Else
          + Set the $tilde v$'s last element in group $g$ to $bold(s)$.
      + $c_(tilde omega) <-$ cumulative sum of $tilde v$
    + $c <- omega c_1 + (1 - omega)c_0$ // Multiplication and addition element-wise.
    + Find the inverse of $sigma$.
    + Apply the $sigma^(-1)$ to $c$.
    + Return $c$
    #line(length: 100%, stroke: 0.5pt)
  ],
  caption: [Source-backed algorithmic procedure]
)
