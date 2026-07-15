#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)

#align(center)[
  #text(size: 17pt, weight: "bold")[Table Sample 7]
  #v(0.5em)
  #text(size: 12pt)[Dataset-expansion sample]
  #v(1.5em)
]

= Results

The table below is drawn from a source-backed image-to-LaTeX benchmark and reproduced verbatim.

#v(1fr)

#figure(
  caption: text(size: 8pt)[Timing results for option pricing.],
  placement: bottom,
  {
    v(-0.2cm)
    set text(size: 7.5pt)
    
    let hline = table.hline
    let vline = table.vline
    
    table(
      columns: (auto, auto, auto, auto, 0.3em, auto, auto, auto, 0.3em, auto, auto, auto),
      stroke: none,
      inset: (x: 4pt, y: 3pt),
      
      // Top double hline
      table.hline(stroke: (thickness: 1.2pt)),
      table.hline(stroke: (thickness: 0.4pt), y: 1),
      
      // Header row 1
      table.cell(align: center)[],
      table.cell(colspan: 3, align: center)[Fx Asian call (Set I)],
      table.cell(align: center)[],
      table.cell(colspan: 3, align: center)[Fx Asian put (Set II)],
      table.cell(align: center)[],
      table.cell(colspan: 3, align: center)[Fx-Fl Asian call (Set III)],
      
      // cline 1-12 (full line after header row 1)
      table.hline(stroke: 0.4pt),
      
      // Header row 2
      table.cell(align: center)[],
      table.cell(align: center)[$N_mono("paths")$],
      table.cell(align: center)[time],
      table.cell(align: center)[speed-up],
      table.cell(align: center)[],
      table.cell(align: center)[$N_mono("paths")$],
      table.cell(align: center)[time],
      table.cell(align: center)[speed-up],
      table.cell(align: center)[],
      table.cell(align: center)[$N_mono("paths")$],
      table.cell(align: center)[time],
      table.cell(align: center)[speed-up],
      
      // cline 2-4, 6-8, 10-12
      table.hline(stroke: 0.4pt, start: 1, end: 4),
      table.hline(stroke: 0.4pt, start: 5, end: 8),
      table.hline(stroke: 0.4pt, start: 9, end: 12),
      
      // Data rows group 1
      table.cell(align: center, stroke: (right: 0.4pt))[MC],
      table.cell(align: center)[$10^5$],
      table.cell(align: center)[1951 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[-],
      table.cell(align: center, stroke: (right: 0.4pt))[MC],
      table.cell(align: center)[$10^5$],
      table.cell(align: center)[3134 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[-],
      table.cell(align: center, stroke: (right: 0.4pt))[MC],
      table.cell(align: center)[$10^5$],
      table.cell(align: center)[1996 ms],
      table.cell(align: center)[-],
      
      table.cell(align: center, stroke: (right: 0.4pt))[SC],
      table.cell(align: center)[$10^5$],
      table.cell(align: center)[24 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[81],
      table.cell(align: center, stroke: (right: 0.4pt))[SC],
      table.cell(align: center)[$10^5$],
      table.cell(align: center)[29 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[107],
      table.cell(align: center, stroke: (right: 0.4pt))[SC],
      table.cell(align: center)[$10^5$],
      table.cell(align: center)[69 ms],
      table.cell(align: center)[29],
      
      table.cell(align: center, stroke: (right: 0.4pt))[SA],
      table.cell(align: center)[-],
      table.cell(align: center)[15 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[130],
      table.cell(align: center, stroke: (right: 0.4pt))[SA],
      table.cell(align: center)[-],
      table.cell(align: center)[16 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[196],
      table.cell(align: center, stroke: (right: 0.4pt))[-],
      table.cell(align: center)[-],
      table.cell(align: center)[-],
      table.cell(align: center)[-],
      
      // cline 2-4, 6-8, 10-12
      table.hline(stroke: 0.4pt, start: 1, end: 4),
      table.hline(stroke: 0.4pt, start: 5, end: 8),
      table.hline(stroke: 0.4pt, start: 9, end: 12),
      
      // Data rows group 2
      table.cell(align: center, stroke: (right: 0.4pt))[MC],
      table.cell(align: center)[$2 times 10^5$],
      table.cell(align: center)[3905 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[-],
      table.cell(align: center, stroke: (right: 0.4pt))[MC],
      table.cell(align: center)[$2 times 10^5$],
      table.cell(align: center)[6386 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[-],
      table.cell(align: center, stroke: (right: 0.4pt))[MC],
      table.cell(align: center)[$5 times 10^4$],
      table.cell(align: center)[953 ms],
      table.cell(align: center)[-],
      
      table.cell(align: center, stroke: (right: 0.4pt))[SC],
      table.cell(align: center)[$2 times 10^5$],
      table.cell(align: center)[58 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[68],
      table.cell(align: center, stroke: (right: 0.4pt))[SC],
      table.cell(align: center)[$2 times 10^5$],
      table.cell(align: center)[55 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[116],
      table.cell(align: center, stroke: (right: 0.4pt))[SC],
      table.cell(align: center)[$5 times 10^4$],
      table.cell(align: center)[43 ms],
      table.cell(align: center)[22],
      
      table.cell(align: center, stroke: (right: 0.4pt))[SA],
      table.cell(align: center)[-],
      table.cell(align: center)[15 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[263],
      table.cell(align: center, stroke: (right: 0.4pt))[SA],
      table.cell(align: center)[-],
      table.cell(align: center)[15 ms],
      table.cell(align: center, stroke: (right: 0.4pt))[440],
      table.cell(align: center, stroke: (right: 0.4pt))[-],
      table.cell(align: center)[-],
      table.cell(align: center)[-],
      table.cell(align: center)[-],
    )
  }
)
