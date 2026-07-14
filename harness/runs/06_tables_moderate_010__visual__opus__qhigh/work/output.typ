#set page(
  paper: "us-letter",
  margin: 1in,
  numbering: "1",
  number-align: center,
)
#set text(font: ("New Computer Modern", "Latin Modern Roman"), size: 11pt)
#set par(justify: true, leading: 0.55em, first-line-indent: 0pt)

// Title
#align(center)[
  #text(size: 17.28pt)[Moderate Tables]
  #v(0.5em)
  #text(size: 12pt)[Source-backed grouped table sample]
]
#v(1em)

#text(size: 14.4pt, weight: "bold")[1#h(1em)Tables]
#v(0.3em)

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#let hd = 2pt + black
#let ln = 0.4pt + black

#v(0.8em)
#align(center)[Table 1: Source table 1: 2512.03369_table_1]
#v(0.1em)
#align(center)[
#block(width: 100%, breakable: true)[
#set text(size: 6.8pt)
#set par(leading: 0.28em)
#table(
  columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto, auto),
  align: (center + horizon, center + horizon, center + horizon, center + horizon, center + horizon, center + horizon, center + horizon, center + horizon, center + horizon, center + horizon),
  stroke: none,
  inset: (x: 3pt, y: 1.5pt),
  table.hline(stroke: hd),
  table.vline(x: 1, stroke: ln),
  [*Dataset*], [*Coverage*], [*Task*], [*Spa.\ Reso.*], [*Temp.\ Reos.*], [*Areas\ (km#super[2])*], [*Period*], [*Fig/Video*], [*Device*], [*Mod.*],
  table.hline(stroke: hd),
  [Sim2Real-Fire], [Worldwide], [Fire Mask Forecast\ Fire Mask Backtrack], [30 m], [1 hour], [20,000,000], [2013-2023], [Fig], [Satellite], [5],
  table.hline(stroke: ln),
  [FireSpreadTS], [USA], [Fire Mask Forecast\ Fire Mask Backtrack], [375 m], [1 day], [9,834,000], [2018-2021], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [Mesogeos], [Mediterranean], [Fire Mask Forecast\ Danger Forecast], [1000 m], [1 day], [9,000,999], [2006-2022], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [FireDB], [USA], [Fire Intensity Forecast], [375 m], [1 day], [9,834,000], [2012-2017], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [Next Day fire], [USA], [Fire Mask Forecast], [1 km], [1 day], [9,834,000], [2012-2020], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [SeasFire Cube], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2001-2017], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [CFSDS], [Canada], [Fire Behavior], [180 m], [1 day], [9,985,000], [2002–2021], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [BA-ONFIRE], [Worldwide], [Fire Behavior], [111 km], [1 month], [149,000,000], [1950-2021], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [GlobFire], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2001-2017], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [Re-FWI], [Canada], [Fire Behavior], [80 km], [1 day], [9,985,000], [1980-2018], [Fig], [Satellite], [7],
  table.hline(stroke: ln),
  [GFBS], [Worldwide], [Fire Behavior], [30 m], [16 days], [149,000,000], [2003-2016], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [FPA FOD-A], [USA], [Fire Behavior], [4 km], [1 day], [9,834,000], [1992-2020], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [GFED5], [Worldwide], [Fire Behavior], [500 m], [1 month], [149,000,000], [1997-2020], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [CloCAB], [Worldwide], [Fire Behavior], [27.7 km], [1 month], [149,000,000], [2002-2020], [Fig], [Satellite], [3],
  table.hline(stroke: ln),
  [PT-FireSprd], [Portugal], [Fire Behavior\ Fire Mask Forecast\ Danger Forecast], [4 km], [14 hours], [92,150], [2015-2021], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [NSMC-H8], [China], [Fire Monitoring], [3 km], [1 hour], [9,597,000], [2019-2021], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [WCU-US], [Western USA], [Danger Forecast], [250 m], [5 weeks], [4,200,000], [2005-2017], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [ECUF], [Regions in South Korea], [Danger Forecast\ Casualty Prediction], [1 km], [1 month], [605], [2017-2021], [Fig], [Satellite], [5],
  table.hline(stroke: ln),
  [LCLQ], [Regions in China], [Danger Forecast], [500 m], [12 hour], [16,411], [2015-2020], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [CaBuAr], [Regions in USA], [Fire Mask Forecast], [20 m], [1 year], [450,000], [2015-2022], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [GABAM], [Worldwide], [Fire Behavior], [30 m], [1 year], [149,000,000], [1990-2021], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [Fire Atlas], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2003-2016], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [MODIS], [Worldwide], [Fire Mask Forecast\ Danger Forecast], [1 km], [1 day], [149,000,000], [2000-2024], [Fig], [Satellite], [3],
  table.hline(stroke: ln),
  [VIIRS], [Worldwide], [Fire Mask Forecast\ Danger Forecast], [375 m], [12 hours], [149,000,000], [2012-2024], [Fig], [Satellite], [3],
  table.hline(stroke: ln),
  [NOAA HMS Fire], [North America], [Danger Forecast], [2 km], [1 day], [24,710,000], [2003-2024], [Fig], [Satellite], [3],
  table.hline(stroke: ln),
  [NOAA HMS Smoke], [North America], [Danger Forecast], [2 km], [1 day], [24,710,000], [2005-2024], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [GOES fire], [Western Hemisphere], [Fire Mask Forecast\ Danger Forecast], [2 km], [5 mins], [61,000,000], [2017-2024], [Fig], [Satellite], [4],
  table.hline(stroke: ln),
  [NIFC WP], [USA], [Fire Mask Forecast], [2 km], [5 mins], [9,834,000], [2000-2024], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [FRY], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2005-2011], [Fig], [Satellite], [1],
  table.hline(stroke: ln),
  [FireCanada], [Canada], [Fire Behavior], [1 km], [1 day], [61], [2014.8], [Fig], [Satellite], [3],
  table.hline(stroke: hd),
  [*FireSentry*], [Regions in China], [Fire Video Prediction\ Infrared Video Prediction], [*0.5 m*], [*1 s*], [0.7], [2025.2], [*Video*], [*Drone*], [4],
  table.hline(stroke: hd),
)
]
]

