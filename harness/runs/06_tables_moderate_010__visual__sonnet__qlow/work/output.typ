#set page(paper: "us-letter", margin: 1in)
#set text(size: 11pt, font: "New Computer Modern")
#set par(leading: 0.65em)
#show figure.where(kind: table): set figure.caption(position: top)

#align(center)[
  #text(size: 17pt, weight: "bold")[Moderate Tables]
  #v(0.5em)
  #text(size: 14pt)[Source-backed grouped table sample]
  #v(1.5em)
]

= Tables

These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#v(0.5em)

#figure(
  caption: [Source table 1: 2512.03369\_table\_1],
  kind: table,
  {
    set text(size: 5pt)
    table(
      columns: (1.3fr, 2.3fr, 1.7fr, 0.8fr, 0.8fr, 1.1fr, 0.9fr, 0.9fr, 0.9fr, 0.4fr),
      align: center,
      inset: (x: 2pt, y: 2pt),
      stroke: (x, y) => {
        let vline = if x == 1 { (left: 0.4pt) } else { (:) }
        let hline = if y == 0 { (top: 0.8pt, bottom: 0.8pt) }
          else if y == 1 { (bottom: 0.8pt) }
          else if y == 32 { (bottom: 0.8pt) }
          else { (bottom: 0.4pt) }
        vline + hline
      },
      table.header(
        [*Dataset*], [*Coverage*], [*Task*], [*Spa. \ Reso.*], [*Temp. \ Reos.*], [*Areas \ (km#super[2])*], [*Period*], [*Fig/Video*], [*Device*], [*Mod.*],
      ),
      [Sim2Real-Fire~], [Worldwide], [Fire Mask Forecast \ Fire Mask Backtrack], [30 m], [1 hour], [20,000,000], [2013-2023], [Fig], [Satellite], [5],
      [FireSpreadTS~], [USA], [Fire Mask Forecast \ Fire Mask Backtrack], [375 m], [1 day], [9,834,000], [2018-2021], [Fig], [Satellite], [4],
      [Mesogeos~], [Mediterranean], [Fire Mask Forecast \ Danger Forecast], [1000 m], [1 day], [9,000,999], [2006-2022], [Fig], [Satellite], [4],
      [FireDB~], [USA], [Fire Intensity Forecast], [375 m], [1 day], [9,834,000], [2012-2017], [Fig], [Satellite], [4],
      [Next Day fire~], [USA], [Fire Mask Forecast], [1 km], [1 day], [9,834,000], [2012-2020], [Fig], [Satellite], [4],
      [SeasFire Cube~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2001-2017], [Fig], [Satellite], [4],
      [CFSDS~], [Canada], [Fire Behavior], [180 m], [1 day], [9,985,000], [2002–2021], [Fig], [Satellite], [4],
      [BA-ONFIRE~], [Worldwide], [Fire Behavior], [111 km], [1 month], [149,000,000], [1950-2021], [Fig], [Satellite], [1],
      [GlobFire~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2001-2017], [Fig], [Satellite], [1],
      [Re-FWI~], [Canada], [Fire Behavior], [80 km], [1 day], [9,985,000], [1980-2018], [Fig], [Satellite], [7],
      [GFBS~], [Worldwide], [Fire Behavior], [30 m], [16 days], [149,000,000], [2003-2016], [Fig], [Satellite], [1],
      [FPA FOD-A~], [USA], [Fire Behavior], [4 km], [1 day], [9,834,000], [1992-2020], [Fig], [Satellite], [4],
      [GFED5~], [Worldwide], [Fire Behavior], [500 m], [1 month], [149,000,000], [1997-2020], [Fig], [Satellite], [1],
      [CloCAB~], [Worldwide], [Fire Behavior], [27.7 km], [1 month], [149,000,000], [2002-2020], [Fig], [Satellite], [3],
      [PT-FireSprd~], [Portugal], [Fire Behavior \ Fire Mask Forecast \ Danger Forecast], [4 km], [14 hours], [92,150], [2015-2021], [Fig], [Satellite], [1],
      [NSMC-H8~], [China], [Fire Monitoring], [3 km], [1 hour], [9,597,000], [2019-2021], [Fig], [Satellite], [1],
      [WCU-US~], [Western USA], [Danger Forecast], [250 m], [5 weeks], [4,200,000], [2005-2017], [Fig], [Satellite], [1],
      [ECUF~], [Regions in South Korea], [Danger Forecast \ Casualty Prediction], [1 km], [1 month], [605], [2017-2021], [Fig], [Satellite], [5],
      [LCLQ~], [Regions in China], [Danger Forecast], [500 m], [12 hour], [16,411], [2015-2020], [Fig], [Satellite], [4],
      [CaBuAr~], [Regions in USA], [Fire Mask Forecast], [20 m], [1 year], [450,000], [2015-2022], [Fig], [Satellite], [1],
      [GABAM~], [Worldwide], [Fire Behavior], [30 m], [1 year], [149,000,000], [1990-2021], [Fig], [Satellite], [1],
      [Fire Atlas~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2003-2016], [Fig], [Satellite], [1],
      [MODIS~], [Worldwide], [Fire Mask Forecast \ Danger Forecast], [1 km], [1 day], [149,000,000], [2000-2024], [Fig], [Satellite], [3],
      [VIIRS~], [Worldwide], [Fire Mask Forecast \ Danger Forecast], [375 m], [12 hours], [149,000,000], [2012-2024], [Fig], [Satellite], [3],
      [NOAA HMS Fire~], [North America], [Danger Forecast], [2 km], [1 day], [24,710,000], [2003-2024], [Fig], [Satellite], [3],
      [NOAA HMS Smoke~], [North America], [Danger Forecast], [2 km], [1 day], [24,710,000], [2005-2024], [Fig], [Satellite], [1],
      [GOES fire~], [Western Hemisphere], [Fire Mask Forecast \ Danger Forecast], [2 km], [5 mins], [61,000,000], [2017-2024], [Fig], [Satellite], [4],
      [NIFC WP~], [USA], [Fire Mask Forecast], [2 km], [5 mins], [9,834,000], [2000-2024], [Fig], [Satellite], [1],
      [FRY~], [Worldwide], [Fire Behavior], [500 m], [1 day], [149,000,000], [2005-2011], [Fig], [Satellite], [1],
      [FireCanada~], [Canada], [Fire Behavior], [1 km], [1 day], [61], [2014.8], [Fig], [Satellite], [3],
      [*FireSentry*], [Regions in China], [Fire Video Prediction \ Infrared Video Prediction], [*0.5 m*], [*1 s*], [0.7], [2025.2], [*Video*], [*Drone*], [4],
    )
  }
)

#pagebreak()
#v(1.5in)

#figure(
  caption: [Source table 2: 2512.01188\_table\_1],
  kind: table,
  {
    set text(size: 10pt)
    table(
      columns: (1fr, 1fr, 1fr, 1fr, 1fr),
      align: center,
      stroke: none,
      inset: (x: 6pt, y: 5pt),
      table.hline(stroke: 0.8pt),
      table.header(
        [Task \ Platform],
        [Target Obs. \ Privileged Obs.],
        [Reward \ Demos],
        [Offline Steps \ Online Steps],
        [Description],
      ),
      table.hline(stroke: 0.5pt),
      table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Camouflage Pick \ Sim. Koch], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Side Cam \ True Obj. Pos], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Sparse \ 100 suboptimal], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[20K \ 80K], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Pick up barely \ visible object],
      table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Fully Obs. Pick \ Sim. xArm], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Side Cam \ True Obj. Pos], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Sparse \ 100 suboptimal], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[20K \ 20K], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Pick up fully \ visible object],
      table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[AP Koch \ Sim. Koch], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Wrist Cam \ True Obj. Pos], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Sparse \ 100 suboptimal], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[100K \ 900K], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Locate then pick \ up object],
      table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Blind Pick \ Real Koch], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Joints, Init Obj. Pos \ Obj. Pos Estimate], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Dense \ 100 suboptimal], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[20K \ 1.2K], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Pick object from \ proprioception],
      table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Bookshelf-P \ Real Franka], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Wrist Cam, Joints \ Bbox, Mask], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Dense \ ~150 suboptimal], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[100K \ 0], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Look for object & \ switch to $pi_0$],
      table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Bookshelf-D \ Real Franka], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Wrist Cam, Joints \ Bbox, Mask], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Dense \ ~100 suboptimal], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[100K \ 0], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Look for object & \ switch to $pi_0$],
      table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Shelf-Cabinet \ Real Franka], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Wrist Cam, Joints \ Bbox, Mask], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Dense \ ~30 suboptimal], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[100K \ 0], table.cell(inset: (x: 6pt, top: 5pt, bottom: 8pt))[Look for object & \ switch to $pi_0$],
      [Complex \ Real Franka], [Wrist Cam, Joints \ Bbox, Mask], [Dense \ ~50 expert], [100K \ 0], [Look for object & \ switch to $pi_0$],
      table.hline(stroke: 0.8pt),
    )
  }
)
