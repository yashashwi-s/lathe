#set page(paper: "us-letter", margin: 1in)
#set text(font: "Linux Libertine", size: 11pt)

#align(center, [
  #text(size: 1.5em, weight: "bold")[Moderate Tables] \
  Source-backed grouped table sample
])

= Tables
These tables are grouped from source-backed LaTeX table data and compiled as a single benchmark data point.

#figure(
  caption: [Source table 1: 2512.03369_table_1],
  table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto, auto, auto),
    stroke: (x, y) => (
      top: if y <= 1 { 1.5pt } else { 0.5pt },
      bottom: if y == 31 { 1.5pt } else if y == 30 { 1.5pt } else { 0pt },
    ),
    align: center + horizon,
    [*Dataset*], [*Coverage*], [*Task*], [*Spa. \ Reso.*], [*Temp. \ Reos.*], [*Areas \ (km$^2$)*], [*Period*], [*Fig/Video*], [*Device*], [*Mod.*],
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
    [*FireSentry*], [Regions in China], [Fire Video Prediction \ Infrared Video Prediction], [*0.5 m*], [*1 s*], [0.7], [2025.2], [*Video*], [*Drone*], [4]
  )
)

#figure(
  caption: [Source table 2: 2512.01188_table_1],
  table(
    columns: (auto, auto, auto, auto, auto),
    stroke: (x, y) => (
      top: if y == 0 or y == 1 { 1pt } else { 0pt },
      bottom: if y == 0 { 1pt } else if y == 9 { 1pt } else { 0pt },
    ),
    align: left + horizon,
    [Task \ Platform], [Target Obs. \ Privileged Obs.], [Reward \ Demos], [Offline Steps \ Online Steps], [Description],
    [Camouflage Pick \ Sim. Koch], [Side Cam \ True Obj. Pos], [Sparse \ 100 suboptimal], [20K \ 80K], [Pick up barely \ visible object],
    [Fully Obs. Pick \ Sim. xArm], [Side Cam \ True Obj. Pos], [Sparse \ 100 suboptimal], [20K \ 20K], [Pick up fully \ visible object],
    [AP Koch \ Sim. Koch], [Wrist Cam \ True Obj. Pos], [Sparse \ 100 suboptimal], [100K \ 900K], [Locate then pick \ up object],
    [Blind Pick \ Real Koch], [Joints, Init Obj. Pos \ Obj. Pos Estimate], [Dense \ 100 suboptimal], [20K \ 1.2K], [Pick object from \ proprioception],
    [Bookshelf-P \ Real Franka], [Wrist Cam, Joints \ Bbox, Mask], [Dense \ $\sim$150 suboptimal], [100K \ 0], [Look for object \& \ switch to $\pi_0$],
    [Bookshelf-D \ Real Franka], [Wrist Cam, Joints \ Bbox, Mask], [Dense \ $\sim$100 suboptimal], [100K \ 0], [Look for object \& \ switch to $\pi_0$],
    [Shelf-Cabinet \ Real Franka], [Wrist Cam, Joints \ Bbox, Mask], [Dense \ $\sim$30 suboptimal], [100K \ 0], [Look for object \& \ switch to $\pi_0$],
    [Complex \ Real Franka], [Wrist Cam, Joints \ Bbox, Mask], [Dense \ $\sim$50 expert], [100K \ 0], [Look for object \& \ switch to $\pi_0$]
  )
)
