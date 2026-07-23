#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)

#align(center)[
  #text(size: 1.44em, weight: "bold")[Table Sample 7] \
  #text(size: 1.2em)[Dataset-expansion sample] \
  #v(1em)
]

#section[Results]
The table below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#figure(
  caption: [
    #text(size: 0.85em)[Timing results for option pricing.]
  ],
  placement: bottom,
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto, auto),
    stroke: none,
    inset: (x: 2pt, y: 4pt),
    align: center + horizon,
    
    table.hline(y: 0, stroke: 0.8pt),
    table.hline(y: 1, stroke: 0.8pt),
    
    [], colspan(3)[Fx Asian call (Set I)], [], colspan(3)[Fx Asian put (Set II)], [], colspan(3)[Fx-Fl Asian call (Set III)],
    
    [], [$N_("paths")$], [time], [speed-up], [], [$N_("paths")$], [time], [speed-up], [], [$N_("paths")$], [time], [speed-up],
    
    table.hline(y: 2, start: 1, end: 3),
    table.hline(y: 2, start: 5, end: 7),
    table.hline(y: 2, start: 9, end: 11),
    
    [MC], [$10^5$], [1951 ms], [-], [MC], [$10^5$], [3134 ms], [-], [MC], [$10^5$], [1996 ms], [-],
    [SC], [$10^5$], [24 ms], [81], [SC], [$10^5$], [29 ms], [107], [SC], [$10^5$], [69 ms], [29],
    [SA], [-], [15 ms], [130], [SA], [-], [16 ms], [196], [-], [-], [-], [-],
    
    table.hline(y: 6, start: 1, end: 3),
    table.hline(y: 6, start: 5, end: 7),
    table.hline(y: 6, start: 9, end: 11),
    
    [MC], [$2 times 10^5$], [3905 ms], [-], [MC], [$2 times 10^5$], [6386 ms], [-], [MC], [$5 times 10^4$], [953 ms], [-],
    [SC], [$2 times 10^5$], [58 ms], [68], [SC], [$2 times 10^5$], [55 ms], [116], [SC], [$5 times 10^4$], [43 ms], [22],
    [SA], [-], [15 ms], [263], [SA], [-], [15 ms], [440], [-], [-], [-], [-],
  )
)
