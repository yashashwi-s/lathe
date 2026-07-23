#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt)
#import "@preview/cetz:0.3.1": canvas, draw

#align(center)[
  #text(size: 2em, weight: "bold")[Plot Sample 3] \
  Dataset-expansion sample
]

= Visualization
The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  canvas({
    import draw: *
    set-style(stroke: 1.5pt)
    let red-color = rgb(182, 5, 60)
    let blue-color = rgb(6, 79, 97)
    let dark-red = rgb(108, 4, 35)

    line((52.05, 101.79), (72.55, 101.79))
    line((72.55, 101.79), (92.38, 72.25))
    line((72.55, 101.79), (90.72, 129.04), stroke: red-color)
    line((90.72, 129.04), (92.38, 131.54), stroke: red-color)
    line((112.9, 101.79), (94.09, 129.07), stroke: red-color)
    line((94.09, 129.07), (92.38, 131.54), stroke: red-color)
    line((112.9, 101.79), (134.4, 101.79))
    line((92.38, 131.54), (92.38, 150.45))
    line((92.38, 72.25), (112.9, 101.79))
    line((92.38, 52.84), (92.38, 72.25))
    line((104.28, 162.26), (92.38, 150.45))
    line((81.28, 163.26), (92.38, 150.45))

    line((216.85, 101.79), (237.35, 101.79))
    line((237.35, 101.79), (257.18, 72.25))
    line((237.35, 101.79), (255.52, 129.04), stroke: red-color)
    line((255.52, 129.04), (257.18, 131.54), stroke: red-color)
    line((277.7, 101.79), (258.88, 129.07), stroke: red-color)
    line((258.88, 129.07), (257.18, 131.54), stroke: red-color)
    line((277.7, 101.79), (299.2, 101.79))
    line((257.18, 131.54), (257.18, 150.45))
    line((257.18, 72.25), (277.7, 101.79))
    line((257.18, 52.84), (257.18, 72.25))
    line((245.37, 40.94), (257.18, 52.84))
    line((268.38, 40.11), (257.18, 52.84))
    line((269.08, 162.26), (257.18, 150.45))
    line((246.08, 163.26), (257.18, 150.45))
    line((40.24, 113.69), (52.05, 101.79))
    line((39.24, 90.69), (52.05, 101.79))

    content((301.86, 94.01), text(fill: blue-color)[$d$])
    content((201.04, 94.61), text(fill: blue-color)[$b$])
    content((244.74, 104.01), text(fill: red-color, size: 0.8em)[$\gamma$])
    content((55.05, 86.24), [$\ell_2$])
    content((229.79, 77.79), [$x_1$])
    content((268.79, 77.79), [$x_2$])
    content((232.83, 24.4), text(fill: blue-color)[$c_1$])
    content((264.5, 24.4), text(fill: blue-color)[$c_2$])
    content((136.63, 94.31), text(fill: blue-color)[$d$])
    content((69.38, 163.46), text(fill: blue-color)[$a_1$])
    content((88.18, 35.6), text(fill: blue-color)[$c$])
    content((79.5, 104.01), text(fill: red-color, size: 0.8em)[$\gamma$])
    content((64.45, 110.51), text(fill: dark-red, size: 0.8em)[$h_1$])
    content((94.38, 134.94), [$\ell_1$])
    content((68.05, 75.79), [$x_1$])
    content((102.98, 163.46), text(fill: blue-color)[$a_2$])
    content((101.38, 75.79), [$x_2$])
    content((106.05, 110.51), text(fill: dark-red, size: 0.8em)[$h_2$])
    content((232.38, 163.46), text(fill: blue-color)[$a_1$])
    content((265.98, 163.46), text(fill: blue-color)[$a_2$])
    content((21.29, 78), text(fill: blue-color)[$b_2$])
    content((21.29, 105.61), text(fill: blue-color)[$b_1$])
    content((229.45, 110.51), text(fill: dark-red, size: 0.8em)[$h_1$])
    content((272.05, 110.51), text(fill: dark-red, size: 0.8em)[$h_2$])
    content((259.18, 134.94), [$\ell_1$])
    content((259.18, 56.24), [$\ell_2$])
  }),
  caption: [Source-backed plot.]
)
