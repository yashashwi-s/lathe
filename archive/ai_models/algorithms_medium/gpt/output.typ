#import "@preview/algorithmic:1.0.7"
#import algorithmic: style-algorithm, algorithm-figure

#set page(margin: 1in)
#set text(size: 10pt)

#show: style-algorithm.with(caption-style: text)
#show figure.where(kind: "algorithm"): set figure.caption(position: top)

#algorithm-figure(
[Binary Search Validation],
{
import algorithmic: *

```
If($#text("target") = #text("array")[#text("mid")]$, {
  Return[$#text("mid")$]
})
ElseIf($#text("target") < #text("array")[#text("mid")]$, {
  Assign[$#text("high")$][$#text("mid") - 1$]
})
Else({
  Assign[$#text("low")$][$#text("mid") + 1$]
})
```

},
)
