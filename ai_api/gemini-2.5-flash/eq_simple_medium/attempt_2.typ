#set text(font: "New Computer Modern")
#set page(
  footer: [
    #h(1fr) #page-number() #h(1fr)
  ]
)

The Gaussian integral over the real line is remarkably elegant:
#equation(
  integral(from: -infinity, to: infinity, e^(-x^2) d x) = sqrt(pi),
  numbering: "(1)"
)