#pagebreak()

#v(3in)

#align(center)[Table 2: Source table 2: 2512.01188_table_1]
#v(0.2em)

#block(width: 100%)[
#set text(size: 11pt)
#set par(leading: 0.5em)
#table(
  columns: (1.4fr, 1.6fr, 1.5fr, 1.3fr, 1.3fr),
  align: (center + horizon, center + horizon, center + horizon, center + horizon, center + horizon),
  stroke: none,
  row-gutter: 6pt,
  inset: (x: 4pt, y: 3pt),
  table.hline(stroke: 0.6pt),
  [Task\ Platform], [Target Obs.\ Privileged Obs.], [Reward\ Demos], [Offline Steps\ Online Steps], [Description],
  table.hline(stroke: 0.4pt),
  [Camouflage Pick\ Sim. Koch], [Side Cam\ True Obj. Pos], [Sparse\ 100 suboptimal], [20K\ 80K], [Pick up barely\ visible object],
  [Fully Obs. Pick\ Sim. xArm], [Side Cam\ True Obj. Pos], [Sparse\ 100 suboptimal], [20K\ 20K], [Pick up fully\ visible object],
  [AP Koch\ Sim. Koch], [Wrist Cam\ True Obj. Pos], [Sparse\ 100 suboptimal], [100K\ 900K], [Locate then pick\ up object],
  [Blind Pick\ Real Koch], [Joints, Init Obj. Pos\ Obj. Pos Estimate], [Dense\ 100 suboptimal], [20K\ 1.2K], [Pick object from\ proprioception],
  [Bookshelf-P\ Real Franka], [Wrist Cam, Joints\ Bbox, Mask], [Dense\ $tilde.op 150$ suboptimal], [100K\ 0], [Look for object &\ switch to $pi_0$],
  [Bookshelf-D\ Real Franka], [Wrist Cam, Joints\ Bbox, Mask], [Dense\ $tilde.op 100$ suboptimal], [100K\ 0], [Look for object &\ switch to $pi_0$],
  [Shelf-Cabinet\ Real Franka], [Wrist Cam, Joints\ Bbox, Mask], [Dense\ $tilde.op 30$ suboptimal], [100K\ 0], [Look for object &\ switch to $pi_0$],
  [Complex\ Real Franka], [Wrist Cam, Joints\ Bbox, Mask], [Dense\ $tilde.op 50$ expert], [100K\ 0], [Look for object &\ switch to $pi_0$],
  table.hline(stroke: 0.6pt),
)
]
