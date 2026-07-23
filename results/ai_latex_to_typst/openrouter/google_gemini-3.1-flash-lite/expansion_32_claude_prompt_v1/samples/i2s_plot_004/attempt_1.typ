#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt)

#align(center)[
  #text(size: 1.44em, weight: "bold")[Plot Sample 4] \
  Dataset-expansion sample
]

#section("Visualization")
The figure below is a TikZ/pgfplots drawing drawn from a source-backed image-to-LaTeX benchmark.

#figure(
  canvas(length: 0.75pt, {
    import draw: *
    
    // Helper for arrowheads
    let arrow_head = (fill: black) => {
      polygon((8.93, -4.29), (0, 0), (8.93, 4.29), fill: fill, stroke: none)
    }

    // Drawing lines
    line((73, 178), (107.5, 133.37), mark: (end: arrow_head()))
    line((73, 178), (107.52, 223.61), mark: (end: arrow_head()))
    line((207, 225), (240.33, 225), mark: (end: arrow_head()))
    line((207, 132), (240.33, 132), mark: (end: arrow_head()))
    
    // Blue box
    rect((345.33, 108), (435.33, 246), radius: 10pt, fill: rgb(74, 144, 226, 84))
    
    line((308, 226), (341.29, 226.26), mark: (end: arrow_head()))
    line((308, 133), (341.29, 133.26), mark: (end: arrow_head()))
    line((345.33, 160), (435.33, 160))
    line((345.33, 193), (435.33, 193))
    line((437, 225), (470.33, 225), mark: (end: arrow_head()))
    line((437, 132), (470.33, 132), mark: (end: arrow_head()))
    
    // Dashed lines
    let gray = rgb(128, 128, 128)
    line((308, 177), (341.29, 177.26), stroke: (dash: "dashed", paint: gray), mark: (end: arrow_head(fill: gray)))
    line((160.29, 154.86), (185.89, 174.19), stroke: (dash: "dashed", paint: gray), mark: (end: arrow_head(fill: gray)))
    line((160.29, 199.86), (186, 177.95), stroke: (dash: "dashed", paint: gray), mark: (end: arrow_head(fill: gray)))
    rect((190, 165), (307, 189), stroke: (dash: "dashed", paint: gray))

    // Text nodes
    content((25, 68), $t=1$)
    rect((-15, 155), (72, 200))
    content((38.5, 177.5), align(center)[passive LPs\ndeposit])
    
    rect((110, 108), (206, 153))
    content((158, 130.5), align(center)[informed\ntrader arrives])
    
    rect((110, 201), (206, 246))
    content((158, 223.5), align(center)[uninformed\ntrader arrives])
    
    rect((244, 201), (307, 246))
    content((275.5, 223.5), align(center)[JIT LP\ndeposits])
    
    content((390.33, 126), align(center)[#text(size: 0.8em)[JIT LP\ndeposits]])
    content((382.5, 224), align(center)[#text(size: 0.8em)[JIT LP\nwithdraws]])
    content((390.5, 176.5), align(center)[swap])
    
    rect((244, 108), (307, 153))
    content((275.5, 130.5), align(center)[JIT LP\ndeposits])
    
    rect((474, 108), (529, 153))
    content((501.5, 130.5), align(center)[price\nshock])
    
    rect((474, 201), (531, 246))
    content((502.5, 223.5), align(center)[reverse\ntrade])
    
    content((139, 68), $t=2$)
    content((257, 68), $t=3$)
    content((372, 68), $t=4$)
    content((483, 68), $t=5$)
    content((248.5, 177), align(center)[#text(size: 0.8em, fill: gray)[to public mempool]])
  }),
  caption: [Source-backed plot.]
)
