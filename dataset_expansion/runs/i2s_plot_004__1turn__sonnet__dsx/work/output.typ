#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Plot Sample 4]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1em)
]

= Visualization

The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  caption: [Source-backed plot.],
  {
    v(0.5em)
    let s = 0.75
    // We'll render the TikZ diagram using CeTZ
    import "@preview/cetz:0.3.1": canvas, draw

    canvas(length: 1pt, {
      import draw: *

      // Helper for arrowhead
      let arrow-tip = ((x, y), angle-deg) => {
        let angle-rad = angle-deg * calc.pi / 180
        let size = 6pt
        let dx = calc.cos(angle-rad) * size
        let dy = calc.sin(angle-rad) * size
        let px1 = x + calc.cos((angle-deg + 150) * calc.pi / 180) * 5
        let py1 = y + calc.sin((angle-deg + 150) * calc.pi / 180) * 5
        let px2 = x + calc.cos((angle-deg - 150) * calc.pi / 180) * 5
        let py2 = y + calc.sin((angle-deg - 150) * calc.pi / 180) * 5
        fill(black)
        stroke(none)
        line((px1, py1), (x, y), (px2, py2), close: true)
      }

      // Coordinate transform: TikZ coords (x,y) with yscale=-1
      // We map: tx = x * 0.75, ty = -y * 0.75 (yscale=-1)
      let t(x, y) = (x * s, -y * s)

      // Draw line with arrow: from (x1,y1) to arrow tip end at (ex, ey)
      // The arrow is drawn at the end point
      let arrow-line(x1, y1, x2, y2, col: black, dashed: false) = {
        let dx = x2 - x1
        let dy = -(y2 - y1)  // flipped because yscale=-1
        let len = calc.sqrt(dx*dx + dy*dy)
        let ux = dx / len
        let uy = dy / len
        // Shorten end by arrowhead size
        let tip-len = 5
        let ex = x2 * s - ux * tip-len
        let ey = -y2 * s - uy * tip-len

        stroke(col)
        if dashed {
          set-style(stroke: (paint: col, dash: (array: (4.5pt, 4.5pt), phase: 0pt)))
        }
        line(t(x1, y1), (ex, ey))

        // Arrowhead
        let angle-rad = calc.atan2(uy, ux)
        let a = angle-rad
        let sz = 5.0
        let tipx = x2 * s
        let tipy = -y2 * s
        fill(col)
        stroke(none)
        line(
          (tipx - sz * calc.cos(a) + sz * 0.45 * calc.sin(a),
           tipy - sz * calc.sin(a) - sz * 0.45 * calc.cos(a)),
          (tipx, tipy),
          (tipx - sz * calc.cos(a) - sz * 0.45 * calc.sin(a),
           tipy - sz * calc.sin(a) + sz * 0.45 * calc.cos(a)),
          close: true
        )
        stroke(black)
        if dashed {
          set-style(stroke: black)
        }
      }

      // --- Arrows ---
      // (73,178) -> arrowhead at (109.33,131)
      arrow-line(73, 178, 109.33, 131)
      // (73,178) -> arrowhead at (109.33,226)
      arrow-line(73, 178, 109.33, 226)
      // (207,225) -> arrowhead at (243.33,225)
      arrow-line(207, 225, 243.33, 225)
      // (207,132) -> arrowhead at (243.33,132)
      arrow-line(207, 132, 243.33, 132)
      // (308,226) -> arrowhead at (344.29,226.29)
      arrow-line(308, 226, 344.29, 226.29)
      // (308,133) -> arrowhead at (344.29,133.29)
      arrow-line(308, 133, 344.29, 133.29)
      // (437,225) -> arrowhead at (473.33,225)
      arrow-line(437, 225, 473.33, 225)
      // (437,132) -> arrowhead at (473.33,132)
      arrow-line(437, 132, 473.33, 132)

      // Blue filled rounded rect for t=4 box
      let blue-col = rgb(74, 144, 226)
      fill(color.linear-rgb(blue-col.components().at(0), blue-col.components().at(1), blue-col.components().at(2), 33%))
      stroke(blue-col)
      rect(t(345.33, 126), t(435.33, 246), radius: 10 * s)
      fill(none)
      stroke(black)

      // Internal horizontal lines in blue box
      line(t(345.33, 160), t(435.33, 160))
      line(t(345.33, 193), t(435.33, 193))

      // Dashed gray arrow: (308,177) -> (344.29,177.29)
      let gray = rgb(128, 128, 128)
      arrow-line(308, 177, 344.29, 177.29, col: gray, dashed: true)
      // Dashed gray arrow: (160.29,154.86) -> (188.29,176)
      arrow-line(160.29, 154.86, 188.29, 176, col: gray, dashed: true)
      // Dashed gray arrow: (160.29,199.86) -> (188.29,176)
      arrow-line(160.29, 199.86, 188.29, 176, col: gray, dashed: true)

      // Dashed gray box: (190,165) -- (307,165) -- (307,189) -- (190,189) -- cycle
      stroke((paint: gray, dash: (array: (4.5pt, 4.5pt), phase: 0pt)))
      fill(none)
      rect(t(190, 165), t(307, 189))
      stroke(black)

      // Outline boxes (unfilled)
      stroke(black)
      fill(none)

      // (-15,155) -- (72,155) -- (72,200) -- (-15,200) -- cycle  [passive LPs box]
      rect(t(-15, 155), t(72, 200))
      // (110,108) -- (206,108) -- (206,153) -- (110,153) -- cycle [informed trader]
      rect(t(110, 108), t(206, 153))
      // (110,201) -- (206,201) -- (206,246) -- (110,246) -- cycle [uninformed trader]
      rect(t(110, 201), t(206, 246))
      // (244,201) -- (307,201) -- (307,246) -- (244,246) -- cycle [JIT LP deposits bottom]
      rect(t(244, 201), t(307, 246))
      // (244,108) -- (307,108) -- (307,153) -- (244,153) -- cycle [JIT LP deposits top]
      rect(t(244, 108), t(307, 153))
      // (474,108) -- (529,108) -- (529,153) -- (474,153) -- cycle [price shock]
      rect(t(474, 108), t(529, 153))
      // (474,201) -- (531,201) -- (531,246) -- (474,246) -- cycle [reverse trade]
      rect(t(474, 201), t(531, 246))

      // --- Text labels ---
      // t=1,2,3,4,5 time labels
      set-style(stroke: none, fill: none)

      content(t(25, 68), anchor: "north-west",
        $t=1$
      )
      content(t(139, 68), anchor: "north-west",
        $t=2$
      )
      content(t(257, 68), anchor: "north-west",
        $t=3$
      )
      content(t(372, 68), anchor: "north-west",
        $t=4$
      )
      content(t(483, 68), anchor: "north-west",
        $t=5$
      )

      // "passive LPs deposit" box text
      content(
        (t(-15,155).at(0) + (72-(-15))*s/2, t(-15,155).at(1) - (200-155)*s/2),
        anchor: "center",
        text(size: 8pt)[#align(center)[passive LPs \ deposit]]
      )

      // "informed trader arrives"
      content(
        (t(110,108).at(0) + (206-110)*s/2, t(110,108).at(1) - (153-108)*s/2),
        anchor: "center",
        text(size: 8pt)[#align(center)[informed \ trader arrives]]
      )

      // "uninformed trader arrives"
      content(
        (t(110,201).at(0) + (206-110)*s/2, t(110,201).at(1) - (246-201)*s/2),
        anchor: "center",
        text(size: 8pt)[#align(center)[uninformed \ trader arrives]]
      )

      // "JIT LP deposits" top-right box
      content(
        (t(244,108).at(0) + (307-244)*s/2, t(244,108).at(1) - (153-108)*s/2),
        anchor: "center",
        text(size: 8pt)[#align(center)[JIT LP \ deposits]]
      )

      // "JIT LP deposits" bottom-right box
      content(
        (t(244,201).at(0) + (307-244)*s/2, t(244,201).at(1) - (246-201)*s/2),
        anchor: "center",
        text(size: 8pt)[#align(center)[JIT LP \ deposits]]
      )

      // Blue box texts
      content(
        (t(345.33,126).at(0) + (435.33-345.33)*s/2, t(345.33,126).at(1) - (160-126)*s/2),
        anchor: "center",
        text(size: 7pt)[#align(center)[JIT LP \ deposits]]
      )

      content(
        (t(345.33,160).at(0) + (435.33-345.33)*s/2, t(345.33,160).at(1) - (193-160)*s/2),
        anchor: "center",
        text(size: 7pt)[#align(center)[swap]]
      )

      content(
        (t(345.33,193).at(0) + (435.33-345.33)*s/2, t(345.33,193).at(1) - (246-193)*s/2),
        anchor: "center",
        text(size: 7pt)[#align(center)[JIT LP \ withdraws]]
      )

      // "price shock"
      content(
        (t(474,108).at(0) + (529-474)*s/2, t(474,108).at(1) - (153-108)*s/2),
        anchor: "center",
        text(size: 8pt)[#align(center)[price \ shock]]
      )

      // "reverse trade"
      content(
        (t(474,201).at(0) + (531-474)*s/2, t(474,201).at(1) - (246-201)*s/2),
        anchor: "center",
        text(size: 8pt)[#align(center)[reverse \ trade]]
      )

      // "to public mempool" (gray dashed box label)
      content(
        (t(190,165).at(0) + (307-190)*s/2, t(190,165).at(1) - (189-165)*s/2),
        anchor: "center",
        text(size: 7pt, fill: rgb(128,128,128))[#align(center)[to public mempool]]
      )
    })
    v(0.5cm)
  }
)
