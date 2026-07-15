#import "@preview/cetz:0.3.4"

#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, leading: 0.55em)

#align(center)[
  #v(4.5em)
  #text(size: 17.28pt)[Plot Sample 1]
  #v(0.6em)
  Dataset-expansion sample
]

#v(1.5em)

#heading(numbering: "1", level: 1)[Visualization]

The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#let sc = 0.75
#let px(p) = (p.at(0) * sc * 1pt, -p.at(1) * sc * 1pt)

#let v0 = (328.41, 104.55)
#let v1 = (514.77, 239.95)
#let v2 = (443.59, 459.02)
#let v3 = (213.24, 459.02)
#let v4 = (142.06, 239.95)

#figure(
  {
    import cetz.draw: *
    cetz.canvas({
      set-style(stroke: (paint: rgb(42, 175, 236), thickness: 2.8pt))
      let k = 0.03528  // pt to cm
      let P(p) = (p.at(0) * sc * k, -p.at(1) * sc * k)
      let edges = (
        (v0,v1),(v1,v2),(v4,v0),(v4,v3),(v3,v2),
        (v0,v2),(v4,v2),(v1,v3),(v4,v1),(v0,v3),
      )
      for e in edges { line(P(e.at(0)), P(e.at(1))) }
      let r = 36.11 * sc * k
      for (p, lbl) in ((v0,"9"),(v1,"9"),(v2,"6"),(v3,"4"),(v4,"4")) {
        circle(P(p), radius: r, fill: white)
        content(P(p), text(size: 20pt)[#lbl])
      }
      // outer labels
      content(P((328.41, 40)), text(size: 12pt)[$6 5/6$])
      content(P((580, 217)), text(size: 12pt)[$6 5/6$])
      content(P((500, 490)), text(size: 12pt)[$6 1/3$])
      content(P((85, 239)), text(size: 12pt)[$6$])
      content(P((175, 510)), text(size: 12pt)[$6$])
    })
  },
  caption: [Source-backed plot.],
)
