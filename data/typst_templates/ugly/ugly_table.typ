#set page(width: 595.28pt, height: 841.89pt, margin: 0pt)
#import "@preview/absolute-place:1.0.0": *

// This is an ugly table recreated manually
#place(dx: 50pt, dy: 100pt)[#rect(width: 100pt, height: 20pt, stroke: 1pt)]
#place(dx: 150pt, dy: 100pt)[#rect(width: 100pt, height: 20pt, stroke: 1pt)]
#place(dx: 50pt, dy: 120pt)[#rect(width: 100pt, height: 20pt, stroke: 1pt)]
#place(dx: 150pt, dy: 120pt)[#rect(width: 100pt, height: 20pt, stroke: 1pt)]

#place(dx: 55pt, dy: 105pt)[Header 1]
#place(dx: 155pt, dy: 105pt)[Header 2]
#place(dx: 55pt, dy: 125pt)[Row 1, Col 1]
#place(dx: 155pt, dy: 125pt)[Row 1, Col 2]

// Repeated magic numbers
#place(dx: 50pt, dy: 200pt)[#text(size: 14pt)[Ugly Section 1]]
#place(dx: 50pt, dy: 220pt)[#text(size: 12pt, fill: blue)[Some content with blue fill.]]
#place(dx: 50pt, dy: 240pt)[#text(size: 12pt, fill: blue)[More content with blue fill.]]
