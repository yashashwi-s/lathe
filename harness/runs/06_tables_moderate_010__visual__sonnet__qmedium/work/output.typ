#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.65em)
#set heading(numbering: "1")

#align(center)[
  #text(size: 17pt, weight: "bold")[Moderate Tables]
  #v(0.4em)
  #text(size: 12pt)[Source-backed grouped table sample]
  #v(2em)
]

= Tables

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#v(1.5em)

#align(center)[
  #text(size: 10pt)[Table 1: Source table 1: 2512.03369\_table\_1]
]
#v(0.3em)

#set text(size: 7pt)
#table(
  columns: (auto, auto, 1fr, auto, auto, auto, auto, auto, auto, auto),
  align: center,
  stroke: none,
  inset: (x: 3pt, y: 2.5pt),

  table.vline(x: 1, stroke: 0.4pt),
  table.hline(stroke: 1.5pt),
  table.cell([*Dataset*]),
  table.cell([*Coverage*]),
  table.cell([*Task*]),
  table.cell([*Spa. \ Reso.*]),
  table.cell([*Temp. \ Reos.*]),
  table.cell([*Areas \ (km#super[2])*]),
  table.cell([*Period*]),
  table.cell([*Fig/Video*]),
  table.cell([*Device*]),
  table.cell([*Mod.*]),
  table.hline(stroke: 1.5pt),

  [Sim2Real-Fire~], [Worldwide], [Fire Mask Forecast \ Fire Mask Backtrack], [30 m], [1 hour], [20,000,000], [2013-2023], [Fig], [Satellite], [5],
  table.hline(stroke: 0.4pt),
  [FireSpreadTS~], [USA], [Fire Mask Forecast \ Fire Mask Backtrack], [375 m], [1 day], [9,834,000], [2018-2021], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [Mesogeos~], [Mediterranean], [Fire Mask Forecast \ Danger Forecast], [1000 m], [1 day], [9,000,999], [2006-2022], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [FireDB~], [USA], [Fire Intensity Forecast], [375 m], [1 day], [9,834,000], [2012-2017], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [Next Day fire~], [USA], [Fire Mask Forecast], [1 km], [1 day], [9,834,000], [2012-2020], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [SeasFire Cube~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2001-2017], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [CFSDS~], [Canada], [Fire Behavior], [180 m], [1 day], [9,985,000], [2002–2021], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [BA-ONFIRE~], [Worldwide], [Fire Behavior], [111 km], [1 month], [149,000,000], [1950-2021], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [GlobFire~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2001-2017], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [Re-FWI~], [Canada], [Fire Behavior], [80 km], [1 day], [9,985,000], [1980-2018], [Fig], [Satellite], [7],
  table.hline(stroke: 0.4pt),
  [GFBS~], [Worldwide], [Fire Behavior], [30 m], [16 days], [149,000,000], [2003-2016], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [FPA FOD-A~], [USA], [Fire Behavior], [4 km], [1 day], [9,834,000], [1992-2020], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [GFED5~], [Worldwide], [Fire Behavior], [500 m], [1 month], [149,000,000], [1997-2020], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [CloCAB~], [Worldwide], [Fire Behavior], [27.7 km], [1 month], [149,000,000], [2002-2020], [Fig], [Satellite], [3],
  table.hline(stroke: 0.4pt),
  [PT-FireSprd~], [Portugal], [Fire Behavior \ Fire Mask Forecast \ Danger Forecast], [4 km], [14 hours], [92,150], [2015-2021], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [NSMC-H8~], [China], [Fire Monitoring], [3 km], [1 hour], [9,597,000], [2019-2021], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [WCU-US~], [Western USA], [Danger Forecast], [250 m], [5 weeks], [4,200,000], [2005-2017], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [ECUF~], [Regions in South Korea], [Danger Forecast \ Casualty Prediction], [1 km], [1 month], [605], [2017-2021], [Fig], [Satellite], [5],
  table.hline(stroke: 0.4pt),
  [LCLQ~], [Regions in China], [Danger Forecast], [500 m], [12 hour], [16,411], [2015-2020], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [CaBuAr~], [Regions in USA], [Fire Mask Forecast], [20 m], [1 year], [450,000], [2015-2022], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [GABAM~], [Worldwide], [Fire Behavior], [30 m], [1 year], [149,000,000], [1990-2021], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [Fire Atlas~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2003-2016], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [MODIS~], [Worldwide], [Fire Mask Forecast \ Danger Forecast], [1 km], [1 day], [149,000,000], [2000-2024], [Fig], [Satellite], [3],
  table.hline(stroke: 0.4pt),
  [VIIRS~], [Worldwide], [Fire Mask Forecast \ Danger Forecast], [375 m], [12 hours], [149,000,000], [2012-2024], [Fig], [Satellite], [3],
  table.hline(stroke: 0.4pt),
  [NOAA HMS Fire~], [North America], [Danger Forecast], [2 km], [1 day], [24,710,000], [2003-2024], [Fig], [Satellite], [3],
  table.hline(stroke: 0.4pt),
  [NOAA HMS Smoke~], [North America], [Danger Forecast], [2 km], [1 day], [24,710,000], [2005-2024], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [GOES fire~], [Western Hemisphere], [Fire Mask Forecast \ Danger Forecast], [2 km], [5 mins], [61,000,000], [2017-2024], [Fig], [Satellite], [4],
  table.hline(stroke: 0.4pt),
  [NIFC WP~], [USA], [Fire Mask Forecast], [2 km], [5 mins], [9,834,000], [2000-2024], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [FRY~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2005-2011], [Fig], [Satellite], [1],
  table.hline(stroke: 0.4pt),
  [FireCanada~], [Canada], [Fire Behavior], [1 km], [1 day], [61], [2014.8], [Fig], [Satellite], [3],
  table.hline(stroke: 1.5pt),
  table.cell([*FireSentry*]), [Regions in China], [Fire Video Prediction \ Infrared Video Prediction], table.cell([*0.5 m*]), table.cell([*1 s*]), [0.7], [2025.2], table.cell([*Video*]), table.cell([*Drone*]), [4],
  table.hline(stroke: 1.5pt),
)

#set text(size: 11pt)

#pagebreak()

#v(12em)

#align(center)[
  #text(size: 10pt)[Table 2: Source table 2: 2512.01188\_table\_1]
]
#v(0.3em)

#set text(size: 10pt)
#table(
  columns: (1fr, 1fr, 1fr, 1fr, 1fr),
  align: center,
  stroke: none,
  inset: (x: 6pt, y: 5pt),

  table.hline(stroke: 0.8pt),
  [Task \ Platform],
  [Target Obs. \ Privileged Obs.],
  [Reward \ Demos],
  [Offline Steps \ Online Steps],
  [Description],
  table.hline(stroke: 0.5pt),

  [Camouflage Pick \ Sim. Koch],
  [Side Cam \ True Obj. Pos],
  [Sparse \ 100 suboptimal],
  [20K \ 80K],
  [Pick up barely \ visible object],

  table.cell(colspan: 5, inset: (y: 2pt))[],

  [Fully Obs. Pick \ Sim. xArm],
  [Side Cam \ True Obj. Pos],
  [Sparse \ 100 suboptimal],
  [20K \ 20K],
  [Pick up fully \ visible object],

  table.cell(colspan: 5, inset: (y: 2pt))[],

  [AP Koch \ Sim. Koch],
  [Wrist Cam \ True Obj. Pos],
  [Sparse \ 100 suboptimal],
  [100K \ 900K],
  [Locate then pick \ up object],

  table.cell(colspan: 5, inset: (y: 2pt))[],

  [Blind Pick \ Real Koch],
  [Joints, Init Obj. Pos \ Obj. Pos Estimate],
  [Dense \ 100 suboptimal],
  [20K \ 1.2K],
  [Pick object from \ proprioception],

  table.cell(colspan: 5, inset: (y: 2pt))[],

  [Bookshelf-P \ Real Franka],
  [Wrist Cam, Joints \ Bbox, Mask],
  [Dense \ $∼$150 suboptimal],
  [100K \ 0],
  [Look for object & \ switch to $π_0$],

  table.cell(colspan: 5, inset: (y: 2pt))[],

  [Bookshelf-D \ Real Franka],
  [Wrist Cam, Joints \ Bbox, Mask],
  [Dense \ $∼$100 suboptimal],
  [100K \ 0],
  [Look for object & \ switch to $π_0$],

  table.cell(colspan: 5, inset: (y: 2pt))[],

  [Shelf-Cabinet \ Real Franka],
  [Wrist Cam, Joints \ Bbox, Mask],
  [Dense \ $∼$30 suboptimal],
  [100K \ 0],
  [Look for object & \ switch to $π_0$],

  table.cell(colspan: 5, inset: (y: 2pt))[],

  [Complex \ Real Franka],
  [Wrist Cam, Joints \ Bbox, Mask],
  [Dense \ $∼$50 expert],
  [100K \ 0],
  [Look for object & \ switch to $π_0$],

  table.hline(stroke: 0.8pt),
)
#set text(size: 11pt)
