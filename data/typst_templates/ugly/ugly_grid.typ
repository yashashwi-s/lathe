#set page(width: 595.28pt, height: 841.89pt, margin: 0pt)

// Manual lines to fake a grid
#place(dx: 10pt, dy: 50pt)[#line(start: (0pt, 0pt), end: (200pt, 0pt))]
#place(dx: 10pt, dy: 70pt)[#line(start: (0pt, 0pt), end: (200pt, 0pt))]
#place(dx: 10pt, dy: 90pt)[#line(start: (0pt, 0pt), end: (200pt, 0pt))]

#place(dx: 10pt, dy: 50pt)[#line(start: (0pt, 0pt), end: (0pt, 40pt))]
#place(dx: 110pt, dy: 50pt)[#line(start: (0pt, 0pt), end: (0pt, 40pt))]
#place(dx: 210pt, dy: 50pt)[#line(start: (0pt, 0pt), end: (0pt, 40pt))]

// Content manually placed
#place(dx: 15pt, dy: 55pt)[Name]
#place(dx: 115pt, dy: 55pt)[Age]
#place(dx: 15pt, dy: 75pt)[Alice]
#place(dx: 115pt, dy: 75pt)[30]

// Repeated sizes and magic numbers
#place(dx: 10pt, dy: 120pt)[#text(size: 10.5pt, font: "Arial")[Some text]]
#place(dx: 10pt, dy: 140pt)[#text(size: 10.5pt, font: "Arial")[More text]]
#place(dx: 10pt, dy: 160pt)[#text(size: 10.5pt, font: "Arial")[Even more text]]
