#set page(paper: "a4")
#set heading(numbering: "1.")
#set math.equation(numbering: "(1)")

    #block(width: 100%, stroke: 1pt, inset: 10pt)[
  #text(weight: "bold")[Algorithm]

```
 \caption{Binary Search Validation} algorithmic \If{$target = array[mid]$} \State \textbf{return} $mid$ \ElsIf{$target < array[mid]$} \State$high \gets mid - 1$ \Else \State$low \gets mid + 1$ \EndIf algorithmic 
```
]

