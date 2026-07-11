#show figure.where(kind: "algorithm"): it => block(width: 100%)[
#set align(left)
#line(length: 100%, stroke: 0.8pt)
#pad(y: 0.3em)[*#it.supplement #it.counter.display()* #it.caption.body]
#line(length: 100%, stroke: 0.4pt)
#pad(left: 1.5em, y: 0.3em)[#it.body]
#line(length: 100%, stroke: 0.8pt)
]

#figure(
kind: "algorithm",
supplement: [Algorithm],
caption: [Binary Search Validation],
)[
*if* $"target" = "array"["mid"]$ *then*

#h(1.5em) *return* $"mid"$

*else if* $"target" < "array"["mid"]$ *then*

#h(1.5em) $"high" <- "mid" - 1$

*else*

#h(1.5em) $"low" <- "mid" + 1$

*end if*
]