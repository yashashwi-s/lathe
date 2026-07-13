#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#show figure.where(kind: "algorithm"): set figure.caption(position: top)

#figure(
kind: "algorithm",
supplement: [Algorithm],
caption: [Simple Variable Assignment],
block(inset: (left: 1.2em))[
#stack(
spacing: 0.4em,
[$#text("counter") <- 0$],
[$total <- sum_(i = 1)^10 i$],
)
],
)
